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
#// Feed API: WP_SimplePie_Sanitize_KSES class
#// 
#// @package WordPress
#// @subpackage Feed
#// @since 4.7.0
#// 
#// 
#// Core class used to implement SimpliePie feed sanitization.
#// 
#// Extends the SimplePie_Sanitize class to use KSES, because
#// we cannot universally count on DOMDocument being available.
#// 
#// @since 3.5.0
#// 
#// @see SimplePie_Sanitize
#//
class WP_SimplePie_Sanitize_KSES(SimplePie_Sanitize):
    #// 
    #// WordPress SimplePie sanitization using KSES.
    #// 
    #// Sanitizes the incoming data, to ensure that it matches the type of data expected, using KSES.
    #// 
    #// @since 3.5.0
    #// 
    #// @param mixed   $data The data that needs to be sanitized.
    #// @param integer $type The type of data that it's supposed to be.
    #// @param string  $base Optional. The `xml:base` value to use when converting relative
    #// URLs to absolute ones. Default empty.
    #// @return mixed Sanitized data.
    #//
    def sanitize(self, data_=None, type_=None, base_=""):
        
        
        data_ = php_trim(data_)
        if type_ & SIMPLEPIE_CONSTRUCT_MAYBE_HTML:
            if php_preg_match("/(&(#(x[0-9a-fA-F]+|[0-9]+)|[a-zA-Z0-9]+)|<\\/[A-Za-z][^\\x09\\x0A\\x0B\\x0C\\x0D\\x20\\x2F\\x3E]*" + SIMPLEPIE_PCRE_HTML_ATTRIBUTE + ">)/", data_):
                type_ |= SIMPLEPIE_CONSTRUCT_HTML
            else:
                type_ |= SIMPLEPIE_CONSTRUCT_TEXT
            # end if
        # end if
        if type_ & SIMPLEPIE_CONSTRUCT_BASE64:
            data_ = php_base64_decode(data_)
        # end if
        if type_ & SIMPLEPIE_CONSTRUCT_HTML | SIMPLEPIE_CONSTRUCT_XHTML:
            data_ = wp_kses_post(data_)
            if "UTF-8" != self.output_encoding:
                data_ = self.registry.call("Misc", "change_encoding", Array(data_, "UTF-8", self.output_encoding))
            # end if
            return data_
        else:
            return super().sanitize(data_, type_, base_)
        # end if
    # end def sanitize
# end class WP_SimplePie_Sanitize_KSES
