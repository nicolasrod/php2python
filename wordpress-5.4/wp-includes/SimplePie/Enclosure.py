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
#// SimplePie
#// 
#// A PHP-Based RSS and Atom Feed Framework.
#// Takes the hard work out of managing a complete RSS/Atom solution.
#// 
#// Copyright (c) 2004-2012, Ryan Parman, Geoffrey Sneddon, Ryan McCue, and contributors
#// All rights reserved.
#// 
#// Redistribution and use in source and binary forms, with or without modification, are
#// permitted provided that the following conditions are met:
#// 
#// Redistributions of source code must retain the above copyright notice, this list of
#// conditions and the following disclaimer.
#// 
#// Redistributions in binary form must reproduce the above copyright notice, this list
#// of conditions and the following disclaimer in the documentation and/or other materials
#// provided with the distribution.
#// 
#// Neither the name of the SimplePie Team nor the names of its contributors may be used
#// to endorse or promote products derived from this software without specific prior
#// written permission.
#// 
#// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS
#// OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
#// AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS
#// AND CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#// CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#// SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
#// OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#// POSSIBILITY OF SUCH DAMAGE.
#// 
#// @package SimplePie
#// @version 1.3.1
#// @copyright 2004-2012 Ryan Parman, Geoffrey Sneddon, Ryan McCue
#// @author Ryan Parman
#// @author Geoffrey Sneddon
#// @author Ryan McCue
#// @link http://simplepie.org/ SimplePie
#// @license http://www.opensource.org/licenses/bsd-license.php BSD License
#// 
#// 
#// Handles everything related to enclosures (including Media RSS and iTunes RSS)
#// 
#// Used by {@see SimplePie_Item::get_enclosure()} and {@see SimplePie_Item::get_enclosures()}
#// 
#// This class can be overloaded with {@see SimplePie::set_enclosure_class()}
#// 
#// @package SimplePie
#// @subpackage API
#//
class SimplePie_Enclosure():
    bitrate = Array()
    captions = Array()
    categories = Array()
    channels = Array()
    copyright = Array()
    credits = Array()
    description = Array()
    duration = Array()
    expression = Array()
    framerate = Array()
    handler = Array()
    hashes = Array()
    height = Array()
    javascript = Array()
    keywords = Array()
    lang = Array()
    length = Array()
    link = Array()
    medium = Array()
    player = Array()
    ratings = Array()
    restrictions = Array()
    samplingrate = Array()
    thumbnails = Array()
    title = Array()
    type = Array()
    width = Array()
    #// 
    #// Constructor, used to input the data
    #// 
    #// For documentation on all the parameters, see the corresponding
    #// properties and their accessors
    #// 
    #// @uses idna_convert If available, this will convert an IDN
    #//
    def __init__(self, link=None, type=None, length=None, javascript=None, bitrate=None, captions=None, categories=None, channels=None, copyright=None, credits=None, description=None, duration=None, expression=None, framerate=None, hashes=None, height=None, keywords=None, lang=None, medium=None, player=None, ratings=None, restrictions=None, samplingrate=None, thumbnails=None, title=None, width=None):
        
        self.bitrate = bitrate
        self.captions = captions
        self.categories = categories
        self.channels = channels
        self.copyright = copyright
        self.credits = credits
        self.description = description
        self.duration = duration
        self.expression = expression
        self.framerate = framerate
        self.hashes = hashes
        self.height = height
        self.keywords = keywords
        self.lang = lang
        self.length = length
        self.link = link
        self.medium = medium
        self.player = player
        self.ratings = ratings
        self.restrictions = restrictions
        self.samplingrate = samplingrate
        self.thumbnails = thumbnails
        self.title = title
        self.type = type
        self.width = width
        if php_class_exists("idna_convert"):
            idn = php_new_class("idna_convert", lambda : idna_convert())
            parsed = SimplePie_Misc.parse_url(link)
            self.link = SimplePie_Misc.compress_parse_url(parsed["scheme"], idn.encode(parsed["authority"]), parsed["path"], parsed["query"], parsed["fragment"])
        # end if
        self.handler = self.get_handler()
        pass
    # end def __init__
    #// 
    #// String-ified version
    #// 
    #// @return string
    #//
    def __tostring(self):
        
        #// There is no $this->data here
        return php_md5(serialize(self))
    # end def __tostring
    #// 
    #// Get the bitrate
    #// 
    #// @return string|null
    #//
    def get_bitrate(self):
        
        if self.bitrate != None:
            return self.bitrate
        else:
            return None
        # end if
    # end def get_bitrate
    #// 
    #// Get a single caption
    #// 
    #// @param int $key
    #// @return SimplePie_Caption|null
    #//
    def get_caption(self, key=0):
        
        captions = self.get_captions()
        if (php_isset(lambda : captions[key])):
            return captions[key]
        else:
            return None
        # end if
    # end def get_caption
    #// 
    #// Get all captions
    #// 
    #// @return array|null Array of {@see SimplePie_Caption} objects
    #//
    def get_captions(self):
        
        if self.captions != None:
            return self.captions
        else:
            return None
        # end if
    # end def get_captions
    #// 
    #// Get a single category
    #// 
    #// @param int $key
    #// @return SimplePie_Category|null
    #//
    def get_category(self, key=0):
        
        categories = self.get_categories()
        if (php_isset(lambda : categories[key])):
            return categories[key]
        else:
            return None
        # end if
    # end def get_category
    #// 
    #// Get all categories
    #// 
    #// @return array|null Array of {@see SimplePie_Category} objects
    #//
    def get_categories(self):
        
        if self.categories != None:
            return self.categories
        else:
            return None
        # end if
    # end def get_categories
    #// 
    #// Get the number of audio channels
    #// 
    #// @return int|null
    #//
    def get_channels(self):
        
        if self.channels != None:
            return self.channels
        else:
            return None
        # end if
    # end def get_channels
    #// 
    #// Get the copyright information
    #// 
    #// @return SimplePie_Copyright|null
    #//
    def get_copyright(self):
        
        if self.copyright != None:
            return self.copyright
        else:
            return None
        # end if
    # end def get_copyright
    #// 
    #// Get a single credit
    #// 
    #// @param int $key
    #// @return SimplePie_Credit|null
    #//
    def get_credit(self, key=0):
        
        credits = self.get_credits()
        if (php_isset(lambda : credits[key])):
            return credits[key]
        else:
            return None
        # end if
    # end def get_credit
    #// 
    #// Get all credits
    #// 
    #// @return array|null Array of {@see SimplePie_Credit} objects
    #//
    def get_credits(self):
        
        if self.credits != None:
            return self.credits
        else:
            return None
        # end if
    # end def get_credits
    #// 
    #// Get the description of the enclosure
    #// 
    #// @return string|null
    #//
    def get_description(self):
        
        if self.description != None:
            return self.description
        else:
            return None
        # end if
    # end def get_description
    #// 
    #// Get the duration of the enclosure
    #// 
    #// @param string $convert Convert seconds into hh:mm:ss
    #// @return string|int|null 'hh:mm:ss' string if `$convert` was specified, otherwise integer (or null if none found)
    #//
    def get_duration(self, convert=False):
        
        if self.duration != None:
            if convert:
                time = SimplePie_Misc.time_hms(self.duration)
                return time
            else:
                return self.duration
            # end if
        else:
            return None
        # end if
    # end def get_duration
    #// 
    #// Get the expression
    #// 
    #// @return string Probably one of 'sample', 'full', 'nonstop', 'clip'. Defaults to 'full'
    #//
    def get_expression(self):
        
        if self.expression != None:
            return self.expression
        else:
            return "full"
        # end if
    # end def get_expression
    #// 
    #// Get the file extension
    #// 
    #// @return string|null
    #//
    def get_extension(self):
        
        if self.link != None:
            url = SimplePie_Misc.parse_url(self.link)
            if url["path"] != "":
                return pathinfo(url["path"], PATHINFO_EXTENSION)
            # end if
        # end if
        return None
    # end def get_extension
    #// 
    #// Get the framerate (in frames-per-second)
    #// 
    #// @return string|null
    #//
    def get_framerate(self):
        
        if self.framerate != None:
            return self.framerate
        else:
            return None
        # end if
    # end def get_framerate
    #// 
    #// Get the preferred handler
    #// 
    #// @return string|null One of 'flash', 'fmedia', 'quicktime', 'wmedia', 'mp3'
    #//
    def get_handler(self):
        
        return self.get_real_type(True)
    # end def get_handler
    #// 
    #// Get a single hash
    #// 
    #// @link http://www.rssboard.org/media-rss#media-hash
    #// @param int $key
    #// @return string|null Hash as per `media:hash`, prefixed with "$algo:"
    #//
    def get_hash(self, key=0):
        
        hashes = self.get_hashes()
        if (php_isset(lambda : hashes[key])):
            return hashes[key]
        else:
            return None
        # end if
    # end def get_hash
    #// 
    #// Get all credits
    #// 
    #// @return array|null Array of strings, see {@see get_hash()}
    #//
    def get_hashes(self):
        
        if self.hashes != None:
            return self.hashes
        else:
            return None
        # end if
    # end def get_hashes
    #// 
    #// Get the height
    #// 
    #// @return string|null
    #//
    def get_height(self):
        
        if self.height != None:
            return self.height
        else:
            return None
        # end if
    # end def get_height
    #// 
    #// Get the language
    #// 
    #// @link http://tools.ietf.org/html/rfc3066
    #// @return string|null Language code as per RFC 3066
    #//
    def get_language(self):
        
        if self.lang != None:
            return self.lang
        else:
            return None
        # end if
    # end def get_language
    #// 
    #// Get a single keyword
    #// 
    #// @param int $key
    #// @return string|null
    #//
    def get_keyword(self, key=0):
        
        keywords = self.get_keywords()
        if (php_isset(lambda : keywords[key])):
            return keywords[key]
        else:
            return None
        # end if
    # end def get_keyword
    #// 
    #// Get all keywords
    #// 
    #// @return array|null Array of strings
    #//
    def get_keywords(self):
        
        if self.keywords != None:
            return self.keywords
        else:
            return None
        # end if
    # end def get_keywords
    #// 
    #// Get length
    #// 
    #// @return float Length in bytes
    #//
    def get_length(self):
        
        if self.length != None:
            return self.length
        else:
            return None
        # end if
    # end def get_length
    #// 
    #// Get the URL
    #// 
    #// @return string|null
    #//
    def get_link(self):
        
        if self.link != None:
            return urldecode(self.link)
        else:
            return None
        # end if
    # end def get_link
    #// 
    #// Get the medium
    #// 
    #// @link http://www.rssboard.org/media-rss#media-content
    #// @return string|null Should be one of 'image', 'audio', 'video', 'document', 'executable'
    #//
    def get_medium(self):
        
        if self.medium != None:
            return self.medium
        else:
            return None
        # end if
    # end def get_medium
    #// 
    #// Get the player URL
    #// 
    #// Typically the same as {@see get_permalink()}
    #// @return string|null Player URL
    #//
    def get_player(self):
        
        if self.player != None:
            return self.player
        else:
            return None
        # end if
    # end def get_player
    #// 
    #// Get a single rating
    #// 
    #// @param int $key
    #// @return SimplePie_Rating|null
    #//
    def get_rating(self, key=0):
        
        ratings = self.get_ratings()
        if (php_isset(lambda : ratings[key])):
            return ratings[key]
        else:
            return None
        # end if
    # end def get_rating
    #// 
    #// Get all ratings
    #// 
    #// @return array|null Array of {@see SimplePie_Rating} objects
    #//
    def get_ratings(self):
        
        if self.ratings != None:
            return self.ratings
        else:
            return None
        # end if
    # end def get_ratings
    #// 
    #// Get a single restriction
    #// 
    #// @param int $key
    #// @return SimplePie_Restriction|null
    #//
    def get_restriction(self, key=0):
        
        restrictions = self.get_restrictions()
        if (php_isset(lambda : restrictions[key])):
            return restrictions[key]
        else:
            return None
        # end if
    # end def get_restriction
    #// 
    #// Get all restrictions
    #// 
    #// @return array|null Array of {@see SimplePie_Restriction} objects
    #//
    def get_restrictions(self):
        
        if self.restrictions != None:
            return self.restrictions
        else:
            return None
        # end if
    # end def get_restrictions
    #// 
    #// Get the sampling rate (in kHz)
    #// 
    #// @return string|null
    #//
    def get_sampling_rate(self):
        
        if self.samplingrate != None:
            return self.samplingrate
        else:
            return None
        # end if
    # end def get_sampling_rate
    #// 
    #// Get the file size (in MiB)
    #// 
    #// @return float|null File size in mebibytes (1048 bytes)
    #//
    def get_size(self):
        
        length = self.get_length()
        if length != None:
            return round(length / 1048576, 2)
        else:
            return None
        # end if
    # end def get_size
    #// 
    #// Get a single thumbnail
    #// 
    #// @param int $key
    #// @return string|null Thumbnail URL
    #//
    def get_thumbnail(self, key=0):
        
        thumbnails = self.get_thumbnails()
        if (php_isset(lambda : thumbnails[key])):
            return thumbnails[key]
        else:
            return None
        # end if
    # end def get_thumbnail
    #// 
    #// Get all thumbnails
    #// 
    #// @return array|null Array of thumbnail URLs
    #//
    def get_thumbnails(self):
        
        if self.thumbnails != None:
            return self.thumbnails
        else:
            return None
        # end if
    # end def get_thumbnails
    #// 
    #// Get the title
    #// 
    #// @return string|null
    #//
    def get_title(self):
        
        if self.title != None:
            return self.title
        else:
            return None
        # end if
    # end def get_title
    #// 
    #// Get mimetype of the enclosure
    #// 
    #// @see get_real_type()
    #// @return string|null MIME type
    #//
    def get_type(self):
        
        if self.type != None:
            return self.type
        else:
            return None
        # end if
    # end def get_type
    #// 
    #// Get the width
    #// 
    #// @return string|null
    #//
    def get_width(self):
        
        if self.width != None:
            return self.width
        else:
            return None
        # end if
    # end def get_width
    #// 
    #// Embed the enclosure using `<embed>`
    #// 
    #// @deprecated Use the second parameter to {@see embed} instead
    #// 
    #// @param array|string $options See first paramter to {@see embed}
    #// @return string HTML string to output
    #//
    def native_embed(self, options=""):
        
        return self.embed(options, True)
    # end def native_embed
    #// 
    #// Embed the enclosure using Javascript
    #// 
    #// `$options` is an array or comma-separated key:value string, with the
    #// following properties:
    #// 
    #// - `alt` (string): Alternate content for when an end-user does not have
    #// the appropriate handler installed or when a file type is
    #// unsupported. Can be any text or HTML. Defaults to blank.
    #// - `altclass` (string): If a file type is unsupported, the end-user will
    #// see the alt text (above) linked directly to the content. That link
    #// will have this value as its class name. Defaults to blank.
    #// - `audio` (string): This is an image that should be used as a
    #// placeholder for audio files before they're loaded (QuickTime-only).
    #// Can be any relative or absolute URL. Defaults to blank.
    #// - `bgcolor` (string): The background color for the media, if not
    #// already transparent. Defaults to `#ffffff`.
    #// - `height` (integer): The height of the embedded media. Accepts any
    #// numeric pixel value (such as `360`) or `auto`. Defaults to `auto`,
    #// and it is recommended that you use this default.
    #// - `loop` (boolean): Do you want the media to loop when its done?
    #// Defaults to `false`.
    #// - `mediaplayer` (string): The location of the included
    #// `mediaplayer.swf` file. This allows for the playback of Flash Video
    #// (`.flv`) files, and is the default handler for non-Odeo MP3's.
    #// Defaults to blank.
    #// - `video` (string): This is an image that should be used as a
    #// placeholder for video files before they're loaded (QuickTime-only).
    #// Can be any relative or absolute URL. Defaults to blank.
    #// - `width` (integer): The width of the embedded media. Accepts any
    #// numeric pixel value (such as `480`) or `auto`. Defaults to `auto`,
    #// and it is recommended that you use this default.
    #// - `widescreen` (boolean): Is the enclosure widescreen or standard?
    #// This applies only to video enclosures, and will automatically resize
    #// the content appropriately.  Defaults to `false`, implying 4:3 mode.
    #// 
    #// Note: Non-widescreen (4:3) mode with `width` and `height` set to `auto`
    #// will default to 480x360 video resolution.  Widescreen (16:9) mode with
    #// `width` and `height` set to `auto` will default to 480x270 video resolution.
    #// 
    #// @todo If the dimensions for media:content are defined, use them when width/height are set to 'auto'.
    #// @param array|string $options Comma-separated key:value list, or array
    #// @param bool $native Use `<embed>`
    #// @return string HTML string to output
    #//
    def embed(self, options="", native=False):
        
        #// Set up defaults
        audio = ""
        video = ""
        alt = ""
        altclass = ""
        loop = "false"
        width = "auto"
        height = "auto"
        bgcolor = "#ffffff"
        mediaplayer = ""
        widescreen = False
        handler = self.get_handler()
        type = self.get_real_type()
        #// Process options and reassign values as necessary
        if php_is_array(options):
            extract(options)
        else:
            options = php_explode(",", options)
            for option in options:
                opt = php_explode(":", option, 2)
                if (php_isset(lambda : opt[0]) and php_isset(lambda : opt[1])):
                    opt[0] = php_trim(opt[0])
                    opt[1] = php_trim(opt[1])
                    for case in Switch(opt[0]):
                        if case("audio"):
                            audio = opt[1]
                            break
                        # end if
                        if case("video"):
                            video = opt[1]
                            break
                        # end if
                        if case("alt"):
                            alt = opt[1]
                            break
                        # end if
                        if case("altclass"):
                            altclass = opt[1]
                            break
                        # end if
                        if case("loop"):
                            loop = opt[1]
                            break
                        # end if
                        if case("width"):
                            width = opt[1]
                            break
                        # end if
                        if case("height"):
                            height = opt[1]
                            break
                        # end if
                        if case("bgcolor"):
                            bgcolor = opt[1]
                            break
                        # end if
                        if case("mediaplayer"):
                            mediaplayer = opt[1]
                            break
                        # end if
                        if case("widescreen"):
                            widescreen = opt[1]
                            break
                        # end if
                    # end for
                # end if
            # end for
        # end if
        mime = php_explode("/", type, 2)
        mime = mime[0]
        #// Process values for 'auto'
        if width == "auto":
            if mime == "video":
                if height == "auto":
                    width = 480
                elif widescreen:
                    width = round(php_intval(height) / 9 * 16)
                else:
                    width = round(php_intval(height) / 3 * 4)
                # end if
            else:
                width = "100%"
            # end if
        # end if
        if height == "auto":
            if mime == "audio":
                height = 0
            elif mime == "video":
                if width == "auto":
                    if widescreen:
                        height = 270
                    else:
                        height = 360
                    # end if
                elif widescreen:
                    height = round(php_intval(width) / 16 * 9)
                else:
                    height = round(php_intval(width) / 4 * 3)
                # end if
            else:
                height = 376
            # end if
        elif mime == "audio":
            height = 0
        # end if
        #// Set proper placeholder value
        if mime == "audio":
            placeholder = audio
        elif mime == "video":
            placeholder = video
        # end if
        embed = ""
        #// Flash
        if handler == "flash":
            if native:
                embed += "<embed src=\"" + self.get_link() + str("\" pluginspage=\"http://adobe.com/go/getflashplayer\" type=\"") + str(type) + str("\" quality=\"high\" width=\"") + str(width) + str("\" height=\"") + str(height) + str("\" bgcolor=\"") + str(bgcolor) + str("\" loop=\"") + str(loop) + str("\"></embed>")
            else:
                embed += str("<script type='text/javascript'>embed_flash('") + str(bgcolor) + str("', '") + str(width) + str("', '") + str(height) + str("', '") + self.get_link() + str("', '") + str(loop) + str("', '") + str(type) + str("');</script>")
            # end if
            #// Flash Media Player file types.
            #// Preferred handler for MP3 file types.
        elif handler == "fmedia" or handler == "mp3" and mediaplayer != "":
            height += 20
            if native:
                embed += str("<embed src=\"") + str(mediaplayer) + str("\" pluginspage=\"http://adobe.com/go/getflashplayer\" type=\"application/x-shockwave-flash\" quality=\"high\" width=\"") + str(width) + str("\" height=\"") + str(height) + str("\" wmode=\"transparent\" flashvars=\"file=") + rawurlencode(self.get_link() + "?file_extension=." + self.get_extension()) + str("&autostart=false&repeat=") + str(loop) + str("&showdigits=true&showfsbutton=false\"></embed>")
            else:
                embed += str("<script type='text/javascript'>embed_flv('") + str(width) + str("', '") + str(height) + str("', '") + rawurlencode(self.get_link() + "?file_extension=." + self.get_extension()) + str("', '") + str(placeholder) + str("', '") + str(loop) + str("', '") + str(mediaplayer) + str("');</script>")
            # end if
            #// QuickTime 7 file types.  Need to test with QuickTime 6.
            #// Only handle MP3's if the Flash Media Player is not present.
        elif handler == "quicktime" or handler == "mp3" and mediaplayer == "":
            height += 16
            if native:
                if placeholder != "":
                    embed += str("<embed type=\"") + str(type) + str("\" style=\"cursor:hand; cursor:pointer;\" href=\"") + self.get_link() + str("\" src=\"") + str(placeholder) + str("\" width=\"") + str(width) + str("\" height=\"") + str(height) + str("\" autoplay=\"false\" target=\"myself\" controller=\"false\" loop=\"") + str(loop) + str("\" scale=\"aspect\" bgcolor=\"") + str(bgcolor) + str("\" pluginspage=\"http://apple.com/quicktime/download/\"></embed>")
                else:
                    embed += str("<embed type=\"") + str(type) + str("\" style=\"cursor:hand; cursor:pointer;\" src=\"") + self.get_link() + str("\" width=\"") + str(width) + str("\" height=\"") + str(height) + str("\" autoplay=\"false\" target=\"myself\" controller=\"true\" loop=\"") + str(loop) + str("\" scale=\"aspect\" bgcolor=\"") + str(bgcolor) + str("\" pluginspage=\"http://apple.com/quicktime/download/\"></embed>")
                # end if
            else:
                embed += str("<script type='text/javascript'>embed_quicktime('") + str(type) + str("', '") + str(bgcolor) + str("', '") + str(width) + str("', '") + str(height) + str("', '") + self.get_link() + str("', '") + str(placeholder) + str("', '") + str(loop) + str("');</script>")
            # end if
            #// Windows Media
        elif handler == "wmedia":
            height += 45
            if native:
                embed += "<embed type=\"application/x-mplayer2\" src=\"" + self.get_link() + str("\" autosize=\"1\" width=\"") + str(width) + str("\" height=\"") + str(height) + str("\" showcontrols=\"1\" showstatusbar=\"0\" showdisplay=\"0\" autostart=\"0\"></embed>")
            else:
                embed += str("<script type='text/javascript'>embed_wmedia('") + str(width) + str("', '") + str(height) + str("', '") + self.get_link() + "');</script>"
            # end if
        else:
            embed += "<a href=\"" + self.get_link() + "\" class=\"" + altclass + "\">" + alt + "</a>"
        # end if
        return embed
    # end def embed
    #// 
    #// Get the real media type
    #// 
    #// Often, feeds lie to us, necessitating a bit of deeper inspection. This
    #// converts types to their canonical representations based on the file
    #// extension
    #// 
    #// @see get_type()
    #// @param bool $find_handler Internal use only, use {@see get_handler()} instead
    #// @return string MIME type
    #//
    def get_real_type(self, find_handler=False):
        
        #// Mime-types by handler.
        types_flash = Array("application/x-shockwave-flash", "application/futuresplash")
        #// Flash
        types_fmedia = Array("video/flv", "video/x-flv", "flv-application/octet-stream")
        #// Flash Media Player
        types_quicktime = Array("audio/3gpp", "audio/3gpp2", "audio/aac", "audio/x-aac", "audio/aiff", "audio/x-aiff", "audio/mid", "audio/midi", "audio/x-midi", "audio/mp4", "audio/m4a", "audio/x-m4a", "audio/wav", "audio/x-wav", "video/3gpp", "video/3gpp2", "video/m4v", "video/x-m4v", "video/mp4", "video/mpeg", "video/x-mpeg", "video/quicktime", "video/sd-video")
        #// QuickTime
        types_wmedia = Array("application/asx", "application/x-mplayer2", "audio/x-ms-wma", "audio/x-ms-wax", "video/x-ms-asf-plugin", "video/x-ms-asf", "video/x-ms-wm", "video/x-ms-wmv", "video/x-ms-wvx")
        #// Windows Media
        types_mp3 = Array("audio/mp3", "audio/x-mp3", "audio/mpeg", "audio/x-mpeg")
        #// MP3
        if self.get_type() != None:
            type = php_strtolower(self.type)
        else:
            type = None
        # end if
        #// If we encounter an unsupported mime-type, check the file extension and guess intelligently.
        if (not php_in_array(type, php_array_merge(types_flash, types_fmedia, types_quicktime, types_wmedia, types_mp3))):
            for case in Switch(php_strtolower(self.get_extension())):
                if case("aac"):
                    pass
                # end if
                if case("adts"):
                    type = "audio/acc"
                    break
                # end if
                if case("aif"):
                    pass
                # end if
                if case("aifc"):
                    pass
                # end if
                if case("aiff"):
                    pass
                # end if
                if case("cdda"):
                    type = "audio/aiff"
                    break
                # end if
                if case("bwf"):
                    type = "audio/wav"
                    break
                # end if
                if case("kar"):
                    pass
                # end if
                if case("mid"):
                    pass
                # end if
                if case("midi"):
                    pass
                # end if
                if case("smf"):
                    type = "audio/midi"
                    break
                # end if
                if case("m4a"):
                    type = "audio/x-m4a"
                    break
                # end if
                if case("mp3"):
                    pass
                # end if
                if case("swa"):
                    type = "audio/mp3"
                    break
                # end if
                if case("wav"):
                    type = "audio/wav"
                    break
                # end if
                if case("wax"):
                    type = "audio/x-ms-wax"
                    break
                # end if
                if case("wma"):
                    type = "audio/x-ms-wma"
                    break
                # end if
                if case("3gp"):
                    pass
                # end if
                if case("3gpp"):
                    type = "video/3gpp"
                    break
                # end if
                if case("3g2"):
                    pass
                # end if
                if case("3gp2"):
                    type = "video/3gpp2"
                    break
                # end if
                if case("asf"):
                    type = "video/x-ms-asf"
                    break
                # end if
                if case("flv"):
                    type = "video/x-flv"
                    break
                # end if
                if case("m1a"):
                    pass
                # end if
                if case("m1s"):
                    pass
                # end if
                if case("m1v"):
                    pass
                # end if
                if case("m15"):
                    pass
                # end if
                if case("m75"):
                    pass
                # end if
                if case("mp2"):
                    pass
                # end if
                if case("mpa"):
                    pass
                # end if
                if case("mpeg"):
                    pass
                # end if
                if case("mpg"):
                    pass
                # end if
                if case("mpm"):
                    pass
                # end if
                if case("mpv"):
                    type = "video/mpeg"
                    break
                # end if
                if case("m4v"):
                    type = "video/x-m4v"
                    break
                # end if
                if case("mov"):
                    pass
                # end if
                if case("qt"):
                    type = "video/quicktime"
                    break
                # end if
                if case("mp4"):
                    pass
                # end if
                if case("mpg4"):
                    type = "video/mp4"
                    break
                # end if
                if case("sdv"):
                    type = "video/sd-video"
                    break
                # end if
                if case("wm"):
                    type = "video/x-ms-wm"
                    break
                # end if
                if case("wmv"):
                    type = "video/x-ms-wmv"
                    break
                # end if
                if case("wvx"):
                    type = "video/x-ms-wvx"
                    break
                # end if
                if case("spl"):
                    type = "application/futuresplash"
                    break
                # end if
                if case("swf"):
                    type = "application/x-shockwave-flash"
                    break
                # end if
            # end for
        # end if
        if find_handler:
            if php_in_array(type, types_flash):
                return "flash"
            elif php_in_array(type, types_fmedia):
                return "fmedia"
            elif php_in_array(type, types_quicktime):
                return "quicktime"
            elif php_in_array(type, types_wmedia):
                return "wmedia"
            elif php_in_array(type, types_mp3):
                return "mp3"
            else:
                return None
            # end if
        else:
            return type
        # end if
    # end def get_real_type
# end class SimplePie_Enclosure
