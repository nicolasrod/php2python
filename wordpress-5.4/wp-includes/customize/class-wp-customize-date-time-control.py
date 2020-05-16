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
#// Customize API: WP_Customize_Date_Time_Control class
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 4.9.0
#// 
#// 
#// Customize Date Time Control class.
#// 
#// @since 4.9.0
#// 
#// @see WP_Customize_Control
#//
class WP_Customize_Date_Time_Control(WP_Customize_Control):
    type = "date_time"
    min_year = 1000
    max_year = 9999
    allow_past_date = True
    include_time = True
    twelve_hour_format = True
    #// 
    #// Don't render the control's content - it's rendered with a JS template.
    #// 
    #// @since 4.9.0
    #//
    def render_content(self):
        
        pass
    # end def render_content
    #// 
    #// Export data to JS.
    #// 
    #// @since 4.9.0
    #// @return array
    #//
    def json(self):
        
        data = super().json()
        data["maxYear"] = php_intval(self.max_year)
        data["minYear"] = php_intval(self.min_year)
        data["allowPastDate"] = php_bool(self.allow_past_date)
        data["twelveHourFormat"] = php_bool(self.twelve_hour_format)
        data["includeTime"] = php_bool(self.include_time)
        return data
    # end def json
    #// 
    #// Renders a JS template for the content of date time control.
    #// 
    #// @since 4.9.0
    #//
    def content_template(self):
        
        data = php_array_merge(self.json(), self.get_month_choices())
        timezone_info = self.get_timezone_info()
        date_format = get_option("date_format")
        date_format = php_preg_replace("/(?<!\\\\)[Yyo]/", "%1$s", date_format)
        date_format = php_preg_replace("/(?<!\\\\)[FmMn]/", "%2$s", date_format)
        date_format = php_preg_replace("/(?<!\\\\)[jd]/", "%3$s", date_format)
        #// Fallback to ISO date format if year, month, or day are missing from the date format.
        if 1 != php_substr_count(date_format, "%1$s") or 1 != php_substr_count(date_format, "%2$s") or 1 != php_substr_count(date_format, "%3$s"):
            date_format = "%1$s-%2$s-%3$s"
        # end if
        php_print("\n       <# _.defaults( data, ")
        php_print(wp_json_encode(data))
        php_print(""" ); #>
        <# var idPrefix = _.uniqueId( 'el' ) + '-'; #>
        <# if ( data.label ) { #>
        <span class=\"customize-control-title\">
        {{ data.label }}
        </span>
        <# } #>
        <div class=\"customize-control-notifications-container\"></div>
        <# if ( data.description ) { #>
        <span class=\"description customize-control-description\">{{ data.description }}</span>
        <# } #>
        <div class=\"date-time-fields {{ data.includeTime ? 'includes-time' : '' }}\">
        <fieldset class=\"day-row\">
        <legend class=\"title-day {{ ! data.includeTime ? 'screen-reader-text' : '' }}\">""")
        esc_html_e("Date")
        php_print("</legend>\n              <div class=\"day-fields clear\">\n                  ")
        ob_start()
        php_print("                 <label for=\"{{ idPrefix }}date-time-month\" class=\"screen-reader-text\">")
        esc_html_e("Month")
        php_print("""</label>
        <select id=\"{{ idPrefix }}date-time-month\" class=\"date-input month\" data-component=\"month\">
        <# _.each( data.month_choices, function( choice ) {
    if ( _.isObject( choice ) && ! _.isUndefined( choice.text ) && ! _.isUndefined( choice.value ) ) {
        text = choice.text;
        value = choice.value;
        }
        #>
        <option value=\"{{ value }}\" >
        {{ text }}
        </option>
        <# } ); #>
        </select>
        """)
        month_field = php_trim(ob_get_clean())
        php_print("\n                   ")
        ob_start()
        php_print("                 <label for=\"{{ idPrefix }}date-time-day\" class=\"screen-reader-text\">")
        esc_html_e("Day")
        php_print("</label>\n                   <input id=\"{{ idPrefix }}date-time-day\" type=\"number\" size=\"2\" autocomplete=\"off\" class=\"date-input day\" data-component=\"day\" min=\"1\" max=\"31\" />\n                 ")
        day_field = php_trim(ob_get_clean())
        php_print("\n                   ")
        ob_start()
        php_print("                 <label for=\"{{ idPrefix }}date-time-year\" class=\"screen-reader-text\">")
        esc_html_e("Year")
        php_print("</label>\n                   <input id=\"{{ idPrefix }}date-time-year\" type=\"number\" size=\"4\" autocomplete=\"off\" class=\"date-input year\" data-component=\"year\" min=\"{{ data.minYear }}\" max=\"{{ data.maxYear }}\">\n                   ")
        year_field = php_trim(ob_get_clean())
        php_print("\n                   ")
        printf(date_format, year_field, month_field, day_field)
        php_print("""               </div>
        </fieldset>
        <# if ( data.includeTime ) { #>
        <fieldset class=\"time-row clear\">
        <legend class=\"title-time\">""")
        esc_html_e("Time")
        php_print("</legend>\n                  <div class=\"time-fields clear\">\n                     <label for=\"{{ idPrefix }}date-time-hour\" class=\"screen-reader-text\">")
        esc_html_e("Hour")
        php_print("""</label>
        <# var maxHour = data.twelveHourFormat ? 12 : 23; #>
        <# var minHour = data.twelveHourFormat ? 1 : 0; #>
        <input id=\"{{ idPrefix }}date-time-hour\" type=\"number\" size=\"2\" autocomplete=\"off\" class=\"date-input hour\" data-component=\"hour\" min=\"{{ minHour }}\" max=\"{{ maxHour }}\">
        :
        <label for=\"{{ idPrefix }}date-time-minute\" class=\"screen-reader-text\">""")
        esc_html_e("Minute")
        php_print("""</label>
        <input id=\"{{ idPrefix }}date-time-minute\" type=\"number\" size=\"2\" autocomplete=\"off\" class=\"date-input minute\" data-component=\"minute\" min=\"0\" max=\"59\">
        <# if ( data.twelveHourFormat ) { #>
        <label for=\"{{ idPrefix }}date-time-meridian\" class=\"screen-reader-text\">""")
        esc_html_e("Meridian")
        php_print("</label>\n                           <select id=\"{{ idPrefix }}date-time-meridian\" class=\"date-input meridian\" data-component=\"meridian\">\n                                <option value=\"am\">")
        esc_html_e("AM")
        php_print("</option>\n                              <option value=\"pm\">")
        esc_html_e("PM")
        php_print("""</option>
        </select>
        <# } #>
        <p>""")
        php_print(timezone_info["description"])
        php_print("""</p>
        </div>
        </fieldset>
        <# } #>
        </div>
        """)
    # end def content_template
    #// 
    #// Generate options for the month Select.
    #// 
    #// Based on touch_time().
    #// 
    #// @since 4.9.0
    #// @see touch_time()
    #// 
    #// @global WP_Locale $wp_locale WordPress date and time locale object.
    #// 
    #// @return array
    #//
    def get_month_choices(self):
        
        global wp_locale
        php_check_if_defined("wp_locale")
        months = Array()
        i = 1
        while i < 13:
            
            month_text = wp_locale.get_month_abbrev(wp_locale.get_month(i))
            #// translators: 1: Month number (01, 02, etc.), 2: Month abbreviation.
            months[i]["text"] = php_sprintf(__("%1$s-%2$s"), i, month_text)
            months[i]["value"] = i
            i += 1
        # end while
        return Array({"month_choices": months})
    # end def get_month_choices
    #// 
    #// Get timezone info.
    #// 
    #// @since 4.9.0
    #// 
    #// @return array abbr and description.
    #//
    def get_timezone_info(self):
        
        tz_string = get_option("timezone_string")
        timezone_info = Array()
        if tz_string:
            try: 
                tz = php_new_class("DateTimezone", lambda : DateTimezone(tz_string))
            except Exception as e:
                tz = ""
            # end try
            if tz:
                now = php_new_class("DateTime", lambda : DateTime("now", tz))
                formatted_gmt_offset = self.format_gmt_offset(tz.getoffset(now) / 3600)
                tz_name = php_str_replace("_", " ", tz.getname())
                timezone_info["abbr"] = now.format("T")
                timezone_info["description"] = php_sprintf(__("Your timezone is set to %1$s (%2$s), currently %3$s (Coordinated Universal Time %4$s)."), tz_name, "<abbr>" + timezone_info["abbr"] + "</abbr>", "<abbr>UTC</abbr>" + formatted_gmt_offset, formatted_gmt_offset)
            else:
                timezone_info["description"] = ""
            # end if
        else:
            formatted_gmt_offset = self.format_gmt_offset(php_intval(get_option("gmt_offset", 0)))
            timezone_info["description"] = php_sprintf(__("Your timezone is set to %1$s (Coordinated Universal Time %2$s)."), "<abbr>UTC</abbr>" + formatted_gmt_offset, formatted_gmt_offset)
        # end if
        return timezone_info
    # end def get_timezone_info
    #// 
    #// Format GMT Offset.
    #// 
    #// @since 4.9.0
    #// @see wp_timezone_choice()
    #// 
    #// @param float $offset Offset in hours.
    #// @return string Formatted offset.
    #//
    def format_gmt_offset(self, offset=None):
        
        if 0 <= offset:
            formatted_offset = "+" + php_str(offset)
        else:
            formatted_offset = php_str(offset)
        # end if
        formatted_offset = php_str_replace(Array(".25", ".5", ".75"), Array(":15", ":30", ":45"), formatted_offset)
        return formatted_offset
    # end def format_gmt_offset
# end class WP_Customize_Date_Time_Control
