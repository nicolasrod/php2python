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
#// HTTP API: WP_HTTP_Proxy class
#// 
#// @package WordPress
#// @subpackage HTTP
#// @since 4.4.0
#// 
#// 
#// Core class used to implement HTTP API proxy support.
#// 
#// There are caveats to proxy support. It requires that defines be made in the wp-config.php file to
#// enable proxy support. There are also a few filters that plugins can hook into for some of the
#// constants.
#// 
#// Please note that only BASIC authentication is supported by most transports.
#// cURL MAY support more methods (such as NTLM authentication) depending on your environment.
#// 
#// The constants are as follows:
#// <ol>
#// <li>WP_PROXY_HOST - Enable proxy support and host for connecting.</li>
#// <li>WP_PROXY_PORT - Proxy port for connection. No default, must be defined.</li>
#// <li>WP_PROXY_USERNAME - Proxy username, if it requires authentication.</li>
#// <li>WP_PROXY_PASSWORD - Proxy password, if it requires authentication.</li>
#// <li>WP_PROXY_BYPASS_HOSTS - Will prevent the hosts in this list from going through the proxy.
#// You do not need to have localhost and the site host in this list, because they will not be passed
#// through the proxy. The list should be presented in a comma separated list, wildcards using * are supported, eg. *.wordpress.org</li>
#// </ol>
#// 
#// An example can be as seen below.
#// 
#// define('WP_PROXY_HOST', '192.168.84.101');
#// define('WP_PROXY_PORT', '8080');
#// define('WP_PROXY_BYPASS_HOSTS', 'localhost, www.example.com, *.wordpress.org');
#// 
#// @link https://core.trac.wordpress.org/ticket/4011 Proxy support ticket in WordPress.
#// @link https://core.trac.wordpress.org/ticket/14636 Allow wildcard domains in WP_PROXY_BYPASS_HOSTS
#// 
#// @since 2.8.0
#//
class WP_HTTP_Proxy():
    #// 
    #// Whether proxy connection should be used.
    #// 
    #// @since 2.8.0
    #// 
    #// @use WP_PROXY_HOST
    #// @use WP_PROXY_PORT
    #// 
    #// @return bool
    #//
    def is_enabled(self):
        
        
        return php_defined("WP_PROXY_HOST") and php_defined("WP_PROXY_PORT")
    # end def is_enabled
    #// 
    #// Whether authentication should be used.
    #// 
    #// @since 2.8.0
    #// 
    #// @use WP_PROXY_USERNAME
    #// @use WP_PROXY_PASSWORD
    #// 
    #// @return bool
    #//
    def use_authentication(self):
        
        
        return php_defined("WP_PROXY_USERNAME") and php_defined("WP_PROXY_PASSWORD")
    # end def use_authentication
    #// 
    #// Retrieve the host for the proxy server.
    #// 
    #// @since 2.8.0
    #// 
    #// @return string
    #//
    def host(self):
        
        
        if php_defined("WP_PROXY_HOST"):
            return WP_PROXY_HOST
        # end if
        return ""
    # end def host
    #// 
    #// Retrieve the port for the proxy server.
    #// 
    #// @since 2.8.0
    #// 
    #// @return string
    #//
    def port(self):
        
        
        if php_defined("WP_PROXY_PORT"):
            return WP_PROXY_PORT
        # end if
        return ""
    # end def port
    #// 
    #// Retrieve the username for proxy authentication.
    #// 
    #// @since 2.8.0
    #// 
    #// @return string
    #//
    def username(self):
        
        
        if php_defined("WP_PROXY_USERNAME"):
            return WP_PROXY_USERNAME
        # end if
        return ""
    # end def username
    #// 
    #// Retrieve the password for proxy authentication.
    #// 
    #// @since 2.8.0
    #// 
    #// @return string
    #//
    def password(self):
        
        
        if php_defined("WP_PROXY_PASSWORD"):
            return WP_PROXY_PASSWORD
        # end if
        return ""
    # end def password
    #// 
    #// Retrieve authentication string for proxy authentication.
    #// 
    #// @since 2.8.0
    #// 
    #// @return string
    #//
    def authentication(self):
        
        
        return self.username() + ":" + self.password()
    # end def authentication
    #// 
    #// Retrieve header string for proxy authentication.
    #// 
    #// @since 2.8.0
    #// 
    #// @return string
    #//
    def authentication_header(self):
        
        
        return "Proxy-Authorization: Basic " + php_base64_encode(self.authentication())
    # end def authentication_header
    #// 
    #// Determines whether the request should be sent through a proxy.
    #// 
    #// We want to keep localhost and the site URL from being sent through the proxy, because
    #// some proxies can not handle this. We also have the constant available for defining other
    #// hosts that won't be sent through the proxy.
    #// 
    #// @since 2.8.0
    #// 
    #// @staticvar array|null $bypass_hosts
    #// @staticvar array      $wildcard_regex
    #// 
    #// @param string $uri URI to check.
    #// @return bool True, to send through the proxy and false if, the proxy should not be used.
    #//
    def send_through_proxy(self, uri_=None):
        
        
        #// 
        #// parse_url() only handles http, https type URLs, and will emit E_WARNING on failure.
        #// This will be displayed on sites, which is not reasonable.
        #//
        check_ = php_no_error(lambda: php_parse_url(uri_))
        #// Malformed URL, can not process, but this could mean ssl, so let through anyway.
        if False == check_:
            return True
        # end if
        home_ = php_parse_url(get_option("siteurl"))
        #// 
        #// Filters whether to preempt sending the request through the proxy.
        #// 
        #// Returning false will bypass the proxy; returning true will send
        #// the request through the proxy. Returning null bypasses the filter.
        #// 
        #// @since 3.5.0
        #// 
        #// @param bool|null $override Whether to override the request result. Default null.
        #// @param string    $uri      URL to check.
        #// @param array     $check    Associative array result of parsing the request URI.
        #// @param array     $home     Associative array result of parsing the site URL.
        #//
        result_ = apply_filters("pre_http_send_through_proxy", None, uri_, check_, home_)
        if (not php_is_null(result_)):
            return result_
        # end if
        if "localhost" == check_["host"] or (php_isset(lambda : home_["host"])) and home_["host"] == check_["host"]:
            return False
        # end if
        if (not php_defined("WP_PROXY_BYPASS_HOSTS")):
            return True
        # end if
        bypass_hosts_ = None
        wildcard_regex_ = Array()
        if None == bypass_hosts_:
            bypass_hosts_ = php_preg_split("|,\\s*|", WP_PROXY_BYPASS_HOSTS)
            if False != php_strpos(WP_PROXY_BYPASS_HOSTS, "*"):
                wildcard_regex_ = Array()
                for host_ in bypass_hosts_:
                    wildcard_regex_[-1] = php_str_replace("\\*", ".+", preg_quote(host_, "/"))
                # end for
                wildcard_regex_ = "/^(" + php_implode("|", wildcard_regex_) + ")$/i"
            # end if
        # end if
        if (not php_empty(lambda : wildcard_regex_)):
            return (not php_preg_match(wildcard_regex_, check_["host"]))
        else:
            return (not php_in_array(check_["host"], bypass_hosts_))
        # end if
    # end def send_through_proxy
# end class WP_HTTP_Proxy
