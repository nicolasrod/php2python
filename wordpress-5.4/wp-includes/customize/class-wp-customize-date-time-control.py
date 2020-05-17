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
    #// 
    #// Customize control type.
    #// 
    #// @since 4.9.0
    #// @var string
    #//
    type = "date_time"
    #// 
    #// Minimum Year.
    #// 
    #// @since 4.9.0
    #// @var integer
    #//
    min_year = 1000
    #// 
    #// Maximum Year.
    #// 
    #// @since 4.9.0
    #// @var integer
    #//
    max_year = 9999
    #// 
    #// Allow past date, if set to false user can only select future date.
    #// 
    #// @since 4.9.0
    #// @var boolean
    #//
    allow_past_date = True
    #// 
    #// Whether hours, minutes, and meridian should be shown.
    #// 
    #// @since 4.9.0
    #// @var boolean
    #//
    include_time = True
    #// 
    #// If set to false the control will appear in 24 hour format,
    #// the value will still be saved in Y-m-d H:i:s format.
    #// 
    #// @since 4.9.0
    #// @var boolean
    #//
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
        
        
        data_ = super().json()
        data_["maxYear"] = php_intval(self.max_year)
        data_["minYear"] = php_intval(self.min_year)
        data_["allowPastDate"] = php_bool(self.allow_past_date)
        data_["twelveHourFormat"] = php_bool(self.twelve_hour_format)
        data_["includeTime"] = php_bool(self.include_time)
        return data_
    # end def json
    #// 
    #// Renders a JS template for the content of date time control.
    #// 
    #// @since 4.9.0
    #//
    def content_template(self):
        
        
        data_ = php_array_merge(self.json(), self.get_month_choices())
        timezone_info_ = self.get_timezone_info()
        date_format_ = get_option("date_format")
        date_format_ = php_preg_replace("/(?<!\\\\)[Yyo]/", "%1$s", date_format_)
        date_format_ = php_preg_replace("/(?<!\\\\)[FmMn]/", "%2$s", date_format_)
        date_format_ = php_preg_replace("/(?<!\\\\)[jd]/", "%3$s", date_format_)
        #// Fallback to ISO date format if year, month, or day are missing from the date format.
        if 1 != php_substr_count(date_format_, "%1$s") or 1 != php_substr_count(date_format_, "%2$s") or 1 != php_substr_count(date_format_, "%3$s"):
            date_format_ = "%1$s-%2$s-%3$s"
        # end if
        php_print("\n       <# _.defaults( data, ")
        php_print(wp_json_encode(data_))
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
        month_field_ = php_trim(ob_get_clean())
        php_print("\n                   ")
        ob_start()
        php_print("                 <label for=\"{{ idPrefix }}date-time-day\" class=\"screen-reader-text\">")
        esc_html_e("Day")
        php_print("</label>\n                   <input id=\"{{ idPrefix }}date-time-day\" type=\"number\" size=\"2\" autocomplete=\"off\" class=\"date-input day\" data-component=\"day\" min=\"1\" max=\"31\" />\n                 ")
        day_field_ = php_trim(ob_get_clean())
        php_print("\n                   ")
        ob_start()
        php_print("                 <label for=\"{{ idPrefix }}date-time-year\" class=\"screen-reader-text\">")
        esc_html_e("Year")
        php_print("</label>\n                   <input id=\"{{ idPrefix }}date-time-year\" type=\"number\" size=\"4\" autocomplete=\"off\" class=\"date-input year\" data-component=\"year\" min=\"{{ data.minYear }}\" max=\"{{ data.maxYear }}\">\n                   ")
        year_field_ = php_trim(ob_get_clean())
        php_print("\n                   ")
        printf(date_format_, year_field_, month_field_, day_field_)
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
        php_print(timezone_info_["description"])
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
        
        
        global wp_locale_
        php_check_if_defined("wp_locale_")
        months_ = Array()
        i_ = 1
        while i_ < 13:
            
            month_text_ = wp_locale_.get_month_abbrev(wp_locale_.get_month(i_))
            #// translators: 1: Month number (01, 02, etc.), 2: Month abbreviation.
            months_[i_]["text"] = php_sprintf(__("%1$s-%2$s"), i_, month_text_)
            months_[i_]["value"] = i_
            i_ += 1
        # end while
        return Array({"month_choices": months_})
    # end def get_month_choices
    #// 
    #// Get timezone info.
    #// 
    #// @since 4.9.0
    #// 
    #// @return array abbr and description.
    #//
    def get_timezone_info(self):
        
        
        tz_string_ = get_option("timezone_string")
        timezone_info_ = Array()
        if tz_string_:
            try: 
                tz_ = php_new_class("DateTimezone", lambda : DateTimezone(tz_string_))
            except Exception as e_:
                tz_ = ""
            # end try
            if tz_:
                now_ = php_new_class("DateTime", lambda : DateTime("now", tz_))
                formatted_gmt_offset_ = self.format_gmt_offset(tz_.getoffset(now_) / 3600)
                tz_name_ = php_str_replace("_", " ", tz_.getname())
                timezone_info_["abbr"] = now_.format("T")
                timezone_info_["description"] = php_sprintf(__("Your timezone is set to %1$s (%2$s), currently %3$s (Coordinated Universal Time %4$s)."), tz_name_, "<abbr>" + timezone_info_["abbr"] + "</abbr>", "<abbr>UTC</abbr>" + formatted_gmt_offset_, formatted_gmt_offset_)
            else:
                timezone_info_["description"] = ""
            # end if
        else:
            formatted_gmt_offset_ = self.format_gmt_offset(php_intval(get_option("gmt_offset", 0)))
            timezone_info_["description"] = php_sprintf(__("Your timezone is set to %1$s (Coordinated Universal Time %2$s)."), "<abbr>UTC</abbr>" + formatted_gmt_offset_, formatted_gmt_offset_)
        # end if
        return timezone_info_
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
    def format_gmt_offset(self, offset_=None):
        
        
        if 0 <= offset_:
            formatted_offset_ = "+" + php_str(offset_)
        else:
            formatted_offset_ = php_str(offset_)
        # end if
        formatted_offset_ = php_str_replace(Array(".25", ".5", ".75"), Array(":15", ":30", ":45"), formatted_offset_)
        return formatted_offset_
    # end def format_gmt_offset
# end class WP_Customize_Date_Time_Control
