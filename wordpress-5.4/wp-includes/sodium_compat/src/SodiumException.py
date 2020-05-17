#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
if (not php_class_exists("SodiumException", False)):
    #// 
    #// Class SodiumException
    #//
    class SodiumException(Exception):
        pass
    # end class SodiumException
# end if
