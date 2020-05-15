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
    input = Array()
    output = Array()
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
    def __init__(self, input=None):
        
        self.output = input
        self.input = input
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
    def filter(self, args=Array(), operator="AND"):
        
        if php_empty(lambda : args):
            return self.output
        # end if
        operator = php_strtoupper(operator)
        if (not php_in_array(operator, Array("AND", "OR", "NOT"), True)):
            return Array()
        # end if
        count = php_count(args)
        filtered = Array()
        for key,obj in self.output:
            to_match = obj
            matched = 0
            for m_key,m_value in args:
                if php_array_key_exists(m_key, to_match) and m_value == to_match[m_key]:
                    matched += 1
                # end if
            # end for
            if "AND" == operator and matched == count or "OR" == operator and matched > 0 or "NOT" == operator and 0 == matched:
                filtered[key] = obj
            # end if
        # end for
        self.output = filtered
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
    def pluck(self, field=None, index_key=None):
        
        newlist = Array()
        if (not index_key):
            #// 
            #// This is simple. Could at some point wrap array_column()
            #// if we knew we had an array of arrays.
            #//
            for key,value in self.output:
                if php_is_object(value):
                    newlist[key] = value.field
                else:
                    newlist[key] = value[field]
                # end if
            # end for
            self.output = newlist
            return self.output
        # end if
        #// 
        #// When index_key is not set for a particular item, push the value
        #// to the end of the stack. This is how array_column() behaves.
        #//
        for value in self.output:
            if php_is_object(value):
                if (php_isset(lambda : value.index_key)):
                    newlist[value.index_key] = value.field
                else:
                    newlist[-1] = value.field
                # end if
            else:
                if (php_isset(lambda : value[index_key])):
                    newlist[value[index_key]] = value[field]
                else:
                    newlist[-1] = value[field]
                # end if
            # end if
        # end for
        self.output = newlist
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
    def sort(self, orderby=Array(), order="ASC", preserve_keys=False):
        
        if php_empty(lambda : orderby):
            return self.output
        # end if
        if php_is_string(orderby):
            orderby = Array({orderby: order})
        # end if
        for field,direction in orderby:
            orderby[field] = "DESC" if "DESC" == php_strtoupper(direction) else "ASC"
        # end for
        self.orderby = orderby
        if preserve_keys:
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
    def sort_callback(self, a=None, b=None):
        
        if php_empty(lambda : self.orderby):
            return 0
        # end if
        a = a
        b = b
        for field,direction in self.orderby:
            if (not (php_isset(lambda : a[field]))) or (not (php_isset(lambda : b[field]))):
                continue
            # end if
            if a[field] == b[field]:
                continue
            # end if
            results = Array(1, -1) if "DESC" == direction else Array(-1, 1)
            if php_is_numeric(a[field]) and php_is_numeric(b[field]):
                return results[0] if a[field] < b[field] else results[1]
            # end if
            return results[0] if 0 > strcmp(a[field], b[field]) else results[1]
        # end for
        return 0
    # end def sort_callback
# end class WP_List_Util
