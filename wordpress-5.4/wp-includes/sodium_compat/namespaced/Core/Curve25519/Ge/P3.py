#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
if not php_defined("ParagonIE_Sodium_Core_Curve25519_Ge"):
    class ParagonIE_Sodium_Core_Curve25519_Ge:
        pass
    # end class
# end if
class ParagonIE_Sodium_Core_Curve25519_Ge(ParagonIE_Sodium_Core_Curve25519_Ge):
    _namespace__ = "ParagonIE_Sodium_Core_Curve25519_Ge"
    class P3(ParagonIE_Sodium_Core_Curve25519_Ge_P3):
        pass
    # end class P3
# end class
