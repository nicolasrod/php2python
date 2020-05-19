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
#// List Table API: WP_Privacy_Requests_Table class
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 4.9.6
#//
class WP_Privacy_Requests_Table(WP_List_Table):
    #// 
    #// Action name for the requests this table will work with. Classes
    #// which inherit from WP_Privacy_Requests_Table should define this.
    #// 
    #// Example: 'export_personal_data'.
    #// 
    #// @since 4.9.6
    #// 
    #// @var string $request_type Name of action.
    #//
    request_type = "INVALID"
    #// 
    #// Post type to be used.
    #// 
    #// @since 4.9.6
    #// 
    #// @var string $post_type The post type.
    #//
    post_type = "INVALID"
    #// 
    #// Get columns to show in the list table.
    #// 
    #// @since 4.9.6
    #// 
    #// @return string[] Array of column titles keyed by their column name.
    #//
    def get_columns(self):
        
        
        columns_ = Array({"cb": "<input type=\"checkbox\" />", "email": __("Requester"), "status": __("Status"), "created_timestamp": __("Requested"), "next_steps": __("Next Steps")})
        return columns_
    # end def get_columns
    #// 
    #// Normalize the admin URL to the current page (by request_type).
    #// 
    #// @since 5.3.0
    #// 
    #// @return string URL to the current admin page.
    #//
    def get_admin_url(self):
        
        
        pagenow_ = php_str_replace("_", "-", self.request_type)
        if "remove-personal-data" == pagenow_:
            pagenow_ = "erase-personal-data"
        # end if
        return admin_url(pagenow_ + ".php")
    # end def get_admin_url
    #// 
    #// Get a list of sortable columns.
    #// 
    #// @since 4.9.6
    #// 
    #// @return array Default sortable columns.
    #//
    def get_sortable_columns(self):
        
        
        #// 
        #// The initial sorting is by 'Requested' (post_date) and descending.
        #// With initial sorting, the first click on 'Requested' should be ascending.
        #// With 'Requester' sorting active, the next click on 'Requested' should be descending.
        #//
        desc_first_ = (php_isset(lambda : PHP_REQUEST["orderby"]))
        return Array({"email": "requester", "created_timestamp": Array("requested", desc_first_)})
    # end def get_sortable_columns
    #// 
    #// Default primary column.
    #// 
    #// @since 4.9.6
    #// 
    #// @return string Default primary column name.
    #//
    def get_default_primary_column_name(self):
        
        
        return "email"
    # end def get_default_primary_column_name
    #// 
    #// Count number of requests for each status.
    #// 
    #// @since 4.9.6
    #// 
    #// @return object Number of posts for each status.
    #//
    def get_request_counts(self):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        cache_key_ = self.post_type + "-" + self.request_type
        counts_ = wp_cache_get(cache_key_, "counts")
        if False != counts_:
            return counts_
        # end if
        query_ = str("\n            SELECT post_status, COUNT( * ) AS num_posts\n           FROM ") + str(wpdb_.posts) + str("""\n          WHERE post_type = %s\n          AND post_name = %s\n            GROUP BY post_status""")
        results_ = wpdb_.get_results(wpdb_.prepare(query_, self.post_type, self.request_type), ARRAY_A)
        counts_ = php_array_fill_keys(get_post_stati(), 0)
        for row_ in results_:
            counts_[row_["post_status"]] = row_["num_posts"]
        # end for
        counts_ = counts_
        wp_cache_set(cache_key_, counts_, "counts")
        return counts_
    # end def get_request_counts
    #// 
    #// Get an associative array ( id => link ) with the list of views available on this table.
    #// 
    #// @since 4.9.6
    #// 
    #// @return string[] An array of HTML links keyed by their view.
    #//
    def get_views(self):
        
        
        current_status_ = sanitize_text_field(PHP_REQUEST["filter-status"]) if (php_isset(lambda : PHP_REQUEST["filter-status"])) else ""
        statuses_ = _wp_privacy_statuses()
        views_ = Array()
        counts_ = self.get_request_counts()
        total_requests_ = absint(array_sum(counts_))
        #// Normalized admin URL.
        admin_url_ = self.get_admin_url()
        current_link_attributes_ = " class=\"current\" aria-current=\"page\"" if php_empty(lambda : current_status_) else ""
        status_label_ = php_sprintf(_nx("All <span class=\"count\">(%s)</span>", "All <span class=\"count\">(%s)</span>", total_requests_, "requests"), number_format_i18n(total_requests_))
        views_["all"] = php_sprintf("<a href=\"%s\"%s>%s</a>", esc_url(admin_url_), current_link_attributes_, status_label_)
        for status_,label_ in statuses_.items():
            post_status_ = get_post_status_object(status_)
            if (not post_status_):
                continue
            # end if
            current_link_attributes_ = " class=\"current\" aria-current=\"page\"" if status_ == current_status_ else ""
            total_status_requests_ = absint(counts_.status_)
            status_label_ = php_sprintf(translate_nooped_plural(post_status_.label_count, total_status_requests_), number_format_i18n(total_status_requests_))
            status_link_ = add_query_arg("filter-status", status_, admin_url_)
            views_[status_] = php_sprintf("<a href=\"%s\"%s>%s</a>", esc_url(status_link_), current_link_attributes_, status_label_)
        # end for
        return views_
    # end def get_views
    #// 
    #// Get bulk actions.
    #// 
    #// @since 4.9.6
    #// 
    #// @return string[] Array of bulk action labels keyed by their action.
    #//
    def get_bulk_actions(self):
        
        
        return Array({"delete": __("Delete Requests"), "resend": __("Resend Confirmation Requests")})
    # end def get_bulk_actions
    #// 
    #// Process bulk actions.
    #// 
    #// @since 4.9.6
    #//
    def process_bulk_action(self):
        
        
        action_ = self.current_action()
        request_ids_ = wp_parse_id_list(wp_unslash(PHP_REQUEST["request_id"])) if (php_isset(lambda : PHP_REQUEST["request_id"])) else Array()
        count_ = 0
        if request_ids_:
            check_admin_referer("bulk-privacy_requests")
        # end if
        for case in Switch(action_):
            if case("delete"):
                for request_id_ in request_ids_:
                    if wp_delete_post(request_id_, True):
                        count_ += 1
                    # end if
                # end for
                add_settings_error("bulk_action", "bulk_action", php_sprintf(_n("Deleted %d request", "Deleted %d requests", count_), count_), "success")
                break
            # end if
            if case("resend"):
                for request_id_ in request_ids_:
                    resend_ = _wp_privacy_resend_request(request_id_)
                    if resend_ and (not is_wp_error(resend_)):
                        count_ += 1
                    # end if
                # end for
                add_settings_error("bulk_action", "bulk_action", php_sprintf(_n("Re-sent %d request", "Re-sent %d requests", count_), count_), "success")
                break
            # end if
        # end for
    # end def process_bulk_action
    #// 
    #// Prepare items to output.
    #// 
    #// @since 4.9.6
    #// @since 5.1.0 Added support for column sorting.
    #//
    def prepare_items(self):
        
        
        self.items = Array()
        posts_per_page_ = self.get_items_per_page(self.request_type + "_requests_per_page")
        args_ = Array({"post_type": self.post_type, "post_name__in": Array(self.request_type), "posts_per_page": posts_per_page_, "offset": php_max(0, absint(PHP_REQUEST["paged"]) - 1) * posts_per_page_ if (php_isset(lambda : PHP_REQUEST["paged"])) else 0, "post_status": "any", "s": sanitize_text_field(PHP_REQUEST["s"]) if (php_isset(lambda : PHP_REQUEST["s"])) else ""})
        orderby_mapping_ = Array({"requester": "post_title", "requested": "post_date"})
        if (php_isset(lambda : PHP_REQUEST["orderby"])) and (php_isset(lambda : orderby_mapping_[PHP_REQUEST["orderby"]])):
            args_["orderby"] = orderby_mapping_[PHP_REQUEST["orderby"]]
        # end if
        if (php_isset(lambda : PHP_REQUEST["order"])) and php_in_array(php_strtoupper(PHP_REQUEST["order"]), Array("ASC", "DESC"), True):
            args_["order"] = php_strtoupper(PHP_REQUEST["order"])
        # end if
        if (not php_empty(lambda : PHP_REQUEST["filter-status"])):
            filter_status_ = sanitize_text_field(PHP_REQUEST["filter-status"]) if (php_isset(lambda : PHP_REQUEST["filter-status"])) else ""
            args_["post_status"] = filter_status_
        # end if
        requests_query_ = php_new_class("WP_Query", lambda : WP_Query(args_))
        requests_ = requests_query_.posts
        for request_ in requests_:
            self.items[-1] = wp_get_user_request(request_.ID)
        # end for
        self.items = php_array_filter(self.items)
        self.set_pagination_args(Array({"total_items": requests_query_.found_posts, "per_page": posts_per_page_}))
    # end def prepare_items
    #// 
    #// Checkbox column.
    #// 
    #// @since 4.9.6
    #// 
    #// @param WP_User_Request $item Item being shown.
    #// @return string Checkbox column markup.
    #//
    def column_cb(self, item_=None):
        
        
        return php_sprintf("<input type=\"checkbox\" name=\"request_id[]\" value=\"%1$s\" /><span class=\"spinner\"></span>", esc_attr(item_.ID))
    # end def column_cb
    #// 
    #// Status column.
    #// 
    #// @since 4.9.6
    #// 
    #// @param WP_User_Request $item Item being shown.
    #// @return string Status column markup.
    #//
    def column_status(self, item_=None):
        
        
        status_ = get_post_status(item_.ID)
        status_object_ = get_post_status_object(status_)
        if (not status_object_) or php_empty(lambda : status_object_.label):
            return "-"
        # end if
        timestamp_ = False
        for case in Switch(status_):
            if case("request-confirmed"):
                timestamp_ = item_.confirmed_timestamp
                break
            # end if
            if case("request-completed"):
                timestamp_ = item_.completed_timestamp
                break
            # end if
        # end for
        php_print("<span class=\"status-label status-" + esc_attr(status_) + "\">")
        php_print(esc_html(status_object_.label))
        if timestamp_:
            php_print(" (" + self.get_timestamp_as_date(timestamp_) + ")")
        # end if
        php_print("</span>")
    # end def column_status
    #// 
    #// Convert timestamp for display.
    #// 
    #// @since 4.9.6
    #// 
    #// @param int $timestamp Event timestamp.
    #// @return string Human readable date.
    #//
    def get_timestamp_as_date(self, timestamp_=None):
        
        
        if php_empty(lambda : timestamp_):
            return ""
        # end if
        time_diff_ = time() - timestamp_
        if time_diff_ >= 0 and time_diff_ < DAY_IN_SECONDS:
            #// translators: %s: Human-readable time difference.
            return php_sprintf(__("%s ago"), human_time_diff(timestamp_))
        # end if
        return date_i18n(get_option("date_format"), timestamp_)
    # end def get_timestamp_as_date
    #// 
    #// Default column handler.
    #// 
    #// @since 4.9.6
    #// 
    #// @param WP_User_Request $item        Item being shown.
    #// @param string          $column_name Name of column being shown.
    #// @return string Default column output.
    #//
    def column_default(self, item_=None, column_name_=None):
        
        
        cell_value_ = item_.column_name_
        if php_in_array(column_name_, Array("created_timestamp"), True):
            return self.get_timestamp_as_date(cell_value_)
        # end if
        return cell_value_
    # end def column_default
    #// 
    #// Actions column. Overridden by children.
    #// 
    #// @since 4.9.6
    #// 
    #// @param WP_User_Request $item Item being shown.
    #// @return string Email column markup.
    #//
    def column_email(self, item_=None):
        
        
        return php_sprintf("<a href=\"%1$s\">%2$s</a> %3$s", esc_url("mailto:" + item_.email), item_.email, self.row_actions(Array()))
    # end def column_email
    #// 
    #// Next steps column. Overridden by children.
    #// 
    #// @since 4.9.6
    #// 
    #// @param WP_User_Request $item Item being shown.
    #//
    def column_next_steps(self, item_=None):
        
        
        pass
    # end def column_next_steps
    #// 
    #// Generates content for a single row of the table,
    #// 
    #// @since 4.9.6
    #// 
    #// @param WP_User_Request $item The current item.
    #//
    def single_row(self, item_=None):
        
        
        status_ = item_.status
        php_print("<tr id=\"request-" + esc_attr(item_.ID) + "\" class=\"status-" + esc_attr(status_) + "\">")
        self.single_row_columns(item_)
        php_print("</tr>")
    # end def single_row
    #// 
    #// Embed scripts used to perform actions. Overridden by children.
    #// 
    #// @since 4.9.6
    #//
    def embed_scripts(self):
        
        
        pass
    # end def embed_scripts
# end class WP_Privacy_Requests_Table
