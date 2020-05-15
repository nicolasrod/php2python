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
if php_class_exists("ParagonIE_Sodium_Core_Curve25519_Ge_Cached", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_Core_Curve25519_Ge_Cached
#//
class ParagonIE_Sodium_Core_Curve25519_Ge_Cached():
    YplusX = Array()
    YminusX = Array()
    Z = Array()
    T2d = Array()
    #// 
    #// ParagonIE_Sodium_Core_Curve25519_Ge_Cached constructor.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe|null $YplusX
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe|null $YminusX
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe|null $Z
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe|null $T2d
    #//
    def __init__(self, YplusX=None, YminusX=None, Z=None, T2d=None):
        
        if YplusX == None:
            YplusX = php_new_class("ParagonIE_Sodium_Core_Curve25519_Fe", lambda : ParagonIE_Sodium_Core_Curve25519_Fe())
        # end if
        self.YplusX = YplusX
        if YminusX == None:
            YminusX = php_new_class("ParagonIE_Sodium_Core_Curve25519_Fe", lambda : ParagonIE_Sodium_Core_Curve25519_Fe())
        # end if
        self.YminusX = YminusX
        if Z == None:
            Z = php_new_class("ParagonIE_Sodium_Core_Curve25519_Fe", lambda : ParagonIE_Sodium_Core_Curve25519_Fe())
        # end if
        self.Z = Z
        if T2d == None:
            T2d = php_new_class("ParagonIE_Sodium_Core_Curve25519_Fe", lambda : ParagonIE_Sodium_Core_Curve25519_Fe())
        # end if
        self.T2d = T2d
    # end def __init__
# end class ParagonIE_Sodium_Core_Curve25519_Ge_Cached
