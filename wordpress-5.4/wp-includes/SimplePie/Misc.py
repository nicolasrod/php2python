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
#// Miscellanous utilities
#// 
#// @package SimplePie
#//
class SimplePie_Misc():
    @classmethod
    def time_hms(self, seconds=None):
        
        time = ""
        hours = floor(seconds / 3600)
        remainder = seconds % 3600
        if hours > 0:
            time += hours + ":"
        # end if
        minutes = floor(remainder / 60)
        seconds = remainder % 60
        if minutes < 10 and hours > 0:
            minutes = "0" + minutes
        # end if
        if seconds < 10:
            seconds = "0" + seconds
        # end if
        time += minutes + ":"
        time += seconds
        return time
    # end def time_hms
    @classmethod
    def absolutize_url(self, relative=None, base=None):
        
        iri = SimplePie_IRI.absolutize(php_new_class("SimplePie_IRI", lambda : SimplePie_IRI(base)), relative)
        if iri == False:
            return False
        # end if
        return iri.get_uri()
    # end def absolutize_url
    #// 
    #// Get a HTML/XML element from a HTML string
    #// 
    #// @deprecated Use DOMDocument instead (parsing HTML with regex is bad!)
    #// @param string $realname Element name (including namespace prefix if applicable)
    #// @param string $string HTML document
    #// @return array
    #//
    @classmethod
    def get_element(self, realname=None, string=None):
        
        return_ = Array()
        name = preg_quote(realname, "/")
        if preg_match_all(str("/<(") + str(name) + str(")") + SIMPLEPIE_PCRE_HTML_ATTRIBUTE + str("(>(.*)<\\/") + str(name) + str(">|(\\/)?>)/siU"), string, matches, PREG_SET_ORDER | PREG_OFFSET_CAPTURE):
            i = 0
            total_matches = php_count(matches)
            while i < total_matches:
                
                return_[i]["tag"] = realname
                return_[i]["full"] = matches[i][0][0]
                return_[i]["offset"] = matches[i][0][1]
                if php_strlen(matches[i][3][0]) <= 2:
                    return_[i]["self_closing"] = True
                else:
                    return_[i]["self_closing"] = False
                    return_[i]["content"] = matches[i][4][0]
                # end if
                return_[i]["attribs"] = Array()
                if (php_isset(lambda : matches[i][2][0])) and preg_match_all("/[\\x09\\x0A\\x0B\\x0C\\x0D\\x20]+([^\\x09\\x0A\\x0B\\x0C\\x0D\\x20\\x2F\\x3E][^\\x09\\x0A\\x0B\\x0C\\x0D\\x20\\x2F\\x3D\\x3E]*)(?:[\\x09\\x0A\\x0B\\x0C\\x0D\\x20]*=[\\x09\\x0A\\x0B\\x0C\\x0D\\x20]*(?:\"([^\"]*)\"|'([^']*)'|([^\\x09\\x0A\\x0B\\x0C\\x0D\\x20\\x22\\x27\\x3E][^\\x09\\x0A\\x0B\\x0C\\x0D\\x20\\x3E]*)?))?/", " " + matches[i][2][0] + " ", attribs, PREG_SET_ORDER):
                    j = 0
                    total_attribs = php_count(attribs)
                    while j < total_attribs:
                        
                        if php_count(attribs[j]) == 2:
                            attribs[j][2] = attribs[j][1]
                        # end if
                        return_[i]["attribs"][php_strtolower(attribs[j][1])]["data"] = SimplePie_Misc.entities_decode(php_end(attribs[j]))
                        j += 1
                    # end while
                # end if
                i += 1
            # end while
        # end if
        return return_
    # end def get_element
    @classmethod
    def element_implode(self, element=None):
        
        full = str("<") + str(element["tag"])
        for key,value in element["attribs"]:
            key = php_strtolower(key)
            full += str(" ") + str(key) + str("=\"") + htmlspecialchars(value["data"]) + "\""
        # end for
        if element["self_closing"]:
            full += " />"
        else:
            full += str(">") + str(element["content"]) + str("</") + str(element["tag"]) + str(">")
        # end if
        return full
    # end def element_implode
    @classmethod
    def error(self, message=None, level=None, file=None, line=None):
        
        if php_ini_get("error_reporting") & level > 0:
            for case in Switch(level):
                if case(E_USER_ERROR):
                    note = "PHP Error"
                    break
                # end if
                if case(E_USER_WARNING):
                    note = "PHP Warning"
                    break
                # end if
                if case(E_USER_NOTICE):
                    note = "PHP Notice"
                    break
                # end if
                if case():
                    note = "Unknown Error"
                    break
                # end if
            # end for
            log_error = True
            if (not php_function_exists("error_log")):
                log_error = False
            # end if
            log_file = php_no_error(lambda: php_ini_get("error_log"))
            if (not php_empty(lambda : log_file)) and "syslog" != log_file and (not php_no_error(lambda: php_is_writable(log_file))):
                log_error = False
            # end if
            if log_error:
                php_no_error(lambda: php_error_log(str(note) + str(": ") + str(message) + str(" in ") + str(file) + str(" on line ") + str(line), 0))
            # end if
        # end if
        return message
    # end def error
    @classmethod
    def fix_protocol(self, url=None, http=1):
        
        url = SimplePie_Misc.normalize_url(url)
        parsed = SimplePie_Misc.parse_url(url)
        if parsed["scheme"] != "" and parsed["scheme"] != "http" and parsed["scheme"] != "https":
            return SimplePie_Misc.fix_protocol(SimplePie_Misc.compress_parse_url("http", parsed["authority"], parsed["path"], parsed["query"], parsed["fragment"]), http)
        # end if
        if parsed["scheme"] == "" and parsed["authority"] == "" and (not php_file_exists(url)):
            return SimplePie_Misc.fix_protocol(SimplePie_Misc.compress_parse_url("http", parsed["path"], "", parsed["query"], parsed["fragment"]), http)
        # end if
        if http == 2 and parsed["scheme"] != "":
            return str("feed:") + str(url)
        elif http == 3 and php_strtolower(parsed["scheme"]) == "http":
            return php_substr_replace(url, "podcast", 0, 4)
        elif http == 4 and php_strtolower(parsed["scheme"]) == "http":
            return php_substr_replace(url, "itpc", 0, 4)
        else:
            return url
        # end if
    # end def fix_protocol
    @classmethod
    def parse_url(self, url=None):
        
        iri = php_new_class("SimplePie_IRI", lambda : SimplePie_IRI(url))
        return Array({"scheme": str(iri.scheme), "authority": str(iri.authority), "path": str(iri.path), "query": str(iri.query), "fragment": str(iri.fragment)})
    # end def parse_url
    @classmethod
    def compress_parse_url(self, scheme="", authority="", path="", query="", fragment=""):
        
        iri = php_new_class("SimplePie_IRI", lambda : SimplePie_IRI(""))
        iri.scheme = scheme
        iri.authority = authority
        iri.path = path
        iri.query = query
        iri.fragment = fragment
        return iri.get_uri()
    # end def compress_parse_url
    @classmethod
    def normalize_url(self, url=None):
        
        iri = php_new_class("SimplePie_IRI", lambda : SimplePie_IRI(url))
        return iri.get_uri()
    # end def normalize_url
    @classmethod
    def percent_encoding_normalization(self, match=None):
        
        integer = hexdec(match[1])
        if integer >= 65 and integer <= 90 or integer >= 97 and integer <= 122 or integer >= 48 and integer <= 57 or integer == 45 or integer == 46 or integer == 95 or integer == 126:
            return chr(integer)
        else:
            return php_strtoupper(match[0])
        # end if
    # end def percent_encoding_normalization
    #// 
    #// Converts a Windows-1252 encoded string to a UTF-8 encoded string
    #// 
    #// @static
    #// @param string $string Windows-1252 encoded string
    #// @return string UTF-8 encoded string
    #//
    @classmethod
    def windows_1252_to_utf8(self, string=None):
        
        convert_table = Array({"": "â¬", "": "ï¿½", "": "â", "": "Æ", "": "â", "": "â¦", "": "â ", "": "â¡", "": "Ë", "": "â°", "": "Å ", "": "â¹", "": "Å", "": "ï¿½", "": "Å½", "": "ï¿½", "": "ï¿½", "": "â", "": "â", "": "â", "": "â", "": "â¢", "": "â", "": "â", "": "Ë", "": "â¢", "": "Å¡", "": "âº", "": "Å", "": "ï¿½", "": "Å¾", "": "Å¸", " ": "Â ", "¡": "Â¡", "¢": "Â¢", "£": "Â£", "¤": "Â¤", "¥": "Â¥", "¦": "Â¦", "§": "Â§", "¨": "Â¨", "©": "Â©", "ª": "Âª", "«": "Â«", "¬": "Â¬", "­": "Â­", "®": "Â®", "¯": "Â¯", "°": "Â°", "±": "Â±", "²": "Â²", "³": "Â³", "´": "Â´", "µ": "Âµ", "¶": "Â¶", "·": "Â·", "¸": "Â¸", "¹": "Â¹", "º": "Âº", "»": "Â»", "¼": "Â¼", "½": "Â½", "¾": "Â¾", "¿": "Â¿", "À": "Ã", "Á": "Ã", "Â": "Ã", "Ã": "Ã", "Ä": "Ã", "Å": "Ã", "Æ": "Ã", "Ç": "Ã", "È": "Ã", "É": "Ã", "Ê": "Ã", "Ë": "Ã", "Ì": "Ã", "Í": "Ã", "Î": "Ã", "Ï": "Ã", "Ð": "Ã", "Ñ": "Ã", "Ò": "Ã", "Ó": "Ã", "Ô": "Ã", "Õ": "Ã", "Ö": "Ã", "×": "Ã", "Ø": "Ã", "Ù": "Ã", "Ú": "Ã", "Û": "Ã", "Ü": "Ã", "Ý": "Ã", "Þ": "Ã", "ß": "Ã", "à": "Ã ", "á": "Ã¡", "â": "Ã¢", "ã": "Ã£", "ä": "Ã¤", "å": "Ã¥", "æ": "Ã¦", "ç": "Ã§", "è": "Ã¨", "é": "Ã©", "ê": "Ãª", "ë": "Ã«", "ì": "Ã¬", "í": "Ã­", "î": "Ã®", "ï": "Ã¯", "ð": "Ã°", "ñ": "Ã±", "ò": "Ã²", "ó": "Ã³", "ô": "Ã´", "õ": "Ãµ", "ö": "Ã¶", "÷": "Ã·", "ø": "Ã¸", "ù": "Ã¹", "ú": "Ãº", "û": "Ã»", "ü": "Ã¼", "ý": "Ã½", "þ": "Ã¾", "ÿ": "Ã¿"})
        return php_strtr(string, convert_table)
    # end def windows_1252_to_utf8
    #// 
    #// Change a string from one encoding to another
    #// 
    #// @param string $data Raw data in $input encoding
    #// @param string $input Encoding of $data
    #// @param string $output Encoding you want
    #// @return string|boolean False if we can't convert it
    #//
    @classmethod
    def change_encoding(self, data=None, input=None, output=None):
        
        input = SimplePie_Misc.encoding(input)
        output = SimplePie_Misc.encoding(output)
        #// We fail to fail on non US-ASCII bytes
        if input == "US-ASCII":
            non_ascii_octects = ""
            if (not non_ascii_octects):
                i = 128
                while i <= 255:
                    
                    non_ascii_octects += chr(i)
                    i += 1
                # end while
            # end if
            data = php_substr(data, 0, strcspn(data, non_ascii_octects))
        # end if
        #// This is first, as behaviour of this is completely predictable
        if input == "windows-1252" and output == "UTF-8":
            return SimplePie_Misc.windows_1252_to_utf8(data)
            #// This is second, as behaviour of this varies only with PHP version (the middle part of this expression checks the encoding is supported).
        elif php_function_exists("mb_convert_encoding") and SimplePie_Misc.change_encoding_mbstring(data, input, output):
            return_ = SimplePie_Misc.change_encoding_mbstring(data, input, output)
            return return_
            #// This is last, as behaviour of this varies with OS userland and PHP version
        elif php_function_exists("iconv") and SimplePie_Misc.change_encoding_iconv(data, input, output):
            return_ = SimplePie_Misc.change_encoding_iconv(data, input, output)
            return return_
        else:
            return False
        # end if
    # end def change_encoding
    def change_encoding_mbstring(self, data=None, input=None, output=None):
        
        if input == "windows-949":
            input = "EUC-KR"
        # end if
        if output == "windows-949":
            output = "EUC-KR"
        # end if
        if input == "Windows-31J":
            input = "SJIS"
        # end if
        if output == "Windows-31J":
            output = "SJIS"
        # end if
        #// Check that the encoding is supported
        if php_no_error(lambda: mb_convert_encoding("", "UTF-16BE", input)) == " ":
            return False
        # end if
        if (not php_in_array(input, mb_list_encodings())):
            return False
        # end if
        #// Let's do some conversion
        return_ = php_no_error(lambda: mb_convert_encoding(data, output, input))
        if return_:
            return return_
        # end if
        return False
    # end def change_encoding_mbstring
    def change_encoding_iconv(self, data=None, input=None, output=None):
        
        return php_no_error(lambda: iconv(input, output, data))
    # end def change_encoding_iconv
    #// 
    #// Normalize an encoding name
    #// 
    #// This is automatically generated by create.php
    #// 
    #// To generate it, run `php create.php` on the command line, and copy the
    #// output to replace this function.
    #// 
    #// @param string $charset Character set to standardise
    #// @return string Standardised name
    #//
    @classmethod
    def encoding(self, charset=None):
        
        #// Normalization from UTS #22
        for case in Switch(php_strtolower(php_preg_replace("/(?:[^a-zA-Z0-9]+|([^0-9])0+)/", "\\1", charset))):
            if case("adobestandardencoding"):
                pass
            # end if
            if case("csadobestandardencoding"):
                return "Adobe-Standard-Encoding"
            # end if
            if case("adobesymbolencoding"):
                pass
            # end if
            if case("cshppsmath"):
                return "Adobe-Symbol-Encoding"
            # end if
            if case("ami1251"):
                pass
            # end if
            if case("amiga1251"):
                return "Amiga-1251"
            # end if
            if case("ansix31101983"):
                pass
            # end if
            if case("csat5001983"):
                pass
            # end if
            if case("csiso99naplps"):
                pass
            # end if
            if case("isoir99"):
                pass
            # end if
            if case("naplps"):
                return "ANSI_X3.110-1983"
            # end if
            if case("arabic7"):
                pass
            # end if
            if case("asmo449"):
                pass
            # end if
            if case("csiso89asmo449"):
                pass
            # end if
            if case("iso9036"):
                pass
            # end if
            if case("isoir89"):
                return "ASMO_449"
            # end if
            if case("big5"):
                pass
            # end if
            if case("csbig5"):
                return "Big5"
            # end if
            if case("big5hkscs"):
                return "Big5-HKSCS"
            # end if
            if case("bocu1"):
                pass
            # end if
            if case("csbocu1"):
                return "BOCU-1"
            # end if
            if case("brf"):
                pass
            # end if
            if case("csbrf"):
                return "BRF"
            # end if
            if case("bs4730"):
                pass
            # end if
            if case("csiso4unitedkingdom"):
                pass
            # end if
            if case("gb"):
                pass
            # end if
            if case("iso646gb"):
                pass
            # end if
            if case("isoir4"):
                pass
            # end if
            if case("uk"):
                return "BS_4730"
            # end if
            if case("bsviewdata"):
                pass
            # end if
            if case("csiso47bsviewdata"):
                pass
            # end if
            if case("isoir47"):
                return "BS_viewdata"
            # end if
            if case("cesu8"):
                pass
            # end if
            if case("cscesu8"):
                return "CESU-8"
            # end if
            if case("ca"):
                pass
            # end if
            if case("csa71"):
                pass
            # end if
            if case("csaz243419851"):
                pass
            # end if
            if case("csiso121canadian1"):
                pass
            # end if
            if case("iso646ca"):
                pass
            # end if
            if case("isoir121"):
                return "CSA_Z243.4-1985-1"
            # end if
            if case("csa72"):
                pass
            # end if
            if case("csaz243419852"):
                pass
            # end if
            if case("csiso122canadian2"):
                pass
            # end if
            if case("iso646ca2"):
                pass
            # end if
            if case("isoir122"):
                return "CSA_Z243.4-1985-2"
            # end if
            if case("csaz24341985gr"):
                pass
            # end if
            if case("csiso123csaz24341985gr"):
                pass
            # end if
            if case("isoir123"):
                return "CSA_Z243.4-1985-gr"
            # end if
            if case("csiso139csn369103"):
                pass
            # end if
            if case("csn369103"):
                pass
            # end if
            if case("isoir139"):
                return "CSN_369103"
            # end if
            if case("csdecmcs"):
                pass
            # end if
            if case("dec"):
                pass
            # end if
            if case("decmcs"):
                return "DEC-MCS"
            # end if
            if case("csiso21german"):
                pass
            # end if
            if case("de"):
                pass
            # end if
            if case("din66003"):
                pass
            # end if
            if case("iso646de"):
                pass
            # end if
            if case("isoir21"):
                return "DIN_66003"
            # end if
            if case("csdkus"):
                pass
            # end if
            if case("dkus"):
                return "dk-us"
            # end if
            if case("csiso646danish"):
                pass
            # end if
            if case("dk"):
                pass
            # end if
            if case("ds2089"):
                pass
            # end if
            if case("iso646dk"):
                return "DS_2089"
            # end if
            if case("csibmebcdicatde"):
                pass
            # end if
            if case("ebcdicatde"):
                return "EBCDIC-AT-DE"
            # end if
            if case("csebcdicatdea"):
                pass
            # end if
            if case("ebcdicatdea"):
                return "EBCDIC-AT-DE-A"
            # end if
            if case("csebcdiccafr"):
                pass
            # end if
            if case("ebcdiccafr"):
                return "EBCDIC-CA-FR"
            # end if
            if case("csebcdicdkno"):
                pass
            # end if
            if case("ebcdicdkno"):
                return "EBCDIC-DK-NO"
            # end if
            if case("csebcdicdknoa"):
                pass
            # end if
            if case("ebcdicdknoa"):
                return "EBCDIC-DK-NO-A"
            # end if
            if case("csebcdices"):
                pass
            # end if
            if case("ebcdices"):
                return "EBCDIC-ES"
            # end if
            if case("csebcdicesa"):
                pass
            # end if
            if case("ebcdicesa"):
                return "EBCDIC-ES-A"
            # end if
            if case("csebcdicess"):
                pass
            # end if
            if case("ebcdicess"):
                return "EBCDIC-ES-S"
            # end if
            if case("csebcdicfise"):
                pass
            # end if
            if case("ebcdicfise"):
                return "EBCDIC-FI-SE"
            # end if
            if case("csebcdicfisea"):
                pass
            # end if
            if case("ebcdicfisea"):
                return "EBCDIC-FI-SE-A"
            # end if
            if case("csebcdicfr"):
                pass
            # end if
            if case("ebcdicfr"):
                return "EBCDIC-FR"
            # end if
            if case("csebcdicit"):
                pass
            # end if
            if case("ebcdicit"):
                return "EBCDIC-IT"
            # end if
            if case("csebcdicpt"):
                pass
            # end if
            if case("ebcdicpt"):
                return "EBCDIC-PT"
            # end if
            if case("csebcdicuk"):
                pass
            # end if
            if case("ebcdicuk"):
                return "EBCDIC-UK"
            # end if
            if case("csebcdicus"):
                pass
            # end if
            if case("ebcdicus"):
                return "EBCDIC-US"
            # end if
            if case("csiso111ecmacyrillic"):
                pass
            # end if
            if case("ecmacyrillic"):
                pass
            # end if
            if case("isoir111"):
                pass
            # end if
            if case("koi8e"):
                return "ECMA-cyrillic"
            # end if
            if case("csiso17spanish"):
                pass
            # end if
            if case("es"):
                pass
            # end if
            if case("iso646es"):
                pass
            # end if
            if case("isoir17"):
                return "ES"
            # end if
            if case("csiso85spanish2"):
                pass
            # end if
            if case("es2"):
                pass
            # end if
            if case("iso646es2"):
                pass
            # end if
            if case("isoir85"):
                return "ES2"
            # end if
            if case("cseucpkdfmtjapanese"):
                pass
            # end if
            if case("eucjp"):
                pass
            # end if
            if case("extendedunixcodepackedformatforjapanese"):
                return "EUC-JP"
            # end if
            if case("cseucfixwidjapanese"):
                pass
            # end if
            if case("extendedunixcodefixedwidthforjapanese"):
                return "Extended_UNIX_Code_Fixed_Width_for_Japanese"
            # end if
            if case("gb18030"):
                return "GB18030"
            # end if
            if case("chinese"):
                pass
            # end if
            if case("cp936"):
                pass
            # end if
            if case("csgb2312"):
                pass
            # end if
            if case("csiso58gb231280"):
                pass
            # end if
            if case("gb2312"):
                pass
            # end if
            if case("gb231280"):
                pass
            # end if
            if case("gbk"):
                pass
            # end if
            if case("isoir58"):
                pass
            # end if
            if case("ms936"):
                pass
            # end if
            if case("windows936"):
                return "GBK"
            # end if
            if case("cn"):
                pass
            # end if
            if case("csiso57gb1988"):
                pass
            # end if
            if case("gb198880"):
                pass
            # end if
            if case("iso646cn"):
                pass
            # end if
            if case("isoir57"):
                return "GB_1988-80"
            # end if
            if case("csiso153gost1976874"):
                pass
            # end if
            if case("gost1976874"):
                pass
            # end if
            if case("isoir153"):
                pass
            # end if
            if case("stsev35888"):
                return "GOST_19768-74"
            # end if
            if case("csiso150"):
                pass
            # end if
            if case("csiso150greekccitt"):
                pass
            # end if
            if case("greekccitt"):
                pass
            # end if
            if case("isoir150"):
                return "greek-ccitt"
            # end if
            if case("csiso88greek7"):
                pass
            # end if
            if case("greek7"):
                pass
            # end if
            if case("isoir88"):
                return "greek7"
            # end if
            if case("csiso18greek7old"):
                pass
            # end if
            if case("greek7old"):
                pass
            # end if
            if case("isoir18"):
                return "greek7-old"
            # end if
            if case("cshpdesktop"):
                pass
            # end if
            if case("hpdesktop"):
                return "HP-DeskTop"
            # end if
            if case("cshplegal"):
                pass
            # end if
            if case("hplegal"):
                return "HP-Legal"
            # end if
            if case("cshpmath8"):
                pass
            # end if
            if case("hpmath8"):
                return "HP-Math8"
            # end if
            if case("cshppifont"):
                pass
            # end if
            if case("hppifont"):
                return "HP-Pi-font"
            # end if
            if case("cshproman8"):
                pass
            # end if
            if case("hproman8"):
                pass
            # end if
            if case("r8"):
                pass
            # end if
            if case("roman8"):
                return "hp-roman8"
            # end if
            if case("hzgb2312"):
                return "HZ-GB-2312"
            # end if
            if case("csibmsymbols"):
                pass
            # end if
            if case("ibmsymbols"):
                return "IBM-Symbols"
            # end if
            if case("csibmthai"):
                pass
            # end if
            if case("ibmthai"):
                return "IBM-Thai"
            # end if
            if case("cp37"):
                pass
            # end if
            if case("csibm37"):
                pass
            # end if
            if case("ebcdiccpca"):
                pass
            # end if
            if case("ebcdiccpnl"):
                pass
            # end if
            if case("ebcdiccpus"):
                pass
            # end if
            if case("ebcdiccpwt"):
                pass
            # end if
            if case("ibm37"):
                return "IBM037"
            # end if
            if case("cp38"):
                pass
            # end if
            if case("csibm38"):
                pass
            # end if
            if case("ebcdicint"):
                pass
            # end if
            if case("ibm38"):
                return "IBM038"
            # end if
            if case("cp273"):
                pass
            # end if
            if case("csibm273"):
                pass
            # end if
            if case("ibm273"):
                return "IBM273"
            # end if
            if case("cp274"):
                pass
            # end if
            if case("csibm274"):
                pass
            # end if
            if case("ebcdicbe"):
                pass
            # end if
            if case("ibm274"):
                return "IBM274"
            # end if
            if case("cp275"):
                pass
            # end if
            if case("csibm275"):
                pass
            # end if
            if case("ebcdicbr"):
                pass
            # end if
            if case("ibm275"):
                return "IBM275"
            # end if
            if case("csibm277"):
                pass
            # end if
            if case("ebcdiccpdk"):
                pass
            # end if
            if case("ebcdiccpno"):
                pass
            # end if
            if case("ibm277"):
                return "IBM277"
            # end if
            if case("cp278"):
                pass
            # end if
            if case("csibm278"):
                pass
            # end if
            if case("ebcdiccpfi"):
                pass
            # end if
            if case("ebcdiccpse"):
                pass
            # end if
            if case("ibm278"):
                return "IBM278"
            # end if
            if case("cp280"):
                pass
            # end if
            if case("csibm280"):
                pass
            # end if
            if case("ebcdiccpit"):
                pass
            # end if
            if case("ibm280"):
                return "IBM280"
            # end if
            if case("cp281"):
                pass
            # end if
            if case("csibm281"):
                pass
            # end if
            if case("ebcdicjpe"):
                pass
            # end if
            if case("ibm281"):
                return "IBM281"
            # end if
            if case("cp284"):
                pass
            # end if
            if case("csibm284"):
                pass
            # end if
            if case("ebcdiccpes"):
                pass
            # end if
            if case("ibm284"):
                return "IBM284"
            # end if
            if case("cp285"):
                pass
            # end if
            if case("csibm285"):
                pass
            # end if
            if case("ebcdiccpgb"):
                pass
            # end if
            if case("ibm285"):
                return "IBM285"
            # end if
            if case("cp290"):
                pass
            # end if
            if case("csibm290"):
                pass
            # end if
            if case("ebcdicjpkana"):
                pass
            # end if
            if case("ibm290"):
                return "IBM290"
            # end if
            if case("cp297"):
                pass
            # end if
            if case("csibm297"):
                pass
            # end if
            if case("ebcdiccpfr"):
                pass
            # end if
            if case("ibm297"):
                return "IBM297"
            # end if
            if case("cp420"):
                pass
            # end if
            if case("csibm420"):
                pass
            # end if
            if case("ebcdiccpar1"):
                pass
            # end if
            if case("ibm420"):
                return "IBM420"
            # end if
            if case("cp423"):
                pass
            # end if
            if case("csibm423"):
                pass
            # end if
            if case("ebcdiccpgr"):
                pass
            # end if
            if case("ibm423"):
                return "IBM423"
            # end if
            if case("cp424"):
                pass
            # end if
            if case("csibm424"):
                pass
            # end if
            if case("ebcdiccphe"):
                pass
            # end if
            if case("ibm424"):
                return "IBM424"
            # end if
            if case("437"):
                pass
            # end if
            if case("cp437"):
                pass
            # end if
            if case("cspc8codepage437"):
                pass
            # end if
            if case("ibm437"):
                return "IBM437"
            # end if
            if case("cp500"):
                pass
            # end if
            if case("csibm500"):
                pass
            # end if
            if case("ebcdiccpbe"):
                pass
            # end if
            if case("ebcdiccpch"):
                pass
            # end if
            if case("ibm500"):
                return "IBM500"
            # end if
            if case("cp775"):
                pass
            # end if
            if case("cspc775baltic"):
                pass
            # end if
            if case("ibm775"):
                return "IBM775"
            # end if
            if case("850"):
                pass
            # end if
            if case("cp850"):
                pass
            # end if
            if case("cspc850multilingual"):
                pass
            # end if
            if case("ibm850"):
                return "IBM850"
            # end if
            if case("851"):
                pass
            # end if
            if case("cp851"):
                pass
            # end if
            if case("csibm851"):
                pass
            # end if
            if case("ibm851"):
                return "IBM851"
            # end if
            if case("852"):
                pass
            # end if
            if case("cp852"):
                pass
            # end if
            if case("cspcp852"):
                pass
            # end if
            if case("ibm852"):
                return "IBM852"
            # end if
            if case("855"):
                pass
            # end if
            if case("cp855"):
                pass
            # end if
            if case("csibm855"):
                pass
            # end if
            if case("ibm855"):
                return "IBM855"
            # end if
            if case("857"):
                pass
            # end if
            if case("cp857"):
                pass
            # end if
            if case("csibm857"):
                pass
            # end if
            if case("ibm857"):
                return "IBM857"
            # end if
            if case("ccsid858"):
                pass
            # end if
            if case("cp858"):
                pass
            # end if
            if case("ibm858"):
                pass
            # end if
            if case("pcmultilingual850euro"):
                return "IBM00858"
            # end if
            if case("860"):
                pass
            # end if
            if case("cp860"):
                pass
            # end if
            if case("csibm860"):
                pass
            # end if
            if case("ibm860"):
                return "IBM860"
            # end if
            if case("861"):
                pass
            # end if
            if case("cp861"):
                pass
            # end if
            if case("cpis"):
                pass
            # end if
            if case("csibm861"):
                pass
            # end if
            if case("ibm861"):
                return "IBM861"
            # end if
            if case("862"):
                pass
            # end if
            if case("cp862"):
                pass
            # end if
            if case("cspc862latinhebrew"):
                pass
            # end if
            if case("ibm862"):
                return "IBM862"
            # end if
            if case("863"):
                pass
            # end if
            if case("cp863"):
                pass
            # end if
            if case("csibm863"):
                pass
            # end if
            if case("ibm863"):
                return "IBM863"
            # end if
            if case("cp864"):
                pass
            # end if
            if case("csibm864"):
                pass
            # end if
            if case("ibm864"):
                return "IBM864"
            # end if
            if case("865"):
                pass
            # end if
            if case("cp865"):
                pass
            # end if
            if case("csibm865"):
                pass
            # end if
            if case("ibm865"):
                return "IBM865"
            # end if
            if case("866"):
                pass
            # end if
            if case("cp866"):
                pass
            # end if
            if case("csibm866"):
                pass
            # end if
            if case("ibm866"):
                return "IBM866"
            # end if
            if case("cp868"):
                pass
            # end if
            if case("cpar"):
                pass
            # end if
            if case("csibm868"):
                pass
            # end if
            if case("ibm868"):
                return "IBM868"
            # end if
            if case("869"):
                pass
            # end if
            if case("cp869"):
                pass
            # end if
            if case("cpgr"):
                pass
            # end if
            if case("csibm869"):
                pass
            # end if
            if case("ibm869"):
                return "IBM869"
            # end if
            if case("cp870"):
                pass
            # end if
            if case("csibm870"):
                pass
            # end if
            if case("ebcdiccproece"):
                pass
            # end if
            if case("ebcdiccpyu"):
                pass
            # end if
            if case("ibm870"):
                return "IBM870"
            # end if
            if case("cp871"):
                pass
            # end if
            if case("csibm871"):
                pass
            # end if
            if case("ebcdiccpis"):
                pass
            # end if
            if case("ibm871"):
                return "IBM871"
            # end if
            if case("cp880"):
                pass
            # end if
            if case("csibm880"):
                pass
            # end if
            if case("ebcdiccyrillic"):
                pass
            # end if
            if case("ibm880"):
                return "IBM880"
            # end if
            if case("cp891"):
                pass
            # end if
            if case("csibm891"):
                pass
            # end if
            if case("ibm891"):
                return "IBM891"
            # end if
            if case("cp903"):
                pass
            # end if
            if case("csibm903"):
                pass
            # end if
            if case("ibm903"):
                return "IBM903"
            # end if
            if case("904"):
                pass
            # end if
            if case("cp904"):
                pass
            # end if
            if case("csibbm904"):
                pass
            # end if
            if case("ibm904"):
                return "IBM904"
            # end if
            if case("cp905"):
                pass
            # end if
            if case("csibm905"):
                pass
            # end if
            if case("ebcdiccptr"):
                pass
            # end if
            if case("ibm905"):
                return "IBM905"
            # end if
            if case("cp918"):
                pass
            # end if
            if case("csibm918"):
                pass
            # end if
            if case("ebcdiccpar2"):
                pass
            # end if
            if case("ibm918"):
                return "IBM918"
            # end if
            if case("ccsid924"):
                pass
            # end if
            if case("cp924"):
                pass
            # end if
            if case("ebcdiclatin9euro"):
                pass
            # end if
            if case("ibm924"):
                return "IBM00924"
            # end if
            if case("cp1026"):
                pass
            # end if
            if case("csibm1026"):
                pass
            # end if
            if case("ibm1026"):
                return "IBM1026"
            # end if
            if case("ibm1047"):
                return "IBM1047"
            # end if
            if case("ccsid1140"):
                pass
            # end if
            if case("cp1140"):
                pass
            # end if
            if case("ebcdicus37euro"):
                pass
            # end if
            if case("ibm1140"):
                return "IBM01140"
            # end if
            if case("ccsid1141"):
                pass
            # end if
            if case("cp1141"):
                pass
            # end if
            if case("ebcdicde273euro"):
                pass
            # end if
            if case("ibm1141"):
                return "IBM01141"
            # end if
            if case("ccsid1142"):
                pass
            # end if
            if case("cp1142"):
                pass
            # end if
            if case("ebcdicdk277euro"):
                pass
            # end if
            if case("ebcdicno277euro"):
                pass
            # end if
            if case("ibm1142"):
                return "IBM01142"
            # end if
            if case("ccsid1143"):
                pass
            # end if
            if case("cp1143"):
                pass
            # end if
            if case("ebcdicfi278euro"):
                pass
            # end if
            if case("ebcdicse278euro"):
                pass
            # end if
            if case("ibm1143"):
                return "IBM01143"
            # end if
            if case("ccsid1144"):
                pass
            # end if
            if case("cp1144"):
                pass
            # end if
            if case("ebcdicit280euro"):
                pass
            # end if
            if case("ibm1144"):
                return "IBM01144"
            # end if
            if case("ccsid1145"):
                pass
            # end if
            if case("cp1145"):
                pass
            # end if
            if case("ebcdices284euro"):
                pass
            # end if
            if case("ibm1145"):
                return "IBM01145"
            # end if
            if case("ccsid1146"):
                pass
            # end if
            if case("cp1146"):
                pass
            # end if
            if case("ebcdicgb285euro"):
                pass
            # end if
            if case("ibm1146"):
                return "IBM01146"
            # end if
            if case("ccsid1147"):
                pass
            # end if
            if case("cp1147"):
                pass
            # end if
            if case("ebcdicfr297euro"):
                pass
            # end if
            if case("ibm1147"):
                return "IBM01147"
            # end if
            if case("ccsid1148"):
                pass
            # end if
            if case("cp1148"):
                pass
            # end if
            if case("ebcdicinternational500euro"):
                pass
            # end if
            if case("ibm1148"):
                return "IBM01148"
            # end if
            if case("ccsid1149"):
                pass
            # end if
            if case("cp1149"):
                pass
            # end if
            if case("ebcdicis871euro"):
                pass
            # end if
            if case("ibm1149"):
                return "IBM01149"
            # end if
            if case("csiso143iecp271"):
                pass
            # end if
            if case("iecp271"):
                pass
            # end if
            if case("isoir143"):
                return "IEC_P27-1"
            # end if
            if case("csiso49inis"):
                pass
            # end if
            if case("inis"):
                pass
            # end if
            if case("isoir49"):
                return "INIS"
            # end if
            if case("csiso50inis8"):
                pass
            # end if
            if case("inis8"):
                pass
            # end if
            if case("isoir50"):
                return "INIS-8"
            # end if
            if case("csiso51iniscyrillic"):
                pass
            # end if
            if case("iniscyrillic"):
                pass
            # end if
            if case("isoir51"):
                return "INIS-cyrillic"
            # end if
            if case("csinvariant"):
                pass
            # end if
            if case("invariant"):
                return "INVARIANT"
            # end if
            if case("iso2022cn"):
                return "ISO-2022-CN"
            # end if
            if case("iso2022cnext"):
                return "ISO-2022-CN-EXT"
            # end if
            if case("csiso2022jp"):
                pass
            # end if
            if case("iso2022jp"):
                return "ISO-2022-JP"
            # end if
            if case("csiso2022jp2"):
                pass
            # end if
            if case("iso2022jp2"):
                return "ISO-2022-JP-2"
            # end if
            if case("csiso2022kr"):
                pass
            # end if
            if case("iso2022kr"):
                return "ISO-2022-KR"
            # end if
            if case("cswindows30latin1"):
                pass
            # end if
            if case("iso88591windows30latin1"):
                return "ISO-8859-1-Windows-3.0-Latin-1"
            # end if
            if case("cswindows31latin1"):
                pass
            # end if
            if case("iso88591windows31latin1"):
                return "ISO-8859-1-Windows-3.1-Latin-1"
            # end if
            if case("csisolatin2"):
                pass
            # end if
            if case("iso88592"):
                pass
            # end if
            if case("iso885921987"):
                pass
            # end if
            if case("isoir101"):
                pass
            # end if
            if case("l2"):
                pass
            # end if
            if case("latin2"):
                return "ISO-8859-2"
            # end if
            if case("cswindows31latin2"):
                pass
            # end if
            if case("iso88592windowslatin2"):
                return "ISO-8859-2-Windows-Latin-2"
            # end if
            if case("csisolatin3"):
                pass
            # end if
            if case("iso88593"):
                pass
            # end if
            if case("iso885931988"):
                pass
            # end if
            if case("isoir109"):
                pass
            # end if
            if case("l3"):
                pass
            # end if
            if case("latin3"):
                return "ISO-8859-3"
            # end if
            if case("csisolatin4"):
                pass
            # end if
            if case("iso88594"):
                pass
            # end if
            if case("iso885941988"):
                pass
            # end if
            if case("isoir110"):
                pass
            # end if
            if case("l4"):
                pass
            # end if
            if case("latin4"):
                return "ISO-8859-4"
            # end if
            if case("csisolatincyrillic"):
                pass
            # end if
            if case("cyrillic"):
                pass
            # end if
            if case("iso88595"):
                pass
            # end if
            if case("iso885951988"):
                pass
            # end if
            if case("isoir144"):
                return "ISO-8859-5"
            # end if
            if case("arabic"):
                pass
            # end if
            if case("asmo708"):
                pass
            # end if
            if case("csisolatinarabic"):
                pass
            # end if
            if case("ecma114"):
                pass
            # end if
            if case("iso88596"):
                pass
            # end if
            if case("iso885961987"):
                pass
            # end if
            if case("isoir127"):
                return "ISO-8859-6"
            # end if
            if case("csiso88596e"):
                pass
            # end if
            if case("iso88596e"):
                return "ISO-8859-6-E"
            # end if
            if case("csiso88596i"):
                pass
            # end if
            if case("iso88596i"):
                return "ISO-8859-6-I"
            # end if
            if case("csisolatingreek"):
                pass
            # end if
            if case("ecma118"):
                pass
            # end if
            if case("elot928"):
                pass
            # end if
            if case("greek"):
                pass
            # end if
            if case("greek8"):
                pass
            # end if
            if case("iso88597"):
                pass
            # end if
            if case("iso885971987"):
                pass
            # end if
            if case("isoir126"):
                return "ISO-8859-7"
            # end if
            if case("csisolatinhebrew"):
                pass
            # end if
            if case("hebrew"):
                pass
            # end if
            if case("iso88598"):
                pass
            # end if
            if case("iso885981988"):
                pass
            # end if
            if case("isoir138"):
                return "ISO-8859-8"
            # end if
            if case("csiso88598e"):
                pass
            # end if
            if case("iso88598e"):
                return "ISO-8859-8-E"
            # end if
            if case("csiso88598i"):
                pass
            # end if
            if case("iso88598i"):
                return "ISO-8859-8-I"
            # end if
            if case("cswindows31latin5"):
                pass
            # end if
            if case("iso88599windowslatin5"):
                return "ISO-8859-9-Windows-Latin-5"
            # end if
            if case("csisolatin6"):
                pass
            # end if
            if case("iso885910"):
                pass
            # end if
            if case("iso8859101992"):
                pass
            # end if
            if case("isoir157"):
                pass
            # end if
            if case("l6"):
                pass
            # end if
            if case("latin6"):
                return "ISO-8859-10"
            # end if
            if case("iso885913"):
                return "ISO-8859-13"
            # end if
            if case("iso885914"):
                pass
            # end if
            if case("iso8859141998"):
                pass
            # end if
            if case("isoceltic"):
                pass
            # end if
            if case("isoir199"):
                pass
            # end if
            if case("l8"):
                pass
            # end if
            if case("latin8"):
                return "ISO-8859-14"
            # end if
            if case("iso885915"):
                pass
            # end if
            if case("latin9"):
                return "ISO-8859-15"
            # end if
            if case("iso885916"):
                pass
            # end if
            if case("iso8859162001"):
                pass
            # end if
            if case("isoir226"):
                pass
            # end if
            if case("l10"):
                pass
            # end if
            if case("latin10"):
                return "ISO-8859-16"
            # end if
            if case("iso10646j1"):
                return "ISO-10646-J-1"
            # end if
            if case("csunicode"):
                pass
            # end if
            if case("iso10646ucs2"):
                return "ISO-10646-UCS-2"
            # end if
            if case("csucs4"):
                pass
            # end if
            if case("iso10646ucs4"):
                return "ISO-10646-UCS-4"
            # end if
            if case("csunicodeascii"):
                pass
            # end if
            if case("iso10646ucsbasic"):
                return "ISO-10646-UCS-Basic"
            # end if
            if case("csunicodelatin1"):
                pass
            # end if
            if case("iso10646"):
                pass
            # end if
            if case("iso10646unicodelatin1"):
                return "ISO-10646-Unicode-Latin1"
            # end if
            if case("csiso10646utf1"):
                pass
            # end if
            if case("iso10646utf1"):
                return "ISO-10646-UTF-1"
            # end if
            if case("csiso115481"):
                pass
            # end if
            if case("iso115481"):
                pass
            # end if
            if case("isotr115481"):
                return "ISO-11548-1"
            # end if
            if case("csiso90"):
                pass
            # end if
            if case("isoir90"):
                return "iso-ir-90"
            # end if
            if case("csunicodeibm1261"):
                pass
            # end if
            if case("isounicodeibm1261"):
                return "ISO-Unicode-IBM-1261"
            # end if
            if case("csunicodeibm1264"):
                pass
            # end if
            if case("isounicodeibm1264"):
                return "ISO-Unicode-IBM-1264"
            # end if
            if case("csunicodeibm1265"):
                pass
            # end if
            if case("isounicodeibm1265"):
                return "ISO-Unicode-IBM-1265"
            # end if
            if case("csunicodeibm1268"):
                pass
            # end if
            if case("isounicodeibm1268"):
                return "ISO-Unicode-IBM-1268"
            # end if
            if case("csunicodeibm1276"):
                pass
            # end if
            if case("isounicodeibm1276"):
                return "ISO-Unicode-IBM-1276"
            # end if
            if case("csiso646basic1983"):
                pass
            # end if
            if case("iso646basic1983"):
                pass
            # end if
            if case("ref"):
                return "ISO_646.basic:1983"
            # end if
            if case("csiso2intlrefversion"):
                pass
            # end if
            if case("irv"):
                pass
            # end if
            if case("iso646irv1983"):
                pass
            # end if
            if case("isoir2"):
                return "ISO_646.irv:1983"
            # end if
            if case("csiso2033"):
                pass
            # end if
            if case("e13b"):
                pass
            # end if
            if case("iso20331983"):
                pass
            # end if
            if case("isoir98"):
                return "ISO_2033-1983"
            # end if
            if case("csiso5427cyrillic"):
                pass
            # end if
            if case("iso5427"):
                pass
            # end if
            if case("isoir37"):
                return "ISO_5427"
            # end if
            if case("iso5427cyrillic1981"):
                pass
            # end if
            if case("iso54271981"):
                pass
            # end if
            if case("isoir54"):
                return "ISO_5427:1981"
            # end if
            if case("csiso5428greek"):
                pass
            # end if
            if case("iso54281980"):
                pass
            # end if
            if case("isoir55"):
                return "ISO_5428:1980"
            # end if
            if case("csiso6937add"):
                pass
            # end if
            if case("iso6937225"):
                pass
            # end if
            if case("isoir152"):
                return "ISO_6937-2-25"
            # end if
            if case("csisotextcomm"):
                pass
            # end if
            if case("iso69372add"):
                pass
            # end if
            if case("isoir142"):
                return "ISO_6937-2-add"
            # end if
            if case("csiso8859supp"):
                pass
            # end if
            if case("iso8859supp"):
                pass
            # end if
            if case("isoir154"):
                pass
            # end if
            if case("latin125"):
                return "ISO_8859-supp"
            # end if
            if case("csiso10367box"):
                pass
            # end if
            if case("iso10367box"):
                pass
            # end if
            if case("isoir155"):
                return "ISO_10367-box"
            # end if
            if case("csiso15italian"):
                pass
            # end if
            if case("iso646it"):
                pass
            # end if
            if case("isoir15"):
                pass
            # end if
            if case("it"):
                return "IT"
            # end if
            if case("csiso13jisc6220jp"):
                pass
            # end if
            if case("isoir13"):
                pass
            # end if
            if case("jisc62201969"):
                pass
            # end if
            if case("jisc62201969jp"):
                pass
            # end if
            if case("katakana"):
                pass
            # end if
            if case("x2017"):
                return "JIS_C6220-1969-jp"
            # end if
            if case("csiso14jisc6220ro"):
                pass
            # end if
            if case("iso646jp"):
                pass
            # end if
            if case("isoir14"):
                pass
            # end if
            if case("jisc62201969ro"):
                pass
            # end if
            if case("jp"):
                return "JIS_C6220-1969-ro"
            # end if
            if case("csiso42jisc62261978"):
                pass
            # end if
            if case("isoir42"):
                pass
            # end if
            if case("jisc62261978"):
                return "JIS_C6226-1978"
            # end if
            if case("csiso87jisx208"):
                pass
            # end if
            if case("isoir87"):
                pass
            # end if
            if case("jisc62261983"):
                pass
            # end if
            if case("jisx2081983"):
                pass
            # end if
            if case("x208"):
                return "JIS_C6226-1983"
            # end if
            if case("csiso91jisc62291984a"):
                pass
            # end if
            if case("isoir91"):
                pass
            # end if
            if case("jisc62291984a"):
                pass
            # end if
            if case("jpocra"):
                return "JIS_C6229-1984-a"
            # end if
            if case("csiso92jisc62991984b"):
                pass
            # end if
            if case("iso646jpocrb"):
                pass
            # end if
            if case("isoir92"):
                pass
            # end if
            if case("jisc62291984b"):
                pass
            # end if
            if case("jpocrb"):
                return "JIS_C6229-1984-b"
            # end if
            if case("csiso93jis62291984badd"):
                pass
            # end if
            if case("isoir93"):
                pass
            # end if
            if case("jisc62291984badd"):
                pass
            # end if
            if case("jpocrbadd"):
                return "JIS_C6229-1984-b-add"
            # end if
            if case("csiso94jis62291984hand"):
                pass
            # end if
            if case("isoir94"):
                pass
            # end if
            if case("jisc62291984hand"):
                pass
            # end if
            if case("jpocrhand"):
                return "JIS_C6229-1984-hand"
            # end if
            if case("csiso95jis62291984handadd"):
                pass
            # end if
            if case("isoir95"):
                pass
            # end if
            if case("jisc62291984handadd"):
                pass
            # end if
            if case("jpocrhandadd"):
                return "JIS_C6229-1984-hand-add"
            # end if
            if case("csiso96jisc62291984kana"):
                pass
            # end if
            if case("isoir96"):
                pass
            # end if
            if case("jisc62291984kana"):
                return "JIS_C6229-1984-kana"
            # end if
            if case("csjisencoding"):
                pass
            # end if
            if case("jisencoding"):
                return "JIS_Encoding"
            # end if
            if case("cshalfwidthkatakana"):
                pass
            # end if
            if case("jisx201"):
                pass
            # end if
            if case("x201"):
                return "JIS_X0201"
            # end if
            if case("csiso159jisx2121990"):
                pass
            # end if
            if case("isoir159"):
                pass
            # end if
            if case("jisx2121990"):
                pass
            # end if
            if case("x212"):
                return "JIS_X0212-1990"
            # end if
            if case("csiso141jusib1002"):
                pass
            # end if
            if case("iso646yu"):
                pass
            # end if
            if case("isoir141"):
                pass
            # end if
            if case("js"):
                pass
            # end if
            if case("jusib1002"):
                pass
            # end if
            if case("yu"):
                return "JUS_I.B1.002"
            # end if
            if case("csiso147macedonian"):
                pass
            # end if
            if case("isoir147"):
                pass
            # end if
            if case("jusib1003mac"):
                pass
            # end if
            if case("macedonian"):
                return "JUS_I.B1.003-mac"
            # end if
            if case("csiso146serbian"):
                pass
            # end if
            if case("isoir146"):
                pass
            # end if
            if case("jusib1003serb"):
                pass
            # end if
            if case("serbian"):
                return "JUS_I.B1.003-serb"
            # end if
            if case("koi7switched"):
                return "KOI7-switched"
            # end if
            if case("cskoi8r"):
                pass
            # end if
            if case("koi8r"):
                return "KOI8-R"
            # end if
            if case("koi8u"):
                return "KOI8-U"
            # end if
            if case("csksc5636"):
                pass
            # end if
            if case("iso646kr"):
                pass
            # end if
            if case("ksc5636"):
                return "KSC5636"
            # end if
            if case("cskz1048"):
                pass
            # end if
            if case("kz1048"):
                pass
            # end if
            if case("rk1048"):
                pass
            # end if
            if case("strk10482002"):
                return "KZ-1048"
            # end if
            if case("csiso19latingreek"):
                pass
            # end if
            if case("isoir19"):
                pass
            # end if
            if case("latingreek"):
                return "latin-greek"
            # end if
            if case("csiso27latingreek1"):
                pass
            # end if
            if case("isoir27"):
                pass
            # end if
            if case("latingreek1"):
                return "Latin-greek-1"
            # end if
            if case("csiso158lap"):
                pass
            # end if
            if case("isoir158"):
                pass
            # end if
            if case("lap"):
                pass
            # end if
            if case("latinlap"):
                return "latin-lap"
            # end if
            if case("csmacintosh"):
                pass
            # end if
            if case("mac"):
                pass
            # end if
            if case("macintosh"):
                return "macintosh"
            # end if
            if case("csmicrosoftpublishing"):
                pass
            # end if
            if case("microsoftpublishing"):
                return "Microsoft-Publishing"
            # end if
            if case("csmnem"):
                pass
            # end if
            if case("mnem"):
                return "MNEM"
            # end if
            if case("csmnemonic"):
                pass
            # end if
            if case("mnemonic"):
                return "MNEMONIC"
            # end if
            if case("csiso86hungarian"):
                pass
            # end if
            if case("hu"):
                pass
            # end if
            if case("iso646hu"):
                pass
            # end if
            if case("isoir86"):
                pass
            # end if
            if case("msz77953"):
                return "MSZ_7795.3"
            # end if
            if case("csnatsdano"):
                pass
            # end if
            if case("isoir91"):
                pass
            # end if
            if case("natsdano"):
                return "NATS-DANO"
            # end if
            if case("csnatsdanoadd"):
                pass
            # end if
            if case("isoir92"):
                pass
            # end if
            if case("natsdanoadd"):
                return "NATS-DANO-ADD"
            # end if
            if case("csnatssefi"):
                pass
            # end if
            if case("isoir81"):
                pass
            # end if
            if case("natssefi"):
                return "NATS-SEFI"
            # end if
            if case("csnatssefiadd"):
                pass
            # end if
            if case("isoir82"):
                pass
            # end if
            if case("natssefiadd"):
                return "NATS-SEFI-ADD"
            # end if
            if case("csiso151cuba"):
                pass
            # end if
            if case("cuba"):
                pass
            # end if
            if case("iso646cu"):
                pass
            # end if
            if case("isoir151"):
                pass
            # end if
            if case("ncnc1081"):
                return "NC_NC00-10:81"
            # end if
            if case("csiso69french"):
                pass
            # end if
            if case("fr"):
                pass
            # end if
            if case("iso646fr"):
                pass
            # end if
            if case("isoir69"):
                pass
            # end if
            if case("nfz62010"):
                return "NF_Z_62-010"
            # end if
            if case("csiso25french"):
                pass
            # end if
            if case("iso646fr1"):
                pass
            # end if
            if case("isoir25"):
                pass
            # end if
            if case("nfz620101973"):
                return "NF_Z_62-010_(1973)"
            # end if
            if case("csiso60danishnorwegian"):
                pass
            # end if
            if case("csiso60norwegian1"):
                pass
            # end if
            if case("iso646no"):
                pass
            # end if
            if case("isoir60"):
                pass
            # end if
            if case("no"):
                pass
            # end if
            if case("ns45511"):
                return "NS_4551-1"
            # end if
            if case("csiso61norwegian2"):
                pass
            # end if
            if case("iso646no2"):
                pass
            # end if
            if case("isoir61"):
                pass
            # end if
            if case("no2"):
                pass
            # end if
            if case("ns45512"):
                return "NS_4551-2"
            # end if
            if case("osdebcdicdf3irv"):
                return "OSD_EBCDIC_DF03_IRV"
            # end if
            if case("osdebcdicdf41"):
                return "OSD_EBCDIC_DF04_1"
            # end if
            if case("osdebcdicdf415"):
                return "OSD_EBCDIC_DF04_15"
            # end if
            if case("cspc8danishnorwegian"):
                pass
            # end if
            if case("pc8danishnorwegian"):
                return "PC8-Danish-Norwegian"
            # end if
            if case("cspc8turkish"):
                pass
            # end if
            if case("pc8turkish"):
                return "PC8-Turkish"
            # end if
            if case("csiso16portuguese"):
                pass
            # end if
            if case("iso646pt"):
                pass
            # end if
            if case("isoir16"):
                pass
            # end if
            if case("pt"):
                return "PT"
            # end if
            if case("csiso84portuguese2"):
                pass
            # end if
            if case("iso646pt2"):
                pass
            # end if
            if case("isoir84"):
                pass
            # end if
            if case("pt2"):
                return "PT2"
            # end if
            if case("cp154"):
                pass
            # end if
            if case("csptcp154"):
                pass
            # end if
            if case("cyrillicasian"):
                pass
            # end if
            if case("pt154"):
                pass
            # end if
            if case("ptcp154"):
                return "PTCP154"
            # end if
            if case("scsu"):
                return "SCSU"
            # end if
            if case("csiso10swedish"):
                pass
            # end if
            if case("fi"):
                pass
            # end if
            if case("iso646fi"):
                pass
            # end if
            if case("iso646se"):
                pass
            # end if
            if case("isoir10"):
                pass
            # end if
            if case("se"):
                pass
            # end if
            if case("sen850200b"):
                return "SEN_850200_B"
            # end if
            if case("csiso11swedishfornames"):
                pass
            # end if
            if case("iso646se2"):
                pass
            # end if
            if case("isoir11"):
                pass
            # end if
            if case("se2"):
                pass
            # end if
            if case("sen850200c"):
                return "SEN_850200_C"
            # end if
            if case("csiso102t617bit"):
                pass
            # end if
            if case("isoir102"):
                pass
            # end if
            if case("t617bit"):
                return "T.61-7bit"
            # end if
            if case("csiso103t618bit"):
                pass
            # end if
            if case("isoir103"):
                pass
            # end if
            if case("t61"):
                pass
            # end if
            if case("t618bit"):
                return "T.61-8bit"
            # end if
            if case("csiso128t101g2"):
                pass
            # end if
            if case("isoir128"):
                pass
            # end if
            if case("t101g2"):
                return "T.101-G2"
            # end if
            if case("cstscii"):
                pass
            # end if
            if case("tscii"):
                return "TSCII"
            # end if
            if case("csunicode11"):
                pass
            # end if
            if case("unicode11"):
                return "UNICODE-1-1"
            # end if
            if case("csunicode11utf7"):
                pass
            # end if
            if case("unicode11utf7"):
                return "UNICODE-1-1-UTF-7"
            # end if
            if case("csunknown8bit"):
                pass
            # end if
            if case("unknown8bit"):
                return "UNKNOWN-8BIT"
            # end if
            if case("ansix341968"):
                pass
            # end if
            if case("ansix341986"):
                pass
            # end if
            if case("ascii"):
                pass
            # end if
            if case("cp367"):
                pass
            # end if
            if case("csascii"):
                pass
            # end if
            if case("ibm367"):
                pass
            # end if
            if case("iso646irv1991"):
                pass
            # end if
            if case("iso646us"):
                pass
            # end if
            if case("isoir6"):
                pass
            # end if
            if case("us"):
                pass
            # end if
            if case("usascii"):
                return "US-ASCII"
            # end if
            if case("csusdk"):
                pass
            # end if
            if case("usdk"):
                return "us-dk"
            # end if
            if case("utf7"):
                return "UTF-7"
            # end if
            if case("utf8"):
                return "UTF-8"
            # end if
            if case("utf16"):
                return "UTF-16"
            # end if
            if case("utf16be"):
                return "UTF-16BE"
            # end if
            if case("utf16le"):
                return "UTF-16LE"
            # end if
            if case("utf32"):
                return "UTF-32"
            # end if
            if case("utf32be"):
                return "UTF-32BE"
            # end if
            if case("utf32le"):
                return "UTF-32LE"
            # end if
            if case("csventurainternational"):
                pass
            # end if
            if case("venturainternational"):
                return "Ventura-International"
            # end if
            if case("csventuramath"):
                pass
            # end if
            if case("venturamath"):
                return "Ventura-Math"
            # end if
            if case("csventuraus"):
                pass
            # end if
            if case("venturaus"):
                return "Ventura-US"
            # end if
            if case("csiso70videotexsupp1"):
                pass
            # end if
            if case("isoir70"):
                pass
            # end if
            if case("videotexsuppl"):
                return "videotex-suppl"
            # end if
            if case("csviqr"):
                pass
            # end if
            if case("viqr"):
                return "VIQR"
            # end if
            if case("csviscii"):
                pass
            # end if
            if case("viscii"):
                return "VISCII"
            # end if
            if case("csshiftjis"):
                pass
            # end if
            if case("cswindows31j"):
                pass
            # end if
            if case("mskanji"):
                pass
            # end if
            if case("shiftjis"):
                pass
            # end if
            if case("windows31j"):
                return "Windows-31J"
            # end if
            if case("iso885911"):
                pass
            # end if
            if case("tis620"):
                return "windows-874"
            # end if
            if case("cseuckr"):
                pass
            # end if
            if case("csksc56011987"):
                pass
            # end if
            if case("euckr"):
                pass
            # end if
            if case("isoir149"):
                pass
            # end if
            if case("korean"):
                pass
            # end if
            if case("ksc5601"):
                pass
            # end if
            if case("ksc56011987"):
                pass
            # end if
            if case("ksc56011989"):
                pass
            # end if
            if case("windows949"):
                return "windows-949"
            # end if
            if case("windows1250"):
                return "windows-1250"
            # end if
            if case("windows1251"):
                return "windows-1251"
            # end if
            if case("cp819"):
                pass
            # end if
            if case("csisolatin1"):
                pass
            # end if
            if case("ibm819"):
                pass
            # end if
            if case("iso88591"):
                pass
            # end if
            if case("iso885911987"):
                pass
            # end if
            if case("isoir100"):
                pass
            # end if
            if case("l1"):
                pass
            # end if
            if case("latin1"):
                pass
            # end if
            if case("windows1252"):
                return "windows-1252"
            # end if
            if case("windows1253"):
                return "windows-1253"
            # end if
            if case("csisolatin5"):
                pass
            # end if
            if case("iso88599"):
                pass
            # end if
            if case("iso885991989"):
                pass
            # end if
            if case("isoir148"):
                pass
            # end if
            if case("l5"):
                pass
            # end if
            if case("latin5"):
                pass
            # end if
            if case("windows1254"):
                return "windows-1254"
            # end if
            if case("windows1255"):
                return "windows-1255"
            # end if
            if case("windows1256"):
                return "windows-1256"
            # end if
            if case("windows1257"):
                return "windows-1257"
            # end if
            if case("windows1258"):
                return "windows-1258"
            # end if
            if case():
                return charset
            # end if
        # end for
    # end def encoding
    @classmethod
    def get_curl_version(self):
        
        curl = curl_version()
        if php_is_array(curl):
            curl = curl["version"]
        elif php_substr(curl, 0, 5) == "curl/":
            curl = php_substr(curl, 5, strcspn(curl, "  \n\r", 5))
        elif php_substr(curl, 0, 8) == "libcurl/":
            curl = php_substr(curl, 8, strcspn(curl, "  \n\r", 8))
        else:
            curl = 0
        # end if
        return curl
    # end def get_curl_version
    #// 
    #// Strip HTML comments
    #// 
    #// @param string $data Data to strip comments from
    #// @return string Comment stripped string
    #//
    @classmethod
    def strip_comments(self, data=None):
        
        output = ""
        while True:
            start = php_strpos(data, "<!--")
            if not (start != False):
                break
            # end if
            output += php_substr(data, 0, start)
            end_ = php_strpos(data, "-->", start)
            if end_ != False:
                data = php_substr_replace(data, "", 0, end_ + 3)
            else:
                data = ""
            # end if
        # end while
        return output + data
    # end def strip_comments
    @classmethod
    def parse_date(self, dt=None):
        
        parser = SimplePie_Parse_Date.get()
        return parser.parse(dt)
    # end def parse_date
    #// 
    #// Decode HTML entities
    #// 
    #// @deprecated Use DOMDocument instead
    #// @param string $data Input data
    #// @return string Output data
    #//
    @classmethod
    def entities_decode(self, data=None):
        
        decoder = php_new_class("SimplePie_Decode_HTML_Entities", lambda : SimplePie_Decode_HTML_Entities(data))
        return decoder.parse()
    # end def entities_decode
    #// 
    #// Remove RFC822 comments
    #// 
    #// @param string $data Data to strip comments from
    #// @return string Comment stripped string
    #//
    @classmethod
    def uncomment_rfc822(self, string=None):
        
        string = str(string)
        position = 0
        length = php_strlen(string)
        depth = 0
        output = ""
        while True:
            pos = php_strpos(string, "(", position)
            if not (position < length and pos != False):
                break
            # end if
            output += php_substr(string, position, pos - position)
            position = pos + 1
            if string[pos - 1] != "\\":
                depth += 1
                while True:
                    
                    if not (depth and position < length):
                        break
                    # end if
                    position += strcspn(string, "()", position)
                    if string[position - 1] == "\\":
                        position += 1
                        continue
                    elif (php_isset(lambda : string[position])):
                        for case in Switch(string[position]):
                            if case("("):
                                depth += 1
                                break
                            # end if
                            if case(")"):
                                depth -= 1
                                break
                            # end if
                        # end for
                        position += 1
                    else:
                        break
                    # end if
                # end while
            else:
                output += "("
            # end if
        # end while
        output += php_substr(string, position)
        return output
    # end def uncomment_rfc822
    @classmethod
    def parse_mime(self, mime=None):
        
        pos = php_strpos(mime, ";")
        if pos == False:
            return php_trim(mime)
        else:
            return php_trim(php_substr(mime, 0, pos))
        # end if
    # end def parse_mime
    @classmethod
    def atom_03_construct_type(self, attribs=None):
        
        if (php_isset(lambda : attribs[""]["mode"])) and php_strtolower(php_trim(attribs[""]["mode"]) == "base64"):
            mode = SIMPLEPIE_CONSTRUCT_BASE64
        else:
            mode = SIMPLEPIE_CONSTRUCT_NONE
        # end if
        if (php_isset(lambda : attribs[""]["type"])):
            for case in Switch(php_strtolower(php_trim(attribs[""]["type"]))):
                if case("text"):
                    pass
                # end if
                if case("text/plain"):
                    return SIMPLEPIE_CONSTRUCT_TEXT | mode
                # end if
                if case("html"):
                    pass
                # end if
                if case("text/html"):
                    return SIMPLEPIE_CONSTRUCT_HTML | mode
                # end if
                if case("xhtml"):
                    pass
                # end if
                if case("application/xhtml+xml"):
                    return SIMPLEPIE_CONSTRUCT_XHTML | mode
                # end if
                if case():
                    return SIMPLEPIE_CONSTRUCT_NONE | mode
                # end if
            # end for
        else:
            return SIMPLEPIE_CONSTRUCT_TEXT | mode
        # end if
    # end def atom_03_construct_type
    @classmethod
    def atom_10_construct_type(self, attribs=None):
        
        if (php_isset(lambda : attribs[""]["type"])):
            for case in Switch(php_strtolower(php_trim(attribs[""]["type"]))):
                if case("text"):
                    return SIMPLEPIE_CONSTRUCT_TEXT
                # end if
                if case("html"):
                    return SIMPLEPIE_CONSTRUCT_HTML
                # end if
                if case("xhtml"):
                    return SIMPLEPIE_CONSTRUCT_XHTML
                # end if
                if case():
                    return SIMPLEPIE_CONSTRUCT_NONE
                # end if
            # end for
        # end if
        return SIMPLEPIE_CONSTRUCT_TEXT
    # end def atom_10_construct_type
    @classmethod
    def atom_10_content_construct_type(self, attribs=None):
        
        if (php_isset(lambda : attribs[""]["type"])):
            type = php_strtolower(php_trim(attribs[""]["type"]))
            for case in Switch(type):
                if case("text"):
                    return SIMPLEPIE_CONSTRUCT_TEXT
                # end if
                if case("html"):
                    return SIMPLEPIE_CONSTRUCT_HTML
                # end if
                if case("xhtml"):
                    return SIMPLEPIE_CONSTRUCT_XHTML
                # end if
            # end for
            if php_in_array(php_substr(type, -4), Array("+xml", "/xml")) or php_substr(type, 0, 5) == "text/":
                return SIMPLEPIE_CONSTRUCT_NONE
            else:
                return SIMPLEPIE_CONSTRUCT_BASE64
            # end if
        else:
            return SIMPLEPIE_CONSTRUCT_TEXT
        # end if
    # end def atom_10_content_construct_type
    @classmethod
    def is_isegment_nz_nc(self, string=None):
        
        return bool(php_preg_match("/^([A-Za-z0-9\\-._~\\x{A0}-\\x{D7FF}\\x{F900}-\\x{FDCF}\\x{FDF0}-\\x{FFEF}\\x{10000}-\\x{1FFFD}\\x{20000}-\\x{2FFFD}\\x{30000}-\\x{3FFFD}\\x{40000}-\\x{4FFFD}\\x{50000}-\\x{5FFFD}\\x{60000}-\\x{6FFFD}\\x{70000}-\\x{7FFFD}\\x{80000}-\\x{8FFFD}\\x{90000}-\\x{9FFFD}\\x{A0000}-\\x{AFFFD}\\x{B0000}-\\x{BFFFD}\\x{C0000}-\\x{CFFFD}\\x{D0000}-\\x{DFFFD}\\x{E1000}-\\x{EFFFD}!$&'()*+,;=@]|(%[0-9ABCDEF]{2}))+$/u", string))
    # end def is_isegment_nz_nc
    @classmethod
    def space_seperated_tokens(self, string=None):
        
        space_characters = "    \n\r"
        string_length = php_strlen(string)
        position = strspn(string, space_characters)
        tokens = Array()
        while True:
            
            if not (position < string_length):
                break
            # end if
            len = strcspn(string, space_characters, position)
            tokens[-1] = php_substr(string, position, len)
            position += len
            position += strspn(string, space_characters, position)
        # end while
        return tokens
    # end def space_seperated_tokens
    #// 
    #// Converts a unicode codepoint to a UTF-8 character
    #// 
    #// @static
    #// @param int $codepoint Unicode codepoint
    #// @return string UTF-8 character
    #//
    @classmethod
    def codepoint_to_utf8(self, codepoint=None):
        
        codepoint = int(codepoint)
        if codepoint < 0:
            return False
        else:
            if codepoint <= 127:
                return chr(codepoint)
            else:
                if codepoint <= 2047:
                    return chr(192 | codepoint >> 6) + chr(128 | codepoint & 63)
                else:
                    if codepoint <= 65535:
                        return chr(224 | codepoint >> 12) + chr(128 | codepoint >> 6 & 63) + chr(128 | codepoint & 63)
                    else:
                        if codepoint <= 1114111:
                            return chr(240 | codepoint >> 18) + chr(128 | codepoint >> 12 & 63) + chr(128 | codepoint >> 6 & 63) + chr(128 | codepoint & 63)
                        else:
                            #// U+FFFD REPLACEMENT CHARACTER
                            return "ï¿½"
                        # end if
                    # end if
                # end if
            # end if
        # end if
    # end def codepoint_to_utf8
    #// 
    #// Similar to parse_str()
    #// 
    #// Returns an associative array of name/value pairs, where the value is an
    #// array of values that have used the same name
    #// 
    #// @static
    #// @param string $str The input string.
    #// @return array
    #//
    @classmethod
    def parse_str(self, str=None):
        
        return_ = Array()
        str = php_explode("&", str)
        for section in str:
            if php_strpos(section, "=") != False:
                name, value = php_explode("=", section, 2)
                return_[urldecode(name)][-1] = urldecode(value)
            else:
                return_[urldecode(section)][-1] = None
            # end if
        # end for
        return return_
    # end def parse_str
    #// 
    #// Detect XML encoding, as per XML 1.0 Appendix F.1
    #// 
    #// @todo Add support for EBCDIC
    #// @param string $data XML data
    #// @param SimplePie_Registry $registry Class registry
    #// @return array Possible encodings
    #//
    @classmethod
    def xml_encoding(self, data=None, registry=None):
        
        #// UTF-32 Big Endian BOM
        if php_substr(data, 0, 4) == "  þÿ":
            encoding[-1] = "UTF-32BE"
            #// UTF-32 Little Endian BOM
        elif php_substr(data, 0, 4) == "ÿþ  ":
            encoding[-1] = "UTF-32LE"
            #// UTF-16 Big Endian BOM
        elif php_substr(data, 0, 2) == "þÿ":
            encoding[-1] = "UTF-16BE"
            #// UTF-16 Little Endian BOM
        elif php_substr(data, 0, 2) == "ÿþ":
            encoding[-1] = "UTF-16LE"
            #// UTF-8 BOM
        elif php_substr(data, 0, 3) == "ï»¿":
            encoding[-1] = "UTF-8"
            #// UTF-32 Big Endian Without BOM
        elif php_substr(data, 0, 20) == "   <   ?   x   m   l":
            pos = php_strpos(data, "   ?   >")
            if pos:
                parser = registry.create("XML_Declaration_Parser", Array(SimplePie_Misc.change_encoding(php_substr(data, 20, pos - 20), "UTF-32BE", "UTF-8")))
                if parser.parse():
                    encoding[-1] = parser.encoding
                # end if
            # end if
            encoding[-1] = "UTF-32BE"
            #// UTF-32 Little Endian Without BOM
        elif php_substr(data, 0, 20) == "<   ?   x   m   l   ":
            pos = php_strpos(data, "?   >   ")
            if pos:
                parser = registry.create("XML_Declaration_Parser", Array(SimplePie_Misc.change_encoding(php_substr(data, 20, pos - 20), "UTF-32LE", "UTF-8")))
                if parser.parse():
                    encoding[-1] = parser.encoding
                # end if
            # end if
            encoding[-1] = "UTF-32LE"
            #// UTF-16 Big Endian Without BOM
        elif php_substr(data, 0, 10) == " < ? x m l":
            pos = php_strpos(data, " ? >")
            if pos:
                parser = registry.create("XML_Declaration_Parser", Array(SimplePie_Misc.change_encoding(php_substr(data, 20, pos - 10), "UTF-16BE", "UTF-8")))
                if parser.parse():
                    encoding[-1] = parser.encoding
                # end if
            # end if
            encoding[-1] = "UTF-16BE"
            #// UTF-16 Little Endian Without BOM
        elif php_substr(data, 0, 10) == "< ? x m l ":
            pos = php_strpos(data, "? > ")
            if pos:
                parser = registry.create("XML_Declaration_Parser", Array(SimplePie_Misc.change_encoding(php_substr(data, 20, pos - 10), "UTF-16LE", "UTF-8")))
                if parser.parse():
                    encoding[-1] = parser.encoding
                # end if
            # end if
            encoding[-1] = "UTF-16LE"
            #// US-ASCII (or superset)
        elif php_substr(data, 0, 5) == "<?xml":
            pos = php_strpos(data, "?>")
            if pos:
                parser = registry.create("XML_Declaration_Parser", Array(php_substr(data, 5, pos - 5)))
                if parser.parse():
                    encoding[-1] = parser.encoding
                # end if
            # end if
            encoding[-1] = "UTF-8"
        else:
            encoding[-1] = "UTF-8"
        # end if
        return encoding
    # end def xml_encoding
    @classmethod
    def output_javascript(self):
        
        if php_function_exists("ob_gzhandler"):
            ob_start("ob_gzhandler")
        # end if
        php_header("Content-type: text/javascript; charset: UTF-8")
        php_header("Cache-Control: must-revalidate")
        php_header("Expires: " + gmdate("D, d M Y H:i:s", time() + 604800) + " GMT")
        pass
        php_print("""function embed_quicktime(type, bgcolor, width, height, link, placeholder, loop) {
    if (placeholder != '') {
        document.writeln('<embed type=\"'+type+'\" style=\"cursor:hand; cursor:pointer;\" href=\"'+link+'\" src=\"'+placeholder+'\" width=\"'+width+'\" height=\"'+height+'\" autoplay=\"false\" target=\"myself\" controller=\"false\" loop=\"'+loop+'\" scale=\"aspect\" bgcolor=\"'+bgcolor+'\" pluginspage=\"http://www.apple.com/quicktime/download/\"></embed>');
        }
    else {
        document.writeln('<embed type=\"'+type+'\" style=\"cursor:hand; cursor:pointer;\" src=\"'+link+'\" width=\"'+width+'\" height=\"'+height+'\" autoplay=\"false\" target=\"myself\" controller=\"true\" loop=\"'+loop+'\" scale=\"aspect\" bgcolor=\"'+bgcolor+'\" pluginspage=\"http://www.apple.com/quicktime/download/\"></embed>');
        }
        }
        function embed_flash(bgcolor, width, height, link, loop, type) {
        document.writeln('<embed src=\"'+link+'\" pluginspage=\"http://www.macromedia.com/go/getflashplayer\" type=\"'+type+'\" quality=\"high\" width=\"'+width+'\" height=\"'+height+'\" bgcolor=\"'+bgcolor+'\" loop=\"'+loop+'\"></embed>');
        }
        function embed_flv(width, height, link, placeholder, loop, player) {
        document.writeln('<embed src=\"'+player+'\" pluginspage=\"http://www.macromedia.com/go/getflashplayer\" type=\"application/x-shockwave-flash\" quality=\"high\" width=\"'+width+'\" height=\"'+height+'\" wmode=\"transparent\" flashvars=\"file='+link+'&autostart=false&repeat='+loop+'&showdigits=true&showfsbutton=false\"></embed>');
        }
        function embed_wmedia(width, height, link) {
        document.writeln('<embed type=\"application/x-mplayer2\" src=\"'+link+'\" autosize=\"1\" width=\"'+width+'\" height=\"'+height+'\" showcontrols=\"1\" showstatusbar=\"0\" showdisplay=\"0\" autostart=\"0\"></embed>');
        }
        """)
    # end def output_javascript
    #// 
    #// Get the SimplePie build timestamp
    #// 
    #// Uses the git index if it exists, otherwise uses the modification time
    #// of the newest file.
    #//
    @classmethod
    def get_build(self):
        
        root = php_dirname(php_dirname(__FILE__))
        if php_file_exists(root + "/.git/index"):
            return filemtime(root + "/.git/index")
        elif php_file_exists(root + "/SimplePie"):
            time = 0
            for file in glob(root + "/SimplePie/*.php"):
                mtime = filemtime(file)
                if mtime > time:
                    time = mtime
                # end if
            # end for
            return time
        elif php_file_exists(php_dirname(__FILE__) + "/Core.php"):
            return filemtime(php_dirname(__FILE__) + "/Core.php")
        else:
            return filemtime(__FILE__)
        # end if
    # end def get_build
    #// 
    #// Format debugging information
    #//
    @classmethod
    def debug(self, sp=None):
        
        info = "SimplePie " + SIMPLEPIE_VERSION + " Build " + SIMPLEPIE_BUILD + "\n"
        info += "PHP " + PHP_VERSION + "\n"
        if sp.error() != None:
            info += "Error occurred: " + sp.error() + "\n"
        else:
            info += "No error found.\n"
        # end if
        info += "Extensions:\n"
        extensions = Array("pcre", "curl", "zlib", "mbstring", "iconv", "xmlreader", "xml")
        for ext in extensions:
            if php_extension_loaded(ext):
                info += str("    ") + str(ext) + str(" loaded\n")
                for case in Switch(ext):
                    if case("pcre"):
                        info += "      Version " + PCRE_VERSION + "\n"
                        break
                    # end if
                    if case("curl"):
                        version = curl_version()
                        info += "      Version " + version["version"] + "\n"
                        break
                    # end if
                    if case("mbstring"):
                        info += "      Overloading: " + mb_get_info("func_overload") + "\n"
                        break
                    # end if
                    if case("iconv"):
                        info += "      Version " + ICONV_VERSION + "\n"
                        break
                    # end if
                    if case("xml"):
                        info += "      Version " + LIBXML_DOTTED_VERSION + "\n"
                        break
                    # end if
                # end for
            else:
                info += str("    ") + str(ext) + str(" not loaded\n")
            # end if
        # end for
        return info
    # end def debug
    @classmethod
    def silence_errors(self, num=None, str=None):
        
        pass
    # end def silence_errors
# end class SimplePie_Misc
