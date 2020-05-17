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
#// Decode HTML Entities
#// 
#// This implements HTML5 as of revision 967 (2007-06-28)
#// 
#// @deprecated Use DOMDocument instead!
#// @package SimplePie
#//
class SimplePie_Decode_HTML_Entities():
    #// 
    #// Data to be parsed
    #// 
    #// @access private
    #// @var string
    #//
    data = ""
    #// 
    #// Currently consumed bytes
    #// 
    #// @access private
    #// @var string
    #//
    consumed = ""
    #// 
    #// Position of the current byte being parsed
    #// 
    #// @access private
    #// @var int
    #//
    position = 0
    #// 
    #// Create an instance of the class with the input data
    #// 
    #// @access public
    #// @param string $data Input data
    #//
    def __init__(self, data_=None):
        
        
        self.data = data_
    # end def __init__
    #// 
    #// Parse the input data
    #// 
    #// @access public
    #// @return string Output data
    #//
    def parse(self):
        
        
        while True:
            self.position = php_strpos(self.data, "&", self.position)
            if not (self.position != False):
                break
            # end if
            self.consume()
            self.entity()
            self.consumed = ""
        # end while
        return self.data
    # end def parse
    #// 
    #// Consume the next byte
    #// 
    #// @access private
    #// @return mixed The next byte, or false, if there is no more data
    #//
    def consume(self):
        
        
        if (php_isset(lambda : self.data[self.position])):
            self.consumed += self.data[self.position]
            self.position += 1
            return self.data[self.position]
            self.position += 1
        else:
            return False
        # end if
    # end def consume
    #// 
    #// Consume a range of characters
    #// 
    #// @access private
    #// @param string $chars Characters to consume
    #// @return mixed A series of characters that match the range, or false
    #//
    def consume_range(self, chars_=None):
        
        
        len_ = strspn(self.data, chars_, self.position)
        if len_:
            data_ = php_substr(self.data, self.position, len_)
            self.consumed += data_
            self.position += len_
            return data_
        else:
            return False
        # end if
    # end def consume_range
    #// 
    #// Unconsume one byte
    #// 
    #// @access private
    #//
    def unconsume(self):
        
        
        self.consumed = php_substr(self.consumed, 0, -1)
        self.position -= 1
    # end def unconsume
    #// 
    #// Decode an entity
    #// 
    #// @access private
    #//
    def entity(self):
        
        
        for case in Switch(self.consume()):
            if case("   "):
                pass
            # end if
            if case("\n"):
                pass
            # end if
            if case(""):
                pass
            # end if
            if case(""):
                pass
            # end if
            if case(""):
                pass
            # end if
            if case(" "):
                pass
            # end if
            if case("<"):
                pass
            # end if
            if case("&"):
                pass
            # end if
            if case(False):
                break
            # end if
            if case("#"):
                for case in Switch(self.consume()):
                    if case("x"):
                        pass
                    # end if
                    if case("X"):
                        range_ = "0123456789ABCDEFabcdef"
                        hex_ = True
                        break
                    # end if
                    if case():
                        range_ = "0123456789"
                        hex_ = False
                        self.unconsume()
                        break
                    # end if
                # end for
                codepoint_ = self.consume_range(range_)
                if codepoint_:
                    windows_1252_specials_ = Array({13: "\n", 128: "â¬", 129: "ï¿½", 130: "â", 131: "Æ", 132: "â", 133: "â¦", 134: "â ", 135: "â¡", 136: "Ë", 137: "â°", 138: "Å ", 139: "â¹", 140: "Å", 141: "ï¿½", 142: "Å½", 143: "ï¿½", 144: "ï¿½", 145: "â", 146: "â", 147: "â", 148: "â", 149: "â¢", 150: "â", 151: "â", 152: "Ë", 153: "â¢", 154: "Å¡", 155: "âº", 156: "Å", 157: "ï¿½", 158: "Å¾", 159: "Å¸"})
                    if hex_:
                        codepoint_ = hexdec(codepoint_)
                    else:
                        codepoint_ = php_intval(codepoint_)
                    # end if
                    if (php_isset(lambda : windows_1252_specials_[codepoint_])):
                        replacement_ = windows_1252_specials_[codepoint_]
                    else:
                        replacement_ = SimplePie_Misc.codepoint_to_utf8(codepoint_)
                    # end if
                    if (not php_in_array(self.consume(), Array(";", False), True)):
                        self.unconsume()
                    # end if
                    consumed_length_ = php_strlen(self.consumed)
                    self.data = php_substr_replace(self.data, replacement_, self.position - consumed_length_, consumed_length_)
                    self.position += php_strlen(replacement_) - consumed_length_
                # end if
                break
            # end if
            if case():
                entities_ = Array({"Aacute": "Ã", "aacute": "Ã¡", "Aacute;": "Ã", "aacute;": "Ã¡", "Acirc": "Ã", "acirc": "Ã¢", "Acirc;": "Ã", "acirc;": "Ã¢", "acute": "Â´", "acute;": "Â´", "AElig": "Ã", "aelig": "Ã¦", "AElig;": "Ã", "aelig;": "Ã¦", "Agrave": "Ã", "agrave": "Ã ", "Agrave;": "Ã", "agrave;": "Ã ", "alefsym;": "âµ", "Alpha;": "Î", "alpha;": "Î±", "AMP": "&", "amp": "&", "AMP;": "&", "amp;": "&", "and;": "â§", "ang;": "â ", "apos;": "'", "Aring": "Ã", "aring": "Ã¥", "Aring;": "Ã", "aring;": "Ã¥", "asymp;": "â", "Atilde": "Ã", "atilde": "Ã£", "Atilde;": "Ã", "atilde;": "Ã£", "Auml": "Ã", "auml": "Ã¤", "Auml;": "Ã", "auml;": "Ã¤", "bdquo;": "â", "Beta;": "Î", "beta;": "Î²", "brvbar": "Â¦", "brvbar;": "Â¦", "bull;": "â¢", "cap;": "â©", "Ccedil": "Ã", "ccedil": "Ã§", "Ccedil;": "Ã", "ccedil;": "Ã§", "cedil": "Â¸", "cedil;": "Â¸", "cent": "Â¢", "cent;": "Â¢", "Chi;": "Î§", "chi;": "Ï", "circ;": "Ë", "clubs;": "â£", "cong;": "â", "COPY": "Â©", "copy": "Â©", "COPY;": "Â©", "copy;": "Â©", "crarr;": "âµ", "cup;": "âª", "curren": "Â¤", "curren;": "Â¤", "Dagger;": "â¡", "dagger;": "â ", "dArr;": "â", "darr;": "â", "deg": "Â°", "deg;": "Â°", "Delta;": "Î", "delta;": "Î´", "diams;": "â¦", "divide": "Ã·", "divide;": "Ã·", "Eacute": "Ã", "eacute": "Ã©", "Eacute;": "Ã", "eacute;": "Ã©", "Ecirc": "Ã", "ecirc": "Ãª", "Ecirc;": "Ã", "ecirc;": "Ãª", "Egrave": "Ã", "egrave": "Ã¨", "Egrave;": "Ã", "egrave;": "Ã¨", "empty;": "â", "emsp;": "â", "ensp;": "â", "Epsilon;": "Î", "epsilon;": "Îµ", "equiv;": "â¡", "Eta;": "Î", "eta;": "Î·", "ETH": "Ã", "eth": "Ã°", "ETH;": "Ã", "eth;": "Ã°", "Euml": "Ã", "euml": "Ã«", "Euml;": "Ã", "euml;": "Ã«", "euro;": "â¬", "exist;": "â", "fnof;": "Æ", "forall;": "â", "frac12": "Â½", "frac12;": "Â½", "frac14": "Â¼", "frac14;": "Â¼", "frac34": "Â¾", "frac34;": "Â¾", "frasl;": "â", "Gamma;": "Î", "gamma;": "Î³", "ge;": "â¥", "GT": ">", "gt": ">", "GT;": ">", "gt;": ">", "hArr;": "â", "harr;": "â", "hearts;": "â¥", "hellip;": "â¦", "Iacute": "Ã", "iacute": "Ã­", "Iacute;": "Ã", "iacute;": "Ã­", "Icirc": "Ã", "icirc": "Ã®", "Icirc;": "Ã", "icirc;": "Ã®", "iexcl": "Â¡", "iexcl;": "Â¡", "Igrave": "Ã", "igrave": "Ã¬", "Igrave;": "Ã", "igrave;": "Ã¬", "image;": "â", "infin;": "â", "int;": "â«", "Iota;": "Î", "iota;": "Î¹", "iquest": "Â¿", "iquest;": "Â¿", "isin;": "â", "Iuml": "Ã", "iuml": "Ã¯", "Iuml;": "Ã", "iuml;": "Ã¯", "Kappa;": "Î", "kappa;": "Îº", "Lambda;": "Î", "lambda;": "Î»", "lang;": "ã", "laquo": "Â«", "laquo;": "Â«", "lArr;": "â", "larr;": "â", "lceil;": "â", "ldquo;": "â", "le;": "â¤", "lfloor;": "â", "lowast;": "â", "loz;": "â", "lrm;": "â", "lsaquo;": "â¹", "lsquo;": "â", "LT": "<", "lt": "<", "LT;": "<", "lt;": "<", "macr": "Â¯", "macr;": "Â¯", "mdash;": "â", "micro": "Âµ", "micro;": "Âµ", "middot": "Â·", "middot;": "Â·", "minus;": "â", "Mu;": "Î", "mu;": "Î¼", "nabla;": "â", "nbsp": "Â ", "nbsp;": "Â ", "ndash;": "â", "ne;": "â ", "ni;": "â", "not": "Â¬", "not;": "Â¬", "notin;": "â", "nsub;": "â", "Ntilde": "Ã", "ntilde": "Ã±", "Ntilde;": "Ã", "ntilde;": "Ã±", "Nu;": "Î", "nu;": "Î½", "Oacute": "Ã", "oacute": "Ã³", "Oacute;": "Ã", "oacute;": "Ã³", "Ocirc": "Ã", "ocirc": "Ã´", "Ocirc;": "Ã", "ocirc;": "Ã´", "OElig;": "Å", "oelig;": "Å", "Ograve": "Ã", "ograve": "Ã²", "Ograve;": "Ã", "ograve;": "Ã²", "oline;": "â¾", "Omega;": "Î©", "omega;": "Ï", "Omicron;": "Î", "omicron;": "Î¿", "oplus;": "â", "or;": "â¨", "ordf": "Âª", "ordf;": "Âª", "ordm": "Âº", "ordm;": "Âº", "Oslash": "Ã", "oslash": "Ã¸", "Oslash;": "Ã", "oslash;": "Ã¸", "Otilde": "Ã", "otilde": "Ãµ", "Otilde;": "Ã", "otilde;": "Ãµ", "otimes;": "â", "Ouml": "Ã", "ouml": "Ã¶", "Ouml;": "Ã", "ouml;": "Ã¶", "para": "Â¶", "para;": "Â¶", "part;": "â", "permil;": "â°", "perp;": "â¥", "Phi;": "Î¦", "phi;": "Ï", "Pi;": "Î ", "pi;": "Ï", "piv;": "Ï", "plusmn": "Â±", "plusmn;": "Â±", "pound": "Â£", "pound;": "Â£", "Prime;": "â³", "prime;": "â²", "prod;": "â", "prop;": "â", "Psi;": "Î¨", "psi;": "Ï", "QUOT": "\"", "quot": "\"", "QUOT;": "\"", "quot;": "\"", "radic;": "â", "rang;": "ã", "raquo": "Â»", "raquo;": "Â»", "rArr;": "â", "rarr;": "â", "rceil;": "â", "rdquo;": "â", "real;": "â", "REG": "Â®", "reg": "Â®", "REG;": "Â®", "reg;": "Â®", "rfloor;": "â", "Rho;": "Î¡", "rho;": "Ï", "rlm;": "â", "rsaquo;": "âº", "rsquo;": "â", "sbquo;": "â", "Scaron;": "Å ", "scaron;": "Å¡", "sdot;": "â", "sect": "Â§", "sect;": "Â§", "shy": "Â­", "shy;": "Â­", "Sigma;": "Î£", "sigma;": "Ï", "sigmaf;": "Ï", "sim;": "â¼", "spades;": "â ", "sub;": "â", "sube;": "â", "sum;": "â", "sup;": "â", "sup1": "Â¹", "sup1;": "Â¹", "sup2": "Â²", "sup2;": "Â²", "sup3": "Â³", "sup3;": "Â³", "supe;": "â", "szlig": "Ã", "szlig;": "Ã", "Tau;": "Î¤", "tau;": "Ï", "there4;": "â´", "Theta;": "Î", "theta;": "Î¸", "thetasym;": "Ï", "thinsp;": "â", "THORN": "Ã", "thorn": "Ã¾", "THORN;": "Ã", "thorn;": "Ã¾", "tilde;": "Ë", "times": "Ã", "times;": "Ã", "TRADE;": "â¢", "trade;": "â¢", "Uacute": "Ã", "uacute": "Ãº", "Uacute;": "Ã", "uacute;": "Ãº", "uArr;": "â", "uarr;": "â", "Ucirc": "Ã", "ucirc": "Ã»", "Ucirc;": "Ã", "ucirc;": "Ã»", "Ugrave": "Ã", "ugrave": "Ã¹", "Ugrave;": "Ã", "ugrave;": "Ã¹", "uml": "Â¨", "uml;": "Â¨", "upsih;": "Ï", "Upsilon;": "Î¥", "upsilon;": "Ï", "Uuml": "Ã", "uuml": "Ã¼", "Uuml;": "Ã", "uuml;": "Ã¼", "weierp;": "â", "Xi;": "Î", "xi;": "Î¾", "Yacute": "Ã", "yacute": "Ã½", "Yacute;": "Ã", "yacute;": "Ã½", "yen": "Â¥", "yen;": "Â¥", "yuml": "Ã¿", "Yuml;": "Å¸", "yuml;": "Ã¿", "Zeta;": "Î", "zeta;": "Î¶", "zwj;": "â", "zwnj;": "â"})
                i_ = 0
                match_ = None
                while i_ < 9 and self.consume() != False:
                    
                    consumed_ = php_substr(self.consumed, 1)
                    if (php_isset(lambda : entities_[consumed_])):
                        match_ = consumed_
                    # end if
                    i_ += 1
                # end while
                if match_ != None:
                    self.data = php_substr_replace(self.data, entities_[match_], self.position - php_strlen(consumed_) - 1, php_strlen(match_) + 1)
                    self.position += php_strlen(entities_[match_]) - php_strlen(consumed_) - 1
                # end if
                break
            # end if
        # end for
    # end def entity
# end class SimplePie_Decode_HTML_Entities
