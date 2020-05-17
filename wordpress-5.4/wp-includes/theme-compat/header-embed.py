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
#// Contains the post embed header template
#// 
#// When a post is embedded in an iframe, this file is used to create the header output
#// if the active theme does not include a header-embed.php template.
#// 
#// @package WordPress
#// @subpackage Theme_Compat
#// @since 4.5.0
#//
if (not php_headers_sent()):
    php_header("X-WP-embed: true")
# end if
php_print("<!DOCTYPE html>\n<html ")
language_attributes()
php_print(" class=\"no-js\">\n<head>\n  <title>")
php_print(wp_get_document_title())
php_print("</title>\n   <meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\">\n ")
#// 
#// Prints scripts or data in the embed template head tag.
#// 
#// @since 4.4.0
#//
do_action("embed_head")
php_print("</head>\n<body ")
body_class()
php_print(">\n")
