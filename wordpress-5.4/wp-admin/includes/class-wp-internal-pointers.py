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
#// Administration API: WP_Internal_Pointers class
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 4.4.0
#// 
#// 
#// Core class used to implement an internal admin pointers API.
#// 
#// @since 3.3.0
#//
class WP_Internal_Pointers():
    #// 
    #// Initializes the new feature pointers.
    #// 
    #// @since 3.3.0
    #// 
    #// All pointers can be disabled using the following:
    #// remove_action( 'admin_enqueue_scripts', array( 'WP_Internal_Pointers', 'enqueue_scripts' ) );
    #// 
    #// Individual pointers (e.g. wp390_widgets) can be disabled using the following:
    #// 
    #// function yourprefix_remove_pointers() {
    #// remove_action(
    #// 'admin_print_footer_scripts',
    #// array( 'WP_Internal_Pointers', 'pointer_wp390_widgets' )
    #// );
    #// }
    #// add_action( 'admin_enqueue_scripts', 'yourprefix_remove_pointers', 11 );
    #// 
    #// @param string $hook_suffix The current admin page.
    #//
    @classmethod
    def enqueue_scripts(self, hook_suffix=None):
        
        #// 
        #// Register feature pointers
        #// 
        #// Format:
        #// array(
        #// hook_suffix => pointer callback
        #// )
        #// 
        #// Example:
        #// array(
        #// 'themes.php' => 'wp390_widgets'
        #// )
        #//
        registered_pointers = Array()
        #// Check if screen related pointer is registered.
        if php_empty(lambda : registered_pointers[hook_suffix]):
            return
        # end if
        pointers = registered_pointers[hook_suffix]
        #// 
        #// Specify required capabilities for feature pointers
        #// 
        #// Format:
        #// array(
        #// pointer callback => Array of required capabilities
        #// )
        #// 
        #// Example:
        #// array(
        #// 'wp390_widgets' => array( 'edit_theme_options' )
        #// )
        #//
        caps_required = Array()
        #// Get dismissed pointers.
        dismissed = php_explode(",", php_str(get_user_meta(get_current_user_id(), "dismissed_wp_pointers", True)))
        got_pointers = False
        for pointer in php_array_diff(pointers, dismissed):
            if (php_isset(lambda : caps_required[pointer])):
                for cap in caps_required[pointer]:
                    if (not current_user_can(cap)):
                        continue
                    # end if
                # end for
            # end if
            #// Bind pointer print function.
            add_action("admin_print_footer_scripts", Array("WP_Internal_Pointers", "pointer_" + pointer))
            got_pointers = True
        # end for
        if (not got_pointers):
            return
        # end if
        #// Add pointers script and style to queue.
        wp_enqueue_style("wp-pointer")
        wp_enqueue_script("wp-pointer")
    # end def enqueue_scripts
    #// 
    #// Print the pointer JavaScript data.
    #// 
    #// @since 3.3.0
    #// 
    #// @param string $pointer_id The pointer ID.
    #// @param string $selector The HTML elements, on which the pointer should be attached.
    #// @param array  $args Arguments to be passed to the pointer JS (see wp-pointer.js).
    #//
    def print_js(self, pointer_id=None, selector=None, args=None):
        
        if php_empty(lambda : pointer_id) or php_empty(lambda : selector) or php_empty(lambda : args) or php_empty(lambda : args["content"]):
            return
        # end if
        php_print("     <script type=\"text/javascript\">\n     (function($){\n         var options = ")
        php_print(wp_json_encode(args))
        php_print(""", setup;
    if ( ! options )
        return;
        options = $.extend( options, {
        close: function() {
        $.post( ajaxurl, {
        pointer: '""")
        php_print(pointer_id)
        php_print("""',
        action: 'dismiss-wp-pointer'
        });
        }
        });
        setup = function() {
        $('""")
        php_print(selector)
        php_print("""').first().pointer( options ).pointer('open');
        };
    if ( options.position && options.position.defer_loading )
        $(window).bind( 'load.wp-pointers', setup );
    else
        $(document).ready( setup );
        })( jQuery );
        </script>
        """)
    # end def print_js
    @classmethod
    def pointer_wp330_toolbar(self):
        
        pass
    # end def pointer_wp330_toolbar
    @classmethod
    def pointer_wp330_media_uploader(self):
        
        pass
    # end def pointer_wp330_media_uploader
    @classmethod
    def pointer_wp330_saving_widgets(self):
        
        pass
    # end def pointer_wp330_saving_widgets
    @classmethod
    def pointer_wp340_customize_current_theme_link(self):
        
        pass
    # end def pointer_wp340_customize_current_theme_link
    @classmethod
    def pointer_wp340_choose_image_from_library(self):
        
        pass
    # end def pointer_wp340_choose_image_from_library
    @classmethod
    def pointer_wp350_media(self):
        
        pass
    # end def pointer_wp350_media
    @classmethod
    def pointer_wp360_revisions(self):
        
        pass
    # end def pointer_wp360_revisions
    @classmethod
    def pointer_wp360_locks(self):
        
        pass
    # end def pointer_wp360_locks
    @classmethod
    def pointer_wp390_widgets(self):
        
        pass
    # end def pointer_wp390_widgets
    @classmethod
    def pointer_wp410_dfw(self):
        
        pass
    # end def pointer_wp410_dfw
    @classmethod
    def pointer_wp496_privacy(self):
        
        pass
    # end def pointer_wp496_privacy
    #// 
    #// Prevents new users from seeing existing 'new feature' pointers.
    #// 
    #// @since 3.3.0
    #// 
    #// @param int $user_id User ID.
    #//
    @classmethod
    def dismiss_pointers_for_new_users(self, user_id=None):
        
        add_user_meta(user_id, "dismissed_wp_pointers", "")
    # end def dismiss_pointers_for_new_users
# end class WP_Internal_Pointers
