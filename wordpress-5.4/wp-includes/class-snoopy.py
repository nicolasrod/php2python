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
#// Deprecated. Use WP_HTTP (http.php) instead.
#//
_deprecated_file(php_basename(__FILE__), "3.0.0", WPINC + "/http.php")
if (not php_class_exists("Snoopy", False)):
    #// 
    #// Snoopy - the PHP net client
    #// Author: Monte Ohrt <monte@ispi.net>
    #// Copyright (c): 1999-2008 New Digital Group, all rights reserved
    #// Version: 1.2.4
    #// This library is free software; you can redistribute it and/or
    #// modify it under the terms of the GNU Lesser General Public
    #// License as published by the Free Software Foundation; either
    #// version 2.1 of the License, or (at your option) any later version.
    #// 
    #// This library is distributed in the hope that it will be useful,
    #// but WITHOUT ANY WARRANTY; without even the implied warranty of
    #// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    #// Lesser General Public License for more details.
    #// 
    #// You should have received a copy of the GNU Lesser General Public
    #// License along with this library; if not, write to the Free Software
    #// Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
    #// You may contact the author of Snoopy by e-mail at:
    #// monte@ohrt.com
    #// The latest version of Snoopy can be obtained from:
    #// http://snoopy.sourceforge.net
    #//
    class Snoopy():
        #// Public variables
        #// user definable vars
        host = "www.php.net"
        #// host name we are connecting to
        port = 80
        #// port we are connecting to
        proxy_host = ""
        #// proxy host to use
        proxy_port = ""
        #// proxy port to use
        proxy_user = ""
        #// proxy user to use
        proxy_pass = ""
        #// proxy password to use
        agent = "Snoopy v1.2.4"
        #// agent we masquerade as
        referer = ""
        #// referer info to pass
        cookies = Array()
        #// array of cookies to pass
        #// $cookies["username"]="joe";
        rawheaders = Array()
        #// array of raw headers to send
        #// $rawheaders["Content-type"]="text/html";
        maxredirs = 5
        #// http redirection depth maximum. 0 = disallow
        lastredirectaddr = ""
        #// contains address of last redirected address
        offsiteok = True
        #// allows redirection off-site
        maxframes = 0
        #// frame content depth maximum. 0 = disallow
        expandlinks = True
        #// expand links to fully qualified URLs.
        #// this only applies to fetchlinks()
        #// submitlinks(), and submittext()
        passcookies = True
        #// pass set cookies back through redirects
        #// NOTE: this currently does not respect
        #// dates, domains or paths.
        user = ""
        #// user for http authentication
        pass_ = ""
        #// password for http authentication
        #// http accept types
        accept = "image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, */*"
        results = ""
        #// where the content is put
        error = ""
        #// error messages sent here
        response_code = ""
        #// response code returned from server
        headers = Array()
        #// headers returned from server sent here
        maxlength = 500000
        #// max return data length (body)
        read_timeout = 0
        #// timeout on read operations, in seconds
        #// supported only since PHP 4 Beta 4
        #// set to 0 to disallow timeouts
        timed_out = False
        #// if a read operation timed out
        status = 0
        #// http request status
        temp_dir = "/tmp"
        #// temporary directory that the webserver
        #// has permission to write to.
        #// under Windows, this should be C:\temp
        curl_path = "/usr/local/bin/curl"
        #// Snoopy will use cURL for fetching
        #// SSL content if a full system path to
        #// the cURL binary is supplied here.
        #// set to false if you do not have
        #// cURL installed. See http://curl.haxx.se
        #// for details on installing cURL.
        #// Snoopy does *not* use the cURL
        #// library functions built into php,
        #// as these functions are not stable
        #// as of this Snoopy release.
        #// Private variables
        _maxlinelen = 4096
        #// max line length (headers)
        _httpmethod = "GET"
        #// default http request method
        _httpversion = "HTTP/1.0"
        #// default http request version
        _submit_method = "POST"
        #// default submit method
        _submit_type = "application/x-www-form-urlencoded"
        #// default submit type
        _mime_boundary = ""
        #// MIME boundary for multipart/form-data submit type
        _redirectaddr = False
        #// will be set if page fetched is a redirect
        _redirectdepth = 0
        #// increments on an http redirect
        _frameurls = Array()
        #// frame src urls
        _framedepth = 0
        #// increments on frame depth
        _isproxy = False
        #// set if using a proxy server
        _fp_timeout = 30
        #// timeout for socket connection
        #// ======================================================================*\
#// Function:   fetch
        #// Purpose:    fetch the contents of a web page
        #// (and possibly other protocols in the
        #// future like ftp, nntp, gopher, etc.)
        #// Input:      $URI    the location of the page to fetch
        #// Output:     $this->results  the output text from the fetch
        #// \*======================================================================
        def fetch(self, URI_=None):
            
            
            #// preg_match("|^([^:]+)://([^:/]+)(:[\d]+)*(.*)|",$URI,$URI_PARTS);
            URI_PARTS_ = php_parse_url(URI_)
            if (not php_empty(lambda : URI_PARTS_["user"])):
                self.user = URI_PARTS_["user"]
            # end if
            if (not php_empty(lambda : URI_PARTS_["pass"])):
                self.pass_ = URI_PARTS_["pass"]
            # end if
            if php_empty(lambda : URI_PARTS_["query"]):
                URI_PARTS_["query"] = ""
            # end if
            if php_empty(lambda : URI_PARTS_["path"]):
                URI_PARTS_["path"] = ""
            # end if
            for case in Switch(php_strtolower(URI_PARTS_["scheme"])):
                if case("http"):
                    self.host = URI_PARTS_["host"]
                    if (not php_empty(lambda : URI_PARTS_["port"])):
                        self.port = URI_PARTS_["port"]
                    # end if
                    if self._connect(fp_):
                        if self._isproxy:
                            #// using proxy, send entire URI
                            self._httprequest(URI_, fp_, URI_, self._httpmethod)
                        else:
                            path_ = URI_PARTS_["path"] + "?" + URI_PARTS_["query"] if URI_PARTS_["query"] else ""
                            #// no proxy, send only the path
                            self._httprequest(path_, fp_, URI_, self._httpmethod)
                        # end if
                        self._disconnect(fp_)
                        if self._redirectaddr:
                            #// url was redirected, check if we've hit the max depth
                            if self.maxredirs > self._redirectdepth:
                                #// only follow redirect if it's on this site, or offsiteok is true
                                if php_preg_match("|^http://" + preg_quote(self.host) + "|i", self._redirectaddr) or self.offsiteok:
                                    #// follow the redirect
                                    self._redirectdepth += 1
                                    self.lastredirectaddr = self._redirectaddr
                                    self.fetch(self._redirectaddr)
                                # end if
                            # end if
                        # end if
                        if self._framedepth < self.maxframes and php_count(self._frameurls) > 0:
                            frameurls_ = self._frameurls
                            self._frameurls = Array()
                            while True:
                                frameurl_ = each(frameurls_)
                                if not (frameurl_):
                                    break
                                # end if
                                if self._framedepth < self.maxframes:
                                    self.fetch(frameurl_)
                                    self._framedepth += 1
                                else:
                                    break
                                # end if
                            # end while
                        # end if
                    else:
                        return False
                    # end if
                    return True
                    break
                # end if
                if case("https"):
                    if (not self.curl_path):
                        return False
                    # end if
                    if php_function_exists("is_executable"):
                        if (not is_executable(self.curl_path)):
                            return False
                        # end if
                    # end if
                    self.host = URI_PARTS_["host"]
                    if (not php_empty(lambda : URI_PARTS_["port"])):
                        self.port = URI_PARTS_["port"]
                    # end if
                    if self._isproxy:
                        #// using proxy, send entire URI
                        self._httpsrequest(URI_, URI_, self._httpmethod)
                    else:
                        path_ = URI_PARTS_["path"] + "?" + URI_PARTS_["query"] if URI_PARTS_["query"] else ""
                        #// no proxy, send only the path
                        self._httpsrequest(path_, URI_, self._httpmethod)
                    # end if
                    if self._redirectaddr:
                        #// url was redirected, check if we've hit the max depth
                        if self.maxredirs > self._redirectdepth:
                            #// only follow redirect if it's on this site, or offsiteok is true
                            if php_preg_match("|^http://" + preg_quote(self.host) + "|i", self._redirectaddr) or self.offsiteok:
                                #// follow the redirect
                                self._redirectdepth += 1
                                self.lastredirectaddr = self._redirectaddr
                                self.fetch(self._redirectaddr)
                            # end if
                        # end if
                    # end if
                    if self._framedepth < self.maxframes and php_count(self._frameurls) > 0:
                        frameurls_ = self._frameurls
                        self._frameurls = Array()
                        while True:
                            frameurl_ = each(frameurls_)
                            if not (frameurl_):
                                break
                            # end if
                            if self._framedepth < self.maxframes:
                                self.fetch(frameurl_)
                                self._framedepth += 1
                            else:
                                break
                            # end if
                        # end while
                    # end if
                    return True
                    break
                # end if
                if case():
                    #// not a valid protocol
                    self.error = "Invalid protocol \"" + URI_PARTS_["scheme"] + "\"\\n"
                    return False
                    break
                # end if
            # end for
            return True
        # end def fetch
        #// ======================================================================*\
#// Function:   submit
        #// Purpose:    submit an http form
        #// Input:      $URI    the location to post the data
        #// $formvars   the formvars to use.
        #// format: $formvars["var"] = "val";
        #// $formfiles  an array of files to submit
        #// format: $formfiles["var"] = "/dir/filename.ext";
        #// Output:     $this->results  the text output from the post
        #// \*======================================================================
        def submit(self, URI_=None, formvars_="", formfiles_=""):
            
            
            postdata_ = None
            postdata_ = self._prepare_post_body(formvars_, formfiles_)
            URI_PARTS_ = php_parse_url(URI_)
            if (not php_empty(lambda : URI_PARTS_["user"])):
                self.user = URI_PARTS_["user"]
            # end if
            if (not php_empty(lambda : URI_PARTS_["pass"])):
                self.pass_ = URI_PARTS_["pass"]
            # end if
            if php_empty(lambda : URI_PARTS_["query"]):
                URI_PARTS_["query"] = ""
            # end if
            if php_empty(lambda : URI_PARTS_["path"]):
                URI_PARTS_["path"] = ""
            # end if
            for case in Switch(php_strtolower(URI_PARTS_["scheme"])):
                if case("http"):
                    self.host = URI_PARTS_["host"]
                    if (not php_empty(lambda : URI_PARTS_["port"])):
                        self.port = URI_PARTS_["port"]
                    # end if
                    if self._connect(fp_):
                        if self._isproxy:
                            #// using proxy, send entire URI
                            self._httprequest(URI_, fp_, URI_, self._submit_method, self._submit_type, postdata_)
                        else:
                            path_ = URI_PARTS_["path"] + "?" + URI_PARTS_["query"] if URI_PARTS_["query"] else ""
                            #// no proxy, send only the path
                            self._httprequest(path_, fp_, URI_, self._submit_method, self._submit_type, postdata_)
                        # end if
                        self._disconnect(fp_)
                        if self._redirectaddr:
                            #// url was redirected, check if we've hit the max depth
                            if self.maxredirs > self._redirectdepth:
                                if (not php_preg_match("|^" + URI_PARTS_["scheme"] + "://|", self._redirectaddr)):
                                    self._redirectaddr = self._expandlinks(self._redirectaddr, URI_PARTS_["scheme"] + "://" + URI_PARTS_["host"])
                                # end if
                                #// only follow redirect if it's on this site, or offsiteok is true
                                if php_preg_match("|^http://" + preg_quote(self.host) + "|i", self._redirectaddr) or self.offsiteok:
                                    #// follow the redirect
                                    self._redirectdepth += 1
                                    self.lastredirectaddr = self._redirectaddr
                                    if php_strpos(self._redirectaddr, "?") > 0:
                                        self.fetch(self._redirectaddr)
                                    else:
                                        self.submit(self._redirectaddr, formvars_, formfiles_)
                                    # end if
                                # end if
                            # end if
                        # end if
                        if self._framedepth < self.maxframes and php_count(self._frameurls) > 0:
                            frameurls_ = self._frameurls
                            self._frameurls = Array()
                            while True:
                                frameurl_ = each(frameurls_)
                                if not (frameurl_):
                                    break
                                # end if
                                if self._framedepth < self.maxframes:
                                    self.fetch(frameurl_)
                                    self._framedepth += 1
                                else:
                                    break
                                # end if
                            # end while
                        # end if
                    else:
                        return False
                    # end if
                    return True
                    break
                # end if
                if case("https"):
                    if (not self.curl_path):
                        return False
                    # end if
                    if php_function_exists("is_executable"):
                        if (not is_executable(self.curl_path)):
                            return False
                        # end if
                    # end if
                    self.host = URI_PARTS_["host"]
                    if (not php_empty(lambda : URI_PARTS_["port"])):
                        self.port = URI_PARTS_["port"]
                    # end if
                    if self._isproxy:
                        #// using proxy, send entire URI
                        self._httpsrequest(URI_, URI_, self._submit_method, self._submit_type, postdata_)
                    else:
                        path_ = URI_PARTS_["path"] + "?" + URI_PARTS_["query"] if URI_PARTS_["query"] else ""
                        #// no proxy, send only the path
                        self._httpsrequest(path_, URI_, self._submit_method, self._submit_type, postdata_)
                    # end if
                    if self._redirectaddr:
                        #// url was redirected, check if we've hit the max depth
                        if self.maxredirs > self._redirectdepth:
                            if (not php_preg_match("|^" + URI_PARTS_["scheme"] + "://|", self._redirectaddr)):
                                self._redirectaddr = self._expandlinks(self._redirectaddr, URI_PARTS_["scheme"] + "://" + URI_PARTS_["host"])
                            # end if
                            #// only follow redirect if it's on this site, or offsiteok is true
                            if php_preg_match("|^http://" + preg_quote(self.host) + "|i", self._redirectaddr) or self.offsiteok:
                                #// follow the redirect
                                self._redirectdepth += 1
                                self.lastredirectaddr = self._redirectaddr
                                if php_strpos(self._redirectaddr, "?") > 0:
                                    self.fetch(self._redirectaddr)
                                else:
                                    self.submit(self._redirectaddr, formvars_, formfiles_)
                                # end if
                            # end if
                        # end if
                    # end if
                    if self._framedepth < self.maxframes and php_count(self._frameurls) > 0:
                        frameurls_ = self._frameurls
                        self._frameurls = Array()
                        while True:
                            frameurl_ = each(frameurls_)
                            if not (frameurl_):
                                break
                            # end if
                            if self._framedepth < self.maxframes:
                                self.fetch(frameurl_)
                                self._framedepth += 1
                            else:
                                break
                            # end if
                        # end while
                    # end if
                    return True
                    break
                # end if
                if case():
                    #// not a valid protocol
                    self.error = "Invalid protocol \"" + URI_PARTS_["scheme"] + "\"\\n"
                    return False
                    break
                # end if
            # end for
            return True
        # end def submit
        #// ======================================================================*\
#// Function:   fetchlinks
        #// Purpose:    fetch the links from a web page
        #// Input:      $URI    where you are fetching from
        #// Output:     $this->results  an array of the URLs
        #// \*======================================================================
        def fetchlinks(self, URI_=None):
            
            
            if self.fetch(URI_):
                if self.lastredirectaddr:
                    URI_ = self.lastredirectaddr
                # end if
                if php_is_array(self.results):
                    x_ = 0
                    while x_ < php_count(self.results):
                        
                        self.results[x_] = self._striplinks(self.results[x_])
                        x_ += 1
                    # end while
                else:
                    self.results = self._striplinks(self.results)
                # end if
                if self.expandlinks:
                    self.results = self._expandlinks(self.results, URI_)
                # end if
                return True
            else:
                return False
            # end if
        # end def fetchlinks
        #// ======================================================================*\
#// Function:   fetchform
        #// Purpose:    fetch the form elements from a web page
        #// Input:      $URI    where you are fetching from
        #// Output:     $this->results  the resulting html form
        #// \*======================================================================
        def fetchform(self, URI_=None):
            
            
            if self.fetch(URI_):
                if php_is_array(self.results):
                    x_ = 0
                    while x_ < php_count(self.results):
                        
                        self.results[x_] = self._stripform(self.results[x_])
                        x_ += 1
                    # end while
                else:
                    self.results = self._stripform(self.results)
                # end if
                return True
            else:
                return False
            # end if
        # end def fetchform
        #// ======================================================================*\
#// Function:   fetchtext
        #// Purpose:    fetch the text from a web page, stripping the links
        #// Input:      $URI    where you are fetching from
        #// Output:     $this->results  the text from the web page
        #// \*======================================================================
        def fetchtext(self, URI_=None):
            
            
            if self.fetch(URI_):
                if php_is_array(self.results):
                    x_ = 0
                    while x_ < php_count(self.results):
                        
                        self.results[x_] = self._striptext(self.results[x_])
                        x_ += 1
                    # end while
                else:
                    self.results = self._striptext(self.results)
                # end if
                return True
            else:
                return False
            # end if
        # end def fetchtext
        #// ======================================================================*\
#// Function:   submitlinks
        #// Purpose:    grab links from a form submission
        #// Input:      $URI    where you are submitting from
        #// Output:     $this->results  an array of the links from the post
        #// \*======================================================================
        def submitlinks(self, URI_=None, formvars_="", formfiles_=""):
            
            
            if self.submit(URI_, formvars_, formfiles_):
                if self.lastredirectaddr:
                    URI_ = self.lastredirectaddr
                # end if
                if php_is_array(self.results):
                    x_ = 0
                    while x_ < php_count(self.results):
                        
                        self.results[x_] = self._striplinks(self.results[x_])
                        if self.expandlinks:
                            self.results[x_] = self._expandlinks(self.results[x_], URI_)
                        # end if
                        x_ += 1
                    # end while
                else:
                    self.results = self._striplinks(self.results)
                    if self.expandlinks:
                        self.results = self._expandlinks(self.results, URI_)
                    # end if
                # end if
                return True
            else:
                return False
            # end if
        # end def submitlinks
        #// ======================================================================*\
#// Function:   submittext
        #// Purpose:    grab text from a form submission
        #// Input:      $URI    where you are submitting from
        #// Output:     $this->results  the text from the web page
        #// \*======================================================================
        def submittext(self, URI_=None, formvars_="", formfiles_=""):
            
            
            if self.submit(URI_, formvars_, formfiles_):
                if self.lastredirectaddr:
                    URI_ = self.lastredirectaddr
                # end if
                if php_is_array(self.results):
                    x_ = 0
                    while x_ < php_count(self.results):
                        
                        self.results[x_] = self._striptext(self.results[x_])
                        if self.expandlinks:
                            self.results[x_] = self._expandlinks(self.results[x_], URI_)
                        # end if
                        x_ += 1
                    # end while
                else:
                    self.results = self._striptext(self.results)
                    if self.expandlinks:
                        self.results = self._expandlinks(self.results, URI_)
                    # end if
                # end if
                return True
            else:
                return False
            # end if
        # end def submittext
        #// ======================================================================*\
#// Function:   set_submit_multipart
        #// Purpose:    Set the form submission content type to
        #// multipart/form-data
        #// \*======================================================================
        def set_submit_multipart(self):
            
            
            self._submit_type = "multipart/form-data"
        # end def set_submit_multipart
        #// ======================================================================*\
#// Function:   set_submit_normal
        #// Purpose:    Set the form submission content type to
        #// application/x-www-form-urlencoded
        #// \*======================================================================
        def set_submit_normal(self):
            
            
            self._submit_type = "application/x-www-form-urlencoded"
        # end def set_submit_normal
        #// ======================================================================*\
#// Private functions
        #// \*======================================================================
        #// ======================================================================*\
#// Function:   _striplinks
        #// Purpose:    strip the hyperlinks from an html document
        #// Input:      $document   document to strip.
        #// Output:     $match      an array of the links
        #// \*======================================================================
        def _striplinks(self, document_=None):
            
            
            preg_match_all("""'<\\s*a\\s.*?href\\s*=\\s*            # find <a href=
            ([\"\\'])?                  # find single or double quote
            (?(1) (.*?)\\1 | ([^\\s\\>]+))      # if quote found, match up to next matching
            # quote, otherwise match up to next space
            'isx""", document_, links_)
            #// catenate the non-empty matches from the conditional subpattern
            while True:
                key_, val_ = each(links_[2])
                if not (key_, val_):
                    break
                # end if
                if (not php_empty(lambda : val_)):
                    match_[-1] = val_
                # end if
            # end while
            while True:
                key_, val_ = each(links_[3])
                if not (key_, val_):
                    break
                # end if
                if (not php_empty(lambda : val_)):
                    match_[-1] = val_
                # end if
            # end while
            #// return the links
            return match_
        # end def _striplinks
        #// ======================================================================*\
#// Function:   _stripform
        #// Purpose:    strip the form elements from an html document
        #// Input:      $document   document to strip.
        #// Output:     $match      an array of the links
        #// \*======================================================================
        def _stripform(self, document_=None):
            
            
            preg_match_all("""'<\\/?(FORM|INPUT|SELECT|TEXTAREA|(OPTION))[^<>]*>(?(2)(.*(?=<\\/?(option|select)[^<>]*>[
            ]*)|(?=[
            ]*))|(?=[
            ]*))'Usi""", document_, elements_)
            #// catenate the matches
            match_ = php_implode("\r\n", elements_[0])
            #// return the links
            return match_
        # end def _stripform
        #// ======================================================================*\
#// Function:   _striptext
        #// Purpose:    strip the text from an html document
        #// Input:      $document   document to strip.
        #// Output:     $text       the resulting text
        #// \*======================================================================
        def _striptext(self, document_=None):
            
            
            #// I didn't use preg eval (//e) since that is only available in PHP 4.0.
            #// so, list your entities one by one here. I included some of the
            #// more common ones.
            search_ = Array("'<script[^>]*?>.*?</script>'si", "'<[\\/\\!]*?[^<>]*?>'si", "'([\r\n])[\\s]+'", "'&(quot|#34|#034|#x22);'i", "'&(amp|#38|#038|#x26);'i", "'&(lt|#60|#060|#x3c);'i", "'&(gt|#62|#062|#x3e);'i", "'&(nbsp|#160|#xa0);'i", "'&(iexcl|#161);'i", "'&(cent|#162);'i", "'&(pound|#163);'i", "'&(copy|#169);'i", "'&(reg|#174);'i", "'&(deg|#176);'i", "'&(#39|#039|#x27);'", "'&(euro|#8364);'i", "'&a(uml|UML);'", "'&o(uml|UML);'", "'&u(uml|UML);'", "'&A(uml|UML);'", "'&O(uml|UML);'", "'&U(uml|UML);'", "'&szlig;'i")
            replace_ = Array("", "", "\\1", "\"", "&", "<", ">", " ", chr(161), chr(162), chr(163), chr(169), chr(174), chr(176), chr(39), chr(128), chr(228), chr(246), chr(252), chr(196), chr(214), chr(220), chr(223))
            text_ = php_preg_replace(search_, replace_, document_)
            return text_
        # end def _striptext
        #// ======================================================================*\
#// Function:   _expandlinks
        #// Purpose:    expand each link into a fully qualified URL
        #// Input:      $links          the links to qualify
        #// $URI            the full URI to get the base from
        #// Output:     $expandedLinks  the expanded links
        #// \*======================================================================
        def _expandlinks(self, links_=None, URI_=None):
            
            
            php_preg_match("/^[^\\?]+/", URI_, match_)
            match_ = php_preg_replace("|/[^\\/\\.]+\\.[^\\/\\.]+$|", "", match_[0])
            match_ = php_preg_replace("|/$|", "", match_)
            match_part_ = php_parse_url(match_)
            match_root_ = match_part_["scheme"] + "://" + match_part_["host"]
            search_ = Array("|^http://" + preg_quote(self.host) + "|i", "|^(\\/)|i", "|^(?!http://)(?!mailto:)|i", "|/\\./|", "|/[^\\/]+/\\.\\./|")
            replace_ = Array("", match_root_ + "/", match_ + "/", "/", "/")
            expandedLinks_ = php_preg_replace(search_, replace_, links_)
            return expandedLinks_
        # end def _expandlinks
        #// ======================================================================*\
#// Function:   _httprequest
        #// Purpose:    go get the http data from the server
        #// Input:      $url        the url to fetch
        #// $fp         the current open file pointer
        #// $URI        the full URI
        #// $body       body contents to send if any (POST)
        #// Output:
        #// \*======================================================================
        def _httprequest(self, url_=None, fp_=None, URI_=None, http_method_=None, content_type_="", body_=""):
            
            
            cookie_headers_ = ""
            if self.passcookies and self._redirectaddr:
                self.setcookies()
            # end if
            URI_PARTS_ = php_parse_url(URI_)
            if php_empty(lambda : url_):
                url_ = "/"
            # end if
            headers_ = http_method_ + " " + url_ + " " + self._httpversion + "\r\n"
            if (not php_empty(lambda : self.agent)):
                headers_ += "User-Agent: " + self.agent + "\r\n"
            # end if
            if (not php_empty(lambda : self.host)) and (not (php_isset(lambda : self.rawheaders["Host"]))):
                headers_ += "Host: " + self.host
                if (not php_empty(lambda : self.port)) and self.port != 80:
                    headers_ += ":" + self.port
                # end if
                headers_ += "\r\n"
            # end if
            if (not php_empty(lambda : self.accept)):
                headers_ += "Accept: " + self.accept + "\r\n"
            # end if
            if (not php_empty(lambda : self.referer)):
                headers_ += "Referer: " + self.referer + "\r\n"
            # end if
            if (not php_empty(lambda : self.cookies)):
                if (not php_is_array(self.cookies)):
                    self.cookies = self.cookies
                # end if
                reset(self.cookies)
                if php_count(self.cookies) > 0:
                    cookie_headers_ += "Cookie: "
                    for cookieKey_,cookieVal_ in self.cookies.items():
                        cookie_headers_ += cookieKey_ + "=" + urlencode(cookieVal_) + "; "
                    # end for
                    headers_ += php_substr(cookie_headers_, 0, -2) + "\r\n"
                # end if
            # end if
            if (not php_empty(lambda : self.rawheaders)):
                if (not php_is_array(self.rawheaders)):
                    self.rawheaders = self.rawheaders
                # end if
                while True:
                    headerKey_, headerVal_ = each(self.rawheaders)
                    if not (headerKey_, headerVal_):
                        break
                    # end if
                    headers_ += headerKey_ + ": " + headerVal_ + "\r\n"
                # end while
            # end if
            if (not php_empty(lambda : content_type_)):
                headers_ += str("Content-type: ") + str(content_type_)
                if content_type_ == "multipart/form-data":
                    headers_ += "; boundary=" + self._mime_boundary
                # end if
                headers_ += "\r\n"
            # end if
            if (not php_empty(lambda : body_)):
                headers_ += "Content-length: " + php_strlen(body_) + "\r\n"
            # end if
            if (not php_empty(lambda : self.user)) or (not php_empty(lambda : self.pass_)):
                headers_ += "Authorization: Basic " + php_base64_encode(self.user + ":" + self.pass_) + "\r\n"
            # end if
            #// add proxy auth headers
            if (not php_empty(lambda : self.proxy_user)):
                headers_ += "Proxy-Authorization: " + "Basic " + php_base64_encode(self.proxy_user + ":" + self.proxy_pass) + "\r\n"
            # end if
            headers_ += "\r\n"
            #// set the read timeout if needed
            if self.read_timeout > 0:
                socket_set_timeout(fp_, self.read_timeout)
            # end if
            self.timed_out = False
            fwrite(fp_, headers_ + body_, php_strlen(headers_ + body_))
            self._redirectaddr = False
            self.headers = None
            while True:
                currentHeader_ = php_fgets(fp_, self._maxlinelen)
                if not (currentHeader_):
                    break
                # end if
                if self.read_timeout > 0 and self._check_timeout(fp_):
                    self.status = -100
                    return False
                # end if
                if currentHeader_ == "\r\n":
                    break
                # end if
                #// if a header begins with Location: or URI:, set the redirect
                if php_preg_match("/^(Location:|URI:)/i", currentHeader_):
                    #// get URL portion of the redirect
                    php_preg_match("/^(Location:|URI:)[ ]+(.*)/i", chop(currentHeader_), matches_)
                    #// look for :// in the Location header to see if hostname is included
                    if (not php_preg_match("|\\:\\/\\/|", matches_[2])):
                        #// no host in the path, so prepend
                        self._redirectaddr = URI_PARTS_["scheme"] + "://" + self.host + ":" + self.port
                        #// eliminate double slash
                        if (not php_preg_match("|^/|", matches_[2])):
                            self._redirectaddr += "/" + matches_[2]
                        else:
                            self._redirectaddr += matches_[2]
                        # end if
                    else:
                        self._redirectaddr = matches_[2]
                    # end if
                # end if
                if php_preg_match("|^HTTP/|", currentHeader_):
                    if php_preg_match("|^HTTP/[^\\s]*\\s(.*?)\\s|", currentHeader_, status_):
                        self.status = status_[1]
                    # end if
                    self.response_code = currentHeader_
                # end if
                self.headers[-1] = currentHeader_
            # end while
            results_ = ""
            while True:
                _data_ = fread(fp_, self.maxlength)
                if php_strlen(_data_) == 0:
                    break
                # end if
                results_ += _data_
                
                if True:
                    break
                # end if
            # end while
            if self.read_timeout > 0 and self._check_timeout(fp_):
                self.status = -100
                return False
            # end if
            #// check if there is a redirect meta tag
            if php_preg_match("'<meta[\\s]*http-equiv[^>]*?content[\\s]*=[\\s]*[\"\\']?\\d+;[\\s]*URL[\\s]*=[\\s]*([^\"\\']*?)[\"\\']?>'i", results_, match_):
                self._redirectaddr = self._expandlinks(match_[1], URI_)
            # end if
            #// have we hit our frame depth and is there frame src to fetch?
            if self._framedepth < self.maxframes and preg_match_all("'<frame\\s+.*src[\\s]*=[\\'\"]?([^\\'\"\\>]+)'i", results_, match_):
                self.results[-1] = results_
                x_ = 0
                while x_ < php_count(match_[1]):
                    
                    self._frameurls[-1] = self._expandlinks(match_[1][x_], URI_PARTS_["scheme"] + "://" + self.host)
                    x_ += 1
                # end while
                #// have we already fetched framed content?
            elif php_is_array(self.results):
                self.results[-1] = results_
            else:
                self.results = results_
            # end if
            return True
        # end def _httprequest
        #// ======================================================================*\
#// Function:   _httpsrequest
        #// Purpose:    go get the https data from the server using curl
        #// Input:      $url        the url to fetch
        #// $URI        the full URI
        #// $body       body contents to send if any (POST)
        #// Output:
        #// \*======================================================================
        def _httpsrequest(self, url_=None, URI_=None, http_method_=None, content_type_="", body_=""):
            
            
            if self.passcookies and self._redirectaddr:
                self.setcookies()
            # end if
            headers_ = Array()
            URI_PARTS_ = php_parse_url(URI_)
            if php_empty(lambda : url_):
                url_ = "/"
            # end if
            #// GET ... header not needed for curl
            #// $headers[] = $http_method." ".$url." ".$this->_httpversion;
            if (not php_empty(lambda : self.agent)):
                headers_[-1] = "User-Agent: " + self.agent
            # end if
            if (not php_empty(lambda : self.host)):
                if (not php_empty(lambda : self.port)):
                    headers_[-1] = "Host: " + self.host + ":" + self.port
                else:
                    headers_[-1] = "Host: " + self.host
                # end if
            # end if
            if (not php_empty(lambda : self.accept)):
                headers_[-1] = "Accept: " + self.accept
            # end if
            if (not php_empty(lambda : self.referer)):
                headers_[-1] = "Referer: " + self.referer
            # end if
            if (not php_empty(lambda : self.cookies)):
                if (not php_is_array(self.cookies)):
                    self.cookies = self.cookies
                # end if
                reset(self.cookies)
                if php_count(self.cookies) > 0:
                    cookie_str_ = "Cookie: "
                    for cookieKey_,cookieVal_ in self.cookies.items():
                        cookie_str_ += cookieKey_ + "=" + urlencode(cookieVal_) + "; "
                    # end for
                    headers_[-1] = php_substr(cookie_str_, 0, -2)
                # end if
            # end if
            if (not php_empty(lambda : self.rawheaders)):
                if (not php_is_array(self.rawheaders)):
                    self.rawheaders = self.rawheaders
                # end if
                while True:
                    headerKey_, headerVal_ = each(self.rawheaders)
                    if not (headerKey_, headerVal_):
                        break
                    # end if
                    headers_[-1] = headerKey_ + ": " + headerVal_
                # end while
            # end if
            if (not php_empty(lambda : content_type_)):
                if content_type_ == "multipart/form-data":
                    headers_[-1] = str("Content-type: ") + str(content_type_) + str("; boundary=") + self._mime_boundary
                else:
                    headers_[-1] = str("Content-type: ") + str(content_type_)
                # end if
            # end if
            if (not php_empty(lambda : body_)):
                headers_[-1] = "Content-length: " + php_strlen(body_)
            # end if
            if (not php_empty(lambda : self.user)) or (not php_empty(lambda : self.pass_)):
                headers_[-1] = "Authorization: BASIC " + php_base64_encode(self.user + ":" + self.pass_)
            # end if
            headerfile_ = php_tempnam(self.temp_dir, "sno")
            cmdline_params_ = "-k -D " + escapeshellarg(headerfile_)
            for header_ in headers_:
                cmdline_params_ += " -H " + escapeshellarg(header_)
            # end for
            if (not php_empty(lambda : body_)):
                cmdline_params_ += " -d " + escapeshellarg(body_)
            # end if
            if self.read_timeout > 0:
                cmdline_params_ += " -m " + escapeshellarg(self.read_timeout)
            # end if
            php_exec(self.curl_path + " " + cmdline_params_ + " " + escapeshellarg(URI_), results_, return_)
            if return_:
                self.error = str("Error: cURL could not retrieve the document, error ") + str(return_) + str(".")
                return False
            # end if
            results_ = php_implode("\r\n", results_)
            result_headers_ = file(str(headerfile_))
            self._redirectaddr = False
            self.headers = None
            currentHeader_ = 0
            while currentHeader_ < php_count(result_headers_):
                
                #// if a header begins with Location: or URI:, set the redirect
                if php_preg_match("/^(Location: |URI: )/i", result_headers_[currentHeader_]):
                    #// get URL portion of the redirect
                    php_preg_match("/^(Location: |URI:)\\s+(.*)/", chop(result_headers_[currentHeader_]), matches_)
                    #// look for :// in the Location header to see if hostname is included
                    if (not php_preg_match("|\\:\\/\\/|", matches_[2])):
                        #// no host in the path, so prepend
                        self._redirectaddr = URI_PARTS_["scheme"] + "://" + self.host + ":" + self.port
                        #// eliminate double slash
                        if (not php_preg_match("|^/|", matches_[2])):
                            self._redirectaddr += "/" + matches_[2]
                        else:
                            self._redirectaddr += matches_[2]
                        # end if
                    else:
                        self._redirectaddr = matches_[2]
                    # end if
                # end if
                if php_preg_match("|^HTTP/|", result_headers_[currentHeader_]):
                    self.response_code = result_headers_[currentHeader_]
                # end if
                self.headers[-1] = result_headers_[currentHeader_]
                currentHeader_ += 1
            # end while
            #// check if there is a redirect meta tag
            if php_preg_match("'<meta[\\s]*http-equiv[^>]*?content[\\s]*=[\\s]*[\"\\']?\\d+;[\\s]*URL[\\s]*=[\\s]*([^\"\\']*?)[\"\\']?>'i", results_, match_):
                self._redirectaddr = self._expandlinks(match_[1], URI_)
            # end if
            #// have we hit our frame depth and is there frame src to fetch?
            if self._framedepth < self.maxframes and preg_match_all("'<frame\\s+.*src[\\s]*=[\\'\"]?([^\\'\"\\>]+)'i", results_, match_):
                self.results[-1] = results_
                x_ = 0
                while x_ < php_count(match_[1]):
                    
                    self._frameurls[-1] = self._expandlinks(match_[1][x_], URI_PARTS_["scheme"] + "://" + self.host)
                    x_ += 1
                # end while
                #// have we already fetched framed content?
            elif php_is_array(self.results):
                self.results[-1] = results_
            else:
                self.results = results_
            # end if
            unlink(str(headerfile_))
            return True
        # end def _httpsrequest
        #// ======================================================================*\
#// Function:   setcookies()
        #// Purpose:    set cookies for a redirection
        #// \*======================================================================
        def setcookies(self):
            
            
            x_ = 0
            while x_ < php_count(self.headers):
                
                if php_preg_match("/^set-cookie:[\\s]+([^=]+)=([^;]+)/i", self.headers[x_], match_):
                    self.cookies[match_[1]] = urldecode(match_[2])
                # end if
                x_ += 1
            # end while
        # end def setcookies
        #// ======================================================================*\
#// Function:   _check_timeout
        #// Purpose:    checks whether timeout has occurred
        #// Input:      $fp file pointer
        #// \*======================================================================
        def _check_timeout(self, fp_=None):
            
            
            if self.read_timeout > 0:
                fp_status_ = socket_get_status(fp_)
                if fp_status_["timed_out"]:
                    self.timed_out = True
                    return True
                # end if
            # end if
            return False
        # end def _check_timeout
        #// ======================================================================*\
#// Function:   _connect
        #// Purpose:    make a socket connection
        #// Input:      $fp file pointer
        #// \*======================================================================
        def _connect(self, fp_=None):
            
            
            if (not php_empty(lambda : self.proxy_host)) and (not php_empty(lambda : self.proxy_port)):
                self._isproxy = True
                host_ = self.proxy_host
                port_ = self.proxy_port
            else:
                host_ = self.host
                port_ = self.port
            # end if
            self.status = 0
            fp_ = fsockopen(host_, port_, errno_, errstr_, self._fp_timeout)
            if fp_:
                #// socket connection succeeded
                return True
            else:
                #// socket connection failed
                self.status = errno_
                for case in Switch(errno_):
                    if case(-3):
                        self.error = "socket creation failed (-3)"
                    # end if
                    if case(-4):
                        self.error = "dns lookup failure (-4)"
                    # end if
                    if case(-5):
                        self.error = "connection refused or timed out (-5)"
                    # end if
                    if case():
                        self.error = "connection failed (" + errno_ + ")"
                    # end if
                # end for
                return False
            # end if
        # end def _connect
        #// ======================================================================*\
#// Function:   _disconnect
        #// Purpose:    disconnect a socket connection
        #// Input:      $fp file pointer
        #// \*======================================================================
        def _disconnect(self, fp_=None):
            
            
            return php_fclose(fp_)
        # end def _disconnect
        #// ======================================================================*\
#// Function:   _prepare_post_body
        #// Purpose:    Prepare post body according to encoding type
        #// Input:      $formvars  - form variables
        #// $formfiles - form upload files
        #// Output:     post body
        #// \*======================================================================
        def _prepare_post_body(self, formvars_=None, formfiles_=None):
            
            
            settype(formvars_, "array")
            settype(formfiles_, "array")
            postdata_ = ""
            if php_count(formvars_) == 0 and php_count(formfiles_) == 0:
                return
            # end if
            for case in Switch(self._submit_type):
                if case("application/x-www-form-urlencoded"):
                    reset(formvars_)
                    while True:
                        key_, val_ = each(formvars_)
                        if not (key_, val_):
                            break
                        # end if
                        if php_is_array(val_) or php_is_object(val_):
                            while True:
                                cur_key_, cur_val_ = each(val_)
                                if not (cur_key_, cur_val_):
                                    break
                                # end if
                                postdata_ += urlencode(key_) + "[]=" + urlencode(cur_val_) + "&"
                            # end while
                        else:
                            postdata_ += urlencode(key_) + "=" + urlencode(val_) + "&"
                        # end if
                    # end while
                    break
                # end if
                if case("multipart/form-data"):
                    self._mime_boundary = "Snoopy" + php_md5(php_uniqid(php_microtime()))
                    reset(formvars_)
                    while True:
                        key_, val_ = each(formvars_)
                        if not (key_, val_):
                            break
                        # end if
                        if php_is_array(val_) or php_is_object(val_):
                            while True:
                                cur_key_, cur_val_ = each(val_)
                                if not (cur_key_, cur_val_):
                                    break
                                # end if
                                postdata_ += "--" + self._mime_boundary + "\r\n"
                                postdata_ += str("Content-Disposition: form-data; name=\"") + str(key_) + str("\\[\\]\"\r\n\r\n")
                                postdata_ += str(cur_val_) + str("\r\n")
                            # end while
                        else:
                            postdata_ += "--" + self._mime_boundary + "\r\n"
                            postdata_ += str("Content-Disposition: form-data; name=\"") + str(key_) + str("\"\r\n\r\n")
                            postdata_ += str(val_) + str("\r\n")
                        # end if
                    # end while
                    reset(formfiles_)
                    while True:
                        field_name_, file_names_ = each(formfiles_)
                        if not (field_name_, file_names_):
                            break
                        # end if
                        settype(file_names_, "array")
                        while True:
                            file_name_ = each(file_names_)
                            if not (file_name_):
                                break
                            # end if
                            if (not php_is_readable(file_name_)):
                                continue
                            # end if
                            fp_ = fopen(file_name_, "r")
                            file_content_ = fread(fp_, filesize(file_name_))
                            php_fclose(fp_)
                            base_name_ = php_basename(file_name_)
                            postdata_ += "--" + self._mime_boundary + "\r\n"
                            postdata_ += str("Content-Disposition: form-data; name=\"") + str(field_name_) + str("\"; filename=\"") + str(base_name_) + str("\"\r\n\r\n")
                            postdata_ += str(file_content_) + str("\r\n")
                        # end while
                    # end while
                    postdata_ += "--" + self._mime_boundary + "--\r\n"
                    break
                # end if
            # end for
            return postdata_
        # end def _prepare_post_body
    # end class Snoopy
# end if
