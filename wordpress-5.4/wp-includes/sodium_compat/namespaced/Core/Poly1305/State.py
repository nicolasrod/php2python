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
if not php_defined("ParagonIE_Sodium_Core_Poly1305"):
    class ParagonIE_Sodium_Core_Poly1305:
        pass
    # end class
# end if
class ParagonIE_Sodium_Core_Poly1305(ParagonIE_Sodium_Core_Poly1305):
    _namespace__ = "ParagonIE_Sodium_Core_Poly1305"
    class State(ParagonIE_Sodium_Core_Poly1305_State):
        pass
    # end class State
# end class
