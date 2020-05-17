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
#// General API for generating and formatting diffs - the differences between
#// two sequences of strings.
#// 
#// The original PHP version of this code was written by Geoffrey T. Dairiki
#// <dairiki@dairiki.org>, and is used/adapted with his permission.
#// 
#// Copyright 2004 Geoffrey T. Dairiki <dairiki@dairiki.org>
#// Copyright 2004-2010 The Horde Project (http://www.horde.org/)
#// 
#// See the enclosed file COPYING for license information (LGPL). If you did
#// not receive this file, see http://opensource.org/licenses/lgpl-license.php.
#// 
#// @package Text_Diff
#// @author  Geoffrey T. Dairiki <dairiki@dairiki.org>
#//
class Text_Diff():
    #// 
    #// Array of changes.
    #// 
    #// @var array
    #//
    _edits = Array()
    #// 
    #// Computes diffs between sequences of strings.
    #// 
    #// @param string $engine     Name of the diffing engine to use.  'auto'
    #// will automatically select the best.
    #// @param array $params      Parameters to pass to the diffing engine.
    #// Normally an array of two arrays, each
    #// containing the lines from a file.
    #//
    def __init__(self, engine_=None, params_=None):
        
        
        #// Backward compatibility workaround.
        if (not php_is_string(engine_)):
            params_ = Array(engine_, params_)
            engine_ = "auto"
        # end if
        if engine_ == "auto":
            engine_ = "xdiff" if php_extension_loaded("xdiff") else "native"
        else:
            engine_ = php_basename(engine_)
        # end if
        #// WP #7391
        php_include_file(php_dirname(__FILE__) + "/Diff/Engine/" + engine_ + ".php", once=True)
        class_ = "Text_Diff_Engine_" + engine_
        diff_engine_ = php_new_class(class_, lambda : {**locals(), **globals()}[class_]())
        self._edits = call_user_func_array(Array(diff_engine_, "diff"), params_)
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def text_diff(self, engine_=None, params_=None):
        
        
        self.__init__(engine_, params_)
    # end def text_diff
    #// 
    #// Returns the array of differences.
    #//
    def getdiff(self):
        
        
        return self._edits
    # end def getdiff
    #// 
    #// returns the number of new (added) lines in a given diff.
    #// 
    #// @since Text_Diff 1.1.0
    #// 
    #// @return integer The number of new lines
    #//
    def countaddedlines(self):
        
        
        count_ = 0
        for edit_ in self._edits:
            if php_is_a(edit_, "Text_Diff_Op_add") or php_is_a(edit_, "Text_Diff_Op_change"):
                count_ += edit_.nfinal()
            # end if
        # end for
        return count_
    # end def countaddedlines
    #// 
    #// Returns the number of deleted (removed) lines in a given diff.
    #// 
    #// @since Text_Diff 1.1.0
    #// 
    #// @return integer The number of deleted lines
    #//
    def countdeletedlines(self):
        
        
        count_ = 0
        for edit_ in self._edits:
            if php_is_a(edit_, "Text_Diff_Op_delete") or php_is_a(edit_, "Text_Diff_Op_change"):
                count_ += edit_.norig()
            # end if
        # end for
        return count_
    # end def countdeletedlines
    #// 
    #// Computes a reversed diff.
    #// 
    #// Example:
    #// <code>
    #// $diff = new Text_Diff($lines1, $lines2);
    #// $rev = $diff->reverse();
    #// </code>
    #// 
    #// @return Text_Diff  A Diff object representing the inverse of the
    #// original diff.  Note that we purposely don't return a
    #// reference here, since this essentially is a clone()
    #// method.
    #//
    def reverse(self):
        
        
        if php_version_compare(php_zend_version(), "2", ">"):
            rev_ = copy.deepcopy(self)
        else:
            rev_ = self
        # end if
        rev_._edits = Array()
        for edit_ in self._edits:
            rev_._edits[-1] = edit_.reverse()
        # end for
        return rev_
    # end def reverse
    #// 
    #// Checks for an empty diff.
    #// 
    #// @return boolean  True if two sequences were identical.
    #//
    def isempty(self):
        
        
        for edit_ in self._edits:
            if (not php_is_a(edit_, "Text_Diff_Op_copy")):
                return False
            # end if
        # end for
        return True
    # end def isempty
    #// 
    #// Computes the length of the Longest Common Subsequence (LCS).
    #// 
    #// This is mostly for diagnostic purposes.
    #// 
    #// @return integer  The length of the LCS.
    #//
    def lcs(self):
        
        
        lcs_ = 0
        for edit_ in self._edits:
            if php_is_a(edit_, "Text_Diff_Op_copy"):
                lcs_ += php_count(edit_.orig)
            # end if
        # end for
        return lcs_
    # end def lcs
    #// 
    #// Gets the original set of lines.
    #// 
    #// This reconstructs the $from_lines parameter passed to the constructor.
    #// 
    #// @return array  The original sequence of strings.
    #//
    def getoriginal(self):
        
        
        lines_ = Array()
        for edit_ in self._edits:
            if edit_.orig:
                array_splice(lines_, php_count(lines_), 0, edit_.orig)
            # end if
        # end for
        return lines_
    # end def getoriginal
    #// 
    #// Gets the final set of lines.
    #// 
    #// This reconstructs the $to_lines parameter passed to the constructor.
    #// 
    #// @return array  The sequence of strings.
    #//
    def getfinal(self):
        
        
        lines_ = Array()
        for edit_ in self._edits:
            if edit_.final:
                array_splice(lines_, php_count(lines_), 0, edit_.final)
            # end if
        # end for
        return lines_
    # end def getfinal
    #// 
    #// Removes trailing newlines from a line of text. This is meant to be used
    #// with array_walk().
    #// 
    #// @param string $line  The line to trim.
    #// @param integer $key  The index of the line in the array. Not used.
    #//
    def trimnewlines(self, line_=None, key_=None):
        
        
        line_ = php_str_replace(Array("\n", "\r"), "", line_)
    # end def trimnewlines
    #// 
    #// Determines the location of the system temporary directory.
    #// 
    #// @static
    #// 
    #// @access protected
    #// 
    #// @return string  A directory name which can be used for temp files.
    #// Returns false if one could not be found.
    #//
    def _gettempdir(self):
        
        
        tmp_locations_ = Array("/tmp", "/var/tmp", "c:\\WUTemp", "c:\\temp", "c:\\windows\\temp", "c:\\winnt\\temp")
        #// Try PHP's upload_tmp_dir directive.
        tmp_ = php_ini_get("upload_tmp_dir")
        #// Otherwise, try to determine the TMPDIR environment variable.
        if (not php_strlen(tmp_)):
            tmp_ = php_getenv("TMPDIR")
        # end if
        #// If we still cannot determine a value, then cycle through a list of
        #// preset possibilities.
        while True:
            
            if not ((not php_strlen(tmp_)) and php_count(tmp_locations_)):
                break
            # end if
            tmp_check_ = php_array_shift(tmp_locations_)
            if php_no_error(lambda: php_is_dir(tmp_check_)):
                tmp_ = tmp_check_
            # end if
        # end while
        #// If it is still empty, we have failed, so return false; otherwise
        #// return the directory determined.
        return tmp_ if php_strlen(tmp_) else False
    # end def _gettempdir
    #// 
    #// Checks a diff for validity.
    #// 
    #// This is here only for debugging purposes.
    #//
    def _check(self, from_lines_=None, to_lines_=None):
        
        
        if serialize(from_lines_) != serialize(self.getoriginal()):
            trigger_error("Reconstructed original doesn't match", E_USER_ERROR)
        # end if
        if serialize(to_lines_) != serialize(self.getfinal()):
            trigger_error("Reconstructed final doesn't match", E_USER_ERROR)
        # end if
        rev_ = self.reverse()
        if serialize(to_lines_) != serialize(rev_.getoriginal()):
            trigger_error("Reversed original doesn't match", E_USER_ERROR)
        # end if
        if serialize(from_lines_) != serialize(rev_.getfinal()):
            trigger_error("Reversed final doesn't match", E_USER_ERROR)
        # end if
        prevtype_ = None
        for edit_ in self._edits:
            if prevtype_ == get_class(edit_):
                trigger_error("Edit sequence is non-optimal", E_USER_ERROR)
            # end if
            prevtype_ = get_class(edit_)
        # end for
        return True
    # end def _check
# end class Text_Diff
#// 
#// @package Text_Diff
#// @author  Geoffrey T. Dairiki <dairiki@dairiki.org>
#//
class Text_MappedDiff(Text_Diff):
    #// 
    #// Computes a diff between sequences of strings.
    #// 
    #// This can be used to compute things like case-insensitve diffs, or diffs
    #// which ignore changes in white-space.
    #// 
    #// @param array $from_lines         An array of strings.
    #// @param array $to_lines           An array of strings.
    #// @param array $mapped_from_lines  This array should have the same size
    #// number of elements as $from_lines.  The
    #// elements in $mapped_from_lines and
    #// $mapped_to_lines are what is actually
    #// compared when computing the diff.
    #// @param array $mapped_to_lines    This array should have the same number
    #// of elements as $to_lines.
    #//
    def __init__(self, from_lines_=None, to_lines_=None, mapped_from_lines_=None, mapped_to_lines_=None):
        
        
        assert(php_count(from_lines_) == php_count(mapped_from_lines_))
        assert(php_count(to_lines_) == php_count(mapped_to_lines_))
        super().text_diff(mapped_from_lines_, mapped_to_lines_)
        xi_ = yi_ = 0
        i_ = 0
        while i_ < php_count(self._edits):
            
            orig_ = self._edits[i_].orig
            if php_is_array(orig_):
                orig_ = php_array_slice(from_lines_, xi_, php_count(orig_))
                xi_ += php_count(orig_)
            # end if
            final_ = self._edits[i_].final
            if php_is_array(final_):
                final_ = php_array_slice(to_lines_, yi_, php_count(final_))
                yi_ += php_count(final_)
            # end if
            i_ += 1
        # end while
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def text_mappeddiff(self, from_lines_=None, to_lines_=None, mapped_from_lines_=None, mapped_to_lines_=None):
        
        
        self.__init__(from_lines_, to_lines_, mapped_from_lines_, mapped_to_lines_)
    # end def text_mappeddiff
# end class Text_MappedDiff
#// 
#// @package Text_Diff
#// @author  Geoffrey T. Dairiki <dairiki@dairiki.org>
#// 
#// @access private
#//
class Text_Diff_Op():
    orig = Array()
    final = Array()
    def reverse(self):
        
        
        trigger_error("Abstract method", E_USER_ERROR)
    # end def reverse
    def norig(self):
        
        
        return php_count(self.orig) if self.orig else 0
    # end def norig
    def nfinal(self):
        
        
        return php_count(self.final) if self.final else 0
    # end def nfinal
# end class Text_Diff_Op
#// 
#// @package Text_Diff
#// @author  Geoffrey T. Dairiki <dairiki@dairiki.org>
#// 
#// @access private
#//
class Text_Diff_Op_copy(Text_Diff_Op):
    #// 
    #// PHP5 constructor.
    #//
    def __init__(self, orig_=None, final_=None):
        if final_ is None:
            final_ = False
        # end if
        
        if (not php_is_array(final_)):
            final_ = orig_
        # end if
        self.orig = orig_
        self.final = final_
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def text_diff_op_copy(self, orig_=None, final_=None):
        if final_ is None:
            final_ = False
        # end if
        
        self.__init__(orig_, final_)
    # end def text_diff_op_copy
    def reverse(self):
        
        
        reverse_ = php_new_class("Text_Diff_Op_copy", lambda : Text_Diff_Op_copy(self.final, self.orig))
        return reverse_
    # end def reverse
# end class Text_Diff_Op_copy
#// 
#// @package Text_Diff
#// @author  Geoffrey T. Dairiki <dairiki@dairiki.org>
#// 
#// @access private
#//
class Text_Diff_Op_delete(Text_Diff_Op):
    #// 
    #// PHP5 constructor.
    #//
    def __init__(self, lines_=None):
        
        
        self.orig = lines_
        self.final = False
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def text_diff_op_delete(self, lines_=None):
        
        
        self.__init__(lines_)
    # end def text_diff_op_delete
    def reverse(self):
        
        
        reverse_ = php_new_class("Text_Diff_Op_add", lambda : Text_Diff_Op_add(self.orig))
        return reverse_
    # end def reverse
# end class Text_Diff_Op_delete
#// 
#// @package Text_Diff
#// @author  Geoffrey T. Dairiki <dairiki@dairiki.org>
#// 
#// @access private
#//
class Text_Diff_Op_add(Text_Diff_Op):
    #// 
    #// PHP5 constructor.
    #//
    def __init__(self, lines_=None):
        
        
        self.final = lines_
        self.orig = False
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def text_diff_op_add(self, lines_=None):
        
        
        self.__init__(lines_)
    # end def text_diff_op_add
    def reverse(self):
        
        
        reverse_ = php_new_class("Text_Diff_Op_delete", lambda : Text_Diff_Op_delete(self.final))
        return reverse_
    # end def reverse
# end class Text_Diff_Op_add
#// 
#// @package Text_Diff
#// @author  Geoffrey T. Dairiki <dairiki@dairiki.org>
#// 
#// @access private
#//
class Text_Diff_Op_change(Text_Diff_Op):
    #// 
    #// PHP5 constructor.
    #//
    def __init__(self, orig_=None, final_=None):
        
        
        self.orig = orig_
        self.final = final_
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def text_diff_op_change(self, orig_=None, final_=None):
        
        
        self.__init__(orig_, final_)
    # end def text_diff_op_change
    def reverse(self):
        
        
        reverse_ = php_new_class("Text_Diff_Op_change", lambda : Text_Diff_Op_change(self.final, self.orig))
        return reverse_
    # end def reverse
# end class Text_Diff_Op_change
