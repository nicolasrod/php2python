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
#// getID3() by James Heinrich <info@getid3.org>
#// available at https://github.com/JamesHeinrich/getID3
#// or https://www.getid3.org
#// or http://getid3.sourceforge.net
#// see readme.txt for more details
#// 
#// 
#// module.audio.ac3.php
#// module for analyzing AC-3 (aka Dolby Digital) audio files
#// dependencies: NONE
#// 
#//
class getid3_ac3(getid3_handler):
    AC3header = Array()
    BSIoffset = 0
    syncword = 2935
    #// 
    #// @return bool
    #//
    def analyze(self):
        
        info = self.getid3.info
        #// AH
        info["ac3"]["raw"]["bsi"] = Array()
        thisfile_ac3 = info["ac3"]
        thisfile_ac3_raw = thisfile_ac3["raw"]
        thisfile_ac3_raw_bsi = thisfile_ac3_raw["bsi"]
        #// http://www.atsc.org/standards/a_52a.pdf
        info["fileformat"] = "ac3"
        #// An AC-3 serial coded audio bit stream is made up of a sequence of synchronization frames
        #// Each synchronization frame contains 6 coded audio blocks (AB), each of which represent 256
        #// new audio samples per channel. A synchronization information (SI) header at the beginning
        #// of each frame contains information needed to acquire and maintain synchronization. A
        #// bit stream information (BSI) header follows SI, and contains parameters describing the coded
        #// audio service. The coded audio blocks may be followed by an auxiliary data (Aux) field. At the
        #// end of each frame is an error check field that includes a CRC word for error detection. An
        #// additional CRC word is located in the SI header, the use of which, by a decoder, is optional.
        #// 
        #// syncinfo() | bsi() | AB0 | AB1 | AB2 | AB3 | AB4 | AB5 | Aux | CRC
        #// syncinfo() {
        #// syncword    16
        #// crc1        16
        #// fscod        2
        #// frmsizecod   6
        #// } /* end of syncinfo
        self.fseek(info["avdataoffset"])
        tempAC3header = self.fread(100)
        #// should be enough to cover all data, there are some variable-length fields...?
        self.AC3header["syncinfo"] = getid3_lib.bigendian2int(php_substr(tempAC3header, 0, 2))
        self.AC3header["bsi"] = getid3_lib.bigendian2bin(php_substr(tempAC3header, 2))
        thisfile_ac3_raw_bsi["bsid"] = getid3_lib.littleendian2int(php_substr(tempAC3header, 5, 1)) & 248 >> 3
        tempAC3header = None
        if self.AC3header["syncinfo"] != self.syncword:
            if (not self.isdependencyfor("matroska")):
                info["fileformat"] = None
                info["ac3"] = None
                return self.error("Expecting \"" + dechex(self.syncword) + "\" at offset " + info["avdataoffset"] + ", found \"" + dechex(self.AC3header["syncinfo"]) + "\"")
            # end if
        # end if
        info["audio"]["dataformat"] = "ac3"
        info["audio"]["bitrate_mode"] = "cbr"
        info["audio"]["lossless"] = False
        if thisfile_ac3_raw_bsi["bsid"] <= 8:
            thisfile_ac3_raw_bsi["crc1"] = getid3_lib.bin2dec(self.readheaderbsi(16))
            thisfile_ac3_raw_bsi["fscod"] = self.readheaderbsi(2)
            #// 5.4.1.3
            thisfile_ac3_raw_bsi["frmsizecod"] = self.readheaderbsi(6)
            #// 5.4.1.4
            if thisfile_ac3_raw_bsi["frmsizecod"] > 37:
                #// binary: 100101 - see Table 5.18 Frame Size Code Table (1 word = 16 bits)
                self.warning("Unexpected ac3.bsi.frmsizecod value: " + thisfile_ac3_raw_bsi["frmsizecod"] + ", bitrate not set correctly")
            # end if
            thisfile_ac3_raw_bsi["bsid"] = self.readheaderbsi(5)
            #// we already know this from pre-parsing the version identifier, but re-read it to let the bitstream flow as intended
            thisfile_ac3_raw_bsi["bsmod"] = self.readheaderbsi(3)
            thisfile_ac3_raw_bsi["acmod"] = self.readheaderbsi(3)
            if thisfile_ac3_raw_bsi["acmod"] & 1:
                #// If the lsb of acmod is a 1, center channel is in use and cmixlev follows in the bit stream.
                thisfile_ac3_raw_bsi["cmixlev"] = self.readheaderbsi(2)
                thisfile_ac3["center_mix_level"] = self.centermixlevellookup(thisfile_ac3_raw_bsi["cmixlev"])
            # end if
            if thisfile_ac3_raw_bsi["acmod"] & 4:
                #// If the msb of acmod is a 1, surround channels are in use and surmixlev follows in the bit stream.
                thisfile_ac3_raw_bsi["surmixlev"] = self.readheaderbsi(2)
                thisfile_ac3["surround_mix_level"] = self.surroundmixlevellookup(thisfile_ac3_raw_bsi["surmixlev"])
            # end if
            if thisfile_ac3_raw_bsi["acmod"] == 2:
                #// When operating in the two channel mode, this 2-bit code indicates whether or not the program has been encoded in Dolby Surround.
                thisfile_ac3_raw_bsi["dsurmod"] = self.readheaderbsi(2)
                thisfile_ac3["dolby_surround_mode"] = self.dolbysurroundmodelookup(thisfile_ac3_raw_bsi["dsurmod"])
            # end if
            thisfile_ac3_raw_bsi["flags"]["lfeon"] = bool(self.readheaderbsi(1))
            #// This indicates how far the average dialogue level is below digital 100 percent. Valid values are 1-31.
            #// The value of 0 is reserved. The values of 1 to 31 are interpreted as -1 dB to -31 dB with respect to digital 100 percent.
            thisfile_ac3_raw_bsi["dialnorm"] = self.readheaderbsi(5)
            #// 5.4.2.8 dialnorm: Dialogue Normalization, 5 Bits
            thisfile_ac3_raw_bsi["flags"]["compr"] = bool(self.readheaderbsi(1))
            #// 5.4.2.9 compre: Compression Gain Word Exists, 1 Bit
            if thisfile_ac3_raw_bsi["flags"]["compr"]:
                thisfile_ac3_raw_bsi["compr"] = self.readheaderbsi(8)
                #// 5.4.2.10 compr: Compression Gain Word, 8 Bits
                thisfile_ac3["heavy_compression"] = self.heavycompression(thisfile_ac3_raw_bsi["compr"])
            # end if
            thisfile_ac3_raw_bsi["flags"]["langcod"] = bool(self.readheaderbsi(1))
            #// 5.4.2.11 langcode: Language Code Exists, 1 Bit
            if thisfile_ac3_raw_bsi["flags"]["langcod"]:
                thisfile_ac3_raw_bsi["langcod"] = self.readheaderbsi(8)
                pass
            # end if
            thisfile_ac3_raw_bsi["flags"]["audprodinfo"] = bool(self.readheaderbsi(1))
            #// 5.4.2.13 audprodie: Audio Production Information Exists, 1 Bit
            if thisfile_ac3_raw_bsi["flags"]["audprodinfo"]:
                thisfile_ac3_raw_bsi["mixlevel"] = self.readheaderbsi(5)
                #// 5.4.2.14 mixlevel: Mixing Level, 5 Bits
                thisfile_ac3_raw_bsi["roomtyp"] = self.readheaderbsi(2)
                #// 5.4.2.15 roomtyp: Room Type, 2 Bits
                thisfile_ac3["mixing_level"] = 80 + thisfile_ac3_raw_bsi["mixlevel"] + "dB"
                thisfile_ac3["room_type"] = self.roomtypelookup(thisfile_ac3_raw_bsi["roomtyp"])
            # end if
            thisfile_ac3_raw_bsi["dialnorm2"] = self.readheaderbsi(5)
            #// 5.4.2.16 dialnorm2: Dialogue Normalization, ch2, 5 Bits
            thisfile_ac3["dialogue_normalization2"] = "-" + thisfile_ac3_raw_bsi["dialnorm2"] + "dB"
            #// This indicates how far the average dialogue level is below digital 100 percent. Valid values are 1-31. The value of 0 is reserved. The values of 1 to 31 are interpreted as -1 dB to -31 dB with respect to digital 100 percent.
            thisfile_ac3_raw_bsi["flags"]["compr2"] = bool(self.readheaderbsi(1))
            #// 5.4.2.17 compr2e: Compression Gain Word Exists, ch2, 1 Bit
            if thisfile_ac3_raw_bsi["flags"]["compr2"]:
                thisfile_ac3_raw_bsi["compr2"] = self.readheaderbsi(8)
                #// 5.4.2.18 compr2: Compression Gain Word, ch2, 8 Bits
                thisfile_ac3["heavy_compression2"] = self.heavycompression(thisfile_ac3_raw_bsi["compr2"])
            # end if
            thisfile_ac3_raw_bsi["flags"]["langcod2"] = bool(self.readheaderbsi(1))
            #// 5.4.2.19 langcod2e: Language Code Exists, ch2, 1 Bit
            if thisfile_ac3_raw_bsi["flags"]["langcod2"]:
                thisfile_ac3_raw_bsi["langcod2"] = self.readheaderbsi(8)
                pass
            # end if
            thisfile_ac3_raw_bsi["flags"]["audprodinfo2"] = bool(self.readheaderbsi(1))
            #// 5.4.2.21 audprodi2e: Audio Production Information Exists, ch2, 1 Bit
            if thisfile_ac3_raw_bsi["flags"]["audprodinfo2"]:
                thisfile_ac3_raw_bsi["mixlevel2"] = self.readheaderbsi(5)
                #// 5.4.2.22 mixlevel2: Mixing Level, ch2, 5 Bits
                thisfile_ac3_raw_bsi["roomtyp2"] = self.readheaderbsi(2)
                #// 5.4.2.23 roomtyp2: Room Type, ch2, 2 Bits
                thisfile_ac3["mixing_level2"] = 80 + thisfile_ac3_raw_bsi["mixlevel2"] + "dB"
                thisfile_ac3["room_type2"] = self.roomtypelookup(thisfile_ac3_raw_bsi["roomtyp2"])
            # end if
            thisfile_ac3_raw_bsi["copyright"] = bool(self.readheaderbsi(1))
            #// 5.4.2.24 copyrightb: Copyright Bit, 1 Bit
            thisfile_ac3_raw_bsi["original"] = bool(self.readheaderbsi(1))
            #// 5.4.2.25 origbs: Original Bit Stream, 1 Bit
            thisfile_ac3_raw_bsi["flags"]["timecod1"] = self.readheaderbsi(2)
            #// 5.4.2.26 timecod1e, timcode2e: Time Code (first and second) Halves Exist, 2 Bits
            if thisfile_ac3_raw_bsi["flags"]["timecod1"] & 1:
                thisfile_ac3_raw_bsi["timecod1"] = self.readheaderbsi(14)
                #// 5.4.2.27 timecod1: Time code first half, 14 bits
                thisfile_ac3["timecode1"] = 0
                thisfile_ac3["timecode1"] += thisfile_ac3_raw_bsi["timecod1"] & 15872 >> 9 * 3600
                #// The first 5 bits of this 14-bit field represent the time in hours, with valid values of 0�23
                thisfile_ac3["timecode1"] += thisfile_ac3_raw_bsi["timecod1"] & 504 >> 3 * 60
                #// The next 6 bits represent the time in minutes, with valid values of 0�59
                thisfile_ac3["timecode1"] += thisfile_ac3_raw_bsi["timecod1"] & 3 >> 0 * 8
                pass
            # end if
            if thisfile_ac3_raw_bsi["flags"]["timecod1"] & 2:
                thisfile_ac3_raw_bsi["timecod2"] = self.readheaderbsi(14)
                #// 5.4.2.28 timecod2: Time code second half, 14 bits
                thisfile_ac3["timecode2"] = 0
                thisfile_ac3["timecode2"] += thisfile_ac3_raw_bsi["timecod2"] & 14336 >> 11 * 1
                #// The first 3 bits of this 14-bit field represent the time in seconds, with valid values from 0�7 (representing 0-7 seconds)
                thisfile_ac3["timecode2"] += thisfile_ac3_raw_bsi["timecod2"] & 1984 >> 6 * 1 / 30
                #// The next 5 bits represents the time in frames, with valid values from 0�29 (one frame = 1/30th of a second)
                thisfile_ac3["timecode2"] += thisfile_ac3_raw_bsi["timecod2"] & 63 >> 0 * 1 / 30 / 60
                pass
            # end if
            thisfile_ac3_raw_bsi["flags"]["addbsi"] = bool(self.readheaderbsi(1))
            if thisfile_ac3_raw_bsi["flags"]["addbsi"]:
                thisfile_ac3_raw_bsi["addbsi_length"] = self.readheaderbsi(6) + 1
                #// This 6-bit code, which exists only if addbside is a 1, indicates the length in bytes of additional bit stream information. The valid range of addbsil is 0�63, indicating 1�64 additional bytes, respectively.
                self.AC3header["bsi"] += getid3_lib.bigendian2bin(self.fread(thisfile_ac3_raw_bsi["addbsi_length"]))
                thisfile_ac3_raw_bsi["addbsi_data"] = php_substr(self.AC3header["bsi"], self.BSIoffset, thisfile_ac3_raw_bsi["addbsi_length"] * 8)
                self.BSIoffset += thisfile_ac3_raw_bsi["addbsi_length"] * 8
            # end if
        elif thisfile_ac3_raw_bsi["bsid"] <= 16:
            #// E-AC3
            self.error("E-AC3 parsing is incomplete and experimental in this version of getID3 (" + self.getid3.version() + "). Notably the bitrate calculations are wrong -- value might (or not) be correct, but it is not calculated correctly. Email info@getid3.org if you know how to calculate EAC3 bitrate correctly.")
            info["audio"]["dataformat"] = "eac3"
            thisfile_ac3_raw_bsi["strmtyp"] = self.readheaderbsi(2)
            thisfile_ac3_raw_bsi["substreamid"] = self.readheaderbsi(3)
            thisfile_ac3_raw_bsi["frmsiz"] = self.readheaderbsi(11)
            thisfile_ac3_raw_bsi["fscod"] = self.readheaderbsi(2)
            if thisfile_ac3_raw_bsi["fscod"] == 3:
                thisfile_ac3_raw_bsi["fscod2"] = self.readheaderbsi(2)
                thisfile_ac3_raw_bsi["numblkscod"] = 3
                pass
            else:
                thisfile_ac3_raw_bsi["numblkscod"] = self.readheaderbsi(2)
            # end if
            thisfile_ac3["bsi"]["blocks_per_sync_frame"] = self.blockspersyncframe(thisfile_ac3_raw_bsi["numblkscod"])
            thisfile_ac3_raw_bsi["acmod"] = self.readheaderbsi(3)
            thisfile_ac3_raw_bsi["flags"]["lfeon"] = bool(self.readheaderbsi(1))
            thisfile_ac3_raw_bsi["bsid"] = self.readheaderbsi(5)
            #// we already know this from pre-parsing the version identifier, but re-read it to let the bitstream flow as intended
            thisfile_ac3_raw_bsi["dialnorm"] = self.readheaderbsi(5)
            thisfile_ac3_raw_bsi["flags"]["compr"] = bool(self.readheaderbsi(1))
            if thisfile_ac3_raw_bsi["flags"]["compr"]:
                thisfile_ac3_raw_bsi["compr"] = self.readheaderbsi(8)
            # end if
            if thisfile_ac3_raw_bsi["acmod"] == 0:
                #// if 1+1 mode (dual mono, so some items need a second value)
                thisfile_ac3_raw_bsi["dialnorm2"] = self.readheaderbsi(5)
                thisfile_ac3_raw_bsi["flags"]["compr2"] = bool(self.readheaderbsi(1))
                if thisfile_ac3_raw_bsi["flags"]["compr2"]:
                    thisfile_ac3_raw_bsi["compr2"] = self.readheaderbsi(8)
                # end if
            # end if
            if thisfile_ac3_raw_bsi["strmtyp"] == 1:
                #// if dependent stream
                thisfile_ac3_raw_bsi["flags"]["chanmap"] = bool(self.readheaderbsi(1))
                if thisfile_ac3_raw_bsi["flags"]["chanmap"]:
                    thisfile_ac3_raw_bsi["chanmap"] = self.readheaderbsi(8)
                # end if
            # end if
            thisfile_ac3_raw_bsi["flags"]["mixmdat"] = bool(self.readheaderbsi(1))
            if thisfile_ac3_raw_bsi["flags"]["mixmdat"]:
                #// Mixing metadata
                if thisfile_ac3_raw_bsi["acmod"] > 2:
                    #// if more than 2 channels
                    thisfile_ac3_raw_bsi["dmixmod"] = self.readheaderbsi(2)
                # end if
                if thisfile_ac3_raw_bsi["acmod"] & 1 and thisfile_ac3_raw_bsi["acmod"] > 2:
                    #// if three front channels exist
                    thisfile_ac3_raw_bsi["ltrtcmixlev"] = self.readheaderbsi(3)
                    thisfile_ac3_raw_bsi["lorocmixlev"] = self.readheaderbsi(3)
                # end if
                if thisfile_ac3_raw_bsi["acmod"] & 4:
                    #// if a surround channel exists
                    thisfile_ac3_raw_bsi["ltrtsurmixlev"] = self.readheaderbsi(3)
                    thisfile_ac3_raw_bsi["lorosurmixlev"] = self.readheaderbsi(3)
                # end if
                if thisfile_ac3_raw_bsi["flags"]["lfeon"]:
                    #// if the LFE channel exists
                    thisfile_ac3_raw_bsi["flags"]["lfemixlevcod"] = bool(self.readheaderbsi(1))
                    if thisfile_ac3_raw_bsi["flags"]["lfemixlevcod"]:
                        thisfile_ac3_raw_bsi["lfemixlevcod"] = self.readheaderbsi(5)
                    # end if
                # end if
                if thisfile_ac3_raw_bsi["strmtyp"] == 0:
                    #// if independent stream
                    thisfile_ac3_raw_bsi["flags"]["pgmscl"] = bool(self.readheaderbsi(1))
                    if thisfile_ac3_raw_bsi["flags"]["pgmscl"]:
                        thisfile_ac3_raw_bsi["pgmscl"] = self.readheaderbsi(6)
                    # end if
                    if thisfile_ac3_raw_bsi["acmod"] == 0:
                        #// if 1+1 mode (dual mono, so some items need a second value)
                        thisfile_ac3_raw_bsi["flags"]["pgmscl2"] = bool(self.readheaderbsi(1))
                        if thisfile_ac3_raw_bsi["flags"]["pgmscl2"]:
                            thisfile_ac3_raw_bsi["pgmscl2"] = self.readheaderbsi(6)
                        # end if
                    # end if
                    thisfile_ac3_raw_bsi["flags"]["extpgmscl"] = bool(self.readheaderbsi(1))
                    if thisfile_ac3_raw_bsi["flags"]["extpgmscl"]:
                        thisfile_ac3_raw_bsi["extpgmscl"] = self.readheaderbsi(6)
                    # end if
                    thisfile_ac3_raw_bsi["mixdef"] = self.readheaderbsi(2)
                    if thisfile_ac3_raw_bsi["mixdef"] == 1:
                        #// mixing option 2
                        thisfile_ac3_raw_bsi["premixcmpsel"] = bool(self.readheaderbsi(1))
                        thisfile_ac3_raw_bsi["drcsrc"] = bool(self.readheaderbsi(1))
                        thisfile_ac3_raw_bsi["premixcmpscl"] = self.readheaderbsi(3)
                    elif thisfile_ac3_raw_bsi["mixdef"] == 2:
                        #// mixing option 3
                        thisfile_ac3_raw_bsi["mixdata"] = self.readheaderbsi(12)
                    elif thisfile_ac3_raw_bsi["mixdef"] == 3:
                        #// mixing option 4
                        mixdefbitsread = 0
                        thisfile_ac3_raw_bsi["mixdeflen"] = self.readheaderbsi(5)
                        mixdefbitsread += 5
                        thisfile_ac3_raw_bsi["flags"]["mixdata2"] = bool(self.readheaderbsi(1))
                        mixdefbitsread += 1
                        if thisfile_ac3_raw_bsi["flags"]["mixdata2"]:
                            thisfile_ac3_raw_bsi["premixcmpsel"] = bool(self.readheaderbsi(1))
                            mixdefbitsread += 1
                            thisfile_ac3_raw_bsi["drcsrc"] = bool(self.readheaderbsi(1))
                            mixdefbitsread += 1
                            thisfile_ac3_raw_bsi["premixcmpscl"] = self.readheaderbsi(3)
                            mixdefbitsread += 3
                            thisfile_ac3_raw_bsi["flags"]["extpgmlscl"] = bool(self.readheaderbsi(1))
                            mixdefbitsread += 1
                            if thisfile_ac3_raw_bsi["flags"]["extpgmlscl"]:
                                thisfile_ac3_raw_bsi["extpgmlscl"] = self.readheaderbsi(4)
                                mixdefbitsread += 4
                            # end if
                            thisfile_ac3_raw_bsi["flags"]["extpgmcscl"] = bool(self.readheaderbsi(1))
                            mixdefbitsread += 1
                            if thisfile_ac3_raw_bsi["flags"]["extpgmcscl"]:
                                thisfile_ac3_raw_bsi["extpgmcscl"] = self.readheaderbsi(4)
                                mixdefbitsread += 4
                            # end if
                            thisfile_ac3_raw_bsi["flags"]["extpgmrscl"] = bool(self.readheaderbsi(1))
                            mixdefbitsread += 1
                            if thisfile_ac3_raw_bsi["flags"]["extpgmrscl"]:
                                thisfile_ac3_raw_bsi["extpgmrscl"] = self.readheaderbsi(4)
                            # end if
                            thisfile_ac3_raw_bsi["flags"]["extpgmlsscl"] = bool(self.readheaderbsi(1))
                            mixdefbitsread += 1
                            if thisfile_ac3_raw_bsi["flags"]["extpgmlsscl"]:
                                thisfile_ac3_raw_bsi["extpgmlsscl"] = self.readheaderbsi(4)
                                mixdefbitsread += 4
                            # end if
                            thisfile_ac3_raw_bsi["flags"]["extpgmrsscl"] = bool(self.readheaderbsi(1))
                            mixdefbitsread += 1
                            if thisfile_ac3_raw_bsi["flags"]["extpgmrsscl"]:
                                thisfile_ac3_raw_bsi["extpgmrsscl"] = self.readheaderbsi(4)
                                mixdefbitsread += 4
                            # end if
                            thisfile_ac3_raw_bsi["flags"]["extpgmlfescl"] = bool(self.readheaderbsi(1))
                            mixdefbitsread += 1
                            if thisfile_ac3_raw_bsi["flags"]["extpgmlfescl"]:
                                thisfile_ac3_raw_bsi["extpgmlfescl"] = self.readheaderbsi(4)
                                mixdefbitsread += 4
                            # end if
                            thisfile_ac3_raw_bsi["flags"]["dmixscl"] = bool(self.readheaderbsi(1))
                            mixdefbitsread += 1
                            if thisfile_ac3_raw_bsi["flags"]["dmixscl"]:
                                thisfile_ac3_raw_bsi["dmixscl"] = self.readheaderbsi(4)
                                mixdefbitsread += 4
                            # end if
                            thisfile_ac3_raw_bsi["flags"]["addch"] = bool(self.readheaderbsi(1))
                            mixdefbitsread += 1
                            if thisfile_ac3_raw_bsi["flags"]["addch"]:
                                thisfile_ac3_raw_bsi["flags"]["extpgmaux1scl"] = bool(self.readheaderbsi(1))
                                mixdefbitsread += 1
                                if thisfile_ac3_raw_bsi["flags"]["extpgmaux1scl"]:
                                    thisfile_ac3_raw_bsi["extpgmaux1scl"] = self.readheaderbsi(4)
                                    mixdefbitsread += 4
                                # end if
                                thisfile_ac3_raw_bsi["flags"]["extpgmaux2scl"] = bool(self.readheaderbsi(1))
                                mixdefbitsread += 1
                                if thisfile_ac3_raw_bsi["flags"]["extpgmaux2scl"]:
                                    thisfile_ac3_raw_bsi["extpgmaux2scl"] = self.readheaderbsi(4)
                                    mixdefbitsread += 4
                                # end if
                            # end if
                        # end if
                        thisfile_ac3_raw_bsi["flags"]["mixdata3"] = bool(self.readheaderbsi(1))
                        mixdefbitsread += 1
                        if thisfile_ac3_raw_bsi["flags"]["mixdata3"]:
                            thisfile_ac3_raw_bsi["spchdat"] = self.readheaderbsi(5)
                            mixdefbitsread += 5
                            thisfile_ac3_raw_bsi["flags"]["addspchdat"] = bool(self.readheaderbsi(1))
                            mixdefbitsread += 1
                            if thisfile_ac3_raw_bsi["flags"]["addspchdat"]:
                                thisfile_ac3_raw_bsi["spchdat1"] = self.readheaderbsi(5)
                                mixdefbitsread += 5
                                thisfile_ac3_raw_bsi["spchan1att"] = self.readheaderbsi(2)
                                mixdefbitsread += 2
                                thisfile_ac3_raw_bsi["flags"]["addspchdat1"] = bool(self.readheaderbsi(1))
                                mixdefbitsread += 1
                                if thisfile_ac3_raw_bsi["flags"]["addspchdat1"]:
                                    thisfile_ac3_raw_bsi["spchdat2"] = self.readheaderbsi(5)
                                    mixdefbitsread += 5
                                    thisfile_ac3_raw_bsi["spchan2att"] = self.readheaderbsi(3)
                                    mixdefbitsread += 3
                                # end if
                            # end if
                        # end if
                        mixdata_bits = 8 * thisfile_ac3_raw_bsi["mixdeflen"] + 2 - mixdefbitsread
                        mixdata_fill = 8 - mixdata_bits % 8 if mixdata_bits % 8 else 0
                        thisfile_ac3_raw_bsi["mixdata"] = self.readheaderbsi(mixdata_bits)
                        thisfile_ac3_raw_bsi["mixdatafill"] = self.readheaderbsi(mixdata_fill)
                        mixdefbitsread = None
                        mixdata_bits = None
                        mixdata_fill = None
                    # end if
                    if thisfile_ac3_raw_bsi["acmod"] < 2:
                        #// if mono or dual mono source
                        thisfile_ac3_raw_bsi["flags"]["paninfo"] = bool(self.readheaderbsi(1))
                        if thisfile_ac3_raw_bsi["flags"]["paninfo"]:
                            thisfile_ac3_raw_bsi["panmean"] = self.readheaderbsi(8)
                            thisfile_ac3_raw_bsi["paninfo"] = self.readheaderbsi(6)
                        # end if
                        if thisfile_ac3_raw_bsi["acmod"] == 0:
                            #// if 1+1 mode (dual mono, so some items need a second value)
                            thisfile_ac3_raw_bsi["flags"]["paninfo2"] = bool(self.readheaderbsi(1))
                            if thisfile_ac3_raw_bsi["flags"]["paninfo2"]:
                                thisfile_ac3_raw_bsi["panmean2"] = self.readheaderbsi(8)
                                thisfile_ac3_raw_bsi["paninfo2"] = self.readheaderbsi(6)
                            # end if
                        # end if
                    # end if
                    thisfile_ac3_raw_bsi["flags"]["frmmixcfginfo"] = bool(self.readheaderbsi(1))
                    if thisfile_ac3_raw_bsi["flags"]["frmmixcfginfo"]:
                        #// mixing configuration information
                        if thisfile_ac3_raw_bsi["numblkscod"] == 0:
                            thisfile_ac3_raw_bsi["blkmixcfginfo"][0] = self.readheaderbsi(5)
                        else:
                            blk = 0
                            while blk < thisfile_ac3_raw_bsi["numblkscod"]:
                                
                                thisfile_ac3_raw_bsi["flags"]["blkmixcfginfo" + blk] = bool(self.readheaderbsi(1))
                                if thisfile_ac3_raw_bsi["flags"]["blkmixcfginfo" + blk]:
                                    #// mixing configuration information
                                    thisfile_ac3_raw_bsi["blkmixcfginfo"][blk] = self.readheaderbsi(5)
                                # end if
                                blk += 1
                            # end while
                        # end if
                    # end if
                # end if
            # end if
            thisfile_ac3_raw_bsi["flags"]["infomdat"] = bool(self.readheaderbsi(1))
            if thisfile_ac3_raw_bsi["flags"]["infomdat"]:
                #// Informational metadata
                thisfile_ac3_raw_bsi["bsmod"] = self.readheaderbsi(3)
                thisfile_ac3_raw_bsi["flags"]["copyrightb"] = bool(self.readheaderbsi(1))
                thisfile_ac3_raw_bsi["flags"]["origbs"] = bool(self.readheaderbsi(1))
                if thisfile_ac3_raw_bsi["acmod"] == 2:
                    #// if in 2/0 mode
                    thisfile_ac3_raw_bsi["dsurmod"] = self.readheaderbsi(2)
                    thisfile_ac3_raw_bsi["dheadphonmod"] = self.readheaderbsi(2)
                # end if
                if thisfile_ac3_raw_bsi["acmod"] >= 6:
                    #// if both surround channels exist
                    thisfile_ac3_raw_bsi["dsurexmod"] = self.readheaderbsi(2)
                # end if
                thisfile_ac3_raw_bsi["flags"]["audprodi"] = bool(self.readheaderbsi(1))
                if thisfile_ac3_raw_bsi["flags"]["audprodi"]:
                    thisfile_ac3_raw_bsi["mixlevel"] = self.readheaderbsi(5)
                    thisfile_ac3_raw_bsi["roomtyp"] = self.readheaderbsi(2)
                    thisfile_ac3_raw_bsi["flags"]["adconvtyp"] = bool(self.readheaderbsi(1))
                # end if
                if thisfile_ac3_raw_bsi["acmod"] == 0:
                    #// if 1+1 mode (dual mono, so some items need a second value)
                    thisfile_ac3_raw_bsi["flags"]["audprodi2"] = bool(self.readheaderbsi(1))
                    if thisfile_ac3_raw_bsi["flags"]["audprodi2"]:
                        thisfile_ac3_raw_bsi["mixlevel2"] = self.readheaderbsi(5)
                        thisfile_ac3_raw_bsi["roomtyp2"] = self.readheaderbsi(2)
                        thisfile_ac3_raw_bsi["flags"]["adconvtyp2"] = bool(self.readheaderbsi(1))
                    # end if
                # end if
                if thisfile_ac3_raw_bsi["fscod"] < 3:
                    #// if not half sample rate
                    thisfile_ac3_raw_bsi["flags"]["sourcefscod"] = bool(self.readheaderbsi(1))
                # end if
            # end if
            if thisfile_ac3_raw_bsi["strmtyp"] == 0 and thisfile_ac3_raw_bsi["numblkscod"] != 3:
                #// if both surround channels exist
                thisfile_ac3_raw_bsi["flags"]["convsync"] = bool(self.readheaderbsi(1))
            # end if
            if thisfile_ac3_raw_bsi["strmtyp"] == 2:
                #// if bit stream converted from AC-3
                if thisfile_ac3_raw_bsi["numblkscod"] != 3:
                    #// 6 blocks per syncframe
                    thisfile_ac3_raw_bsi["flags"]["blkid"] = 1
                else:
                    thisfile_ac3_raw_bsi["flags"]["blkid"] = bool(self.readheaderbsi(1))
                # end if
                if thisfile_ac3_raw_bsi["flags"]["blkid"]:
                    thisfile_ac3_raw_bsi["frmsizecod"] = self.readheaderbsi(6)
                # end if
            # end if
            thisfile_ac3_raw_bsi["flags"]["addbsi"] = bool(self.readheaderbsi(1))
            if thisfile_ac3_raw_bsi["flags"]["addbsi"]:
                thisfile_ac3_raw_bsi["addbsil"] = self.readheaderbsi(6)
                thisfile_ac3_raw_bsi["addbsi"] = self.readheaderbsi(thisfile_ac3_raw_bsi["addbsil"] + 1 * 8)
            # end if
        else:
            self.error("Bit stream identification is version " + thisfile_ac3_raw_bsi["bsid"] + ", but getID3() only understands up to version 16. Please submit a support ticket with a sample file.")
            info["ac3"] = None
            return False
        # end if
        if (php_isset(lambda : thisfile_ac3_raw_bsi["fscod2"])):
            thisfile_ac3["sample_rate"] = self.sampleratecodelookup2(thisfile_ac3_raw_bsi["fscod2"])
        else:
            thisfile_ac3["sample_rate"] = self.sampleratecodelookup(thisfile_ac3_raw_bsi["fscod"])
        # end if
        if thisfile_ac3_raw_bsi["fscod"] <= 3:
            info["audio"]["sample_rate"] = thisfile_ac3["sample_rate"]
        else:
            self.warning("Unexpected ac3.bsi.fscod value: " + thisfile_ac3_raw_bsi["fscod"])
        # end if
        if (php_isset(lambda : thisfile_ac3_raw_bsi["frmsizecod"])):
            thisfile_ac3["frame_length"] = self.framesizelookup(thisfile_ac3_raw_bsi["frmsizecod"], thisfile_ac3_raw_bsi["fscod"])
            thisfile_ac3["bitrate"] = self.bitratelookup(thisfile_ac3_raw_bsi["frmsizecod"])
        elif (not php_empty(lambda : thisfile_ac3_raw_bsi["frmsiz"])):
            #// this isn't right, but it's (usually) close, roughly 5% less than it should be.
            #// but WHERE is the actual bitrate value stored in EAC3?? email info@getid3.org if you know!
            thisfile_ac3["bitrate"] = thisfile_ac3_raw_bsi["frmsiz"] + 1 * 16 * 30
            #// The frmsiz field shall contain a value one less than the overall size of the coded syncframe in 16-bit words. That is, this field may assume a value ranging from 0 to 2047, and these values correspond to syncframe sizes ranging from 1 to 2048.
            #// kludge-fix to make it approximately the expected value, still not "right":
            thisfile_ac3["bitrate"] = round(thisfile_ac3["bitrate"] * 1.05 / 16000) * 16000
        # end if
        info["audio"]["bitrate"] = thisfile_ac3["bitrate"]
        if (php_isset(lambda : thisfile_ac3_raw_bsi["bsmod"])) and (php_isset(lambda : thisfile_ac3_raw_bsi["acmod"])):
            thisfile_ac3["service_type"] = self.servicetypelookup(thisfile_ac3_raw_bsi["bsmod"], thisfile_ac3_raw_bsi["acmod"])
        # end if
        ac3_coding_mode = self.audiocodingmodelookup(thisfile_ac3_raw_bsi["acmod"])
        for key,value in ac3_coding_mode:
            thisfile_ac3[key] = value
        # end for
        for case in Switch(thisfile_ac3_raw_bsi["acmod"]):
            if case(0):
                pass
            # end if
            if case(1):
                info["audio"]["channelmode"] = "mono"
                break
            # end if
            if case(3):
                pass
            # end if
            if case(4):
                info["audio"]["channelmode"] = "stereo"
                break
            # end if
            if case():
                info["audio"]["channelmode"] = "surround"
                break
            # end if
        # end for
        info["audio"]["channels"] = thisfile_ac3["num_channels"]
        thisfile_ac3["lfe_enabled"] = thisfile_ac3_raw_bsi["flags"]["lfeon"]
        if thisfile_ac3_raw_bsi["flags"]["lfeon"]:
            info["audio"]["channels"] += ".1"
        # end if
        thisfile_ac3["channels_enabled"] = self.channelsenabledlookup(thisfile_ac3_raw_bsi["acmod"], thisfile_ac3_raw_bsi["flags"]["lfeon"])
        thisfile_ac3["dialogue_normalization"] = "-" + thisfile_ac3_raw_bsi["dialnorm"] + "dB"
        return True
    # end def analyze
    #// 
    #// @param int $length
    #// 
    #// @return float|int
    #//
    def readheaderbsi(self, length=None):
        
        data = php_substr(self.AC3header["bsi"], self.BSIoffset, length)
        self.BSIoffset += length
        return bindec(data)
    # end def readheaderbsi
    #// 
    #// @param int $fscod
    #// 
    #// @return int|string|false
    #//
    @classmethod
    def sampleratecodelookup(self, fscod=None):
        
        sampleRateCodeLookup = Array({0: 48000, 1: 44100, 2: 32000, 3: "reserved"})
        return sampleRateCodeLookup[fscod] if (php_isset(lambda : sampleRateCodeLookup[fscod])) else False
    # end def sampleratecodelookup
    #// 
    #// @param int $fscod2
    #// 
    #// @return int|string|false
    #//
    @classmethod
    def sampleratecodelookup2(self, fscod2=None):
        
        sampleRateCodeLookup2 = Array({0: 24000, 1: 22050, 2: 16000, 3: "reserved"})
        return sampleRateCodeLookup2[fscod2] if (php_isset(lambda : sampleRateCodeLookup2[fscod2])) else False
    # end def sampleratecodelookup2
    #// 
    #// @param int $bsmod
    #// @param int $acmod
    #// 
    #// @return string|false
    #//
    @classmethod
    def servicetypelookup(self, bsmod=None, acmod=None):
        
        serviceTypeLookup = Array()
        if php_empty(lambda : serviceTypeLookup):
            i = 0
            while i <= 7:
                
                serviceTypeLookup[0][i] = "main audio service: complete main (CM)"
                serviceTypeLookup[1][i] = "main audio service: music and effects (ME)"
                serviceTypeLookup[2][i] = "associated service: visually impaired (VI)"
                serviceTypeLookup[3][i] = "associated service: hearing impaired (HI)"
                serviceTypeLookup[4][i] = "associated service: dialogue (D)"
                serviceTypeLookup[5][i] = "associated service: commentary (C)"
                serviceTypeLookup[6][i] = "associated service: emergency (E)"
                i += 1
            # end while
            serviceTypeLookup[7][1] = "associated service: voice over (VO)"
            i = 2
            while i <= 7:
                
                serviceTypeLookup[7][i] = "main audio service: karaoke"
                i += 1
            # end while
        # end if
        return serviceTypeLookup[bsmod][acmod] if (php_isset(lambda : serviceTypeLookup[bsmod][acmod])) else False
    # end def servicetypelookup
    #// 
    #// @param int $acmod
    #// 
    #// @return array|false
    #//
    @classmethod
    def audiocodingmodelookup(self, acmod=None):
        
        audioCodingModeLookup = Array({0: Array({"channel_config": "1+1", "num_channels": 2, "channel_order": "Ch1,Ch2"})}, {1: Array({"channel_config": "1/0", "num_channels": 1, "channel_order": "C"})}, {2: Array({"channel_config": "2/0", "num_channels": 2, "channel_order": "L,R"})}, {3: Array({"channel_config": "3/0", "num_channels": 3, "channel_order": "L,C,R"})}, {4: Array({"channel_config": "2/1", "num_channels": 3, "channel_order": "L,R,S"})}, {5: Array({"channel_config": "3/1", "num_channels": 4, "channel_order": "L,C,R,S"})}, {6: Array({"channel_config": "2/2", "num_channels": 4, "channel_order": "L,R,SL,SR"})}, {7: Array({"channel_config": "3/2", "num_channels": 5, "channel_order": "L,C,R,SL,SR"})})
        return audioCodingModeLookup[acmod] if (php_isset(lambda : audioCodingModeLookup[acmod])) else False
    # end def audiocodingmodelookup
    #// 
    #// @param int $cmixlev
    #// 
    #// @return int|float|string|false
    #//
    @classmethod
    def centermixlevellookup(self, cmixlev=None):
        
        centerMixLevelLookup = None
        if php_empty(lambda : centerMixLevelLookup):
            centerMixLevelLookup = Array({0: pow(2, -3 / 6), 1: pow(2, -4.5 / 6), 2: pow(2, -6 / 6), 3: "reserved"})
        # end if
        return centerMixLevelLookup[cmixlev] if (php_isset(lambda : centerMixLevelLookup[cmixlev])) else False
    # end def centermixlevellookup
    #// 
    #// @param int $surmixlev
    #// 
    #// @return int|float|string|false
    #//
    @classmethod
    def surroundmixlevellookup(self, surmixlev=None):
        
        surroundMixLevelLookup = None
        if php_empty(lambda : surroundMixLevelLookup):
            surroundMixLevelLookup = Array({0: pow(2, -3 / 6), 1: pow(2, -6 / 6), 2: 0, 3: "reserved"})
        # end if
        return surroundMixLevelLookup[surmixlev] if (php_isset(lambda : surroundMixLevelLookup[surmixlev])) else False
    # end def surroundmixlevellookup
    #// 
    #// @param int $dsurmod
    #// 
    #// @return string|false
    #//
    @classmethod
    def dolbysurroundmodelookup(self, dsurmod=None):
        
        dolbySurroundModeLookup = Array({0: "not indicated", 1: "Not Dolby Surround encoded", 2: "Dolby Surround encoded", 3: "reserved"})
        return dolbySurroundModeLookup[dsurmod] if (php_isset(lambda : dolbySurroundModeLookup[dsurmod])) else False
    # end def dolbysurroundmodelookup
    #// 
    #// @param int  $acmod
    #// @param bool $lfeon
    #// 
    #// @return array
    #//
    @classmethod
    def channelsenabledlookup(self, acmod=None, lfeon=None):
        
        lookup = Array({"ch1": acmod == 0, "ch2": acmod == 0, "left": acmod > 1, "right": acmod > 1, "center": bool(acmod & 1), "surround_mono": False, "surround_left": False, "surround_right": False, "lfe": lfeon})
        for case in Switch(acmod):
            if case(4):
                pass
            # end if
            if case(5):
                lookup["surround_mono"] = True
                break
            # end if
            if case(6):
                pass
            # end if
            if case(7):
                lookup["surround_left"] = True
                lookup["surround_right"] = True
                break
            # end if
        # end for
        return lookup
    # end def channelsenabledlookup
    #// 
    #// @param int $compre
    #// 
    #// @return float|int
    #//
    @classmethod
    def heavycompression(self, compre=None):
        
        #// The first four bits indicate gain changes in 6.02dB increments which can be
        #// implemented with an arithmetic shift operation. The following four bits
        #// indicate linear gain changes, and require a 5-bit multiply.
        #// We will represent the two 4-bit fields of compr as follows:
        #// X0 X1 X2 X3 . Y4 Y5 Y6 Y7
        #// The meaning of the X values is most simply described by considering X to represent a 4-bit
        #// signed integer with values from -8 to +7. The gain indicated by X is then (X + 1) * 6.02 dB. The
        #// following table shows this in detail.
        #// Meaning of 4 msb of compr
        #// 7    +48.16 dB
        #// 6    +42.14 dB
        #// 5    +36.12 dB
        #// 4    +30.10 dB
        #// 3    +24.08 dB
        #// 2    +18.06 dB
        #// 1    +12.04 dB
        #// 0     +6.02 dB
        #// -1         0 dB
        #// -2     -6.02 dB
        #// -3    -12.04 dB
        #// -4    -18.06 dB
        #// -5    -24.08 dB
        #// -6    -30.10 dB
        #// -7    -36.12 dB
        #// -8    -42.14 dB
        fourbit = php_str_pad(decbin(compre & 240 >> 4), 4, "0", STR_PAD_LEFT)
        if fourbit[0] == "1":
            log_gain = -8 + bindec(php_substr(fourbit, 1))
        else:
            log_gain = bindec(php_substr(fourbit, 1))
        # end if
        log_gain = log_gain + 1 * getid3_lib.rgadamplitude2db(2)
        #// The value of Y is a linear representation of a gain change of up to -6 dB. Y is considered to
        #// be an unsigned fractional integer, with a leading value of 1, or: 0.1 Y4 Y5 Y6 Y7 (base 2). Y can
        #// represent values between 0.111112 (or 31/32) and 0.100002 (or 1/2). Thus, Y can represent gain
        #// changes from -0.28 dB to -6.02 dB.
        lin_gain = 16 + compre & 15 / 32
        #// The combination of X and Y values allows compr to indicate gain changes from
        #// 48.16 - 0.28 = +47.89 dB, to
        #// -42.14 - 6.02 = -48.16 dB.
        return log_gain - lin_gain
    # end def heavycompression
    #// 
    #// @param int $roomtyp
    #// 
    #// @return string|false
    #//
    @classmethod
    def roomtypelookup(self, roomtyp=None):
        
        roomTypeLookup = Array({0: "not indicated", 1: "large room, X curve monitor", 2: "small room, flat monitor", 3: "reserved"})
        return roomTypeLookup[roomtyp] if (php_isset(lambda : roomTypeLookup[roomtyp])) else False
    # end def roomtypelookup
    #// 
    #// @param int $frmsizecod
    #// @param int $fscod
    #// 
    #// @return int|false
    #//
    @classmethod
    def framesizelookup(self, frmsizecod=None, fscod=None):
        
        #// LSB is whether padding is used or not
        padding = bool(frmsizecod & 1)
        framesizeid = frmsizecod & 62 >> 1
        frameSizeLookup = Array()
        if php_empty(lambda : frameSizeLookup):
            frameSizeLookup = Array({0: Array(128, 138, 192), 1: Array(160, 174, 240), 2: Array(192, 208, 288), 3: Array(224, 242, 336), 4: Array(256, 278, 384), 5: Array(320, 348, 480), 6: Array(384, 416, 576), 7: Array(448, 486, 672), 8: Array(512, 556, 768), 9: Array(640, 696, 960), 10: Array(768, 834, 1152), 11: Array(896, 974, 1344), 12: Array(1024, 1114, 1536), 13: Array(1280, 1392, 1920), 14: Array(1536, 1670, 2304), 15: Array(1792, 1950, 2688), 16: Array(2048, 2228, 3072), 17: Array(2304, 2506, 3456), 18: Array(2560, 2786, 3840)})
        # end if
        paddingBytes = 0
        if fscod == 1 and padding:
            #// frame lengths are padded by 1 word (16 bits) at 44100
            #// (fscode==1) means 44100Hz (see sampleRateCodeLookup)
            paddingBytes = 2
        # end if
        return frameSizeLookup[framesizeid][fscod] + paddingBytes if (php_isset(lambda : frameSizeLookup[framesizeid][fscod])) else False
    # end def framesizelookup
    #// 
    #// @param int $frmsizecod
    #// 
    #// @return int|false
    #//
    @classmethod
    def bitratelookup(self, frmsizecod=None):
        
        #// LSB is whether padding is used or not
        padding = bool(frmsizecod & 1)
        framesizeid = frmsizecod & 62 >> 1
        bitrateLookup = Array({0: 32000, 1: 40000, 2: 48000, 3: 56000, 4: 64000, 5: 80000, 6: 96000, 7: 112000, 8: 128000, 9: 160000, 10: 192000, 11: 224000, 12: 256000, 13: 320000, 14: 384000, 15: 448000, 16: 512000, 17: 576000, 18: 640000})
        return bitrateLookup[framesizeid] if (php_isset(lambda : bitrateLookup[framesizeid])) else False
    # end def bitratelookup
    #// 
    #// @param int $numblkscod
    #// 
    #// @return int|false
    #//
    @classmethod
    def blockspersyncframe(self, numblkscod=None):
        
        blocksPerSyncFrameLookup = Array({0: 1, 1: 2, 2: 3, 3: 6})
        return blocksPerSyncFrameLookup[numblkscod] if (php_isset(lambda : blocksPerSyncFrameLookup[numblkscod])) else False
    # end def blockspersyncframe
# end class getid3_ac3
