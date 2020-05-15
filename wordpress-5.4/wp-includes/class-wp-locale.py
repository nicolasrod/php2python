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
#// Locale API: WP_Locale class
#// 
#// @package WordPress
#// @subpackage i18n
#// @since 4.6.0
#// 
#// 
#// Core class used to store translated data for a locale.
#// 
#// @since 2.1.0
#// @since 4.6.0 Moved to its own file from wp-includes/locale.php.
#//
class WP_Locale():
    weekday = Array()
    weekday_initial = Array()
    weekday_abbrev = Array()
    month = Array()
    month_genitive = Array()
    month_abbrev = Array()
    meridiem = Array()
    text_direction = "ltr"
    number_format = Array()
    #// 
    #// Constructor which calls helper methods to set up object variables.
    #// 
    #// @since 2.1.0
    #//
    def __init__(self):
        
        self.init()
        self.register_globals()
    # end def __init__
    #// 
    #// Sets up the translated strings and object properties.
    #// 
    #// The method creates the translatable strings for various
    #// calendar elements. Which allows for specifying locale
    #// specific calendar names and text direction.
    #// 
    #// @since 2.1.0
    #// 
    #// @global string $text_direction
    #// @global string $wp_version     The WordPress version string.
    #//
    def init(self):
        
        #// The weekdays.
        self.weekday[0] = __("Sunday")
        self.weekday[1] = __("Monday")
        self.weekday[2] = __("Tuesday")
        self.weekday[3] = __("Wednesday")
        self.weekday[4] = __("Thursday")
        self.weekday[5] = __("Friday")
        self.weekday[6] = __("Saturday")
        #// The first letter of each day.
        self.weekday_initial[__("Sunday")] = _x("S", "Sunday initial")
        self.weekday_initial[__("Monday")] = _x("M", "Monday initial")
        self.weekday_initial[__("Tuesday")] = _x("T", "Tuesday initial")
        self.weekday_initial[__("Wednesday")] = _x("W", "Wednesday initial")
        self.weekday_initial[__("Thursday")] = _x("T", "Thursday initial")
        self.weekday_initial[__("Friday")] = _x("F", "Friday initial")
        self.weekday_initial[__("Saturday")] = _x("S", "Saturday initial")
        #// Abbreviations for each day.
        self.weekday_abbrev[__("Sunday")] = __("Sun")
        self.weekday_abbrev[__("Monday")] = __("Mon")
        self.weekday_abbrev[__("Tuesday")] = __("Tue")
        self.weekday_abbrev[__("Wednesday")] = __("Wed")
        self.weekday_abbrev[__("Thursday")] = __("Thu")
        self.weekday_abbrev[__("Friday")] = __("Fri")
        self.weekday_abbrev[__("Saturday")] = __("Sat")
        #// The months.
        self.month["01"] = __("January")
        self.month["02"] = __("February")
        self.month["03"] = __("March")
        self.month["04"] = __("April")
        self.month["05"] = __("May")
        self.month["06"] = __("June")
        self.month["07"] = __("July")
        self.month["08"] = __("August")
        self.month["09"] = __("September")
        self.month["10"] = __("October")
        self.month["11"] = __("November")
        self.month["12"] = __("December")
        #// The months, genitive.
        self.month_genitive["01"] = _x("January", "genitive")
        self.month_genitive["02"] = _x("February", "genitive")
        self.month_genitive["03"] = _x("March", "genitive")
        self.month_genitive["04"] = _x("April", "genitive")
        self.month_genitive["05"] = _x("May", "genitive")
        self.month_genitive["06"] = _x("June", "genitive")
        self.month_genitive["07"] = _x("July", "genitive")
        self.month_genitive["08"] = _x("August", "genitive")
        self.month_genitive["09"] = _x("September", "genitive")
        self.month_genitive["10"] = _x("October", "genitive")
        self.month_genitive["11"] = _x("November", "genitive")
        self.month_genitive["12"] = _x("December", "genitive")
        #// Abbreviations for each month.
        self.month_abbrev[__("January")] = _x("Jan", "January abbreviation")
        self.month_abbrev[__("February")] = _x("Feb", "February abbreviation")
        self.month_abbrev[__("March")] = _x("Mar", "March abbreviation")
        self.month_abbrev[__("April")] = _x("Apr", "April abbreviation")
        self.month_abbrev[__("May")] = _x("May", "May abbreviation")
        self.month_abbrev[__("June")] = _x("Jun", "June abbreviation")
        self.month_abbrev[__("July")] = _x("Jul", "July abbreviation")
        self.month_abbrev[__("August")] = _x("Aug", "August abbreviation")
        self.month_abbrev[__("September")] = _x("Sep", "September abbreviation")
        self.month_abbrev[__("October")] = _x("Oct", "October abbreviation")
        self.month_abbrev[__("November")] = _x("Nov", "November abbreviation")
        self.month_abbrev[__("December")] = _x("Dec", "December abbreviation")
        #// The meridiems.
        self.meridiem["am"] = __("am")
        self.meridiem["pm"] = __("pm")
        self.meridiem["AM"] = __("AM")
        self.meridiem["PM"] = __("PM")
        #// Numbers formatting.
        #// See https://www.php.net/number_format
        #// translators: $thousands_sep argument for https://www.php.net/number_format, default is ','
        thousands_sep = __("number_format_thousands_sep")
        #// Replace space with a non-breaking space to avoid wrapping.
        thousands_sep = php_str_replace(" ", "&nbsp;", thousands_sep)
        self.number_format["thousands_sep"] = "," if "number_format_thousands_sep" == thousands_sep else thousands_sep
        #// translators: $dec_point argument for https://www.php.net/number_format, default is '.'
        decimal_point = __("number_format_decimal_point")
        self.number_format["decimal_point"] = "." if "number_format_decimal_point" == decimal_point else decimal_point
        #// Set text direction.
        if (php_isset(lambda : PHP_GLOBALS["text_direction"])):
            self.text_direction = PHP_GLOBALS["text_direction"]
            pass
        elif "rtl" == _x("ltr", "text direction"):
            self.text_direction = "rtl"
        # end if
    # end def init
    #// 
    #// Retrieve the full translated weekday word.
    #// 
    #// Week starts on translated Sunday and can be fetched
    #// by using 0 (zero). So the week starts with 0 (zero)
    #// and ends on Saturday with is fetched by using 6 (six).
    #// 
    #// @since 2.1.0
    #// 
    #// @param int $weekday_number 0 for Sunday through 6 Saturday.
    #// @return string Full translated weekday.
    #//
    def get_weekday(self, weekday_number=None):
        
        return self.weekday[weekday_number]
    # end def get_weekday
    #// 
    #// Retrieve the translated weekday initial.
    #// 
    #// The weekday initial is retrieved by the translated
    #// full weekday word. When translating the weekday initial
    #// pay attention to make sure that the starting letter does
    #// not conflict.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string $weekday_name Full translated weekday word.
    #// @return string Translated weekday initial.
    #//
    def get_weekday_initial(self, weekday_name=None):
        
        return self.weekday_initial[weekday_name]
    # end def get_weekday_initial
    #// 
    #// Retrieve the translated weekday abbreviation.
    #// 
    #// The weekday abbreviation is retrieved by the translated
    #// full weekday word.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string $weekday_name Full translated weekday word.
    #// @return string Translated weekday abbreviation.
    #//
    def get_weekday_abbrev(self, weekday_name=None):
        
        return self.weekday_abbrev[weekday_name]
    # end def get_weekday_abbrev
    #// 
    #// Retrieve the full translated month by month number.
    #// 
    #// The $month_number parameter has to be a string
    #// because it must have the '0' in front of any number
    #// that is less than 10. Starts from '01' and ends at
    #// '12'.
    #// 
    #// You can use an integer instead and it will add the
    #// '0' before the numbers less than 10 for you.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string|int $month_number '01' through '12'.
    #// @return string Translated full month name.
    #//
    def get_month(self, month_number=None):
        
        return self.month[zeroise(month_number, 2)]
    # end def get_month
    #// 
    #// Retrieve translated version of month abbreviation string.
    #// 
    #// The $month_name parameter is expected to be the translated or
    #// translatable version of the month.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string $month_name Translated month to get abbreviated version.
    #// @return string Translated abbreviated month.
    #//
    def get_month_abbrev(self, month_name=None):
        
        return self.month_abbrev[month_name]
    # end def get_month_abbrev
    #// 
    #// Retrieve translated version of meridiem string.
    #// 
    #// The $meridiem parameter is expected to not be translated.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string $meridiem Either 'am', 'pm', 'AM', or 'PM'. Not translated version.
    #// @return string Translated version
    #//
    def get_meridiem(self, meridiem=None):
        
        return self.meridiem[meridiem]
    # end def get_meridiem
    #// 
    #// Global variables are deprecated.
    #// 
    #// For backward compatibility only.
    #// 
    #// @deprecated For backward compatibility only.
    #// 
    #// @global array $weekday
    #// @global array $weekday_initial
    #// @global array $weekday_abbrev
    #// @global array $month
    #// @global array $month_abbrev
    #// 
    #// @since 2.1.0
    #//
    def register_globals(self):
        global PHP_GLOBALS
        PHP_GLOBALS["weekday"] = self.weekday
        PHP_GLOBALS["weekday_initial"] = self.weekday_initial
        PHP_GLOBALS["weekday_abbrev"] = self.weekday_abbrev
        PHP_GLOBALS["month"] = self.month
        PHP_GLOBALS["month_abbrev"] = self.month_abbrev
    # end def register_globals
    #// 
    #// Checks if current locale is RTL.
    #// 
    #// @since 3.0.0
    #// @return bool Whether locale is RTL.
    #//
    def is_rtl(self):
        
        return "rtl" == self.text_direction
    # end def is_rtl
    #// 
    #// Register date/time format strings for general POT.
    #// 
    #// Private, unused method to add some date/time formats translated
    #// on wp-admin/options-general.php to the general POT that would
    #// otherwise be added to the admin POT.
    #// 
    #// @since 3.6.0
    #//
    def _strings_for_pot(self):
        
        #// translators: Localized date format, see https://www.php.net/date
        __("F j, Y")
        #// translators: Localized time format, see https://www.php.net/date
        __("g:i a")
        #// translators: Localized date and time format, see https://www.php.net/date
        __("F j, Y g:i a")
    # end def _strings_for_pot
# end class WP_Locale
