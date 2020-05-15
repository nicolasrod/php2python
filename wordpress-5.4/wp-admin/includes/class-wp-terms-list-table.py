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
#// List Table API: WP_Terms_List_Table class
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 3.1.0
#// 
#// 
#// Core class used to implement displaying terms in a list table.
#// 
#// @since 3.1.0
#// @access private
#// 
#// @see WP_List_Table
#//
class WP_Terms_List_Table(WP_List_Table):
    callback_args = Array()
    level = Array()
    #// 
    #// Constructor.
    #// 
    #// @since 3.1.0
    #// 
    #// @see WP_List_Table::__construct() for more information on default arguments.
    #// 
    #// @global string $post_type
    #// @global string $taxonomy
    #// @global string $action
    #// @global object $tax
    #// 
    #// @param array $args An associative array of arguments.
    #//
    def __init__(self, args=Array()):
        
        global post_type,taxonomy,action,tax
        php_check_if_defined("post_type","taxonomy","action","tax")
        super().__init__(Array({"plural": "tags", "singular": "tag", "screen": args["screen"] if (php_isset(lambda : args["screen"])) else None}))
        action = self.screen.action
        post_type = self.screen.post_type
        taxonomy = self.screen.taxonomy
        if php_empty(lambda : taxonomy):
            taxonomy = "post_tag"
        # end if
        if (not taxonomy_exists(taxonomy)):
            wp_die(__("Invalid taxonomy."))
        # end if
        tax = get_taxonomy(taxonomy)
        #// @todo Still needed? Maybe just the show_ui part.
        if php_empty(lambda : post_type) or (not php_in_array(post_type, get_post_types(Array({"show_ui": True})))):
            post_type = "post"
        # end if
    # end def __init__
    #// 
    #// @return bool
    #//
    def ajax_user_can(self):
        
        return current_user_can(get_taxonomy(self.screen.taxonomy).cap.manage_terms)
    # end def ajax_user_can
    #// 
    #//
    def prepare_items(self):
        
        tags_per_page = self.get_items_per_page("edit_" + self.screen.taxonomy + "_per_page")
        if "post_tag" == self.screen.taxonomy:
            #// 
            #// Filters the number of terms displayed per page for the Tags list table.
            #// 
            #// @since 2.8.0
            #// 
            #// @param int $tags_per_page Number of tags to be displayed. Default 20.
            #//
            tags_per_page = apply_filters("edit_tags_per_page", tags_per_page)
            #// 
            #// Filters the number of terms displayed per page for the Tags list table.
            #// 
            #// @since 2.7.0
            #// @deprecated 2.8.0 Use {@see 'edit_tags_per_page'} instead.
            #// 
            #// @param int $tags_per_page Number of tags to be displayed. Default 20.
            #//
            tags_per_page = apply_filters_deprecated("tagsperpage", Array(tags_per_page), "2.8.0", "edit_tags_per_page")
        elif "category" == self.screen.taxonomy:
            #// 
            #// Filters the number of terms displayed per page for the Categories list table.
            #// 
            #// @since 2.8.0
            #// 
            #// @param int $tags_per_page Number of categories to be displayed. Default 20.
            #//
            tags_per_page = apply_filters("edit_categories_per_page", tags_per_page)
        # end if
        search = php_trim(wp_unslash(PHP_REQUEST["s"])) if (not php_empty(lambda : PHP_REQUEST["s"])) else ""
        args = Array({"search": search, "page": self.get_pagenum(), "number": tags_per_page})
        if (not php_empty(lambda : PHP_REQUEST["orderby"])):
            args["orderby"] = php_trim(wp_unslash(PHP_REQUEST["orderby"]))
        # end if
        if (not php_empty(lambda : PHP_REQUEST["order"])):
            args["order"] = php_trim(wp_unslash(PHP_REQUEST["order"]))
        # end if
        self.callback_args = args
        self.set_pagination_args(Array({"total_items": wp_count_terms(self.screen.taxonomy, compact("search")), "per_page": tags_per_page}))
    # end def prepare_items
    #// 
    #// @return bool
    #//
    def has_items(self):
        
        #// @todo Populate $this->items in prepare_items().
        return True
    # end def has_items
    #// 
    #//
    def no_items(self):
        
        php_print(get_taxonomy(self.screen.taxonomy).labels.not_found)
    # end def no_items
    #// 
    #// @return array
    #//
    def get_bulk_actions(self):
        
        actions = Array()
        if current_user_can(get_taxonomy(self.screen.taxonomy).cap.delete_terms):
            actions["delete"] = __("Delete")
        # end if
        return actions
    # end def get_bulk_actions
    #// 
    #// @return string
    #//
    def current_action(self):
        
        if (php_isset(lambda : PHP_REQUEST["action"])) and (php_isset(lambda : PHP_REQUEST["delete_tags"])) and "delete" == PHP_REQUEST["action"] or "delete" == PHP_REQUEST["action2"]:
            return "bulk-delete"
        # end if
        return super().current_action()
    # end def current_action
    #// 
    #// @return array
    #//
    def get_columns(self):
        
        columns = Array({"cb": "<input type=\"checkbox\" />", "name": _x("Name", "term name"), "description": __("Description"), "slug": __("Slug")})
        if "link_category" == self.screen.taxonomy:
            columns["links"] = __("Links")
        else:
            columns["posts"] = _x("Count", "Number/count of items")
        # end if
        return columns
    # end def get_columns
    #// 
    #// @return array
    #//
    def get_sortable_columns(self):
        
        return Array({"name": "name", "description": "description", "slug": "slug", "posts": "count", "links": "count"})
    # end def get_sortable_columns
    #// 
    #//
    def display_rows_or_placeholder(self):
        
        taxonomy = self.screen.taxonomy
        args = wp_parse_args(self.callback_args, Array({"taxonomy": taxonomy, "page": 1, "number": 20, "search": "", "hide_empty": 0}))
        page = args["page"]
        #// Set variable because $args['number'] can be subsequently overridden.
        number = args["number"]
        offset = page - 1 * number
        args["offset"] = offset
        #// Convert it to table rows.
        count = 0
        if is_taxonomy_hierarchical(taxonomy) and (not (php_isset(lambda : args["orderby"]))):
            #// We'll need the full set of terms then.
            args["number"] = 0
            args["offset"] = args["number"]
        # end if
        terms = get_terms(args)
        if php_empty(lambda : terms) or (not php_is_array(terms)):
            php_print("<tr class=\"no-items\"><td class=\"colspanchange\" colspan=\"" + self.get_column_count() + "\">")
            self.no_items()
            php_print("</td></tr>")
            return
        # end if
        if is_taxonomy_hierarchical(taxonomy) and (not (php_isset(lambda : args["orderby"]))):
            if (not php_empty(lambda : args["search"])):
                #// Ignore children on searches.
                children = Array()
            else:
                children = _get_term_hierarchy(taxonomy)
            # end if
            #// 
            #// Some funky recursion to get the job done (paging & parents mainly) is contained within.
            #// Skip it for non-hierarchical taxonomies for performance sake.
            #//
            self._rows(taxonomy, terms, children, offset, number, count)
        else:
            for term in terms:
                self.single_row(term)
            # end for
        # end if
    # end def display_rows_or_placeholder
    #// 
    #// @param string $taxonomy
    #// @param array $terms
    #// @param array $children
    #// @param int   $start
    #// @param int   $per_page
    #// @param int   $count
    #// @param int   $parent
    #// @param int   $level
    #//
    def _rows(self, taxonomy=None, terms=None, children=None, start=None, per_page=None, count=None, parent=0, level=0):
        
        end_ = start + per_page
        for key,term in terms:
            if count >= end_:
                break
            # end if
            if term.parent != parent and php_empty(lambda : PHP_REQUEST["s"]):
                continue
            # end if
            #// If the page starts in a subtree, print the parents.
            if count == start and term.parent > 0 and php_empty(lambda : PHP_REQUEST["s"]):
                my_parents = Array()
                parent_ids = Array()
                p = term.parent
                while True:
                    
                    if not (p):
                        break
                    # end if
                    my_parent = get_term(p, taxonomy)
                    my_parents[-1] = my_parent
                    p = my_parent.parent
                    if php_in_array(p, parent_ids):
                        break
                    # end if
                    parent_ids[-1] = p
                # end while
                parent_ids = None
                num_parents = php_count(my_parents)
                while True:
                    my_parent = php_array_pop(my_parents)
                    if not (my_parent):
                        break
                    # end if
                    php_print(" ")
                    self.single_row(my_parent, level - num_parents)
                    num_parents -= 1
                # end while
            # end if
            if count >= start:
                php_print(" ")
                self.single_row(term, level)
            # end if
            count += 1
            terms[key] = None
            if (php_isset(lambda : children[term.term_id])) and php_empty(lambda : PHP_REQUEST["s"]):
                self._rows(taxonomy, terms, children, start, per_page, count, term.term_id, level + 1)
            # end if
        # end for
    # end def _rows
    #// 
    #// @global string $taxonomy
    #// @param WP_Term $tag Term object.
    #// @param int $level
    #//
    def single_row(self, tag=None, level=0):
        
        global taxonomy
        php_check_if_defined("taxonomy")
        tag = sanitize_term(tag, taxonomy)
        self.level = level
        if tag.parent:
            count = php_count(get_ancestors(tag.term_id, taxonomy, "taxonomy"))
            level = "level-" + count
        else:
            level = "level-0"
        # end if
        php_print("<tr id=\"tag-" + tag.term_id + "\" class=\"" + level + "\">")
        self.single_row_columns(tag)
        php_print("</tr>")
    # end def single_row
    #// 
    #// @param WP_Term $tag Term object.
    #// @return string
    #//
    def column_cb(self, tag=None):
        
        if current_user_can("delete_term", tag.term_id):
            return php_sprintf("<label class=\"screen-reader-text\" for=\"cb-select-%1$s\">%2$s</label>" + "<input type=\"checkbox\" name=\"delete_tags[]\" value=\"%1$s\" id=\"cb-select-%1$s\" />", tag.term_id, php_sprintf(__("Select %s"), tag.name))
        # end if
        return "&nbsp;"
    # end def column_cb
    #// 
    #// @param WP_Term $tag Term object.
    #// @return string
    #//
    def column_name(self, tag=None):
        
        taxonomy = self.screen.taxonomy
        pad = php_str_repeat("&#8212; ", php_max(0, self.level))
        #// 
        #// Filters display of the term name in the terms list table.
        #// 
        #// The default output may include padding due to the term's
        #// current level in the term hierarchy.
        #// 
        #// @since 2.5.0
        #// 
        #// @see WP_Terms_List_Table::column_name()
        #// 
        #// @param string $pad_tag_name The term name, padded if not top-level.
        #// @param WP_Term $tag         Term object.
        #//
        name = apply_filters("term_name", pad + " " + tag.name, tag)
        qe_data = get_term(tag.term_id, taxonomy, OBJECT, "edit")
        uri = wp_get_referer() if wp_doing_ajax() else PHP_SERVER["REQUEST_URI"]
        edit_link = get_edit_term_link(tag.term_id, taxonomy, self.screen.post_type)
        if edit_link:
            edit_link = add_query_arg("wp_http_referer", urlencode(wp_unslash(uri)), edit_link)
            name = php_sprintf("<a class=\"row-title\" href=\"%s\" aria-label=\"%s\">%s</a>", esc_url(edit_link), esc_attr(php_sprintf(__("&#8220;%s&#8221; (Edit)"), tag.name)), name)
        # end if
        out = php_sprintf("<strong>%s</strong><br />", name)
        out += "<div class=\"hidden\" id=\"inline_" + qe_data.term_id + "\">"
        out += "<div class=\"name\">" + qe_data.name + "</div>"
        #// This filter is documented in wp-admin/edit-tag-form.php
        out += "<div class=\"slug\">" + apply_filters("editable_slug", qe_data.slug, qe_data) + "</div>"
        out += "<div class=\"parent\">" + qe_data.parent + "</div></div>"
        return out
    # end def column_name
    #// 
    #// Gets the name of the default primary column.
    #// 
    #// @since 4.3.0
    #// 
    #// @return string Name of the default primary column, in this case, 'name'.
    #//
    def get_default_primary_column_name(self):
        
        return "name"
    # end def get_default_primary_column_name
    #// 
    #// Generates and displays row action links.
    #// 
    #// @since 4.3.0
    #// 
    #// @param WP_Term $tag         Tag being acted upon.
    #// @param string  $column_name Current column name.
    #// @param string  $primary     Primary column name.
    #// @return string Row actions output for terms, or an empty string
    #// if the current column is not the primary column.
    #//
    def handle_row_actions(self, tag=None, column_name=None, primary=None):
        
        if primary != column_name:
            return ""
        # end if
        taxonomy = self.screen.taxonomy
        tax = get_taxonomy(taxonomy)
        uri = wp_get_referer() if wp_doing_ajax() else PHP_SERVER["REQUEST_URI"]
        edit_link = add_query_arg("wp_http_referer", urlencode(wp_unslash(uri)), get_edit_term_link(tag.term_id, taxonomy, self.screen.post_type))
        actions = Array()
        if current_user_can("edit_term", tag.term_id):
            actions["edit"] = php_sprintf("<a href=\"%s\" aria-label=\"%s\">%s</a>", esc_url(edit_link), esc_attr(php_sprintf(__("Edit &#8220;%s&#8221;"), tag.name)), __("Edit"))
            actions["inline hide-if-no-js"] = php_sprintf("<button type=\"button\" class=\"button-link editinline\" aria-label=\"%s\" aria-expanded=\"false\">%s</button>", esc_attr(php_sprintf(__("Quick edit &#8220;%s&#8221; inline"), tag.name)), __("Quick&nbsp;Edit"))
        # end if
        if current_user_can("delete_term", tag.term_id):
            actions["delete"] = php_sprintf("<a href=\"%s\" class=\"delete-tag aria-button-if-js\" aria-label=\"%s\">%s</a>", wp_nonce_url(str("edit-tags.php?action=delete&amp;taxonomy=") + str(taxonomy) + str("&amp;tag_ID=") + str(tag.term_id), "delete-tag_" + tag.term_id), esc_attr(php_sprintf(__("Delete &#8220;%s&#8221;"), tag.name)), __("Delete"))
        # end if
        if is_taxonomy_viewable(tax):
            actions["view"] = php_sprintf("<a href=\"%s\" aria-label=\"%s\">%s</a>", get_term_link(tag), esc_attr(php_sprintf(__("View &#8220;%s&#8221; archive"), tag.name)), __("View"))
        # end if
        #// 
        #// Filters the action links displayed for each term in the Tags list table.
        #// 
        #// @since 2.8.0
        #// @deprecated 3.0.0 Use {@see '{$taxonomy}_row_actions'} instead.
        #// 
        #// @param string[] $actions An array of action links to be displayed. Default
        #// 'Edit', 'Quick Edit', 'Delete', and 'View'.
        #// @param WP_Term  $tag     Term object.
        #//
        actions = apply_filters_deprecated("tag_row_actions", Array(actions, tag), "3.0.0", "{$taxonomy}_row_actions")
        #// 
        #// Filters the action links displayed for each term in the terms list table.
        #// 
        #// The dynamic portion of the hook name, `$taxonomy`, refers to the taxonomy slug.
        #// 
        #// @since 3.0.0
        #// 
        #// @param string[] $actions An array of action links to be displayed. Default
        #// 'Edit', 'Quick Edit', 'Delete', and 'View'.
        #// @param WP_Term  $tag     Term object.
        #//
        actions = apply_filters(str(taxonomy) + str("_row_actions"), actions, tag)
        return self.row_actions(actions)
    # end def handle_row_actions
    #// 
    #// @param WP_Term $tag Term object.
    #// @return string
    #//
    def column_description(self, tag=None):
        
        if tag.description:
            return tag.description
        else:
            return "<span aria-hidden=\"true\">&#8212;</span><span class=\"screen-reader-text\">" + __("No description") + "</span>"
        # end if
    # end def column_description
    #// 
    #// @param WP_Term $tag Term object.
    #// @return string
    #//
    def column_slug(self, tag=None):
        
        #// This filter is documented in wp-admin/edit-tag-form.php
        return apply_filters("editable_slug", tag.slug, tag)
    # end def column_slug
    #// 
    #// @param WP_Term $tag Term object.
    #// @return string
    #//
    def column_posts(self, tag=None):
        
        count = number_format_i18n(tag.count)
        tax = get_taxonomy(self.screen.taxonomy)
        ptype_object = get_post_type_object(self.screen.post_type)
        if (not ptype_object.show_ui):
            return count
        # end if
        if tax.query_var:
            args = Array({tax.query_var: tag.slug})
        else:
            args = Array({"taxonomy": tax.name, "term": tag.slug})
        # end if
        if "post" != self.screen.post_type:
            args["post_type"] = self.screen.post_type
        # end if
        if "attachment" == self.screen.post_type:
            return "<a href='" + esc_url(add_query_arg(args, "upload.php")) + str("'>") + str(count) + str("</a>")
        # end if
        return "<a href='" + esc_url(add_query_arg(args, "edit.php")) + str("'>") + str(count) + str("</a>")
    # end def column_posts
    #// 
    #// @param WP_Term $tag Term object.
    #// @return string
    #//
    def column_links(self, tag=None):
        
        count = number_format_i18n(tag.count)
        if count:
            count = str("<a href='link-manager.php?cat_id=") + str(tag.term_id) + str("'>") + str(count) + str("</a>")
        # end if
        return count
    # end def column_links
    #// 
    #// @param WP_Term $tag Term object.
    #// @param string $column_name
    #// @return string
    #//
    def column_default(self, tag=None, column_name=None):
        
        #// 
        #// Filters the displayed columns in the terms list table.
        #// 
        #// The dynamic portion of the hook name, `$this->screen->taxonomy`,
        #// refers to the slug of the current taxonomy.
        #// 
        #// @since 2.8.0
        #// 
        #// @param string $string      Blank string.
        #// @param string $column_name Name of the column.
        #// @param int    $term_id     Term ID.
        #//
        return apply_filters(str("manage_") + str(self.screen.taxonomy) + str("_custom_column"), "", column_name, tag.term_id)
    # end def column_default
    #// 
    #// Outputs the hidden row displayed when inline editing
    #// 
    #// @since 3.1.0
    #//
    def inline_edit(self):
        
        tax = get_taxonomy(self.screen.taxonomy)
        if (not current_user_can(tax.cap.edit_terms)):
            return
        # end if
        php_print("""
        <form method=\"get\">
        <table style=\"display: none\"><tbody id=\"inlineedit\">
        <tr id=\"inline-edit\" class=\"inline-edit-row\" style=\"display: none\">
        <td colspan=\"""")
        php_print(self.get_column_count())
        php_print("""\" class=\"colspanchange\">
        <fieldset>
        <legend class=\"inline-edit-legend\">""")
        _e("Quick Edit")
        php_print("""</legend>
        <div class=\"inline-edit-col\">
        <label>
        <span class=\"title\">""")
        _ex("Name", "term name")
        php_print("""</span>
        <span class=\"input-text-wrap\"><input type=\"text\" name=\"name\" class=\"ptitle\" value=\"\" /></span>
        </label>
        """)
        if (not global_terms_enabled()):
            php_print("                 <label>\n                       <span class=\"title\">")
            _e("Slug")
            php_print("""</span>
            <span class=\"input-text-wrap\"><input type=\"text\" name=\"slug\" class=\"ptitle\" value=\"\" /></span>
            </label>
            """)
        # end if
        php_print("""               </div>
        </fieldset>
        """)
        core_columns = Array({"cb": True, "description": True, "name": True, "slug": True, "posts": True})
        columns = self.get_column_info()
        for column_name,column_display_name in columns:
            if (php_isset(lambda : core_columns[column_name])):
                continue
            # end if
            #// This action is documented in wp-admin/includes/class-wp-posts-list-table.php
            do_action("quick_edit_custom_box", column_name, "edit-tags", self.screen.taxonomy)
        # end for
        php_print("\n           <div class=\"inline-edit-save submit\">\n               <button type=\"button\" class=\"cancel button alignleft\">")
        _e("Cancel")
        php_print("</button>\n              <button type=\"button\" class=\"save button button-primary alignright\">")
        php_print(tax.labels.update_item)
        php_print("""</button>
        <span class=\"spinner\"></span>
        """)
        wp_nonce_field("taxinlineeditnonce", "_inline_edit", False)
        php_print("             <input type=\"hidden\" name=\"taxonomy\" value=\"")
        php_print(esc_attr(self.screen.taxonomy))
        php_print("\" />\n              <input type=\"hidden\" name=\"post_type\" value=\"")
        php_print(esc_attr(self.screen.post_type))
        php_print("""\" />
        <br class=\"clear\" />
        <div class=\"notice notice-error notice-alt inline hidden\">
        <p class=\"error\"></p>
        </div>
        </div>
        </td></tr>
        </tbody></table>
        </form>
        """)
    # end def inline_edit
# end class WP_Terms_List_Table
