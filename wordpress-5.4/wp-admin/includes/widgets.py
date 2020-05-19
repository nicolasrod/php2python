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
#// WordPress Widgets Administration API
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// 
#// Display list of the available widgets.
#// 
#// @since 2.5.0
#// 
#// @global array $wp_registered_widgets
#// @global array $wp_registered_widget_controls
#//
def wp_list_widgets(*_args_):
    
    
    global wp_registered_widgets_
    global wp_registered_widget_controls_
    php_check_if_defined("wp_registered_widgets_","wp_registered_widget_controls_")
    sort_ = wp_registered_widgets_
    usort(sort_, "_sort_name_callback")
    done_ = Array()
    for widget_ in sort_:
        if php_in_array(widget_["callback"], done_, True):
            continue
        # end if
        sidebar_ = is_active_widget(widget_["callback"], widget_["id"], False, False)
        done_[-1] = widget_["callback"]
        if (not (php_isset(lambda : widget_["params"][0]))):
            widget_["params"][0] = Array()
        # end if
        args_ = Array({"widget_id": widget_["id"], "widget_name": widget_["name"], "_display": "template"})
        if (php_isset(lambda : wp_registered_widget_controls_[widget_["id"]]["id_base"])) and (php_isset(lambda : widget_["params"][0]["number"])):
            id_base_ = wp_registered_widget_controls_[widget_["id"]]["id_base"]
            args_["_temp_id"] = str(id_base_) + str("-__i__")
            args_["_multi_num"] = next_widget_id_number(id_base_)
            args_["_add"] = "multi"
        else:
            args_["_add"] = "single"
            if sidebar_:
                args_["_hide"] = "1"
            # end if
        # end if
        control_args_ = Array({0: args_, 1: widget_["params"][0]})
        sidebar_args_ = wp_list_widget_controls_dynamic_sidebar(control_args_)
        wp_widget_control(sidebar_args_)
    # end for
# end def wp_list_widgets
#// 
#// Callback to sort array by a 'name' key.
#// 
#// @since 3.1.0
#// @access private
#// 
#// @return int
#//
def _sort_name_callback(a_=None, b_=None, *_args_):
    
    
    return strnatcasecmp(a_["name"], b_["name"])
# end def _sort_name_callback
#// 
#// Show the widgets and their settings for a sidebar.
#// Used in the admin widget config screen.
#// 
#// @since 2.5.0
#// 
#// @param string $sidebar      Sidebar ID.
#// @param string $sidebar_name Optional. Sidebar name. Default empty.
#//
def wp_list_widget_controls(sidebar_=None, sidebar_name_="", *_args_):
    
    
    add_filter("dynamic_sidebar_params", "wp_list_widget_controls_dynamic_sidebar")
    description_ = wp_sidebar_description(sidebar_)
    php_print("<div id=\"" + esc_attr(sidebar_) + "\" class=\"widgets-sortables\">")
    if sidebar_name_:
        add_to_ = php_sprintf(__("Add to: %s"), sidebar_name_)
        php_print("     <div class=\"sidebar-name\" data-add-to=\"")
        php_print(esc_attr(add_to_))
        php_print("\">\n            <button type=\"button\" class=\"handlediv hide-if-no-js\" aria-expanded=\"true\">\n             <span class=\"screen-reader-text\">")
        php_print(esc_html(sidebar_name_))
        php_print("""</span>
        <span class=\"toggle-indicator\" aria-hidden=\"true\"></span>
        </button>
        <h2>""")
        php_print(esc_html(sidebar_name_))
        php_print(" <span class=\"spinner\"></span></h2>\n      </div>\n        ")
    # end if
    if (not php_empty(lambda : description_)):
        php_print("     <div class=\"sidebar-description\">\n           <p class=\"description\">")
        php_print(description_)
        php_print("</p>\n       </div>\n        ")
    # end if
    dynamic_sidebar(sidebar_)
    php_print("</div>")
# end def wp_list_widget_controls
#// 
#// Retrieves the widget control arguments.
#// 
#// @since 2.5.0
#// 
#// @global array $wp_registered_widgets
#// 
#// @staticvar int $i
#// 
#// @param array $params
#// @return array
#//
def wp_list_widget_controls_dynamic_sidebar(params_=None, *_args_):
    
    
    global wp_registered_widgets_
    php_check_if_defined("wp_registered_widgets_")
    i_ = 0
    i_ += 1
    widget_id_ = params_[0]["widget_id"]
    id_ = params_[0]["_temp_id"] if (php_isset(lambda : params_[0]["_temp_id"])) else widget_id_
    hidden_ = " style=\"display:none;\"" if (php_isset(lambda : params_[0]["_hide"])) else ""
    params_[0]["before_widget"] = str("<div id='widget-") + str(i_) + str("_") + str(id_) + str("' class='widget'") + str(hidden_) + str(">")
    params_[0]["after_widget"] = "</div>"
    params_[0]["before_title"] = "%BEG_OF_TITLE%"
    #// Deprecated.
    params_[0]["after_title"] = "%END_OF_TITLE%"
    #// Deprecated.
    if php_is_callable(wp_registered_widgets_[widget_id_]["callback"]):
        wp_registered_widgets_[widget_id_]["_callback"] = wp_registered_widgets_[widget_id_]["callback"]
        wp_registered_widgets_[widget_id_]["callback"] = "wp_widget_control"
    # end if
    return params_
# end def wp_list_widget_controls_dynamic_sidebar
#// 
#// @global array $wp_registered_widgets
#// 
#// @param string $id_base
#// @return int
#//
def next_widget_id_number(id_base_=None, *_args_):
    
    
    global wp_registered_widgets_
    php_check_if_defined("wp_registered_widgets_")
    number_ = 1
    for widget_id_,widget_ in wp_registered_widgets_.items():
        if php_preg_match("/" + id_base_ + "-([0-9]+)$/", widget_id_, matches_):
            number_ = php_max(number_, matches_[1])
        # end if
    # end for
    number_ += 1
    return number_
# end def next_widget_id_number
#// 
#// Meta widget used to display the control form for a widget.
#// 
#// Called from dynamic_sidebar().
#// 
#// @since 2.5.0
#// 
#// @global array $wp_registered_widgets
#// @global array $wp_registered_widget_controls
#// @global array $sidebars_widgets
#// 
#// @param array $sidebar_args
#// @return array
#//
def wp_widget_control(sidebar_args_=None, *_args_):
    
    
    global wp_registered_widgets_
    global wp_registered_widget_controls_
    global sidebars_widgets_
    php_check_if_defined("wp_registered_widgets_","wp_registered_widget_controls_","sidebars_widgets_")
    widget_id_ = sidebar_args_["widget_id"]
    sidebar_id_ = sidebar_args_["id"] if (php_isset(lambda : sidebar_args_["id"])) else False
    key_ = php_array_search(widget_id_, sidebars_widgets_[sidebar_id_]) if sidebar_id_ else "-1"
    #// Position of widget in sidebar.
    control_ = wp_registered_widget_controls_[widget_id_] if (php_isset(lambda : wp_registered_widget_controls_[widget_id_])) else Array()
    widget_ = wp_registered_widgets_[widget_id_]
    id_format_ = widget_["id"]
    widget_number_ = control_["params"][0]["number"] if (php_isset(lambda : control_["params"][0]["number"])) else ""
    id_base_ = control_["id_base"] if (php_isset(lambda : control_["id_base"])) else widget_id_
    width_ = control_["width"] if (php_isset(lambda : control_["width"])) else ""
    height_ = control_["height"] if (php_isset(lambda : control_["height"])) else ""
    multi_number_ = sidebar_args_["_multi_num"] if (php_isset(lambda : sidebar_args_["_multi_num"])) else ""
    add_new_ = sidebar_args_["_add"] if (php_isset(lambda : sidebar_args_["_add"])) else ""
    before_form_ = sidebar_args_["before_form"] if (php_isset(lambda : sidebar_args_["before_form"])) else "<form method=\"post\">"
    after_form_ = sidebar_args_["after_form"] if (php_isset(lambda : sidebar_args_["after_form"])) else "</form>"
    before_widget_content_ = sidebar_args_["before_widget_content"] if (php_isset(lambda : sidebar_args_["before_widget_content"])) else "<div class=\"widget-content\">"
    after_widget_content_ = sidebar_args_["after_widget_content"] if (php_isset(lambda : sidebar_args_["after_widget_content"])) else "</div>"
    query_arg_ = Array({"editwidget": widget_["id"]})
    if add_new_:
        query_arg_["addnew"] = 1
        if multi_number_:
            query_arg_["num"] = multi_number_
            query_arg_["base"] = id_base_
        # end if
    else:
        query_arg_["sidebar"] = sidebar_id_
        query_arg_["key"] = key_
    # end if
    #// 
    #// We aren't showing a widget control, we're outputting a template
    #// for a multi-widget control.
    #//
    if (php_isset(lambda : sidebar_args_["_display"])) and "template" == sidebar_args_["_display"] and widget_number_:
        #// number == -1 implies a template where id numbers are replaced by a generic '__i__'.
        control_["params"][0]["number"] = -1
        #// With id_base widget id's are constructed like {$id_base}-{$id_number}.
        if (php_isset(lambda : control_["id_base"])):
            id_format_ = control_["id_base"] + "-__i__"
        # end if
    # end if
    wp_registered_widgets_[widget_id_]["callback"] = wp_registered_widgets_[widget_id_]["_callback"]
    wp_registered_widgets_[widget_id_]["_callback"] = None
    widget_title_ = esc_html(strip_tags(sidebar_args_["widget_name"]))
    has_form_ = "noform"
    php_print(sidebar_args_["before_widget"])
    php_print("""   <div class=\"widget-top\">
    <div class=\"widget-title-action\">
    <button type=\"button\" class=\"widget-action hide-if-no-js\" aria-expanded=\"false\">
    <span class=\"screen-reader-text edit\">
    """)
    #// translators: %s: Widget title.
    printf(__("Edit widget: %s"), widget_title_)
    php_print("         </span>\n           <span class=\"screen-reader-text add\">\n               ")
    #// translators: %s: Widget title.
    printf(__("Add widget: %s"), widget_title_)
    php_print("""           </span>
    <span class=\"toggle-indicator\" aria-hidden=\"true\"></span>
    </button>
    <a class=\"widget-control-edit hide-if-js\" href=\"""")
    php_print(esc_url(add_query_arg(query_arg_)))
    php_print("\">\n            <span class=\"edit\">")
    _ex("Edit", "widget")
    php_print("</span>\n            <span class=\"add\">")
    _ex("Add", "widget")
    php_print("</span>\n            <span class=\"screen-reader-text\">")
    php_print(widget_title_)
    php_print("""</span>
    </a>
    </div>
    <div class=\"widget-title\"><h3>""")
    php_print(widget_title_)
    php_print("""<span class=\"in-widget-title\"></span></h3></div>
    </div>
    <div class=\"widget-inside\">
    """)
    php_print(before_form_)
    php_print(" ")
    php_print(before_widget_content_)
    php_print(" ")
    if (php_isset(lambda : control_["callback"])):
        has_form_ = call_user_func_array(control_["callback"], control_["params"])
    else:
        php_print("     <p>" + __("There are no options for this widget.") + "</p>\n")
    # end if
    noform_class_ = ""
    if "noform" == has_form_:
        noform_class_ = " widget-control-noform"
    # end if
    php_print(" ")
    php_print(after_widget_content_)
    php_print(" <input type=\"hidden\" name=\"widget-id\" class=\"widget-id\" value=\"")
    php_print(esc_attr(id_format_))
    php_print("\" />\n  <input type=\"hidden\" name=\"id_base\" class=\"id_base\" value=\"")
    php_print(esc_attr(id_base_))
    php_print("\" />\n  <input type=\"hidden\" name=\"widget-width\" class=\"widget-width\" value=\"")
    php_print(esc_attr(width_))
    php_print("\" />\n  <input type=\"hidden\" name=\"widget-height\" class=\"widget-height\" value=\"")
    php_print(esc_attr(height_))
    php_print("\" />\n  <input type=\"hidden\" name=\"widget_number\" class=\"widget_number\" value=\"")
    php_print(esc_attr(widget_number_))
    php_print("\" />\n  <input type=\"hidden\" name=\"multi_number\" class=\"multi_number\" value=\"")
    php_print(esc_attr(multi_number_))
    php_print("\" />\n  <input type=\"hidden\" name=\"add_new\" class=\"add_new\" value=\"")
    php_print(esc_attr(add_new_))
    php_print("""\" />
    <div class=\"widget-control-actions\">
    <div class=\"alignleft\">
    <button type=\"button\" class=\"button-link button-link-delete widget-control-remove\">""")
    _e("Delete")
    php_print("""</button>
    <span class=\"widget-control-close-wrapper\">
    |
    <button type=\"button\" class=\"button-link widget-control-close\">""")
    _e("Done")
    php_print("""</button>
    </span>
    </div>
    <div class=\"alignright""")
    php_print(noform_class_)
    php_print("\">\n            ")
    submit_button(__("Save"), "primary widget-control-save right", "savewidget", False, Array({"id": "widget-" + esc_attr(id_format_) + "-savewidget"}))
    php_print("""           <span class=\"spinner\"></span>
    </div>
    <br class=\"clear\" />
    </div>
    """)
    php_print(after_form_)
    php_print("""   </div>
    <div class=\"widget-description\">
    """)
    widget_description_ = wp_widget_description(widget_id_)
    php_print(str(widget_description_) + str("\n") if widget_description_ else str(widget_title_) + str("\n"))
    php_print(" </div>\n    ")
    php_print(sidebar_args_["after_widget"])
    return sidebar_args_
# end def wp_widget_control
#// 
#// @param string $classes
#// @return string
#//
def wp_widgets_access_body_class(classes_=None, *_args_):
    
    
    return str(classes_) + str(" widgets_access ")
# end def wp_widgets_access_body_class
