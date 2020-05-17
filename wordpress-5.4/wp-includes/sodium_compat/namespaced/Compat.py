#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
if not php_defined("ParagonIE_Sodium"):
    class ParagonIE_Sodium:
        pass
    # end class
# end if
class ParagonIE_Sodium(ParagonIE_Sodium):
    _namespace__ = "ParagonIE_Sodium"
    class Compat(ParagonIE_Sodium_Compat):
        pass
    # end class Compat
# end class
