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
#// Class for generating SQL clauses that filter a primary query according to date.
#// 
#// WP_Date_Query is a helper that allows primary query classes, such as WP_Query, to filter
#// their results by date columns, by generating `WHERE` subclauses to be attached to the
#// primary SQL query string.
#// 
#// Attempting to filter by an invalid date value (eg month=13) will generate SQL that will
#// return no results. In these cases, a _doing_it_wrong() error notice is also thrown.
#// See WP_Date_Query::validate_date_values().
#// 
#// @link https://developer.wordpress.org/reference/classes/wp_query
#// 
#// @since 3.7.0
#//
class WP_Date_Query():
    queries = Array()
    relation = "AND"
    column = "post_date"
    compare = "="
    time_keys = Array("after", "before", "year", "month", "monthnum", "week", "w", "dayofyear", "day", "dayofweek", "dayofweek_iso", "hour", "minute", "second")
    #// 
    #// Constructor.
    #// 
    #// Time-related parameters that normally require integer values ('year', 'month', 'week', 'dayofyear', 'day',
    #// 'dayofweek', 'dayofweek_iso', 'hour', 'minute', 'second') accept arrays of integers for some values of
    #// 'compare'. When 'compare' is 'IN' or 'NOT IN', arrays are accepted; when 'compare' is 'BETWEEN' or 'NOT
    #// BETWEEN', arrays of two valid values are required. See individual argument descriptions for accepted values.
    #// 
    #// @since 3.7.0
    #// @since 4.0.0 The $inclusive logic was updated to include all times within the date range.
    #// @since 4.1.0 Introduced 'dayofweek_iso' time type parameter.
    #// 
    #// @param array $date_query {
    #// Array of date query clauses.
    #// 
    #// @type array {
    #// @type string $column   Optional. The column to query against. If undefined, inherits the value of
    #// the `$default_column` parameter. Accepts 'post_date', 'post_date_gmt',
    #// 'post_modified','post_modified_gmt', 'comment_date', 'comment_date_gmt'.
    #// Default 'post_date'.
    #// @type string $compare  Optional. The comparison operator. Accepts '=', '!=', '>', '>=', '<', '<=',
    #// 'IN', 'NOT IN', 'BETWEEN', 'NOT BETWEEN'. Default '='.
    #// @type string $relation Optional. The boolean relationship between the date queries. Accepts 'OR' or 'AND'.
    #// Default 'OR'.
    #// @type array {
    #// Optional. An array of first-order clause parameters, or another fully-formed date query.
    #// 
    #// @type string|array $before {
    #// Optional. Date to retrieve posts before. Accepts `strtotime()`-compatible string,
    #// or array of 'year', 'month', 'day' values.
    #// 
    #// @type string $year  The four-digit year. Default empty. Accepts any four-digit year.
    #// @type string $month Optional when passing array.The month of the year.
    #// Default (string:empty)|(array:1). Accepts numbers 1-12.
    #// @type string $day   Optional when passing array.The day of the month.
    #// Default (string:empty)|(array:1). Accepts numbers 1-31.
    #// }
    #// @type string|array $after {
    #// Optional. Date to retrieve posts after. Accepts `strtotime()`-compatible string,
    #// or array of 'year', 'month', 'day' values.
    #// 
    #// @type string $year  The four-digit year. Accepts any four-digit year. Default empty.
    #// @type string $month Optional when passing array. The month of the year. Accepts numbers 1-12.
    #// Default (string:empty)|(array:12).
    #// @type string $day   Optional when passing array.The day of the month. Accepts numbers 1-31.
    #// Default (string:empty)|(array:last day of month).
    #// }
    #// @type string       $column        Optional. Used to add a clause comparing a column other than the
    #// column specified in the top-level `$column` parameter. Accepts
    #// 'post_date', 'post_date_gmt', 'post_modified', 'post_modified_gmt',
    #// 'comment_date', 'comment_date_gmt'. Default is the value of
    #// top-level `$column`.
    #// @type string       $compare       Optional. The comparison operator. Accepts '=', '!=', '>', '>=',
    #// '<', '<=', 'IN', 'NOT IN', 'BETWEEN', 'NOT BETWEEN'. 'IN',
    #// 'NOT IN', 'BETWEEN', and 'NOT BETWEEN'. Comparisons support
    #// arrays in some time-related parameters. Default '='.
    #// @type bool         $inclusive     Optional. Include results from dates specified in 'before' or
    #// 'after'. Default false.
    #// @type int|array    $year          Optional. The four-digit year number. Accepts any four-digit year
    #// or an array of years if `$compare` supports it. Default empty.
    #// @type int|array    $month         Optional. The two-digit month number. Accepts numbers 1-12 or an
    #// array of valid numbers if `$compare` supports it. Default empty.
    #// @type int|array    $week          Optional. The week number of the year. Accepts numbers 0-53 or an
    #// array of valid numbers if `$compare` supports it. Default empty.
    #// @type int|array    $dayofyear     Optional. The day number of the year. Accepts numbers 1-366 or an
    #// array of valid numbers if `$compare` supports it.
    #// @type int|array    $day           Optional. The day of the month. Accepts numbers 1-31 or an array
    #// of valid numbers if `$compare` supports it. Default empty.
    #// @type int|array    $dayofweek     Optional. The day number of the week. Accepts numbers 1-7 (1 is
    #// Sunday) or an array of valid numbers if `$compare` supports it.
    #// Default empty.
    #// @type int|array    $dayofweek_iso Optional. The day number of the week (ISO). Accepts numbers 1-7
    #// (1 is Monday) or an array of valid numbers if `$compare` supports it.
    #// Default empty.
    #// @type int|array    $hour          Optional. The hour of the day. Accepts numbers 0-23 or an array
    #// of valid numbers if `$compare` supports it. Default empty.
    #// @type int|array    $minute        Optional. The minute of the hour. Accepts numbers 0-60 or an array
    #// of valid numbers if `$compare` supports it. Default empty.
    #// @type int|array    $second        Optional. The second of the minute. Accepts numbers 0-60 or an
    #// array of valid numbers if `$compare` supports it. Default empty.
    #// }
    #// }
    #// }
    #// @param string $default_column Optional. Default column to query against. Default 'post_date'.
    #// Accepts 'post_date', 'post_date_gmt', 'post_modified', 'post_modified_gmt',
    #// 'comment_date', 'comment_date_gmt'.
    #//
    def __init__(self, date_query=None, default_column="post_date"):
        
        if php_empty(lambda : date_query) or (not php_is_array(date_query)):
            return
        # end if
        if (php_isset(lambda : date_query["relation"])) and "OR" == php_strtoupper(date_query["relation"]):
            self.relation = "OR"
        else:
            self.relation = "AND"
        # end if
        #// Support for passing time-based keys in the top level of the $date_query array.
        if (not (php_isset(lambda : date_query[0]))):
            date_query = Array(date_query)
        # end if
        if (not php_empty(lambda : date_query["column"])):
            date_query["column"] = esc_sql(date_query["column"])
        else:
            date_query["column"] = esc_sql(default_column)
        # end if
        self.column = self.validate_column(self.column)
        self.compare = self.get_compare(date_query)
        self.queries = self.sanitize_query(date_query)
    # end def __init__
    #// 
    #// Recursive-friendly query sanitizer.
    #// 
    #// Ensures that each query-level clause has a 'relation' key, and that
    #// each first-order clause contains all the necessary keys from
    #// `$defaults`.
    #// 
    #// @since 4.1.0
    #// 
    #// @param array $queries
    #// @param array $parent_query
    #// 
    #// @return array Sanitized queries.
    #//
    def sanitize_query(self, queries=None, parent_query=None):
        
        cleaned_query = Array()
        defaults = Array({"column": "post_date", "compare": "=", "relation": "AND"})
        #// Numeric keys should always have array values.
        for qkey,qvalue in queries:
            if php_is_numeric(qkey) and (not php_is_array(qvalue)):
                queries[qkey] = None
            # end if
        # end for
        #// Each query should have a value for each default key. Inherit from the parent when possible.
        for dkey,dvalue in defaults:
            if (php_isset(lambda : queries[dkey])):
                continue
            # end if
            if (php_isset(lambda : parent_query[dkey])):
                queries[dkey] = parent_query[dkey]
            else:
                queries[dkey] = dvalue
            # end if
        # end for
        #// Validate the dates passed in the query.
        if self.is_first_order_clause(queries):
            self.validate_date_values(queries)
        # end if
        for key,q in queries:
            if (not php_is_array(q)) or php_in_array(key, self.time_keys, True):
                #// This is a first-order query. Trust the values and sanitize when building SQL.
                cleaned_query[key] = q
            else:
                #// Any array without a time key is another query, so we recurse.
                cleaned_query[-1] = self.sanitize_query(q, queries)
            # end if
        # end for
        return cleaned_query
    # end def sanitize_query
    #// 
    #// Determine whether this is a first-order clause.
    #// 
    #// Checks to see if the current clause has any time-related keys.
    #// If so, it's first-order.
    #// 
    #// @since 4.1.0
    #// 
    #// @param  array $query Query clause.
    #// @return bool True if this is a first-order clause.
    #//
    def is_first_order_clause(self, query=None):
        
        time_keys = php_array_intersect(self.time_keys, php_array_keys(query))
        return (not php_empty(lambda : time_keys))
    # end def is_first_order_clause
    #// 
    #// Determines and validates what comparison operator to use.
    #// 
    #// @since 3.7.0
    #// 
    #// @param array $query A date query or a date subquery.
    #// @return string The comparison operator.
    #//
    def get_compare(self, query=None):
        
        if (not php_empty(lambda : query["compare"])) and php_in_array(query["compare"], Array("=", "!=", ">", ">=", "<", "<=", "IN", "NOT IN", "BETWEEN", "NOT BETWEEN")):
            return php_strtoupper(query["compare"])
        # end if
        return self.compare
    # end def get_compare
    #// 
    #// Validates the given date_query values and triggers errors if something is not valid.
    #// 
    #// Note that date queries with invalid date ranges are allowed to
    #// continue (though of course no items will be found for impossible dates).
    #// This method only generates debug notices for these cases.
    #// 
    #// @since 4.1.0
    #// 
    #// @param  array $date_query The date_query array.
    #// @return bool  True if all values in the query are valid, false if one or more fail.
    #//
    def validate_date_values(self, date_query=Array()):
        
        if php_empty(lambda : date_query):
            return False
        # end if
        valid = True
        #// 
        #// Validate 'before' and 'after' up front, then let the
        #// validation routine continue to be sure that all invalid
        #// values generate errors too.
        #//
        if php_array_key_exists("before", date_query) and php_is_array(date_query["before"]):
            valid = self.validate_date_values(date_query["before"])
        # end if
        if php_array_key_exists("after", date_query) and php_is_array(date_query["after"]):
            valid = self.validate_date_values(date_query["after"])
        # end if
        #// Array containing all min-max checks.
        min_max_checks = Array()
        #// Days per year.
        if php_array_key_exists("year", date_query):
            #// 
            #// If a year exists in the date query, we can use it to get the days.
            #// If multiple years are provided (as in a BETWEEN), use the first one.
            #//
            if php_is_array(date_query["year"]):
                _year = reset(date_query["year"])
            else:
                _year = date_query["year"]
            # end if
            max_days_of_year = gmdate("z", mktime(0, 0, 0, 12, 31, _year)) + 1
        else:
            #// Otherwise we use the max of 366 (leap-year).
            max_days_of_year = 366
        # end if
        min_max_checks["dayofyear"] = Array({"min": 1, "max": max_days_of_year})
        #// Days per week.
        min_max_checks["dayofweek"] = Array({"min": 1, "max": 7})
        #// Days per week.
        min_max_checks["dayofweek_iso"] = Array({"min": 1, "max": 7})
        #// Months per year.
        min_max_checks["month"] = Array({"min": 1, "max": 12})
        #// Weeks per year.
        if (php_isset(lambda : _year)):
            #// 
            #// If we have a specific year, use it to calculate number of weeks.
            #// Note: the number of weeks in a year is the date in which Dec 28 appears.
            #//
            week_count = gmdate("W", mktime(0, 0, 0, 12, 28, _year))
        else:
            #// Otherwise set the week-count to a maximum of 53.
            week_count = 53
        # end if
        min_max_checks["week"] = Array({"min": 1, "max": week_count})
        #// Days per month.
        min_max_checks["day"] = Array({"min": 1, "max": 31})
        #// Hours per day.
        min_max_checks["hour"] = Array({"min": 0, "max": 23})
        #// Minutes per hour.
        min_max_checks["minute"] = Array({"min": 0, "max": 59})
        #// Seconds per minute.
        min_max_checks["second"] = Array({"min": 0, "max": 59})
        #// Concatenate and throw a notice for each invalid value.
        for key,check in min_max_checks:
            if (not php_array_key_exists(key, date_query)):
                continue
            # end if
            #// Throw a notice for each failing value.
            for _value in date_query[key]:
                is_between = _value >= check["min"] and _value <= check["max"]
                if (not php_is_numeric(_value)) or (not is_between):
                    error = php_sprintf(__("Invalid value %1$s for %2$s. Expected value should be between %3$s and %4$s."), "<code>" + esc_html(_value) + "</code>", "<code>" + esc_html(key) + "</code>", "<code>" + esc_html(check["min"]) + "</code>", "<code>" + esc_html(check["max"]) + "</code>")
                    _doing_it_wrong(__CLASS__, error, "4.1.0")
                    valid = False
                # end if
            # end for
        # end for
        #// If we already have invalid date messages, don't bother running through checkdate().
        if (not valid):
            return valid
        # end if
        day_month_year_error_msg = ""
        day_exists = php_array_key_exists("day", date_query) and php_is_numeric(date_query["day"])
        month_exists = php_array_key_exists("month", date_query) and php_is_numeric(date_query["month"])
        year_exists = php_array_key_exists("year", date_query) and php_is_numeric(date_query["year"])
        if day_exists and month_exists and year_exists:
            #// 1. Checking day, month, year combination.
            if (not wp_checkdate(date_query["month"], date_query["day"], date_query["year"], php_sprintf("%s-%s-%s", date_query["year"], date_query["month"], date_query["day"]))):
                day_month_year_error_msg = php_sprintf(__("The following values do not describe a valid date: year %1$s, month %2$s, day %3$s."), "<code>" + esc_html(date_query["year"]) + "</code>", "<code>" + esc_html(date_query["month"]) + "</code>", "<code>" + esc_html(date_query["day"]) + "</code>")
                valid = False
            # end if
        elif day_exists and month_exists:
            #// 
            #// 2. checking day, month combination
            #// We use 2012 because, as a leap year, it's the most permissive.
            #//
            if (not wp_checkdate(date_query["month"], date_query["day"], 2012, php_sprintf("2012-%s-%s", date_query["month"], date_query["day"]))):
                day_month_year_error_msg = php_sprintf(__("The following values do not describe a valid date: month %1$s, day %2$s."), "<code>" + esc_html(date_query["month"]) + "</code>", "<code>" + esc_html(date_query["day"]) + "</code>")
                valid = False
            # end if
        # end if
        if (not php_empty(lambda : day_month_year_error_msg)):
            _doing_it_wrong(__CLASS__, day_month_year_error_msg, "4.1.0")
        # end if
        return valid
    # end def validate_date_values
    #// 
    #// Validates a column name parameter.
    #// 
    #// Column names without a table prefix (like 'post_date') are checked against a whitelist of
    #// known tables, and then, if found, have a table prefix (such as 'wp_posts.') prepended.
    #// Prefixed column names (such as 'wp_posts.post_date') bypass this whitelist check,
    #// and are only sanitized to remove illegal characters.
    #// 
    #// @since 3.7.0
    #// 
    #// @param string $column The user-supplied column name.
    #// @return string A validated column name value.
    #//
    def validate_column(self, column=None):
        
        global wpdb
        php_check_if_defined("wpdb")
        valid_columns = Array("post_date", "post_date_gmt", "post_modified", "post_modified_gmt", "comment_date", "comment_date_gmt", "user_registered", "registered", "last_updated")
        #// Attempt to detect a table prefix.
        if False == php_strpos(column, "."):
            #// 
            #// Filters the list of valid date query columns.
            #// 
            #// @since 3.7.0
            #// @since 4.1.0 Added 'user_registered' to the default recognized columns.
            #// 
            #// @param string[] $valid_columns An array of valid date query columns. Defaults
            #// are 'post_date', 'post_date_gmt', 'post_modified',
            #// 'post_modified_gmt', 'comment_date', 'comment_date_gmt',
            #// 'user_registered'
            #//
            if (not php_in_array(column, apply_filters("date_query_valid_columns", valid_columns))):
                column = "post_date"
            # end if
            known_columns = Array({wpdb.posts: Array("post_date", "post_date_gmt", "post_modified", "post_modified_gmt"), wpdb.comments: Array("comment_date", "comment_date_gmt"), wpdb.users: Array("user_registered"), wpdb.blogs: Array("registered", "last_updated")})
            #// If it's a known column name, add the appropriate table prefix.
            for table_name,table_columns in known_columns:
                if php_in_array(column, table_columns):
                    column = table_name + "." + column
                    break
                # end if
            # end for
        # end if
        #// Remove unsafe characters.
        return php_preg_replace("/[^a-zA-Z0-9_$\\.]/", "", column)
    # end def validate_column
    #// 
    #// Generate WHERE clause to be appended to a main query.
    #// 
    #// @since 3.7.0
    #// 
    #// @return string MySQL WHERE clause.
    #//
    def get_sql(self):
        
        sql = self.get_sql_clauses()
        where = sql["where"]
        #// 
        #// Filters the date query WHERE clause.
        #// 
        #// @since 3.7.0
        #// 
        #// @param string        $where WHERE clause of the date query.
        #// @param WP_Date_Query $this  The WP_Date_Query instance.
        #//
        return apply_filters("get_date_sql", where, self)
    # end def get_sql
    #// 
    #// Generate SQL clauses to be appended to a main query.
    #// 
    #// Called by the public WP_Date_Query::get_sql(), this method is abstracted
    #// out to maintain parity with the other Query classes.
    #// 
    #// @since 4.1.0
    #// 
    #// @return array {
    #// Array containing JOIN and WHERE SQL clauses to append to the main query.
    #// 
    #// @type string $join  SQL fragment to append to the main JOIN clause.
    #// @type string $where SQL fragment to append to the main WHERE clause.
    #// }
    #//
    def get_sql_clauses(self):
        
        sql = self.get_sql_for_query(self.queries)
        if (not php_empty(lambda : sql["where"])):
            sql["where"] = " AND " + sql["where"]
        # end if
        return sql
    # end def get_sql_clauses
    #// 
    #// Generate SQL clauses for a single query array.
    #// 
    #// If nested subqueries are found, this method recurses the tree to
    #// produce the properly nested SQL.
    #// 
    #// @since 4.1.0
    #// 
    #// @param array $query Query to parse.
    #// @param int   $depth Optional. Number of tree levels deep we currently are.
    #// Used to calculate indentation. Default 0.
    #// @return array {
    #// Array containing JOIN and WHERE SQL clauses to append to a single query array.
    #// 
    #// @type string $join  SQL fragment to append to the main JOIN clause.
    #// @type string $where SQL fragment to append to the main WHERE clause.
    #// }
    #//
    def get_sql_for_query(self, query=None, depth=0):
        
        sql_chunks = Array({"join": Array(), "where": Array()})
        sql = Array({"join": "", "where": ""})
        indent = ""
        i = 0
        while i < depth:
            
            indent += "  "
            i += 1
        # end while
        for key,clause in query:
            if "relation" == key:
                relation = query["relation"]
            elif php_is_array(clause):
                #// This is a first-order clause.
                if self.is_first_order_clause(clause):
                    clause_sql = self.get_sql_for_clause(clause, query)
                    where_count = php_count(clause_sql["where"])
                    if (not where_count):
                        sql_chunks["where"][-1] = ""
                    elif 1 == where_count:
                        sql_chunks["where"][-1] = clause_sql["where"][0]
                    else:
                        sql_chunks["where"][-1] = "( " + php_implode(" AND ", clause_sql["where"]) + " )"
                    # end if
                    sql_chunks["join"] = php_array_merge(sql_chunks["join"], clause_sql["join"])
                    pass
                else:
                    clause_sql = self.get_sql_for_query(clause, depth + 1)
                    sql_chunks["where"][-1] = clause_sql["where"]
                    sql_chunks["join"][-1] = clause_sql["join"]
                # end if
            # end if
        # end for
        #// Filter to remove empties.
        sql_chunks["join"] = php_array_filter(sql_chunks["join"])
        sql_chunks["where"] = php_array_filter(sql_chunks["where"])
        if php_empty(lambda : relation):
            relation = "AND"
        # end if
        #// Filter duplicate JOIN clauses and combine into a single string.
        if (not php_empty(lambda : sql_chunks["join"])):
            sql["join"] = php_implode(" ", array_unique(sql_chunks["join"]))
        # end if
        #// Generate a single WHERE clause with proper brackets and indentation.
        if (not php_empty(lambda : sql_chunks["where"])):
            sql["where"] = "( " + "\n  " + indent + php_implode(" " + "\n  " + indent + relation + " " + "\n  " + indent, sql_chunks["where"]) + "\n" + indent + ")"
        # end if
        return sql
    # end def get_sql_for_query
    #// 
    #// Turns a single date clause into pieces for a WHERE clause.
    #// 
    #// A wrapper for get_sql_for_clause(), included here for backward
    #// compatibility while retaining the naming convention across Query classes.
    #// 
    #// @since 3.7.0
    #// 
    #// @param  array $query Date query arguments.
    #// @return array {
    #// Array containing JOIN and WHERE SQL clauses to append to the main query.
    #// 
    #// @type string $join  SQL fragment to append to the main JOIN clause.
    #// @type string $where SQL fragment to append to the main WHERE clause.
    #// }
    #//
    def get_sql_for_subquery(self, query=None):
        
        return self.get_sql_for_clause(query, "")
    # end def get_sql_for_subquery
    #// 
    #// Turns a first-order date query into SQL for a WHERE clause.
    #// 
    #// @since 4.1.0
    #// 
    #// @param  array $query        Date query clause.
    #// @param  array $parent_query Parent query of the current date query.
    #// @return array {
    #// Array containing JOIN and WHERE SQL clauses to append to the main query.
    #// 
    #// @type string $join  SQL fragment to append to the main JOIN clause.
    #// @type string $where SQL fragment to append to the main WHERE clause.
    #// }
    #//
    def get_sql_for_clause(self, query=None, parent_query=None):
        
        global wpdb
        php_check_if_defined("wpdb")
        #// The sub-parts of a $where part.
        where_parts = Array()
        column = esc_sql(query["column"]) if (not php_empty(lambda : query["column"])) else self.column
        column = self.validate_column(column)
        compare = self.get_compare(query)
        inclusive = (not php_empty(lambda : query["inclusive"]))
        #// Assign greater- and less-than values.
        lt = "<"
        gt = ">"
        if inclusive:
            lt += "="
            gt += "="
        # end if
        #// Range queries.
        if (not php_empty(lambda : query["after"])):
            where_parts[-1] = wpdb.prepare(str(column) + str(" ") + str(gt) + str(" %s"), self.build_mysql_datetime(query["after"], (not inclusive)))
        # end if
        if (not php_empty(lambda : query["before"])):
            where_parts[-1] = wpdb.prepare(str(column) + str(" ") + str(lt) + str(" %s"), self.build_mysql_datetime(query["before"], inclusive))
        # end if
        #// Specific value queries.
        date_units = Array({"YEAR": Array("year"), "MONTH": Array("month", "monthnum"), "_wp_mysql_week": Array("week", "w"), "DAYOFYEAR": Array("dayofyear"), "DAYOFMONTH": Array("day"), "DAYOFWEEK": Array("dayofweek"), "WEEKDAY": Array("dayofweek_iso")})
        #// Check of the possible date units and add them to the query.
        for sql_part,query_parts in date_units:
            for query_part in query_parts:
                if (php_isset(lambda : query[query_part])):
                    value = self.build_value(compare, query[query_part])
                    if value:
                        for case in Switch(sql_part):
                            if case("_wp_mysql_week"):
                                where_parts[-1] = _wp_mysql_week(column) + str(" ") + str(compare) + str(" ") + str(value)
                                break
                            # end if
                            if case("WEEKDAY"):
                                where_parts[-1] = str(sql_part) + str("( ") + str(column) + str(" ) + 1 ") + str(compare) + str(" ") + str(value)
                                break
                            # end if
                            if case():
                                where_parts[-1] = str(sql_part) + str("( ") + str(column) + str(" ) ") + str(compare) + str(" ") + str(value)
                            # end if
                        # end for
                        break
                    # end if
                # end if
            # end for
        # end for
        if (php_isset(lambda : query["hour"])) or (php_isset(lambda : query["minute"])) or (php_isset(lambda : query["second"])):
            #// Avoid notices.
            for unit in Array("hour", "minute", "second"):
                if (not (php_isset(lambda : query[unit]))):
                    query[unit] = None
                # end if
            # end for
            time_query = self.build_time_query(column, compare, query["hour"], query["minute"], query["second"])
            if time_query:
                where_parts[-1] = time_query
            # end if
        # end if
        #// 
        #// Return an array of 'join' and 'where' for compatibility
        #// with other query classes.
        #//
        return Array({"where": where_parts, "join": Array()})
    # end def get_sql_for_clause
    #// 
    #// Builds and validates a value string based on the comparison operator.
    #// 
    #// @since 3.7.0
    #// 
    #// @param string $compare The compare operator to use
    #// @param string|array $value The value
    #// @return string|false|int The value to be used in SQL or false on error.
    #//
    def build_value(self, compare=None, value=None):
        
        if (not (php_isset(lambda : value))):
            return False
        # end if
        for case in Switch(compare):
            if case("IN"):
                pass
            # end if
            if case("NOT IN"):
                value = value
                #// Remove non-numeric values.
                value = php_array_filter(value, "is_numeric")
                if php_empty(lambda : value):
                    return False
                # end if
                return "(" + php_implode(",", php_array_map("intval", value)) + ")"
            # end if
            if case("BETWEEN"):
                pass
            # end if
            if case("NOT BETWEEN"):
                if (not php_is_array(value)) or 2 != php_count(value):
                    value = Array(value, value)
                else:
                    value = php_array_values(value)
                # end if
                #// If either value is non-numeric, bail.
                for v in value:
                    if (not php_is_numeric(v)):
                        return False
                    # end if
                # end for
                value = php_array_map("intval", value)
                return value[0] + " AND " + value[1]
            # end if
            if case():
                if (not php_is_numeric(value)):
                    return False
                # end if
                return php_int(value)
            # end if
        # end for
    # end def build_value
    #// 
    #// Builds a MySQL format date/time based on some query parameters.
    #// 
    #// You can pass an array of values (year, month, etc.) with missing parameter values being defaulted to
    #// either the maximum or minimum values (controlled by the $default_to parameter). Alternatively you can
    #// pass a string that will be passed to date_create().
    #// 
    #// @since 3.7.0
    #// 
    #// @param string|array $datetime       An array of parameters or a strotime() string
    #// @param bool         $default_to_max Whether to round up incomplete dates. Supported by values
    #// of $datetime that are arrays, or string values that are a
    #// subset of MySQL date format ('Y', 'Y-m', 'Y-m-d', 'Y-m-d H:i').
    #// Default: false.
    #// @return string|false A MySQL format date/time or false on failure
    #//
    def build_mysql_datetime(self, datetime=None, default_to_max=False):
        
        if (not php_is_array(datetime)):
            #// 
            #// Try to parse some common date formats, so we can detect
            #// the level of precision and support the 'inclusive' parameter.
            #//
            if php_preg_match("/^(\\d{4})$/", datetime, matches):
                #// Y
                datetime = Array({"year": php_intval(matches[1])})
            elif php_preg_match("/^(\\d{4})\\-(\\d{2})$/", datetime, matches):
                #// Y-m
                datetime = Array({"year": php_intval(matches[1]), "month": php_intval(matches[2])})
            elif php_preg_match("/^(\\d{4})\\-(\\d{2})\\-(\\d{2})$/", datetime, matches):
                #// Y-m-d
                datetime = Array({"year": php_intval(matches[1]), "month": php_intval(matches[2]), "day": php_intval(matches[3])})
            elif php_preg_match("/^(\\d{4})\\-(\\d{2})\\-(\\d{2}) (\\d{2}):(\\d{2})$/", datetime, matches):
                #// Y-m-d H:i
                datetime = Array({"year": php_intval(matches[1]), "month": php_intval(matches[2]), "day": php_intval(matches[3]), "hour": php_intval(matches[4]), "minute": php_intval(matches[5])})
            # end if
            #// If no match is found, we don't support default_to_max.
            if (not php_is_array(datetime)):
                wp_timezone = wp_timezone()
                #// Assume local timezone if not provided.
                dt = date_create(datetime, wp_timezone)
                if False == dt:
                    return gmdate("Y-m-d H:i:s", False)
                # end if
                return dt.settimezone(wp_timezone).format("Y-m-d H:i:s")
            # end if
        # end if
        datetime = php_array_map("absint", datetime)
        if (not (php_isset(lambda : datetime["year"]))):
            datetime["year"] = current_time("Y")
        # end if
        if (not (php_isset(lambda : datetime["month"]))):
            datetime["month"] = 12 if default_to_max else 1
        # end if
        if (not (php_isset(lambda : datetime["day"]))):
            datetime["day"] = php_int(gmdate("t", mktime(0, 0, 0, datetime["month"], 1, datetime["year"]))) if default_to_max else 1
        # end if
        if (not (php_isset(lambda : datetime["hour"]))):
            datetime["hour"] = 23 if default_to_max else 0
        # end if
        if (not (php_isset(lambda : datetime["minute"]))):
            datetime["minute"] = 59 if default_to_max else 0
        # end if
        if (not (php_isset(lambda : datetime["second"]))):
            datetime["second"] = 59 if default_to_max else 0
        # end if
        return php_sprintf("%04d-%02d-%02d %02d:%02d:%02d", datetime["year"], datetime["month"], datetime["day"], datetime["hour"], datetime["minute"], datetime["second"])
    # end def build_mysql_datetime
    #// 
    #// Builds a query string for comparing time values (hour, minute, second).
    #// 
    #// If just hour, minute, or second is set than a normal comparison will be done.
    #// However if multiple values are passed, a pseudo-decimal time will be created
    #// in order to be able to accurately compare against.
    #// 
    #// @since 3.7.0
    #// 
    #// @param string $column The column to query against. Needs to be pre-validated!
    #// @param string $compare The comparison operator. Needs to be pre-validated!
    #// @param int|null $hour Optional. An hour value (0-23).
    #// @param int|null $minute Optional. A minute value (0-59).
    #// @param int|null $second Optional. A second value (0-59).
    #// @return string|false A query part or false on failure.
    #//
    def build_time_query(self, column=None, compare=None, hour=None, minute=None, second=None):
        
        global wpdb
        php_check_if_defined("wpdb")
        #// Have to have at least one.
        if (not (php_isset(lambda : hour))) and (not (php_isset(lambda : minute))) and (not (php_isset(lambda : second))):
            return False
        # end if
        #// Complex combined queries aren't supported for multi-value queries.
        if php_in_array(compare, Array("IN", "NOT IN", "BETWEEN", "NOT BETWEEN")):
            return_ = Array()
            value = self.build_value(compare, hour)
            if False != value:
                return_[-1] = str("HOUR( ") + str(column) + str(" ) ") + str(compare) + str(" ") + str(value)
            # end if
            value = self.build_value(compare, minute)
            if False != value:
                return_[-1] = str("MINUTE( ") + str(column) + str(" ) ") + str(compare) + str(" ") + str(value)
            # end if
            value = self.build_value(compare, second)
            if False != value:
                return_[-1] = str("SECOND( ") + str(column) + str(" ) ") + str(compare) + str(" ") + str(value)
            # end if
            return php_implode(" AND ", return_)
        # end if
        #// Cases where just one unit is set.
        if (php_isset(lambda : hour)) and (not (php_isset(lambda : minute))) and (not (php_isset(lambda : second))):
            value = self.build_value(compare, hour)
            if False != value:
                return str("HOUR( ") + str(column) + str(" ) ") + str(compare) + str(" ") + str(value)
            # end if
        elif (not (php_isset(lambda : hour))) and (php_isset(lambda : minute)) and (not (php_isset(lambda : second))):
            value = self.build_value(compare, minute)
            if False != value:
                return str("MINUTE( ") + str(column) + str(" ) ") + str(compare) + str(" ") + str(value)
            # end if
        elif (not (php_isset(lambda : hour))) and (not (php_isset(lambda : minute))) and (php_isset(lambda : second)):
            value = self.build_value(compare, second)
            if False != value:
                return str("SECOND( ") + str(column) + str(" ) ") + str(compare) + str(" ") + str(value)
            # end if
        # end if
        #// Single units were already handled. Since hour & second isn't allowed, minute must to be set.
        if (not (php_isset(lambda : minute))):
            return False
        # end if
        format = ""
        time = ""
        #// Hour.
        if None != hour:
            format += "%H."
            time += php_sprintf("%02d", hour) + "."
        else:
            format += "0."
            time += "0."
        # end if
        #// Minute.
        format += "%i"
        time += php_sprintf("%02d", minute)
        if (php_isset(lambda : second)):
            format += "%s"
            time += php_sprintf("%02d", second)
        # end if
        return wpdb.prepare(str("DATE_FORMAT( ") + str(column) + str(", %s ) ") + str(compare) + str(" %f"), format, time)
    # end def build_time_query
# end class WP_Date_Query
