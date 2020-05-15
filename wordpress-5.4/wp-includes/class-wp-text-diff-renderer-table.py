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
    _leading_context_lines = 10000
    _trailing_context_lines = 10000
    _diff_threshold = 0.6
    inline_diff_renderer = "WP_Text_Diff_Renderer_inline"
    _show_split_view = True
    compat_fields = Array("_show_split_view", "inline_diff_renderer", "_diff_threshold")
    count_cache = Array()
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
    def __init__(self, params=Array()):
        
        super().__init__(params)
        if (php_isset(lambda : params["show_split_view"])):
            self._show_split_view = params["show_split_view"]
        # end if
    # end def __init__
    #// 
    #// @ignore
    #// 
    #// @param string $header
    #// @return string
    #//
    def _startblock(self, header=None):
        
        return ""
    # end def _startblock
    #// 
    #// @ignore
    #// 
    #// @param array $lines
    #// @param string $prefix
    #//
    def _lines(self, lines=None, prefix=" "):
        
        pass
    # end def _lines
    #// 
    #// @ignore
    #// 
    #// @param string $line HTML-escape the value.
    #// @return string
    #//
    def addedline(self, line=None):
        
        return "<td class='diff-addedline'><span aria-hidden='true' class='dashicons dashicons-plus'></span><span class='screen-reader-text'>" + __("Added:") + str(" </span>") + str(line) + str("</td>")
    # end def addedline
    #// 
    #// @ignore
    #// 
    #// @param string $line HTML-escape the value.
    #// @return string
    #//
    def deletedline(self, line=None):
        
        return "<td class='diff-deletedline'><span aria-hidden='true' class='dashicons dashicons-minus'></span><span class='screen-reader-text'>" + __("Deleted:") + str(" </span>") + str(line) + str("</td>")
    # end def deletedline
    #// 
    #// @ignore
    #// 
    #// @param string $line HTML-escape the value.
    #// @return string
    #//
    def contextline(self, line=None):
        
        return "<td class='diff-context'><span class='screen-reader-text'>" + __("Unchanged:") + str(" </span>") + str(line) + str("</td>")
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
    def _added(self, lines=None, encode=True):
        
        r = ""
        for line in lines:
            if encode:
                processed_line = htmlspecialchars(line)
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
                line = apply_filters("process_text_diff_html", processed_line, line, "added")
            # end if
            if self._show_split_view:
                r += "<tr>" + self.emptyline() + self.emptyline() + self.addedline(line) + "</tr>\n"
            else:
                r += "<tr>" + self.addedline(line) + "</tr>\n"
            # end if
        # end for
        return r
    # end def _added
    #// 
    #// @ignore
    #// 
    #// @param array $lines
    #// @param bool $encode
    #// @return string
    #//
    def _deleted(self, lines=None, encode=True):
        
        r = ""
        for line in lines:
            if encode:
                processed_line = htmlspecialchars(line)
                #// This filter is documented in wp-includes/wp-diff.php
                line = apply_filters("process_text_diff_html", processed_line, line, "deleted")
            # end if
            if self._show_split_view:
                r += "<tr>" + self.deletedline(line) + self.emptyline() + self.emptyline() + "</tr>\n"
            else:
                r += "<tr>" + self.deletedline(line) + "</tr>\n"
            # end if
        # end for
        return r
    # end def _deleted
    #// 
    #// @ignore
    #// 
    #// @param array $lines
    #// @param bool $encode
    #// @return string
    #//
    def _context(self, lines=None, encode=True):
        
        r = ""
        for line in lines:
            if encode:
                processed_line = htmlspecialchars(line)
                #// This filter is documented in wp-includes/wp-diff.php
                line = apply_filters("process_text_diff_html", processed_line, line, "unchanged")
            # end if
            if self._show_split_view:
                r += "<tr>" + self.contextline(line) + self.emptyline() + self.contextline(line) + "</tr>\n"
            else:
                r += "<tr>" + self.contextline(line) + "</tr>\n"
            # end if
        # end for
        return r
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
    def _changed(self, orig=None, final=None):
        
        r = ""
        #// 
        #// Does the aforementioned additional processing:
        #// _matches tell what rows are "the same" in orig and final. Those pairs will be diffed to get word changes.
        #// - match is numeric: an index in other column.
        #// - match is 'X': no match. It is a new row.
        #// _rows are column vectors for the orig column and the final column.
        #// - row >= 0: an indix of the $orig or $final array.
        #// - row < 0: a blank row for that column.
        #//
        orig_matches, final_matches, orig_rows, final_rows = self.interleave_changed_lines(orig, final)
        #// These will hold the word changes as determined by an inline diff.
        orig_diffs = Array()
        final_diffs = Array()
        #// Compute word diffs for each matched pair using the inline diff.
        for o,f in orig_matches:
            if php_is_numeric(o) and php_is_numeric(f):
                text_diff = php_new_class("Text_Diff", lambda : Text_Diff("auto", Array(Array(orig[o]), Array(final[f]))))
                renderer = php_new_class(self.inline_diff_renderer, lambda : {**locals(), **globals()}[self.inline_diff_renderer]())
                diff = renderer.render(text_diff)
                #// If they're too different, don't include any <ins> or <del>'s.
                if preg_match_all("!(<ins>.*?</ins>|<del>.*?</del>)!", diff, diff_matches):
                    #// Length of all text between <ins> or <del>.
                    stripped_matches = php_strlen(strip_tags(join(" ", diff_matches[0])))
                    #// Since we count length of text between <ins> or <del> (instead of picking just one),
                    #// we double the length of chars not in those tags.
                    stripped_diff = php_strlen(strip_tags(diff)) * 2 - stripped_matches
                    diff_ratio = stripped_matches / stripped_diff
                    if diff_ratio > self._diff_threshold:
                        continue
                        pass
                    # end if
                # end if
                #// Un-inline the diffs by removing <del> or <ins>.
                orig_diffs[o] = php_preg_replace("|<ins>.*?</ins>|", "", diff)
                final_diffs[f] = php_preg_replace("|<del>.*?</del>|", "", diff)
            # end if
        # end for
        for row in php_array_keys(orig_rows):
            #// Both columns have blanks. Ignore them.
            if orig_rows[row] < 0 and final_rows[row] < 0:
                continue
            # end if
            #// If we have a word based diff, use it. Otherwise, use the normal line.
            if (php_isset(lambda : orig_diffs[orig_rows[row]])):
                orig_line = orig_diffs[orig_rows[row]]
            elif (php_isset(lambda : orig[orig_rows[row]])):
                orig_line = htmlspecialchars(orig[orig_rows[row]])
            else:
                orig_line = ""
            # end if
            if (php_isset(lambda : final_diffs[final_rows[row]])):
                final_line = final_diffs[final_rows[row]]
            elif (php_isset(lambda : final[final_rows[row]])):
                final_line = htmlspecialchars(final[final_rows[row]])
            else:
                final_line = ""
            # end if
            if orig_rows[row] < 0:
                #// Orig is blank. This is really an added row.
                r += self._added(Array(final_line), False)
            elif final_rows[row] < 0:
                #// Final is blank. This is really a deleted row.
                r += self._deleted(Array(orig_line), False)
            else:
                #// A true changed row.
                if self._show_split_view:
                    r += "<tr>" + self.deletedline(orig_line) + self.emptyline() + self.addedline(final_line) + "</tr>\n"
                else:
                    r += "<tr>" + self.deletedline(orig_line) + "</tr><tr>" + self.addedline(final_line) + "</tr>\n"
                # end if
            # end if
        # end for
        return r
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
    def interleave_changed_lines(self, orig=None, final=None):
        
        #// Contains all pairwise string comparisons. Keys are such that this need only be a one dimensional array.
        matches = Array()
        for o in php_array_keys(orig):
            for f in php_array_keys(final):
                matches[str(o) + str(",") + str(f)] = self.compute_string_distance(orig[o], final[f])
            # end for
        # end for
        asort(matches)
        #// Order by string distance.
        orig_matches = Array()
        final_matches = Array()
        for keys,difference in matches:
            o, f = php_explode(",", keys)
            o = int(o)
            f = int(f)
            #// Already have better matches for these guys.
            if (php_isset(lambda : orig_matches[o])) and (php_isset(lambda : final_matches[f])):
                continue
            # end if
            #// First match for these guys. Must be best match.
            if (not (php_isset(lambda : orig_matches[o]))) and (not (php_isset(lambda : final_matches[f]))):
                orig_matches[o] = f
                final_matches[f] = o
                continue
            # end if
            #// Best match of this final is already taken? Must mean this final is a new row.
            if (php_isset(lambda : orig_matches[o])):
                final_matches[f] = "x"
            elif (php_isset(lambda : final_matches[f])):
                #// Best match of this orig is already taken? Must mean this orig is a deleted row.
                orig_matches[o] = "x"
            # end if
        # end for
        #// We read the text in this order.
        ksort(orig_matches)
        ksort(final_matches)
        #// Stores rows and blanks for each column.
        orig_rows = php_array_keys(orig_matches)
        orig_rows_copy = orig_rows
        final_rows = php_array_keys(final_matches)
        #// Interleaves rows with blanks to keep matches aligned.
        #// We may end up with some extraneous blank rows, but we'll just ignore them later.
        for orig_row in orig_rows_copy:
            final_pos = php_array_search(orig_matches[orig_row], final_rows, True)
            orig_pos = int(php_array_search(orig_row, orig_rows, True))
            if False == final_pos:
                #// This orig is paired with a blank final.
                array_splice(final_rows, orig_pos, 0, -1)
            elif final_pos < orig_pos:
                #// This orig's match is up a ways. Pad final with blank rows.
                diff_array = range(-1, final_pos - orig_pos)
                array_splice(final_rows, orig_pos, 0, diff_array)
            elif final_pos > orig_pos:
                #// This orig's match is down a ways. Pad orig with blank rows.
                diff_array = range(-1, orig_pos - final_pos)
                array_splice(orig_rows, orig_pos, 0, diff_array)
            # end if
        # end for
        #// Pad the ends with blank rows if the columns aren't the same length.
        diff_count = php_count(orig_rows) - php_count(final_rows)
        if diff_count < 0:
            while True:
                
                if not (diff_count < 0):
                    break
                # end if
                php_array_push(orig_rows, diff_count)
                diff_count += 1
            # end while
        elif diff_count > 0:
            diff_count = -1 * diff_count
            while True:
                
                if not (diff_count < 0):
                    break
                # end if
                php_array_push(final_rows, diff_count)
                diff_count += 1
            # end while
        # end if
        return Array(orig_matches, final_matches, orig_rows, final_rows)
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
    def compute_string_distance(self, string1=None, string2=None):
        
        #// Use an md5 hash of the strings for a count cache, as it's fast to generate, and collisions aren't a concern.
        count_key1 = php_md5(string1)
        count_key2 = php_md5(string2)
        #// Cache vectors containing character frequency for all chars in each string.
        if (not (php_isset(lambda : self.count_cache[count_key1]))):
            self.count_cache[count_key1] = count_chars(string1)
        # end if
        if (not (php_isset(lambda : self.count_cache[count_key2]))):
            self.count_cache[count_key2] = count_chars(string2)
        # end if
        chars1 = self.count_cache[count_key1]
        chars2 = self.count_cache[count_key2]
        difference_key = php_md5(php_implode(",", chars1) + ":" + php_implode(",", chars2))
        if (not (php_isset(lambda : self.difference_cache[difference_key]))):
            #// L1-norm of difference vector.
            self.difference_cache[difference_key] = array_sum(php_array_map(Array(self, "difference"), chars1, chars2))
        # end if
        difference = self.difference_cache[difference_key]
        #// $string1 has zero length? Odd. Give huge penalty by not dividing.
        if (not string1):
            return difference
        # end if
        #// Return distance per character (of string1).
        return difference / php_strlen(string1)
    # end def compute_string_distance
    #// 
    #// @ignore
    #// @since 2.6.0
    #// 
    #// @param int $a
    #// @param int $b
    #// @return int
    #//
    def difference(self, a=None, b=None):
        
        return abs(a - b)
    # end def difference
    #// 
    #// Make private properties readable for backward compatibility.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $name Property to get.
    #// @return mixed Property.
    #//
    def __get(self, name=None):
        
        if php_in_array(name, self.compat_fields):
            return self.name
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
    def __set(self, name=None, value=None):
        
        if php_in_array(name, self.compat_fields):
            self.name = value
            return self.name
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
    def __isset(self, name=None):
        
        if php_in_array(name, self.compat_fields):
            return (php_isset(lambda : self.name))
        # end if
    # end def __isset
    #// 
    #// Make private properties un-settable for backward compatibility.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string $name Property to unset.
    #//
    def __unset(self, name=None):
        
        if php_in_array(name, self.compat_fields):
            self.name = None
        # end if
    # end def __unset
# end class WP_Text_Diff_Renderer_Table
