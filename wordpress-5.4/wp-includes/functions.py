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
def mysql2date(format_=None, date_=None, translate_=None, *_args_):
    if translate_ is None:
        translate_ = True
    # end if
    
    if php_empty(lambda : date_):
        return False
    # end if
    datetime_ = date_create(date_, wp_timezone())
    if False == datetime_:
        return False
    # end if
    #// Returns a sum of timestamp with timezone offset. Ideally should never be used.
    if "G" == format_ or "U" == format_:
        return datetime_.gettimestamp() + datetime_.getoffset()
    # end if
    if translate_:
        return wp_date(format_, datetime_.gettimestamp())
    # end if
    return datetime_.format(format_)
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
def current_time(type_=None, gmt_=0, *_args_):
    
    
    #// Don't use non-GMT timestamp, unless you know the difference and really need to.
    if "timestamp" == type_ or "U" == type_:
        return time() if gmt_ else time() + php_int(get_option("gmt_offset") * HOUR_IN_SECONDS)
    # end if
    if "mysql" == type_:
        type_ = "Y-m-d H:i:s"
    # end if
    timezone_ = php_new_class("DateTimeZone", lambda : DateTimeZone("UTC")) if gmt_ else wp_timezone()
    datetime_ = php_new_class("DateTime", lambda : DateTime("now", timezone_))
    return datetime_.format(type_)
# end def current_time
#// 
#// Retrieves the current time as an object with the timezone from settings.
#// 
#// @since 5.3.0
#// 
#// @return DateTimeImmutable Date and time object.
#//
def current_datetime(*_args_):
    
    
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
def wp_timezone_string(*_args_):
    
    
    timezone_string_ = get_option("timezone_string")
    if timezone_string_:
        return timezone_string_
    # end if
    offset_ = php_float(get_option("gmt_offset"))
    hours_ = php_int(offset_)
    minutes_ = offset_ - hours_
    sign_ = "-" if offset_ < 0 else "+"
    abs_hour_ = abs(hours_)
    abs_mins_ = abs(minutes_ * 60)
    tz_offset_ = php_sprintf("%s%02d:%02d", sign_, abs_hour_, abs_mins_)
    return tz_offset_
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
def wp_timezone(*_args_):
    
    
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
def date_i18n(format_=None, timestamp_with_offset_=None, gmt_=None, *_args_):
    if timestamp_with_offset_ is None:
        timestamp_with_offset_ = False
    # end if
    if gmt_ is None:
        gmt_ = False
    # end if
    
    timestamp_ = timestamp_with_offset_
    #// If timestamp is omitted it should be current time (summed with offset, unless `$gmt` is true).
    if (not php_is_numeric(timestamp_)):
        timestamp_ = current_time("timestamp", gmt_)
    # end if
    #// 
    #// This is a legacy implementation quirk that the returned timestamp is also with offset.
    #// Ideally this function should never be used to produce a timestamp.
    #//
    if "U" == format_:
        date_ = timestamp_
    elif gmt_ and False == timestamp_with_offset_:
        #// Current time in UTC.
        date_ = wp_date(format_, None, php_new_class("DateTimeZone", lambda : DateTimeZone("UTC")))
    elif False == timestamp_with_offset_:
        #// Current time in site's timezone.
        date_ = wp_date(format_)
    else:
        #// 
        #// Timestamp with offset is typically produced by a UTC `strtotime()` call on an input without timezone.
        #// This is the best attempt to reverse that operation into a local time to use.
        #//
        local_time_ = gmdate("Y-m-d H:i:s", timestamp_)
        timezone_ = wp_timezone()
        datetime_ = date_create(local_time_, timezone_)
        date_ = wp_date(format_, datetime_.gettimestamp(), timezone_)
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
    date_ = apply_filters("date_i18n", date_, format_, timestamp_, gmt_)
    return date_
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
def wp_date(format_=None, timestamp_=None, timezone_=None, *_args_):
    if timestamp_ is None:
        timestamp_ = None
    # end if
    if timezone_ is None:
        timezone_ = None
    # end if
    
    global wp_locale_
    php_check_if_defined("wp_locale_")
    if None == timestamp_:
        timestamp_ = time()
    elif (not php_is_numeric(timestamp_)):
        return False
    # end if
    if (not timezone_):
        timezone_ = wp_timezone()
    # end if
    datetime_ = date_create("@" + timestamp_)
    datetime_.settimezone(timezone_)
    if php_empty(lambda : wp_locale_.month) or php_empty(lambda : wp_locale_.weekday):
        date_ = datetime_.format(format_)
    else:
        #// We need to unpack shorthand `r` format because it has parts that might be localized.
        format_ = php_preg_replace("/(?<!\\\\)r/", DATE_RFC2822, format_)
        new_format_ = ""
        format_length_ = php_strlen(format_)
        month_ = wp_locale_.get_month(datetime_.format("m"))
        weekday_ = wp_locale_.get_weekday(datetime_.format("w"))
        i_ = 0
        while i_ < format_length_:
            
            for case in Switch(format_[i_]):
                if case("D"):
                    new_format_ += addcslashes(wp_locale_.get_weekday_abbrev(weekday_), "\\A..Za..z")
                    break
                # end if
                if case("F"):
                    new_format_ += addcslashes(month_, "\\A..Za..z")
                    break
                # end if
                if case("l"):
                    new_format_ += addcslashes(weekday_, "\\A..Za..z")
                    break
                # end if
                if case("M"):
                    new_format_ += addcslashes(wp_locale_.get_month_abbrev(month_), "\\A..Za..z")
                    break
                # end if
                if case("a"):
                    new_format_ += addcslashes(wp_locale_.get_meridiem(datetime_.format("a")), "\\A..Za..z")
                    break
                # end if
                if case("A"):
                    new_format_ += addcslashes(wp_locale_.get_meridiem(datetime_.format("A")), "\\A..Za..z")
                    break
                # end if
                if case("\\"):
                    new_format_ += format_[i_]
                    #// If character follows a slash, we add it without translating.
                    if i_ < format_length_:
                        i_ += 1
                        new_format_ += format_[i_]
                    # end if
                    break
                # end if
                if case():
                    new_format_ += format_[i_]
                    break
                # end if
            # end for
            i_ += 1
        # end while
        date_ = datetime_.format(new_format_)
        date_ = wp_maybe_decline_date(date_, format_)
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
    date_ = apply_filters("wp_date", date_, format_, timestamp_, timezone_)
    return date_
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
def wp_maybe_decline_date(date_=None, format_="", *_args_):
    
    
    global wp_locale_
    php_check_if_defined("wp_locale_")
    #// i18n functions are not available in SHORTINIT mode.
    if (not php_function_exists("_x")):
        return date_
    # end if
    #// 
    #// translators: If months in your language require a genitive case,
    #// translate this to 'on'. Do not translate into your own language.
    #//
    if "on" == _x("off", "decline months names: on or off"):
        months_ = wp_locale_.month
        months_genitive_ = wp_locale_.month_genitive
        #// 
        #// Match a format like 'j F Y' or 'j. F' (day of the month, followed by month name)
        #// and decline the month.
        #//
        if format_:
            decline_ = php_preg_match("#[dj]\\.? F#", format_)
        else:
            #// If the format is not passed, try to guess it from the date string.
            decline_ = php_preg_match("#\\b\\d{1,2}\\.? [^\\d ]+\\b#u", date_)
        # end if
        if decline_:
            for key_,month_ in months_.items():
                months_[key_] = "# " + preg_quote(month_, "#") + "\\b#u"
            # end for
            for key_,month_ in months_genitive_.items():
                months_genitive_[key_] = " " + month_
            # end for
            date_ = php_preg_replace(months_, months_genitive_, date_)
        # end if
        #// 
        #// Match a format like 'F jS' or 'F j' (month name, followed by day with an optional ordinal suffix)
        #// and change it to declined 'j F'.
        #//
        if format_:
            decline_ = php_preg_match("#F [dj]#", format_)
        else:
            #// If the format is not passed, try to guess it from the date string.
            decline_ = php_preg_match("#\\b[^\\d ]+ \\d{1,2}(st|nd|rd|th)?\\b#u", php_trim(date_))
        # end if
        if decline_:
            for key_,month_ in months_.items():
                months_[key_] = "#\\b" + preg_quote(month_, "#") + " (\\d{1,2})(st|nd|rd|th)?([-â]\\d{1,2})?(st|nd|rd|th)?\\b#u"
            # end for
            for key_,month_ in months_genitive_.items():
                months_genitive_[key_] = "$1$3 " + month_
            # end for
            date_ = php_preg_replace(months_, months_genitive_, date_)
        # end if
    # end if
    #// Used for locale-specific rules.
    locale_ = get_locale()
    if "ca" == locale_:
        #// " de abril| de agost| de octubre..." -> " d'abril| d'agost| d'octubre..."
        date_ = php_preg_replace("# de ([ao])#i", " d'\\1", date_)
    # end if
    return date_
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
def number_format_i18n(number_=None, decimals_=0, *_args_):
    
    
    global wp_locale_
    php_check_if_defined("wp_locale_")
    if (php_isset(lambda : wp_locale_)):
        formatted_ = number_format(number_, absint(decimals_), wp_locale_.number_format["decimal_point"], wp_locale_.number_format["thousands_sep"])
    else:
        formatted_ = number_format(number_, absint(decimals_))
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
    return apply_filters("number_format_i18n", formatted_, number_, decimals_)
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
def size_format(bytes_=None, decimals_=0, *_args_):
    
    
    quant_ = Array({"TB": TB_IN_BYTES, "GB": GB_IN_BYTES, "MB": MB_IN_BYTES, "KB": KB_IN_BYTES, "B": 1})
    if 0 == bytes_:
        return number_format_i18n(0, decimals_) + " B"
    # end if
    for unit_,mag_ in quant_.items():
        if doubleval(bytes_) >= mag_:
            return number_format_i18n(bytes_ / mag_, decimals_) + " " + unit_
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
def human_readable_duration(duration_="", *_args_):
    
    
    if php_empty(lambda : duration_) or (not php_is_string(duration_)):
        return False
    # end if
    duration_ = php_trim(duration_)
    #// Remove prepended negative sign.
    if "-" == php_substr(duration_, 0, 1):
        duration_ = php_substr(duration_, 1)
    # end if
    #// Extract duration parts.
    duration_parts_ = php_array_reverse(php_explode(":", duration_))
    duration_count_ = php_count(duration_parts_)
    hour_ = None
    minute_ = None
    second_ = None
    if 3 == duration_count_:
        #// Validate HH:ii:ss duration format.
        if (not php_bool(php_preg_match("/^([0-9]+):([0-5]?[0-9]):([0-5]?[0-9])$/", duration_))):
            return False
        # end if
        #// Three parts: hours, minutes & seconds.
        second_, minute_, hour_ = duration_parts_
    elif 2 == duration_count_:
        #// Validate ii:ss duration format.
        if (not php_bool(php_preg_match("/^([0-5]?[0-9]):([0-5]?[0-9])$/", duration_))):
            return False
        # end if
        #// Two parts: minutes & seconds.
        second_, minute_ = duration_parts_
    else:
        return False
    # end if
    human_readable_duration_ = Array()
    #// Add the hour part to the string.
    if php_is_numeric(hour_):
        #// translators: %s: Time duration in hour or hours.
        human_readable_duration_[-1] = php_sprintf(_n("%s hour", "%s hours", hour_), php_int(hour_))
    # end if
    #// Add the minute part to the string.
    if php_is_numeric(minute_):
        #// translators: %s: Time duration in minute or minutes.
        human_readable_duration_[-1] = php_sprintf(_n("%s minute", "%s minutes", minute_), php_int(minute_))
    # end if
    #// Add the second part to the string.
    if php_is_numeric(second_):
        #// translators: %s: Time duration in second or seconds.
        human_readable_duration_[-1] = php_sprintf(_n("%s second", "%s seconds", second_), php_int(second_))
    # end if
    return php_implode(", ", human_readable_duration_)
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
def get_weekstartend(mysqlstring_=None, start_of_week_="", *_args_):
    
    
    #// MySQL string year.
    my_ = php_substr(mysqlstring_, 0, 4)
    #// MySQL string month.
    mm_ = php_substr(mysqlstring_, 8, 2)
    #// MySQL string day.
    md_ = php_substr(mysqlstring_, 5, 2)
    #// The timestamp for MySQL string day.
    day_ = mktime(0, 0, 0, md_, mm_, my_)
    #// The day of the week from the timestamp.
    weekday_ = gmdate("w", day_)
    if (not php_is_numeric(start_of_week_)):
        start_of_week_ = get_option("start_of_week")
    # end if
    if weekday_ < start_of_week_:
        weekday_ += 7
    # end if
    #// The most recent week start day on or before $day.
    start_ = day_ - DAY_IN_SECONDS * weekday_ - start_of_week_
    #// $start + 1 week - 1 second.
    end_ = start_ + WEEK_IN_SECONDS - 1
    return php_compact("start_", "end_")
# end def get_weekstartend
#// 
#// Unserialize value only if it was serialized.
#// 
#// @since 2.0.0
#// 
#// @param string $original Maybe unserialized original, if is needed.
#// @return mixed Unserialized data can be any type.
#//
def maybe_unserialize(original_=None, *_args_):
    
    
    if is_serialized(original_):
        #// Don't attempt to unserialize data that wasn't serialized going in.
        return php_no_error(lambda: unserialize(original_))
    # end if
    return original_
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
def is_serialized(data_=None, strict_=None, *_args_):
    if strict_ is None:
        strict_ = True
    # end if
    
    #// If it isn't a string, it isn't serialized.
    if (not php_is_string(data_)):
        return False
    # end if
    data_ = php_trim(data_)
    if "N;" == data_:
        return True
    # end if
    if php_strlen(data_) < 4:
        return False
    # end if
    if ":" != data_[1]:
        return False
    # end if
    if strict_:
        lastc_ = php_substr(data_, -1)
        if ";" != lastc_ and "}" != lastc_:
            return False
        # end if
    else:
        semicolon_ = php_strpos(data_, ";")
        brace_ = php_strpos(data_, "}")
        #// Either ; or } must exist.
        if False == semicolon_ and False == brace_:
            return False
        # end if
        #// But neither must be in the first X characters.
        if False != semicolon_ and semicolon_ < 3:
            return False
        # end if
        if False != brace_ and brace_ < 4:
            return False
        # end if
    # end if
    token_ = data_[0]
    for case in Switch(token_):
        if case("s"):
            if strict_:
                if "\"" != php_substr(data_, -2, 1):
                    return False
                # end if
            elif False == php_strpos(data_, "\""):
                return False
            # end if
        # end if
        if case("a"):
            pass
        # end if
        if case("O"):
            return php_bool(php_preg_match(str("/^") + str(token_) + str(":[0-9]+:/s"), data_))
        # end if
        if case("b"):
            pass
        # end if
        if case("i"):
            pass
        # end if
        if case("d"):
            end_ = "$" if strict_ else ""
            return php_bool(php_preg_match(str("/^") + str(token_) + str(":[0-9.E+-]+;") + str(end_) + str("/"), data_))
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
def is_serialized_string(data_=None, *_args_):
    
    
    #// if it isn't a string, it isn't a serialized string.
    if (not php_is_string(data_)):
        return False
    # end if
    data_ = php_trim(data_)
    if php_strlen(data_) < 4:
        return False
    elif ":" != data_[1]:
        return False
    elif ";" != php_substr(data_, -1):
        return False
    elif "s" != data_[0]:
        return False
    elif "\"" != php_substr(data_, -2, 1):
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
def maybe_serialize(data_=None, *_args_):
    
    
    if php_is_array(data_) or php_is_object(data_):
        return serialize(data_)
    # end if
    #// 
    #// Double serialization is required for backward compatibility.
    #// See https://core.trac.wordpress.org/ticket/12930
    #// Also the world will end. See WP 3.6.1.
    #//
    if is_serialized(data_, False):
        return serialize(data_)
    # end if
    return data_
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
def xmlrpc_getposttitle(content_=None, *_args_):
    
    
    global post_default_title_
    php_check_if_defined("post_default_title_")
    if php_preg_match("/<title>(.+?)<\\/title>/is", content_, matchtitle_):
        post_title_ = matchtitle_[1]
    else:
        post_title_ = post_default_title_
    # end if
    return post_title_
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
def xmlrpc_getpostcategory(content_=None, *_args_):
    
    
    global post_default_category_
    php_check_if_defined("post_default_category_")
    if php_preg_match("/<category>(.+?)<\\/category>/is", content_, matchcat_):
        post_category_ = php_trim(matchcat_[1], ",")
        post_category_ = php_explode(",", post_category_)
    else:
        post_category_ = post_default_category_
    # end if
    return post_category_
# end def xmlrpc_getpostcategory
#// 
#// XMLRPC XML content without title and category elements.
#// 
#// @since 0.71
#// 
#// @param string $content XML-RPC XML Request content.
#// @return string XMLRPC XML Request content without title and category elements.
#//
def xmlrpc_removepostdata(content_=None, *_args_):
    
    
    content_ = php_preg_replace("/<title>(.+?)<\\/title>/si", "", content_)
    content_ = php_preg_replace("/<category>(.+?)<\\/category>/si", "", content_)
    content_ = php_trim(content_)
    return content_
# end def xmlrpc_removepostdata
#// 
#// Use RegEx to extract URLs from arbitrary content.
#// 
#// @since 3.7.0
#// 
#// @param string $content Content to extract URLs from.
#// @return string[] Array of URLs found in passed string.
#//
def wp_extract_urls(content_=None, *_args_):
    
    
    preg_match_all("#([\"']?)(" + "(?:([\\w-]+:)?//?)" + "[^\\s()<>]+" + "[.]" + "(?:" + "\\([\\w\\d]+\\)|" + "(?:" + "[^`!()\\[\\]{};:'\".,<>Â«Â»ââââ\\s]|" + "(?:[:]\\d+)?/?" + ")+" + ")" + ")\\1#", content_, post_links_)
    post_links_ = array_unique(php_array_map("html_entity_decode", post_links_[2]))
    return php_array_values(post_links_)
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
def do_enclose(content_=None, post_=None, *_args_):
    if content_ is None:
        content_ = None
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    #// @todo Tidy this code and make the debug code optional.
    php_include_file(ABSPATH + WPINC + "/class-IXR.php", once=False)
    post_ = get_post(post_)
    if (not post_):
        return False
    # end if
    if None == content_:
        content_ = post_.post_content
    # end if
    post_links_ = Array()
    pung_ = get_enclosed(post_.ID)
    post_links_temp_ = wp_extract_urls(content_)
    for link_test_ in pung_:
        #// Link is no longer in post.
        if (not php_in_array(link_test_, post_links_temp_, True)):
            mids_ = wpdb_.get_col(wpdb_.prepare(str("SELECT meta_id FROM ") + str(wpdb_.postmeta) + str(" WHERE post_id = %d AND meta_key = 'enclosure' AND meta_value LIKE %s"), post_.ID, wpdb_.esc_like(link_test_) + "%"))
            for mid_ in mids_:
                delete_metadata_by_mid("post", mid_)
            # end for
        # end if
    # end for
    for link_test_ in post_links_temp_:
        #// If we haven't pung it already.
        if (not php_in_array(link_test_, pung_, True)):
            test_ = php_no_error(lambda: php_parse_url(link_test_))
            if False == test_:
                continue
            # end if
            if (php_isset(lambda : test_["query"])):
                post_links_[-1] = link_test_
            elif (php_isset(lambda : test_["path"])) and "/" != test_["path"] and "" != test_["path"]:
                post_links_[-1] = link_test_
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
    post_links_ = apply_filters("enclosure_links", post_links_, post_.ID)
    for url_ in post_links_:
        if "" != url_ and (not wpdb_.get_var(wpdb_.prepare(str("SELECT post_id FROM ") + str(wpdb_.postmeta) + str(" WHERE post_id = %d AND meta_key = 'enclosure' AND meta_value LIKE %s"), post_.ID, wpdb_.esc_like(url_) + "%"))):
            headers_ = wp_get_http_headers(url_)
            if headers_:
                len_ = php_int(headers_["content-length"]) if (php_isset(lambda : headers_["content-length"])) else 0
                type_ = headers_["content-type"] if (php_isset(lambda : headers_["content-type"])) else ""
                allowed_types_ = Array("video", "audio")
                #// Check to see if we can figure out the mime type from the extension.
                url_parts_ = php_no_error(lambda: php_parse_url(url_))
                if False != url_parts_:
                    extension_ = pathinfo(url_parts_["path"], PATHINFO_EXTENSION)
                    if (not php_empty(lambda : extension_)):
                        for exts_,mime_ in wp_get_mime_types().items():
                            if php_preg_match("!^(" + exts_ + ")$!i", extension_):
                                type_ = mime_
                                break
                            # end if
                        # end for
                    # end if
                # end if
                if php_in_array(php_substr(type_, 0, php_strpos(type_, "/")), allowed_types_, True):
                    add_post_meta(post_.ID, "enclosure", str(url_) + str("\n") + str(len_) + str("\n") + str(mime_) + str("\n"))
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
def wp_get_http_headers(url_=None, deprecated_=None, *_args_):
    if deprecated_ is None:
        deprecated_ = False
    # end if
    
    if (not php_empty(lambda : deprecated_)):
        _deprecated_argument(inspect.currentframe().f_code.co_name, "2.7.0")
    # end if
    response_ = wp_safe_remote_head(url_)
    if is_wp_error(response_):
        return False
    # end if
    return wp_remote_retrieve_headers(response_)
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
def is_new_day(*_args_):
    
    
    global currentday_
    global previousday_
    php_check_if_defined("currentday_","previousday_")
    if currentday_ != previousday_:
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
def build_query(data_=None, *_args_):
    
    
    return _http_build_query(data_, None, "&", "", False)
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
def _http_build_query(data_=None, prefix_=None, sep_=None, key_="", urlencode_=None, *_args_):
    if prefix_ is None:
        prefix_ = None
    # end if
    if sep_ is None:
        sep_ = None
    # end if
    if urlencode_ is None:
        urlencode_ = True
    # end if
    
    ret_ = Array()
    for k_,v_ in data_.items():
        if urlencode_:
            k_ = urlencode(k_)
        # end if
        if php_is_int(k_) and None != prefix_:
            k_ = prefix_ + k_
        # end if
        if (not php_empty(lambda : key_)):
            k_ = key_ + "%5B" + k_ + "%5D"
        # end if
        if None == v_:
            continue
        elif False == v_:
            v_ = "0"
        # end if
        if php_is_array(v_) or php_is_object(v_):
            php_array_push(ret_, _http_build_query(v_, "", sep_, k_, urlencode_))
        elif urlencode_:
            php_array_push(ret_, k_ + "=" + urlencode(v_))
        else:
            php_array_push(ret_, k_ + "=" + v_)
        # end if
    # end for
    if None == sep_:
        sep_ = php_ini_get("arg_separator.output")
    # end if
    return php_implode(sep_, ret_)
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
def add_query_arg(*args_):
    
    
    if php_is_array(args_[0]):
        if php_count(args_) < 2 or False == args_[1]:
            uri_ = PHP_SERVER["REQUEST_URI"]
        else:
            uri_ = args_[1]
        # end if
    else:
        if php_count(args_) < 3 or False == args_[2]:
            uri_ = PHP_SERVER["REQUEST_URI"]
        else:
            uri_ = args_[2]
        # end if
    # end if
    frag_ = php_strstr(uri_, "#")
    if frag_:
        uri_ = php_substr(uri_, 0, -php_strlen(frag_))
    else:
        frag_ = ""
    # end if
    if 0 == php_stripos(uri_, "http://"):
        protocol_ = "http://"
        uri_ = php_substr(uri_, 7)
    elif 0 == php_stripos(uri_, "https://"):
        protocol_ = "https://"
        uri_ = php_substr(uri_, 8)
    else:
        protocol_ = ""
    # end if
    if php_strpos(uri_, "?") != False:
        base_, query_ = php_explode("?", uri_, 2)
        base_ += "?"
    elif protocol_ or php_strpos(uri_, "=") == False:
        base_ = uri_ + "?"
        query_ = ""
    else:
        base_ = ""
        query_ = uri_
    # end if
    wp_parse_str(query_, qs_)
    qs_ = urlencode_deep(qs_)
    #// This re-URL-encodes things that were already in the query string.
    if php_is_array(args_[0]):
        for k_,v_ in args_[0].items():
            qs_[k_] = v_
        # end for
    else:
        qs_[args_[0]] = args_[1]
    # end if
    for k_,v_ in qs_.items():
        if False == v_:
            qs_[k_] = None
        # end if
    # end for
    ret_ = build_query(qs_)
    ret_ = php_trim(ret_, "?")
    ret_ = php_preg_replace("#=(&|$)#", "$1", ret_)
    ret_ = protocol_ + base_ + ret_ + frag_
    ret_ = php_rtrim(ret_, "?")
    return ret_
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
def remove_query_arg(key_=None, query_=None, *_args_):
    if query_ is None:
        query_ = False
    # end if
    
    if php_is_array(key_):
        #// Removing multiple keys.
        for k_ in key_:
            query_ = add_query_arg(k_, False, query_)
        # end for
        return query_
    # end if
    return add_query_arg(key_, False, query_)
# end def remove_query_arg
#// 
#// Returns an array of single-use query variable names that can be removed from a URL.
#// 
#// @since 4.4.0
#// 
#// @return string[] An array of parameters to remove from the URL.
#//
def wp_removable_query_args(*_args_):
    
    
    removable_query_args_ = Array("activate", "activated", "approved", "deactivate", "deleted", "disabled", "doing_wp_cron", "enabled", "error", "hotkeys_highlight_first", "hotkeys_highlight_last", "locked", "message", "same", "saved", "settings-updated", "skipped", "spammed", "trashed", "unspammed", "untrashed", "update", "updated", "wp-post-new-reload")
    #// 
    #// Filters the list of query variables to remove.
    #// 
    #// @since 4.2.0
    #// 
    #// @param string[] $removable_query_args An array of query variables to remove from a URL.
    #//
    return apply_filters("removable_query_args", removable_query_args_)
# end def wp_removable_query_args
#// 
#// Walks the array while sanitizing the contents.
#// 
#// @since 0.71
#// 
#// @param array $array Array to walk while sanitizing contents.
#// @return array Sanitized $array.
#//
def add_magic_quotes(array_=None, *_args_):
    
    
    for k_,v_ in array_.items():
        if php_is_array(v_):
            array_[k_] = add_magic_quotes(v_)
        else:
            array_[k_] = addslashes(v_)
        # end if
    # end for
    return array_
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
def wp_remote_fopen(uri_=None, *_args_):
    
    
    parsed_url_ = php_no_error(lambda: php_parse_url(uri_))
    if (not parsed_url_) or (not php_is_array(parsed_url_)):
        return False
    # end if
    options_ = Array()
    options_["timeout"] = 10
    response_ = wp_safe_remote_get(uri_, options_)
    if is_wp_error(response_):
        return False
    # end if
    return wp_remote_retrieve_body(response_)
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
def wp(query_vars_="", *_args_):
    
    
    global wp_
    global wp_query_
    global wp_the_query_
    php_check_if_defined("wp_","wp_query_","wp_the_query_")
    wp_.main(query_vars_)
    if (not (php_isset(lambda : wp_the_query_))):
        wp_the_query_ = wp_query_
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
def get_status_header_desc(code_=None, *_args_):
    
    
    global wp_header_to_desc_
    php_check_if_defined("wp_header_to_desc_")
    code_ = absint(code_)
    if (not (php_isset(lambda : wp_header_to_desc_))):
        wp_header_to_desc_ = Array({100: "Continue", 101: "Switching Protocols", 102: "Processing", 103: "Early Hints", 200: "OK", 201: "Created", 202: "Accepted", 203: "Non-Authoritative Information", 204: "No Content", 205: "Reset Content", 206: "Partial Content", 207: "Multi-Status", 226: "IM Used", 300: "Multiple Choices", 301: "Moved Permanently", 302: "Found", 303: "See Other", 304: "Not Modified", 305: "Use Proxy", 306: "Reserved", 307: "Temporary Redirect", 308: "Permanent Redirect", 400: "Bad Request", 401: "Unauthorized", 402: "Payment Required", 403: "Forbidden", 404: "Not Found", 405: "Method Not Allowed", 406: "Not Acceptable", 407: "Proxy Authentication Required", 408: "Request Timeout", 409: "Conflict", 410: "Gone", 411: "Length Required", 412: "Precondition Failed", 413: "Request Entity Too Large", 414: "Request-URI Too Long", 415: "Unsupported Media Type", 416: "Requested Range Not Satisfiable", 417: "Expectation Failed", 418: "I'm a teapot", 421: "Misdirected Request", 422: "Unprocessable Entity", 423: "Locked", 424: "Failed Dependency", 426: "Upgrade Required", 428: "Precondition Required", 429: "Too Many Requests", 431: "Request Header Fields Too Large", 451: "Unavailable For Legal Reasons", 500: "Internal Server Error", 501: "Not Implemented", 502: "Bad Gateway", 503: "Service Unavailable", 504: "Gateway Timeout", 505: "HTTP Version Not Supported", 506: "Variant Also Negotiates", 507: "Insufficient Storage", 510: "Not Extended", 511: "Network Authentication Required"})
    # end if
    if (php_isset(lambda : wp_header_to_desc_[code_])):
        return wp_header_to_desc_[code_]
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
def status_header(code_=None, description_="", *_args_):
    
    
    if (not description_):
        description_ = get_status_header_desc(code_)
    # end if
    if php_empty(lambda : description_):
        return
    # end if
    protocol_ = wp_get_server_protocol()
    status_header_ = str(protocol_) + str(" ") + str(code_) + str(" ") + str(description_)
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
        status_header_ = apply_filters("status_header", status_header_, code_, description_, protocol_)
    # end if
    if (not php_headers_sent()):
        php_header(status_header_, True, code_)
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
def wp_get_nocache_headers(*_args_):
    
    
    headers_ = Array({"Expires": "Wed, 11 Jan 1984 05:00:00 GMT", "Cache-Control": "no-cache, must-revalidate, max-age=0"})
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
        headers_ = apply_filters("nocache_headers", headers_)
    # end if
    headers_["Last-Modified"] = False
    return headers_
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
def nocache_headers(*_args_):
    
    
    if php_headers_sent():
        return
    # end if
    headers_ = wp_get_nocache_headers()
    headers_["Last-Modified"] = None
    php_header_remove("Last-Modified")
    for name_,field_value_ in headers_.items():
        php_header(str(name_) + str(": ") + str(field_value_))
    # end for
# end def nocache_headers
#// 
#// Set the headers for caching for 10 days with JavaScript content type.
#// 
#// @since 2.1.0
#//
def cache_javascript_headers(*_args_):
    
    
    expiresOffset_ = 10 * DAY_IN_SECONDS
    php_header("Content-Type: text/javascript; charset=" + get_bloginfo("charset"))
    php_header("Vary: Accept-Encoding")
    #// Handle proxies.
    php_header("Expires: " + gmdate("D, d M Y H:i:s", time() + expiresOffset_) + " GMT")
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
def get_num_queries(*_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    return wpdb_.num_queries
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
def bool_from_yn(yn_=None, *_args_):
    
    
    return php_strtolower(yn_) == "y"
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
def do_feed(*_args_):
    
    
    global wp_query_
    php_check_if_defined("wp_query_")
    feed_ = get_query_var("feed")
    #// Remove the pad, if present.
    feed_ = php_preg_replace("/^_+/", "", feed_)
    if "" == feed_ or "feed" == feed_:
        feed_ = get_default_feed()
    # end if
    if (not has_action(str("do_feed_") + str(feed_))):
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
    do_action(str("do_feed_") + str(feed_), wp_query_.is_comment_feed, feed_)
# end def do_feed
#// 
#// Load the RDF RSS 0.91 Feed template.
#// 
#// @since 2.1.0
#// 
#// @see load_template()
#//
def do_feed_rdf(*_args_):
    
    
    load_template(ABSPATH + WPINC + "/feed-rdf.php")
# end def do_feed_rdf
#// 
#// Load the RSS 1.0 Feed Template.
#// 
#// @since 2.1.0
#// 
#// @see load_template()
#//
def do_feed_rss(*_args_):
    
    
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
def do_feed_rss2(for_comments_=None, *_args_):
    
    
    if for_comments_:
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
def do_feed_atom(for_comments_=None, *_args_):
    
    
    if for_comments_:
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
def do_robots(*_args_):
    
    
    php_header("Content-Type: text/plain; charset=utf-8")
    #// 
    #// Fires when displaying the robots.txt file.
    #// 
    #// @since 2.1.0
    #//
    do_action("do_robotstxt")
    output_ = "User-agent: *\n"
    public_ = get_option("blog_public")
    site_url_ = php_parse_url(site_url())
    path_ = site_url_["path"] if (not php_empty(lambda : site_url_["path"])) else ""
    output_ += str("Disallow: ") + str(path_) + str("/wp-admin/\n")
    output_ += str("Allow: ") + str(path_) + str("/wp-admin/admin-ajax.php\n")
    #// 
    #// Filters the robots.txt output.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string $output The robots.txt output.
    #// @param bool   $public Whether the site is considered "public".
    #//
    php_print(apply_filters("robots_txt", output_, public_))
# end def do_robots
#// 
#// Display the favicon.ico file content.
#// 
#// @since 5.4.0
#//
def do_favicon(*_args_):
    
    
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
def is_blog_installed(*_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    #// 
    #// Check cache first. If options table goes away and we have true
    #// cached, oh well.
    #//
    if wp_cache_get("is_blog_installed"):
        return True
    # end if
    suppress_ = wpdb_.suppress_errors()
    if (not wp_installing()):
        alloptions_ = wp_load_alloptions()
    # end if
    #// If siteurl is not set to autoload, check it specifically.
    if (not (php_isset(lambda : alloptions_["siteurl"]))):
        installed_ = wpdb_.get_var(str("SELECT option_value FROM ") + str(wpdb_.options) + str(" WHERE option_name = 'siteurl'"))
    else:
        installed_ = alloptions_["siteurl"]
    # end if
    wpdb_.suppress_errors(suppress_)
    installed_ = (not php_empty(lambda : installed_))
    wp_cache_set("is_blog_installed", installed_)
    if installed_:
        return True
    # end if
    #// If visiting repair.php, return true and let it take over.
    if php_defined("WP_REPAIRING"):
        return True
    # end if
    suppress_ = wpdb_.suppress_errors()
    #// 
    #// Loop over the WP tables. If none exist, then scratch installation is allowed.
    #// If one or more exist, suggest table repair since we got here because the
    #// options table could not be accessed.
    #//
    wp_tables_ = wpdb_.tables()
    for table_ in wp_tables_:
        #// The existence of custom user tables shouldn't suggest an insane state or prevent a clean installation.
        if php_defined("CUSTOM_USER_TABLE") and CUSTOM_USER_TABLE == table_:
            continue
        # end if
        if php_defined("CUSTOM_USER_META_TABLE") and CUSTOM_USER_META_TABLE == table_:
            continue
        # end if
        if (not wpdb_.get_results(str("DESCRIBE ") + str(table_) + str(";"))):
            continue
        # end if
        #// One or more tables exist. We are insane.
        wp_load_translations_early()
        #// Die with a DB error.
        wpdb_.error = php_sprintf(__("One or more database tables are unavailable. The database may need to be <a href=\"%s\">repaired</a>."), "maint/repair.php?referrer=is_blog_installed")
        dead_db()
    # end for
    wpdb_.suppress_errors(suppress_)
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
def wp_nonce_url(actionurl_=None, action_=None, name_="_wpnonce", *_args_):
    if action_ is None:
        action_ = -1
    # end if
    
    actionurl_ = php_str_replace("&amp;", "&", actionurl_)
    return esc_html(add_query_arg(name_, wp_create_nonce(action_), actionurl_))
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
def wp_nonce_field(action_=None, name_="_wpnonce", referer_=None, echo_=None, *_args_):
    if action_ is None:
        action_ = -1
    # end if
    if referer_ is None:
        referer_ = True
    # end if
    if echo_ is None:
        echo_ = True
    # end if
    
    name_ = esc_attr(name_)
    nonce_field_ = "<input type=\"hidden\" id=\"" + name_ + "\" name=\"" + name_ + "\" value=\"" + wp_create_nonce(action_) + "\" />"
    if referer_:
        nonce_field_ += wp_referer_field(False)
    # end if
    if echo_:
        php_print(nonce_field_)
    # end if
    return nonce_field_
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
def wp_referer_field(echo_=None, *_args_):
    if echo_ is None:
        echo_ = True
    # end if
    
    referer_field_ = "<input type=\"hidden\" name=\"_wp_http_referer\" value=\"" + esc_attr(wp_unslash(PHP_SERVER["REQUEST_URI"])) + "\" />"
    if echo_:
        php_print(referer_field_)
    # end if
    return referer_field_
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
def wp_original_referer_field(echo_=None, jump_back_to_="current", *_args_):
    if echo_ is None:
        echo_ = True
    # end if
    
    ref_ = wp_get_original_referer()
    if (not ref_):
        ref_ = wp_get_referer() if "previous" == jump_back_to_ else wp_unslash(PHP_SERVER["REQUEST_URI"])
    # end if
    orig_referer_field_ = "<input type=\"hidden\" name=\"_wp_original_http_referer\" value=\"" + esc_attr(ref_) + "\" />"
    if echo_:
        php_print(orig_referer_field_)
    # end if
    return orig_referer_field_
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
def wp_get_referer(*_args_):
    
    
    if (not php_function_exists("wp_validate_redirect")):
        return False
    # end if
    ref_ = wp_get_raw_referer()
    if ref_ and wp_unslash(PHP_SERVER["REQUEST_URI"]) != ref_ and home_url() + wp_unslash(PHP_SERVER["REQUEST_URI"]) != ref_:
        return wp_validate_redirect(ref_, False)
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
def wp_get_raw_referer(*_args_):
    
    
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
def wp_get_original_referer(*_args_):
    
    
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
def wp_mkdir_p(target_=None, *_args_):
    
    
    wrapper_ = None
    #// Strip the protocol.
    if wp_is_stream(target_):
        wrapper_, target_ = php_explode("://", target_, 2)
    # end if
    #// From php.net/mkdir user contributed notes.
    target_ = php_str_replace("//", "/", target_)
    #// Put the wrapper back on the target.
    if None != wrapper_:
        target_ = wrapper_ + "://" + target_
    # end if
    #// 
    #// Safe mode fails with a trailing slash under certain PHP versions.
    #// Use rtrim() instead of untrailingslashit to avoid formatting.php dependency.
    #//
    target_ = php_rtrim(target_, "/")
    if php_empty(lambda : target_):
        target_ = "/"
    # end if
    if php_file_exists(target_):
        return php_no_error(lambda: php_is_dir(target_))
    # end if
    #// Do not allow path traversals.
    if False != php_strpos(target_, "../") or False != php_strpos(target_, ".." + DIRECTORY_SEPARATOR):
        return False
    # end if
    #// We need to find the permissions of the parent folder that exists and inherit that.
    target_parent_ = php_dirname(target_)
    while True:
        
        if not ("." != target_parent_ and (not php_is_dir(target_parent_)) and php_dirname(target_parent_) != target_parent_):
            break
        # end if
        target_parent_ = php_dirname(target_parent_)
    # end while
    #// Get the permission bits.
    stat_ = php_no_error(lambda: stat(target_parent_))
    if stat_:
        dir_perms_ = stat_["mode"] & 4095
    else:
        dir_perms_ = 511
    # end if
    if php_no_error(lambda: mkdir(target_, dir_perms_, True)):
        #// 
        #// If a umask is set that modifies $dir_perms, we'll have to re-set
        #// the $dir_perms correctly with chmod()
        #//
        if dir_perms_ & (1 << (umask()).bit_length()) - 1 - umask() != dir_perms_:
            folder_parts_ = php_explode("/", php_substr(target_, php_strlen(target_parent_) + 1))
            i_ = 1
            c_ = php_count(folder_parts_)
            while i_ <= c_:
                
                chmod(target_parent_ + "/" + php_implode("/", php_array_slice(folder_parts_, 0, i_)), dir_perms_)
                i_ += 1
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
def path_is_absolute(path_=None, *_args_):
    
    
    #// 
    #// Check to see if the path is a stream and check to see if its an actual
    #// path or file as realpath() does not support stream wrappers.
    #//
    if wp_is_stream(path_) and php_is_dir(path_) or php_is_file(path_):
        return True
    # end if
    #// 
    #// This is definitive if true but fails if $path does not exist or contains
    #// a symbolic link.
    #//
    if php_realpath(path_) == path_:
        return True
    # end if
    if php_strlen(path_) == 0 or "." == path_[0]:
        return False
    # end if
    #// Windows allows absolute paths like this.
    if php_preg_match("#^[a-zA-Z]:\\\\#", path_):
        return True
    # end if
    #// A path starting with / or \ is absolute; anything else is relative.
    return "/" == path_[0] or "\\" == path_[0]
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
def path_join(base_=None, path_=None, *_args_):
    
    
    if path_is_absolute(path_):
        return path_
    # end if
    return php_rtrim(base_, "/") + "/" + php_ltrim(path_, "/")
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
def wp_normalize_path(path_=None, *_args_):
    
    
    wrapper_ = ""
    if wp_is_stream(path_):
        wrapper_, path_ = php_explode("://", path_, 2)
        wrapper_ += "://"
    # end if
    #// Standardise all paths to use '/'.
    path_ = php_str_replace("\\", "/", path_)
    #// Replace multiple slashes down to a singular, allowing for network shares having two slashes.
    path_ = php_preg_replace("|(?<=.)/+|", "/", path_)
    #// Windows paths should uppercase the drive letter.
    if ":" == php_substr(path_, 1, 1):
        path_ = ucfirst(path_)
    # end if
    return wrapper_ + path_
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
def get_temp_dir(*_args_):
    
    
    temp_ = ""
    if php_defined("WP_TEMP_DIR"):
        return trailingslashit(WP_TEMP_DIR)
    # end if
    if temp_:
        return trailingslashit(temp_)
    # end if
    if php_function_exists("sys_get_temp_dir"):
        temp_ = php_sys_get_temp_dir()
        if php_no_error(lambda: php_is_dir(temp_)) and wp_is_writable(temp_):
            return trailingslashit(temp_)
        # end if
    # end if
    temp_ = php_ini_get("upload_tmp_dir")
    if php_no_error(lambda: php_is_dir(temp_)) and wp_is_writable(temp_):
        return trailingslashit(temp_)
    # end if
    temp_ = WP_CONTENT_DIR + "/"
    if php_is_dir(temp_) and wp_is_writable(temp_):
        return temp_
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
def wp_is_writable(path_=None, *_args_):
    
    
    if "WIN" == php_strtoupper(php_substr(PHP_OS, 0, 3)):
        return win_is_writable(path_)
    else:
        return php_no_error(lambda: php_is_writable(path_))
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
def win_is_writable(path_=None, *_args_):
    
    
    if "/" == path_[php_strlen(path_) - 1]:
        #// If it looks like a directory, check a random file within the directory.
        return win_is_writable(path_ + php_uniqid(mt_rand()) + ".tmp")
    elif php_is_dir(path_):
        #// If it's a directory (and not a file), check a random file within the directory.
        return win_is_writable(path_ + "/" + php_uniqid(mt_rand()) + ".tmp")
    # end if
    #// Check tmp file for read/write capabilities.
    should_delete_tmp_file_ = (not php_file_exists(path_))
    f_ = php_no_error(lambda: fopen(path_, "a"))
    if False == f_:
        return False
    # end if
    php_fclose(f_)
    if should_delete_tmp_file_:
        unlink(path_)
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
def wp_get_upload_dir(*_args_):
    
    
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
def wp_upload_dir(time_=None, create_dir_=None, refresh_cache_=None, *_args_):
    if time_ is None:
        time_ = None
    # end if
    if create_dir_ is None:
        create_dir_ = True
    # end if
    if refresh_cache_ is None:
        refresh_cache_ = False
    # end if
    
    cache_ = Array()
    tested_paths_ = Array()
    key_ = php_sprintf("%d-%s", get_current_blog_id(), php_str(time_))
    if refresh_cache_ or php_empty(lambda : cache_[key_]):
        cache_[key_] = _wp_upload_dir(time_)
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
    uploads_ = apply_filters("upload_dir", cache_[key_])
    if create_dir_:
        path_ = uploads_["path"]
        if php_array_key_exists(path_, tested_paths_):
            uploads_["error"] = tested_paths_[path_]
        else:
            if (not wp_mkdir_p(path_)):
                if 0 == php_strpos(uploads_["basedir"], ABSPATH):
                    error_path_ = php_str_replace(ABSPATH, "", uploads_["basedir"]) + uploads_["subdir"]
                else:
                    error_path_ = wp_basename(uploads_["basedir"]) + uploads_["subdir"]
                # end if
                uploads_["error"] = php_sprintf(__("Unable to create directory %s. Is its parent directory writable by the server?"), esc_html(error_path_))
            # end if
            tested_paths_[path_] = uploads_["error"]
        # end if
    # end if
    return uploads_
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
def _wp_upload_dir(time_=None, *_args_):
    if time_ is None:
        time_ = None
    # end if
    
    siteurl_ = get_option("siteurl")
    upload_path_ = php_trim(get_option("upload_path"))
    if php_empty(lambda : upload_path_) or "wp-content/uploads" == upload_path_:
        dir_ = WP_CONTENT_DIR + "/uploads"
    elif 0 != php_strpos(upload_path_, ABSPATH):
        #// $dir is absolute, $upload_path is (maybe) relative to ABSPATH.
        dir_ = path_join(ABSPATH, upload_path_)
    else:
        dir_ = upload_path_
    # end if
    url_ = get_option("upload_url_path")
    if (not url_):
        if php_empty(lambda : upload_path_) or "wp-content/uploads" == upload_path_ or upload_path_ == dir_:
            url_ = WP_CONTENT_URL + "/uploads"
        else:
            url_ = trailingslashit(siteurl_) + upload_path_
        # end if
    # end if
    #// 
    #// Honor the value of UPLOADS. This happens as long as ms-files rewriting is disabled.
    #// We also sometimes obey UPLOADS when rewriting is enabled -- see the next block.
    #//
    if php_defined("UPLOADS") and (not is_multisite() and get_site_option("ms_files_rewriting")):
        dir_ = ABSPATH + UPLOADS
        url_ = trailingslashit(siteurl_) + UPLOADS
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
                ms_dir_ = "/sites/" + get_current_blog_id()
            else:
                ms_dir_ = "/" + get_current_blog_id()
            # end if
            dir_ += ms_dir_
            url_ += ms_dir_
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
                dir_ = untrailingslashit(BLOGUPLOADDIR)
            else:
                dir_ = ABSPATH + UPLOADS
            # end if
            url_ = trailingslashit(siteurl_) + "files"
        # end if
    # end if
    basedir_ = dir_
    baseurl_ = url_
    subdir_ = ""
    if get_option("uploads_use_yearmonth_folders"):
        #// Generate the yearly and monthly directories.
        if (not time_):
            time_ = current_time("mysql")
        # end if
        y_ = php_substr(time_, 0, 4)
        m_ = php_substr(time_, 5, 2)
        subdir_ = str("/") + str(y_) + str("/") + str(m_)
    # end if
    dir_ += subdir_
    url_ += subdir_
    return Array({"path": dir_, "url": url_, "subdir": subdir_, "basedir": basedir_, "baseurl": baseurl_, "error": False})
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
def wp_unique_filename(dir_=None, filename_=None, unique_filename_callback_=None, *_args_):
    if unique_filename_callback_ is None:
        unique_filename_callback_ = None
    # end if
    
    #// Sanitize the file name before we begin processing.
    filename_ = sanitize_file_name(filename_)
    ext2_ = None
    #// Separate the filename into a name and extension.
    ext_ = pathinfo(filename_, PATHINFO_EXTENSION)
    name_ = pathinfo(filename_, PATHINFO_BASENAME)
    if ext_:
        ext_ = "." + ext_
    # end if
    #// Edge case: if file is named '.ext', treat as an empty name.
    if name_ == ext_:
        name_ = ""
    # end if
    #// 
    #// Increment the file number until we have a unique file to save in $dir.
    #// Use callback if supplied.
    #//
    if unique_filename_callback_ and php_is_callable(unique_filename_callback_):
        filename_ = php_call_user_func(unique_filename_callback_, dir_, name_, ext_)
    else:
        number_ = ""
        fname_ = pathinfo(filename_, PATHINFO_FILENAME)
        #// Always append a number to file names that can potentially match image sub-size file names.
        if fname_ and php_preg_match("/-(?:\\d+x\\d+|scaled|rotated)$/", fname_):
            number_ = 1
            #// At this point the file name may not be unique. This is tested below and the $number is incremented.
            filename_ = php_str_replace(str(fname_) + str(ext_), str(fname_) + str("-") + str(number_) + str(ext_), filename_)
        # end if
        #// Change '.ext' to lower case.
        if ext_ and php_strtolower(ext_) != ext_:
            ext2_ = php_strtolower(ext_)
            filename2_ = php_preg_replace("|" + preg_quote(ext_) + "$|", ext2_, filename_)
            #// Check for both lower and upper case extension or image sub-sizes may be overwritten.
            while True:
                
                if not (php_file_exists(dir_ + str("/") + str(filename_)) or php_file_exists(dir_ + str("/") + str(filename2_))):
                    break
                # end if
                new_number_ = php_int(number_) + 1
                filename_ = php_str_replace(Array(str("-") + str(number_) + str(ext_), str(number_) + str(ext_)), str("-") + str(new_number_) + str(ext_), filename_)
                filename2_ = php_str_replace(Array(str("-") + str(number_) + str(ext2_), str(number_) + str(ext2_)), str("-") + str(new_number_) + str(ext2_), filename2_)
                number_ = new_number_
            # end while
            filename_ = filename2_
        else:
            while True:
                
                if not (php_file_exists(dir_ + str("/") + str(filename_))):
                    break
                # end if
                new_number_ = php_int(number_) + 1
                if "" == str(number_) + str(ext_):
                    filename_ = str(filename_) + str("-") + str(new_number_)
                else:
                    filename_ = php_str_replace(Array(str("-") + str(number_) + str(ext_), str(number_) + str(ext_)), str("-") + str(new_number_) + str(ext_), filename_)
                # end if
                number_ = new_number_
            # end while
        # end if
        #// Prevent collisions with existing file names that contain dimension-like strings
        #// (whether they are subsizes or originals uploaded prior to #42437).
        upload_dir_ = wp_get_upload_dir()
        #// The (resized) image files would have name and extension, and will be in the uploads dir.
        if name_ and ext_ and php_no_error(lambda: php_is_dir(dir_)) and False != php_strpos(dir_, upload_dir_["basedir"]):
            #// List of all files and directories contained in $dir.
            files_ = php_no_error(lambda: scandir(dir_))
            if (not php_empty(lambda : files_)):
                #// Remove "dot" dirs.
                files_ = php_array_diff(files_, Array(".", ".."))
            # end if
            if (not php_empty(lambda : files_)):
                #// The extension case may have changed above.
                new_ext_ = ext2_ if (not php_empty(lambda : ext2_)) else ext_
                #// Ensure this never goes into infinite loop
                #// as it uses pathinfo() and regex in the check, but string replacement for the changes.
                count_ = php_count(files_)
                i_ = 0
                while True:
                    
                    if not (i_ <= count_ and _wp_check_existing_file_names(filename_, files_)):
                        break
                    # end if
                    new_number_ = php_int(number_) + 1
                    filename_ = php_str_replace(Array(str("-") + str(number_) + str(new_ext_), str(number_) + str(new_ext_)), str("-") + str(new_number_) + str(new_ext_), filename_)
                    number_ = new_number_
                    i_ += 1
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
    return apply_filters("wp_unique_filename", filename_, ext_, dir_, unique_filename_callback_)
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
def _wp_check_existing_file_names(filename_=None, files_=None, *_args_):
    
    
    fname_ = pathinfo(filename_, PATHINFO_FILENAME)
    ext_ = pathinfo(filename_, PATHINFO_EXTENSION)
    #// Edge case, file names like `.ext`.
    if php_empty(lambda : fname_):
        return False
    # end if
    if ext_:
        ext_ = str(".") + str(ext_)
    # end if
    regex_ = "/^" + preg_quote(fname_) + "-(?:\\d+x\\d+|scaled|rotated)" + preg_quote(ext_) + "$/i"
    for file_ in files_:
        if php_preg_match(regex_, file_):
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
def wp_upload_bits(name_=None, deprecated_=None, bits_=None, time_=None, *_args_):
    if time_ is None:
        time_ = None
    # end if
    
    if (not php_empty(lambda : deprecated_)):
        _deprecated_argument(inspect.currentframe().f_code.co_name, "2.0.0")
    # end if
    if php_empty(lambda : name_):
        return Array({"error": __("Empty filename")})
    # end if
    wp_filetype_ = wp_check_filetype(name_)
    if (not wp_filetype_["ext"]) and (not current_user_can("unfiltered_upload")):
        return Array({"error": __("Sorry, this file type is not permitted for security reasons.")})
    # end if
    upload_ = wp_upload_dir(time_)
    if False != upload_["error"]:
        return upload_
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
    upload_bits_error_ = apply_filters("wp_upload_bits", Array({"name": name_, "bits": bits_, "time": time_}))
    if (not php_is_array(upload_bits_error_)):
        upload_["error"] = upload_bits_error_
        return upload_
    # end if
    filename_ = wp_unique_filename(upload_["path"], name_)
    new_file_ = upload_["path"] + str("/") + str(filename_)
    if (not wp_mkdir_p(php_dirname(new_file_))):
        if 0 == php_strpos(upload_["basedir"], ABSPATH):
            error_path_ = php_str_replace(ABSPATH, "", upload_["basedir"]) + upload_["subdir"]
        else:
            error_path_ = wp_basename(upload_["basedir"]) + upload_["subdir"]
        # end if
        message_ = php_sprintf(__("Unable to create directory %s. Is its parent directory writable by the server?"), error_path_)
        return Array({"error": message_})
    # end if
    ifp_ = php_no_error(lambda: fopen(new_file_, "wb"))
    if (not ifp_):
        return Array({"error": php_sprintf(__("Could not write file %s"), new_file_)})
    # end if
    fwrite(ifp_, bits_)
    php_fclose(ifp_)
    clearstatcache()
    #// Set correct file permissions.
    stat_ = php_no_error(lambda: stat(php_dirname(new_file_)))
    perms_ = stat_["mode"] & 4095
    perms_ = perms_ & 438
    chmod(new_file_, perms_)
    clearstatcache()
    #// Compute the URL.
    url_ = upload_["url"] + str("/") + str(filename_)
    #// This filter is documented in wp-admin/includes/file.php
    return apply_filters("wp_handle_upload", Array({"file": new_file_, "url": url_, "type": wp_filetype_["type"], "error": False}), "sideload")
# end def wp_upload_bits
#// 
#// Retrieve the file type based on the extension name.
#// 
#// @since 2.5.0
#// 
#// @param string $ext The extension to search.
#// @return string|void The file type, example: audio, video, document, spreadsheet, etc.
#//
def wp_ext2type(ext_=None, *_args_):
    
    
    ext_ = php_strtolower(ext_)
    ext2type_ = wp_get_ext_types()
    for type_,exts_ in ext2type_.items():
        if php_in_array(ext_, exts_):
            return type_
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
def wp_check_filetype(filename_=None, mimes_=None, *_args_):
    if mimes_ is None:
        mimes_ = None
    # end if
    
    if php_empty(lambda : mimes_):
        mimes_ = get_allowed_mime_types()
    # end if
    type_ = False
    ext_ = False
    for ext_preg_,mime_match_ in mimes_.items():
        ext_preg_ = "!\\.(" + ext_preg_ + ")$!i"
        if php_preg_match(ext_preg_, filename_, ext_matches_):
            type_ = mime_match_
            ext_ = ext_matches_[1]
            break
        # end if
    # end for
    return php_compact("ext_", "type_")
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
def wp_check_filetype_and_ext(file_=None, filename_=None, mimes_=None, *_args_):
    if mimes_ is None:
        mimes_ = None
    # end if
    
    proper_filename_ = False
    #// Do basic extension validation and MIME mapping.
    wp_filetype_ = wp_check_filetype(filename_, mimes_)
    ext_ = wp_filetype_["ext"]
    type_ = wp_filetype_["type"]
    #// We can't do any further validation without a file to work with.
    if (not php_file_exists(file_)):
        return php_compact("ext_", "type_", "proper_filename_")
    # end if
    real_mime_ = False
    #// Validate image types.
    if type_ and 0 == php_strpos(type_, "image/"):
        #// Attempt to figure out what type of image it actually is.
        real_mime_ = wp_get_image_mime(file_)
        if real_mime_ and real_mime_ != type_:
            #// 
            #// Filters the list mapping image mime types to their respective extensions.
            #// 
            #// @since 3.0.0
            #// 
            #// @param  array $mime_to_ext Array of image mime types and their matching extensions.
            #//
            mime_to_ext_ = apply_filters("getimagesize_mimes_to_exts", Array({"image/jpeg": "jpg", "image/png": "png", "image/gif": "gif", "image/bmp": "bmp", "image/tiff": "tif"}))
            #// Replace whatever is after the last period in the filename with the correct extension.
            if (not php_empty(lambda : mime_to_ext_[real_mime_])):
                filename_parts_ = php_explode(".", filename_)
                php_array_pop(filename_parts_)
                filename_parts_[-1] = mime_to_ext_[real_mime_]
                new_filename_ = php_implode(".", filename_parts_)
                if new_filename_ != filename_:
                    proper_filename_ = new_filename_
                    pass
                # end if
                #// Redefine the extension / MIME.
                wp_filetype_ = wp_check_filetype(new_filename_, mimes_)
                ext_ = wp_filetype_["ext"]
                type_ = wp_filetype_["type"]
            else:
                #// Reset $real_mime and try validating again.
                real_mime_ = False
            # end if
        # end if
    # end if
    #// Validate files that didn't get validated during previous checks.
    if type_ and (not real_mime_) and php_extension_loaded("fileinfo"):
        finfo_ = finfo_open(FILEINFO_MIME_TYPE)
        real_mime_ = finfo_file(finfo_, file_)
        finfo_close(finfo_)
        #// fileinfo often misidentifies obscure files as one of these types.
        nonspecific_types_ = Array("application/octet-stream", "application/encrypted", "application/CDFV2-encrypted", "application/zip")
        #// 
        #// If $real_mime doesn't match the content type we're expecting from the file's extension,
        #// we need to do some additional vetting. Media types and those listed in $nonspecific_types are
        #// allowed some leeway, but anything else must exactly match the real content type.
        #//
        if php_in_array(real_mime_, nonspecific_types_, True):
            #// File is a non-specific binary type. That's ok if it's a type that generally tends to be binary.
            if (not php_in_array(php_substr(type_, 0, strcspn(type_, "/")), Array("application", "video", "audio"))):
                type_ = False
                ext_ = False
            # end if
        elif 0 == php_strpos(real_mime_, "video/") or 0 == php_strpos(real_mime_, "audio/"):
            #// 
            #// For these types, only the major type must match the real value.
            #// This means that common mismatches are forgiven: application/vnd.apple.numbers is often misidentified as application/zip,
            #// and some media files are commonly named with the wrong extension (.mov instead of .mp4)
            #//
            if php_substr(real_mime_, 0, strcspn(real_mime_, "/")) != php_substr(type_, 0, strcspn(type_, "/")):
                type_ = False
                ext_ = False
            # end if
        elif "text/plain" == real_mime_:
            #// A few common file types are occasionally detected as text/plain; allow those.
            if (not php_in_array(type_, Array("text/plain", "text/csv", "text/richtext", "text/tsv", "text/vtt"))):
                type_ = False
                ext_ = False
            # end if
        elif "text/rtf" == real_mime_:
            #// Special casing for RTF files.
            if (not php_in_array(type_, Array("text/rtf", "text/plain", "application/rtf"))):
                type_ = False
                ext_ = False
            # end if
        else:
            if type_ != real_mime_:
                #// 
                #// Everything else including image/* and application/*:
                #// If the real content type doesn't match the file extension, assume it's dangerous.
                #//
                type_ = False
                ext_ = False
            # end if
        # end if
    # end if
    #// The mime type must be allowed.
    if type_:
        allowed_ = get_allowed_mime_types()
        if (not php_in_array(type_, allowed_)):
            type_ = False
            ext_ = False
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
    return apply_filters("wp_check_filetype_and_ext", php_compact("ext_", "type_", "proper_filename_"), file_, filename_, mimes_, real_mime_)
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
def wp_get_image_mime(file_=None, *_args_):
    
    
    #// 
    #// Use exif_imagetype() to check the mimetype if available or fall back to
    #// getimagesize() if exif isn't avaialbe. If either function throws an Exception
    #// we assume the file could not be validated.
    #//
    try: 
        if php_is_callable("exif_imagetype"):
            imagetype_ = exif_imagetype(file_)
            mime_ = image_type_to_mime_type(imagetype_) if imagetype_ else False
        elif php_function_exists("getimagesize"):
            imagesize_ = php_no_error(lambda: getimagesize(file_))
            mime_ = imagesize_["mime"] if (php_isset(lambda : imagesize_["mime"])) else False
        else:
            mime_ = False
        # end if
    except Exception as e_:
        mime_ = False
    # end try
    return mime_
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
def wp_get_mime_types(*_args_):
    
    
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
def wp_get_ext_types(*_args_):
    
    
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
def get_allowed_mime_types(user_=None, *_args_):
    if user_ is None:
        user_ = None
    # end if
    
    t_ = wp_get_mime_types()
    t_["swf"] = None
    t_["exe"] = None
    if php_function_exists("current_user_can"):
        unfiltered_ = user_can(user_, "unfiltered_html") if user_ else current_user_can("unfiltered_html")
    # end if
    if php_empty(lambda : unfiltered_):
        t_["htm|html"] = None
        t_["js"] = None
    # end if
    #// 
    #// Filters list of allowed mime types and file extensions.
    #// 
    #// @since 2.0.0
    #// 
    #// @param array            $t    Mime types keyed by the file extension regex corresponding to those types.
    #// @param int|WP_User|null $user User ID, User object or null if not provided (indicates current user).
    #//
    return apply_filters("upload_mimes", t_, user_)
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
def wp_nonce_ays(action_=None, *_args_):
    
    
    if "log-out" == action_:
        html_ = php_sprintf(__("You are attempting to log out of %s"), get_bloginfo("name"))
        html_ += "</p><p>"
        redirect_to_ = PHP_REQUEST["redirect_to"] if (php_isset(lambda : PHP_REQUEST["redirect_to"])) else ""
        html_ += php_sprintf(__("Do you really want to <a href=\"%s\">log out</a>?"), wp_logout_url(redirect_to_))
    else:
        html_ = __("The link you followed has expired.")
        if wp_get_referer():
            html_ += "</p><p>"
            html_ += php_sprintf("<a href=\"%s\">%s</a>", esc_url(remove_query_arg("updated", wp_get_referer())), __("Please try again."))
        # end if
    # end if
    wp_die(html_, __("Something went wrong."), 403)
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
def wp_die(message_="", title_="", args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    global wp_query_
    php_check_if_defined("wp_query_")
    if php_is_int(args_):
        args_ = Array({"response": args_})
    elif php_is_int(title_):
        args_ = Array({"response": title_})
        title_ = ""
    # end if
    if wp_doing_ajax():
        #// 
        #// Filters the callback for killing WordPress execution for Ajax requests.
        #// 
        #// @since 3.4.0
        #// 
        #// @param callable $function Callback function name.
        #//
        function_ = apply_filters("wp_die_ajax_handler", "_ajax_wp_die_handler")
    elif wp_is_json_request():
        #// 
        #// Filters the callback for killing WordPress execution for JSON requests.
        #// 
        #// @since 5.1.0
        #// 
        #// @param callable $function Callback function name.
        #//
        function_ = apply_filters("wp_die_json_handler", "_json_wp_die_handler")
    elif wp_is_jsonp_request():
        #// 
        #// Filters the callback for killing WordPress execution for JSONP requests.
        #// 
        #// @since 5.2.0
        #// 
        #// @param callable $function Callback function name.
        #//
        function_ = apply_filters("wp_die_jsonp_handler", "_jsonp_wp_die_handler")
    elif php_defined("XMLRPC_REQUEST") and XMLRPC_REQUEST:
        #// 
        #// Filters the callback for killing WordPress execution for XML-RPC requests.
        #// 
        #// @since 3.4.0
        #// 
        #// @param callable $function Callback function name.
        #//
        function_ = apply_filters("wp_die_xmlrpc_handler", "_xmlrpc_wp_die_handler")
    elif wp_is_xml_request() or (php_isset(lambda : wp_query_)) and php_function_exists("is_feed") and is_feed() or php_function_exists("is_comment_feed") and is_comment_feed() or php_function_exists("is_trackback") and is_trackback():
        #// 
        #// Filters the callback for killing WordPress execution for XML requests.
        #// 
        #// @since 5.2.0
        #// 
        #// @param callable $function Callback function name.
        #//
        function_ = apply_filters("wp_die_xml_handler", "_xml_wp_die_handler")
    else:
        #// 
        #// Filters the callback for killing WordPress execution for all non-Ajax, non-JSON, non-XML requests.
        #// 
        #// @since 3.0.0
        #// 
        #// @param callable $function Callback function name.
        #//
        function_ = apply_filters("wp_die_handler", "_default_wp_die_handler")
    # end if
    php_call_user_func(function_, message_, title_, args_)
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
def _default_wp_die_handler(message_=None, title_="", args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    message_, title_, parsed_args_ = _wp_die_process_input(message_, title_, args_)
    if php_is_string(message_):
        if (not php_empty(lambda : parsed_args_["additional_errors"])):
            message_ = php_array_merge(Array(message_), wp_list_pluck(parsed_args_["additional_errors"], "message"))
            message_ = "<ul>\n      <li>" + php_join("</li>\n       <li>", message_) + "</li>\n </ul>"
        # end if
        message_ = php_sprintf("<div class=\"wp-die-message\">%s</div>", message_)
    # end if
    have_gettext_ = php_function_exists("__")
    if (not php_empty(lambda : parsed_args_["link_url"])) and (not php_empty(lambda : parsed_args_["link_text"])):
        link_url_ = parsed_args_["link_url"]
        if php_function_exists("esc_url"):
            link_url_ = esc_url(link_url_)
        # end if
        link_text_ = parsed_args_["link_text"]
        message_ += str("\n<p><a href='") + str(link_url_) + str("'>") + str(link_text_) + str("</a></p>")
    # end if
    if (php_isset(lambda : parsed_args_["back_link"])) and parsed_args_["back_link"]:
        back_text_ = __("&laquo; Back") if have_gettext_ else "&laquo; Back"
        message_ += str("\n<p><a href='javascript:history.back()'>") + str(back_text_) + str("</a></p>")
    # end if
    if (not did_action("admin_head")):
        if (not php_headers_sent()):
            php_header(str("Content-Type: text/html; charset=") + str(parsed_args_["charset"]))
            status_header(parsed_args_["response"])
            nocache_headers()
        # end if
        text_direction_ = parsed_args_["text_direction"]
        if php_function_exists("language_attributes") and php_function_exists("is_rtl"):
            dir_attr_ = get_language_attributes()
        else:
            dir_attr_ = str("dir='") + str(text_direction_) + str("'")
        # end if
        php_print("<!DOCTYPE html>\n<html xmlns=\"http://www.w3.org/1999/xhtml\" ")
        php_print(dir_attr_)
        php_print(">\n<head>\n  <meta http-equiv=\"Content-Type\" content=\"text/html; charset=")
        php_print(parsed_args_["charset"])
        php_print("\" />\n  <meta name=\"viewport\" content=\"width=device-width\">\n       ")
        if php_function_exists("wp_no_robots"):
            wp_no_robots()
        # end if
        php_print(" <title>")
        php_print(title_)
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
        if "rtl" == text_direction_:
            php_print("body { font-family: Tahoma, Arial; }")
        # end if
        php_print("""   </style>
        </head>
        <body id=\"error-page\">
        """)
    # end if
    pass
    php_print(" ")
    php_print(message_)
    php_print("</body>\n</html>\n   ")
    if parsed_args_["exit"]:
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
def _ajax_wp_die_handler(message_=None, title_="", args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    #// Set default 'response' to 200 for AJAX requests.
    args_ = wp_parse_args(args_, Array({"response": 200}))
    message_, title_, parsed_args_ = _wp_die_process_input(message_, title_, args_)
    if (not php_headers_sent()):
        #// This is intentional. For backward-compatibility, support passing null here.
        if None != args_["response"]:
            status_header(parsed_args_["response"])
        # end if
        nocache_headers()
    # end if
    if php_is_scalar(message_):
        message_ = php_str(message_)
    else:
        message_ = "0"
    # end if
    if parsed_args_["exit"]:
        php_print(message_)
        php_exit()
    # end if
    php_print(message_)
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
def _json_wp_die_handler(message_=None, title_="", args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    message_, title_, parsed_args_ = _wp_die_process_input(message_, title_, args_)
    data_ = Array({"code": parsed_args_["code"], "message": message_, "data": Array({"status": parsed_args_["response"]})}, {"additional_errors": parsed_args_["additional_errors"]})
    if (not php_headers_sent()):
        php_header(str("Content-Type: application/json; charset=") + str(parsed_args_["charset"]))
        if None != parsed_args_["response"]:
            status_header(parsed_args_["response"])
        # end if
        nocache_headers()
    # end if
    php_print(wp_json_encode(data_))
    if parsed_args_["exit"]:
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
def _jsonp_wp_die_handler(message_=None, title_="", args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    message_, title_, parsed_args_ = _wp_die_process_input(message_, title_, args_)
    data_ = Array({"code": parsed_args_["code"], "message": message_, "data": Array({"status": parsed_args_["response"]})}, {"additional_errors": parsed_args_["additional_errors"]})
    if (not php_headers_sent()):
        php_header(str("Content-Type: application/javascript; charset=") + str(parsed_args_["charset"]))
        php_header("X-Content-Type-Options: nosniff")
        php_header("X-Robots-Tag: noindex")
        if None != parsed_args_["response"]:
            status_header(parsed_args_["response"])
        # end if
        nocache_headers()
    # end if
    result_ = wp_json_encode(data_)
    jsonp_callback_ = PHP_REQUEST["_jsonp"]
    php_print("/**/" + jsonp_callback_ + "(" + result_ + ")")
    if parsed_args_["exit"]:
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
def _xmlrpc_wp_die_handler(message_=None, title_="", args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    global wp_xmlrpc_server_
    php_check_if_defined("wp_xmlrpc_server_")
    message_, title_, parsed_args_ = _wp_die_process_input(message_, title_, args_)
    if (not php_headers_sent()):
        nocache_headers()
    # end if
    if wp_xmlrpc_server_:
        error_ = php_new_class("IXR_Error", lambda : IXR_Error(parsed_args_["response"], message_))
        wp_xmlrpc_server_.output(error_.getxml())
    # end if
    if parsed_args_["exit"]:
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
def _xml_wp_die_handler(message_=None, title_="", args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    message_, title_, parsed_args_ = _wp_die_process_input(message_, title_, args_)
    message_ = php_htmlspecialchars(message_)
    title_ = php_htmlspecialchars(title_)
    xml_ = str("<error>\n    <code>") + str(parsed_args_["code"]) + str("</code>\n    <title><![CDATA[") + str(title_) + str("]]></title>\n    <message><![CDATA[") + str(message_) + str("]]></message>\n    <data>\n        <status>") + str(parsed_args_["response"]) + str("""</status>\n    </data>\n</error>\n""")
    if (not php_headers_sent()):
        php_header(str("Content-Type: text/xml; charset=") + str(parsed_args_["charset"]))
        if None != parsed_args_["response"]:
            status_header(parsed_args_["response"])
        # end if
        nocache_headers()
    # end if
    php_print(xml_)
    if parsed_args_["exit"]:
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
def _scalar_wp_die_handler(message_="", title_="", args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    message_, title_, parsed_args_ = _wp_die_process_input(message_, title_, args_)
    if parsed_args_["exit"]:
        if php_is_scalar(message_):
            php_print(php_str(message_))
            php_exit()
        # end if
        php_exit(0)
    # end if
    if php_is_scalar(message_):
        php_print(php_str(message_))
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
def _wp_die_process_input(message_=None, title_="", args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    defaults_ = Array({"response": 0, "code": "", "exit": True, "back_link": False, "link_url": "", "link_text": "", "text_direction": "", "charset": "utf-8", "additional_errors": Array()})
    args_ = wp_parse_args(args_, defaults_)
    if php_function_exists("is_wp_error") and is_wp_error(message_):
        if (not php_empty(lambda : message_.errors)):
            errors_ = Array()
            for error_code_,error_messages_ in message_.errors.items():
                for error_message_ in error_messages_:
                    errors_[-1] = Array({"code": error_code_, "message": error_message_, "data": message_.get_error_data(error_code_)})
                # end for
            # end for
            message_ = errors_[0]["message"]
            if php_empty(lambda : args_["code"]):
                args_["code"] = errors_[0]["code"]
            # end if
            if php_empty(lambda : args_["response"]) and php_is_array(errors_[0]["data"]) and (not php_empty(lambda : errors_[0]["data"]["status"])):
                args_["response"] = errors_[0]["data"]["status"]
            # end if
            if php_empty(lambda : title_) and php_is_array(errors_[0]["data"]) and (not php_empty(lambda : errors_[0]["data"]["title"])):
                title_ = errors_[0]["data"]["title"]
            # end if
            errors_[0] = None
            args_["additional_errors"] = php_array_values(errors_)
        else:
            message_ = ""
        # end if
    # end if
    have_gettext_ = php_function_exists("__")
    #// The $title and these specific $args must always have a non-empty value.
    if php_empty(lambda : args_["code"]):
        args_["code"] = "wp_die"
    # end if
    if php_empty(lambda : args_["response"]):
        args_["response"] = 500
    # end if
    if php_empty(lambda : title_):
        title_ = __("WordPress &rsaquo; Error") if have_gettext_ else "WordPress &rsaquo; Error"
    # end if
    if php_empty(lambda : args_["text_direction"]) or (not php_in_array(args_["text_direction"], Array("ltr", "rtl"), True)):
        args_["text_direction"] = "ltr"
        if php_function_exists("is_rtl") and is_rtl():
            args_["text_direction"] = "rtl"
        # end if
    # end if
    if (not php_empty(lambda : args_["charset"])):
        args_["charset"] = _canonical_charset(args_["charset"])
    # end if
    return Array(message_, title_, args_)
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
def wp_json_encode(data_=None, options_=0, depth_=512, *_args_):
    
    
    json_ = php_json_encode(data_, options_, depth_)
    #// If json_encode() was successful, no need to do more sanity checking.
    if False != json_:
        return json_
    # end if
    try: 
        data_ = _wp_json_sanity_check(data_, depth_)
    except Exception as e_:
        return False
    # end try
    return php_json_encode(data_, options_, depth_)
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
def _wp_json_sanity_check(data_=None, depth_=None, *_args_):
    
    
    if depth_ < 0:
        raise php_new_class("Exception", lambda : Exception("Reached depth limit"))
    # end if
    if php_is_array(data_):
        output_ = Array()
        for id_,el_ in data_.items():
            #// Don't forget to sanitize the ID!
            if php_is_string(id_):
                clean_id_ = _wp_json_convert_string(id_)
            else:
                clean_id_ = id_
            # end if
            #// Check the element type, so that we're only recursing if we really have to.
            if php_is_array(el_) or php_is_object(el_):
                output_[clean_id_] = _wp_json_sanity_check(el_, depth_ - 1)
            elif php_is_string(el_):
                output_[clean_id_] = _wp_json_convert_string(el_)
            else:
                output_[clean_id_] = el_
            # end if
        # end for
    elif php_is_object(data_):
        output_ = php_new_class("stdClass", lambda : stdClass())
        for id_,el_ in data_.items():
            if php_is_string(id_):
                clean_id_ = _wp_json_convert_string(id_)
            else:
                clean_id_ = id_
            # end if
            if php_is_array(el_) or php_is_object(el_):
                output_.clean_id_ = _wp_json_sanity_check(el_, depth_ - 1)
            elif php_is_string(el_):
                output_.clean_id_ = _wp_json_convert_string(el_)
            else:
                output_.clean_id_ = el_
            # end if
        # end for
    elif php_is_string(data_):
        return _wp_json_convert_string(data_)
    else:
        return data_
    # end if
    return output_
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
def _wp_json_convert_string(string_=None, *_args_):
    
    
    use_mb_ = None
    if php_is_null(use_mb_):
        use_mb_ = php_function_exists("mb_convert_encoding")
    # end if
    if use_mb_:
        encoding_ = mb_detect_encoding(string_, mb_detect_order(), True)
        if encoding_:
            return mb_convert_encoding(string_, "UTF-8", encoding_)
        else:
            return mb_convert_encoding(string_, "UTF-8", "UTF-8")
        # end if
    else:
        return wp_check_invalid_utf8(string_, True)
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
def _wp_json_prepare_data(data_=None, *_args_):
    
    
    _deprecated_function(inspect.currentframe().f_code.co_name, "5.3.0")
    return data_
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
def wp_send_json(response_=None, status_code_=None, *_args_):
    if status_code_ is None:
        status_code_ = None
    # end if
    
    if (not php_headers_sent()):
        php_header("Content-Type: application/json; charset=" + get_option("blog_charset"))
        if None != status_code_:
            status_header(status_code_)
        # end if
    # end if
    php_print(wp_json_encode(response_))
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
def wp_send_json_success(data_=None, status_code_=None, *_args_):
    if data_ is None:
        data_ = None
    # end if
    if status_code_ is None:
        status_code_ = None
    # end if
    
    response_ = Array({"success": True})
    if (php_isset(lambda : data_)):
        response_["data"] = data_
    # end if
    wp_send_json(response_, status_code_)
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
def wp_send_json_error(data_=None, status_code_=None, *_args_):
    if data_ is None:
        data_ = None
    # end if
    if status_code_ is None:
        status_code_ = None
    # end if
    
    response_ = Array({"success": False})
    if (php_isset(lambda : data_)):
        if is_wp_error(data_):
            result_ = Array()
            for code_,messages_ in data_.errors.items():
                for message_ in messages_:
                    result_[-1] = Array({"code": code_, "message": message_})
                # end for
            # end for
            response_["data"] = result_
        else:
            response_["data"] = data_
        # end if
    # end if
    wp_send_json(response_, status_code_)
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
def wp_check_jsonp_callback(callback_=None, *_args_):
    
    
    if (not php_is_string(callback_)):
        return False
    # end if
    php_preg_replace("/[^\\w\\.]/", "", callback_, -1, illegal_char_count_)
    return 0 == illegal_char_count_
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
def _config_wp_home(url_="", *_args_):
    
    
    if php_defined("WP_HOME"):
        return untrailingslashit(WP_HOME)
    # end if
    return url_
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
def _config_wp_siteurl(url_="", *_args_):
    
    
    if php_defined("WP_SITEURL"):
        return untrailingslashit(WP_SITEURL)
    # end if
    return url_
# end def _config_wp_siteurl
#// 
#// Delete the fresh site option.
#// 
#// @since 4.7.0
#// @access private
#//
def _delete_option_fresh_site(*_args_):
    
    
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
def _mce_set_direction(mce_init_=None, *_args_):
    
    
    if is_rtl():
        mce_init_["directionality"] = "rtl"
        mce_init_["rtl_ui"] = True
        if (not php_empty(lambda : mce_init_["plugins"])) and php_strpos(mce_init_["plugins"], "directionality") == False:
            mce_init_["plugins"] += ",directionality"
        # end if
        if (not php_empty(lambda : mce_init_["toolbar1"])) and (not php_preg_match("/\\bltr\\b/", mce_init_["toolbar1"])):
            mce_init_["toolbar1"] += ",ltr"
        # end if
    # end if
    return mce_init_
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
def smilies_init(*_args_):
    
    
    global wpsmiliestrans_
    global wp_smiliessearch_
    php_check_if_defined("wpsmiliestrans_","wp_smiliessearch_")
    #// Don't bother setting up smilies if they are disabled.
    if (not get_option("use_smilies")):
        return
    # end if
    if (not (php_isset(lambda : wpsmiliestrans_))):
        wpsmiliestrans_ = Array({":mrgreen:": "mrgreen.png", ":neutral:": "ð", ":twisted:": "ð", ":arrow:": "â¡", ":shock:": "ð¯", ":smile:": "ð", ":???:": "ð", ":cool:": "ð", ":evil:": "ð¿", ":grin:": "ð", ":idea:": "ð¡", ":oops:": "ð³", ":razz:": "ð", ":roll:": "ð", ":wink:": "ð", ":cry:": "ð¥", ":eek:": "ð®", ":lol:": "ð", ":mad:": "ð¡", ":sad:": "ð", "8-)": "ð", "8-O": "ð¯", ":-(": "ð", ":-)": "ð", ":-?": "ð", ":-D": "ð", ":-P": "ð", ":-o": "ð®", ":-x": "ð¡", ":-|": "ð", ";-)": "ð", "8O": "ð¯", ":(": "ð", ":)": "ð", ":?": "ð", ":D": "ð", ":P": "ð", ":o": "ð®", ":x": "ð¡", ":|": "ð", ";)": "ð", ":!:": "â", ":?:": "â"})
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
    wpsmiliestrans_ = apply_filters("smilies", wpsmiliestrans_)
    if php_count(wpsmiliestrans_) == 0:
        return
    # end if
    #// 
    #// NOTE: we sort the smilies in reverse key order. This is to make sure
    #// we match the longest possible smilie (:???: vs :?) as the regular
    #// expression used below is first-match
    #//
    krsort(wpsmiliestrans_)
    spaces_ = wp_spaces_regexp()
    #// Begin first "subpattern".
    wp_smiliessearch_ = "/(?<=" + spaces_ + "|^)"
    subchar_ = ""
    for smiley_,img_ in wpsmiliestrans_.items():
        firstchar_ = php_substr(smiley_, 0, 1)
        rest_ = php_substr(smiley_, 1)
        #// New subpattern?
        if firstchar_ != subchar_:
            if "" != subchar_:
                wp_smiliessearch_ += ")(?=" + spaces_ + "|$)"
                #// End previous "subpattern".
                wp_smiliessearch_ += "|(?<=" + spaces_ + "|^)"
                pass
            # end if
            subchar_ = firstchar_
            wp_smiliessearch_ += preg_quote(firstchar_, "/") + "(?:"
        else:
            wp_smiliessearch_ += "|"
        # end if
        wp_smiliessearch_ += preg_quote(rest_, "/")
    # end for
    wp_smiliessearch_ += ")(?=" + spaces_ + "|$)/m"
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
def wp_parse_args(args_=None, defaults_="", *_args_):
    
    
    if php_is_object(args_):
        parsed_args_ = get_object_vars(args_)
    elif php_is_array(args_):
        parsed_args_ = args_
    else:
        wp_parse_str(args_, parsed_args_)
    # end if
    if php_is_array(defaults_):
        return php_array_merge(defaults_, parsed_args_)
    # end if
    return parsed_args_
# end def wp_parse_args
#// 
#// Cleans up an array, comma- or space-separated list of scalar values.
#// 
#// @since 5.1.0
#// 
#// @param array|string $list List of values.
#// @return array Sanitized array of values.
#//
def wp_parse_list(list_=None, *_args_):
    
    
    if (not php_is_array(list_)):
        return php_preg_split("/[\\s,]+/", list_, -1, PREG_SPLIT_NO_EMPTY)
    # end if
    return list_
# end def wp_parse_list
#// 
#// Clean up an array, comma- or space-separated list of IDs.
#// 
#// @since 3.0.0
#// 
#// @param array|string $list List of ids.
#// @return int[] Sanitized array of IDs.
#//
def wp_parse_id_list(list_=None, *_args_):
    
    
    list_ = wp_parse_list(list_)
    return array_unique(php_array_map("absint", list_))
# end def wp_parse_id_list
#// 
#// Clean up an array, comma- or space-separated list of slugs.
#// 
#// @since 4.7.0
#// 
#// @param  array|string $list List of slugs.
#// @return string[] Sanitized array of slugs.
#//
def wp_parse_slug_list(list_=None, *_args_):
    
    
    list_ = wp_parse_list(list_)
    return array_unique(php_array_map("sanitize_title", list_))
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
def wp_array_slice_assoc(array_=None, keys_=None, *_args_):
    
    
    slice_ = Array()
    for key_ in keys_:
        if (php_isset(lambda : array_[key_])):
            slice_[key_] = array_[key_]
        # end if
    # end for
    return slice_
# end def wp_array_slice_assoc
#// 
#// Determines if the variable is a numeric-indexed array.
#// 
#// @since 4.4.0
#// 
#// @param mixed $data Variable to check.
#// @return bool Whether the variable is a list.
#//
def wp_is_numeric_array(data_=None, *_args_):
    
    
    if (not php_is_array(data_)):
        return False
    # end if
    keys_ = php_array_keys(data_)
    string_keys_ = php_array_filter(keys_, "is_string")
    return php_count(string_keys_) == 0
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
def wp_filter_object_list(list_=None, args_=None, operator_="and", field_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    if field_ is None:
        field_ = False
    # end if
    
    if (not php_is_array(list_)):
        return Array()
    # end if
    util_ = php_new_class("WP_List_Util", lambda : WP_List_Util(list_))
    util_.filter(args_, operator_)
    if field_:
        util_.pluck(field_)
    # end if
    return util_.get_output()
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
def wp_list_filter(list_=None, args_=None, operator_="AND", *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    if (not php_is_array(list_)):
        return Array()
    # end if
    util_ = php_new_class("WP_List_Util", lambda : WP_List_Util(list_))
    return util_.filter(args_, operator_)
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
def wp_list_pluck(list_=None, field_=None, index_key_=None, *_args_):
    if index_key_ is None:
        index_key_ = None
    # end if
    
    util_ = php_new_class("WP_List_Util", lambda : WP_List_Util(list_))
    return util_.pluck(field_, index_key_)
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
def wp_list_sort(list_=None, orderby_=None, order_="ASC", preserve_keys_=None, *_args_):
    if orderby_ is None:
        orderby_ = Array()
    # end if
    if preserve_keys_ is None:
        preserve_keys_ = False
    # end if
    
    if (not php_is_array(list_)):
        return Array()
    # end if
    util_ = php_new_class("WP_List_Util", lambda : WP_List_Util(list_))
    return util_.sort(orderby_, order_, preserve_keys_)
# end def wp_list_sort
#// 
#// Determines if Widgets library should be loaded.
#// 
#// Checks to make sure that the widgets library hasn't already been loaded.
#// If it hasn't, then it will load the widgets library and run an action hook.
#// 
#// @since 2.2.0
#//
def wp_maybe_load_widgets(*_args_):
    
    
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
def wp_widgets_add_menu(*_args_):
    
    
    global submenu_
    php_check_if_defined("submenu_")
    if (not current_theme_supports("widgets")):
        return
    # end if
    submenu_["themes.php"][7] = Array(__("Widgets"), "edit_theme_options", "widgets.php")
    php_ksort(submenu_["themes.php"], SORT_NUMERIC)
# end def wp_widgets_add_menu
#// 
#// Flush all output buffers for PHP 5.2.
#// 
#// Make sure all output buffers are flushed before our singletons are destroyed.
#// 
#// @since 2.2.0
#//
def wp_ob_end_flush_all(*_args_):
    
    
    levels_ = ob_get_level()
    i_ = 0
    while i_ < levels_:
        
        ob_end_flush()
        i_ += 1
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
def dead_db(*_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    wp_load_translations_early()
    #// Load custom DB error template, if present.
    if php_file_exists(WP_CONTENT_DIR + "/db-error.php"):
        php_include_file(WP_CONTENT_DIR + "/db-error.php", once=True)
        php_exit(0)
    # end if
    #// If installing or in the admin, provide the verbose message.
    if wp_installing() or php_defined("WP_ADMIN"):
        wp_die(wpdb_.error)
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
def absint(maybeint_=None, *_args_):
    
    
    return abs(php_intval(maybeint_))
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
def _deprecated_function(function_=None, version_=None, replacement_=None, *_args_):
    if replacement_ is None:
        replacement_ = None
    # end if
    
    #// 
    #// Fires when a deprecated function is called.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $function    The function that was called.
    #// @param string $replacement The function that should have been called.
    #// @param string $version     The version of WordPress that deprecated the function.
    #//
    do_action("deprecated_function_run", function_, replacement_, version_)
    #// 
    #// Filters whether to trigger an error for deprecated functions.
    #// 
    #// @since 2.5.0
    #// 
    #// @param bool $trigger Whether to trigger the error for deprecated functions. Default true.
    #//
    if WP_DEBUG and apply_filters("deprecated_function_trigger_error", True):
        if php_function_exists("__"):
            if (not php_is_null(replacement_)):
                trigger_error(php_sprintf(__("%1$s is <strong>deprecated</strong> since version %2$s! Use %3$s instead."), function_, version_, replacement_), E_USER_DEPRECATED)
            else:
                trigger_error(php_sprintf(__("%1$s is <strong>deprecated</strong> since version %2$s with no alternative available."), function_, version_), E_USER_DEPRECATED)
            # end if
        else:
            if (not php_is_null(replacement_)):
                trigger_error(php_sprintf("%1$s is <strong>deprecated</strong> since version %2$s! Use %3$s instead.", function_, version_, replacement_), E_USER_DEPRECATED)
            else:
                trigger_error(php_sprintf("%1$s is <strong>deprecated</strong> since version %2$s with no alternative available.", function_, version_), E_USER_DEPRECATED)
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
def _deprecated_constructor(class_=None, version_=None, parent_class_="", *_args_):
    
    
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
    do_action("deprecated_constructor_run", class_, version_, parent_class_)
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
            if (not php_empty(lambda : parent_class_)):
                trigger_error(php_sprintf(__("The called constructor method for %1$s in %2$s is <strong>deprecated</strong> since version %3$s! Use %4$s instead."), class_, parent_class_, version_, "<code>__construct()</code>"), E_USER_DEPRECATED)
            else:
                trigger_error(php_sprintf(__("The called constructor method for %1$s is <strong>deprecated</strong> since version %2$s! Use %3$s instead."), class_, version_, "<code>__construct()</code>"), E_USER_DEPRECATED)
            # end if
        else:
            if (not php_empty(lambda : parent_class_)):
                trigger_error(php_sprintf("The called constructor method for %1$s in %2$s is <strong>deprecated</strong> since version %3$s! Use %4$s instead.", class_, parent_class_, version_, "<code>__construct()</code>"), E_USER_DEPRECATED)
            else:
                trigger_error(php_sprintf("The called constructor method for %1$s is <strong>deprecated</strong> since version %2$s! Use %3$s instead.", class_, version_, "<code>__construct()</code>"), E_USER_DEPRECATED)
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
def _deprecated_file(file_=None, version_=None, replacement_=None, message_="", *_args_):
    if replacement_ is None:
        replacement_ = None
    # end if
    
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
    do_action("deprecated_file_included", file_, replacement_, version_, message_)
    #// 
    #// Filters whether to trigger an error for deprecated files.
    #// 
    #// @since 2.5.0
    #// 
    #// @param bool $trigger Whether to trigger the error for deprecated files. Default true.
    #//
    if WP_DEBUG and apply_filters("deprecated_file_trigger_error", True):
        message_ = "" if php_empty(lambda : message_) else " " + message_
        if php_function_exists("__"):
            if (not php_is_null(replacement_)):
                trigger_error(php_sprintf(__("%1$s is <strong>deprecated</strong> since version %2$s! Use %3$s instead."), file_, version_, replacement_) + message_, E_USER_DEPRECATED)
            else:
                trigger_error(php_sprintf(__("%1$s is <strong>deprecated</strong> since version %2$s with no alternative available."), file_, version_) + message_, E_USER_DEPRECATED)
            # end if
        else:
            if (not php_is_null(replacement_)):
                trigger_error(php_sprintf("%1$s is <strong>deprecated</strong> since version %2$s! Use %3$s instead.", file_, version_, replacement_) + message_, E_USER_DEPRECATED)
            else:
                trigger_error(php_sprintf("%1$s is <strong>deprecated</strong> since version %2$s with no alternative available.", file_, version_) + message_, E_USER_DEPRECATED)
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
def _deprecated_argument(function_=None, version_=None, message_=None, *_args_):
    if message_ is None:
        message_ = None
    # end if
    
    #// 
    #// Fires when a deprecated argument is called.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string $function The function that was called.
    #// @param string $message  A message regarding the change.
    #// @param string $version  The version of WordPress that deprecated the argument used.
    #//
    do_action("deprecated_argument_run", function_, message_, version_)
    #// 
    #// Filters whether to trigger an error for deprecated arguments.
    #// 
    #// @since 3.0.0
    #// 
    #// @param bool $trigger Whether to trigger the error for deprecated arguments. Default true.
    #//
    if WP_DEBUG and apply_filters("deprecated_argument_trigger_error", True):
        if php_function_exists("__"):
            if (not php_is_null(message_)):
                trigger_error(php_sprintf(__("%1$s was called with an argument that is <strong>deprecated</strong> since version %2$s! %3$s"), function_, version_, message_), E_USER_DEPRECATED)
            else:
                trigger_error(php_sprintf(__("%1$s was called with an argument that is <strong>deprecated</strong> since version %2$s with no alternative available."), function_, version_), E_USER_DEPRECATED)
            # end if
        else:
            if (not php_is_null(message_)):
                trigger_error(php_sprintf("%1$s was called with an argument that is <strong>deprecated</strong> since version %2$s! %3$s", function_, version_, message_), E_USER_DEPRECATED)
            else:
                trigger_error(php_sprintf("%1$s was called with an argument that is <strong>deprecated</strong> since version %2$s with no alternative available.", function_, version_), E_USER_DEPRECATED)
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
def _deprecated_hook(hook_=None, version_=None, replacement_=None, message_=None, *_args_):
    if replacement_ is None:
        replacement_ = None
    # end if
    if message_ is None:
        message_ = None
    # end if
    
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
    do_action("deprecated_hook_run", hook_, replacement_, version_, message_)
    #// 
    #// Filters whether to trigger deprecated hook errors.
    #// 
    #// @since 4.6.0
    #// 
    #// @param bool $trigger Whether to trigger deprecated hook errors. Requires
    #// `WP_DEBUG` to be defined true.
    #//
    if WP_DEBUG and apply_filters("deprecated_hook_trigger_error", True):
        message_ = "" if php_empty(lambda : message_) else " " + message_
        if (not php_is_null(replacement_)):
            trigger_error(php_sprintf(__("%1$s is <strong>deprecated</strong> since version %2$s! Use %3$s instead."), hook_, version_, replacement_) + message_, E_USER_DEPRECATED)
        else:
            trigger_error(php_sprintf(__("%1$s is <strong>deprecated</strong> since version %2$s with no alternative available."), hook_, version_) + message_, E_USER_DEPRECATED)
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
def _doing_it_wrong(function_=None, message_=None, version_=None, *_args_):
    
    
    #// 
    #// Fires when the given function is being used incorrectly.
    #// 
    #// @since 3.1.0
    #// 
    #// @param string $function The function that was called.
    #// @param string $message  A message explaining what has been done incorrectly.
    #// @param string $version  The version of WordPress where the message was added.
    #//
    do_action("doing_it_wrong_run", function_, message_, version_)
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
    if WP_DEBUG and apply_filters("doing_it_wrong_trigger_error", True, function_, message_, version_):
        if php_function_exists("__"):
            if php_is_null(version_):
                version_ = ""
            else:
                #// translators: %s: Version number.
                version_ = php_sprintf(__("(This message was added in version %s.)"), version_)
            # end if
            message_ += " " + php_sprintf(__("Please see <a href=\"%s\">Debugging in WordPress</a> for more information."), __("https://wordpress.org/support/article/debugging-in-wordpress/"))
            trigger_error(php_sprintf(__("%1$s was called <strong>incorrectly</strong>. %2$s %3$s"), function_, message_, version_), E_USER_NOTICE)
        else:
            if php_is_null(version_):
                version_ = ""
            else:
                version_ = php_sprintf("(This message was added in version %s.)", version_)
            # end if
            message_ += php_sprintf(" Please see <a href=\"%s\">Debugging in WordPress</a> for more information.", "https://wordpress.org/support/article/debugging-in-wordpress/")
            trigger_error(php_sprintf("%1$s was called <strong>incorrectly</strong>. %2$s %3$s", function_, message_, version_), E_USER_NOTICE)
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
def is_lighttpd_before_150(*_args_):
    
    
    server_parts_ = php_explode("/", PHP_SERVER["SERVER_SOFTWARE"] if (php_isset(lambda : PHP_SERVER["SERVER_SOFTWARE"])) else "")
    server_parts_[1] = server_parts_[1] if (php_isset(lambda : server_parts_[1])) else ""
    return "lighttpd" == server_parts_[0] and -1 == php_version_compare(server_parts_[1], "1.5.0")
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
def apache_mod_loaded(mod_=None, default_=None, *_args_):
    if default_ is None:
        default_ = False
    # end if
    
    global is_apache_
    php_check_if_defined("is_apache_")
    if (not is_apache_):
        return False
    # end if
    if php_function_exists("apache_get_modules"):
        mods_ = apache_get_modules()
        if php_in_array(mod_, mods_):
            return True
        # end if
    elif php_function_exists("phpinfo") and False == php_strpos(php_ini_get("disable_functions"), "phpinfo"):
        ob_start()
        phpinfo(8)
        phpinfo_ = ob_get_clean()
        if False != php_strpos(phpinfo_, mod_):
            return True
        # end if
    # end if
    return default_
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
def iis7_supports_permalinks(*_args_):
    
    
    global is_iis7_
    php_check_if_defined("is_iis7_")
    supports_permalinks_ = False
    if is_iis7_:
        #// First we check if the DOMDocument class exists. If it does not exist, then we cannot
        #// easily update the xml configuration file, hence we just bail out and tell user that
        #// pretty permalinks cannot be used.
        #// 
        #// Next we check if the URL Rewrite Module 1.1 is loaded and enabled for the web site. When
        #// URL Rewrite 1.1 is loaded it always sets a server variable called 'IIS_UrlRewriteModule'.
        #// Lastly we make sure that PHP is running via FastCGI. This is important because if it runs
        #// via ISAPI then pretty permalinks will not work.
        #//
        supports_permalinks_ = php_class_exists("DOMDocument", False) and (php_isset(lambda : PHP_SERVER["IIS_UrlRewriteModule"])) and PHP_SAPI == "cgi-fcgi"
    # end if
    #// 
    #// Filters whether IIS 7+ supports pretty permalinks.
    #// 
    #// @since 2.8.0
    #// 
    #// @param bool $supports_permalinks Whether IIS7 supports permalinks. Default false.
    #//
    return apply_filters("iis7_supports_permalinks", supports_permalinks_)
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
def validate_file(file_=None, allowed_files_=None, *_args_):
    if allowed_files_ is None:
        allowed_files_ = Array()
    # end if
    
    #// `../` on its own is not allowed:
    if "../" == file_:
        return 1
    # end if
    #// More than one occurence of `../` is not allowed:
    if preg_match_all("#\\.\\./#", file_, matches_, PREG_SET_ORDER) and php_count(matches_) > 1:
        return 1
    # end if
    #// `../` which does not occur at the end of the path is not allowed:
    if False != php_strpos(file_, "../") and "../" != php_mb_substr(file_, -3, 3):
        return 1
    # end if
    #// Files not in the allowed file list are not allowed:
    if (not php_empty(lambda : allowed_files_)) and (not php_in_array(file_, allowed_files_)):
        return 3
    # end if
    #// Absolute Windows drive paths are not allowed:
    if ":" == php_substr(file_, 1, 1):
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
def force_ssl_admin(force_=None, *_args_):
    if force_ is None:
        force_ = None
    # end if
    
    forced_ = False
    if (not php_is_null(force_)):
        old_forced_ = forced_
        forced_ = force_
        return old_forced_
    # end if
    return forced_
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
def wp_guess_url(*_args_):
    
    
    if php_defined("WP_SITEURL") and "" != WP_SITEURL:
        url_ = WP_SITEURL
    else:
        abspath_fix_ = php_str_replace("\\", "/", ABSPATH)
        script_filename_dir_ = php_dirname(PHP_SERVER["SCRIPT_FILENAME"])
        #// The request is for the admin.
        if php_strpos(PHP_SERVER["REQUEST_URI"], "wp-admin") != False or php_strpos(PHP_SERVER["REQUEST_URI"], "wp-login.php") != False:
            path_ = php_preg_replace("#/(wp-admin/.*|wp-login.php)#i", "", PHP_SERVER["REQUEST_URI"])
            pass
        elif script_filename_dir_ + "/" == abspath_fix_:
            #// Strip off any file/query params in the path.
            path_ = php_preg_replace("#/[^/]*$#i", "", PHP_SERVER["PHP_SELF"])
        else:
            if False != php_strpos(PHP_SERVER["SCRIPT_FILENAME"], abspath_fix_):
                #// Request is hitting a file inside ABSPATH.
                directory_ = php_str_replace(ABSPATH, "", script_filename_dir_)
                #// Strip off the subdirectory, and any file/query params.
                path_ = php_preg_replace("#/" + preg_quote(directory_, "#") + "/[^/]*$#i", "", PHP_SERVER["REQUEST_URI"])
            elif False != php_strpos(abspath_fix_, script_filename_dir_):
                #// Request is hitting a file above ABSPATH.
                subdirectory_ = php_substr(abspath_fix_, php_strpos(abspath_fix_, script_filename_dir_) + php_strlen(script_filename_dir_))
                #// Strip off any file/query params from the path, appending the subdirectory to the installation.
                path_ = php_preg_replace("#/[^/]*$#i", "", PHP_SERVER["REQUEST_URI"]) + subdirectory_
            else:
                path_ = PHP_SERVER["REQUEST_URI"]
            # end if
        # end if
        schema_ = "https://" if is_ssl() else "http://"
        #// set_url_scheme() is not defined yet.
        url_ = schema_ + PHP_SERVER["HTTP_HOST"] + path_
    # end if
    return php_rtrim(url_, "/")
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
def wp_suspend_cache_addition(suspend_=None, *_args_):
    if suspend_ is None:
        suspend_ = None
    # end if
    
    _suspend_ = False
    if php_is_bool(suspend_):
        _suspend_ = suspend_
    # end if
    return _suspend_
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
def wp_suspend_cache_invalidation(suspend_=None, *_args_):
    if suspend_ is None:
        suspend_ = True
    # end if
    
    global _wp_suspend_cache_invalidation_
    php_check_if_defined("_wp_suspend_cache_invalidation_")
    current_suspend_ = _wp_suspend_cache_invalidation_
    _wp_suspend_cache_invalidation_ = suspend_
    return current_suspend_
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
def is_main_site(site_id_=None, network_id_=None, *_args_):
    if site_id_ is None:
        site_id_ = None
    # end if
    if network_id_ is None:
        network_id_ = None
    # end if
    
    if (not is_multisite()):
        return True
    # end if
    if (not site_id_):
        site_id_ = get_current_blog_id()
    # end if
    site_id_ = php_int(site_id_)
    return get_main_site_id(network_id_) == site_id_
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
def get_main_site_id(network_id_=None, *_args_):
    if network_id_ is None:
        network_id_ = None
    # end if
    
    if (not is_multisite()):
        return get_current_blog_id()
    # end if
    network_ = get_network(network_id_)
    if (not network_):
        return 0
    # end if
    return network_.site_id
# end def get_main_site_id
#// 
#// Determine whether a network is the main network of the Multisite installation.
#// 
#// @since 3.7.0
#// 
#// @param int $network_id Optional. Network ID to test. Defaults to current network.
#// @return bool True if $network_id is the main network, or if not running Multisite.
#//
def is_main_network(network_id_=None, *_args_):
    if network_id_ is None:
        network_id_ = None
    # end if
    
    if (not is_multisite()):
        return True
    # end if
    if None == network_id_:
        network_id_ = get_current_network_id()
    # end if
    network_id_ = php_int(network_id_)
    return get_main_network_id() == network_id_
# end def is_main_network
#// 
#// Get the main network ID.
#// 
#// @since 4.3.0
#// 
#// @return int The ID of the main network.
#//
def get_main_network_id(*_args_):
    
    
    if (not is_multisite()):
        return 1
    # end if
    current_network_ = get_network()
    if php_defined("PRIMARY_NETWORK_ID"):
        main_network_id_ = PRIMARY_NETWORK_ID
    elif (php_isset(lambda : current_network_.id)) and 1 == php_int(current_network_.id):
        #// If the current network has an ID of 1, assume it is the main network.
        main_network_id_ = 1
    else:
        _networks_ = get_networks(Array({"fields": "ids", "number": 1}))
        main_network_id_ = php_array_shift(_networks_)
    # end if
    #// 
    #// Filters the main network ID.
    #// 
    #// @since 4.3.0
    #// 
    #// @param int $main_network_id The ID of the main network.
    #//
    return php_int(apply_filters("get_main_network_id", main_network_id_))
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
def global_terms_enabled(*_args_):
    
    
    if (not is_multisite()):
        return False
    # end if
    global_terms_ = None
    if php_is_null(global_terms_):
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
        filter_ = apply_filters("global_terms_enabled", None)
        if (not php_is_null(filter_)):
            global_terms_ = php_bool(filter_)
        else:
            global_terms_ = php_bool(get_site_option("global_terms_enabled", False))
        # end if
    # end if
    return global_terms_
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
def is_site_meta_supported(*_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if (not is_multisite()):
        return False
    # end if
    network_id_ = get_main_network_id()
    supported_ = get_network_option(network_id_, "site_meta_supported", False)
    if False == supported_:
        supported_ = 1 if wpdb_.get_var(str("SHOW TABLES LIKE '") + str(wpdb_.blogmeta) + str("'")) else 0
        update_network_option(network_id_, "site_meta_supported", supported_)
    # end if
    return php_bool(supported_)
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
def wp_timezone_override_offset(*_args_):
    
    
    timezone_string_ = get_option("timezone_string")
    if (not timezone_string_):
        return False
    # end if
    timezone_object_ = timezone_open(timezone_string_)
    datetime_object_ = date_create()
    if False == timezone_object_ or False == datetime_object_:
        return False
    # end if
    return round(timezone_offset_get(timezone_object_, datetime_object_) / HOUR_IN_SECONDS, 2)
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
def _wp_timezone_choice_usort_callback(a_=None, b_=None, *_args_):
    
    
    #// Don't use translated versions of Etc.
    if "Etc" == a_["continent"] and "Etc" == b_["continent"]:
        #// Make the order of these more like the old dropdown.
        if "GMT+" == php_substr(a_["city"], 0, 4) and "GMT+" == php_substr(b_["city"], 0, 4):
            return -1 * strnatcasecmp(a_["city"], b_["city"])
        # end if
        if "UTC" == a_["city"]:
            if "GMT+" == php_substr(b_["city"], 0, 4):
                return 1
            # end if
            return -1
        # end if
        if "UTC" == b_["city"]:
            if "GMT+" == php_substr(a_["city"], 0, 4):
                return -1
            # end if
            return 1
        # end if
        return strnatcasecmp(a_["city"], b_["city"])
    # end if
    if a_["t_continent"] == b_["t_continent"]:
        if a_["t_city"] == b_["t_city"]:
            return strnatcasecmp(a_["t_subcity"], b_["t_subcity"])
        # end if
        return strnatcasecmp(a_["t_city"], b_["t_city"])
    else:
        #// Force Etc to the bottom of the list.
        if "Etc" == a_["continent"]:
            return 1
        # end if
        if "Etc" == b_["continent"]:
            return -1
        # end if
        return strnatcasecmp(a_["t_continent"], b_["t_continent"])
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
def wp_timezone_choice(selected_zone_=None, locale_=None, *_args_):
    if locale_ is None:
        locale_ = None
    # end if
    
    mo_loaded_ = False
    locale_loaded_ = None
    continents_ = Array("Africa", "America", "Antarctica", "Arctic", "Asia", "Atlantic", "Australia", "Europe", "Indian", "Pacific")
    #// Load translations for continents and cities.
    if (not mo_loaded_) or locale_ != locale_loaded_:
        locale_loaded_ = locale_ if locale_ else get_locale()
        mofile_ = WP_LANG_DIR + "/continents-cities-" + locale_loaded_ + ".mo"
        unload_textdomain("continents-cities")
        load_textdomain("continents-cities", mofile_)
        mo_loaded_ = True
    # end if
    zonen_ = Array()
    for zone_ in timezone_identifiers_list():
        zone_ = php_explode("/", zone_)
        if (not php_in_array(zone_[0], continents_)):
            continue
        # end if
        #// This determines what gets set and translated - we don't translate Etc/* strings here, they are done later.
        exists_ = Array({0: (php_isset(lambda : zone_[0])) and zone_[0], 1: (php_isset(lambda : zone_[1])) and zone_[1], 2: (php_isset(lambda : zone_[2])) and zone_[2]})
        exists_[3] = exists_[0] and "Etc" != zone_[0]
        exists_[4] = exists_[1] and exists_[3]
        exists_[5] = exists_[2] and exists_[3]
        #// phpcs:disable WordPress.WP.I18n.LowLevelTranslationFunction,WordPress.WP.I18n.NonSingularStringLiteralText
        zonen_[-1] = Array({"continent": zone_[0] if exists_[0] else "", "city": zone_[1] if exists_[1] else "", "subcity": zone_[2] if exists_[2] else "", "t_continent": translate(php_str_replace("_", " ", zone_[0]), "continents-cities") if exists_[3] else "", "t_city": translate(php_str_replace("_", " ", zone_[1]), "continents-cities") if exists_[4] else "", "t_subcity": translate(php_str_replace("_", " ", zone_[2]), "continents-cities") if exists_[5] else ""})
        pass
    # end for
    usort(zonen_, "_wp_timezone_choice_usort_callback")
    structure_ = Array()
    if php_empty(lambda : selected_zone_):
        structure_[-1] = "<option selected=\"selected\" value=\"\">" + __("Select a city") + "</option>"
    # end if
    for key_,zone_ in zonen_.items():
        #// Build value in an array to join later.
        value_ = Array(zone_["continent"])
        if php_empty(lambda : zone_["city"]):
            #// It's at the continent level (generally won't happen).
            display_ = zone_["t_continent"]
        else:
            #// It's inside a continent group.
            #// Continent optgroup.
            if (not (php_isset(lambda : zonen_[key_ - 1]))) or zonen_[key_ - 1]["continent"] != zone_["continent"]:
                label_ = zone_["t_continent"]
                structure_[-1] = "<optgroup label=\"" + esc_attr(label_) + "\">"
            # end if
            #// Add the city to the value.
            value_[-1] = zone_["city"]
            display_ = zone_["t_city"]
            if (not php_empty(lambda : zone_["subcity"])):
                #// Add the subcity to the value.
                value_[-1] = zone_["subcity"]
                display_ += " - " + zone_["t_subcity"]
            # end if
        # end if
        #// Build the value.
        value_ = php_join("/", value_)
        selected_ = ""
        if value_ == selected_zone_:
            selected_ = "selected=\"selected\" "
        # end if
        structure_[-1] = "<option " + selected_ + "value=\"" + esc_attr(value_) + "\">" + esc_html(display_) + "</option>"
        #// Close continent optgroup.
        if (not php_empty(lambda : zone_["city"])) and (not (php_isset(lambda : zonen_[key_ + 1]))) or (php_isset(lambda : zonen_[key_ + 1])) and zonen_[key_ + 1]["continent"] != zone_["continent"]:
            structure_[-1] = "</optgroup>"
        # end if
    # end for
    #// Do UTC.
    structure_[-1] = "<optgroup label=\"" + esc_attr__("UTC") + "\">"
    selected_ = ""
    if "UTC" == selected_zone_:
        selected_ = "selected=\"selected\" "
    # end if
    structure_[-1] = "<option " + selected_ + "value=\"" + esc_attr("UTC") + "\">" + __("UTC") + "</option>"
    structure_[-1] = "</optgroup>"
    #// Do manual UTC offsets.
    structure_[-1] = "<optgroup label=\"" + esc_attr__("Manual Offsets") + "\">"
    offset_range_ = Array(-12, -11.5, -11, -10.5, -10, -9.5, -9, -8.5, -8, -7.5, -7, -6.5, -6, -5.5, -5, -4.5, -4, -3.5, -3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 5.75, 6, 6.5, 7, 7.5, 8, 8.5, 8.75, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.75, 13, 13.75, 14)
    for offset_ in offset_range_:
        if 0 <= offset_:
            offset_name_ = "+" + offset_
        else:
            offset_name_ = php_str(offset_)
        # end if
        offset_value_ = offset_name_
        offset_name_ = php_str_replace(Array(".25", ".5", ".75"), Array(":15", ":30", ":45"), offset_name_)
        offset_name_ = "UTC" + offset_name_
        offset_value_ = "UTC" + offset_value_
        selected_ = ""
        if offset_value_ == selected_zone_:
            selected_ = "selected=\"selected\" "
        # end if
        structure_[-1] = "<option " + selected_ + "value=\"" + esc_attr(offset_value_) + "\">" + esc_html(offset_name_) + "</option>"
    # end for
    structure_[-1] = "</optgroup>"
    return php_join("\n", structure_)
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
def _cleanup_header_comment(str_=None, *_args_):
    
    
    return php_trim(php_preg_replace("/\\s*(?:\\*\\/|\\?>).*/", "", str_))
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
def wp_scheduled_delete(*_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    delete_timestamp_ = time() - DAY_IN_SECONDS * EMPTY_TRASH_DAYS
    posts_to_delete_ = wpdb_.get_results(wpdb_.prepare(str("SELECT post_id FROM ") + str(wpdb_.postmeta) + str(" WHERE meta_key = '_wp_trash_meta_time' AND meta_value < %d"), delete_timestamp_), ARRAY_A)
    for post_ in posts_to_delete_:
        post_id_ = php_int(post_["post_id"])
        if (not post_id_):
            continue
        # end if
        del_post_ = get_post(post_id_)
        if (not del_post_) or "trash" != del_post_.post_status:
            delete_post_meta(post_id_, "_wp_trash_meta_status")
            delete_post_meta(post_id_, "_wp_trash_meta_time")
        else:
            wp_delete_post(post_id_)
        # end if
    # end for
    comments_to_delete_ = wpdb_.get_results(wpdb_.prepare(str("SELECT comment_id FROM ") + str(wpdb_.commentmeta) + str(" WHERE meta_key = '_wp_trash_meta_time' AND meta_value < %d"), delete_timestamp_), ARRAY_A)
    for comment_ in comments_to_delete_:
        comment_id_ = php_int(comment_["comment_id"])
        if (not comment_id_):
            continue
        # end if
        del_comment_ = get_comment(comment_id_)
        if (not del_comment_) or "trash" != del_comment_.comment_approved:
            delete_comment_meta(comment_id_, "_wp_trash_meta_time")
            delete_comment_meta(comment_id_, "_wp_trash_meta_status")
        else:
            wp_delete_comment(del_comment_)
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
def get_file_data(file_=None, default_headers_=None, context_="", *_args_):
    
    
    #// We don't need to write to the file, so just open for reading.
    fp_ = fopen(file_, "r")
    #// Pull only the first 8 KB of the file in.
    file_data_ = fread(fp_, 8 * KB_IN_BYTES)
    #// PHP will close file handle, but we are good citizens.
    php_fclose(fp_)
    #// Make sure we catch CR-only line endings.
    file_data_ = php_str_replace("\r", "\n", file_data_)
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
    extra_headers_ = apply_filters(str("extra_") + str(context_) + str("_headers"), Array()) if context_ else Array()
    if extra_headers_:
        extra_headers_ = php_array_combine(extra_headers_, extra_headers_)
        #// Keys equal values.
        all_headers_ = php_array_merge(extra_headers_, default_headers_)
    else:
        all_headers_ = default_headers_
    # end if
    for field_,regex_ in all_headers_.items():
        if php_preg_match("/^[ \\t\\/*#@]*" + preg_quote(regex_, "/") + ":(.*)$/mi", file_data_, match_) and match_[1]:
            all_headers_[field_] = _cleanup_header_comment(match_[1])
        else:
            all_headers_[field_] = ""
        # end if
    # end for
    return all_headers_
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
def __return_true(*_args_):
    
    
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
def __return_false(*_args_):
    
    
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
def __return_zero(*_args_):
    
    
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
def __return_empty_array(*_args_):
    
    
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
def __return_null(*_args_):
    
    
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
def __return_empty_string(*_args_):
    
    
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
def send_nosniff_header(*_args_):
    
    
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
def _wp_mysql_week(column_=None, *_args_):
    
    
    start_of_week_ = php_int(get_option("start_of_week"))
    for case in Switch(start_of_week_):
        if case(1):
            return str("WEEK( ") + str(column_) + str(", 1 )")
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
            return str("WEEK( DATE_SUB( ") + str(column_) + str(", INTERVAL ") + str(start_of_week_) + str(" DAY ), 0 )")
        # end if
        if case(0):
            pass
        # end if
        if case():
            return str("WEEK( ") + str(column_) + str(", 0 )")
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
def wp_find_hierarchy_loop(callback_=None, start_=None, start_parent_=None, callback_args_=None, *_args_):
    if callback_args_ is None:
        callback_args_ = Array()
    # end if
    
    override_ = Array() if php_is_null(start_parent_) else Array({start_: start_parent_})
    arbitrary_loop_member_ = wp_find_hierarchy_loop_tortoise_hare(callback_, start_, override_, callback_args_)
    if (not arbitrary_loop_member_):
        return Array()
    # end if
    return wp_find_hierarchy_loop_tortoise_hare(callback_, arbitrary_loop_member_, override_, callback_args_, True)
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
def wp_find_hierarchy_loop_tortoise_hare(callback_=None, start_=None, override_=None, callback_args_=None, _return_loop_=None, *_args_):
    if override_ is None:
        override_ = Array()
    # end if
    if callback_args_ is None:
        callback_args_ = Array()
    # end if
    if _return_loop_ is None:
        _return_loop_ = False
    # end if
    
    tortoise_ = start_
    hare_ = start_
    evanescent_hare_ = start_
    return_ = Array()
    #// Set evanescent_hare to one past hare.
    #// Increment hare two steps.
    while True:
        evanescent_hare_ = override_[hare_] if (php_isset(lambda : override_[hare_])) else call_user_func_array(callback_, php_array_merge(Array(hare_), callback_args_))
        hare_ = override_[evanescent_hare_] if (php_isset(lambda : override_[evanescent_hare_])) else call_user_func_array(callback_, php_array_merge(Array(evanescent_hare_), callback_args_))
        if not (tortoise_ and evanescent_hare_ and hare_):
            break
        # end if
        if _return_loop_:
            return_[tortoise_] = True
            return_[evanescent_hare_] = True
            return_[hare_] = True
        # end if
        #// Tortoise got lapped - must be a loop.
        if tortoise_ == evanescent_hare_ or tortoise_ == hare_:
            return return_ if _return_loop_ else tortoise_
        # end if
        #// Increment tortoise by one step.
        tortoise_ = override_[tortoise_] if (php_isset(lambda : override_[tortoise_])) else call_user_func_array(callback_, php_array_merge(Array(tortoise_), callback_args_))
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
def send_frame_options_header(*_args_):
    
    
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
def wp_allowed_protocols(*_args_):
    
    
    protocols_ = Array()
    if php_empty(lambda : protocols_):
        protocols_ = Array("http", "https", "ftp", "ftps", "mailto", "news", "irc", "gopher", "nntp", "feed", "telnet", "mms", "rtsp", "sms", "svn", "tel", "fax", "xmpp", "webcal", "urn")
    # end if
    if (not did_action("wp_loaded")):
        #// 
        #// Filters the list of protocols allowed in HTML attributes.
        #// 
        #// @since 3.0.0
        #// 
        #// @param string[] $protocols Array of allowed protocols e.g. 'http', 'ftp', 'tel', and more.
        #//
        protocols_ = array_unique(apply_filters("kses_allowed_protocols", protocols_))
    # end if
    return protocols_
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
def wp_debug_backtrace_summary(ignore_class_=None, skip_frames_=0, pretty_=None, *_args_):
    if ignore_class_ is None:
        ignore_class_ = None
    # end if
    if pretty_ is None:
        pretty_ = True
    # end if
    
    truncate_paths_ = None
    trace_ = php_debug_backtrace(False)
    caller_ = Array()
    check_class_ = (not php_is_null(ignore_class_))
    skip_frames_ += 1
    #// Skip this function.
    if (not (php_isset(lambda : truncate_paths_))):
        truncate_paths_ = Array(wp_normalize_path(WP_CONTENT_DIR), wp_normalize_path(ABSPATH))
    # end if
    for call_ in trace_:
        if skip_frames_ > 0:
            skip_frames_ -= 1
        elif (php_isset(lambda : call_["class"])):
            if check_class_ and ignore_class_ == call_["class"]:
                continue
                pass
            # end if
            caller_[-1] = str(call_["class"]) + str(call_["type"]) + str(call_["function"])
        else:
            if php_in_array(call_["function"], Array("do_action", "apply_filters", "do_action_ref_array", "apply_filters_ref_array")):
                caller_[-1] = str(call_["function"]) + str("('") + str(call_["args"][0]) + str("')")
            elif php_in_array(call_["function"], Array("include", "include_once", "require", "require_once")):
                filename_ = call_["args"][0] if (php_isset(lambda : call_["args"][0])) else ""
                caller_[-1] = call_["function"] + "('" + php_str_replace(truncate_paths_, "", wp_normalize_path(filename_)) + "')"
            else:
                caller_[-1] = call_["function"]
            # end if
        # end if
    # end for
    if pretty_:
        return php_join(", ", php_array_reverse(caller_))
    else:
        return caller_
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
def _get_non_cached_ids(object_ids_=None, cache_key_=None, *_args_):
    
    
    clean_ = Array()
    for id_ in object_ids_:
        id_ = php_int(id_)
        if (not wp_cache_get(id_, cache_key_)):
            clean_[-1] = id_
        # end if
    # end for
    return clean_
# end def _get_non_cached_ids
#// 
#// Test if the current device has the capability to upload files.
#// 
#// @since 3.4.0
#// @access private
#// 
#// @return bool Whether the device is able to upload files.
#//
def _device_can_upload(*_args_):
    
    
    if (not wp_is_mobile()):
        return True
    # end if
    ua_ = PHP_SERVER["HTTP_USER_AGENT"]
    if php_strpos(ua_, "iPhone") != False or php_strpos(ua_, "iPad") != False or php_strpos(ua_, "iPod") != False:
        return php_preg_match("#OS ([\\d_]+) like Mac OS X#", ua_, version_) and php_version_compare(version_[1], "6", ">=")
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
def wp_is_stream(path_=None, *_args_):
    
    
    scheme_separator_ = php_strpos(path_, "://")
    if False == scheme_separator_:
        #// $path isn't a stream.
        return False
    # end if
    stream_ = php_substr(path_, 0, scheme_separator_)
    return php_in_array(stream_, stream_get_wrappers(), True)
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
def wp_checkdate(month_=None, day_=None, year_=None, source_date_=None, *_args_):
    
    
    #// 
    #// Filters whether the given date is valid for the Gregorian calendar.
    #// 
    #// @since 3.5.0
    #// 
    #// @param bool   $checkdate   Whether the given date is valid.
    #// @param string $source_date Date to check.
    #//
    return apply_filters("wp_checkdate", checkdate(month_, day_, year_), source_date_)
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
def wp_auth_check_load(*_args_):
    
    
    if (not is_admin()) and (not is_user_logged_in()):
        return
    # end if
    if php_defined("IFRAME_REQUEST"):
        return
    # end if
    screen_ = get_current_screen()
    hidden_ = Array("update", "update-network", "update-core", "update-core-network", "upgrade", "upgrade-network", "network")
    show_ = (not php_in_array(screen_.id, hidden_))
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
    if apply_filters("wp_auth_check_load", show_, screen_):
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
def wp_auth_check_html(*_args_):
    
    
    login_url_ = wp_login_url()
    current_domain_ = "https://" if is_ssl() else "http://" + PHP_SERVER["HTTP_HOST"]
    same_domain_ = php_strpos(login_url_, current_domain_) == 0
    #// 
    #// Filters whether the authentication check originated at the same domain.
    #// 
    #// @since 3.6.0
    #// 
    #// @param bool $same_domain Whether the authentication check originated at the same domain.
    #//
    same_domain_ = apply_filters("wp_auth_check_same_domain", same_domain_)
    wrap_class_ = "hidden" if same_domain_ else "hidden fallback"
    php_print(" <div id=\"wp-auth-check-wrap\" class=\"")
    php_print(wrap_class_)
    php_print("""\">
    <div id=\"wp-auth-check-bg\"></div>
    <div id=\"wp-auth-check\">
    <button type=\"button\" class=\"wp-auth-check-close button-link\"><span class=\"screen-reader-text\">""")
    _e("Close dialog")
    php_print("</span></button>\n   ")
    if same_domain_:
        login_src_ = add_query_arg(Array({"interim-login": "1", "wp_lang": get_user_locale()}), login_url_)
        php_print("     <div id=\"wp-auth-check-form\" class=\"loading\" data-src=\"")
        php_print(esc_url(login_src_))
        php_print("\"></div>\n      ")
    # end if
    php_print(" <div class=\"wp-auth-fallback\">\n      <p><b class=\"wp-auth-fallback-expired\" tabindex=\"0\">")
    _e("Session expired")
    php_print("</b></p>\n       <p><a href=\"")
    php_print(esc_url(login_url_))
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
def wp_auth_check(response_=None, *_args_):
    
    
    response_["wp-auth-check"] = is_user_logged_in() and php_empty(lambda : PHP_GLOBALS["login_grace_period"])
    return response_
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
def get_tag_regex(tag_=None, *_args_):
    
    
    if php_empty(lambda : tag_):
        return
    # end if
    return php_sprintf("<%1$s[^<]*(?:>[\\s\\S]*<\\/%1$s>|\\s*\\/>)", tag_escape(tag_))
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
def _canonical_charset(charset_=None, *_args_):
    
    
    if "utf-8" == php_strtolower(charset_) or "utf8" == php_strtolower(charset_):
        return "UTF-8"
    # end if
    if "iso-8859-1" == php_strtolower(charset_) or "iso8859-1" == php_strtolower(charset_):
        return "ISO-8859-1"
    # end if
    return charset_
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
def mbstring_binary_safe_encoding(reset_=None, *_args_):
    if reset_ is None:
        reset_ = False
    # end if
    
    encodings_ = Array()
    overloaded_ = None
    if php_is_null(overloaded_):
        overloaded_ = php_function_exists("mb_internal_encoding") and php_ini_get("mbstring.func_overload") & 2
    # end if
    if False == overloaded_:
        return
    # end if
    if (not reset_):
        encoding_ = mb_internal_encoding()
        php_array_push(encodings_, encoding_)
        mb_internal_encoding("ISO-8859-1")
    # end if
    if reset_ and encodings_:
        encoding_ = php_array_pop(encodings_)
        mb_internal_encoding(encoding_)
    # end if
# end def mbstring_binary_safe_encoding
#// 
#// Reset the mbstring internal encoding to a users previously set encoding.
#// 
#// @see mbstring_binary_safe_encoding()
#// 
#// @since 3.7.0
#//
def reset_mbstring_encoding(*_args_):
    
    
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
def wp_validate_boolean(var_=None, *_args_):
    
    
    if php_is_bool(var_):
        return var_
    # end if
    if php_is_string(var_) and "false" == php_strtolower(var_):
        return False
    # end if
    return php_bool(var_)
# end def wp_validate_boolean
#// 
#// Delete a file
#// 
#// @since 4.2.0
#// 
#// @param string $file The path to the file to delete.
#//
def wp_delete_file(file_=None, *_args_):
    
    
    #// 
    #// Filters the path of the file to delete.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string $file Path to the file to delete.
    #//
    delete_ = apply_filters("wp_delete_file", file_)
    if (not php_empty(lambda : delete_)):
        php_no_error(lambda: unlink(delete_))
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
def wp_delete_file_from_directory(file_=None, directory_=None, *_args_):
    
    
    if wp_is_stream(file_):
        real_file_ = file_
        real_directory_ = directory_
    else:
        real_file_ = php_realpath(wp_normalize_path(file_))
        real_directory_ = php_realpath(wp_normalize_path(directory_))
    # end if
    if False != real_file_:
        real_file_ = wp_normalize_path(real_file_)
    # end if
    if False != real_directory_:
        real_directory_ = wp_normalize_path(real_directory_)
    # end if
    if False == real_file_ or False == real_directory_ or php_strpos(real_file_, trailingslashit(real_directory_)) != 0:
        return False
    # end if
    wp_delete_file(file_)
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
def wp_post_preview_js(*_args_):
    
    
    global post_
    php_check_if_defined("post_")
    if (not is_preview()) or php_empty(lambda : post_):
        return
    # end if
    #// Has to match the window name used in post_submit_meta_box().
    name_ = "wp-preview-" + php_int(post_.ID)
    php_print("""   <script>
    ( function() {
    var query = document.location.search;
if ( query && query.indexOf( 'preview=true' ) !== -1 ) {
    window.name = '""")
    php_print(name_)
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
def mysql_to_rfc3339(date_string_=None, *_args_):
    
    
    return mysql2date("Y-m-d\\TH:i:s", date_string_, False)
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
def wp_raise_memory_limit(context_="admin", *_args_):
    
    
    #// Exit early if the limit cannot be changed.
    if False == wp_is_ini_value_changeable("memory_limit"):
        return False
    # end if
    current_limit_ = php_ini_get("memory_limit")
    current_limit_int_ = wp_convert_hr_to_bytes(current_limit_)
    if -1 == current_limit_int_:
        return False
    # end if
    wp_max_limit_ = WP_MAX_MEMORY_LIMIT
    wp_max_limit_int_ = wp_convert_hr_to_bytes(wp_max_limit_)
    filtered_limit_ = wp_max_limit_
    for case in Switch(context_):
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
            filtered_limit_ = apply_filters("admin_memory_limit", filtered_limit_)
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
            filtered_limit_ = apply_filters("image_memory_limit", filtered_limit_)
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
            filtered_limit_ = apply_filters(str(context_) + str("_memory_limit"), filtered_limit_)
            break
        # end if
    # end for
    filtered_limit_int_ = wp_convert_hr_to_bytes(filtered_limit_)
    if -1 == filtered_limit_int_ or filtered_limit_int_ > wp_max_limit_int_ and filtered_limit_int_ > current_limit_int_:
        if False != php_ini_set("memory_limit", filtered_limit_):
            return filtered_limit_
        else:
            return False
        # end if
    elif -1 == wp_max_limit_int_ or wp_max_limit_int_ > current_limit_int_:
        if False != php_ini_set("memory_limit", wp_max_limit_):
            return wp_max_limit_
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
def wp_generate_uuid4(*_args_):
    
    
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
def wp_is_uuid(uuid_=None, version_=None, *_args_):
    if version_ is None:
        version_ = None
    # end if
    
    if (not php_is_string(uuid_)):
        return False
    # end if
    if php_is_numeric(version_):
        if 4 != php_int(version_):
            _doing_it_wrong(inspect.currentframe().f_code.co_name, __("Only UUID V4 is supported at this time."), "4.9.0")
            return False
        # end if
        regex_ = "/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/"
    else:
        regex_ = "/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/"
    # end if
    return php_bool(php_preg_match(regex_, uuid_))
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
def wp_unique_id(prefix_="", *_args_):
    
    
    id_counter_ = 0
    id_counter_ += 1
    id_counter_ += 1
    return prefix_ + php_str(id_counter_)
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
def wp_cache_get_last_changed(group_=None, *_args_):
    
    
    last_changed_ = wp_cache_get("last_changed", group_)
    if (not last_changed_):
        last_changed_ = php_microtime()
        wp_cache_set("last_changed", last_changed_, group_)
    # end if
    return last_changed_
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
def wp_site_admin_email_change_notification(old_email_=None, new_email_=None, option_name_=None, *_args_):
    
    
    send_ = True
    #// Don't send the notification to the default 'admin_email' value.
    if "you@example.com" == old_email_:
        send_ = False
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
    send_ = apply_filters("send_site_admin_email_change_email", send_, old_email_, new_email_)
    if (not send_):
        return
    # end if
    #// translators: Do not translate OLD_EMAIL, NEW_EMAIL, SITENAME, SITEURL: those are placeholders.
    email_change_text_ = __("""Hi,
    This notice confirms that the admin email address was changed on ###SITENAME###.
    The new admin email address is ###NEW_EMAIL###.
    This email has been sent to ###OLD_EMAIL###
    Regards,
    All at ###SITENAME###
    ###SITEURL###""")
    email_change_email_ = Array({"to": old_email_, "subject": __("[%s] Admin Email Changed"), "message": email_change_text_, "headers": ""})
    #// Get site name.
    site_name_ = wp_specialchars_decode(get_option("blogname"), ENT_QUOTES)
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
    email_change_email_ = apply_filters("site_admin_email_change_email", email_change_email_, old_email_, new_email_)
    email_change_email_["message"] = php_str_replace("###OLD_EMAIL###", old_email_, email_change_email_["message"])
    email_change_email_["message"] = php_str_replace("###NEW_EMAIL###", new_email_, email_change_email_["message"])
    email_change_email_["message"] = php_str_replace("###SITENAME###", site_name_, email_change_email_["message"])
    email_change_email_["message"] = php_str_replace("###SITEURL###", home_url(), email_change_email_["message"])
    wp_mail(email_change_email_["to"], php_sprintf(email_change_email_["subject"], site_name_), email_change_email_["message"], email_change_email_["headers"])
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
def wp_privacy_anonymize_ip(ip_addr_=None, ipv6_fallback_=None, *_args_):
    if ipv6_fallback_ is None:
        ipv6_fallback_ = False
    # end if
    
    #// Detect what kind of IP address this is.
    ip_prefix_ = ""
    is_ipv6_ = php_substr_count(ip_addr_, ":") > 1
    is_ipv4_ = 3 == php_substr_count(ip_addr_, ".")
    if is_ipv6_ and is_ipv4_:
        #// IPv6 compatibility mode, temporarily strip the IPv6 part, and treat it like IPv4.
        ip_prefix_ = "::ffff:"
        ip_addr_ = php_preg_replace("/^\\[?[0-9a-f:]*:/i", "", ip_addr_)
        ip_addr_ = php_str_replace("]", "", ip_addr_)
        is_ipv6_ = False
    # end if
    if is_ipv6_:
        #// IPv6 addresses will always be enclosed in [] if there's a port.
        left_bracket_ = php_strpos(ip_addr_, "[")
        right_bracket_ = php_strpos(ip_addr_, "]")
        percent_ = php_strpos(ip_addr_, "%")
        netmask_ = "ffff:ffff:ffff:ffff:0000:0000:0000:0000"
        #// Strip the port (and [] from IPv6 addresses), if they exist.
        if False != left_bracket_ and False != right_bracket_:
            ip_addr_ = php_substr(ip_addr_, left_bracket_ + 1, right_bracket_ - left_bracket_ - 1)
        elif False != left_bracket_ or False != right_bracket_:
            #// The IP has one bracket, but not both, so it's malformed.
            return "::"
        # end if
        #// Strip the reachability scope.
        if False != percent_:
            ip_addr_ = php_substr(ip_addr_, 0, percent_)
        # end if
        #// No invalid characters should be left.
        if php_preg_match("/[^0-9a-f:]/i", ip_addr_):
            return "::"
        # end if
        #// Partially anonymize the IP by reducing it to the corresponding network ID.
        if php_function_exists("inet_pton") and php_function_exists("inet_ntop"):
            ip_addr_ = inet_ntop(inet_pton(ip_addr_) & inet_pton(netmask_))
            if False == ip_addr_:
                return "::"
            # end if
        elif (not ipv6_fallback_):
            return "::"
        # end if
    elif is_ipv4_:
        #// Strip any port and partially anonymize the IP.
        last_octet_position_ = php_strrpos(ip_addr_, ".")
        ip_addr_ = php_substr(ip_addr_, 0, last_octet_position_) + ".0"
    else:
        return "0.0.0.0"
    # end if
    #// Restore the IPv6 prefix to compatibility mode addresses.
    return ip_prefix_ + ip_addr_
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
def wp_privacy_anonymize_data(type_=None, data_="", *_args_):
    
    
    for case in Switch(type_):
        if case("email"):
            anonymous_ = "deleted@site.invalid"
            break
        # end if
        if case("url"):
            anonymous_ = "https://site.invalid"
            break
        # end if
        if case("ip"):
            anonymous_ = wp_privacy_anonymize_ip(data_)
            break
        # end if
        if case("date"):
            anonymous_ = "0000-00-00 00:00:00"
            break
        # end if
        if case("text"):
            #// translators: Deleted text.
            anonymous_ = __("[deleted]")
            break
        # end if
        if case("longtext"):
            #// translators: Deleted long text.
            anonymous_ = __("This content was deleted by the author.")
            break
        # end if
        if case():
            anonymous_ = ""
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
    return apply_filters("wp_privacy_anonymize_data", anonymous_, type_, data_)
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
def wp_privacy_exports_dir(*_args_):
    
    
    upload_dir_ = wp_upload_dir()
    exports_dir_ = trailingslashit(upload_dir_["basedir"]) + "wp-personal-data-exports/"
    #// 
    #// Filters the directory used to store personal data export files.
    #// 
    #// @since 4.9.6
    #// 
    #// @param string $exports_dir Exports directory.
    #//
    return apply_filters("wp_privacy_exports_dir", exports_dir_)
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
def wp_privacy_exports_url(*_args_):
    
    
    upload_dir_ = wp_upload_dir()
    exports_url_ = trailingslashit(upload_dir_["baseurl"]) + "wp-personal-data-exports/"
    #// 
    #// Filters the URL of the directory used to store personal data export files.
    #// 
    #// @since 4.9.6
    #// 
    #// @param string $exports_url Exports directory URL.
    #//
    return apply_filters("wp_privacy_exports_url", exports_url_)
# end def wp_privacy_exports_url
#// 
#// Schedule a `WP_Cron` job to delete expired export files.
#// 
#// @since 4.9.6
#//
def wp_schedule_delete_old_privacy_export_files(*_args_):
    
    
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
def wp_privacy_delete_old_export_files(*_args_):
    
    
    exports_dir_ = wp_privacy_exports_dir()
    if (not php_is_dir(exports_dir_)):
        return
    # end if
    php_include_file(ABSPATH + "wp-admin/includes/file.php", once=True)
    export_files_ = list_files(exports_dir_, 100, Array("index.html"))
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
    expiration_ = apply_filters("wp_privacy_export_expiration", 3 * DAY_IN_SECONDS)
    for export_file_ in export_files_:
        file_age_in_seconds_ = time() - filemtime(export_file_)
        if expiration_ < file_age_in_seconds_:
            unlink(export_file_)
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
def wp_get_update_php_url(*_args_):
    
    
    default_url_ = wp_get_default_update_php_url()
    update_url_ = default_url_
    if False != php_getenv("WP_UPDATE_PHP_URL"):
        update_url_ = php_getenv("WP_UPDATE_PHP_URL")
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
    update_url_ = apply_filters("wp_update_php_url", update_url_)
    if php_empty(lambda : update_url_):
        update_url_ = default_url_
    # end if
    return update_url_
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
def wp_get_default_update_php_url(*_args_):
    
    
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
def wp_update_php_annotation(before_="<p class=\"description\">", after_="</p>", *_args_):
    
    
    annotation_ = wp_get_update_php_annotation()
    if annotation_:
        php_print(before_ + annotation_ + after_)
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
def wp_get_update_php_annotation(*_args_):
    
    
    update_url_ = wp_get_update_php_url()
    default_url_ = wp_get_default_update_php_url()
    if update_url_ == default_url_:
        return ""
    # end if
    annotation_ = php_sprintf(__("This resource is provided by your web host, and is specific to your site. For more information, <a href=\"%s\" target=\"_blank\">see the official WordPress documentation</a>."), esc_url(default_url_))
    return annotation_
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
def wp_get_direct_php_update_url(*_args_):
    
    
    direct_update_url_ = ""
    if False != php_getenv("WP_DIRECT_UPDATE_PHP_URL"):
        direct_update_url_ = php_getenv("WP_DIRECT_UPDATE_PHP_URL")
    # end if
    #// 
    #// Filters the URL for directly updating the PHP version the site is running on from the host.
    #// 
    #// @since 5.1.1
    #// 
    #// @param string $direct_update_url URL for directly updating PHP.
    #//
    direct_update_url_ = apply_filters("wp_direct_php_update_url", direct_update_url_)
    return direct_update_url_
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
def wp_direct_php_update_button(*_args_):
    
    
    direct_update_url_ = wp_get_direct_php_update_url()
    if php_empty(lambda : direct_update_url_):
        return
    # end if
    php_print("<p class=\"button-container\">")
    php_printf("<a class=\"button button-primary\" href=\"%1$s\" target=\"_blank\" rel=\"noopener noreferrer\">%2$s <span class=\"screen-reader-text\">%3$s</span><span aria-hidden=\"true\" class=\"dashicons dashicons-external\"></span></a>", esc_url(direct_update_url_), __("Update PHP"), __("(opens in a new tab)"))
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
def get_dirsize(directory_=None, max_execution_time_=None, *_args_):
    if max_execution_time_ is None:
        max_execution_time_ = None
    # end if
    
    dirsize_ = get_transient("dirsize_cache")
    if php_is_array(dirsize_) and (php_isset(lambda : dirsize_[directory_]["size"])):
        return dirsize_[directory_]["size"]
    # end if
    if (not php_is_array(dirsize_)):
        dirsize_ = Array()
    # end if
    #// Exclude individual site directories from the total when checking the main site of a network,
    #// as they are subdirectories and should not be counted.
    if is_multisite() and is_main_site():
        dirsize_[directory_]["size"] = recurse_dirsize(directory_, directory_ + "/sites", max_execution_time_)
    else:
        dirsize_[directory_]["size"] = recurse_dirsize(directory_, None, max_execution_time_)
    # end if
    set_transient("dirsize_cache", dirsize_, HOUR_IN_SECONDS)
    return dirsize_[directory_]["size"]
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
def recurse_dirsize(directory_=None, exclude_=None, max_execution_time_=None, *_args_):
    if exclude_ is None:
        exclude_ = None
    # end if
    if max_execution_time_ is None:
        max_execution_time_ = None
    # end if
    
    size_ = 0
    directory_ = untrailingslashit(directory_)
    if (not php_file_exists(directory_)) or (not php_is_dir(directory_)) or (not php_is_readable(directory_)):
        return False
    # end if
    if php_is_string(exclude_) and directory_ == exclude_ or php_is_array(exclude_) and php_in_array(directory_, exclude_, True):
        return False
    # end if
    if None == max_execution_time_:
        #// Keep the previous behavior but attempt to prevent fatal errors from timeout if possible.
        if php_function_exists("ini_get"):
            max_execution_time_ = php_ini_get("max_execution_time")
        else:
            #// Disable...
            max_execution_time_ = 0
        # end if
        #// Leave 1 second "buffer" for other operations if $max_execution_time has reasonable value.
        if max_execution_time_ > 10:
            max_execution_time_ -= 1
        # end if
    # end if
    handle_ = php_opendir(directory_)
    if handle_:
        while True:
            file_ = php_readdir(handle_)
            if not (file_ != False):
                break
            # end if
            path_ = directory_ + "/" + file_
            if "." != file_ and ".." != file_:
                if php_is_file(path_):
                    size_ += filesize(path_)
                elif php_is_dir(path_):
                    handlesize_ = recurse_dirsize(path_, exclude_, max_execution_time_)
                    if handlesize_ > 0:
                        size_ += handlesize_
                    # end if
                # end if
                if max_execution_time_ > 0 and php_microtime(True) - WP_START_TIMESTAMP > max_execution_time_:
                    #// Time exceeded. Give up instead of risking a fatal timeout.
                    size_ = None
                    break
                # end if
            # end if
        # end while
        php_closedir(handle_)
    # end if
    return size_
# end def recurse_dirsize
#// 
#// Checks compatibility with the current WordPress version.
#// 
#// @since 5.2.0
#// 
#// @param string $required Minimum required WordPress version.
#// @return bool True if required version is compatible or empty, false if not.
#//
def is_wp_version_compatible(required_=None, *_args_):
    
    
    return php_empty(lambda : required_) or php_version_compare(get_bloginfo("version"), required_, ">=")
# end def is_wp_version_compatible
#// 
#// Checks compatibility with the current PHP version.
#// 
#// @since 5.2.0
#// 
#// @param string $required Minimum required PHP version.
#// @return bool True if required version is compatible or empty, false if not.
#//
def is_php_version_compatible(required_=None, *_args_):
    
    
    return php_empty(lambda : required_) or php_version_compare(php_phpversion(), required_, ">=")
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
def wp_fuzzy_number_match(expected_=None, actual_=None, precision_=1, *_args_):
    
    
    return abs(php_float(expected_) - php_float(actual_)) <= precision_
# end def wp_fuzzy_number_match
