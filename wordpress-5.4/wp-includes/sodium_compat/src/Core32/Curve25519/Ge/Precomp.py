#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
if php_class_exists("ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp
#//
class ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp():
    #// 
    #// @var ParagonIE_Sodium_Core32_Curve25519_Fe
    #//
    yplusx = Array()
    #// 
    #// @var ParagonIE_Sodium_Core32_Curve25519_Fe
    #//
    yminusx = Array()
    #// 
    #// @var ParagonIE_Sodium_Core32_Curve25519_Fe
    #//
    xy2d = Array()
    #// 
    #// ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp constructor.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $yplusx
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $yminusx
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $xy2d
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def __init__(self, yplusx_=None, yminusx_=None, xy2d_=None):
        
        
        if yplusx_ == None:
            yplusx_ = ParagonIE_Sodium_Core32_Curve25519.fe_0()
        # end if
        self.yplusx = yplusx_
        if yminusx_ == None:
            yminusx_ = ParagonIE_Sodium_Core32_Curve25519.fe_0()
        # end if
        self.yminusx = yminusx_
        if xy2d_ == None:
            xy2d_ = ParagonIE_Sodium_Core32_Curve25519.fe_0()
        # end if
        self.xy2d = xy2d_
    # end def __init__
# end class ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp
