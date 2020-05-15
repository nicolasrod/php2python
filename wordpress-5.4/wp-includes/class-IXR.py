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
#// IXR - The Incutio XML-RPC Library
#// 
#// Copyright (c) 2010, Incutio Ltd.
#// All rights reserved.
#// 
#// Redistribution and use in source and binary forms, with or without
#// modification, are permitted provided that the following conditions are met:
#// 
#// - Redistributions of source code must retain the above copyright notice,
#// this list of conditions and the following disclaimer.
#// - Redistributions in binary form must reproduce the above copyright
#// notice, this list of conditions and the following disclaimer in the
#// documentation and/or other materials provided with the distribution.
#// - Neither the name of Incutio Ltd. nor the names of its contributors
#// may be used to endorse or promote products derived from this software
#// without specific prior written permission.
#// 
#// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#// IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#// THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#// PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
#// CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#// EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#// PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#// PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
#// OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
#// USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#// 
#// @package IXR
#// @since 1.5.0
#// 
#// @copyright  Incutio Ltd 2010 (http://www.incutio.com)
#// @version    1.7.4 7th September 2010
#// @author     Simon Willison
#// @link       http://scripts.incutio.com/xmlrpc/ Site/manual
#// @license    http://www.opensource.org/licenses/bsd-license.php BSD
#//
php_include_file(ABSPATH + WPINC + "/IXR/class-IXR-server.php", once=True)
php_include_file(ABSPATH + WPINC + "/IXR/class-IXR-base64.php", once=True)
php_include_file(ABSPATH + WPINC + "/IXR/class-IXR-client.php", once=True)
php_include_file(ABSPATH + WPINC + "/IXR/class-IXR-clientmulticall.php", once=True)
php_include_file(ABSPATH + WPINC + "/IXR/class-IXR-date.php", once=True)
php_include_file(ABSPATH + WPINC + "/IXR/class-IXR-error.php", once=True)
php_include_file(ABSPATH + WPINC + "/IXR/class-IXR-introspectionserver.php", once=True)
php_include_file(ABSPATH + WPINC + "/IXR/class-IXR-message.php", once=True)
php_include_file(ABSPATH + WPINC + "/IXR/class-IXR-request.php", once=True)
php_include_file(ABSPATH + WPINC + "/IXR/class-IXR-value.php", once=True)
