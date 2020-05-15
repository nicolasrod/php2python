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
if php_class_exists("ParagonIE_Sodium_Core32_HSalsa20", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_Core32_HSalsa20
#//
class ParagonIE_Sodium_Core32_HSalsa20(ParagonIE_Sodium_Core32_Salsa20):
    #// 
    #// Calculate an hsalsa20 hash of a single block
    #// 
    #// HSalsa20 doesn't have a counter and will never be used for more than
    #// one block (used to derive a subkey for xsalsa20).
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $in
    #// @param string $k
    #// @param string|null $c
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def hsalsa20(self, in_=None, k=None, c=None):
        
        #// 
        #// @var ParagonIE_Sodium_Core32_Int32 $x0
        #// @var ParagonIE_Sodium_Core32_Int32 $x1
        #// @var ParagonIE_Sodium_Core32_Int32 $x2
        #// @var ParagonIE_Sodium_Core32_Int32 $x3
        #// @var ParagonIE_Sodium_Core32_Int32 $x4
        #// @var ParagonIE_Sodium_Core32_Int32 $x5
        #// @var ParagonIE_Sodium_Core32_Int32 $x6
        #// @var ParagonIE_Sodium_Core32_Int32 $x7
        #// @var ParagonIE_Sodium_Core32_Int32 $x8
        #// @var ParagonIE_Sodium_Core32_Int32 $x9
        #// @var ParagonIE_Sodium_Core32_Int32 $x10
        #// @var ParagonIE_Sodium_Core32_Int32 $x11
        #// @var ParagonIE_Sodium_Core32_Int32 $x12
        #// @var ParagonIE_Sodium_Core32_Int32 $x13
        #// @var ParagonIE_Sodium_Core32_Int32 $x14
        #// @var ParagonIE_Sodium_Core32_Int32 $x15
        #// @var ParagonIE_Sodium_Core32_Int32 $j0
        #// @var ParagonIE_Sodium_Core32_Int32 $j1
        #// @var ParagonIE_Sodium_Core32_Int32 $j2
        #// @var ParagonIE_Sodium_Core32_Int32 $j3
        #// @var ParagonIE_Sodium_Core32_Int32 $j4
        #// @var ParagonIE_Sodium_Core32_Int32 $j5
        #// @var ParagonIE_Sodium_Core32_Int32 $j6
        #// @var ParagonIE_Sodium_Core32_Int32 $j7
        #// @var ParagonIE_Sodium_Core32_Int32 $j8
        #// @var ParagonIE_Sodium_Core32_Int32 $j9
        #// @var ParagonIE_Sodium_Core32_Int32 $j10
        #// @var ParagonIE_Sodium_Core32_Int32 $j11
        #// @var ParagonIE_Sodium_Core32_Int32 $j12
        #// @var ParagonIE_Sodium_Core32_Int32 $j13
        #// @var ParagonIE_Sodium_Core32_Int32 $j14
        #// @var ParagonIE_Sodium_Core32_Int32 $j15
        #//
        if self.strlen(k) < 32:
            raise php_new_class("RangeException", lambda : RangeException("Key must be 32 bytes long"))
        # end if
        if c == None:
            x0 = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32(Array(24944, 30821)))
            x5 = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32(Array(13088, 25710)))
            x10 = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32(Array(31074, 11570)))
            x15 = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32(Array(27424, 25972)))
        else:
            x0 = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(c, 0, 4))
            x5 = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(c, 4, 4))
            x10 = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(c, 8, 4))
            x15 = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(c, 12, 4))
        # end if
        x1 = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(k, 0, 4))
        x2 = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(k, 4, 4))
        x3 = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(k, 8, 4))
        x4 = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(k, 12, 4))
        x6 = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(in_, 0, 4))
        x7 = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(in_, 4, 4))
        x8 = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(in_, 8, 4))
        x9 = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(in_, 12, 4))
        x11 = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(k, 16, 4))
        x12 = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(k, 20, 4))
        x13 = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(k, 24, 4))
        x14 = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(k, 28, 4))
        i = self.ROUNDS
        while i > 0:
            
            x4 = x4.xorint32(x0.addint32(x12).rotateleft(7))
            x8 = x8.xorint32(x4.addint32(x0).rotateleft(9))
            x12 = x12.xorint32(x8.addint32(x4).rotateleft(13))
            x0 = x0.xorint32(x12.addint32(x8).rotateleft(18))
            x9 = x9.xorint32(x5.addint32(x1).rotateleft(7))
            x13 = x13.xorint32(x9.addint32(x5).rotateleft(9))
            x1 = x1.xorint32(x13.addint32(x9).rotateleft(13))
            x5 = x5.xorint32(x1.addint32(x13).rotateleft(18))
            x14 = x14.xorint32(x10.addint32(x6).rotateleft(7))
            x2 = x2.xorint32(x14.addint32(x10).rotateleft(9))
            x6 = x6.xorint32(x2.addint32(x14).rotateleft(13))
            x10 = x10.xorint32(x6.addint32(x2).rotateleft(18))
            x3 = x3.xorint32(x15.addint32(x11).rotateleft(7))
            x7 = x7.xorint32(x3.addint32(x15).rotateleft(9))
            x11 = x11.xorint32(x7.addint32(x3).rotateleft(13))
            x15 = x15.xorint32(x11.addint32(x7).rotateleft(18))
            x1 = x1.xorint32(x0.addint32(x3).rotateleft(7))
            x2 = x2.xorint32(x1.addint32(x0).rotateleft(9))
            x3 = x3.xorint32(x2.addint32(x1).rotateleft(13))
            x0 = x0.xorint32(x3.addint32(x2).rotateleft(18))
            x6 = x6.xorint32(x5.addint32(x4).rotateleft(7))
            x7 = x7.xorint32(x6.addint32(x5).rotateleft(9))
            x4 = x4.xorint32(x7.addint32(x6).rotateleft(13))
            x5 = x5.xorint32(x4.addint32(x7).rotateleft(18))
            x11 = x11.xorint32(x10.addint32(x9).rotateleft(7))
            x8 = x8.xorint32(x11.addint32(x10).rotateleft(9))
            x9 = x9.xorint32(x8.addint32(x11).rotateleft(13))
            x10 = x10.xorint32(x9.addint32(x8).rotateleft(18))
            x12 = x12.xorint32(x15.addint32(x14).rotateleft(7))
            x13 = x13.xorint32(x12.addint32(x15).rotateleft(9))
            x14 = x14.xorint32(x13.addint32(x12).rotateleft(13))
            x15 = x15.xorint32(x14.addint32(x13).rotateleft(18))
            i -= 2
        # end while
        return x0.toreversestring() + x5.toreversestring() + x10.toreversestring() + x15.toreversestring() + x6.toreversestring() + x7.toreversestring() + x8.toreversestring() + x9.toreversestring()
    # end def hsalsa20
# end class ParagonIE_Sodium_Core32_HSalsa20
