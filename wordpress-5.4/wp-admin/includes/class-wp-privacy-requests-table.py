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
#// List Table API: WP_Privacy_Requests_Table class
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 4.9.6
#//
class WP_Privacy_Requests_Table(WP_List_Table):
    request_type = "INVALID"
    post_type = "INVALID"
    #// 
    #// Get columns to show in the list table.
    #// 
    #// @since 4.9.6
    #// 
    #// @return string[] Array of column titles keyed by their column name.
    #//
    def get_columns(self):
        
        columns = Array({"cb": "<input type=\"checkbox\" />", "email": __("Requester"), "status": __("Status"), "created_timestamp": __("Requested"), "next_steps": __("Next Steps")})
        return columns
    # end def get_columns
    #// 
    #// Normalize the admin URL to the current page (by request_type).
    #// 
    #// @since 5.3.0
    #// 
    #// @return string URL to the current admin page.
    #//
    def get_admin_url(self):
        
        pagenow = php_str_replace("_", "-", self.request_type)
        if "remove-personal-data" == pagenow:
            pagenow = "erase-personal-data"
        # end if
        return admin_url(pagenow + ".php")
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
        desc_first = (php_isset(lambda : PHP_REQUEST["orderby"]))
        return Array({"email": "requester", "created_timestamp": Array("requested", desc_first)})
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
        
        global wpdb
        php_check_if_defined("wpdb")
        cache_key = self.post_type + "-" + self.request_type
        counts = wp_cache_get(cache_key, "counts")
        if False != counts:
            return counts
        # end if
        query = str("\n         SELECT post_status, COUNT( * ) AS num_posts\n           FROM ") + str(wpdb.posts) + str("""\n           WHERE post_type = %s\n          AND post_name = %s\n            GROUP BY post_status""")
        results = wpdb.get_results(wpdb.prepare(query, self.post_type, self.request_type), ARRAY_A)
        counts = php_array_fill_keys(get_post_stati(), 0)
        for row in results:
            counts[row["post_status"]] = row["num_posts"]
        # end for
        counts = counts
        wp_cache_set(cache_key, counts, "counts")
        return counts
    # end def get_request_counts
    #// 
    #// Get an associative array ( id => link ) with the list of views available on this table.
    #// 
    #// @since 4.9.6
    #// 
    #// @return string[] An array of HTML links keyed by their view.
    #//
    def get_views(self):
        
        current_status = sanitize_text_field(PHP_REQUEST["filter-status"]) if (php_isset(lambda : PHP_REQUEST["filter-status"])) else ""
        statuses = _wp_privacy_statuses()
        views = Array()
        counts = self.get_request_counts()
        total_requests = absint(array_sum(counts))
        #// Normalized admin URL.
        admin_url = self.get_admin_url()
        current_link_attributes = " class=\"current\" aria-current=\"page\"" if php_empty(lambda : current_status) else ""
        status_label = php_sprintf(_nx("All <span class=\"count\">(%s)</span>", "All <span class=\"count\">(%s)</span>", total_requests, "requests"), number_format_i18n(total_requests))
        views["all"] = php_sprintf("<a href=\"%s\"%s>%s</a>", esc_url(admin_url), current_link_attributes, status_label)
        for status,label in statuses:
            post_status = get_post_status_object(status)
            if (not post_status):
                continue
            # end if
            current_link_attributes = " class=\"current\" aria-current=\"page\"" if status == current_status else ""
            total_status_requests = absint(counts.status)
            status_label = php_sprintf(translate_nooped_plural(post_status.label_count, total_status_requests), number_format_i18n(total_status_requests))
            status_link = add_query_arg("filter-status", status, admin_url)
            views[status] = php_sprintf("<a href=\"%s\"%s>%s</a>", esc_url(status_link), current_link_attributes, status_label)
        # end for
        return views
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
        
        action = self.current_action()
        request_ids = wp_parse_id_list(wp_unslash(PHP_REQUEST["request_id"])) if (php_isset(lambda : PHP_REQUEST["request_id"])) else Array()
        count = 0
        if request_ids:
            check_admin_referer("bulk-privacy_requests")
        # end if
        for case in Switch(action):
            if case("delete"):
                for request_id in request_ids:
                    if wp_delete_post(request_id, True):
                        count += 1
                    # end if
                # end for
                add_settings_error("bulk_action", "bulk_action", php_sprintf(_n("Deleted %d request", "Deleted %d requests", count), count), "success")
                break
            # end if
            if case("resend"):
                for request_id in request_ids:
                    resend = _wp_privacy_resend_request(request_id)
                    if resend and (not is_wp_error(resend)):
                        count += 1
                    # end if
                # end for
                add_settings_error("bulk_action", "bulk_action", php_sprintf(_n("Re-sent %d request", "Re-sent %d requests", count), count), "success")
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
        posts_per_page = self.get_items_per_page(self.request_type + "_requests_per_page")
        args = Array({"post_type": self.post_type, "post_name__in": Array(self.request_type), "posts_per_page": posts_per_page, "offset": php_max(0, absint(PHP_REQUEST["paged"]) - 1) * posts_per_page if (php_isset(lambda : PHP_REQUEST["paged"])) else 0, "post_status": "any", "s": sanitize_text_field(PHP_REQUEST["s"]) if (php_isset(lambda : PHP_REQUEST["s"])) else ""})
        orderby_mapping = Array({"requester": "post_title", "requested": "post_date"})
        if (php_isset(lambda : PHP_REQUEST["orderby"])) and (php_isset(lambda : orderby_mapping[PHP_REQUEST["orderby"]])):
            args["orderby"] = orderby_mapping[PHP_REQUEST["orderby"]]
        # end if
        if (php_isset(lambda : PHP_REQUEST["order"])) and php_in_array(php_strtoupper(PHP_REQUEST["order"]), Array("ASC", "DESC"), True):
            args["order"] = php_strtoupper(PHP_REQUEST["order"])
        # end if
        if (not php_empty(lambda : PHP_REQUEST["filter-status"])):
            filter_status = sanitize_text_field(PHP_REQUEST["filter-status"]) if (php_isset(lambda : PHP_REQUEST["filter-status"])) else ""
            args["post_status"] = filter_status
        # end if
        requests_query = php_new_class("WP_Query", lambda : WP_Query(args))
        requests = requests_query.posts
        for request in requests:
            self.items[-1] = wp_get_user_request(request.ID)
        # end for
        self.items = php_array_filter(self.items)
        self.set_pagination_args(Array({"total_items": requests_query.found_posts, "per_page": posts_per_page}))
    # end def prepare_items
    #// 
    #// Checkbox column.
    #// 
    #// @since 4.9.6
    #// 
    #// @param WP_User_Request $item Item being shown.
    #// @return string Checkbox column markup.
    #//
    def column_cb(self, item=None):
        
        return php_sprintf("<input type=\"checkbox\" name=\"request_id[]\" value=\"%1$s\" /><span class=\"spinner\"></span>", esc_attr(item.ID))
    # end def column_cb
    #// 
    #// Status column.
    #// 
    #// @since 4.9.6
    #// 
    #// @param WP_User_Request $item Item being shown.
    #// @return string Status column markup.
    #//
    def column_status(self, item=None):
        
        status = get_post_status(item.ID)
        status_object = get_post_status_object(status)
        if (not status_object) or php_empty(lambda : status_object.label):
            return "-"
        # end if
        timestamp = False
        for case in Switch(status):
            if case("request-confirmed"):
                timestamp = item.confirmed_timestamp
                break
            # end if
            if case("request-completed"):
                timestamp = item.completed_timestamp
                break
            # end if
        # end for
        php_print("<span class=\"status-label status-" + esc_attr(status) + "\">")
        php_print(esc_html(status_object.label))
        if timestamp:
            php_print(" (" + self.get_timestamp_as_date(timestamp) + ")")
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
    def get_timestamp_as_date(self, timestamp=None):
        
        if php_empty(lambda : timestamp):
            return ""
        # end if
        time_diff = time() - timestamp
        if time_diff >= 0 and time_diff < DAY_IN_SECONDS:
            #// translators: %s: Human-readable time difference.
            return php_sprintf(__("%s ago"), human_time_diff(timestamp))
        # end if
        return date_i18n(get_option("date_format"), timestamp)
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
    def column_default(self, item=None, column_name=None):
        
        cell_value = item.column_name
        if php_in_array(column_name, Array("created_timestamp"), True):
            return self.get_timestamp_as_date(cell_value)
        # end if
        return cell_value
    # end def column_default
    #// 
    #// Actions column. Overridden by children.
    #// 
    #// @since 4.9.6
    #// 
    #// @param WP_User_Request $item Item being shown.
    #// @return string Email column markup.
    #//
    def column_email(self, item=None):
        
        return php_sprintf("<a href=\"%1$s\">%2$s</a> %3$s", esc_url("mailto:" + item.email), item.email, self.row_actions(Array()))
    # end def column_email
    #// 
    #// Next steps column. Overridden by children.
    #// 
    #// @since 4.9.6
    #// 
    #// @param WP_User_Request $item Item being shown.
    #//
    def column_next_steps(self, item=None):
        
        pass
    # end def column_next_steps
    #// 
    #// Generates content for a single row of the table,
    #// 
    #// @since 4.9.6
    #// 
    #// @param WP_User_Request $item The current item.
    #//
    def single_row(self, item=None):
        
        status = item.status
        php_print("<tr id=\"request-" + esc_attr(item.ID) + "\" class=\"status-" + esc_attr(status) + "\">")
        self.single_row_columns(item)
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
