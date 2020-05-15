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
    def __init__(self, engine=None, params=None):
        
        #// Backward compatibility workaround.
        if (not php_is_string(engine)):
            params = Array(engine, params)
            engine = "auto"
        # end if
        if engine == "auto":
            engine = "xdiff" if php_extension_loaded("xdiff") else "native"
        else:
            engine = php_basename(engine)
        # end if
        #// WP #7391
        php_include_file(php_dirname(__FILE__) + "/Diff/Engine/" + engine + ".php", once=True)
        class_ = "Text_Diff_Engine_" + engine
        diff_engine = php_new_class(class_, lambda : {**locals(), **globals()}[class_]())
        self._edits = call_user_func_array(Array(diff_engine, "diff"), params)
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def text_diff(self, engine=None, params=None):
        
        self.__init__(engine, params)
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
        
        count = 0
        for edit in self._edits:
            if php_is_a(edit, "Text_Diff_Op_add") or php_is_a(edit, "Text_Diff_Op_change"):
                count += edit.nfinal()
            # end if
        # end for
        return count
    # end def countaddedlines
    #// 
    #// Returns the number of deleted (removed) lines in a given diff.
    #// 
    #// @since Text_Diff 1.1.0
    #// 
    #// @return integer The number of deleted lines
    #//
    def countdeletedlines(self):
        
        count = 0
        for edit in self._edits:
            if php_is_a(edit, "Text_Diff_Op_delete") or php_is_a(edit, "Text_Diff_Op_change"):
                count += edit.norig()
            # end if
        # end for
        return count
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
            rev = copy.deepcopy(self)
        else:
            rev = self
        # end if
        rev._edits = Array()
        for edit in self._edits:
            rev._edits[-1] = edit.reverse()
        # end for
        return rev
    # end def reverse
    #// 
    #// Checks for an empty diff.
    #// 
    #// @return boolean  True if two sequences were identical.
    #//
    def isempty(self):
        
        for edit in self._edits:
            if (not php_is_a(edit, "Text_Diff_Op_copy")):
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
        
        lcs = 0
        for edit in self._edits:
            if php_is_a(edit, "Text_Diff_Op_copy"):
                lcs += php_count(edit.orig)
            # end if
        # end for
        return lcs
    # end def lcs
    #// 
    #// Gets the original set of lines.
    #// 
    #// This reconstructs the $from_lines parameter passed to the constructor.
    #// 
    #// @return array  The original sequence of strings.
    #//
    def getoriginal(self):
        
        lines = Array()
        for edit in self._edits:
            if edit.orig:
                array_splice(lines, php_count(lines), 0, edit.orig)
            # end if
        # end for
        return lines
    # end def getoriginal
    #// 
    #// Gets the final set of lines.
    #// 
    #// This reconstructs the $to_lines parameter passed to the constructor.
    #// 
    #// @return array  The sequence of strings.
    #//
    def getfinal(self):
        
        lines = Array()
        for edit in self._edits:
            if edit.final:
                array_splice(lines, php_count(lines), 0, edit.final)
            # end if
        # end for
        return lines
    # end def getfinal
    #// 
    #// Removes trailing newlines from a line of text. This is meant to be used
    #// with array_walk().
    #// 
    #// @param string $line  The line to trim.
    #// @param integer $key  The index of the line in the array. Not used.
    #//
    def trimnewlines(self, line=None, key=None):
        
        line = php_str_replace(Array("\n", "\r"), "", line)
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
        
        tmp_locations = Array("/tmp", "/var/tmp", "c:\\WUTemp", "c:\\temp", "c:\\windows\\temp", "c:\\winnt\\temp")
        #// Try PHP's upload_tmp_dir directive.
        tmp = php_ini_get("upload_tmp_dir")
        #// Otherwise, try to determine the TMPDIR environment variable.
        if (not php_strlen(tmp)):
            tmp = php_getenv("TMPDIR")
        # end if
        #// If we still cannot determine a value, then cycle through a list of
        #// preset possibilities.
        while True:
            
            if not ((not php_strlen(tmp)) and php_count(tmp_locations)):
                break
            # end if
            tmp_check = php_array_shift(tmp_locations)
            if php_no_error(lambda: php_is_dir(tmp_check)):
                tmp = tmp_check
            # end if
        # end while
        #// If it is still empty, we have failed, so return false; otherwise
        #// return the directory determined.
        return tmp if php_strlen(tmp) else False
    # end def _gettempdir
    #// 
    #// Checks a diff for validity.
    #// 
    #// This is here only for debugging purposes.
    #//
    def _check(self, from_lines=None, to_lines=None):
        
        if serialize(from_lines) != serialize(self.getoriginal()):
            trigger_error("Reconstructed original doesn't match", E_USER_ERROR)
        # end if
        if serialize(to_lines) != serialize(self.getfinal()):
            trigger_error("Reconstructed final doesn't match", E_USER_ERROR)
        # end if
        rev = self.reverse()
        if serialize(to_lines) != serialize(rev.getoriginal()):
            trigger_error("Reversed original doesn't match", E_USER_ERROR)
        # end if
        if serialize(from_lines) != serialize(rev.getfinal()):
            trigger_error("Reversed final doesn't match", E_USER_ERROR)
        # end if
        prevtype = None
        for edit in self._edits:
            if prevtype == get_class(edit):
                trigger_error("Edit sequence is non-optimal", E_USER_ERROR)
            # end if
            prevtype = get_class(edit)
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
    def __init__(self, from_lines=None, to_lines=None, mapped_from_lines=None, mapped_to_lines=None):
        
        assert(php_count(from_lines) == php_count(mapped_from_lines))
        assert(php_count(to_lines) == php_count(mapped_to_lines))
        super().text_diff(mapped_from_lines, mapped_to_lines)
        xi = yi = 0
        i = 0
        while i < php_count(self._edits):
            
            orig = self._edits[i].orig
            if php_is_array(orig):
                orig = php_array_slice(from_lines, xi, php_count(orig))
                xi += php_count(orig)
            # end if
            final = self._edits[i].final
            if php_is_array(final):
                final = php_array_slice(to_lines, yi, php_count(final))
                yi += php_count(final)
            # end if
            i += 1
        # end while
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def text_mappeddiff(self, from_lines=None, to_lines=None, mapped_from_lines=None, mapped_to_lines=None):
        
        self.__init__(from_lines, to_lines, mapped_from_lines, mapped_to_lines)
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
    def __init__(self, orig=None, final=False):
        
        if (not php_is_array(final)):
            final = orig
        # end if
        self.orig = orig
        self.final = final
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def text_diff_op_copy(self, orig=None, final=False):
        
        self.__init__(orig, final)
    # end def text_diff_op_copy
    def reverse(self):
        
        reverse = php_new_class("Text_Diff_Op_copy", lambda : Text_Diff_Op_copy(self.final, self.orig))
        return reverse
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
    def __init__(self, lines=None):
        
        self.orig = lines
        self.final = False
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def text_diff_op_delete(self, lines=None):
        
        self.__init__(lines)
    # end def text_diff_op_delete
    def reverse(self):
        
        reverse = php_new_class("Text_Diff_Op_add", lambda : Text_Diff_Op_add(self.orig))
        return reverse
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
    def __init__(self, lines=None):
        
        self.final = lines
        self.orig = False
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def text_diff_op_add(self, lines=None):
        
        self.__init__(lines)
    # end def text_diff_op_add
    def reverse(self):
        
        reverse = php_new_class("Text_Diff_Op_delete", lambda : Text_Diff_Op_delete(self.final))
        return reverse
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
    def __init__(self, orig=None, final=None):
        
        self.orig = orig
        self.final = final
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def text_diff_op_change(self, orig=None, final=None):
        
        self.__init__(orig, final)
    # end def text_diff_op_change
    def reverse(self):
        
        reverse = php_new_class("Text_Diff_Op_change", lambda : Text_Diff_Op_change(self.final, self.orig))
        return reverse
    # end def reverse
# end class Text_Diff_Op_change
