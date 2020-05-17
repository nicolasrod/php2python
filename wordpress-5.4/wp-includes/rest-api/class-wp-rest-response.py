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
#// REST API: WP_REST_Response class
#// 
#// @package WordPress
#// @subpackage REST_API
#// @since 4.4.0
#// 
#// 
#// Core class used to implement a REST response object.
#// 
#// @since 4.4.0
#// 
#// @see WP_HTTP_Response
#//
class WP_REST_Response(WP_HTTP_Response):
    #// 
    #// Links related to the response.
    #// 
    #// @since 4.4.0
    #// @var array
    #//
    links = Array()
    #// 
    #// The route that was to create the response.
    #// 
    #// @since 4.4.0
    #// @var string
    #//
    matched_route = ""
    #// 
    #// The handler that was used to create the response.
    #// 
    #// @since 4.4.0
    #// @var null|array
    #//
    matched_handler = None
    #// 
    #// Adds a link to the response.
    #// 
    #// @internal The $rel parameter is first, as this looks nicer when sending multiple.
    #// 
    #// @since 4.4.0
    #// 
    #// @link https://tools.ietf.org/html/rfc5988
    #// @link https://www.iana.org/assignments/link-relations/link-relations.xml
    #// 
    #// @param string $rel        Link relation. Either an IANA registered type,
    #// or an absolute URL.
    #// @param string $href       Target URI for the link.
    #// @param array  $attributes Optional. Link parameters to send along with the URL. Default empty array.
    #//
    def add_link(self, rel_=None, href_=None, attributes_=None):
        if attributes_ is None:
            attributes_ = Array()
        # end if
        
        if php_empty(lambda : self.links[rel_]):
            self.links[rel_] = Array()
        # end if
        if (php_isset(lambda : attributes_["href"])):
            attributes_["href"] = None
        # end if
        self.links[rel_][-1] = Array({"href": href_, "attributes": attributes_})
    # end def add_link
    #// 
    #// Removes a link from the response.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $rel  Link relation. Either an IANA registered type, or an absolute URL.
    #// @param string $href Optional. Only remove links for the relation matching the given href.
    #// Default null.
    #//
    def remove_link(self, rel_=None, href_=None):
        if href_ is None:
            href_ = None
        # end if
        
        if (not (php_isset(lambda : self.links[rel_]))):
            return
        # end if
        if href_:
            self.links[rel_] = wp_list_filter(self.links[rel_], Array({"href": href_}), "NOT")
        else:
            self.links[rel_] = Array()
        # end if
        if (not self.links[rel_]):
            self.links[rel_] = None
        # end if
    # end def remove_link
    #// 
    #// Adds multiple links to the response.
    #// 
    #// Link data should be an associative array with link relation as the key.
    #// The value can either be an associative array of link attributes
    #// (including `href` with the URL for the response), or a list of these
    #// associative arrays.
    #// 
    #// @since 4.4.0
    #// 
    #// @param array $links Map of link relation to list of links.
    #//
    def add_links(self, links_=None):
        
        
        for rel_,set_ in links_:
            #// If it's a single link, wrap with an array for consistent handling.
            if (php_isset(lambda : set_["href"])):
                set_ = Array(set_)
            # end if
            for attributes_ in set_:
                self.add_link(rel_, attributes_["href"], attributes_)
            # end for
        # end for
    # end def add_links
    #// 
    #// Retrieves links for the response.
    #// 
    #// @since 4.4.0
    #// 
    #// @return array List of links.
    #//
    def get_links(self):
        
        
        return self.links
    # end def get_links
    #// 
    #// Sets a single link header.
    #// 
    #// @internal The $rel parameter is first, as this looks nicer when sending multiple.
    #// 
    #// @since 4.4.0
    #// 
    #// @link https://tools.ietf.org/html/rfc5988
    #// @link https://www.iana.org/assignments/link-relations/link-relations.xml
    #// 
    #// @param string $rel   Link relation. Either an IANA registered type, or an absolute URL.
    #// @param string $link  Target IRI for the link.
    #// @param array  $other Optional. Other parameters to send, as an assocative array.
    #// Default empty array.
    #//
    def link_header(self, rel_=None, link_=None, other_=None):
        if other_ is None:
            other_ = Array()
        # end if
        
        header_ = "<" + link_ + ">; rel=\"" + rel_ + "\""
        for key_,value_ in other_:
            if "title" == key_:
                value_ = "\"" + value_ + "\""
            # end if
            header_ += "; " + key_ + "=" + value_
        # end for
        self.header("Link", header_, False)
    # end def link_header
    #// 
    #// Retrieves the route that was used.
    #// 
    #// @since 4.4.0
    #// 
    #// @return string The matched route.
    #//
    def get_matched_route(self):
        
        
        return self.matched_route
    # end def get_matched_route
    #// 
    #// Sets the route (regex for path) that caused the response.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $route Route name.
    #//
    def set_matched_route(self, route_=None):
        
        
        self.matched_route = route_
    # end def set_matched_route
    #// 
    #// Retrieves the handler that was used to generate the response.
    #// 
    #// @since 4.4.0
    #// 
    #// @return null|array The handler that was used to create the response.
    #//
    def get_matched_handler(self):
        
        
        return self.matched_handler
    # end def get_matched_handler
    #// 
    #// Sets the handler that was responsible for generating the response.
    #// 
    #// @since 4.4.0
    #// 
    #// @param array $handler The matched handler.
    #//
    def set_matched_handler(self, handler_=None):
        
        
        self.matched_handler = handler_
    # end def set_matched_handler
    #// 
    #// Checks if the response is an error, i.e. >= 400 response code.
    #// 
    #// @since 4.4.0
    #// 
    #// @return bool Whether the response is an error.
    #//
    def is_error(self):
        
        
        return self.get_status() >= 400
    # end def is_error
    #// 
    #// Retrieves a WP_Error object from the response.
    #// 
    #// @since 4.4.0
    #// 
    #// @return WP_Error|null WP_Error or null on not an errored response.
    #//
    def as_error(self):
        
        
        if (not self.is_error()):
            return None
        # end if
        error_ = php_new_class("WP_Error", lambda : WP_Error())
        if php_is_array(self.get_data()):
            data_ = self.get_data()
            error_.add(data_["code"], data_["message"], data_["data"])
            if (not php_empty(lambda : data_["additional_errors"])):
                for err_ in data_["additional_errors"]:
                    error_.add(err_["code"], err_["message"], err_["data"])
                # end for
            # end if
        else:
            error_.add(self.get_status(), "", Array({"status": self.get_status()}))
        # end if
        return error_
    # end def as_error
    #// 
    #// Retrieves the CURIEs (compact URIs) used for relations.
    #// 
    #// @since 4.5.0
    #// 
    #// @return array Compact URIs.
    #//
    def get_curies(self):
        
        
        curies_ = Array(Array({"name": "wp", "href": "https://api.w.org/{rel}"}, {"templated": True}))
        #// 
        #// Filters extra CURIEs available on API responses.
        #// 
        #// CURIEs allow a shortened version of URI relations. This allows a more
        #// usable form for custom relations than using the full URI. These work
        #// similarly to how XML namespaces work.
        #// 
        #// Registered CURIES need to specify a name and URI template. This will
        #// automatically transform URI relations into their shortened version.
        #// The shortened relation follows the format `{name}:{rel}`. `{rel}` in
        #// the URI template will be replaced with the `{rel}` part of the
        #// shortened relation.
        #// 
        #// For example, a CURIE with name `example` and URI template
        #// `http://w.org/{rel}` would transform a `http://w.org/term` relation
        #// into `example:term`.
        #// 
        #// Well-behaved clients should expand and normalise these back to their
        #// full URI relation, however some naive clients may not resolve these
        #// correctly, so adding new CURIEs may break backward compatibility.
        #// 
        #// @since 4.5.0
        #// 
        #// @param array $additional Additional CURIEs to register with the API.
        #//
        additional_ = apply_filters("rest_response_link_curies", Array())
        return php_array_merge(curies_, additional_)
    # end def get_curies
# end class WP_REST_Response
