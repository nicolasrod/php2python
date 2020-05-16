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
#// Main WordPress API
#// 
#// @package WordPress
#//
php_include_file(ABSPATH + WPINC + "/option.php", once=False)
#// 
#// Convert given MySQL date string into a different format.
#// 
#// `$format` should be a PHP date format string.
#// 'U' and 'G' formats will return a sum of timestamp with timezone offset.
#// `$date` is expected to be local time in MySQL format (`Y-m-d H:i:s`).
#// 
#// Historically UTC time could be passed to the function to produce Unix timestamp.
#// 
#// If `$translate` is true then the given date and format string will
#// be passed to `wp_date()` for translation.
#// 
#// @since 0.71
#// 
#// @param string $format    Format of the date to return.
#// @param string $date      Date string to convert.
#// @param bool   $translate Whether the return date should be translated. Default true.
#// @return string|int|false Formatted date string or sum of Unix timestamp and timezone offset.
#// False on failure.
#//
def mysql2date(format=None, date=None, translate=True, *args_):
    
    if php_empty(lambda : date):
        return False
    # end if
    datetime = date_create(date, wp_timezone())
    if False == datetime:
        return False
    # end if
    #// Returns a sum of timestamp with timezone offset. Ideally should never be used.
    if "G" == format or "U" == format:
        return datetime.gettimestamp() + datetime.getoffset()
    # end if
    if translate:
        return wp_date(format, datetime.gettimestamp())
    # end if
    return datetime.format(format)
# end def mysql2date
#// 
#// Retrieves the current time based on specified type.
#// 
#// The 'mysql' type will return the time in the format for MySQL DATETIME field.
#// The 'timestamp' type will return the current timestamp or a sum of timestamp
#// and timezone offset, depending on `$gmt`.
#// Other strings will be interpreted as PHP date formats (e.g. 'Y-m-d').
#// 
#// If $gmt is set to either '1' or 'true', then both types will use GMT time.
#// if $gmt is false, the output is adjusted with the GMT offset in the WordPress option.
#// 
#// @since 1.0.0
#// 
#// @param string   $type Type of time to retrieve. Accepts 'mysql', 'timestamp',
#// or PHP date format string (e.g. 'Y-m-d').
#// @param int|bool $gmt  Optional. Whether to use GMT timezone. Default false.
#// @return int|string Integer if $type is 'timestamp', string otherwise.
#//
def current_time(type=None, gmt=0, *args_):
    
    #// Don't use non-GMT timestamp, unless you know the difference and really need to.
    if "timestamp" == type or "U" == type:
        return time() if gmt else time() + php_int(get_option("gmt_offset") * HOUR_IN_SECONDS)
    # end if
    if "mysql" == type:
        type = "Y-m-d H:i:s"
    # end if
    timezone = php_new_class("DateTimeZone", lambda : DateTimeZone("UTC")) if gmt else wp_timezone()
    datetime = php_new_class("DateTime", lambda : DateTime("now", timezone))
    return datetime.format(type)
# end def current_time
#// 
#// Retrieves the current time as an object with the timezone from settings.
#// 
#// @since 5.3.0
#// 
#// @return DateTimeImmutable Date and time object.
#//
def current_datetime(*args_):
    
    return php_new_class("DateTimeImmutable", lambda : DateTimeImmutable("now", wp_timezone()))
# end def current_datetime
#// 
#// Retrieves the timezone from site settings as a string.
#// 
#// Uses the `timezone_string` option to get a proper timezone if available,
#// otherwise falls back to an offset.
#// 
#// @since 5.3.0
#// 
#// @return string PHP timezone string or a ±HH:MM offset.
#//
def wp_timezone_string(*args_):
    
    timezone_string = get_option("timezone_string")
    if timezone_string:
        return timezone_string
    # end if
    offset = php_float(get_option("gmt_offset"))
    hours = php_int(offset)
    minutes = offset - hours
    sign = "-" if offset < 0 else "+"
    abs_hour = abs(hours)
    abs_mins = abs(minutes * 60)
    tz_offset = php_sprintf("%s%02d:%02d", sign, abs_hour, abs_mins)
    return tz_offset
# end def wp_timezone_string
#// 
#// Retrieves the timezone from site settings as a `DateTimeZone` object.
#// 
#// Timezone can be based on a PHP timezone string or a ±HH:MM offset.
#// 
#// @since 5.3.0
#// 
#// @return DateTimeZone Timezone object.
#//
def wp_timezone(*args_):
    
    return php_new_class("DateTimeZone", lambda : DateTimeZone(wp_timezone_string()))
# end def wp_timezone
#// 
#// Retrieves the date in localized format, based on a sum of Unix timestamp and
#// timezone offset in seconds.
#// 
#// If the locale specifies the locale month and weekday, then the locale will
#// take over the format for the date. If it isn't, then the date format string
#// will be used instead.
#// 
#// Note that due to the way WP typically generates a sum of timestamp and offset
#// with `strtotime()`, it implies offset added at a _current_ time, not at the time
#// the timestamp represents. Storing such timestamps or calculating them differently
#// will lead to invalid output.
#// 
#// @since 0.71
#// @since 5.3.0 Converted into a wrapper for wp_date().
#// 
#// @global WP_Locale $wp_locale WordPress date and time locale object.
#// 
#// @param string   $format                Format to display the date.
#// @param int|bool $timestamp_with_offset Optional. A sum of Unix timestamp and timezone offset
#// in seconds. Default false.
#// @param bool     $gmt                   Optional. Whether to use GMT timezone. Only applies
#// if timestamp is not provided. Default false.
#// @return string The date, translated if locale specifies it.
#//
def date_i18n(format=None, timestamp_with_offset=False, gmt=False, *args_):
    
    timestamp = timestamp_with_offset
    #// If timestamp is omitted it should be current time (summed with offset, unless `$gmt` is true).
    if (not php_is_numeric(timestamp)):
        timestamp = current_time("timestamp", gmt)
    # end if
    #// 
    #// This is a legacy implementation quirk that the returned timestamp is also with offset.
    #// Ideally this function should never be used to produce a timestamp.
    #//
    if "U" == format:
        date = timestamp
    elif gmt and False == timestamp_with_offset:
        #// Current time in UTC.
        date = wp_date(format, None, php_new_class("DateTimeZone", lambda : DateTimeZone("UTC")))
    elif False == timestamp_with_offset:
        #// Current time in site's timezone.
        date = wp_date(format)
    else:
        #// 
        #// Timestamp with offset is typically produced by a UTC `strtotime()` call on an input without timezone.
        #// This is the best attempt to reverse that operation into a local time to use.
        #//
        local_time = gmdate("Y-m-d H:i:s", timestamp)
        timezone = wp_timezone()
        datetime = date_create(local_time, timezone)
        date = wp_date(format, datetime.gettimestamp(), timezone)
    # end if
    #// 
    #// Filters the date formatted based on the locale.
    #// 
    #// @since 2.8.0
    #// 
    #// @param string $date      Formatted date string.
    #// @param string $format    Format to display the date.
    #// @param int    $timestamp A sum of Unix timestamp and timezone offset in seconds.
    #// Might be without offset if input omitted timestamp but requested GMT.
    #// @param bool   $gmt       Whether to use GMT timezone. Only applies if timestamp was not provided.
    #// Default false.
    #//
    date = apply_filters("date_i18n", date, format, timestamp, gmt)
    return date
# end def date_i18n
#// 
#// Retrieves the date, in localized format.
#// 
#// This is a newer function, intended to replace `date_i18n()` without legacy quirks in it.
#// 
#// Note that, unlike `date_i18n()`, this function accepts a true Unix timestamp, not summed
#// with timezone offset.
#// 
#// @since 5.3.0
#// 
#// @param string       $format    PHP date format.
#// @param int          $timestamp Optional. Unix timestamp. Defaults to current time.
#// @param DateTimeZone $timezone  Optional. Timezone to output result in. Defaults to timezone
#// from site settings.
#// @return string|false The date, translated if locale specifies it. False on invalid timestamp input.
#//
def wp_date(format=None, timestamp=None, timezone=None, *args_):
    
    global wp_locale
    php_check_if_defined("wp_locale")
    if None == timestamp:
        timestamp = time()
    elif (not php_is_numeric(timestamp)):
        return False
    # end if
    if (not timezone):
        timezone = wp_timezone()
    # end if
    datetime = date_create("@" + timestamp)
    datetime.settimezone(timezone)
    if php_empty(lambda : wp_locale.month) or php_empty(lambda : wp_locale.weekday):
        date = datetime.format(format)
    else:
        #// We need to unpack shorthand `r` format because it has parts that might be localized.
        format = php_preg_replace("/(?<!\\\\)r/", DATE_RFC2822, format)
        new_format = ""
        format_length = php_strlen(format)
        month = wp_locale.get_month(datetime.format("m"))
        weekday = wp_locale.get_weekday(datetime.format("w"))
        i = 0
        while i < format_length:
            
            for case in Switch(format[i]):
                if case("D"):
                    new_format += addcslashes(wp_locale.get_weekday_abbrev(weekday), "\\A..Za..z")
                    break
                # end if
                if case("F"):
                    new_format += addcslashes(month, "\\A..Za..z")
                    break
                # end if
                if case("l"):
                    new_format += addcslashes(weekday, "\\A..Za..z")
                    break
                # end if
                if case("M"):
                    new_format += addcslashes(wp_locale.get_month_abbrev(month), "\\A..Za..z")
                    break
                # end if
                if case("a"):
                    new_format += addcslashes(wp_locale.get_meridiem(datetime.format("a")), "\\A..Za..z")
                    break
                # end if
                if case("A"):
                    new_format += addcslashes(wp_locale.get_meridiem(datetime.format("A")), "\\A..Za..z")
                    break
                # end if
                if case("\\"):
                    new_format += format[i]
                    #// If character follows a slash, we add it without translating.
                    if i < format_length:
                        i += 1
                        new_format += format[i]
                    # end if
                    break
                # end if
                if case():
                    new_format += format[i]
                    break
                # end if
            # end for
            i += 1
        # end while
        date = datetime.format(new_format)
        date = wp_maybe_decline_date(date, format)
    # end if
    #// 
    #// Filters the date formatted based on the locale.
    #// 
    #// @since 5.3.0
    #// 
    #// @param string       $date      Formatted date string.
    #// @param string       $format    Format to display the date.
    #// @param int          $timestamp Unix timestamp.
    #// @param DateTimeZone $timezone  Timezone.
    #// 
    #//
    date = apply_filters("wp_date", date, format, timestamp, timezone)
    return date
# end def wp_date
#// 
#// Determines if the date should be declined.
#// 
#// If the locale specifies that month names require a genitive case in certain
#// formats (like 'j F Y'), the month name will be replaced with a correct form.
#// 
#// @since 4.4.0
#// @since 5.4.0 The `$format` parameter was added.
#// 
#// @global WP_Locale $wp_locale WordPress date and time locale object.
#// 
#// @param string $date   Formatted date string.
#// @param string $format Optional. Date format to check. Default empty string.
#// @return string The date, declined if locale specifies it.
#//
def wp_maybe_decline_date(date=None, format="", *args_):
    
    global wp_locale
    php_check_if_defined("wp_locale")
    #// i18n functions are not available in SHORTINIT mode.
    if (not php_function_exists("_x")):
        return date
    # end if
    #// 
    #// translators: If months in your language require a genitive case,
    #// translate this to 'on'. Do not translate into your own language.
    #//
    if "on" == _x("off", "decline months names: on or off"):
        months = wp_locale.month
        months_genitive = wp_locale.month_genitive
        #// 
        #// Match a format like 'j F Y' or 'j. F' (day of the month, followed by month name)
        #// and decline the month.
        #//
        if format:
            decline = php_preg_match("#[dj]\\.? F#", format)
        else:
            #// If the format is not passed, try to guess it from the date string.
            decline = php_preg_match("#\\b\\d{1,2}\\.? [^\\d ]+\\b#u", date)
        # end if
        if decline:
            for key,month in months:
                months[key] = "# " + preg_quote(month, "#") + "\\b#u"
            # end for
            for key,month in months_genitive:
                months_genitive[key] = " " + month
            # end for
            date = php_preg_replace(months, months_genitive, date)
        # end if
        #// 
        #// Match a format like 'F jS' or 'F j' (month name, followed by day with an optional ordinal suffix)
        #// and change it to declined 'j F'.
        #//
        if format:
            decline = php_preg_match("#F [dj]#", format)
        else:
            #// If the format is not passed, try to guess it from the date string.
            decline = php_preg_match("#\\b[^\\d ]+ \\d{1,2}(st|nd|rd|th)?\\b#u", php_trim(date))
        # end if
        if decline:
            for key,month in months:
                months[key] = "#\\b" + preg_quote(month, "#") + " (\\d{1,2})(st|nd|rd|th)?([-â]\\d{1,2})?(st|nd|rd|th)?\\b#u"
            # end for
            for key,month in months_genitive:
                months_genitive[key] = "$1$3 " + month
            # end for
            date = php_preg_replace(months, months_genitive, date)
        # end if
    # end if
    #// Used for locale-specific rules.
    locale = get_locale()
    if "ca" == locale:
        #// " de abril| de agost| de octubre..." -> " d'abril| d'agost| d'octubre..."
        date = php_preg_replace("# de ([ao])#i", " d'\\1", date)
    # end if
    return date
# end def wp_maybe_decline_date
#// 
#// Convert float number to format based on the locale.
#// 
#// @since 2.3.0
#// 
#// @global WP_Locale $wp_locale WordPress date and time locale object.
#// 
#// @param float $number   The number to convert based on locale.
#// @param int   $decimals Optional. Precision of the number of decimal places. Default 0.
#// @return string Converted number in string format.
#//
def number_format_i18n(number=None, decimals=0, *args_):
    
    global wp_locale
    php_check_if_defined("wp_locale")
    if (php_isset(lambda : wp_locale)):
        formatted = number_format(number, absint(decimals), wp_locale.number_format["decimal_point"], wp_locale.number_format["thousands_sep"])
    else:
        formatted = number_format(number, absint(decimals))
    # end if
    #// 
    #// Filters the number formatted based on the locale.
    #// 
    #// @since 2.8.0
    #// @since 4.9.0 The `$number` and `$decimals` parameters were added.
    #// 
    #// @param string $formatted Converted number in string format.
    #// @param float  $number    The number to convert based on locale.
    #// @param int    $decimals  Precision of the number of decimal places.
    #//
    return apply_filters("number_format_i18n", formatted, number, decimals)
# end def number_format_i18n
#// 
#// Convert number of bytes largest unit bytes will fit into.
#// 
#// It is easier to read 1 KB than 1024 bytes and 1 MB than 1048576 bytes. Converts
#// number of bytes to human readable number by taking the number of that unit
#// that the bytes will go into it. Supports TB value.
#// 
#// Please note that integers in PHP are limited to 32 bits, unless they are on
#// 64 bit architecture, then they have 64 bit size. If you need to place the
#// larger size then what PHP integer type will hold, then use a string. It will
#// be converted to a double, which should always have 64 bit length.
#// 
#// Technically the correct unit names for powers of 1024 are KiB, MiB etc.
#// 
#// @since 2.3.0
#// 
#// @param int|string $bytes    Number of bytes. Note max integer size for integers.
#// @param int        $decimals Optional. Precision of number of decimal places. Default 0.
#// @return string|false False on failure. Number string on success.
#//
def size_format(bytes=None, decimals=0, *args_):
    
    quant = Array({"TB": TB_IN_BYTES, "GB": GB_IN_BYTES, "MB": MB_IN_BYTES, "KB": KB_IN_BYTES, "B": 1})
    if 0 == bytes:
        return number_format_i18n(0, decimals) + " B"
    # end if
    for unit,mag in quant:
        if doubleval(bytes) >= mag:
            return number_format_i18n(bytes / mag, decimals) + " " + unit
        # end if
    # end for
    return False
# end def size_format
#// 
#// Convert a duration to human readable format.
#// 
#// @since 5.1.0
#// 
#// @param string $duration Duration will be in string format (HH:ii:ss) OR (ii:ss),
#// with a possible prepended negative sign (-).
#// @return string|false A human readable duration string, false on failure.
#//
def human_readable_duration(duration="", *args_):
    
    if php_empty(lambda : duration) or (not php_is_string(duration)):
        return False
    # end if
    duration = php_trim(duration)
    #// Remove prepended negative sign.
    if "-" == php_substr(duration, 0, 1):
        duration = php_substr(duration, 1)
    # end if
    #// Extract duration parts.
    duration_parts = array_reverse(php_explode(":", duration))
    duration_count = php_count(duration_parts)
    hour = None
    minute = None
    second = None
    if 3 == duration_count:
        #// Validate HH:ii:ss duration format.
        if (not php_bool(php_preg_match("/^([0-9]+):([0-5]?[0-9]):([0-5]?[0-9])$/", duration))):
            return False
        # end if
        #// Three parts: hours, minutes & seconds.
        second, minute, hour = duration_parts
    elif 2 == duration_count:
        #// Validate ii:ss duration format.
        if (not php_bool(php_preg_match("/^([0-5]?[0-9]):([0-5]?[0-9])$/", duration))):
            return False
        # end if
        #// Two parts: minutes & seconds.
        second, minute = duration_parts
    else:
        return False
    # end if
    human_readable_duration = Array()
    #// Add the hour part to the string.
    if php_is_numeric(hour):
        #// translators: %s: Time duration in hour or hours.
        human_readable_duration[-1] = php_sprintf(_n("%s hour", "%s hours", hour), php_int(hour))
    # end if
    #// Add the minute part to the string.
    if php_is_numeric(minute):
        #// translators: %s: Time duration in minute or minutes.
        human_readable_duration[-1] = php_sprintf(_n("%s minute", "%s minutes", minute), php_int(minute))
    # end if
    #// Add the second part to the string.
    if php_is_numeric(second):
        #// translators: %s: Time duration in second or seconds.
        human_readable_duration[-1] = php_sprintf(_n("%s second", "%s seconds", second), php_int(second))
    # end if
    return php_implode(", ", human_readable_duration)
# end def human_readable_duration
#// 
#// Get the week start and end from the datetime or date string from MySQL.
#// 
#// @since 0.71
#// 
#// @param string     $mysqlstring   Date or datetime field type from MySQL.
#// @param int|string $start_of_week Optional. Start of the week as an integer. Default empty string.
#// @return array Keys are 'start' and 'end'.
#//
def get_weekstartend(mysqlstring=None, start_of_week="", *args_):
    
    #// MySQL string year.
    my = php_substr(mysqlstring, 0, 4)
    #// MySQL string month.
    mm = php_substr(mysqlstring, 8, 2)
    #// MySQL string day.
    md = php_substr(mysqlstring, 5, 2)
    #// The timestamp for MySQL string day.
    day = mktime(0, 0, 0, md, mm, my)
    #// The day of the week from the timestamp.
    weekday = gmdate("w", day)
    if (not php_is_numeric(start_of_week)):
        start_of_week = get_option("start_of_week")
    # end if
    if weekday < start_of_week:
        weekday += 7
    # end if
    #// The most recent week start day on or before $day.
    start = day - DAY_IN_SECONDS * weekday - start_of_week
    #// $start + 1 week - 1 second.
    end_ = start + WEEK_IN_SECONDS - 1
    return compact("start", "end")
# end def get_weekstartend
#// 
#// Unserialize value only if it was serialized.
#// 
#// @since 2.0.0
#// 
#// @param string $original Maybe unserialized original, if is needed.
#// @return mixed Unserialized data can be any type.
#//
def maybe_unserialize(original=None, *args_):
    
    if is_serialized(original):
        #// Don't attempt to unserialize data that wasn't serialized going in.
        return php_no_error(lambda: unserialize(original))
    # end if
    return original
# end def maybe_unserialize
#// 
#// Check value to find if it was serialized.
#// 
#// If $data is not an string, then returned value will always be false.
#// Serialized data is always a string.
#// 
#// @since 2.0.5
#// 
#// @param string $data   Value to check to see if was serialized.
#// @param bool   $strict Optional. Whether to be strict about the end of the string. Default true.
#// @return bool False if not serialized and true if it was.
#//
def is_serialized(data=None, strict=True, *args_):
    
    #// If it isn't a string, it isn't serialized.
    if (not php_is_string(data)):
        return False
    # end if
    data = php_trim(data)
    if "N;" == data:
        return True
    # end if
    if php_strlen(data) < 4:
        return False
    # end if
    if ":" != data[1]:
        return False
    # end if
    if strict:
        lastc = php_substr(data, -1)
        if ";" != lastc and "}" != lastc:
            return False
        # end if
    else:
        semicolon = php_strpos(data, ";")
        brace = php_strpos(data, "}")
        #// Either ; or } must exist.
        if False == semicolon and False == brace:
            return False
        # end if
        #// But neither must be in the first X characters.
        if False != semicolon and semicolon < 3:
            return False
        # end if
        if False != brace and brace < 4:
            return False
        # end if
    # end if
    token = data[0]
    for case in Switch(token):
        if case("s"):
            if strict:
                if "\"" != php_substr(data, -2, 1):
                    return False
                # end if
            elif False == php_strpos(data, "\""):
                return False
            # end if
        # end if
        if case("a"):
            pass
        # end if
        if case("O"):
            return php_bool(php_preg_match(str("/^") + str(token) + str(":[0-9]+:/s"), data))
        # end if
        if case("b"):
            pass
        # end if
        if case("i"):
            pass
        # end if
        if case("d"):
            end_ = "$" if strict else ""
            return php_bool(php_preg_match(str("/^") + str(token) + str(":[0-9.E+-]+;") + str(end_) + str("/"), data))
        # end if
    # end for
    return False
# end def is_serialized
#// 
#// Check whether serialized data is of string type.
#// 
#// @since 2.0.5
#// 
#// @param string $data Serialized data.
#// @return bool False if not a serialized string, true if it is.
#//
def is_serialized_string(data=None, *args_):
    
    #// if it isn't a string, it isn't a serialized string.
    if (not php_is_string(data)):
        return False
    # end if
    data = php_trim(data)
    if php_strlen(data) < 4:
        return False
    elif ":" != data[1]:
        return False
    elif ";" != php_substr(data, -1):
        return False
    elif "s" != data[0]:
        return False
    elif "\"" != php_substr(data, -2, 1):
        return False
    else:
        return True
    # end if
# end def is_serialized_string
#// 
#// Serialize data, if needed.
#// 
#// @since 2.0.5
#// 
#// @param string|array|object $data Data that might be serialized.
#// @return mixed A scalar data
#//
def maybe_serialize(data=None, *args_):
    
    if php_is_array(data) or php_is_object(data):
        return serialize(data)
    # end if
    #// 
    #// Double serialization is required for backward compatibility.
    #// See https://core.trac.wordpress.org/ticket/12930
    #// Also the world will end. See WP 3.6.1.
    #//
    if is_serialized(data, False):
        return serialize(data)
    # end if
    return data
# end def maybe_serialize
#// 
#// Retrieve post title from XMLRPC XML.
#// 
#// If the title element is not part of the XML, then the default post title from
#// the $post_default_title will be used instead.
#// 
#// @since 0.71
#// 
#// @global string $post_default_title Default XML-RPC post title.
#// 
#// @param string $content XMLRPC XML Request content
#// @return string Post title
#//
def xmlrpc_getposttitle(content=None, *args_):
    
    global post_default_title
    php_check_if_defined("post_default_title")
    if php_preg_match("/<title>(.+?)<\\/title>/is", content, matchtitle):
        post_title = matchtitle[1]
    else:
        post_title = post_default_title
    # end if
    return post_title
# end def xmlrpc_getposttitle
#// 
#// Retrieve the post category or categories from XMLRPC XML.
#// 
#// If the category element is not found, then the default post category will be
#// used. The return type then would be what $post_default_category. If the
#// category is found, then it will always be an array.
#// 
#// @since 0.71
#// 
#// @global string $post_default_category Default XML-RPC post category.
#// 
#// @param string $content XMLRPC XML Request content
#// @return string|array List of categories or category name.
#//
def xmlrpc_getpostcategory(content=None, *args_):
    
    global post_default_category
    php_check_if_defined("post_default_category")
    if php_preg_match("/<category>(.+?)<\\/category>/is", content, matchcat):
        post_category = php_trim(matchcat[1], ",")
        post_category = php_explode(",", post_category)
    else:
        post_category = post_default_category
    # end if
    return post_category
# end def xmlrpc_getpostcategory
#// 
#// XMLRPC XML content without title and category elements.
#// 
#// @since 0.71
#// 
#// @param string $content XML-RPC XML Request content.
#// @return string XMLRPC XML Request content without title and category elements.
#//
def xmlrpc_removepostdata(content=None, *args_):
    
    content = php_preg_replace("/<title>(.+?)<\\/title>/si", "", content)
    content = php_preg_replace("/<category>(.+?)<\\/category>/si", "", content)
    content = php_trim(content)
    return content
# end def xmlrpc_removepostdata
#// 
#// Use RegEx to extract URLs from arbitrary content.
#// 
#// @since 3.7.0
#// 
#// @param string $content Content to extract URLs from.
#// @return string[] Array of URLs found in passed string.
#//
def wp_extract_urls(content=None, *args_):
    
    preg_match_all("#([\"']?)(" + "(?:([\\w-]+:)?//?)" + "[^\\s()<>]+" + "[.]" + "(?:" + "\\([\\w\\d]+\\)|" + "(?:" + "[^`!()\\[\\]{};:'\".,<>Â«Â»ââââ\\s]|" + "(?:[:]\\d+)?/?" + ")+" + ")" + ")\\1#", content, post_links)
    post_links = array_unique(php_array_map("html_entity_decode", post_links[2]))
    return php_array_values(post_links)
# end def wp_extract_urls
#// 
#// Check content for video and audio links to add as enclosures.
#// 
#// Will not add enclosures that have already been added and will
#// remove enclosures that are no longer in the post. This is called as
#// pingbacks and trackbacks.
#// 
#// @since 1.5.0
#// @since 5.3.0 The `$content` parameter was made optional, and the `$post` parameter was
#// updated to accept a post ID or a WP_Post object.
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string         $content Post content. If `null`, the `post_content` field from `$post` is used.
#// @param int|WP_Post    $post    Post ID or post object.
#// @return null|bool Returns false if post is not found.
#//
def do_enclose(content=None, post=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    #// @todo Tidy this code and make the debug code optional.
    php_include_file(ABSPATH + WPINC + "/class-IXR.php", once=False)
    post = get_post(post)
    if (not post):
        return False
    # end if
    if None == content:
        content = post.post_content
    # end if
    post_links = Array()
    pung = get_enclosed(post.ID)
    post_links_temp = wp_extract_urls(content)
    for link_test in pung:
        #// Link is no longer in post.
        if (not php_in_array(link_test, post_links_temp, True)):
            mids = wpdb.get_col(wpdb.prepare(str("SELECT meta_id FROM ") + str(wpdb.postmeta) + str(" WHERE post_id = %d AND meta_key = 'enclosure' AND meta_value LIKE %s"), post.ID, wpdb.esc_like(link_test) + "%"))
            for mid in mids:
                delete_metadata_by_mid("post", mid)
            # end for
        # end if
    # end for
    for link_test in post_links_temp:
        #// If we haven't pung it already.
        if (not php_in_array(link_test, pung, True)):
            test = php_no_error(lambda: php_parse_url(link_test))
            if False == test:
                continue
            # end if
            if (php_isset(lambda : test["query"])):
                post_links[-1] = link_test
            elif (php_isset(lambda : test["path"])) and "/" != test["path"] and "" != test["path"]:
                post_links[-1] = link_test
            # end if
        # end if
    # end for
    #// 
    #// Filters the list of enclosure links before querying the database.
    #// 
    #// Allows for the addition and/or removal of potential enclosures to save
    #// to postmeta before checking the database for existing enclosures.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string[] $post_links An array of enclosure links.
    #// @param int      $post_ID    Post ID.
    #//
    post_links = apply_filters("enclosure_links", post_links, post.ID)
    for url in post_links:
        if "" != url and (not wpdb.get_var(wpdb.prepare(str("SELECT post_id FROM ") + str(wpdb.postmeta) + str(" WHERE post_id = %d AND meta_key = 'enclosure' AND meta_value LIKE %s"), post.ID, wpdb.esc_like(url) + "%"))):
            headers = wp_get_http_headers(url)
            if headers:
                len = php_int(headers["content-length"]) if (php_isset(lambda : headers["content-length"])) else 0
                type = headers["content-type"] if (php_isset(lambda : headers["content-type"])) else ""
                allowed_types = Array("video", "audio")
                #// Check to see if we can figure out the mime type from the extension.
                url_parts = php_no_error(lambda: php_parse_url(url))
                if False != url_parts:
                    extension = pathinfo(url_parts["path"], PATHINFO_EXTENSION)
                    if (not php_empty(lambda : extension)):
                        for exts,mime in wp_get_mime_types():
                            if php_preg_match("!^(" + exts + ")$!i", extension):
                                type = mime
                                break
                            # end if
                        # end for
                    # end if
                # end if
                if php_in_array(php_substr(type, 0, php_strpos(type, "/")), allowed_types, True):
                    add_post_meta(post.ID, "enclosure", str(url) + str("\n") + str(len) + str("\n") + str(mime) + str("\n"))
                # end if
            # end if
        # end if
    # end for
# end def do_enclose
#// 
#// Retrieve HTTP Headers from URL.
#// 
#// @since 1.5.1
#// 
#// @param string $url        URL to retrieve HTTP headers from.
#// @param bool   $deprecated Not Used.
#// @return bool|string False on failure, headers on success.
#//
def wp_get_http_headers(url=None, deprecated=False, *args_):
    
    if (not php_empty(lambda : deprecated)):
        _deprecated_argument(__FUNCTION__, "2.7.0")
    # end if
    response = wp_safe_remote_head(url)
    if is_wp_error(response):
        return False
    # end if
    return wp_remote_retrieve_headers(response)
# end def wp_get_http_headers
#// 
#// Determines whether the publish date of the current post in the loop is different
#// from the publish date of the previous post in the loop.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 0.71
#// 
#// @global string $currentday  The day of the current post in the loop.
#// @global string $previousday The day of the previous post in the loop.
#// 
#// @return int 1 when new day, 0 if not a new day.
#//
def is_new_day(*args_):
    
    global currentday,previousday
    php_check_if_defined("currentday","previousday")
    if currentday != previousday:
        return 1
    else:
        return 0
    # end if
# end def is_new_day
#// 
#// Build URL query based on an associative and, or indexed array.
#// 
#// This is a convenient function for easily building url queries. It sets the
#// separator to '&' and uses _http_build_query() function.
#// 
#// @since 2.3.0
#// 
#// @see _http_build_query() Used to build the query
#// @link https://www.php.net/manual/en/function.http-build-query.php for more on what
#// http_build_query() does.
#// 
#// @param array $data URL-encode key/value pairs.
#// @return string URL-encoded string.
#//
def build_query(data=None, *args_):
    
    return _http_build_query(data, None, "&", "", False)
# end def build_query
#// 
#// From php.net (modified by Mark Jaquith to behave like the native PHP5 function).
#// 
#// @since 3.2.0
#// @access private
#// 
#// @see https://www.php.net/manual/en/function.http-build-query.php
#// 
#// @param array|object  $data       An array or object of data. Converted to array.
#// @param string        $prefix     Optional. Numeric index. If set, start parameter numbering with it.
#// Default null.
#// @param string        $sep        Optional. Argument separator; defaults to 'arg_separator.output'.
#// Default null.
#// @param string        $key        Optional. Used to prefix key name. Default empty.
#// @param bool          $urlencode  Optional. Whether to use urlencode() in the result. Default true.
#// 
#// @return string The query string.
#//
def _http_build_query(data=None, prefix=None, sep=None, key="", urlencode=True, *args_):
    
    ret = Array()
    for k,v in data:
        if urlencode:
            k = urlencode(k)
        # end if
        if php_is_int(k) and None != prefix:
            k = prefix + k
        # end if
        if (not php_empty(lambda : key)):
            k = key + "%5B" + k + "%5D"
        # end if
        if None == v:
            continue
        elif False == v:
            v = "0"
        # end if
        if php_is_array(v) or php_is_object(v):
            php_array_push(ret, _http_build_query(v, "", sep, k, urlencode))
        elif urlencode:
            php_array_push(ret, k + "=" + urlencode(v))
        else:
            php_array_push(ret, k + "=" + v)
        # end if
    # end for
    if None == sep:
        sep = php_ini_get("arg_separator.output")
    # end if
    return php_implode(sep, ret)
# end def _http_build_query
#// 
#// Retrieves a modified URL query string.
#// 
#// You can rebuild the URL and append query variables to the URL query by using this function.
#// There are two ways to use this function; either a single key and value, or an associative array.
#// 
#// Using a single key and value:
#// 
#// add_query_arg( 'key', 'value', 'http://example.com' );
#// 
#// Using an associative array:
#// 
#// add_query_arg( array(
#// 'key1' => 'value1',
#// 'key2' => 'value2',
#// ), 'http://example.com' );
#// 
#// Omitting the URL from either use results in the current URL being used
#// (the value of `$_SERVER['REQUEST_URI']`).
#// 
#// Values are expected to be encoded appropriately with urlencode() or rawurlencode().
#// 
#// Setting any query variable's value to boolean false removes the key (see remove_query_arg()).
#// 
#// Important: The return value of add_query_arg() is not escaped by default. Output should be
#// late-escaped with esc_url() or similar to help prevent vulnerability to cross-site scripting
#// (XSS) attacks.
#// 
#// @since 1.5.0
#// @since 5.3.0 Formalized the existing and already documented parameters
#// by adding `...$args` to the function signature.
#// 
#// @param string|array $key   Either a query variable key, or an associative array of query variables.
#// @param string       $value Optional. Either a query variable value, or a URL to act upon.
#// @param string       $url   Optional. A URL to act upon.
#// @return string New URL query string (unescaped).
#//
def add_query_arg(*args):
    
    if php_is_array(args[0]):
        if php_count(args) < 2 or False == args[1]:
            uri = PHP_SERVER["REQUEST_URI"]
        else:
            uri = args[1]
        # end if
    else:
        if php_count(args) < 3 or False == args[2]:
            uri = PHP_SERVER["REQUEST_URI"]
        else:
            uri = args[2]
        # end if
    # end if
    frag = php_strstr(uri, "#")
    if frag:
        uri = php_substr(uri, 0, -php_strlen(frag))
    else:
        frag = ""
    # end if
    if 0 == php_stripos(uri, "http://"):
        protocol = "http://"
        uri = php_substr(uri, 7)
    elif 0 == php_stripos(uri, "https://"):
        protocol = "https://"
        uri = php_substr(uri, 8)
    else:
        protocol = ""
    # end if
    if php_strpos(uri, "?") != False:
        base, query = php_explode("?", uri, 2)
        base += "?"
    elif protocol or php_strpos(uri, "=") == False:
        base = uri + "?"
        query = ""
    else:
        base = ""
        query = uri
    # end if
    wp_parse_str(query, qs)
    qs = urlencode_deep(qs)
    #// This re-URL-encodes things that were already in the query string.
    if php_is_array(args[0]):
        for k,v in args[0]:
            qs[k] = v
        # end for
    else:
        qs[args[0]] = args[1]
    # end if
    for k,v in qs:
        if False == v:
            qs[k] = None
        # end if
    # end for
    ret = build_query(qs)
    ret = php_trim(ret, "?")
    ret = php_preg_replace("#=(&|$)#", "$1", ret)
    ret = protocol + base + ret + frag
    ret = php_rtrim(ret, "?")
    return ret
# end def add_query_arg
#// 
#// Removes an item or items from a query string.
#// 
#// @since 1.5.0
#// 
#// @param string|array $key   Query key or keys to remove.
#// @param bool|string  $query Optional. When false uses the current URL. Default false.
#// @return string New URL query string.
#//
def remove_query_arg(key=None, query=False, *args_):
    
    if php_is_array(key):
        #// Removing multiple keys.
        for k in key:
            query = add_query_arg(k, False, query)
        # end for
        return query
    # end if
    return add_query_arg(key, False, query)
# end def remove_query_arg
#// 
#// Returns an array of single-use query variable names that can be removed from a URL.
#// 
#// @since 4.4.0
#// 
#// @return string[] An array of parameters to remove from the URL.
#//
def wp_removable_query_args(*args_):
    
    removable_query_args = Array("activate", "activated", "approved", "deactivate", "deleted", "disabled", "doing_wp_cron", "enabled", "error", "hotkeys_highlight_first", "hotkeys_highlight_last", "locked", "message", "same", "saved", "settings-updated", "skipped", "spammed", "trashed", "unspammed", "untrashed", "update", "updated", "wp-post-new-reload")
    #// 
    #// Filters the list of query variables to remove.
    #// 
    #// @since 4.2.0
    #// 
    #// @param string[] $removable_query_args An array of query variables to remove from a URL.
    #//
    return apply_filters("removable_query_args", removable_query_args)
# end def wp_removable_query_args
#// 
#// Walks the array while sanitizing the contents.
#// 
#// @since 0.71
#// 
#// @param array $array Array to walk while sanitizing contents.
#// @return array Sanitized $array.
#//
def add_magic_quotes(array=None, *args_):
    
    for k,v in array:
        if php_is_array(v):
            array[k] = add_magic_quotes(v)
        else:
            array[k] = addslashes(v)
        # end if
    # end for
    return array
# end def add_magic_quotes
#// 
#// HTTP request for URI to retrieve content.
#// 
#// @since 1.5.1
#// 
#// @see wp_safe_remote_get()
#// 
#// @param string $uri URI/URL of web page to retrieve.
#// @return string|false HTTP content. False on failure.
#//
def wp_remote_fopen(uri=None, *args_):
    
    parsed_url = php_no_error(lambda: php_parse_url(uri))
    if (not parsed_url) or (not php_is_array(parsed_url)):
        return False
    # end if
    options = Array()
    options["timeout"] = 10
    response = wp_safe_remote_get(uri, options)
    if is_wp_error(response):
        return False
    # end if
    return wp_remote_retrieve_body(response)
# end def wp_remote_fopen
#// 
#// Set up the WordPress query.
#// 
#// @since 2.0.0
#// 
#// @global WP       $wp           Current WordPress environment instance.
#// @global WP_Query $wp_query     WordPress Query object.
#// @global WP_Query $wp_the_query Copy of the WordPress Query object.
#// 
#// @param string|array $query_vars Default WP_Query arguments.
#//
def wp(query_vars="", *args_):
    
    global wp,wp_query,wp_the_query
    php_check_if_defined("wp","wp_query","wp_the_query")
    wp.main(query_vars)
    if (not (php_isset(lambda : wp_the_query))):
        wp_the_query = wp_query
    # end if
# end def wp
#// 
#// Retrieve the description for the HTTP status.
#// 
#// @since 2.3.0
#// @since 3.9.0 Added status codes 418, 428, 429, 431, and 511.
#// @since 4.5.0 Added status codes 308, 421, and 451.
#// @since 5.1.0 Added status code 103.
#// 
#// @global array $wp_header_to_desc
#// 
#// @param int $code HTTP status code.
#// @return string Status description if found, an empty string otherwise.
#//
def get_status_header_desc(code=None, *args_):
    
    global wp_header_to_desc
    php_check_if_defined("wp_header_to_desc")
    code = absint(code)
    if (not (php_isset(lambda : wp_header_to_desc))):
        wp_header_to_desc = Array({100: "Continue", 101: "Switching Protocols", 102: "Processing", 103: "Early Hints", 200: "OK", 201: "Created", 202: "Accepted", 203: "Non-Authoritative Information", 204: "No Content", 205: "Reset Content", 206: "Partial Content", 207: "Multi-Status", 226: "IM Used", 300: "Multiple Choices", 301: "Moved Permanently", 302: "Found", 303: "See Other", 304: "Not Modified", 305: "Use Proxy", 306: "Reserved", 307: "Temporary Redirect", 308: "Permanent Redirect", 400: "Bad Request", 401: "Unauthorized", 402: "Payment Required", 403: "Forbidden", 404: "Not Found", 405: "Method Not Allowed", 406: "Not Acceptable", 407: "Proxy Authentication Required", 408: "Request Timeout", 409: "Conflict", 410: "Gone", 411: "Length Required", 412: "Precondition Failed", 413: "Request Entity Too Large", 414: "Request-URI Too Long", 415: "Unsupported Media Type", 416: "Requested Range Not Satisfiable", 417: "Expectation Failed", 418: "I'm a teapot", 421: "Misdirected Request", 422: "Unprocessable Entity", 423: "Locked", 424: "Failed Dependency", 426: "Upgrade Required", 428: "Precondition Required", 429: "Too Many Requests", 431: "Request Header Fields Too Large", 451: "Unavailable For Legal Reasons", 500: "Internal Server Error", 501: "Not Implemented", 502: "Bad Gateway", 503: "Service Unavailable", 504: "Gateway Timeout", 505: "HTTP Version Not Supported", 506: "Variant Also Negotiates", 507: "Insufficient Storage", 510: "Not Extended", 511: "Network Authentication Required"})
    # end if
    if (php_isset(lambda : wp_header_to_desc[code])):
        return wp_header_to_desc[code]
    else:
        return ""
    # end if
# end def get_status_header_desc
#// 
#// Set HTTP status header.
#// 
#// @since 2.0.0
#// @since 4.4.0 Added the `$description` parameter.
#// 
#// @see get_status_header_desc()
#// 
#// @param int    $code        HTTP status code.
#// @param string $description Optional. A custom description for the HTTP status.
#//
def status_header(code=None, description="", *args_):
    
    if (not description):
        description = get_status_header_desc(code)
    # end if
    if php_empty(lambda : description):
        return
    # end if
    protocol = wp_get_server_protocol()
    status_header = str(protocol) + str(" ") + str(code) + str(" ") + str(description)
    if php_function_exists("apply_filters"):
        #// 
        #// Filters an HTTP status header.
        #// 
        #// @since 2.2.0
        #// 
        #// @param string $status_header HTTP status header.
        #// @param int    $code          HTTP status code.
        #// @param string $description   Description for the status code.
        #// @param string $protocol      Server protocol.
        #//
        status_header = apply_filters("status_header", status_header, code, description, protocol)
    # end if
    if (not php_headers_sent()):
        php_header(status_header, True, code)
    # end if
# end def status_header
#// 
#// Get the header information to prevent caching.
#// 
#// The several different headers cover the different ways cache prevention
#// is handled by different browsers
#// 
#// @since 2.8.0
#// 
#// @return array The associative array of header names and field values.
#//
def wp_get_nocache_headers(*args_):
    
    headers = Array({"Expires": "Wed, 11 Jan 1984 05:00:00 GMT", "Cache-Control": "no-cache, must-revalidate, max-age=0"})
    if php_function_exists("apply_filters"):
        #// 
        #// Filters the cache-controlling headers.
        #// 
        #// @since 2.8.0
        #// 
        #// @see wp_get_nocache_headers()
        #// 
        #// @param array $headers {
        #// Header names and field values.
        #// 
        #// @type string $Expires       Expires header.
        #// @type string $Cache-Control Cache-Control header.
        #// }
        #//
        headers = apply_filters("nocache_headers", headers)
    # end if
    headers["Last-Modified"] = False
    return headers
# end def wp_get_nocache_headers
#// 
#// Set the headers to prevent caching for the different browsers.
#// 
#// Different browsers support different nocache headers, so several
#// headers must be sent so that all of them get the point that no
#// caching should occur.
#// 
#// @since 2.0.0
#// 
#// @see wp_get_nocache_headers()
#//
def nocache_headers(*args_):
    
    if php_headers_sent():
        return
    # end if
    headers = wp_get_nocache_headers()
    headers["Last-Modified"] = None
    php_header_remove("Last-Modified")
    for name,field_value in headers:
        php_header(str(name) + str(": ") + str(field_value))
    # end for
# end def nocache_headers
#// 
#// Set the headers for caching for 10 days with JavaScript content type.
#// 
#// @since 2.1.0
#//
def cache_javascript_headers(*args_):
    
    expiresOffset = 10 * DAY_IN_SECONDS
    php_header("Content-Type: text/javascript; charset=" + get_bloginfo("charset"))
    php_header("Vary: Accept-Encoding")
    #// Handle proxies.
    php_header("Expires: " + gmdate("D, d M Y H:i:s", time() + expiresOffset) + " GMT")
# end def cache_javascript_headers
#// 
#// Retrieve the number of database queries during the WordPress execution.
#// 
#// @since 2.0.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @return int Number of database queries.
#//
def get_num_queries(*args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    return wpdb.num_queries
# end def get_num_queries
#// 
#// Whether input is yes or no.
#// 
#// Must be 'y' to be true.
#// 
#// @since 1.0.0
#// 
#// @param string $yn Character string containing either 'y' (yes) or 'n' (no).
#// @return bool True if yes, false on anything else.
#//
def bool_from_yn(yn=None, *args_):
    
    return php_strtolower(yn) == "y"
# end def bool_from_yn
#// 
#// Load the feed template from the use of an action hook.
#// 
#// If the feed action does not have a hook, then the function will die with a
#// message telling the visitor that the feed is not valid.
#// 
#// It is better to only have one hook for each feed.
#// 
#// @since 2.1.0
#// 
#// @global WP_Query $wp_query WordPress Query object.
#//
def do_feed(*args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    feed = get_query_var("feed")
    #// Remove the pad, if present.
    feed = php_preg_replace("/^_+/", "", feed)
    if "" == feed or "feed" == feed:
        feed = get_default_feed()
    # end if
    if (not has_action(str("do_feed_") + str(feed))):
        wp_die(__("Error: This is not a valid feed template."), "", Array({"response": 404}))
    # end if
    #// 
    #// Fires once the given feed is loaded.
    #// 
    #// The dynamic portion of the hook name, `$feed`, refers to the feed template name.
    #// Possible values include: 'rdf', 'rss', 'rss2', and 'atom'.
    #// 
    #// @since 2.1.0
    #// @since 4.4.0 The `$feed` parameter was added.
    #// 
    #// @param bool   $is_comment_feed Whether the feed is a comment feed.
    #// @param string $feed            The feed name.
    #//
    do_action(str("do_feed_") + str(feed), wp_query.is_comment_feed, feed)
# end def do_feed
#// 
#// Load the RDF RSS 0.91 Feed template.
#// 
#// @since 2.1.0
#// 
#// @see load_template()
#//
def do_feed_rdf(*args_):
    
    load_template(ABSPATH + WPINC + "/feed-rdf.php")
# end def do_feed_rdf
#// 
#// Load the RSS 1.0 Feed Template.
#// 
#// @since 2.1.0
#// 
#// @see load_template()
#//
def do_feed_rss(*args_):
    
    load_template(ABSPATH + WPINC + "/feed-rss.php")
# end def do_feed_rss
#// 
#// Load either the RSS2 comment feed or the RSS2 posts feed.
#// 
#// @since 2.1.0
#// 
#// @see load_template()
#// 
#// @param bool $for_comments True for the comment feed, false for normal feed.
#//
def do_feed_rss2(for_comments=None, *args_):
    
    if for_comments:
        load_template(ABSPATH + WPINC + "/feed-rss2-comments.php")
    else:
        load_template(ABSPATH + WPINC + "/feed-rss2.php")
    # end if
# end def do_feed_rss2
#// 
#// Load either Atom comment feed or Atom posts feed.
#// 
#// @since 2.1.0
#// 
#// @see load_template()
#// 
#// @param bool $for_comments True for the comment feed, false for normal feed.
#//
def do_feed_atom(for_comments=None, *args_):
    
    if for_comments:
        load_template(ABSPATH + WPINC + "/feed-atom-comments.php")
    else:
        load_template(ABSPATH + WPINC + "/feed-atom.php")
    # end if
# end def do_feed_atom
#// 
#// Displays the default robots.txt file content.
#// 
#// @since 2.1.0
#// @since 5.3.0 Remove the "Disallow: /" output if search engine visiblity is
#// discouraged in favor of robots meta HTML tag in wp_no_robots().
#//
def do_robots(*args_):
    
    php_header("Content-Type: text/plain; charset=utf-8")
    #// 
    #// Fires when displaying the robots.txt file.
    #// 
    #// @since 2.1.0
    #//
    do_action("do_robotstxt")
    output = "User-agent: *\n"
    public = get_option("blog_public")
    site_url = php_parse_url(site_url())
    path = site_url["path"] if (not php_empty(lambda : site_url["path"])) else ""
    output += str("Disallow: ") + str(path) + str("/wp-admin/\n")
    output += str("Allow: ") + str(path) + str("/wp-admin/admin-ajax.php\n")
    #// 
    #// Filters the robots.txt output.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string $output The robots.txt output.
    #// @param bool   $public Whether the site is considered "public".
    #//
    php_print(apply_filters("robots_txt", output, public))
# end def do_robots
#// 
#// Display the favicon.ico file content.
#// 
#// @since 5.4.0
#//
def do_favicon(*args_):
    
    #// 
    #// Fires when serving the favicon.ico file.
    #// 
    #// @since 5.4.0
    #//
    do_action("do_faviconico")
    wp_redirect(get_site_icon_url(32, admin_url("images/w-logo-blue.png")))
    php_exit(0)
# end def do_favicon
#// 
#// Determines whether WordPress is already installed.
#// 
#// The cache will be checked first. If you have a cache plugin, which saves
#// the cache values, then this will work. If you use the default WordPress
#// cache, and the database goes away, then you might have problems.
#// 
#// Checks for the 'siteurl' option for whether WordPress is installed.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 2.1.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @return bool Whether the site is already installed.
#//
def is_blog_installed(*args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    #// 
    #// Check cache first. If options table goes away and we have true
    #// cached, oh well.
    #//
    if wp_cache_get("is_blog_installed"):
        return True
    # end if
    suppress = wpdb.suppress_errors()
    if (not wp_installing()):
        alloptions = wp_load_alloptions()
    # end if
    #// If siteurl is not set to autoload, check it specifically.
    if (not (php_isset(lambda : alloptions["siteurl"]))):
        installed = wpdb.get_var(str("SELECT option_value FROM ") + str(wpdb.options) + str(" WHERE option_name = 'siteurl'"))
    else:
        installed = alloptions["siteurl"]
    # end if
    wpdb.suppress_errors(suppress)
    installed = (not php_empty(lambda : installed))
    wp_cache_set("is_blog_installed", installed)
    if installed:
        return True
    # end if
    #// If visiting repair.php, return true and let it take over.
    if php_defined("WP_REPAIRING"):
        return True
    # end if
    suppress = wpdb.suppress_errors()
    #// 
    #// Loop over the WP tables. If none exist, then scratch installation is allowed.
    #// If one or more exist, suggest table repair since we got here because the
    #// options table could not be accessed.
    #//
    wp_tables = wpdb.tables()
    for table in wp_tables:
        #// The existence of custom user tables shouldn't suggest an insane state or prevent a clean installation.
        if php_defined("CUSTOM_USER_TABLE") and CUSTOM_USER_TABLE == table:
            continue
        # end if
        if php_defined("CUSTOM_USER_META_TABLE") and CUSTOM_USER_META_TABLE == table:
            continue
        # end if
        if (not wpdb.get_results(str("DESCRIBE ") + str(table) + str(";"))):
            continue
        # end if
        #// One or more tables exist. We are insane.
        wp_load_translations_early()
        #// Die with a DB error.
        wpdb.error = php_sprintf(__("One or more database tables are unavailable. The database may need to be <a href=\"%s\">repaired</a>."), "maint/repair.php?referrer=is_blog_installed")
        dead_db()
    # end for
    wpdb.suppress_errors(suppress)
    wp_cache_set("is_blog_installed", False)
    return False
# end def is_blog_installed
#// 
#// Retrieve URL with nonce added to URL query.
#// 
#// @since 2.0.4
#// 
#// @param string     $actionurl URL to add nonce action.
#// @param int|string $action    Optional. Nonce action name. Default -1.
#// @param string     $name      Optional. Nonce name. Default '_wpnonce'.
#// @return string Escaped URL with nonce action added.
#//
def wp_nonce_url(actionurl=None, action=-1, name="_wpnonce", *args_):
    
    actionurl = php_str_replace("&amp;", "&", actionurl)
    return esc_html(add_query_arg(name, wp_create_nonce(action), actionurl))
# end def wp_nonce_url
#// 
#// Retrieve or display nonce hidden field for forms.
#// 
#// The nonce field is used to validate that the contents of the form came from
#// the location on the current site and not somewhere else. The nonce does not
#// offer absolute protection, but should protect against most cases. It is very
#// important to use nonce field in forms.
#// 
#// The $action and $name are optional, but if you want to have better security,
#// it is strongly suggested to set those two parameters. It is easier to just
#// call the function without any parameters, because validation of the nonce
#// doesn't require any parameters, but since crackers know what the default is
#// it won't be difficult for them to find a way around your nonce and cause
#// damage.
#// 
#// The input name will be whatever $name value you gave. The input value will be
#// the nonce creation value.
#// 
#// @since 2.0.4
#// 
#// @param int|string $action  Optional. Action name. Default -1.
#// @param string     $name    Optional. Nonce name. Default '_wpnonce'.
#// @param bool       $referer Optional. Whether to set the referer field for validation. Default true.
#// @param bool       $echo    Optional. Whether to display or return hidden form field. Default true.
#// @return string Nonce field HTML markup.
#//
def wp_nonce_field(action=-1, name="_wpnonce", referer=True, echo=True, *args_):
    
    name = esc_attr(name)
    nonce_field = "<input type=\"hidden\" id=\"" + name + "\" name=\"" + name + "\" value=\"" + wp_create_nonce(action) + "\" />"
    if referer:
        nonce_field += wp_referer_field(False)
    # end if
    if echo:
        php_print(nonce_field)
    # end if
    return nonce_field
# end def wp_nonce_field
#// 
#// Retrieve or display referer hidden field for forms.
#// 
#// The referer link is the current Request URI from the server super global. The
#// input name is '_wp_http_referer', in case you wanted to check manually.
#// 
#// @since 2.0.4
#// 
#// @param bool $echo Optional. Whether to echo or return the referer field. Default true.
#// @return string Referer field HTML markup.
#//
def wp_referer_field(echo=True, *args_):
    
    referer_field = "<input type=\"hidden\" name=\"_wp_http_referer\" value=\"" + esc_attr(wp_unslash(PHP_SERVER["REQUEST_URI"])) + "\" />"
    if echo:
        php_print(referer_field)
    # end if
    return referer_field
# end def wp_referer_field
#// 
#// Retrieve or display original referer hidden field for forms.
#// 
#// The input name is '_wp_original_http_referer' and will be either the same
#// value of wp_referer_field(), if that was posted already or it will be the
#// current page, if it doesn't exist.
#// 
#// @since 2.0.4
#// 
#// @param bool   $echo         Optional. Whether to echo the original http referer. Default true.
#// @param string $jump_back_to Optional. Can be 'previous' or page you want to jump back to.
#// Default 'current'.
#// @return string Original referer field.
#//
def wp_original_referer_field(echo=True, jump_back_to="current", *args_):
    
    ref = wp_get_original_referer()
    if (not ref):
        ref = wp_get_referer() if "previous" == jump_back_to else wp_unslash(PHP_SERVER["REQUEST_URI"])
    # end if
    orig_referer_field = "<input type=\"hidden\" name=\"_wp_original_http_referer\" value=\"" + esc_attr(ref) + "\" />"
    if echo:
        php_print(orig_referer_field)
    # end if
    return orig_referer_field
# end def wp_original_referer_field
#// 
#// Retrieve referer from '_wp_http_referer' or HTTP referer.
#// 
#// If it's the same as the current request URL, will return false.
#// 
#// @since 2.0.4
#// 
#// @return string|false Referer URL on success, false on failure.
#//
def wp_get_referer(*args_):
    
    if (not php_function_exists("wp_validate_redirect")):
        return False
    # end if
    ref = wp_get_raw_referer()
    if ref and wp_unslash(PHP_SERVER["REQUEST_URI"]) != ref and home_url() + wp_unslash(PHP_SERVER["REQUEST_URI"]) != ref:
        return wp_validate_redirect(ref, False)
    # end if
    return False
# end def wp_get_referer
#// 
#// Retrieves unvalidated referer from '_wp_http_referer' or HTTP referer.
#// 
#// Do not use for redirects, use wp_get_referer() instead.
#// 
#// @since 4.5.0
#// 
#// @return string|false Referer URL on success, false on failure.
#//
def wp_get_raw_referer(*args_):
    
    if (not php_empty(lambda : PHP_REQUEST["_wp_http_referer"])):
        return wp_unslash(PHP_REQUEST["_wp_http_referer"])
    elif (not php_empty(lambda : PHP_SERVER["HTTP_REFERER"])):
        return wp_unslash(PHP_SERVER["HTTP_REFERER"])
    # end if
    return False
# end def wp_get_raw_referer
#// 
#// Retrieve original referer that was posted, if it exists.
#// 
#// @since 2.0.4
#// 
#// @return string|false False if no original referer or original referer if set.
#//
def wp_get_original_referer(*args_):
    
    if (not php_empty(lambda : PHP_REQUEST["_wp_original_http_referer"])) and php_function_exists("wp_validate_redirect"):
        return wp_validate_redirect(wp_unslash(PHP_REQUEST["_wp_original_http_referer"]), False)
    # end if
    return False
# end def wp_get_original_referer
#// 
#// Recursive directory creation based on full path.
#// 
#// Will attempt to set permissions on folders.
#// 
#// @since 2.0.1
#// 
#// @param string $target Full path to attempt to create.
#// @return bool Whether the path was created. True if path already exists.
#//
def wp_mkdir_p(target=None, *args_):
    
    wrapper = None
    #// Strip the protocol.
    if wp_is_stream(target):
        wrapper, target = php_explode("://", target, 2)
    # end if
    #// From php.net/mkdir user contributed notes.
    target = php_str_replace("//", "/", target)
    #// Put the wrapper back on the target.
    if None != wrapper:
        target = wrapper + "://" + target
    # end if
    #// 
    #// Safe mode fails with a trailing slash under certain PHP versions.
    #// Use rtrim() instead of untrailingslashit to avoid formatting.php dependency.
    #//
    target = php_rtrim(target, "/")
    if php_empty(lambda : target):
        target = "/"
    # end if
    if php_file_exists(target):
        return php_no_error(lambda: php_is_dir(target))
    # end if
    #// Do not allow path traversals.
    if False != php_strpos(target, "../") or False != php_strpos(target, ".." + DIRECTORY_SEPARATOR):
        return False
    # end if
    #// We need to find the permissions of the parent folder that exists and inherit that.
    target_parent = php_dirname(target)
    while True:
        
        if not ("." != target_parent and (not php_is_dir(target_parent)) and php_dirname(target_parent) != target_parent):
            break
        # end if
        target_parent = php_dirname(target_parent)
    # end while
    #// Get the permission bits.
    stat = php_no_error(lambda: stat(target_parent))
    if stat:
        dir_perms = stat["mode"] & 4095
    else:
        dir_perms = 511
    # end if
    if php_no_error(lambda: mkdir(target, dir_perms, True)):
        #// 
        #// If a umask is set that modifies $dir_perms, we'll have to re-set
        #// the $dir_perms correctly with chmod()
        #//
        if dir_perms & (1 << (umask()).bit_length()) - 1 - umask() != dir_perms:
            folder_parts = php_explode("/", php_substr(target, php_strlen(target_parent) + 1))
            i = 1
            c = php_count(folder_parts)
            while i <= c:
                
                chmod(target_parent + "/" + php_implode("/", php_array_slice(folder_parts, 0, i)), dir_perms)
                i += 1
            # end while
        # end if
        return True
    # end if
    return False
# end def wp_mkdir_p
#// 
#// Test if a given filesystem path is absolute.
#// 
#// For example, '/foo/bar', or 'c:\windows'.
#// 
#// @since 2.5.0
#// 
#// @param string $path File path.
#// @return bool True if path is absolute, false is not absolute.
#//
def path_is_absolute(path=None, *args_):
    
    #// 
    #// Check to see if the path is a stream and check to see if its an actual
    #// path or file as realpath() does not support stream wrappers.
    #//
    if wp_is_stream(path) and php_is_dir(path) or php_is_file(path):
        return True
    # end if
    #// 
    #// This is definitive if true but fails if $path does not exist or contains
    #// a symbolic link.
    #//
    if php_realpath(path) == path:
        return True
    # end if
    if php_strlen(path) == 0 or "." == path[0]:
        return False
    # end if
    #// Windows allows absolute paths like this.
    if php_preg_match("#^[a-zA-Z]:\\\\#", path):
        return True
    # end if
    #// A path starting with / or \ is absolute; anything else is relative.
    return "/" == path[0] or "\\" == path[0]
# end def path_is_absolute
#// 
#// Join two filesystem paths together.
#// 
#// For example, 'give me $path relative to $base'. If the $path is absolute,
#// then it the full path is returned.
#// 
#// @since 2.5.0
#// 
#// @param string $base Base path.
#// @param string $path Path relative to $base.
#// @return string The path with the base or absolute path.
#//
def path_join(base=None, path=None, *args_):
    
    if path_is_absolute(path):
        return path
    # end if
    return php_rtrim(base, "/") + "/" + php_ltrim(path, "/")
# end def path_join
#// 
#// Normalize a filesystem path.
#// 
#// On windows systems, replaces backslashes with forward slashes
#// and forces upper-case drive letters.
#// Allows for two leading slashes for Windows network shares, but
#// ensures that all other duplicate slashes are reduced to a single.
#// 
#// @since 3.9.0
#// @since 4.4.0 Ensures upper-case drive letters on Windows systems.
#// @since 4.5.0 Allows for Windows network shares.
#// @since 4.9.7 Allows for PHP file wrappers.
#// 
#// @param string $path Path to normalize.
#// @return string Normalized path.
#//
def wp_normalize_path(path=None, *args_):
    
    wrapper = ""
    if wp_is_stream(path):
        wrapper, path = php_explode("://", path, 2)
        wrapper += "://"
    # end if
    #// Standardise all paths to use '/'.
    path = php_str_replace("\\", "/", path)
    #// Replace multiple slashes down to a singular, allowing for network shares having two slashes.
    path = php_preg_replace("|(?<=.)/+|", "/", path)
    #// Windows paths should uppercase the drive letter.
    if ":" == php_substr(path, 1, 1):
        path = ucfirst(path)
    # end if
    return wrapper + path
# end def wp_normalize_path
#// 
#// Determine a writable directory for temporary files.
#// 
#// Function's preference is the return value of sys_get_temp_dir(),
#// followed by your PHP temporary upload directory, followed by WP_CONTENT_DIR,
#// before finally defaulting to /tmp
#// 
#// In the event that this function does not find a writable location,
#// It may be overridden by the WP_TEMP_DIR constant in your wp-config.php file.
#// 
#// @since 2.5.0
#// 
#// @staticvar string $temp
#// 
#// @return string Writable temporary directory.
#//
def get_temp_dir(*args_):
    
    temp = ""
    if php_defined("WP_TEMP_DIR"):
        return trailingslashit(WP_TEMP_DIR)
    # end if
    if temp:
        return trailingslashit(temp)
    # end if
    if php_function_exists("sys_get_temp_dir"):
        temp = php_sys_get_temp_dir()
        if php_no_error(lambda: php_is_dir(temp)) and wp_is_writable(temp):
            return trailingslashit(temp)
        # end if
    # end if
    temp = php_ini_get("upload_tmp_dir")
    if php_no_error(lambda: php_is_dir(temp)) and wp_is_writable(temp):
        return trailingslashit(temp)
    # end if
    temp = WP_CONTENT_DIR + "/"
    if php_is_dir(temp) and wp_is_writable(temp):
        return temp
    # end if
    return "/tmp/"
# end def get_temp_dir
#// 
#// Determine if a directory is writable.
#// 
#// This function is used to work around certain ACL issues in PHP primarily
#// affecting Windows Servers.
#// 
#// @since 3.6.0
#// 
#// @see win_is_writable()
#// 
#// @param string $path Path to check for write-ability.
#// @return bool Whether the path is writable.
#//
def wp_is_writable(path=None, *args_):
    
    if "WIN" == php_strtoupper(php_substr(PHP_OS, 0, 3)):
        return win_is_writable(path)
    else:
        return php_no_error(lambda: php_is_writable(path))
    # end if
# end def wp_is_writable
#// 
#// Workaround for Windows bug in is_writable() function
#// 
#// PHP has issues with Windows ACL's for determine if a
#// directory is writable or not, this works around them by
#// checking the ability to open files rather than relying
#// upon PHP to interprate the OS ACL.
#// 
#// @since 2.8.0
#// 
#// @see https://bugs.php.net/bug.php?id=27609
#// @see https://bugs.php.net/bug.php?id=30931
#// 
#// @param string $path Windows path to check for write-ability.
#// @return bool Whether the path is writable.
#//
def win_is_writable(path=None, *args_):
    
    if "/" == path[php_strlen(path) - 1]:
        #// If it looks like a directory, check a random file within the directory.
        return win_is_writable(path + uniqid(mt_rand()) + ".tmp")
    elif php_is_dir(path):
        #// If it's a directory (and not a file), check a random file within the directory.
        return win_is_writable(path + "/" + uniqid(mt_rand()) + ".tmp")
    # end if
    #// Check tmp file for read/write capabilities.
    should_delete_tmp_file = (not php_file_exists(path))
    f = php_no_error(lambda: fopen(path, "a"))
    if False == f:
        return False
    # end if
    php_fclose(f)
    if should_delete_tmp_file:
        unlink(path)
    # end if
    return True
# end def win_is_writable
#// 
#// Retrieves uploads directory information.
#// 
#// Same as wp_upload_dir() but "light weight" as it doesn't attempt to create the uploads directory.
#// Intended for use in themes, when only 'basedir' and 'baseurl' are needed, generally in all cases
#// when not uploading files.
#// 
#// @since 4.5.0
#// 
#// @see wp_upload_dir()
#// 
#// @return array See wp_upload_dir() for description.
#//
def wp_get_upload_dir(*args_):
    
    return wp_upload_dir(None, False)
# end def wp_get_upload_dir
#// 
#// Returns an array containing the current upload directory's path and URL.
#// 
#// Checks the 'upload_path' option, which should be from the web root folder,
#// and if it isn't empty it will be used. If it is empty, then the path will be
#// 'WP_CONTENT_DIR/uploads'. If the 'UPLOADS' constant is defined, then it will
#// override the 'upload_path' option and 'WP_CONTENT_DIR/uploads' path.
#// 
#// The upload URL path is set either by the 'upload_url_path' option or by using
#// the 'WP_CONTENT_URL' constant and appending '/uploads' to the path.
#// 
#// If the 'uploads_use_yearmonth_folders' is set to true (checkbox if checked in
#// the administration settings panel), then the time will be used. The format
#// will be year first and then month.
#// 
#// If the path couldn't be created, then an error will be returned with the key
#// 'error' containing the error message. The error suggests that the parent
#// directory is not writable by the server.
#// 
#// @since 2.0.0
#// @uses _wp_upload_dir()
#// 
#// @staticvar array $cache
#// @staticvar array $tested_paths
#// 
#// @param string $time Optional. Time formatted in 'yyyy/mm'. Default null.
#// @param bool   $create_dir Optional. Whether to check and create the uploads directory.
#// Default true for backward compatibility.
#// @param bool   $refresh_cache Optional. Whether to refresh the cache. Default false.
#// @return array {
#// Array of information about the upload directory.
#// 
#// @type string       $path    Base directory and subdirectory or full path to upload directory.
#// @type string       $url     Base URL and subdirectory or absolute URL to upload directory.
#// @type string       $subdir  Subdirectory if uploads use year/month folders option is on.
#// @type string       $basedir Path without subdir.
#// @type string       $baseurl URL path without subdir.
#// @type string|false $error   False or error message.
#// }
#//
def wp_upload_dir(time=None, create_dir=True, refresh_cache=False, *args_):
    
    cache = Array()
    tested_paths = Array()
    key = php_sprintf("%d-%s", get_current_blog_id(), php_str(time))
    if refresh_cache or php_empty(lambda : cache[key]):
        cache[key] = _wp_upload_dir(time)
    # end if
    #// 
    #// Filters the uploads directory data.
    #// 
    #// @since 2.0.0
    #// 
    #// @param array $uploads {
    #// Array of information about the upload directory.
    #// 
    #// @type string       $path    Base directory and subdirectory or full path to upload directory.
    #// @type string       $url     Base URL and subdirectory or absolute URL to upload directory.
    #// @type string       $subdir  Subdirectory if uploads use year/month folders option is on.
    #// @type string       $basedir Path without subdir.
    #// @type string       $baseurl URL path without subdir.
    #// @type string|false $error   False or error message.
    #// }
    #//
    uploads = apply_filters("upload_dir", cache[key])
    if create_dir:
        path = uploads["path"]
        if php_array_key_exists(path, tested_paths):
            uploads["error"] = tested_paths[path]
        else:
            if (not wp_mkdir_p(path)):
                if 0 == php_strpos(uploads["basedir"], ABSPATH):
                    error_path = php_str_replace(ABSPATH, "", uploads["basedir"]) + uploads["subdir"]
                else:
                    error_path = wp_basename(uploads["basedir"]) + uploads["subdir"]
                # end if
                uploads["error"] = php_sprintf(__("Unable to create directory %s. Is its parent directory writable by the server?"), esc_html(error_path))
            # end if
            tested_paths[path] = uploads["error"]
        # end if
    # end if
    return uploads
# end def wp_upload_dir
#// 
#// A non-filtered, non-cached version of wp_upload_dir() that doesn't check the path.
#// 
#// @since 4.5.0
#// @access private
#// 
#// @param string $time Optional. Time formatted in 'yyyy/mm'. Default null.
#// @return array See wp_upload_dir()
#//
def _wp_upload_dir(time=None, *args_):
    
    siteurl = get_option("siteurl")
    upload_path = php_trim(get_option("upload_path"))
    if php_empty(lambda : upload_path) or "wp-content/uploads" == upload_path:
        dir = WP_CONTENT_DIR + "/uploads"
    elif 0 != php_strpos(upload_path, ABSPATH):
        #// $dir is absolute, $upload_path is (maybe) relative to ABSPATH.
        dir = path_join(ABSPATH, upload_path)
    else:
        dir = upload_path
    # end if
    url = get_option("upload_url_path")
    if (not url):
        if php_empty(lambda : upload_path) or "wp-content/uploads" == upload_path or upload_path == dir:
            url = WP_CONTENT_URL + "/uploads"
        else:
            url = trailingslashit(siteurl) + upload_path
        # end if
    # end if
    #// 
    #// Honor the value of UPLOADS. This happens as long as ms-files rewriting is disabled.
    #// We also sometimes obey UPLOADS when rewriting is enabled -- see the next block.
    #//
    if php_defined("UPLOADS") and (not is_multisite() and get_site_option("ms_files_rewriting")):
        dir = ABSPATH + UPLOADS
        url = trailingslashit(siteurl) + UPLOADS
    # end if
    #// If multisite (and if not the main site in a post-MU network).
    if is_multisite() and (not is_main_network() and is_main_site() and php_defined("MULTISITE")):
        if (not get_site_option("ms_files_rewriting")):
            #// 
            #// If ms-files rewriting is disabled (networks created post-3.5), it is fairly
            #// straightforward: Append sites/%d if we're not on the main site (for post-MU
            #// networks). (The extra directory prevents a four-digit ID from conflicting with
            #// a year-based directory for the main site. But if a MU-era network has disabled
            #// ms-files rewriting manually, they don't need the extra directory, as they never
            #// had wp-content/uploads for the main site.)
            #//
            if php_defined("MULTISITE"):
                ms_dir = "/sites/" + get_current_blog_id()
            else:
                ms_dir = "/" + get_current_blog_id()
            # end if
            dir += ms_dir
            url += ms_dir
        elif php_defined("UPLOADS") and (not ms_is_switched()):
            #// 
            #// Handle the old-form ms-files.php rewriting if the network still has that enabled.
            #// When ms-files rewriting is enabled, then we only listen to UPLOADS when:
            #// 1) We are not on the main site in a post-MU network, as wp-content/uploads is used
            #// there, and
            #// 2) We are not switched, as ms_upload_constants() hardcodes these constants to reflect
            #// the original blog ID.
            #// 
            #// Rather than UPLOADS, we actually use BLOGUPLOADDIR if it is set, as it is absolute.
            #// (And it will be set, see ms_upload_constants().) Otherwise, UPLOADS can be used, as
            #// as it is relative to ABSPATH. For the final piece: when UPLOADS is used with ms-files
            #// rewriting in multisite, the resulting URL is /files. (#WP22702 for background.)
            #//
            if php_defined("BLOGUPLOADDIR"):
                dir = untrailingslashit(BLOGUPLOADDIR)
            else:
                dir = ABSPATH + UPLOADS
            # end if
            url = trailingslashit(siteurl) + "files"
        # end if
    # end if
    basedir = dir
    baseurl = url
    subdir = ""
    if get_option("uploads_use_yearmonth_folders"):
        #// Generate the yearly and monthly directories.
        if (not time):
            time = current_time("mysql")
        # end if
        y = php_substr(time, 0, 4)
        m = php_substr(time, 5, 2)
        subdir = str("/") + str(y) + str("/") + str(m)
    # end if
    dir += subdir
    url += subdir
    return Array({"path": dir, "url": url, "subdir": subdir, "basedir": basedir, "baseurl": baseurl, "error": False})
# end def _wp_upload_dir
#// 
#// Get a filename that is sanitized and unique for the given directory.
#// 
#// If the filename is not unique, then a number will be added to the filename
#// before the extension, and will continue adding numbers until the filename is
#// unique.
#// 
#// The callback is passed three parameters, the first one is the directory, the
#// second is the filename, and the third is the extension.
#// 
#// @since 2.5.0
#// 
#// @param string   $dir                      Directory.
#// @param string   $filename                 File name.
#// @param callable $unique_filename_callback Callback. Default null.
#// @return string New filename, if given wasn't unique.
#//
def wp_unique_filename(dir=None, filename=None, unique_filename_callback=None, *args_):
    
    #// Sanitize the file name before we begin processing.
    filename = sanitize_file_name(filename)
    ext2 = None
    #// Separate the filename into a name and extension.
    ext = pathinfo(filename, PATHINFO_EXTENSION)
    name = pathinfo(filename, PATHINFO_BASENAME)
    if ext:
        ext = "." + ext
    # end if
    #// Edge case: if file is named '.ext', treat as an empty name.
    if name == ext:
        name = ""
    # end if
    #// 
    #// Increment the file number until we have a unique file to save in $dir.
    #// Use callback if supplied.
    #//
    if unique_filename_callback and php_is_callable(unique_filename_callback):
        filename = php_call_user_func(unique_filename_callback, dir, name, ext)
    else:
        number = ""
        fname = pathinfo(filename, PATHINFO_FILENAME)
        #// Always append a number to file names that can potentially match image sub-size file names.
        if fname and php_preg_match("/-(?:\\d+x\\d+|scaled|rotated)$/", fname):
            number = 1
            #// At this point the file name may not be unique. This is tested below and the $number is incremented.
            filename = php_str_replace(str(fname) + str(ext), str(fname) + str("-") + str(number) + str(ext), filename)
        # end if
        #// Change '.ext' to lower case.
        if ext and php_strtolower(ext) != ext:
            ext2 = php_strtolower(ext)
            filename2 = php_preg_replace("|" + preg_quote(ext) + "$|", ext2, filename)
            #// Check for both lower and upper case extension or image sub-sizes may be overwritten.
            while True:
                
                if not (php_file_exists(dir + str("/") + str(filename)) or php_file_exists(dir + str("/") + str(filename2))):
                    break
                # end if
                new_number = php_int(number) + 1
                filename = php_str_replace(Array(str("-") + str(number) + str(ext), str(number) + str(ext)), str("-") + str(new_number) + str(ext), filename)
                filename2 = php_str_replace(Array(str("-") + str(number) + str(ext2), str(number) + str(ext2)), str("-") + str(new_number) + str(ext2), filename2)
                number = new_number
            # end while
            filename = filename2
        else:
            while True:
                
                if not (php_file_exists(dir + str("/") + str(filename))):
                    break
                # end if
                new_number = php_int(number) + 1
                if "" == str(number) + str(ext):
                    filename = str(filename) + str("-") + str(new_number)
                else:
                    filename = php_str_replace(Array(str("-") + str(number) + str(ext), str(number) + str(ext)), str("-") + str(new_number) + str(ext), filename)
                # end if
                number = new_number
            # end while
        # end if
        #// Prevent collisions with existing file names that contain dimension-like strings
        #// (whether they are subsizes or originals uploaded prior to #42437).
        upload_dir = wp_get_upload_dir()
        #// The (resized) image files would have name and extension, and will be in the uploads dir.
        if name and ext and php_no_error(lambda: php_is_dir(dir)) and False != php_strpos(dir, upload_dir["basedir"]):
            #// List of all files and directories contained in $dir.
            files = php_no_error(lambda: scandir(dir))
            if (not php_empty(lambda : files)):
                #// Remove "dot" dirs.
                files = php_array_diff(files, Array(".", ".."))
            # end if
            if (not php_empty(lambda : files)):
                #// The extension case may have changed above.
                new_ext = ext2 if (not php_empty(lambda : ext2)) else ext
                #// Ensure this never goes into infinite loop
                #// as it uses pathinfo() and regex in the check, but string replacement for the changes.
                count = php_count(files)
                i = 0
                while True:
                    
                    if not (i <= count and _wp_check_existing_file_names(filename, files)):
                        break
                    # end if
                    new_number = php_int(number) + 1
                    filename = php_str_replace(Array(str("-") + str(number) + str(new_ext), str(number) + str(new_ext)), str("-") + str(new_number) + str(new_ext), filename)
                    number = new_number
                    i += 1
                # end while
            # end if
        # end if
    # end if
    #// 
    #// Filters the result when generating a unique file name.
    #// 
    #// @since 4.5.0
    #// 
    #// @param string        $filename                 Unique file name.
    #// @param string        $ext                      File extension, eg. ".png".
    #// @param string        $dir                      Directory path.
    #// @param callable|null $unique_filename_callback Callback function that generates the unique file name.
    #//
    return apply_filters("wp_unique_filename", filename, ext, dir, unique_filename_callback)
# end def wp_unique_filename
#// 
#// Helper function to check if a file name could match an existing image sub-size file name.
#// 
#// @since 5.3.1
#// @access private
#// 
#// @param string $filename The file name to check.
#// $param array  $files    An array of existing files in the directory.
#// $return bool True if the tested file name could match an existing file, false otherwise.
#//
def _wp_check_existing_file_names(filename=None, files=None, *args_):
    
    fname = pathinfo(filename, PATHINFO_FILENAME)
    ext = pathinfo(filename, PATHINFO_EXTENSION)
    #// Edge case, file names like `.ext`.
    if php_empty(lambda : fname):
        return False
    # end if
    if ext:
        ext = str(".") + str(ext)
    # end if
    regex = "/^" + preg_quote(fname) + "-(?:\\d+x\\d+|scaled|rotated)" + preg_quote(ext) + "$/i"
    for file in files:
        if php_preg_match(regex, file):
            return True
        # end if
    # end for
    return False
# end def _wp_check_existing_file_names
#// 
#// Create a file in the upload folder with given content.
#// 
#// If there is an error, then the key 'error' will exist with the error message.
#// If success, then the key 'file' will have the unique file path, the 'url' key
#// will have the link to the new file. and the 'error' key will be set to false.
#// 
#// This function will not move an uploaded file to the upload folder. It will
#// create a new file with the content in $bits parameter. If you move the upload
#// file, read the content of the uploaded file, and then you can give the
#// filename and content to this function, which will add it to the upload
#// folder.
#// 
#// The permissions will be set on the new file automatically by this function.
#// 
#// @since 2.0.0
#// 
#// @param string       $name       Filename.
#// @param null|string  $deprecated Never used. Set to null.
#// @param string       $bits       File content
#// @param string       $time       Optional. Time formatted in 'yyyy/mm'. Default null.
#// @return array
#//
def wp_upload_bits(name=None, deprecated=None, bits=None, time=None, *args_):
    
    if (not php_empty(lambda : deprecated)):
        _deprecated_argument(__FUNCTION__, "2.0.0")
    # end if
    if php_empty(lambda : name):
        return Array({"error": __("Empty filename")})
    # end if
    wp_filetype = wp_check_filetype(name)
    if (not wp_filetype["ext"]) and (not current_user_can("unfiltered_upload")):
        return Array({"error": __("Sorry, this file type is not permitted for security reasons.")})
    # end if
    upload = wp_upload_dir(time)
    if False != upload["error"]:
        return upload
    # end if
    #// 
    #// Filters whether to treat the upload bits as an error.
    #// 
    #// Returning a non-array from the filter will effectively short-circuit preparing the upload
    #// bits, returning that value instead. An error message should be returned as a string.
    #// 
    #// @since 3.0.0
    #// 
    #// @param array|string $upload_bits_error An array of upload bits data, or error message to return.
    #//
    upload_bits_error = apply_filters("wp_upload_bits", Array({"name": name, "bits": bits, "time": time}))
    if (not php_is_array(upload_bits_error)):
        upload["error"] = upload_bits_error
        return upload
    # end if
    filename = wp_unique_filename(upload["path"], name)
    new_file = upload["path"] + str("/") + str(filename)
    if (not wp_mkdir_p(php_dirname(new_file))):
        if 0 == php_strpos(upload["basedir"], ABSPATH):
            error_path = php_str_replace(ABSPATH, "", upload["basedir"]) + upload["subdir"]
        else:
            error_path = wp_basename(upload["basedir"]) + upload["subdir"]
        # end if
        message = php_sprintf(__("Unable to create directory %s. Is its parent directory writable by the server?"), error_path)
        return Array({"error": message})
    # end if
    ifp = php_no_error(lambda: fopen(new_file, "wb"))
    if (not ifp):
        return Array({"error": php_sprintf(__("Could not write file %s"), new_file)})
    # end if
    fwrite(ifp, bits)
    php_fclose(ifp)
    clearstatcache()
    #// Set correct file permissions.
    stat = php_no_error(lambda: stat(php_dirname(new_file)))
    perms = stat["mode"] & 4095
    perms = perms & 438
    chmod(new_file, perms)
    clearstatcache()
    #// Compute the URL.
    url = upload["url"] + str("/") + str(filename)
    #// This filter is documented in wp-admin/includes/file.php
    return apply_filters("wp_handle_upload", Array({"file": new_file, "url": url, "type": wp_filetype["type"], "error": False}), "sideload")
# end def wp_upload_bits
#// 
#// Retrieve the file type based on the extension name.
#// 
#// @since 2.5.0
#// 
#// @param string $ext The extension to search.
#// @return string|void The file type, example: audio, video, document, spreadsheet, etc.
#//
def wp_ext2type(ext=None, *args_):
    
    ext = php_strtolower(ext)
    ext2type = wp_get_ext_types()
    for type,exts in ext2type:
        if php_in_array(ext, exts):
            return type
        # end if
    # end for
# end def wp_ext2type
#// 
#// Retrieve the file type from the file name.
#// 
#// You can optionally define the mime array, if needed.
#// 
#// @since 2.0.4
#// 
#// @param string   $filename File name or path.
#// @param string[] $mimes    Optional. Array of mime types keyed by their file extension regex.
#// @return array {
#// Values for the extension and mime type.
#// 
#// @type string|false $ext  File extension, or false if the file doesn't match a mime type.
#// @type string|false $type File mime type, or false if the file doesn't match a mime type.
#// }
#//
def wp_check_filetype(filename=None, mimes=None, *args_):
    
    if php_empty(lambda : mimes):
        mimes = get_allowed_mime_types()
    # end if
    type = False
    ext = False
    for ext_preg,mime_match in mimes:
        ext_preg = "!\\.(" + ext_preg + ")$!i"
        if php_preg_match(ext_preg, filename, ext_matches):
            type = mime_match
            ext = ext_matches[1]
            break
        # end if
    # end for
    return compact("ext", "type")
# end def wp_check_filetype
#// 
#// Attempt to determine the real file type of a file.
#// 
#// If unable to, the file name extension will be used to determine type.
#// 
#// If it's determined that the extension does not match the file's real type,
#// then the "proper_filename" value will be set with a proper filename and extension.
#// 
#// Currently this function only supports renaming images validated via wp_get_image_mime().
#// 
#// @since 3.0.0
#// 
#// @param string   $file     Full path to the file.
#// @param string   $filename The name of the file (may differ from $file due to $file being
#// in a tmp directory).
#// @param string[] $mimes    Optional. Array of mime types keyed by their file extension regex.
#// @return array {
#// Values for the extension, mime type, and corrected filename.
#// 
#// @type string|false $ext             File extension, or false if the file doesn't match a mime type.
#// @type string|false $type            File mime type, or false if the file doesn't match a mime type.
#// @type string|false $proper_filename File name with its correct extension, or false if it cannot be determined.
#// }
#//
def wp_check_filetype_and_ext(file=None, filename=None, mimes=None, *args_):
    
    proper_filename = False
    #// Do basic extension validation and MIME mapping.
    wp_filetype = wp_check_filetype(filename, mimes)
    ext = wp_filetype["ext"]
    type = wp_filetype["type"]
    #// We can't do any further validation without a file to work with.
    if (not php_file_exists(file)):
        return compact("ext", "type", "proper_filename")
    # end if
    real_mime = False
    #// Validate image types.
    if type and 0 == php_strpos(type, "image/"):
        #// Attempt to figure out what type of image it actually is.
        real_mime = wp_get_image_mime(file)
        if real_mime and real_mime != type:
            #// 
            #// Filters the list mapping image mime types to their respective extensions.
            #// 
            #// @since 3.0.0
            #// 
            #// @param  array $mime_to_ext Array of image mime types and their matching extensions.
            #//
            mime_to_ext = apply_filters("getimagesize_mimes_to_exts", Array({"image/jpeg": "jpg", "image/png": "png", "image/gif": "gif", "image/bmp": "bmp", "image/tiff": "tif"}))
            #// Replace whatever is after the last period in the filename with the correct extension.
            if (not php_empty(lambda : mime_to_ext[real_mime])):
                filename_parts = php_explode(".", filename)
                php_array_pop(filename_parts)
                filename_parts[-1] = mime_to_ext[real_mime]
                new_filename = php_implode(".", filename_parts)
                if new_filename != filename:
                    proper_filename = new_filename
                    pass
                # end if
                #// Redefine the extension / MIME.
                wp_filetype = wp_check_filetype(new_filename, mimes)
                ext = wp_filetype["ext"]
                type = wp_filetype["type"]
            else:
                #// Reset $real_mime and try validating again.
                real_mime = False
            # end if
        # end if
    # end if
    #// Validate files that didn't get validated during previous checks.
    if type and (not real_mime) and php_extension_loaded("fileinfo"):
        finfo = finfo_open(FILEINFO_MIME_TYPE)
        real_mime = finfo_file(finfo, file)
        finfo_close(finfo)
        #// fileinfo often misidentifies obscure files as one of these types.
        nonspecific_types = Array("application/octet-stream", "application/encrypted", "application/CDFV2-encrypted", "application/zip")
        #// 
        #// If $real_mime doesn't match the content type we're expecting from the file's extension,
        #// we need to do some additional vetting. Media types and those listed in $nonspecific_types are
        #// allowed some leeway, but anything else must exactly match the real content type.
        #//
        if php_in_array(real_mime, nonspecific_types, True):
            #// File is a non-specific binary type. That's ok if it's a type that generally tends to be binary.
            if (not php_in_array(php_substr(type, 0, strcspn(type, "/")), Array("application", "video", "audio"))):
                type = False
                ext = False
            # end if
        elif 0 == php_strpos(real_mime, "video/") or 0 == php_strpos(real_mime, "audio/"):
            #// 
            #// For these types, only the major type must match the real value.
            #// This means that common mismatches are forgiven: application/vnd.apple.numbers is often misidentified as application/zip,
            #// and some media files are commonly named with the wrong extension (.mov instead of .mp4)
            #//
            if php_substr(real_mime, 0, strcspn(real_mime, "/")) != php_substr(type, 0, strcspn(type, "/")):
                type = False
                ext = False
            # end if
        elif "text/plain" == real_mime:
            #// A few common file types are occasionally detected as text/plain; allow those.
            if (not php_in_array(type, Array("text/plain", "text/csv", "text/richtext", "text/tsv", "text/vtt"))):
                type = False
                ext = False
            # end if
        elif "text/rtf" == real_mime:
            #// Special casing for RTF files.
            if (not php_in_array(type, Array("text/rtf", "text/plain", "application/rtf"))):
                type = False
                ext = False
            # end if
        else:
            if type != real_mime:
                #// 
                #// Everything else including image/* and application/*:
                #// If the real content type doesn't match the file extension, assume it's dangerous.
                #//
                type = False
                ext = False
            # end if
        # end if
    # end if
    #// The mime type must be allowed.
    if type:
        allowed = get_allowed_mime_types()
        if (not php_in_array(type, allowed)):
            type = False
            ext = False
        # end if
    # end if
    #// 
    #// Filters the "real" file type of the given file.
    #// 
    #// @since 3.0.0
    #// @since 5.1.0 The $real_mime parameter was added.
    #// 
    #// @param array       $wp_check_filetype_and_ext {
    #// Values for the extension, mime type, and corrected filename.
    #// 
    #// @type string|false $ext             File extension, or false if the file doesn't match a mime type.
    #// @type string|false $type            File mime type, or false if the file doesn't match a mime type.
    #// @type string|false $proper_filename File name with its correct extension, or false if it cannot be determined.
    #// }
    #// @param string      $file                      Full path to the file.
    #// @param string      $filename                  The name of the file (may differ from $file due to
    #// $file being in a tmp directory).
    #// @param string[]    $mimes                     Array of mime types keyed by their file extension regex.
    #// @param string|bool $real_mime                 The actual mime type or false if the type cannot be determined.
    #//
    return apply_filters("wp_check_filetype_and_ext", compact("ext", "type", "proper_filename"), file, filename, mimes, real_mime)
# end def wp_check_filetype_and_ext
#// 
#// Returns the real mime type of an image file.
#// 
#// This depends on exif_imagetype() or getimagesize() to determine real mime types.
#// 
#// @since 4.7.1
#// 
#// @param string $file Full path to the file.
#// @return string|false The actual mime type or false if the type cannot be determined.
#//
def wp_get_image_mime(file=None, *args_):
    
    #// 
    #// Use exif_imagetype() to check the mimetype if available or fall back to
    #// getimagesize() if exif isn't avaialbe. If either function throws an Exception
    #// we assume the file could not be validated.
    #//
    try: 
        if php_is_callable("exif_imagetype"):
            imagetype = exif_imagetype(file)
            mime = image_type_to_mime_type(imagetype) if imagetype else False
        elif php_function_exists("getimagesize"):
            imagesize = php_no_error(lambda: getimagesize(file))
            mime = imagesize["mime"] if (php_isset(lambda : imagesize["mime"])) else False
        else:
            mime = False
        # end if
    except Exception as e:
        mime = False
    # end try
    return mime
# end def wp_get_image_mime
#// 
#// Retrieve list of mime types and file extensions.
#// 
#// @since 3.5.0
#// @since 4.2.0 Support was added for GIMP (.xcf) files.
#// @since 4.9.2 Support was added for Flac (.flac) files.
#// @since 4.9.6 Support was added for AAC (.aac) files.
#// 
#// @return string[] Array of mime types keyed by the file extension regex corresponding to those types.
#//
def wp_get_mime_types(*args_):
    
    #// 
    #// Filters the list of mime types and file extensions.
    #// 
    #// This filter should be used to add, not remove, mime types. To remove
    #// mime types, use the {@see 'upload_mimes'} filter.
    #// 
    #// @since 3.5.0
    #// 
    #// @param string[] $wp_get_mime_types Mime types keyed by the file extension regex
    #// corresponding to those types.
    #//
    return apply_filters("mime_types", Array({"jpg|jpeg|jpe": "image/jpeg", "gif": "image/gif", "png": "image/png", "bmp": "image/bmp", "tiff|tif": "image/tiff", "ico": "image/x-icon", "asf|asx": "video/x-ms-asf", "wmv": "video/x-ms-wmv", "wmx": "video/x-ms-wmx", "wm": "video/x-ms-wm", "avi": "video/avi", "divx": "video/divx", "flv": "video/x-flv", "mov|qt": "video/quicktime", "mpeg|mpg|mpe": "video/mpeg", "mp4|m4v": "video/mp4", "ogv": "video/ogg", "webm": "video/webm", "mkv": "video/x-matroska", "3gp|3gpp": "video/3gpp", "3g2|3gp2": "video/3gpp2", "txt|asc|c|cc|h|srt": "text/plain", "csv": "text/csv", "tsv": "text/tab-separated-values", "ics": "text/calendar", "rtx": "text/richtext", "css": "text/css", "htm|html": "text/html", "vtt": "text/vtt", "dfxp": "application/ttaf+xml", "mp3|m4a|m4b": "audio/mpeg", "aac": "audio/aac", "ra|ram": "audio/x-realaudio", "wav": "audio/wav", "ogg|oga": "audio/ogg", "flac": "audio/flac", "mid|midi": "audio/midi", "wma": "audio/x-ms-wma", "wax": "audio/x-ms-wax", "mka": "audio/x-matroska", "rtf": "application/rtf", "js": "application/javascript", "pdf": "application/pdf", "swf": "application/x-shockwave-flash", "class": "application/java", "tar": "application/x-tar", "zip": "application/zip", "gz|gzip": "application/x-gzip", "rar": "application/rar", "7z": "application/x-7z-compressed", "exe": "application/x-msdownload", "psd": "application/octet-stream", "xcf": "application/octet-stream", "doc": "application/msword", "pot|pps|ppt": "application/vnd.ms-powerpoint", "wri": "application/vnd.ms-write", "xla|xls|xlt|xlw": "application/vnd.ms-excel", "mdb": "application/vnd.ms-access", "mpp": "application/vnd.ms-project", "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "docm": "application/vnd.ms-word.document.macroEnabled.12", "dotx": "application/vnd.openxmlformats-officedocument.wordprocessingml.template", "dotm": "application/vnd.ms-word.template.macroEnabled.12", "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "xlsm": "application/vnd.ms-excel.sheet.macroEnabled.12", "xlsb": "application/vnd.ms-excel.sheet.binary.macroEnabled.12", "xltx": "application/vnd.openxmlformats-officedocument.spreadsheetml.template", "xltm": "application/vnd.ms-excel.template.macroEnabled.12", "xlam": "application/vnd.ms-excel.addin.macroEnabled.12", "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation", "pptm": "application/vnd.ms-powerpoint.presentation.macroEnabled.12", "ppsx": "application/vnd.openxmlformats-officedocument.presentationml.slideshow", "ppsm": "application/vnd.ms-powerpoint.slideshow.macroEnabled.12", "potx": "application/vnd.openxmlformats-officedocument.presentationml.template", "potm": "application/vnd.ms-powerpoint.template.macroEnabled.12", "ppam": "application/vnd.ms-powerpoint.addin.macroEnabled.12", "sldx": "application/vnd.openxmlformats-officedocument.presentationml.slide", "sldm": "application/vnd.ms-powerpoint.slide.macroEnabled.12", "onetoc|onetoc2|onetmp|onepkg": "application/onenote", "oxps": "application/oxps", "xps": "application/vnd.ms-xpsdocument", "odt": "application/vnd.oasis.opendocument.text", "odp": "application/vnd.oasis.opendocument.presentation", "ods": "application/vnd.oasis.opendocument.spreadsheet", "odg": "application/vnd.oasis.opendocument.graphics", "odc": "application/vnd.oasis.opendocument.chart", "odb": "application/vnd.oasis.opendocument.database", "odf": "application/vnd.oasis.opendocument.formula", "wp|wpd": "application/wordperfect", "key": "application/vnd.apple.keynote", "numbers": "application/vnd.apple.numbers", "pages": "application/vnd.apple.pages"}))
# end def wp_get_mime_types
#// 
#// Retrieves the list of common file extensions and their types.
#// 
#// @since 4.6.0
#// 
#// @return array[] Multi-dimensional array of file extensions types keyed by the type of file.
#//
def wp_get_ext_types(*args_):
    
    #// 
    #// Filters file type based on the extension name.
    #// 
    #// @since 2.5.0
    #// 
    #// @see wp_ext2type()
    #// 
    #// @param array[] $ext2type Multi-dimensional array of file extensions types keyed by the type of file.
    #//
    return apply_filters("ext2type", Array({"image": Array("jpg", "jpeg", "jpe", "gif", "png", "bmp", "tif", "tiff", "ico"), "audio": Array("aac", "ac3", "aif", "aiff", "flac", "m3a", "m4a", "m4b", "mka", "mp1", "mp2", "mp3", "ogg", "oga", "ram", "wav", "wma"), "video": Array("3g2", "3gp", "3gpp", "asf", "avi", "divx", "dv", "flv", "m4v", "mkv", "mov", "mp4", "mpeg", "mpg", "mpv", "ogm", "ogv", "qt", "rm", "vob", "wmv"), "document": Array("doc", "docx", "docm", "dotm", "odt", "pages", "pdf", "xps", "oxps", "rtf", "wp", "wpd", "psd", "xcf"), "spreadsheet": Array("numbers", "ods", "xls", "xlsx", "xlsm", "xlsb"), "interactive": Array("swf", "key", "ppt", "pptx", "pptm", "pps", "ppsx", "ppsm", "sldx", "sldm", "odp"), "text": Array("asc", "csv", "tsv", "txt"), "archive": Array("bz2", "cab", "dmg", "gz", "rar", "sea", "sit", "sqx", "tar", "tgz", "zip", "7z"), "code": Array("css", "htm", "html", "php", "js")}))
# end def wp_get_ext_types
#// 
#// Retrieve list of allowed mime types and file extensions.
#// 
#// @since 2.8.6
#// 
#// @param int|WP_User $user Optional. User to check. Defaults to current user.
#// @return string[] Array of mime types keyed by the file extension regex corresponding
#// to those types.
#//
def get_allowed_mime_types(user=None, *args_):
    
    t = wp_get_mime_types()
    t["swf"] = None
    t["exe"] = None
    if php_function_exists("current_user_can"):
        unfiltered = user_can(user, "unfiltered_html") if user else current_user_can("unfiltered_html")
    # end if
    if php_empty(lambda : unfiltered):
        t["htm|html"] = None
        t["js"] = None
    # end if
    #// 
    #// Filters list of allowed mime types and file extensions.
    #// 
    #// @since 2.0.0
    #// 
    #// @param array            $t    Mime types keyed by the file extension regex corresponding to those types.
    #// @param int|WP_User|null $user User ID, User object or null if not provided (indicates current user).
    #//
    return apply_filters("upload_mimes", t, user)
# end def get_allowed_mime_types
#// 
#// Display "Are You Sure" message to confirm the action being taken.
#// 
#// If the action has the nonce explain message, then it will be displayed
#// along with the "Are you sure?" message.
#// 
#// @since 2.0.4
#// 
#// @param string $action The nonce action.
#//
def wp_nonce_ays(action=None, *args_):
    
    if "log-out" == action:
        html = php_sprintf(__("You are attempting to log out of %s"), get_bloginfo("name"))
        html += "</p><p>"
        redirect_to = PHP_REQUEST["redirect_to"] if (php_isset(lambda : PHP_REQUEST["redirect_to"])) else ""
        html += php_sprintf(__("Do you really want to <a href=\"%s\">log out</a>?"), wp_logout_url(redirect_to))
    else:
        html = __("The link you followed has expired.")
        if wp_get_referer():
            html += "</p><p>"
            html += php_sprintf("<a href=\"%s\">%s</a>", esc_url(remove_query_arg("updated", wp_get_referer())), __("Please try again."))
        # end if
    # end if
    wp_die(html, __("Something went wrong."), 403)
# end def wp_nonce_ays
#// 
#// Kills WordPress execution and displays HTML page with an error message.
#// 
#// This function complements the `die()` PHP function. The difference is that
#// HTML will be displayed to the user. It is recommended to use this function
#// only when the execution should not continue any further. It is not recommended
#// to call this function very often, and try to handle as many errors as possible
#// silently or more gracefully.
#// 
#// As a shorthand, the desired HTTP response code may be passed as an integer to
#// the `$title` parameter (the default title would apply) or the `$args` parameter.
#// 
#// @since 2.0.4
#// @since 4.1.0 The `$title` and `$args` parameters were changed to optionally accept
#// an integer to be used as the response code.
#// @since 5.1.0 The `$link_url`, `$link_text`, and `$exit` arguments were added.
#// @since 5.3.0 The `$charset` argument was added.
#// 
#// @global WP_Query $wp_query WordPress Query object.
#// 
#// @param string|WP_Error  $message Optional. Error message. If this is a WP_Error object,
#// and not an Ajax or XML-RPC request, the error's messages are used.
#// Default empty.
#// @param string|int       $title   Optional. Error title. If `$message` is a `WP_Error` object,
#// error data with the key 'title' may be used to specify the title.
#// If `$title` is an integer, then it is treated as the response
#// code. Default empty.
#// @param string|array|int $args {
#// Optional. Arguments to control behavior. If `$args` is an integer, then it is treated
#// as the response code. Default empty array.
#// 
#// @type int    $response       The HTTP response code. Default 200 for Ajax requests, 500 otherwise.
#// @type string $link_url       A URL to include a link to. Only works in combination with $link_text.
#// Default empty string.
#// @type string $link_text      A label for the link to include. Only works in combination with $link_url.
#// Default empty string.
#// @type bool   $back_link      Whether to include a link to go back. Default false.
#// @type string $text_direction The text direction. This is only useful internally, when WordPress
#// is still loading and the site's locale is not set up yet. Accepts 'rtl'.
#// Default is the value of is_rtl().
#// @type string $charset        Character set of the HTML output. Default 'utf-8'.
#// @type string $code           Error code to use. Default is 'wp_die', or the main error code if $message
#// is a WP_Error.
#// @type bool   $exit           Whether to exit the process after completion. Default true.
#// }
#//
def wp_die(message="", title="", args=Array(), *args_):
    
    global wp_query
    php_check_if_defined("wp_query")
    if php_is_int(args):
        args = Array({"response": args})
    elif php_is_int(title):
        args = Array({"response": title})
        title = ""
    # end if
    if wp_doing_ajax():
        #// 
        #// Filters the callback for killing WordPress execution for Ajax requests.
        #// 
        #// @since 3.4.0
        #// 
        #// @param callable $function Callback function name.
        #//
        function = apply_filters("wp_die_ajax_handler", "_ajax_wp_die_handler")
    elif wp_is_json_request():
        #// 
        #// Filters the callback for killing WordPress execution for JSON requests.
        #// 
        #// @since 5.1.0
        #// 
        #// @param callable $function Callback function name.
        #//
        function = apply_filters("wp_die_json_handler", "_json_wp_die_handler")
    elif wp_is_jsonp_request():
        #// 
        #// Filters the callback for killing WordPress execution for JSONP requests.
        #// 
        #// @since 5.2.0
        #// 
        #// @param callable $function Callback function name.
        #//
        function = apply_filters("wp_die_jsonp_handler", "_jsonp_wp_die_handler")
    elif php_defined("XMLRPC_REQUEST") and XMLRPC_REQUEST:
        #// 
        #// Filters the callback for killing WordPress execution for XML-RPC requests.
        #// 
        #// @since 3.4.0
        #// 
        #// @param callable $function Callback function name.
        #//
        function = apply_filters("wp_die_xmlrpc_handler", "_xmlrpc_wp_die_handler")
    elif wp_is_xml_request() or (php_isset(lambda : wp_query)) and php_function_exists("is_feed") and is_feed() or php_function_exists("is_comment_feed") and is_comment_feed() or php_function_exists("is_trackback") and is_trackback():
        #// 
        #// Filters the callback for killing WordPress execution for XML requests.
        #// 
        #// @since 5.2.0
        #// 
        #// @param callable $function Callback function name.
        #//
        function = apply_filters("wp_die_xml_handler", "_xml_wp_die_handler")
    else:
        #// 
        #// Filters the callback for killing WordPress execution for all non-Ajax, non-JSON, non-XML requests.
        #// 
        #// @since 3.0.0
        #// 
        #// @param callable $function Callback function name.
        #//
        function = apply_filters("wp_die_handler", "_default_wp_die_handler")
    # end if
    php_call_user_func(function, message, title, args)
# end def wp_die
#// 
#// Kills WordPress execution and displays HTML page with an error message.
#// 
#// This is the default handler for wp_die(). If you want a custom one,
#// you can override this using the {@see 'wp_die_handler'} filter in wp_die().
#// 
#// @since 3.0.0
#// @access private
#// 
#// @param string|WP_Error $message Error message or WP_Error object.
#// @param string          $title   Optional. Error title. Default empty.
#// @param string|array    $args    Optional. Arguments to control behavior. Default empty array.
#//
def _default_wp_die_handler(message=None, title="", args=Array(), *args_):
    
    message, title, parsed_args = _wp_die_process_input(message, title, args)
    if php_is_string(message):
        if (not php_empty(lambda : parsed_args["additional_errors"])):
            message = php_array_merge(Array(message), wp_list_pluck(parsed_args["additional_errors"], "message"))
            message = "<ul>\n       <li>" + join("</li>\n       <li>", message) + "</li>\n  </ul>"
        # end if
        message = php_sprintf("<div class=\"wp-die-message\">%s</div>", message)
    # end if
    have_gettext = php_function_exists("__")
    if (not php_empty(lambda : parsed_args["link_url"])) and (not php_empty(lambda : parsed_args["link_text"])):
        link_url = parsed_args["link_url"]
        if php_function_exists("esc_url"):
            link_url = esc_url(link_url)
        # end if
        link_text = parsed_args["link_text"]
        message += str("\n<p><a href='") + str(link_url) + str("'>") + str(link_text) + str("</a></p>")
    # end if
    if (php_isset(lambda : parsed_args["back_link"])) and parsed_args["back_link"]:
        back_text = __("&laquo; Back") if have_gettext else "&laquo; Back"
        message += str("\n<p><a href='javascript:history.back()'>") + str(back_text) + str("</a></p>")
    # end if
    if (not did_action("admin_head")):
        if (not php_headers_sent()):
            php_header(str("Content-Type: text/html; charset=") + str(parsed_args["charset"]))
            status_header(parsed_args["response"])
            nocache_headers()
        # end if
        text_direction = parsed_args["text_direction"]
        if php_function_exists("language_attributes") and php_function_exists("is_rtl"):
            dir_attr = get_language_attributes()
        else:
            dir_attr = str("dir='") + str(text_direction) + str("'")
        # end if
        php_print("<!DOCTYPE html>\n<html xmlns=\"http://www.w3.org/1999/xhtml\" ")
        php_print(dir_attr)
        php_print(">\n<head>\n  <meta http-equiv=\"Content-Type\" content=\"text/html; charset=")
        php_print(parsed_args["charset"])
        php_print("\" />\n  <meta name=\"viewport\" content=\"width=device-width\">\n       ")
        if php_function_exists("wp_no_robots"):
            wp_no_robots()
        # end if
        php_print(" <title>")
        php_print(title)
        php_print("""</title>
        <style type=\"text/css\">
        html {
        background: #f1f1f1;
        }
        body {
        background: #fff;
        color: #444;
        font-family: -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, Oxygen-Sans, Ubuntu, Cantarell, \"Helvetica Neue\", sans-serif;
        margin: 2em auto;
        padding: 1em 2em;
        max-width: 700px;
        -webkit-box-shadow: 0 1px 3px rgba(0, 0, 0, 0.13);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.13);
        }
        h1 {
        border-bottom: 1px solid #dadada;
        clear: both;
        color: #666;
        font-size: 24px;
        margin: 30px 0 0 0;
        padding: 0;
        padding-bottom: 7px;
        }
        #error-page {
        margin-top: 50px;
        }
        #error-page p,
        #error-page .wp-die-message {
        font-size: 14px;
        line-height: 1.5;
        margin: 25px 0 20px;
        }
        #error-page code {
        font-family: Consolas, Monaco, monospace;
        }
        ul li {
        margin-bottom: 10px;
        font-size: 14px ;
        }
        a {
        color: #0073aa;
        }
        a:hover,
        a:active {
        color: #00a0d2;
        }
        a:focus {
        color: #124964;
        -webkit-box-shadow:
        0 0 0 1px #5b9dd9,
        0 0 2px 1px rgba(30, 140, 190, 0.8);
        box-shadow:
        0 0 0 1px #5b9dd9,
        0 0 2px 1px rgba(30, 140, 190, 0.8);
        outline: none;
        }
        .button {
        background: #f7f7f7;
        border: 1px solid #ccc;
        color: #555;
        display: inline-block;
        text-decoration: none;
        font-size: 13px;
        line-height: 2;
        height: 28px;
        margin: 0;
        padding: 0 10px 1px;
        cursor: pointer;
        -webkit-border-radius: 3px;
        -webkit-appearance: none;
        border-radius: 3px;
        white-space: nowrap;
        -webkit-box-sizing: border-box;
        -moz-box-sizing:    border-box;
        box-sizing:         border-box;
        -webkit-box-shadow: 0 1px 0 #ccc;
        box-shadow: 0 1px 0 #ccc;
        vertical-align: top;
        }
        .button.button-large {
        height: 30px;
        line-height: 2.15384615;
        padding: 0 12px 2px;
        }
        .button:hover,
        .button:focus {
        background: #fafafa;
        border-color: #999;
        color: #23282d;
        }
        .button:focus {
        border-color: #5b9dd9;
        -webkit-box-shadow: 0 0 3px rgba(0, 115, 170, 0.8);
        box-shadow: 0 0 3px rgba(0, 115, 170, 0.8);
        outline: none;
        }
        .button:active {
        background: #eee;
        border-color: #999;
        -webkit-box-shadow: inset 0 2px 5px -3px rgba(0, 0, 0, 0.5);
        box-shadow: inset 0 2px 5px -3px rgba(0, 0, 0, 0.5);
        }
        """)
        if "rtl" == text_direction:
            php_print("body { font-family: Tahoma, Arial; }")
        # end if
        php_print("""   </style>
        </head>
        <body id=\"error-page\">
        """)
    # end if
    pass
    php_print(" ")
    php_print(message)
    php_print("</body>\n</html>\n   ")
    if parsed_args["exit"]:
        php_exit(0)
    # end if
# end def _default_wp_die_handler
#// 
#// Kills WordPress execution and displays Ajax response with an error message.
#// 
#// This is the handler for wp_die() when processing Ajax requests.
#// 
#// @since 3.4.0
#// @access private
#// 
#// @param string       $message Error message.
#// @param string       $title   Optional. Error title (unused). Default empty.
#// @param string|array $args    Optional. Arguments to control behavior. Default empty array.
#//
def _ajax_wp_die_handler(message=None, title="", args=Array(), *args_):
    
    #// Set default 'response' to 200 for AJAX requests.
    args = wp_parse_args(args, Array({"response": 200}))
    message, title, parsed_args = _wp_die_process_input(message, title, args)
    if (not php_headers_sent()):
        #// This is intentional. For backward-compatibility, support passing null here.
        if None != args["response"]:
            status_header(parsed_args["response"])
        # end if
        nocache_headers()
    # end if
    if is_scalar(message):
        message = php_str(message)
    else:
        message = "0"
    # end if
    if parsed_args["exit"]:
        php_print(message)
        php_exit()
    # end if
    php_print(message)
# end def _ajax_wp_die_handler
#// 
#// Kills WordPress execution and displays JSON response with an error message.
#// 
#// This is the handler for wp_die() when processing JSON requests.
#// 
#// @since 5.1.0
#// @access private
#// 
#// @param string       $message Error message.
#// @param string       $title   Optional. Error title. Default empty.
#// @param string|array $args    Optional. Arguments to control behavior. Default empty array.
#//
def _json_wp_die_handler(message=None, title="", args=Array(), *args_):
    
    message, title, parsed_args = _wp_die_process_input(message, title, args)
    data = Array({"code": parsed_args["code"], "message": message, "data": Array({"status": parsed_args["response"]})}, {"additional_errors": parsed_args["additional_errors"]})
    if (not php_headers_sent()):
        php_header(str("Content-Type: application/json; charset=") + str(parsed_args["charset"]))
        if None != parsed_args["response"]:
            status_header(parsed_args["response"])
        # end if
        nocache_headers()
    # end if
    php_print(wp_json_encode(data))
    if parsed_args["exit"]:
        php_exit(0)
    # end if
# end def _json_wp_die_handler
#// 
#// Kills WordPress execution and displays JSONP response with an error message.
#// 
#// This is the handler for wp_die() when processing JSONP requests.
#// 
#// @since 5.2.0
#// @access private
#// 
#// @param string       $message Error message.
#// @param string       $title   Optional. Error title. Default empty.
#// @param string|array $args    Optional. Arguments to control behavior. Default empty array.
#//
def _jsonp_wp_die_handler(message=None, title="", args=Array(), *args_):
    
    message, title, parsed_args = _wp_die_process_input(message, title, args)
    data = Array({"code": parsed_args["code"], "message": message, "data": Array({"status": parsed_args["response"]})}, {"additional_errors": parsed_args["additional_errors"]})
    if (not php_headers_sent()):
        php_header(str("Content-Type: application/javascript; charset=") + str(parsed_args["charset"]))
        php_header("X-Content-Type-Options: nosniff")
        php_header("X-Robots-Tag: noindex")
        if None != parsed_args["response"]:
            status_header(parsed_args["response"])
        # end if
        nocache_headers()
    # end if
    result = wp_json_encode(data)
    jsonp_callback = PHP_REQUEST["_jsonp"]
    php_print("/**/" + jsonp_callback + "(" + result + ")")
    if parsed_args["exit"]:
        php_exit(0)
    # end if
# end def _jsonp_wp_die_handler
#// 
#// Kills WordPress execution and displays XML response with an error message.
#// 
#// This is the handler for wp_die() when processing XMLRPC requests.
#// 
#// @since 3.2.0
#// @access private
#// 
#// @global wp_xmlrpc_server $wp_xmlrpc_server
#// 
#// @param string       $message Error message.
#// @param string       $title   Optional. Error title. Default empty.
#// @param string|array $args    Optional. Arguments to control behavior. Default empty array.
#//
def _xmlrpc_wp_die_handler(message=None, title="", args=Array(), *args_):
    
    global wp_xmlrpc_server
    php_check_if_defined("wp_xmlrpc_server")
    message, title, parsed_args = _wp_die_process_input(message, title, args)
    if (not php_headers_sent()):
        nocache_headers()
    # end if
    if wp_xmlrpc_server:
        error = php_new_class("IXR_Error", lambda : IXR_Error(parsed_args["response"], message))
        wp_xmlrpc_server.output(error.getxml())
    # end if
    if parsed_args["exit"]:
        php_exit(0)
    # end if
# end def _xmlrpc_wp_die_handler
#// 
#// Kills WordPress execution and displays XML response with an error message.
#// 
#// This is the handler for wp_die() when processing XML requests.
#// 
#// @since 5.2.0
#// @access private
#// 
#// @param string       $message Error message.
#// @param string       $title   Optional. Error title. Default empty.
#// @param string|array $args    Optional. Arguments to control behavior. Default empty array.
#//
def _xml_wp_die_handler(message=None, title="", args=Array(), *args_):
    
    message, title, parsed_args = _wp_die_process_input(message, title, args)
    message = htmlspecialchars(message)
    title = htmlspecialchars(title)
    xml = str("<error>\n    <code>") + str(parsed_args["code"]) + str("</code>\n    <title><![CDATA[") + str(title) + str("]]></title>\n    <message><![CDATA[") + str(message) + str("]]></message>\n    <data>\n        <status>") + str(parsed_args["response"]) + str("""</status>\n    </data>\n</error>\n""")
    if (not php_headers_sent()):
        php_header(str("Content-Type: text/xml; charset=") + str(parsed_args["charset"]))
        if None != parsed_args["response"]:
            status_header(parsed_args["response"])
        # end if
        nocache_headers()
    # end if
    php_print(xml)
    if parsed_args["exit"]:
        php_exit(0)
    # end if
# end def _xml_wp_die_handler
#// 
#// Kills WordPress execution and displays an error message.
#// 
#// This is the handler for wp_die() when processing APP requests.
#// 
#// @since 3.4.0
#// @since 5.1.0 Added the $title and $args parameters.
#// @access private
#// 
#// @param string       $message Optional. Response to print. Default empty.
#// @param string       $title   Optional. Error title (unused). Default empty.
#// @param string|array $args    Optional. Arguments to control behavior. Default empty array.
#//
def _scalar_wp_die_handler(message="", title="", args=Array(), *args_):
    
    message, title, parsed_args = _wp_die_process_input(message, title, args)
    if parsed_args["exit"]:
        if is_scalar(message):
            php_print(php_str(message))
            php_exit()
        # end if
        php_exit(0)
    # end if
    if is_scalar(message):
        php_print(php_str(message))
    # end if
# end def _scalar_wp_die_handler
#// 
#// Processes arguments passed to wp_die() consistently for its handlers.
#// 
#// @since 5.1.0
#// @access private
#// 
#// @param string|WP_Error $message Error message or WP_Error object.
#// @param string          $title   Optional. Error title. Default empty.
#// @param string|array    $args    Optional. Arguments to control behavior. Default empty array.
#// @return array {
#// Processed arguments.
#// 
#// @type string $0 Error message.
#// @type string $1 Error title.
#// @type array  $2 Arguments to control behavior.
#// }
#//
def _wp_die_process_input(message=None, title="", args=Array(), *args_):
    
    defaults = Array({"response": 0, "code": "", "exit": True, "back_link": False, "link_url": "", "link_text": "", "text_direction": "", "charset": "utf-8", "additional_errors": Array()})
    args = wp_parse_args(args, defaults)
    if php_function_exists("is_wp_error") and is_wp_error(message):
        if (not php_empty(lambda : message.errors)):
            errors = Array()
            for error_code,error_messages in message.errors:
                for error_message in error_messages:
                    errors[-1] = Array({"code": error_code, "message": error_message, "data": message.get_error_data(error_code)})
                # end for
            # end for
            message = errors[0]["message"]
            if php_empty(lambda : args["code"]):
                args["code"] = errors[0]["code"]
            # end if
            if php_empty(lambda : args["response"]) and php_is_array(errors[0]["data"]) and (not php_empty(lambda : errors[0]["data"]["status"])):
                args["response"] = errors[0]["data"]["status"]
            # end if
            if php_empty(lambda : title) and php_is_array(errors[0]["data"]) and (not php_empty(lambda : errors[0]["data"]["title"])):
                title = errors[0]["data"]["title"]
            # end if
            errors[0] = None
            args["additional_errors"] = php_array_values(errors)
        else:
            message = ""
        # end if
    # end if
    have_gettext = php_function_exists("__")
    #// The $title and these specific $args must always have a non-empty value.
    if php_empty(lambda : args["code"]):
        args["code"] = "wp_die"
    # end if
    if php_empty(lambda : args["response"]):
        args["response"] = 500
    # end if
    if php_empty(lambda : title):
        title = __("WordPress &rsaquo; Error") if have_gettext else "WordPress &rsaquo; Error"
    # end if
    if php_empty(lambda : args["text_direction"]) or (not php_in_array(args["text_direction"], Array("ltr", "rtl"), True)):
        args["text_direction"] = "ltr"
        if php_function_exists("is_rtl") and is_rtl():
            args["text_direction"] = "rtl"
        # end if
    # end if
    if (not php_empty(lambda : args["charset"])):
        args["charset"] = _canonical_charset(args["charset"])
    # end if
    return Array(message, title, args)
# end def _wp_die_process_input
#// 
#// Encode a variable into JSON, with some sanity checks.
#// 
#// @since 4.1.0
#// @since 5.3.0 No longer handles support for PHP < 5.6.
#// 
#// @param mixed $data    Variable (usually an array or object) to encode as JSON.
#// @param int   $options Optional. Options to be passed to json_encode(). Default 0.
#// @param int   $depth   Optional. Maximum depth to walk through $data. Must be
#// greater than 0. Default 512.
#// @return string|false The JSON encoded string, or false if it cannot be encoded.
#//
def wp_json_encode(data=None, options=0, depth=512, *args_):
    
    json = php_json_encode(data, options, depth)
    #// If json_encode() was successful, no need to do more sanity checking.
    if False != json:
        return json
    # end if
    try: 
        data = _wp_json_sanity_check(data, depth)
    except Exception as e:
        return False
    # end try
    return php_json_encode(data, options, depth)
# end def wp_json_encode
#// 
#// Perform sanity checks on data that shall be encoded to JSON.
#// 
#// @ignore
#// @since 4.1.0
#// @access private
#// 
#// @see wp_json_encode()
#// 
#// @param mixed $data  Variable (usually an array or object) to encode as JSON.
#// @param int   $depth Maximum depth to walk through $data. Must be greater than 0.
#// @return mixed The sanitized data that shall be encoded to JSON.
#//
def _wp_json_sanity_check(data=None, depth=None, *args_):
    
    if depth < 0:
        raise php_new_class("Exception", lambda : Exception("Reached depth limit"))
    # end if
    if php_is_array(data):
        output = Array()
        for id,el in data:
            #// Don't forget to sanitize the ID!
            if php_is_string(id):
                clean_id = _wp_json_convert_string(id)
            else:
                clean_id = id
            # end if
            #// Check the element type, so that we're only recursing if we really have to.
            if php_is_array(el) or php_is_object(el):
                output[clean_id] = _wp_json_sanity_check(el, depth - 1)
            elif php_is_string(el):
                output[clean_id] = _wp_json_convert_string(el)
            else:
                output[clean_id] = el
            # end if
        # end for
    elif php_is_object(data):
        output = php_new_class("stdClass", lambda : stdClass())
        for id,el in data:
            if php_is_string(id):
                clean_id = _wp_json_convert_string(id)
            else:
                clean_id = id
            # end if
            if php_is_array(el) or php_is_object(el):
                output.clean_id = _wp_json_sanity_check(el, depth - 1)
            elif php_is_string(el):
                output.clean_id = _wp_json_convert_string(el)
            else:
                output.clean_id = el
            # end if
        # end for
    elif php_is_string(data):
        return _wp_json_convert_string(data)
    else:
        return data
    # end if
    return output
# end def _wp_json_sanity_check
#// 
#// Convert a string to UTF-8, so that it can be safely encoded to JSON.
#// 
#// @ignore
#// @since 4.1.0
#// @access private
#// 
#// @see _wp_json_sanity_check()
#// 
#// @staticvar bool $use_mb
#// 
#// @param string $string The string which is to be converted.
#// @return string The checked string.
#//
def _wp_json_convert_string(string=None, *args_):
    
    use_mb = None
    if is_null(use_mb):
        use_mb = php_function_exists("mb_convert_encoding")
    # end if
    if use_mb:
        encoding = mb_detect_encoding(string, mb_detect_order(), True)
        if encoding:
            return mb_convert_encoding(string, "UTF-8", encoding)
        else:
            return mb_convert_encoding(string, "UTF-8", "UTF-8")
        # end if
    else:
        return wp_check_invalid_utf8(string, True)
    # end if
# end def _wp_json_convert_string
#// 
#// Prepares response data to be serialized to JSON.
#// 
#// This supports the JsonSerializable interface for PHP 5.2-5.3 as well.
#// 
#// @ignore
#// @since 4.4.0
#// @deprecated 5.3.0 This function is no longer needed as support for PHP 5.2-5.3
#// has been dropped.
#// @access     private
#// 
#// @param mixed $data Native representation.
#// @return bool|int|float|null|string|array Data ready for `json_encode()`.
#//
def _wp_json_prepare_data(data=None, *args_):
    
    _deprecated_function(__FUNCTION__, "5.3.0")
    return data
# end def _wp_json_prepare_data
#// 
#// Send a JSON response back to an Ajax request.
#// 
#// @since 3.5.0
#// @since 4.7.0 The `$status_code` parameter was added.
#// 
#// @param mixed $response    Variable (usually an array or object) to encode as JSON,
#// then print and die.
#// @param int   $status_code The HTTP status code to output.
#//
def wp_send_json(response=None, status_code=None, *args_):
    
    if (not php_headers_sent()):
        php_header("Content-Type: application/json; charset=" + get_option("blog_charset"))
        if None != status_code:
            status_header(status_code)
        # end if
    # end if
    php_print(wp_json_encode(response))
    if wp_doing_ajax():
        wp_die("", "", Array({"response": None}))
    else:
        php_exit(0)
    # end if
# end def wp_send_json
#// 
#// Send a JSON response back to an Ajax request, indicating success.
#// 
#// @since 3.5.0
#// @since 4.7.0 The `$status_code` parameter was added.
#// 
#// @param mixed $data        Data to encode as JSON, then print and die.
#// @param int   $status_code The HTTP status code to output.
#//
def wp_send_json_success(data=None, status_code=None, *args_):
    
    response = Array({"success": True})
    if (php_isset(lambda : data)):
        response["data"] = data
    # end if
    wp_send_json(response, status_code)
# end def wp_send_json_success
#// 
#// Send a JSON response back to an Ajax request, indicating failure.
#// 
#// If the `$data` parameter is a WP_Error object, the errors
#// within the object are processed and output as an array of error
#// codes and corresponding messages. All other types are output
#// without further processing.
#// 
#// @since 3.5.0
#// @since 4.1.0 The `$data` parameter is now processed if a WP_Error object is passed in.
#// @since 4.7.0 The `$status_code` parameter was added.
#// 
#// @param mixed $data        Data to encode as JSON, then print and die.
#// @param int   $status_code The HTTP status code to output.
#//
def wp_send_json_error(data=None, status_code=None, *args_):
    
    response = Array({"success": False})
    if (php_isset(lambda : data)):
        if is_wp_error(data):
            result = Array()
            for code,messages in data.errors:
                for message in messages:
                    result[-1] = Array({"code": code, "message": message})
                # end for
            # end for
            response["data"] = result
        else:
            response["data"] = data
        # end if
    # end if
    wp_send_json(response, status_code)
# end def wp_send_json_error
#// 
#// Checks that a JSONP callback is a valid JavaScript callback.
#// 
#// Only allows alphanumeric characters and the dot character in callback
#// function names. This helps to mitigate XSS attacks caused by directly
#// outputting user input.
#// 
#// @since 4.6.0
#// 
#// @param string $callback Supplied JSONP callback function.
#// @return bool True if valid callback, otherwise false.
#//
def wp_check_jsonp_callback(callback=None, *args_):
    
    if (not php_is_string(callback)):
        return False
    # end if
    php_preg_replace("/[^\\w\\.]/", "", callback, -1, illegal_char_count)
    return 0 == illegal_char_count
# end def wp_check_jsonp_callback
#// 
#// Retrieve the WordPress home page URL.
#// 
#// If the constant named 'WP_HOME' exists, then it will be used and returned
#// by the function. This can be used to counter the redirection on your local
#// development environment.
#// 
#// @since 2.2.0
#// @access private
#// 
#// @see WP_HOME
#// 
#// @param string $url URL for the home location.
#// @return string Homepage location.
#//
def _config_wp_home(url="", *args_):
    
    if php_defined("WP_HOME"):
        return untrailingslashit(WP_HOME)
    # end if
    return url
# end def _config_wp_home
#// 
#// Retrieve the WordPress site URL.
#// 
#// If the constant named 'WP_SITEURL' is defined, then the value in that
#// constant will always be returned. This can be used for debugging a site
#// on your localhost while not having to change the database to your URL.
#// 
#// @since 2.2.0
#// @access private
#// 
#// @see WP_SITEURL
#// 
#// @param string $url URL to set the WordPress site location.
#// @return string The WordPress Site URL.
#//
def _config_wp_siteurl(url="", *args_):
    
    if php_defined("WP_SITEURL"):
        return untrailingslashit(WP_SITEURL)
    # end if
    return url
# end def _config_wp_siteurl
#// 
#// Delete the fresh site option.
#// 
#// @since 4.7.0
#// @access private
#//
def _delete_option_fresh_site(*args_):
    
    update_option("fresh_site", "0")
# end def _delete_option_fresh_site
#// 
#// Set the localized direction for MCE plugin.
#// 
#// Will only set the direction to 'rtl', if the WordPress locale has
#// the text direction set to 'rtl'.
#// 
#// Fills in the 'directionality' setting, enables the 'directionality'
#// plugin, and adds the 'ltr' button to 'toolbar1', formerly
#// 'theme_advanced_buttons1' array keys. These keys are then returned
#// in the $mce_init (TinyMCE settings) array.
#// 
#// @since 2.1.0
#// @access private
#// 
#// @param array $mce_init MCE settings array.
#// @return array Direction set for 'rtl', if needed by locale.
#//
def _mce_set_direction(mce_init=None, *args_):
    
    if is_rtl():
        mce_init["directionality"] = "rtl"
        mce_init["rtl_ui"] = True
        if (not php_empty(lambda : mce_init["plugins"])) and php_strpos(mce_init["plugins"], "directionality") == False:
            mce_init["plugins"] += ",directionality"
        # end if
        if (not php_empty(lambda : mce_init["toolbar1"])) and (not php_preg_match("/\\bltr\\b/", mce_init["toolbar1"])):
            mce_init["toolbar1"] += ",ltr"
        # end if
    # end if
    return mce_init
# end def _mce_set_direction
#// 
#// Convert smiley code to the icon graphic file equivalent.
#// 
#// You can turn off smilies, by going to the write setting screen and unchecking
#// the box, or by setting 'use_smilies' option to false or removing the option.
#// 
#// Plugins may override the default smiley list by setting the $wpsmiliestrans
#// to an array, with the key the code the blogger types in and the value the
#// image file.
#// 
#// The $wp_smiliessearch global is for the regular expression and is set each
#// time the function is called.
#// 
#// The full list of smilies can be found in the function and won't be listed in
#// the description. Probably should create a Codex page for it, so that it is
#// available.
#// 
#// @global array $wpsmiliestrans
#// @global array $wp_smiliessearch
#// 
#// @since 2.2.0
#//
def smilies_init(*args_):
    
    global wpsmiliestrans,wp_smiliessearch
    php_check_if_defined("wpsmiliestrans","wp_smiliessearch")
    #// Don't bother setting up smilies if they are disabled.
    if (not get_option("use_smilies")):
        return
    # end if
    if (not (php_isset(lambda : wpsmiliestrans))):
        wpsmiliestrans = Array({":mrgreen:": "mrgreen.png", ":neutral:": "ð", ":twisted:": "ð", ":arrow:": "â¡", ":shock:": "ð¯", ":smile:": "ð", ":???:": "ð", ":cool:": "ð", ":evil:": "ð¿", ":grin:": "ð", ":idea:": "ð¡", ":oops:": "ð³", ":razz:": "ð", ":roll:": "ð", ":wink:": "ð", ":cry:": "ð¥", ":eek:": "ð®", ":lol:": "ð", ":mad:": "ð¡", ":sad:": "ð", "8-)": "ð", "8-O": "ð¯", ":-(": "ð", ":-)": "ð", ":-?": "ð", ":-D": "ð", ":-P": "ð", ":-o": "ð®", ":-x": "ð¡", ":-|": "ð", ";-)": "ð", "8O": "ð¯", ":(": "ð", ":)": "ð", ":?": "ð", ":D": "ð", ":P": "ð", ":o": "ð®", ":x": "ð¡", ":|": "ð", ";)": "ð", ":!:": "â", ":?:": "â"})
    # end if
    #// 
    #// Filters all the smilies.
    #// 
    #// This filter must be added before `smilies_init` is run, as
    #// it is normally only run once to setup the smilies regex.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string[] $wpsmiliestrans List of the smilies' hexadecimal representations, keyed by their smily code.
    #//
    wpsmiliestrans = apply_filters("smilies", wpsmiliestrans)
    if php_count(wpsmiliestrans) == 0:
        return
    # end if
    #// 
    #// NOTE: we sort the smilies in reverse key order. This is to make sure
    #// we match the longest possible smilie (:???: vs :?) as the regular
    #// expression used below is first-match
    #//
    krsort(wpsmiliestrans)
    spaces = wp_spaces_regexp()
    #// Begin first "subpattern".
    wp_smiliessearch = "/(?<=" + spaces + "|^)"
    subchar = ""
    for smiley,img in wpsmiliestrans:
        firstchar = php_substr(smiley, 0, 1)
        rest = php_substr(smiley, 1)
        #// New subpattern?
        if firstchar != subchar:
            if "" != subchar:
                wp_smiliessearch += ")(?=" + spaces + "|$)"
                #// End previous "subpattern".
                wp_smiliessearch += "|(?<=" + spaces + "|^)"
                pass
            # end if
            subchar = firstchar
            wp_smiliessearch += preg_quote(firstchar, "/") + "(?:"
        else:
            wp_smiliessearch += "|"
        # end if
        wp_smiliessearch += preg_quote(rest, "/")
    # end for
    wp_smiliessearch += ")(?=" + spaces + "|$)/m"
# end def smilies_init
#// 
#// Merge user defined arguments into defaults array.
#// 
#// This function is used throughout WordPress to allow for both string or array
#// to be merged into another array.
#// 
#// @since 2.2.0
#// @since 2.3.0 `$args` can now also be an object.
#// 
#// @param string|array|object $args     Value to merge with $defaults.
#// @param array               $defaults Optional. Array that serves as the defaults. Default empty.
#// @return array Merged user defined values with defaults.
#//
def wp_parse_args(args=None, defaults="", *args_):
    
    if php_is_object(args):
        parsed_args = get_object_vars(args)
    elif php_is_array(args):
        parsed_args = args
    else:
        wp_parse_str(args, parsed_args)
    # end if
    if php_is_array(defaults):
        return php_array_merge(defaults, parsed_args)
    # end if
    return parsed_args
# end def wp_parse_args
#// 
#// Cleans up an array, comma- or space-separated list of scalar values.
#// 
#// @since 5.1.0
#// 
#// @param array|string $list List of values.
#// @return array Sanitized array of values.
#//
def wp_parse_list(list=None, *args_):
    
    if (not php_is_array(list)):
        return php_preg_split("/[\\s,]+/", list, -1, PREG_SPLIT_NO_EMPTY)
    # end if
    return list
# end def wp_parse_list
#// 
#// Clean up an array, comma- or space-separated list of IDs.
#// 
#// @since 3.0.0
#// 
#// @param array|string $list List of ids.
#// @return int[] Sanitized array of IDs.
#//
def wp_parse_id_list(list=None, *args_):
    
    list = wp_parse_list(list)
    return array_unique(php_array_map("absint", list))
# end def wp_parse_id_list
#// 
#// Clean up an array, comma- or space-separated list of slugs.
#// 
#// @since 4.7.0
#// 
#// @param  array|string $list List of slugs.
#// @return string[] Sanitized array of slugs.
#//
def wp_parse_slug_list(list=None, *args_):
    
    list = wp_parse_list(list)
    return array_unique(php_array_map("sanitize_title", list))
# end def wp_parse_slug_list
#// 
#// Extract a slice of an array, given a list of keys.
#// 
#// @since 3.1.0
#// 
#// @param array $array The original array.
#// @param array $keys  The list of keys.
#// @return array The array slice.
#//
def wp_array_slice_assoc(array=None, keys=None, *args_):
    
    slice = Array()
    for key in keys:
        if (php_isset(lambda : array[key])):
            slice[key] = array[key]
        # end if
    # end for
    return slice
# end def wp_array_slice_assoc
#// 
#// Determines if the variable is a numeric-indexed array.
#// 
#// @since 4.4.0
#// 
#// @param mixed $data Variable to check.
#// @return bool Whether the variable is a list.
#//
def wp_is_numeric_array(data=None, *args_):
    
    if (not php_is_array(data)):
        return False
    # end if
    keys = php_array_keys(data)
    string_keys = php_array_filter(keys, "is_string")
    return php_count(string_keys) == 0
# end def wp_is_numeric_array
#// 
#// Filters a list of objects, based on a set of key => value arguments.
#// 
#// @since 3.0.0
#// @since 4.7.0 Uses `WP_List_Util` class.
#// 
#// @param array       $list     An array of objects to filter
#// @param array       $args     Optional. An array of key => value arguments to match
#// against each object. Default empty array.
#// @param string      $operator Optional. The logical operation to perform. 'or' means
#// only one element from the array needs to match; 'and'
#// means all elements must match; 'not' means no elements may
#// match. Default 'and'.
#// @param bool|string $field    A field from the object to place instead of the entire object.
#// Default false.
#// @return array A list of objects or object fields.
#//
def wp_filter_object_list(list=None, args=Array(), operator="and", field=False, *args_):
    
    if (not php_is_array(list)):
        return Array()
    # end if
    util = php_new_class("WP_List_Util", lambda : WP_List_Util(list))
    util.filter(args, operator)
    if field:
        util.pluck(field)
    # end if
    return util.get_output()
# end def wp_filter_object_list
#// 
#// Filters a list of objects, based on a set of key => value arguments.
#// 
#// @since 3.1.0
#// @since 4.7.0 Uses `WP_List_Util` class.
#// 
#// @param array  $list     An array of objects to filter.
#// @param array  $args     Optional. An array of key => value arguments to match
#// against each object. Default empty array.
#// @param string $operator Optional. The logical operation to perform. 'AND' means
#// all elements from the array must match. 'OR' means only
#// one element needs to match. 'NOT' means no elements may
#// match. Default 'AND'.
#// @return array Array of found values.
#//
def wp_list_filter(list=None, args=Array(), operator="AND", *args_):
    
    if (not php_is_array(list)):
        return Array()
    # end if
    util = php_new_class("WP_List_Util", lambda : WP_List_Util(list))
    return util.filter(args, operator)
# end def wp_list_filter
#// 
#// Pluck a certain field out of each object in a list.
#// 
#// This has the same functionality and prototype of
#// array_column() (PHP 5.5) but also supports objects.
#// 
#// @since 3.1.0
#// @since 4.0.0 $index_key parameter added.
#// @since 4.7.0 Uses `WP_List_Util` class.
#// 
#// @param array      $list      List of objects or arrays
#// @param int|string $field     Field from the object to place instead of the entire object
#// @param int|string $index_key Optional. Field from the object to use as keys for the new array.
#// Default null.
#// @return array Array of found values. If `$index_key` is set, an array of found values with keys
#// corresponding to `$index_key`. If `$index_key` is null, array keys from the original
#// `$list` will be preserved in the results.
#//
def wp_list_pluck(list=None, field=None, index_key=None, *args_):
    
    util = php_new_class("WP_List_Util", lambda : WP_List_Util(list))
    return util.pluck(field, index_key)
# end def wp_list_pluck
#// 
#// Sorts a list of objects, based on one or more orderby arguments.
#// 
#// @since 4.7.0
#// 
#// @param array        $list          An array of objects to sort.
#// @param string|array $orderby       Optional. Either the field name to order by or an array
#// of multiple orderby fields as $orderby => $order.
#// @param string       $order         Optional. Either 'ASC' or 'DESC'. Only used if $orderby
#// is a string.
#// @param bool         $preserve_keys Optional. Whether to preserve keys. Default false.
#// @return array The sorted array.
#//
def wp_list_sort(list=None, orderby=Array(), order="ASC", preserve_keys=False, *args_):
    
    if (not php_is_array(list)):
        return Array()
    # end if
    util = php_new_class("WP_List_Util", lambda : WP_List_Util(list))
    return util.sort(orderby, order, preserve_keys)
# end def wp_list_sort
#// 
#// Determines if Widgets library should be loaded.
#// 
#// Checks to make sure that the widgets library hasn't already been loaded.
#// If it hasn't, then it will load the widgets library and run an action hook.
#// 
#// @since 2.2.0
#//
def wp_maybe_load_widgets(*args_):
    
    #// 
    #// Filters whether to load the Widgets library.
    #// 
    #// Passing a falsey value to the filter will effectively short-circuit
    #// the Widgets library from loading.
    #// 
    #// @since 2.8.0
    #// 
    #// @param bool $wp_maybe_load_widgets Whether to load the Widgets library.
    #// Default true.
    #//
    if (not apply_filters("load_default_widgets", True)):
        return
    # end if
    php_include_file(ABSPATH + WPINC + "/default-widgets.php", once=True)
    add_action("_admin_menu", "wp_widgets_add_menu")
# end def wp_maybe_load_widgets
#// 
#// Append the Widgets menu to the themes main menu.
#// 
#// @since 2.2.0
#// 
#// @global array $submenu
#//
def wp_widgets_add_menu(*args_):
    
    global submenu
    php_check_if_defined("submenu")
    if (not current_theme_supports("widgets")):
        return
    # end if
    submenu["themes.php"][7] = Array(__("Widgets"), "edit_theme_options", "widgets.php")
    ksort(submenu["themes.php"], SORT_NUMERIC)
# end def wp_widgets_add_menu
#// 
#// Flush all output buffers for PHP 5.2.
#// 
#// Make sure all output buffers are flushed before our singletons are destroyed.
#// 
#// @since 2.2.0
#//
def wp_ob_end_flush_all(*args_):
    
    levels = ob_get_level()
    i = 0
    while i < levels:
        
        ob_end_flush()
        i += 1
    # end while
# end def wp_ob_end_flush_all
#// 
#// Load custom DB error or display WordPress DB error.
#// 
#// If a file exists in the wp-content directory named db-error.php, then it will
#// be loaded instead of displaying the WordPress DB error. If it is not found,
#// then the WordPress DB error will be displayed instead.
#// 
#// The WordPress DB error sets the HTTP status header to 500 to try to prevent
#// search engines from caching the message. Custom DB messages should do the
#// same.
#// 
#// This function was backported to WordPress 2.3.2, but originally was added
#// in WordPress 2.5.0.
#// 
#// @since 2.3.2
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#//
def dead_db(*args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    wp_load_translations_early()
    #// Load custom DB error template, if present.
    if php_file_exists(WP_CONTENT_DIR + "/db-error.php"):
        php_include_file(WP_CONTENT_DIR + "/db-error.php", once=True)
        php_exit(0)
    # end if
    #// If installing or in the admin, provide the verbose message.
    if wp_installing() or php_defined("WP_ADMIN"):
        wp_die(wpdb.error)
    # end if
    #// Otherwise, be terse.
    wp_die("<h1>" + __("Error establishing a database connection") + "</h1>", __("Database Error"))
# end def dead_db
#// 
#// Convert a value to non-negative integer.
#// 
#// @since 2.5.0
#// 
#// @param mixed $maybeint Data you wish to have converted to a non-negative integer.
#// @return int A non-negative integer.
#//
def absint(maybeint=None, *args_):
    
    return abs(php_intval(maybeint))
# end def absint
#// 
#// Mark a function as deprecated and inform when it has been used.
#// 
#// There is a {@see 'hook deprecated_function_run'} that will be called that can be used
#// to get the backtrace up to what file and function called the deprecated
#// function.
#// 
#// The current behavior is to trigger a user error if `WP_DEBUG` is true.
#// 
#// This function is to be used in every function that is deprecated.
#// 
#// @since 2.5.0
#// @since 5.4.0 This function is no longer marked as "private".
#// @since 5.4.0 The error type is now classified as E_USER_DEPRECATED (used to default to E_USER_NOTICE).
#// 
#// @param string $function    The function that was called.
#// @param string $version     The version of WordPress that deprecated the function.
#// @param string $replacement Optional. The function that should have been called. Default null.
#//
def _deprecated_function(function=None, version=None, replacement=None, *args_):
    
    #// 
    #// Fires when a deprecated function is called.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $function    The function that was called.
    #// @param string $replacement The function that should have been called.
    #// @param string $version     The version of WordPress that deprecated the function.
    #//
    do_action("deprecated_function_run", function, replacement, version)
    #// 
    #// Filters whether to trigger an error for deprecated functions.
    #// 
    #// @since 2.5.0
    #// 
    #// @param bool $trigger Whether to trigger the error for deprecated functions. Default true.
    #//
    if WP_DEBUG and apply_filters("deprecated_function_trigger_error", True):
        if php_function_exists("__"):
            if (not is_null(replacement)):
                trigger_error(php_sprintf(__("%1$s is <strong>deprecated</strong> since version %2$s! Use %3$s instead."), function, version, replacement), E_USER_DEPRECATED)
            else:
                trigger_error(php_sprintf(__("%1$s is <strong>deprecated</strong> since version %2$s with no alternative available."), function, version), E_USER_DEPRECATED)
            # end if
        else:
            if (not is_null(replacement)):
                trigger_error(php_sprintf("%1$s is <strong>deprecated</strong> since version %2$s! Use %3$s instead.", function, version, replacement), E_USER_DEPRECATED)
            else:
                trigger_error(php_sprintf("%1$s is <strong>deprecated</strong> since version %2$s with no alternative available.", function, version), E_USER_DEPRECATED)
            # end if
        # end if
    # end if
# end def _deprecated_function
#// 
#// Marks a constructor as deprecated and informs when it has been used.
#// 
#// Similar to _deprecated_function(), but with different strings. Used to
#// remove PHP4 style constructors.
#// 
#// The current behavior is to trigger a user error if `WP_DEBUG` is true.
#// 
#// This function is to be used in every PHP4 style constructor method that is deprecated.
#// 
#// @since 4.3.0
#// @since 4.5.0 Added the `$parent_class` parameter.
#// @since 5.4.0 This function is no longer marked as "private".
#// @since 5.4.0 The error type is now classified as E_USER_DEPRECATED (used to default to E_USER_NOTICE).
#// 
#// @param string $class        The class containing the deprecated constructor.
#// @param string $version      The version of WordPress that deprecated the function.
#// @param string $parent_class Optional. The parent class calling the deprecated constructor.
#// Default empty string.
#//
def _deprecated_constructor(class_=None, version=None, parent_class="", *args_):
    
    #// 
    #// Fires when a deprecated constructor is called.
    #// 
    #// @since 4.3.0
    #// @since 4.5.0 Added the `$parent_class` parameter.
    #// 
    #// @param string $class        The class containing the deprecated constructor.
    #// @param string $version      The version of WordPress that deprecated the function.
    #// @param string $parent_class The parent class calling the deprecated constructor.
    #//
    do_action("deprecated_constructor_run", class_, version, parent_class)
    #// 
    #// Filters whether to trigger an error for deprecated functions.
    #// 
    #// `WP_DEBUG` must be true in addition to the filter evaluating to true.
    #// 
    #// @since 4.3.0
    #// 
    #// @param bool $trigger Whether to trigger the error for deprecated functions. Default true.
    #//
    if WP_DEBUG and apply_filters("deprecated_constructor_trigger_error", True):
        if php_function_exists("__"):
            if (not php_empty(lambda : parent_class)):
                trigger_error(php_sprintf(__("The called constructor method for %1$s in %2$s is <strong>deprecated</strong> since version %3$s! Use %4$s instead."), class_, parent_class, version, "<code>__construct()</code>"), E_USER_DEPRECATED)
            else:
                trigger_error(php_sprintf(__("The called constructor method for %1$s is <strong>deprecated</strong> since version %2$s! Use %3$s instead."), class_, version, "<code>__construct()</code>"), E_USER_DEPRECATED)
            # end if
        else:
            if (not php_empty(lambda : parent_class)):
                trigger_error(php_sprintf("The called constructor method for %1$s in %2$s is <strong>deprecated</strong> since version %3$s! Use %4$s instead.", class_, parent_class, version, "<code>__construct()</code>"), E_USER_DEPRECATED)
            else:
                trigger_error(php_sprintf("The called constructor method for %1$s is <strong>deprecated</strong> since version %2$s! Use %3$s instead.", class_, version, "<code>__construct()</code>"), E_USER_DEPRECATED)
            # end if
        # end if
    # end if
# end def _deprecated_constructor
#// 
#// Mark a file as deprecated and inform when it has been used.
#// 
#// There is a hook {@see 'deprecated_file_included'} that will be called that can be used
#// to get the backtrace up to what file and function included the deprecated
#// file.
#// 
#// The current behavior is to trigger a user error if `WP_DEBUG` is true.
#// 
#// This function is to be used in every file that is deprecated.
#// 
#// @since 2.5.0
#// @since 5.4.0 This function is no longer marked as "private".
#// @since 5.4.0 The error type is now classified as E_USER_DEPRECATED (used to default to E_USER_NOTICE).
#// 
#// @param string $file        The file that was included.
#// @param string $version     The version of WordPress that deprecated the file.
#// @param string $replacement Optional. The file that should have been included based on ABSPATH.
#// Default null.
#// @param string $message     Optional. A message regarding the change. Default empty.
#//
def _deprecated_file(file=None, version=None, replacement=None, message="", *args_):
    
    #// 
    #// Fires when a deprecated file is called.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $file        The file that was called.
    #// @param string $replacement The file that should have been included based on ABSPATH.
    #// @param string $version     The version of WordPress that deprecated the file.
    #// @param string $message     A message regarding the change.
    #//
    do_action("deprecated_file_included", file, replacement, version, message)
    #// 
    #// Filters whether to trigger an error for deprecated files.
    #// 
    #// @since 2.5.0
    #// 
    #// @param bool $trigger Whether to trigger the error for deprecated files. Default true.
    #//
    if WP_DEBUG and apply_filters("deprecated_file_trigger_error", True):
        message = "" if php_empty(lambda : message) else " " + message
        if php_function_exists("__"):
            if (not is_null(replacement)):
                trigger_error(php_sprintf(__("%1$s is <strong>deprecated</strong> since version %2$s! Use %3$s instead."), file, version, replacement) + message, E_USER_DEPRECATED)
            else:
                trigger_error(php_sprintf(__("%1$s is <strong>deprecated</strong> since version %2$s with no alternative available."), file, version) + message, E_USER_DEPRECATED)
            # end if
        else:
            if (not is_null(replacement)):
                trigger_error(php_sprintf("%1$s is <strong>deprecated</strong> since version %2$s! Use %3$s instead.", file, version, replacement) + message, E_USER_DEPRECATED)
            else:
                trigger_error(php_sprintf("%1$s is <strong>deprecated</strong> since version %2$s with no alternative available.", file, version) + message, E_USER_DEPRECATED)
            # end if
        # end if
    # end if
# end def _deprecated_file
#// 
#// Mark a function argument as deprecated and inform when it has been used.
#// 
#// This function is to be used whenever a deprecated function argument is used.
#// Before this function is called, the argument must be checked for whether it was
#// used by comparing it to its default value or evaluating whether it is empty.
#// For example:
#// 
#// if ( ! empty( $deprecated ) ) {
#// _deprecated_argument( __FUNCTION__, '3.0.0' );
#// }
#// 
#// There is a hook deprecated_argument_run that will be called that can be used
#// to get the backtrace up to what file and function used the deprecated
#// argument.
#// 
#// The current behavior is to trigger a user error if WP_DEBUG is true.
#// 
#// @since 3.0.0
#// @since 5.4.0 This function is no longer marked as "private".
#// @since 5.4.0 The error type is now classified as E_USER_DEPRECATED (used to default to E_USER_NOTICE).
#// 
#// @param string $function The function that was called.
#// @param string $version  The version of WordPress that deprecated the argument used.
#// @param string $message  Optional. A message regarding the change. Default null.
#//
def _deprecated_argument(function=None, version=None, message=None, *args_):
    
    #// 
    #// Fires when a deprecated argument is called.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string $function The function that was called.
    #// @param string $message  A message regarding the change.
    #// @param string $version  The version of WordPress that deprecated the argument used.
    #//
    do_action("deprecated_argument_run", function, message, version)
    #// 
    #// Filters whether to trigger an error for deprecated arguments.
    #// 
    #// @since 3.0.0
    #// 
    #// @param bool $trigger Whether to trigger the error for deprecated arguments. Default true.
    #//
    if WP_DEBUG and apply_filters("deprecated_argument_trigger_error", True):
        if php_function_exists("__"):
            if (not is_null(message)):
                trigger_error(php_sprintf(__("%1$s was called with an argument that is <strong>deprecated</strong> since version %2$s! %3$s"), function, version, message), E_USER_DEPRECATED)
            else:
                trigger_error(php_sprintf(__("%1$s was called with an argument that is <strong>deprecated</strong> since version %2$s with no alternative available."), function, version), E_USER_DEPRECATED)
            # end if
        else:
            if (not is_null(message)):
                trigger_error(php_sprintf("%1$s was called with an argument that is <strong>deprecated</strong> since version %2$s! %3$s", function, version, message), E_USER_DEPRECATED)
            else:
                trigger_error(php_sprintf("%1$s was called with an argument that is <strong>deprecated</strong> since version %2$s with no alternative available.", function, version), E_USER_DEPRECATED)
            # end if
        # end if
    # end if
# end def _deprecated_argument
#// 
#// Marks a deprecated action or filter hook as deprecated and throws a notice.
#// 
#// Use the {@see 'deprecated_hook_run'} action to get the backtrace describing where
#// the deprecated hook was called.
#// 
#// Default behavior is to trigger a user error if `WP_DEBUG` is true.
#// 
#// This function is called by the do_action_deprecated() and apply_filters_deprecated()
#// functions, and so generally does not need to be called directly.
#// 
#// @since 4.6.0
#// @since 5.4.0 The error type is now classified as E_USER_DEPRECATED (used to default to E_USER_NOTICE).
#// @access private
#// 
#// @param string $hook        The hook that was used.
#// @param string $version     The version of WordPress that deprecated the hook.
#// @param string $replacement Optional. The hook that should have been used. Default null.
#// @param string $message     Optional. A message regarding the change. Default null.
#//
def _deprecated_hook(hook=None, version=None, replacement=None, message=None, *args_):
    
    #// 
    #// Fires when a deprecated hook is called.
    #// 
    #// @since 4.6.0
    #// 
    #// @param string $hook        The hook that was called.
    #// @param string $replacement The hook that should be used as a replacement.
    #// @param string $version     The version of WordPress that deprecated the argument used.
    #// @param string $message     A message regarding the change.
    #//
    do_action("deprecated_hook_run", hook, replacement, version, message)
    #// 
    #// Filters whether to trigger deprecated hook errors.
    #// 
    #// @since 4.6.0
    #// 
    #// @param bool $trigger Whether to trigger deprecated hook errors. Requires
    #// `WP_DEBUG` to be defined true.
    #//
    if WP_DEBUG and apply_filters("deprecated_hook_trigger_error", True):
        message = "" if php_empty(lambda : message) else " " + message
        if (not is_null(replacement)):
            trigger_error(php_sprintf(__("%1$s is <strong>deprecated</strong> since version %2$s! Use %3$s instead."), hook, version, replacement) + message, E_USER_DEPRECATED)
        else:
            trigger_error(php_sprintf(__("%1$s is <strong>deprecated</strong> since version %2$s with no alternative available."), hook, version) + message, E_USER_DEPRECATED)
        # end if
    # end if
# end def _deprecated_hook
#// 
#// Mark something as being incorrectly called.
#// 
#// There is a hook {@see 'doing_it_wrong_run'} that will be called that can be used
#// to get the backtrace up to what file and function called the deprecated
#// function.
#// 
#// The current behavior is to trigger a user error if `WP_DEBUG` is true.
#// 
#// @since 3.1.0
#// @since 5.4.0 This function is no longer marked as "private".
#// 
#// @param string $function The function that was called.
#// @param string $message  A message explaining what has been done incorrectly.
#// @param string $version  The version of WordPress where the message was added.
#//
def _doing_it_wrong(function=None, message=None, version=None, *args_):
    
    #// 
    #// Fires when the given function is being used incorrectly.
    #// 
    #// @since 3.1.0
    #// 
    #// @param string $function The function that was called.
    #// @param string $message  A message explaining what has been done incorrectly.
    #// @param string $version  The version of WordPress where the message was added.
    #//
    do_action("doing_it_wrong_run", function, message, version)
    #// 
    #// Filters whether to trigger an error for _doing_it_wrong() calls.
    #// 
    #// @since 3.1.0
    #// @since 5.1.0 Added the $function, $message and $version parameters.
    #// 
    #// @param bool   $trigger  Whether to trigger the error for _doing_it_wrong() calls. Default true.
    #// @param string $function The function that was called.
    #// @param string $message  A message explaining what has been done incorrectly.
    #// @param string $version  The version of WordPress where the message was added.
    #//
    if WP_DEBUG and apply_filters("doing_it_wrong_trigger_error", True, function, message, version):
        if php_function_exists("__"):
            if is_null(version):
                version = ""
            else:
                #// translators: %s: Version number.
                version = php_sprintf(__("(This message was added in version %s.)"), version)
            # end if
            message += " " + php_sprintf(__("Please see <a href=\"%s\">Debugging in WordPress</a> for more information."), __("https://wordpress.org/support/article/debugging-in-wordpress/"))
            trigger_error(php_sprintf(__("%1$s was called <strong>incorrectly</strong>. %2$s %3$s"), function, message, version), E_USER_NOTICE)
        else:
            if is_null(version):
                version = ""
            else:
                version = php_sprintf("(This message was added in version %s.)", version)
            # end if
            message += php_sprintf(" Please see <a href=\"%s\">Debugging in WordPress</a> for more information.", "https://wordpress.org/support/article/debugging-in-wordpress/")
            trigger_error(php_sprintf("%1$s was called <strong>incorrectly</strong>. %2$s %3$s", function, message, version), E_USER_NOTICE)
        # end if
    # end if
# end def _doing_it_wrong
#// 
#// Is the server running earlier than 1.5.0 version of lighttpd?
#// 
#// @since 2.5.0
#// 
#// @return bool Whether the server is running lighttpd < 1.5.0.
#//
def is_lighttpd_before_150(*args_):
    
    server_parts = php_explode("/", PHP_SERVER["SERVER_SOFTWARE"] if (php_isset(lambda : PHP_SERVER["SERVER_SOFTWARE"])) else "")
    server_parts[1] = server_parts[1] if (php_isset(lambda : server_parts[1])) else ""
    return "lighttpd" == server_parts[0] and -1 == php_version_compare(server_parts[1], "1.5.0")
# end def is_lighttpd_before_150
#// 
#// Does the specified module exist in the Apache config?
#// 
#// @since 2.5.0
#// 
#// @global bool $is_apache
#// 
#// @param string $mod     The module, e.g. mod_rewrite.
#// @param bool   $default Optional. The default return value if the module is not found. Default false.
#// @return bool Whether the specified module is loaded.
#//
def apache_mod_loaded(mod=None, default=False, *args_):
    
    global is_apache
    php_check_if_defined("is_apache")
    if (not is_apache):
        return False
    # end if
    if php_function_exists("apache_get_modules"):
        mods = apache_get_modules()
        if php_in_array(mod, mods):
            return True
        # end if
    elif php_function_exists("phpinfo") and False == php_strpos(php_ini_get("disable_functions"), "phpinfo"):
        ob_start()
        phpinfo(8)
        phpinfo = ob_get_clean()
        if False != php_strpos(phpinfo, mod):
            return True
        # end if
    # end if
    return default
# end def apache_mod_loaded
#// 
#// Check if IIS 7+ supports pretty permalinks.
#// 
#// @since 2.8.0
#// 
#// @global bool $is_iis7
#// 
#// @return bool Whether IIS7 supports permalinks.
#//
def iis7_supports_permalinks(*args_):
    
    global is_iis7
    php_check_if_defined("is_iis7")
    supports_permalinks = False
    if is_iis7:
        #// First we check if the DOMDocument class exists. If it does not exist, then we cannot
        #// easily update the xml configuration file, hence we just bail out and tell user that
        #// pretty permalinks cannot be used.
        #// 
        #// Next we check if the URL Rewrite Module 1.1 is loaded and enabled for the web site. When
        #// URL Rewrite 1.1 is loaded it always sets a server variable called 'IIS_UrlRewriteModule'.
        #// Lastly we make sure that PHP is running via FastCGI. This is important because if it runs
        #// via ISAPI then pretty permalinks will not work.
        #//
        supports_permalinks = php_class_exists("DOMDocument", False) and (php_isset(lambda : PHP_SERVER["IIS_UrlRewriteModule"])) and PHP_SAPI == "cgi-fcgi"
    # end if
    #// 
    #// Filters whether IIS 7+ supports pretty permalinks.
    #// 
    #// @since 2.8.0
    #// 
    #// @param bool $supports_permalinks Whether IIS7 supports permalinks. Default false.
    #//
    return apply_filters("iis7_supports_permalinks", supports_permalinks)
# end def iis7_supports_permalinks
#// 
#// Validates a file name and path against an allowed set of rules.
#// 
#// A return value of `1` means the file path contains directory traversal.
#// 
#// A return value of `2` means the file path contains a Windows drive path.
#// 
#// A return value of `3` means the file is not in the allowed files list.
#// 
#// @since 1.2.0
#// 
#// @param string   $file          File path.
#// @param string[] $allowed_files Optional. Array of allowed files.
#// @return int 0 means nothing is wrong, greater than 0 means something was wrong.
#//
def validate_file(file=None, allowed_files=Array(), *args_):
    
    #// `../` on its own is not allowed:
    if "../" == file:
        return 1
    # end if
    #// More than one occurence of `../` is not allowed:
    if preg_match_all("#\\.\\./#", file, matches, PREG_SET_ORDER) and php_count(matches) > 1:
        return 1
    # end if
    #// `../` which does not occur at the end of the path is not allowed:
    if False != php_strpos(file, "../") and "../" != php_mb_substr(file, -3, 3):
        return 1
    # end if
    #// Files not in the allowed file list are not allowed:
    if (not php_empty(lambda : allowed_files)) and (not php_in_array(file, allowed_files)):
        return 3
    # end if
    #// Absolute Windows drive paths are not allowed:
    if ":" == php_substr(file, 1, 1):
        return 2
    # end if
    return 0
# end def validate_file
#// 
#// Whether to force SSL used for the Administration Screens.
#// 
#// @since 2.6.0
#// 
#// @staticvar bool $forced
#// 
#// @param string|bool $force Optional. Whether to force SSL in admin screens. Default null.
#// @return bool True if forced, false if not forced.
#//
def force_ssl_admin(force=None, *args_):
    
    forced = False
    if (not is_null(force)):
        old_forced = forced
        forced = force
        return old_forced
    # end if
    return forced
# end def force_ssl_admin
#// 
#// Guess the URL for the site.
#// 
#// Will remove wp-admin links to retrieve only return URLs not in the wp-admin
#// directory.
#// 
#// @since 2.6.0
#// 
#// @return string The guessed URL.
#//
def wp_guess_url(*args_):
    
    if php_defined("WP_SITEURL") and "" != WP_SITEURL:
        url = WP_SITEURL
    else:
        abspath_fix = php_str_replace("\\", "/", ABSPATH)
        script_filename_dir = php_dirname(PHP_SERVER["SCRIPT_FILENAME"])
        #// The request is for the admin.
        if php_strpos(PHP_SERVER["REQUEST_URI"], "wp-admin") != False or php_strpos(PHP_SERVER["REQUEST_URI"], "wp-login.php") != False:
            path = php_preg_replace("#/(wp-admin/.*|wp-login.php)#i", "", PHP_SERVER["REQUEST_URI"])
            pass
        elif script_filename_dir + "/" == abspath_fix:
            #// Strip off any file/query params in the path.
            path = php_preg_replace("#/[^/]*$#i", "", PHP_SERVER["PHP_SELF"])
        else:
            if False != php_strpos(PHP_SERVER["SCRIPT_FILENAME"], abspath_fix):
                #// Request is hitting a file inside ABSPATH.
                directory = php_str_replace(ABSPATH, "", script_filename_dir)
                #// Strip off the subdirectory, and any file/query params.
                path = php_preg_replace("#/" + preg_quote(directory, "#") + "/[^/]*$#i", "", PHP_SERVER["REQUEST_URI"])
            elif False != php_strpos(abspath_fix, script_filename_dir):
                #// Request is hitting a file above ABSPATH.
                subdirectory = php_substr(abspath_fix, php_strpos(abspath_fix, script_filename_dir) + php_strlen(script_filename_dir))
                #// Strip off any file/query params from the path, appending the subdirectory to the installation.
                path = php_preg_replace("#/[^/]*$#i", "", PHP_SERVER["REQUEST_URI"]) + subdirectory
            else:
                path = PHP_SERVER["REQUEST_URI"]
            # end if
        # end if
        schema = "https://" if is_ssl() else "http://"
        #// set_url_scheme() is not defined yet.
        url = schema + PHP_SERVER["HTTP_HOST"] + path
    # end if
    return php_rtrim(url, "/")
# end def wp_guess_url
#// 
#// Temporarily suspend cache additions.
#// 
#// Stops more data being added to the cache, but still allows cache retrieval.
#// This is useful for actions, such as imports, when a lot of data would otherwise
#// be almost uselessly added to the cache.
#// 
#// Suspension lasts for a single page load at most. Remember to call this
#// function again if you wish to re-enable cache adds earlier.
#// 
#// @since 3.3.0
#// 
#// @staticvar bool $_suspend
#// 
#// @param bool $suspend Optional. Suspends additions if true, re-enables them if false.
#// @return bool The current suspend setting
#//
def wp_suspend_cache_addition(suspend=None, *args_):
    
    _suspend = False
    if php_is_bool(suspend):
        _suspend = suspend
    # end if
    return _suspend
# end def wp_suspend_cache_addition
#// 
#// Suspend cache invalidation.
#// 
#// Turns cache invalidation on and off. Useful during imports where you don't want to do
#// invalidations every time a post is inserted. Callers must be sure that what they are
#// doing won't lead to an inconsistent cache when invalidation is suspended.
#// 
#// @since 2.7.0
#// 
#// @global bool $_wp_suspend_cache_invalidation
#// 
#// @param bool $suspend Optional. Whether to suspend or enable cache invalidation. Default true.
#// @return bool The current suspend setting.
#//
def wp_suspend_cache_invalidation(suspend=True, *args_):
    
    global _wp_suspend_cache_invalidation
    php_check_if_defined("_wp_suspend_cache_invalidation")
    current_suspend = _wp_suspend_cache_invalidation
    _wp_suspend_cache_invalidation = suspend
    return current_suspend
# end def wp_suspend_cache_invalidation
#// 
#// Determine whether a site is the main site of the current network.
#// 
#// @since 3.0.0
#// @since 4.9.0 The `$network_id` parameter was added.
#// 
#// @param int $site_id    Optional. Site ID to test. Defaults to current site.
#// @param int $network_id Optional. Network ID of the network to check for.
#// Defaults to current network.
#// @return bool True if $site_id is the main site of the network, or if not
#// running Multisite.
#//
def is_main_site(site_id=None, network_id=None, *args_):
    
    if (not is_multisite()):
        return True
    # end if
    if (not site_id):
        site_id = get_current_blog_id()
    # end if
    site_id = php_int(site_id)
    return get_main_site_id(network_id) == site_id
# end def is_main_site
#// 
#// Gets the main site ID.
#// 
#// @since 4.9.0
#// 
#// @param int $network_id Optional. The ID of the network for which to get the main site.
#// Defaults to the current network.
#// @return int The ID of the main site.
#//
def get_main_site_id(network_id=None, *args_):
    
    if (not is_multisite()):
        return get_current_blog_id()
    # end if
    network = get_network(network_id)
    if (not network):
        return 0
    # end if
    return network.site_id
# end def get_main_site_id
#// 
#// Determine whether a network is the main network of the Multisite installation.
#// 
#// @since 3.7.0
#// 
#// @param int $network_id Optional. Network ID to test. Defaults to current network.
#// @return bool True if $network_id is the main network, or if not running Multisite.
#//
def is_main_network(network_id=None, *args_):
    
    if (not is_multisite()):
        return True
    # end if
    if None == network_id:
        network_id = get_current_network_id()
    # end if
    network_id = php_int(network_id)
    return get_main_network_id() == network_id
# end def is_main_network
#// 
#// Get the main network ID.
#// 
#// @since 4.3.0
#// 
#// @return int The ID of the main network.
#//
def get_main_network_id(*args_):
    
    if (not is_multisite()):
        return 1
    # end if
    current_network = get_network()
    if php_defined("PRIMARY_NETWORK_ID"):
        main_network_id = PRIMARY_NETWORK_ID
    elif (php_isset(lambda : current_network.id)) and 1 == php_int(current_network.id):
        #// If the current network has an ID of 1, assume it is the main network.
        main_network_id = 1
    else:
        _networks = get_networks(Array({"fields": "ids", "number": 1}))
        main_network_id = php_array_shift(_networks)
    # end if
    #// 
    #// Filters the main network ID.
    #// 
    #// @since 4.3.0
    #// 
    #// @param int $main_network_id The ID of the main network.
    #//
    return php_int(apply_filters("get_main_network_id", main_network_id))
# end def get_main_network_id
#// 
#// Determine whether global terms are enabled.
#// 
#// @since 3.0.0
#// 
#// @staticvar bool $global_terms
#// 
#// @return bool True if multisite and global terms enabled.
#//
def global_terms_enabled(*args_):
    
    if (not is_multisite()):
        return False
    # end if
    global_terms = None
    if is_null(global_terms):
        #// 
        #// Filters whether global terms are enabled.
        #// 
        #// Passing a non-null value to the filter will effectively short-circuit the function,
        #// returning the value of the 'global_terms_enabled' site option instead.
        #// 
        #// @since 3.0.0
        #// 
        #// @param null $enabled Whether global terms are enabled.
        #//
        filter = apply_filters("global_terms_enabled", None)
        if (not is_null(filter)):
            global_terms = php_bool(filter)
        else:
            global_terms = php_bool(get_site_option("global_terms_enabled", False))
        # end if
    # end if
    return global_terms
# end def global_terms_enabled
#// 
#// Determines whether site meta is enabled.
#// 
#// This function checks whether the 'blogmeta' database table exists. The result is saved as
#// a setting for the main network, making it essentially a global setting. Subsequent requests
#// will refer to this setting instead of running the query.
#// 
#// @since 5.1.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @return bool True if site meta is supported, false otherwise.
#//
def is_site_meta_supported(*args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if (not is_multisite()):
        return False
    # end if
    network_id = get_main_network_id()
    supported = get_network_option(network_id, "site_meta_supported", False)
    if False == supported:
        supported = 1 if wpdb.get_var(str("SHOW TABLES LIKE '") + str(wpdb.blogmeta) + str("'")) else 0
        update_network_option(network_id, "site_meta_supported", supported)
    # end if
    return php_bool(supported)
# end def is_site_meta_supported
#// 
#// gmt_offset modification for smart timezone handling.
#// 
#// Overrides the gmt_offset option if we have a timezone_string available.
#// 
#// @since 2.8.0
#// 
#// @return float|false Timezone GMT offset, false otherwise.
#//
def wp_timezone_override_offset(*args_):
    
    timezone_string = get_option("timezone_string")
    if (not timezone_string):
        return False
    # end if
    timezone_object = timezone_open(timezone_string)
    datetime_object = date_create()
    if False == timezone_object or False == datetime_object:
        return False
    # end if
    return round(timezone_offset_get(timezone_object, datetime_object) / HOUR_IN_SECONDS, 2)
# end def wp_timezone_override_offset
#// 
#// Sort-helper for timezones.
#// 
#// @since 2.9.0
#// @access private
#// 
#// @param array $a
#// @param array $b
#// @return int
#//
def _wp_timezone_choice_usort_callback(a=None, b=None, *args_):
    
    #// Don't use translated versions of Etc.
    if "Etc" == a["continent"] and "Etc" == b["continent"]:
        #// Make the order of these more like the old dropdown.
        if "GMT+" == php_substr(a["city"], 0, 4) and "GMT+" == php_substr(b["city"], 0, 4):
            return -1 * strnatcasecmp(a["city"], b["city"])
        # end if
        if "UTC" == a["city"]:
            if "GMT+" == php_substr(b["city"], 0, 4):
                return 1
            # end if
            return -1
        # end if
        if "UTC" == b["city"]:
            if "GMT+" == php_substr(a["city"], 0, 4):
                return -1
            # end if
            return 1
        # end if
        return strnatcasecmp(a["city"], b["city"])
    # end if
    if a["t_continent"] == b["t_continent"]:
        if a["t_city"] == b["t_city"]:
            return strnatcasecmp(a["t_subcity"], b["t_subcity"])
        # end if
        return strnatcasecmp(a["t_city"], b["t_city"])
    else:
        #// Force Etc to the bottom of the list.
        if "Etc" == a["continent"]:
            return 1
        # end if
        if "Etc" == b["continent"]:
            return -1
        # end if
        return strnatcasecmp(a["t_continent"], b["t_continent"])
    # end if
# end def _wp_timezone_choice_usort_callback
#// 
#// Gives a nicely-formatted list of timezone strings.
#// 
#// @since 2.9.0
#// @since 4.7.0 Added the `$locale` parameter.
#// 
#// @staticvar bool $mo_loaded
#// @staticvar string $locale_loaded
#// 
#// @param string $selected_zone Selected timezone.
#// @param string $locale        Optional. Locale to load the timezones in. Default current site locale.
#// @return string
#//
def wp_timezone_choice(selected_zone=None, locale=None, *args_):
    
    mo_loaded = False
    locale_loaded = None
    continents = Array("Africa", "America", "Antarctica", "Arctic", "Asia", "Atlantic", "Australia", "Europe", "Indian", "Pacific")
    #// Load translations for continents and cities.
    if (not mo_loaded) or locale != locale_loaded:
        locale_loaded = locale if locale else get_locale()
        mofile = WP_LANG_DIR + "/continents-cities-" + locale_loaded + ".mo"
        unload_textdomain("continents-cities")
        load_textdomain("continents-cities", mofile)
        mo_loaded = True
    # end if
    zonen = Array()
    for zone in timezone_identifiers_list():
        zone = php_explode("/", zone)
        if (not php_in_array(zone[0], continents)):
            continue
        # end if
        #// This determines what gets set and translated - we don't translate Etc/* strings here, they are done later.
        exists = Array({0: (php_isset(lambda : zone[0])) and zone[0], 1: (php_isset(lambda : zone[1])) and zone[1], 2: (php_isset(lambda : zone[2])) and zone[2]})
        exists[3] = exists[0] and "Etc" != zone[0]
        exists[4] = exists[1] and exists[3]
        exists[5] = exists[2] and exists[3]
        #// phpcs:disable WordPress.WP.I18n.LowLevelTranslationFunction,WordPress.WP.I18n.NonSingularStringLiteralText
        zonen[-1] = Array({"continent": zone[0] if exists[0] else "", "city": zone[1] if exists[1] else "", "subcity": zone[2] if exists[2] else "", "t_continent": translate(php_str_replace("_", " ", zone[0]), "continents-cities") if exists[3] else "", "t_city": translate(php_str_replace("_", " ", zone[1]), "continents-cities") if exists[4] else "", "t_subcity": translate(php_str_replace("_", " ", zone[2]), "continents-cities") if exists[5] else ""})
        pass
    # end for
    usort(zonen, "_wp_timezone_choice_usort_callback")
    structure = Array()
    if php_empty(lambda : selected_zone):
        structure[-1] = "<option selected=\"selected\" value=\"\">" + __("Select a city") + "</option>"
    # end if
    for key,zone in zonen:
        #// Build value in an array to join later.
        value = Array(zone["continent"])
        if php_empty(lambda : zone["city"]):
            #// It's at the continent level (generally won't happen).
            display = zone["t_continent"]
        else:
            #// It's inside a continent group.
            #// Continent optgroup.
            if (not (php_isset(lambda : zonen[key - 1]))) or zonen[key - 1]["continent"] != zone["continent"]:
                label = zone["t_continent"]
                structure[-1] = "<optgroup label=\"" + esc_attr(label) + "\">"
            # end if
            #// Add the city to the value.
            value[-1] = zone["city"]
            display = zone["t_city"]
            if (not php_empty(lambda : zone["subcity"])):
                #// Add the subcity to the value.
                value[-1] = zone["subcity"]
                display += " - " + zone["t_subcity"]
            # end if
        # end if
        #// Build the value.
        value = join("/", value)
        selected = ""
        if value == selected_zone:
            selected = "selected=\"selected\" "
        # end if
        structure[-1] = "<option " + selected + "value=\"" + esc_attr(value) + "\">" + esc_html(display) + "</option>"
        #// Close continent optgroup.
        if (not php_empty(lambda : zone["city"])) and (not (php_isset(lambda : zonen[key + 1]))) or (php_isset(lambda : zonen[key + 1])) and zonen[key + 1]["continent"] != zone["continent"]:
            structure[-1] = "</optgroup>"
        # end if
    # end for
    #// Do UTC.
    structure[-1] = "<optgroup label=\"" + esc_attr__("UTC") + "\">"
    selected = ""
    if "UTC" == selected_zone:
        selected = "selected=\"selected\" "
    # end if
    structure[-1] = "<option " + selected + "value=\"" + esc_attr("UTC") + "\">" + __("UTC") + "</option>"
    structure[-1] = "</optgroup>"
    #// Do manual UTC offsets.
    structure[-1] = "<optgroup label=\"" + esc_attr__("Manual Offsets") + "\">"
    offset_range = Array(-12, -11.5, -11, -10.5, -10, -9.5, -9, -8.5, -8, -7.5, -7, -6.5, -6, -5.5, -5, -4.5, -4, -3.5, -3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 5.75, 6, 6.5, 7, 7.5, 8, 8.5, 8.75, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.75, 13, 13.75, 14)
    for offset in offset_range:
        if 0 <= offset:
            offset_name = "+" + offset
        else:
            offset_name = php_str(offset)
        # end if
        offset_value = offset_name
        offset_name = php_str_replace(Array(".25", ".5", ".75"), Array(":15", ":30", ":45"), offset_name)
        offset_name = "UTC" + offset_name
        offset_value = "UTC" + offset_value
        selected = ""
        if offset_value == selected_zone:
            selected = "selected=\"selected\" "
        # end if
        structure[-1] = "<option " + selected + "value=\"" + esc_attr(offset_value) + "\">" + esc_html(offset_name) + "</option>"
    # end for
    structure[-1] = "</optgroup>"
    return join("\n", structure)
# end def wp_timezone_choice
#// 
#// Strip close comment and close php tags from file headers used by WP.
#// 
#// @since 2.8.0
#// @access private
#// 
#// @see https://core.trac.wordpress.org/ticket/8497
#// 
#// @param string $str Header comment to clean up.
#// @return string
#//
def _cleanup_header_comment(str=None, *args_):
    
    return php_trim(php_preg_replace("/\\s*(?:\\*\\/|\\?>).*/", "", str))
# end def _cleanup_header_comment
#// 
#// Permanently delete comments or posts of any type that have held a status
#// of 'trash' for the number of days defined in EMPTY_TRASH_DAYS.
#// 
#// The default value of `EMPTY_TRASH_DAYS` is 30 (days).
#// 
#// @since 2.9.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#//
def wp_scheduled_delete(*args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    delete_timestamp = time() - DAY_IN_SECONDS * EMPTY_TRASH_DAYS
    posts_to_delete = wpdb.get_results(wpdb.prepare(str("SELECT post_id FROM ") + str(wpdb.postmeta) + str(" WHERE meta_key = '_wp_trash_meta_time' AND meta_value < %d"), delete_timestamp), ARRAY_A)
    for post in posts_to_delete:
        post_id = php_int(post["post_id"])
        if (not post_id):
            continue
        # end if
        del_post = get_post(post_id)
        if (not del_post) or "trash" != del_post.post_status:
            delete_post_meta(post_id, "_wp_trash_meta_status")
            delete_post_meta(post_id, "_wp_trash_meta_time")
        else:
            wp_delete_post(post_id)
        # end if
    # end for
    comments_to_delete = wpdb.get_results(wpdb.prepare(str("SELECT comment_id FROM ") + str(wpdb.commentmeta) + str(" WHERE meta_key = '_wp_trash_meta_time' AND meta_value < %d"), delete_timestamp), ARRAY_A)
    for comment in comments_to_delete:
        comment_id = php_int(comment["comment_id"])
        if (not comment_id):
            continue
        # end if
        del_comment = get_comment(comment_id)
        if (not del_comment) or "trash" != del_comment.comment_approved:
            delete_comment_meta(comment_id, "_wp_trash_meta_time")
            delete_comment_meta(comment_id, "_wp_trash_meta_status")
        else:
            wp_delete_comment(del_comment)
        # end if
    # end for
# end def wp_scheduled_delete
#// 
#// Retrieve metadata from a file.
#// 
#// Searches for metadata in the first 8 KB of a file, such as a plugin or theme.
#// Each piece of metadata must be on its own line. Fields can not span multiple
#// lines, the value will get cut at the end of the first line.
#// 
#// If the file data is not within that first 8 KB, then the author should correct
#// their plugin file and move the data headers to the top.
#// 
#// @link https://codex.wordpress.org/File_Header
#// 
#// @since 2.9.0
#// 
#// @param string $file            Absolute path to the file.
#// @param array  $default_headers List of headers, in the format `array( 'HeaderKey' => 'Header Name' )`.
#// @param string $context         Optional. If specified adds filter hook {@see 'extra_$context_headers'}.
#// Default empty.
#// @return string[] Array of file header values keyed by header name.
#//
def get_file_data(file=None, default_headers=None, context="", *args_):
    
    #// We don't need to write to the file, so just open for reading.
    fp = fopen(file, "r")
    #// Pull only the first 8 KB of the file in.
    file_data = fread(fp, 8 * KB_IN_BYTES)
    #// PHP will close file handle, but we are good citizens.
    php_fclose(fp)
    #// Make sure we catch CR-only line endings.
    file_data = php_str_replace("\r", "\n", file_data)
    #// 
    #// Filters extra file headers by context.
    #// 
    #// The dynamic portion of the hook name, `$context`, refers to
    #// the context where extra headers might be loaded.
    #// 
    #// @since 2.9.0
    #// 
    #// @param array $extra_context_headers Empty array by default.
    #//
    extra_headers = apply_filters(str("extra_") + str(context) + str("_headers"), Array()) if context else Array()
    if extra_headers:
        extra_headers = php_array_combine(extra_headers, extra_headers)
        #// Keys equal values.
        all_headers = php_array_merge(extra_headers, default_headers)
    else:
        all_headers = default_headers
    # end if
    for field,regex in all_headers:
        if php_preg_match("/^[ \\t\\/*#@]*" + preg_quote(regex, "/") + ":(.*)$/mi", file_data, match) and match[1]:
            all_headers[field] = _cleanup_header_comment(match[1])
        else:
            all_headers[field] = ""
        # end if
    # end for
    return all_headers
# end def get_file_data
#// 
#// Returns true.
#// 
#// Useful for returning true to filters easily.
#// 
#// @since 3.0.0
#// 
#// @see __return_false()
#// 
#// @return true True.
#//
def __return_true(*args_):
    
    #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.FunctionDoubleUnderscore,PHPCompatibility.FunctionNameRestrictions.ReservedFunctionNames.FunctionDoubleUnderscore
    return True
# end def __return_true
#// 
#// Returns false.
#// 
#// Useful for returning false to filters easily.
#// 
#// @since 3.0.0
#// 
#// @see __return_true()
#// 
#// @return false False.
#//
def __return_false(*args_):
    
    #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.FunctionDoubleUnderscore,PHPCompatibility.FunctionNameRestrictions.ReservedFunctionNames.FunctionDoubleUnderscore
    return False
# end def __return_false
#// 
#// Returns 0.
#// 
#// Useful for returning 0 to filters easily.
#// 
#// @since 3.0.0
#// 
#// @return int 0.
#//
def __return_zero(*args_):
    
    #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.FunctionDoubleUnderscore,PHPCompatibility.FunctionNameRestrictions.ReservedFunctionNames.FunctionDoubleUnderscore
    return 0
# end def __return_zero
#// 
#// Returns an empty array.
#// 
#// Useful for returning an empty array to filters easily.
#// 
#// @since 3.0.0
#// 
#// @return array Empty array.
#//
def __return_empty_array(*args_):
    
    #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.FunctionDoubleUnderscore,PHPCompatibility.FunctionNameRestrictions.ReservedFunctionNames.FunctionDoubleUnderscore
    return Array()
# end def __return_empty_array
#// 
#// Returns null.
#// 
#// Useful for returning null to filters easily.
#// 
#// @since 3.4.0
#// 
#// @return null Null value.
#//
def __return_null(*args_):
    
    #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.FunctionDoubleUnderscore,PHPCompatibility.FunctionNameRestrictions.ReservedFunctionNames.FunctionDoubleUnderscore
    return None
# end def __return_null
#// 
#// Returns an empty string.
#// 
#// Useful for returning an empty string to filters easily.
#// 
#// @since 3.7.0
#// 
#// @see __return_null()
#// 
#// @return string Empty string.
#//
def __return_empty_string(*args_):
    
    #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.FunctionDoubleUnderscore,PHPCompatibility.FunctionNameRestrictions.ReservedFunctionNames.FunctionDoubleUnderscore
    return ""
# end def __return_empty_string
#// 
#// Send a HTTP header to disable content type sniffing in browsers which support it.
#// 
#// @since 3.0.0
#// 
#// @see https://blogs.msdn.com/ie/archive/2008/07/02/ie8-security-part-v-comprehensive-protection.aspx
#// @see https://src.chromium.org/viewvc/chrome?view=rev&revision=6985
#//
def send_nosniff_header(*args_):
    
    php_header("X-Content-Type-Options: nosniff")
# end def send_nosniff_header
#// 
#// Return a MySQL expression for selecting the week number based on the start_of_week option.
#// 
#// @ignore
#// @since 3.0.0
#// 
#// @param string $column Database column.
#// @return string SQL clause.
#//
def _wp_mysql_week(column=None, *args_):
    
    start_of_week = php_int(get_option("start_of_week"))
    for case in Switch(start_of_week):
        if case(1):
            return str("WEEK( ") + str(column) + str(", 1 )")
        # end if
        if case(2):
            pass
        # end if
        if case(3):
            pass
        # end if
        if case(4):
            pass
        # end if
        if case(5):
            pass
        # end if
        if case(6):
            return str("WEEK( DATE_SUB( ") + str(column) + str(", INTERVAL ") + str(start_of_week) + str(" DAY ), 0 )")
        # end if
        if case(0):
            pass
        # end if
        if case():
            return str("WEEK( ") + str(column) + str(", 0 )")
        # end if
    # end for
# end def _wp_mysql_week
#// 
#// Find hierarchy loops using a callback function that maps object IDs to parent IDs.
#// 
#// @since 3.1.0
#// @access private
#// 
#// @param callable $callback      Function that accepts ( ID, $callback_args ) and outputs parent_ID.
#// @param int      $start         The ID to start the loop check at.
#// @param int      $start_parent  The parent_ID of $start to use instead of calling $callback( $start ).
#// Use null to always use $callback
#// @param array    $callback_args Optional. Additional arguments to send to $callback.
#// @return array IDs of all members of loop.
#//
def wp_find_hierarchy_loop(callback=None, start=None, start_parent=None, callback_args=Array(), *args_):
    
    override = Array() if is_null(start_parent) else Array({start: start_parent})
    arbitrary_loop_member = wp_find_hierarchy_loop_tortoise_hare(callback, start, override, callback_args)
    if (not arbitrary_loop_member):
        return Array()
    # end if
    return wp_find_hierarchy_loop_tortoise_hare(callback, arbitrary_loop_member, override, callback_args, True)
# end def wp_find_hierarchy_loop
#// 
#// Use the "The Tortoise and the Hare" algorithm to detect loops.
#// 
#// For every step of the algorithm, the hare takes two steps and the tortoise one.
#// If the hare ever laps the tortoise, there must be a loop.
#// 
#// @since 3.1.0
#// @access private
#// 
#// @param callable $callback      Function that accepts ( ID, callback_arg, ... ) and outputs parent_ID.
#// @param int      $start         The ID to start the loop check at.
#// @param array    $override      Optional. An array of ( ID => parent_ID, ... ) to use instead of $callback.
#// Default empty array.
#// @param array    $callback_args Optional. Additional arguments to send to $callback. Default empty array.
#// @param bool     $_return_loop  Optional. Return loop members or just detect presence of loop? Only set
#// to true if you already know the given $start is part of a loop (otherwise
#// the returned array might include branches). Default false.
#// @return mixed Scalar ID of some arbitrary member of the loop, or array of IDs of all members of loop if
#// $_return_loop
#//
def wp_find_hierarchy_loop_tortoise_hare(callback=None, start=None, override=Array(), callback_args=Array(), _return_loop=False, *args_):
    
    tortoise = start
    hare = start
    evanescent_hare = start
    return_ = Array()
    #// Set evanescent_hare to one past hare.
    #// Increment hare two steps.
    while True:
        evanescent_hare = override[hare] if (php_isset(lambda : override[hare])) else call_user_func_array(callback, php_array_merge(Array(hare), callback_args))
        hare = override[evanescent_hare] if (php_isset(lambda : override[evanescent_hare])) else call_user_func_array(callback, php_array_merge(Array(evanescent_hare), callback_args))
        if not (tortoise and evanescent_hare and hare):
            break
        # end if
        if _return_loop:
            return_[tortoise] = True
            return_[evanescent_hare] = True
            return_[hare] = True
        # end if
        #// Tortoise got lapped - must be a loop.
        if tortoise == evanescent_hare or tortoise == hare:
            return return_ if _return_loop else tortoise
        # end if
        #// Increment tortoise by one step.
        tortoise = override[tortoise] if (php_isset(lambda : override[tortoise])) else call_user_func_array(callback, php_array_merge(Array(tortoise), callback_args))
    # end while
    return False
# end def wp_find_hierarchy_loop_tortoise_hare
#// 
#// Send a HTTP header to limit rendering of pages to same origin iframes.
#// 
#// @since 3.1.3
#// 
#// @see https://developer.mozilla.org/en/the_x-frame-options_response_header
#//
def send_frame_options_header(*args_):
    
    php_header("X-Frame-Options: SAMEORIGIN")
# end def send_frame_options_header
#// 
#// Retrieve a list of protocols to allow in HTML attributes.
#// 
#// @since 3.3.0
#// @since 4.3.0 Added 'webcal' to the protocols array.
#// @since 4.7.0 Added 'urn' to the protocols array.
#// @since 5.3.0 Added 'sms' to the protocols array.
#// 
#// @see wp_kses()
#// @see esc_url()
#// 
#// @staticvar array $protocols
#// 
#// @return string[] Array of allowed protocols. Defaults to an array containing 'http', 'https',
#// 'ftp', 'ftps', 'mailto', 'news', 'irc', 'gopher', 'nntp', 'feed', 'telnet',
#// 'mms', 'rtsp', 'sms', 'svn', 'tel', 'fax', 'xmpp', 'webcal', and 'urn'.
#// This covers all common link protocols, except for 'javascript' which should not
#// be allowed for untrusted users.
#//
def wp_allowed_protocols(*args_):
    
    protocols = Array()
    if php_empty(lambda : protocols):
        protocols = Array("http", "https", "ftp", "ftps", "mailto", "news", "irc", "gopher", "nntp", "feed", "telnet", "mms", "rtsp", "sms", "svn", "tel", "fax", "xmpp", "webcal", "urn")
    # end if
    if (not did_action("wp_loaded")):
        #// 
        #// Filters the list of protocols allowed in HTML attributes.
        #// 
        #// @since 3.0.0
        #// 
        #// @param string[] $protocols Array of allowed protocols e.g. 'http', 'ftp', 'tel', and more.
        #//
        protocols = array_unique(apply_filters("kses_allowed_protocols", protocols))
    # end if
    return protocols
# end def wp_allowed_protocols
#// 
#// Return a comma-separated string of functions that have been called to get
#// to the current point in code.
#// 
#// @since 3.4.0
#// 
#// @see https://core.trac.wordpress.org/ticket/19589
#// 
#// @staticvar array $truncate_paths Array of paths to truncate.
#// 
#// @param string $ignore_class Optional. A class to ignore all function calls within - useful
#// when you want to just give info about the callee. Default null.
#// @param int    $skip_frames  Optional. A number of stack frames to skip - useful for unwinding
#// back to the source of the issue. Default 0.
#// @param bool   $pretty       Optional. Whether or not you want a comma separated string or raw
#// array returned. Default true.
#// @return string|array Either a string containing a reversed comma separated trace or an array
#// of individual calls.
#//
def wp_debug_backtrace_summary(ignore_class=None, skip_frames=0, pretty=True, *args_):
    
    truncate_paths = None
    trace = debug_backtrace(False)
    caller = Array()
    check_class = (not is_null(ignore_class))
    skip_frames += 1
    #// Skip this function.
    if (not (php_isset(lambda : truncate_paths))):
        truncate_paths = Array(wp_normalize_path(WP_CONTENT_DIR), wp_normalize_path(ABSPATH))
    # end if
    for call in trace:
        if skip_frames > 0:
            skip_frames -= 1
        elif (php_isset(lambda : call["class"])):
            if check_class and ignore_class == call["class"]:
                continue
                pass
            # end if
            caller[-1] = str(call["class"]) + str(call["type"]) + str(call["function"])
        else:
            if php_in_array(call["function"], Array("do_action", "apply_filters", "do_action_ref_array", "apply_filters_ref_array")):
                caller[-1] = str(call["function"]) + str("('") + str(call["args"][0]) + str("')")
            elif php_in_array(call["function"], Array("include", "include_once", "require", "require_once")):
                filename = call["args"][0] if (php_isset(lambda : call["args"][0])) else ""
                caller[-1] = call["function"] + "('" + php_str_replace(truncate_paths, "", wp_normalize_path(filename)) + "')"
            else:
                caller[-1] = call["function"]
            # end if
        # end if
    # end for
    if pretty:
        return join(", ", array_reverse(caller))
    else:
        return caller
    # end if
# end def wp_debug_backtrace_summary
#// 
#// Retrieve IDs that are not already present in the cache.
#// 
#// @since 3.4.0
#// @access private
#// 
#// @param int[]  $object_ids Array of IDs.
#// @param string $cache_key  The cache bucket to check against.
#// @return int[] Array of IDs not present in the cache.
#//
def _get_non_cached_ids(object_ids=None, cache_key=None, *args_):
    
    clean = Array()
    for id in object_ids:
        id = php_int(id)
        if (not wp_cache_get(id, cache_key)):
            clean[-1] = id
        # end if
    # end for
    return clean
# end def _get_non_cached_ids
#// 
#// Test if the current device has the capability to upload files.
#// 
#// @since 3.4.0
#// @access private
#// 
#// @return bool Whether the device is able to upload files.
#//
def _device_can_upload(*args_):
    
    if (not wp_is_mobile()):
        return True
    # end if
    ua = PHP_SERVER["HTTP_USER_AGENT"]
    if php_strpos(ua, "iPhone") != False or php_strpos(ua, "iPad") != False or php_strpos(ua, "iPod") != False:
        return php_preg_match("#OS ([\\d_]+) like Mac OS X#", ua, version) and php_version_compare(version[1], "6", ">=")
    # end if
    return True
# end def _device_can_upload
#// 
#// Test if a given path is a stream URL
#// 
#// @since 3.5.0
#// 
#// @param string $path The resource path or URL.
#// @return bool True if the path is a stream URL.
#//
def wp_is_stream(path=None, *args_):
    
    scheme_separator = php_strpos(path, "://")
    if False == scheme_separator:
        #// $path isn't a stream.
        return False
    # end if
    stream = php_substr(path, 0, scheme_separator)
    return php_in_array(stream, stream_get_wrappers(), True)
# end def wp_is_stream
#// 
#// Test if the supplied date is valid for the Gregorian calendar.
#// 
#// @since 3.5.0
#// 
#// @link https://www.php.net/manual/en/function.checkdate.php
#// 
#// @param  int    $month       Month number.
#// @param  int    $day         Day number.
#// @param  int    $year        Year number.
#// @param  string $source_date The date to filter.
#// @return bool True if valid date, false if not valid date.
#//
def wp_checkdate(month=None, day=None, year=None, source_date=None, *args_):
    
    #// 
    #// Filters whether the given date is valid for the Gregorian calendar.
    #// 
    #// @since 3.5.0
    #// 
    #// @param bool   $checkdate   Whether the given date is valid.
    #// @param string $source_date Date to check.
    #//
    return apply_filters("wp_checkdate", checkdate(month, day, year), source_date)
# end def wp_checkdate
#// 
#// Load the auth check for monitoring whether the user is still logged in.
#// 
#// Can be disabled with remove_action( 'admin_enqueue_scripts', 'wp_auth_check_load' );
#// 
#// This is disabled for certain screens where a login screen could cause an
#// inconvenient interruption. A filter called {@see 'wp_auth_check_load'} can be used
#// for fine-grained control.
#// 
#// @since 3.6.0
#//
def wp_auth_check_load(*args_):
    
    if (not is_admin()) and (not is_user_logged_in()):
        return
    # end if
    if php_defined("IFRAME_REQUEST"):
        return
    # end if
    screen = get_current_screen()
    hidden = Array("update", "update-network", "update-core", "update-core-network", "upgrade", "upgrade-network", "network")
    show = (not php_in_array(screen.id, hidden))
    #// 
    #// Filters whether to load the authentication check.
    #// 
    #// Passing a falsey value to the filter will effectively short-circuit
    #// loading the authentication check.
    #// 
    #// @since 3.6.0
    #// 
    #// @param bool      $show   Whether to load the authentication check.
    #// @param WP_Screen $screen The current screen object.
    #//
    if apply_filters("wp_auth_check_load", show, screen):
        wp_enqueue_style("wp-auth-check")
        wp_enqueue_script("wp-auth-check")
        add_action("admin_print_footer_scripts", "wp_auth_check_html", 5)
        add_action("wp_print_footer_scripts", "wp_auth_check_html", 5)
    # end if
# end def wp_auth_check_load
#// 
#// Output the HTML that shows the wp-login dialog when the user is no longer logged in.
#// 
#// @since 3.6.0
#//
def wp_auth_check_html(*args_):
    
    login_url = wp_login_url()
    current_domain = "https://" if is_ssl() else "http://" + PHP_SERVER["HTTP_HOST"]
    same_domain = php_strpos(login_url, current_domain) == 0
    #// 
    #// Filters whether the authentication check originated at the same domain.
    #// 
    #// @since 3.6.0
    #// 
    #// @param bool $same_domain Whether the authentication check originated at the same domain.
    #//
    same_domain = apply_filters("wp_auth_check_same_domain", same_domain)
    wrap_class = "hidden" if same_domain else "hidden fallback"
    php_print(" <div id=\"wp-auth-check-wrap\" class=\"")
    php_print(wrap_class)
    php_print("""\">
    <div id=\"wp-auth-check-bg\"></div>
    <div id=\"wp-auth-check\">
    <button type=\"button\" class=\"wp-auth-check-close button-link\"><span class=\"screen-reader-text\">""")
    _e("Close dialog")
    php_print("</span></button>\n   ")
    if same_domain:
        login_src = add_query_arg(Array({"interim-login": "1", "wp_lang": get_user_locale()}), login_url)
        php_print("     <div id=\"wp-auth-check-form\" class=\"loading\" data-src=\"")
        php_print(esc_url(login_src))
        php_print("\"></div>\n      ")
    # end if
    php_print(" <div class=\"wp-auth-fallback\">\n      <p><b class=\"wp-auth-fallback-expired\" tabindex=\"0\">")
    _e("Session expired")
    php_print("</b></p>\n       <p><a href=\"")
    php_print(esc_url(login_url))
    php_print("\" target=\"_blank\">")
    _e("Please log in again.")
    php_print("</a>\n       ")
    _e("The login page will open in a new tab. After logging in you can close it and return to this page.")
    php_print("""</p>
    </div>
    </div>
    </div>
    """)
# end def wp_auth_check_html
#// 
#// Check whether a user is still logged in, for the heartbeat.
#// 
#// Send a result that shows a log-in box if the user is no longer logged in,
#// or if their cookie is within the grace period.
#// 
#// @since 3.6.0
#// 
#// @global int $login_grace_period
#// 
#// @param array $response  The Heartbeat response.
#// @return array The Heartbeat response with 'wp-auth-check' value set.
#//
def wp_auth_check(response=None, *args_):
    
    response["wp-auth-check"] = is_user_logged_in() and php_empty(lambda : PHP_GLOBALS["login_grace_period"])
    return response
# end def wp_auth_check
#// 
#// Return RegEx body to liberally match an opening HTML tag.
#// 
#// Matches an opening HTML tag that:
#// 1. Is self-closing or
#// 2. Has no body but has a closing tag of the same name or
#// 3. Contains a body and a closing tag of the same name
#// 
#// Note: this RegEx does not balance inner tags and does not attempt
#// to produce valid HTML
#// 
#// @since 3.6.0
#// 
#// @param string $tag An HTML tag name. Example: 'video'.
#// @return string Tag RegEx.
#//
def get_tag_regex(tag=None, *args_):
    
    if php_empty(lambda : tag):
        return
    # end if
    return php_sprintf("<%1$s[^<]*(?:>[\\s\\S]*<\\/%1$s>|\\s*\\/>)", tag_escape(tag))
# end def get_tag_regex
#// 
#// Retrieve a canonical form of the provided charset appropriate for passing to PHP
#// functions such as htmlspecialchars() and charset html attributes.
#// 
#// @since 3.6.0
#// @access private
#// 
#// @see https://core.trac.wordpress.org/ticket/23688
#// 
#// @param string $charset A charset name.
#// @return string The canonical form of the charset.
#//
def _canonical_charset(charset=None, *args_):
    
    if "utf-8" == php_strtolower(charset) or "utf8" == php_strtolower(charset):
        return "UTF-8"
    # end if
    if "iso-8859-1" == php_strtolower(charset) or "iso8859-1" == php_strtolower(charset):
        return "ISO-8859-1"
    # end if
    return charset
# end def _canonical_charset
#// 
#// Set the mbstring internal encoding to a binary safe encoding when func_overload
#// is enabled.
#// 
#// When mbstring.func_overload is in use for multi-byte encodings, the results from
#// strlen() and similar functions respect the utf8 characters, causing binary data
#// to return incorrect lengths.
#// 
#// This function overrides the mbstring encoding to a binary-safe encoding, and
#// resets it to the users expected encoding afterwards through the
#// `reset_mbstring_encoding` function.
#// 
#// It is safe to recursively call this function, however each
#// `mbstring_binary_safe_encoding()` call must be followed up with an equal number
#// of `reset_mbstring_encoding()` calls.
#// 
#// @since 3.7.0
#// 
#// @see reset_mbstring_encoding()
#// 
#// @staticvar array $encodings
#// @staticvar bool  $overloaded
#// 
#// @param bool $reset Optional. Whether to reset the encoding back to a previously-set encoding.
#// Default false.
#//
def mbstring_binary_safe_encoding(reset=False, *args_):
    
    encodings = Array()
    overloaded = None
    if is_null(overloaded):
        overloaded = php_function_exists("mb_internal_encoding") and php_ini_get("mbstring.func_overload") & 2
    # end if
    if False == overloaded:
        return
    # end if
    if (not reset):
        encoding = mb_internal_encoding()
        php_array_push(encodings, encoding)
        mb_internal_encoding("ISO-8859-1")
    # end if
    if reset and encodings:
        encoding = php_array_pop(encodings)
        mb_internal_encoding(encoding)
    # end if
# end def mbstring_binary_safe_encoding
#// 
#// Reset the mbstring internal encoding to a users previously set encoding.
#// 
#// @see mbstring_binary_safe_encoding()
#// 
#// @since 3.7.0
#//
def reset_mbstring_encoding(*args_):
    
    mbstring_binary_safe_encoding(True)
# end def reset_mbstring_encoding
#// 
#// Filter/validate a variable as a boolean.
#// 
#// Alternative to `filter_var( $var, FILTER_VALIDATE_BOOLEAN )`.
#// 
#// @since 4.0.0
#// 
#// @param mixed $var Boolean value to validate.
#// @return bool Whether the value is validated.
#//
def wp_validate_boolean(var=None, *args_):
    
    if php_is_bool(var):
        return var
    # end if
    if php_is_string(var) and "false" == php_strtolower(var):
        return False
    # end if
    return php_bool(var)
# end def wp_validate_boolean
#// 
#// Delete a file
#// 
#// @since 4.2.0
#// 
#// @param string $file The path to the file to delete.
#//
def wp_delete_file(file=None, *args_):
    
    #// 
    #// Filters the path of the file to delete.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string $file Path to the file to delete.
    #//
    delete = apply_filters("wp_delete_file", file)
    if (not php_empty(lambda : delete)):
        php_no_error(lambda: unlink(delete))
    # end if
# end def wp_delete_file
#// 
#// Deletes a file if its path is within the given directory.
#// 
#// @since 4.9.7
#// 
#// @param string $file      Absolute path to the file to delete.
#// @param string $directory Absolute path to a directory.
#// @return bool True on success, false on failure.
#//
def wp_delete_file_from_directory(file=None, directory=None, *args_):
    
    if wp_is_stream(file):
        real_file = file
        real_directory = directory
    else:
        real_file = php_realpath(wp_normalize_path(file))
        real_directory = php_realpath(wp_normalize_path(directory))
    # end if
    if False != real_file:
        real_file = wp_normalize_path(real_file)
    # end if
    if False != real_directory:
        real_directory = wp_normalize_path(real_directory)
    # end if
    if False == real_file or False == real_directory or php_strpos(real_file, trailingslashit(real_directory)) != 0:
        return False
    # end if
    wp_delete_file(file)
    return True
# end def wp_delete_file_from_directory
#// 
#// Outputs a small JS snippet on preview tabs/windows to remove `window.name` on unload.
#// 
#// This prevents reusing the same tab for a preview when the user has navigated away.
#// 
#// @since 4.3.0
#// 
#// @global WP_Post $post Global post object.
#//
def wp_post_preview_js(*args_):
    
    global post
    php_check_if_defined("post")
    if (not is_preview()) or php_empty(lambda : post):
        return
    # end if
    #// Has to match the window name used in post_submit_meta_box().
    name = "wp-preview-" + php_int(post.ID)
    php_print("""   <script>
    ( function() {
    var query = document.location.search;
if ( query && query.indexOf( 'preview=true' ) !== -1 ) {
    window.name = '""")
    php_print(name)
    php_print("""';
    }
if ( window.addEventListener ) {
    window.addEventListener( 'unload', function() { window.name = ''; }, false );
    }
    }());
    </script>
    """)
# end def wp_post_preview_js
#// 
#// Parses and formats a MySQL datetime (Y-m-d H:i:s) for ISO8601 (Y-m-d\TH:i:s).
#// 
#// Explicitly strips timezones, as datetimes are not saved with any timezone
#// information. Including any information on the offset could be misleading.
#// 
#// Despite historical function name, the output does not conform to RFC3339 format,
#// which must contain timezone.
#// 
#// @since 4.4.0
#// 
#// @param string $date_string Date string to parse and format.
#// @return string Date formatted for ISO8601 without time zone.
#//
def mysql_to_rfc3339(date_string=None, *args_):
    
    return mysql2date("Y-m-d\\TH:i:s", date_string, False)
# end def mysql_to_rfc3339
#// 
#// Attempts to raise the PHP memory limit for memory intensive processes.
#// 
#// Only allows raising the existing limit and prevents lowering it.
#// 
#// @since 4.6.0
#// 
#// @param string $context Optional. Context in which the function is called. Accepts either 'admin',
#// 'image', or an arbitrary other context. If an arbitrary context is passed,
#// the similarly arbitrary {@see '{$context}_memory_limit'} filter will be
#// invoked. Default 'admin'.
#// @return bool|int|string The limit that was set or false on failure.
#//
def wp_raise_memory_limit(context="admin", *args_):
    
    #// Exit early if the limit cannot be changed.
    if False == wp_is_ini_value_changeable("memory_limit"):
        return False
    # end if
    current_limit = php_ini_get("memory_limit")
    current_limit_int = wp_convert_hr_to_bytes(current_limit)
    if -1 == current_limit_int:
        return False
    # end if
    wp_max_limit = WP_MAX_MEMORY_LIMIT
    wp_max_limit_int = wp_convert_hr_to_bytes(wp_max_limit)
    filtered_limit = wp_max_limit
    for case in Switch(context):
        if case("admin"):
            #// 
            #// Filters the maximum memory limit available for administration screens.
            #// 
            #// This only applies to administrators, who may require more memory for tasks
            #// like updates. Memory limits when processing images (uploaded or edited by
            #// users of any role) are handled separately.
            #// 
            #// The `WP_MAX_MEMORY_LIMIT` constant specifically defines the maximum memory
            #// limit available when in the administration back end. The default is 256M
            #// (256 megabytes of memory) or the original `memory_limit` php.ini value if
            #// this is higher.
            #// 
            #// @since 3.0.0
            #// @since 4.6.0 The default now takes the original `memory_limit` into account.
            #// 
            #// @param int|string $filtered_limit The maximum WordPress memory limit. Accepts an integer
            #// (bytes), or a shorthand string notation, such as '256M'.
            #//
            filtered_limit = apply_filters("admin_memory_limit", filtered_limit)
            break
        # end if
        if case("image"):
            #// 
            #// Filters the memory limit allocated for image manipulation.
            #// 
            #// @since 3.5.0
            #// @since 4.6.0 The default now takes the original `memory_limit` into account.
            #// 
            #// @param int|string $filtered_limit Maximum memory limit to allocate for images.
            #// Default `WP_MAX_MEMORY_LIMIT` or the original
            #// php.ini `memory_limit`, whichever is higher.
            #// Accepts an integer (bytes), or a shorthand string
            #// notation, such as '256M'.
            #//
            filtered_limit = apply_filters("image_memory_limit", filtered_limit)
            break
        # end if
        if case():
            #// 
            #// Filters the memory limit allocated for arbitrary contexts.
            #// 
            #// The dynamic portion of the hook name, `$context`, refers to an arbitrary
            #// context passed on calling the function. This allows for plugins to define
            #// their own contexts for raising the memory limit.
            #// 
            #// @since 4.6.0
            #// 
            #// @param int|string $filtered_limit Maximum memory limit to allocate for images.
            #// Default '256M' or the original php.ini `memory_limit`,
            #// whichever is higher. Accepts an integer (bytes), or a
            #// shorthand string notation, such as '256M'.
            #//
            filtered_limit = apply_filters(str(context) + str("_memory_limit"), filtered_limit)
            break
        # end if
    # end for
    filtered_limit_int = wp_convert_hr_to_bytes(filtered_limit)
    if -1 == filtered_limit_int or filtered_limit_int > wp_max_limit_int and filtered_limit_int > current_limit_int:
        if False != php_ini_set("memory_limit", filtered_limit):
            return filtered_limit
        else:
            return False
        # end if
    elif -1 == wp_max_limit_int or wp_max_limit_int > current_limit_int:
        if False != php_ini_set("memory_limit", wp_max_limit):
            return wp_max_limit
        else:
            return False
        # end if
    # end if
    return False
# end def wp_raise_memory_limit
#// 
#// Generate a random UUID (version 4).
#// 
#// @since 4.7.0
#// 
#// @return string UUID.
#//
def wp_generate_uuid4(*args_):
    
    return php_sprintf("%04x%04x-%04x-%04x-%04x-%04x%04x%04x", mt_rand(0, 65535), mt_rand(0, 65535), mt_rand(0, 65535), mt_rand(0, 4095) | 16384, mt_rand(0, 16383) | 32768, mt_rand(0, 65535), mt_rand(0, 65535), mt_rand(0, 65535))
# end def wp_generate_uuid4
#// 
#// Validates that a UUID is valid.
#// 
#// @since 4.9.0
#// 
#// @param mixed $uuid    UUID to check.
#// @param int   $version Specify which version of UUID to check against. Default is none,
#// to accept any UUID version. Otherwise, only version allowed is `4`.
#// @return bool The string is a valid UUID or false on failure.
#//
def wp_is_uuid(uuid=None, version=None, *args_):
    
    if (not php_is_string(uuid)):
        return False
    # end if
    if php_is_numeric(version):
        if 4 != php_int(version):
            _doing_it_wrong(__FUNCTION__, __("Only UUID V4 is supported at this time."), "4.9.0")
            return False
        # end if
        regex = "/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/"
    else:
        regex = "/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/"
    # end if
    return php_bool(php_preg_match(regex, uuid))
# end def wp_is_uuid
#// 
#// Get unique ID.
#// 
#// This is a PHP implementation of Underscore's uniqueId method. A static variable
#// contains an integer that is incremented with each call. This number is returned
#// with the optional prefix. As such the returned value is not universally unique,
#// but it is unique across the life of the PHP process.
#// 
#// @since 5.0.3
#// 
#// @staticvar int $id_counter
#// 
#// @param string $prefix Prefix for the returned ID.
#// @return string Unique ID.
#//
def wp_unique_id(prefix="", *args_):
    
    id_counter = 0
    id_counter += 1
    return prefix + php_str(id_counter)
# end def wp_unique_id
#// 
#// Get last changed date for the specified cache group.
#// 
#// @since 4.7.0
#// 
#// @param string $group Where the cache contents are grouped.
#// 
#// @return string $last_changed UNIX timestamp with microseconds representing when the group was last changed.
#//
def wp_cache_get_last_changed(group=None, *args_):
    
    last_changed = wp_cache_get("last_changed", group)
    if (not last_changed):
        last_changed = php_microtime()
        wp_cache_set("last_changed", last_changed, group)
    # end if
    return last_changed
# end def wp_cache_get_last_changed
#// 
#// Send an email to the old site admin email address when the site admin email address changes.
#// 
#// @since 4.9.0
#// 
#// @param string $old_email   The old site admin email address.
#// @param string $new_email   The new site admin email address.
#// @param string $option_name The relevant database option name.
#//
def wp_site_admin_email_change_notification(old_email=None, new_email=None, option_name=None, *args_):
    
    send = True
    #// Don't send the notification to the default 'admin_email' value.
    if "you@example.com" == old_email:
        send = False
    # end if
    #// 
    #// Filters whether to send the site admin email change notification email.
    #// 
    #// @since 4.9.0
    #// 
    #// @param bool   $send      Whether to send the email notification.
    #// @param string $old_email The old site admin email address.
    #// @param string $new_email The new site admin email address.
    #//
    send = apply_filters("send_site_admin_email_change_email", send, old_email, new_email)
    if (not send):
        return
    # end if
    #// translators: Do not translate OLD_EMAIL, NEW_EMAIL, SITENAME, SITEURL: those are placeholders.
    email_change_text = __("""Hi,
    This notice confirms that the admin email address was changed on ###SITENAME###.
    The new admin email address is ###NEW_EMAIL###.
    This email has been sent to ###OLD_EMAIL###
    Regards,
    All at ###SITENAME###
    ###SITEURL###""")
    email_change_email = Array({"to": old_email, "subject": __("[%s] Admin Email Changed"), "message": email_change_text, "headers": ""})
    #// Get site name.
    site_name = wp_specialchars_decode(get_option("blogname"), ENT_QUOTES)
    #// 
    #// Filters the contents of the email notification sent when the site admin email address is changed.
    #// 
    #// @since 4.9.0
    #// 
    #// @param array $email_change_email {
    #// Used to build wp_mail().
    #// 
    #// @type string $to      The intended recipient.
    #// @type string $subject The subject of the email.
    #// @type string $message The content of the email.
    #// The following strings have a special meaning and will get replaced dynamically:
    #// - ###OLD_EMAIL### The old site admin email address.
    #// - ###NEW_EMAIL### The new site admin email address.
    #// - ###SITENAME###  The name of the site.
    #// - ###SITEURL###   The URL to the site.
    #// @type string $headers Headers.
    #// }
    #// @param string $old_email The old site admin email address.
    #// @param string $new_email The new site admin email address.
    #//
    email_change_email = apply_filters("site_admin_email_change_email", email_change_email, old_email, new_email)
    email_change_email["message"] = php_str_replace("###OLD_EMAIL###", old_email, email_change_email["message"])
    email_change_email["message"] = php_str_replace("###NEW_EMAIL###", new_email, email_change_email["message"])
    email_change_email["message"] = php_str_replace("###SITENAME###", site_name, email_change_email["message"])
    email_change_email["message"] = php_str_replace("###SITEURL###", home_url(), email_change_email["message"])
    wp_mail(email_change_email["to"], php_sprintf(email_change_email["subject"], site_name), email_change_email["message"], email_change_email["headers"])
# end def wp_site_admin_email_change_notification
#// 
#// Return an anonymized IPv4 or IPv6 address.
#// 
#// @since 4.9.6 Abstracted from `WP_Community_Events::get_unsafe_client_ip()`.
#// 
#// @param  string $ip_addr        The IPv4 or IPv6 address to be anonymized.
#// @param  bool   $ipv6_fallback  Optional. Whether to return the original IPv6 address if the needed functions
#// to anonymize it are not present. Default false, return `::` (unspecified address).
#// @return string  The anonymized IP address.
#//
def wp_privacy_anonymize_ip(ip_addr=None, ipv6_fallback=False, *args_):
    
    #// Detect what kind of IP address this is.
    ip_prefix = ""
    is_ipv6 = php_substr_count(ip_addr, ":") > 1
    is_ipv4 = 3 == php_substr_count(ip_addr, ".")
    if is_ipv6 and is_ipv4:
        #// IPv6 compatibility mode, temporarily strip the IPv6 part, and treat it like IPv4.
        ip_prefix = "::ffff:"
        ip_addr = php_preg_replace("/^\\[?[0-9a-f:]*:/i", "", ip_addr)
        ip_addr = php_str_replace("]", "", ip_addr)
        is_ipv6 = False
    # end if
    if is_ipv6:
        #// IPv6 addresses will always be enclosed in [] if there's a port.
        left_bracket = php_strpos(ip_addr, "[")
        right_bracket = php_strpos(ip_addr, "]")
        percent = php_strpos(ip_addr, "%")
        netmask = "ffff:ffff:ffff:ffff:0000:0000:0000:0000"
        #// Strip the port (and [] from IPv6 addresses), if they exist.
        if False != left_bracket and False != right_bracket:
            ip_addr = php_substr(ip_addr, left_bracket + 1, right_bracket - left_bracket - 1)
        elif False != left_bracket or False != right_bracket:
            #// The IP has one bracket, but not both, so it's malformed.
            return "::"
        # end if
        #// Strip the reachability scope.
        if False != percent:
            ip_addr = php_substr(ip_addr, 0, percent)
        # end if
        #// No invalid characters should be left.
        if php_preg_match("/[^0-9a-f:]/i", ip_addr):
            return "::"
        # end if
        #// Partially anonymize the IP by reducing it to the corresponding network ID.
        if php_function_exists("inet_pton") and php_function_exists("inet_ntop"):
            ip_addr = inet_ntop(inet_pton(ip_addr) & inet_pton(netmask))
            if False == ip_addr:
                return "::"
            # end if
        elif (not ipv6_fallback):
            return "::"
        # end if
    elif is_ipv4:
        #// Strip any port and partially anonymize the IP.
        last_octet_position = php_strrpos(ip_addr, ".")
        ip_addr = php_substr(ip_addr, 0, last_octet_position) + ".0"
    else:
        return "0.0.0.0"
    # end if
    #// Restore the IPv6 prefix to compatibility mode addresses.
    return ip_prefix + ip_addr
# end def wp_privacy_anonymize_ip
#// 
#// Return uniform "anonymous" data by type.
#// 
#// @since 4.9.6
#// 
#// @param  string $type The type of data to be anonymized.
#// @param  string $data Optional The data to be anonymized.
#// @return string The anonymous data for the requested type.
#//
def wp_privacy_anonymize_data(type=None, data="", *args_):
    
    for case in Switch(type):
        if case("email"):
            anonymous = "deleted@site.invalid"
            break
        # end if
        if case("url"):
            anonymous = "https://site.invalid"
            break
        # end if
        if case("ip"):
            anonymous = wp_privacy_anonymize_ip(data)
            break
        # end if
        if case("date"):
            anonymous = "0000-00-00 00:00:00"
            break
        # end if
        if case("text"):
            #// translators: Deleted text.
            anonymous = __("[deleted]")
            break
        # end if
        if case("longtext"):
            #// translators: Deleted long text.
            anonymous = __("This content was deleted by the author.")
            break
        # end if
        if case():
            anonymous = ""
            break
        # end if
    # end for
    #// 
    #// Filters the anonymous data for each type.
    #// 
    #// @since 4.9.6
    #// 
    #// @param string $anonymous Anonymized data.
    #// @param string $type      Type of the data.
    #// @param string $data      Original data.
    #//
    return apply_filters("wp_privacy_anonymize_data", anonymous, type, data)
# end def wp_privacy_anonymize_data
#// 
#// Returns the directory used to store personal data export files.
#// 
#// @since 4.9.6
#// 
#// @see wp_privacy_exports_url
#// 
#// @return string Exports directory.
#//
def wp_privacy_exports_dir(*args_):
    
    upload_dir = wp_upload_dir()
    exports_dir = trailingslashit(upload_dir["basedir"]) + "wp-personal-data-exports/"
    #// 
    #// Filters the directory used to store personal data export files.
    #// 
    #// @since 4.9.6
    #// 
    #// @param string $exports_dir Exports directory.
    #//
    return apply_filters("wp_privacy_exports_dir", exports_dir)
# end def wp_privacy_exports_dir
#// 
#// Returns the URL of the directory used to store personal data export files.
#// 
#// @since 4.9.6
#// 
#// @see wp_privacy_exports_dir
#// 
#// @return string Exports directory URL.
#//
def wp_privacy_exports_url(*args_):
    
    upload_dir = wp_upload_dir()
    exports_url = trailingslashit(upload_dir["baseurl"]) + "wp-personal-data-exports/"
    #// 
    #// Filters the URL of the directory used to store personal data export files.
    #// 
    #// @since 4.9.6
    #// 
    #// @param string $exports_url Exports directory URL.
    #//
    return apply_filters("wp_privacy_exports_url", exports_url)
# end def wp_privacy_exports_url
#// 
#// Schedule a `WP_Cron` job to delete expired export files.
#// 
#// @since 4.9.6
#//
def wp_schedule_delete_old_privacy_export_files(*args_):
    
    if wp_installing():
        return
    # end if
    if (not wp_next_scheduled("wp_privacy_delete_old_export_files")):
        wp_schedule_event(time(), "hourly", "wp_privacy_delete_old_export_files")
    # end if
# end def wp_schedule_delete_old_privacy_export_files
#// 
#// Cleans up export files older than three days old.
#// 
#// The export files are stored in `wp-content/uploads`, and are therefore publicly
#// accessible. A CSPRN is appended to the filename to mitigate the risk of an
#// unauthorized person downloading the file, but it is still possible. Deleting
#// the file after the data subject has had a chance to delete it adds an additional
#// layer of protection.
#// 
#// @since 4.9.6
#//
def wp_privacy_delete_old_export_files(*args_):
    
    exports_dir = wp_privacy_exports_dir()
    if (not php_is_dir(exports_dir)):
        return
    # end if
    php_include_file(ABSPATH + "wp-admin/includes/file.php", once=True)
    export_files = list_files(exports_dir, 100, Array("index.html"))
    #// 
    #// Filters the lifetime, in seconds, of a personal data export file.
    #// 
    #// By default, the lifetime is 3 days. Once the file reaches that age, it will automatically
    #// be deleted by a cron job.
    #// 
    #// @since 4.9.6
    #// 
    #// @param int $expiration The expiration age of the export, in seconds.
    #//
    expiration = apply_filters("wp_privacy_export_expiration", 3 * DAY_IN_SECONDS)
    for export_file in export_files:
        file_age_in_seconds = time() - filemtime(export_file)
        if expiration < file_age_in_seconds:
            unlink(export_file)
        # end if
    # end for
# end def wp_privacy_delete_old_export_files
#// 
#// Gets the URL to learn more about updating the PHP version the site is running on.
#// 
#// This URL can be overridden by specifying an environment variable `WP_UPDATE_PHP_URL` or by using the
#// {@see 'wp_update_php_url'} filter. Providing an empty string is not allowed and will result in the
#// default URL being used. Furthermore the page the URL links to should preferably be localized in the
#// site language.
#// 
#// @since 5.1.0
#// 
#// @return string URL to learn more about updating PHP.
#//
def wp_get_update_php_url(*args_):
    
    default_url = wp_get_default_update_php_url()
    update_url = default_url
    if False != php_getenv("WP_UPDATE_PHP_URL"):
        update_url = php_getenv("WP_UPDATE_PHP_URL")
    # end if
    #// 
    #// Filters the URL to learn more about updating the PHP version the site is running on.
    #// 
    #// Providing an empty string is not allowed and will result in the default URL being used. Furthermore
    #// the page the URL links to should preferably be localized in the site language.
    #// 
    #// @since 5.1.0
    #// 
    #// @param string $update_url URL to learn more about updating PHP.
    #//
    update_url = apply_filters("wp_update_php_url", update_url)
    if php_empty(lambda : update_url):
        update_url = default_url
    # end if
    return update_url
# end def wp_get_update_php_url
#// 
#// Gets the default URL to learn more about updating the PHP version the site is running on.
#// 
#// Do not use this function to retrieve this URL. Instead, use {@see wp_get_update_php_url()} when relying on the URL.
#// This function does not allow modifying the returned URL, and is only used to compare the actually used URL with the
#// default one.
#// 
#// @since 5.1.0
#// @access private
#// 
#// @return string Default URL to learn more about updating PHP.
#//
def wp_get_default_update_php_url(*args_):
    
    return _x("https://wordpress.org/support/update-php/", "localized PHP upgrade information page")
# end def wp_get_default_update_php_url
#// 
#// Prints the default annotation for the web host altering the "Update PHP" page URL.
#// 
#// This function is to be used after {@see wp_get_update_php_url()} to display a consistent
#// annotation if the web host has altered the default "Update PHP" page URL.
#// 
#// @since 5.1.0
#// @since 5.2.0 Added the `$before` and `$after` parameters.
#// 
#// @param string $before Markup to output before the annotation. Default `<p class="description">`.
#// @param string $after  Markup to output after the annotation. Default `</p>`.
#//
def wp_update_php_annotation(before="<p class=\"description\">", after="</p>", *args_):
    
    annotation = wp_get_update_php_annotation()
    if annotation:
        php_print(before + annotation + after)
    # end if
# end def wp_update_php_annotation
#// 
#// Returns the default annotation for the web hosting altering the "Update PHP" page URL.
#// 
#// This function is to be used after {@see wp_get_update_php_url()} to return a consistent
#// annotation if the web host has altered the default "Update PHP" page URL.
#// 
#// @since 5.2.0
#// 
#// @return string $message Update PHP page annotation. An empty string if no custom URLs are provided.
#//
def wp_get_update_php_annotation(*args_):
    
    update_url = wp_get_update_php_url()
    default_url = wp_get_default_update_php_url()
    if update_url == default_url:
        return ""
    # end if
    annotation = php_sprintf(__("This resource is provided by your web host, and is specific to your site. For more information, <a href=\"%s\" target=\"_blank\">see the official WordPress documentation</a>."), esc_url(default_url))
    return annotation
# end def wp_get_update_php_annotation
#// 
#// Gets the URL for directly updating the PHP version the site is running on.
#// 
#// A URL will only be returned if the `WP_DIRECT_UPDATE_PHP_URL` environment variable is specified or
#// by using the {@see 'wp_direct_php_update_url'} filter. This allows hosts to send users directly to
#// the page where they can update PHP to a newer version.
#// 
#// @since 5.1.1
#// 
#// @return string URL for directly updating PHP or empty string.
#//
def wp_get_direct_php_update_url(*args_):
    
    direct_update_url = ""
    if False != php_getenv("WP_DIRECT_UPDATE_PHP_URL"):
        direct_update_url = php_getenv("WP_DIRECT_UPDATE_PHP_URL")
    # end if
    #// 
    #// Filters the URL for directly updating the PHP version the site is running on from the host.
    #// 
    #// @since 5.1.1
    #// 
    #// @param string $direct_update_url URL for directly updating PHP.
    #//
    direct_update_url = apply_filters("wp_direct_php_update_url", direct_update_url)
    return direct_update_url
# end def wp_get_direct_php_update_url
#// 
#// Display a button directly linking to a PHP update process.
#// 
#// This provides hosts with a way for users to be sent directly to their PHP update process.
#// 
#// The button is only displayed if a URL is returned by `wp_get_direct_php_update_url()`.
#// 
#// @since 5.1.1
#//
def wp_direct_php_update_button(*args_):
    
    direct_update_url = wp_get_direct_php_update_url()
    if php_empty(lambda : direct_update_url):
        return
    # end if
    php_print("<p class=\"button-container\">")
    printf("<a class=\"button button-primary\" href=\"%1$s\" target=\"_blank\" rel=\"noopener noreferrer\">%2$s <span class=\"screen-reader-text\">%3$s</span><span aria-hidden=\"true\" class=\"dashicons dashicons-external\"></span></a>", esc_url(direct_update_url), __("Update PHP"), __("(opens in a new tab)"))
    php_print("</p>")
# end def wp_direct_php_update_button
#// 
#// Get the size of a directory.
#// 
#// A helper function that is used primarily to check whether
#// a blog has exceeded its allowed upload space.
#// 
#// @since MU (3.0.0)
#// @since 5.2.0 $max_execution_time parameter added.
#// 
#// @param string $directory Full path of a directory.
#// @param int    $max_execution_time Maximum time to run before giving up. In seconds.
#// The timeout is global and is measured from the moment WordPress started to load.
#// @return int|false|null Size in bytes if a valid directory. False if not. Null if timeout.
#//
def get_dirsize(directory=None, max_execution_time=None, *args_):
    
    dirsize = get_transient("dirsize_cache")
    if php_is_array(dirsize) and (php_isset(lambda : dirsize[directory]["size"])):
        return dirsize[directory]["size"]
    # end if
    if (not php_is_array(dirsize)):
        dirsize = Array()
    # end if
    #// Exclude individual site directories from the total when checking the main site of a network,
    #// as they are subdirectories and should not be counted.
    if is_multisite() and is_main_site():
        dirsize[directory]["size"] = recurse_dirsize(directory, directory + "/sites", max_execution_time)
    else:
        dirsize[directory]["size"] = recurse_dirsize(directory, None, max_execution_time)
    # end if
    set_transient("dirsize_cache", dirsize, HOUR_IN_SECONDS)
    return dirsize[directory]["size"]
# end def get_dirsize
#// 
#// Get the size of a directory recursively.
#// 
#// Used by get_dirsize() to get a directory's size when it contains
#// other directories.
#// 
#// @since MU (3.0.0)
#// @since 4.3.0 $exclude parameter added.
#// @since 5.2.0 $max_execution_time parameter added.
#// 
#// @param string $directory       Full path of a directory.
#// @param string|array $exclude   Optional. Full path of a subdirectory to exclude from the total, or array of paths.
#// Expected without trailing slash(es).
#// @param int $max_execution_time Maximum time to run before giving up. In seconds.
#// The timeout is global and is measured from the moment WordPress started to load.
#// @return int|false|null Size in bytes if a valid directory. False if not. Null if timeout.
#//
def recurse_dirsize(directory=None, exclude=None, max_execution_time=None, *args_):
    
    size = 0
    directory = untrailingslashit(directory)
    if (not php_file_exists(directory)) or (not php_is_dir(directory)) or (not php_is_readable(directory)):
        return False
    # end if
    if php_is_string(exclude) and directory == exclude or php_is_array(exclude) and php_in_array(directory, exclude, True):
        return False
    # end if
    if None == max_execution_time:
        #// Keep the previous behavior but attempt to prevent fatal errors from timeout if possible.
        if php_function_exists("ini_get"):
            max_execution_time = php_ini_get("max_execution_time")
        else:
            #// Disable...
            max_execution_time = 0
        # end if
        #// Leave 1 second "buffer" for other operations if $max_execution_time has reasonable value.
        if max_execution_time > 10:
            max_execution_time -= 1
        # end if
    # end if
    handle = php_opendir(directory)
    if handle:
        while True:
            file = php_readdir(handle)
            if not (file != False):
                break
            # end if
            path = directory + "/" + file
            if "." != file and ".." != file:
                if php_is_file(path):
                    size += filesize(path)
                elif php_is_dir(path):
                    handlesize = recurse_dirsize(path, exclude, max_execution_time)
                    if handlesize > 0:
                        size += handlesize
                    # end if
                # end if
                if max_execution_time > 0 and php_microtime(True) - WP_START_TIMESTAMP > max_execution_time:
                    #// Time exceeded. Give up instead of risking a fatal timeout.
                    size = None
                    break
                # end if
            # end if
        # end while
        php_closedir(handle)
    # end if
    return size
# end def recurse_dirsize
#// 
#// Checks compatibility with the current WordPress version.
#// 
#// @since 5.2.0
#// 
#// @param string $required Minimum required WordPress version.
#// @return bool True if required version is compatible or empty, false if not.
#//
def is_wp_version_compatible(required=None, *args_):
    
    return php_empty(lambda : required) or php_version_compare(get_bloginfo("version"), required, ">=")
# end def is_wp_version_compatible
#// 
#// Checks compatibility with the current PHP version.
#// 
#// @since 5.2.0
#// 
#// @param string $required Minimum required PHP version.
#// @return bool True if required version is compatible or empty, false if not.
#//
def is_php_version_compatible(required=None, *args_):
    
    return php_empty(lambda : required) or php_version_compare(php_phpversion(), required, ">=")
# end def is_php_version_compatible
#// 
#// Check if two numbers are nearly the same.
#// 
#// This is similar to using `round()` but the precision is more fine-grained.
#// 
#// @since 5.3.0
#// 
#// @param int|float $expected  The expected value.
#// @param int|float $actual    The actual number.
#// @param int|float $precision The allowed variation.
#// @return bool Whether the numbers match whithin the specified precision.
#//
def wp_fuzzy_number_match(expected=None, actual=None, precision=1, *args_):
    
    return abs(php_float(expected) - php_float(actual)) <= precision
# end def wp_fuzzy_number_match
