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
        host = "www.php.net"
        port = 80
        proxy_host = ""
        proxy_port = ""
        proxy_user = ""
        proxy_pass = ""
        agent = "Snoopy v1.2.4"
        referer = ""
        cookies = Array()
        rawheaders = Array()
        maxredirs = 5
        lastredirectaddr = ""
        offsiteok = True
        maxframes = 0
        expandlinks = True
        passcookies = True
        user = ""
        pass_ = ""
        accept = "image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, */*"
        results = ""
        error = ""
        response_code = ""
        headers = Array()
        maxlength = 500000
        read_timeout = 0
        timed_out = False
        status = 0
        temp_dir = "/tmp"
        curl_path = "/usr/local/bin/curl"
        _maxlinelen = 4096
        _httpmethod = "GET"
        _httpversion = "HTTP/1.0"
        _submit_method = "POST"
        _submit_type = "application/x-www-form-urlencoded"
        _mime_boundary = ""
        _redirectaddr = False
        _redirectdepth = 0
        _frameurls = Array()
        _framedepth = 0
        _isproxy = False
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
        def fetch(self, URI=None):
            
            #// preg_match("|^([^:]+)://([^:/]+)(:[\d]+)*(.*)|",$URI,$URI_PARTS);
            URI_PARTS = php_parse_url(URI)
            if (not php_empty(lambda : URI_PARTS["user"])):
                self.user = URI_PARTS["user"]
            # end if
            if (not php_empty(lambda : URI_PARTS["pass"])):
                self.pass_ = URI_PARTS["pass"]
            # end if
            if php_empty(lambda : URI_PARTS["query"]):
                URI_PARTS["query"] = ""
            # end if
            if php_empty(lambda : URI_PARTS["path"]):
                URI_PARTS["path"] = ""
            # end if
            for case in Switch(php_strtolower(URI_PARTS["scheme"])):
                if case("http"):
                    self.host = URI_PARTS["host"]
                    if (not php_empty(lambda : URI_PARTS["port"])):
                        self.port = URI_PARTS["port"]
                    # end if
                    if self._connect(fp):
                        if self._isproxy:
                            #// using proxy, send entire URI
                            self._httprequest(URI, fp, URI, self._httpmethod)
                        else:
                            path = URI_PARTS["path"] + "?" + URI_PARTS["query"] if URI_PARTS["query"] else ""
                            #// no proxy, send only the path
                            self._httprequest(path, fp, URI, self._httpmethod)
                        # end if
                        self._disconnect(fp)
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
                            frameurls = self._frameurls
                            self._frameurls = Array()
                            while True:
                                frameurl = each(frameurls)
                                if not (frameurl):
                                    break
                                # end if
                                if self._framedepth < self.maxframes:
                                    self.fetch(frameurl)
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
                    self.host = URI_PARTS["host"]
                    if (not php_empty(lambda : URI_PARTS["port"])):
                        self.port = URI_PARTS["port"]
                    # end if
                    if self._isproxy:
                        #// using proxy, send entire URI
                        self._httpsrequest(URI, URI, self._httpmethod)
                    else:
                        path = URI_PARTS["path"] + "?" + URI_PARTS["query"] if URI_PARTS["query"] else ""
                        #// no proxy, send only the path
                        self._httpsrequest(path, URI, self._httpmethod)
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
                        frameurls = self._frameurls
                        self._frameurls = Array()
                        while True:
                            frameurl = each(frameurls)
                            if not (frameurl):
                                break
                            # end if
                            if self._framedepth < self.maxframes:
                                self.fetch(frameurl)
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
                    self.error = "Invalid protocol \"" + URI_PARTS["scheme"] + "\"\\n"
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
        def submit(self, URI=None, formvars="", formfiles=""):
            
            postdata = None
            postdata = self._prepare_post_body(formvars, formfiles)
            URI_PARTS = php_parse_url(URI)
            if (not php_empty(lambda : URI_PARTS["user"])):
                self.user = URI_PARTS["user"]
            # end if
            if (not php_empty(lambda : URI_PARTS["pass"])):
                self.pass_ = URI_PARTS["pass"]
            # end if
            if php_empty(lambda : URI_PARTS["query"]):
                URI_PARTS["query"] = ""
            # end if
            if php_empty(lambda : URI_PARTS["path"]):
                URI_PARTS["path"] = ""
            # end if
            for case in Switch(php_strtolower(URI_PARTS["scheme"])):
                if case("http"):
                    self.host = URI_PARTS["host"]
                    if (not php_empty(lambda : URI_PARTS["port"])):
                        self.port = URI_PARTS["port"]
                    # end if
                    if self._connect(fp):
                        if self._isproxy:
                            #// using proxy, send entire URI
                            self._httprequest(URI, fp, URI, self._submit_method, self._submit_type, postdata)
                        else:
                            path = URI_PARTS["path"] + "?" + URI_PARTS["query"] if URI_PARTS["query"] else ""
                            #// no proxy, send only the path
                            self._httprequest(path, fp, URI, self._submit_method, self._submit_type, postdata)
                        # end if
                        self._disconnect(fp)
                        if self._redirectaddr:
                            #// url was redirected, check if we've hit the max depth
                            if self.maxredirs > self._redirectdepth:
                                if (not php_preg_match("|^" + URI_PARTS["scheme"] + "://|", self._redirectaddr)):
                                    self._redirectaddr = self._expandlinks(self._redirectaddr, URI_PARTS["scheme"] + "://" + URI_PARTS["host"])
                                # end if
                                #// only follow redirect if it's on this site, or offsiteok is true
                                if php_preg_match("|^http://" + preg_quote(self.host) + "|i", self._redirectaddr) or self.offsiteok:
                                    #// follow the redirect
                                    self._redirectdepth += 1
                                    self.lastredirectaddr = self._redirectaddr
                                    if php_strpos(self._redirectaddr, "?") > 0:
                                        self.fetch(self._redirectaddr)
                                    else:
                                        self.submit(self._redirectaddr, formvars, formfiles)
                                    # end if
                                # end if
                            # end if
                        # end if
                        if self._framedepth < self.maxframes and php_count(self._frameurls) > 0:
                            frameurls = self._frameurls
                            self._frameurls = Array()
                            while True:
                                frameurl = each(frameurls)
                                if not (frameurl):
                                    break
                                # end if
                                if self._framedepth < self.maxframes:
                                    self.fetch(frameurl)
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
                    self.host = URI_PARTS["host"]
                    if (not php_empty(lambda : URI_PARTS["port"])):
                        self.port = URI_PARTS["port"]
                    # end if
                    if self._isproxy:
                        #// using proxy, send entire URI
                        self._httpsrequest(URI, URI, self._submit_method, self._submit_type, postdata)
                    else:
                        path = URI_PARTS["path"] + "?" + URI_PARTS["query"] if URI_PARTS["query"] else ""
                        #// no proxy, send only the path
                        self._httpsrequest(path, URI, self._submit_method, self._submit_type, postdata)
                    # end if
                    if self._redirectaddr:
                        #// url was redirected, check if we've hit the max depth
                        if self.maxredirs > self._redirectdepth:
                            if (not php_preg_match("|^" + URI_PARTS["scheme"] + "://|", self._redirectaddr)):
                                self._redirectaddr = self._expandlinks(self._redirectaddr, URI_PARTS["scheme"] + "://" + URI_PARTS["host"])
                            # end if
                            #// only follow redirect if it's on this site, or offsiteok is true
                            if php_preg_match("|^http://" + preg_quote(self.host) + "|i", self._redirectaddr) or self.offsiteok:
                                #// follow the redirect
                                self._redirectdepth += 1
                                self.lastredirectaddr = self._redirectaddr
                                if php_strpos(self._redirectaddr, "?") > 0:
                                    self.fetch(self._redirectaddr)
                                else:
                                    self.submit(self._redirectaddr, formvars, formfiles)
                                # end if
                            # end if
                        # end if
                    # end if
                    if self._framedepth < self.maxframes and php_count(self._frameurls) > 0:
                        frameurls = self._frameurls
                        self._frameurls = Array()
                        while True:
                            frameurl = each(frameurls)
                            if not (frameurl):
                                break
                            # end if
                            if self._framedepth < self.maxframes:
                                self.fetch(frameurl)
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
                    self.error = "Invalid protocol \"" + URI_PARTS["scheme"] + "\"\\n"
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
        def fetchlinks(self, URI=None):
            
            if self.fetch(URI):
                if self.lastredirectaddr:
                    URI = self.lastredirectaddr
                # end if
                if php_is_array(self.results):
                    x = 0
                    while x < php_count(self.results):
                        
                        self.results[x] = self._striplinks(self.results[x])
                        x += 1
                    # end while
                else:
                    self.results = self._striplinks(self.results)
                # end if
                if self.expandlinks:
                    self.results = self._expandlinks(self.results, URI)
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
        def fetchform(self, URI=None):
            
            if self.fetch(URI):
                if php_is_array(self.results):
                    x = 0
                    while x < php_count(self.results):
                        
                        self.results[x] = self._stripform(self.results[x])
                        x += 1
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
        def fetchtext(self, URI=None):
            
            if self.fetch(URI):
                if php_is_array(self.results):
                    x = 0
                    while x < php_count(self.results):
                        
                        self.results[x] = self._striptext(self.results[x])
                        x += 1
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
        def submitlinks(self, URI=None, formvars="", formfiles=""):
            
            if self.submit(URI, formvars, formfiles):
                if self.lastredirectaddr:
                    URI = self.lastredirectaddr
                # end if
                if php_is_array(self.results):
                    x = 0
                    while x < php_count(self.results):
                        
                        self.results[x] = self._striplinks(self.results[x])
                        if self.expandlinks:
                            self.results[x] = self._expandlinks(self.results[x], URI)
                        # end if
                        x += 1
                    # end while
                else:
                    self.results = self._striplinks(self.results)
                    if self.expandlinks:
                        self.results = self._expandlinks(self.results, URI)
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
        def submittext(self, URI=None, formvars="", formfiles=""):
            
            if self.submit(URI, formvars, formfiles):
                if self.lastredirectaddr:
                    URI = self.lastredirectaddr
                # end if
                if php_is_array(self.results):
                    x = 0
                    while x < php_count(self.results):
                        
                        self.results[x] = self._striptext(self.results[x])
                        if self.expandlinks:
                            self.results[x] = self._expandlinks(self.results[x], URI)
                        # end if
                        x += 1
                    # end while
                else:
                    self.results = self._striptext(self.results)
                    if self.expandlinks:
                        self.results = self._expandlinks(self.results, URI)
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
        def _striplinks(self, document=None):
            
            preg_match_all("""'<\\s*a\\s.*?href\\s*=\\s*            # find <a href=
            ([\"\\'])?                  # find single or double quote
            (?(1) (.*?)\\1 | ([^\\s\\>]+))      # if quote found, match up to next matching
            # quote, otherwise match up to next space
            'isx""", document, links)
            #// catenate the non-empty matches from the conditional subpattern
            while True:
                key, val = each(links[2])
                if not (key, val):
                    break
                # end if
                if (not php_empty(lambda : val)):
                    match[-1] = val
                # end if
            # end while
            while True:
                key, val = each(links[3])
                if not (key, val):
                    break
                # end if
                if (not php_empty(lambda : val)):
                    match[-1] = val
                # end if
            # end while
            #// return the links
            return match
        # end def _striplinks
        #// ======================================================================*\
#// Function:   _stripform
        #// Purpose:    strip the form elements from an html document
        #// Input:      $document   document to strip.
        #// Output:     $match      an array of the links
        #// \*======================================================================
        def _stripform(self, document=None):
            
            preg_match_all("""'<\\/?(FORM|INPUT|SELECT|TEXTAREA|(OPTION))[^<>]*>(?(2)(.*(?=<\\/?(option|select)[^<>]*>[
            ]*)|(?=[
            ]*))|(?=[
            ]*))'Usi""", document, elements)
            #// catenate the matches
            match = php_implode("\r\n", elements[0])
            #// return the links
            return match
        # end def _stripform
        #// ======================================================================*\
#// Function:   _striptext
        #// Purpose:    strip the text from an html document
        #// Input:      $document   document to strip.
        #// Output:     $text       the resulting text
        #// \*======================================================================
        def _striptext(self, document=None):
            
            #// I didn't use preg eval (//e) since that is only available in PHP 4.0.
            #// so, list your entities one by one here. I included some of the
            #// more common ones.
            search = Array("'<script[^>]*?>.*?</script>'si", "'<[\\/\\!]*?[^<>]*?>'si", "'([\r\n])[\\s]+'", "'&(quot|#34|#034|#x22);'i", "'&(amp|#38|#038|#x26);'i", "'&(lt|#60|#060|#x3c);'i", "'&(gt|#62|#062|#x3e);'i", "'&(nbsp|#160|#xa0);'i", "'&(iexcl|#161);'i", "'&(cent|#162);'i", "'&(pound|#163);'i", "'&(copy|#169);'i", "'&(reg|#174);'i", "'&(deg|#176);'i", "'&(#39|#039|#x27);'", "'&(euro|#8364);'i", "'&a(uml|UML);'", "'&o(uml|UML);'", "'&u(uml|UML);'", "'&A(uml|UML);'", "'&O(uml|UML);'", "'&U(uml|UML);'", "'&szlig;'i")
            replace = Array("", "", "\\1", "\"", "&", "<", ">", " ", chr(161), chr(162), chr(163), chr(169), chr(174), chr(176), chr(39), chr(128), chr(228), chr(246), chr(252), chr(196), chr(214), chr(220), chr(223))
            text = php_preg_replace(search, replace, document)
            return text
        # end def _striptext
        #// ======================================================================*\
#// Function:   _expandlinks
        #// Purpose:    expand each link into a fully qualified URL
        #// Input:      $links          the links to qualify
        #// $URI            the full URI to get the base from
        #// Output:     $expandedLinks  the expanded links
        #// \*======================================================================
        def _expandlinks(self, links=None, URI=None):
            
            php_preg_match("/^[^\\?]+/", URI, match)
            match = php_preg_replace("|/[^\\/\\.]+\\.[^\\/\\.]+$|", "", match[0])
            match = php_preg_replace("|/$|", "", match)
            match_part = php_parse_url(match)
            match_root = match_part["scheme"] + "://" + match_part["host"]
            search = Array("|^http://" + preg_quote(self.host) + "|i", "|^(\\/)|i", "|^(?!http://)(?!mailto:)|i", "|/\\./|", "|/[^\\/]+/\\.\\./|")
            replace = Array("", match_root + "/", match + "/", "/", "/")
            expandedLinks = php_preg_replace(search, replace, links)
            return expandedLinks
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
        def _httprequest(self, url=None, fp=None, URI=None, http_method=None, content_type="", body=""):
            
            cookie_headers = ""
            if self.passcookies and self._redirectaddr:
                self.setcookies()
            # end if
            URI_PARTS = php_parse_url(URI)
            if php_empty(lambda : url):
                url = "/"
            # end if
            headers = http_method + " " + url + " " + self._httpversion + "\r\n"
            if (not php_empty(lambda : self.agent)):
                headers += "User-Agent: " + self.agent + "\r\n"
            # end if
            if (not php_empty(lambda : self.host)) and (not (php_isset(lambda : self.rawheaders["Host"]))):
                headers += "Host: " + self.host
                if (not php_empty(lambda : self.port)) and self.port != 80:
                    headers += ":" + self.port
                # end if
                headers += "\r\n"
            # end if
            if (not php_empty(lambda : self.accept)):
                headers += "Accept: " + self.accept + "\r\n"
            # end if
            if (not php_empty(lambda : self.referer)):
                headers += "Referer: " + self.referer + "\r\n"
            # end if
            if (not php_empty(lambda : self.cookies)):
                if (not php_is_array(self.cookies)):
                    self.cookies = self.cookies
                # end if
                reset(self.cookies)
                if php_count(self.cookies) > 0:
                    cookie_headers += "Cookie: "
                    for cookieKey,cookieVal in self.cookies:
                        cookie_headers += cookieKey + "=" + urlencode(cookieVal) + "; "
                    # end for
                    headers += php_substr(cookie_headers, 0, -2) + "\r\n"
                # end if
            # end if
            if (not php_empty(lambda : self.rawheaders)):
                if (not php_is_array(self.rawheaders)):
                    self.rawheaders = self.rawheaders
                # end if
                while True:
                    headerKey, headerVal = each(self.rawheaders)
                    if not (headerKey, headerVal):
                        break
                    # end if
                    headers += headerKey + ": " + headerVal + "\r\n"
                # end while
            # end if
            if (not php_empty(lambda : content_type)):
                headers += str("Content-type: ") + str(content_type)
                if content_type == "multipart/form-data":
                    headers += "; boundary=" + self._mime_boundary
                # end if
                headers += "\r\n"
            # end if
            if (not php_empty(lambda : body)):
                headers += "Content-length: " + php_strlen(body) + "\r\n"
            # end if
            if (not php_empty(lambda : self.user)) or (not php_empty(lambda : self.pass_)):
                headers += "Authorization: Basic " + php_base64_encode(self.user + ":" + self.pass_) + "\r\n"
            # end if
            #// add proxy auth headers
            if (not php_empty(lambda : self.proxy_user)):
                headers += "Proxy-Authorization: " + "Basic " + php_base64_encode(self.proxy_user + ":" + self.proxy_pass) + "\r\n"
            # end if
            headers += "\r\n"
            #// set the read timeout if needed
            if self.read_timeout > 0:
                socket_set_timeout(fp, self.read_timeout)
            # end if
            self.timed_out = False
            fwrite(fp, headers + body, php_strlen(headers + body))
            self._redirectaddr = False
            self.headers = None
            while True:
                currentHeader = php_fgets(fp, self._maxlinelen)
                if not (currentHeader):
                    break
                # end if
                if self.read_timeout > 0 and self._check_timeout(fp):
                    self.status = -100
                    return False
                # end if
                if currentHeader == "\r\n":
                    break
                # end if
                #// if a header begins with Location: or URI:, set the redirect
                if php_preg_match("/^(Location:|URI:)/i", currentHeader):
                    #// get URL portion of the redirect
                    php_preg_match("/^(Location:|URI:)[ ]+(.*)/i", chop(currentHeader), matches)
                    #// look for :// in the Location header to see if hostname is included
                    if (not php_preg_match("|\\:\\/\\/|", matches[2])):
                        #// no host in the path, so prepend
                        self._redirectaddr = URI_PARTS["scheme"] + "://" + self.host + ":" + self.port
                        #// eliminate double slash
                        if (not php_preg_match("|^/|", matches[2])):
                            self._redirectaddr += "/" + matches[2]
                        else:
                            self._redirectaddr += matches[2]
                        # end if
                    else:
                        self._redirectaddr = matches[2]
                    # end if
                # end if
                if php_preg_match("|^HTTP/|", currentHeader):
                    if php_preg_match("|^HTTP/[^\\s]*\\s(.*?)\\s|", currentHeader, status):
                        self.status = status[1]
                    # end if
                    self.response_code = currentHeader
                # end if
                self.headers[-1] = currentHeader
            # end while
            results = ""
            while True:
                _data = fread(fp, self.maxlength)
                if php_strlen(_data) == 0:
                    break
                # end if
                results += _data
                
                if True:
                    break
                # end if
            # end while
            if self.read_timeout > 0 and self._check_timeout(fp):
                self.status = -100
                return False
            # end if
            #// check if there is a redirect meta tag
            if php_preg_match("'<meta[\\s]*http-equiv[^>]*?content[\\s]*=[\\s]*[\"\\']?\\d+;[\\s]*URL[\\s]*=[\\s]*([^\"\\']*?)[\"\\']?>'i", results, match):
                self._redirectaddr = self._expandlinks(match[1], URI)
            # end if
            #// have we hit our frame depth and is there frame src to fetch?
            if self._framedepth < self.maxframes and preg_match_all("'<frame\\s+.*src[\\s]*=[\\'\"]?([^\\'\"\\>]+)'i", results, match):
                self.results[-1] = results
                x = 0
                while x < php_count(match[1]):
                    
                    self._frameurls[-1] = self._expandlinks(match[1][x], URI_PARTS["scheme"] + "://" + self.host)
                    x += 1
                # end while
                #// have we already fetched framed content?
            elif php_is_array(self.results):
                self.results[-1] = results
            else:
                self.results = results
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
        def _httpsrequest(self, url=None, URI=None, http_method=None, content_type="", body=""):
            
            if self.passcookies and self._redirectaddr:
                self.setcookies()
            # end if
            headers = Array()
            URI_PARTS = php_parse_url(URI)
            if php_empty(lambda : url):
                url = "/"
            # end if
            #// GET ... header not needed for curl
            #// $headers[] = $http_method." ".$url." ".$this->_httpversion;
            if (not php_empty(lambda : self.agent)):
                headers[-1] = "User-Agent: " + self.agent
            # end if
            if (not php_empty(lambda : self.host)):
                if (not php_empty(lambda : self.port)):
                    headers[-1] = "Host: " + self.host + ":" + self.port
                else:
                    headers[-1] = "Host: " + self.host
                # end if
            # end if
            if (not php_empty(lambda : self.accept)):
                headers[-1] = "Accept: " + self.accept
            # end if
            if (not php_empty(lambda : self.referer)):
                headers[-1] = "Referer: " + self.referer
            # end if
            if (not php_empty(lambda : self.cookies)):
                if (not php_is_array(self.cookies)):
                    self.cookies = self.cookies
                # end if
                reset(self.cookies)
                if php_count(self.cookies) > 0:
                    cookie_str = "Cookie: "
                    for cookieKey,cookieVal in self.cookies:
                        cookie_str += cookieKey + "=" + urlencode(cookieVal) + "; "
                    # end for
                    headers[-1] = php_substr(cookie_str, 0, -2)
                # end if
            # end if
            if (not php_empty(lambda : self.rawheaders)):
                if (not php_is_array(self.rawheaders)):
                    self.rawheaders = self.rawheaders
                # end if
                while True:
                    headerKey, headerVal = each(self.rawheaders)
                    if not (headerKey, headerVal):
                        break
                    # end if
                    headers[-1] = headerKey + ": " + headerVal
                # end while
            # end if
            if (not php_empty(lambda : content_type)):
                if content_type == "multipart/form-data":
                    headers[-1] = str("Content-type: ") + str(content_type) + str("; boundary=") + self._mime_boundary
                else:
                    headers[-1] = str("Content-type: ") + str(content_type)
                # end if
            # end if
            if (not php_empty(lambda : body)):
                headers[-1] = "Content-length: " + php_strlen(body)
            # end if
            if (not php_empty(lambda : self.user)) or (not php_empty(lambda : self.pass_)):
                headers[-1] = "Authorization: BASIC " + php_base64_encode(self.user + ":" + self.pass_)
            # end if
            headerfile = php_tempnam(self.temp_dir, "sno")
            cmdline_params = "-k -D " + escapeshellarg(headerfile)
            for header in headers:
                cmdline_params += " -H " + escapeshellarg(header)
            # end for
            if (not php_empty(lambda : body)):
                cmdline_params += " -d " + escapeshellarg(body)
            # end if
            if self.read_timeout > 0:
                cmdline_params += " -m " + escapeshellarg(self.read_timeout)
            # end if
            exec(self.curl_path + " " + cmdline_params + " " + escapeshellarg(URI), results, return_)
            if return_:
                self.error = str("Error: cURL could not retrieve the document, error ") + str(return_) + str(".")
                return False
            # end if
            results = php_implode("\r\n", results)
            result_headers = file(str(headerfile))
            self._redirectaddr = False
            self.headers = None
            currentHeader = 0
            while currentHeader < php_count(result_headers):
                
                #// if a header begins with Location: or URI:, set the redirect
                if php_preg_match("/^(Location: |URI: )/i", result_headers[currentHeader]):
                    #// get URL portion of the redirect
                    php_preg_match("/^(Location: |URI:)\\s+(.*)/", chop(result_headers[currentHeader]), matches)
                    #// look for :// in the Location header to see if hostname is included
                    if (not php_preg_match("|\\:\\/\\/|", matches[2])):
                        #// no host in the path, so prepend
                        self._redirectaddr = URI_PARTS["scheme"] + "://" + self.host + ":" + self.port
                        #// eliminate double slash
                        if (not php_preg_match("|^/|", matches[2])):
                            self._redirectaddr += "/" + matches[2]
                        else:
                            self._redirectaddr += matches[2]
                        # end if
                    else:
                        self._redirectaddr = matches[2]
                    # end if
                # end if
                if php_preg_match("|^HTTP/|", result_headers[currentHeader]):
                    self.response_code = result_headers[currentHeader]
                # end if
                self.headers[-1] = result_headers[currentHeader]
                currentHeader += 1
            # end while
            #// check if there is a redirect meta tag
            if php_preg_match("'<meta[\\s]*http-equiv[^>]*?content[\\s]*=[\\s]*[\"\\']?\\d+;[\\s]*URL[\\s]*=[\\s]*([^\"\\']*?)[\"\\']?>'i", results, match):
                self._redirectaddr = self._expandlinks(match[1], URI)
            # end if
            #// have we hit our frame depth and is there frame src to fetch?
            if self._framedepth < self.maxframes and preg_match_all("'<frame\\s+.*src[\\s]*=[\\'\"]?([^\\'\"\\>]+)'i", results, match):
                self.results[-1] = results
                x = 0
                while x < php_count(match[1]):
                    
                    self._frameurls[-1] = self._expandlinks(match[1][x], URI_PARTS["scheme"] + "://" + self.host)
                    x += 1
                # end while
                #// have we already fetched framed content?
            elif php_is_array(self.results):
                self.results[-1] = results
            else:
                self.results = results
            # end if
            unlink(str(headerfile))
            return True
        # end def _httpsrequest
        #// ======================================================================*\
#// Function:   setcookies()
        #// Purpose:    set cookies for a redirection
        #// \*======================================================================
        def setcookies(self):
            
            x = 0
            while x < php_count(self.headers):
                
                if php_preg_match("/^set-cookie:[\\s]+([^=]+)=([^;]+)/i", self.headers[x], match):
                    self.cookies[match[1]] = urldecode(match[2])
                # end if
                x += 1
            # end while
        # end def setcookies
        #// ======================================================================*\
#// Function:   _check_timeout
        #// Purpose:    checks whether timeout has occurred
        #// Input:      $fp file pointer
        #// \*======================================================================
        def _check_timeout(self, fp=None):
            
            if self.read_timeout > 0:
                fp_status = socket_get_status(fp)
                if fp_status["timed_out"]:
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
        def _connect(self, fp=None):
            
            if (not php_empty(lambda : self.proxy_host)) and (not php_empty(lambda : self.proxy_port)):
                self._isproxy = True
                host = self.proxy_host
                port = self.proxy_port
            else:
                host = self.host
                port = self.port
            # end if
            self.status = 0
            fp = fsockopen(host, port, errno, errstr, self._fp_timeout)
            if fp:
                #// socket connection succeeded
                return True
            else:
                #// socket connection failed
                self.status = errno
                for case in Switch(errno):
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
                        self.error = "connection failed (" + errno + ")"
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
        def _disconnect(self, fp=None):
            
            return php_fclose(fp)
        # end def _disconnect
        #// ======================================================================*\
#// Function:   _prepare_post_body
        #// Purpose:    Prepare post body according to encoding type
        #// Input:      $formvars  - form variables
        #// $formfiles - form upload files
        #// Output:     post body
        #// \*======================================================================
        def _prepare_post_body(self, formvars=None, formfiles=None):
            
            settype(formvars, "array")
            settype(formfiles, "array")
            postdata = ""
            if php_count(formvars) == 0 and php_count(formfiles) == 0:
                return
            # end if
            for case in Switch(self._submit_type):
                if case("application/x-www-form-urlencoded"):
                    reset(formvars)
                    while True:
                        key, val = each(formvars)
                        if not (key, val):
                            break
                        # end if
                        if php_is_array(val) or php_is_object(val):
                            while True:
                                cur_key, cur_val = each(val)
                                if not (cur_key, cur_val):
                                    break
                                # end if
                                postdata += urlencode(key) + "[]=" + urlencode(cur_val) + "&"
                            # end while
                        else:
                            postdata += urlencode(key) + "=" + urlencode(val) + "&"
                        # end if
                    # end while
                    break
                # end if
                if case("multipart/form-data"):
                    self._mime_boundary = "Snoopy" + php_md5(uniqid(php_microtime()))
                    reset(formvars)
                    while True:
                        key, val = each(formvars)
                        if not (key, val):
                            break
                        # end if
                        if php_is_array(val) or php_is_object(val):
                            while True:
                                cur_key, cur_val = each(val)
                                if not (cur_key, cur_val):
                                    break
                                # end if
                                postdata += "--" + self._mime_boundary + "\r\n"
                                postdata += str("Content-Disposition: form-data; name=\"") + str(key) + str("\\[\\]\"\r\n\r\n")
                                postdata += str(cur_val) + str("\r\n")
                            # end while
                        else:
                            postdata += "--" + self._mime_boundary + "\r\n"
                            postdata += str("Content-Disposition: form-data; name=\"") + str(key) + str("\"\r\n\r\n")
                            postdata += str(val) + str("\r\n")
                        # end if
                    # end while
                    reset(formfiles)
                    while True:
                        field_name, file_names = each(formfiles)
                        if not (field_name, file_names):
                            break
                        # end if
                        settype(file_names, "array")
                        while True:
                            file_name = each(file_names)
                            if not (file_name):
                                break
                            # end if
                            if (not php_is_readable(file_name)):
                                continue
                            # end if
                            fp = fopen(file_name, "r")
                            file_content = fread(fp, filesize(file_name))
                            php_fclose(fp)
                            base_name = php_basename(file_name)
                            postdata += "--" + self._mime_boundary + "\r\n"
                            postdata += str("Content-Disposition: form-data; name=\"") + str(field_name) + str("\"; filename=\"") + str(base_name) + str("\"\r\n\r\n")
                            postdata += str(file_content) + str("\r\n")
                        # end while
                    # end while
                    postdata += "--" + self._mime_boundary + "--\r\n"
                    break
                # end if
            # end for
            return postdata
        # end def _prepare_post_body
    # end class Snoopy
# end if
