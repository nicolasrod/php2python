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
            
            header_string = ""
            for header,value in self.headers:
                header_string += str(header) + str(": ") + str(value) + str("\n")
            # end for
            poified = PO.poify(header_string)
            if self.comments_before_headers:
                before_headers = self.prepend_each_line(php_rtrim(self.comments_before_headers) + "\n", "# ")
            else:
                before_headers = ""
            # end if
            return php_rtrim(str(before_headers) + str("msgid \"\"\nmsgstr ") + str(poified))
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
        def export(self, include_headers=True):
            
            res = ""
            if include_headers:
                res += self.export_headers()
                res += "\n\n"
            # end if
            res += self.export_entries()
            return res
        # end def export
        #// 
        #// Same as {@link export}, but writes the result to a file
        #// 
        #// @param string $filename where to write the PO string
        #// @param bool $include_headers whether to include tje headers in the export
        #// @return bool true on success, false on error
        #//
        def export_to_file(self, filename=None, include_headers=True):
            
            fh = fopen(filename, "w")
            if False == fh:
                return False
            # end if
            export = self.export(include_headers)
            res = fwrite(fh, export)
            if False == res:
                return False
            # end if
            return php_fclose(fh)
        # end def export_to_file
        #// 
        #// Text to include as a comment before the start of the PO contents
        #// 
        #// Doesn't need to include # in the beginning of lines, these are added automatically
        #//
        def set_comment_before_headers(self, text=None):
            
            self.comments_before_headers = text
        # end def set_comment_before_headers
        #// 
        #// Formats a string in PO-style
        #// 
        #// @param string $string the string to format
        #// @return string the poified string
        #//
        @classmethod
        def poify(self, string=None):
            
            quote = "\""
            slash = "\\"
            newline = "\n"
            replaces = Array({str(slash): str(slash) + str(slash), str(quote): str(slash) + str(quote), "   ": "\\t"})
            string = php_str_replace(php_array_keys(replaces), php_array_values(replaces), string)
            po = quote + php_implode(str(slash) + str("n") + str(quote) + str(newline) + str(quote), php_explode(newline, string)) + quote
            #// Add empty string on first line for readbility.
            if False != php_strpos(string, newline) and php_substr_count(string, newline) > 1 or php_substr(string, -php_strlen(newline)) != newline:
                po = str(quote) + str(quote) + str(newline) + str(po)
            # end if
            #// Remove empty strings.
            po = php_str_replace(str(newline) + str(quote) + str(quote), "", po)
            return po
        # end def poify
        #// 
        #// Gives back the original string from a PO-formatted string
        #// 
        #// @param string $string PO-formatted string
        #// @return string enascaped string
        #//
        @classmethod
        def unpoify(self, string=None):
            
            escapes = Array({"t": " ", "n": "\n", "r": "\r", "\\": "\\"})
            lines = php_array_map("trim", php_explode("\n", string))
            lines = php_array_map(Array("PO", "trim_quotes"), lines)
            unpoified = ""
            previous_is_backslash = False
            for line in lines:
                preg_match_all("/./u", line, chars)
                chars = chars[0]
                for char in chars:
                    if (not previous_is_backslash):
                        if "\\" == char:
                            previous_is_backslash = True
                        else:
                            unpoified += char
                        # end if
                    else:
                        previous_is_backslash = False
                        unpoified += escapes[char] if (php_isset(lambda : escapes[char])) else char
                    # end if
                # end for
            # end for
            #// Standardise the line endings on imported content, technically PO files shouldn't contain \r.
            unpoified = php_str_replace(Array("\r\n", "\r"), "\n", unpoified)
            return unpoified
        # end def unpoify
        #// 
        #// Inserts $with in the beginning of every new line of $string and
        #// returns the modified string
        #// 
        #// @param string $string prepend lines in this string
        #// @param string $with prepend lines with this string
        #//
        @classmethod
        def prepend_each_line(self, string=None, with_=None):
            
            lines = php_explode("\n", string)
            append = ""
            if "\n" == php_substr(string, -1) and "" == php_end(lines):
                #// 
                #// Last line might be empty because $string was terminated
                #// with a newline, remove it from the $lines array,
                #// we'll restore state by re-terminating the string at the end.
                #//
                php_array_pop(lines)
                append = "\n"
            # end if
            for line in lines:
                line = with_ + line
            # end for
            line = None
            return php_implode("\n", lines) + append
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
        def comment_block(self, text=None, char=" "):
            
            text = wordwrap(text, PO_MAX_LINE_LEN - 3)
            return PO.prepend_each_line(text, str("#") + str(char) + str(" "))
        # end def comment_block
        #// 
        #// Builds a string from the entry for inclusion in PO file
        #// 
        #// @param Translation_Entry $entry the entry to convert to po string (passed by reference).
        #// @return string|false PO-style formatted string for the entry or
        #// false if the entry is empty
        #//
        @classmethod
        def export_entry(self, entry=None):
            
            if None == entry.singular or "" == entry.singular:
                return False
            # end if
            po = Array()
            if (not php_empty(lambda : entry.translator_comments)):
                po[-1] = PO.comment_block(entry.translator_comments)
            # end if
            if (not php_empty(lambda : entry.extracted_comments)):
                po[-1] = PO.comment_block(entry.extracted_comments, ".")
            # end if
            if (not php_empty(lambda : entry.references)):
                po[-1] = PO.comment_block(php_implode(" ", entry.references), ":")
            # end if
            if (not php_empty(lambda : entry.flags)):
                po[-1] = PO.comment_block(php_implode(", ", entry.flags), ",")
            # end if
            if entry.context:
                po[-1] = "msgctxt " + PO.poify(entry.context)
            # end if
            po[-1] = "msgid " + PO.poify(entry.singular)
            if (not entry.is_plural):
                translation = "" if php_empty(lambda : entry.translations) else entry.translations[0]
                translation = PO.match_begin_and_end_newlines(translation, entry.singular)
                po[-1] = "msgstr " + PO.poify(translation)
            else:
                po[-1] = "msgid_plural " + PO.poify(entry.plural)
                translations = Array("", "") if php_empty(lambda : entry.translations) else entry.translations
                for i,translation in translations:
                    translation = PO.match_begin_and_end_newlines(translation, entry.plural)
                    po[-1] = str("msgstr[") + str(i) + str("] ") + PO.poify(translation)
                # end for
            # end if
            return php_implode("\n", po)
        # end def export_entry
        @classmethod
        def match_begin_and_end_newlines(self, translation=None, original=None):
            
            if "" == translation:
                return translation
            # end if
            original_begin = "\n" == php_substr(original, 0, 1)
            original_end = "\n" == php_substr(original, -1)
            translation_begin = "\n" == php_substr(translation, 0, 1)
            translation_end = "\n" == php_substr(translation, -1)
            if original_begin:
                if (not translation_begin):
                    translation = "\n" + translation
                # end if
            elif translation_begin:
                translation = php_ltrim(translation, "\n")
            # end if
            if original_end:
                if (not translation_end):
                    translation += "\n"
                # end if
            elif translation_end:
                translation = php_rtrim(translation, "\n")
            # end if
            return translation
        # end def match_begin_and_end_newlines
        #// 
        #// @param string $filename
        #// @return boolean
        #//
        def import_from_file(self, filename=None):
            
            f = fopen(filename, "r")
            if (not f):
                return False
            # end if
            lineno = 0
            while True:
                
                if not (True):
                    break
                # end if
                res = self.read_entry(f, lineno)
                if (not res):
                    break
                # end if
                if "" == res["entry"].singular:
                    self.set_headers(self.make_headers(res["entry"].translations[0]))
                else:
                    self.add_entry(res["entry"])
                # end if
            # end while
            PO.read_line(f, "clear")
            if False == res:
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
        def is_final(self, context=None):
            
            return "msgstr" == context or "msgstr_plural" == context
        # end def is_final
        #// 
        #// @param resource $f
        #// @param int      $lineno
        #// @return null|false|array
        #//
        def read_entry(self, f=None, lineno=0):
            
            entry = php_new_class("Translation_Entry", lambda : Translation_Entry())
            #// Where were we in the last step.
            #// Can be: comment, msgctxt, msgid, msgid_plural, msgstr, msgstr_plural.
            context = ""
            msgstr_index = 0
            while True:
                
                if not (True):
                    break
                # end if
                lineno += 1
                line = PO.read_line(f)
                if (not line):
                    if php_feof(f):
                        if self.is_final(context):
                            break
                        elif (not context):
                            #// We haven't read a line and EOF came.
                            return None
                        else:
                            return False
                        # end if
                    else:
                        return False
                    # end if
                # end if
                if "\n" == line:
                    continue
                # end if
                line = php_trim(line)
                if php_preg_match("/^#/", line, m):
                    #// The comment is the start of a new entry.
                    if self.is_final(context):
                        PO.read_line(f, "put-back")
                        lineno -= 1
                        break
                    # end if
                    #// Comments have to be at the beginning.
                    if context and "comment" != context:
                        return False
                    # end if
                    #// Add comment.
                    self.add_comment_to_entry(entry, line)
                elif php_preg_match("/^msgctxt\\s+(\".*\")/", line, m):
                    if self.is_final(context):
                        PO.read_line(f, "put-back")
                        lineno -= 1
                        break
                    # end if
                    if context and "comment" != context:
                        return False
                    # end if
                    context = "msgctxt"
                    entry.context += PO.unpoify(m[1])
                elif php_preg_match("/^msgid\\s+(\".*\")/", line, m):
                    if self.is_final(context):
                        PO.read_line(f, "put-back")
                        lineno -= 1
                        break
                    # end if
                    if context and "msgctxt" != context and "comment" != context:
                        return False
                    # end if
                    context = "msgid"
                    entry.singular += PO.unpoify(m[1])
                elif php_preg_match("/^msgid_plural\\s+(\".*\")/", line, m):
                    if "msgid" != context:
                        return False
                    # end if
                    context = "msgid_plural"
                    entry.is_plural = True
                    entry.plural += PO.unpoify(m[1])
                elif php_preg_match("/^msgstr\\s+(\".*\")/", line, m):
                    if "msgid" != context:
                        return False
                    # end if
                    context = "msgstr"
                    entry.translations = Array(PO.unpoify(m[1]))
                elif php_preg_match("/^msgstr\\[(\\d+)\\]\\s+(\".*\")/", line, m):
                    if "msgid_plural" != context and "msgstr_plural" != context:
                        return False
                    # end if
                    context = "msgstr_plural"
                    msgstr_index = m[1]
                    entry.translations[m[1]] = PO.unpoify(m[2])
                elif php_preg_match("/^\".*\"$/", line):
                    unpoified = PO.unpoify(line)
                    for case in Switch(context):
                        if case("msgid"):
                            entry.singular += unpoified
                            break
                        # end if
                        if case("msgctxt"):
                            entry.context += unpoified
                            break
                        # end if
                        if case("msgid_plural"):
                            entry.plural += unpoified
                            break
                        # end if
                        if case("msgstr"):
                            entry.translations[0] += unpoified
                            break
                        # end if
                        if case("msgstr_plural"):
                            entry.translations[msgstr_index] += unpoified
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
            have_translations = False
            for t in entry.translations:
                if t or "0" == t:
                    have_translations = True
                    break
                # end if
            # end for
            if False == have_translations:
                entry.translations = Array()
            # end if
            return Array({"entry": entry, "lineno": lineno})
        # end def read_entry
        #// 
        #// @staticvar string   $last_line
        #// @staticvar boolean  $use_last_line
        #// 
        #// @param     resource $f
        #// @param     string   $action
        #// @return boolean
        #//
        def read_line(self, f=None, action="read"):
            
            last_line = ""
            use_last_line = False
            if "clear" == action:
                last_line = ""
                return True
            # end if
            if "put-back" == action:
                use_last_line = True
                return True
            # end if
            line = last_line if use_last_line else php_fgets(f)
            line = php_rtrim(line, "\r\n") + "\n" if "\r\n" == php_substr(line, -2) else line
            last_line = line
            use_last_line = False
            return line
        # end def read_line
        #// 
        #// @param Translation_Entry $entry
        #// @param string            $po_comment_line
        #//
        def add_comment_to_entry(self, entry=None, po_comment_line=None):
            
            first_two = php_substr(po_comment_line, 0, 2)
            comment = php_trim(php_substr(po_comment_line, 2))
            if "#:" == first_two:
                entry.references = php_array_merge(entry.references, php_preg_split("/\\s+/", comment))
            elif "#." == first_two:
                entry.extracted_comments = php_trim(entry.extracted_comments + "\n" + comment)
            elif "#," == first_two:
                entry.flags = php_array_merge(entry.flags, php_preg_split("/,\\s*/", comment))
            else:
                entry.translator_comments = php_trim(entry.translator_comments + "\n" + comment)
            # end if
        # end def add_comment_to_entry
        #// 
        #// @param string $s
        #// @return string
        #//
        @classmethod
        def trim_quotes(self, s=None):
            
            if php_substr(s, 0, 1) == "\"":
                s = php_substr(s, 1)
            # end if
            if php_substr(s, -1, 1) == "\"":
                s = php_substr(s, 0, -1)
            # end if
            return s
        # end def trim_quotes
    # end class PO
# end if
