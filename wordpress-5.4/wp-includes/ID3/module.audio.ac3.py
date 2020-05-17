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
    #// 
    #// @var array
    #//
    AC3header = Array()
    #// 
    #// @var int
    #//
    BSIoffset = 0
    syncword = 2935
    #// 
    #// @return bool
    #//
    def analyze(self):
        
        
        info_ = self.getid3.info
        #// AH
        info_["ac3"]["raw"]["bsi"] = Array()
        thisfile_ac3_ = info_["ac3"]
        thisfile_ac3_raw_ = thisfile_ac3_["raw"]
        thisfile_ac3_raw_bsi_ = thisfile_ac3_raw_["bsi"]
        #// http://www.atsc.org/standards/a_52a.pdf
        info_["fileformat"] = "ac3"
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
        self.fseek(info_["avdataoffset"])
        tempAC3header_ = self.fread(100)
        #// should be enough to cover all data, there are some variable-length fields...?
        self.AC3header["syncinfo"] = getid3_lib.bigendian2int(php_substr(tempAC3header_, 0, 2))
        self.AC3header["bsi"] = getid3_lib.bigendian2bin(php_substr(tempAC3header_, 2))
        thisfile_ac3_raw_bsi_["bsid"] = getid3_lib.littleendian2int(php_substr(tempAC3header_, 5, 1)) & 248 >> 3
        tempAC3header_ = None
        if self.AC3header["syncinfo"] != self.syncword:
            if (not self.isdependencyfor("matroska")):
                info_["fileformat"] = None
                info_["ac3"] = None
                return self.error("Expecting \"" + dechex(self.syncword) + "\" at offset " + info_["avdataoffset"] + ", found \"" + dechex(self.AC3header["syncinfo"]) + "\"")
            # end if
        # end if
        info_["audio"]["dataformat"] = "ac3"
        info_["audio"]["bitrate_mode"] = "cbr"
        info_["audio"]["lossless"] = False
        if thisfile_ac3_raw_bsi_["bsid"] <= 8:
            thisfile_ac3_raw_bsi_["crc1"] = getid3_lib.bin2dec(self.readheaderbsi(16))
            thisfile_ac3_raw_bsi_["fscod"] = self.readheaderbsi(2)
            #// 5.4.1.3
            thisfile_ac3_raw_bsi_["frmsizecod"] = self.readheaderbsi(6)
            #// 5.4.1.4
            if thisfile_ac3_raw_bsi_["frmsizecod"] > 37:
                #// binary: 100101 - see Table 5.18 Frame Size Code Table (1 word = 16 bits)
                self.warning("Unexpected ac3.bsi.frmsizecod value: " + thisfile_ac3_raw_bsi_["frmsizecod"] + ", bitrate not set correctly")
            # end if
            thisfile_ac3_raw_bsi_["bsid"] = self.readheaderbsi(5)
            #// we already know this from pre-parsing the version identifier, but re-read it to let the bitstream flow as intended
            thisfile_ac3_raw_bsi_["bsmod"] = self.readheaderbsi(3)
            thisfile_ac3_raw_bsi_["acmod"] = self.readheaderbsi(3)
            if thisfile_ac3_raw_bsi_["acmod"] & 1:
                #// If the lsb of acmod is a 1, center channel is in use and cmixlev follows in the bit stream.
                thisfile_ac3_raw_bsi_["cmixlev"] = self.readheaderbsi(2)
                thisfile_ac3_["center_mix_level"] = self.centermixlevellookup(thisfile_ac3_raw_bsi_["cmixlev"])
            # end if
            if thisfile_ac3_raw_bsi_["acmod"] & 4:
                #// If the msb of acmod is a 1, surround channels are in use and surmixlev follows in the bit stream.
                thisfile_ac3_raw_bsi_["surmixlev"] = self.readheaderbsi(2)
                thisfile_ac3_["surround_mix_level"] = self.surroundmixlevellookup(thisfile_ac3_raw_bsi_["surmixlev"])
            # end if
            if thisfile_ac3_raw_bsi_["acmod"] == 2:
                #// When operating in the two channel mode, this 2-bit code indicates whether or not the program has been encoded in Dolby Surround.
                thisfile_ac3_raw_bsi_["dsurmod"] = self.readheaderbsi(2)
                thisfile_ac3_["dolby_surround_mode"] = self.dolbysurroundmodelookup(thisfile_ac3_raw_bsi_["dsurmod"])
            # end if
            thisfile_ac3_raw_bsi_["flags"]["lfeon"] = php_bool(self.readheaderbsi(1))
            #// This indicates how far the average dialogue level is below digital 100 percent. Valid values are 1-31.
            #// The value of 0 is reserved. The values of 1 to 31 are interpreted as -1 dB to -31 dB with respect to digital 100 percent.
            thisfile_ac3_raw_bsi_["dialnorm"] = self.readheaderbsi(5)
            #// 5.4.2.8 dialnorm: Dialogue Normalization, 5 Bits
            thisfile_ac3_raw_bsi_["flags"]["compr"] = php_bool(self.readheaderbsi(1))
            #// 5.4.2.9 compre: Compression Gain Word Exists, 1 Bit
            if thisfile_ac3_raw_bsi_["flags"]["compr"]:
                thisfile_ac3_raw_bsi_["compr"] = self.readheaderbsi(8)
                #// 5.4.2.10 compr: Compression Gain Word, 8 Bits
                thisfile_ac3_["heavy_compression"] = self.heavycompression(thisfile_ac3_raw_bsi_["compr"])
            # end if
            thisfile_ac3_raw_bsi_["flags"]["langcod"] = php_bool(self.readheaderbsi(1))
            #// 5.4.2.11 langcode: Language Code Exists, 1 Bit
            if thisfile_ac3_raw_bsi_["flags"]["langcod"]:
                thisfile_ac3_raw_bsi_["langcod"] = self.readheaderbsi(8)
                pass
            # end if
            thisfile_ac3_raw_bsi_["flags"]["audprodinfo"] = php_bool(self.readheaderbsi(1))
            #// 5.4.2.13 audprodie: Audio Production Information Exists, 1 Bit
            if thisfile_ac3_raw_bsi_["flags"]["audprodinfo"]:
                thisfile_ac3_raw_bsi_["mixlevel"] = self.readheaderbsi(5)
                #// 5.4.2.14 mixlevel: Mixing Level, 5 Bits
                thisfile_ac3_raw_bsi_["roomtyp"] = self.readheaderbsi(2)
                #// 5.4.2.15 roomtyp: Room Type, 2 Bits
                thisfile_ac3_["mixing_level"] = 80 + thisfile_ac3_raw_bsi_["mixlevel"] + "dB"
                thisfile_ac3_["room_type"] = self.roomtypelookup(thisfile_ac3_raw_bsi_["roomtyp"])
            # end if
            thisfile_ac3_raw_bsi_["dialnorm2"] = self.readheaderbsi(5)
            #// 5.4.2.16 dialnorm2: Dialogue Normalization, ch2, 5 Bits
            thisfile_ac3_["dialogue_normalization2"] = "-" + thisfile_ac3_raw_bsi_["dialnorm2"] + "dB"
            #// This indicates how far the average dialogue level is below digital 100 percent. Valid values are 1-31. The value of 0 is reserved. The values of 1 to 31 are interpreted as -1 dB to -31 dB with respect to digital 100 percent.
            thisfile_ac3_raw_bsi_["flags"]["compr2"] = php_bool(self.readheaderbsi(1))
            #// 5.4.2.17 compr2e: Compression Gain Word Exists, ch2, 1 Bit
            if thisfile_ac3_raw_bsi_["flags"]["compr2"]:
                thisfile_ac3_raw_bsi_["compr2"] = self.readheaderbsi(8)
                #// 5.4.2.18 compr2: Compression Gain Word, ch2, 8 Bits
                thisfile_ac3_["heavy_compression2"] = self.heavycompression(thisfile_ac3_raw_bsi_["compr2"])
            # end if
            thisfile_ac3_raw_bsi_["flags"]["langcod2"] = php_bool(self.readheaderbsi(1))
            #// 5.4.2.19 langcod2e: Language Code Exists, ch2, 1 Bit
            if thisfile_ac3_raw_bsi_["flags"]["langcod2"]:
                thisfile_ac3_raw_bsi_["langcod2"] = self.readheaderbsi(8)
                pass
            # end if
            thisfile_ac3_raw_bsi_["flags"]["audprodinfo2"] = php_bool(self.readheaderbsi(1))
            #// 5.4.2.21 audprodi2e: Audio Production Information Exists, ch2, 1 Bit
            if thisfile_ac3_raw_bsi_["flags"]["audprodinfo2"]:
                thisfile_ac3_raw_bsi_["mixlevel2"] = self.readheaderbsi(5)
                #// 5.4.2.22 mixlevel2: Mixing Level, ch2, 5 Bits
                thisfile_ac3_raw_bsi_["roomtyp2"] = self.readheaderbsi(2)
                #// 5.4.2.23 roomtyp2: Room Type, ch2, 2 Bits
                thisfile_ac3_["mixing_level2"] = 80 + thisfile_ac3_raw_bsi_["mixlevel2"] + "dB"
                thisfile_ac3_["room_type2"] = self.roomtypelookup(thisfile_ac3_raw_bsi_["roomtyp2"])
            # end if
            thisfile_ac3_raw_bsi_["copyright"] = php_bool(self.readheaderbsi(1))
            #// 5.4.2.24 copyrightb: Copyright Bit, 1 Bit
            thisfile_ac3_raw_bsi_["original"] = php_bool(self.readheaderbsi(1))
            #// 5.4.2.25 origbs: Original Bit Stream, 1 Bit
            thisfile_ac3_raw_bsi_["flags"]["timecod1"] = self.readheaderbsi(2)
            #// 5.4.2.26 timecod1e, timcode2e: Time Code (first and second) Halves Exist, 2 Bits
            if thisfile_ac3_raw_bsi_["flags"]["timecod1"] & 1:
                thisfile_ac3_raw_bsi_["timecod1"] = self.readheaderbsi(14)
                #// 5.4.2.27 timecod1: Time code first half, 14 bits
                thisfile_ac3_["timecode1"] = 0
                thisfile_ac3_["timecode1"] += thisfile_ac3_raw_bsi_["timecod1"] & 15872 >> 9 * 3600
                #// The first 5 bits of this 14-bit field represent the time in hours, with valid values of 0�23
                thisfile_ac3_["timecode1"] += thisfile_ac3_raw_bsi_["timecod1"] & 504 >> 3 * 60
                #// The next 6 bits represent the time in minutes, with valid values of 0�59
                thisfile_ac3_["timecode1"] += thisfile_ac3_raw_bsi_["timecod1"] & 3 >> 0 * 8
                pass
            # end if
            if thisfile_ac3_raw_bsi_["flags"]["timecod1"] & 2:
                thisfile_ac3_raw_bsi_["timecod2"] = self.readheaderbsi(14)
                #// 5.4.2.28 timecod2: Time code second half, 14 bits
                thisfile_ac3_["timecode2"] = 0
                thisfile_ac3_["timecode2"] += thisfile_ac3_raw_bsi_["timecod2"] & 14336 >> 11 * 1
                #// The first 3 bits of this 14-bit field represent the time in seconds, with valid values from 0�7 (representing 0-7 seconds)
                thisfile_ac3_["timecode2"] += thisfile_ac3_raw_bsi_["timecod2"] & 1984 >> 6 * 1 / 30
                #// The next 5 bits represents the time in frames, with valid values from 0�29 (one frame = 1/30th of a second)
                thisfile_ac3_["timecode2"] += thisfile_ac3_raw_bsi_["timecod2"] & 63 >> 0 * 1 / 30 / 60
                pass
            # end if
            thisfile_ac3_raw_bsi_["flags"]["addbsi"] = php_bool(self.readheaderbsi(1))
            if thisfile_ac3_raw_bsi_["flags"]["addbsi"]:
                thisfile_ac3_raw_bsi_["addbsi_length"] = self.readheaderbsi(6) + 1
                #// This 6-bit code, which exists only if addbside is a 1, indicates the length in bytes of additional bit stream information. The valid range of addbsil is 0�63, indicating 1�64 additional bytes, respectively.
                self.AC3header["bsi"] += getid3_lib.bigendian2bin(self.fread(thisfile_ac3_raw_bsi_["addbsi_length"]))
                thisfile_ac3_raw_bsi_["addbsi_data"] = php_substr(self.AC3header["bsi"], self.BSIoffset, thisfile_ac3_raw_bsi_["addbsi_length"] * 8)
                self.BSIoffset += thisfile_ac3_raw_bsi_["addbsi_length"] * 8
            # end if
        elif thisfile_ac3_raw_bsi_["bsid"] <= 16:
            #// E-AC3
            self.error("E-AC3 parsing is incomplete and experimental in this version of getID3 (" + self.getid3.version() + "). Notably the bitrate calculations are wrong -- value might (or not) be correct, but it is not calculated correctly. Email info@getid3.org if you know how to calculate EAC3 bitrate correctly.")
            info_["audio"]["dataformat"] = "eac3"
            thisfile_ac3_raw_bsi_["strmtyp"] = self.readheaderbsi(2)
            thisfile_ac3_raw_bsi_["substreamid"] = self.readheaderbsi(3)
            thisfile_ac3_raw_bsi_["frmsiz"] = self.readheaderbsi(11)
            thisfile_ac3_raw_bsi_["fscod"] = self.readheaderbsi(2)
            if thisfile_ac3_raw_bsi_["fscod"] == 3:
                thisfile_ac3_raw_bsi_["fscod2"] = self.readheaderbsi(2)
                thisfile_ac3_raw_bsi_["numblkscod"] = 3
                pass
            else:
                thisfile_ac3_raw_bsi_["numblkscod"] = self.readheaderbsi(2)
            # end if
            thisfile_ac3_["bsi"]["blocks_per_sync_frame"] = self.blockspersyncframe(thisfile_ac3_raw_bsi_["numblkscod"])
            thisfile_ac3_raw_bsi_["acmod"] = self.readheaderbsi(3)
            thisfile_ac3_raw_bsi_["flags"]["lfeon"] = php_bool(self.readheaderbsi(1))
            thisfile_ac3_raw_bsi_["bsid"] = self.readheaderbsi(5)
            #// we already know this from pre-parsing the version identifier, but re-read it to let the bitstream flow as intended
            thisfile_ac3_raw_bsi_["dialnorm"] = self.readheaderbsi(5)
            thisfile_ac3_raw_bsi_["flags"]["compr"] = php_bool(self.readheaderbsi(1))
            if thisfile_ac3_raw_bsi_["flags"]["compr"]:
                thisfile_ac3_raw_bsi_["compr"] = self.readheaderbsi(8)
            # end if
            if thisfile_ac3_raw_bsi_["acmod"] == 0:
                #// if 1+1 mode (dual mono, so some items need a second value)
                thisfile_ac3_raw_bsi_["dialnorm2"] = self.readheaderbsi(5)
                thisfile_ac3_raw_bsi_["flags"]["compr2"] = php_bool(self.readheaderbsi(1))
                if thisfile_ac3_raw_bsi_["flags"]["compr2"]:
                    thisfile_ac3_raw_bsi_["compr2"] = self.readheaderbsi(8)
                # end if
            # end if
            if thisfile_ac3_raw_bsi_["strmtyp"] == 1:
                #// if dependent stream
                thisfile_ac3_raw_bsi_["flags"]["chanmap"] = php_bool(self.readheaderbsi(1))
                if thisfile_ac3_raw_bsi_["flags"]["chanmap"]:
                    thisfile_ac3_raw_bsi_["chanmap"] = self.readheaderbsi(8)
                # end if
            # end if
            thisfile_ac3_raw_bsi_["flags"]["mixmdat"] = php_bool(self.readheaderbsi(1))
            if thisfile_ac3_raw_bsi_["flags"]["mixmdat"]:
                #// Mixing metadata
                if thisfile_ac3_raw_bsi_["acmod"] > 2:
                    #// if more than 2 channels
                    thisfile_ac3_raw_bsi_["dmixmod"] = self.readheaderbsi(2)
                # end if
                if thisfile_ac3_raw_bsi_["acmod"] & 1 and thisfile_ac3_raw_bsi_["acmod"] > 2:
                    #// if three front channels exist
                    thisfile_ac3_raw_bsi_["ltrtcmixlev"] = self.readheaderbsi(3)
                    thisfile_ac3_raw_bsi_["lorocmixlev"] = self.readheaderbsi(3)
                # end if
                if thisfile_ac3_raw_bsi_["acmod"] & 4:
                    #// if a surround channel exists
                    thisfile_ac3_raw_bsi_["ltrtsurmixlev"] = self.readheaderbsi(3)
                    thisfile_ac3_raw_bsi_["lorosurmixlev"] = self.readheaderbsi(3)
                # end if
                if thisfile_ac3_raw_bsi_["flags"]["lfeon"]:
                    #// if the LFE channel exists
                    thisfile_ac3_raw_bsi_["flags"]["lfemixlevcod"] = php_bool(self.readheaderbsi(1))
                    if thisfile_ac3_raw_bsi_["flags"]["lfemixlevcod"]:
                        thisfile_ac3_raw_bsi_["lfemixlevcod"] = self.readheaderbsi(5)
                    # end if
                # end if
                if thisfile_ac3_raw_bsi_["strmtyp"] == 0:
                    #// if independent stream
                    thisfile_ac3_raw_bsi_["flags"]["pgmscl"] = php_bool(self.readheaderbsi(1))
                    if thisfile_ac3_raw_bsi_["flags"]["pgmscl"]:
                        thisfile_ac3_raw_bsi_["pgmscl"] = self.readheaderbsi(6)
                    # end if
                    if thisfile_ac3_raw_bsi_["acmod"] == 0:
                        #// if 1+1 mode (dual mono, so some items need a second value)
                        thisfile_ac3_raw_bsi_["flags"]["pgmscl2"] = php_bool(self.readheaderbsi(1))
                        if thisfile_ac3_raw_bsi_["flags"]["pgmscl2"]:
                            thisfile_ac3_raw_bsi_["pgmscl2"] = self.readheaderbsi(6)
                        # end if
                    # end if
                    thisfile_ac3_raw_bsi_["flags"]["extpgmscl"] = php_bool(self.readheaderbsi(1))
                    if thisfile_ac3_raw_bsi_["flags"]["extpgmscl"]:
                        thisfile_ac3_raw_bsi_["extpgmscl"] = self.readheaderbsi(6)
                    # end if
                    thisfile_ac3_raw_bsi_["mixdef"] = self.readheaderbsi(2)
                    if thisfile_ac3_raw_bsi_["mixdef"] == 1:
                        #// mixing option 2
                        thisfile_ac3_raw_bsi_["premixcmpsel"] = php_bool(self.readheaderbsi(1))
                        thisfile_ac3_raw_bsi_["drcsrc"] = php_bool(self.readheaderbsi(1))
                        thisfile_ac3_raw_bsi_["premixcmpscl"] = self.readheaderbsi(3)
                    elif thisfile_ac3_raw_bsi_["mixdef"] == 2:
                        #// mixing option 3
                        thisfile_ac3_raw_bsi_["mixdata"] = self.readheaderbsi(12)
                    elif thisfile_ac3_raw_bsi_["mixdef"] == 3:
                        #// mixing option 4
                        mixdefbitsread_ = 0
                        thisfile_ac3_raw_bsi_["mixdeflen"] = self.readheaderbsi(5)
                        mixdefbitsread_ += 5
                        thisfile_ac3_raw_bsi_["flags"]["mixdata2"] = php_bool(self.readheaderbsi(1))
                        mixdefbitsread_ += 1
                        if thisfile_ac3_raw_bsi_["flags"]["mixdata2"]:
                            thisfile_ac3_raw_bsi_["premixcmpsel"] = php_bool(self.readheaderbsi(1))
                            mixdefbitsread_ += 1
                            thisfile_ac3_raw_bsi_["drcsrc"] = php_bool(self.readheaderbsi(1))
                            mixdefbitsread_ += 1
                            thisfile_ac3_raw_bsi_["premixcmpscl"] = self.readheaderbsi(3)
                            mixdefbitsread_ += 3
                            thisfile_ac3_raw_bsi_["flags"]["extpgmlscl"] = php_bool(self.readheaderbsi(1))
                            mixdefbitsread_ += 1
                            if thisfile_ac3_raw_bsi_["flags"]["extpgmlscl"]:
                                thisfile_ac3_raw_bsi_["extpgmlscl"] = self.readheaderbsi(4)
                                mixdefbitsread_ += 4
                            # end if
                            thisfile_ac3_raw_bsi_["flags"]["extpgmcscl"] = php_bool(self.readheaderbsi(1))
                            mixdefbitsread_ += 1
                            if thisfile_ac3_raw_bsi_["flags"]["extpgmcscl"]:
                                thisfile_ac3_raw_bsi_["extpgmcscl"] = self.readheaderbsi(4)
                                mixdefbitsread_ += 4
                            # end if
                            thisfile_ac3_raw_bsi_["flags"]["extpgmrscl"] = php_bool(self.readheaderbsi(1))
                            mixdefbitsread_ += 1
                            if thisfile_ac3_raw_bsi_["flags"]["extpgmrscl"]:
                                thisfile_ac3_raw_bsi_["extpgmrscl"] = self.readheaderbsi(4)
                            # end if
                            thisfile_ac3_raw_bsi_["flags"]["extpgmlsscl"] = php_bool(self.readheaderbsi(1))
                            mixdefbitsread_ += 1
                            if thisfile_ac3_raw_bsi_["flags"]["extpgmlsscl"]:
                                thisfile_ac3_raw_bsi_["extpgmlsscl"] = self.readheaderbsi(4)
                                mixdefbitsread_ += 4
                            # end if
                            thisfile_ac3_raw_bsi_["flags"]["extpgmrsscl"] = php_bool(self.readheaderbsi(1))
                            mixdefbitsread_ += 1
                            if thisfile_ac3_raw_bsi_["flags"]["extpgmrsscl"]:
                                thisfile_ac3_raw_bsi_["extpgmrsscl"] = self.readheaderbsi(4)
                                mixdefbitsread_ += 4
                            # end if
                            thisfile_ac3_raw_bsi_["flags"]["extpgmlfescl"] = php_bool(self.readheaderbsi(1))
                            mixdefbitsread_ += 1
                            if thisfile_ac3_raw_bsi_["flags"]["extpgmlfescl"]:
                                thisfile_ac3_raw_bsi_["extpgmlfescl"] = self.readheaderbsi(4)
                                mixdefbitsread_ += 4
                            # end if
                            thisfile_ac3_raw_bsi_["flags"]["dmixscl"] = php_bool(self.readheaderbsi(1))
                            mixdefbitsread_ += 1
                            if thisfile_ac3_raw_bsi_["flags"]["dmixscl"]:
                                thisfile_ac3_raw_bsi_["dmixscl"] = self.readheaderbsi(4)
                                mixdefbitsread_ += 4
                            # end if
                            thisfile_ac3_raw_bsi_["flags"]["addch"] = php_bool(self.readheaderbsi(1))
                            mixdefbitsread_ += 1
                            if thisfile_ac3_raw_bsi_["flags"]["addch"]:
                                thisfile_ac3_raw_bsi_["flags"]["extpgmaux1scl"] = php_bool(self.readheaderbsi(1))
                                mixdefbitsread_ += 1
                                if thisfile_ac3_raw_bsi_["flags"]["extpgmaux1scl"]:
                                    thisfile_ac3_raw_bsi_["extpgmaux1scl"] = self.readheaderbsi(4)
                                    mixdefbitsread_ += 4
                                # end if
                                thisfile_ac3_raw_bsi_["flags"]["extpgmaux2scl"] = php_bool(self.readheaderbsi(1))
                                mixdefbitsread_ += 1
                                if thisfile_ac3_raw_bsi_["flags"]["extpgmaux2scl"]:
                                    thisfile_ac3_raw_bsi_["extpgmaux2scl"] = self.readheaderbsi(4)
                                    mixdefbitsread_ += 4
                                # end if
                            # end if
                        # end if
                        thisfile_ac3_raw_bsi_["flags"]["mixdata3"] = php_bool(self.readheaderbsi(1))
                        mixdefbitsread_ += 1
                        if thisfile_ac3_raw_bsi_["flags"]["mixdata3"]:
                            thisfile_ac3_raw_bsi_["spchdat"] = self.readheaderbsi(5)
                            mixdefbitsread_ += 5
                            thisfile_ac3_raw_bsi_["flags"]["addspchdat"] = php_bool(self.readheaderbsi(1))
                            mixdefbitsread_ += 1
                            if thisfile_ac3_raw_bsi_["flags"]["addspchdat"]:
                                thisfile_ac3_raw_bsi_["spchdat1"] = self.readheaderbsi(5)
                                mixdefbitsread_ += 5
                                thisfile_ac3_raw_bsi_["spchan1att"] = self.readheaderbsi(2)
                                mixdefbitsread_ += 2
                                thisfile_ac3_raw_bsi_["flags"]["addspchdat1"] = php_bool(self.readheaderbsi(1))
                                mixdefbitsread_ += 1
                                if thisfile_ac3_raw_bsi_["flags"]["addspchdat1"]:
                                    thisfile_ac3_raw_bsi_["spchdat2"] = self.readheaderbsi(5)
                                    mixdefbitsread_ += 5
                                    thisfile_ac3_raw_bsi_["spchan2att"] = self.readheaderbsi(3)
                                    mixdefbitsread_ += 3
                                # end if
                            # end if
                        # end if
                        mixdata_bits_ = 8 * thisfile_ac3_raw_bsi_["mixdeflen"] + 2 - mixdefbitsread_
                        mixdata_fill_ = 8 - mixdata_bits_ % 8 if mixdata_bits_ % 8 else 0
                        thisfile_ac3_raw_bsi_["mixdata"] = self.readheaderbsi(mixdata_bits_)
                        thisfile_ac3_raw_bsi_["mixdatafill"] = self.readheaderbsi(mixdata_fill_)
                        mixdefbitsread_ = None
                        mixdata_bits_ = None
                        mixdata_fill_ = None
                    # end if
                    if thisfile_ac3_raw_bsi_["acmod"] < 2:
                        #// if mono or dual mono source
                        thisfile_ac3_raw_bsi_["flags"]["paninfo"] = php_bool(self.readheaderbsi(1))
                        if thisfile_ac3_raw_bsi_["flags"]["paninfo"]:
                            thisfile_ac3_raw_bsi_["panmean"] = self.readheaderbsi(8)
                            thisfile_ac3_raw_bsi_["paninfo"] = self.readheaderbsi(6)
                        # end if
                        if thisfile_ac3_raw_bsi_["acmod"] == 0:
                            #// if 1+1 mode (dual mono, so some items need a second value)
                            thisfile_ac3_raw_bsi_["flags"]["paninfo2"] = php_bool(self.readheaderbsi(1))
                            if thisfile_ac3_raw_bsi_["flags"]["paninfo2"]:
                                thisfile_ac3_raw_bsi_["panmean2"] = self.readheaderbsi(8)
                                thisfile_ac3_raw_bsi_["paninfo2"] = self.readheaderbsi(6)
                            # end if
                        # end if
                    # end if
                    thisfile_ac3_raw_bsi_["flags"]["frmmixcfginfo"] = php_bool(self.readheaderbsi(1))
                    if thisfile_ac3_raw_bsi_["flags"]["frmmixcfginfo"]:
                        #// mixing configuration information
                        if thisfile_ac3_raw_bsi_["numblkscod"] == 0:
                            thisfile_ac3_raw_bsi_["blkmixcfginfo"][0] = self.readheaderbsi(5)
                        else:
                            blk_ = 0
                            while blk_ < thisfile_ac3_raw_bsi_["numblkscod"]:
                                
                                thisfile_ac3_raw_bsi_["flags"]["blkmixcfginfo" + blk_] = php_bool(self.readheaderbsi(1))
                                if thisfile_ac3_raw_bsi_["flags"]["blkmixcfginfo" + blk_]:
                                    #// mixing configuration information
                                    thisfile_ac3_raw_bsi_["blkmixcfginfo"][blk_] = self.readheaderbsi(5)
                                # end if
                                blk_ += 1
                            # end while
                        # end if
                    # end if
                # end if
            # end if
            thisfile_ac3_raw_bsi_["flags"]["infomdat"] = php_bool(self.readheaderbsi(1))
            if thisfile_ac3_raw_bsi_["flags"]["infomdat"]:
                #// Informational metadata
                thisfile_ac3_raw_bsi_["bsmod"] = self.readheaderbsi(3)
                thisfile_ac3_raw_bsi_["flags"]["copyrightb"] = php_bool(self.readheaderbsi(1))
                thisfile_ac3_raw_bsi_["flags"]["origbs"] = php_bool(self.readheaderbsi(1))
                if thisfile_ac3_raw_bsi_["acmod"] == 2:
                    #// if in 2/0 mode
                    thisfile_ac3_raw_bsi_["dsurmod"] = self.readheaderbsi(2)
                    thisfile_ac3_raw_bsi_["dheadphonmod"] = self.readheaderbsi(2)
                # end if
                if thisfile_ac3_raw_bsi_["acmod"] >= 6:
                    #// if both surround channels exist
                    thisfile_ac3_raw_bsi_["dsurexmod"] = self.readheaderbsi(2)
                # end if
                thisfile_ac3_raw_bsi_["flags"]["audprodi"] = php_bool(self.readheaderbsi(1))
                if thisfile_ac3_raw_bsi_["flags"]["audprodi"]:
                    thisfile_ac3_raw_bsi_["mixlevel"] = self.readheaderbsi(5)
                    thisfile_ac3_raw_bsi_["roomtyp"] = self.readheaderbsi(2)
                    thisfile_ac3_raw_bsi_["flags"]["adconvtyp"] = php_bool(self.readheaderbsi(1))
                # end if
                if thisfile_ac3_raw_bsi_["acmod"] == 0:
                    #// if 1+1 mode (dual mono, so some items need a second value)
                    thisfile_ac3_raw_bsi_["flags"]["audprodi2"] = php_bool(self.readheaderbsi(1))
                    if thisfile_ac3_raw_bsi_["flags"]["audprodi2"]:
                        thisfile_ac3_raw_bsi_["mixlevel2"] = self.readheaderbsi(5)
                        thisfile_ac3_raw_bsi_["roomtyp2"] = self.readheaderbsi(2)
                        thisfile_ac3_raw_bsi_["flags"]["adconvtyp2"] = php_bool(self.readheaderbsi(1))
                    # end if
                # end if
                if thisfile_ac3_raw_bsi_["fscod"] < 3:
                    #// if not half sample rate
                    thisfile_ac3_raw_bsi_["flags"]["sourcefscod"] = php_bool(self.readheaderbsi(1))
                # end if
            # end if
            if thisfile_ac3_raw_bsi_["strmtyp"] == 0 and thisfile_ac3_raw_bsi_["numblkscod"] != 3:
                #// if both surround channels exist
                thisfile_ac3_raw_bsi_["flags"]["convsync"] = php_bool(self.readheaderbsi(1))
            # end if
            if thisfile_ac3_raw_bsi_["strmtyp"] == 2:
                #// if bit stream converted from AC-3
                if thisfile_ac3_raw_bsi_["numblkscod"] != 3:
                    #// 6 blocks per syncframe
                    thisfile_ac3_raw_bsi_["flags"]["blkid"] = 1
                else:
                    thisfile_ac3_raw_bsi_["flags"]["blkid"] = php_bool(self.readheaderbsi(1))
                # end if
                if thisfile_ac3_raw_bsi_["flags"]["blkid"]:
                    thisfile_ac3_raw_bsi_["frmsizecod"] = self.readheaderbsi(6)
                # end if
            # end if
            thisfile_ac3_raw_bsi_["flags"]["addbsi"] = php_bool(self.readheaderbsi(1))
            if thisfile_ac3_raw_bsi_["flags"]["addbsi"]:
                thisfile_ac3_raw_bsi_["addbsil"] = self.readheaderbsi(6)
                thisfile_ac3_raw_bsi_["addbsi"] = self.readheaderbsi(thisfile_ac3_raw_bsi_["addbsil"] + 1 * 8)
            # end if
        else:
            self.error("Bit stream identification is version " + thisfile_ac3_raw_bsi_["bsid"] + ", but getID3() only understands up to version 16. Please submit a support ticket with a sample file.")
            info_["ac3"] = None
            return False
        # end if
        if (php_isset(lambda : thisfile_ac3_raw_bsi_["fscod2"])):
            thisfile_ac3_["sample_rate"] = self.sampleratecodelookup2(thisfile_ac3_raw_bsi_["fscod2"])
        else:
            thisfile_ac3_["sample_rate"] = self.sampleratecodelookup(thisfile_ac3_raw_bsi_["fscod"])
        # end if
        if thisfile_ac3_raw_bsi_["fscod"] <= 3:
            info_["audio"]["sample_rate"] = thisfile_ac3_["sample_rate"]
        else:
            self.warning("Unexpected ac3.bsi.fscod value: " + thisfile_ac3_raw_bsi_["fscod"])
        # end if
        if (php_isset(lambda : thisfile_ac3_raw_bsi_["frmsizecod"])):
            thisfile_ac3_["frame_length"] = self.framesizelookup(thisfile_ac3_raw_bsi_["frmsizecod"], thisfile_ac3_raw_bsi_["fscod"])
            thisfile_ac3_["bitrate"] = self.bitratelookup(thisfile_ac3_raw_bsi_["frmsizecod"])
        elif (not php_empty(lambda : thisfile_ac3_raw_bsi_["frmsiz"])):
            #// this isn't right, but it's (usually) close, roughly 5% less than it should be.
            #// but WHERE is the actual bitrate value stored in EAC3?? email info@getid3.org if you know!
            thisfile_ac3_["bitrate"] = thisfile_ac3_raw_bsi_["frmsiz"] + 1 * 16 * 30
            #// The frmsiz field shall contain a value one less than the overall size of the coded syncframe in 16-bit words. That is, this field may assume a value ranging from 0 to 2047, and these values correspond to syncframe sizes ranging from 1 to 2048.
            #// kludge-fix to make it approximately the expected value, still not "right":
            thisfile_ac3_["bitrate"] = round(thisfile_ac3_["bitrate"] * 1.05 / 16000) * 16000
        # end if
        info_["audio"]["bitrate"] = thisfile_ac3_["bitrate"]
        if (php_isset(lambda : thisfile_ac3_raw_bsi_["bsmod"])) and (php_isset(lambda : thisfile_ac3_raw_bsi_["acmod"])):
            thisfile_ac3_["service_type"] = self.servicetypelookup(thisfile_ac3_raw_bsi_["bsmod"], thisfile_ac3_raw_bsi_["acmod"])
        # end if
        ac3_coding_mode_ = self.audiocodingmodelookup(thisfile_ac3_raw_bsi_["acmod"])
        for key_,value_ in ac3_coding_mode_:
            thisfile_ac3_[key_] = value_
        # end for
        for case in Switch(thisfile_ac3_raw_bsi_["acmod"]):
            if case(0):
                pass
            # end if
            if case(1):
                info_["audio"]["channelmode"] = "mono"
                break
            # end if
            if case(3):
                pass
            # end if
            if case(4):
                info_["audio"]["channelmode"] = "stereo"
                break
            # end if
            if case():
                info_["audio"]["channelmode"] = "surround"
                break
            # end if
        # end for
        info_["audio"]["channels"] = thisfile_ac3_["num_channels"]
        thisfile_ac3_["lfe_enabled"] = thisfile_ac3_raw_bsi_["flags"]["lfeon"]
        if thisfile_ac3_raw_bsi_["flags"]["lfeon"]:
            info_["audio"]["channels"] += ".1"
        # end if
        thisfile_ac3_["channels_enabled"] = self.channelsenabledlookup(thisfile_ac3_raw_bsi_["acmod"], thisfile_ac3_raw_bsi_["flags"]["lfeon"])
        thisfile_ac3_["dialogue_normalization"] = "-" + thisfile_ac3_raw_bsi_["dialnorm"] + "dB"
        return True
    # end def analyze
    #// 
    #// @param int $length
    #// 
    #// @return float|int
    #//
    def readheaderbsi(self, length_=None):
        
        
        data_ = php_substr(self.AC3header["bsi"], self.BSIoffset, length_)
        self.BSIoffset += length_
        return bindec(data_)
    # end def readheaderbsi
    #// 
    #// @param int $fscod
    #// 
    #// @return int|string|false
    #//
    @classmethod
    def sampleratecodelookup(self, fscod_=None):
        
        
        sampleRateCodeLookup_ = Array({0: 48000, 1: 44100, 2: 32000, 3: "reserved"})
        return sampleRateCodeLookup_[fscod_] if (php_isset(lambda : sampleRateCodeLookup_[fscod_])) else False
    # end def sampleratecodelookup
    #// 
    #// @param int $fscod2
    #// 
    #// @return int|string|false
    #//
    @classmethod
    def sampleratecodelookup2(self, fscod2_=None):
        
        
        sampleRateCodeLookup2_ = Array({0: 24000, 1: 22050, 2: 16000, 3: "reserved"})
        return sampleRateCodeLookup2_[fscod2_] if (php_isset(lambda : sampleRateCodeLookup2_[fscod2_])) else False
    # end def sampleratecodelookup2
    #// 
    #// @param int $bsmod
    #// @param int $acmod
    #// 
    #// @return string|false
    #//
    @classmethod
    def servicetypelookup(self, bsmod_=None, acmod_=None):
        
        
        serviceTypeLookup_ = Array()
        if php_empty(lambda : serviceTypeLookup_):
            i_ = 0
            while i_ <= 7:
                
                serviceTypeLookup_[0][i_] = "main audio service: complete main (CM)"
                serviceTypeLookup_[1][i_] = "main audio service: music and effects (ME)"
                serviceTypeLookup_[2][i_] = "associated service: visually impaired (VI)"
                serviceTypeLookup_[3][i_] = "associated service: hearing impaired (HI)"
                serviceTypeLookup_[4][i_] = "associated service: dialogue (D)"
                serviceTypeLookup_[5][i_] = "associated service: commentary (C)"
                serviceTypeLookup_[6][i_] = "associated service: emergency (E)"
                i_ += 1
            # end while
            serviceTypeLookup_[7][1] = "associated service: voice over (VO)"
            i_ = 2
            while i_ <= 7:
                
                serviceTypeLookup_[7][i_] = "main audio service: karaoke"
                i_ += 1
            # end while
        # end if
        return serviceTypeLookup_[bsmod_][acmod_] if (php_isset(lambda : serviceTypeLookup_[bsmod_][acmod_])) else False
    # end def servicetypelookup
    #// 
    #// @param int $acmod
    #// 
    #// @return array|false
    #//
    @classmethod
    def audiocodingmodelookup(self, acmod_=None):
        
        
        audioCodingModeLookup_ = Array({0: Array({"channel_config": "1+1", "num_channels": 2, "channel_order": "Ch1,Ch2"})}, {1: Array({"channel_config": "1/0", "num_channels": 1, "channel_order": "C"})}, {2: Array({"channel_config": "2/0", "num_channels": 2, "channel_order": "L,R"})}, {3: Array({"channel_config": "3/0", "num_channels": 3, "channel_order": "L,C,R"})}, {4: Array({"channel_config": "2/1", "num_channels": 3, "channel_order": "L,R,S"})}, {5: Array({"channel_config": "3/1", "num_channels": 4, "channel_order": "L,C,R,S"})}, {6: Array({"channel_config": "2/2", "num_channels": 4, "channel_order": "L,R,SL,SR"})}, {7: Array({"channel_config": "3/2", "num_channels": 5, "channel_order": "L,C,R,SL,SR"})})
        return audioCodingModeLookup_[acmod_] if (php_isset(lambda : audioCodingModeLookup_[acmod_])) else False
    # end def audiocodingmodelookup
    #// 
    #// @param int $cmixlev
    #// 
    #// @return int|float|string|false
    #//
    @classmethod
    def centermixlevellookup(self, cmixlev_=None):
        
        
        centerMixLevelLookup_ = None
        if php_empty(lambda : centerMixLevelLookup_):
            centerMixLevelLookup_ = Array({0: pow(2, -3 / 6), 1: pow(2, -4.5 / 6), 2: pow(2, -6 / 6), 3: "reserved"})
        # end if
        return centerMixLevelLookup_[cmixlev_] if (php_isset(lambda : centerMixLevelLookup_[cmixlev_])) else False
    # end def centermixlevellookup
    #// 
    #// @param int $surmixlev
    #// 
    #// @return int|float|string|false
    #//
    @classmethod
    def surroundmixlevellookup(self, surmixlev_=None):
        
        
        surroundMixLevelLookup_ = None
        if php_empty(lambda : surroundMixLevelLookup_):
            surroundMixLevelLookup_ = Array({0: pow(2, -3 / 6), 1: pow(2, -6 / 6), 2: 0, 3: "reserved"})
        # end if
        return surroundMixLevelLookup_[surmixlev_] if (php_isset(lambda : surroundMixLevelLookup_[surmixlev_])) else False
    # end def surroundmixlevellookup
    #// 
    #// @param int $dsurmod
    #// 
    #// @return string|false
    #//
    @classmethod
    def dolbysurroundmodelookup(self, dsurmod_=None):
        
        
        dolbySurroundModeLookup_ = Array({0: "not indicated", 1: "Not Dolby Surround encoded", 2: "Dolby Surround encoded", 3: "reserved"})
        return dolbySurroundModeLookup_[dsurmod_] if (php_isset(lambda : dolbySurroundModeLookup_[dsurmod_])) else False
    # end def dolbysurroundmodelookup
    #// 
    #// @param int  $acmod
    #// @param bool $lfeon
    #// 
    #// @return array
    #//
    @classmethod
    def channelsenabledlookup(self, acmod_=None, lfeon_=None):
        
        
        lookup_ = Array({"ch1": acmod_ == 0, "ch2": acmod_ == 0, "left": acmod_ > 1, "right": acmod_ > 1, "center": php_bool(acmod_ & 1), "surround_mono": False, "surround_left": False, "surround_right": False, "lfe": lfeon_})
        for case in Switch(acmod_):
            if case(4):
                pass
            # end if
            if case(5):
                lookup_["surround_mono"] = True
                break
            # end if
            if case(6):
                pass
            # end if
            if case(7):
                lookup_["surround_left"] = True
                lookup_["surround_right"] = True
                break
            # end if
        # end for
        return lookup_
    # end def channelsenabledlookup
    #// 
    #// @param int $compre
    #// 
    #// @return float|int
    #//
    @classmethod
    def heavycompression(self, compre_=None):
        
        
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
        fourbit_ = php_str_pad(decbin(compre_ & 240 >> 4), 4, "0", STR_PAD_LEFT)
        if fourbit_[0] == "1":
            log_gain_ = -8 + bindec(php_substr(fourbit_, 1))
        else:
            log_gain_ = bindec(php_substr(fourbit_, 1))
        # end if
        log_gain_ = log_gain_ + 1 * getid3_lib.rgadamplitude2db(2)
        #// The value of Y is a linear representation of a gain change of up to -6 dB. Y is considered to
        #// be an unsigned fractional integer, with a leading value of 1, or: 0.1 Y4 Y5 Y6 Y7 (base 2). Y can
        #// represent values between 0.111112 (or 31/32) and 0.100002 (or 1/2). Thus, Y can represent gain
        #// changes from -0.28 dB to -6.02 dB.
        lin_gain_ = 16 + compre_ & 15 / 32
        #// The combination of X and Y values allows compr to indicate gain changes from
        #// 48.16 - 0.28 = +47.89 dB, to
        #// -42.14 - 6.02 = -48.16 dB.
        return log_gain_ - lin_gain_
    # end def heavycompression
    #// 
    #// @param int $roomtyp
    #// 
    #// @return string|false
    #//
    @classmethod
    def roomtypelookup(self, roomtyp_=None):
        
        
        roomTypeLookup_ = Array({0: "not indicated", 1: "large room, X curve monitor", 2: "small room, flat monitor", 3: "reserved"})
        return roomTypeLookup_[roomtyp_] if (php_isset(lambda : roomTypeLookup_[roomtyp_])) else False
    # end def roomtypelookup
    #// 
    #// @param int $frmsizecod
    #// @param int $fscod
    #// 
    #// @return int|false
    #//
    @classmethod
    def framesizelookup(self, frmsizecod_=None, fscod_=None):
        
        
        #// LSB is whether padding is used or not
        padding_ = php_bool(frmsizecod_ & 1)
        framesizeid_ = frmsizecod_ & 62 >> 1
        frameSizeLookup_ = Array()
        if php_empty(lambda : frameSizeLookup_):
            frameSizeLookup_ = Array({0: Array(128, 138, 192), 1: Array(160, 174, 240), 2: Array(192, 208, 288), 3: Array(224, 242, 336), 4: Array(256, 278, 384), 5: Array(320, 348, 480), 6: Array(384, 416, 576), 7: Array(448, 486, 672), 8: Array(512, 556, 768), 9: Array(640, 696, 960), 10: Array(768, 834, 1152), 11: Array(896, 974, 1344), 12: Array(1024, 1114, 1536), 13: Array(1280, 1392, 1920), 14: Array(1536, 1670, 2304), 15: Array(1792, 1950, 2688), 16: Array(2048, 2228, 3072), 17: Array(2304, 2506, 3456), 18: Array(2560, 2786, 3840)})
        # end if
        paddingBytes_ = 0
        if fscod_ == 1 and padding_:
            #// frame lengths are padded by 1 word (16 bits) at 44100
            #// (fscode==1) means 44100Hz (see sampleRateCodeLookup)
            paddingBytes_ = 2
        # end if
        return frameSizeLookup_[framesizeid_][fscod_] + paddingBytes_ if (php_isset(lambda : frameSizeLookup_[framesizeid_][fscod_])) else False
    # end def framesizelookup
    #// 
    #// @param int $frmsizecod
    #// 
    #// @return int|false
    #//
    @classmethod
    def bitratelookup(self, frmsizecod_=None):
        
        
        #// LSB is whether padding is used or not
        padding_ = php_bool(frmsizecod_ & 1)
        framesizeid_ = frmsizecod_ & 62 >> 1
        bitrateLookup_ = Array({0: 32000, 1: 40000, 2: 48000, 3: 56000, 4: 64000, 5: 80000, 6: 96000, 7: 112000, 8: 128000, 9: 160000, 10: 192000, 11: 224000, 12: 256000, 13: 320000, 14: 384000, 15: 448000, 16: 512000, 17: 576000, 18: 640000})
        return bitrateLookup_[framesizeid_] if (php_isset(lambda : bitrateLookup_[framesizeid_])) else False
    # end def bitratelookup
    #// 
    #// @param int $numblkscod
    #// 
    #// @return int|false
    #//
    @classmethod
    def blockspersyncframe(self, numblkscod_=None):
        
        
        blocksPerSyncFrameLookup_ = Array({0: 1, 1: 2, 2: 3, 3: 6})
        return blocksPerSyncFrameLookup_[numblkscod_] if (php_isset(lambda : blocksPerSyncFrameLookup_[numblkscod_])) else False
    # end def blockspersyncframe
# end class getid3_ac3
