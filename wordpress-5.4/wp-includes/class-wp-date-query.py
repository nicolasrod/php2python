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
    #// 
    #// Array of date queries.
    #// 
    #// See WP_Date_Query::__construct() for information on date query arguments.
    #// 
    #// @since 3.7.0
    #// @var array
    #//
    queries = Array()
    #// 
    #// The default relation between top-level queries. Can be either 'AND' or 'OR'.
    #// 
    #// @since 3.7.0
    #// @var string
    #//
    relation = "AND"
    #// 
    #// The column to query against. Can be changed via the query arguments.
    #// 
    #// @since 3.7.0
    #// @var string
    #//
    column = "post_date"
    #// 
    #// The value comparison operator. Can be changed via the query arguments.
    #// 
    #// @since 3.7.0
    #// @var array
    #//
    compare = "="
    #// 
    #// Supported time-related parameter keys.
    #// 
    #// @since 4.1.0
    #// @var array
    #//
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
    def __init__(self, date_query_=None, default_column_="post_date"):
        
        
        if php_empty(lambda : date_query_) or (not php_is_array(date_query_)):
            return
        # end if
        if (php_isset(lambda : date_query_["relation"])) and "OR" == php_strtoupper(date_query_["relation"]):
            self.relation = "OR"
        else:
            self.relation = "AND"
        # end if
        #// Support for passing time-based keys in the top level of the $date_query array.
        if (not (php_isset(lambda : date_query_[0]))):
            date_query_ = Array(date_query_)
        # end if
        if (not php_empty(lambda : date_query_["column"])):
            date_query_["column"] = esc_sql(date_query_["column"])
        else:
            date_query_["column"] = esc_sql(default_column_)
        # end if
        self.column = self.validate_column(self.column)
        self.compare = self.get_compare(date_query_)
        self.queries = self.sanitize_query(date_query_)
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
    def sanitize_query(self, queries_=None, parent_query_=None):
        if parent_query_ is None:
            parent_query_ = None
        # end if
        
        cleaned_query_ = Array()
        defaults_ = Array({"column": "post_date", "compare": "=", "relation": "AND"})
        #// Numeric keys should always have array values.
        for qkey_,qvalue_ in queries_.items():
            if php_is_numeric(qkey_) and (not php_is_array(qvalue_)):
                queries_[qkey_] = None
            # end if
        # end for
        #// Each query should have a value for each default key. Inherit from the parent when possible.
        for dkey_,dvalue_ in defaults_.items():
            if (php_isset(lambda : queries_[dkey_])):
                continue
            # end if
            if (php_isset(lambda : parent_query_[dkey_])):
                queries_[dkey_] = parent_query_[dkey_]
            else:
                queries_[dkey_] = dvalue_
            # end if
        # end for
        #// Validate the dates passed in the query.
        if self.is_first_order_clause(queries_):
            self.validate_date_values(queries_)
        # end if
        for key_,q_ in queries_.items():
            if (not php_is_array(q_)) or php_in_array(key_, self.time_keys, True):
                #// This is a first-order query. Trust the values and sanitize when building SQL.
                cleaned_query_[key_] = q_
            else:
                #// Any array without a time key is another query, so we recurse.
                cleaned_query_[-1] = self.sanitize_query(q_, queries_)
            # end if
        # end for
        return cleaned_query_
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
    def is_first_order_clause(self, query_=None):
        
        
        time_keys_ = php_array_intersect(self.time_keys, php_array_keys(query_))
        return (not php_empty(lambda : time_keys_))
    # end def is_first_order_clause
    #// 
    #// Determines and validates what comparison operator to use.
    #// 
    #// @since 3.7.0
    #// 
    #// @param array $query A date query or a date subquery.
    #// @return string The comparison operator.
    #//
    def get_compare(self, query_=None):
        
        
        if (not php_empty(lambda : query_["compare"])) and php_in_array(query_["compare"], Array("=", "!=", ">", ">=", "<", "<=", "IN", "NOT IN", "BETWEEN", "NOT BETWEEN")):
            return php_strtoupper(query_["compare"])
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
    def validate_date_values(self, date_query_=None):
        if date_query_ is None:
            date_query_ = Array()
        # end if
        
        if php_empty(lambda : date_query_):
            return False
        # end if
        valid_ = True
        #// 
        #// Validate 'before' and 'after' up front, then let the
        #// validation routine continue to be sure that all invalid
        #// values generate errors too.
        #//
        if php_array_key_exists("before", date_query_) and php_is_array(date_query_["before"]):
            valid_ = self.validate_date_values(date_query_["before"])
        # end if
        if php_array_key_exists("after", date_query_) and php_is_array(date_query_["after"]):
            valid_ = self.validate_date_values(date_query_["after"])
        # end if
        #// Array containing all min-max checks.
        min_max_checks_ = Array()
        #// Days per year.
        if php_array_key_exists("year", date_query_):
            #// 
            #// If a year exists in the date query, we can use it to get the days.
            #// If multiple years are provided (as in a BETWEEN), use the first one.
            #//
            if php_is_array(date_query_["year"]):
                _year_ = reset(date_query_["year"])
            else:
                _year_ = date_query_["year"]
            # end if
            max_days_of_year_ = gmdate("z", mktime(0, 0, 0, 12, 31, _year_)) + 1
        else:
            #// Otherwise we use the max of 366 (leap-year).
            max_days_of_year_ = 366
        # end if
        min_max_checks_["dayofyear"] = Array({"min": 1, "max": max_days_of_year_})
        #// Days per week.
        min_max_checks_["dayofweek"] = Array({"min": 1, "max": 7})
        #// Days per week.
        min_max_checks_["dayofweek_iso"] = Array({"min": 1, "max": 7})
        #// Months per year.
        min_max_checks_["month"] = Array({"min": 1, "max": 12})
        #// Weeks per year.
        if (php_isset(lambda : _year_)):
            #// 
            #// If we have a specific year, use it to calculate number of weeks.
            #// Note: the number of weeks in a year is the date in which Dec 28 appears.
            #//
            week_count_ = gmdate("W", mktime(0, 0, 0, 12, 28, _year_))
        else:
            #// Otherwise set the week-count to a maximum of 53.
            week_count_ = 53
        # end if
        min_max_checks_["week"] = Array({"min": 1, "max": week_count_})
        #// Days per month.
        min_max_checks_["day"] = Array({"min": 1, "max": 31})
        #// Hours per day.
        min_max_checks_["hour"] = Array({"min": 0, "max": 23})
        #// Minutes per hour.
        min_max_checks_["minute"] = Array({"min": 0, "max": 59})
        #// Seconds per minute.
        min_max_checks_["second"] = Array({"min": 0, "max": 59})
        #// Concatenate and throw a notice for each invalid value.
        for key_,check_ in min_max_checks_.items():
            if (not php_array_key_exists(key_, date_query_)):
                continue
            # end if
            #// Throw a notice for each failing value.
            for _value_ in date_query_[key_]:
                is_between_ = _value_ >= check_["min"] and _value_ <= check_["max"]
                if (not php_is_numeric(_value_)) or (not is_between_):
                    error_ = php_sprintf(__("Invalid value %1$s for %2$s. Expected value should be between %3$s and %4$s."), "<code>" + esc_html(_value_) + "</code>", "<code>" + esc_html(key_) + "</code>", "<code>" + esc_html(check_["min"]) + "</code>", "<code>" + esc_html(check_["max"]) + "</code>")
                    _doing_it_wrong(__CLASS__, error_, "4.1.0")
                    valid_ = False
                # end if
            # end for
        # end for
        #// If we already have invalid date messages, don't bother running through checkdate().
        if (not valid_):
            return valid_
        # end if
        day_month_year_error_msg_ = ""
        day_exists_ = php_array_key_exists("day", date_query_) and php_is_numeric(date_query_["day"])
        month_exists_ = php_array_key_exists("month", date_query_) and php_is_numeric(date_query_["month"])
        year_exists_ = php_array_key_exists("year", date_query_) and php_is_numeric(date_query_["year"])
        if day_exists_ and month_exists_ and year_exists_:
            #// 1. Checking day, month, year combination.
            if (not wp_checkdate(date_query_["month"], date_query_["day"], date_query_["year"], php_sprintf("%s-%s-%s", date_query_["year"], date_query_["month"], date_query_["day"]))):
                day_month_year_error_msg_ = php_sprintf(__("The following values do not describe a valid date: year %1$s, month %2$s, day %3$s."), "<code>" + esc_html(date_query_["year"]) + "</code>", "<code>" + esc_html(date_query_["month"]) + "</code>", "<code>" + esc_html(date_query_["day"]) + "</code>")
                valid_ = False
            # end if
        elif day_exists_ and month_exists_:
            #// 
            #// 2. checking day, month combination
            #// We use 2012 because, as a leap year, it's the most permissive.
            #//
            if (not wp_checkdate(date_query_["month"], date_query_["day"], 2012, php_sprintf("2012-%s-%s", date_query_["month"], date_query_["day"]))):
                day_month_year_error_msg_ = php_sprintf(__("The following values do not describe a valid date: month %1$s, day %2$s."), "<code>" + esc_html(date_query_["month"]) + "</code>", "<code>" + esc_html(date_query_["day"]) + "</code>")
                valid_ = False
            # end if
        # end if
        if (not php_empty(lambda : day_month_year_error_msg_)):
            _doing_it_wrong(__CLASS__, day_month_year_error_msg_, "4.1.0")
        # end if
        return valid_
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
    def validate_column(self, column_=None):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        valid_columns_ = Array("post_date", "post_date_gmt", "post_modified", "post_modified_gmt", "comment_date", "comment_date_gmt", "user_registered", "registered", "last_updated")
        #// Attempt to detect a table prefix.
        if False == php_strpos(column_, "."):
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
            if (not php_in_array(column_, apply_filters("date_query_valid_columns", valid_columns_))):
                column_ = "post_date"
            # end if
            known_columns_ = Array({wpdb_.posts: Array("post_date", "post_date_gmt", "post_modified", "post_modified_gmt"), wpdb_.comments: Array("comment_date", "comment_date_gmt"), wpdb_.users: Array("user_registered"), wpdb_.blogs: Array("registered", "last_updated")})
            #// If it's a known column name, add the appropriate table prefix.
            for table_name_,table_columns_ in known_columns_.items():
                if php_in_array(column_, table_columns_):
                    column_ = table_name_ + "." + column_
                    break
                # end if
            # end for
        # end if
        #// Remove unsafe characters.
        return php_preg_replace("/[^a-zA-Z0-9_$\\.]/", "", column_)
    # end def validate_column
    #// 
    #// Generate WHERE clause to be appended to a main query.
    #// 
    #// @since 3.7.0
    #// 
    #// @return string MySQL WHERE clause.
    #//
    def get_sql(self):
        
        
        sql_ = self.get_sql_clauses()
        where_ = sql_["where"]
        #// 
        #// Filters the date query WHERE clause.
        #// 
        #// @since 3.7.0
        #// 
        #// @param string        $where WHERE clause of the date query.
        #// @param WP_Date_Query $this  The WP_Date_Query instance.
        #//
        return apply_filters("get_date_sql", where_, self)
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
        
        
        sql_ = self.get_sql_for_query(self.queries)
        if (not php_empty(lambda : sql_["where"])):
            sql_["where"] = " AND " + sql_["where"]
        # end if
        return sql_
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
    def get_sql_for_query(self, query_=None, depth_=0):
        
        
        sql_chunks_ = Array({"join": Array(), "where": Array()})
        sql_ = Array({"join": "", "where": ""})
        indent_ = ""
        i_ = 0
        while i_ < depth_:
            
            indent_ += "  "
            i_ += 1
        # end while
        for key_,clause_ in query_.items():
            if "relation" == key_:
                relation_ = query_["relation"]
            elif php_is_array(clause_):
                #// This is a first-order clause.
                if self.is_first_order_clause(clause_):
                    clause_sql_ = self.get_sql_for_clause(clause_, query_)
                    where_count_ = php_count(clause_sql_["where"])
                    if (not where_count_):
                        sql_chunks_["where"][-1] = ""
                    elif 1 == where_count_:
                        sql_chunks_["where"][-1] = clause_sql_["where"][0]
                    else:
                        sql_chunks_["where"][-1] = "( " + php_implode(" AND ", clause_sql_["where"]) + " )"
                    # end if
                    sql_chunks_["join"] = php_array_merge(sql_chunks_["join"], clause_sql_["join"])
                    pass
                else:
                    clause_sql_ = self.get_sql_for_query(clause_, depth_ + 1)
                    sql_chunks_["where"][-1] = clause_sql_["where"]
                    sql_chunks_["join"][-1] = clause_sql_["join"]
                # end if
            # end if
        # end for
        #// Filter to remove empties.
        sql_chunks_["join"] = php_array_filter(sql_chunks_["join"])
        sql_chunks_["where"] = php_array_filter(sql_chunks_["where"])
        if php_empty(lambda : relation_):
            relation_ = "AND"
        # end if
        #// Filter duplicate JOIN clauses and combine into a single string.
        if (not php_empty(lambda : sql_chunks_["join"])):
            sql_["join"] = php_implode(" ", array_unique(sql_chunks_["join"]))
        # end if
        #// Generate a single WHERE clause with proper brackets and indentation.
        if (not php_empty(lambda : sql_chunks_["where"])):
            sql_["where"] = "( " + "\n  " + indent_ + php_implode(" " + "\n  " + indent_ + relation_ + " " + "\n  " + indent_, sql_chunks_["where"]) + "\n" + indent_ + ")"
        # end if
        return sql_
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
    def get_sql_for_subquery(self, query_=None):
        
        
        return self.get_sql_for_clause(query_, "")
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
    def get_sql_for_clause(self, query_=None, parent_query_=None):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        #// The sub-parts of a $where part.
        where_parts_ = Array()
        column_ = esc_sql(query_["column"]) if (not php_empty(lambda : query_["column"])) else self.column
        column_ = self.validate_column(column_)
        compare_ = self.get_compare(query_)
        inclusive_ = (not php_empty(lambda : query_["inclusive"]))
        #// Assign greater- and less-than values.
        lt_ = "<"
        gt_ = ">"
        if inclusive_:
            lt_ += "="
            gt_ += "="
        # end if
        #// Range queries.
        if (not php_empty(lambda : query_["after"])):
            where_parts_[-1] = wpdb_.prepare(str(column_) + str(" ") + str(gt_) + str(" %s"), self.build_mysql_datetime(query_["after"], (not inclusive_)))
        # end if
        if (not php_empty(lambda : query_["before"])):
            where_parts_[-1] = wpdb_.prepare(str(column_) + str(" ") + str(lt_) + str(" %s"), self.build_mysql_datetime(query_["before"], inclusive_))
        # end if
        #// Specific value queries.
        date_units_ = Array({"YEAR": Array("year"), "MONTH": Array("month", "monthnum"), "_wp_mysql_week": Array("week", "w"), "DAYOFYEAR": Array("dayofyear"), "DAYOFMONTH": Array("day"), "DAYOFWEEK": Array("dayofweek"), "WEEKDAY": Array("dayofweek_iso")})
        #// Check of the possible date units and add them to the query.
        for sql_part_,query_parts_ in date_units_.items():
            for query_part_ in query_parts_:
                if (php_isset(lambda : query_[query_part_])):
                    value_ = self.build_value(compare_, query_[query_part_])
                    if value_:
                        for case in Switch(sql_part_):
                            if case("_wp_mysql_week"):
                                where_parts_[-1] = _wp_mysql_week(column_) + str(" ") + str(compare_) + str(" ") + str(value_)
                                break
                            # end if
                            if case("WEEKDAY"):
                                where_parts_[-1] = str(sql_part_) + str("( ") + str(column_) + str(" ) + 1 ") + str(compare_) + str(" ") + str(value_)
                                break
                            # end if
                            if case():
                                where_parts_[-1] = str(sql_part_) + str("( ") + str(column_) + str(" ) ") + str(compare_) + str(" ") + str(value_)
                            # end if
                        # end for
                        break
                    # end if
                # end if
            # end for
        # end for
        if (php_isset(lambda : query_["hour"])) or (php_isset(lambda : query_["minute"])) or (php_isset(lambda : query_["second"])):
            #// Avoid notices.
            for unit_ in Array("hour", "minute", "second"):
                if (not (php_isset(lambda : query_[unit_]))):
                    query_[unit_] = None
                # end if
            # end for
            time_query_ = self.build_time_query(column_, compare_, query_["hour"], query_["minute"], query_["second"])
            if time_query_:
                where_parts_[-1] = time_query_
            # end if
        # end if
        #// 
        #// Return an array of 'join' and 'where' for compatibility
        #// with other query classes.
        #//
        return Array({"where": where_parts_, "join": Array()})
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
    def build_value(self, compare_=None, value_=None):
        
        
        if (not (php_isset(lambda : value_))):
            return False
        # end if
        for case in Switch(compare_):
            if case("IN"):
                pass
            # end if
            if case("NOT IN"):
                value_ = value_
                #// Remove non-numeric values.
                value_ = php_array_filter(value_, "is_numeric")
                if php_empty(lambda : value_):
                    return False
                # end if
                return "(" + php_implode(",", php_array_map("intval", value_)) + ")"
            # end if
            if case("BETWEEN"):
                pass
            # end if
            if case("NOT BETWEEN"):
                if (not php_is_array(value_)) or 2 != php_count(value_):
                    value_ = Array(value_, value_)
                else:
                    value_ = php_array_values(value_)
                # end if
                #// If either value is non-numeric, bail.
                for v_ in value_:
                    if (not php_is_numeric(v_)):
                        return False
                    # end if
                # end for
                value_ = php_array_map("intval", value_)
                return value_[0] + " AND " + value_[1]
            # end if
            if case():
                if (not php_is_numeric(value_)):
                    return False
                # end if
                return php_int(value_)
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
    def build_mysql_datetime(self, datetime_=None, default_to_max_=None):
        if default_to_max_ is None:
            default_to_max_ = False
        # end if
        
        if (not php_is_array(datetime_)):
            #// 
            #// Try to parse some common date formats, so we can detect
            #// the level of precision and support the 'inclusive' parameter.
            #//
            if php_preg_match("/^(\\d{4})$/", datetime_, matches_):
                #// Y
                datetime_ = Array({"year": php_intval(matches_[1])})
            elif php_preg_match("/^(\\d{4})\\-(\\d{2})$/", datetime_, matches_):
                #// Y-m
                datetime_ = Array({"year": php_intval(matches_[1]), "month": php_intval(matches_[2])})
            elif php_preg_match("/^(\\d{4})\\-(\\d{2})\\-(\\d{2})$/", datetime_, matches_):
                #// Y-m-d
                datetime_ = Array({"year": php_intval(matches_[1]), "month": php_intval(matches_[2]), "day": php_intval(matches_[3])})
            elif php_preg_match("/^(\\d{4})\\-(\\d{2})\\-(\\d{2}) (\\d{2}):(\\d{2})$/", datetime_, matches_):
                #// Y-m-d H:i
                datetime_ = Array({"year": php_intval(matches_[1]), "month": php_intval(matches_[2]), "day": php_intval(matches_[3]), "hour": php_intval(matches_[4]), "minute": php_intval(matches_[5])})
            # end if
            #// If no match is found, we don't support default_to_max.
            if (not php_is_array(datetime_)):
                wp_timezone_ = wp_timezone()
                #// Assume local timezone if not provided.
                dt_ = date_create(datetime_, wp_timezone_)
                if False == dt_:
                    return gmdate("Y-m-d H:i:s", False)
                # end if
                return dt_.settimezone(wp_timezone_).format("Y-m-d H:i:s")
            # end if
        # end if
        datetime_ = php_array_map("absint", datetime_)
        if (not (php_isset(lambda : datetime_["year"]))):
            datetime_["year"] = current_time("Y")
        # end if
        if (not (php_isset(lambda : datetime_["month"]))):
            datetime_["month"] = 12 if default_to_max_ else 1
        # end if
        if (not (php_isset(lambda : datetime_["day"]))):
            datetime_["day"] = php_int(gmdate("t", mktime(0, 0, 0, datetime_["month"], 1, datetime_["year"]))) if default_to_max_ else 1
        # end if
        if (not (php_isset(lambda : datetime_["hour"]))):
            datetime_["hour"] = 23 if default_to_max_ else 0
        # end if
        if (not (php_isset(lambda : datetime_["minute"]))):
            datetime_["minute"] = 59 if default_to_max_ else 0
        # end if
        if (not (php_isset(lambda : datetime_["second"]))):
            datetime_["second"] = 59 if default_to_max_ else 0
        # end if
        return php_sprintf("%04d-%02d-%02d %02d:%02d:%02d", datetime_["year"], datetime_["month"], datetime_["day"], datetime_["hour"], datetime_["minute"], datetime_["second"])
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
    def build_time_query(self, column_=None, compare_=None, hour_=None, minute_=None, second_=None):
        if hour_ is None:
            hour_ = None
        # end if
        if minute_ is None:
            minute_ = None
        # end if
        if second_ is None:
            second_ = None
        # end if
        
        global wpdb_
        php_check_if_defined("wpdb_")
        #// Have to have at least one.
        if (not (php_isset(lambda : hour_))) and (not (php_isset(lambda : minute_))) and (not (php_isset(lambda : second_))):
            return False
        # end if
        #// Complex combined queries aren't supported for multi-value queries.
        if php_in_array(compare_, Array("IN", "NOT IN", "BETWEEN", "NOT BETWEEN")):
            return_ = Array()
            value_ = self.build_value(compare_, hour_)
            if False != value_:
                return_[-1] = str("HOUR( ") + str(column_) + str(" ) ") + str(compare_) + str(" ") + str(value_)
            # end if
            value_ = self.build_value(compare_, minute_)
            if False != value_:
                return_[-1] = str("MINUTE( ") + str(column_) + str(" ) ") + str(compare_) + str(" ") + str(value_)
            # end if
            value_ = self.build_value(compare_, second_)
            if False != value_:
                return_[-1] = str("SECOND( ") + str(column_) + str(" ) ") + str(compare_) + str(" ") + str(value_)
            # end if
            return php_implode(" AND ", return_)
        # end if
        #// Cases where just one unit is set.
        if (php_isset(lambda : hour_)) and (not (php_isset(lambda : minute_))) and (not (php_isset(lambda : second_))):
            value_ = self.build_value(compare_, hour_)
            if False != value_:
                return str("HOUR( ") + str(column_) + str(" ) ") + str(compare_) + str(" ") + str(value_)
            # end if
        elif (not (php_isset(lambda : hour_))) and (php_isset(lambda : minute_)) and (not (php_isset(lambda : second_))):
            value_ = self.build_value(compare_, minute_)
            if False != value_:
                return str("MINUTE( ") + str(column_) + str(" ) ") + str(compare_) + str(" ") + str(value_)
            # end if
        elif (not (php_isset(lambda : hour_))) and (not (php_isset(lambda : minute_))) and (php_isset(lambda : second_)):
            value_ = self.build_value(compare_, second_)
            if False != value_:
                return str("SECOND( ") + str(column_) + str(" ) ") + str(compare_) + str(" ") + str(value_)
            # end if
        # end if
        #// Single units were already handled. Since hour & second isn't allowed, minute must to be set.
        if (not (php_isset(lambda : minute_))):
            return False
        # end if
        format_ = ""
        time_ = ""
        #// Hour.
        if None != hour_:
            format_ += "%H."
            time_ += php_sprintf("%02d", hour_) + "."
        else:
            format_ += "0."
            time_ += "0."
        # end if
        #// Minute.
        format_ += "%i"
        time_ += php_sprintf("%02d", minute_)
        if (php_isset(lambda : second_)):
            format_ += "%s"
            time_ += php_sprintf("%02d", second_)
        # end if
        return wpdb_.prepare(str("DATE_FORMAT( ") + str(column_) + str(", %s ) ") + str(compare_) + str(" %f"), format_, time_)
    # end def build_time_query
# end class WP_Date_Query
