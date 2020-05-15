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
#// Edit Tags Administration: Messages
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 4.4.0
#//
messages = Array()
#// 0 = unused. Messages start at index 1.
messages["_item"] = Array({0: "", 1: __("Item added."), 2: __("Item deleted."), 3: __("Item updated."), 4: __("Item not added."), 5: __("Item not updated."), 6: __("Items deleted.")})
messages["category"] = Array({0: "", 1: __("Category added."), 2: __("Category deleted."), 3: __("Category updated."), 4: __("Category not added."), 5: __("Category not updated."), 6: __("Categories deleted.")})
messages["post_tag"] = Array({0: "", 1: __("Tag added."), 2: __("Tag deleted."), 3: __("Tag updated."), 4: __("Tag not added."), 5: __("Tag not updated."), 6: __("Tags deleted.")})
#// 
#// Filters the messages displayed when a tag is updated.
#// 
#// @since 3.7.0
#// 
#// @param array $messages The messages to be displayed.
#//
messages = apply_filters("term_updated_messages", messages)
message = False
if (php_isset(lambda : PHP_REQUEST["message"])) and int(PHP_REQUEST["message"]):
    msg = int(PHP_REQUEST["message"])
    if (php_isset(lambda : messages[taxonomy][msg])):
        message = messages[taxonomy][msg]
    elif (not (php_isset(lambda : messages[taxonomy]))) and (php_isset(lambda : messages["_item"][msg])):
        message = messages["_item"][msg]
    # end if
# end if
