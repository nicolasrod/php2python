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
#// A class to render Diffs in different formats.
#// 
#// This class renders the diff in classic diff format. It is intended that
#// this class be customized via inheritance, to obtain fancier outputs.
#// 
#// Copyright 2004-2010 The Horde Project (http://www.horde.org/)
#// 
#// See the enclosed file COPYING for license information (LGPL). If you did
#// not receive this file, see http://opensource.org/licenses/lgpl-license.php.
#// 
#// @package Text_Diff
#//
class Text_Diff_Renderer():
    _leading_context_lines = 0
    _trailing_context_lines = 0
    #// 
    #// Constructor.
    #//
    def __init__(self, params=Array()):
        
        for param,value in params:
            v = "_" + param
            if (php_isset(lambda : self.v)):
                self.v = value
            # end if
        # end for
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def text_diff_renderer(self, params=Array()):
        
        self.__init__(params)
    # end def text_diff_renderer
    #// 
    #// Get any renderer parameters.
    #// 
    #// @return array  All parameters of this renderer object.
    #//
    def getparams(self):
        
        params = Array()
        for k,v in get_object_vars(self):
            if k[0] == "_":
                params[php_substr(k, 1)] = v
            # end if
        # end for
        return params
    # end def getparams
    #// 
    #// Renders a diff.
    #// 
    #// @param Text_Diff $diff  A Text_Diff object.
    #// 
    #// @return string  The formatted output.
    #//
    def render(self, diff=None):
        
        xi = yi = 1
        block = False
        context = Array()
        nlead = self._leading_context_lines
        ntrail = self._trailing_context_lines
        output = self._startdiff()
        diffs = diff.getdiff()
        for i,edit in diffs:
            #// If these are unchanged (copied) lines, and we want to keep
            #// leading or trailing context lines, extract them from the copy
            #// block.
            if php_is_a(edit, "Text_Diff_Op_copy"):
                #// Do we have any diff blocks yet?
                if php_is_array(block):
                    #// How many lines to keep as context from the copy
                    #// block.
                    keep = ntrail if i == php_count(diffs) - 1 else nlead + ntrail
                    if php_count(edit.orig) <= keep:
                        #// We have less lines in the block than we want for
                        #// context => keep the whole block.
                        block[-1] = edit
                    else:
                        if ntrail:
                            #// Create a new block with as many lines as we need
                            #// for the trailing context.
                            context = php_array_slice(edit.orig, 0, ntrail)
                            block[-1] = php_new_class("Text_Diff_Op_copy", lambda : Text_Diff_Op_copy(context))
                        # end if
                        #// @todo
                        output += self._block(x0, ntrail + xi - x0, y0, ntrail + yi - y0, block)
                        block = False
                    # end if
                # end if
                #// Keep the copy block as the context for the next block.
                context = edit.orig
            else:
                #// Don't we have any diff blocks yet?
                if (not php_is_array(block)):
                    #// Extract context lines from the preceding copy block.
                    context = php_array_slice(context, php_count(context) - nlead)
                    x0 = xi - php_count(context)
                    y0 = yi - php_count(context)
                    block = Array()
                    if context:
                        block[-1] = php_new_class("Text_Diff_Op_copy", lambda : Text_Diff_Op_copy(context))
                    # end if
                # end if
                block[-1] = edit
            # end if
            if edit.orig:
                xi += php_count(edit.orig)
            # end if
            if edit.final:
                yi += php_count(edit.final)
            # end if
        # end for
        if php_is_array(block):
            output += self._block(x0, xi - x0, y0, yi - y0, block)
        # end if
        return output + self._enddiff()
    # end def render
    def _block(self, xbeg=None, xlen=None, ybeg=None, ylen=None, edits=None):
        
        output = self._startblock(self._blockheader(xbeg, xlen, ybeg, ylen))
        for edit in edits:
            for case in Switch(php_strtolower(get_class(edit))):
                if case("text_diff_op_copy"):
                    output += self._context(edit.orig)
                    break
                # end if
                if case("text_diff_op_add"):
                    output += self._added(edit.final)
                    break
                # end if
                if case("text_diff_op_delete"):
                    output += self._deleted(edit.orig)
                    break
                # end if
                if case("text_diff_op_change"):
                    output += self._changed(edit.orig, edit.final)
                    break
                # end if
            # end for
        # end for
        return output + self._endblock()
    # end def _block
    def _startdiff(self):
        
        return ""
    # end def _startdiff
    def _enddiff(self):
        
        return ""
    # end def _enddiff
    def _blockheader(self, xbeg=None, xlen=None, ybeg=None, ylen=None):
        
        if xlen > 1:
            xbeg += "," + xbeg + xlen - 1
        # end if
        if ylen > 1:
            ybeg += "," + ybeg + ylen - 1
        # end if
        #// this matches the GNU Diff behaviour
        if xlen and (not ylen):
            ybeg -= 1
        elif (not xlen):
            xbeg -= 1
        # end if
        return xbeg + "c" if ylen else "d" if xlen else "a" + ybeg
    # end def _blockheader
    def _startblock(self, header=None):
        
        return header + "\n"
    # end def _startblock
    def _endblock(self):
        
        return ""
    # end def _endblock
    def _lines(self, lines=None, prefix=" "):
        
        return prefix + php_implode(str("\n") + str(prefix), lines) + "\n"
    # end def _lines
    def _context(self, lines=None):
        
        return self._lines(lines, "  ")
    # end def _context
    def _added(self, lines=None):
        
        return self._lines(lines, "> ")
    # end def _added
    def _deleted(self, lines=None):
        
        return self._lines(lines, "< ")
    # end def _deleted
    def _changed(self, orig=None, final=None):
        
        return self._deleted(orig) + "---\n" + self._added(final)
    # end def _changed
# end class Text_Diff_Renderer
