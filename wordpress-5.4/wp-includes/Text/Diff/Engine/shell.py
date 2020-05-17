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
#// Class used internally by Diff to actually compute the diffs.
#// 
#// This class uses the Unix `diff` program via shell_exec to compute the
#// differences between the two input arrays.
#// 
#// Copyright 2007-2010 The Horde Project (http://www.horde.org/)
#// 
#// See the enclosed file COPYING for license information (LGPL). If you did
#// not receive this file, see http://opensource.org/licenses/lgpl-license.php.
#// 
#// @author  Milian Wolff <mail@milianw.de>
#// @package Text_Diff
#// @since   0.3.0
#//
class Text_Diff_Engine_shell():
    #// 
    #// Path to the diff executable
    #// 
    #// @var string
    #//
    _diffCommand = "diff"
    #// 
    #// Returns the array of differences.
    #// 
    #// @param array $from_lines lines of text from old file
    #// @param array $to_lines   lines of text from new file
    #// 
    #// @return array all changes made (array with Text_Diff_Op_* objects)
    #//
    def diff(self, from_lines_=None, to_lines_=None):
        
        
        array_walk(from_lines_, Array("Text_Diff", "trimNewlines"))
        array_walk(to_lines_, Array("Text_Diff", "trimNewlines"))
        temp_dir_ = Text_Diff._gettempdir()
        #// Execute gnu diff or similar to get a standard diff file.
        from_file_ = php_tempnam(temp_dir_, "Text_Diff")
        to_file_ = php_tempnam(temp_dir_, "Text_Diff")
        fp_ = fopen(from_file_, "w")
        fwrite(fp_, php_implode("\n", from_lines_))
        php_fclose(fp_)
        fp_ = fopen(to_file_, "w")
        fwrite(fp_, php_implode("\n", to_lines_))
        php_fclose(fp_)
        diff_ = shell_exec(self._diffCommand + " " + from_file_ + " " + to_file_)
        unlink(from_file_)
        unlink(to_file_)
        if is_null(diff_):
            #// No changes were made
            return Array(php_new_class("Text_Diff_Op_copy", lambda : Text_Diff_Op_copy(from_lines_)))
        # end if
        from_line_no_ = 1
        to_line_no_ = 1
        edits_ = Array()
        #// Get changed lines by parsing something like:
        #// 0a1,2
        #// 1,2c4,6
        #// 1,5d6
        preg_match_all("#^(\\d+)(?:,(\\d+))?([adc])(\\d+)(?:,(\\d+))?$#m", diff_, matches_, PREG_SET_ORDER)
        for match_ in matches_:
            if (not (php_isset(lambda : match_[5]))):
                #// This paren is not set every time (see regex).
                match_[5] = False
            # end if
            if match_[3] == "a":
                from_line_no_ -= 1
            # end if
            if match_[3] == "d":
                to_line_no_ -= 1
            # end if
            if from_line_no_ < match_[1] or to_line_no_ < match_[4]:
                #// copied lines
                assert("$match[1] - $from_line_no == $match[4] - $to_line_no")
                php_array_push(edits_, php_new_class("Text_Diff_Op_copy", lambda : Text_Diff_Op_copy(self._getlines(from_lines_, from_line_no_, match_[1] - 1), self._getlines(to_lines_, to_line_no_, match_[4] - 1))))
            # end if
            for case in Switch(match_[3]):
                if case("d"):
                    #// deleted lines
                    php_array_push(edits_, php_new_class("Text_Diff_Op_delete", lambda : Text_Diff_Op_delete(self._getlines(from_lines_, from_line_no_, match_[2]))))
                    to_line_no_ += 1
                    break
                # end if
                if case("c"):
                    #// changed lines
                    php_array_push(edits_, php_new_class("Text_Diff_Op_change", lambda : Text_Diff_Op_change(self._getlines(from_lines_, from_line_no_, match_[2]), self._getlines(to_lines_, to_line_no_, match_[5]))))
                    break
                # end if
                if case("a"):
                    #// added lines
                    php_array_push(edits_, php_new_class("Text_Diff_Op_add", lambda : Text_Diff_Op_add(self._getlines(to_lines_, to_line_no_, match_[5]))))
                    from_line_no_ += 1
                    break
                # end if
            # end for
        # end for
        if (not php_empty(lambda : from_lines_)):
            #// Some lines might still be pending. Add them as copied
            php_array_push(edits_, php_new_class("Text_Diff_Op_copy", lambda : Text_Diff_Op_copy(self._getlines(from_lines_, from_line_no_, from_line_no_ + php_count(from_lines_) - 1), self._getlines(to_lines_, to_line_no_, to_line_no_ + php_count(to_lines_) - 1))))
        # end if
        return edits_
    # end def diff
    #// 
    #// Get lines from either the old or new text
    #// 
    #// @access private
    #// 
    #// @param array $text_lines Either $from_lines or $to_lines (passed by reference).
    #// @param int   $line_no    Current line number (passed by reference).
    #// @param int   $end        Optional end line, when we want to chop more
    #// than one line.
    #// 
    #// @return array The chopped lines
    #//
    def _getlines(self, text_lines_=None, line_no_=None, end_=None):
        if end_ is None:
            end_ = False
        # end if
        
        if (not php_empty(lambda : end_)):
            lines_ = Array()
            #// We can shift even more
            while True:
                
                if not (line_no_ <= end_):
                    break
                # end if
                php_array_push(lines_, php_array_shift(text_lines_))
                line_no_ += 1
            # end while
        else:
            lines_ = Array(php_array_shift(text_lines_))
            line_no_ += 1
        # end if
        return lines_
    # end def _getlines
# end class Text_Diff_Engine_shell
