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
#// HTTP API: Requests hook bridge class
#// 
#// @package WordPress
#// @subpackage HTTP
#// @since 4.7.0
#// 
#// 
#// Bridge to connect Requests internal hooks to WordPress actions.
#// 
#// @since 4.7.0
#// 
#// @see Requests_Hooks
#//
class WP_HTTP_Requests_Hooks(Requests_Hooks):
    url = Array()
    request = Array()
    #// 
    #// Constructor.
    #// 
    #// @param string $url URL to request.
    #// @param array $request Request data in WP_Http format.
    #//
    def __init__(self, url=None, request=None):
        
        self.url = url
        self.request = request
    # end def __init__
    #// 
    #// Dispatch a Requests hook to a native WordPress action.
    #// 
    #// @param string $hook Hook name.
    #// @param array $parameters Parameters to pass to callbacks.
    #// @return boolean True if hooks were run, false if nothing was hooked.
    #//
    def dispatch(self, hook=None, parameters=Array()):
        
        result = super().dispatch(hook, parameters)
        #// Handle back-compat actions.
        for case in Switch(hook):
            if case("curl.before_send"):
                #// This action is documented in wp-includes/class-wp-http-curl.php
                do_action_ref_array("http_api_curl", Array(parameters[0], self.request, self.url))
                break
            # end if
        # end for
        #// 
        #// Transforms a native Request hook to a WordPress actions.
        #// 
        #// This action maps Requests internal hook to a native WordPress action.
        #// 
        #// @see https://github.com/rmccue/Requests/blob/master/docs/hooks.md
        #// 
        #// @param array $parameters Parameters from Requests internal hook.
        #// @param array $request Request data in WP_Http format.
        #// @param string $url URL to request.
        #//
        do_action_ref_array(str("requests-") + str(hook), parameters, self.request, self.url)
        #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
        return result
    # end def dispatch
# end class WP_HTTP_Requests_Hooks
