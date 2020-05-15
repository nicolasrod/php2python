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
if php_class_exists("ParagonIE_Sodium_Core_Curve25519_Ge_P2", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_Core_Curve25519_Ge_P2
#//
class ParagonIE_Sodium_Core_Curve25519_Ge_P2():
    X = Array()
    Y = Array()
    Z = Array()
    #// 
    #// ParagonIE_Sodium_Core_Curve25519_Ge_P2 constructor.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe|null $x
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe|null $y
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe|null $z
    #//
    def __init__(self, x=None, y=None, z=None):
        
        if x == None:
            x = php_new_class("ParagonIE_Sodium_Core_Curve25519_Fe", lambda : ParagonIE_Sodium_Core_Curve25519_Fe())
        # end if
        self.X = x
        if y == None:
            y = php_new_class("ParagonIE_Sodium_Core_Curve25519_Fe", lambda : ParagonIE_Sodium_Core_Curve25519_Fe())
        # end if
        self.Y = y
        if z == None:
            z = php_new_class("ParagonIE_Sodium_Core_Curve25519_Fe", lambda : ParagonIE_Sodium_Core_Curve25519_Fe())
        # end if
        self.Z = z
    # end def __init__
# end class ParagonIE_Sodium_Core_Curve25519_Ge_P2
