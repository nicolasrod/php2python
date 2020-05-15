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
#// IDNA URL encoder
#// 
#// Note: Not fully compliant, as nameprep does nothing yet.
#// 
#// @package Requests
#// @subpackage Utilities
#// @see https://tools.ietf.org/html/rfc3490 IDNA specification
#// @see https://tools.ietf.org/html/rfc3492 Punycode/Bootstrap specification
#//
class Requests_IDNAEncoder():
    ACE_PREFIX = "xn--"
    BOOTSTRAP_BASE = 36
    BOOTSTRAP_TMIN = 1
    BOOTSTRAP_TMAX = 26
    BOOTSTRAP_SKEW = 38
    BOOTSTRAP_DAMP = 700
    BOOTSTRAP_INITIAL_BIAS = 72
    BOOTSTRAP_INITIAL_N = 128
    #// #@-
    #// 
    #// Encode a hostname using Punycode
    #// 
    #// @param string $string Hostname
    #// @return string Punycode-encoded hostname
    #//
    @classmethod
    def encode(self, string=None):
        
        parts = php_explode(".", string)
        for part in parts:
            part = self.to_ascii(part)
        # end for
        return php_implode(".", parts)
    # end def encode
    #// 
    #// Convert a UTF-8 string to an ASCII string using Punycode
    #// 
    #// @throws Requests_Exception Provided string longer than 64 ASCII characters (`idna.provided_too_long`)
    #// @throws Requests_Exception Prepared string longer than 64 ASCII characters (`idna.prepared_too_long`)
    #// @throws Requests_Exception Provided string already begins with xn-- (`idna.provided_is_prefixed`)
    #// @throws Requests_Exception Encoded string longer than 64 ASCII characters (`idna.encoded_too_long`)
    #// 
    #// @param string $string ASCII or UTF-8 string (max length 64 characters)
    #// @return string ASCII string
    #//
    @classmethod
    def to_ascii(self, string=None):
        
        #// Step 1: Check if the string is already ASCII
        if self.is_ascii(string):
            #// Skip to step 7
            if php_strlen(string) < 64:
                return string
            # end if
            raise php_new_class("Requests_Exception", lambda : Requests_Exception("Provided string is too long", "idna.provided_too_long", string))
        # end if
        #// Step 2: nameprep
        string = self.nameprep(string)
        #// Step 3: UseSTD3ASCIIRules is false, continue
        #// Step 4: Check if it's ASCII now
        if self.is_ascii(string):
            #// Skip to step 7
            if php_strlen(string) < 64:
                return string
            # end if
            raise php_new_class("Requests_Exception", lambda : Requests_Exception("Prepared string is too long", "idna.prepared_too_long", string))
        # end if
        #// Step 5: Check ACE prefix
        if php_strpos(string, self.ACE_PREFIX) == 0:
            raise php_new_class("Requests_Exception", lambda : Requests_Exception("Provided string begins with ACE prefix", "idna.provided_is_prefixed", string))
        # end if
        #// Step 6: Encode with Punycode
        string = self.punycode_encode(string)
        #// Step 7: Prepend ACE prefix
        string = self.ACE_PREFIX + string
        #// Step 8: Check size
        if php_strlen(string) < 64:
            return string
        # end if
        raise php_new_class("Requests_Exception", lambda : Requests_Exception("Encoded string is too long", "idna.encoded_too_long", string))
    # end def to_ascii
    #// 
    #// Check whether a given string contains only ASCII characters
    #// 
    #// @internal (Testing found regex was the fastest implementation)
    #// 
    #// @param string $string
    #// @return bool Is the string ASCII-only?
    #//
    def is_ascii(self, string=None):
        
        return php_preg_match("/(?:[^\\x00-\\x7F])/", string) != 1
    # end def is_ascii
    #// 
    #// Prepare a string for use as an IDNA name
    #// 
    #// @todo Implement this based on RFC 3491 and the newer 5891
    #// @param string $string
    #// @return string Prepared string
    #//
    def nameprep(self, string=None):
        
        return string
    # end def nameprep
    #// 
    #// Convert a UTF-8 string to a UCS-4 codepoint array
    #// 
    #// Based on Requests_IRI::replace_invalid_with_pct_encoding()
    #// 
    #// @throws Requests_Exception Invalid UTF-8 codepoint (`idna.invalidcodepoint`)
    #// @param string $input
    #// @return array Unicode code points
    #//
    def utf8_to_codepoints(self, input=None):
        
        codepoints = Array()
        #// Get number of bytes
        strlen = php_strlen(input)
        position = 0
        while position < strlen:
            
            value = php_ord(input[position])
            #// One byte sequence:
            if (1 << (value).bit_length()) - 1 - value & 128 == 128:
                character = value
                length = 1
                remaining = 0
                #// Two byte sequence:
            elif value & 224 == 192:
                character = value & 31 << 6
                length = 2
                remaining = 1
                #// Three byte sequence:
            elif value & 240 == 224:
                character = value & 15 << 12
                length = 3
                remaining = 2
                #// Four byte sequence:
            elif value & 248 == 240:
                character = value & 7 << 18
                length = 4
                remaining = 3
            else:
                raise php_new_class("Requests_Exception", lambda : Requests_Exception("Invalid Unicode codepoint", "idna.invalidcodepoint", value))
            # end if
            if remaining > 0:
                if position + length > strlen:
                    raise php_new_class("Requests_Exception", lambda : Requests_Exception("Invalid Unicode codepoint", "idna.invalidcodepoint", character))
                # end if
                position += 1
                while remaining > 0:
                    
                    value = php_ord(input[position])
                    #// If it is invalid, count the sequence as invalid and reprocess the current byte:
                    if value & 192 != 128:
                        raise php_new_class("Requests_Exception", lambda : Requests_Exception("Invalid Unicode codepoint", "idna.invalidcodepoint", character))
                    # end if
                    remaining -= 1
                    character |= value & 63 << remaining * 6
                    position += 1
                # end while
                position -= 1
            # end if
            if length > 1 and character <= 127 or length > 2 and character <= 2047 or length > 3 and character <= 65535 or character & 65534 == 65534 or character >= 64976 and character <= 65007 or character > 55295 and character < 63744 or character < 32 or character > 126 and character < 160 or character > 983037:
                raise php_new_class("Requests_Exception", lambda : Requests_Exception("Invalid Unicode codepoint", "idna.invalidcodepoint", character))
            # end if
            codepoints[-1] = character
            position += 1
        # end while
        return codepoints
    # end def utf8_to_codepoints
    #// 
    #// RFC3492-compliant encoder
    #// 
    #// @internal Pseudo-code from Section 6.3 is commented with "#" next to relevant code
    #// @throws Requests_Exception On character outside of the domain (never happens with Punycode) (`idna.character_outside_domain`)
    #// 
    #// @param string $input UTF-8 encoded string to encode
    #// @return string Punycode-encoded string
    #//
    @classmethod
    def punycode_encode(self, input=None):
        
        output = ""
        #// #       let n = initial_n
        n = self.BOOTSTRAP_INITIAL_N
        #// #       let delta = 0
        delta = 0
        #// #       let bias = initial_bias
        bias = self.BOOTSTRAP_INITIAL_BIAS
        #// #       let h = b = the number of basic code points in the input
        h = b = 0
        #// see loop
        #// #       copy them to the output in order
        codepoints = self.utf8_to_codepoints(input)
        extended = Array()
        for char in codepoints:
            if char < 128:
                #// Character is valid ASCII
                #// TODO: this should also check if it's valid for a URL
                output += chr(char)
                h += 1
                #// Check if the character is non-ASCII, but below initial n
                #// This never occurs for Punycode, so ignore in coverage
                #// @codeCoverageIgnoreStart
            elif char < n:
                raise php_new_class("Requests_Exception", lambda : Requests_Exception("Invalid character", "idna.character_outside_domain", char))
            else:
                extended[char] = True
            # end if
        # end for
        extended = php_array_keys(extended)
        sort(extended)
        b = h
        #// #       [copy them] followed by a delimiter if b > 0
        if php_strlen(output) > 0:
            output += "-"
        # end if
        #// #       {if the input contains a non-basic code point < n then fail}
        #// #       while h < length(input) do begin
        while True:
            
            if not (h < php_count(codepoints)):
                break
            # end if
            #// #           let m = the minimum code point >= n in the input
            m = php_array_shift(extended)
            #// printf('next code point to insert is %s' . PHP_EOL, dechex($m));
            #// #           let delta = delta + (m - n) * (h + 1), fail on overflow
            delta += m - n * h + 1
            #// #           let n = m
            n = m
            #// #           for each code point c in the input (in order) do begin
            num = 0
            while num < php_count(codepoints):
                
                c = codepoints[num]
                #// #               if c < n then increment delta, fail on overflow
                if c < n:
                    delta += 1
                    #// #               if c == n then begin
                elif c == n:
                    #// #                   let q = delta
                    q = delta
                    #// #                   for k = base to infinity in steps of base do begin
                    k = self.BOOTSTRAP_BASE
                    while True:
                        
                        #// #                       let t = tmin if k <= bias {+ tmin}, or
                        #// #                               tmax if k >= bias + tmax, or k - bias otherwise
                        if k <= bias + self.BOOTSTRAP_TMIN:
                            t = self.BOOTSTRAP_TMIN
                        elif k >= bias + self.BOOTSTRAP_TMAX:
                            t = self.BOOTSTRAP_TMAX
                        else:
                            t = k - bias
                        # end if
                        #// #                       if q < t then break
                        if q < t:
                            break
                        # end if
                        #// #                       output the code point for digit t + ((q - t) mod (base - t))
                        digit = t + q - t % self.BOOTSTRAP_BASE - t
                        output += self.digit_to_char(digit)
                        #// #                       let q = (q - t) div (base - t)
                        q = floor(q - t / self.BOOTSTRAP_BASE - t)
                        pass
                        k += self.BOOTSTRAP_BASE
                    # end while
                    #// #                   output the code point for digit q
                    output += self.digit_to_char(q)
                    #// #                   let bias = adapt(delta, h + 1, test h equals b?)
                    bias = self.adapt(delta, h + 1, h == b)
                    #// #                   let delta = 0
                    delta = 0
                    #// #                   increment h
                    h += 1
                    pass
                # end if
                pass
                num += 1
            # end while
            #// #           increment delta and n
            delta += 1
            n += 1
            pass
        # end while
        return output
    # end def punycode_encode
    #// 
    #// Convert a digit to its respective character
    #// 
    #// @see https://tools.ietf.org/html/rfc3492#section-5
    #// @throws Requests_Exception On invalid digit (`idna.invalid_digit`)
    #// 
    #// @param int $digit Digit in the range 0-35
    #// @return string Single character corresponding to digit
    #//
    def digit_to_char(self, digit=None):
        
        #// @codeCoverageIgnoreStart
        #// As far as I know, this never happens, but still good to be sure.
        if digit < 0 or digit > 35:
            raise php_new_class("Requests_Exception", lambda : Requests_Exception(php_sprintf("Invalid digit %d", digit), "idna.invalid_digit", digit))
        # end if
        #// @codeCoverageIgnoreEnd
        digits = "abcdefghijklmnopqrstuvwxyz0123456789"
        return php_substr(digits, digit, 1)
    # end def digit_to_char
    #// 
    #// Adapt the bias
    #// 
    #// @see https://tools.ietf.org/html/rfc3492#section-6.1
    #// @param int $delta
    #// @param int $numpoints
    #// @param bool $firsttime
    #// @return int New bias
    #//
    def adapt(self, delta=None, numpoints=None, firsttime=None):
        
        #// #   function adapt(delta,numpoints,firsttime):
        #// #       if firsttime then let delta = delta div damp
        if firsttime:
            delta = floor(delta / self.BOOTSTRAP_DAMP)
        else:
            delta = floor(delta / 2)
        # end if
        #// #       let delta = delta + (delta div numpoints)
        delta += floor(delta / numpoints)
        #// #       let k = 0
        k = 0
        #// #       while delta > ((base - tmin) * tmax) div 2 do begin
        max = floor(self.BOOTSTRAP_BASE - self.BOOTSTRAP_TMIN * self.BOOTSTRAP_TMAX / 2)
        while True:
            
            if not (delta > max):
                break
            # end if
            #// #           let delta = delta div (base - tmin)
            delta = floor(delta / self.BOOTSTRAP_BASE - self.BOOTSTRAP_TMIN)
            #// #           let k = k + base
            k += self.BOOTSTRAP_BASE
            pass
        # end while
        #// #       return k + (((base - tmin + 1) * delta) div (delta + skew))
        return k + floor(self.BOOTSTRAP_BASE - self.BOOTSTRAP_TMIN + 1 * delta / delta + self.BOOTSTRAP_SKEW)
    # end def adapt
# end class Requests_IDNAEncoder
