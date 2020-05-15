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
#// Class for a set of entries for translation and their associated headers
#// 
#// @version $Id: translations.php 1157 2015-11-20 04:30:11Z dd32 $
#// @package pomo
#// @subpackage translations
#//
php_include_file(__DIR__ + "/plural-forms.php", once=True)
php_include_file(__DIR__ + "/entry.php", once=True)
if (not php_class_exists("Translations", False)):
    class Translations():
        entries = Array()
        headers = Array()
        #// 
        #// Add entry to the PO structure
        #// 
        #// @param array|Translation_Entry $entry
        #// @return bool true on success, false if the entry doesn't have a key
        #//
        def add_entry(self, entry=None):
            
            if php_is_array(entry):
                entry = php_new_class("Translation_Entry", lambda : Translation_Entry(entry))
            # end if
            key = entry.key()
            if False == key:
                return False
            # end if
            self.entries[key] = entry
            return True
        # end def add_entry
        #// 
        #// @param array|Translation_Entry $entry
        #// @return bool
        #//
        def add_entry_or_merge(self, entry=None):
            
            if php_is_array(entry):
                entry = php_new_class("Translation_Entry", lambda : Translation_Entry(entry))
            # end if
            key = entry.key()
            if False == key:
                return False
            # end if
            if (php_isset(lambda : self.entries[key])):
                self.entries[key].merge_with(entry)
            else:
                self.entries[key] = entry
            # end if
            return True
        # end def add_entry_or_merge
        #// 
        #// Sets $header PO header to $value
        #// 
        #// If the header already exists, it will be overwritten
        #// 
        #// TODO: this should be out of this class, it is gettext specific
        #// 
        #// @param string $header header name, without trailing :
        #// @param string $value header value, without trailing \n
        #//
        def set_header(self, header=None, value=None):
            
            self.headers[header] = value
        # end def set_header
        #// 
        #// @param array $headers
        #//
        def set_headers(self, headers=None):
            
            for header,value in headers:
                self.set_header(header, value)
            # end for
        # end def set_headers
        #// 
        #// @param string $header
        #//
        def get_header(self, header=None):
            
            return self.headers[header] if (php_isset(lambda : self.headers[header])) else False
        # end def get_header
        #// 
        #// @param Translation_Entry $entry
        #//
        def translate_entry(self, entry=None):
            
            key = entry.key()
            return self.entries[key] if (php_isset(lambda : self.entries[key])) else False
        # end def translate_entry
        #// 
        #// @param string $singular
        #// @param string $context
        #// @return string
        #//
        def translate(self, singular=None, context=None):
            
            entry = php_new_class("Translation_Entry", lambda : Translation_Entry(Array({"singular": singular, "context": context})))
            translated = self.translate_entry(entry)
            return translated.translations[0] if translated and (not php_empty(lambda : translated.translations)) else singular
        # end def translate
        #// 
        #// Given the number of items, returns the 0-based index of the plural form to use
        #// 
        #// Here, in the base Translations class, the common logic for English is implemented:
        #// 0 if there is one element, 1 otherwise
        #// 
        #// This function should be overridden by the subclasses. For example MO/PO can derive the logic
        #// from their headers.
        #// 
        #// @param integer $count number of items
        #//
        def select_plural_form(self, count=None):
            
            return 0 if 1 == count else 1
        # end def select_plural_form
        #// 
        #// @return int
        #//
        def get_plural_forms_count(self):
            
            return 2
        # end def get_plural_forms_count
        #// 
        #// @param string $singular
        #// @param string $plural
        #// @param int    $count
        #// @param string $context
        #//
        def translate_plural(self, singular=None, plural=None, count=None, context=None):
            
            entry = php_new_class("Translation_Entry", lambda : Translation_Entry(Array({"singular": singular, "plural": plural, "context": context})))
            translated = self.translate_entry(entry)
            index = self.select_plural_form(count)
            total_plural_forms = self.get_plural_forms_count()
            if translated and 0 <= index and index < total_plural_forms and php_is_array(translated.translations) and (php_isset(lambda : translated.translations[index])):
                return translated.translations[index]
            else:
                return singular if 1 == count else plural
            # end if
        # end def translate_plural
        #// 
        #// Merge $other in the current object.
        #// 
        #// @param Object $other Another Translation object, whose translations will be merged in this one (passed by reference).
        #// @return void
        #//
        def merge_with(self, other=None):
            
            for entry in other.entries:
                self.entries[entry.key()] = entry
            # end for
        # end def merge_with
        #// 
        #// @param object $other
        #//
        def merge_originals_with(self, other=None):
            
            for entry in other.entries:
                if (not (php_isset(lambda : self.entries[entry.key()]))):
                    self.entries[entry.key()] = entry
                else:
                    self.entries[entry.key()].merge_with(entry)
                # end if
            # end for
        # end def merge_originals_with
    # end class Translations
    class Gettext_Translations(Translations):
        #// 
        #// The gettext implementation of select_plural_form.
        #// 
        #// It lives in this class, because there are more than one descendand, which will use it and
        #// they can't share it effectively.
        #// 
        #// @param int $count
        #//
        def gettext_select_plural_form(self, count=None):
            
            if (not (php_isset(lambda : self._gettext_select_plural_form))) or php_is_null(self._gettext_select_plural_form):
                nplurals, expression = self.nplurals_and_expression_from_header(self.get_header("Plural-Forms"))
                self._nplurals = nplurals
                self._gettext_select_plural_form = self.make_plural_form_function(nplurals, expression)
            # end if
            return php_call_user_func(self._gettext_select_plural_form, count)
        # end def gettext_select_plural_form
        #// 
        #// @param string $header
        #// @return array
        #//
        def nplurals_and_expression_from_header(self, header=None):
            
            if php_preg_match("/^\\s*nplurals\\s*=\\s*(\\d+)\\s*;\\s+plural\\s*=\\s*(.+)$/", header, matches):
                nplurals = int(matches[1])
                expression = php_trim(matches[2])
                return Array(nplurals, expression)
            else:
                return Array(2, "n != 1")
            # end if
        # end def nplurals_and_expression_from_header
        #// 
        #// Makes a function, which will return the right translation index, according to the
        #// plural forms header
        #// 
        #// @param int    $nplurals
        #// @param string $expression
        #//
        def make_plural_form_function(self, nplurals=None, expression=None):
            
            try: 
                handler = php_new_class("Plural_Forms", lambda : Plural_Forms(php_rtrim(expression, ";")))
                return Array(handler, "get")
            except Exception as e:
                #// Fall back to default plural-form function.
                return self.make_plural_form_function(2, "n != 1")
            # end try
        # end def make_plural_form_function
        #// 
        #// Adds parentheses to the inner parts of ternary operators in
        #// plural expressions, because PHP evaluates ternary oerators from left to right
        #// 
        #// @param string $expression the expression without parentheses
        #// @return string the expression with parentheses added
        #//
        def parenthesize_plural_exression(self, expression=None):
            
            expression += ";"
            res = ""
            depth = 0
            i = 0
            while i < php_strlen(expression):
                
                char = expression[i]
                for case in Switch(char):
                    if case("?"):
                        res += " ? ("
                        depth += 1
                        break
                    # end if
                    if case(":"):
                        res += ") : ("
                        break
                    # end if
                    if case(";"):
                        res += php_str_repeat(")", depth) + ";"
                        depth = 0
                        break
                    # end if
                    if case():
                        res += char
                    # end if
                # end for
                i += 1
            # end while
            return php_rtrim(res, ";")
        # end def parenthesize_plural_exression
        #// 
        #// @param string $translation
        #// @return array
        #//
        def make_headers(self, translation=None):
            
            headers = Array()
            #// Sometimes \n's are used instead of real new lines.
            translation = php_str_replace("\\n", "\n", translation)
            lines = php_explode("\n", translation)
            for line in lines:
                parts = php_explode(":", line, 2)
                if (not (php_isset(lambda : parts[1]))):
                    continue
                # end if
                headers[php_trim(parts[0])] = php_trim(parts[1])
            # end for
            return headers
        # end def make_headers
        #// 
        #// @param string $header
        #// @param string $value
        #//
        def set_header(self, header=None, value=None):
            
            super().set_header(header, value)
            if "Plural-Forms" == header:
                nplurals, expression = self.nplurals_and_expression_from_header(self.get_header("Plural-Forms"))
                self._nplurals = nplurals
                self._gettext_select_plural_form = self.make_plural_form_function(nplurals, expression)
            # end if
        # end def set_header
    # end class Gettext_Translations
# end if
if (not php_class_exists("NOOP_Translations", False)):
    #// 
    #// Provides the same interface as Translations, but doesn't do anything
    #//
    class NOOP_Translations():
        entries = Array()
        headers = Array()
        def add_entry(self, entry=None):
            
            return True
        # end def add_entry
        #// 
        #// @param string $header
        #// @param string $value
        #//
        def set_header(self, header=None, value=None):
            
            pass
        # end def set_header
        #// 
        #// @param array $headers
        #//
        def set_headers(self, headers=None):
            
            pass
        # end def set_headers
        #// 
        #// @param string $header
        #// @return false
        #//
        def get_header(self, header=None):
            
            return False
        # end def get_header
        #// 
        #// @param Translation_Entry $entry
        #// @return false
        #//
        def translate_entry(self, entry=None):
            
            return False
        # end def translate_entry
        #// 
        #// @param string $singular
        #// @param string $context
        #//
        def translate(self, singular=None, context=None):
            
            return singular
        # end def translate
        #// 
        #// @param int $count
        #// @return bool
        #//
        def select_plural_form(self, count=None):
            
            return 0 if 1 == count else 1
        # end def select_plural_form
        #// 
        #// @return int
        #//
        def get_plural_forms_count(self):
            
            return 2
        # end def get_plural_forms_count
        #// 
        #// @param string $singular
        #// @param string $plural
        #// @param int    $count
        #// @param string $context
        #//
        def translate_plural(self, singular=None, plural=None, count=None, context=None):
            
            return singular if 1 == count else plural
        # end def translate_plural
        #// 
        #// @param object $other
        #//
        def merge_with(self, other=None):
            
            pass
        # end def merge_with
    # end class NOOP_Translations
# end if
