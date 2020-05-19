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
#// @package Hello_Dolly
#// @version 1.7.2
#// 
#// 
#// Plugin Name: Hello Dolly
#// Plugin URI: http://wordpress.org/plugins/hello-dolly
#// Description: This is not just a plugin, it symbolizes the hope and enthusiasm of an entire generation summed up in two words sung most famously by Louis Armstrong: Hello, Dolly. When activated you will randomly see a lyric from <cite>Hello, Dolly</cite> in the upper right of your admin screen on every page.
#// Author: Matt Mullenweg
#// Version: 1.7.2
#// Author URI: http://ma.tt
#//
def hello_dolly_get_lyric(*_args_):
    
    
    #// These are the lyrics to Hello Dolly
    lyrics_ = """Hello, Dolly
    Well, hello, Dolly
    It's so nice to have you back where you belong
    You're lookin' swell, Dolly
    I can tell, Dolly
    You're still glowin', you're still crowin'
    You're still goin' strong
    I feel the room swayin'
    While the band's playin'
    One of our old favorite songs from way back when
    So, take her wrap, fellas
    Dolly, never go away again
    Hello, Dolly
    Well, hello, Dolly
    It's so nice to have you back where you belong
    You're lookin' swell, Dolly
    I can tell, Dolly
    You're still glowin', you're still crowin'
    You're still goin' strong
    I feel the room swayin'
    While the band's playin'
    One of our old favorite songs from way back when
    So, golly, gee, fellas
    Have a little faith in me, fellas
    Dolly, never go away
    Promise, you'll never go away
    Dolly'll never go away again"""
    #// Here we split it into lines.
    lyrics_ = php_explode("\n", lyrics_)
    #// And then randomly choose a line.
    return wptexturize(lyrics_[mt_rand(0, php_count(lyrics_) - 1)])
# end def hello_dolly_get_lyric
#// This just echoes the chosen line, we'll position it later.
def hello_dolly(*_args_):
    
    
    chosen_ = hello_dolly_get_lyric()
    lang_ = ""
    if "en_" != php_substr(get_user_locale(), 0, 3):
        lang_ = " lang=\"en\""
    # end if
    php_printf("<p id=\"dolly\"><span class=\"screen-reader-text\">%s </span><span dir=\"ltr\"%s>%s</span></p>", __("Quote from Hello Dolly song, by Jerry Herman:"), lang_, chosen_)
# end def hello_dolly
#// Now we set that function up to execute when the admin_notices action is called.
add_action("admin_notices", "hello_dolly")
#// We need some CSS to position the paragraph.
def dolly_css(*_args_):
    
    
    php_print("""
    <style type='text/css'>
    #dolly {
    float: right;
    padding: 5px 10px;
    margin: 0;
    font-size: 12px;
    line-height: 1.6666;
    }
    .rtl #dolly {
    float: left;
    }
    .block-editor-page #dolly {
    display: none;
    }
    @media screen and (max-width: 782px) {
    #dolly,
    .rtl #dolly {
    float: none;
    padding-left: 0;
    padding-right: 0;
    }
    }
    </style>
    """)
# end def dolly_css
add_action("admin_head", "dolly_css")
