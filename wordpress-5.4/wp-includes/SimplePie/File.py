#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
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
    def __init__(self, url_=None, timeout_=10, redirects_=5, headers_=None, useragent_=None, force_fsockopen_=None):
        if force_fsockopen_ is None:
            force_fsockopen_ = False
        # end if
        
        if php_class_exists("idna_convert"):
            idn_ = php_new_class("idna_convert", lambda : idna_convert())
            parsed_ = SimplePie_Misc.parse_url(url_)
            url_ = SimplePie_Misc.compress_parse_url(parsed_["scheme"], idn_.encode(parsed_["authority"]), parsed_["path"], parsed_["query"], parsed_["fragment"])
        # end if
        self.url = url_
        self.useragent = useragent_
        if php_preg_match("/^http(s)?:\\/\\//i", url_):
            if useragent_ == None:
                useragent_ = php_ini_get("user_agent")
                self.useragent = useragent_
            # end if
            if (not php_is_array(headers_)):
                headers_ = Array()
            # end if
            if (not force_fsockopen_) and php_function_exists("curl_exec"):
                self.method = SIMPLEPIE_FILE_SOURCE_REMOTE | SIMPLEPIE_FILE_SOURCE_CURL
                fp_ = curl_init()
                headers2_ = Array()
                for key_,value_ in headers_:
                    headers2_[-1] = str(key_) + str(": ") + str(value_)
                # end for
                if php_version_compare(SimplePie_Misc.get_curl_version(), "7.10.5", ">="):
                    curl_setopt(fp_, CURLOPT_ENCODING, "")
                # end if
                curl_setopt(fp_, CURLOPT_URL, url_)
                curl_setopt(fp_, CURLOPT_HEADER, 1)
                curl_setopt(fp_, CURLOPT_RETURNTRANSFER, 1)
                curl_setopt(fp_, CURLOPT_TIMEOUT, timeout_)
                curl_setopt(fp_, CURLOPT_CONNECTTIMEOUT, timeout_)
                curl_setopt(fp_, CURLOPT_REFERER, url_)
                curl_setopt(fp_, CURLOPT_USERAGENT, useragent_)
                curl_setopt(fp_, CURLOPT_HTTPHEADER, headers2_)
                if (not php_ini_get("open_basedir")) and (not php_ini_get("safe_mode")) and php_version_compare(SimplePie_Misc.get_curl_version(), "7.15.2", ">="):
                    curl_setopt(fp_, CURLOPT_FOLLOWLOCATION, 1)
                    curl_setopt(fp_, CURLOPT_MAXREDIRS, redirects_)
                # end if
                self.headers = curl_exec(fp_)
                if curl_errno(fp_) == 23 or curl_errno(fp_) == 61:
                    curl_setopt(fp_, CURLOPT_ENCODING, "none")
                    self.headers = curl_exec(fp_)
                # end if
                if curl_errno(fp_):
                    self.error = "cURL error " + curl_errno(fp_) + ": " + curl_error(fp_)
                    self.success = False
                else:
                    info_ = curl_getinfo(fp_)
                    curl_close(fp_)
                    self.headers = php_explode("\r\n\r\n", self.headers, info_["redirect_count"] + 1)
                    self.headers = php_array_pop(self.headers)
                    parser_ = php_new_class("SimplePie_HTTP_Parser", lambda : SimplePie_HTTP_Parser(self.headers))
                    if parser_.parse():
                        self.headers = parser_.headers
                        self.body = parser_.body
                        self.status_code = parser_.status_code
                        if php_in_array(self.status_code, Array(300, 301, 302, 303, 307)) or self.status_code > 307 and self.status_code < 400 and (php_isset(lambda : self.headers["location"])) and self.redirects < redirects_:
                            self.redirects += 1
                            location_ = SimplePie_Misc.absolutize_url(self.headers["location"], url_)
                            return self.__init__(location_, timeout_, redirects_, headers_, useragent_, force_fsockopen_)
                        # end if
                    # end if
                # end if
            else:
                self.method = SIMPLEPIE_FILE_SOURCE_REMOTE | SIMPLEPIE_FILE_SOURCE_FSOCKOPEN
                url_parts_ = php_parse_url(url_)
                socket_host_ = url_parts_["host"]
                if (php_isset(lambda : url_parts_["scheme"])) and php_strtolower(url_parts_["scheme"]) == "https":
                    socket_host_ = str("ssl://") + str(url_parts_["host"])
                    url_parts_["port"] = 443
                # end if
                if (not (php_isset(lambda : url_parts_["port"]))):
                    url_parts_["port"] = 80
                # end if
                fp_ = php_no_error(lambda: fsockopen(socket_host_, url_parts_["port"], errno_, errstr_, timeout_))
                if (not fp_):
                    self.error = "fsockopen error: " + errstr_
                    self.success = False
                else:
                    stream_set_timeout(fp_, timeout_)
                    if (php_isset(lambda : url_parts_["path"])):
                        if (php_isset(lambda : url_parts_["query"])):
                            get_ = str(url_parts_["path"]) + str("?") + str(url_parts_["query"])
                        else:
                            get_ = url_parts_["path"]
                        # end if
                    else:
                        get_ = "/"
                    # end if
                    out_ = str("GET ") + str(get_) + str(" HTTP/1.1\r\n")
                    out_ += str("Host: ") + str(url_parts_["host"]) + str("\r\n")
                    out_ += str("User-Agent: ") + str(useragent_) + str("\r\n")
                    if php_extension_loaded("zlib"):
                        out_ += "Accept-Encoding: x-gzip,gzip,deflate\r\n"
                    # end if
                    if (php_isset(lambda : url_parts_["user"])) and (php_isset(lambda : url_parts_["pass"])):
                        out_ += "Authorization: Basic " + php_base64_encode(str(url_parts_["user"]) + str(":") + str(url_parts_["pass"])) + "\r\n"
                    # end if
                    for key_,value_ in headers_:
                        out_ += str(key_) + str(": ") + str(value_) + str("\r\n")
                    # end for
                    out_ += "Connection: Close\r\n\r\n"
                    fwrite(fp_, out_)
                    info_ = stream_get_meta_data(fp_)
                    self.headers = ""
                    while True:
                        
                        if not ((not info_["eof"]) and (not info_["timed_out"])):
                            break
                        # end if
                        self.headers += fread(fp_, 1160)
                        info_ = stream_get_meta_data(fp_)
                    # end while
                    if (not info_["timed_out"]):
                        parser_ = php_new_class("SimplePie_HTTP_Parser", lambda : SimplePie_HTTP_Parser(self.headers))
                        if parser_.parse():
                            self.headers = parser_.headers
                            self.body = parser_.body
                            self.status_code = parser_.status_code
                            if php_in_array(self.status_code, Array(300, 301, 302, 303, 307)) or self.status_code > 307 and self.status_code < 400 and (php_isset(lambda : self.headers["location"])) and self.redirects < redirects_:
                                self.redirects += 1
                                location_ = SimplePie_Misc.absolutize_url(self.headers["location"], url_)
                                return self.__init__(location_, timeout_, redirects_, headers_, useragent_, force_fsockopen_)
                            # end if
                            if (php_isset(lambda : self.headers["content-encoding"])):
                                #// Hey, we act dumb elsewhere, so let's do that here too
                                for case in Switch(php_strtolower(php_trim(self.headers["content-encoding"], "  \n\r "))):
                                    if case("gzip"):
                                        pass
                                    # end if
                                    if case("x-gzip"):
                                        decoder_ = php_new_class("SimplePie_gzdecode", lambda : SimplePie_gzdecode(self.body))
                                        if (not decoder_.parse()):
                                            self.error = "Unable to decode HTTP \"gzip\" stream"
                                            self.success = False
                                        else:
                                            self.body = decoder_.data
                                        # end if
                                        break
                                    # end if
                                    if case("deflate"):
                                        decompressed_ = gzinflate(self.body)
                                        if decompressed_ != False:
                                            self.body = decompressed_
                                        else:
                                            decompressed_ = gzuncompress(self.body)
                                            if decompressed_ != False:
                                                self.body = decompressed_
                                            else:
                                                decompressed_ = gzdecode(self.body)
                                                if php_function_exists("gzdecode") and decompressed_ != False:
                                                    self.body = decompressed_
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
                    php_fclose(fp_)
                # end if
            # end if
        else:
            self.method = SIMPLEPIE_FILE_SOURCE_LOCAL | SIMPLEPIE_FILE_SOURCE_FILE_GET_CONTENTS
            self.body = php_file_get_contents(url_)
            if (not self.body):
                self.error = "file_get_contents could not read the file"
                self.success = False
            # end if
        # end if
    # end def __init__
# end class SimplePie_File
