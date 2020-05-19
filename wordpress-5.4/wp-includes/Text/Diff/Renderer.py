#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
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
    #// 
    #// Number of leading context "lines" to preserve.
    #// 
    #// This should be left at zero for this class, but subclasses may want to
    #// set this to other values.
    #//
    _leading_context_lines = 0
    #// 
    #// Number of trailing context "lines" to preserve.
    #// 
    #// This should be left at zero for this class, but subclasses may want to
    #// set this to other values.
    #//
    _trailing_context_lines = 0
    #// 
    #// Constructor.
    #//
    def __init__(self, params_=None):
        if params_ is None:
            params_ = Array()
        # end if
        
        for param_,value_ in params_.items():
            v_ = "_" + param_
            if (php_isset(lambda : self.v_)):
                self.v_ = value_
            # end if
        # end for
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def text_diff_renderer(self, params_=None):
        if params_ is None:
            params_ = Array()
        # end if
        
        self.__init__(params_)
    # end def text_diff_renderer
    #// 
    #// Get any renderer parameters.
    #// 
    #// @return array  All parameters of this renderer object.
    #//
    def getparams(self):
        
        
        params_ = Array()
        for k_,v_ in get_object_vars(self).items():
            if k_[0] == "_":
                params_[php_substr(k_, 1)] = v_
            # end if
        # end for
        return params_
    # end def getparams
    #// 
    #// Renders a diff.
    #// 
    #// @param Text_Diff $diff  A Text_Diff object.
    #// 
    #// @return string  The formatted output.
    #//
    def render(self, diff_=None):
        
        
        xi_ = yi_ = 1
        block_ = False
        context_ = Array()
        nlead_ = self._leading_context_lines
        ntrail_ = self._trailing_context_lines
        output_ = self._startdiff()
        diffs_ = diff_.getdiff()
        for i_,edit_ in diffs_.items():
            #// If these are unchanged (copied) lines, and we want to keep
            #// leading or trailing context lines, extract them from the copy
            #// block.
            if php_is_a(edit_, "Text_Diff_Op_copy"):
                #// Do we have any diff blocks yet?
                if php_is_array(block_):
                    #// How many lines to keep as context from the copy
                    #// block.
                    keep_ = ntrail_ if i_ == php_count(diffs_) - 1 else nlead_ + ntrail_
                    if php_count(edit_.orig) <= keep_:
                        #// We have less lines in the block than we want for
                        #// context => keep the whole block.
                        block_[-1] = edit_
                    else:
                        if ntrail_:
                            #// Create a new block with as many lines as we need
                            #// for the trailing context.
                            context_ = php_array_slice(edit_.orig, 0, ntrail_)
                            block_[-1] = php_new_class("Text_Diff_Op_copy", lambda : Text_Diff_Op_copy(context_))
                        # end if
                        #// @todo
                        output_ += self._block(x0_, ntrail_ + xi_ - x0_, y0_, ntrail_ + yi_ - y0_, block_)
                        block_ = False
                    # end if
                # end if
                #// Keep the copy block as the context for the next block.
                context_ = edit_.orig
            else:
                #// Don't we have any diff blocks yet?
                if (not php_is_array(block_)):
                    #// Extract context lines from the preceding copy block.
                    context_ = php_array_slice(context_, php_count(context_) - nlead_)
                    x0_ = xi_ - php_count(context_)
                    y0_ = yi_ - php_count(context_)
                    block_ = Array()
                    if context_:
                        block_[-1] = php_new_class("Text_Diff_Op_copy", lambda : Text_Diff_Op_copy(context_))
                    # end if
                # end if
                block_[-1] = edit_
            # end if
            if edit_.orig:
                xi_ += php_count(edit_.orig)
            # end if
            if edit_.final:
                yi_ += php_count(edit_.final)
            # end if
        # end for
        if php_is_array(block_):
            output_ += self._block(x0_, xi_ - x0_, y0_, yi_ - y0_, block_)
        # end if
        return output_ + self._enddiff()
    # end def render
    def _block(self, xbeg_=None, xlen_=None, ybeg_=None, ylen_=None, edits_=None):
        
        
        output_ = self._startblock(self._blockheader(xbeg_, xlen_, ybeg_, ylen_))
        for edit_ in edits_:
            for case in Switch(php_strtolower(get_class(edit_))):
                if case("text_diff_op_copy"):
                    output_ += self._context(edit_.orig)
                    break
                # end if
                if case("text_diff_op_add"):
                    output_ += self._added(edit_.final)
                    break
                # end if
                if case("text_diff_op_delete"):
                    output_ += self._deleted(edit_.orig)
                    break
                # end if
                if case("text_diff_op_change"):
                    output_ += self._changed(edit_.orig, edit_.final)
                    break
                # end if
            # end for
        # end for
        return output_ + self._endblock()
    # end def _block
    def _startdiff(self):
        
        
        return ""
    # end def _startdiff
    def _enddiff(self):
        
        
        return ""
    # end def _enddiff
    def _blockheader(self, xbeg_=None, xlen_=None, ybeg_=None, ylen_=None):
        
        
        if xlen_ > 1:
            xbeg_ += "," + xbeg_ + xlen_ - 1
        # end if
        if ylen_ > 1:
            ybeg_ += "," + ybeg_ + ylen_ - 1
        # end if
        #// this matches the GNU Diff behaviour
        if xlen_ and (not ylen_):
            ybeg_ -= 1
        elif (not xlen_):
            xbeg_ -= 1
        # end if
        return xbeg_ + "c" if ylen_ else "d" if xlen_ else "a" + ybeg_
    # end def _blockheader
    def _startblock(self, header_=None):
        
        
        return header_ + "\n"
    # end def _startblock
    def _endblock(self):
        
        
        return ""
    # end def _endblock
    def _lines(self, lines_=None, prefix_=" "):
        
        
        return prefix_ + php_implode(str("\n") + str(prefix_), lines_) + "\n"
    # end def _lines
    def _context(self, lines_=None):
        
        
        return self._lines(lines_, "  ")
    # end def _context
    def _added(self, lines_=None):
        
        
        return self._lines(lines_, "> ")
    # end def _added
    def _deleted(self, lines_=None):
        
        
        return self._lines(lines_, "< ")
    # end def _deleted
    def _changed(self, orig_=None, final_=None):
        
        
        return self._deleted(orig_) + "---\n" + self._added(final_)
    # end def _changed
# end class Text_Diff_Renderer
