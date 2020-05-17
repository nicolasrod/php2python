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
#// Javascript Loader Class
#// 
#// Allow `async` and `defer` while enqueuing Javascript.
#// 
#// Based on a solution in WP Rig.
#// 
#// @package WordPress
#// @subpackage Twenty_Twenty
#// @since Twenty Twenty 1.0
#//
if (not php_class_exists("TwentyTwenty_Script_Loader")):
    #// 
    #// A class that provides a way to add `async` or `defer` attributes to scripts.
    #//
    class TwentyTwenty_Script_Loader():
        #// 
        #// Adds async/defer attributes to enqueued / registered scripts.
        #// 
        #// If #12009 lands in WordPress, this function can no-op since it would be handled in core.
        #// 
        #// @link https://core.trac.wordpress.org/ticket/12009
        #// 
        #// @param string $tag    The script tag.
        #// @param string $handle The script handle.
        #// @return string Script HTML string.
        #//
        def filter_script_loader_tag(self, tag_=None, handle_=None):
            
            
            for attr_ in Array("async", "defer"):
                if (not wp_scripts().get_data(handle_, attr_)):
                    continue
                # end if
                #// Prevent adding attribute when already added in #12009.
                if (not php_preg_match(str(":\\s") + str(attr_) + str("(=|>|\\s):"), tag_)):
                    tag_ = php_preg_replace(":(?=></script>):", str(" ") + str(attr_), tag_, 1)
                # end if
                break
            # end for
            return tag_
        # end def filter_script_loader_tag
    # end class TwentyTwenty_Script_Loader
# end if
