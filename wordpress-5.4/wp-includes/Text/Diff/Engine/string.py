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
    def diff(self, diff_=None, mode_="autodetect"):
        
        
        #// Detect line breaks.
        lnbr_ = "\n"
        if php_strpos(diff_, "\r\n") != False:
            lnbr_ = "\r\n"
        elif php_strpos(diff_, "\r") != False:
            lnbr_ = "\r"
        # end if
        #// Make sure we have a line break at the EOF.
        if php_substr(diff_, -php_strlen(lnbr_)) != lnbr_:
            diff_ += lnbr_
        # end if
        if mode_ != "autodetect" and mode_ != "context" and mode_ != "unified":
            return PEAR.raiseerror("Type of diff is unsupported")
        # end if
        if mode_ == "autodetect":
            context_ = php_strpos(diff_, "***")
            unified_ = php_strpos(diff_, "---")
            if context_ == unified_:
                return PEAR.raiseerror("Type of diff could not be detected")
            elif context_ == False or unified_ == False:
                mode_ = "context" if context_ != False else "unified"
            else:
                mode_ = "context" if context_ < unified_ else "unified"
            # end if
        # end if
        #// Split by new line and remove the diff header, if there is one.
        diff_ = php_explode(lnbr_, diff_)
        if mode_ == "context" and php_strpos(diff_[0], "***") == 0 or mode_ == "unified" and php_strpos(diff_[0], "---") == 0:
            php_array_shift(diff_)
            php_array_shift(diff_)
        # end if
        if mode_ == "context":
            return self.parsecontextdiff(diff_)
        else:
            return self.parseunifieddiff(diff_)
        # end if
    # end def diff
    #// 
    #// Parses an array containing the unified diff.
    #// 
    #// @param array $diff  Array of lines.
    #// 
    #// @return array  List of all diff operations.
    #//
    def parseunifieddiff(self, diff_=None):
        
        
        edits_ = Array()
        end_ = php_count(diff_) - 1
        i_ = 0
        while i_ < end_:
            
            diff1_ = Array()
            for case in Switch(php_substr(diff_[i_], 0, 1)):
                if case(" "):
                    i_ += 1
                    while True:
                        diff1_[-1] = php_substr(diff_[i_], 1)
                        i_ += 1
                        if i_ < end_ and php_substr(diff_[i_], 0, 1) == " ":
                            break
                        # end if
                    # end while
                    edits_[-1] = php_new_class("Text_Diff_Op_copy", lambda : Text_Diff_Op_copy(diff1_))
                    break
                # end if
                if case("+"):
                    i_ += 1
                    #// get all new lines
                    while True:
                        diff1_[-1] = php_substr(diff_[i_], 1)
                        i_ += 1
                        if i_ < end_ and php_substr(diff_[i_], 0, 1) == "+":
                            break
                        # end if
                    # end while
                    edits_[-1] = php_new_class("Text_Diff_Op_add", lambda : Text_Diff_Op_add(diff1_))
                    break
                # end if
                if case("-"):
                    #// get changed or removed lines
                    diff2_ = Array()
                    i_ += 1
                    while True:
                        diff1_[-1] = php_substr(diff_[i_], 1)
                        i_ += 1
                        if i_ < end_ and php_substr(diff_[i_], 0, 1) == "-":
                            break
                        # end if
                    # end while
                    while True:
                        
                        if not (i_ < end_ and php_substr(diff_[i_], 0, 1) == "+"):
                            break
                        # end if
                        diff2_[-1] = php_substr(diff_[i_], 1)
                        i_ += 1
                    # end while
                    if php_count(diff2_) == 0:
                        edits_[-1] = php_new_class("Text_Diff_Op_delete", lambda : Text_Diff_Op_delete(diff1_))
                    else:
                        edits_[-1] = php_new_class("Text_Diff_Op_change", lambda : Text_Diff_Op_change(diff1_, diff2_))
                    # end if
                    break
                # end if
                if case():
                    i_ += 1
                    break
                # end if
            # end for
            
        # end while
        return edits_
    # end def parseunifieddiff
    #// 
    #// Parses an array containing the context diff.
    #// 
    #// @param array $diff  Array of lines.
    #// 
    #// @return array  List of all diff operations.
    #//
    def parsecontextdiff(self, diff_=None):
        
        
        edits_ = Array()
        i_ = max_i_ = j_ = max_j_ = 0
        end_ = php_count(diff_) - 1
        while True:
            
            if not (i_ < end_ and j_ < end_):
                break
            # end if
            while True:
                
                if not (i_ >= max_i_ and j_ >= max_j_):
                    break
                # end if
                #// Find the boundaries of the diff output of the two files
                i_ = j_
                while i_ < end_ and php_substr(diff_[i_], 0, 3) == "***":
                    
                    
                    i_ += 1
                # end while
                max_i_ = i_
                while max_i_ < end_ and php_substr(diff_[max_i_], 0, 3) != "---":
                    
                    
                    max_i_ += 1
                # end while
                j_ = max_i_
                while j_ < end_ and php_substr(diff_[j_], 0, 3) == "---":
                    
                    
                    j_ += 1
                # end while
                max_j_ = j_
                while max_j_ < end_ and php_substr(diff_[max_j_], 0, 3) != "***":
                    
                    
                    max_j_ += 1
                # end while
            # end while
            #// find what hasn't been changed
            array_ = Array()
            while True:
                
                if not (i_ < max_i_ and j_ < max_j_ and strcmp(diff_[i_], diff_[j_]) == 0):
                    break
                # end if
                array_[-1] = php_substr(diff_[i_], 2)
                i_ += 1
                j_ += 1
            # end while
            while True:
                
                if not (i_ < max_i_ and max_j_ - j_ <= 1):
                    break
                # end if
                if diff_[i_] != "" and php_substr(diff_[i_], 0, 1) != " ":
                    break
                # end if
                array_[-1] = php_substr(diff_[i_], 2)
                i_ += 1
            # end while
            while True:
                
                if not (j_ < max_j_ and max_i_ - i_ <= 1):
                    break
                # end if
                if diff_[j_] != "" and php_substr(diff_[j_], 0, 1) != " ":
                    break
                # end if
                array_[-1] = php_substr(diff_[j_], 2)
                j_ += 1
            # end while
            if php_count(array_) > 0:
                edits_[-1] = php_new_class("Text_Diff_Op_copy", lambda : Text_Diff_Op_copy(array_))
            # end if
            if i_ < max_i_:
                diff1_ = Array()
                for case in Switch(php_substr(diff_[i_], 0, 1)):
                    if case("!"):
                        diff2_ = Array()
                        i_ += 1
                        while True:
                            diff1_[-1] = php_substr(diff_[i_], 2)
                            if j_ < max_j_ and php_substr(diff_[j_], 0, 1) == "!":
                                diff2_[-1] = php_substr(diff_[j_], 2)
                                j_ += 1
                                j_ += 1
                            # end if
                            i_ += 1
                            if i_ < max_i_ and php_substr(diff_[i_], 0, 1) == "!":
                                break
                            # end if
                        # end while
                        edits_[-1] = php_new_class("Text_Diff_Op_change", lambda : Text_Diff_Op_change(diff1_, diff2_))
                        break
                    # end if
                    if case("+"):
                        i_ += 1
                        while True:
                            diff1_[-1] = php_substr(diff_[i_], 2)
                            i_ += 1
                            if i_ < max_i_ and php_substr(diff_[i_], 0, 1) == "+":
                                break
                            # end if
                        # end while
                        edits_[-1] = php_new_class("Text_Diff_Op_add", lambda : Text_Diff_Op_add(diff1_))
                        break
                    # end if
                    if case("-"):
                        i_ += 1
                        while True:
                            diff1_[-1] = php_substr(diff_[i_], 2)
                            i_ += 1
                            if i_ < max_i_ and php_substr(diff_[i_], 0, 1) == "-":
                                break
                            # end if
                        # end while
                        edits_[-1] = php_new_class("Text_Diff_Op_delete", lambda : Text_Diff_Op_delete(diff1_))
                        break
                    # end if
                # end for
            # end if
            if j_ < max_j_:
                diff2_ = Array()
                for case in Switch(php_substr(diff_[j_], 0, 1)):
                    if case("+"):
                        while True:
                            diff2_[-1] = php_substr(diff_[j_], 2)
                            j_ += 1
                            j_ += 1
                            
                            if j_ < max_j_ and php_substr(diff_[j_], 0, 1) == "+":
                                break
                            # end if
                        # end while
                        edits_[-1] = php_new_class("Text_Diff_Op_add", lambda : Text_Diff_Op_add(diff2_))
                        break
                    # end if
                    if case("-"):
                        while True:
                            diff2_[-1] = php_substr(diff_[j_], 2)
                            j_ += 1
                            j_ += 1
                            
                            if j_ < max_j_ and php_substr(diff_[j_], 0, 1) == "-":
                                break
                            # end if
                        # end while
                        edits_[-1] = php_new_class("Text_Diff_Op_delete", lambda : Text_Diff_Op_delete(diff2_))
                        break
                    # end if
                # end for
            # end if
        # end while
        return edits_
    # end def parsecontextdiff
# end class Text_Diff_Engine_string
