#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
if not php_defined("ParagonIE_Sodium_Core"):
    class ParagonIE_Sodium_Core:
        pass
    # end class
# end if
class ParagonIE_Sodium_Core(ParagonIE_Sodium_Core):
    _namespace__ = "ParagonIE_Sodium_Core"
    class Xsalsa20(ParagonIE_Sodium_Core_XSalsa20):
        pass
    # end class Xsalsa20
# end class
