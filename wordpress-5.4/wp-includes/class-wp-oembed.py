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
#// API for fetching the HTML to embed remote content based on a provided URL
#// 
#// Used internally by the WP_Embed class, but is designed to be generic.
#// 
#// @link https://wordpress.org/support/article/embeds
#// @link http://oembed.com
#// 
#// @package WordPress
#// @subpackage oEmbed
#// 
#// 
#// Core class used to implement oEmbed functionality.
#// 
#// @since 2.9.0
#//
class WP_oEmbed():
    #// 
    #// A list of oEmbed providers.
    #// 
    #// @since 2.9.0
    #// @var array
    #//
    providers = Array()
    #// 
    #// A list of an early oEmbed providers.
    #// 
    #// @since 4.0.0
    #// @var array
    #//
    early_providers = Array()
    #// 
    #// A list of private/protected methods, used for backward compatibility.
    #// 
    #// @since 4.2.0
    #// @var array
    #//
    compat_methods = Array("_fetch_with_format", "_parse_json", "_parse_xml", "_parse_xml_body")
    #// 
    #// Constructor.
    #// 
    #// @since 2.9.0
    #//
    def __init__(self):
        
        
        host_ = urlencode(home_url())
        providers_ = Array({"#https?://((m|www)\\.)?youtube\\.com/watch.*#i": Array("https://www.youtube.com/oembed", True), "#https?://((m|www)\\.)?youtube\\.com/playlist.*#i": Array("https://www.youtube.com/oembed", True), "#https?://youtu\\.be/.*#i": Array("https://www.youtube.com/oembed", True), "#https?://(.+\\.)?vimeo\\.com/.*#i": Array("https://vimeo.com/api/oembed.{format}", True)}, {"#https?://(www\\.)?dailymotion\\.com/.*#i": Array("https://www.dailymotion.com/services/oembed", True), "#https?://dai\\.ly/.*#i": Array("https://www.dailymotion.com/services/oembed", True), "#https?://(www\\.)?flickr\\.com/.*#i": Array("https://www.flickr.com/services/oembed/", True), "#https?://flic\\.kr/.*#i": Array("https://www.flickr.com/services/oembed/", True), "#https?://(.+\\.)?smugmug\\.com/.*#i": Array("https://api.smugmug.com/services/oembed/", True), "#https?://(www\\.)?hulu\\.com/watch/.*#i": Array("https://www.hulu.com/api/oembed.{format}", True)}, {"#https?://(www\\.)?scribd\\.com/(doc|document)/.*#i": Array("https://www.scribd.com/services/oembed", True), "#https?://wordpress\\.tv/.*#i": Array("https://wordpress.tv/oembed/", True), "#https?://(.+\\.)?polldaddy\\.com/.*#i": Array("https://api.crowdsignal.com/oembed", True), "#https?://poll\\.fm/.*#i": Array("https://api.crowdsignal.com/oembed", True), "#https?://(.+\\.)?survey\\.fm/.*#i": Array("https://api.crowdsignal.com/oembed", True), "#https?://(www\\.)?twitter\\.com/\\w{1,15}/status(es)?/.*#i": Array("https://publish.twitter.com/oembed", True)}, {"#https?://(www\\.)?twitter\\.com/\\w{1,15}$#i": Array("https://publish.twitter.com/oembed", True)}, {"#https?://(www\\.)?twitter\\.com/\\w{1,15}/likes$#i": Array("https://publish.twitter.com/oembed", True)}, {"#https?://(www\\.)?twitter\\.com/\\w{1,15}/lists/.*#i": Array("https://publish.twitter.com/oembed", True)}, {"#https?://(www\\.)?twitter\\.com/\\w{1,15}/timelines/.*#i": Array("https://publish.twitter.com/oembed", True)}, {"#https?://(www\\.)?twitter\\.com/i/moments/.*#i": Array("https://publish.twitter.com/oembed", True), "#https?://(www\\.)?soundcloud\\.com/.*#i": Array("https://soundcloud.com/oembed", True), "#https?://(.+?\\.)?slideshare\\.net/.*#i": Array("https://www.slideshare.net/api/oembed/2", True), "#https?://(www\\.)?instagr(\\.am|am\\.com)/(p|tv)/.*#i": Array("https://api.instagram.com/oembed", True), "#https?://(open|play)\\.spotify\\.com/.*#i": Array("https://embed.spotify.com/oembed/", True), "#https?://(.+\\.)?imgur\\.com/.*#i": Array("https://api.imgur.com/oembed", True), "#https?://(www\\.)?meetu(\\.ps|p\\.com)/.*#i": Array("https://api.meetup.com/oembed", True), "#https?://(www\\.)?issuu\\.com/.+/docs/.+#i": Array("https://issuu.com/oembed_wp", True), "#https?://(www\\.)?mixcloud\\.com/.*#i": Array("https://www.mixcloud.com/oembed", True), "#https?://(www\\.|embed\\.)?ted\\.com/talks/.*#i": Array("https://www.ted.com/services/v1/oembed.{format}", True)}, {"#https?://(www\\.)?(animoto|video214)\\.com/play/.*#i": Array("https://animoto.com/oembeds/create", True), "#https?://(.+)\\.tumblr\\.com/post/.*#i": Array("https://www.tumblr.com/oembed/1.0", True), "#https?://(www\\.)?kickstarter\\.com/projects/.*#i": Array("https://www.kickstarter.com/services/oembed", True), "#https?://kck\\.st/.*#i": Array("https://www.kickstarter.com/services/oembed", True), "#https?://cloudup\\.com/.*#i": Array("https://cloudup.com/oembed", True), "#https?://(www\\.)?reverbnation\\.com/.*#i": Array("https://www.reverbnation.com/oembed", True), "#https?://videopress\\.com/v/.*#": Array("https://public-api.wordpress.com/oembed/?for=" + host_, True), "#https?://(www\\.)?reddit\\.com/r/[^/]+/comments/.*#i": Array("https://www.reddit.com/oembed", True), "#https?://(www\\.)?speakerdeck\\.com/.*#i": Array("https://speakerdeck.com/oembed.{format}", True)}, {"#https?://www\\.facebook\\.com/.*/posts/.*#i": Array("https://www.facebook.com/plugins/post/oembed.json/", True), "#https?://www\\.facebook\\.com/.*/activity/.*#i": Array("https://www.facebook.com/plugins/post/oembed.json/", True), "#https?://www\\.facebook\\.com/.*/photos/.*#i": Array("https://www.facebook.com/plugins/post/oembed.json/", True), "#https?://www\\.facebook\\.com/photo(s/|\\.php).*#i": Array("https://www.facebook.com/plugins/post/oembed.json/", True), "#https?://www\\.facebook\\.com/permalink\\.php.*#i": Array("https://www.facebook.com/plugins/post/oembed.json/", True), "#https?://www\\.facebook\\.com/media/.*#i": Array("https://www.facebook.com/plugins/post/oembed.json/", True), "#https?://www\\.facebook\\.com/questions/.*#i": Array("https://www.facebook.com/plugins/post/oembed.json/", True), "#https?://www\\.facebook\\.com/notes/.*#i": Array("https://www.facebook.com/plugins/post/oembed.json/", True), "#https?://www\\.facebook\\.com/.*/videos/.*#i": Array("https://www.facebook.com/plugins/video/oembed.json/", True), "#https?://www\\.facebook\\.com/video\\.php.*#i": Array("https://www.facebook.com/plugins/video/oembed.json/", True), "#https?://(www\\.)?screencast\\.com/.*#i": Array("https://api.screencast.com/external/oembed", True), "#https?://([a-z0-9-]+\\.)?amazon\\.(com|com\\.mx|com\\.br|ca)/.*#i": Array("https://read.amazon.com/kp/api/oembed", True), "#https?://([a-z0-9-]+\\.)?amazon\\.(co\\.uk|de|fr|it|es|in|nl|ru)/.*#i": Array("https://read.amazon.co.uk/kp/api/oembed", True), "#https?://([a-z0-9-]+\\.)?amazon\\.(co\\.jp|com\\.au)/.*#i": Array("https://read.amazon.com.au/kp/api/oembed", True), "#https?://([a-z0-9-]+\\.)?amazon\\.cn/.*#i": Array("https://read.amazon.cn/kp/api/oembed", True), "#https?://(www\\.)?a\\.co/.*#i": Array("https://read.amazon.com/kp/api/oembed", True), "#https?://(www\\.)?amzn\\.to/.*#i": Array("https://read.amazon.com/kp/api/oembed", True), "#https?://(www\\.)?amzn\\.eu/.*#i": Array("https://read.amazon.co.uk/kp/api/oembed", True), "#https?://(www\\.)?amzn\\.in/.*#i": Array("https://read.amazon.in/kp/api/oembed", True), "#https?://(www\\.)?amzn\\.asia/.*#i": Array("https://read.amazon.com.au/kp/api/oembed", True), "#https?://(www\\.)?z\\.cn/.*#i": Array("https://read.amazon.cn/kp/api/oembed", True), "#https?://www\\.someecards\\.com/.+-cards/.+#i": Array("https://www.someecards.com/v2/oembed/", True), "#https?://www\\.someecards\\.com/usercards/viewcard/.+#i": Array("https://www.someecards.com/v2/oembed/", True), "#https?://some\\.ly\\/.+#i": Array("https://www.someecards.com/v2/oembed/", True), "#https?://(www\\.)?tiktok\\.com/.*/video/.*#i": Array("https://www.tiktok.com/oembed", True)})
        if (not php_empty(lambda : self.early_providers["add"])):
            for format_,data_ in self.early_providers["add"].items():
                providers_[format_] = data_
            # end for
        # end if
        if (not php_empty(lambda : self.early_providers["remove"])):
            for format_ in self.early_providers["remove"]:
                providers_[format_] = None
            # end for
        # end if
        self.early_providers = Array()
        #// 
        #// Filters the list of whitelisted oEmbed providers.
        #// 
        #// Since WordPress 4.4, oEmbed discovery is enabled for all users and allows embedding of sanitized
        #// iframes. The providers in this list are whitelisted, meaning they are trusted and allowed to
        #// embed any content, such as iframes, videos, JavaScript, and arbitrary HTML.
        #// 
        #// Supported providers:
        #// 
        #// |   Provider   |                     Flavor                |  Since  |
        #// | ------------ | ----------------------------------------- | ------- |
        #// | Dailymotion  | dailymotion.com                           | 2.9.0   |
        #// | Flickr       | flickr.com                                | 2.9.0   |
        #// | Hulu         | hulu.com                                  | 2.9.0   |
        #// | Scribd       | scribd.com                                | 2.9.0   |
        #// | Vimeo        | vimeo.com                                 | 2.9.0   |
        #// | WordPress.tv | wordpress.tv                              | 2.9.0   |
        #// | YouTube      | youtube.com/watch                         | 2.9.0   |
        #// | Crowdsignal  | polldaddy.com                             | 3.0.0   |
        #// | SmugMug      | smugmug.com                               | 3.0.0   |
        #// | YouTube      | youtu.be                                  | 3.0.0   |
        #// | Twitter      | twitter.com                               | 3.4.0   |
        #// | Instagram    | instagram.com                             | 3.5.0   |
        #// | Instagram    | instagr.am                                | 3.5.0   |
        #// | Slideshare   | slideshare.net                            | 3.5.0   |
        #// | SoundCloud   | soundcloud.com                            | 3.5.0   |
        #// | Dailymotion  | dai.ly                                    | 3.6.0   |
        #// | Flickr       | flic.kr                                   | 3.6.0   |
        #// | Spotify      | spotify.com                               | 3.6.0   |
        #// | Imgur        | imgur.com                                 | 3.9.0   |
        #// | Meetup.com   | meetup.com                                | 3.9.0   |
        #// | Meetup.com   | meetu.ps                                  | 3.9.0   |
        #// | Animoto      | animoto.com                               | 4.0.0   |
        #// | Animoto      | video214.com                              | 4.0.0   |
        #// | Issuu        | issuu.com                                 | 4.0.0   |
        #// | Mixcloud     | mixcloud.com                              | 4.0.0   |
        #// | Crowdsignal  | poll.fm                                   | 4.0.0   |
        #// | TED          | ted.com                                   | 4.0.0   |
        #// | YouTube      | youtube.com/playlist                      | 4.0.0   |
        #// | Tumblr       | tumblr.com                                | 4.2.0   |
        #// | Kickstarter  | kickstarter.com                           | 4.2.0   |
        #// | Kickstarter  | kck.st                                    | 4.2.0   |
        #// | Cloudup      | cloudup.com                               | 4.3.0   |
        #// | ReverbNation | reverbnation.com                          | 4.4.0   |
        #// | VideoPress   | videopress.com                            | 4.4.0   |
        #// | Reddit       | reddit.com                                | 4.4.0   |
        #// | Speaker Deck | speakerdeck.com                           | 4.4.0   |
        #// | Twitter      | twitter.com/timelines                     | 4.5.0   |
        #// | Twitter      | twitter.com/moments                       | 4.5.0   |
        #// | Facebook     | facebook.com                              | 4.7.0   |
        #// | Twitter      | twitter.com/user                          | 4.7.0   |
        #// | Twitter      | twitter.com/likes                         | 4.7.0   |
        #// | Twitter      | twitter.com/lists                         | 4.7.0   |
        #// | Screencast   | screencast.com                            | 4.8.0   |
        #// | Amazon       | amazon.com (com.mx, com.br, ca)           | 4.9.0   |
        #// | Amazon       | amazon.de (fr, it, es, in, nl, ru, co.uk) | 4.9.0   |
        #// | Amazon       | amazon.co.jp (com.au)                     | 4.9.0   |
        #// | Amazon       | amazon.cn                                 | 4.9.0   |
        #// | Amazon       | a.co                                      | 4.9.0   |
        #// | Amazon       | amzn.to (eu, in, asia)                    | 4.9.0   |
        #// | Amazon       | z.cn                                      | 4.9.0   |
        #// | Someecards   | someecards.com                            | 4.9.0   |
        #// | Someecards   | some.ly                                   | 4.9.0   |
        #// | Crowdsignal  | survey.fm                                 | 5.1.0   |
        #// | Instagram TV | instagram.com                             | 5.1.0   |
        #// | Instagram TV | instagr.am                                | 5.1.0   |
        #// | TikTok       | tiktok.com                                | 5.4.0   |
        #// 
        #// No longer supported providers:
        #// 
        #// |   Provider   |        Flavor        |   Since   |  Removed  |
        #// | ------------ | -------------------- | --------- | --------- |
        #// | Qik          | qik.com              | 2.9.0     | 3.9.0     |
        #// | Viddler      | viddler.com          | 2.9.0     | 4.0.0     |
        #// | Revision3    | revision3.com        | 2.9.0     | 4.2.0     |
        #// | Blip         | blip.tv              | 2.9.0     | 4.4.0     |
        #// | Rdio         | rdio.com             | 3.6.0     | 4.4.1     |
        #// | Rdio         | rd.io                | 3.6.0     | 4.4.1     |
        #// | Vine         | vine.co              | 4.1.0     | 4.9.0     |
        #// | Photobucket  | photobucket.com      | 2.9.0     | 5.1.0     |
        #// | Funny or Die | funnyordie.com       | 3.0.0     | 5.1.0     |
        #// | CollegeHumor | collegehumor.com     | 4.0.0     | 5.3.1     |
        #// 
        #// @see wp_oembed_add_provider()
        #// 
        #// @since 2.9.0
        #// 
        #// @param array[] $providers An array of arrays containing data about popular oEmbed providers.
        #//
        self.providers = apply_filters("oembed_providers", providers_)
        #// Fix any embeds that contain new lines in the middle of the HTML which breaks wpautop().
        add_filter("oembed_dataparse", Array(self, "_strip_newlines"), 10, 3)
    # end def __init__
    #// 
    #// Exposes private/protected methods for backward compatibility.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string   $name      Method to call.
    #// @param array    $arguments Arguments to pass when calling.
    #// @return mixed|bool Return value of the callback, false otherwise.
    #//
    def __call(self, name_=None, arguments_=None):
        
        
        if php_in_array(name_, self.compat_methods):
            return self.name_(arguments_)
        # end if
        return False
    # end def __call
    #// 
    #// Takes a URL and returns the corresponding oEmbed provider's URL, if there is one.
    #// 
    #// @since 4.0.0
    #// 
    #// @see WP_oEmbed::discover()
    #// 
    #// @param string        $url  The URL to the content.
    #// @param string|array  $args Optional provider arguments.
    #// @return string|false The oEmbed provider URL on success, false on failure.
    #//
    def get_provider(self, url_=None, args_=""):
        
        
        args_ = wp_parse_args(args_)
        provider_ = False
        if (not (php_isset(lambda : args_["discover"]))):
            args_["discover"] = True
        # end if
        for matchmask_,data_ in self.providers.items():
            providerurl_, regex_ = data_
            #// Turn the asterisk-type provider URLs into regex.
            if (not regex_):
                matchmask_ = "#" + php_str_replace("___wildcard___", "(.+)", preg_quote(php_str_replace("*", "___wildcard___", matchmask_), "#")) + "#i"
                matchmask_ = php_preg_replace("|^#http\\\\://|", "#https?\\://", matchmask_)
            # end if
            if php_preg_match(matchmask_, url_):
                provider_ = php_str_replace("{format}", "json", providerurl_)
                break
            # end if
        # end for
        if (not provider_) and args_["discover"]:
            provider_ = self.discover(url_)
        # end if
        return provider_
    # end def get_provider
    #// 
    #// Adds an oEmbed provider.
    #// 
    #// The provider is added just-in-time when wp_oembed_add_provider() is called before
    #// the {@see 'plugins_loaded'} hook.
    #// 
    #// The just-in-time addition is for the benefit of the {@see 'oembed_providers'} filter.
    #// 
    #// @since 4.0.0
    #// 
    #// @see wp_oembed_add_provider()
    #// 
    #// @param string $format   Format of URL that this provider can handle. You can use
    #// asterisks as wildcards.
    #// @param string $provider The URL to the oEmbed provider..
    #// @param bool   $regex    Optional. Whether the $format parameter is in a regex format.
    #// Default false.
    #//
    @classmethod
    def _add_provider_early(self, format_=None, provider_=None, regex_=None):
        if regex_ is None:
            regex_ = False
        # end if
        
        if php_empty(lambda : self.early_providers["add"]):
            self.early_providers["add"] = Array()
        # end if
        self.early_providers["add"][format_] = Array(provider_, regex_)
    # end def _add_provider_early
    #// 
    #// Removes an oEmbed provider.
    #// 
    #// The provider is removed just-in-time when wp_oembed_remove_provider() is called before
    #// the {@see 'plugins_loaded'} hook.
    #// 
    #// The just-in-time removal is for the benefit of the {@see 'oembed_providers'} filter.
    #// 
    #// @since 4.0.0
    #// 
    #// @see wp_oembed_remove_provider()
    #// 
    #// @param string $format The format of URL that this provider can handle. You can use
    #// asterisks as wildcards.
    #//
    @classmethod
    def _remove_provider_early(self, format_=None):
        
        
        if php_empty(lambda : self.early_providers["remove"]):
            self.early_providers["remove"] = Array()
        # end if
        self.early_providers["remove"][-1] = format_
    # end def _remove_provider_early
    #// 
    #// Takes a URL and attempts to return the oEmbed data.
    #// 
    #// @see WP_oEmbed::fetch()
    #// 
    #// @since 4.8.0
    #// 
    #// @param string       $url  The URL to the content that should be attempted to be embedded.
    #// @param array|string $args Optional. Arguments, usually passed from a shortcode. Default empty.
    #// @return object|false The result in the form of an object on success, false on failure.
    #//
    def get_data(self, url_=None, args_=""):
        
        
        args_ = wp_parse_args(args_)
        provider_ = self.get_provider(url_, args_)
        if (not provider_):
            return False
        # end if
        data_ = self.fetch(provider_, url_, args_)
        if False == data_:
            return False
        # end if
        return data_
    # end def get_data
    #// 
    #// The do-it-all function that takes a URL and attempts to return the HTML.
    #// 
    #// @see WP_oEmbed::fetch()
    #// @see WP_oEmbed::data2html()
    #// 
    #// @since 2.9.0
    #// 
    #// @param string       $url  The URL to the content that should be attempted to be embedded.
    #// @param array|string $args Optional. Arguments, usually passed from a shortcode. Default empty.
    #// @return string|false The UNSANITIZED (and potentially unsafe) HTML that should be used to embed on success,
    #// false on failure.
    #//
    def get_html(self, url_=None, args_=""):
        
        
        #// 
        #// Filters the oEmbed result before any HTTP requests are made.
        #// 
        #// This allows one to short-circuit the default logic, perhaps by
        #// replacing it with a routine that is more optimal for your setup.
        #// 
        #// Passing a non-null value to the filter will effectively short-circuit retrieval,
        #// returning the passed value instead.
        #// 
        #// @since 4.5.3
        #// 
        #// @param null|string $result The UNSANITIZED (and potentially unsafe) HTML that should be used to embed.
        #// Default null to continue retrieving the result.
        #// @param string      $url    The URL to the content that should be attempted to be embedded.
        #// @param array       $args   Optional. Arguments, usually passed from a shortcode. Default empty.
        #//
        pre_ = apply_filters("pre_oembed_result", None, url_, args_)
        if None != pre_:
            return pre_
        # end if
        data_ = self.get_data(url_, args_)
        if False == data_:
            return False
        # end if
        #// 
        #// Filters the HTML returned by the oEmbed provider.
        #// 
        #// @since 2.9.0
        #// 
        #// @param string|false $data The returned oEmbed HTML (false if unsafe).
        #// @param string       $url  URL of the content to be embedded.
        #// @param array        $args Optional arguments, usually passed from a shortcode.
        #//
        return apply_filters("oembed_result", self.data2html(data_, url_), url_, args_)
    # end def get_html
    #// 
    #// Attempts to discover link tags at the given URL for an oEmbed provider.
    #// 
    #// @since 2.9.0
    #// 
    #// @param string $url The URL that should be inspected for discovery `<link>` tags.
    #// @return string|false The oEmbed provider URL on success, false on failure.
    #//
    def discover(self, url_=None):
        
        
        providers_ = Array()
        args_ = Array({"limit_response_size": 153600})
        #// 
        #// Filters oEmbed remote get arguments.
        #// 
        #// @since 4.0.0
        #// 
        #// @see WP_Http::request()
        #// 
        #// @param array  $args oEmbed remote get arguments.
        #// @param string $url  URL to be inspected.
        #//
        args_ = apply_filters("oembed_remote_get_args", args_, url_)
        #// Fetch URL content.
        request_ = wp_safe_remote_get(url_, args_)
        html_ = wp_remote_retrieve_body(request_)
        if html_:
            #// 
            #// Filters the link types that contain oEmbed provider URLs.
            #// 
            #// @since 2.9.0
            #// 
            #// @param string[] $format Array of oEmbed link types. Accepts 'application/json+oembed',
            #// 'text/xml+oembed', and 'application/xml+oembed' (incorrect,
            #// used by at least Vimeo).
            #//
            linktypes_ = apply_filters("oembed_linktypes", Array({"application/json+oembed": "json", "text/xml+oembed": "xml", "application/xml+oembed": "xml"}))
            #// Strip <body>.
            html_head_end_ = php_stripos(html_, "</head>")
            if html_head_end_:
                html_ = php_substr(html_, 0, html_head_end_)
            # end if
            #// Do a quick check.
            tagfound_ = False
            for linktype_,format_ in linktypes_.items():
                if php_stripos(html_, linktype_):
                    tagfound_ = True
                    break
                # end if
            # end for
            if tagfound_ and preg_match_all("#<link([^<>]+)/?>#iU", html_, links_):
                for link_ in links_[1]:
                    atts_ = shortcode_parse_atts(link_)
                    if (not php_empty(lambda : atts_["type"])) and (not php_empty(lambda : linktypes_[atts_["type"]])) and (not php_empty(lambda : atts_["href"])):
                        providers_[linktypes_[atts_["type"]]] = htmlspecialchars_decode(atts_["href"])
                        #// Stop here if it's JSON (that's all we need).
                        if "json" == linktypes_[atts_["type"]]:
                            break
                        # end if
                    # end if
                # end for
            # end if
        # end if
        #// JSON is preferred to XML.
        if (not php_empty(lambda : providers_["json"])):
            return providers_["json"]
        elif (not php_empty(lambda : providers_["xml"])):
            return providers_["xml"]
        else:
            return False
        # end if
    # end def discover
    #// 
    #// Connects to a oEmbed provider and returns the result.
    #// 
    #// @since 2.9.0
    #// 
    #// @param string       $provider The URL to the oEmbed provider.
    #// @param string       $url      The URL to the content that is desired to be embedded.
    #// @param array|string $args     Optional. Arguments, usually passed from a shortcode. Default empty.
    #// @return object|false The result in the form of an object on success, false on failure.
    #//
    def fetch(self, provider_=None, url_=None, args_=""):
        
        
        args_ = wp_parse_args(args_, wp_embed_defaults(url_))
        provider_ = add_query_arg("maxwidth", php_int(args_["width"]), provider_)
        provider_ = add_query_arg("maxheight", php_int(args_["height"]), provider_)
        provider_ = add_query_arg("url", urlencode(url_), provider_)
        provider_ = add_query_arg("dnt", 1, provider_)
        #// 
        #// Filters the oEmbed URL to be fetched.
        #// 
        #// @since 2.9.0
        #// @since 4.9.0 The `dnt` (Do Not Track) query parameter was added to all oEmbed provider URLs.
        #// 
        #// @param string $provider URL of the oEmbed provider.
        #// @param string $url      URL of the content to be embedded.
        #// @param array  $args     Optional arguments, usually passed from a shortcode.
        #//
        provider_ = apply_filters("oembed_fetch_url", provider_, url_, args_)
        for format_ in Array("json", "xml"):
            result_ = self._fetch_with_format(provider_, format_)
            if is_wp_error(result_) and "not-implemented" == result_.get_error_code():
                continue
            # end if
            return result_ if result_ and (not is_wp_error(result_)) else False
        # end for
        return False
    # end def fetch
    #// 
    #// Fetches result from an oEmbed provider for a specific format and complete provider URL
    #// 
    #// @since 3.0.0
    #// 
    #// @param string $provider_url_with_args URL to the provider with full arguments list (url, maxheight, etc.)
    #// @param string $format                 Format to use.
    #// @return object|false|WP_Error The result in the form of an object on success, false on failure.
    #//
    def _fetch_with_format(self, provider_url_with_args_=None, format_=None):
        
        
        provider_url_with_args_ = add_query_arg("format", format_, provider_url_with_args_)
        #// This filter is documented in wp-includes/class-wp-oembed.php
        args_ = apply_filters("oembed_remote_get_args", Array(), provider_url_with_args_)
        response_ = wp_safe_remote_get(provider_url_with_args_, args_)
        if 501 == wp_remote_retrieve_response_code(response_):
            return php_new_class("WP_Error", lambda : WP_Error("not-implemented"))
        # end if
        body_ = wp_remote_retrieve_body(response_)
        if (not body_):
            return False
        # end if
        parse_method_ = str("_parse_") + str(format_)
        return self.parse_method_(body_)
    # end def _fetch_with_format
    #// 
    #// Parses a json response body.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string $response_body
    #// @return object|false
    #//
    def _parse_json(self, response_body_=None):
        
        
        data_ = php_json_decode(php_trim(response_body_))
        return data_ if data_ and php_is_object(data_) else False
    # end def _parse_json
    #// 
    #// Parses an XML response body.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string $response_body
    #// @return object|false
    #//
    def _parse_xml(self, response_body_=None):
        
        
        if (not php_function_exists("libxml_disable_entity_loader")):
            return False
        # end if
        loader_ = libxml_disable_entity_loader(True)
        errors_ = libxml_use_internal_errors(True)
        return_ = self._parse_xml_body(response_body_)
        libxml_use_internal_errors(errors_)
        libxml_disable_entity_loader(loader_)
        return return_
    # end def _parse_xml
    #// 
    #// Serves as a helper function for parsing an XML response body.
    #// 
    #// @since 3.6.0
    #// 
    #// @param string $response_body
    #// @return stdClass|false
    #//
    def _parse_xml_body(self, response_body_=None):
        
        
        if (not php_function_exists("simplexml_import_dom")) or (not php_class_exists("DOMDocument", False)):
            return False
        # end if
        dom_ = php_new_class("DOMDocument", lambda : DOMDocument())
        success_ = dom_.loadxml(response_body_)
        if (not success_):
            return False
        # end if
        if (php_isset(lambda : dom_.doctype)):
            return False
        # end if
        for child_ in dom_.childNodes:
            if XML_DOCUMENT_TYPE_NODE == child_.nodeType:
                return False
            # end if
        # end for
        xml_ = simplexml_import_dom(dom_)
        if (not xml_):
            return False
        # end if
        return_ = php_new_class("stdClass", lambda : stdClass())
        for key_,value_ in xml_.items():
            return_.key_ = php_str(value_)
        # end for
        return return_
    # end def _parse_xml_body
    #// 
    #// Converts a data object from WP_oEmbed::fetch() and returns the HTML.
    #// 
    #// @since 2.9.0
    #// 
    #// @param object $data A data object result from an oEmbed provider.
    #// @param string $url  The URL to the content that is desired to be embedded.
    #// @return string|false The HTML needed to embed on success, false on failure.
    #//
    def data2html(self, data_=None, url_=None):
        
        
        if (not php_is_object(data_)) or php_empty(lambda : data_.type):
            return False
        # end if
        return_ = False
        for case in Switch(data_.type):
            if case("photo"):
                if php_empty(lambda : data_.url) or php_empty(lambda : data_.width) or php_empty(lambda : data_.height):
                    break
                # end if
                if (not php_is_string(data_.url)) or (not php_is_numeric(data_.width)) or (not php_is_numeric(data_.height)):
                    break
                # end if
                title_ = data_.title if (not php_empty(lambda : data_.title)) and php_is_string(data_.title) else ""
                return_ = "<a href=\"" + esc_url(url_) + "\"><img src=\"" + esc_url(data_.url) + "\" alt=\"" + esc_attr(title_) + "\" width=\"" + esc_attr(data_.width) + "\" height=\"" + esc_attr(data_.height) + "\" /></a>"
                break
            # end if
            if case("video"):
                pass
            # end if
            if case("rich"):
                if (not php_empty(lambda : data_.html)) and php_is_string(data_.html):
                    return_ = data_.html
                # end if
                break
            # end if
            if case("link"):
                if (not php_empty(lambda : data_.title)) and php_is_string(data_.title):
                    return_ = "<a href=\"" + esc_url(url_) + "\">" + esc_html(data_.title) + "</a>"
                # end if
                break
            # end if
            if case():
                return_ = False
            # end if
        # end for
        #// 
        #// Filters the returned oEmbed HTML.
        #// 
        #// Use this filter to add support for custom data types, or to filter the result.
        #// 
        #// @since 2.9.0
        #// 
        #// @param string $return The returned oEmbed HTML.
        #// @param object $data   A data object result from an oEmbed provider.
        #// @param string $url    The URL of the content to be embedded.
        #//
        return apply_filters("oembed_dataparse", return_, data_, url_)
    # end def data2html
    #// 
    #// Strips any new lines from the HTML.
    #// 
    #// @since 2.9.0 as strip_scribd_newlines()
    #// @since 3.0.0
    #// 
    #// @param string $html Existing HTML.
    #// @param object $data Data object from WP_oEmbed::data2html()
    #// @param string $url The original URL passed to oEmbed.
    #// @return string Possibly modified $html
    #//
    def _strip_newlines(self, html_=None, data_=None, url_=None):
        
        
        if False == php_strpos(html_, "\n"):
            return html_
        # end if
        count_ = 1
        found_ = Array()
        token_ = "__PRE__"
        search_ = Array("   ", "\n", "\r", " ")
        replace_ = Array("__TAB__", "__NL__", "__CR__", "__SPACE__")
        tokenized_ = php_str_replace(search_, replace_, html_)
        preg_match_all("#(<pre[^>]*>.+?</pre>)#i", tokenized_, matches_, PREG_SET_ORDER)
        for i_,match_ in matches_.items():
            tag_html_ = php_str_replace(replace_, search_, match_[0])
            tag_token_ = token_ + i_
            found_[tag_token_] = tag_html_
            html_ = php_str_replace(tag_html_, tag_token_, html_, count_)
        # end for
        replaced_ = php_str_replace(replace_, search_, html_)
        stripped_ = php_str_replace(Array("\r\n", "\n"), "", replaced_)
        pre_ = php_array_values(found_)
        tokens_ = php_array_keys(found_)
        return php_str_replace(tokens_, pre_, stripped_)
    # end def _strip_newlines
# end class WP_oEmbed
