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
#// Parses unified or context diffs output from eg. the diff utility.
#// 
#// Example:
#// <code>
#// $patch = file_get_contents('example.patch');
#// $diff = new Text_Diff('string', array($patch));
#// $renderer = new Text_Diff_Renderer_inline();
#// echo $renderer->render($diff);
#// </code>
#// 
#// Copyright 2005 Örjan Persson <o@42mm.org>
#// Copyright 2005-2010 The Horde Project (http://www.horde.org/)
#// 
#// See the enclosed file COPYING for license information (LGPL). If you did
#// not receive this file, see http://opensource.org/licenses/lgpl-license.php.
#// 
#// @author  Örjan Persson <o@42mm.org>
#// @package Text_Diff
#// @since   0.2.0
#//
class Text_Diff_Engine_string():
    #// 
    #// Parses a unified or context diff.
    #// 
    #// First param contains the whole diff and the second can be used to force
    #// a specific diff type. If the second parameter is 'autodetect', the
    #// diff will be examined to find out which type of diff this is.
    #// 
    #// @param string $diff  The diff content.
    #// @param string $mode  The diff mode of the content in $diff. One of
    #// 'context', 'unified', or 'autodetect'.
    #// 
    #// @return array  List of all diff operations.
    #//
    def diff(self, diff=None, mode="autodetect"):
        
        #// Detect line breaks.
        lnbr = "\n"
        if php_strpos(diff, "\r\n") != False:
            lnbr = "\r\n"
        elif php_strpos(diff, "\r") != False:
            lnbr = "\r"
        # end if
        #// Make sure we have a line break at the EOF.
        if php_substr(diff, -php_strlen(lnbr)) != lnbr:
            diff += lnbr
        # end if
        if mode != "autodetect" and mode != "context" and mode != "unified":
            return PEAR.raiseerror("Type of diff is unsupported")
        # end if
        if mode == "autodetect":
            context = php_strpos(diff, "***")
            unified = php_strpos(diff, "---")
            if context == unified:
                return PEAR.raiseerror("Type of diff could not be detected")
            elif context == False or unified == False:
                mode = "context" if context != False else "unified"
            else:
                mode = "context" if context < unified else "unified"
            # end if
        # end if
        #// Split by new line and remove the diff header, if there is one.
        diff = php_explode(lnbr, diff)
        if mode == "context" and php_strpos(diff[0], "***") == 0 or mode == "unified" and php_strpos(diff[0], "---") == 0:
            php_array_shift(diff)
            php_array_shift(diff)
        # end if
        if mode == "context":
            return self.parsecontextdiff(diff)
        else:
            return self.parseunifieddiff(diff)
        # end if
    # end def diff
    #// 
    #// Parses an array containing the unified diff.
    #// 
    #// @param array $diff  Array of lines.
    #// 
    #// @return array  List of all diff operations.
    #//
    def parseunifieddiff(self, diff=None):
        
        edits = Array()
        end_ = php_count(diff) - 1
        i = 0
        while i < end_:
            
            diff1 = Array()
            for case in Switch(php_substr(diff[i], 0, 1)):
                if case(" "):
                    i += 1
                    while True:
                        diff1[-1] = php_substr(diff[i], 1)
                        
                        if i < end_ and php_substr(diff[i], 0, 1) == " ":
                            break
                        # end if
                    # end while
                    edits[-1] = php_new_class("Text_Diff_Op_copy", lambda : Text_Diff_Op_copy(diff1))
                    break
                # end if
                if case("+"):
                    i += 1
                    #// get all new lines
                    while True:
                        diff1[-1] = php_substr(diff[i], 1)
                        
                        if i < end_ and php_substr(diff[i], 0, 1) == "+":
                            break
                        # end if
                    # end while
                    edits[-1] = php_new_class("Text_Diff_Op_add", lambda : Text_Diff_Op_add(diff1))
                    break
                # end if
                if case("-"):
                    #// get changed or removed lines
                    diff2 = Array()
                    i += 1
                    while True:
                        diff1[-1] = php_substr(diff[i], 1)
                        
                        if i < end_ and php_substr(diff[i], 0, 1) == "-":
                            break
                        # end if
                    # end while
                    while True:
                        
                        if not (i < end_ and php_substr(diff[i], 0, 1) == "+"):
                            break
                        # end if
                        diff2[-1] = php_substr(diff[i], 1)
                        i += 1
                    # end while
                    if php_count(diff2) == 0:
                        edits[-1] = php_new_class("Text_Diff_Op_delete", lambda : Text_Diff_Op_delete(diff1))
                    else:
                        edits[-1] = php_new_class("Text_Diff_Op_change", lambda : Text_Diff_Op_change(diff1, diff2))
                    # end if
                    break
                # end if
                if case():
                    i += 1
                    break
                # end if
            # end for
            
        # end while
        return edits
    # end def parseunifieddiff
    #// 
    #// Parses an array containing the context diff.
    #// 
    #// @param array $diff  Array of lines.
    #// 
    #// @return array  List of all diff operations.
    #//
    def parsecontextdiff(self, diff=None):
        
        edits = Array()
        i = max_i = j = max_j = 0
        end_ = php_count(diff) - 1
        while True:
            
            if not (i < end_ and j < end_):
                break
            # end if
            while True:
                
                if not (i >= max_i and j >= max_j):
                    break
                # end if
                #// Find the boundaries of the diff output of the two files
                i = j
                while i < end_ and php_substr(diff[i], 0, 3) == "***":
                    
                    
                    i += 1
                # end while
                max_i = i
                while max_i < end_ and php_substr(diff[max_i], 0, 3) != "---":
                    
                    
                    max_i += 1
                # end while
                j = max_i
                while j < end_ and php_substr(diff[j], 0, 3) == "---":
                    
                    
                    j += 1
                # end while
                max_j = j
                while max_j < end_ and php_substr(diff[max_j], 0, 3) != "***":
                    
                    
                    max_j += 1
                # end while
            # end while
            #// find what hasn't been changed
            array = Array()
            while True:
                
                if not (i < max_i and j < max_j and strcmp(diff[i], diff[j]) == 0):
                    break
                # end if
                array[-1] = php_substr(diff[i], 2)
                i += 1
                j += 1
            # end while
            while True:
                
                if not (i < max_i and max_j - j <= 1):
                    break
                # end if
                if diff[i] != "" and php_substr(diff[i], 0, 1) != " ":
                    break
                # end if
                array[-1] = php_substr(diff[i], 2)
                i += 1
            # end while
            while True:
                
                if not (j < max_j and max_i - i <= 1):
                    break
                # end if
                if diff[j] != "" and php_substr(diff[j], 0, 1) != " ":
                    break
                # end if
                array[-1] = php_substr(diff[j], 2)
                j += 1
            # end while
            if php_count(array) > 0:
                edits[-1] = php_new_class("Text_Diff_Op_copy", lambda : Text_Diff_Op_copy(array))
            # end if
            if i < max_i:
                diff1 = Array()
                for case in Switch(php_substr(diff[i], 0, 1)):
                    if case("!"):
                        diff2 = Array()
                        i += 1
                        while True:
                            diff1[-1] = php_substr(diff[i], 2)
                            if j < max_j and php_substr(diff[j], 0, 1) == "!":
                                diff2[-1] = php_substr(diff[j], 2)
                                j += 1
                            # end if
                            
                            if i < max_i and php_substr(diff[i], 0, 1) == "!":
                                break
                            # end if
                        # end while
                        edits[-1] = php_new_class("Text_Diff_Op_change", lambda : Text_Diff_Op_change(diff1, diff2))
                        break
                    # end if
                    if case("+"):
                        i += 1
                        while True:
                            diff1[-1] = php_substr(diff[i], 2)
                            
                            if i < max_i and php_substr(diff[i], 0, 1) == "+":
                                break
                            # end if
                        # end while
                        edits[-1] = php_new_class("Text_Diff_Op_add", lambda : Text_Diff_Op_add(diff1))
                        break
                    # end if
                    if case("-"):
                        i += 1
                        while True:
                            diff1[-1] = php_substr(diff[i], 2)
                            
                            if i < max_i and php_substr(diff[i], 0, 1) == "-":
                                break
                            # end if
                        # end while
                        edits[-1] = php_new_class("Text_Diff_Op_delete", lambda : Text_Diff_Op_delete(diff1))
                        break
                    # end if
                # end for
            # end if
            if j < max_j:
                diff2 = Array()
                for case in Switch(php_substr(diff[j], 0, 1)):
                    if case("+"):
                        while True:
                            diff2[-1] = php_substr(diff[j], 2)
                            j += 1
                            
                            if j < max_j and php_substr(diff[j], 0, 1) == "+":
                                break
                            # end if
                        # end while
                        edits[-1] = php_new_class("Text_Diff_Op_add", lambda : Text_Diff_Op_add(diff2))
                        break
                    # end if
                    if case("-"):
                        while True:
                            diff2[-1] = php_substr(diff[j], 2)
                            j += 1
                            
                            if j < max_j and php_substr(diff[j], 0, 1) == "-":
                                break
                            # end if
                        # end while
                        edits[-1] = php_new_class("Text_Diff_Op_delete", lambda : Text_Diff_Op_delete(diff2))
                        break
                    # end if
                # end for
            # end if
        # end while
        return edits
    # end def parsecontextdiff
# end class Text_Diff_Engine_string
