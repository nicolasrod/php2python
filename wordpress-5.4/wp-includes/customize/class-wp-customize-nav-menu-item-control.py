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
#// Customize API: WP_Customize_Nav_Menu_Item_Control class
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 4.4.0
#// 
#// 
#// Customize control to represent the name field for a given menu.
#// 
#// @since 4.3.0
#// 
#// @see WP_Customize_Control
#//
class WP_Customize_Nav_Menu_Item_Control(WP_Customize_Control):
    #// 
    #// Control type.
    #// 
    #// @since 4.3.0
    #// @var string
    #//
    type = "nav_menu_item"
    #// 
    #// The nav menu item setting.
    #// 
    #// @since 4.3.0
    #// @var WP_Customize_Nav_Menu_Item_Setting
    #//
    setting = Array()
    #// 
    #// Constructor.
    #// 
    #// @since 4.3.0
    #// 
    #// @see WP_Customize_Control::__construct()
    #// 
    #// @param WP_Customize_Manager $manager Customizer bootstrap instance.
    #// @param string               $id      The control ID.
    #// @param array                $args    Optional. Arguments to override class property defaults.
    #// See WP_Customize_Control::__construct() for information
    #// on accepted arguments. Default empty array.
    #//
    def __init__(self, manager_=None, id_=None, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        super().__init__(manager_, id_, args_)
    # end def __init__
    #// 
    #// Don't render the control's content - it's rendered with a JS template.
    #// 
    #// @since 4.3.0
    #//
    def render_content(self):
        
        
        pass
    # end def render_content
    #// 
    #// JS/Underscore template for the control UI.
    #// 
    #// @since 4.3.0
    #//
    def content_template(self):
        
        
        php_print("""       <div class=\"menu-item-bar\">
        <div class=\"menu-item-handle\">
        <span class=\"item-type\" aria-hidden=\"true\">{{ data.item_type_label }}</span>
        <span class=\"item-title\" aria-hidden=\"true\">
        <span class=\"spinner\"></span>
        <span class=\"menu-item-title<# if ( ! data.title && ! data.original_title ) { #> no-title<# } #>\">{{ data.title || data.original_title || wp.customize.Menus.data.l10n.untitled }}</span>
        </span>
        <span class=\"item-controls\">
        <button type=\"button\" class=\"button-link item-edit\" aria-expanded=\"false\"><span class=\"screen-reader-text\">
        """)
        #// translators: 1: Title of a menu item, 2: Type of a menu item.
        printf(__("Edit menu item: %1$s (%2$s)"), "{{ data.title || wp.customize.Menus.data.l10n.untitled }}", "{{ data.item_type_label }}")
        php_print("                 </span><span class=\"toggle-indicator\" aria-hidden=\"true\"></span></button>\n                 <button type=\"button\" class=\"button-link item-delete submitdelete deletion\"><span class=\"screen-reader-text\">\n                   ")
        #// translators: 1: Title of a menu item, 2: Type of a menu item.
        printf(__("Remove Menu Item: %1$s (%2$s)"), "{{ data.title || wp.customize.Menus.data.l10n.untitled }}", "{{ data.item_type_label }}")
        php_print("""                   </span></button>
        </span>
        </div>
        </div>
        <div class=\"menu-item-settings\" id=\"menu-item-settings-{{ data.menu_item_id }}\">
        <# if ( 'custom' === data.item_type ) { #>
        <p class=\"field-url description description-thin\">
        <label for=\"edit-menu-item-url-{{ data.menu_item_id }}\">
        """)
        _e("URL")
        php_print("""<br />
        <input class=\"widefat code edit-menu-item-url\" type=\"text\" id=\"edit-menu-item-url-{{ data.menu_item_id }}\" name=\"menu-item-url\" />
        </label>
        </p>
        <# } #>
        <p class=\"description description-thin\">
        <label for=\"edit-menu-item-title-{{ data.menu_item_id }}\">
        """)
        _e("Navigation Label")
        php_print("""<br />
        <input type=\"text\" id=\"edit-menu-item-title-{{ data.menu_item_id }}\" placeholder=\"{{ data.original_title }}\" class=\"widefat edit-menu-item-title\" name=\"menu-item-title\" />
        </label>
        </p>
        <p class=\"field-link-target description description-thin\">
        <label for=\"edit-menu-item-target-{{ data.menu_item_id }}\">
        <input type=\"checkbox\" id=\"edit-menu-item-target-{{ data.menu_item_id }}\" class=\"edit-menu-item-target\" value=\"_blank\" name=\"menu-item-target\" />
        """)
        _e("Open link in a new tab")
        php_print("""               </label>
        </p>
        <p class=\"field-title-attribute field-attr-title description description-thin\">
        <label for=\"edit-menu-item-attr-title-{{ data.menu_item_id }}\">
        """)
        _e("Title Attribute")
        php_print("""<br />
        <input type=\"text\" id=\"edit-menu-item-attr-title-{{ data.menu_item_id }}\" class=\"widefat edit-menu-item-attr-title\" name=\"menu-item-attr-title\" />
        </label>
        </p>
        <p class=\"field-css-classes description description-thin\">
        <label for=\"edit-menu-item-classes-{{ data.menu_item_id }}\">
        """)
        _e("CSS Classes")
        php_print("""<br />
        <input type=\"text\" id=\"edit-menu-item-classes-{{ data.menu_item_id }}\" class=\"widefat code edit-menu-item-classes\" name=\"menu-item-classes\" />
        </label>
        </p>
        <p class=\"field-xfn description description-thin\">
        <label for=\"edit-menu-item-xfn-{{ data.menu_item_id }}\">
        """)
        _e("Link Relationship (XFN)")
        php_print("""<br />
        <input type=\"text\" id=\"edit-menu-item-xfn-{{ data.menu_item_id }}\" class=\"widefat code edit-menu-item-xfn\" name=\"menu-item-xfn\" />
        </label>
        </p>
        <p class=\"field-description description description-thin\">
        <label for=\"edit-menu-item-description-{{ data.menu_item_id }}\">
        """)
        _e("Description")
        php_print("<br />\n                 <textarea id=\"edit-menu-item-description-{{ data.menu_item_id }}\" class=\"widefat edit-menu-item-description\" rows=\"3\" cols=\"20\" name=\"menu-item-description\">{{ data.description }}</textarea>\n                  <span class=\"description\">")
        _e("The description will be displayed in the menu if the current theme supports it.")
        php_print("""</span>
        </label>
        </p>
        """)
        #// 
        #// Fires at the end of the form field template for nav menu items in the customizer.
        #// 
        #// Additional fields can be rendered here and managed in JavaScript.
        #// 
        #// @since 5.4.0
        #//
        do_action("wp_nav_menu_item_custom_fields_customize_template")
        php_print("""
        <div class=\"menu-item-actions description-thin submitbox\">
        <# if ( ( 'post_type' === data.item_type || 'taxonomy' === data.item_type ) && '' !== data.original_title ) { #>
        <p class=\"link-to-original\">
        """)
        #// translators: Nav menu item original title. %s: Original title.
        printf(__("Original: %s"), "<a class=\"original-link\" href=\"{{ data.url }}\">{{ data.original_title }}</a>")
        php_print("""               </p>
        <# } #>
        <button type=\"button\" class=\"button-link button-link-delete item-delete submitdelete deletion\">""")
        _e("Remove")
        php_print("""</button>
        <span class=\"spinner\"></span>
        </div>
        <input type=\"hidden\" name=\"menu-item-db-id[{{ data.menu_item_id }}]\" class=\"menu-item-data-db-id\" value=\"{{ data.menu_item_id }}\" />
        <input type=\"hidden\" name=\"menu-item-parent-id[{{ data.menu_item_id }}]\" class=\"menu-item-data-parent-id\" value=\"{{ data.parent }}\" />
        </div><!-- .menu-item-settings-->
        <ul class=\"menu-item-transport\"></ul>
        """)
    # end def content_template
    #// 
    #// Return parameters for this control.
    #// 
    #// @since 4.3.0
    #// 
    #// @return array Exported parameters.
    #//
    def json(self):
        
        
        exported_ = super().json()
        exported_["menu_item_id"] = self.setting.post_id
        return exported_
    # end def json
# end class WP_Customize_Nav_Menu_Item_Control
