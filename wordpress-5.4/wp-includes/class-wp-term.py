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
#// Taxonomy API: WP_Term class
#// 
#// @package WordPress
#// @subpackage Taxonomy
#// @since 4.4.0
#// 
#// 
#// Core class used to implement the WP_Term object.
#// 
#// @since 4.4.0
#// 
#// @property-read object $data Sanitized term data.
#//
class WP_Term():
    term_id = Array()
    name = ""
    slug = ""
    term_group = ""
    term_taxonomy_id = 0
    taxonomy = ""
    description = ""
    parent = 0
    count = 0
    filter = "raw"
    #// 
    #// Retrieve WP_Term instance.
    #// 
    #// @since 4.4.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param int    $term_id  Term ID.
    #// @param string $taxonomy Optional. Limit matched terms to those matching `$taxonomy`. Only used for
    #// disambiguating potentially shared terms.
    #// @return WP_Term|WP_Error|false Term object, if found. WP_Error if `$term_id` is shared between taxonomies and
    #// there's insufficient data to distinguish which term is intended.
    #// False for other failures.
    #//
    @classmethod
    def get_instance(self, term_id=None, taxonomy=None):
        
        global wpdb
        php_check_if_defined("wpdb")
        term_id = php_int(term_id)
        if (not term_id):
            return False
        # end if
        _term = wp_cache_get(term_id, "terms")
        #// If there isn't a cached version, hit the database.
        if (not _term) or taxonomy and taxonomy != _term.taxonomy:
            #// Any term found in the cache is not a match, so don't use it.
            _term = False
            #// Grab all matching terms, in case any are shared between taxonomies.
            terms = wpdb.get_results(wpdb.prepare(str("SELECT t.*, tt.* FROM ") + str(wpdb.terms) + str(" AS t INNER JOIN ") + str(wpdb.term_taxonomy) + str(" AS tt ON t.term_id = tt.term_id WHERE t.term_id = %d"), term_id))
            if (not terms):
                return False
            # end if
            #// If a taxonomy was specified, find a match.
            if taxonomy:
                for match in terms:
                    if taxonomy == match.taxonomy:
                        _term = match
                        break
                    # end if
                # end for
                pass
            elif 1 == php_count(terms):
                _term = reset(terms)
                pass
            else:
                #// If the term is shared only with invalid taxonomies, return the one valid term.
                for t in terms:
                    if (not taxonomy_exists(t.taxonomy)):
                        continue
                    # end if
                    #// Only hit if we've already identified a term in a valid taxonomy.
                    if _term:
                        return php_new_class("WP_Error", lambda : WP_Error("ambiguous_term_id", __("Term ID is shared between multiple taxonomies"), term_id))
                    # end if
                    _term = t
                # end for
            # end if
            if (not _term):
                return False
            # end if
            #// Don't return terms from invalid taxonomies.
            if (not taxonomy_exists(_term.taxonomy)):
                return php_new_class("WP_Error", lambda : WP_Error("invalid_taxonomy", __("Invalid taxonomy.")))
            # end if
            _term = sanitize_term(_term, _term.taxonomy, "raw")
            #// Don't cache terms that are shared between taxonomies.
            if 1 == php_count(terms):
                wp_cache_add(term_id, _term, "terms")
            # end if
        # end if
        term_obj = php_new_class("WP_Term", lambda : WP_Term(_term))
        term_obj.filter(term_obj.filter)
        return term_obj
    # end def get_instance
    #// 
    #// Constructor.
    #// 
    #// @since 4.4.0
    #// 
    #// @param WP_Term|object $term Term object.
    #//
    def __init__(self, term=None):
        
        for key,value in get_object_vars(term):
            self.key = value
        # end for
    # end def __init__
    #// 
    #// Sanitizes term fields, according to the filter type provided.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $filter Filter context. Accepts 'edit', 'db', 'display', 'attribute', 'js', 'raw'.
    #//
    def filter(self, filter=None):
        
        sanitize_term(self, self.taxonomy, filter)
    # end def filter
    #// 
    #// Converts an object to array.
    #// 
    #// @since 4.4.0
    #// 
    #// @return array Object as array.
    #//
    def to_array(self):
        
        return get_object_vars(self)
    # end def to_array
    #// 
    #// Getter.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $key Property to get.
    #// @return mixed Property value.
    #//
    def __get(self, key=None):
        
        for case in Switch(key):
            if case("data"):
                data = php_new_class("stdClass", lambda : stdClass())
                columns = Array("term_id", "name", "slug", "term_group", "term_taxonomy_id", "taxonomy", "description", "parent", "count")
                for column in columns:
                    data.column = self.column if (php_isset(lambda : self.column)) else None
                # end for
                return sanitize_term(data, data.taxonomy, "raw")
            # end if
        # end for
    # end def __get
# end class WP_Term
