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
#// Send XML response back to Ajax request.
#// 
#// @package WordPress
#// @since 2.1.0
#//
class WP_Ajax_Response():
    responses = Array()
    #// 
    #// Constructor - Passes args to WP_Ajax_Response::add().
    #// 
    #// @since 2.1.0
    #// @see WP_Ajax_Response::add()
    #// 
    #// @param string|array $args Optional. Will be passed to add() method.
    #//
    def __init__(self, args=""):
        
        if (not php_empty(lambda : args)):
            self.add(args)
        # end if
    # end def __init__
    #// 
    #// Appends data to an XML response based on given arguments.
    #// 
    #// With `$args` defaults, extra data output would be:
    #// 
    #// <response action='{$action}_$id'>
    #// <$what id='$id' position='$position'>
    #// <response_data><![CDATA[$data]]></response_data>
    #// </$what>
    #// </response>
    #// 
    #// @since 2.1.0
    #// 
    #// @param string|array $args {
    #// Optional. An array or string of XML response arguments.
    #// 
    #// @type string          $what         XML-RPC response type. Used as a child element of `<response>`.
    #// Default 'object' (`<object>`).
    #// @type string|false    $action       Value to use for the `action` attribute in `<response>`. Will be
    #// appended with `_$id` on output. If false, `$action` will default to
    #// the value of `$_POST['action']`. Default false.
    #// @type int|WP_Error    $id           The response ID, used as the response type `id` attribute. Also
    #// accepts a `WP_Error` object if the ID does not exist. Default 0.
    #// @type int|false       $old_id       The previous response ID. Used as the value for the response type
    #// `old_id` attribute. False hides the attribute. Default false.
    #// @type string          $position     Value of the response type `position` attribute. Accepts 1 (bottom),
    #// -1 (top), html ID (after), or -html ID (before). Default 1 (bottom).
    #// @type string|WP_Error $data         The response content/message. Also accepts a WP_Error object if the
    #// ID does not exist. Default empty.
    #// @type array           $supplemental An array of extra strings that will be output within a `<supplemental>`
    #// element as CDATA. Default empty array.
    #// }
    #// @return string XML response.
    #//
    def add(self, args=""):
        
        defaults = Array({"what": "object", "action": False, "id": "0", "old_id": False, "position": 1, "data": "", "supplemental": Array()})
        parsed_args = wp_parse_args(args, defaults)
        position = php_preg_replace("/[^a-z0-9:_-]/i", "", parsed_args["position"])
        id = parsed_args["id"]
        what = parsed_args["what"]
        action = parsed_args["action"]
        old_id = parsed_args["old_id"]
        data = parsed_args["data"]
        if is_wp_error(id):
            data = id
            id = 0
        # end if
        response = ""
        if is_wp_error(data):
            for code in data.get_error_codes():
                response += str("<wp_error code='") + str(code) + str("'><![CDATA[") + data.get_error_message(code) + "]]></wp_error>"
                error_data = data.get_error_data(code)
                if (not error_data):
                    continue
                # end if
                class_ = ""
                if php_is_object(error_data):
                    class_ = " class=\"" + get_class(error_data) + "\""
                    error_data = get_object_vars(error_data)
                # end if
                response += str("<wp_error_data code='") + str(code) + str("'") + str(class_) + str(">")
                if is_scalar(error_data):
                    response += str("<![CDATA[") + str(error_data) + str("]]>")
                elif php_is_array(error_data):
                    for k,v in error_data:
                        response += str("<") + str(k) + str("><![CDATA[") + str(v) + str("]]></") + str(k) + str(">")
                    # end for
                # end if
                response += "</wp_error_data>"
            # end for
        else:
            response = str("<response_data><![CDATA[") + str(data) + str("]]></response_data>")
        # end if
        s = ""
        if php_is_array(parsed_args["supplemental"]):
            for k,v in parsed_args["supplemental"]:
                s += str("<") + str(k) + str("><![CDATA[") + str(v) + str("]]></") + str(k) + str(">")
            # end for
            s = str("<supplemental>") + str(s) + str("</supplemental>")
        # end if
        if False == action:
            action = PHP_POST["action"]
        # end if
        x = ""
        x += str("<response action='") + str(action) + str("_") + str(id) + str("'>")
        #// The action attribute in the xml output is formatted like a nonce action.
        x += str("<") + str(what) + str(" id='") + str(id) + str("' ") + "" if False == old_id else str("old_id='") + str(old_id) + str("' ") + str("position='") + str(position) + str("'>")
        x += response
        x += s
        x += str("</") + str(what) + str(">")
        x += "</response>"
        self.responses[-1] = x
        return x
    # end def add
    #// 
    #// Display XML formatted responses.
    #// 
    #// Sets the content type header to text/xml.
    #// 
    #// @since 2.1.0
    #//
    def send(self):
        
        php_header("Content-Type: text/xml; charset=" + get_option("blog_charset"))
        php_print("<?xml version='1.0' encoding='" + get_option("blog_charset") + "' standalone='yes'?><wp_ajax>")
        for response in self.responses:
            php_print(response)
        # end for
        php_print("</wp_ajax>")
        if wp_doing_ajax():
            wp_die()
        else:
            php_exit(0)
        # end if
    # end def send
# end class WP_Ajax_Response
