#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
if php_class_exists("ParagonIE_Sodium_Core32_Util", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_Core_Util
#//
class ParagonIE_Sodium_Core32_Util(ParagonIE_Sodium_Core_Util):
    pass
# end class ParagonIE_Sodium_Core32_Util
