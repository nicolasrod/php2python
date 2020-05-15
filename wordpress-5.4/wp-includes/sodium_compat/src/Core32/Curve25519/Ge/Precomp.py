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
if php_class_exists("ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp
#//
class ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp():
    yplusx = Array()
    yminusx = Array()
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
    def __init__(self, yplusx=None, yminusx=None, xy2d=None):
        
        if yplusx == None:
            yplusx = ParagonIE_Sodium_Core32_Curve25519.fe_0()
        # end if
        self.yplusx = yplusx
        if yminusx == None:
            yminusx = ParagonIE_Sodium_Core32_Curve25519.fe_0()
        # end if
        self.yminusx = yminusx
        if xy2d == None:
            xy2d = ParagonIE_Sodium_Core32_Curve25519.fe_0()
        # end if
        self.xy2d = xy2d
    # end def __init__
# end class ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp
