#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
if php_class_exists("ParagonIE_Sodium_Core32_Curve25519_Ge_P2", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_Core32_Curve25519_Ge_P2
#//
class ParagonIE_Sodium_Core32_Curve25519_Ge_P2():
    #// 
    #// @var ParagonIE_Sodium_Core32_Curve25519_Fe
    #//
    X = Array()
    #// 
    #// @var ParagonIE_Sodium_Core32_Curve25519_Fe
    #//
    Y = Array()
    #// 
    #// @var ParagonIE_Sodium_Core32_Curve25519_Fe
    #//
    Z = Array()
    #// 
    #// ParagonIE_Sodium_Core32_Curve25519_Ge_P2 constructor.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe|null $x
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe|null $y
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe|null $z
    #//
    def __init__(self, x_=None, y_=None, z_=None):
        
        
        if x_ == None:
            x_ = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Fe", lambda : ParagonIE_Sodium_Core32_Curve25519_Fe())
        # end if
        self.X = x_
        if y_ == None:
            y_ = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Fe", lambda : ParagonIE_Sodium_Core32_Curve25519_Fe())
        # end if
        self.Y = y_
        if z_ == None:
            z_ = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Fe", lambda : ParagonIE_Sodium_Core32_Curve25519_Fe())
        # end if
        self.Z = z_
    # end def __init__
# end class ParagonIE_Sodium_Core32_Curve25519_Ge_P2
