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
#// Contains Translation_Entry class
#// 
#// @version $Id: entry.php 1157 2015-11-20 04:30:11Z dd32 $
#// @package pomo
#// @subpackage entry
#//
if (not php_class_exists("Translation_Entry", False)):
    #// 
    #// Translation_Entry class encapsulates a translatable string
    #//
    class Translation_Entry():
        #// 
        #// Whether the entry contains a string and its plural form, default is false
        #// 
        #// @var boolean
        #//
        is_plural = False
        context = None
        singular = None
        plural = None
        translations = Array()
        translator_comments = ""
        extracted_comments = ""
        references = Array()
        flags = Array()
        #// 
        #// @param array $args associative array, support following keys:
        #// - singular (string) -- the string to translate, if omitted and empty entry will be created
        #// - plural (string) -- the plural form of the string, setting this will set {@link $is_plural} to true
        #// - translations (array) -- translations of the string and possibly -- its plural forms
        #// - context (string) -- a string differentiating two equal strings used in different contexts
        #// - translator_comments (string) -- comments left by translators
        #// - extracted_comments (string) -- comments left by developers
        #// - references (array) -- places in the code this strings is used, in relative_to_root_path/file.php:linenum form
        #// - flags (array) -- flags like php-format
        #//
        def __init__(self, args_=None):
            if args_ is None:
                args_ = Array()
            # end if
            
            #// If no singular -- empty object.
            if (not (php_isset(lambda : args_["singular"]))):
                return
            # end if
            #// Get member variable values from args hash.
            for varname_,value_ in args_:
                self.varname_ = value_
            # end for
            if (php_isset(lambda : args_["plural"])) and args_["plural"]:
                self.is_plural = True
            # end if
            if (not php_is_array(self.translations)):
                self.translations = Array()
            # end if
            if (not php_is_array(self.references)):
                self.references = Array()
            # end if
            if (not php_is_array(self.flags)):
                self.flags = Array()
            # end if
        # end def __init__
        #// 
        #// PHP4 constructor.
        #// 
        #// @deprecated 5.4.0 Use __construct() instead.
        #// 
        #// @see Translation_Entry::__construct()
        #//
        def translation_entry(self, args_=None):
            if args_ is None:
                args_ = Array()
            # end if
            
            _deprecated_constructor(self.class_, "5.4.0", static.class_)
            self.__init__(args_)
        # end def translation_entry
        #// 
        #// Generates a unique key for this entry
        #// 
        #// @return string|bool the key or false if the entry is empty
        #//
        def key(self):
            
            
            if None == self.singular or "" == self.singular:
                return False
            # end if
            #// Prepend context and EOT, like in MO files.
            key_ = self.singular if (not self.context) else self.context + "" + self.singular
            #// Standardize on \n line endings.
            key_ = php_str_replace(Array("\r\n", "\r"), "\n", key_)
            return key_
        # end def key
        #// 
        #// @param object $other
        #//
        def merge_with(self, other_=None):
            
            
            self.flags = array_unique(php_array_merge(self.flags, other_.flags))
            self.references = array_unique(php_array_merge(self.references, other_.references))
            if self.extracted_comments != other_.extracted_comments:
                self.extracted_comments += other_.extracted_comments
            # end if
        # end def merge_with
    # end class Translation_Entry
# end if
