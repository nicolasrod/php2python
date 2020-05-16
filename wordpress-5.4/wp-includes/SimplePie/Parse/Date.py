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
#// Date Parser
#// 
#// @package SimplePie
#// @subpackage Parsing
#//
class SimplePie_Parse_Date():
    date = Array()
    day = Array({"mon": 1, "monday": 1, "tue": 2, "tuesday": 2, "wed": 3, "wednesday": 3, "thu": 4, "thursday": 4, "fri": 5, "friday": 5, "sat": 6, "saturday": 6, "sun": 7, "sunday": 7, "maandag": 1, "dinsdag": 2, "woensdag": 3, "donderdag": 4, "vrijdag": 5, "zaterdag": 6, "zondag": 7, "lundi": 1, "mardi": 2, "mercredi": 3, "jeudi": 4, "vendredi": 5, "samedi": 6, "dimanche": 7, "montag": 1, "dienstag": 2, "mittwoch": 3, "donnerstag": 4, "freitag": 5, "samstag": 6, "sonnabend": 6, "sonntag": 7, "lunedÃ¬": 1, "martedÃ¬": 2, "mercoledÃ¬": 3, "giovedÃ¬": 4, "venerdÃ¬": 5, "sabato": 6, "domenica": 7, "lunes": 1, "martes": 2, "miÃ©rcoles": 3, "jueves": 4, "viernes": 5, "sÃ¡bado": 6, "domingo": 7, "maanantai": 1, "tiistai": 2, "keskiviikko": 3, "torstai": 4, "perjantai": 5, "lauantai": 6, "sunnuntai": 7, "hÃ©tfÅ": 1, "kedd": 2, "szerda": 3, "csÃ¼tÃ¶rtok": 4, "pÃ©ntek": 5, "szombat": 6, "vasÃ¡rnap": 7, "ÎÎµÏ": 1, "Î¤ÏÎ¹": 2, "Î¤ÎµÏ": 3, "Î ÎµÎ¼": 4, "Î Î±Ï": 5, "Î£Î±Î²": 6, "ÎÏÏ": 7})
    month = Array({"jan": 1, "january": 1, "feb": 2, "february": 2, "mar": 3, "march": 3, "apr": 4, "april": 4, "may": 5, "jun": 6, "june": 6, "jul": 7, "july": 7, "aug": 8, "august": 8, "sep": 9, "september": 8, "oct": 10, "october": 10, "nov": 11, "november": 11, "dec": 12, "december": 12, "januari": 1, "februari": 2, "maart": 3, "april": 4, "mei": 5, "juni": 6, "juli": 7, "augustus": 8, "september": 9, "oktober": 10, "november": 11, "december": 12, "janvier": 1, "fÃ©vrier": 2, "mars": 3, "avril": 4, "mai": 5, "juin": 6, "juillet": 7, "aoÃ»t": 8, "septembre": 9, "octobre": 10, "novembre": 11, "dÃ©cembre": 12, "januar": 1, "februar": 2, "mÃ¤rz": 3, "april": 4, "mai": 5, "juni": 6, "juli": 7, "august": 8, "september": 9, "oktober": 10, "november": 11, "dezember": 12, "gennaio": 1, "febbraio": 2, "marzo": 3, "aprile": 4, "maggio": 5, "giugno": 6, "luglio": 7, "agosto": 8, "settembre": 9, "ottobre": 10, "novembre": 11, "dicembre": 12, "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6, "julio": 7, "agosto": 8, "septiembre": 9, "setiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12, "tammikuu": 1, "helmikuu": 2, "maaliskuu": 3, "huhtikuu": 4, "toukokuu": 5, "kesÃ¤kuu": 6, "heinÃ¤kuu": 7, "elokuu": 8, "suuskuu": 9, "lokakuu": 10, "marras": 11, "joulukuu": 12, "januÃ¡r": 1, "februÃ¡r": 2, "mÃ¡rcius": 3, "Ã¡prilis": 4, "mÃ¡jus": 5, "jÃºnius": 6, "jÃºlius": 7, "augusztus": 8, "szeptember": 9, "oktÃ³ber": 10, "november": 11, "december": 12, "ÎÎ±Î½": 1, "Î¦ÎµÎ²": 2, "ÎÎ¬Ï": 3, "ÎÎ±Ï": 3, "ÎÏÏ": 4, "ÎÎ¬Î¹": 5, "ÎÎ±Ï": 5, "ÎÎ±Î¹": 5, "ÎÎ¿ÏÎ½": 6, "ÎÎ¿Î½": 6, "ÎÎ¿ÏÎ»": 7, "ÎÎ¿Î»": 7, "ÎÏÎ³": 8, "ÎÏÎ³": 8, "Î£ÎµÏ": 9, "ÎÎºÏ": 10, "ÎÎ¿Î­": 11, "ÎÎµÎº": 12})
    timezone = Array({"ACDT": 37800, "ACIT": 28800, "ACST": 34200, "ACT": -18000, "ACWDT": 35100, "ACWST": 31500, "AEDT": 39600, "AEST": 36000, "AFT": 16200, "AKDT": -28800, "AKST": -32400, "AMDT": 18000, "AMT": -14400, "ANAST": 46800, "ANAT": 43200, "ART": -10800, "AZOST": -3600, "AZST": 18000, "AZT": 14400, "BIOT": 21600, "BIT": -43200, "BOT": -14400, "BRST": -7200, "BRT": -10800, "BST": 3600, "BTT": 21600, "CAST": 18000, "CAT": 7200, "CCT": 23400, "CDT": -18000, "CEDT": 7200, "CEST": 7200, "CET": 3600, "CGST": -7200, "CGT": -10800, "CHADT": 49500, "CHAST": 45900, "CIST": -28800, "CKT": -36000, "CLDT": -10800, "CLST": -14400, "COT": -18000, "CST": -21600, "CVT": -3600, "CXT": 25200, "DAVT": 25200, "DTAT": 36000, "EADT": -18000, "EAST": -21600, "EAT": 10800, "ECT": -18000, "EDT": -14400, "EEST": 10800, "EET": 7200, "EGT": -3600, "EKST": 21600, "EST": -18000, "FJT": 43200, "FKDT": -10800, "FKST": -14400, "FNT": -7200, "GALT": -21600, "GEDT": 14400, "GEST": 10800, "GFT": -10800, "GILT": 43200, "GIT": -32400, "GST": 14400, "GST": -7200, "GYT": -14400, "HAA": -10800, "HAC": -18000, "HADT": -32400, "HAE": -14400, "HAP": -25200, "HAR": -21600, "HAST": -36000, "HAT": -9000, "HAY": -28800, "HKST": 28800, "HMT": 18000, "HNA": -14400, "HNC": -21600, "HNE": -18000, "HNP": -28800, "HNR": -25200, "HNT": -12600, "HNY": -32400, "IRDT": 16200, "IRKST": 32400, "IRKT": 28800, "IRST": 12600, "JFDT": -10800, "JFST": -14400, "JST": 32400, "KGST": 21600, "KGT": 18000, "KOST": 39600, "KOVST": 28800, "KOVT": 25200, "KRAST": 28800, "KRAT": 25200, "KST": 32400, "LHDT": 39600, "LHST": 37800, "LINT": 50400, "LKT": 21600, "MAGST": 43200, "MAGT": 39600, "MAWT": 21600, "MDT": -21600, "MESZ": 7200, "MEZ": 3600, "MHT": 43200, "MIT": -34200, "MNST": 32400, "MSDT": 14400, "MSST": 10800, "MST": -25200, "MUT": 14400, "MVT": 18000, "MYT": 28800, "NCT": 39600, "NDT": -9000, "NFT": 41400, "NMIT": 36000, "NOVST": 25200, "NOVT": 21600, "NPT": 20700, "NRT": 43200, "NST": -12600, "NUT": -39600, "NZDT": 46800, "NZST": 43200, "OMSST": 25200, "OMST": 21600, "PDT": -25200, "PET": -18000, "PETST": 46800, "PETT": 43200, "PGT": 36000, "PHOT": 46800, "PHT": 28800, "PKT": 18000, "PMDT": -7200, "PMST": -10800, "PONT": 39600, "PST": -28800, "PWT": 32400, "PYST": -10800, "PYT": -14400, "RET": 14400, "ROTT": -10800, "SAMST": 18000, "SAMT": 14400, "SAST": 7200, "SBT": 39600, "SCDT": 46800, "SCST": 43200, "SCT": 14400, "SEST": 3600, "SGT": 28800, "SIT": 28800, "SRT": -10800, "SST": -39600, "SYST": 10800, "SYT": 7200, "TFT": 18000, "THAT": -36000, "TJT": 18000, "TKT": -36000, "TMT": 18000, "TOT": 46800, "TPT": 32400, "TRUT": 36000, "TVT": 43200, "TWT": 28800, "UYST": -7200, "UYT": -10800, "UZT": 18000, "VET": -14400, "VLAST": 39600, "VLAT": 36000, "VOST": 21600, "VUT": 39600, "WAST": 7200, "WAT": 3600, "WDT": 32400, "WEST": 3600, "WFT": 43200, "WIB": 25200, "WIT": 32400, "WITA": 28800, "WKST": 18000, "WST": 28800, "YAKST": 36000, "YAKT": 32400, "YAPT": 36000, "YEKST": 21600, "YEKT": 18000})
    day_pcre = Array()
    month_pcre = Array()
    built_in = Array()
    user = Array()
    #// 
    #// Create new SimplePie_Parse_Date object, and set self::day_pcre,
    #// self::month_pcre, and self::built_in
    #// 
    #// @access private
    #//
    def __init__(self):
        
        self.day_pcre = "(" + php_implode("|", php_array_keys(self.day)) + ")"
        self.month_pcre = "(" + php_implode("|", php_array_keys(self.month)) + ")"
        __init__.cache = None
        if (not (php_isset(lambda : __init__.cache[get_class(self)]))):
            all_methods = get_class_methods(self)
            for method in all_methods:
                if php_strtolower(php_substr(method, 0, 5)) == "date_":
                    __init__.cache[get_class(self)][-1] = method
                # end if
            # end for
        # end if
        for method in __init__.cache[get_class(self)]:
            self.built_in[-1] = method
        # end for
    # end def __init__
    #// 
    #// Get the object
    #// 
    #// @access public
    #//
    @classmethod
    def get(self):
        
        get.object = None
        if (not get.object):
            get.object = php_new_class("SimplePie_Parse_Date", lambda : SimplePie_Parse_Date())
        # end if
        return get.object
    # end def get
    #// 
    #// Parse a date
    #// 
    #// @final
    #// @access public
    #// @param string $date Date to parse
    #// @return int Timestamp corresponding to date string, or false on failure
    #//
    def parse(self, date=None):
        
        for method in self.user:
            returned = php_call_user_func(method, date)
            if returned != False:
                return returned
            # end if
        # end for
        for method in self.built_in:
            returned = php_call_user_func(Array(self, method), date)
            if returned != False:
                return returned
            # end if
        # end for
        return False
    # end def parse
    #// 
    #// Add a callback method to parse a date
    #// 
    #// @final
    #// @access public
    #// @param callable $callback
    #//
    def add_callback(self, callback=None):
        
        if php_is_callable(callback):
            self.user[-1] = callback
        else:
            trigger_error("User-supplied function must be a valid callback", E_USER_WARNING)
        # end if
    # end def add_callback
    #// 
    #// Parse a superset of W3C-DTF (allows hyphens and colons to be omitted, as
    #// well as allowing any of upper or lower case "T", horizontal tabs, or
    #// spaces to be used as the time seperator (including more than one))
    #// 
    #// @access protected
    #// @return int Timestamp
    #//
    def date_w3cdtf(self, date=None):
        
        date_w3cdtf.pcre = None
        if (not date_w3cdtf.pcre):
            year = "([0-9]{4})"
            month = day
            decimal = "([0-9]*)"
            zone = "(?:(Z)|([+\\-])([0-9]{1,2}):?([0-9]{1,2}))"
            date_w3cdtf.pcre = "/^" + year + "(?:-?" + month + "(?:-?" + day + "(?:[Tt\\x09\\x20]+" + hour + "(?::?" + minute + "(?::?" + second + "(?:." + decimal + ")?)?)?" + zone + ")?)?)?$/"
        # end if
        if php_preg_match(date_w3cdtf.pcre, date, match):
            #// 
            #// Capturing subpatterns:
            #// 1: Year
            #// 2: Month
            #// 3: Day
            #// 4: Hour
            #// 5: Minute
            #// 6: Second
            #// 7: Decimal fraction of a second
            #// 8: Zulu
            #// 9: Timezone ±
            #// 10: Timezone hours
            #// 11: Timezone minutes
            #// 
            #// Fill in empty matches
            i = php_count(match)
            while i <= 3:
                
                match[i] = "1"
                i += 1
            # end while
            i = php_count(match)
            while i <= 7:
                
                match[i] = "0"
                i += 1
            # end while
            #// Numeric timezone
            if (php_isset(lambda : match[9])) and match[9] != "":
                timezone = match[10] * 3600
                timezone += match[11] * 60
                if match[9] == "-":
                    timezone = 0 - timezone
                # end if
            else:
                timezone = 0
            # end if
            #// Convert the number of seconds to an integer, taking decimals into account
            second = round(match[6] + match[7] / pow(10, php_strlen(match[7])))
            return gmmktime(match[4], match[5], second, match[2], match[3], match[1]) - timezone
        else:
            return False
        # end if
    # end def date_w3cdtf
    #// 
    #// Remove RFC822 comments
    #// 
    #// @access protected
    #// @param string $data Data to strip comments from
    #// @return string Comment stripped string
    #//
    def remove_rfc2822_comments(self, string=None):
        
        string = php_str(string)
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
    # end def remove_rfc2822_comments
    #// 
    #// Parse RFC2822's date format
    #// 
    #// @access protected
    #// @return int Timestamp
    #//
    def date_rfc2822(self, date=None):
        
        date_rfc2822.pcre = None
        if (not date_rfc2822.pcre):
            wsp = "[\\x09\\x20]"
            fws = "(?:" + wsp + "+|" + wsp + "*(?:\\x0D\\x0A" + wsp + "+)+)"
            optional_fws = fws + "?"
            day_name = self.day_pcre
            month = self.month_pcre
            day = "([0-9]{1,2})"
            hour = minute
            year = "([0-9]{2,4})"
            num_zone = "([+\\-])([0-9]{2})([0-9]{2})"
            character_zone = "([A-Z]{1,5})"
            zone = "(?:" + num_zone + "|" + character_zone + ")"
            date_rfc2822.pcre = "/(?:" + optional_fws + day_name + optional_fws + ",)?" + optional_fws + day + fws + month + fws + year + fws + hour + optional_fws + ":" + optional_fws + minute + "(?:" + optional_fws + ":" + optional_fws + second + ")?" + fws + zone + "/i"
        # end if
        if php_preg_match(date_rfc2822.pcre, self.remove_rfc2822_comments(date), match):
            #// 
            #// Capturing subpatterns:
            #// 1: Day name
            #// 2: Day
            #// 3: Month
            #// 4: Year
            #// 5: Hour
            #// 6: Minute
            #// 7: Second
            #// 8: Timezone ±
            #// 9: Timezone hours
            #// 10: Timezone minutes
            #// 11: Alphabetic timezone
            #// 
            #// Find the month number
            month = self.month[php_strtolower(match[3])]
            #// Numeric timezone
            if match[8] != "":
                timezone = match[9] * 3600
                timezone += match[10] * 60
                if match[8] == "-":
                    timezone = 0 - timezone
                # end if
                #// Character timezone
            elif (php_isset(lambda : self.timezone[php_strtoupper(match[11])])):
                timezone = self.timezone[php_strtoupper(match[11])]
            else:
                timezone = 0
            # end if
            #// Deal with 2/3 digit years
            if match[4] < 50:
                match[4] += 2000
            elif match[4] < 1000:
                match[4] += 1900
            # end if
            #// Second is optional, if it is empty set it to zero
            if match[7] != "":
                second = match[7]
            else:
                second = 0
            # end if
            return gmmktime(match[5], match[6], second, month, match[2], match[4]) - timezone
        else:
            return False
        # end if
    # end def date_rfc2822
    #// 
    #// Parse RFC850's date format
    #// 
    #// @access protected
    #// @return int Timestamp
    #//
    def date_rfc850(self, date=None):
        
        date_rfc850.pcre = None
        if (not date_rfc850.pcre):
            space = "[\\x09\\x20]+"
            day_name = self.day_pcre
            month = self.month_pcre
            day = "([0-9]{1,2})"
            year = hour
            zone = "([A-Z]{1,5})"
            date_rfc850.pcre = "/^" + day_name + "," + space + day + "-" + month + "-" + year + space + hour + ":" + minute + ":" + second + space + zone + "$/i"
        # end if
        if php_preg_match(date_rfc850.pcre, date, match):
            #// 
            #// Capturing subpatterns:
            #// 1: Day name
            #// 2: Day
            #// 3: Month
            #// 4: Year
            #// 5: Hour
            #// 6: Minute
            #// 7: Second
            #// 8: Timezone
            #// 
            #// Month
            month = self.month[php_strtolower(match[3])]
            #// Character timezone
            if (php_isset(lambda : self.timezone[php_strtoupper(match[8])])):
                timezone = self.timezone[php_strtoupper(match[8])]
            else:
                timezone = 0
            # end if
            #// Deal with 2 digit year
            if match[4] < 50:
                match[4] += 2000
            else:
                match[4] += 1900
            # end if
            return gmmktime(match[5], match[6], match[7], month, match[2], match[4]) - timezone
        else:
            return False
        # end if
    # end def date_rfc850
    #// 
    #// Parse C99's asctime()'s date format
    #// 
    #// @access protected
    #// @return int Timestamp
    #//
    def date_asctime(self, date=None):
        
        date_asctime.pcre = None
        if (not date_asctime.pcre):
            space = "[\\x09\\x20]+"
            wday_name = self.day_pcre
            mon_name = self.month_pcre
            day = "([0-9]{1,2})"
            hour = sec
            year = "([0-9]{4})"
            terminator = "\\x0A?\\x00?"
            date_asctime.pcre = "/^" + wday_name + space + mon_name + space + day + space + hour + ":" + min + ":" + sec + space + year + terminator + "$/i"
        # end if
        if php_preg_match(date_asctime.pcre, date, match):
            #// 
            #// Capturing subpatterns:
            #// 1: Day name
            #// 2: Month
            #// 3: Day
            #// 4: Hour
            #// 5: Minute
            #// 6: Second
            #// 7: Year
            #//
            month = self.month[php_strtolower(match[2])]
            return gmmktime(match[4], match[5], match[6], month, match[3], match[7])
        else:
            return False
        # end if
    # end def date_asctime
    #// 
    #// Parse dates using strtotime()
    #// 
    #// @access protected
    #// @return int Timestamp
    #//
    def date_strtotime(self, date=None):
        
        strtotime = strtotime(date)
        if strtotime == -1 or strtotime == False:
            return False
        else:
            return strtotime
        # end if
    # end def date_strtotime
# end class SimplePie_Parse_Date
