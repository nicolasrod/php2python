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
if php_class_exists("ParagonIE_Sodium_Core_HSalsa20", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_Core_HSalsa20
#//
class ParagonIE_Sodium_Core_HSalsa20(ParagonIE_Sodium_Core_Salsa20):
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
    #// @throws TypeError
    #//
    @classmethod
    def hsalsa20(self, in_=None, k=None, c=None):
        
        if c == None:
            x0 = 1634760805
            x5 = 857760878
            x10 = 2036477234
            x15 = 1797285236
        else:
            x0 = self.load_4(self.substr(c, 0, 4))
            x5 = self.load_4(self.substr(c, 4, 4))
            x10 = self.load_4(self.substr(c, 8, 4))
            x15 = self.load_4(self.substr(c, 12, 4))
        # end if
        x1 = self.load_4(self.substr(k, 0, 4))
        x2 = self.load_4(self.substr(k, 4, 4))
        x3 = self.load_4(self.substr(k, 8, 4))
        x4 = self.load_4(self.substr(k, 12, 4))
        x11 = self.load_4(self.substr(k, 16, 4))
        x12 = self.load_4(self.substr(k, 20, 4))
        x13 = self.load_4(self.substr(k, 24, 4))
        x14 = self.load_4(self.substr(k, 28, 4))
        x6 = self.load_4(self.substr(in_, 0, 4))
        x7 = self.load_4(self.substr(in_, 4, 4))
        x8 = self.load_4(self.substr(in_, 8, 4))
        x9 = self.load_4(self.substr(in_, 12, 4))
        i = self.ROUNDS
        while i > 0:
            
            x4 ^= self.rotate(x0 + x12, 7)
            x8 ^= self.rotate(x4 + x0, 9)
            x12 ^= self.rotate(x8 + x4, 13)
            x0 ^= self.rotate(x12 + x8, 18)
            x9 ^= self.rotate(x5 + x1, 7)
            x13 ^= self.rotate(x9 + x5, 9)
            x1 ^= self.rotate(x13 + x9, 13)
            x5 ^= self.rotate(x1 + x13, 18)
            x14 ^= self.rotate(x10 + x6, 7)
            x2 ^= self.rotate(x14 + x10, 9)
            x6 ^= self.rotate(x2 + x14, 13)
            x10 ^= self.rotate(x6 + x2, 18)
            x3 ^= self.rotate(x15 + x11, 7)
            x7 ^= self.rotate(x3 + x15, 9)
            x11 ^= self.rotate(x7 + x3, 13)
            x15 ^= self.rotate(x11 + x7, 18)
            x1 ^= self.rotate(x0 + x3, 7)
            x2 ^= self.rotate(x1 + x0, 9)
            x3 ^= self.rotate(x2 + x1, 13)
            x0 ^= self.rotate(x3 + x2, 18)
            x6 ^= self.rotate(x5 + x4, 7)
            x7 ^= self.rotate(x6 + x5, 9)
            x4 ^= self.rotate(x7 + x6, 13)
            x5 ^= self.rotate(x4 + x7, 18)
            x11 ^= self.rotate(x10 + x9, 7)
            x8 ^= self.rotate(x11 + x10, 9)
            x9 ^= self.rotate(x8 + x11, 13)
            x10 ^= self.rotate(x9 + x8, 18)
            x12 ^= self.rotate(x15 + x14, 7)
            x13 ^= self.rotate(x12 + x15, 9)
            x14 ^= self.rotate(x13 + x12, 13)
            x15 ^= self.rotate(x14 + x13, 18)
            i -= 2
        # end while
        return self.store32_le(x0) + self.store32_le(x5) + self.store32_le(x10) + self.store32_le(x15) + self.store32_le(x6) + self.store32_le(x7) + self.store32_le(x8) + self.store32_le(x9)
    # end def hsalsa20
# end class ParagonIE_Sodium_Core_HSalsa20
