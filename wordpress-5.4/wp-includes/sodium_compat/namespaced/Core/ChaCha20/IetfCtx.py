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
if not php_defined("ParagonIE_Sodium_Core_ChaCha20"):
    class ParagonIE_Sodium_Core_ChaCha20:
        pass
    # end class
# end if
class ParagonIE_Sodium_Core_ChaCha20(ParagonIE_Sodium_Core_ChaCha20):
    _namespace__ = "ParagonIE_Sodium_Core_ChaCha20"
    class IetfCtx(ParagonIE_Sodium_Core_ChaCha20_IetfCtx):
        pass
    # end class IetfCtx
# end class
