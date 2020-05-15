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
#// Server-side rendering of the `core/categories` block.
#// 
#// @package WordPress
#// 
#// 
#// Renders the `core/categories` block on server.
#// 
#// @param array $attributes The block attributes.
#// 
#// @return string Returns the categories list/dropdown markup.
#//
def render_block_core_categories(attributes=None, *args_):
    
    block_id = 0
    block_id += 1
    args = Array({"echo": False, "hierarchical": (not php_empty(lambda : attributes["showHierarchy"])), "orderby": "name", "show_count": (not php_empty(lambda : attributes["showPostCounts"])), "title_li": ""})
    if (not php_empty(lambda : attributes["displayAsDropdown"])):
        id = "wp-block-categories-" + block_id
        args["id"] = id
        args["show_option_none"] = __("Select Category")
        wrapper_markup = "<div class=\"%1$s\">%2$s</div>"
        items_markup = wp_dropdown_categories(args)
        type = "dropdown"
        if (not is_admin()):
            wrapper_markup += build_dropdown_script_block_core_categories(id)
        # end if
    else:
        wrapper_markup = "<ul class=\"%1$s\">%2$s</ul>"
        items_markup = wp_list_categories(args)
        type = "list"
    # end if
    class_ = str("wp-block-categories wp-block-categories-") + str(type)
    if (php_isset(lambda : attributes["align"])):
        class_ += str(" align") + str(attributes["align"])
    # end if
    if (php_isset(lambda : attributes["className"])):
        class_ += str(" ") + str(attributes["className"])
    # end if
    return php_sprintf(wrapper_markup, esc_attr(class_), items_markup)
# end def render_block_core_categories
#// 
#// Generates the inline script for a categories dropdown field.
#// 
#// @param string $dropdown_id ID of the dropdown field.
#// 
#// @return string Returns the dropdown onChange redirection script.
#//
def build_dropdown_script_block_core_categories(dropdown_id=None, *args_):
    
    ob_start()
    php_print("""   <script type='text/javascript'>
    /* <![CDATA[ */
    ( function() {
    var dropdown = document.getElementById( '""")
    php_print(esc_js(dropdown_id))
    php_print("""' );
    function onCatChange() {
if ( dropdown.options[ dropdown.selectedIndex ].value > 0 ) {
    location.href = \"""")
    php_print(home_url())
    php_print("""/?cat=\" + dropdown.options[ dropdown.selectedIndex ].value;
    }
    }
    dropdown.onchange = onCatChange;
    })();
    /* ]]> */
    </script>
    """)
    return ob_get_clean()
# end def build_dropdown_script_block_core_categories
#// 
#// Registers the `core/categories` block on server.
#//
def register_block_core_categories(*args_):
    
    register_block_type("core/categories", Array({"attributes": Array({"align": Array({"type": "string", "enum": Array("left", "center", "right", "wide", "full")})}, {"className": Array({"type": "string"})}, {"displayAsDropdown": Array({"type": "boolean", "default": False})}, {"showHierarchy": Array({"type": "boolean", "default": False})}, {"showPostCounts": Array({"type": "boolean", "default": False})})}, {"render_callback": "render_block_core_categories"}))
# end def register_block_core_categories
add_action("init", "register_block_core_categories")
