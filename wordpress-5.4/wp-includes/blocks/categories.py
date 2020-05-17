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
def render_block_core_categories(attributes_=None, *_args_):
    
    
    block_id_ = 0
    block_id_ += 1
    args_ = Array({"echo": False, "hierarchical": (not php_empty(lambda : attributes_["showHierarchy"])), "orderby": "name", "show_count": (not php_empty(lambda : attributes_["showPostCounts"])), "title_li": ""})
    if (not php_empty(lambda : attributes_["displayAsDropdown"])):
        id_ = "wp-block-categories-" + block_id_
        args_["id"] = id_
        args_["show_option_none"] = __("Select Category")
        wrapper_markup_ = "<div class=\"%1$s\">%2$s</div>"
        items_markup_ = wp_dropdown_categories(args_)
        type_ = "dropdown"
        if (not is_admin()):
            wrapper_markup_ += build_dropdown_script_block_core_categories(id_)
        # end if
    else:
        wrapper_markup_ = "<ul class=\"%1$s\">%2$s</ul>"
        items_markup_ = wp_list_categories(args_)
        type_ = "list"
    # end if
    class_ = str("wp-block-categories wp-block-categories-") + str(type_)
    if (php_isset(lambda : attributes_["align"])):
        class_ += str(" align") + str(attributes_["align"])
    # end if
    if (php_isset(lambda : attributes_["className"])):
        class_ += str(" ") + str(attributes_["className"])
    # end if
    return php_sprintf(wrapper_markup_, esc_attr(class_), items_markup_)
# end def render_block_core_categories
#// 
#// Generates the inline script for a categories dropdown field.
#// 
#// @param string $dropdown_id ID of the dropdown field.
#// 
#// @return string Returns the dropdown onChange redirection script.
#//
def build_dropdown_script_block_core_categories(dropdown_id_=None, *_args_):
    
    
    ob_start()
    php_print("""   <script type='text/javascript'>
    /* <![CDATA[ */
    ( function() {
    var dropdown = document.getElementById( '""")
    php_print(esc_js(dropdown_id_))
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
def register_block_core_categories(*_args_):
    
    
    register_block_type("core/categories", Array({"attributes": Array({"align": Array({"type": "string", "enum": Array("left", "center", "right", "wide", "full")})}, {"className": Array({"type": "string"})}, {"displayAsDropdown": Array({"type": "boolean", "default": False})}, {"showHierarchy": Array({"type": "boolean", "default": False})}, {"showPostCounts": Array({"type": "boolean", "default": False})})}, {"render_callback": "render_block_core_categories"}))
# end def register_block_core_categories
add_action("init", "register_block_core_categories")
