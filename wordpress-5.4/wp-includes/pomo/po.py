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
#// Class for working with PO files
#// 
#// @version $Id: po.php 1158 2015-11-20 04:31:23Z dd32 $
#// @package pomo
#// @subpackage po
#//
php_include_file(__DIR__ + "/translations.php", once=True)
if (not php_defined("PO_MAX_LINE_LEN")):
    php_define("PO_MAX_LINE_LEN", 79)
# end if
php_ini_set("auto_detect_line_endings", 1)
#// 
#// Routines for working with PO files
#//
if (not php_class_exists("PO", False)):
    class PO(Gettext_Translations):
        comments_before_headers = ""
        #// 
        #// Exports headers to a PO entry
        #// 
        #// @return string msgid/msgstr PO entry for this PO file headers, doesn't contain newline at the end
        #//
        def export_headers(self):
            
            
            header_string_ = ""
            for header_,value_ in self.headers:
                header_string_ += str(header_) + str(": ") + str(value_) + str("\n")
            # end for
            poified_ = PO.poify(header_string_)
            if self.comments_before_headers:
                before_headers_ = self.prepend_each_line(php_rtrim(self.comments_before_headers) + "\n", "# ")
            else:
                before_headers_ = ""
            # end if
            return php_rtrim(str(before_headers_) + str("msgid \"\"\nmsgstr ") + str(poified_))
        # end def export_headers
        #// 
        #// Exports all entries to PO format
        #// 
        #// @return string sequence of mgsgid/msgstr PO strings, doesn't containt newline at the end
        #//
        def export_entries(self):
            
            
            #// TODO: Sorting.
            return php_implode("\n\n", php_array_map(Array("PO", "export_entry"), self.entries))
        # end def export_entries
        #// 
        #// Exports the whole PO file as a string
        #// 
        #// @param bool $include_headers whether to include the headers in the export
        #// @return string ready for inclusion in PO file string for headers and all the enrtries
        #//
        def export(self, include_headers_=None):
            if include_headers_ is None:
                include_headers_ = True
            # end if
            
            res_ = ""
            if include_headers_:
                res_ += self.export_headers()
                res_ += "\n\n"
            # end if
            res_ += self.export_entries()
            return res_
        # end def export
        #// 
        #// Same as {@link export}, but writes the result to a file
        #// 
        #// @param string $filename where to write the PO string
        #// @param bool $include_headers whether to include tje headers in the export
        #// @return bool true on success, false on error
        #//
        def export_to_file(self, filename_=None, include_headers_=None):
            if include_headers_ is None:
                include_headers_ = True
            # end if
            
            fh_ = fopen(filename_, "w")
            if False == fh_:
                return False
            # end if
            export_ = self.export(include_headers_)
            res_ = fwrite(fh_, export_)
            if False == res_:
                return False
            # end if
            return php_fclose(fh_)
        # end def export_to_file
        #// 
        #// Text to include as a comment before the start of the PO contents
        #// 
        #// Doesn't need to include # in the beginning of lines, these are added automatically
        #//
        def set_comment_before_headers(self, text_=None):
            
            
            self.comments_before_headers = text_
        # end def set_comment_before_headers
        #// 
        #// Formats a string in PO-style
        #// 
        #// @param string $string the string to format
        #// @return string the poified string
        #//
        @classmethod
        def poify(self, string_=None):
            
            
            quote_ = "\""
            slash_ = "\\"
            newline_ = "\n"
            replaces_ = Array({str(slash_): str(slash_) + str(slash_), str(quote_): str(slash_) + str(quote_), "    ": "\\t"})
            string_ = php_str_replace(php_array_keys(replaces_), php_array_values(replaces_), string_)
            po_ = quote_ + php_implode(str(slash_) + str("n") + str(quote_) + str(newline_) + str(quote_), php_explode(newline_, string_)) + quote_
            #// Add empty string on first line for readbility.
            if False != php_strpos(string_, newline_) and php_substr_count(string_, newline_) > 1 or php_substr(string_, -php_strlen(newline_)) != newline_:
                po_ = str(quote_) + str(quote_) + str(newline_) + str(po_)
            # end if
            #// Remove empty strings.
            po_ = php_str_replace(str(newline_) + str(quote_) + str(quote_), "", po_)
            return po_
        # end def poify
        #// 
        #// Gives back the original string from a PO-formatted string
        #// 
        #// @param string $string PO-formatted string
        #// @return string enascaped string
        #//
        @classmethod
        def unpoify(self, string_=None):
            
            
            escapes_ = Array({"t": "    ", "n": "\n", "r": "\r", "\\": "\\"})
            lines_ = php_array_map("trim", php_explode("\n", string_))
            lines_ = php_array_map(Array("PO", "trim_quotes"), lines_)
            unpoified_ = ""
            previous_is_backslash_ = False
            for line_ in lines_:
                preg_match_all("/./u", line_, chars_)
                chars_ = chars_[0]
                for char_ in chars_:
                    if (not previous_is_backslash_):
                        if "\\" == char_:
                            previous_is_backslash_ = True
                        else:
                            unpoified_ += char_
                        # end if
                    else:
                        previous_is_backslash_ = False
                        unpoified_ += escapes_[char_] if (php_isset(lambda : escapes_[char_])) else char_
                    # end if
                # end for
            # end for
            #// Standardise the line endings on imported content, technically PO files shouldn't contain \r.
            unpoified_ = php_str_replace(Array("\r\n", "\r"), "\n", unpoified_)
            return unpoified_
        # end def unpoify
        #// 
        #// Inserts $with in the beginning of every new line of $string and
        #// returns the modified string
        #// 
        #// @param string $string prepend lines in this string
        #// @param string $with prepend lines with this string
        #//
        @classmethod
        def prepend_each_line(self, string_=None, with_=None):
            
            
            lines_ = php_explode("\n", string_)
            append_ = ""
            if "\n" == php_substr(string_, -1) and "" == php_end(lines_):
                #// 
                #// Last line might be empty because $string was terminated
                #// with a newline, remove it from the $lines array,
                #// we'll restore state by re-terminating the string at the end.
                #//
                php_array_pop(lines_)
                append_ = "\n"
            # end if
            for line_ in lines_:
                line_ = with_ + line_
            # end for
            line_ = None
            return php_implode("\n", lines_) + append_
        # end def prepend_each_line
        #// 
        #// Prepare a text as a comment -- wraps the lines and prepends #
        #// and a special character to each line
        #// 
        #// @access private
        #// @param string $text the comment text
        #// @param string $char character to denote a special PO comment,
        #// like :, default is a space
        #//
        @classmethod
        def comment_block(self, text_=None, char_=" "):
            
            
            text_ = wordwrap(text_, PO_MAX_LINE_LEN - 3)
            return PO.prepend_each_line(text_, str("#") + str(char_) + str(" "))
        # end def comment_block
        #// 
        #// Builds a string from the entry for inclusion in PO file
        #// 
        #// @param Translation_Entry $entry the entry to convert to po string (passed by reference).
        #// @return string|false PO-style formatted string for the entry or
        #// false if the entry is empty
        #//
        @classmethod
        def export_entry(self, entry_=None):
            
            
            if None == entry_.singular or "" == entry_.singular:
                return False
            # end if
            po_ = Array()
            if (not php_empty(lambda : entry_.translator_comments)):
                po_[-1] = PO.comment_block(entry_.translator_comments)
            # end if
            if (not php_empty(lambda : entry_.extracted_comments)):
                po_[-1] = PO.comment_block(entry_.extracted_comments, ".")
            # end if
            if (not php_empty(lambda : entry_.references)):
                po_[-1] = PO.comment_block(php_implode(" ", entry_.references), ":")
            # end if
            if (not php_empty(lambda : entry_.flags)):
                po_[-1] = PO.comment_block(php_implode(", ", entry_.flags), ",")
            # end if
            if entry_.context:
                po_[-1] = "msgctxt " + PO.poify(entry_.context)
            # end if
            po_[-1] = "msgid " + PO.poify(entry_.singular)
            if (not entry_.is_plural):
                translation_ = "" if php_empty(lambda : entry_.translations) else entry_.translations[0]
                translation_ = PO.match_begin_and_end_newlines(translation_, entry_.singular)
                po_[-1] = "msgstr " + PO.poify(translation_)
            else:
                po_[-1] = "msgid_plural " + PO.poify(entry_.plural)
                translations_ = Array("", "") if php_empty(lambda : entry_.translations) else entry_.translations
                for i_,translation_ in translations_:
                    translation_ = PO.match_begin_and_end_newlines(translation_, entry_.plural)
                    po_[-1] = str("msgstr[") + str(i_) + str("] ") + PO.poify(translation_)
                # end for
            # end if
            return php_implode("\n", po_)
        # end def export_entry
        @classmethod
        def match_begin_and_end_newlines(self, translation_=None, original_=None):
            
            
            if "" == translation_:
                return translation_
            # end if
            original_begin_ = "\n" == php_substr(original_, 0, 1)
            original_end_ = "\n" == php_substr(original_, -1)
            translation_begin_ = "\n" == php_substr(translation_, 0, 1)
            translation_end_ = "\n" == php_substr(translation_, -1)
            if original_begin_:
                if (not translation_begin_):
                    translation_ = "\n" + translation_
                # end if
            elif translation_begin_:
                translation_ = php_ltrim(translation_, "\n")
            # end if
            if original_end_:
                if (not translation_end_):
                    translation_ += "\n"
                # end if
            elif translation_end_:
                translation_ = php_rtrim(translation_, "\n")
            # end if
            return translation_
        # end def match_begin_and_end_newlines
        #// 
        #// @param string $filename
        #// @return boolean
        #//
        def import_from_file(self, filename_=None):
            
            
            f_ = fopen(filename_, "r")
            if (not f_):
                return False
            # end if
            lineno_ = 0
            while True:
                
                if not (True):
                    break
                # end if
                res_ = self.read_entry(f_, lineno_)
                if (not res_):
                    break
                # end if
                if "" == res_["entry"].singular:
                    self.set_headers(self.make_headers(res_["entry"].translations[0]))
                else:
                    self.add_entry(res_["entry"])
                # end if
            # end while
            PO.read_line(f_, "clear")
            if False == res_:
                return False
            # end if
            if (not self.headers) and (not self.entries):
                return False
            # end if
            return True
        # end def import_from_file
        #// 
        #// Helper function for read_entry
        #// 
        #// @param string $context
        #// @return bool
        #//
        def is_final(self, context_=None):
            
            
            return "msgstr" == context_ or "msgstr_plural" == context_
        # end def is_final
        #// 
        #// @param resource $f
        #// @param int      $lineno
        #// @return null|false|array
        #//
        def read_entry(self, f_=None, lineno_=0):
            
            
            entry_ = php_new_class("Translation_Entry", lambda : Translation_Entry())
            #// Where were we in the last step.
            #// Can be: comment, msgctxt, msgid, msgid_plural, msgstr, msgstr_plural.
            context_ = ""
            msgstr_index_ = 0
            while True:
                
                if not (True):
                    break
                # end if
                lineno_ += 1
                line_ = PO.read_line(f_)
                if (not line_):
                    if php_feof(f_):
                        if self.is_final(context_):
                            break
                        elif (not context_):
                            #// We haven't read a line and EOF came.
                            return None
                        else:
                            return False
                        # end if
                    else:
                        return False
                    # end if
                # end if
                if "\n" == line_:
                    continue
                # end if
                line_ = php_trim(line_)
                if php_preg_match("/^#/", line_, m_):
                    #// The comment is the start of a new entry.
                    if self.is_final(context_):
                        PO.read_line(f_, "put-back")
                        lineno_ -= 1
                        break
                    # end if
                    #// Comments have to be at the beginning.
                    if context_ and "comment" != context_:
                        return False
                    # end if
                    #// Add comment.
                    self.add_comment_to_entry(entry_, line_)
                elif php_preg_match("/^msgctxt\\s+(\".*\")/", line_, m_):
                    if self.is_final(context_):
                        PO.read_line(f_, "put-back")
                        lineno_ -= 1
                        break
                    # end if
                    if context_ and "comment" != context_:
                        return False
                    # end if
                    context_ = "msgctxt"
                    entry_.context += PO.unpoify(m_[1])
                elif php_preg_match("/^msgid\\s+(\".*\")/", line_, m_):
                    if self.is_final(context_):
                        PO.read_line(f_, "put-back")
                        lineno_ -= 1
                        break
                    # end if
                    if context_ and "msgctxt" != context_ and "comment" != context_:
                        return False
                    # end if
                    context_ = "msgid"
                    entry_.singular += PO.unpoify(m_[1])
                elif php_preg_match("/^msgid_plural\\s+(\".*\")/", line_, m_):
                    if "msgid" != context_:
                        return False
                    # end if
                    context_ = "msgid_plural"
                    entry_.is_plural = True
                    entry_.plural += PO.unpoify(m_[1])
                elif php_preg_match("/^msgstr\\s+(\".*\")/", line_, m_):
                    if "msgid" != context_:
                        return False
                    # end if
                    context_ = "msgstr"
                    entry_.translations = Array(PO.unpoify(m_[1]))
                elif php_preg_match("/^msgstr\\[(\\d+)\\]\\s+(\".*\")/", line_, m_):
                    if "msgid_plural" != context_ and "msgstr_plural" != context_:
                        return False
                    # end if
                    context_ = "msgstr_plural"
                    msgstr_index_ = m_[1]
                    entry_.translations[m_[1]] = PO.unpoify(m_[2])
                elif php_preg_match("/^\".*\"$/", line_):
                    unpoified_ = PO.unpoify(line_)
                    for case in Switch(context_):
                        if case("msgid"):
                            entry_.singular += unpoified_
                            break
                        # end if
                        if case("msgctxt"):
                            entry_.context += unpoified_
                            break
                        # end if
                        if case("msgid_plural"):
                            entry_.plural += unpoified_
                            break
                        # end if
                        if case("msgstr"):
                            entry_.translations[0] += unpoified_
                            break
                        # end if
                        if case("msgstr_plural"):
                            entry_.translations[msgstr_index_] += unpoified_
                            break
                        # end if
                        if case():
                            return False
                        # end if
                    # end for
                else:
                    return False
                # end if
            # end while
            have_translations_ = False
            for t_ in entry_.translations:
                if t_ or "0" == t_:
                    have_translations_ = True
                    break
                # end if
            # end for
            if False == have_translations_:
                entry_.translations = Array()
            # end if
            return Array({"entry": entry_, "lineno": lineno_})
        # end def read_entry
        #// 
        #// @staticvar string   $last_line
        #// @staticvar boolean  $use_last_line
        #// 
        #// @param     resource $f
        #// @param     string   $action
        #// @return boolean
        #//
        def read_line(self, f_=None, action_="read"):
            
            
            last_line_ = ""
            use_last_line_ = False
            if "clear" == action_:
                last_line_ = ""
                return True
            # end if
            if "put-back" == action_:
                use_last_line_ = True
                return True
            # end if
            line_ = last_line_ if use_last_line_ else php_fgets(f_)
            line_ = php_rtrim(line_, "\r\n") + "\n" if "\r\n" == php_substr(line_, -2) else line_
            last_line_ = line_
            use_last_line_ = False
            return line_
        # end def read_line
        #// 
        #// @param Translation_Entry $entry
        #// @param string            $po_comment_line
        #//
        def add_comment_to_entry(self, entry_=None, po_comment_line_=None):
            
            
            first_two_ = php_substr(po_comment_line_, 0, 2)
            comment_ = php_trim(php_substr(po_comment_line_, 2))
            if "#:" == first_two_:
                entry_.references = php_array_merge(entry_.references, php_preg_split("/\\s+/", comment_))
            elif "#." == first_two_:
                entry_.extracted_comments = php_trim(entry_.extracted_comments + "\n" + comment_)
            elif "#," == first_two_:
                entry_.flags = php_array_merge(entry_.flags, php_preg_split("/,\\s*/", comment_))
            else:
                entry_.translator_comments = php_trim(entry_.translator_comments + "\n" + comment_)
            # end if
        # end def add_comment_to_entry
        #// 
        #// @param string $s
        #// @return string
        #//
        @classmethod
        def trim_quotes(self, s_=None):
            
            
            if php_substr(s_, 0, 1) == "\"":
                s_ = php_substr(s_, 1)
            # end if
            if php_substr(s_, -1, 1) == "\"":
                s_ = php_substr(s_, 0, -1)
            # end if
            return s_
        # end def trim_quotes
    # end class PO
# end if
