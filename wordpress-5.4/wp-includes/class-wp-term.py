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
    #// 
    #// Term ID.
    #// 
    #// @since 4.4.0
    #// @var int
    #//
    term_id = Array()
    #// 
    #// The term's name.
    #// 
    #// @since 4.4.0
    #// @var string
    #//
    name = ""
    #// 
    #// The term's slug.
    #// 
    #// @since 4.4.0
    #// @var string
    #//
    slug = ""
    #// 
    #// The term's term_group.
    #// 
    #// @since 4.4.0
    #// @var string
    #//
    term_group = ""
    #// 
    #// Term Taxonomy ID.
    #// 
    #// @since 4.4.0
    #// @var int
    #//
    term_taxonomy_id = 0
    #// 
    #// The term's taxonomy name.
    #// 
    #// @since 4.4.0
    #// @var string
    #//
    taxonomy = ""
    #// 
    #// The term's description.
    #// 
    #// @since 4.4.0
    #// @var string
    #//
    description = ""
    #// 
    #// ID of a term's parent term.
    #// 
    #// @since 4.4.0
    #// @var int
    #//
    parent = 0
    #// 
    #// Cached object count for this term.
    #// 
    #// @since 4.4.0
    #// @var int
    #//
    count = 0
    #// 
    #// Stores the term object's sanitization level.
    #// 
    #// Does not correspond to a database field.
    #// 
    #// @since 4.4.0
    #// @var string
    #//
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
    def get_instance(self, term_id_=None, taxonomy_=None):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        term_id_ = php_int(term_id_)
        if (not term_id_):
            return False
        # end if
        _term_ = wp_cache_get(term_id_, "terms")
        #// If there isn't a cached version, hit the database.
        if (not _term_) or taxonomy_ and taxonomy_ != _term_.taxonomy:
            #// Any term found in the cache is not a match, so don't use it.
            _term_ = False
            #// Grab all matching terms, in case any are shared between taxonomies.
            terms_ = wpdb_.get_results(wpdb_.prepare(str("SELECT t.*, tt.* FROM ") + str(wpdb_.terms) + str(" AS t INNER JOIN ") + str(wpdb_.term_taxonomy) + str(" AS tt ON t.term_id = tt.term_id WHERE t.term_id = %d"), term_id_))
            if (not terms_):
                return False
            # end if
            #// If a taxonomy was specified, find a match.
            if taxonomy_:
                for match_ in terms_:
                    if taxonomy_ == match_.taxonomy:
                        _term_ = match_
                        break
                    # end if
                # end for
                pass
            elif 1 == php_count(terms_):
                _term_ = reset(terms_)
                pass
            else:
                #// If the term is shared only with invalid taxonomies, return the one valid term.
                for t_ in terms_:
                    if (not taxonomy_exists(t_.taxonomy)):
                        continue
                    # end if
                    #// Only hit if we've already identified a term in a valid taxonomy.
                    if _term_:
                        return php_new_class("WP_Error", lambda : WP_Error("ambiguous_term_id", __("Term ID is shared between multiple taxonomies"), term_id_))
                    # end if
                    _term_ = t_
                # end for
            # end if
            if (not _term_):
                return False
            # end if
            #// Don't return terms from invalid taxonomies.
            if (not taxonomy_exists(_term_.taxonomy)):
                return php_new_class("WP_Error", lambda : WP_Error("invalid_taxonomy", __("Invalid taxonomy.")))
            # end if
            _term_ = sanitize_term(_term_, _term_.taxonomy, "raw")
            #// Don't cache terms that are shared between taxonomies.
            if 1 == php_count(terms_):
                wp_cache_add(term_id_, _term_, "terms")
            # end if
        # end if
        term_obj_ = php_new_class("WP_Term", lambda : WP_Term(_term_))
        term_obj_.filter(term_obj_.filter)
        return term_obj_
    # end def get_instance
    #// 
    #// Constructor.
    #// 
    #// @since 4.4.0
    #// 
    #// @param WP_Term|object $term Term object.
    #//
    def __init__(self, term_=None):
        
        
        for key_,value_ in get_object_vars(term_):
            self.key_ = value_
        # end for
    # end def __init__
    #// 
    #// Sanitizes term fields, according to the filter type provided.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $filter Filter context. Accepts 'edit', 'db', 'display', 'attribute', 'js', 'raw'.
    #//
    def filter(self, filter_=None):
        
        
        sanitize_term(self, self.taxonomy, filter_)
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
    def __get(self, key_=None):
        
        
        for case in Switch(key_):
            if case("data"):
                data_ = php_new_class("stdClass", lambda : stdClass())
                columns_ = Array("term_id", "name", "slug", "term_group", "term_taxonomy_id", "taxonomy", "description", "parent", "count")
                for column_ in columns_:
                    data_.column_ = self.column_ if (php_isset(lambda : self.column_)) else None
                # end for
                return sanitize_term(data_, data_.taxonomy, "raw")
            # end if
        # end for
    # end def __get
# end class WP_Term
