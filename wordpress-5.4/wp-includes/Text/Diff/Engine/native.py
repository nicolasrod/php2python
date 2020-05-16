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
#// Class used internally by Text_Diff to actually compute the diffs.
#// 
#// This class is implemented using native PHP code.
#// 
#// The algorithm used here is mostly lifted from the perl module
#// Algorithm::Diff (version 1.06) by Ned Konz, which is available at:
#// http://www.perl.com/CPAN/authors/id/N/NE/NEDKONZ/Algorithm-Diff-1.06.zip
#// 
#// More ideas are taken from: http://www.ics.uci.edu/~eppstein/161/960229.html
#// 
#// Some ideas (and a bit of code) are taken from analyze.c, of GNU
#// diffutils-2.7, which can be found at:
#// ftp://gnudist.gnu.org/pub/gnu/diffutils/diffutils-2.7.tar.gz
#// 
#// Some ideas (subdivision by NCHUNKS > 2, and some optimizations) are from
#// Geoffrey T. Dairiki <dairiki@dairiki.org>. The original PHP version of this
#// code was written by him, and is used/adapted with his permission.
#// 
#// Copyright 2004-2010 The Horde Project (http://www.horde.org/)
#// 
#// See the enclosed file COPYING for license information (LGPL). If you did
#// not receive this file, see http://opensource.org/licenses/lgpl-license.php.
#// 
#// @author  Geoffrey T. Dairiki <dairiki@dairiki.org>
#// @package Text_Diff
#//
class Text_Diff_Engine_native():
    def diff(self, from_lines=None, to_lines=None):
        
        array_walk(from_lines, Array("Text_Diff", "trimNewlines"))
        array_walk(to_lines, Array("Text_Diff", "trimNewlines"))
        n_from = php_count(from_lines)
        n_to = php_count(to_lines)
        self.xchanged = self.ychanged = Array()
        self.xv = self.yv = Array()
        self.xind = self.yind = Array()
        self.seq = None
        self.in_seq = None
        self.lcs = None
        #// Skip leading common lines.
        skip = 0
        while skip < n_from and skip < n_to:
            
            if from_lines[skip] != to_lines[skip]:
                break
            # end if
            self.xchanged[skip] = self.ychanged[skip] = False
            skip += 1
        # end while
        #// Skip trailing common lines.
        xi = n_from
        yi = n_to
        endskip = 0
        while xi > skip and yi > skip:
            
            if from_lines[xi] != to_lines[yi]:
                xi -= 1
                yi -= 1
                break
            # end if
            self.xchanged[xi] = self.ychanged[yi] = False
            endskip += 1
        # end while
        #// Ignore lines which do not exist in both files.
        xi = skip
        while xi < n_from - endskip:
            
            xhash[from_lines[xi]] = 1
            xi += 1
        # end while
        yi = skip
        while yi < n_to - endskip:
            
            line = to_lines[yi]
            self.ychanged[yi] = php_empty(lambda : xhash[line])
            if self.ychanged[yi]:
                continue
            # end if
            yhash[line] = 1
            self.yv[-1] = line
            self.yind[-1] = yi
            yi += 1
        # end while
        xi = skip
        while xi < n_from - endskip:
            
            line = from_lines[xi]
            self.xchanged[xi] = php_empty(lambda : yhash[line])
            if self.xchanged[xi]:
                continue
            # end if
            self.xv[-1] = line
            self.xind[-1] = xi
            xi += 1
        # end while
        #// Find the LCS.
        self._compareseq(0, php_count(self.xv), 0, php_count(self.yv))
        #// Merge edits when possible.
        self._shiftboundaries(from_lines, self.xchanged, self.ychanged)
        self._shiftboundaries(to_lines, self.ychanged, self.xchanged)
        #// Compute the edit operations.
        edits = Array()
        xi = yi = 0
        while True:
            
            if not (xi < n_from or yi < n_to):
                break
            # end if
            assert(yi < n_to or self.xchanged[xi])
            assert(xi < n_from or self.ychanged[yi])
            #// Skip matching "snake".
            copy = Array()
            while True:
                
                if not (xi < n_from and yi < n_to and (not self.xchanged[xi]) and (not self.ychanged[yi])):
                    break
                # end if
                copy[-1] = from_lines[xi]
                xi += 1
                yi += 1
            # end while
            if copy:
                edits[-1] = php_new_class("Text_Diff_Op_copy", lambda : Text_Diff_Op_copy(copy))
            # end if
            #// Find deletes & adds.
            delete = Array()
            while True:
                
                if not (xi < n_from and self.xchanged[xi]):
                    break
                # end if
                delete[-1] = from_lines[xi]
                xi += 1
            # end while
            add = Array()
            while True:
                
                if not (yi < n_to and self.ychanged[yi]):
                    break
                # end if
                add[-1] = to_lines[yi]
                yi += 1
            # end while
            if delete and add:
                edits[-1] = php_new_class("Text_Diff_Op_change", lambda : Text_Diff_Op_change(delete, add))
            elif delete:
                edits[-1] = php_new_class("Text_Diff_Op_delete", lambda : Text_Diff_Op_delete(delete))
            elif add:
                edits[-1] = php_new_class("Text_Diff_Op_add", lambda : Text_Diff_Op_add(add))
            # end if
        # end while
        return edits
    # end def diff
    #// 
    #// Divides the Largest Common Subsequence (LCS) of the sequences (XOFF,
    #// XLIM) and (YOFF, YLIM) into NCHUNKS approximately equally sized
    #// segments.
    #// 
    #// Returns (LCS, PTS).  LCS is the length of the LCS. PTS is an array of
    #// NCHUNKS+1 (X, Y) indexes giving the diving points between sub
    #// sequences.  The first sub-sequence is contained in (X0, X1), (Y0, Y1),
    #// the second in (X1, X2), (Y1, Y2) and so on.  Note that (X0, Y0) ==
    #// (XOFF, YOFF) and (X[NCHUNKS], Y[NCHUNKS]) == (XLIM, YLIM).
    #// 
    #// This function assumes that the first lines of the specified portions of
    #// the two files do not match, and likewise that the last lines do not
    #// match.  The caller must trim matching lines from the beginning and end
    #// of the portions it is going to specify.
    #//
    def _diag(self, xoff=None, xlim=None, yoff=None, ylim=None, nchunks=None):
        
        flip = False
        if xlim - xoff > ylim - yoff:
            #// Things seems faster (I'm not sure I understand why) when the
            #// shortest sequence is in X.
            flip = True
            xoff, xlim, yoff, ylim = Array(yoff, ylim, xoff, xlim)
        # end if
        if flip:
            i = ylim - 1
            while i >= yoff:
                
                ymatches[self.xv[i]][-1] = i
                i -= 1
            # end while
        else:
            i = ylim - 1
            while i >= yoff:
                
                ymatches[self.yv[i]][-1] = i
                i -= 1
            # end while
        # end if
        self.lcs = 0
        self.seq[0] = yoff - 1
        self.in_seq = Array()
        ymids[0] = Array()
        numer = xlim - xoff + nchunks - 1
        x = xoff
        chunk = 0
        while chunk < nchunks:
            
            if chunk > 0:
                i = 0
                while i <= self.lcs:
                    
                    ymids[i][chunk - 1] = self.seq[i]
                    i += 1
                # end while
            # end if
            x1 = xoff + php_int(numer + xlim - xoff * chunk / nchunks)
            while x < x1:
                
                line = self.yv[x] if flip else self.xv[x]
                if php_empty(lambda : ymatches[line]):
                    continue
                # end if
                matches = ymatches[line]
                reset(matches)
                while True:
                    y = current(matches)
                    if not (y):
                        break
                    # end if
                    if php_empty(lambda : self.in_seq[y]):
                        k = self._lcspos(y)
                        assert(k > 0)
                        ymids[k] = ymids[k - 1]
                        break
                    # end if
                    next(matches)
                # end while
                while True:
                    y = current(matches)
                    if not (y):
                        break
                    # end if
                    if y > self.seq[k - 1]:
                        assert(y <= self.seq[k])
                        #// Optimization: this is a common case: next match is
                        #// just replacing previous match.
                        self.in_seq[self.seq[k]] = False
                        self.seq[k] = y
                        self.in_seq[y] = 1
                    elif php_empty(lambda : self.in_seq[y]):
                        k = self._lcspos(y)
                        assert(k > 0)
                        ymids[k] = ymids[k - 1]
                    # end if
                    next(matches)
                # end while
                x += 1
            # end while
            chunk += 1
        # end while
        seps[-1] = Array(yoff, xoff) if flip else Array(xoff, yoff)
        ymid = ymids[self.lcs]
        n = 0
        while n < nchunks - 1:
            
            x1 = xoff + php_int(numer + xlim - xoff * n / nchunks)
            y1 = ymid[n] + 1
            seps[-1] = Array(y1, x1) if flip else Array(x1, y1)
            n += 1
        # end while
        seps[-1] = Array(ylim, xlim) if flip else Array(xlim, ylim)
        return Array(self.lcs, seps)
    # end def _diag
    self.lcs += 1
    def _lcspos(self, ypos=None):
        
        end_ = self.lcs
        if end_ == 0 or ypos > self.seq[end_]:
            self.lcs += 1
            self.seq[self.lcs] = ypos
            self.in_seq[ypos] = 1
            return self.lcs
        # end if
        beg = 1
        while True:
            
            if not (beg < end_):
                break
            # end if
            mid = php_int(beg + end_ / 2)
            if ypos > self.seq[mid]:
                beg = mid + 1
            else:
                end_ = mid
            # end if
        # end while
        assert(ypos != self.seq[end_])
        self.in_seq[self.seq[end_]] = False
        self.seq[end_] = ypos
        self.in_seq[ypos] = 1
        return end_
    # end def _lcspos
    #// 
    #// Finds LCS of two sequences.
    #// 
    #// The results are recorded in the vectors $this->{x,y}changed[], by
    #// storing a 1 in the element for each line that is an insertion or
    #// deletion (ie. is not in the LCS).
    #// 
    #// The subsequence of file 0 is (XOFF, XLIM) and likewise for file 1.
    #// 
    #// Note that XLIM, YLIM are exclusive bounds.  All line numbers are
    #// origin-0 and discarded lines are not counted.
    #//
    def _compareseq(self, xoff=None, xlim=None, yoff=None, ylim=None):
        
        #// Slide down the bottom initial diagonal.
        while True:
            
            if not (xoff < xlim and yoff < ylim and self.xv[xoff] == self.yv[yoff]):
                break
            # end if
            xoff += 1
            yoff += 1
        # end while
        #// Slide up the top initial diagonal.
        while True:
            
            if not (xlim > xoff and ylim > yoff and self.xv[xlim - 1] == self.yv[ylim - 1]):
                break
            # end if
            xlim -= 1
            ylim -= 1
        # end while
        if xoff == xlim or yoff == ylim:
            lcs = 0
        else:
            #// This is ad hoc but seems to work well.  $nchunks =
            #// sqrt(min($xlim - $xoff, $ylim - $yoff) / 2.5); $nchunks =
            #// max(2,min(8,(int)$nchunks));
            nchunks = php_min(7, xlim - xoff, ylim - yoff) + 1
            lcs, seps = self._diag(xoff, xlim, yoff, ylim, nchunks)
        # end if
        if lcs == 0:
            #// X and Y sequences have no common subsequence: mark all
            #// changed.
            while True:
                
                if not (yoff < ylim):
                    break
                # end if
                self.ychanged[self.yind[yoff]] = 1
                yoff += 1
            # end while
            while True:
                
                if not (xoff < xlim):
                    break
                # end if
                self.xchanged[self.xind[xoff]] = 1
                xoff += 1
            # end while
        else:
            #// Use the partitions to split this problem into subproblems.
            reset(seps)
            pt1 = seps[0]
            while True:
                pt2 = next(seps)
                if not (pt2):
                    break
                # end if
                self._compareseq(pt1[0], pt2[0], pt1[1], pt2[1])
                pt1 = pt2
            # end while
        # end if
    # end def _compareseq
    yoff += 1
    xoff += 1
    start -= 1
    i -= 1
    start -= 1
    i -= 1
    #// 
    #// Adjusts inserts/deletes of identical lines to join changes as much as
    #// possible.
    #// 
    #// We do something when a run of changed lines include a line at one end
    #// and has an excluded, identical line at the other.  We are free to
    #// choose which identical line is included.  `compareseq' usually chooses
    #// the one at the beginning, but usually it is cleaner to consider the
    #// following identical line to be the "change".
    #// 
    #// This is extracted verbatim from analyze.c (GNU diffutils-2.7).
    #//
    def _shiftboundaries(self, lines=None, changed=None, other_changed=None):
        
        i = 0
        j = 0
        assert(php_count(lines) == php_count(changed))
        len = php_count(lines)
        other_len = php_count(other_changed)
        while True:
            
            if not (1):
                break
            # end if
            #// Scan forward to find the beginning of another run of
            #// changes. Also keep track of the corresponding point in the
            #// other file.
            #// 
            #// Throughout this code, $i and $j are adjusted together so that
            #// the first $i elements of $changed and the first $j elements of
            #// $other_changed both contain the same number of zeros (unchanged
            #// lines).
            #// 
            #// Furthermore, $j is always kept so that $j == $other_len or
            #// $other_changed[$j] == false.
            while True:
                
                if not (j < other_len and other_changed[j]):
                    break
                # end if
                j += 1
            # end while
            while True:
                
                if not (i < len and (not changed[i])):
                    break
                # end if
                assert(j < other_len and (not other_changed[j]))
                i += 1
                j += 1
                while True:
                    
                    if not (j < other_len and other_changed[j]):
                        break
                    # end if
                    j += 1
                # end while
            # end while
            if i == len:
                break
            # end if
            start = i
            #// Find the end of this run of changes.
            while True:
                
                if not (i < len and changed[i]):
                    break
                # end if
                i += 1
                continue
            # end while
            while True:
                #// Record the length of this run of changes, so that we can
                #// later determine whether the run has grown.
                runlength = i - start
                #// Move the changed region back, so long as the previous
                #// unchanged line matches the last changed one.  This merges
                #// with previous changed regions.
                while True:
                    
                    if not (start > 0 and lines[start - 1] == lines[i - 1]):
                        break
                    # end if
                    start -= 1
                    changed[start] = 1
                    i -= 1
                    changed[i] = False
                    while True:
                        
                        if not (start > 0 and changed[start - 1]):
                            break
                        # end if
                        start -= 1
                    # end while
                    assert(j > 0)
                    while True:
                        
                        if not (other_changed[j]):
                            break
                        # end if
                        j -= 1
                        continue
                    # end while
                    assert(j >= 0 and (not other_changed[j]))
                # end while
                #// Set CORRESPONDING to the end of the changed run, at the
                #// last point where it corresponds to a changed run in the
                #// other file. CORRESPONDING == LEN means no such point has
                #// been found.
                corresponding = i if j < other_len else len
                #// Move the changed region forward, so long as the first
                #// changed line matches the following unchanged one.  This
                #// merges with following changed regions.  Do this second, so
                #// that if there are no merges, the changed region is moved
                #// forward as far as possible.
                while True:
                    
                    if not (i < len and lines[start] == lines[i]):
                        break
                    # end if
                    changed[start] = False
                    start += 1
                    changed[i] = 1
                    i += 1
                    while True:
                        
                        if not (i < len and changed[i]):
                            break
                        # end if
                        i += 1
                    # end while
                    assert(j < other_len and (not other_changed[j]))
                    j += 1
                    if j < other_len and other_changed[j]:
                        corresponding = i
                        while True:
                            
                            if not (j < other_len and other_changed[j]):
                                break
                            # end if
                            j += 1
                        # end while
                    # end if
                # end while
                
                if runlength != i - start:
                    break
                # end if
            # end while
            #// If possible, move the fully-merged run of changes back to a
            #// corresponding run in the other file.
            while True:
                
                if not (corresponding < i):
                    break
                # end if
                start -= 1
                changed[start] = 1
                i -= 1
                changed[i] = 0
                assert(j > 0)
                while True:
                    
                    if not (other_changed[j]):
                        break
                    # end if
                    j -= 1
                    continue
                # end while
                assert(j >= 0 and (not other_changed[j]))
            # end while
        # end while
    # end def _shiftboundaries
    start += 1
    i += 1
# end class Text_Diff_Engine_native
