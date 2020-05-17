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
#// WordPress implementation for PHP functions either missing from older PHP versions or not included by default.
#// 
#// @package PHP
#// @access private
#// 
#// If gettext isn't available.
if (not php_function_exists("_")):
    def _(string_=None, *_args_):
        
        
        return string_
    # end def _
# end if
#// 
#// Returns whether PCRE/u (PCRE_UTF8 modifier) is available for use.
#// 
#// @ignore
#// @since 4.2.2
#// @access private
#// 
#// @staticvar string $utf8_pcre
#// 
#// @param bool $set - Used for testing only
#// null   : default - get PCRE/u capability
#// false  : Used for testing - return false for future calls to this function
#// 'reset': Used for testing - restore default behavior of this function
#//
def _wp_can_use_pcre_u(set_=None, *_args_):
    
    
    utf8_pcre_ = "reset"
    if None != set_:
        utf8_pcre_ = set_
    # end if
    if "reset" == utf8_pcre_:
        #// phpcs:ignore WordPress.PHP.NoSilencedErrors.Discouraged -- intentional error generated to detect PCRE/u support.
        utf8_pcre_ = php_no_error(lambda: php_preg_match("/^./u", "a"))
    # end if
    return utf8_pcre_
# end def _wp_can_use_pcre_u
if (not php_function_exists("mb_substr")):
    #// 
    #// Compat function to mimic mb_substr().
    #// 
    #// @ignore
    #// @since 3.2.0
    #// 
    #// @see _mb_substr()
    #// 
    #// @param string      $str      The string to extract the substring from.
    #// @param int         $start    Position to being extraction from in `$str`.
    #// @param int|null    $length   Optional. Maximum number of characters to extract from `$str`.
    #// Default null.
    #// @param string|null $encoding Optional. Character encoding to use. Default null.
    #// @return string Extracted substring.
    #//
    def mb_substr(str_=None, start_=None, length_=None, encoding_=None, *_args_):
        
        
        return _mb_substr(str_, start_, length_, encoding_)
    # end def mb_substr
# end if
#// 
#// Internal compat function to mimic mb_substr().
#// 
#// Only understands UTF-8 and 8bit.  All other character sets will be treated as 8bit.
#// For $encoding === UTF-8, the $str input is expected to be a valid UTF-8 byte sequence.
#// The behavior of this function for invalid inputs is undefined.
#// 
#// @ignore
#// @since 3.2.0
#// 
#// @param string      $str      The string to extract the substring from.
#// @param int         $start    Position to being extraction from in `$str`.
#// @param int|null    $length   Optional. Maximum number of characters to extract from `$str`.
#// Default null.
#// @param string|null $encoding Optional. Character encoding to use. Default null.
#// @return string Extracted substring.
#//
def _mb_substr(str_=None, start_=None, length_=None, encoding_=None, *_args_):
    
    
    if None == encoding_:
        encoding_ = get_option("blog_charset")
    # end if
    #// 
    #// The solution below works only for UTF-8, so in case of a different
    #// charset just use built-in substr().
    #//
    if (not php_in_array(encoding_, Array("utf8", "utf-8", "UTF8", "UTF-8"))):
        return php_substr(str_, start_) if is_null(length_) else php_substr(str_, start_, length_)
    # end if
    if _wp_can_use_pcre_u():
        #// Use the regex unicode support to separate the UTF-8 characters into an array.
        preg_match_all("/./us", str_, match_)
        chars_ = php_array_slice(match_[0], start_) if is_null(length_) else php_array_slice(match_[0], start_, length_)
        return php_implode("", chars_)
    # end if
    regex_ = """/(
    [\\x00-\\x7F]                  # single-byte sequences   0xxxxxxx
    | [\\xC2-\\xDF][\\x80-\\xBF]       # double-byte sequences   110xxxxx 10xxxxxx
    | \\xE0[\\xA0-\\xBF][\\x80-\\xBF]   # triple-byte sequences   1110xxxx 10xxxxxx * 2
    | [\\xE1-\\xEC][\\x80-\\xBF]{2}
    | \\xED[\\x80-\\x9F][\\x80-\\xBF]
    | [\\xEE-\\xEF][\\x80-\\xBF]{2}
    | \\xF0[\\x90-\\xBF][\\x80-\\xBF]{2} # four-byte sequences   11110xxx 10xxxxxx * 3
    | [\\xF1-\\xF3][\\x80-\\xBF]{3}
    | \\xF4[\\x80-\\x8F][\\x80-\\xBF]{2}
    )/x"""
    #// Start with 1 element instead of 0 since the first thing we do is pop.
    chars_ = Array("")
    while True:
        #// We had some string left over from the last round, but we counted it in that last round.
        php_array_pop(chars_)
        #// 
        #// Split by UTF-8 character, limit to 1000 characters (last array element will contain
        #// the rest of the string).
        #//
        pieces_ = php_preg_split(regex_, str_, 1000, PREG_SPLIT_DELIM_CAPTURE | PREG_SPLIT_NO_EMPTY)
        chars_ = php_array_merge(chars_, pieces_)
        pass
        str_ = php_array_pop(pieces_)
        if php_count(pieces_) > 1 and str_:
            break
        # end if
    # end while
    return join("", php_array_slice(chars_, start_, length_))
# end def _mb_substr
if (not php_function_exists("mb_strlen")):
    #// 
    #// Compat function to mimic mb_strlen().
    #// 
    #// @ignore
    #// @since 4.2.0
    #// 
    #// @see _mb_strlen()
    #// 
    #// @param string      $str      The string to retrieve the character length from.
    #// @param string|null $encoding Optional. Character encoding to use. Default null.
    #// @return int String length of `$str`.
    #//
    def mb_strlen(str_=None, encoding_=None, *_args_):
        
        
        return _mb_strlen(str_, encoding_)
    # end def mb_strlen
# end if
#// 
#// Internal compat function to mimic mb_strlen().
#// 
#// Only understands UTF-8 and 8bit.  All other character sets will be treated as 8bit.
#// For $encoding === UTF-8, the `$str` input is expected to be a valid UTF-8 byte
#// sequence. The behavior of this function for invalid inputs is undefined.
#// 
#// @ignore
#// @since 4.2.0
#// 
#// @param string      $str      The string to retrieve the character length from.
#// @param string|null $encoding Optional. Character encoding to use. Default null.
#// @return int String length of `$str`.
#//
def _mb_strlen(str_=None, encoding_=None, *_args_):
    
    
    if None == encoding_:
        encoding_ = get_option("blog_charset")
    # end if
    #// 
    #// The solution below works only for UTF-8, so in case of a different charset
    #// just use built-in strlen().
    #//
    if (not php_in_array(encoding_, Array("utf8", "utf-8", "UTF8", "UTF-8"))):
        return php_strlen(str_)
    # end if
    if _wp_can_use_pcre_u():
        #// Use the regex unicode support to separate the UTF-8 characters into an array.
        preg_match_all("/./us", str_, match_)
        return php_count(match_[0])
    # end if
    regex_ = """/(?:
    [\\x00-\\x7F]                  # single-byte sequences   0xxxxxxx
    | [\\xC2-\\xDF][\\x80-\\xBF]       # double-byte sequences   110xxxxx 10xxxxxx
    | \\xE0[\\xA0-\\xBF][\\x80-\\xBF]   # triple-byte sequences   1110xxxx 10xxxxxx * 2
    | [\\xE1-\\xEC][\\x80-\\xBF]{2}
    | \\xED[\\x80-\\x9F][\\x80-\\xBF]
    | [\\xEE-\\xEF][\\x80-\\xBF]{2}
    | \\xF0[\\x90-\\xBF][\\x80-\\xBF]{2} # four-byte sequences   11110xxx 10xxxxxx * 3
    | [\\xF1-\\xF3][\\x80-\\xBF]{3}
    | \\xF4[\\x80-\\x8F][\\x80-\\xBF]{2}
    )/x"""
    #// Start at 1 instead of 0 since the first thing we do is decrement.
    count_ = 1
    while True:
        #// We had some string left over from the last round, but we counted it in that last round.
        count_ -= 1
        #// 
        #// Split by UTF-8 character, limit to 1000 characters (last array element will contain
        #// the rest of the string).
        #//
        pieces_ = php_preg_split(regex_, str_, 1000)
        #// Increment.
        count_ += php_count(pieces_)
        pass
        str_ = php_array_pop(pieces_)
        if str_:
            break
        # end if
    # end while
    #// Fencepost: preg_split() always returns one extra item in the array.
    count_ -= 1
    return count_
# end def _mb_strlen
if (not php_function_exists("hash_hmac")):
    #// 
    #// Compat function to mimic hash_hmac().
    #// 
    #// The Hash extension is bundled with PHP by default since PHP 5.1.2.
    #// However, the extension may be explicitly disabled on select servers.
    #// As of PHP 7.4.0, the Hash extension is a core PHP extension and can no
    #// longer be disabled.
    #// I.e. when PHP 7.4.0 becomes the minimum requirement, this polyfill
    #// and the associated `_hash_hmac()` function can be safely removed.
    #// 
    #// @ignore
    #// @since 3.2.0
    #// 
    #// @see _hash_hmac()
    #// 
    #// @param string $algo       Hash algorithm. Accepts 'md5' or 'sha1'.
    #// @param string $data       Data to be hashed.
    #// @param string $key        Secret key to use for generating the hash.
    #// @param bool   $raw_output Optional. Whether to output raw binary data (true),
    #// or lowercase hexits (false). Default false.
    #// @return string|false The hash in output determined by `$raw_output`. False if `$algo`
    #// is unknown or invalid.
    #//
    def hash_hmac(algo_=None, data_=None, key_=None, raw_output_=None, *_args_):
        if raw_output_ is None:
            raw_output_ = False
        # end if
        
        return _hash_hmac(algo_, data_, key_, raw_output_)
    # end def hash_hmac
# end if
#// 
#// Internal compat function to mimic hash_hmac().
#// 
#// @ignore
#// @since 3.2.0
#// 
#// @param string $algo       Hash algorithm. Accepts 'md5' or 'sha1'.
#// @param string $data       Data to be hashed.
#// @param string $key        Secret key to use for generating the hash.
#// @param bool   $raw_output Optional. Whether to output raw binary data (true),
#// or lowercase hexits (false). Default false.
#// @return string|false The hash in output determined by `$raw_output`. False if `$algo`
#// is unknown or invalid.
#//
def _hash_hmac(algo_=None, data_=None, key_=None, raw_output_=None, *_args_):
    if raw_output_ is None:
        raw_output_ = False
    # end if
    
    packs_ = Array({"md5": "H32", "sha1": "H40"})
    if (not (php_isset(lambda : packs_[algo_]))):
        return False
    # end if
    pack_ = packs_[algo_]
    if php_strlen(key_) > 64:
        key_ = pack(pack_, algo_(key_))
    # end if
    key_ = php_str_pad(key_, 64, chr(0))
    ipad_ = php_substr(key_, 0, 64) ^ php_str_repeat(chr(54), 64)
    opad_ = php_substr(key_, 0, 64) ^ php_str_repeat(chr(92), 64)
    hmac_ = algo_(opad_ + pack(pack_, algo_(ipad_ + data_)))
    if raw_output_:
        return pack(pack_, hmac_)
    # end if
    return hmac_
# end def _hash_hmac
if (not php_function_exists("hash_equals")):
    #// 
    #// Timing attack safe string comparison
    #// 
    #// Compares two strings using the same time whether they're equal or not.
    #// 
    #// Note: It can leak the length of a string when arguments of differing length are supplied.
    #// 
    #// This function was added in PHP 5.6.
    #// However, the Hash extension may be explicitly disabled on select servers.
    #// As of PHP 7.4.0, the Hash extension is a core PHP extension and can no
    #// longer be disabled.
    #// I.e. when PHP 7.4.0 becomes the minimum requirement, this polyfill
    #// can be safely removed.
    #// 
    #// @since 3.9.2
    #// 
    #// @param string $a Expected string.
    #// @param string $b Actual, user supplied, string.
    #// @return bool Whether strings are equal.
    #//
    def hash_equals(a_=None, b_=None, *_args_):
        
        
        a_length_ = php_strlen(a_)
        if php_strlen(b_) != a_length_:
            return False
        # end if
        result_ = 0
        #// Do not attempt to "optimize" this.
        i_ = 0
        while i_ < a_length_:
            
            result_ |= php_ord(a_[i_]) ^ php_ord(b_[i_])
            i_ += 1
        # end while
        return 0 == result_
    # end def hash_equals
# end if
#// random_int() was introduced in PHP 7.0.
if (not php_function_exists("random_int")):
    php_include_file(ABSPATH + WPINC + "/random_compat/random.php", once=False)
# end if
#// sodium_crypto_box() was introduced in PHP 7.2.
if (not php_function_exists("sodium_crypto_box")):
    php_include_file(ABSPATH + WPINC + "/sodium_compat/autoload.php", once=False)
# end if
if (not php_function_exists("is_countable")):
    #// 
    #// Polyfill for is_countable() function added in PHP 7.3.
    #// 
    #// Verify that the content of a variable is an array or an object
    #// implementing the Countable interface.
    #// 
    #// @since 4.9.6
    #// 
    #// @param mixed $var The value to check.
    #// 
    #// @return bool True if `$var` is countable, false otherwise.
    #//
    def is_countable(var_=None, *_args_):
        
        
        return php_is_array(var_) or type(var_).__name__ == "Countable" or type(var_).__name__ == "SimpleXMLElement" or type(var_).__name__ == "ResourceBundle"
    # end def is_countable
# end if
if (not php_function_exists("is_iterable")):
    #// 
    #// Polyfill for is_iterable() function added in PHP 7.1.
    #// 
    #// Verify that the content of a variable is an array or an object
    #// implementing the Traversable interface.
    #// 
    #// @since 4.9.6
    #// 
    #// @param mixed $var The value to check.
    #// 
    #// @return bool True if `$var` is iterable, false otherwise.
    #//
    def is_iterable(var_=None, *_args_):
        
        
        return php_is_array(var_) or type(var_).__name__ == "Traversable"
    # end def is_iterable
# end if
