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
#// Customize API: WP_Customize_Upload_Control class
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 4.4.0
#// 
#// 
#// Customize Upload Control Class.
#// 
#// @since 3.4.0
#// 
#// @see WP_Customize_Media_Control
#//
class WP_Customize_Upload_Control(WP_Customize_Media_Control):
    type = "upload"
    mime_type = ""
    button_labels = Array()
    removed = ""
    context = Array()
    extensions = Array()
    #// Unused.
    #// 
    #// Refresh the parameters passed to the JavaScript via JSON.
    #// 
    #// @since 3.4.0
    #// 
    #// @uses WP_Customize_Media_Control::to_json()
    #//
    def to_json(self):
        
        super().to_json()
        value = self.value()
        if value:
            #// Get the attachment model for the existing file.
            attachment_id = attachment_url_to_postid(value)
            if attachment_id:
                self.json["attachment"] = wp_prepare_attachment_for_js(attachment_id)
            # end if
        # end if
    # end def to_json
# end class WP_Customize_Upload_Control
