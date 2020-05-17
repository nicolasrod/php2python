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
    def encode(self, string_=None):
        
        
        parts_ = php_explode(".", string_)
        for part_ in parts_:
            part_ = self.to_ascii(part_)
        # end for
        return php_implode(".", parts_)
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
    def to_ascii(self, string_=None):
        
        
        #// Step 1: Check if the string is already ASCII
        if self.is_ascii(string_):
            #// Skip to step 7
            if php_strlen(string_) < 64:
                return string_
            # end if
            raise php_new_class("Requests_Exception", lambda : Requests_Exception("Provided string is too long", "idna.provided_too_long", string_))
        # end if
        #// Step 2: nameprep
        string_ = self.nameprep(string_)
        #// Step 3: UseSTD3ASCIIRules is false, continue
        #// Step 4: Check if it's ASCII now
        if self.is_ascii(string_):
            #// Skip to step 7
            if php_strlen(string_) < 64:
                return string_
            # end if
            raise php_new_class("Requests_Exception", lambda : Requests_Exception("Prepared string is too long", "idna.prepared_too_long", string_))
        # end if
        #// Step 5: Check ACE prefix
        if php_strpos(string_, self.ACE_PREFIX) == 0:
            raise php_new_class("Requests_Exception", lambda : Requests_Exception("Provided string begins with ACE prefix", "idna.provided_is_prefixed", string_))
        # end if
        #// Step 6: Encode with Punycode
        string_ = self.punycode_encode(string_)
        #// Step 7: Prepend ACE prefix
        string_ = self.ACE_PREFIX + string_
        #// Step 8: Check size
        if php_strlen(string_) < 64:
            return string_
        # end if
        raise php_new_class("Requests_Exception", lambda : Requests_Exception("Encoded string is too long", "idna.encoded_too_long", string_))
    # end def to_ascii
    #// 
    #// Check whether a given string contains only ASCII characters
    #// 
    #// @internal (Testing found regex was the fastest implementation)
    #// 
    #// @param string $string
    #// @return bool Is the string ASCII-only?
    #//
    def is_ascii(self, string_=None):
        
        
        return php_preg_match("/(?:[^\\x00-\\x7F])/", string_) != 1
    # end def is_ascii
    #// 
    #// Prepare a string for use as an IDNA name
    #// 
    #// @todo Implement this based on RFC 3491 and the newer 5891
    #// @param string $string
    #// @return string Prepared string
    #//
    def nameprep(self, string_=None):
        
        
        return string_
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
    def utf8_to_codepoints(self, input_=None):
        
        
        codepoints_ = Array()
        #// Get number of bytes
        strlen_ = php_strlen(input_)
        position_ = 0
        while position_ < strlen_:
            
            value_ = php_ord(input_[position_])
            #// One byte sequence:
            if (1 << (value_).bit_length()) - 1 - value_ & 128 == 128:
                character_ = value_
                length_ = 1
                remaining_ = 0
                #// Two byte sequence:
            elif value_ & 224 == 192:
                character_ = value_ & 31 << 6
                length_ = 2
                remaining_ = 1
                #// Three byte sequence:
            elif value_ & 240 == 224:
                character_ = value_ & 15 << 12
                length_ = 3
                remaining_ = 2
                #// Four byte sequence:
            elif value_ & 248 == 240:
                character_ = value_ & 7 << 18
                length_ = 4
                remaining_ = 3
            else:
                raise php_new_class("Requests_Exception", lambda : Requests_Exception("Invalid Unicode codepoint", "idna.invalidcodepoint", value_))
            # end if
            if remaining_ > 0:
                if position_ + length_ > strlen_:
                    raise php_new_class("Requests_Exception", lambda : Requests_Exception("Invalid Unicode codepoint", "idna.invalidcodepoint", character_))
                # end if
                position_ += 1
                while remaining_ > 0:
                    
                    value_ = php_ord(input_[position_])
                    #// If it is invalid, count the sequence as invalid and reprocess the current byte:
                    if value_ & 192 != 128:
                        raise php_new_class("Requests_Exception", lambda : Requests_Exception("Invalid Unicode codepoint", "idna.invalidcodepoint", character_))
                    # end if
                    remaining_ -= 1
                    character_ |= value_ & 63 << remaining_ * 6
                    position_ += 1
                # end while
                position_ -= 1
            # end if
            if length_ > 1 and character_ <= 127 or length_ > 2 and character_ <= 2047 or length_ > 3 and character_ <= 65535 or character_ & 65534 == 65534 or character_ >= 64976 and character_ <= 65007 or character_ > 55295 and character_ < 63744 or character_ < 32 or character_ > 126 and character_ < 160 or character_ > 983037:
                raise php_new_class("Requests_Exception", lambda : Requests_Exception("Invalid Unicode codepoint", "idna.invalidcodepoint", character_))
            # end if
            codepoints_[-1] = character_
            position_ += 1
        # end while
        return codepoints_
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
    def punycode_encode(self, input_=None):
        
        
        output_ = ""
        #// #       let n = initial_n
        n_ = self.BOOTSTRAP_INITIAL_N
        #// #       let delta = 0
        delta_ = 0
        #// #       let bias = initial_bias
        bias_ = self.BOOTSTRAP_INITIAL_BIAS
        #// #       let h = b = the number of basic code points in the input
        h_ = b_ = 0
        #// see loop
        #// #       copy them to the output in order
        codepoints_ = self.utf8_to_codepoints(input_)
        extended_ = Array()
        for char_ in codepoints_:
            if char_ < 128:
                #// Character is valid ASCII
                #// TODO: this should also check if it's valid for a URL
                output_ += chr(char_)
                h_ += 1
                #// Check if the character is non-ASCII, but below initial n
                #// This never occurs for Punycode, so ignore in coverage
                #// @codeCoverageIgnoreStart
            elif char_ < n_:
                raise php_new_class("Requests_Exception", lambda : Requests_Exception("Invalid character", "idna.character_outside_domain", char_))
            else:
                extended_[char_] = True
            # end if
        # end for
        extended_ = php_array_keys(extended_)
        sort(extended_)
        b_ = h_
        #// #       [copy them] followed by a delimiter if b > 0
        if php_strlen(output_) > 0:
            output_ += "-"
        # end if
        #// #       {if the input contains a non-basic code point < n then fail}
        #// #       while h < length(input) do begin
        while True:
            
            if not (h_ < php_count(codepoints_)):
                break
            # end if
            #// #           let m = the minimum code point >= n in the input
            m_ = php_array_shift(extended_)
            #// printf('next code point to insert is %s' . PHP_EOL, dechex($m));
            #// #           let delta = delta + (m - n) * (h + 1), fail on overflow
            delta_ += m_ - n_ * h_ + 1
            #// #           let n = m
            n_ = m_
            #// #           for each code point c in the input (in order) do begin
            num_ = 0
            while num_ < php_count(codepoints_):
                
                c_ = codepoints_[num_]
                #// #               if c < n then increment delta, fail on overflow
                if c_ < n_:
                    delta_ += 1
                    #// #               if c == n then begin
                elif c_ == n_:
                    #// #                   let q = delta
                    q_ = delta_
                    #// #                   for k = base to infinity in steps of base do begin
                    k_ = self.BOOTSTRAP_BASE
                    while True:
                        
                        #// #                       let t = tmin if k <= bias {+ tmin}, or
                        #// #                               tmax if k >= bias + tmax, or k - bias otherwise
                        if k_ <= bias_ + self.BOOTSTRAP_TMIN:
                            t_ = self.BOOTSTRAP_TMIN
                        elif k_ >= bias_ + self.BOOTSTRAP_TMAX:
                            t_ = self.BOOTSTRAP_TMAX
                        else:
                            t_ = k_ - bias_
                        # end if
                        #// #                       if q < t then break
                        if q_ < t_:
                            break
                        # end if
                        #// #                       output the code point for digit t + ((q - t) mod (base - t))
                        digit_ = t_ + q_ - t_ % self.BOOTSTRAP_BASE - t_
                        output_ += self.digit_to_char(digit_)
                        #// #                       let q = (q - t) div (base - t)
                        q_ = floor(q_ - t_ / self.BOOTSTRAP_BASE - t_)
                        pass
                        k_ += self.BOOTSTRAP_BASE
                    # end while
                    #// #                   output the code point for digit q
                    output_ += self.digit_to_char(q_)
                    #// #                   let bias = adapt(delta, h + 1, test h equals b?)
                    bias_ = self.adapt(delta_, h_ + 1, h_ == b_)
                    #// #                   let delta = 0
                    delta_ = 0
                    #// #                   increment h
                    h_ += 1
                    pass
                # end if
                pass
                num_ += 1
            # end while
            #// #           increment delta and n
            delta_ += 1
            n_ += 1
            pass
        # end while
        return output_
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
    def digit_to_char(self, digit_=None):
        
        
        #// @codeCoverageIgnoreStart
        #// As far as I know, this never happens, but still good to be sure.
        if digit_ < 0 or digit_ > 35:
            raise php_new_class("Requests_Exception", lambda : Requests_Exception(php_sprintf("Invalid digit %d", digit_), "idna.invalid_digit", digit_))
        # end if
        #// @codeCoverageIgnoreEnd
        digits_ = "abcdefghijklmnopqrstuvwxyz0123456789"
        return php_substr(digits_, digit_, 1)
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
    def adapt(self, delta_=None, numpoints_=None, firsttime_=None):
        
        
        #// #   function adapt(delta,numpoints,firsttime):
        #// #       if firsttime then let delta = delta div damp
        if firsttime_:
            delta_ = floor(delta_ / self.BOOTSTRAP_DAMP)
        else:
            delta_ = floor(delta_ / 2)
        # end if
        #// #       let delta = delta + (delta div numpoints)
        delta_ += floor(delta_ / numpoints_)
        #// #       let k = 0
        k_ = 0
        #// #       while delta > ((base - tmin) * tmax) div 2 do begin
        max_ = floor(self.BOOTSTRAP_BASE - self.BOOTSTRAP_TMIN * self.BOOTSTRAP_TMAX / 2)
        while True:
            
            if not (delta_ > max_):
                break
            # end if
            #// #           let delta = delta div (base - tmin)
            delta_ = floor(delta_ / self.BOOTSTRAP_BASE - self.BOOTSTRAP_TMIN)
            #// #           let k = k + base
            k_ += self.BOOTSTRAP_BASE
            pass
        # end while
        #// #       return k + (((base - tmin + 1) * delta) div (delta + skew))
        return k_ + floor(self.BOOTSTRAP_BASE - self.BOOTSTRAP_TMIN + 1 * delta_ / delta_ + self.BOOTSTRAP_SKEW)
    # end def adapt
# end class Requests_IDNAEncoder
