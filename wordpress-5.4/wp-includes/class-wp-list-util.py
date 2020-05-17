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
#// WordPress List utility class
#// 
#// @package WordPress
#// @since 4.7.0
#// 
#// 
#// List utility.
#// 
#// Utility class to handle operations on an array of objects.
#// 
#// @since 4.7.0
#//
class WP_List_Util():
    #// 
    #// The input array.
    #// 
    #// @since 4.7.0
    #// @var array
    #//
    input = Array()
    #// 
    #// The output array.
    #// 
    #// @since 4.7.0
    #// @var array
    #//
    output = Array()
    #// 
    #// Temporary arguments for sorting.
    #// 
    #// @since 4.7.0
    #// @var array
    #//
    orderby = Array()
    #// 
    #// Constructor.
    #// 
    #// Sets the input array.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array $input Array to perform operations on.
    #//
    def __init__(self, input_=None):
        
        
        self.output = input_
        self.input = input_
    # end def __init__
    #// 
    #// Returns the original input array.
    #// 
    #// @since 4.7.0
    #// 
    #// @return array The input array.
    #//
    def get_input(self):
        
        
        return self.input
    # end def get_input
    #// 
    #// Returns the output array.
    #// 
    #// @since 4.7.0
    #// 
    #// @return array The output array.
    #//
    def get_output(self):
        
        
        return self.output
    # end def get_output
    #// 
    #// Filters the list, based on a set of key => value arguments.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array  $args     Optional. An array of key => value arguments to match
    #// against each object. Default empty array.
    #// @param string $operator Optional. The logical operation to perform. 'AND' means
    #// all elements from the array must match. 'OR' means only
    #// one element needs to match. 'NOT' means no elements may
    #// match. Default 'AND'.
    #// @return array Array of found values.
    #//
    def filter(self, args_=None, operator_="AND"):
        if args_ is None:
            args_ = Array()
        # end if
        
        if php_empty(lambda : args_):
            return self.output
        # end if
        operator_ = php_strtoupper(operator_)
        if (not php_in_array(operator_, Array("AND", "OR", "NOT"), True)):
            return Array()
        # end if
        count_ = php_count(args_)
        filtered_ = Array()
        for key_,obj_ in self.output:
            to_match_ = obj_
            matched_ = 0
            for m_key_,m_value_ in args_:
                if php_array_key_exists(m_key_, to_match_) and m_value_ == to_match_[m_key_]:
                    matched_ += 1
                # end if
            # end for
            if "AND" == operator_ and matched_ == count_ or "OR" == operator_ and matched_ > 0 or "NOT" == operator_ and 0 == matched_:
                filtered_[key_] = obj_
            # end if
        # end for
        self.output = filtered_
        return self.output
    # end def filter
    #// 
    #// Plucks a certain field out of each object in the list.
    #// 
    #// This has the same functionality and prototype of
    #// array_column() (PHP 5.5) but also supports objects.
    #// 
    #// @since 4.7.0
    #// 
    #// @param int|string $field     Field from the object to place instead of the entire object
    #// @param int|string $index_key Optional. Field from the object to use as keys for the new array.
    #// Default null.
    #// @return array Array of found values. If `$index_key` is set, an array of found values with keys
    #// corresponding to `$index_key`. If `$index_key` is null, array keys from the original
    #// `$list` will be preserved in the results.
    #//
    def pluck(self, field_=None, index_key_=None):
        
        
        newlist_ = Array()
        if (not index_key_):
            #// 
            #// This is simple. Could at some point wrap array_column()
            #// if we knew we had an array of arrays.
            #//
            for key_,value_ in self.output:
                if php_is_object(value_):
                    newlist_[key_] = value_.field_
                else:
                    newlist_[key_] = value_[field_]
                # end if
            # end for
            self.output = newlist_
            return self.output
        # end if
        #// 
        #// When index_key is not set for a particular item, push the value
        #// to the end of the stack. This is how array_column() behaves.
        #//
        for value_ in self.output:
            if php_is_object(value_):
                if (php_isset(lambda : value_.index_key_)):
                    newlist_[value_.index_key_] = value_.field_
                else:
                    newlist_[-1] = value_.field_
                # end if
            else:
                if (php_isset(lambda : value_[index_key_])):
                    newlist_[value_[index_key_]] = value_[field_]
                else:
                    newlist_[-1] = value_[field_]
                # end if
            # end if
        # end for
        self.output = newlist_
        return self.output
    # end def pluck
    #// 
    #// Sorts the list, based on one or more orderby arguments.
    #// 
    #// @since 4.7.0
    #// 
    #// @param string|array $orderby       Optional. Either the field name to order by or an array
    #// of multiple orderby fields as $orderby => $order.
    #// @param string       $order         Optional. Either 'ASC' or 'DESC'. Only used if $orderby
    #// is a string.
    #// @param bool         $preserve_keys Optional. Whether to preserve keys. Default false.
    #// @return array The sorted array.
    #//
    def sort(self, orderby_=None, order_="ASC", preserve_keys_=None):
        if orderby_ is None:
            orderby_ = Array()
        # end if
        if preserve_keys_ is None:
            preserve_keys_ = False
        # end if
        
        if php_empty(lambda : orderby_):
            return self.output
        # end if
        if php_is_string(orderby_):
            orderby_ = Array({orderby_: order_})
        # end if
        for field_,direction_ in orderby_:
            orderby_[field_] = "DESC" if "DESC" == php_strtoupper(direction_) else "ASC"
        # end for
        self.orderby = orderby_
        if preserve_keys_:
            uasort(self.output, Array(self, "sort_callback"))
        else:
            usort(self.output, Array(self, "sort_callback"))
        # end if
        self.orderby = Array()
        return self.output
    # end def sort
    #// 
    #// Callback to sort the list by specific fields.
    #// 
    #// @since 4.7.0
    #// 
    #// @see WP_List_Util::sort()
    #// 
    #// @param object|array $a One object to compare.
    #// @param object|array $b The other object to compare.
    #// @return int 0 if both objects equal. -1 if second object should come first, 1 otherwise.
    #//
    def sort_callback(self, a_=None, b_=None):
        
        
        if php_empty(lambda : self.orderby):
            return 0
        # end if
        a_ = a_
        b_ = b_
        for field_,direction_ in self.orderby:
            if (not (php_isset(lambda : a_[field_]))) or (not (php_isset(lambda : b_[field_]))):
                continue
            # end if
            if a_[field_] == b_[field_]:
                continue
            # end if
            results_ = Array(1, -1) if "DESC" == direction_ else Array(-1, 1)
            if php_is_numeric(a_[field_]) and php_is_numeric(b_[field_]):
                return results_[0] if a_[field_] < b_[field_] else results_[1]
            # end if
            return results_[0] if 0 > strcmp(a_[field_], b_[field_]) else results_[1]
        # end for
        return 0
    # end def sort_callback
# end class WP_List_Util
