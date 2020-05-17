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
        def add_entry(self, entry_=None):
            
            
            if php_is_array(entry_):
                entry_ = php_new_class("Translation_Entry", lambda : Translation_Entry(entry_))
            # end if
            key_ = entry_.key()
            if False == key_:
                return False
            # end if
            self.entries[key_] = entry_
            return True
        # end def add_entry
        #// 
        #// @param array|Translation_Entry $entry
        #// @return bool
        #//
        def add_entry_or_merge(self, entry_=None):
            
            
            if php_is_array(entry_):
                entry_ = php_new_class("Translation_Entry", lambda : Translation_Entry(entry_))
            # end if
            key_ = entry_.key()
            if False == key_:
                return False
            # end if
            if (php_isset(lambda : self.entries[key_])):
                self.entries[key_].merge_with(entry_)
            else:
                self.entries[key_] = entry_
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
        def set_header(self, header_=None, value_=None):
            
            
            self.headers[header_] = value_
        # end def set_header
        #// 
        #// @param array $headers
        #//
        def set_headers(self, headers_=None):
            
            
            for header_,value_ in headers_:
                self.set_header(header_, value_)
            # end for
        # end def set_headers
        #// 
        #// @param string $header
        #//
        def get_header(self, header_=None):
            
            
            return self.headers[header_] if (php_isset(lambda : self.headers[header_])) else False
        # end def get_header
        #// 
        #// @param Translation_Entry $entry
        #//
        def translate_entry(self, entry_=None):
            
            
            key_ = entry_.key()
            return self.entries[key_] if (php_isset(lambda : self.entries[key_])) else False
        # end def translate_entry
        #// 
        #// @param string $singular
        #// @param string $context
        #// @return string
        #//
        def translate(self, singular_=None, context_=None):
            if context_ is None:
                context_ = None
            # end if
            
            entry_ = php_new_class("Translation_Entry", lambda : Translation_Entry(Array({"singular": singular_, "context": context_})))
            translated_ = self.translate_entry(entry_)
            return translated_.translations[0] if translated_ and (not php_empty(lambda : translated_.translations)) else singular_
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
        def select_plural_form(self, count_=None):
            
            
            return 0 if 1 == count_ else 1
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
        def translate_plural(self, singular_=None, plural_=None, count_=None, context_=None):
            if context_ is None:
                context_ = None
            # end if
            
            entry_ = php_new_class("Translation_Entry", lambda : Translation_Entry(Array({"singular": singular_, "plural": plural_, "context": context_})))
            translated_ = self.translate_entry(entry_)
            index_ = self.select_plural_form(count_)
            total_plural_forms_ = self.get_plural_forms_count()
            if translated_ and 0 <= index_ and index_ < total_plural_forms_ and php_is_array(translated_.translations) and (php_isset(lambda : translated_.translations[index_])):
                return translated_.translations[index_]
            else:
                return singular_ if 1 == count_ else plural_
            # end if
        # end def translate_plural
        #// 
        #// Merge $other in the current object.
        #// 
        #// @param Object $other Another Translation object, whose translations will be merged in this one (passed by reference).
        #// @return void
        #//
        def merge_with(self, other_=None):
            
            
            for entry_ in other_.entries:
                self.entries[entry_.key()] = entry_
            # end for
        # end def merge_with
        #// 
        #// @param object $other
        #//
        def merge_originals_with(self, other_=None):
            
            
            for entry_ in other_.entries:
                if (not (php_isset(lambda : self.entries[entry_.key()]))):
                    self.entries[entry_.key()] = entry_
                else:
                    self.entries[entry_.key()].merge_with(entry_)
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
        def gettext_select_plural_form(self, count_=None):
            
            
            if (not (php_isset(lambda : self._gettext_select_plural_form))) or php_is_null(self._gettext_select_plural_form):
                nplurals_, expression_ = self.nplurals_and_expression_from_header(self.get_header("Plural-Forms"))
                self._nplurals = nplurals_
                self._gettext_select_plural_form = self.make_plural_form_function(nplurals_, expression_)
            # end if
            return php_call_user_func(self._gettext_select_plural_form, count_)
        # end def gettext_select_plural_form
        #// 
        #// @param string $header
        #// @return array
        #//
        def nplurals_and_expression_from_header(self, header_=None):
            
            
            if php_preg_match("/^\\s*nplurals\\s*=\\s*(\\d+)\\s*;\\s+plural\\s*=\\s*(.+)$/", header_, matches_):
                nplurals_ = php_int(matches_[1])
                expression_ = php_trim(matches_[2])
                return Array(nplurals_, expression_)
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
        def make_plural_form_function(self, nplurals_=None, expression_=None):
            
            
            try: 
                handler_ = php_new_class("Plural_Forms", lambda : Plural_Forms(php_rtrim(expression_, ";")))
                return Array(handler_, "get")
            except Exception as e_:
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
        def parenthesize_plural_exression(self, expression_=None):
            
            
            expression_ += ";"
            res_ = ""
            depth_ = 0
            i_ = 0
            while i_ < php_strlen(expression_):
                
                char_ = expression_[i_]
                for case in Switch(char_):
                    if case("?"):
                        res_ += " ? ("
                        depth_ += 1
                        break
                    # end if
                    if case(":"):
                        res_ += ") : ("
                        break
                    # end if
                    if case(";"):
                        res_ += php_str_repeat(")", depth_) + ";"
                        depth_ = 0
                        break
                    # end if
                    if case():
                        res_ += char_
                    # end if
                # end for
                i_ += 1
            # end while
            return php_rtrim(res_, ";")
        # end def parenthesize_plural_exression
        #// 
        #// @param string $translation
        #// @return array
        #//
        def make_headers(self, translation_=None):
            
            
            headers_ = Array()
            #// Sometimes \n's are used instead of real new lines.
            translation_ = php_str_replace("\\n", "\n", translation_)
            lines_ = php_explode("\n", translation_)
            for line_ in lines_:
                parts_ = php_explode(":", line_, 2)
                if (not (php_isset(lambda : parts_[1]))):
                    continue
                # end if
                headers_[php_trim(parts_[0])] = php_trim(parts_[1])
            # end for
            return headers_
        # end def make_headers
        #// 
        #// @param string $header
        #// @param string $value
        #//
        def set_header(self, header_=None, value_=None):
            
            
            super().set_header(header_, value_)
            if "Plural-Forms" == header_:
                nplurals_, expression_ = self.nplurals_and_expression_from_header(self.get_header("Plural-Forms"))
                self._nplurals = nplurals_
                self._gettext_select_plural_form = self.make_plural_form_function(nplurals_, expression_)
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
        def add_entry(self, entry_=None):
            
            
            return True
        # end def add_entry
        #// 
        #// @param string $header
        #// @param string $value
        #//
        def set_header(self, header_=None, value_=None):
            
            
            pass
        # end def set_header
        #// 
        #// @param array $headers
        #//
        def set_headers(self, headers_=None):
            
            
            pass
        # end def set_headers
        #// 
        #// @param string $header
        #// @return false
        #//
        def get_header(self, header_=None):
            
            
            return False
        # end def get_header
        #// 
        #// @param Translation_Entry $entry
        #// @return false
        #//
        def translate_entry(self, entry_=None):
            
            
            return False
        # end def translate_entry
        #// 
        #// @param string $singular
        #// @param string $context
        #//
        def translate(self, singular_=None, context_=None):
            if context_ is None:
                context_ = None
            # end if
            
            return singular_
        # end def translate
        #// 
        #// @param int $count
        #// @return bool
        #//
        def select_plural_form(self, count_=None):
            
            
            return 0 if 1 == count_ else 1
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
        def translate_plural(self, singular_=None, plural_=None, count_=None, context_=None):
            if context_ is None:
                context_ = None
            # end if
            
            return singular_ if 1 == count_ else plural_
        # end def translate_plural
        #// 
        #// @param object $other
        #//
        def merge_with(self, other_=None):
            
            
            pass
        # end def merge_with
    # end class NOOP_Translations
# end if
