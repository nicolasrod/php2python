#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import cgi
    import os
    import os.path
    import copy
    import sys
    from goto import with_goto
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
#// 
#// SimplePie
#// 
#// A PHP-Based RSS and Atom Feed Framework.
#// Takes the hard work out of managing a complete RSS/Atom solution.
#// 
#// Copyright (c) 2004-2012, Ryan Parman, Geoffrey Sneddon, Ryan McCue, and contributors
#// All rights reserved.
#// 
#// Redistribution and use in source and binary forms, with or without modification, are
#// permitted provided that the following conditions are met:
#// 
#// Redistributions of source code must retain the above copyright notice, this list of
#// conditions and the following disclaimer.
#// 
#// Redistributions in binary form must reproduce the above copyright notice, this list
#// of conditions and the following disclaimer in the documentation and/or other materials
#// provided with the distribution.
#// 
#// Neither the name of the SimplePie Team nor the names of its contributors may be used
#// to endorse or promote products derived from this software without specific prior
#// written permission.
#// 
#// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS
#// OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
#// AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS
#// AND CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#// CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#// SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
#// OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#// POSSIBILITY OF SUCH DAMAGE.
#// 
#// @package SimplePie
#// @version 1.3.1
#// @copyright 2004-2012 Ryan Parman, Geoffrey Sneddon, Ryan McCue
#// @author Ryan Parman
#// @author Geoffrey Sneddon
#// @author Ryan McCue
#// @link http://simplepie.org/ SimplePie
#// @license http://www.opensource.org/licenses/bsd-license.php BSD License
#// 
#// 
#// Used for fetching remote files and reading local files
#// 
#// Supports HTTP 1.0 via cURL or fsockopen, with spotty HTTP 1.1 support
#// 
#// This class can be overloaded with {@see SimplePie::set_file_class()}
#// 
#// @package SimplePie
#// @subpackage HTTP
#// @todo Move to properly supporting RFC2616 (HTTP/1.1)
#//
class SimplePie_File():
    url = Array()
    useragent = Array()
    success = True
    headers = Array()
    body = Array()
    status_code = Array()
    redirects = 0
    error = Array()
    method = SIMPLEPIE_FILE_SOURCE_NONE
    def __init__(self, url=None, timeout=10, redirects=5, headers=None, useragent=None, force_fsockopen=False):
        
        if php_class_exists("idna_convert"):
            idn = php_new_class("idna_convert", lambda : idna_convert())
            parsed = SimplePie_Misc.parse_url(url)
            url = SimplePie_Misc.compress_parse_url(parsed["scheme"], idn.encode(parsed["authority"]), parsed["path"], parsed["query"], parsed["fragment"])
        # end if
        self.url = url
        self.useragent = useragent
        if php_preg_match("/^http(s)?:\\/\\//i", url):
            if useragent == None:
                useragent = php_ini_get("user_agent")
                self.useragent = useragent
            # end if
            if (not php_is_array(headers)):
                headers = Array()
            # end if
            if (not force_fsockopen) and php_function_exists("curl_exec"):
                self.method = SIMPLEPIE_FILE_SOURCE_REMOTE | SIMPLEPIE_FILE_SOURCE_CURL
                fp = curl_init()
                headers2 = Array()
                for key,value in headers:
                    headers2[-1] = str(key) + str(": ") + str(value)
                # end for
                if php_version_compare(SimplePie_Misc.get_curl_version(), "7.10.5", ">="):
                    curl_setopt(fp, CURLOPT_ENCODING, "")
                # end if
                curl_setopt(fp, CURLOPT_URL, url)
                curl_setopt(fp, CURLOPT_HEADER, 1)
                curl_setopt(fp, CURLOPT_RETURNTRANSFER, 1)
                curl_setopt(fp, CURLOPT_TIMEOUT, timeout)
                curl_setopt(fp, CURLOPT_CONNECTTIMEOUT, timeout)
                curl_setopt(fp, CURLOPT_REFERER, url)
                curl_setopt(fp, CURLOPT_USERAGENT, useragent)
                curl_setopt(fp, CURLOPT_HTTPHEADER, headers2)
                if (not php_ini_get("open_basedir")) and (not php_ini_get("safe_mode")) and php_version_compare(SimplePie_Misc.get_curl_version(), "7.15.2", ">="):
                    curl_setopt(fp, CURLOPT_FOLLOWLOCATION, 1)
                    curl_setopt(fp, CURLOPT_MAXREDIRS, redirects)
                # end if
                self.headers = curl_exec(fp)
                if curl_errno(fp) == 23 or curl_errno(fp) == 61:
                    curl_setopt(fp, CURLOPT_ENCODING, "none")
                    self.headers = curl_exec(fp)
                # end if
                if curl_errno(fp):
                    self.error = "cURL error " + curl_errno(fp) + ": " + curl_error(fp)
                    self.success = False
                else:
                    info = curl_getinfo(fp)
                    curl_close(fp)
                    self.headers = php_explode("\r\n\r\n", self.headers, info["redirect_count"] + 1)
                    self.headers = php_array_pop(self.headers)
                    parser = php_new_class("SimplePie_HTTP_Parser", lambda : SimplePie_HTTP_Parser(self.headers))
                    if parser.parse():
                        self.headers = parser.headers
                        self.body = parser.body
                        self.status_code = parser.status_code
                        if php_in_array(self.status_code, Array(300, 301, 302, 303, 307)) or self.status_code > 307 and self.status_code < 400 and (php_isset(lambda : self.headers["location"])) and self.redirects < redirects:
                            self.redirects += 1
                            location = SimplePie_Misc.absolutize_url(self.headers["location"], url)
                            return self.__init__(location, timeout, redirects, headers, useragent, force_fsockopen)
                        # end if
                    # end if
                # end if
            else:
                self.method = SIMPLEPIE_FILE_SOURCE_REMOTE | SIMPLEPIE_FILE_SOURCE_FSOCKOPEN
                url_parts = php_parse_url(url)
                socket_host = url_parts["host"]
                if (php_isset(lambda : url_parts["scheme"])) and php_strtolower(url_parts["scheme"]) == "https":
                    socket_host = str("ssl://") + str(url_parts["host"])
                    url_parts["port"] = 443
                # end if
                if (not (php_isset(lambda : url_parts["port"]))):
                    url_parts["port"] = 80
                # end if
                fp = php_no_error(lambda: fsockopen(socket_host, url_parts["port"], errno, errstr, timeout))
                if (not fp):
                    self.error = "fsockopen error: " + errstr
                    self.success = False
                else:
                    stream_set_timeout(fp, timeout)
                    if (php_isset(lambda : url_parts["path"])):
                        if (php_isset(lambda : url_parts["query"])):
                            get = str(url_parts["path"]) + str("?") + str(url_parts["query"])
                        else:
                            get = url_parts["path"]
                        # end if
                    else:
                        get = "/"
                    # end if
                    out = str("GET ") + str(get) + str(" HTTP/1.1\r\n")
                    out += str("Host: ") + str(url_parts["host"]) + str("\r\n")
                    out += str("User-Agent: ") + str(useragent) + str("\r\n")
                    if php_extension_loaded("zlib"):
                        out += "Accept-Encoding: x-gzip,gzip,deflate\r\n"
                    # end if
                    if (php_isset(lambda : url_parts["user"])) and (php_isset(lambda : url_parts["pass"])):
                        out += "Authorization: Basic " + php_base64_encode(str(url_parts["user"]) + str(":") + str(url_parts["pass"])) + "\r\n"
                    # end if
                    for key,value in headers:
                        out += str(key) + str(": ") + str(value) + str("\r\n")
                    # end for
                    out += "Connection: Close\r\n\r\n"
                    fwrite(fp, out)
                    info = stream_get_meta_data(fp)
                    self.headers = ""
                    while True:
                        
                        if not ((not info["eof"]) and (not info["timed_out"])):
                            break
                        # end if
                        self.headers += fread(fp, 1160)
                        info = stream_get_meta_data(fp)
                    # end while
                    if (not info["timed_out"]):
                        parser = php_new_class("SimplePie_HTTP_Parser", lambda : SimplePie_HTTP_Parser(self.headers))
                        if parser.parse():
                            self.headers = parser.headers
                            self.body = parser.body
                            self.status_code = parser.status_code
                            if php_in_array(self.status_code, Array(300, 301, 302, 303, 307)) or self.status_code > 307 and self.status_code < 400 and (php_isset(lambda : self.headers["location"])) and self.redirects < redirects:
                                self.redirects += 1
                                location = SimplePie_Misc.absolutize_url(self.headers["location"], url)
                                return self.__init__(location, timeout, redirects, headers, useragent, force_fsockopen)
                            # end if
                            if (php_isset(lambda : self.headers["content-encoding"])):
                                #// Hey, we act dumb elsewhere, so let's do that here too
                                for case in Switch(php_strtolower(php_trim(self.headers["content-encoding"], "  \n\r "))):
                                    if case("gzip"):
                                        pass
                                    # end if
                                    if case("x-gzip"):
                                        decoder = php_new_class("SimplePie_gzdecode", lambda : SimplePie_gzdecode(self.body))
                                        if (not decoder.parse()):
                                            self.error = "Unable to decode HTTP \"gzip\" stream"
                                            self.success = False
                                        else:
                                            self.body = decoder.data
                                        # end if
                                        break
                                    # end if
                                    if case("deflate"):
                                        decompressed = gzinflate(self.body)
                                        if decompressed != False:
                                            self.body = decompressed
                                        else:
                                            decompressed = gzuncompress(self.body)
                                            if decompressed != False:
                                                self.body = decompressed
                                            else:
                                                decompressed = gzdecode(self.body)
                                                if php_function_exists("gzdecode") and decompressed != False:
                                                    self.body = decompressed
                                                else:
                                                    self.error = "Unable to decode HTTP \"deflate\" stream"
                                                    self.success = False
                                                # end if
                                            # end if
                                        # end if
                                        break
                                    # end if
                                    if case():
                                        self.error = "Unknown content coding"
                                        self.success = False
                                    # end if
                                # end for
                            # end if
                        # end if
                    else:
                        self.error = "fsocket timed out"
                        self.success = False
                    # end if
                    php_fclose(fp)
                # end if
            # end if
        else:
            self.method = SIMPLEPIE_FILE_SOURCE_LOCAL | SIMPLEPIE_FILE_SOURCE_FILE_GET_CONTENTS
            self.body = php_file_get_contents(url)
            if (not self.body):
                self.error = "file_get_contents could not read the file"
                self.success = False
            # end if
        # end if
    # end def __init__
# end class SimplePie_File
