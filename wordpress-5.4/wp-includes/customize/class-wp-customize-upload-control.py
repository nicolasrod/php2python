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
    #// Unused.
    context = Array()
    #// Unused.
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
        value_ = self.value()
        if value_:
            #// Get the attachment model for the existing file.
            attachment_id_ = attachment_url_to_postid(value_)
            if attachment_id_:
                self.json["attachment"] = wp_prepare_attachment_for_js(attachment_id_)
            # end if
        # end if
    # end def to_json
# end class WP_Customize_Upload_Control
