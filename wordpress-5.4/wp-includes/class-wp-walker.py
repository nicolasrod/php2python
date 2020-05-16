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
#// A class for displaying various tree-like structures.
#// 
#// Extend the Walker class to use it, see examples below. Child classes
#// do not need to implement all of the abstract methods in the class. The child
#// only needs to implement the methods that are needed.
#// 
#// @since 2.1.0
#// 
#// @package WordPress
#// @abstract
#//
class Walker():
    tree_type = Array()
    db_fields = Array()
    max_pages = 1
    has_children = Array()
    #// 
    #// Starts the list before the elements are added.
    #// 
    #// The $args parameter holds additional values that may be used with the child
    #// class methods. This method is called at the start of the output list.
    #// 
    #// @since 2.1.0
    #// @abstract
    #// 
    #// @param string $output Used to append additional content (passed by reference).
    #// @param int    $depth  Depth of the item.
    #// @param array  $args   An array of additional arguments.
    #//
    def start_lvl(self, output=None, depth=0, args=Array()):
        
        pass
    # end def start_lvl
    #// 
    #// Ends the list of after the elements are added.
    #// 
    #// The $args parameter holds additional values that may be used with the child
    #// class methods. This method finishes the list at the end of output of the elements.
    #// 
    #// @since 2.1.0
    #// @abstract
    #// 
    #// @param string $output Used to append additional content (passed by reference).
    #// @param int    $depth  Depth of the item.
    #// @param array  $args   An array of additional arguments.
    #//
    def end_lvl(self, output=None, depth=0, args=Array()):
        
        pass
    # end def end_lvl
    #// 
    #// Start the element output.
    #// 
    #// The $args parameter holds additional values that may be used with the child
    #// class methods. Includes the element output also.
    #// 
    #// @since 2.1.0
    #// @abstract
    #// 
    #// @param string $output            Used to append additional content (passed by reference).
    #// @param object $object            The data object.
    #// @param int    $depth             Depth of the item.
    #// @param array  $args              An array of additional arguments.
    #// @param int    $current_object_id ID of the current item.
    #//
    def start_el(self, output=None, object=None, depth=0, args=Array(), current_object_id=0):
        
        pass
    # end def start_el
    #// 
    #// Ends the element output, if needed.
    #// 
    #// The $args parameter holds additional values that may be used with the child class methods.
    #// 
    #// @since 2.1.0
    #// @abstract
    #// 
    #// @param string $output Used to append additional content (passed by reference).
    #// @param object $object The data object.
    #// @param int    $depth  Depth of the item.
    #// @param array  $args   An array of additional arguments.
    #//
    def end_el(self, output=None, object=None, depth=0, args=Array()):
        
        pass
    # end def end_el
    #// 
    #// Traverse elements to create list from elements.
    #// 
    #// Display one element if the element doesn't have any children otherwise,
    #// display the element and its children. Will only traverse up to the max
    #// depth and no ignore elements under that depth. It is possible to set the
    #// max depth to include all depths, see walk() method.
    #// 
    #// This method should not be called directly, use the walk() method instead.
    #// 
    #// @since 2.5.0
    #// 
    #// @param object $element           Data object.
    #// @param array  $children_elements List of elements to continue traversing (passed by reference).
    #// @param int    $max_depth         Max depth to traverse.
    #// @param int    $depth             Depth of current element.
    #// @param array  $args              An array of arguments.
    #// @param string $output            Used to append additional content (passed by reference).
    #//
    def display_element(self, element=None, children_elements=None, max_depth=None, depth=None, args=None, output=None):
        
        if (not element):
            return
        # end if
        id_field = self.db_fields["id"]
        id = element.id_field
        #// Display this element.
        self.has_children = (not php_empty(lambda : children_elements[id]))
        if (php_isset(lambda : args[0])) and php_is_array(args[0]):
            args[0]["has_children"] = self.has_children
            pass
        # end if
        self.start_el(output, element, depth, php_array_values(args))
        #// Descend only when the depth is right and there are childrens for this element.
        if 0 == max_depth or max_depth > depth + 1 and (php_isset(lambda : children_elements[id])):
            for child in children_elements[id]:
                if (not (php_isset(lambda : newlevel))):
                    newlevel = True
                    #// Start the child delimiter.
                    self.start_lvl(output, depth, php_array_values(args))
                # end if
                self.display_element(child, children_elements, max_depth, depth + 1, args, output)
            # end for
            children_elements[id] = None
        # end if
        if (php_isset(lambda : newlevel)) and newlevel:
            #// End the child delimiter.
            self.end_lvl(output, depth, php_array_values(args))
        # end if
        #// End this element.
        self.end_el(output, element, depth, php_array_values(args))
    # end def display_element
    #// 
    #// Display array of elements hierarchically.
    #// 
    #// Does not assume any existing order of elements.
    #// 
    #// $max_depth = -1 means flatly display every element.
    #// $max_depth = 0 means display all levels.
    #// $max_depth > 0 specifies the number of display levels.
    #// 
    #// @since 2.1.0
    #// @since 5.3.0 Formalized the existing `...$args` parameter by adding it
    #// to the function signature.
    #// 
    #// @param array $elements  An array of elements.
    #// @param int   $max_depth The maximum hierarchical depth.
    #// @param mixed ...$args   Optional additional arguments.
    #// @return string The hierarchical item output.
    #//
    def walk(self, elements=None, max_depth=None, *args):
        
        output = ""
        #// Invalid parameter or nothing to walk.
        if max_depth < -1 or php_empty(lambda : elements):
            return output
        # end if
        parent_field = self.db_fields["parent"]
        #// Flat display.
        if -1 == max_depth:
            empty_array = Array()
            for e in elements:
                self.display_element(e, empty_array, 1, 0, args, output)
            # end for
            return output
        # end if
        #// 
        #// Need to display in hierarchical order.
        #// Separate elements into two buckets: top level and children elements.
        #// Children_elements is two dimensional array, eg.
        #// Children_elements[10][] contains all sub-elements whose parent is 10.
        #//
        top_level_elements = Array()
        children_elements = Array()
        for e in elements:
            if php_empty(lambda : e.parent_field):
                top_level_elements[-1] = e
            else:
                children_elements[e.parent_field][-1] = e
            # end if
        # end for
        #// 
        #// When none of the elements is top level.
        #// Assume the first one must be root of the sub elements.
        #//
        if php_empty(lambda : top_level_elements):
            first = php_array_slice(elements, 0, 1)
            root = first[0]
            top_level_elements = Array()
            children_elements = Array()
            for e in elements:
                if root.parent_field == e.parent_field:
                    top_level_elements[-1] = e
                else:
                    children_elements[e.parent_field][-1] = e
                # end if
            # end for
        # end if
        for e in top_level_elements:
            self.display_element(e, children_elements, max_depth, 0, args, output)
        # end for
        #// 
        #// If we are displaying all levels, and remaining children_elements is not empty,
        #// then we got orphans, which should be displayed regardless.
        #//
        if 0 == max_depth and php_count(children_elements) > 0:
            empty_array = Array()
            for orphans in children_elements:
                for op in orphans:
                    self.display_element(op, empty_array, 1, 0, args, output)
                # end for
            # end for
        # end if
        return output
    # end def walk
    #// 
    #// paged_walk() - produce a page of nested elements
    #// 
    #// Given an array of hierarchical elements, the maximum depth, a specific page number,
    #// and number of elements per page, this function first determines all top level root elements
    #// belonging to that page, then lists them and all of their children in hierarchical order.
    #// 
    #// $max_depth = 0 means display all levels.
    #// $max_depth > 0 specifies the number of display levels.
    #// 
    #// @since 2.7.0
    #// @since 5.3.0 Formalized the existing `...$args` parameter by adding it
    #// to the function signature.
    #// 
    #// @param array $elements
    #// @param int   $max_depth The maximum hierarchical depth.
    #// @param int   $page_num  The specific page number, beginning with 1.
    #// @param int   $per_page
    #// @param mixed ...$args   Optional additional arguments.
    #// @return string XHTML of the specified page of elements
    #//
    def paged_walk(self, elements=None, max_depth=None, page_num=None, per_page=None, *args):
        
        if php_empty(lambda : elements) or max_depth < -1:
            return ""
        # end if
        output = ""
        parent_field = self.db_fields["parent"]
        count = -1
        if -1 == max_depth:
            total_top = php_count(elements)
        # end if
        if page_num < 1 or per_page < 0:
            #// No paging.
            paging = False
            start = 0
            if -1 == max_depth:
                end_ = total_top
            # end if
            self.max_pages = 1
        else:
            paging = True
            start = php_int(page_num) - 1 * php_int(per_page)
            end_ = start + per_page
            if -1 == max_depth:
                self.max_pages = ceil(total_top / per_page)
            # end if
        # end if
        #// Flat display.
        if -1 == max_depth:
            if (not php_empty(lambda : args[0]["reverse_top_level"])):
                elements = array_reverse(elements)
                oldstart = start
                start = total_top - end_
                end_ = total_top - oldstart
            # end if
            empty_array = Array()
            for e in elements:
                count += 1
                if count < start:
                    continue
                # end if
                if count >= end_:
                    break
                # end if
                self.display_element(e, empty_array, 1, 0, args, output)
            # end for
            return output
        # end if
        #// 
        #// Separate elements into two buckets: top level and children elements.
        #// Children_elements is two dimensional array, e.g.
        #// $children_elements[10][] contains all sub-elements whose parent is 10.
        #//
        top_level_elements = Array()
        children_elements = Array()
        for e in elements:
            if 0 == e.parent_field:
                top_level_elements[-1] = e
            else:
                children_elements[e.parent_field][-1] = e
            # end if
        # end for
        total_top = php_count(top_level_elements)
        if paging:
            self.max_pages = ceil(total_top / per_page)
        else:
            end_ = total_top
        # end if
        if (not php_empty(lambda : args[0]["reverse_top_level"])):
            top_level_elements = array_reverse(top_level_elements)
            oldstart = start
            start = total_top - end_
            end_ = total_top - oldstart
        # end if
        if (not php_empty(lambda : args[0]["reverse_children"])):
            for parent,children in children_elements:
                children_elements[parent] = array_reverse(children)
            # end for
        # end if
        for e in top_level_elements:
            count += 1
            #// For the last page, need to unset earlier children in order to keep track of orphans.
            if end_ >= total_top and count < start:
                self.unset_children(e, children_elements)
            # end if
            if count < start:
                continue
            # end if
            if count >= end_:
                break
            # end if
            self.display_element(e, children_elements, max_depth, 0, args, output)
        # end for
        if end_ >= total_top and php_count(children_elements) > 0:
            empty_array = Array()
            for orphans in children_elements:
                for op in orphans:
                    self.display_element(op, empty_array, 1, 0, args, output)
                # end for
            # end for
        # end if
        return output
    # end def paged_walk
    #// 
    #// Calculates the total number of root elements.
    #// 
    #// @since 2.7.0
    #// 
    #// @param array $elements Elements to list.
    #// @return int Number of root elements.
    #//
    def get_number_of_root_elements(self, elements=None):
        
        num = 0
        parent_field = self.db_fields["parent"]
        for e in elements:
            if 0 == e.parent_field:
                num += 1
            # end if
        # end for
        return num
    # end def get_number_of_root_elements
    #// 
    #// Unset all the children for a given top level element.
    #// 
    #// @since 2.7.0
    #// 
    #// @param object $e
    #// @param array $children_elements
    #//
    def unset_children(self, e=None, children_elements=None):
        
        if (not e) or (not children_elements):
            return
        # end if
        id_field = self.db_fields["id"]
        id = e.id_field
        if (not php_empty(lambda : children_elements[id])) and php_is_array(children_elements[id]):
            for child in children_elements[id]:
                self.unset_children(child, children_elements)
            # end for
        # end if
        children_elements[id] = None
    # end def unset_children
# end class Walker
