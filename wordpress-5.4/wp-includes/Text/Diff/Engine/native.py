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
    def diff(self, from_lines_=None, to_lines_=None):
        
        
        array_walk(from_lines_, Array("Text_Diff", "trimNewlines"))
        array_walk(to_lines_, Array("Text_Diff", "trimNewlines"))
        n_from_ = php_count(from_lines_)
        n_to_ = php_count(to_lines_)
        self.xchanged = self.ychanged = Array()
        self.xv = self.yv = Array()
        self.xind = self.yind = Array()
        self.seq = None
        self.in_seq = None
        self.lcs = None
        #// Skip leading common lines.
        skip_ = 0
        while skip_ < n_from_ and skip_ < n_to_:
            
            if from_lines_[skip_] != to_lines_[skip_]:
                break
            # end if
            self.xchanged[skip_] = self.ychanged[skip_] = False
            skip_ += 1
        # end while
        #// Skip trailing common lines.
        xi_ = n_from_
        yi_ = n_to_
        endskip_ = 0
        while xi_ > skip_ and yi_ > skip_:
            xi_ -= 1
            yi_ -= 1
            if from_lines_[xi_] != to_lines_[yi_]:
                xi_ -= 1
                yi_ -= 1
                break
            # end if
            self.xchanged[xi_] = self.ychanged[yi_] = False
            endskip_ += 1
        # end while
        #// Ignore lines which do not exist in both files.
        xi_ = skip_
        while xi_ < n_from_ - endskip_:
            
            xhash_[from_lines_[xi_]] = 1
            xi_ += 1
        # end while
        yi_ = skip_
        while yi_ < n_to_ - endskip_:
            
            line_ = to_lines_[yi_]
            self.ychanged[yi_] = php_empty(lambda : xhash_[line_])
            if self.ychanged[yi_]:
                continue
            # end if
            yhash_[line_] = 1
            self.yv[-1] = line_
            self.yind[-1] = yi_
            yi_ += 1
        # end while
        xi_ = skip_
        while xi_ < n_from_ - endskip_:
            
            line_ = from_lines_[xi_]
            self.xchanged[xi_] = php_empty(lambda : yhash_[line_])
            if self.xchanged[xi_]:
                continue
            # end if
            self.xv[-1] = line_
            self.xind[-1] = xi_
            xi_ += 1
        # end while
        #// Find the LCS.
        self._compareseq(0, php_count(self.xv), 0, php_count(self.yv))
        #// Merge edits when possible.
        self._shiftboundaries(from_lines_, self.xchanged, self.ychanged)
        self._shiftboundaries(to_lines_, self.ychanged, self.xchanged)
        #// Compute the edit operations.
        edits_ = Array()
        xi_ = yi_ = 0
        while True:
            
            if not (xi_ < n_from_ or yi_ < n_to_):
                break
            # end if
            assert(yi_ < n_to_ or self.xchanged[xi_])
            assert(xi_ < n_from_ or self.ychanged[yi_])
            #// Skip matching "snake".
            copy_ = Array()
            while True:
                
                if not (xi_ < n_from_ and yi_ < n_to_ and (not self.xchanged[xi_]) and (not self.ychanged[yi_])):
                    break
                # end if
                copy_[-1] = from_lines_[xi_]
                xi_ += 1
                yi_ += 1
            # end while
            if copy_:
                edits_[-1] = php_new_class("Text_Diff_Op_copy", lambda : Text_Diff_Op_copy(copy_))
            # end if
            #// Find deletes & adds.
            delete_ = Array()
            while True:
                
                if not (xi_ < n_from_ and self.xchanged[xi_]):
                    break
                # end if
                delete_[-1] = from_lines_[xi_]
                xi_ += 1
            # end while
            add_ = Array()
            while True:
                
                if not (yi_ < n_to_ and self.ychanged[yi_]):
                    break
                # end if
                add_[-1] = to_lines_[yi_]
                yi_ += 1
            # end while
            if delete_ and add_:
                edits_[-1] = php_new_class("Text_Diff_Op_change", lambda : Text_Diff_Op_change(delete_, add_))
            elif delete_:
                edits_[-1] = php_new_class("Text_Diff_Op_delete", lambda : Text_Diff_Op_delete(delete_))
            elif add_:
                edits_[-1] = php_new_class("Text_Diff_Op_add", lambda : Text_Diff_Op_add(add_))
            # end if
        # end while
        return edits_
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
    def _diag(self, xoff_=None, xlim_=None, yoff_=None, ylim_=None, nchunks_=None):
        
        
        flip_ = False
        if xlim_ - xoff_ > ylim_ - yoff_:
            #// Things seems faster (I'm not sure I understand why) when the
            #// shortest sequence is in X.
            flip_ = True
            xoff_, xlim_, yoff_, ylim_ = Array(yoff_, ylim_, xoff_, xlim_)
        # end if
        if flip_:
            i_ = ylim_ - 1
            while i_ >= yoff_:
                
                ymatches_[self.xv[i_]][-1] = i_
                i_ -= 1
            # end while
        else:
            i_ = ylim_ - 1
            while i_ >= yoff_:
                
                ymatches_[self.yv[i_]][-1] = i_
                i_ -= 1
            # end while
        # end if
        self.lcs = 0
        self.seq[0] = yoff_ - 1
        self.in_seq = Array()
        ymids_[0] = Array()
        numer_ = xlim_ - xoff_ + nchunks_ - 1
        x_ = xoff_
        chunk_ = 0
        while chunk_ < nchunks_:
            
            if chunk_ > 0:
                i_ = 0
                while i_ <= self.lcs:
                    
                    ymids_[i_][chunk_ - 1] = self.seq[i_]
                    i_ += 1
                # end while
            # end if
            x1_ = xoff_ + php_int(numer_ + xlim_ - xoff_ * chunk_ / nchunks_)
            while x_ < x1_:
                
                line_ = self.yv[x_] if flip_ else self.xv[x_]
                if php_empty(lambda : ymatches_[line_]):
                    continue
                # end if
                matches_ = ymatches_[line_]
                reset(matches_)
                while True:
                    y_ = current(matches_)
                    if not (y_):
                        break
                    # end if
                    if php_empty(lambda : self.in_seq[y_]):
                        k_ = self._lcspos(y_)
                        assert(k_ > 0)
                        ymids_[k_] = ymids_[k_ - 1]
                        break
                    # end if
                    next(matches_)
                # end while
                while True:
                    y_ = current(matches_)
                    if not (y_):
                        break
                    # end if
                    if y_ > self.seq[k_ - 1]:
                        assert(y_ <= self.seq[k_])
                        #// Optimization: this is a common case: next match is
                        #// just replacing previous match.
                        self.in_seq[self.seq[k_]] = False
                        self.seq[k_] = y_
                        self.in_seq[y_] = 1
                    elif php_empty(lambda : self.in_seq[y_]):
                        k_ = self._lcspos(y_)
                        assert(k_ > 0)
                        ymids_[k_] = ymids_[k_ - 1]
                    # end if
                    next(matches_)
                # end while
                x_ += 1
            # end while
            chunk_ += 1
        # end while
        seps_[-1] = Array(yoff_, xoff_) if flip_ else Array(xoff_, yoff_)
        ymid_ = ymids_[self.lcs]
        n_ = 0
        while n_ < nchunks_ - 1:
            
            x1_ = xoff_ + php_int(numer_ + xlim_ - xoff_ * n_ / nchunks_)
            y1_ = ymid_[n_] + 1
            seps_[-1] = Array(y1_, x1_) if flip_ else Array(x1_, y1_)
            n_ += 1
        # end while
        seps_[-1] = Array(ylim_, xlim_) if flip_ else Array(xlim_, ylim_)
        return Array(self.lcs, seps_)
    # end def _diag
    self.lcs += 1
    def _lcspos(self, ypos_=None):
        
        
        end_ = self.lcs
        if end_ == 0 or ypos_ > self.seq[end_]:
            self.lcs += 1
            self.seq[self.lcs] = ypos_
            self.in_seq[ypos_] = 1
            return self.lcs
        # end if
        beg_ = 1
        while True:
            
            if not (beg_ < end_):
                break
            # end if
            mid_ = php_int(beg_ + end_ / 2)
            if ypos_ > self.seq[mid_]:
                beg_ = mid_ + 1
            else:
                end_ = mid_
            # end if
        # end while
        assert(ypos_ != self.seq[end_])
        self.in_seq[self.seq[end_]] = False
        self.seq[end_] = ypos_
        self.in_seq[ypos_] = 1
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
    def _compareseq(self, xoff_=None, xlim_=None, yoff_=None, ylim_=None):
        
        
        #// Slide down the bottom initial diagonal.
        while True:
            
            if not (xoff_ < xlim_ and yoff_ < ylim_ and self.xv[xoff_] == self.yv[yoff_]):
                break
            # end if
            xoff_ += 1
            yoff_ += 1
        # end while
        #// Slide up the top initial diagonal.
        while True:
            
            if not (xlim_ > xoff_ and ylim_ > yoff_ and self.xv[xlim_ - 1] == self.yv[ylim_ - 1]):
                break
            # end if
            xlim_ -= 1
            ylim_ -= 1
        # end while
        if xoff_ == xlim_ or yoff_ == ylim_:
            lcs_ = 0
        else:
            #// This is ad hoc but seems to work well.  $nchunks =
            #// sqrt(min($xlim - $xoff, $ylim - $yoff) / 2.5); $nchunks =
            #// max(2,min(8,(int)$nchunks));
            nchunks_ = php_min(7, xlim_ - xoff_, ylim_ - yoff_) + 1
            lcs_, seps_ = self._diag(xoff_, xlim_, yoff_, ylim_, nchunks_)
        # end if
        if lcs_ == 0:
            #// X and Y sequences have no common subsequence: mark all
            #// changed.
            while True:
                
                if not (yoff_ < ylim_):
                    break
                # end if
                self.ychanged[self.yind[yoff_]] = 1
                yoff_ += 1
            # end while
            while True:
                
                if not (xoff_ < xlim_):
                    break
                # end if
                self.xchanged[self.xind[xoff_]] = 1
                xoff_ += 1
            # end while
        else:
            #// Use the partitions to split this problem into subproblems.
            reset(seps_)
            pt1_ = seps_[0]
            while True:
                pt2_ = next(seps_)
                if not (pt2_):
                    break
                # end if
                self._compareseq(pt1_[0], pt2_[0], pt1_[1], pt2_[1])
                pt1_ = pt2_
            # end while
        # end if
    # end def _compareseq
    yoff_ += 1
    xoff_ += 1
    start_ -= 1
    i_ -= 1
    start_ -= 1
    i_ -= 1
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
    def _shiftboundaries(self, lines_=None, changed_=None, other_changed_=None):
        
        
        i_ = 0
        j_ = 0
        assert(php_count(lines_) == php_count(changed_))
        len_ = php_count(lines_)
        other_len_ = php_count(other_changed_)
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
                
                if not (j_ < other_len_ and other_changed_[j_]):
                    break
                # end if
                j_ += 1
            # end while
            while True:
                
                if not (i_ < len_ and (not changed_[i_])):
                    break
                # end if
                assert(j_ < other_len_ and (not other_changed_[j_]))
                i_ += 1
                j_ += 1
                while True:
                    
                    if not (j_ < other_len_ and other_changed_[j_]):
                        break
                    # end if
                    j_ += 1
                # end while
            # end while
            if i_ == len_:
                break
            # end if
            start_ = i_
            #// Find the end of this run of changes.
            while True:
                i_ += 1
                if not (i_ < len_ and changed_[i_]):
                    break
                # end if
                i_ += 1
                continue
            # end while
            while True:
                #// Record the length of this run of changes, so that we can
                #// later determine whether the run has grown.
                runlength_ = i_ - start_
                #// Move the changed region back, so long as the previous
                #// unchanged line matches the last changed one.  This merges
                #// with previous changed regions.
                while True:
                    
                    if not (start_ > 0 and lines_[start_ - 1] == lines_[i_ - 1]):
                        break
                    # end if
                    start_ -= 1
                    changed_[start_] = 1
                    i_ -= 1
                    changed_[i_] = False
                    while True:
                        
                        if not (start_ > 0 and changed_[start_ - 1]):
                            break
                        # end if
                        start_ -= 1
                    # end while
                    assert(j_ > 0)
                    while True:
                        j_ -= 1
                        if not (other_changed_[j_]):
                            break
                        # end if
                        j_ -= 1
                        continue
                    # end while
                    assert(j_ >= 0 and (not other_changed_[j_]))
                # end while
                #// Set CORRESPONDING to the end of the changed run, at the
                #// last point where it corresponds to a changed run in the
                #// other file. CORRESPONDING == LEN means no such point has
                #// been found.
                corresponding_ = i_ if j_ < other_len_ else len_
                #// Move the changed region forward, so long as the first
                #// changed line matches the following unchanged one.  This
                #// merges with following changed regions.  Do this second, so
                #// that if there are no merges, the changed region is moved
                #// forward as far as possible.
                while True:
                    
                    if not (i_ < len_ and lines_[start_] == lines_[i_]):
                        break
                    # end if
                    changed_[start_] = False
                    start_ += 1
                    changed_[i_] = 1
                    i_ += 1
                    while True:
                        
                        if not (i_ < len_ and changed_[i_]):
                            break
                        # end if
                        i_ += 1
                    # end while
                    assert(j_ < other_len_ and (not other_changed_[j_]))
                    j_ += 1
                    if j_ < other_len_ and other_changed_[j_]:
                        corresponding_ = i_
                        while True:
                            
                            if not (j_ < other_len_ and other_changed_[j_]):
                                break
                            # end if
                            j_ += 1
                        # end while
                    # end if
                # end while
                
                if runlength_ != i_ - start_:
                    break
                # end if
            # end while
            #// If possible, move the fully-merged run of changes back to a
            #// corresponding run in the other file.
            while True:
                
                if not (corresponding_ < i_):
                    break
                # end if
                start_ -= 1
                changed_[start_] = 1
                i_ -= 1
                changed_[i_] = 0
                assert(j_ > 0)
                while True:
                    j_ -= 1
                    if not (other_changed_[j_]):
                        break
                    # end if
                    j_ -= 1
                    continue
                # end while
                assert(j_ >= 0 and (not other_changed_[j_]))
            # end while
        # end while
    # end def _shiftboundaries
    start_ += 1
    i_ += 1
# end class Text_Diff_Engine_native
