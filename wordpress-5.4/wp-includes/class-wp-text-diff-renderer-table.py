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
#// Diff API: WP_Text_Diff_Renderer_Table class
#// 
#// @package WordPress
#// @subpackage Diff
#// @since 4.7.0
#// 
#// 
#// Table renderer to display the diff lines.
#// 
#// @since 2.6.0
#// @uses Text_Diff_Renderer Extends
#//
class WP_Text_Diff_Renderer_Table(Text_Diff_Renderer):
    #// 
    #// @see Text_Diff_Renderer::_leading_context_lines
    #// @var int
    #// @since 2.6.0
    #//
    _leading_context_lines = 10000
    #// 
    #// @see Text_Diff_Renderer::_trailing_context_lines
    #// @var int
    #// @since 2.6.0
    #//
    _trailing_context_lines = 10000
    #// 
    #// Threshold for when a diff should be saved or omitted.
    #// 
    #// @var float
    #// @since 2.6.0
    #//
    _diff_threshold = 0.6
    #// 
    #// Inline display helper object name.
    #// 
    #// @var string
    #// @since 2.6.0
    #//
    inline_diff_renderer = "WP_Text_Diff_Renderer_inline"
    #// 
    #// Should we show the split view or not
    #// 
    #// @var string
    #// @since 3.6.0
    #//
    _show_split_view = True
    compat_fields = Array("_show_split_view", "inline_diff_renderer", "_diff_threshold")
    #// 
    #// Caches the output of count_chars() in compute_string_distance()
    #// 
    #// @var array
    #// @since 5.0.0
    #//
    count_cache = Array()
    #// 
    #// Caches the difference calculation in compute_string_distance()
    #// 
    #// @var array
    #// @since 5.0.0
    #//
    difference_cache = Array()
    #// 
    #// Constructor - Call parent constructor with params array.
    #// 
    #// This will set class properties based on the key value pairs in the array.
    #// 
    #// @since 2.6.0
    #// 
    #// @param array $params
    #//
    def __init__(self, params_=None):
        if params_ is None:
            params_ = Array()
        # end if
        
        super().__init__(params_)
        if (php_isset(lambda : params_["show_split_view"])):
            self._show_split_view = params_["show_split_view"]
        # end if
    # end def __init__
    #// 
    #// @ignore
    #// 
    #// @param string $header
    #// @return string
    #//
    def _startblock(self, header_=None):
        
        
        return ""
    # end def _startblock
    #// 
    #// @ignore
    #// 
    #// @param array $lines
    #// @param string $prefix
    #//
    def _lines(self, lines_=None, prefix_=" "):
        
        
        pass
    # end def _lines
    #// 
    #// @ignore
    #// 
    #// @param string $line HTML-escape the value.
    #// @return string
    #//
    def addedline(self, line_=None):
        
        
        return "<td class='diff-addedline'><span aria-hidden='true' class='dashicons dashicons-plus'></span><span class='screen-reader-text'>" + __("Added:") + str(" </span>") + str(line_) + str("</td>")
    # end def addedline
    #// 
    #// @ignore
    #// 
    #// @param string $line HTML-escape the value.
    #// @return string
    #//
    def deletedline(self, line_=None):
        
        
        return "<td class='diff-deletedline'><span aria-hidden='true' class='dashicons dashicons-minus'></span><span class='screen-reader-text'>" + __("Deleted:") + str(" </span>") + str(line_) + str("</td>")
    # end def deletedline
    #// 
    #// @ignore
    #// 
    #// @param string $line HTML-escape the value.
    #// @return string
    #//
    def contextline(self, line_=None):
        
        
        return "<td class='diff-context'><span class='screen-reader-text'>" + __("Unchanged:") + str(" </span>") + str(line_) + str("</td>")
    # end def contextline
    #// 
    #// @ignore
    #// 
    #// @return string
    #//
    def emptyline(self):
        
        
        return "<td>&nbsp;</td>"
    # end def emptyline
    #// 
    #// @ignore
    #// 
    #// @param array $lines
    #// @param bool $encode
    #// @return string
    #//
    def _added(self, lines_=None, encode_=None):
        if encode_ is None:
            encode_ = True
        # end if
        
        r_ = ""
        for line_ in lines_:
            if encode_:
                processed_line_ = htmlspecialchars(line_)
                #// 
                #// Contextually filters a diffed line.
                #// 
                #// Filters TextDiff processing of diffed line. By default, diffs are processed with
                #// htmlspecialchars. Use this filter to remove or change the processing. Passes a context
                #// indicating if the line is added, deleted or unchanged.
                #// 
                #// @since 4.1.0
                #// 
                #// @param string $processed_line The processed diffed line.
                #// @param string $line           The unprocessed diffed line.
                #// @param string $context        The line context. Values are 'added', 'deleted' or 'unchanged'.
                #//
                line_ = apply_filters("process_text_diff_html", processed_line_, line_, "added")
            # end if
            if self._show_split_view:
                r_ += "<tr>" + self.emptyline() + self.emptyline() + self.addedline(line_) + "</tr>\n"
            else:
                r_ += "<tr>" + self.addedline(line_) + "</tr>\n"
            # end if
        # end for
        return r_
    # end def _added
    #// 
    #// @ignore
    #// 
    #// @param array $lines
    #// @param bool $encode
    #// @return string
    #//
    def _deleted(self, lines_=None, encode_=None):
        if encode_ is None:
            encode_ = True
        # end if
        
        r_ = ""
        for line_ in lines_:
            if encode_:
                processed_line_ = htmlspecialchars(line_)
                #// This filter is documented in wp-includes/wp-diff.php
                line_ = apply_filters("process_text_diff_html", processed_line_, line_, "deleted")
            # end if
            if self._show_split_view:
                r_ += "<tr>" + self.deletedline(line_) + self.emptyline() + self.emptyline() + "</tr>\n"
            else:
                r_ += "<tr>" + self.deletedline(line_) + "</tr>\n"
            # end if
        # end for
        return r_
    # end def _deleted
    #// 
    #// @ignore
    #// 
    #// @param array $lines
    #// @param bool $encode
    #// @return string
    #//
    def _context(self, lines_=None, encode_=None):
        if encode_ is None:
            encode_ = True
        # end if
        
        r_ = ""
        for line_ in lines_:
            if encode_:
                processed_line_ = htmlspecialchars(line_)
                #// This filter is documented in wp-includes/wp-diff.php
                line_ = apply_filters("process_text_diff_html", processed_line_, line_, "unchanged")
            # end if
            if self._show_split_view:
                r_ += "<tr>" + self.contextline(line_) + self.emptyline() + self.contextline(line_) + "</tr>\n"
            else:
                r_ += "<tr>" + self.contextline(line_) + "</tr>\n"
            # end if
        # end for
        return r_
    # end def _context
    #// 
    #// Process changed lines to do word-by-word diffs for extra highlighting.
    #// 
    #// (TRAC style) sometimes these lines can actually be deleted or added rows.
    #// We do additional processing to figure that out
    #// 
    #// @since 2.6.0
    #// 
    #// @param array $orig
    #// @param array $final
    #// @return string
    #//
    def _changed(self, orig_=None, final_=None):
        
        
        r_ = ""
        #// 
        #// Does the aforementioned additional processing:
        #// _matches tell what rows are "the same" in orig and final. Those pairs will be diffed to get word changes.
        #// - match is numeric: an index in other column.
        #// - match is 'X': no match. It is a new row.
        #// _rows are column vectors for the orig column and the final column.
        #// - row >= 0: an indix of the $orig or $final array.
        #// - row < 0: a blank row for that column.
        #//
        orig_matches_, final_matches_, orig_rows_, final_rows_ = self.interleave_changed_lines(orig_, final_)
        #// These will hold the word changes as determined by an inline diff.
        orig_diffs_ = Array()
        final_diffs_ = Array()
        #// Compute word diffs for each matched pair using the inline diff.
        for o_,f_ in orig_matches_.items():
            if php_is_numeric(o_) and php_is_numeric(f_):
                text_diff_ = php_new_class("Text_Diff", lambda : Text_Diff("auto", Array(Array(orig_[o_]), Array(final_[f_]))))
                renderer_ = php_new_class(self.inline_diff_renderer, lambda : {**locals(), **globals()}[self.inline_diff_renderer]())
                diff_ = renderer_.render(text_diff_)
                #// If they're too different, don't include any <ins> or <del>'s.
                if preg_match_all("!(<ins>.*?</ins>|<del>.*?</del>)!", diff_, diff_matches_):
                    #// Length of all text between <ins> or <del>.
                    stripped_matches_ = php_strlen(strip_tags(join(" ", diff_matches_[0])))
                    #// Since we count length of text between <ins> or <del> (instead of picking just one),
                    #// we double the length of chars not in those tags.
                    stripped_diff_ = php_strlen(strip_tags(diff_)) * 2 - stripped_matches_
                    diff_ratio_ = stripped_matches_ / stripped_diff_
                    if diff_ratio_ > self._diff_threshold:
                        continue
                        pass
                    # end if
                # end if
                #// Un-inline the diffs by removing <del> or <ins>.
                orig_diffs_[o_] = php_preg_replace("|<ins>.*?</ins>|", "", diff_)
                final_diffs_[f_] = php_preg_replace("|<del>.*?</del>|", "", diff_)
            # end if
        # end for
        for row_ in php_array_keys(orig_rows_):
            #// Both columns have blanks. Ignore them.
            if orig_rows_[row_] < 0 and final_rows_[row_] < 0:
                continue
            # end if
            #// If we have a word based diff, use it. Otherwise, use the normal line.
            if (php_isset(lambda : orig_diffs_[orig_rows_[row_]])):
                orig_line_ = orig_diffs_[orig_rows_[row_]]
            elif (php_isset(lambda : orig_[orig_rows_[row_]])):
                orig_line_ = htmlspecialchars(orig_[orig_rows_[row_]])
            else:
                orig_line_ = ""
            # end if
            if (php_isset(lambda : final_diffs_[final_rows_[row_]])):
                final_line_ = final_diffs_[final_rows_[row_]]
            elif (php_isset(lambda : final_[final_rows_[row_]])):
                final_line_ = htmlspecialchars(final_[final_rows_[row_]])
            else:
                final_line_ = ""
            # end if
            if orig_rows_[row_] < 0:
                #// Orig is blank. This is really an added row.
                r_ += self._added(Array(final_line_), False)
            elif final_rows_[row_] < 0:
                #// Final is blank. This is really a deleted row.
                r_ += self._deleted(Array(orig_line_), False)
            else:
                #// A true changed row.
                if self._show_split_view:
                    r_ += "<tr>" + self.deletedline(orig_line_) + self.emptyline() + self.addedline(final_line_) + "</tr>\n"
                else:
                    r_ += "<tr>" + self.deletedline(orig_line_) + "</tr><tr>" + self.addedline(final_line_) + "</tr>\n"
                # end if
            # end if
        # end for
        return r_
    # end def _changed
    #// 
    #// Takes changed blocks and matches which rows in orig turned into which rows in final.
    #// 
    #// @since 2.6.0
    #// 
    #// @param array $orig  Lines of the original version of the text.
    #// @param array $final Lines of the final version of the text.
    #// @return array {
    #// Array containing results of comparing the original text to the final text.
    #// 
    #// @type array $orig_matches  Associative array of original matches. Index == row
    #// number of `$orig`, value == corresponding row number
    #// of that same line in `$final` or 'x' if there is no
    #// corresponding row (indicating it is a deleted line).
    #// @type array $final_matches Associative array of final matches. Index == row
    #// number of `$final`, value == corresponding row number
    #// of that same line in `$orig` or 'x' if there is no
    #// corresponding row (indicating it is a new line).
    #// @type array $orig_rows     Associative array of interleaved rows of `$orig` with
    #// blanks to keep matches aligned with side-by-side diff
    #// of `$final`. A value >= 0 corresponds to index of `$orig`.
    #// Value < 0 indicates a blank row.
    #// @type array $final_rows    Associative array of interleaved rows of `$final` with
    #// blanks to keep matches aligned with side-by-side diff
    #// of `$orig`. A value >= 0 corresponds to index of `$final`.
    #// Value < 0 indicates a blank row.
    #// }
    #//
    def interleave_changed_lines(self, orig_=None, final_=None):
        
        
        #// Contains all pairwise string comparisons. Keys are such that this need only be a one dimensional array.
        matches_ = Array()
        for o_ in php_array_keys(orig_):
            for f_ in php_array_keys(final_):
                matches_[str(o_) + str(",") + str(f_)] = self.compute_string_distance(orig_[o_], final_[f_])
            # end for
        # end for
        asort(matches_)
        #// Order by string distance.
        orig_matches_ = Array()
        final_matches_ = Array()
        for keys_,difference_ in matches_.items():
            o_, f_ = php_explode(",", keys_)
            o_ = php_int(o_)
            f_ = php_int(f_)
            #// Already have better matches for these guys.
            if (php_isset(lambda : orig_matches_[o_])) and (php_isset(lambda : final_matches_[f_])):
                continue
            # end if
            #// First match for these guys. Must be best match.
            if (not (php_isset(lambda : orig_matches_[o_]))) and (not (php_isset(lambda : final_matches_[f_]))):
                orig_matches_[o_] = f_
                final_matches_[f_] = o_
                continue
            # end if
            #// Best match of this final is already taken? Must mean this final is a new row.
            if (php_isset(lambda : orig_matches_[o_])):
                final_matches_[f_] = "x"
            elif (php_isset(lambda : final_matches_[f_])):
                #// Best match of this orig is already taken? Must mean this orig is a deleted row.
                orig_matches_[o_] = "x"
            # end if
        # end for
        #// We read the text in this order.
        php_ksort(orig_matches_)
        php_ksort(final_matches_)
        #// Stores rows and blanks for each column.
        orig_rows_ = php_array_keys(orig_matches_)
        orig_rows_copy_ = orig_rows_
        final_rows_ = php_array_keys(final_matches_)
        #// Interleaves rows with blanks to keep matches aligned.
        #// We may end up with some extraneous blank rows, but we'll just ignore them later.
        for orig_row_ in orig_rows_copy_:
            final_pos_ = php_array_search(orig_matches_[orig_row_], final_rows_, True)
            orig_pos_ = php_int(php_array_search(orig_row_, orig_rows_, True))
            if False == final_pos_:
                #// This orig is paired with a blank final.
                array_splice(final_rows_, orig_pos_, 0, -1)
            elif final_pos_ < orig_pos_:
                #// This orig's match is up a ways. Pad final with blank rows.
                diff_array_ = range(-1, final_pos_ - orig_pos_)
                array_splice(final_rows_, orig_pos_, 0, diff_array_)
            elif final_pos_ > orig_pos_:
                #// This orig's match is down a ways. Pad orig with blank rows.
                diff_array_ = range(-1, orig_pos_ - final_pos_)
                array_splice(orig_rows_, orig_pos_, 0, diff_array_)
            # end if
        # end for
        #// Pad the ends with blank rows if the columns aren't the same length.
        diff_count_ = php_count(orig_rows_) - php_count(final_rows_)
        if diff_count_ < 0:
            while True:
                
                if not (diff_count_ < 0):
                    break
                # end if
                php_array_push(orig_rows_, diff_count_)
                diff_count_ += 1
            # end while
        elif diff_count_ > 0:
            diff_count_ = -1 * diff_count_
            while True:
                
                if not (diff_count_ < 0):
                    break
                # end if
                php_array_push(final_rows_, diff_count_)
                diff_count_ += 1
            # end while
        # end if
        return Array(orig_matches_, final_matches_, orig_rows_, final_rows_)
    # end def interleave_changed_lines
    #// 
    #// Computes a number that is intended to reflect the "distance" between two strings.
    #// 
    #// @since 2.6.0
    #// 
    #// @param string $string1
    #// @param string $string2
    #// @return int
    #//
    def compute_string_distance(self, string1_=None, string2_=None):
        
        
        #// Use an md5 hash of the strings for a count cache, as it's fast to generate, and collisions aren't a concern.
        count_key1_ = php_md5(string1_)
        count_key2_ = php_md5(string2_)
        #// Cache vectors containing character frequency for all chars in each string.
        if (not (php_isset(lambda : self.count_cache[count_key1_]))):
            self.count_cache[count_key1_] = count_chars(string1_)
        # end if
        if (not (php_isset(lambda : self.count_cache[count_key2_]))):
            self.count_cache[count_key2_] = count_chars(string2_)
        # end if
        chars1_ = self.count_cache[count_key1_]
        chars2_ = self.count_cache[count_key2_]
        difference_key_ = php_md5(php_implode(",", chars1_) + ":" + php_implode(",", chars2_))
        if (not (php_isset(lambda : self.difference_cache[difference_key_]))):
            #// L1-norm of difference vector.
            self.difference_cache[difference_key_] = array_sum(php_array_map(Array(self, "difference"), chars1_, chars2_))
        # end if
        difference_ = self.difference_cache[difference_key_]
        #// $string1 has zero length? Odd. Give huge penalty by not dividing.
        if (not string1_):
            return difference_
        # end if
        #// Return distance per character (of string1).
        return difference_ / php_strlen(string1_)
    # end def compute_string_distance
    #// 
    #// @ignore
    #// @since 2.6.0
    #// 
    #// @param int $a
    #// @param int $b
    #// @return int
    #//
    def difference(self, a_=None, b_=None):
        
        
        return abs(a_ - b_)
    # end def difference
    #// 
    #// Make private properties readable for backward compatibility.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $name Property to get.
    #// @return mixed Property.
    #//
    def __get(self, name_=None):
        
        
        if php_in_array(name_, self.compat_fields):
            return self.name_
        # end if
    # end def __get
    #// 
    #// Make private properties settable for backward compatibility.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $name  Property to check if set.
    #// @param mixed  $value Property value.
    #// @return mixed Newly-set property.
    #//
    def __set(self, name_=None, value_=None):
        
        
        if php_in_array(name_, self.compat_fields):
            self.name_ = value_
            return self.name_
        # end if
    # end def __set
    #// 
    #// Make private properties checkable for backward compatibility.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $name Property to check if set.
    #// @return bool Whether the property is set.
    #//
    def __isset(self, name_=None):
        
        
        if php_in_array(name_, self.compat_fields):
            return (php_isset(lambda : self.name_))
        # end if
    # end def __isset
    #// 
    #// Make private properties un-settable for backward compatibility.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $name Property to unset.
    #//
    def __unset(self, name_=None):
        
        
        if php_in_array(name_, self.compat_fields):
            self.name_ = None
        # end if
    # end def __unset
# end class WP_Text_Diff_Renderer_Table
