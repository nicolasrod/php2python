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
def wp_list_widgets(*args_):
    
    global wp_registered_widgets,wp_registered_widget_controls
    php_check_if_defined("wp_registered_widgets","wp_registered_widget_controls")
    sort = wp_registered_widgets
    usort(sort, "_sort_name_callback")
    done = Array()
    for widget in sort:
        if php_in_array(widget["callback"], done, True):
            continue
        # end if
        sidebar = is_active_widget(widget["callback"], widget["id"], False, False)
        done[-1] = widget["callback"]
        if (not (php_isset(lambda : widget["params"][0]))):
            widget["params"][0] = Array()
        # end if
        args = Array({"widget_id": widget["id"], "widget_name": widget["name"], "_display": "template"})
        if (php_isset(lambda : wp_registered_widget_controls[widget["id"]]["id_base"])) and (php_isset(lambda : widget["params"][0]["number"])):
            id_base = wp_registered_widget_controls[widget["id"]]["id_base"]
            args["_temp_id"] = str(id_base) + str("-__i__")
            args["_multi_num"] = next_widget_id_number(id_base)
            args["_add"] = "multi"
        else:
            args["_add"] = "single"
            if sidebar:
                args["_hide"] = "1"
            # end if
        # end if
        control_args = Array({0: args, 1: widget["params"][0]})
        sidebar_args = wp_list_widget_controls_dynamic_sidebar(control_args)
        wp_widget_control(sidebar_args)
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
def _sort_name_callback(a=None, b=None, *args_):
    
    return strnatcasecmp(a["name"], b["name"])
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
def wp_list_widget_controls(sidebar=None, sidebar_name="", *args_):
    
    add_filter("dynamic_sidebar_params", "wp_list_widget_controls_dynamic_sidebar")
    description = wp_sidebar_description(sidebar)
    php_print("<div id=\"" + esc_attr(sidebar) + "\" class=\"widgets-sortables\">")
    if sidebar_name:
        add_to = php_sprintf(__("Add to: %s"), sidebar_name)
        php_print("     <div class=\"sidebar-name\" data-add-to=\"")
        php_print(esc_attr(add_to))
        php_print("\">\n            <button type=\"button\" class=\"handlediv hide-if-no-js\" aria-expanded=\"true\">\n             <span class=\"screen-reader-text\">")
        php_print(esc_html(sidebar_name))
        php_print("""</span>
        <span class=\"toggle-indicator\" aria-hidden=\"true\"></span>
        </button>
        <h2>""")
        php_print(esc_html(sidebar_name))
        php_print(" <span class=\"spinner\"></span></h2>\n      </div>\n        ")
    # end if
    if (not php_empty(lambda : description)):
        php_print("     <div class=\"sidebar-description\">\n           <p class=\"description\">")
        php_print(description)
        php_print("</p>\n       </div>\n        ")
    # end if
    dynamic_sidebar(sidebar)
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
def wp_list_widget_controls_dynamic_sidebar(params=None, *args_):
    
    global wp_registered_widgets
    php_check_if_defined("wp_registered_widgets")
    i = 0
    i += 1
    widget_id = params[0]["widget_id"]
    id = params[0]["_temp_id"] if (php_isset(lambda : params[0]["_temp_id"])) else widget_id
    hidden = " style=\"display:none;\"" if (php_isset(lambda : params[0]["_hide"])) else ""
    params[0]["before_widget"] = str("<div id='widget-") + str(i) + str("_") + str(id) + str("' class='widget'") + str(hidden) + str(">")
    params[0]["after_widget"] = "</div>"
    params[0]["before_title"] = "%BEG_OF_TITLE%"
    #// Deprecated.
    params[0]["after_title"] = "%END_OF_TITLE%"
    #// Deprecated.
    if php_is_callable(wp_registered_widgets[widget_id]["callback"]):
        wp_registered_widgets[widget_id]["_callback"] = wp_registered_widgets[widget_id]["callback"]
        wp_registered_widgets[widget_id]["callback"] = "wp_widget_control"
    # end if
    return params
# end def wp_list_widget_controls_dynamic_sidebar
#// 
#// @global array $wp_registered_widgets
#// 
#// @param string $id_base
#// @return int
#//
def next_widget_id_number(id_base=None, *args_):
    
    global wp_registered_widgets
    php_check_if_defined("wp_registered_widgets")
    number = 1
    for widget_id,widget in wp_registered_widgets:
        if php_preg_match("/" + id_base + "-([0-9]+)$/", widget_id, matches):
            number = php_max(number, matches[1])
        # end if
    # end for
    number += 1
    return number
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
def wp_widget_control(sidebar_args=None, *args_):
    
    global wp_registered_widgets,wp_registered_widget_controls,sidebars_widgets
    php_check_if_defined("wp_registered_widgets","wp_registered_widget_controls","sidebars_widgets")
    widget_id = sidebar_args["widget_id"]
    sidebar_id = sidebar_args["id"] if (php_isset(lambda : sidebar_args["id"])) else False
    key = php_array_search(widget_id, sidebars_widgets[sidebar_id]) if sidebar_id else "-1"
    #// Position of widget in sidebar.
    control = wp_registered_widget_controls[widget_id] if (php_isset(lambda : wp_registered_widget_controls[widget_id])) else Array()
    widget = wp_registered_widgets[widget_id]
    id_format = widget["id"]
    widget_number = control["params"][0]["number"] if (php_isset(lambda : control["params"][0]["number"])) else ""
    id_base = control["id_base"] if (php_isset(lambda : control["id_base"])) else widget_id
    width = control["width"] if (php_isset(lambda : control["width"])) else ""
    height = control["height"] if (php_isset(lambda : control["height"])) else ""
    multi_number = sidebar_args["_multi_num"] if (php_isset(lambda : sidebar_args["_multi_num"])) else ""
    add_new = sidebar_args["_add"] if (php_isset(lambda : sidebar_args["_add"])) else ""
    before_form = sidebar_args["before_form"] if (php_isset(lambda : sidebar_args["before_form"])) else "<form method=\"post\">"
    after_form = sidebar_args["after_form"] if (php_isset(lambda : sidebar_args["after_form"])) else "</form>"
    before_widget_content = sidebar_args["before_widget_content"] if (php_isset(lambda : sidebar_args["before_widget_content"])) else "<div class=\"widget-content\">"
    after_widget_content = sidebar_args["after_widget_content"] if (php_isset(lambda : sidebar_args["after_widget_content"])) else "</div>"
    query_arg = Array({"editwidget": widget["id"]})
    if add_new:
        query_arg["addnew"] = 1
        if multi_number:
            query_arg["num"] = multi_number
            query_arg["base"] = id_base
        # end if
    else:
        query_arg["sidebar"] = sidebar_id
        query_arg["key"] = key
    # end if
    #// 
    #// We aren't showing a widget control, we're outputting a template
    #// for a multi-widget control.
    #//
    if (php_isset(lambda : sidebar_args["_display"])) and "template" == sidebar_args["_display"] and widget_number:
        #// number == -1 implies a template where id numbers are replaced by a generic '__i__'.
        control["params"][0]["number"] = -1
        #// With id_base widget id's are constructed like {$id_base}-{$id_number}.
        if (php_isset(lambda : control["id_base"])):
            id_format = control["id_base"] + "-__i__"
        # end if
    # end if
    wp_registered_widgets[widget_id]["callback"] = wp_registered_widgets[widget_id]["_callback"]
    wp_registered_widgets[widget_id]["_callback"] = None
    widget_title = esc_html(strip_tags(sidebar_args["widget_name"]))
    has_form = "noform"
    php_print(sidebar_args["before_widget"])
    php_print("""   <div class=\"widget-top\">
    <div class=\"widget-title-action\">
    <button type=\"button\" class=\"widget-action hide-if-no-js\" aria-expanded=\"false\">
    <span class=\"screen-reader-text edit\">
    """)
    #// translators: %s: Widget title.
    printf(__("Edit widget: %s"), widget_title)
    php_print("         </span>\n           <span class=\"screen-reader-text add\">\n               ")
    #// translators: %s: Widget title.
    printf(__("Add widget: %s"), widget_title)
    php_print("""           </span>
    <span class=\"toggle-indicator\" aria-hidden=\"true\"></span>
    </button>
    <a class=\"widget-control-edit hide-if-js\" href=\"""")
    php_print(esc_url(add_query_arg(query_arg)))
    php_print("\">\n            <span class=\"edit\">")
    _ex("Edit", "widget")
    php_print("</span>\n            <span class=\"add\">")
    _ex("Add", "widget")
    php_print("</span>\n            <span class=\"screen-reader-text\">")
    php_print(widget_title)
    php_print("""</span>
    </a>
    </div>
    <div class=\"widget-title\"><h3>""")
    php_print(widget_title)
    php_print("""<span class=\"in-widget-title\"></span></h3></div>
    </div>
    <div class=\"widget-inside\">
    """)
    php_print(before_form)
    php_print(" ")
    php_print(before_widget_content)
    php_print(" ")
    if (php_isset(lambda : control["callback"])):
        has_form = call_user_func_array(control["callback"], control["params"])
    else:
        php_print("     <p>" + __("There are no options for this widget.") + "</p>\n")
    # end if
    noform_class = ""
    if "noform" == has_form:
        noform_class = " widget-control-noform"
    # end if
    php_print(" ")
    php_print(after_widget_content)
    php_print(" <input type=\"hidden\" name=\"widget-id\" class=\"widget-id\" value=\"")
    php_print(esc_attr(id_format))
    php_print("\" />\n  <input type=\"hidden\" name=\"id_base\" class=\"id_base\" value=\"")
    php_print(esc_attr(id_base))
    php_print("\" />\n  <input type=\"hidden\" name=\"widget-width\" class=\"widget-width\" value=\"")
    php_print(esc_attr(width))
    php_print("\" />\n  <input type=\"hidden\" name=\"widget-height\" class=\"widget-height\" value=\"")
    php_print(esc_attr(height))
    php_print("\" />\n  <input type=\"hidden\" name=\"widget_number\" class=\"widget_number\" value=\"")
    php_print(esc_attr(widget_number))
    php_print("\" />\n  <input type=\"hidden\" name=\"multi_number\" class=\"multi_number\" value=\"")
    php_print(esc_attr(multi_number))
    php_print("\" />\n  <input type=\"hidden\" name=\"add_new\" class=\"add_new\" value=\"")
    php_print(esc_attr(add_new))
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
    php_print(noform_class)
    php_print("\">\n            ")
    submit_button(__("Save"), "primary widget-control-save right", "savewidget", False, Array({"id": "widget-" + esc_attr(id_format) + "-savewidget"}))
    php_print("""           <span class=\"spinner\"></span>
    </div>
    <br class=\"clear\" />
    </div>
    """)
    php_print(after_form)
    php_print("""   </div>
    <div class=\"widget-description\">
    """)
    widget_description = wp_widget_description(widget_id)
    php_print(str(widget_description) + str("\n") if widget_description else str(widget_title) + str("\n"))
    php_print(" </div>\n    ")
    php_print(sidebar_args["after_widget"])
    return sidebar_args
# end def wp_widget_control
#// 
#// @param string $classes
#// @return string
#//
def wp_widgets_access_body_class(classes=None, *args_):
    
    return str(classes) + str(" widgets_access ")
# end def wp_widgets_access_body_class
