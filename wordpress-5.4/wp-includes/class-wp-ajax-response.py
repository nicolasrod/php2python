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
#// Send XML response back to Ajax request.
#// 
#// @package WordPress
#// @since 2.1.0
#//
class WP_Ajax_Response():
    #// 
    #// Store XML responses to send.
    #// 
    #// @since 2.1.0
    #// @var array
    #//
    responses = Array()
    #// 
    #// Constructor - Passes args to WP_Ajax_Response::add().
    #// 
    #// @since 2.1.0
    #// @see WP_Ajax_Response::add()
    #// 
    #// @param string|array $args Optional. Will be passed to add() method.
    #//
    def __init__(self, args_=""):
        
        
        if (not php_empty(lambda : args_)):
            self.add(args_)
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
    def add(self, args_=""):
        
        
        defaults_ = Array({"what": "object", "action": False, "id": "0", "old_id": False, "position": 1, "data": "", "supplemental": Array()})
        parsed_args_ = wp_parse_args(args_, defaults_)
        position_ = php_preg_replace("/[^a-z0-9:_-]/i", "", parsed_args_["position"])
        id_ = parsed_args_["id"]
        what_ = parsed_args_["what"]
        action_ = parsed_args_["action"]
        old_id_ = parsed_args_["old_id"]
        data_ = parsed_args_["data"]
        if is_wp_error(id_):
            data_ = id_
            id_ = 0
        # end if
        response_ = ""
        if is_wp_error(data_):
            for code_ in data_.get_error_codes():
                response_ += str("<wp_error code='") + str(code_) + str("'><![CDATA[") + data_.get_error_message(code_) + "]]></wp_error>"
                error_data_ = data_.get_error_data(code_)
                if (not error_data_):
                    continue
                # end if
                class_ = ""
                if php_is_object(error_data_):
                    class_ = " class=\"" + get_class(error_data_) + "\""
                    error_data_ = get_object_vars(error_data_)
                # end if
                response_ += str("<wp_error_data code='") + str(code_) + str("'") + str(class_) + str(">")
                if is_scalar(error_data_):
                    response_ += str("<![CDATA[") + str(error_data_) + str("]]>")
                elif php_is_array(error_data_):
                    for k_,v_ in error_data_:
                        response_ += str("<") + str(k_) + str("><![CDATA[") + str(v_) + str("]]></") + str(k_) + str(">")
                    # end for
                # end if
                response_ += "</wp_error_data>"
            # end for
        else:
            response_ = str("<response_data><![CDATA[") + str(data_) + str("]]></response_data>")
        # end if
        s_ = ""
        if php_is_array(parsed_args_["supplemental"]):
            for k_,v_ in parsed_args_["supplemental"]:
                s_ += str("<") + str(k_) + str("><![CDATA[") + str(v_) + str("]]></") + str(k_) + str(">")
            # end for
            s_ = str("<supplemental>") + str(s_) + str("</supplemental>")
        # end if
        if False == action_:
            action_ = PHP_POST["action"]
        # end if
        x_ = ""
        x_ += str("<response action='") + str(action_) + str("_") + str(id_) + str("'>")
        #// The action attribute in the xml output is formatted like a nonce action.
        x_ += str("<") + str(what_) + str(" id='") + str(id_) + str("' ") + "" if False == old_id_ else str("old_id='") + str(old_id_) + str("' ") + str("position='") + str(position_) + str("'>")
        x_ += response_
        x_ += s_
        x_ += str("</") + str(what_) + str(">")
        x_ += "</response>"
        self.responses[-1] = x_
        return x_
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
        for response_ in self.responses:
            php_print(response_)
        # end for
        php_print("</wp_ajax>")
        if wp_doing_ajax():
            wp_die()
        else:
            php_exit(0)
        # end if
    # end def send
# end class WP_Ajax_Response
