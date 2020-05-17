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
    #// 
    #// @var string
    #// @see get_bitrate()
    #//
    bitrate = Array()
    #// 
    #// @var array
    #// @see get_captions()
    #//
    captions = Array()
    #// 
    #// @var array
    #// @see get_categories()
    #//
    categories = Array()
    #// 
    #// @var int
    #// @see get_channels()
    #//
    channels = Array()
    #// 
    #// @var SimplePie_Copyright
    #// @see get_copyright()
    #//
    copyright = Array()
    #// 
    #// @var array
    #// @see get_credits()
    #//
    credits = Array()
    #// 
    #// @var string
    #// @see get_description()
    #//
    description = Array()
    #// 
    #// @var int
    #// @see get_duration()
    #//
    duration = Array()
    #// 
    #// @var string
    #// @see get_expression()
    #//
    expression = Array()
    #// 
    #// @var string
    #// @see get_framerate()
    #//
    framerate = Array()
    #// 
    #// @var string
    #// @see get_handler()
    #//
    handler = Array()
    #// 
    #// @var array
    #// @see get_hashes()
    #//
    hashes = Array()
    #// 
    #// @var string
    #// @see get_height()
    #//
    height = Array()
    #// 
    #// @deprecated
    #// @var null
    #//
    javascript = Array()
    #// 
    #// @var array
    #// @see get_keywords()
    #//
    keywords = Array()
    #// 
    #// @var string
    #// @see get_language()
    #//
    lang = Array()
    #// 
    #// @var string
    #// @see get_length()
    #//
    length = Array()
    #// 
    #// @var string
    #// @see get_link()
    #//
    link = Array()
    #// 
    #// @var string
    #// @see get_medium()
    #//
    medium = Array()
    #// 
    #// @var string
    #// @see get_player()
    #//
    player = Array()
    #// 
    #// @var array
    #// @see get_ratings()
    #//
    ratings = Array()
    #// 
    #// @var array
    #// @see get_restrictions()
    #//
    restrictions = Array()
    #// 
    #// @var string
    #// @see get_sampling_rate()
    #//
    samplingrate = Array()
    #// 
    #// @var array
    #// @see get_thumbnails()
    #//
    thumbnails = Array()
    #// 
    #// @var string
    #// @see get_title()
    #//
    title = Array()
    #// 
    #// @var string
    #// @see get_type()
    #//
    type = Array()
    #// 
    #// @var string
    #// @see get_width()
    #//
    width = Array()
    #// 
    #// Constructor, used to input the data
    #// 
    #// For documentation on all the parameters, see the corresponding
    #// properties and their accessors
    #// 
    #// @uses idna_convert If available, this will convert an IDN
    #//
    def __init__(self, link_=None, type_=None, length_=None, javascript_=None, bitrate_=None, captions_=None, categories_=None, channels_=None, copyright_=None, credits_=None, description_=None, duration_=None, expression_=None, framerate_=None, hashes_=None, height_=None, keywords_=None, lang_=None, medium_=None, player_=None, ratings_=None, restrictions_=None, samplingrate_=None, thumbnails_=None, title_=None, width_=None):
        
        
        self.bitrate = bitrate_
        self.captions = captions_
        self.categories = categories_
        self.channels = channels_
        self.copyright = copyright_
        self.credits = credits_
        self.description = description_
        self.duration = duration_
        self.expression = expression_
        self.framerate = framerate_
        self.hashes = hashes_
        self.height = height_
        self.keywords = keywords_
        self.lang = lang_
        self.length = length_
        self.link = link_
        self.medium = medium_
        self.player = player_
        self.ratings = ratings_
        self.restrictions = restrictions_
        self.samplingrate = samplingrate_
        self.thumbnails = thumbnails_
        self.title = title_
        self.type = type_
        self.width = width_
        if php_class_exists("idna_convert"):
            idn_ = php_new_class("idna_convert", lambda : idna_convert())
            parsed_ = SimplePie_Misc.parse_url(link_)
            self.link = SimplePie_Misc.compress_parse_url(parsed_["scheme"], idn_.encode(parsed_["authority"]), parsed_["path"], parsed_["query"], parsed_["fragment"])
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
    def get_caption(self, key_=0):
        
        
        captions_ = self.get_captions()
        if (php_isset(lambda : captions_[key_])):
            return captions_[key_]
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
    def get_category(self, key_=0):
        
        
        categories_ = self.get_categories()
        if (php_isset(lambda : categories_[key_])):
            return categories_[key_]
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
    def get_credit(self, key_=0):
        
        
        credits_ = self.get_credits()
        if (php_isset(lambda : credits_[key_])):
            return credits_[key_]
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
    def get_duration(self, convert_=None):
        if convert_ is None:
            convert_ = False
        # end if
        
        if self.duration != None:
            if convert_:
                time_ = SimplePie_Misc.time_hms(self.duration)
                return time_
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
            url_ = SimplePie_Misc.parse_url(self.link)
            if url_["path"] != "":
                return pathinfo(url_["path"], PATHINFO_EXTENSION)
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
    def get_hash(self, key_=0):
        
        
        hashes_ = self.get_hashes()
        if (php_isset(lambda : hashes_[key_])):
            return hashes_[key_]
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
    def get_keyword(self, key_=0):
        
        
        keywords_ = self.get_keywords()
        if (php_isset(lambda : keywords_[key_])):
            return keywords_[key_]
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
    def get_rating(self, key_=0):
        
        
        ratings_ = self.get_ratings()
        if (php_isset(lambda : ratings_[key_])):
            return ratings_[key_]
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
    def get_restriction(self, key_=0):
        
        
        restrictions_ = self.get_restrictions()
        if (php_isset(lambda : restrictions_[key_])):
            return restrictions_[key_]
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
        
        
        length_ = self.get_length()
        if length_ != None:
            return round(length_ / 1048576, 2)
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
    def get_thumbnail(self, key_=0):
        
        
        thumbnails_ = self.get_thumbnails()
        if (php_isset(lambda : thumbnails_[key_])):
            return thumbnails_[key_]
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
    def native_embed(self, options_=""):
        
        
        return self.embed(options_, True)
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
    def embed(self, options_="", native_=None):
        if native_ is None:
            native_ = False
        # end if
        
        #// Set up defaults
        audio_ = ""
        video_ = ""
        alt_ = ""
        altclass_ = ""
        loop_ = "false"
        width_ = "auto"
        height_ = "auto"
        bgcolor_ = "#ffffff"
        mediaplayer_ = ""
        widescreen_ = False
        handler_ = self.get_handler()
        type_ = self.get_real_type()
        #// Process options and reassign values as necessary
        if php_is_array(options_):
            extract(options_)
        else:
            options_ = php_explode(",", options_)
            for option_ in options_:
                opt_ = php_explode(":", option_, 2)
                if (php_isset(lambda : opt_[0]) and php_isset(lambda : opt_[1])):
                    opt_[0] = php_trim(opt_[0])
                    opt_[1] = php_trim(opt_[1])
                    for case in Switch(opt_[0]):
                        if case("audio"):
                            audio_ = opt_[1]
                            break
                        # end if
                        if case("video"):
                            video_ = opt_[1]
                            break
                        # end if
                        if case("alt"):
                            alt_ = opt_[1]
                            break
                        # end if
                        if case("altclass"):
                            altclass_ = opt_[1]
                            break
                        # end if
                        if case("loop"):
                            loop_ = opt_[1]
                            break
                        # end if
                        if case("width"):
                            width_ = opt_[1]
                            break
                        # end if
                        if case("height"):
                            height_ = opt_[1]
                            break
                        # end if
                        if case("bgcolor"):
                            bgcolor_ = opt_[1]
                            break
                        # end if
                        if case("mediaplayer"):
                            mediaplayer_ = opt_[1]
                            break
                        # end if
                        if case("widescreen"):
                            widescreen_ = opt_[1]
                            break
                        # end if
                    # end for
                # end if
            # end for
        # end if
        mime_ = php_explode("/", type_, 2)
        mime_ = mime_[0]
        #// Process values for 'auto'
        if width_ == "auto":
            if mime_ == "video":
                if height_ == "auto":
                    width_ = 480
                elif widescreen_:
                    width_ = round(php_intval(height_) / 9 * 16)
                else:
                    width_ = round(php_intval(height_) / 3 * 4)
                # end if
            else:
                width_ = "100%"
            # end if
        # end if
        if height_ == "auto":
            if mime_ == "audio":
                height_ = 0
            elif mime_ == "video":
                if width_ == "auto":
                    if widescreen_:
                        height_ = 270
                    else:
                        height_ = 360
                    # end if
                elif widescreen_:
                    height_ = round(php_intval(width_) / 16 * 9)
                else:
                    height_ = round(php_intval(width_) / 4 * 3)
                # end if
            else:
                height_ = 376
            # end if
        elif mime_ == "audio":
            height_ = 0
        # end if
        #// Set proper placeholder value
        if mime_ == "audio":
            placeholder_ = audio_
        elif mime_ == "video":
            placeholder_ = video_
        # end if
        embed_ = ""
        #// Flash
        if handler_ == "flash":
            if native_:
                embed_ += "<embed src=\"" + self.get_link() + str("\" pluginspage=\"http://adobe.com/go/getflashplayer\" type=\"") + str(type_) + str("\" quality=\"high\" width=\"") + str(width_) + str("\" height=\"") + str(height_) + str("\" bgcolor=\"") + str(bgcolor_) + str("\" loop=\"") + str(loop_) + str("\"></embed>")
            else:
                embed_ += str("<script type='text/javascript'>embed_flash('") + str(bgcolor_) + str("', '") + str(width_) + str("', '") + str(height_) + str("', '") + self.get_link() + str("', '") + str(loop_) + str("', '") + str(type_) + str("');</script>")
            # end if
            #// Flash Media Player file types.
            #// Preferred handler for MP3 file types.
        elif handler_ == "fmedia" or handler_ == "mp3" and mediaplayer_ != "":
            height_ += 20
            if native_:
                embed_ += str("<embed src=\"") + str(mediaplayer_) + str("\" pluginspage=\"http://adobe.com/go/getflashplayer\" type=\"application/x-shockwave-flash\" quality=\"high\" width=\"") + str(width_) + str("\" height=\"") + str(height_) + str("\" wmode=\"transparent\" flashvars=\"file=") + rawurlencode(self.get_link() + "?file_extension=." + self.get_extension()) + str("&autostart=false&repeat=") + str(loop_) + str("&showdigits=true&showfsbutton=false\"></embed>")
            else:
                embed_ += str("<script type='text/javascript'>embed_flv('") + str(width_) + str("', '") + str(height_) + str("', '") + rawurlencode(self.get_link() + "?file_extension=." + self.get_extension()) + str("', '") + str(placeholder_) + str("', '") + str(loop_) + str("', '") + str(mediaplayer_) + str("');</script>")
            # end if
            #// QuickTime 7 file types.  Need to test with QuickTime 6.
            #// Only handle MP3's if the Flash Media Player is not present.
        elif handler_ == "quicktime" or handler_ == "mp3" and mediaplayer_ == "":
            height_ += 16
            if native_:
                if placeholder_ != "":
                    embed_ += str("<embed type=\"") + str(type_) + str("\" style=\"cursor:hand; cursor:pointer;\" href=\"") + self.get_link() + str("\" src=\"") + str(placeholder_) + str("\" width=\"") + str(width_) + str("\" height=\"") + str(height_) + str("\" autoplay=\"false\" target=\"myself\" controller=\"false\" loop=\"") + str(loop_) + str("\" scale=\"aspect\" bgcolor=\"") + str(bgcolor_) + str("\" pluginspage=\"http://apple.com/quicktime/download/\"></embed>")
                else:
                    embed_ += str("<embed type=\"") + str(type_) + str("\" style=\"cursor:hand; cursor:pointer;\" src=\"") + self.get_link() + str("\" width=\"") + str(width_) + str("\" height=\"") + str(height_) + str("\" autoplay=\"false\" target=\"myself\" controller=\"true\" loop=\"") + str(loop_) + str("\" scale=\"aspect\" bgcolor=\"") + str(bgcolor_) + str("\" pluginspage=\"http://apple.com/quicktime/download/\"></embed>")
                # end if
            else:
                embed_ += str("<script type='text/javascript'>embed_quicktime('") + str(type_) + str("', '") + str(bgcolor_) + str("', '") + str(width_) + str("', '") + str(height_) + str("', '") + self.get_link() + str("', '") + str(placeholder_) + str("', '") + str(loop_) + str("');</script>")
            # end if
            #// Windows Media
        elif handler_ == "wmedia":
            height_ += 45
            if native_:
                embed_ += "<embed type=\"application/x-mplayer2\" src=\"" + self.get_link() + str("\" autosize=\"1\" width=\"") + str(width_) + str("\" height=\"") + str(height_) + str("\" showcontrols=\"1\" showstatusbar=\"0\" showdisplay=\"0\" autostart=\"0\"></embed>")
            else:
                embed_ += str("<script type='text/javascript'>embed_wmedia('") + str(width_) + str("', '") + str(height_) + str("', '") + self.get_link() + "');</script>"
            # end if
        else:
            embed_ += "<a href=\"" + self.get_link() + "\" class=\"" + altclass_ + "\">" + alt_ + "</a>"
        # end if
        return embed_
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
    def get_real_type(self, find_handler_=None):
        if find_handler_ is None:
            find_handler_ = False
        # end if
        
        #// Mime-types by handler.
        types_flash_ = Array("application/x-shockwave-flash", "application/futuresplash")
        #// Flash
        types_fmedia_ = Array("video/flv", "video/x-flv", "flv-application/octet-stream")
        #// Flash Media Player
        types_quicktime_ = Array("audio/3gpp", "audio/3gpp2", "audio/aac", "audio/x-aac", "audio/aiff", "audio/x-aiff", "audio/mid", "audio/midi", "audio/x-midi", "audio/mp4", "audio/m4a", "audio/x-m4a", "audio/wav", "audio/x-wav", "video/3gpp", "video/3gpp2", "video/m4v", "video/x-m4v", "video/mp4", "video/mpeg", "video/x-mpeg", "video/quicktime", "video/sd-video")
        #// QuickTime
        types_wmedia_ = Array("application/asx", "application/x-mplayer2", "audio/x-ms-wma", "audio/x-ms-wax", "video/x-ms-asf-plugin", "video/x-ms-asf", "video/x-ms-wm", "video/x-ms-wmv", "video/x-ms-wvx")
        #// Windows Media
        types_mp3_ = Array("audio/mp3", "audio/x-mp3", "audio/mpeg", "audio/x-mpeg")
        #// MP3
        if self.get_type() != None:
            type_ = php_strtolower(self.type)
        else:
            type_ = None
        # end if
        #// If we encounter an unsupported mime-type, check the file extension and guess intelligently.
        if (not php_in_array(type_, php_array_merge(types_flash_, types_fmedia_, types_quicktime_, types_wmedia_, types_mp3_))):
            for case in Switch(php_strtolower(self.get_extension())):
                if case("aac"):
                    pass
                # end if
                if case("adts"):
                    type_ = "audio/acc"
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
                    type_ = "audio/aiff"
                    break
                # end if
                if case("bwf"):
                    type_ = "audio/wav"
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
                    type_ = "audio/midi"
                    break
                # end if
                if case("m4a"):
                    type_ = "audio/x-m4a"
                    break
                # end if
                if case("mp3"):
                    pass
                # end if
                if case("swa"):
                    type_ = "audio/mp3"
                    break
                # end if
                if case("wav"):
                    type_ = "audio/wav"
                    break
                # end if
                if case("wax"):
                    type_ = "audio/x-ms-wax"
                    break
                # end if
                if case("wma"):
                    type_ = "audio/x-ms-wma"
                    break
                # end if
                if case("3gp"):
                    pass
                # end if
                if case("3gpp"):
                    type_ = "video/3gpp"
                    break
                # end if
                if case("3g2"):
                    pass
                # end if
                if case("3gp2"):
                    type_ = "video/3gpp2"
                    break
                # end if
                if case("asf"):
                    type_ = "video/x-ms-asf"
                    break
                # end if
                if case("flv"):
                    type_ = "video/x-flv"
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
                    type_ = "video/mpeg"
                    break
                # end if
                if case("m4v"):
                    type_ = "video/x-m4v"
                    break
                # end if
                if case("mov"):
                    pass
                # end if
                if case("qt"):
                    type_ = "video/quicktime"
                    break
                # end if
                if case("mp4"):
                    pass
                # end if
                if case("mpg4"):
                    type_ = "video/mp4"
                    break
                # end if
                if case("sdv"):
                    type_ = "video/sd-video"
                    break
                # end if
                if case("wm"):
                    type_ = "video/x-ms-wm"
                    break
                # end if
                if case("wmv"):
                    type_ = "video/x-ms-wmv"
                    break
                # end if
                if case("wvx"):
                    type_ = "video/x-ms-wvx"
                    break
                # end if
                if case("spl"):
                    type_ = "application/futuresplash"
                    break
                # end if
                if case("swf"):
                    type_ = "application/x-shockwave-flash"
                    break
                # end if
            # end for
        # end if
        if find_handler_:
            if php_in_array(type_, types_flash_):
                return "flash"
            elif php_in_array(type_, types_fmedia_):
                return "fmedia"
            elif php_in_array(type_, types_quicktime_):
                return "quicktime"
            elif php_in_array(type_, types_wmedia_):
                return "wmedia"
            elif php_in_array(type_, types_mp3_):
                return "mp3"
            else:
                return None
            # end if
        else:
            return type_
        # end if
    # end def get_real_type
# end class SimplePie_Enclosure
