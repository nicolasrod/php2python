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
#// 
#// IXR_Error
#// 
#// @package IXR
#// @since 1.5.0
#//
class IXR_Error():
    code = Array()
    message = Array()
    #// 
    #// PHP5 constructor.
    #//
    def __init__(self, code=None, message=None):
        
        self.code = code
        self.message = htmlspecialchars(message)
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def ixr_error(self, code=None, message=None):
        
        self.__init__(code, message)
    # end def ixr_error
    def getxml(self):
        
        xml = str("""<methodResponse>\n  <fault>\n    <value>\n      <struct>\n        <member>\n          <name>faultCode</name>\n          <value><int>""") + str(self.code) + str("""</int></value>\n        </member>\n        <member>\n          <name>faultString</name>\n          <value><string>""") + str(self.message) + str("""</string></value>\n        </member>\n      </struct>\n    </value>\n  </fault>\n</methodResponse>\n""")
        return xml
    # end def getxml
# end class IXR_Error
