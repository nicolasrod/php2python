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
    #// 
    #// What the class handles.
    #// 
    #// @since 2.1.0
    #// @var string
    #//
    tree_type = Array()
    #// 
    #// DB fields to use.
    #// 
    #// @since 2.1.0
    #// @var array
    #//
    db_fields = Array()
    #// 
    #// Max number of pages walked by the paged walker
    #// 
    #// @since 2.7.0
    #// @var int
    #//
    max_pages = 1
    #// 
    #// Whether the current element has children or not.
    #// 
    #// To be used in start_el().
    #// 
    #// @since 4.0.0
    #// @var bool
    #//
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
    def start_lvl(self, output_=None, depth_=0, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
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
    def end_lvl(self, output_=None, depth_=0, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
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
    def start_el(self, output_=None, object_=None, depth_=0, args_=None, current_object_id_=0):
        if args_ is None:
            args_ = Array()
        # end if
        
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
    def end_el(self, output_=None, object_=None, depth_=0, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
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
    def display_element(self, element_=None, children_elements_=None, max_depth_=None, depth_=None, args_=None, output_=None):
        
        
        if (not element_):
            return
        # end if
        id_field_ = self.db_fields["id"]
        id_ = element_.id_field_
        #// Display this element.
        self.has_children = (not php_empty(lambda : children_elements_[id_]))
        if (php_isset(lambda : args_[0])) and php_is_array(args_[0]):
            args_[0]["has_children"] = self.has_children
            pass
        # end if
        self.start_el(output_, element_, depth_, php_array_values(args_))
        #// Descend only when the depth is right and there are childrens for this element.
        if 0 == max_depth_ or max_depth_ > depth_ + 1 and (php_isset(lambda : children_elements_[id_])):
            for child_ in children_elements_[id_]:
                if (not (php_isset(lambda : newlevel_))):
                    newlevel_ = True
                    #// Start the child delimiter.
                    self.start_lvl(output_, depth_, php_array_values(args_))
                # end if
                self.display_element(child_, children_elements_, max_depth_, depth_ + 1, args_, output_)
            # end for
            children_elements_[id_] = None
        # end if
        if (php_isset(lambda : newlevel_)) and newlevel_:
            #// End the child delimiter.
            self.end_lvl(output_, depth_, php_array_values(args_))
        # end if
        #// End this element.
        self.end_el(output_, element_, depth_, php_array_values(args_))
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
    def walk(self, elements_=None, max_depth_=None, *args_):
        
        
        output_ = ""
        #// Invalid parameter or nothing to walk.
        if max_depth_ < -1 or php_empty(lambda : elements_):
            return output_
        # end if
        parent_field_ = self.db_fields["parent"]
        #// Flat display.
        if -1 == max_depth_:
            empty_array_ = Array()
            for e_ in elements_:
                self.display_element(e_, empty_array_, 1, 0, args_, output_)
            # end for
            return output_
        # end if
        #// 
        #// Need to display in hierarchical order.
        #// Separate elements into two buckets: top level and children elements.
        #// Children_elements is two dimensional array, eg.
        #// Children_elements[10][] contains all sub-elements whose parent is 10.
        #//
        top_level_elements_ = Array()
        children_elements_ = Array()
        for e_ in elements_:
            if php_empty(lambda : e_.parent_field_):
                top_level_elements_[-1] = e_
            else:
                children_elements_[e_.parent_field_][-1] = e_
            # end if
        # end for
        #// 
        #// When none of the elements is top level.
        #// Assume the first one must be root of the sub elements.
        #//
        if php_empty(lambda : top_level_elements_):
            first_ = php_array_slice(elements_, 0, 1)
            root_ = first_[0]
            top_level_elements_ = Array()
            children_elements_ = Array()
            for e_ in elements_:
                if root_.parent_field_ == e_.parent_field_:
                    top_level_elements_[-1] = e_
                else:
                    children_elements_[e_.parent_field_][-1] = e_
                # end if
            # end for
        # end if
        for e_ in top_level_elements_:
            self.display_element(e_, children_elements_, max_depth_, 0, args_, output_)
        # end for
        #// 
        #// If we are displaying all levels, and remaining children_elements is not empty,
        #// then we got orphans, which should be displayed regardless.
        #//
        if 0 == max_depth_ and php_count(children_elements_) > 0:
            empty_array_ = Array()
            for orphans_ in children_elements_:
                for op_ in orphans_:
                    self.display_element(op_, empty_array_, 1, 0, args_, output_)
                # end for
            # end for
        # end if
        return output_
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
    def paged_walk(self, elements_=None, max_depth_=None, page_num_=None, per_page_=None, *args_):
        
        
        if php_empty(lambda : elements_) or max_depth_ < -1:
            return ""
        # end if
        output_ = ""
        parent_field_ = self.db_fields["parent"]
        count_ = -1
        if -1 == max_depth_:
            total_top_ = php_count(elements_)
        # end if
        if page_num_ < 1 or per_page_ < 0:
            #// No paging.
            paging_ = False
            start_ = 0
            if -1 == max_depth_:
                end_ = total_top_
            # end if
            self.max_pages = 1
        else:
            paging_ = True
            start_ = php_int(page_num_) - 1 * php_int(per_page_)
            end_ = start_ + per_page_
            if -1 == max_depth_:
                self.max_pages = ceil(total_top_ / per_page_)
            # end if
        # end if
        #// Flat display.
        if -1 == max_depth_:
            if (not php_empty(lambda : args_[0]["reverse_top_level"])):
                elements_ = array_reverse(elements_)
                oldstart_ = start_
                start_ = total_top_ - end_
                end_ = total_top_ - oldstart_
            # end if
            empty_array_ = Array()
            for e_ in elements_:
                count_ += 1
                if count_ < start_:
                    continue
                # end if
                if count_ >= end_:
                    break
                # end if
                self.display_element(e_, empty_array_, 1, 0, args_, output_)
            # end for
            return output_
        # end if
        #// 
        #// Separate elements into two buckets: top level and children elements.
        #// Children_elements is two dimensional array, e.g.
        #// $children_elements[10][] contains all sub-elements whose parent is 10.
        #//
        top_level_elements_ = Array()
        children_elements_ = Array()
        for e_ in elements_:
            if 0 == e_.parent_field_:
                top_level_elements_[-1] = e_
            else:
                children_elements_[e_.parent_field_][-1] = e_
            # end if
        # end for
        total_top_ = php_count(top_level_elements_)
        if paging_:
            self.max_pages = ceil(total_top_ / per_page_)
        else:
            end_ = total_top_
        # end if
        if (not php_empty(lambda : args_[0]["reverse_top_level"])):
            top_level_elements_ = array_reverse(top_level_elements_)
            oldstart_ = start_
            start_ = total_top_ - end_
            end_ = total_top_ - oldstart_
        # end if
        if (not php_empty(lambda : args_[0]["reverse_children"])):
            for parent_,children_ in children_elements_:
                children_elements_[parent_] = array_reverse(children_)
            # end for
        # end if
        for e_ in top_level_elements_:
            count_ += 1
            #// For the last page, need to unset earlier children in order to keep track of orphans.
            if end_ >= total_top_ and count_ < start_:
                self.unset_children(e_, children_elements_)
            # end if
            if count_ < start_:
                continue
            # end if
            if count_ >= end_:
                break
            # end if
            self.display_element(e_, children_elements_, max_depth_, 0, args_, output_)
        # end for
        if end_ >= total_top_ and php_count(children_elements_) > 0:
            empty_array_ = Array()
            for orphans_ in children_elements_:
                for op_ in orphans_:
                    self.display_element(op_, empty_array_, 1, 0, args_, output_)
                # end for
            # end for
        # end if
        return output_
    # end def paged_walk
    #// 
    #// Calculates the total number of root elements.
    #// 
    #// @since 2.7.0
    #// 
    #// @param array $elements Elements to list.
    #// @return int Number of root elements.
    #//
    def get_number_of_root_elements(self, elements_=None):
        
        
        num_ = 0
        parent_field_ = self.db_fields["parent"]
        for e_ in elements_:
            if 0 == e_.parent_field_:
                num_ += 1
            # end if
        # end for
        return num_
    # end def get_number_of_root_elements
    #// 
    #// Unset all the children for a given top level element.
    #// 
    #// @since 2.7.0
    #// 
    #// @param object $e
    #// @param array $children_elements
    #//
    def unset_children(self, e_=None, children_elements_=None):
        
        
        if (not e_) or (not children_elements_):
            return
        # end if
        id_field_ = self.db_fields["id"]
        id_ = e_.id_field_
        if (not php_empty(lambda : children_elements_[id_])) and php_is_array(children_elements_[id_]):
            for child_ in children_elements_[id_]:
                self.unset_children(child_, children_elements_)
            # end for
        # end if
        children_elements_[id_] = None
    # end def unset_children
# end class Walker
