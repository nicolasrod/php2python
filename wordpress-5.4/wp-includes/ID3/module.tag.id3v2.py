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
#// module.tag.id3v2.php
#// module for analyzing ID3v2 tags
#// dependencies: module.tag.id3v1.php
#// 
#//
getid3_lib.includedependency(GETID3_INCLUDEPATH + "module.tag.id3v1.php", __FILE__, True)
class getid3_id3v2(getid3_handler):
    StartingOffset = 0
    #// 
    #// @return bool
    #//
    def analyze(self):
        
        
        info_ = self.getid3.info
        #// Overall tag structure:
        #// +-----------------------------+
        #// |      Header (10 bytes)      |
        #// +-----------------------------+
        #// |       Extended Header       |
        #// | (variable length, OPTIONAL) |
        #// +-----------------------------+
        #// |   Frames (variable length)  |
        #// +-----------------------------+
        #// |           Padding           |
        #// | (variable length, OPTIONAL) |
        #// +-----------------------------+
        #// | Footer (10 bytes, OPTIONAL) |
        #// +-----------------------------+
        #// Header
        #// ID3v2/file identifier      "ID3"
        #// ID3v2 version              $04 00
        #// ID3v2 flags                (%ab000000 in v2.2, %abc00000 in v2.3, %abcd0000 in v2.4.x)
        #// ID3v2 size             4 * %0xxxxxxx
        #// shortcuts
        info_["id3v2"]["header"] = True
        thisfile_id3v2_ = info_["id3v2"]
        thisfile_id3v2_["flags"] = Array()
        thisfile_id3v2_flags_ = thisfile_id3v2_["flags"]
        self.fseek(self.StartingOffset)
        header_ = self.fread(10)
        if php_substr(header_, 0, 3) == "ID3" and php_strlen(header_) == 10:
            thisfile_id3v2_["majorversion"] = php_ord(header_[3])
            thisfile_id3v2_["minorversion"] = php_ord(header_[4])
            #// shortcut
            id3v2_majorversion_ = thisfile_id3v2_["majorversion"]
        else:
            info_["id3v2"] = None
            return False
        # end if
        if id3v2_majorversion_ > 4:
            #// this script probably won't correctly parse ID3v2.5.x and above (if it ever exists)
            self.error("this script only parses up to ID3v2.4.x - this tag is ID3v2." + id3v2_majorversion_ + "." + thisfile_id3v2_["minorversion"])
            return False
        # end if
        id3_flags_ = php_ord(header_[5])
        for case in Switch(id3v2_majorversion_):
            if case(2):
                #// %ab000000 in v2.2
                thisfile_id3v2_flags_["unsynch"] = php_bool(id3_flags_ & 128)
                #// a - Unsynchronisation
                thisfile_id3v2_flags_["compression"] = php_bool(id3_flags_ & 64)
                break
            # end if
            if case(3):
                #// %abc00000 in v2.3
                thisfile_id3v2_flags_["unsynch"] = php_bool(id3_flags_ & 128)
                #// a - Unsynchronisation
                thisfile_id3v2_flags_["exthead"] = php_bool(id3_flags_ & 64)
                #// b - Extended header
                thisfile_id3v2_flags_["experim"] = php_bool(id3_flags_ & 32)
                break
            # end if
            if case(4):
                #// %abcd0000 in v2.4
                thisfile_id3v2_flags_["unsynch"] = php_bool(id3_flags_ & 128)
                #// a - Unsynchronisation
                thisfile_id3v2_flags_["exthead"] = php_bool(id3_flags_ & 64)
                #// b - Extended header
                thisfile_id3v2_flags_["experim"] = php_bool(id3_flags_ & 32)
                #// c - Experimental indicator
                thisfile_id3v2_flags_["isfooter"] = php_bool(id3_flags_ & 16)
                break
            # end if
        # end for
        thisfile_id3v2_["headerlength"] = getid3_lib.bigendian2int(php_substr(header_, 6, 4), 1) + 10
        #// length of ID3v2 tag in 10-byte header doesn't include 10-byte header length
        thisfile_id3v2_["tag_offset_start"] = self.StartingOffset
        thisfile_id3v2_["tag_offset_end"] = thisfile_id3v2_["tag_offset_start"] + thisfile_id3v2_["headerlength"]
        #// create 'encoding' key - used by getid3::HandleAllTags()
        #// in ID3v2 every field can have it's own encoding type
        #// so force everything to UTF-8 so it can be handled consistantly
        thisfile_id3v2_["encoding"] = "UTF-8"
        #// Frames
        #// All ID3v2 frames consists of one frame header followed by one or more
        #// fields containing the actual information. The header is always 10
        #// bytes and laid out as follows:
        #// 
        #// Frame ID      $xx xx xx xx  (four characters)
        #// Size      4 * %0xxxxxxx
        #// Flags         $xx xx
        sizeofframes_ = thisfile_id3v2_["headerlength"] - 10
        #// not including 10-byte initial header
        if (not php_empty(lambda : thisfile_id3v2_["exthead"]["length"])):
            sizeofframes_ -= thisfile_id3v2_["exthead"]["length"] + 4
        # end if
        if (not php_empty(lambda : thisfile_id3v2_flags_["isfooter"])):
            sizeofframes_ -= 10
            pass
        # end if
        if sizeofframes_ > 0:
            framedata_ = self.fread(sizeofframes_)
            #// read all frames from file into $framedata variable
            #// if entire frame data is unsynched, de-unsynch it now (ID3v2.3.x)
            if (not php_empty(lambda : thisfile_id3v2_flags_["unsynch"])) and id3v2_majorversion_ <= 3:
                framedata_ = self.deunsynchronise(framedata_)
            # end if
            #// [in ID3v2.4.0] Unsynchronisation [S:6.1] is done on frame level, instead
            #// of on tag level, making it easier to skip frames, increasing the streamability
            #// of the tag. The unsynchronisation flag in the header [S:3.1] indicates that
            #// there exists an unsynchronised frame, while the new unsynchronisation flag in
            #// the frame header [S:4.1.2] indicates unsynchronisation.
            #// $framedataoffset = 10 + ($thisfile_id3v2['exthead']['length'] ? $thisfile_id3v2['exthead']['length'] + 4 : 0); // how many bytes into the stream - start from after the 10-byte header (and extended header length+4, if present)
            framedataoffset_ = 10
            #// how many bytes into the stream - start from after the 10-byte header
            #// Extended Header
            if (not php_empty(lambda : thisfile_id3v2_flags_["exthead"])):
                extended_header_offset_ = 0
                if id3v2_majorversion_ == 3:
                    #// v2.3 definition:
                    #// Extended header size  $xx xx xx xx   // 32-bit integer
                    #// Extended Flags        $xx xx
                    #// %x0000000 %00000000 // v2.3
                    #// x - CRC data present
                    #// Size of padding       $xx xx xx xx
                    thisfile_id3v2_["exthead"]["length"] = getid3_lib.bigendian2int(php_substr(framedata_, extended_header_offset_, 4), 0)
                    extended_header_offset_ += 4
                    thisfile_id3v2_["exthead"]["flag_bytes"] = 2
                    thisfile_id3v2_["exthead"]["flag_raw"] = getid3_lib.bigendian2int(php_substr(framedata_, extended_header_offset_, thisfile_id3v2_["exthead"]["flag_bytes"]))
                    extended_header_offset_ += thisfile_id3v2_["exthead"]["flag_bytes"]
                    thisfile_id3v2_["exthead"]["flags"]["crc"] = php_bool(thisfile_id3v2_["exthead"]["flag_raw"] & 32768)
                    thisfile_id3v2_["exthead"]["padding_size"] = getid3_lib.bigendian2int(php_substr(framedata_, extended_header_offset_, 4))
                    extended_header_offset_ += 4
                    if thisfile_id3v2_["exthead"]["flags"]["crc"]:
                        thisfile_id3v2_["exthead"]["flag_data"]["crc"] = getid3_lib.bigendian2int(php_substr(framedata_, extended_header_offset_, 4))
                        extended_header_offset_ += 4
                    # end if
                    extended_header_offset_ += thisfile_id3v2_["exthead"]["padding_size"]
                elif id3v2_majorversion_ == 4:
                    #// v2.4 definition:
                    #// Extended header size   4 * %0xxxxxxx // 28-bit synchsafe integer
                    #// Number of flag bytes       $01
                    #// Extended Flags             $xx
                    #// %0bcd0000 // v2.4
                    #// b - Tag is an update
                    #// Flag data length       $00
                    #// c - CRC data present
                    #// Flag data length       $05
                    #// Total frame CRC    5 * %0xxxxxxx
                    #// d - Tag restrictions
                    #// Flag data length       $01
                    thisfile_id3v2_["exthead"]["length"] = getid3_lib.bigendian2int(php_substr(framedata_, extended_header_offset_, 4), True)
                    extended_header_offset_ += 4
                    thisfile_id3v2_["exthead"]["flag_bytes"] = getid3_lib.bigendian2int(php_substr(framedata_, extended_header_offset_, 1))
                    #// should always be 1
                    extended_header_offset_ += 1
                    thisfile_id3v2_["exthead"]["flag_raw"] = getid3_lib.bigendian2int(php_substr(framedata_, extended_header_offset_, thisfile_id3v2_["exthead"]["flag_bytes"]))
                    extended_header_offset_ += thisfile_id3v2_["exthead"]["flag_bytes"]
                    thisfile_id3v2_["exthead"]["flags"]["update"] = php_bool(thisfile_id3v2_["exthead"]["flag_raw"] & 64)
                    thisfile_id3v2_["exthead"]["flags"]["crc"] = php_bool(thisfile_id3v2_["exthead"]["flag_raw"] & 32)
                    thisfile_id3v2_["exthead"]["flags"]["restrictions"] = php_bool(thisfile_id3v2_["exthead"]["flag_raw"] & 16)
                    if thisfile_id3v2_["exthead"]["flags"]["update"]:
                        ext_header_chunk_length_ = getid3_lib.bigendian2int(php_substr(framedata_, extended_header_offset_, 1))
                        #// should be 0
                        extended_header_offset_ += 1
                    # end if
                    if thisfile_id3v2_["exthead"]["flags"]["crc"]:
                        ext_header_chunk_length_ = getid3_lib.bigendian2int(php_substr(framedata_, extended_header_offset_, 1))
                        #// should be 5
                        extended_header_offset_ += 1
                        thisfile_id3v2_["exthead"]["flag_data"]["crc"] = getid3_lib.bigendian2int(php_substr(framedata_, extended_header_offset_, ext_header_chunk_length_), True, False)
                        extended_header_offset_ += ext_header_chunk_length_
                    # end if
                    if thisfile_id3v2_["exthead"]["flags"]["restrictions"]:
                        ext_header_chunk_length_ = getid3_lib.bigendian2int(php_substr(framedata_, extended_header_offset_, 1))
                        #// should be 1
                        extended_header_offset_ += 1
                        #// %ppqrrstt
                        restrictions_raw_ = getid3_lib.bigendian2int(php_substr(framedata_, extended_header_offset_, 1))
                        extended_header_offset_ += 1
                        thisfile_id3v2_["exthead"]["flags"]["restrictions"]["tagsize"] = restrictions_raw_ & 192 >> 6
                        #// p - Tag size restrictions
                        thisfile_id3v2_["exthead"]["flags"]["restrictions"]["textenc"] = restrictions_raw_ & 32 >> 5
                        #// q - Text encoding restrictions
                        thisfile_id3v2_["exthead"]["flags"]["restrictions"]["textsize"] = restrictions_raw_ & 24 >> 3
                        #// r - Text fields size restrictions
                        thisfile_id3v2_["exthead"]["flags"]["restrictions"]["imgenc"] = restrictions_raw_ & 4 >> 2
                        #// s - Image encoding restrictions
                        thisfile_id3v2_["exthead"]["flags"]["restrictions"]["imgsize"] = restrictions_raw_ & 3 >> 0
                        #// t - Image size restrictions
                        thisfile_id3v2_["exthead"]["flags"]["restrictions_text"]["tagsize"] = self.lookupextendedheaderrestrictionstagsizelimits(thisfile_id3v2_["exthead"]["flags"]["restrictions"]["tagsize"])
                        thisfile_id3v2_["exthead"]["flags"]["restrictions_text"]["textenc"] = self.lookupextendedheaderrestrictionstextencodings(thisfile_id3v2_["exthead"]["flags"]["restrictions"]["textenc"])
                        thisfile_id3v2_["exthead"]["flags"]["restrictions_text"]["textsize"] = self.lookupextendedheaderrestrictionstextfieldsize(thisfile_id3v2_["exthead"]["flags"]["restrictions"]["textsize"])
                        thisfile_id3v2_["exthead"]["flags"]["restrictions_text"]["imgenc"] = self.lookupextendedheaderrestrictionsimageencoding(thisfile_id3v2_["exthead"]["flags"]["restrictions"]["imgenc"])
                        thisfile_id3v2_["exthead"]["flags"]["restrictions_text"]["imgsize"] = self.lookupextendedheaderrestrictionsimagesizesize(thisfile_id3v2_["exthead"]["flags"]["restrictions"]["imgsize"])
                    # end if
                    if thisfile_id3v2_["exthead"]["length"] != extended_header_offset_:
                        self.warning("ID3v2.4 extended header length mismatch (expecting " + php_intval(thisfile_id3v2_["exthead"]["length"]) + ", found " + php_intval(extended_header_offset_) + ")")
                    # end if
                # end if
                framedataoffset_ += extended_header_offset_
                framedata_ = php_substr(framedata_, extended_header_offset_)
            # end if
            #// end extended header
            while True:
                
                if not ((php_isset(lambda : framedata_)) and php_strlen(framedata_) > 0):
                    break
                # end if
                #// cycle through until no more frame data is left to parse
                if php_strlen(framedata_) <= self.id3v2headerlength(id3v2_majorversion_):
                    #// insufficient room left in ID3v2 header for actual data - must be padding
                    thisfile_id3v2_["padding"]["start"] = framedataoffset_
                    thisfile_id3v2_["padding"]["length"] = php_strlen(framedata_)
                    thisfile_id3v2_["padding"]["valid"] = True
                    i_ = 0
                    while i_ < thisfile_id3v2_["padding"]["length"]:
                        
                        if framedata_[i_] != " ":
                            thisfile_id3v2_["padding"]["valid"] = False
                            thisfile_id3v2_["padding"]["errorpos"] = thisfile_id3v2_["padding"]["start"] + i_
                            self.warning("Invalid ID3v2 padding found at offset " + thisfile_id3v2_["padding"]["errorpos"] + " (the remaining " + thisfile_id3v2_["padding"]["length"] - i_ + " bytes are considered invalid)")
                            break
                        # end if
                        i_ += 1
                    # end while
                    break
                    pass
                # end if
                frame_header_ = None
                frame_name_ = None
                frame_size_ = None
                frame_flags_ = None
                if id3v2_majorversion_ == 2:
                    #// Frame ID  $xx xx xx (three characters)
                    #// Size      $xx xx xx (24-bit integer)
                    #// Flags     $xx xx
                    frame_header_ = php_substr(framedata_, 0, 6)
                    #// take next 6 bytes for header
                    framedata_ = php_substr(framedata_, 6)
                    #// and leave the rest in $framedata
                    frame_name_ = php_substr(frame_header_, 0, 3)
                    frame_size_ = getid3_lib.bigendian2int(php_substr(frame_header_, 3, 3), 0)
                    frame_flags_ = 0
                    pass
                elif id3v2_majorversion_ > 2:
                    #// Frame ID  $xx xx xx xx (four characters)
                    #// Size      $xx xx xx xx (32-bit integer in v2.3, 28-bit synchsafe in v2.4+)
                    #// Flags     $xx xx
                    frame_header_ = php_substr(framedata_, 0, 10)
                    #// take next 10 bytes for header
                    framedata_ = php_substr(framedata_, 10)
                    #// and leave the rest in $framedata
                    frame_name_ = php_substr(frame_header_, 0, 4)
                    if id3v2_majorversion_ == 3:
                        frame_size_ = getid3_lib.bigendian2int(php_substr(frame_header_, 4, 4), 0)
                        pass
                    else:
                        #// ID3v2.4+
                        frame_size_ = getid3_lib.bigendian2int(php_substr(frame_header_, 4, 4), 1)
                        pass
                    # end if
                    if frame_size_ < php_strlen(framedata_) + 4:
                        nextFrameID_ = php_substr(framedata_, frame_size_, 4)
                        if self.isvalidid3v2framename(nextFrameID_, id3v2_majorversion_):
                            pass
                        elif frame_name_ == " " + "MP3" or frame_name_ == "  " + "MP" or frame_name_ == " MP3" or frame_name_ == "MP3e":
                            pass
                        elif id3v2_majorversion_ == 4 and self.isvalidid3v2framename(php_substr(framedata_, getid3_lib.bigendian2int(php_substr(frame_header_, 4, 4), 0), 4), 3):
                            self.warning("ID3v2 tag written as ID3v2.4, but with non-synchsafe integers (ID3v2.3 style). Older versions of (Helium2; iTunes) are known culprits of this. Tag has been parsed as ID3v2.3")
                            id3v2_majorversion_ = 3
                            frame_size_ = getid3_lib.bigendian2int(php_substr(frame_header_, 4, 4), 0)
                            pass
                        # end if
                    # end if
                    frame_flags_ = getid3_lib.bigendian2int(php_substr(frame_header_, 8, 2))
                # end if
                if id3v2_majorversion_ == 2 and frame_name_ == "   " or frame_name_ == "    ":
                    #// padding encountered
                    thisfile_id3v2_["padding"]["start"] = framedataoffset_
                    thisfile_id3v2_["padding"]["length"] = php_strlen(frame_header_) + php_strlen(framedata_)
                    thisfile_id3v2_["padding"]["valid"] = True
                    len_ = php_strlen(framedata_)
                    i_ = 0
                    while i_ < len_:
                        
                        if framedata_[i_] != " ":
                            thisfile_id3v2_["padding"]["valid"] = False
                            thisfile_id3v2_["padding"]["errorpos"] = thisfile_id3v2_["padding"]["start"] + i_
                            self.warning("Invalid ID3v2 padding found at offset " + thisfile_id3v2_["padding"]["errorpos"] + " (the remaining " + thisfile_id3v2_["padding"]["length"] - i_ + " bytes are considered invalid)")
                            break
                        # end if
                        i_ += 1
                    # end while
                    break
                    pass
                # end if
                iTunesBrokenFrameNameFixed_ = self.id3v22itunesbrokenframename(frame_name_)
                if iTunesBrokenFrameNameFixed_:
                    self.warning("error parsing \"" + frame_name_ + "\" (" + framedataoffset_ + " bytes into the ID3v2." + id3v2_majorversion_ + " tag). (ERROR: IsValidID3v2FrameName(\"" + php_str_replace(" ", " ", frame_name_) + "\", " + id3v2_majorversion_ + "))). [Note: this particular error has been known to happen with tags edited by iTunes (versions \"X v2.0.3\", \"v3.0.1\", \"v7.0.0.70\" are known-guilty, probably others too)]. Translated frame name from \"" + php_str_replace(" ", " ", frame_name_) + "\" to \"" + iTunesBrokenFrameNameFixed_ + "\" for parsing.")
                    frame_name_ = iTunesBrokenFrameNameFixed_
                # end if
                if frame_size_ <= php_strlen(framedata_) and self.isvalidid3v2framename(frame_name_, id3v2_majorversion_):
                    parsedFrame_ = None
                    parsedFrame_["frame_name"] = frame_name_
                    parsedFrame_["frame_flags_raw"] = frame_flags_
                    parsedFrame_["data"] = php_substr(framedata_, 0, frame_size_)
                    parsedFrame_["datalength"] = getid3_lib.castasint(frame_size_)
                    parsedFrame_["dataoffset"] = framedataoffset_
                    self.parseid3v2frame(parsedFrame_)
                    thisfile_id3v2_[frame_name_][-1] = parsedFrame_
                    framedata_ = php_substr(framedata_, frame_size_)
                else:
                    #// invalid frame length or FrameID
                    if frame_size_ <= php_strlen(framedata_):
                        if self.isvalidid3v2framename(php_substr(framedata_, frame_size_, 4), id3v2_majorversion_):
                            #// next frame is valid, just skip the current frame
                            framedata_ = php_substr(framedata_, frame_size_)
                            self.warning("Next ID3v2 frame is valid, skipping current frame.")
                        else:
                            #// next frame is invalid too, abort processing
                            #// unset($framedata);
                            framedata_ = None
                            self.error("Next ID3v2 frame is also invalid, aborting processing.")
                        # end if
                    elif frame_size_ == php_strlen(framedata_):
                        #// this is the last frame, just skip
                        self.warning("This was the last ID3v2 frame.")
                    else:
                        #// next frame is invalid too, abort processing
                        #// unset($framedata);
                        framedata_ = None
                        self.warning("Invalid ID3v2 frame size, aborting.")
                    # end if
                    if (not self.isvalidid3v2framename(frame_name_, id3v2_majorversion_)):
                        for case in Switch(frame_name_):
                            if case("  " + "MP"):
                                pass
                            # end if
                            if case(" " + "MP3"):
                                pass
                            # end if
                            if case(" MP3"):
                                pass
                            # end if
                            if case("MP3e"):
                                pass
                            # end if
                            if case(" " + "MP"):
                                pass
                            # end if
                            if case(" MP"):
                                pass
                            # end if
                            if case("MP3"):
                                self.warning("error parsing \"" + frame_name_ + "\" (" + framedataoffset_ + " bytes into the ID3v2." + id3v2_majorversion_ + " tag). (ERROR: !IsValidID3v2FrameName(\"" + php_str_replace(" ", " ", frame_name_) + "\", " + id3v2_majorversion_ + "))). [Note: this particular error has been known to happen with tags edited by \"MP3ext (www.mutschler.de/mp3ext/)\"]")
                                break
                            # end if
                            if case():
                                self.warning("error parsing \"" + frame_name_ + "\" (" + framedataoffset_ + " bytes into the ID3v2." + id3v2_majorversion_ + " tag). (ERROR: !IsValidID3v2FrameName(\"" + php_str_replace(" ", " ", frame_name_) + "\", " + id3v2_majorversion_ + "))).")
                                break
                            # end if
                        # end for
                    elif (not (php_isset(lambda : framedata_))) or frame_size_ > php_strlen(framedata_):
                        self.error("error parsing \"" + frame_name_ + "\" (" + framedataoffset_ + " bytes into the ID3v2." + id3v2_majorversion_ + " tag). (ERROR: $frame_size (" + frame_size_ + ") > strlen($framedata) (" + php_strlen(framedata_) if (php_isset(lambda : framedata_)) else "null" + ")).")
                    else:
                        self.error("error parsing \"" + frame_name_ + "\" (" + framedataoffset_ + " bytes into the ID3v2." + id3v2_majorversion_ + " tag).")
                    # end if
                # end if
                framedataoffset_ += frame_size_ + self.id3v2headerlength(id3v2_majorversion_)
            # end while
        # end if
        #// Footer
        #// The footer is a copy of the header, but with a different identifier.
        #// ID3v2 identifier           "3DI"
        #// ID3v2 version              $04 00
        #// ID3v2 flags                %abcd0000
        #// ID3v2 size             4 * %0xxxxxxx
        if (php_isset(lambda : thisfile_id3v2_flags_["isfooter"])) and thisfile_id3v2_flags_["isfooter"]:
            footer_ = self.fread(10)
            if php_substr(footer_, 0, 3) == "3DI":
                thisfile_id3v2_["footer"] = True
                thisfile_id3v2_["majorversion_footer"] = php_ord(footer_[3])
                thisfile_id3v2_["minorversion_footer"] = php_ord(footer_[4])
            # end if
            if thisfile_id3v2_["majorversion_footer"] <= 4:
                id3_flags_ = php_ord(footer_[5])
                thisfile_id3v2_flags_["unsynch_footer"] = php_bool(id3_flags_ & 128)
                thisfile_id3v2_flags_["extfoot_footer"] = php_bool(id3_flags_ & 64)
                thisfile_id3v2_flags_["experim_footer"] = php_bool(id3_flags_ & 32)
                thisfile_id3v2_flags_["isfooter_footer"] = php_bool(id3_flags_ & 16)
                thisfile_id3v2_["footerlength"] = getid3_lib.bigendian2int(php_substr(footer_, 6, 4), 1)
            # end if
        # end if
        #// end footer
        if (php_isset(lambda : thisfile_id3v2_["comments"]["genre"])):
            genres_ = Array()
            for key_,value_ in thisfile_id3v2_["comments"]["genre"].items():
                for genre_ in self.parseid3v2genrestring(value_):
                    genres_[-1] = genre_
                # end for
            # end for
            thisfile_id3v2_["comments"]["genre"] = array_unique(genres_)
            key_ = None
            value_ = None
            genres_ = None
            genre_ = None
        # end if
        if (php_isset(lambda : thisfile_id3v2_["comments"]["track_number"])):
            for key_,value_ in thisfile_id3v2_["comments"]["track_number"].items():
                if php_strstr(value_, "/"):
                    thisfile_id3v2_["comments"]["track_number"][key_], thisfile_id3v2_["comments"]["totaltracks"][key_] = php_explode("/", thisfile_id3v2_["comments"]["track_number"][key_])
                # end if
            # end for
        # end if
        if (not (php_isset(lambda : thisfile_id3v2_["comments"]["year"]))) and (not php_empty(lambda : thisfile_id3v2_["comments"]["recording_time"][0])) and php_preg_match("#^([0-9]{4})#", php_trim(thisfile_id3v2_["comments"]["recording_time"][0]), matches_):
            thisfile_id3v2_["comments"]["year"] = Array(matches_[1])
        # end if
        if (not php_empty(lambda : thisfile_id3v2_["TXXX"])):
            #// MediaMonkey does this, maybe others: write a blank RGAD frame, but put replay-gain adjustment values in TXXX frames
            for txxx_array_ in thisfile_id3v2_["TXXX"]:
                for case in Switch(txxx_array_["description"]):
                    if case("replaygain_track_gain"):
                        if php_empty(lambda : info_["replay_gain"]["track"]["adjustment"]) and (not php_empty(lambda : txxx_array_["data"])):
                            info_["replay_gain"]["track"]["adjustment"] = floatval(php_trim(php_str_replace("dB", "", txxx_array_["data"])))
                        # end if
                        break
                    # end if
                    if case("replaygain_track_peak"):
                        if php_empty(lambda : info_["replay_gain"]["track"]["peak"]) and (not php_empty(lambda : txxx_array_["data"])):
                            info_["replay_gain"]["track"]["peak"] = floatval(txxx_array_["data"])
                        # end if
                        break
                    # end if
                    if case("replaygain_album_gain"):
                        if php_empty(lambda : info_["replay_gain"]["album"]["adjustment"]) and (not php_empty(lambda : txxx_array_["data"])):
                            info_["replay_gain"]["album"]["adjustment"] = floatval(php_trim(php_str_replace("dB", "", txxx_array_["data"])))
                        # end if
                        break
                    # end if
                # end for
            # end for
        # end if
        #// Set avdataoffset
        info_["avdataoffset"] = thisfile_id3v2_["headerlength"]
        if (php_isset(lambda : thisfile_id3v2_["footer"])):
            info_["avdataoffset"] += 10
        # end if
        return True
    # end def analyze
    #// 
    #// @param string $genrestring
    #// 
    #// @return array
    #//
    def parseid3v2genrestring(self, genrestring_=None):
        
        
        #// Parse genres into arrays of genreName and genreID
        #// ID3v2.2.x, ID3v2.3.x: '(21)' or '(4)Eurodisco' or '(51)(39)' or '(55)((I think...)'
        #// ID3v2.4.x: '21' $00 'Eurodisco' $00
        clean_genres_ = Array()
        #// hack-fixes for some badly-written ID3v2.3 taggers, while trying not to break correctly-written tags
        if self.getid3.info["id3v2"]["majorversion"] == 3 and (not php_preg_match("#[\\x00]#", genrestring_)):
            #// note: MusicBrainz Picard incorrectly stores plaintext genres separated by "/" when writing in ID3v2.3 mode, hack-fix here:
            #// replace / with NULL, then replace back the two ID3v1 genres that legitimately have "/" as part of the single genre name
            if php_preg_match("#/#", genrestring_):
                genrestring_ = php_str_replace("/", " ", genrestring_)
                genrestring_ = php_str_replace("Pop" + " " + "Funk", "Pop/Funk", genrestring_)
                genrestring_ = php_str_replace("Rock" + " " + "Rock", "Folk/Rock", genrestring_)
            # end if
            #// some other taggers separate multiple genres with semicolon, e.g. "Heavy Metal;Thrash Metal;Metal"
            if php_preg_match("#;#", genrestring_):
                genrestring_ = php_str_replace(";", " ", genrestring_)
            # end if
        # end if
        if php_strpos(genrestring_, " ") == False:
            genrestring_ = php_preg_replace("#\\(([0-9]{1,3})\\)#", "$1" + " ", genrestring_)
        # end if
        genre_elements_ = php_explode(" ", genrestring_)
        for element_ in genre_elements_:
            element_ = php_trim(element_)
            if element_:
                if php_preg_match("#^[0-9]{1,3}$#", element_):
                    clean_genres_[-1] = getid3_id3v1.lookupgenrename(element_)
                else:
                    clean_genres_[-1] = php_str_replace("((", "(", element_)
                # end if
            # end if
        # end for
        return clean_genres_
    # end def parseid3v2genrestring
    #// 
    #// @param array $parsedFrame
    #// 
    #// @return bool
    #//
    def parseid3v2frame(self, parsedFrame_=None):
        
        
        #// shortcuts
        info_ = self.getid3.info
        id3v2_majorversion_ = info_["id3v2"]["majorversion"]
        parsedFrame_["framenamelong"] = self.framenamelonglookup(parsedFrame_["frame_name"])
        if php_empty(lambda : parsedFrame_["framenamelong"]):
            parsedFrame_["framenamelong"] = None
        # end if
        parsedFrame_["framenameshort"] = self.framenameshortlookup(parsedFrame_["frame_name"])
        if php_empty(lambda : parsedFrame_["framenameshort"]):
            parsedFrame_["framenameshort"] = None
        # end if
        if id3v2_majorversion_ >= 3:
            #// frame flags are not part of the ID3v2.2 standard
            if id3v2_majorversion_ == 3:
                #// Frame Header Flags
                #// %abc00000 %ijk00000
                parsedFrame_["flags"]["TagAlterPreservation"] = php_bool(parsedFrame_["frame_flags_raw"] & 32768)
                #// a - Tag alter preservation
                parsedFrame_["flags"]["FileAlterPreservation"] = php_bool(parsedFrame_["frame_flags_raw"] & 16384)
                #// b - File alter preservation
                parsedFrame_["flags"]["ReadOnly"] = php_bool(parsedFrame_["frame_flags_raw"] & 8192)
                #// c - Read only
                parsedFrame_["flags"]["compression"] = php_bool(parsedFrame_["frame_flags_raw"] & 128)
                #// i - Compression
                parsedFrame_["flags"]["Encryption"] = php_bool(parsedFrame_["frame_flags_raw"] & 64)
                #// j - Encryption
                parsedFrame_["flags"]["GroupingIdentity"] = php_bool(parsedFrame_["frame_flags_raw"] & 32)
                pass
            elif id3v2_majorversion_ == 4:
                #// Frame Header Flags
                #// %0abc0000 %0h00kmnp
                parsedFrame_["flags"]["TagAlterPreservation"] = php_bool(parsedFrame_["frame_flags_raw"] & 16384)
                #// a - Tag alter preservation
                parsedFrame_["flags"]["FileAlterPreservation"] = php_bool(parsedFrame_["frame_flags_raw"] & 8192)
                #// b - File alter preservation
                parsedFrame_["flags"]["ReadOnly"] = php_bool(parsedFrame_["frame_flags_raw"] & 4096)
                #// c - Read only
                parsedFrame_["flags"]["GroupingIdentity"] = php_bool(parsedFrame_["frame_flags_raw"] & 64)
                #// h - Grouping identity
                parsedFrame_["flags"]["compression"] = php_bool(parsedFrame_["frame_flags_raw"] & 8)
                #// k - Compression
                parsedFrame_["flags"]["Encryption"] = php_bool(parsedFrame_["frame_flags_raw"] & 4)
                #// m - Encryption
                parsedFrame_["flags"]["Unsynchronisation"] = php_bool(parsedFrame_["frame_flags_raw"] & 2)
                #// n - Unsynchronisation
                parsedFrame_["flags"]["DataLengthIndicator"] = php_bool(parsedFrame_["frame_flags_raw"] & 1)
                #// p - Data length indicator
                #// Frame-level de-unsynchronisation - ID3v2.4
                if parsedFrame_["flags"]["Unsynchronisation"]:
                    parsedFrame_["data"] = self.deunsynchronise(parsedFrame_["data"])
                # end if
                if parsedFrame_["flags"]["DataLengthIndicator"]:
                    parsedFrame_["data_length_indicator"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], 0, 4), 1)
                    parsedFrame_["data"] = php_substr(parsedFrame_["data"], 4)
                # end if
            # end if
            #// Frame-level de-compression
            if parsedFrame_["flags"]["compression"]:
                parsedFrame_["decompressed_size"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], 0, 4))
                if (not php_function_exists("gzuncompress")):
                    self.warning("gzuncompress() support required to decompress ID3v2 frame \"" + parsedFrame_["frame_name"] + "\"")
                else:
                    decompresseddata_ = php_no_error(lambda: gzuncompress(php_substr(parsedFrame_["data"], 4)))
                    if decompresseddata_:
                        #// if ($decompresseddata = @gzuncompress($parsedFrame['data'])) {
                        parsedFrame_["data"] = decompresseddata_
                        decompresseddata_ = None
                    else:
                        self.warning("gzuncompress() failed on compressed contents of ID3v2 frame \"" + parsedFrame_["frame_name"] + "\"")
                    # end if
                # end if
            # end if
        # end if
        if (not php_empty(lambda : parsedFrame_["flags"]["DataLengthIndicator"])):
            if parsedFrame_["data_length_indicator"] != php_strlen(parsedFrame_["data"]):
                self.warning("ID3v2 frame \"" + parsedFrame_["frame_name"] + "\" should be " + parsedFrame_["data_length_indicator"] + " bytes long according to DataLengthIndicator, but found " + php_strlen(parsedFrame_["data"]) + " bytes of data")
            # end if
        # end if
        if (php_isset(lambda : parsedFrame_["datalength"])) and parsedFrame_["datalength"] == 0:
            warning_ = "Frame \"" + parsedFrame_["frame_name"] + "\" at offset " + parsedFrame_["dataoffset"] + " has no data portion"
            for case in Switch(parsedFrame_["frame_name"]):
                if case("WCOM"):
                    warning_ += " (this is known to happen with files tagged by RioPort)"
                    break
                # end if
                if case():
                    break
                # end if
            # end for
            self.warning(warning_)
        elif id3v2_majorversion_ >= 3 and parsedFrame_["frame_name"] == "UFID" or id3v2_majorversion_ == 2 and parsedFrame_["frame_name"] == "UFI":
            #// 4.1   UFI  Unique file identifier
            #// There may be more than one 'UFID' frame in a tag,
            #// but only one with the same 'Owner identifier'.
            #// <Header for 'Unique file identifier', ID: 'UFID'>
            #// Owner identifier        <text string> $00
            #// Identifier              <up to 64 bytes binary data>
            exploded_ = php_explode(" ", parsedFrame_["data"], 2)
            parsedFrame_["ownerid"] = exploded_[0] if (php_isset(lambda : exploded_[0])) else ""
            parsedFrame_["data"] = exploded_[1] if (php_isset(lambda : exploded_[1])) else ""
        elif id3v2_majorversion_ >= 3 and parsedFrame_["frame_name"] == "TXXX" or id3v2_majorversion_ == 2 and parsedFrame_["frame_name"] == "TXX":
            #// 4.2.2 TXX  User defined text information frame
            #// There may be more than one 'TXXX' frame in each tag,
            #// but only one with the same description.
            #// <Header for 'User defined text information frame', ID: 'TXXX'>
            #// Text encoding     $xx
            #// Description       <text string according to encoding> $00 (00)
            #// Value             <text string according to encoding>
            frame_offset_ = 0
            frame_textencoding_ = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            frame_offset_ += 1
            frame_textencoding_terminator_ = self.textencodingterminatorlookup(frame_textencoding_)
            if id3v2_majorversion_ <= 3 and frame_textencoding_ > 1 or id3v2_majorversion_ == 4 and frame_textencoding_ > 3:
                self.warning("Invalid text encoding byte (" + frame_textencoding_ + ") in frame \"" + parsedFrame_["frame_name"] + "\" - defaulting to ISO-8859-1 encoding")
                frame_textencoding_terminator_ = " "
            # end if
            frame_terminatorpos_ = php_strpos(parsedFrame_["data"], frame_textencoding_terminator_, frame_offset_)
            if php_ord(php_substr(parsedFrame_["data"], frame_terminatorpos_ + php_strlen(frame_textencoding_terminator_), 1)) == 0:
                frame_terminatorpos_ += 1
                pass
            # end if
            parsedFrame_["description"] = php_substr(parsedFrame_["data"], frame_offset_, frame_terminatorpos_ - frame_offset_)
            parsedFrame_["description"] = self.makeutf16emptystringempty(parsedFrame_["description"])
            parsedFrame_["encodingid"] = frame_textencoding_
            parsedFrame_["encoding"] = self.textencodingnamelookup(frame_textencoding_)
            parsedFrame_["description"] = php_trim(getid3_lib.iconv_fallback(parsedFrame_["encoding"], info_["id3v2"]["encoding"], parsedFrame_["description"]))
            parsedFrame_["data"] = php_substr(parsedFrame_["data"], frame_terminatorpos_ + php_strlen(frame_textencoding_terminator_))
            parsedFrame_["data"] = self.removestringterminator(parsedFrame_["data"], frame_textencoding_terminator_)
            if (not php_empty(lambda : parsedFrame_["framenameshort"])) and (not php_empty(lambda : parsedFrame_["data"])):
                commentkey_ = parsedFrame_["description"] if parsedFrame_["description"] else php_count(info_["id3v2"]["comments"][parsedFrame_["framenameshort"]]) if (php_isset(lambda : info_["id3v2"]["comments"][parsedFrame_["framenameshort"]])) else 0
                if (not (php_isset(lambda : info_["id3v2"]["comments"][parsedFrame_["framenameshort"]]))) or (not php_array_key_exists(commentkey_, info_["id3v2"]["comments"][parsedFrame_["framenameshort"]])):
                    info_["id3v2"]["comments"][parsedFrame_["framenameshort"]][commentkey_] = php_trim(getid3_lib.iconv_fallback(parsedFrame_["encoding"], info_["id3v2"]["encoding"], parsedFrame_["data"]))
                else:
                    info_["id3v2"]["comments"][parsedFrame_["framenameshort"]][-1] = php_trim(getid3_lib.iconv_fallback(parsedFrame_["encoding"], info_["id3v2"]["encoding"], parsedFrame_["data"]))
                # end if
            # end if
            pass
        elif parsedFrame_["frame_name"][0] == "T":
            #// 4.2. T??[?] Text information frame
            #// There may only be one text information frame of its kind in an tag.
            #// <Header for 'Text information frame', ID: 'T000' - 'TZZZ',
            #// excluding 'TXXX' described in 4.2.6.>
            #// Text encoding                $xx
            #// Information                  <text string(s) according to encoding>
            frame_offset_ = 0
            frame_textencoding_ = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            frame_offset_ += 1
            if id3v2_majorversion_ <= 3 and frame_textencoding_ > 1 or id3v2_majorversion_ == 4 and frame_textencoding_ > 3:
                self.warning("Invalid text encoding byte (" + frame_textencoding_ + ") in frame \"" + parsedFrame_["frame_name"] + "\" - defaulting to ISO-8859-1 encoding")
            # end if
            parsedFrame_["data"] = php_str(php_substr(parsedFrame_["data"], frame_offset_))
            parsedFrame_["data"] = self.removestringterminator(parsedFrame_["data"], self.textencodingterminatorlookup(frame_textencoding_))
            parsedFrame_["encodingid"] = frame_textencoding_
            parsedFrame_["encoding"] = self.textencodingnamelookup(frame_textencoding_)
            if (not php_empty(lambda : parsedFrame_["framenameshort"])) and (not php_empty(lambda : parsedFrame_["data"])):
                #// ID3v2.3 specs say that TPE1 (and others) can contain multiple artist values separated with
                #// This of course breaks when an artist name contains slash character, e.g. "AC/DC"
                #// MP3tag (maybe others) implement alternative system where multiple artists are null-separated, which makes more sense
                #// getID3 will split null-separated artists into multiple artists and leave slash-separated ones to the user
                for case in Switch(parsedFrame_["encoding"]):
                    if case("UTF-16"):
                        pass
                    # end if
                    if case("UTF-16BE"):
                        pass
                    # end if
                    if case("UTF-16LE"):
                        wordsize_ = 2
                        break
                    # end if
                    if case("ISO-8859-1"):
                        pass
                    # end if
                    if case("UTF-8"):
                        pass
                    # end if
                    if case():
                        wordsize_ = 1
                        break
                    # end if
                # end for
                Txxx_elements_ = Array()
                Txxx_elements_start_offset_ = 0
                i_ = 0
                while i_ < php_strlen(parsedFrame_["data"]):
                    
                    if php_substr(parsedFrame_["data"], i_, wordsize_) == php_str_repeat(" ", wordsize_):
                        Txxx_elements_[-1] = php_substr(parsedFrame_["data"], Txxx_elements_start_offset_, i_ - Txxx_elements_start_offset_)
                        Txxx_elements_start_offset_ = i_ + wordsize_
                    # end if
                    i_ += wordsize_
                # end while
                Txxx_elements_[-1] = php_substr(parsedFrame_["data"], Txxx_elements_start_offset_, i_ - Txxx_elements_start_offset_)
                for Txxx_element_ in Txxx_elements_:
                    string_ = getid3_lib.iconv_fallback(parsedFrame_["encoding"], info_["id3v2"]["encoding"], Txxx_element_)
                    if (not php_empty(lambda : string_)):
                        info_["id3v2"]["comments"][parsedFrame_["framenameshort"]][-1] = string_
                    # end if
                # end for
                string_ = None
                wordsize_ = None
                i_ = None
                Txxx_elements_ = None
                Txxx_element_ = None
                Txxx_elements_start_offset_ = None
            # end if
        elif id3v2_majorversion_ >= 3 and parsedFrame_["frame_name"] == "WXXX" or id3v2_majorversion_ == 2 and parsedFrame_["frame_name"] == "WXX":
            #// 4.3.2 WXX  User defined URL link frame
            #// There may be more than one 'WXXX' frame in each tag,
            #// but only one with the same description
            #// <Header for 'User defined URL link frame', ID: 'WXXX'>
            #// Text encoding     $xx
            #// Description       <text string according to encoding> $00 (00)
            #// URL               <text string>
            frame_offset_ = 0
            frame_textencoding_ = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            frame_offset_ += 1
            frame_textencoding_terminator_ = self.textencodingterminatorlookup(frame_textencoding_)
            if id3v2_majorversion_ <= 3 and frame_textencoding_ > 1 or id3v2_majorversion_ == 4 and frame_textencoding_ > 3:
                self.warning("Invalid text encoding byte (" + frame_textencoding_ + ") in frame \"" + parsedFrame_["frame_name"] + "\" - defaulting to ISO-8859-1 encoding")
                frame_textencoding_terminator_ = " "
            # end if
            frame_terminatorpos_ = php_strpos(parsedFrame_["data"], frame_textencoding_terminator_, frame_offset_)
            if php_ord(php_substr(parsedFrame_["data"], frame_terminatorpos_ + php_strlen(frame_textencoding_terminator_), 1)) == 0:
                frame_terminatorpos_ += 1
                pass
            # end if
            parsedFrame_["encodingid"] = frame_textencoding_
            parsedFrame_["encoding"] = self.textencodingnamelookup(frame_textencoding_)
            parsedFrame_["description"] = php_substr(parsedFrame_["data"], frame_offset_, frame_terminatorpos_ - frame_offset_)
            #// according to the frame text encoding
            parsedFrame_["url"] = php_substr(parsedFrame_["data"], frame_terminatorpos_ + php_strlen(frame_textencoding_terminator_))
            #// always ISO-8859-1
            parsedFrame_["description"] = self.removestringterminator(parsedFrame_["description"], frame_textencoding_terminator_)
            parsedFrame_["description"] = self.makeutf16emptystringempty(parsedFrame_["description"])
            if (not php_empty(lambda : parsedFrame_["framenameshort"])) and parsedFrame_["url"]:
                info_["id3v2"]["comments"][parsedFrame_["framenameshort"]][-1] = getid3_lib.iconv_fallback("ISO-8859-1", info_["id3v2"]["encoding"], parsedFrame_["url"])
            # end if
            parsedFrame_["data"] = None
        elif parsedFrame_["frame_name"][0] == "W":
            #// 4.3. W??? URL link frames
            #// There may only be one URL link frame of its kind in a tag,
            #// except when stated otherwise in the frame description
            #// <Header for 'URL link frame', ID: 'W000' - 'WZZZ', excluding 'WXXX'
            #// described in 4.3.2.>
            #// URL              <text string>
            parsedFrame_["url"] = php_trim(parsedFrame_["data"])
            #// always ISO-8859-1
            if (not php_empty(lambda : parsedFrame_["framenameshort"])) and parsedFrame_["url"]:
                info_["id3v2"]["comments"][parsedFrame_["framenameshort"]][-1] = getid3_lib.iconv_fallback("ISO-8859-1", info_["id3v2"]["encoding"], parsedFrame_["url"])
            # end if
            parsedFrame_["data"] = None
        elif id3v2_majorversion_ == 3 and parsedFrame_["frame_name"] == "IPLS" or id3v2_majorversion_ == 2 and parsedFrame_["frame_name"] == "IPL":
            #// 4.4  IPL  Involved people list (ID3v2.2 only)
            #// http://id3.org/id3v2.3.0#sec4.4
            #// There may only be one 'IPL' frame in each tag
            #// <Header for 'User defined URL link frame', ID: 'IPL'>
            #// Text encoding     $xx
            #// People list strings    <textstrings>
            frame_offset_ = 0
            frame_textencoding_ = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            frame_offset_ += 1
            if id3v2_majorversion_ <= 3 and frame_textencoding_ > 1 or id3v2_majorversion_ == 4 and frame_textencoding_ > 3:
                self.warning("Invalid text encoding byte (" + frame_textencoding_ + ") in frame \"" + parsedFrame_["frame_name"] + "\" - defaulting to ISO-8859-1 encoding")
            # end if
            parsedFrame_["encodingid"] = frame_textencoding_
            parsedFrame_["encoding"] = self.textencodingnamelookup(parsedFrame_["encodingid"])
            parsedFrame_["data_raw"] = php_str(php_substr(parsedFrame_["data"], frame_offset_))
            #// https://www.getid3.org/phpBB3/viewtopic.php?t=1369
            #// "this tag typically contains null terminated strings, which are associated in pairs"
            #// "there are users that use the tag incorrectly"
            IPLS_parts_ = Array()
            if php_strpos(parsedFrame_["data_raw"], " ") != False:
                IPLS_parts_unsorted_ = Array()
                if php_strlen(parsedFrame_["data_raw"]) % 2 == 0 and php_substr(parsedFrame_["data_raw"], 0, 2) == "ÿþ" or php_substr(parsedFrame_["data_raw"], 0, 2) == "þÿ":
                    #// UTF-16, be careful looking for null bytes since most 2-byte characters may contain one; you need to find twin null bytes, and on even padding
                    thisILPS_ = ""
                    i_ = 0
                    while i_ < php_strlen(parsedFrame_["data_raw"]):
                        
                        twobytes_ = php_substr(parsedFrame_["data_raw"], i_, 2)
                        if twobytes_ == "  ":
                            IPLS_parts_unsorted_[-1] = getid3_lib.iconv_fallback(parsedFrame_["encoding"], info_["id3v2"]["encoding"], thisILPS_)
                            thisILPS_ = ""
                        else:
                            thisILPS_ += twobytes_
                        # end if
                        i_ += 2
                    # end while
                    if php_strlen(thisILPS_) > 2:
                        #// 2-byte BOM
                        IPLS_parts_unsorted_[-1] = getid3_lib.iconv_fallback(parsedFrame_["encoding"], info_["id3v2"]["encoding"], thisILPS_)
                    # end if
                else:
                    #// ISO-8859-1 or UTF-8 or other single-byte-null character set
                    IPLS_parts_unsorted_ = php_explode(" ", parsedFrame_["data_raw"])
                # end if
                if php_count(IPLS_parts_unsorted_) == 1:
                    #// just a list of names, e.g. "Dino Baptiste, Jimmy Copley, John Gordon, Bernie Marsden, Sharon Watson"
                    for key_,value_ in IPLS_parts_unsorted_.items():
                        IPLS_parts_sorted_ = php_preg_split("#[;,\\r\\n\\t]#", value_)
                        position_ = ""
                        for person_ in IPLS_parts_sorted_:
                            IPLS_parts_[-1] = Array({"position": position_, "person": person_})
                        # end for
                    # end for
                elif php_count(IPLS_parts_unsorted_) % 2 == 0:
                    position_ = ""
                    person_ = ""
                    for key_,value_ in IPLS_parts_unsorted_.items():
                        if key_ % 2 == 0:
                            position_ = value_
                        else:
                            person_ = value_
                            IPLS_parts_[-1] = Array({"position": position_, "person": person_})
                            position_ = ""
                            person_ = ""
                        # end if
                    # end for
                else:
                    for key_,value_ in IPLS_parts_unsorted_.items():
                        IPLS_parts_[-1] = Array(value_)
                    # end for
                # end if
            else:
                IPLS_parts_ = php_preg_split("#[;,\\r\\n\\t]#", parsedFrame_["data_raw"])
            # end if
            parsedFrame_["data"] = IPLS_parts_
            if (not php_empty(lambda : parsedFrame_["framenameshort"])) and (not php_empty(lambda : parsedFrame_["data"])):
                info_["id3v2"]["comments"][parsedFrame_["framenameshort"]][-1] = parsedFrame_["data"]
            # end if
        elif id3v2_majorversion_ >= 3 and parsedFrame_["frame_name"] == "MCDI" or id3v2_majorversion_ == 2 and parsedFrame_["frame_name"] == "MCI":
            #// 4.5   MCI  Music CD identifier
            #// There may only be one 'MCDI' frame in each tag
            #// <Header for 'Music CD identifier', ID: 'MCDI'>
            #// CD TOC                <binary data>
            if (not php_empty(lambda : parsedFrame_["framenameshort"])) and (not php_empty(lambda : parsedFrame_["data"])):
                info_["id3v2"]["comments"][parsedFrame_["framenameshort"]][-1] = parsedFrame_["data"]
            # end if
        elif id3v2_majorversion_ >= 3 and parsedFrame_["frame_name"] == "ETCO" or id3v2_majorversion_ == 2 and parsedFrame_["frame_name"] == "ETC":
            #// 4.6   ETC  Event timing codes
            #// There may only be one 'ETCO' frame in each tag
            #// <Header for 'Event timing codes', ID: 'ETCO'>
            #// Time stamp format    $xx
            #// Where time stamp format is:
            #// $01  (32-bit value) MPEG frames from beginning of file
            #// $02  (32-bit value) milliseconds from beginning of file
            #// Followed by a list of key events in the following format:
            #// Type of event   $xx
            #// Time stamp      $xx (xx ...)
            #// The 'Time stamp' is set to zero if directly at the beginning of the sound
            #// or after the previous event. All events MUST be sorted in chronological order.
            frame_offset_ = 0
            parsedFrame_["timestampformat"] = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            frame_offset_ += 1
            while True:
                
                if not (frame_offset_ < php_strlen(parsedFrame_["data"])):
                    break
                # end if
                parsedFrame_["typeid"] = php_substr(parsedFrame_["data"], frame_offset_, 1)
                frame_offset_ += 1
                frame_offset_ += 1
                parsedFrame_["type"] = self.etcoeventlookup(parsedFrame_["typeid"])
                parsedFrame_["timestamp"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], frame_offset_, 4))
                frame_offset_ += 4
            # end while
            parsedFrame_["data"] = None
        elif id3v2_majorversion_ >= 3 and parsedFrame_["frame_name"] == "MLLT" or id3v2_majorversion_ == 2 and parsedFrame_["frame_name"] == "MLL":
            #// 4.7   MLL MPEG location lookup table
            #// There may only be one 'MLLT' frame in each tag
            #// <Header for 'Location lookup table', ID: 'MLLT'>
            #// MPEG frames between reference  $xx xx
            #// Bytes between reference        $xx xx xx
            #// Milliseconds between reference $xx xx xx
            #// Bits for bytes deviation       $xx
            #// Bits for milliseconds dev.     $xx
            #// Then for every reference the following data is included;
            #// Deviation in bytes         %xxx....
            #// Deviation in milliseconds  %xxx....
            frame_offset_ = 0
            parsedFrame_["framesbetweenreferences"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], 0, 2))
            parsedFrame_["bytesbetweenreferences"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], 2, 3))
            parsedFrame_["msbetweenreferences"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], 5, 3))
            parsedFrame_["bitsforbytesdeviation"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], 8, 1))
            parsedFrame_["bitsformsdeviation"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], 9, 1))
            parsedFrame_["data"] = php_substr(parsedFrame_["data"], 10)
            deviationbitstream_ = ""
            while True:
                
                if not (frame_offset_ < php_strlen(parsedFrame_["data"])):
                    break
                # end if
                deviationbitstream_ += getid3_lib.bigendian2bin(php_substr(parsedFrame_["data"], frame_offset_, 1))
                frame_offset_ += 1
            # end while
            reference_counter_ = 0
            while True:
                
                if not (php_strlen(deviationbitstream_) > 0):
                    break
                # end if
                parsedFrame_[reference_counter_]["bytedeviation"] = bindec(php_substr(deviationbitstream_, 0, parsedFrame_["bitsforbytesdeviation"]))
                parsedFrame_[reference_counter_]["msdeviation"] = bindec(php_substr(deviationbitstream_, parsedFrame_["bitsforbytesdeviation"], parsedFrame_["bitsformsdeviation"]))
                deviationbitstream_ = php_substr(deviationbitstream_, parsedFrame_["bitsforbytesdeviation"] + parsedFrame_["bitsformsdeviation"])
                reference_counter_ += 1
            # end while
            parsedFrame_["data"] = None
        elif id3v2_majorversion_ >= 3 and parsedFrame_["frame_name"] == "SYTC" or id3v2_majorversion_ == 2 and parsedFrame_["frame_name"] == "STC":
            #// 4.8   STC  Synchronised tempo codes
            #// There may only be one 'SYTC' frame in each tag
            #// <Header for 'Synchronised tempo codes', ID: 'SYTC'>
            #// Time stamp format   $xx
            #// Tempo data          <binary data>
            #// Where time stamp format is:
            #// $01  (32-bit value) MPEG frames from beginning of file
            #// $02  (32-bit value) milliseconds from beginning of file
            frame_offset_ = 0
            parsedFrame_["timestampformat"] = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            frame_offset_ += 1
            timestamp_counter_ = 0
            while True:
                
                if not (frame_offset_ < php_strlen(parsedFrame_["data"])):
                    break
                # end if
                parsedFrame_[timestamp_counter_]["tempo"] = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
                frame_offset_ += 1
                frame_offset_ += 1
                if parsedFrame_[timestamp_counter_]["tempo"] == 255:
                    parsedFrame_[timestamp_counter_]["tempo"] += php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
                    frame_offset_ += 1
                # end if
                parsedFrame_[timestamp_counter_]["timestamp"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], frame_offset_, 4))
                frame_offset_ += 4
                timestamp_counter_ += 1
            # end while
            parsedFrame_["data"] = None
        elif id3v2_majorversion_ >= 3 and parsedFrame_["frame_name"] == "USLT" or id3v2_majorversion_ == 2 and parsedFrame_["frame_name"] == "ULT":
            #// 4.9   ULT  Unsynchronised lyric/text transcription
            #// There may be more than one 'Unsynchronised lyrics/text transcription' frame
            #// in each tag, but only one with the same language and content descriptor.
            #// <Header for 'Unsynchronised lyrics/text transcription', ID: 'USLT'>
            #// Text encoding        $xx
            #// Language             $xx xx xx
            #// Content descriptor   <text string according to encoding> $00 (00)
            #// Lyrics/text          <full text string according to encoding>
            frame_offset_ = 0
            frame_textencoding_ = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            frame_offset_ += 1
            frame_textencoding_terminator_ = self.textencodingterminatorlookup(frame_textencoding_)
            if id3v2_majorversion_ <= 3 and frame_textencoding_ > 1 or id3v2_majorversion_ == 4 and frame_textencoding_ > 3:
                self.warning("Invalid text encoding byte (" + frame_textencoding_ + ") in frame \"" + parsedFrame_["frame_name"] + "\" - defaulting to ISO-8859-1 encoding")
                frame_textencoding_terminator_ = " "
            # end if
            frame_language_ = php_substr(parsedFrame_["data"], frame_offset_, 3)
            frame_offset_ += 3
            frame_terminatorpos_ = php_strpos(parsedFrame_["data"], frame_textencoding_terminator_, frame_offset_)
            if php_ord(php_substr(parsedFrame_["data"], frame_terminatorpos_ + php_strlen(frame_textencoding_terminator_), 1)) == 0:
                frame_terminatorpos_ += 1
                pass
            # end if
            parsedFrame_["description"] = php_substr(parsedFrame_["data"], frame_offset_, frame_terminatorpos_ - frame_offset_)
            parsedFrame_["description"] = self.makeutf16emptystringempty(parsedFrame_["description"])
            parsedFrame_["data"] = php_substr(parsedFrame_["data"], frame_terminatorpos_ + php_strlen(frame_textencoding_terminator_))
            parsedFrame_["data"] = self.removestringterminator(parsedFrame_["data"], frame_textencoding_terminator_)
            parsedFrame_["encodingid"] = frame_textencoding_
            parsedFrame_["encoding"] = self.textencodingnamelookup(frame_textencoding_)
            parsedFrame_["language"] = frame_language_
            parsedFrame_["languagename"] = self.languagelookup(frame_language_, False)
            if (not php_empty(lambda : parsedFrame_["framenameshort"])) and (not php_empty(lambda : parsedFrame_["data"])):
                info_["id3v2"]["comments"][parsedFrame_["framenameshort"]][-1] = getid3_lib.iconv_fallback(parsedFrame_["encoding"], info_["id3v2"]["encoding"], parsedFrame_["data"])
            # end if
            parsedFrame_["data"] = None
        elif id3v2_majorversion_ >= 3 and parsedFrame_["frame_name"] == "SYLT" or id3v2_majorversion_ == 2 and parsedFrame_["frame_name"] == "SLT":
            #// 4.10  SLT  Synchronised lyric/text
            #// There may be more than one 'SYLT' frame in each tag,
            #// but only one with the same language and content descriptor.
            #// <Header for 'Synchronised lyrics/text', ID: 'SYLT'>
            #// Text encoding        $xx
            #// Language             $xx xx xx
            #// Time stamp format    $xx
            #// $01  (32-bit value) MPEG frames from beginning of file
            #// $02  (32-bit value) milliseconds from beginning of file
            #// Content type         $xx
            #// Content descriptor   <text string according to encoding> $00 (00)
            #// Terminated text to be synced (typically a syllable)
            #// Sync identifier (terminator to above string)   $00 (00)
            #// Time stamp                                     $xx (xx ...)
            frame_offset_ = 0
            frame_textencoding_ = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            frame_offset_ += 1
            frame_textencoding_terminator_ = self.textencodingterminatorlookup(frame_textencoding_)
            if id3v2_majorversion_ <= 3 and frame_textencoding_ > 1 or id3v2_majorversion_ == 4 and frame_textencoding_ > 3:
                self.warning("Invalid text encoding byte (" + frame_textencoding_ + ") in frame \"" + parsedFrame_["frame_name"] + "\" - defaulting to ISO-8859-1 encoding")
                frame_textencoding_terminator_ = " "
            # end if
            frame_language_ = php_substr(parsedFrame_["data"], frame_offset_, 3)
            frame_offset_ += 3
            parsedFrame_["timestampformat"] = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            frame_offset_ += 1
            parsedFrame_["contenttypeid"] = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            frame_offset_ += 1
            parsedFrame_["contenttype"] = self.sytlcontenttypelookup(parsedFrame_["contenttypeid"])
            parsedFrame_["encodingid"] = frame_textencoding_
            parsedFrame_["encoding"] = self.textencodingnamelookup(frame_textencoding_)
            parsedFrame_["language"] = frame_language_
            parsedFrame_["languagename"] = self.languagelookup(frame_language_, False)
            timestampindex_ = 0
            frame_remainingdata_ = php_substr(parsedFrame_["data"], frame_offset_)
            while True:
                
                if not (php_strlen(frame_remainingdata_)):
                    break
                # end if
                frame_offset_ = 0
                frame_terminatorpos_ = php_strpos(frame_remainingdata_, frame_textencoding_terminator_)
                if frame_terminatorpos_ == False:
                    frame_remainingdata_ = ""
                else:
                    if php_ord(php_substr(frame_remainingdata_, frame_terminatorpos_ + php_strlen(frame_textencoding_terminator_), 1)) == 0:
                        frame_terminatorpos_ += 1
                        pass
                    # end if
                    parsedFrame_["lyrics"][timestampindex_]["data"] = php_substr(frame_remainingdata_, frame_offset_, frame_terminatorpos_ - frame_offset_)
                    frame_remainingdata_ = php_substr(frame_remainingdata_, frame_terminatorpos_ + php_strlen(frame_textencoding_terminator_))
                    if timestampindex_ == 0 and php_ord(frame_remainingdata_[0]) != 0:
                        pass
                    else:
                        parsedFrame_["lyrics"][timestampindex_]["timestamp"] = getid3_lib.bigendian2int(php_substr(frame_remainingdata_, 0, 4))
                        frame_remainingdata_ = php_substr(frame_remainingdata_, 4)
                    # end if
                    timestampindex_ += 1
                # end if
            # end while
            parsedFrame_["data"] = None
        elif id3v2_majorversion_ >= 3 and parsedFrame_["frame_name"] == "COMM" or id3v2_majorversion_ == 2 and parsedFrame_["frame_name"] == "COM":
            #// 4.11  COM  Comments
            #// There may be more than one comment frame in each tag,
            #// but only one with the same language and content descriptor.
            #// <Header for 'Comment', ID: 'COMM'>
            #// Text encoding          $xx
            #// Language               $xx xx xx
            #// Short content descrip. <text string according to encoding> $00 (00)
            #// The actual text        <full text string according to encoding>
            if php_strlen(parsedFrame_["data"]) < 5:
                self.warning("Invalid data (too short) for \"" + parsedFrame_["frame_name"] + "\" frame at offset " + parsedFrame_["dataoffset"])
            else:
                frame_offset_ = 0
                frame_textencoding_ = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
                frame_offset_ += 1
                frame_offset_ += 1
                frame_textencoding_terminator_ = self.textencodingterminatorlookup(frame_textencoding_)
                if id3v2_majorversion_ <= 3 and frame_textencoding_ > 1 or id3v2_majorversion_ == 4 and frame_textencoding_ > 3:
                    self.warning("Invalid text encoding byte (" + frame_textencoding_ + ") in frame \"" + parsedFrame_["frame_name"] + "\" - defaulting to ISO-8859-1 encoding")
                    frame_textencoding_terminator_ = " "
                # end if
                frame_language_ = php_substr(parsedFrame_["data"], frame_offset_, 3)
                frame_offset_ += 3
                frame_terminatorpos_ = php_strpos(parsedFrame_["data"], frame_textencoding_terminator_, frame_offset_)
                if php_ord(php_substr(parsedFrame_["data"], frame_terminatorpos_ + php_strlen(frame_textencoding_terminator_), 1)) == 0:
                    frame_terminatorpos_ += 1
                    pass
                # end if
                parsedFrame_["description"] = php_substr(parsedFrame_["data"], frame_offset_, frame_terminatorpos_ - frame_offset_)
                parsedFrame_["description"] = self.makeutf16emptystringempty(parsedFrame_["description"])
                frame_text_ = php_str(php_substr(parsedFrame_["data"], frame_terminatorpos_ + php_strlen(frame_textencoding_terminator_)))
                frame_text_ = self.removestringterminator(frame_text_, frame_textencoding_terminator_)
                parsedFrame_["encodingid"] = frame_textencoding_
                parsedFrame_["encoding"] = self.textencodingnamelookup(frame_textencoding_)
                parsedFrame_["language"] = frame_language_
                parsedFrame_["languagename"] = self.languagelookup(frame_language_, False)
                parsedFrame_["data"] = frame_text_
                if (not php_empty(lambda : parsedFrame_["framenameshort"])) and (not php_empty(lambda : parsedFrame_["data"])):
                    commentkey_ = parsedFrame_["description"] if parsedFrame_["description"] else php_count(info_["id3v2"]["comments"][parsedFrame_["framenameshort"]]) if (not php_empty(lambda : info_["id3v2"]["comments"][parsedFrame_["framenameshort"]])) else 0
                    if (not (php_isset(lambda : info_["id3v2"]["comments"][parsedFrame_["framenameshort"]]))) or (not php_array_key_exists(commentkey_, info_["id3v2"]["comments"][parsedFrame_["framenameshort"]])):
                        info_["id3v2"]["comments"][parsedFrame_["framenameshort"]][commentkey_] = getid3_lib.iconv_fallback(parsedFrame_["encoding"], info_["id3v2"]["encoding"], parsedFrame_["data"])
                    else:
                        info_["id3v2"]["comments"][parsedFrame_["framenameshort"]][-1] = getid3_lib.iconv_fallback(parsedFrame_["encoding"], info_["id3v2"]["encoding"], parsedFrame_["data"])
                    # end if
                # end if
            # end if
        elif id3v2_majorversion_ >= 4 and parsedFrame_["frame_name"] == "RVA2":
            #// 4.11  RVA2 Relative volume adjustment (2) (ID3v2.4+ only)
            #// There may be more than one 'RVA2' frame in each tag,
            #// but only one with the same identification string
            #// <Header for 'Relative volume adjustment (2)', ID: 'RVA2'>
            #// Identification          <text string> $00
            #// The 'identification' string is used to identify the situation and/or
            #// device where this adjustment should apply. The following is then
            #// repeated for every channel:
            #// Type of channel         $xx
            #// Volume adjustment       $xx xx
            #// Bits representing peak  $xx
            #// Peak volume             $xx (xx ...)
            frame_terminatorpos_ = php_strpos(parsedFrame_["data"], " ")
            frame_idstring_ = php_substr(parsedFrame_["data"], 0, frame_terminatorpos_)
            if php_ord(frame_idstring_) == 0:
                frame_idstring_ = ""
            # end if
            frame_remainingdata_ = php_substr(parsedFrame_["data"], frame_terminatorpos_ + php_strlen(" "))
            parsedFrame_["description"] = frame_idstring_
            RVA2channelcounter_ = 0
            while True:
                
                if not (php_strlen(frame_remainingdata_) >= 5):
                    break
                # end if
                frame_offset_ = 0
                frame_channeltypeid_ = php_ord(php_substr(frame_remainingdata_, frame_offset_, 1))
                frame_offset_ += 1
                frame_offset_ += 1
                parsedFrame_[RVA2channelcounter_]["channeltypeid"] = frame_channeltypeid_
                parsedFrame_[RVA2channelcounter_]["channeltype"] = self.rva2channeltypelookup(frame_channeltypeid_)
                parsedFrame_[RVA2channelcounter_]["volumeadjust"] = getid3_lib.bigendian2int(php_substr(frame_remainingdata_, frame_offset_, 2), False, True)
                #// 16-bit signed
                frame_offset_ += 2
                parsedFrame_[RVA2channelcounter_]["bitspeakvolume"] = php_ord(php_substr(frame_remainingdata_, frame_offset_, 1))
                frame_offset_ += 1
                frame_offset_ += 1
                if parsedFrame_[RVA2channelcounter_]["bitspeakvolume"] < 1 or parsedFrame_[RVA2channelcounter_]["bitspeakvolume"] > 4:
                    self.warning("ID3v2::RVA2 frame[" + RVA2channelcounter_ + "] contains invalid " + parsedFrame_[RVA2channelcounter_]["bitspeakvolume"] + "-byte bits-representing-peak value")
                    break
                # end if
                frame_bytespeakvolume_ = ceil(parsedFrame_[RVA2channelcounter_]["bitspeakvolume"] / 8)
                parsedFrame_[RVA2channelcounter_]["peakvolume"] = getid3_lib.bigendian2int(php_substr(frame_remainingdata_, frame_offset_, frame_bytespeakvolume_))
                frame_remainingdata_ = php_substr(frame_remainingdata_, frame_offset_ + frame_bytespeakvolume_)
                RVA2channelcounter_ += 1
            # end while
            parsedFrame_["data"] = None
        elif id3v2_majorversion_ == 3 and parsedFrame_["frame_name"] == "RVAD" or id3v2_majorversion_ == 2 and parsedFrame_["frame_name"] == "RVA":
            #// 4.12  RVA  Relative volume adjustment (ID3v2.2 only)
            #// There may only be one 'RVA' frame in each tag
            #// <Header for 'Relative volume adjustment', ID: 'RVA'>
            #// ID3v2.2 => Increment/decrement     %000000ba
            #// ID3v2.3 => Increment/decrement     %00fedcba
            #// Bits used for volume descr.        $xx
            #// Relative volume change, right      $xx xx (xx ...) // a
            #// Relative volume change, left       $xx xx (xx ...) // b
            #// Peak volume right                  $xx xx (xx ...)
            #// Peak volume left                   $xx xx (xx ...)
            #// ID3v2.3 only, optional (not present in ID3v2.2):
            #// Relative volume change, right back $xx xx (xx ...) // c
            #// Relative volume change, left back  $xx xx (xx ...) // d
            #// Peak volume right back             $xx xx (xx ...)
            #// Peak volume left back              $xx xx (xx ...)
            #// ID3v2.3 only, optional (not present in ID3v2.2):
            #// Relative volume change, center     $xx xx (xx ...) // e
            #// Peak volume center                 $xx xx (xx ...)
            #// ID3v2.3 only, optional (not present in ID3v2.2):
            #// Relative volume change, bass       $xx xx (xx ...) // f
            #// Peak volume bass                   $xx xx (xx ...)
            frame_offset_ = 0
            frame_incrdecrflags_ = getid3_lib.bigendian2bin(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            frame_offset_ += 1
            parsedFrame_["incdec"]["right"] = php_bool(php_substr(frame_incrdecrflags_, 6, 1))
            parsedFrame_["incdec"]["left"] = php_bool(php_substr(frame_incrdecrflags_, 7, 1))
            parsedFrame_["bitsvolume"] = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            frame_offset_ += 1
            frame_bytesvolume_ = ceil(parsedFrame_["bitsvolume"] / 8)
            parsedFrame_["volumechange"]["right"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], frame_offset_, frame_bytesvolume_))
            if parsedFrame_["incdec"]["right"] == False:
                parsedFrame_["volumechange"]["right"] *= -1
            # end if
            frame_offset_ += frame_bytesvolume_
            parsedFrame_["volumechange"]["left"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], frame_offset_, frame_bytesvolume_))
            if parsedFrame_["incdec"]["left"] == False:
                parsedFrame_["volumechange"]["left"] *= -1
            # end if
            frame_offset_ += frame_bytesvolume_
            parsedFrame_["peakvolume"]["right"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], frame_offset_, frame_bytesvolume_))
            frame_offset_ += frame_bytesvolume_
            parsedFrame_["peakvolume"]["left"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], frame_offset_, frame_bytesvolume_))
            frame_offset_ += frame_bytesvolume_
            if id3v2_majorversion_ == 3:
                parsedFrame_["data"] = php_substr(parsedFrame_["data"], frame_offset_)
                if php_strlen(parsedFrame_["data"]) > 0:
                    parsedFrame_["incdec"]["rightrear"] = php_bool(php_substr(frame_incrdecrflags_, 4, 1))
                    parsedFrame_["incdec"]["leftrear"] = php_bool(php_substr(frame_incrdecrflags_, 5, 1))
                    parsedFrame_["volumechange"]["rightrear"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], frame_offset_, frame_bytesvolume_))
                    if parsedFrame_["incdec"]["rightrear"] == False:
                        parsedFrame_["volumechange"]["rightrear"] *= -1
                    # end if
                    frame_offset_ += frame_bytesvolume_
                    parsedFrame_["volumechange"]["leftrear"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], frame_offset_, frame_bytesvolume_))
                    if parsedFrame_["incdec"]["leftrear"] == False:
                        parsedFrame_["volumechange"]["leftrear"] *= -1
                    # end if
                    frame_offset_ += frame_bytesvolume_
                    parsedFrame_["peakvolume"]["rightrear"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], frame_offset_, frame_bytesvolume_))
                    frame_offset_ += frame_bytesvolume_
                    parsedFrame_["peakvolume"]["leftrear"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], frame_offset_, frame_bytesvolume_))
                    frame_offset_ += frame_bytesvolume_
                # end if
                parsedFrame_["data"] = php_substr(parsedFrame_["data"], frame_offset_)
                if php_strlen(parsedFrame_["data"]) > 0:
                    parsedFrame_["incdec"]["center"] = php_bool(php_substr(frame_incrdecrflags_, 3, 1))
                    parsedFrame_["volumechange"]["center"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], frame_offset_, frame_bytesvolume_))
                    if parsedFrame_["incdec"]["center"] == False:
                        parsedFrame_["volumechange"]["center"] *= -1
                    # end if
                    frame_offset_ += frame_bytesvolume_
                    parsedFrame_["peakvolume"]["center"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], frame_offset_, frame_bytesvolume_))
                    frame_offset_ += frame_bytesvolume_
                # end if
                parsedFrame_["data"] = php_substr(parsedFrame_["data"], frame_offset_)
                if php_strlen(parsedFrame_["data"]) > 0:
                    parsedFrame_["incdec"]["bass"] = php_bool(php_substr(frame_incrdecrflags_, 2, 1))
                    parsedFrame_["volumechange"]["bass"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], frame_offset_, frame_bytesvolume_))
                    if parsedFrame_["incdec"]["bass"] == False:
                        parsedFrame_["volumechange"]["bass"] *= -1
                    # end if
                    frame_offset_ += frame_bytesvolume_
                    parsedFrame_["peakvolume"]["bass"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], frame_offset_, frame_bytesvolume_))
                    frame_offset_ += frame_bytesvolume_
                # end if
            # end if
            parsedFrame_["data"] = None
        elif id3v2_majorversion_ >= 4 and parsedFrame_["frame_name"] == "EQU2":
            #// 4.12  EQU2 Equalisation (2) (ID3v2.4+ only)
            #// There may be more than one 'EQU2' frame in each tag,
            #// but only one with the same identification string
            #// <Header of 'Equalisation (2)', ID: 'EQU2'>
            #// Interpolation method  $xx
            #// $00  Band
            #// $01  Linear
            #// Identification        <text string> $00
            #// The following is then repeated for every adjustment point
            #// Frequency          $xx xx
            #// Volume adjustment  $xx xx
            frame_offset_ = 0
            frame_interpolationmethod_ = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            frame_offset_ += 1
            frame_terminatorpos_ = php_strpos(parsedFrame_["data"], " ", frame_offset_)
            frame_idstring_ = php_substr(parsedFrame_["data"], frame_offset_, frame_terminatorpos_ - frame_offset_)
            if php_ord(frame_idstring_) == 0:
                frame_idstring_ = ""
            # end if
            parsedFrame_["description"] = frame_idstring_
            frame_remainingdata_ = php_substr(parsedFrame_["data"], frame_terminatorpos_ + php_strlen(" "))
            while True:
                
                if not (php_strlen(frame_remainingdata_)):
                    break
                # end if
                frame_frequency_ = getid3_lib.bigendian2int(php_substr(frame_remainingdata_, 0, 2)) / 2
                parsedFrame_["data"][frame_frequency_] = getid3_lib.bigendian2int(php_substr(frame_remainingdata_, 2, 2), False, True)
                frame_remainingdata_ = php_substr(frame_remainingdata_, 4)
            # end while
            parsedFrame_["interpolationmethod"] = frame_interpolationmethod_
            parsedFrame_["data"] = None
        elif id3v2_majorversion_ == 3 and parsedFrame_["frame_name"] == "EQUA" or id3v2_majorversion_ == 2 and parsedFrame_["frame_name"] == "EQU":
            #// 4.13  EQU  Equalisation (ID3v2.2 only)
            #// There may only be one 'EQUA' frame in each tag
            #// <Header for 'Relative volume adjustment', ID: 'EQU'>
            #// Adjustment bits    $xx
            #// This is followed by 2 bytes + ('adjustment bits' rounded up to the
            #// nearest byte) for every equalisation band in the following format,
            #// giving a frequency range of 0 - 32767Hz:
            #// Increment/decrement   %x (MSB of the Frequency)
            #// Frequency             (lower 15 bits)
            #// Adjustment            $xx (xx ...)
            frame_offset_ = 0
            parsedFrame_["adjustmentbits"] = php_substr(parsedFrame_["data"], frame_offset_, 1)
            frame_offset_ += 1
            frame_offset_ += 1
            frame_adjustmentbytes_ = ceil(parsedFrame_["adjustmentbits"] / 8)
            frame_remainingdata_ = php_str(php_substr(parsedFrame_["data"], frame_offset_))
            while True:
                
                if not (php_strlen(frame_remainingdata_) > 0):
                    break
                # end if
                frame_frequencystr_ = getid3_lib.bigendian2bin(php_substr(frame_remainingdata_, 0, 2))
                frame_incdec_ = php_bool(php_substr(frame_frequencystr_, 0, 1))
                frame_frequency_ = bindec(php_substr(frame_frequencystr_, 1, 15))
                parsedFrame_[frame_frequency_]["incdec"] = frame_incdec_
                parsedFrame_[frame_frequency_]["adjustment"] = getid3_lib.bigendian2int(php_substr(frame_remainingdata_, 2, frame_adjustmentbytes_))
                if parsedFrame_[frame_frequency_]["incdec"] == False:
                    parsedFrame_[frame_frequency_]["adjustment"] *= -1
                # end if
                frame_remainingdata_ = php_substr(frame_remainingdata_, 2 + frame_adjustmentbytes_)
            # end while
            parsedFrame_["data"] = None
        elif id3v2_majorversion_ >= 3 and parsedFrame_["frame_name"] == "RVRB" or id3v2_majorversion_ == 2 and parsedFrame_["frame_name"] == "REV":
            #// 4.14  REV  Reverb
            #// There may only be one 'RVRB' frame in each tag.
            #// <Header for 'Reverb', ID: 'RVRB'>
            #// Reverb left (ms)                 $xx xx
            #// Reverb right (ms)                $xx xx
            #// Reverb bounces, left             $xx
            #// Reverb bounces, right            $xx
            #// Reverb feedback, left to left    $xx
            #// Reverb feedback, left to right   $xx
            #// Reverb feedback, right to right  $xx
            #// Reverb feedback, right to left   $xx
            #// Premix left to right             $xx
            #// Premix right to left             $xx
            frame_offset_ = 0
            parsedFrame_["left"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], frame_offset_, 2))
            frame_offset_ += 2
            parsedFrame_["right"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], frame_offset_, 2))
            frame_offset_ += 2
            parsedFrame_["bouncesL"] = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            frame_offset_ += 1
            parsedFrame_["bouncesR"] = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            frame_offset_ += 1
            parsedFrame_["feedbackLL"] = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            frame_offset_ += 1
            parsedFrame_["feedbackLR"] = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            frame_offset_ += 1
            parsedFrame_["feedbackRR"] = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            frame_offset_ += 1
            parsedFrame_["feedbackRL"] = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            frame_offset_ += 1
            parsedFrame_["premixLR"] = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            frame_offset_ += 1
            parsedFrame_["premixRL"] = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            frame_offset_ += 1
            parsedFrame_["data"] = None
        elif id3v2_majorversion_ >= 3 and parsedFrame_["frame_name"] == "APIC" or id3v2_majorversion_ == 2 and parsedFrame_["frame_name"] == "PIC":
            #// 4.15  PIC  Attached picture
            #// There may be several pictures attached to one file,
            #// each in their individual 'APIC' frame, but only one
            #// with the same content descriptor
            #// <Header for 'Attached picture', ID: 'APIC'>
            #// Text encoding      $xx
            #// ID3v2.3+ => MIME type          <text string> $00
            #// ID3v2.2  => Image format       $xx xx xx
            #// Picture type       $xx
            #// Description        <text string according to encoding> $00 (00)
            #// Picture data       <binary data>
            frame_offset_ = 0
            frame_textencoding_ = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            frame_offset_ += 1
            frame_textencoding_terminator_ = self.textencodingterminatorlookup(frame_textencoding_)
            if id3v2_majorversion_ <= 3 and frame_textencoding_ > 1 or id3v2_majorversion_ == 4 and frame_textencoding_ > 3:
                self.warning("Invalid text encoding byte (" + frame_textencoding_ + ") in frame \"" + parsedFrame_["frame_name"] + "\" - defaulting to ISO-8859-1 encoding")
                frame_textencoding_terminator_ = " "
            # end if
            if id3v2_majorversion_ == 2 and php_strlen(parsedFrame_["data"]) > frame_offset_:
                frame_imagetype_ = php_substr(parsedFrame_["data"], frame_offset_, 3)
                if php_strtolower(frame_imagetype_) == "ima":
                    #// complete hack for mp3Rage (www.chaoticsoftware.com) that puts ID3v2.3-formatted
                    #// MIME type instead of 3-char ID3v2.2-format image type  (thanks xbhoffØpacbell*net)
                    frame_terminatorpos_ = php_strpos(parsedFrame_["data"], " ", frame_offset_)
                    frame_mimetype_ = php_substr(parsedFrame_["data"], frame_offset_, frame_terminatorpos_ - frame_offset_)
                    if php_ord(frame_mimetype_) == 0:
                        frame_mimetype_ = ""
                    # end if
                    frame_imagetype_ = php_strtoupper(php_str_replace("image/", "", php_strtolower(frame_mimetype_)))
                    if frame_imagetype_ == "JPEG":
                        frame_imagetype_ = "JPG"
                    # end if
                    frame_offset_ = frame_terminatorpos_ + php_strlen(" ")
                else:
                    frame_offset_ += 3
                # end if
            # end if
            if id3v2_majorversion_ > 2 and php_strlen(parsedFrame_["data"]) > frame_offset_:
                frame_terminatorpos_ = php_strpos(parsedFrame_["data"], " ", frame_offset_)
                frame_mimetype_ = php_substr(parsedFrame_["data"], frame_offset_, frame_terminatorpos_ - frame_offset_)
                if php_ord(frame_mimetype_) == 0:
                    frame_mimetype_ = ""
                # end if
                frame_offset_ = frame_terminatorpos_ + php_strlen(" ")
            # end if
            frame_picturetype_ = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            frame_offset_ += 1
            if frame_offset_ >= parsedFrame_["datalength"]:
                self.warning("data portion of APIC frame is missing at offset " + parsedFrame_["dataoffset"] + 8 + frame_offset_)
            else:
                frame_terminatorpos_ = php_strpos(parsedFrame_["data"], frame_textencoding_terminator_, frame_offset_)
                if php_ord(php_substr(parsedFrame_["data"], frame_terminatorpos_ + php_strlen(frame_textencoding_terminator_), 1)) == 0:
                    frame_terminatorpos_ += 1
                    pass
                # end if
                parsedFrame_["description"] = php_substr(parsedFrame_["data"], frame_offset_, frame_terminatorpos_ - frame_offset_)
                parsedFrame_["description"] = self.makeutf16emptystringempty(parsedFrame_["description"])
                parsedFrame_["encodingid"] = frame_textencoding_
                parsedFrame_["encoding"] = self.textencodingnamelookup(frame_textencoding_)
                if id3v2_majorversion_ == 2:
                    parsedFrame_["imagetype"] = frame_imagetype_ if (php_isset(lambda : frame_imagetype_)) else None
                else:
                    parsedFrame_["mime"] = frame_mimetype_ if (php_isset(lambda : frame_mimetype_)) else None
                # end if
                parsedFrame_["picturetypeid"] = frame_picturetype_
                parsedFrame_["picturetype"] = self.apicpicturetypelookup(frame_picturetype_)
                parsedFrame_["data"] = php_substr(parsedFrame_["data"], frame_terminatorpos_ + php_strlen(frame_textencoding_terminator_))
                parsedFrame_["datalength"] = php_strlen(parsedFrame_["data"])
                parsedFrame_["image_mime"] = ""
                imageinfo_ = Array()
                imagechunkcheck_ = getid3_lib.getdataimagesize(parsedFrame_["data"], imageinfo_)
                if imagechunkcheck_:
                    if imagechunkcheck_[2] >= 1 and imagechunkcheck_[2] <= 3:
                        parsedFrame_["image_mime"] = image_type_to_mime_type(imagechunkcheck_[2])
                        if imagechunkcheck_[0]:
                            parsedFrame_["image_width"] = imagechunkcheck_[0]
                        # end if
                        if imagechunkcheck_[1]:
                            parsedFrame_["image_height"] = imagechunkcheck_[1]
                        # end if
                    # end if
                # end if
                while True:
                    if self.getid3.option_save_attachments == False:
                        parsedFrame_["data"] = None
                        break
                    # end if
                    dir_ = ""
                    if self.getid3.option_save_attachments == True:
                        pass
                    elif php_is_string(self.getid3.option_save_attachments):
                        dir_ = php_rtrim(php_str_replace(Array("/", "\\"), DIRECTORY_SEPARATOR, self.getid3.option_save_attachments), DIRECTORY_SEPARATOR)
                        if (not php_is_dir(dir_)) or (not getID3.is_writable(dir_)):
                            #// cannot write, skip
                            self.warning("attachment at " + frame_offset_ + " cannot be saved to \"" + dir_ + "\" (not writable)")
                            parsedFrame_["data"] = None
                            break
                        # end if
                    # end if
                    #// if we get this far, must be OK
                    if php_is_string(self.getid3.option_save_attachments):
                        destination_filename_ = dir_ + DIRECTORY_SEPARATOR + php_md5(info_["filenamepath"]) + "_" + frame_offset_
                        if (not php_file_exists(destination_filename_)) or getID3.is_writable(destination_filename_):
                            file_put_contents(destination_filename_, parsedFrame_["data"])
                        else:
                            self.warning("attachment at " + frame_offset_ + " cannot be saved to \"" + destination_filename_ + "\" (not writable)")
                        # end if
                        parsedFrame_["data_filename"] = destination_filename_
                        parsedFrame_["data"] = None
                    else:
                        if (not php_empty(lambda : parsedFrame_["framenameshort"])) and (not php_empty(lambda : parsedFrame_["data"])):
                            if (not (php_isset(lambda : info_["id3v2"]["comments"]["picture"]))):
                                info_["id3v2"]["comments"]["picture"] = Array()
                            # end if
                            comments_picture_data_ = Array()
                            for picture_key_ in Array("data", "image_mime", "image_width", "image_height", "imagetype", "picturetype", "description", "datalength"):
                                if (php_isset(lambda : parsedFrame_[picture_key_])):
                                    comments_picture_data_[picture_key_] = parsedFrame_[picture_key_]
                                # end if
                            # end for
                            info_["id3v2"]["comments"]["picture"][-1] = comments_picture_data_
                            comments_picture_data_ = None
                        # end if
                    # end if
                    
                    if False:
                        break
                    # end if
                # end while
            # end if
        elif id3v2_majorversion_ >= 3 and parsedFrame_["frame_name"] == "GEOB" or id3v2_majorversion_ == 2 and parsedFrame_["frame_name"] == "GEO":
            #// 4.16  GEO  General encapsulated object
            #// There may be more than one 'GEOB' frame in each tag,
            #// but only one with the same content descriptor
            #// <Header for 'General encapsulated object', ID: 'GEOB'>
            #// Text encoding          $xx
            #// MIME type              <text string> $00
            #// Filename               <text string according to encoding> $00 (00)
            #// Content description    <text string according to encoding> $00 (00)
            #// Encapsulated object    <binary data>
            frame_offset_ = 0
            frame_textencoding_ = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            frame_offset_ += 1
            frame_textencoding_terminator_ = self.textencodingterminatorlookup(frame_textencoding_)
            if id3v2_majorversion_ <= 3 and frame_textencoding_ > 1 or id3v2_majorversion_ == 4 and frame_textencoding_ > 3:
                self.warning("Invalid text encoding byte (" + frame_textencoding_ + ") in frame \"" + parsedFrame_["frame_name"] + "\" - defaulting to ISO-8859-1 encoding")
                frame_textencoding_terminator_ = " "
            # end if
            frame_terminatorpos_ = php_strpos(parsedFrame_["data"], " ", frame_offset_)
            frame_mimetype_ = php_substr(parsedFrame_["data"], frame_offset_, frame_terminatorpos_ - frame_offset_)
            if php_ord(frame_mimetype_) == 0:
                frame_mimetype_ = ""
            # end if
            frame_offset_ = frame_terminatorpos_ + php_strlen(" ")
            frame_terminatorpos_ = php_strpos(parsedFrame_["data"], frame_textencoding_terminator_, frame_offset_)
            if php_ord(php_substr(parsedFrame_["data"], frame_terminatorpos_ + php_strlen(frame_textencoding_terminator_), 1)) == 0:
                frame_terminatorpos_ += 1
                pass
            # end if
            frame_filename_ = php_substr(parsedFrame_["data"], frame_offset_, frame_terminatorpos_ - frame_offset_)
            if php_ord(frame_filename_) == 0:
                frame_filename_ = ""
            # end if
            frame_offset_ = frame_terminatorpos_ + php_strlen(frame_textencoding_terminator_)
            frame_terminatorpos_ = php_strpos(parsedFrame_["data"], frame_textencoding_terminator_, frame_offset_)
            if php_ord(php_substr(parsedFrame_["data"], frame_terminatorpos_ + php_strlen(frame_textencoding_terminator_), 1)) == 0:
                frame_terminatorpos_ += 1
                pass
            # end if
            parsedFrame_["description"] = php_substr(parsedFrame_["data"], frame_offset_, frame_terminatorpos_ - frame_offset_)
            parsedFrame_["description"] = self.makeutf16emptystringempty(parsedFrame_["description"])
            frame_offset_ = frame_terminatorpos_ + php_strlen(frame_textencoding_terminator_)
            parsedFrame_["objectdata"] = php_str(php_substr(parsedFrame_["data"], frame_offset_))
            parsedFrame_["encodingid"] = frame_textencoding_
            parsedFrame_["encoding"] = self.textencodingnamelookup(frame_textencoding_)
            parsedFrame_["mime"] = frame_mimetype_
            parsedFrame_["filename"] = frame_filename_
            parsedFrame_["data"] = None
        elif id3v2_majorversion_ >= 3 and parsedFrame_["frame_name"] == "PCNT" or id3v2_majorversion_ == 2 and parsedFrame_["frame_name"] == "CNT":
            #// 4.17  CNT  Play counter
            #// There may only be one 'PCNT' frame in each tag.
            #// When the counter reaches all one's, one byte is inserted in
            #// front of the counter thus making the counter eight bits bigger
            #// <Header for 'Play counter', ID: 'PCNT'>
            #// Counter        $xx xx xx xx (xx ...)
            parsedFrame_["data"] = getid3_lib.bigendian2int(parsedFrame_["data"])
        elif id3v2_majorversion_ >= 3 and parsedFrame_["frame_name"] == "POPM" or id3v2_majorversion_ == 2 and parsedFrame_["frame_name"] == "POP":
            #// 4.18  POP  Popularimeter
            #// There may be more than one 'POPM' frame in each tag,
            #// but only one with the same email address
            #// <Header for 'Popularimeter', ID: 'POPM'>
            #// Email to user   <text string> $00
            #// Rating          $xx
            #// Counter         $xx xx xx xx (xx ...)
            frame_offset_ = 0
            frame_terminatorpos_ = php_strpos(parsedFrame_["data"], " ", frame_offset_)
            frame_emailaddress_ = php_substr(parsedFrame_["data"], frame_offset_, frame_terminatorpos_ - frame_offset_)
            if php_ord(frame_emailaddress_) == 0:
                frame_emailaddress_ = ""
            # end if
            frame_offset_ = frame_terminatorpos_ + php_strlen(" ")
            frame_rating_ = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            frame_offset_ += 1
            parsedFrame_["counter"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], frame_offset_))
            parsedFrame_["email"] = frame_emailaddress_
            parsedFrame_["rating"] = frame_rating_
            parsedFrame_["data"] = None
        elif id3v2_majorversion_ >= 3 and parsedFrame_["frame_name"] == "RBUF" or id3v2_majorversion_ == 2 and parsedFrame_["frame_name"] == "BUF":
            #// 4.19  BUF  Recommended buffer size
            #// There may only be one 'RBUF' frame in each tag
            #// <Header for 'Recommended buffer size', ID: 'RBUF'>
            #// Buffer size               $xx xx xx
            #// Embedded info flag        %0000000x
            #// Offset to next tag        $xx xx xx xx
            frame_offset_ = 0
            parsedFrame_["buffersize"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], frame_offset_, 3))
            frame_offset_ += 3
            frame_embeddedinfoflags_ = getid3_lib.bigendian2bin(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            frame_offset_ += 1
            parsedFrame_["flags"]["embededinfo"] = php_bool(php_substr(frame_embeddedinfoflags_, 7, 1))
            parsedFrame_["nexttagoffset"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], frame_offset_, 4))
            parsedFrame_["data"] = None
        elif id3v2_majorversion_ == 2 and parsedFrame_["frame_name"] == "CRM":
            #// 4.20  Encrypted meta frame (ID3v2.2 only)
            #// There may be more than one 'CRM' frame in a tag,
            #// but only one with the same 'owner identifier'
            #// <Header for 'Encrypted meta frame', ID: 'CRM'>
            #// Owner identifier      <textstring> $00 (00)
            #// Content/explanation   <textstring> $00 (00)
            #// Encrypted datablock   <binary data>
            frame_offset_ = 0
            frame_terminatorpos_ = php_strpos(parsedFrame_["data"], " ", frame_offset_)
            frame_ownerid_ = php_substr(parsedFrame_["data"], frame_offset_, frame_terminatorpos_ - frame_offset_)
            frame_offset_ = frame_terminatorpos_ + php_strlen(" ")
            frame_terminatorpos_ = php_strpos(parsedFrame_["data"], " ", frame_offset_)
            parsedFrame_["description"] = php_substr(parsedFrame_["data"], frame_offset_, frame_terminatorpos_ - frame_offset_)
            parsedFrame_["description"] = self.makeutf16emptystringempty(parsedFrame_["description"])
            frame_offset_ = frame_terminatorpos_ + php_strlen(" ")
            parsedFrame_["ownerid"] = frame_ownerid_
            parsedFrame_["data"] = php_str(php_substr(parsedFrame_["data"], frame_offset_))
            parsedFrame_["data"] = None
        elif id3v2_majorversion_ >= 3 and parsedFrame_["frame_name"] == "AENC" or id3v2_majorversion_ == 2 and parsedFrame_["frame_name"] == "CRA":
            #// 4.21  CRA  Audio encryption
            #// There may be more than one 'AENC' frames in a tag,
            #// but only one with the same 'Owner identifier'
            #// <Header for 'Audio encryption', ID: 'AENC'>
            #// Owner identifier   <text string> $00
            #// Preview start      $xx xx
            #// Preview length     $xx xx
            #// Encryption info    <binary data>
            frame_offset_ = 0
            frame_terminatorpos_ = php_strpos(parsedFrame_["data"], " ", frame_offset_)
            frame_ownerid_ = php_substr(parsedFrame_["data"], frame_offset_, frame_terminatorpos_ - frame_offset_)
            if php_ord(frame_ownerid_) == 0:
                frame_ownerid_ = ""
            # end if
            frame_offset_ = frame_terminatorpos_ + php_strlen(" ")
            parsedFrame_["ownerid"] = frame_ownerid_
            parsedFrame_["previewstart"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], frame_offset_, 2))
            frame_offset_ += 2
            parsedFrame_["previewlength"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], frame_offset_, 2))
            frame_offset_ += 2
            parsedFrame_["encryptioninfo"] = php_str(php_substr(parsedFrame_["data"], frame_offset_))
            parsedFrame_["data"] = None
        elif id3v2_majorversion_ >= 3 and parsedFrame_["frame_name"] == "LINK" or id3v2_majorversion_ == 2 and parsedFrame_["frame_name"] == "LNK":
            #// 4.22  LNK  Linked information
            #// There may be more than one 'LINK' frame in a tag,
            #// but only one with the same contents
            #// <Header for 'Linked information', ID: 'LINK'>
            #// ID3v2.3+ => Frame identifier   $xx xx xx xx
            #// ID3v2.2  => Frame identifier   $xx xx xx
            #// URL                            <text string> $00
            #// ID and additional data         <text string(s)>
            frame_offset_ = 0
            if id3v2_majorversion_ == 2:
                parsedFrame_["frameid"] = php_substr(parsedFrame_["data"], frame_offset_, 3)
                frame_offset_ += 3
            else:
                parsedFrame_["frameid"] = php_substr(parsedFrame_["data"], frame_offset_, 4)
                frame_offset_ += 4
            # end if
            frame_terminatorpos_ = php_strpos(parsedFrame_["data"], " ", frame_offset_)
            frame_url_ = php_substr(parsedFrame_["data"], frame_offset_, frame_terminatorpos_ - frame_offset_)
            if php_ord(frame_url_) == 0:
                frame_url_ = ""
            # end if
            frame_offset_ = frame_terminatorpos_ + php_strlen(" ")
            parsedFrame_["url"] = frame_url_
            parsedFrame_["additionaldata"] = php_str(php_substr(parsedFrame_["data"], frame_offset_))
            if (not php_empty(lambda : parsedFrame_["framenameshort"])) and parsedFrame_["url"]:
                info_["id3v2"]["comments"][parsedFrame_["framenameshort"]][-1] = getid3_lib.iconv_fallback_iso88591_utf8(parsedFrame_["url"])
            # end if
            parsedFrame_["data"] = None
        elif id3v2_majorversion_ >= 3 and parsedFrame_["frame_name"] == "POSS":
            #// 4.21  POSS Position synchronisation frame (ID3v2.3+ only)
            #// There may only be one 'POSS' frame in each tag
            #// <Head for 'Position synchronisation', ID: 'POSS'>
            #// Time stamp format         $xx
            #// Position                  $xx (xx ...)
            frame_offset_ = 0
            parsedFrame_["timestampformat"] = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            frame_offset_ += 1
            parsedFrame_["position"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], frame_offset_))
            parsedFrame_["data"] = None
        elif id3v2_majorversion_ >= 3 and parsedFrame_["frame_name"] == "USER":
            #// 4.22  USER Terms of use (ID3v2.3+ only)
            #// There may be more than one 'Terms of use' frame in a tag,
            #// but only one with the same 'Language'
            #// <Header for 'Terms of use frame', ID: 'USER'>
            #// Text encoding        $xx
            #// Language             $xx xx xx
            #// The actual text      <text string according to encoding>
            frame_offset_ = 0
            frame_textencoding_ = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            frame_offset_ += 1
            if id3v2_majorversion_ <= 3 and frame_textencoding_ > 1 or id3v2_majorversion_ == 4 and frame_textencoding_ > 3:
                self.warning("Invalid text encoding byte (" + frame_textencoding_ + ") in frame \"" + parsedFrame_["frame_name"] + "\" - defaulting to ISO-8859-1 encoding")
            # end if
            frame_language_ = php_substr(parsedFrame_["data"], frame_offset_, 3)
            frame_offset_ += 3
            parsedFrame_["language"] = frame_language_
            parsedFrame_["languagename"] = self.languagelookup(frame_language_, False)
            parsedFrame_["encodingid"] = frame_textencoding_
            parsedFrame_["encoding"] = self.textencodingnamelookup(frame_textencoding_)
            parsedFrame_["data"] = php_str(php_substr(parsedFrame_["data"], frame_offset_))
            parsedFrame_["data"] = self.removestringterminator(parsedFrame_["data"], self.textencodingterminatorlookup(frame_textencoding_))
            if (not php_empty(lambda : parsedFrame_["framenameshort"])) and (not php_empty(lambda : parsedFrame_["data"])):
                info_["id3v2"]["comments"][parsedFrame_["framenameshort"]][-1] = getid3_lib.iconv_fallback(parsedFrame_["encoding"], info_["id3v2"]["encoding"], parsedFrame_["data"])
            # end if
            parsedFrame_["data"] = None
        elif id3v2_majorversion_ >= 3 and parsedFrame_["frame_name"] == "OWNE":
            #// 4.23  OWNE Ownership frame (ID3v2.3+ only)
            #// There may only be one 'OWNE' frame in a tag
            #// <Header for 'Ownership frame', ID: 'OWNE'>
            #// Text encoding     $xx
            #// Price paid        <text string> $00
            #// Date of purch.    <text string>
            #// Seller            <text string according to encoding>
            frame_offset_ = 0
            frame_textencoding_ = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            frame_offset_ += 1
            if id3v2_majorversion_ <= 3 and frame_textencoding_ > 1 or id3v2_majorversion_ == 4 and frame_textencoding_ > 3:
                self.warning("Invalid text encoding byte (" + frame_textencoding_ + ") in frame \"" + parsedFrame_["frame_name"] + "\" - defaulting to ISO-8859-1 encoding")
            # end if
            parsedFrame_["encodingid"] = frame_textencoding_
            parsedFrame_["encoding"] = self.textencodingnamelookup(frame_textencoding_)
            frame_terminatorpos_ = php_strpos(parsedFrame_["data"], " ", frame_offset_)
            frame_pricepaid_ = php_substr(parsedFrame_["data"], frame_offset_, frame_terminatorpos_ - frame_offset_)
            frame_offset_ = frame_terminatorpos_ + php_strlen(" ")
            parsedFrame_["pricepaid"]["currencyid"] = php_substr(frame_pricepaid_, 0, 3)
            parsedFrame_["pricepaid"]["currency"] = self.lookupcurrencyunits(parsedFrame_["pricepaid"]["currencyid"])
            parsedFrame_["pricepaid"]["value"] = php_substr(frame_pricepaid_, 3)
            parsedFrame_["purchasedate"] = php_substr(parsedFrame_["data"], frame_offset_, 8)
            if self.isvaliddatestampstring(parsedFrame_["purchasedate"]):
                parsedFrame_["purchasedateunix"] = mktime(0, 0, 0, php_substr(parsedFrame_["purchasedate"], 4, 2), php_substr(parsedFrame_["purchasedate"], 6, 2), php_substr(parsedFrame_["purchasedate"], 0, 4))
            # end if
            frame_offset_ += 8
            parsedFrame_["seller"] = php_str(php_substr(parsedFrame_["data"], frame_offset_))
            parsedFrame_["seller"] = self.removestringterminator(parsedFrame_["seller"], self.textencodingterminatorlookup(frame_textencoding_))
            parsedFrame_["data"] = None
        elif id3v2_majorversion_ >= 3 and parsedFrame_["frame_name"] == "COMR":
            #// 4.24  COMR Commercial frame (ID3v2.3+ only)
            #// There may be more than one 'commercial frame' in a tag,
            #// but no two may be identical
            #// <Header for 'Commercial frame', ID: 'COMR'>
            #// Text encoding      $xx
            #// Price string       <text string> $00
            #// Valid until        <text string>
            #// Contact URL        <text string> $00
            #// Received as        $xx
            #// Name of seller     <text string according to encoding> $00 (00)
            #// Description        <text string according to encoding> $00 (00)
            #// Picture MIME type  <string> $00
            #// Seller logo        <binary data>
            frame_offset_ = 0
            frame_textencoding_ = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            frame_offset_ += 1
            frame_textencoding_terminator_ = self.textencodingterminatorlookup(frame_textencoding_)
            if id3v2_majorversion_ <= 3 and frame_textencoding_ > 1 or id3v2_majorversion_ == 4 and frame_textencoding_ > 3:
                self.warning("Invalid text encoding byte (" + frame_textencoding_ + ") in frame \"" + parsedFrame_["frame_name"] + "\" - defaulting to ISO-8859-1 encoding")
                frame_textencoding_terminator_ = " "
            # end if
            frame_terminatorpos_ = php_strpos(parsedFrame_["data"], " ", frame_offset_)
            frame_pricestring_ = php_substr(parsedFrame_["data"], frame_offset_, frame_terminatorpos_ - frame_offset_)
            frame_offset_ = frame_terminatorpos_ + php_strlen(" ")
            frame_rawpricearray_ = php_explode("/", frame_pricestring_)
            for key_,val_ in frame_rawpricearray_.items():
                frame_currencyid_ = php_substr(val_, 0, 3)
                parsedFrame_["price"][frame_currencyid_]["currency"] = self.lookupcurrencyunits(frame_currencyid_)
                parsedFrame_["price"][frame_currencyid_]["value"] = php_substr(val_, 3)
            # end for
            frame_datestring_ = php_substr(parsedFrame_["data"], frame_offset_, 8)
            frame_offset_ += 8
            frame_terminatorpos_ = php_strpos(parsedFrame_["data"], " ", frame_offset_)
            frame_contacturl_ = php_substr(parsedFrame_["data"], frame_offset_, frame_terminatorpos_ - frame_offset_)
            frame_offset_ = frame_terminatorpos_ + php_strlen(" ")
            frame_receivedasid_ = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            frame_offset_ += 1
            frame_terminatorpos_ = php_strpos(parsedFrame_["data"], frame_textencoding_terminator_, frame_offset_)
            if php_ord(php_substr(parsedFrame_["data"], frame_terminatorpos_ + php_strlen(frame_textencoding_terminator_), 1)) == 0:
                frame_terminatorpos_ += 1
                pass
            # end if
            frame_sellername_ = php_substr(parsedFrame_["data"], frame_offset_, frame_terminatorpos_ - frame_offset_)
            if php_ord(frame_sellername_) == 0:
                frame_sellername_ = ""
            # end if
            frame_offset_ = frame_terminatorpos_ + php_strlen(frame_textencoding_terminator_)
            frame_terminatorpos_ = php_strpos(parsedFrame_["data"], frame_textencoding_terminator_, frame_offset_)
            if php_ord(php_substr(parsedFrame_["data"], frame_terminatorpos_ + php_strlen(frame_textencoding_terminator_), 1)) == 0:
                frame_terminatorpos_ += 1
                pass
            # end if
            parsedFrame_["description"] = php_substr(parsedFrame_["data"], frame_offset_, frame_terminatorpos_ - frame_offset_)
            parsedFrame_["description"] = self.makeutf16emptystringempty(parsedFrame_["description"])
            frame_offset_ = frame_terminatorpos_ + php_strlen(frame_textencoding_terminator_)
            frame_terminatorpos_ = php_strpos(parsedFrame_["data"], " ", frame_offset_)
            frame_mimetype_ = php_substr(parsedFrame_["data"], frame_offset_, frame_terminatorpos_ - frame_offset_)
            frame_offset_ = frame_terminatorpos_ + php_strlen(" ")
            frame_sellerlogo_ = php_substr(parsedFrame_["data"], frame_offset_)
            parsedFrame_["encodingid"] = frame_textencoding_
            parsedFrame_["encoding"] = self.textencodingnamelookup(frame_textencoding_)
            parsedFrame_["pricevaliduntil"] = frame_datestring_
            parsedFrame_["contacturl"] = frame_contacturl_
            parsedFrame_["receivedasid"] = frame_receivedasid_
            parsedFrame_["receivedas"] = self.comrreceivedaslookup(frame_receivedasid_)
            parsedFrame_["sellername"] = frame_sellername_
            parsedFrame_["mime"] = frame_mimetype_
            parsedFrame_["logo"] = frame_sellerlogo_
            parsedFrame_["data"] = None
        elif id3v2_majorversion_ >= 3 and parsedFrame_["frame_name"] == "ENCR":
            #// 4.25  ENCR Encryption method registration (ID3v2.3+ only)
            #// There may be several 'ENCR' frames in a tag,
            #// but only one containing the same symbol
            #// and only one containing the same owner identifier
            #// <Header for 'Encryption method registration', ID: 'ENCR'>
            #// Owner identifier    <text string> $00
            #// Method symbol       $xx
            #// Encryption data     <binary data>
            frame_offset_ = 0
            frame_terminatorpos_ = php_strpos(parsedFrame_["data"], " ", frame_offset_)
            frame_ownerid_ = php_substr(parsedFrame_["data"], frame_offset_, frame_terminatorpos_ - frame_offset_)
            if php_ord(frame_ownerid_) == 0:
                frame_ownerid_ = ""
            # end if
            frame_offset_ = frame_terminatorpos_ + php_strlen(" ")
            parsedFrame_["ownerid"] = frame_ownerid_
            parsedFrame_["methodsymbol"] = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            frame_offset_ += 1
            parsedFrame_["data"] = php_str(php_substr(parsedFrame_["data"], frame_offset_))
        elif id3v2_majorversion_ >= 3 and parsedFrame_["frame_name"] == "GRID":
            #// 4.26  GRID Group identification registration (ID3v2.3+ only)
            #// There may be several 'GRID' frames in a tag,
            #// but only one containing the same symbol
            #// and only one containing the same owner identifier
            #// <Header for 'Group ID registration', ID: 'GRID'>
            #// Owner identifier      <text string> $00
            #// Group symbol          $xx
            #// Group dependent data  <binary data>
            frame_offset_ = 0
            frame_terminatorpos_ = php_strpos(parsedFrame_["data"], " ", frame_offset_)
            frame_ownerid_ = php_substr(parsedFrame_["data"], frame_offset_, frame_terminatorpos_ - frame_offset_)
            if php_ord(frame_ownerid_) == 0:
                frame_ownerid_ = ""
            # end if
            frame_offset_ = frame_terminatorpos_ + php_strlen(" ")
            parsedFrame_["ownerid"] = frame_ownerid_
            parsedFrame_["groupsymbol"] = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            frame_offset_ += 1
            parsedFrame_["data"] = php_str(php_substr(parsedFrame_["data"], frame_offset_))
        elif id3v2_majorversion_ >= 3 and parsedFrame_["frame_name"] == "PRIV":
            #// 4.27  PRIV Private frame (ID3v2.3+ only)
            #// The tag may contain more than one 'PRIV' frame
            #// but only with different contents
            #// <Header for 'Private frame', ID: 'PRIV'>
            #// Owner identifier      <text string> $00
            #// The private data      <binary data>
            frame_offset_ = 0
            frame_terminatorpos_ = php_strpos(parsedFrame_["data"], " ", frame_offset_)
            frame_ownerid_ = php_substr(parsedFrame_["data"], frame_offset_, frame_terminatorpos_ - frame_offset_)
            if php_ord(frame_ownerid_) == 0:
                frame_ownerid_ = ""
            # end if
            frame_offset_ = frame_terminatorpos_ + php_strlen(" ")
            parsedFrame_["ownerid"] = frame_ownerid_
            parsedFrame_["data"] = php_str(php_substr(parsedFrame_["data"], frame_offset_))
        elif id3v2_majorversion_ >= 4 and parsedFrame_["frame_name"] == "SIGN":
            #// 4.28  SIGN Signature frame (ID3v2.4+ only)
            #// There may be more than one 'signature frame' in a tag,
            #// but no two may be identical
            #// <Header for 'Signature frame', ID: 'SIGN'>
            #// Group symbol      $xx
            #// Signature         <binary data>
            frame_offset_ = 0
            parsedFrame_["groupsymbol"] = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            frame_offset_ += 1
            parsedFrame_["data"] = php_str(php_substr(parsedFrame_["data"], frame_offset_))
        elif id3v2_majorversion_ >= 4 and parsedFrame_["frame_name"] == "SEEK":
            #// 4.29  SEEK Seek frame (ID3v2.4+ only)
            #// There may only be one 'seek frame' in a tag
            #// <Header for 'Seek frame', ID: 'SEEK'>
            #// Minimum offset to next tag       $xx xx xx xx
            frame_offset_ = 0
            parsedFrame_["data"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], frame_offset_, 4))
        elif id3v2_majorversion_ >= 4 and parsedFrame_["frame_name"] == "ASPI":
            #// 4.30  ASPI Audio seek point index (ID3v2.4+ only)
            #// There may only be one 'audio seek point index' frame in a tag
            #// <Header for 'Seek Point Index', ID: 'ASPI'>
            #// Indexed data start (S)         $xx xx xx xx
            #// Indexed data length (L)        $xx xx xx xx
            #// Number of index points (N)     $xx xx
            #// Bits per index point (b)       $xx
            #// Then for every index point the following data is included:
            #// Fraction at index (Fi)          $xx (xx)
            frame_offset_ = 0
            parsedFrame_["datastart"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], frame_offset_, 4))
            frame_offset_ += 4
            parsedFrame_["indexeddatalength"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], frame_offset_, 4))
            frame_offset_ += 4
            parsedFrame_["indexpoints"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], frame_offset_, 2))
            frame_offset_ += 2
            parsedFrame_["bitsperpoint"] = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            frame_offset_ += 1
            frame_bytesperpoint_ = ceil(parsedFrame_["bitsperpoint"] / 8)
            i_ = 0
            while i_ < parsedFrame_["indexpoints"]:
                
                parsedFrame_["indexes"][i_] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], frame_offset_, frame_bytesperpoint_))
                frame_offset_ += frame_bytesperpoint_
                i_ += 1
            # end while
            parsedFrame_["data"] = None
        elif id3v2_majorversion_ >= 3 and parsedFrame_["frame_name"] == "RGAD":
            #// Replay Gain Adjustment
            #// http://privatewww.essex.ac.uk/~djmrob/replaygain/file_format_id3v2.html
            #// There may only be one 'RGAD' frame in a tag
            #// <Header for 'Replay Gain Adjustment', ID: 'RGAD'>
            #// Peak Amplitude                      $xx $xx $xx $xx
            #// Radio Replay Gain Adjustment        %aaabbbcd %dddddddd
            #// Audiophile Replay Gain Adjustment   %aaabbbcd %dddddddd
            #// a - name code
            #// b - originator code
            #// c - sign bit
            #// d - replay gain adjustment
            frame_offset_ = 0
            parsedFrame_["peakamplitude"] = getid3_lib.bigendian2float(php_substr(parsedFrame_["data"], frame_offset_, 4))
            frame_offset_ += 4
            rg_track_adjustment_ = getid3_lib.dec2bin(php_substr(parsedFrame_["data"], frame_offset_, 2))
            frame_offset_ += 2
            rg_album_adjustment_ = getid3_lib.dec2bin(php_substr(parsedFrame_["data"], frame_offset_, 2))
            frame_offset_ += 2
            parsedFrame_["raw"]["track"]["name"] = getid3_lib.bin2dec(php_substr(rg_track_adjustment_, 0, 3))
            parsedFrame_["raw"]["track"]["originator"] = getid3_lib.bin2dec(php_substr(rg_track_adjustment_, 3, 3))
            parsedFrame_["raw"]["track"]["signbit"] = getid3_lib.bin2dec(php_substr(rg_track_adjustment_, 6, 1))
            parsedFrame_["raw"]["track"]["adjustment"] = getid3_lib.bin2dec(php_substr(rg_track_adjustment_, 7, 9))
            parsedFrame_["raw"]["album"]["name"] = getid3_lib.bin2dec(php_substr(rg_album_adjustment_, 0, 3))
            parsedFrame_["raw"]["album"]["originator"] = getid3_lib.bin2dec(php_substr(rg_album_adjustment_, 3, 3))
            parsedFrame_["raw"]["album"]["signbit"] = getid3_lib.bin2dec(php_substr(rg_album_adjustment_, 6, 1))
            parsedFrame_["raw"]["album"]["adjustment"] = getid3_lib.bin2dec(php_substr(rg_album_adjustment_, 7, 9))
            parsedFrame_["track"]["name"] = getid3_lib.rgadnamelookup(parsedFrame_["raw"]["track"]["name"])
            parsedFrame_["track"]["originator"] = getid3_lib.rgadoriginatorlookup(parsedFrame_["raw"]["track"]["originator"])
            parsedFrame_["track"]["adjustment"] = getid3_lib.rgadadjustmentlookup(parsedFrame_["raw"]["track"]["adjustment"], parsedFrame_["raw"]["track"]["signbit"])
            parsedFrame_["album"]["name"] = getid3_lib.rgadnamelookup(parsedFrame_["raw"]["album"]["name"])
            parsedFrame_["album"]["originator"] = getid3_lib.rgadoriginatorlookup(parsedFrame_["raw"]["album"]["originator"])
            parsedFrame_["album"]["adjustment"] = getid3_lib.rgadadjustmentlookup(parsedFrame_["raw"]["album"]["adjustment"], parsedFrame_["raw"]["album"]["signbit"])
            info_["replay_gain"]["track"]["peak"] = parsedFrame_["peakamplitude"]
            info_["replay_gain"]["track"]["originator"] = parsedFrame_["track"]["originator"]
            info_["replay_gain"]["track"]["adjustment"] = parsedFrame_["track"]["adjustment"]
            info_["replay_gain"]["album"]["originator"] = parsedFrame_["album"]["originator"]
            info_["replay_gain"]["album"]["adjustment"] = parsedFrame_["album"]["adjustment"]
            parsedFrame_["data"] = None
        elif id3v2_majorversion_ >= 3 and parsedFrame_["frame_name"] == "CHAP":
            #// CHAP Chapters frame (ID3v2.3+ only)
            #// http://id3.org/id3v2-chapters-1.0
            #// <ID3v2.3 or ID3v2.4 frame header, ID: "CHAP">           (10 bytes)
            #// Element ID      <text string> $00
            #// Start time      $xx xx xx xx
            #// End time        $xx xx xx xx
            #// Start offset    $xx xx xx xx
            #// End offset      $xx xx xx xx
            #// <Optional embedded sub-frames>
            frame_offset_ = 0
            php_no_error(lambda: parsedFrame_["element_id"] = php_explode(" ", parsedFrame_["data"], 2))
            frame_offset_ += php_strlen(parsedFrame_["element_id"] + " ")
            parsedFrame_["time_begin"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], frame_offset_, 4))
            frame_offset_ += 4
            parsedFrame_["time_end"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], frame_offset_, 4))
            frame_offset_ += 4
            if php_substr(parsedFrame_["data"], frame_offset_, 4) != "ÿÿÿÿ":
                #// "If these bytes are all set to 0xFF then the value should be ignored and the start time value should be utilized."
                parsedFrame_["offset_begin"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], frame_offset_, 4))
            # end if
            frame_offset_ += 4
            if php_substr(parsedFrame_["data"], frame_offset_, 4) != "ÿÿÿÿ":
                #// "If these bytes are all set to 0xFF then the value should be ignored and the start time value should be utilized."
                parsedFrame_["offset_end"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], frame_offset_, 4))
            # end if
            frame_offset_ += 4
            if frame_offset_ < php_strlen(parsedFrame_["data"]):
                parsedFrame_["subframes"] = Array()
                while True:
                    
                    if not (frame_offset_ < php_strlen(parsedFrame_["data"])):
                        break
                    # end if
                    #// <Optional embedded sub-frames>
                    subframe_ = Array()
                    subframe_["name"] = php_substr(parsedFrame_["data"], frame_offset_, 4)
                    frame_offset_ += 4
                    subframe_["size"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], frame_offset_, 4))
                    frame_offset_ += 4
                    subframe_["flags_raw"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], frame_offset_, 2))
                    frame_offset_ += 2
                    if subframe_["size"] > php_strlen(parsedFrame_["data"]) - frame_offset_:
                        self.warning("CHAP subframe \"" + subframe_["name"] + "\" at frame offset " + frame_offset_ + " claims to be \"" + subframe_["size"] + "\" bytes, which is more than the available data (" + php_strlen(parsedFrame_["data"]) - frame_offset_ + " bytes)")
                        break
                    # end if
                    subframe_rawdata_ = php_substr(parsedFrame_["data"], frame_offset_, subframe_["size"])
                    frame_offset_ += subframe_["size"]
                    subframe_["encodingid"] = php_ord(php_substr(subframe_rawdata_, 0, 1))
                    subframe_["text"] = php_substr(subframe_rawdata_, 1)
                    subframe_["encoding"] = self.textencodingnamelookup(subframe_["encodingid"])
                    encoding_converted_text_ = php_trim(getid3_lib.iconv_fallback(subframe_["encoding"], info_["encoding"], subframe_["text"]))
                    for case in Switch(php_substr(encoding_converted_text_, 0, 2)):
                        if case("ÿþ"):
                            pass
                        # end if
                        if case("þÿ"):
                            for case in Switch(php_strtoupper(info_["id3v2"]["encoding"])):
                                if case("ISO-8859-1"):
                                    pass
                                # end if
                                if case("UTF-8"):
                                    encoding_converted_text_ = php_substr(encoding_converted_text_, 2)
                                    break
                                # end if
                                if case():
                                    break
                                # end if
                            # end for
                            break
                        # end if
                        if case():
                            break
                        # end if
                    # end for
                    for case in Switch(subframe_["name"]):
                        if case("TIT2"):
                            parsedFrame_["chapter_name"] = encoding_converted_text_
                            parsedFrame_["subframes"][-1] = subframe_
                            break
                        # end if
                        if case("TIT3"):
                            parsedFrame_["chapter_description"] = encoding_converted_text_
                            parsedFrame_["subframes"][-1] = subframe_
                            break
                        # end if
                        if case("WXXX"):
                            subframe_["chapter_url_description"], subframe_["chapter_url"] = php_explode(" ", encoding_converted_text_, 2)
                            parsedFrame_["chapter_url"][subframe_["chapter_url_description"]] = subframe_["chapter_url"]
                            parsedFrame_["subframes"][-1] = subframe_
                            break
                        # end if
                        if case("APIC"):
                            if php_preg_match("#^([^\\x00]+)*\\x00(.)([^\\x00]+)*\\x00(.+)$#s", subframe_["text"], matches_):
                                dummy_, subframe_apic_mime_, subframe_apic_picturetype_, subframe_apic_description_, subframe_apic_picturedata_ = matches_
                                subframe_["image_mime"] = php_trim(getid3_lib.iconv_fallback(subframe_["encoding"], info_["encoding"], subframe_apic_mime_))
                                subframe_["picture_type"] = self.apicpicturetypelookup(subframe_apic_picturetype_)
                                subframe_["description"] = php_trim(getid3_lib.iconv_fallback(subframe_["encoding"], info_["encoding"], subframe_apic_description_))
                                if php_strlen(self.textencodingterminatorlookup(subframe_["encoding"])) == 2:
                                    #// the null terminator between "description" and "picture data" could be either 1 byte (ISO-8859-1, UTF-8) or two bytes (UTF-16)
                                    #// the above regex assumes one byte, if it's actually two then strip the second one here
                                    subframe_apic_picturedata_ = php_substr(subframe_apic_picturedata_, 1)
                                # end if
                                subframe_["data"] = subframe_apic_picturedata_
                                dummy_ = None
                                subframe_apic_mime_ = None
                                subframe_apic_picturetype_ = None
                                subframe_apic_description_ = None
                                subframe_apic_picturedata_ = None
                                subframe_["text"] = None
                                parsedFrame_["text"] = None
                                parsedFrame_["subframes"][-1] = subframe_
                                parsedFrame_["picture_present"] = True
                            else:
                                self.warning("ID3v2.CHAP subframe #" + php_count(parsedFrame_["subframes"]) + 1 + " \"" + subframe_["name"] + "\" not in expected format")
                            # end if
                            break
                        # end if
                        if case():
                            self.warning("ID3v2.CHAP subframe \"" + subframe_["name"] + "\" not handled (supported: TIT2, TIT3, WXXX, APIC)")
                            break
                        # end if
                    # end for
                # end while
                subframe_rawdata_ = None
                subframe_ = None
                encoding_converted_text_ = None
                parsedFrame_["data"] = None
                pass
            # end if
            id3v2_chapter_entry_ = Array()
            for id3v2_chapter_key_ in Array("id", "time_begin", "time_end", "offset_begin", "offset_end", "chapter_name", "chapter_description", "chapter_url", "picture_present"):
                if (php_isset(lambda : parsedFrame_[id3v2_chapter_key_])):
                    id3v2_chapter_entry_[id3v2_chapter_key_] = parsedFrame_[id3v2_chapter_key_]
                # end if
            # end for
            if (not (php_isset(lambda : info_["id3v2"]["chapters"]))):
                info_["id3v2"]["chapters"] = Array()
            # end if
            info_["id3v2"]["chapters"][-1] = id3v2_chapter_entry_
            id3v2_chapter_entry_ = None
            id3v2_chapter_key_ = None
        elif id3v2_majorversion_ >= 3 and parsedFrame_["frame_name"] == "CTOC":
            #// CTOC Chapters Table Of Contents frame (ID3v2.3+ only)
            #// http://id3.org/id3v2-chapters-1.0
            #// <ID3v2.3 or ID3v2.4 frame header, ID: "CTOC">           (10 bytes)
            #// Element ID      <text string> $00
            #// CTOC flags        %xx
            #// Entry count       $xx
            #// Child Element ID  <string>$00   /* zero or more child CHAP or CTOC entries
            #// <Optional embedded sub-frames>
            frame_offset_ = 0
            php_no_error(lambda: parsedFrame_["element_id"] = php_explode(" ", parsedFrame_["data"], 2))
            frame_offset_ += php_strlen(parsedFrame_["element_id"] + " ")
            ctoc_flags_raw_ = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            parsedFrame_["entry_count"] = php_ord(php_substr(parsedFrame_["data"], frame_offset_, 1))
            frame_offset_ += 1
            terminator_position_ = None
            i_ = 0
            while i_ < parsedFrame_["entry_count"]:
                
                terminator_position_ = php_strpos(parsedFrame_["data"], " ", frame_offset_)
                parsedFrame_["child_element_ids"][i_] = php_substr(parsedFrame_["data"], frame_offset_, terminator_position_ - frame_offset_)
                frame_offset_ = terminator_position_ + 1
                i_ += 1
            # end while
            parsedFrame_["ctoc_flags"]["ordered"] = php_bool(ctoc_flags_raw_ & 1)
            parsedFrame_["ctoc_flags"]["top_level"] = php_bool(ctoc_flags_raw_ & 3)
            ctoc_flags_raw_ = None
            terminator_position_ = None
            if frame_offset_ < php_strlen(parsedFrame_["data"]):
                parsedFrame_["subframes"] = Array()
                while True:
                    
                    if not (frame_offset_ < php_strlen(parsedFrame_["data"])):
                        break
                    # end if
                    #// <Optional embedded sub-frames>
                    subframe_ = Array()
                    subframe_["name"] = php_substr(parsedFrame_["data"], frame_offset_, 4)
                    frame_offset_ += 4
                    subframe_["size"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], frame_offset_, 4))
                    frame_offset_ += 4
                    subframe_["flags_raw"] = getid3_lib.bigendian2int(php_substr(parsedFrame_["data"], frame_offset_, 2))
                    frame_offset_ += 2
                    if subframe_["size"] > php_strlen(parsedFrame_["data"]) - frame_offset_:
                        self.warning("CTOS subframe \"" + subframe_["name"] + "\" at frame offset " + frame_offset_ + " claims to be \"" + subframe_["size"] + "\" bytes, which is more than the available data (" + php_strlen(parsedFrame_["data"]) - frame_offset_ + " bytes)")
                        break
                    # end if
                    subframe_rawdata_ = php_substr(parsedFrame_["data"], frame_offset_, subframe_["size"])
                    frame_offset_ += subframe_["size"]
                    subframe_["encodingid"] = php_ord(php_substr(subframe_rawdata_, 0, 1))
                    subframe_["text"] = php_substr(subframe_rawdata_, 1)
                    subframe_["encoding"] = self.textencodingnamelookup(subframe_["encodingid"])
                    encoding_converted_text_ = php_trim(getid3_lib.iconv_fallback(subframe_["encoding"], info_["encoding"], subframe_["text"]))
                    for case in Switch(php_substr(encoding_converted_text_, 0, 2)):
                        if case("ÿþ"):
                            pass
                        # end if
                        if case("þÿ"):
                            for case in Switch(php_strtoupper(info_["id3v2"]["encoding"])):
                                if case("ISO-8859-1"):
                                    pass
                                # end if
                                if case("UTF-8"):
                                    encoding_converted_text_ = php_substr(encoding_converted_text_, 2)
                                    break
                                # end if
                                if case():
                                    break
                                # end if
                            # end for
                            break
                        # end if
                        if case():
                            break
                        # end if
                    # end for
                    if subframe_["name"] == "TIT2" or subframe_["name"] == "TIT3":
                        if subframe_["name"] == "TIT2":
                            parsedFrame_["toc_name"] = encoding_converted_text_
                        elif subframe_["name"] == "TIT3":
                            parsedFrame_["toc_description"] = encoding_converted_text_
                        # end if
                        parsedFrame_["subframes"][-1] = subframe_
                    else:
                        self.warning("ID3v2.CTOC subframe \"" + subframe_["name"] + "\" not handled (only TIT2 and TIT3)")
                    # end if
                # end while
                subframe_rawdata_ = None
                subframe_ = None
                encoding_converted_text_ = None
            # end if
        # end if
        return True
    # end def parseid3v2frame
    #// 
    #// @param string $data
    #// 
    #// @return string
    #//
    def deunsynchronise(self, data_=None):
        
        
        return php_str_replace("ÿ ", "ÿ", data_)
    # end def deunsynchronise
    #// 
    #// @param int $index
    #// 
    #// @return string
    #//
    def lookupextendedheaderrestrictionstagsizelimits(self, index_=None):
        
        
        LookupExtendedHeaderRestrictionsTagSizeLimits_ = Array({0: "No more than 128 frames and 1 MB total tag size", 1: "No more than 64 frames and 128 KB total tag size", 2: "No more than 32 frames and 40 KB total tag size", 3: "No more than 32 frames and 4 KB total tag size"})
        return LookupExtendedHeaderRestrictionsTagSizeLimits_[index_] if (php_isset(lambda : LookupExtendedHeaderRestrictionsTagSizeLimits_[index_])) else ""
    # end def lookupextendedheaderrestrictionstagsizelimits
    #// 
    #// @param int $index
    #// 
    #// @return string
    #//
    def lookupextendedheaderrestrictionstextencodings(self, index_=None):
        
        
        LookupExtendedHeaderRestrictionsTextEncodings_ = Array({0: "No restrictions", 1: "Strings are only encoded with ISO-8859-1 or UTF-8"})
        return LookupExtendedHeaderRestrictionsTextEncodings_[index_] if (php_isset(lambda : LookupExtendedHeaderRestrictionsTextEncodings_[index_])) else ""
    # end def lookupextendedheaderrestrictionstextencodings
    #// 
    #// @param int $index
    #// 
    #// @return string
    #//
    def lookupextendedheaderrestrictionstextfieldsize(self, index_=None):
        
        
        LookupExtendedHeaderRestrictionsTextFieldSize_ = Array({0: "No restrictions", 1: "No string is longer than 1024 characters", 2: "No string is longer than 128 characters", 3: "No string is longer than 30 characters"})
        return LookupExtendedHeaderRestrictionsTextFieldSize_[index_] if (php_isset(lambda : LookupExtendedHeaderRestrictionsTextFieldSize_[index_])) else ""
    # end def lookupextendedheaderrestrictionstextfieldsize
    #// 
    #// @param int $index
    #// 
    #// @return string
    #//
    def lookupextendedheaderrestrictionsimageencoding(self, index_=None):
        
        
        LookupExtendedHeaderRestrictionsImageEncoding_ = Array({0: "No restrictions", 1: "Images are encoded only with PNG or JPEG"})
        return LookupExtendedHeaderRestrictionsImageEncoding_[index_] if (php_isset(lambda : LookupExtendedHeaderRestrictionsImageEncoding_[index_])) else ""
    # end def lookupextendedheaderrestrictionsimageencoding
    #// 
    #// @param int $index
    #// 
    #// @return string
    #//
    def lookupextendedheaderrestrictionsimagesizesize(self, index_=None):
        
        
        LookupExtendedHeaderRestrictionsImageSizeSize_ = Array({0: "No restrictions", 1: "All images are 256x256 pixels or smaller", 2: "All images are 64x64 pixels or smaller", 3: "All images are exactly 64x64 pixels, unless required otherwise"})
        return LookupExtendedHeaderRestrictionsImageSizeSize_[index_] if (php_isset(lambda : LookupExtendedHeaderRestrictionsImageSizeSize_[index_])) else ""
    # end def lookupextendedheaderrestrictionsimagesizesize
    #// 
    #// @param string $currencyid
    #// 
    #// @return string
    #//
    def lookupcurrencyunits(self, currencyid_=None):
        
        
        begin_ = 0
        #// This is not a comment!
        #// AED Dirhams
        #// AFA Afghanis
        #// ALL Leke
        #// AMD Drams
        #// ANG Guilders
        #// AOA Kwanza
        #// ARS Pesos
        #// ATS Schillings
        #// AUD Dollars
        #// AWG Guilders
        #// AZM Manats
        #// BAM Convertible Marka
        #// BBD Dollars
        #// BDT Taka
        #// BEF Francs
        #// BGL Leva
        #// BHD Dinars
        #// BIF Francs
        #// BMD Dollars
        #// BND Dollars
        #// BOB Bolivianos
        #// BRL Brazil Real
        #// BSD Dollars
        #// BTN Ngultrum
        #// BWP Pulas
        #// BYR Rubles
        #// BZD Dollars
        #// CAD Dollars
        #// CDF Congolese Francs
        #// CHF Francs
        #// CLP Pesos
        #// CNY Yuan Renminbi
        #// COP Pesos
        #// CRC Colones
        #// CUP Pesos
        #// CVE Escudos
        #// CYP Pounds
        #// CZK Koruny
        #// DEM Deutsche Marks
        #// DJF Francs
        #// DKK Kroner
        #// DOP Pesos
        #// DZD Algeria Dinars
        #// EEK Krooni
        #// EGP Pounds
        #// ERN Nakfa
        #// ESP Pesetas
        #// ETB Birr
        #// EUR Euro
        #// FIM Markkaa
        #// FJD Dollars
        #// FKP Pounds
        #// FRF Francs
        #// GBP Pounds
        #// GEL Lari
        #// GGP Pounds
        #// GHC Cedis
        #// GIP Pounds
        #// GMD Dalasi
        #// GNF Francs
        #// GRD Drachmae
        #// GTQ Quetzales
        #// GYD Dollars
        #// HKD Dollars
        #// HNL Lempiras
        #// HRK Kuna
        #// HTG Gourdes
        #// HUF Forints
        #// IDR Rupiahs
        #// IEP Pounds
        #// ILS New Shekels
        #// IMP Pounds
        #// INR Rupees
        #// IQD Dinars
        #// IRR Rials
        #// ISK Kronur
        #// ITL Lire
        #// JEP Pounds
        #// JMD Dollars
        #// JOD Dinars
        #// JPY Yen
        #// KES Shillings
        #// KGS Soms
        #// KHR Riels
        #// KMF Francs
        #// KPW Won
        #// KWD Dinars
        #// KYD Dollars
        #// KZT Tenge
        #// LAK Kips
        #// LBP Pounds
        #// LKR Rupees
        #// LRD Dollars
        #// LSL Maloti
        #// LTL Litai
        #// LUF Francs
        #// LVL Lati
        #// LYD Dinars
        #// MAD Dirhams
        #// MDL Lei
        #// MGF Malagasy Francs
        #// MKD Denars
        #// MMK Kyats
        #// MNT Tugriks
        #// MOP Patacas
        #// MRO Ouguiyas
        #// MTL Liri
        #// MUR Rupees
        #// MVR Rufiyaa
        #// MWK Kwachas
        #// MXN Pesos
        #// MYR Ringgits
        #// MZM Meticais
        #// NAD Dollars
        #// NGN Nairas
        #// NIO Gold Cordobas
        #// NLG Guilders
        #// NOK Krone
        #// NPR Nepal Rupees
        #// NZD Dollars
        #// OMR Rials
        #// PAB Balboa
        #// PEN Nuevos Soles
        #// PGK Kina
        #// PHP Pesos
        #// PKR Rupees
        #// PLN Zlotych
        #// PTE Escudos
        #// PYG Guarani
        #// QAR Rials
        #// ROL Lei
        #// RUR Rubles
        #// RWF Rwanda Francs
        #// SAR Riyals
        #// SBD Dollars
        #// SCR Rupees
        #// SDD Dinars
        #// SEK Kronor
        #// SGD Dollars
        #// SHP Pounds
        #// SIT Tolars
        #// SKK Koruny
        #// SLL Leones
        #// SOS Shillings
        #// SPL Luigini
        #// SRG Guilders
        #// STD Dobras
        #// SVC Colones
        #// SYP Pounds
        #// SZL Emalangeni
        #// THB Baht
        #// TJR Rubles
        #// TMM Manats
        #// TND Dinars
        #// TOP Pa'anga
        #// TRL Liras
        #// TTD Dollars
        #// TVD Tuvalu Dollars
        #// TWD New Dollars
        #// TZS Shillings
        #// UAH Hryvnia
        #// UGX Shillings
        #// USD Dollars
        #// UYU Pesos
        #// UZS Sums
        #// VAL Lire
        #// VEB Bolivares
        #// VND Dong
        #// VUV Vatu
        #// WST Tala
        #// XAF Francs
        #// XAG Ounces
        #// XAU Ounces
        #// XCD Dollars
        #// XDR Special Drawing Rights
        #// XPD Ounces
        #// XPF Francs
        #// XPT Ounces
        #// YER Rials
        #// YUM New Dinars
        #// ZAR Rand
        #// ZMK Kwacha
        #// ZWD Zimbabwe Dollars
        #//
        return getid3_lib.embeddedlookup(currencyid_, begin_, 0, __FILE__, "id3v2-currency-units")
    # end def lookupcurrencyunits
    #// 
    #// @param string $currencyid
    #// 
    #// @return string
    #//
    def lookupcurrencycountry(self, currencyid_=None):
        
        
        begin_ = 0
        #// This is not a comment!
        #// AED United Arab Emirates
        #// AFA Afghanistan
        #// ALL Albania
        #// AMD Armenia
        #// ANG Netherlands Antilles
        #// AOA Angola
        #// ARS Argentina
        #// ATS Austria
        #// AUD Australia
        #// AWG Aruba
        #// AZM Azerbaijan
        #// BAM Bosnia and Herzegovina
        #// BBD Barbados
        #// BDT Bangladesh
        #// BEF Belgium
        #// BGL Bulgaria
        #// BHD Bahrain
        #// BIF Burundi
        #// BMD Bermuda
        #// BND Brunei Darussalam
        #// BOB Bolivia
        #// BRL Brazil
        #// BSD Bahamas
        #// BTN Bhutan
        #// BWP Botswana
        #// BYR Belarus
        #// BZD Belize
        #// CAD Canada
        #// CDF Congo/Kinshasa
        #// CHF Switzerland
        #// CLP Chile
        #// CNY China
        #// COP Colombia
        #// CRC Costa Rica
        #// CUP Cuba
        #// CVE Cape Verde
        #// CYP Cyprus
        #// CZK Czech Republic
        #// DEM Germany
        #// DJF Djibouti
        #// DKK Denmark
        #// DOP Dominican Republic
        #// DZD Algeria
        #// EEK Estonia
        #// EGP Egypt
        #// ERN Eritrea
        #// ESP Spain
        #// ETB Ethiopia
        #// EUR Euro Member Countries
        #// FIM Finland
        #// FJD Fiji
        #// FKP Falkland Islands (Malvinas)
        #// FRF France
        #// GBP United Kingdom
        #// GEL Georgia
        #// GGP Guernsey
        #// GHC Ghana
        #// GIP Gibraltar
        #// GMD Gambia
        #// GNF Guinea
        #// GRD Greece
        #// GTQ Guatemala
        #// GYD Guyana
        #// HKD Hong Kong
        #// HNL Honduras
        #// HRK Croatia
        #// HTG Haiti
        #// HUF Hungary
        #// IDR Indonesia
        #// IEP Ireland (Eire)
        #// ILS Israel
        #// IMP Isle of Man
        #// INR India
        #// IQD Iraq
        #// IRR Iran
        #// ISK Iceland
        #// ITL Italy
        #// JEP Jersey
        #// JMD Jamaica
        #// JOD Jordan
        #// JPY Japan
        #// KES Kenya
        #// KGS Kyrgyzstan
        #// KHR Cambodia
        #// KMF Comoros
        #// KPW Korea
        #// KWD Kuwait
        #// KYD Cayman Islands
        #// KZT Kazakstan
        #// LAK Laos
        #// LBP Lebanon
        #// LKR Sri Lanka
        #// LRD Liberia
        #// LSL Lesotho
        #// LTL Lithuania
        #// LUF Luxembourg
        #// LVL Latvia
        #// LYD Libya
        #// MAD Morocco
        #// MDL Moldova
        #// MGF Madagascar
        #// MKD Macedonia
        #// MMK Myanmar (Burma)
        #// MNT Mongolia
        #// MOP Macau
        #// MRO Mauritania
        #// MTL Malta
        #// MUR Mauritius
        #// MVR Maldives (Maldive Islands)
        #// MWK Malawi
        #// MXN Mexico
        #// MYR Malaysia
        #// MZM Mozambique
        #// NAD Namibia
        #// NGN Nigeria
        #// NIO Nicaragua
        #// NLG Netherlands (Holland)
        #// NOK Norway
        #// NPR Nepal
        #// NZD New Zealand
        #// OMR Oman
        #// PAB Panama
        #// PEN Peru
        #// PGK Papua New Guinea
        #// PHP Philippines
        #// PKR Pakistan
        #// PLN Poland
        #// PTE Portugal
        #// PYG Paraguay
        #// QAR Qatar
        #// ROL Romania
        #// RUR Russia
        #// RWF Rwanda
        #// SAR Saudi Arabia
        #// SBD Solomon Islands
        #// SCR Seychelles
        #// SDD Sudan
        #// SEK Sweden
        #// SGD Singapore
        #// SHP Saint Helena
        #// SIT Slovenia
        #// SKK Slovakia
        #// SLL Sierra Leone
        #// SOS Somalia
        #// SPL Seborga
        #// SRG Suriname
        #// STD São Tome and Principe
        #// SVC El Salvador
        #// SYP Syria
        #// SZL Swaziland
        #// THB Thailand
        #// TJR Tajikistan
        #// TMM Turkmenistan
        #// TND Tunisia
        #// TOP Tonga
        #// TRL Turkey
        #// TTD Trinidad and Tobago
        #// TVD Tuvalu
        #// TWD Taiwan
        #// TZS Tanzania
        #// UAH Ukraine
        #// UGX Uganda
        #// USD United States of America
        #// UYU Uruguay
        #// UZS Uzbekistan
        #// VAL Vatican City
        #// VEB Venezuela
        #// VND Viet Nam
        #// VUV Vanuatu
        #// WST Samoa
        #// XAF Communauté Financière Africaine
        #// XAG Silver
        #// XAU Gold
        #// XCD East Caribbean
        #// XDR International Monetary Fund
        #// XPD Palladium
        #// XPF Comptoirs Français du Pacifique
        #// XPT Platinum
        #// YER Yemen
        #// YUM Yugoslavia
        #// ZAR South Africa
        #// ZMK Zambia
        #// ZWD Zimbabwe
        #//
        return getid3_lib.embeddedlookup(currencyid_, begin_, 0, __FILE__, "id3v2-currency-country")
    # end def lookupcurrencycountry
    #// 
    #// @param string $languagecode
    #// @param bool   $casesensitive
    #// 
    #// @return string
    #//
    @classmethod
    def languagelookup(self, languagecode_=None, casesensitive_=None):
        if casesensitive_ is None:
            casesensitive_ = False
        # end if
        
        if (not casesensitive_):
            languagecode_ = php_strtolower(languagecode_)
        # end if
        #// http://www.id3.org/id3v2.4.0-structure.txt
        #// [4.   ID3v2 frame overview]
        #// The three byte language field, present in several frames, is used to
        #// describe the language of the frame's content, according to ISO-639-2
        #// [ISO-639-2]. The language should be represented in lower case. If the
        #// language is not known the string "XXX" should be used.
        #// ISO 639-2 - http://www.id3.org/iso639-2.html
        begin_ = 0
        #// This is not a comment!
        #// XXX unknown
        #// xxx unknown
        #// aar Afar
        #// abk Abkhazian
        #// ace Achinese
        #// ach Acoli
        #// ada Adangme
        #// afa Afro-Asiatic (Other)
        #// afh Afrihili
        #// afr Afrikaans
        #// aka Akan
        #// akk Akkadian
        #// alb Albanian
        #// ale Aleut
        #// alg Algonquian Languages
        #// amh Amharic
        #// ang English, Old (ca. 450-1100)
        #// apa Apache Languages
        #// ara Arabic
        #// arc Aramaic
        #// arm Armenian
        #// arn Araucanian
        #// arp Arapaho
        #// art Artificial (Other)
        #// arw Arawak
        #// asm Assamese
        #// ath Athapascan Languages
        #// ava Avaric
        #// ave Avestan
        #// awa Awadhi
        #// aym Aymara
        #// aze Azerbaijani
        #// bad Banda
        #// bai Bamileke Languages
        #// bak Bashkir
        #// bal Baluchi
        #// bam Bambara
        #// ban Balinese
        #// baq Basque
        #// bas Basa
        #// bat Baltic (Other)
        #// bej Beja
        #// bel Byelorussian
        #// bem Bemba
        #// ben Bengali
        #// ber Berber (Other)
        #// bho Bhojpuri
        #// bih Bihari
        #// bik Bikol
        #// bin Bini
        #// bis Bislama
        #// bla Siksika
        #// bnt Bantu (Other)
        #// bod Tibetan
        #// bra Braj
        #// bre Breton
        #// bua Buriat
        #// bug Buginese
        #// bul Bulgarian
        #// bur Burmese
        #// cad Caddo
        #// cai Central American Indian (Other)
        #// car Carib
        #// cat Catalan
        #// cau Caucasian (Other)
        #// ceb Cebuano
        #// cel Celtic (Other)
        #// ces Czech
        #// cha Chamorro
        #// chb Chibcha
        #// che Chechen
        #// chg Chagatai
        #// chi Chinese
        #// chm Mari
        #// chn Chinook jargon
        #// cho Choctaw
        #// chr Cherokee
        #// chu Church Slavic
        #// chv Chuvash
        #// chy Cheyenne
        #// cop Coptic
        #// cor Cornish
        #// cos Corsican
        #// cpe Creoles and Pidgins, English-based (Other)
        #// cpf Creoles and Pidgins, French-based (Other)
        #// cpp Creoles and Pidgins, Portuguese-based (Other)
        #// cre Cree
        #// crp Creoles and Pidgins (Other)
        #// cus Cushitic (Other)
        #// cym Welsh
        #// cze Czech
        #// dak Dakota
        #// dan Danish
        #// del Delaware
        #// deu German
        #// din Dinka
        #// div Divehi
        #// doi Dogri
        #// dra Dravidian (Other)
        #// dua Duala
        #// dum Dutch, Middle (ca. 1050-1350)
        #// dut Dutch
        #// dyu Dyula
        #// dzo Dzongkha
        #// efi Efik
        #// egy Egyptian (Ancient)
        #// eka Ekajuk
        #// ell Greek, Modern (1453-)
        #// elx Elamite
        #// eng English
        #// enm English, Middle (ca. 1100-1500)
        #// epo Esperanto
        #// esk Eskimo (Other)
        #// esl Spanish
        #// est Estonian
        #// eus Basque
        #// ewe Ewe
        #// ewo Ewondo
        #// fan Fang
        #// fao Faroese
        #// fas Persian
        #// fat Fanti
        #// fij Fijian
        #// fin Finnish
        #// fiu Finno-Ugrian (Other)
        #// fon Fon
        #// fra French
        #// fre French
        #// frm French, Middle (ca. 1400-1600)
        #// fro French, Old (842- ca. 1400)
        #// fry Frisian
        #// ful Fulah
        #// gaa Ga
        #// gae Gaelic (Scots)
        #// gai Irish
        #// gay Gayo
        #// gdh Gaelic (Scots)
        #// gem Germanic (Other)
        #// geo Georgian
        #// ger German
        #// gez Geez
        #// gil Gilbertese
        #// glg Gallegan
        #// gmh German, Middle High (ca. 1050-1500)
        #// goh German, Old High (ca. 750-1050)
        #// gon Gondi
        #// got Gothic
        #// grb Grebo
        #// grc Greek, Ancient (to 1453)
        #// gre Greek, Modern (1453-)
        #// grn Guarani
        #// guj Gujarati
        #// hai Haida
        #// hau Hausa
        #// haw Hawaiian
        #// heb Hebrew
        #// her Herero
        #// hil Hiligaynon
        #// him Himachali
        #// hin Hindi
        #// hmo Hiri Motu
        #// hun Hungarian
        #// hup Hupa
        #// hye Armenian
        #// iba Iban
        #// ibo Igbo
        #// ice Icelandic
        #// ijo Ijo
        #// iku Inuktitut
        #// ilo Iloko
        #// ina Interlingua (International Auxiliary language Association)
        #// inc Indic (Other)
        #// ind Indonesian
        #// ine Indo-European (Other)
        #// ine Interlingue
        #// ipk Inupiak
        #// ira Iranian (Other)
        #// iri Irish
        #// iro Iroquoian uages
        #// isl Icelandic
        #// ita Italian
        #// jav Javanese
        #// jaw Javanese
        #// jpn Japanese
        #// jpr Judeo-Persian
        #// jrb Judeo-Arabic
        #// kaa Kara-Kalpak
        #// kab Kabyle
        #// kac Kachin
        #// kal Greenlandic
        #// kam Kamba
        #// kan Kannada
        #// kar Karen
        #// kas Kashmiri
        #// kat Georgian
        #// kau Kanuri
        #// kaw Kawi
        #// kaz Kazakh
        #// kha Khasi
        #// khi Khoisan (Other)
        #// khm Khmer
        #// kho Khotanese
        #// kik Kikuyu
        #// kin Kinyarwanda
        #// kir Kirghiz
        #// kok Konkani
        #// kom Komi
        #// kon Kongo
        #// kor Korean
        #// kpe Kpelle
        #// kro Kru
        #// kru Kurukh
        #// kua Kuanyama
        #// kum Kumyk
        #// kur Kurdish
        #// kus Kusaie
        #// kut Kutenai
        #// lad Ladino
        #// lah Lahnda
        #// lam Lamba
        #// lao Lao
        #// lat Latin
        #// lav Latvian
        #// lez Lezghian
        #// lin Lingala
        #// lit Lithuanian
        #// lol Mongo
        #// loz Lozi
        #// ltz Letzeburgesch
        #// lub Luba-Katanga
        #// lug Ganda
        #// lui Luiseno
        #// lun Lunda
        #// luo Luo (Kenya and Tanzania)
        #// mac Macedonian
        #// mad Madurese
        #// mag Magahi
        #// mah Marshall
        #// mai Maithili
        #// mak Macedonian
        #// mak Makasar
        #// mal Malayalam
        #// man Mandingo
        #// mao Maori
        #// map Austronesian (Other)
        #// mar Marathi
        #// mas Masai
        #// max Manx
        #// may Malay
        #// men Mende
        #// mga Irish, Middle (900 - 1200)
        #// mic Micmac
        #// min Minangkabau
        #// mis Miscellaneous (Other)
        #// mkh Mon-Kmer (Other)
        #// mlg Malagasy
        #// mlt Maltese
        #// mni Manipuri
        #// mno Manobo Languages
        #// moh Mohawk
        #// mol Moldavian
        #// mon Mongolian
        #// mos Mossi
        #// mri Maori
        #// msa Malay
        #// mul Multiple Languages
        #// mun Munda Languages
        #// mus Creek
        #// mwr Marwari
        #// mya Burmese
        #// myn Mayan Languages
        #// nah Aztec
        #// nai North American Indian (Other)
        #// nau Nauru
        #// nav Navajo
        #// nbl Ndebele, South
        #// nde Ndebele, North
        #// ndo Ndongo
        #// nep Nepali
        #// new Newari
        #// nic Niger-Kordofanian (Other)
        #// niu Niuean
        #// nla Dutch
        #// nno Norwegian (Nynorsk)
        #// non Norse, Old
        #// nor Norwegian
        #// nso Sotho, Northern
        #// nub Nubian Languages
        #// nya Nyanja
        #// nym Nyamwezi
        #// nyn Nyankole
        #// nyo Nyoro
        #// nzi Nzima
        #// oci Langue d'Oc (post 1500)
        #// oji Ojibwa
        #// ori Oriya
        #// orm Oromo
        #// osa Osage
        #// oss Ossetic
        #// ota Turkish, Ottoman (1500 - 1928)
        #// oto Otomian Languages
        #// paa Papuan-Australian (Other)
        #// pag Pangasinan
        #// pal Pahlavi
        #// pam Pampanga
        #// pan Panjabi
        #// pap Papiamento
        #// pau Palauan
        #// peo Persian, Old (ca 600 - 400 B.C.)
        #// per Persian
        #// phn Phoenician
        #// pli Pali
        #// pol Polish
        #// pon Ponape
        #// por Portuguese
        #// pra Prakrit uages
        #// pro Provencal, Old (to 1500)
        #// pus Pushto
        #// que Quechua
        #// raj Rajasthani
        #// rar Rarotongan
        #// roa Romance (Other)
        #// roh Rhaeto-Romance
        #// rom Romany
        #// ron Romanian
        #// rum Romanian
        #// run Rundi
        #// rus Russian
        #// sad Sandawe
        #// sag Sango
        #// sah Yakut
        #// sai South American Indian (Other)
        #// sal Salishan Languages
        #// sam Samaritan Aramaic
        #// san Sanskrit
        #// sco Scots
        #// scr Serbo-Croatian
        #// sel Selkup
        #// sem Semitic (Other)
        #// sga Irish, Old (to 900)
        #// shn Shan
        #// sid Sidamo
        #// sin Singhalese
        #// sio Siouan Languages
        #// sit Sino-Tibetan (Other)
        #// sla Slavic (Other)
        #// slk Slovak
        #// slo Slovak
        #// slv Slovenian
        #// smi Sami Languages
        #// smo Samoan
        #// sna Shona
        #// snd Sindhi
        #// sog Sogdian
        #// som Somali
        #// son Songhai
        #// sot Sotho, Southern
        #// spa Spanish
        #// sqi Albanian
        #// srd Sardinian
        #// srr Serer
        #// ssa Nilo-Saharan (Other)
        #// ssw Siswant
        #// ssw Swazi
        #// suk Sukuma
        #// sun Sudanese
        #// sus Susu
        #// sux Sumerian
        #// sve Swedish
        #// swa Swahili
        #// swe Swedish
        #// syr Syriac
        #// tah Tahitian
        #// tam Tamil
        #// tat Tatar
        #// tel Telugu
        #// tem Timne
        #// ter Tereno
        #// tgk Tajik
        #// tgl Tagalog
        #// tha Thai
        #// tib Tibetan
        #// tig Tigre
        #// tir Tigrinya
        #// tiv Tivi
        #// tli Tlingit
        #// tmh Tamashek
        #// tog Tonga (Nyasa)
        #// ton Tonga (Tonga Islands)
        #// tru Truk
        #// tsi Tsimshian
        #// tsn Tswana
        #// tso Tsonga
        #// tuk Turkmen
        #// tum Tumbuka
        #// tur Turkish
        #// tut Altaic (Other)
        #// twi Twi
        #// tyv Tuvinian
        #// uga Ugaritic
        #// uig Uighur
        #// ukr Ukrainian
        #// umb Umbundu
        #// und Undetermined
        #// urd Urdu
        #// uzb Uzbek
        #// vai Vai
        #// ven Venda
        #// vie Vietnamese
        #// vol Volapük
        #// vot Votic
        #// wak Wakashan Languages
        #// wal Walamo
        #// war Waray
        #// was Washo
        #// wel Welsh
        #// wen Sorbian Languages
        #// wol Wolof
        #// xho Xhosa
        #// yao Yao
        #// yap Yap
        #// yid Yiddish
        #// yor Yoruba
        #// zap Zapotec
        #// zen Zenaga
        #// zha Zhuang
        #// zho Chinese
        #// zul Zulu
        #// zun Zuni
        #//
        return getid3_lib.embeddedlookup(languagecode_, begin_, 0, __FILE__, "id3v2-languagecode")
    # end def languagelookup
    #// 
    #// @param int $index
    #// 
    #// @return string
    #//
    @classmethod
    def etcoeventlookup(self, index_=None):
        
        
        if index_ >= 23 and index_ <= 223:
            return "reserved for future use"
        # end if
        if index_ >= 224 and index_ <= 239:
            return "not predefined synch 0-F"
        # end if
        if index_ >= 240 and index_ <= 252:
            return "reserved for future use"
        # end if
        EventLookup_ = Array({0: "padding (has no meaning)", 1: "end of initial silence", 2: "intro start", 3: "main part start", 4: "outro start", 5: "outro end", 6: "verse start", 7: "refrain start", 8: "interlude start", 9: "theme start", 10: "variation start", 11: "key change", 12: "time change", 13: "momentary unwanted noise (Snap, Crackle & Pop)", 14: "sustained noise", 15: "sustained noise end", 16: "intro end", 17: "main part end", 18: "verse end", 19: "refrain end", 20: "theme end", 21: "profanity", 22: "profanity end", 253: "audio end (start of silence)", 254: "audio file ends", 255: "one more byte of events follows"})
        return EventLookup_[index_] if (php_isset(lambda : EventLookup_[index_])) else ""
    # end def etcoeventlookup
    #// 
    #// @param int $index
    #// 
    #// @return string
    #//
    @classmethod
    def sytlcontenttypelookup(self, index_=None):
        
        
        SYTLContentTypeLookup_ = Array({0: "other", 1: "lyrics", 2: "text transcription", 3: "movement/part name", 4: "events", 5: "chord", 6: "trivia/'pop up' information", 7: "URLs to webpages", 8: "URLs to images"})
        return SYTLContentTypeLookup_[index_] if (php_isset(lambda : SYTLContentTypeLookup_[index_])) else ""
    # end def sytlcontenttypelookup
    #// 
    #// @param int   $index
    #// @param bool $returnarray
    #// 
    #// @return array|string
    #//
    @classmethod
    def apicpicturetypelookup(self, index_=None, returnarray_=None):
        if returnarray_ is None:
            returnarray_ = False
        # end if
        
        APICPictureTypeLookup_ = Array({0: "Other", 1: "32x32 pixels 'file icon' (PNG only)", 2: "Other file icon", 3: "Cover (front)", 4: "Cover (back)", 5: "Leaflet page", 6: "Media (e.g. label side of CD)", 7: "Lead artist/lead performer/soloist", 8: "Artist/performer", 9: "Conductor", 10: "Band/Orchestra", 11: "Composer", 12: "Lyricist/text writer", 13: "Recording Location", 14: "During recording", 15: "During performance", 16: "Movie/video screen capture", 17: "A bright coloured fish", 18: "Illustration", 19: "Band/artist logotype", 20: "Publisher/Studio logotype"})
        if returnarray_:
            return APICPictureTypeLookup_
        # end if
        return APICPictureTypeLookup_[index_] if (php_isset(lambda : APICPictureTypeLookup_[index_])) else ""
    # end def apicpicturetypelookup
    #// 
    #// @param int $index
    #// 
    #// @return string
    #//
    @classmethod
    def comrreceivedaslookup(self, index_=None):
        
        
        COMRReceivedAsLookup_ = Array({0: "Other", 1: "Standard CD album with other songs", 2: "Compressed audio on CD", 3: "File over the Internet", 4: "Stream over the Internet", 5: "As note sheets", 6: "As note sheets in a book with other sheets", 7: "Music on other media", 8: "Non-musical merchandise"})
        return COMRReceivedAsLookup_[index_] if (php_isset(lambda : COMRReceivedAsLookup_[index_])) else ""
    # end def comrreceivedaslookup
    #// 
    #// @param int $index
    #// 
    #// @return string
    #//
    @classmethod
    def rva2channeltypelookup(self, index_=None):
        
        
        RVA2ChannelTypeLookup_ = Array({0: "Other", 1: "Master volume", 2: "Front right", 3: "Front left", 4: "Back right", 5: "Back left", 6: "Front centre", 7: "Back centre", 8: "Subwoofer"})
        return RVA2ChannelTypeLookup_[index_] if (php_isset(lambda : RVA2ChannelTypeLookup_[index_])) else ""
    # end def rva2channeltypelookup
    #// 
    #// @param string $framename
    #// 
    #// @return string
    #//
    @classmethod
    def framenamelonglookup(self, framename_=None):
        
        
        begin_ = 0
        #// This is not a comment!
        #// AENC    Audio encryption
        #// APIC    Attached picture
        #// ASPI    Audio seek point index
        #// BUF Recommended buffer size
        #// CNT Play counter
        #// COM Comments
        #// COMM    Comments
        #// COMR    Commercial frame
        #// CRA Audio encryption
        #// CRM Encrypted meta frame
        #// ENCR    Encryption method registration
        #// EQU Equalisation
        #// EQU2    Equalisation (2)
        #// EQUA    Equalisation
        #// ETC Event timing codes
        #// ETCO    Event timing codes
        #// GEO General encapsulated object
        #// GEOB    General encapsulated object
        #// GRID    Group identification registration
        #// IPL Involved people list
        #// IPLS    Involved people list
        #// LINK    Linked information
        #// LNK Linked information
        #// MCDI    Music CD identifier
        #// MCI Music CD Identifier
        #// MLL MPEG location lookup table
        #// MLLT    MPEG location lookup table
        #// OWNE    Ownership frame
        #// PCNT    Play counter
        #// PIC Attached picture
        #// POP Popularimeter
        #// POPM    Popularimeter
        #// POSS    Position synchronisation frame
        #// PRIV    Private frame
        #// RBUF    Recommended buffer size
        #// REV Reverb
        #// RVA Relative volume adjustment
        #// RVA2    Relative volume adjustment (2)
        #// RVAD    Relative volume adjustment
        #// RVRB    Reverb
        #// SEEK    Seek frame
        #// SIGN    Signature frame
        #// SLT Synchronised lyric/text
        #// STC Synced tempo codes
        #// SYLT    Synchronised lyric/text
        #// SYTC    Synchronised tempo codes
        #// TAL Album/Movie/Show title
        #// TALB    Album/Movie/Show title
        #// TBP BPM (Beats Per Minute)
        #// TBPM    BPM (beats per minute)
        #// TCM Composer
        #// TCMP    Part of a compilation
        #// TCO Content type
        #// TCOM    Composer
        #// TCON    Content type
        #// TCOP    Copyright message
        #// TCP Part of a compilation
        #// TCR Copyright message
        #// TDA Date
        #// TDAT    Date
        #// TDEN    Encoding time
        #// TDLY    Playlist delay
        #// TDOR    Original release time
        #// TDRC    Recording time
        #// TDRL    Release time
        #// TDTG    Tagging time
        #// TDY Playlist delay
        #// TEN Encoded by
        #// TENC    Encoded by
        #// TEXT    Lyricist/Text writer
        #// TFLT    File type
        #// TFT File type
        #// TIM Time
        #// TIME    Time
        #// TIPL    Involved people list
        #// TIT1    Content group description
        #// TIT2    Title/songname/content description
        #// TIT3    Subtitle/Description refinement
        #// TKE Initial key
        #// TKEY    Initial key
        #// TLA Language(s)
        #// TLAN    Language(s)
        #// TLE Length
        #// TLEN    Length
        #// TMCL    Musician credits list
        #// TMED    Media type
        #// TMOO    Mood
        #// TMT Media type
        #// TOA Original artist(s)/performer(s)
        #// TOAL    Original album/movie/show title
        #// TOF Original filename
        #// TOFN    Original filename
        #// TOL Original Lyricist(s)/text writer(s)
        #// TOLY    Original lyricist(s)/text writer(s)
        #// TOPE    Original artist(s)/performer(s)
        #// TOR Original release year
        #// TORY    Original release year
        #// TOT Original album/Movie/Show title
        #// TOWN    File owner/licensee
        #// TP1 Lead artist(s)/Lead performer(s)/Soloist(s)/Performing group
        #// TP2 Band/Orchestra/Accompaniment
        #// TP3 Conductor/Performer refinement
        #// TP4 Interpreted, remixed, or otherwise modified by
        #// TPA Part of a set
        #// TPB Publisher
        #// TPE1    Lead performer(s)/Soloist(s)
        #// TPE2    Band/orchestra/accompaniment
        #// TPE3    Conductor/performer refinement
        #// TPE4    Interpreted, remixed, or otherwise modified by
        #// TPOS    Part of a set
        #// TPRO    Produced notice
        #// TPUB    Publisher
        #// TRC ISRC (International Standard Recording Code)
        #// TRCK    Track number/Position in set
        #// TRD Recording dates
        #// TRDA    Recording dates
        #// TRK Track number/Position in set
        #// TRSN    Internet radio station name
        #// TRSO    Internet radio station owner
        #// TS2 Album-Artist sort order
        #// TSA Album sort order
        #// TSC Composer sort order
        #// TSI Size
        #// TSIZ    Size
        #// TSO2    Album-Artist sort order
        #// TSOA    Album sort order
        #// TSOC    Composer sort order
        #// TSOP    Performer sort order
        #// TSOT    Title sort order
        #// TSP Performer sort order
        #// TSRC    ISRC (international standard recording code)
        #// TSS Software/hardware and settings used for encoding
        #// TSSE    Software/Hardware and settings used for encoding
        #// TSST    Set subtitle
        #// TST Title sort order
        #// TT1 Content group description
        #// TT2 Title/Songname/Content description
        #// TT3 Subtitle/Description refinement
        #// TXT Lyricist/text writer
        #// TXX User defined text information frame
        #// TXXX    User defined text information frame
        #// TYE Year
        #// TYER    Year
        #// UFI Unique file identifier
        #// UFID    Unique file identifier
        #// ULT Unsynchronised lyric/text transcription
        #// USER    Terms of use
        #// USLT    Unsynchronised lyric/text transcription
        #// WAF Official audio file webpage
        #// WAR Official artist/performer webpage
        #// WAS Official audio source webpage
        #// WCM Commercial information
        #// WCOM    Commercial information
        #// WCOP    Copyright/Legal information
        #// WCP Copyright/Legal information
        #// WOAF    Official audio file webpage
        #// WOAR    Official artist/performer webpage
        #// WOAS    Official audio source webpage
        #// WORS    Official Internet radio station homepage
        #// WPAY    Payment
        #// WPB Publishers official webpage
        #// WPUB    Publishers official webpage
        #// WXX User defined URL link frame
        #// WXXX    User defined URL link frame
        #// TFEA    Featured Artist
        #// TSTU    Recording Studio
        #// rgad    Replay Gain Adjustment
        #//
        return getid3_lib.embeddedlookup(framename_, begin_, 0, __FILE__, "id3v2-framename_long")
        pass
    # end def framenamelonglookup
    #// 
    #// @param string $framename
    #// 
    #// @return string
    #//
    @classmethod
    def framenameshortlookup(self, framename_=None):
        
        
        begin_ = 0
        #// This is not a comment!
        #// AENC    audio_encryption
        #// APIC    attached_picture
        #// ASPI    audio_seek_point_index
        #// BUF recommended_buffer_size
        #// CNT play_counter
        #// COM comment
        #// COMM    comment
        #// COMR    commercial_frame
        #// CRA audio_encryption
        #// CRM encrypted_meta_frame
        #// ENCR    encryption_method_registration
        #// EQU equalisation
        #// EQU2    equalisation
        #// EQUA    equalisation
        #// ETC event_timing_codes
        #// ETCO    event_timing_codes
        #// GEO general_encapsulated_object
        #// GEOB    general_encapsulated_object
        #// GRID    group_identification_registration
        #// IPL involved_people_list
        #// IPLS    involved_people_list
        #// LINK    linked_information
        #// LNK linked_information
        #// MCDI    music_cd_identifier
        #// MCI music_cd_identifier
        #// MLL mpeg_location_lookup_table
        #// MLLT    mpeg_location_lookup_table
        #// OWNE    ownership_frame
        #// PCNT    play_counter
        #// PIC attached_picture
        #// POP popularimeter
        #// POPM    popularimeter
        #// POSS    position_synchronisation_frame
        #// PRIV    private_frame
        #// RBUF    recommended_buffer_size
        #// REV reverb
        #// RVA relative_volume_adjustment
        #// RVA2    relative_volume_adjustment
        #// RVAD    relative_volume_adjustment
        #// RVRB    reverb
        #// SEEK    seek_frame
        #// SIGN    signature_frame
        #// SLT synchronised_lyric
        #// STC synced_tempo_codes
        #// SYLT    synchronised_lyric
        #// SYTC    synchronised_tempo_codes
        #// TAL album
        #// TALB    album
        #// TBP bpm
        #// TBPM    bpm
        #// TCM composer
        #// TCMP    part_of_a_compilation
        #// TCO genre
        #// TCOM    composer
        #// TCON    genre
        #// TCOP    copyright_message
        #// TCP part_of_a_compilation
        #// TCR copyright_message
        #// TDA date
        #// TDAT    date
        #// TDEN    encoding_time
        #// TDLY    playlist_delay
        #// TDOR    original_release_time
        #// TDRC    recording_time
        #// TDRL    release_time
        #// TDTG    tagging_time
        #// TDY playlist_delay
        #// TEN encoded_by
        #// TENC    encoded_by
        #// TEXT    lyricist
        #// TFLT    file_type
        #// TFT file_type
        #// TIM time
        #// TIME    time
        #// TIPL    involved_people_list
        #// TIT1    content_group_description
        #// TIT2    title
        #// TIT3    subtitle
        #// TKE initial_key
        #// TKEY    initial_key
        #// TLA language
        #// TLAN    language
        #// TLE length
        #// TLEN    length
        #// TMCL    musician_credits_list
        #// TMED    media_type
        #// TMOO    mood
        #// TMT media_type
        #// TOA original_artist
        #// TOAL    original_album
        #// TOF original_filename
        #// TOFN    original_filename
        #// TOL original_lyricist
        #// TOLY    original_lyricist
        #// TOPE    original_artist
        #// TOR original_year
        #// TORY    original_year
        #// TOT original_album
        #// TOWN    file_owner
        #// TP1 artist
        #// TP2 band
        #// TP3 conductor
        #// TP4 remixer
        #// TPA part_of_a_set
        #// TPB publisher
        #// TPE1    artist
        #// TPE2    band
        #// TPE3    conductor
        #// TPE4    remixer
        #// TPOS    part_of_a_set
        #// TPRO    produced_notice
        #// TPUB    publisher
        #// TRC isrc
        #// TRCK    track_number
        #// TRD recording_dates
        #// TRDA    recording_dates
        #// TRK track_number
        #// TRSN    internet_radio_station_name
        #// TRSO    internet_radio_station_owner
        #// TS2 album_artist_sort_order
        #// TSA album_sort_order
        #// TSC composer_sort_order
        #// TSI size
        #// TSIZ    size
        #// TSO2    album_artist_sort_order
        #// TSOA    album_sort_order
        #// TSOC    composer_sort_order
        #// TSOP    performer_sort_order
        #// TSOT    title_sort_order
        #// TSP performer_sort_order
        #// TSRC    isrc
        #// TSS encoder_settings
        #// TSSE    encoder_settings
        #// TSST    set_subtitle
        #// TST title_sort_order
        #// TT1 content_group_description
        #// TT2 title
        #// TT3 subtitle
        #// TXT lyricist
        #// TXX text
        #// TXXX    text
        #// TYE year
        #// TYER    year
        #// UFI unique_file_identifier
        #// UFID    unique_file_identifier
        #// ULT unsynchronised_lyric
        #// USER    terms_of_use
        #// USLT    unsynchronised_lyric
        #// WAF url_file
        #// WAR url_artist
        #// WAS url_source
        #// WCM commercial_information
        #// WCOM    commercial_information
        #// WCOP    copyright
        #// WCP copyright
        #// WOAF    url_file
        #// WOAR    url_artist
        #// WOAS    url_source
        #// WORS    url_station
        #// WPAY    url_payment
        #// WPB url_publisher
        #// WPUB    url_publisher
        #// WXX url_user
        #// WXXX    url_user
        #// TFEA    featured_artist
        #// TSTU    recording_studio
        #// rgad    replay_gain_adjustment
        #//
        return getid3_lib.embeddedlookup(framename_, begin_, 0, __FILE__, "id3v2-framename_short")
    # end def framenameshortlookup
    #// 
    #// @param string $encoding
    #// 
    #// @return string
    #//
    @classmethod
    def textencodingterminatorlookup(self, encoding_=None):
        
        
        TextEncodingTerminatorLookup_ = Array({0: " ", 1: "  ", 2: "  ", 3: " ", 255: "  "})
        return TextEncodingTerminatorLookup_[encoding_] if (php_isset(lambda : TextEncodingTerminatorLookup_[encoding_])) else " "
    # end def textencodingterminatorlookup
    #// 
    #// @param int $encoding
    #// 
    #// @return string
    #//
    @classmethod
    def textencodingnamelookup(self, encoding_=None):
        
        
        TextEncodingNameLookup_ = Array({0: "ISO-8859-1", 1: "UTF-16", 2: "UTF-16BE", 3: "UTF-8", 255: "UTF-16BE"})
        return TextEncodingNameLookup_[encoding_] if (php_isset(lambda : TextEncodingNameLookup_[encoding_])) else "ISO-8859-1"
    # end def textencodingnamelookup
    #// 
    #// @param string $string
    #// @param string $terminator
    #// 
    #// @return string
    #//
    @classmethod
    def removestringterminator(self, string_=None, terminator_=None):
        
        
        #// Null terminator at end of comment string is somewhat ambiguous in the specification, may or may not be implemented by various taggers. Remove terminator only if present.
        #// https://github.com/JamesHeinrich/getID3/issues/121
        #// https://community.mp3tag.de/t/x-trailing-nulls-in-id3v2-comments/19227
        if php_substr(string_, -php_strlen(terminator_), php_strlen(terminator_)) == terminator_:
            string_ = php_substr(string_, 0, -php_strlen(terminator_))
        # end if
        return string_
    # end def removestringterminator
    #// 
    #// @param string $string
    #// 
    #// @return string
    #//
    @classmethod
    def makeutf16emptystringempty(self, string_=None):
        
        
        if php_in_array(string_, Array(" ", "  ", "ÿþ", "þÿ")):
            #// if string only contains a BOM or terminator then make it actually an empty string
            string_ = ""
        # end if
        return string_
    # end def makeutf16emptystringempty
    #// 
    #// @param string $framename
    #// @param int    $id3v2majorversion
    #// 
    #// @return bool|int
    #//
    @classmethod
    def isvalidid3v2framename(self, framename_=None, id3v2majorversion_=None):
        
        
        for case in Switch(id3v2majorversion_):
            if case(2):
                return php_preg_match("#[A-Z][A-Z0-9]{2}#", framename_)
                break
            # end if
            if case(3):
                pass
            # end if
            if case(4):
                return php_preg_match("#[A-Z][A-Z0-9]{3}#", framename_)
                break
            # end if
        # end for
        return False
    # end def isvalidid3v2framename
    #// 
    #// @param string $numberstring
    #// @param bool   $allowdecimal
    #// @param bool   $allownegative
    #// 
    #// @return bool
    #//
    @classmethod
    def isanumber(self, numberstring_=None, allowdecimal_=None, allownegative_=None):
        if allowdecimal_ is None:
            allowdecimal_ = False
        # end if
        if allownegative_ is None:
            allownegative_ = False
        # end if
        
        i_ = 0
        while i_ < php_strlen(numberstring_):
            
            if chr(numberstring_[i_]) < chr("0") or chr(numberstring_[i_]) > chr("9"):
                if numberstring_[i_] == "." and allowdecimal_:
                    pass
                elif numberstring_[i_] == "-" and allownegative_ and i_ == 0:
                    pass
                else:
                    return False
                # end if
            # end if
            i_ += 1
        # end while
        return True
    # end def isanumber
    #// 
    #// @param string $datestamp
    #// 
    #// @return bool
    #//
    @classmethod
    def isvaliddatestampstring(self, datestamp_=None):
        
        
        if php_strlen(datestamp_) != 8:
            return False
        # end if
        if (not self.isanumber(datestamp_, False)):
            return False
        # end if
        year_ = php_substr(datestamp_, 0, 4)
        month_ = php_substr(datestamp_, 4, 2)
        day_ = php_substr(datestamp_, 6, 2)
        if year_ == 0 or month_ == 0 or day_ == 0:
            return False
        # end if
        if month_ > 12:
            return False
        # end if
        if day_ > 31:
            return False
        # end if
        if day_ > 30 and month_ == 4 or month_ == 6 or month_ == 9 or month_ == 11:
            return False
        # end if
        if day_ > 29 and month_ == 2:
            return False
        # end if
        return True
    # end def isvaliddatestampstring
    #// 
    #// @param int $majorversion
    #// 
    #// @return int
    #//
    @classmethod
    def id3v2headerlength(self, majorversion_=None):
        
        
        return 6 if majorversion_ == 2 else 10
    # end def id3v2headerlength
    #// 
    #// @param string $frame_name
    #// 
    #// @return string|false
    #//
    @classmethod
    def id3v22itunesbrokenframename(self, frame_name_=None):
        
        
        ID3v22_iTunes_BrokenFrames_ = Array({"BUF": "RBUF", "CNT": "PCNT", "COM": "COMM", "CRA": "AENC", "EQU": "EQUA", "ETC": "ETCO", "GEO": "GEOB", "IPL": "IPLS", "LNK": "LINK", "MCI": "MCDI", "MLL": "MLLT", "PIC": "APIC", "POP": "POPM", "REV": "RVRB", "RVA": "RVAD", "SLT": "SYLT", "STC": "SYTC", "TAL": "TALB", "TBP": "TBPM", "TCM": "TCOM", "TCO": "TCON", "TCP": "TCMP", "TCR": "TCOP", "TDA": "TDAT", "TDY": "TDLY", "TEN": "TENC", "TFT": "TFLT", "TIM": "TIME", "TKE": "TKEY", "TLA": "TLAN", "TLE": "TLEN", "TMT": "TMED", "TOA": "TOPE", "TOF": "TOFN", "TOL": "TOLY", "TOR": "TORY", "TOT": "TOAL", "TP1": "TPE1", "TP2": "TPE2", "TP3": "TPE3", "TP4": "TPE4", "TPA": "TPOS", "TPB": "TPUB", "TRC": "TSRC", "TRD": "TRDA", "TRK": "TRCK", "TS2": "TSO2", "TSA": "TSOA", "TSC": "TSOC", "TSI": "TSIZ", "TSP": "TSOP", "TSS": "TSSE", "TST": "TSOT", "TT1": "TIT1", "TT2": "TIT2", "TT3": "TIT3", "TXT": "TEXT", "TXX": "TXXX", "TYE": "TYER", "UFI": "UFID", "ULT": "USLT", "WAF": "WOAF", "WAR": "WOAR", "WAS": "WOAS", "WCM": "WCOM", "WCP": "WCOP", "WPB": "WPUB", "WXX": "WXXX"})
        if php_strlen(frame_name_) == 4:
            if php_substr(frame_name_, 3, 1) == " " or php_substr(frame_name_, 3, 1) == " ":
                if (php_isset(lambda : ID3v22_iTunes_BrokenFrames_[php_substr(frame_name_, 0, 3)])):
                    return ID3v22_iTunes_BrokenFrames_[php_substr(frame_name_, 0, 3)]
                # end if
            # end if
        # end if
        return False
    # end def id3v22itunesbrokenframename
# end class getid3_id3v2
