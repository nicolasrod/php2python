#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
if php_class_exists("ParagonIE_Sodium_Core32_Curve25519_Ge_Cached", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_Core32_Curve25519_Ge_Cached
#//
class ParagonIE_Sodium_Core32_Curve25519_Ge_Cached():
    #// 
    #// @var ParagonIE_Sodium_Core32_Curve25519_Fe
    #//
    YplusX = Array()
    #// 
    #// @var ParagonIE_Sodium_Core32_Curve25519_Fe
    #//
    YminusX = Array()
    #// 
    #// @var ParagonIE_Sodium_Core32_Curve25519_Fe
    #//
    Z = Array()
    #// 
    #// @var ParagonIE_Sodium_Core32_Curve25519_Fe
    #//
    T2d = Array()
    #// 
    #// ParagonIE_Sodium_Core32_Curve25519_Ge_Cached constructor.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe|null $YplusX
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe|null $YminusX
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe|null $Z
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe|null $T2d
    #//
    def __init__(self, YplusX_=None, YminusX_=None, Z_=None, T2d_=None):
        
        
        if YplusX_ == None:
            YplusX_ = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Fe", lambda : ParagonIE_Sodium_Core32_Curve25519_Fe())
        # end if
        self.YplusX = YplusX_
        if YminusX_ == None:
            YminusX_ = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Fe", lambda : ParagonIE_Sodium_Core32_Curve25519_Fe())
        # end if
        self.YminusX = YminusX_
        if Z_ == None:
            Z_ = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Fe", lambda : ParagonIE_Sodium_Core32_Curve25519_Fe())
        # end if
        self.Z = Z_
        if T2d_ == None:
            T2d_ = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Fe", lambda : ParagonIE_Sodium_Core32_Curve25519_Fe())
        # end if
        self.T2d = T2d_
    # end def __init__
# end class ParagonIE_Sodium_Core32_Curve25519_Ge_Cached
