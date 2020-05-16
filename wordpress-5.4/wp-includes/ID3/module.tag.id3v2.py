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
        
        info = self.getid3.info
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
        info["id3v2"]["header"] = True
        thisfile_id3v2 = info["id3v2"]
        thisfile_id3v2["flags"] = Array()
        thisfile_id3v2_flags = thisfile_id3v2["flags"]
        self.fseek(self.StartingOffset)
        header = self.fread(10)
        if php_substr(header, 0, 3) == "ID3" and php_strlen(header) == 10:
            thisfile_id3v2["majorversion"] = php_ord(header[3])
            thisfile_id3v2["minorversion"] = php_ord(header[4])
            #// shortcut
            id3v2_majorversion = thisfile_id3v2["majorversion"]
        else:
            info["id3v2"] = None
            return False
        # end if
        if id3v2_majorversion > 4:
            #// this script probably won't correctly parse ID3v2.5.x and above (if it ever exists)
            self.error("this script only parses up to ID3v2.4.x - this tag is ID3v2." + id3v2_majorversion + "." + thisfile_id3v2["minorversion"])
            return False
        # end if
        id3_flags = php_ord(header[5])
        for case in Switch(id3v2_majorversion):
            if case(2):
                #// %ab000000 in v2.2
                thisfile_id3v2_flags["unsynch"] = php_bool(id3_flags & 128)
                #// a - Unsynchronisation
                thisfile_id3v2_flags["compression"] = php_bool(id3_flags & 64)
                break
            # end if
            if case(3):
                #// %abc00000 in v2.3
                thisfile_id3v2_flags["unsynch"] = php_bool(id3_flags & 128)
                #// a - Unsynchronisation
                thisfile_id3v2_flags["exthead"] = php_bool(id3_flags & 64)
                #// b - Extended header
                thisfile_id3v2_flags["experim"] = php_bool(id3_flags & 32)
                break
            # end if
            if case(4):
                #// %abcd0000 in v2.4
                thisfile_id3v2_flags["unsynch"] = php_bool(id3_flags & 128)
                #// a - Unsynchronisation
                thisfile_id3v2_flags["exthead"] = php_bool(id3_flags & 64)
                #// b - Extended header
                thisfile_id3v2_flags["experim"] = php_bool(id3_flags & 32)
                #// c - Experimental indicator
                thisfile_id3v2_flags["isfooter"] = php_bool(id3_flags & 16)
                break
            # end if
        # end for
        thisfile_id3v2["headerlength"] = getid3_lib.bigendian2int(php_substr(header, 6, 4), 1) + 10
        #// length of ID3v2 tag in 10-byte header doesn't include 10-byte header length
        thisfile_id3v2["tag_offset_start"] = self.StartingOffset
        thisfile_id3v2["tag_offset_end"] = thisfile_id3v2["tag_offset_start"] + thisfile_id3v2["headerlength"]
        #// create 'encoding' key - used by getid3::HandleAllTags()
        #// in ID3v2 every field can have it's own encoding type
        #// so force everything to UTF-8 so it can be handled consistantly
        thisfile_id3v2["encoding"] = "UTF-8"
        #// Frames
        #// All ID3v2 frames consists of one frame header followed by one or more
        #// fields containing the actual information. The header is always 10
        #// bytes and laid out as follows:
        #// 
        #// Frame ID      $xx xx xx xx  (four characters)
        #// Size      4 * %0xxxxxxx
        #// Flags         $xx xx
        sizeofframes = thisfile_id3v2["headerlength"] - 10
        #// not including 10-byte initial header
        if (not php_empty(lambda : thisfile_id3v2["exthead"]["length"])):
            sizeofframes -= thisfile_id3v2["exthead"]["length"] + 4
        # end if
        if (not php_empty(lambda : thisfile_id3v2_flags["isfooter"])):
            sizeofframes -= 10
            pass
        # end if
        if sizeofframes > 0:
            framedata = self.fread(sizeofframes)
            #// read all frames from file into $framedata variable
            #// if entire frame data is unsynched, de-unsynch it now (ID3v2.3.x)
            if (not php_empty(lambda : thisfile_id3v2_flags["unsynch"])) and id3v2_majorversion <= 3:
                framedata = self.deunsynchronise(framedata)
            # end if
            #// [in ID3v2.4.0] Unsynchronisation [S:6.1] is done on frame level, instead
            #// of on tag level, making it easier to skip frames, increasing the streamability
            #// of the tag. The unsynchronisation flag in the header [S:3.1] indicates that
            #// there exists an unsynchronised frame, while the new unsynchronisation flag in
            #// the frame header [S:4.1.2] indicates unsynchronisation.
            #// $framedataoffset = 10 + ($thisfile_id3v2['exthead']['length'] ? $thisfile_id3v2['exthead']['length'] + 4 : 0); // how many bytes into the stream - start from after the 10-byte header (and extended header length+4, if present)
            framedataoffset = 10
            #// how many bytes into the stream - start from after the 10-byte header
            #// Extended Header
            if (not php_empty(lambda : thisfile_id3v2_flags["exthead"])):
                extended_header_offset = 0
                if id3v2_majorversion == 3:
                    #// v2.3 definition:
                    #// Extended header size  $xx xx xx xx   // 32-bit integer
                    #// Extended Flags        $xx xx
                    #// %x0000000 %00000000 // v2.3
                    #// x - CRC data present
                    #// Size of padding       $xx xx xx xx
                    thisfile_id3v2["exthead"]["length"] = getid3_lib.bigendian2int(php_substr(framedata, extended_header_offset, 4), 0)
                    extended_header_offset += 4
                    thisfile_id3v2["exthead"]["flag_bytes"] = 2
                    thisfile_id3v2["exthead"]["flag_raw"] = getid3_lib.bigendian2int(php_substr(framedata, extended_header_offset, thisfile_id3v2["exthead"]["flag_bytes"]))
                    extended_header_offset += thisfile_id3v2["exthead"]["flag_bytes"]
                    thisfile_id3v2["exthead"]["flags"]["crc"] = php_bool(thisfile_id3v2["exthead"]["flag_raw"] & 32768)
                    thisfile_id3v2["exthead"]["padding_size"] = getid3_lib.bigendian2int(php_substr(framedata, extended_header_offset, 4))
                    extended_header_offset += 4
                    if thisfile_id3v2["exthead"]["flags"]["crc"]:
                        thisfile_id3v2["exthead"]["flag_data"]["crc"] = getid3_lib.bigendian2int(php_substr(framedata, extended_header_offset, 4))
                        extended_header_offset += 4
                    # end if
                    extended_header_offset += thisfile_id3v2["exthead"]["padding_size"]
                elif id3v2_majorversion == 4:
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
                    thisfile_id3v2["exthead"]["length"] = getid3_lib.bigendian2int(php_substr(framedata, extended_header_offset, 4), True)
                    extended_header_offset += 4
                    thisfile_id3v2["exthead"]["flag_bytes"] = getid3_lib.bigendian2int(php_substr(framedata, extended_header_offset, 1))
                    #// should always be 1
                    extended_header_offset += 1
                    thisfile_id3v2["exthead"]["flag_raw"] = getid3_lib.bigendian2int(php_substr(framedata, extended_header_offset, thisfile_id3v2["exthead"]["flag_bytes"]))
                    extended_header_offset += thisfile_id3v2["exthead"]["flag_bytes"]
                    thisfile_id3v2["exthead"]["flags"]["update"] = php_bool(thisfile_id3v2["exthead"]["flag_raw"] & 64)
                    thisfile_id3v2["exthead"]["flags"]["crc"] = php_bool(thisfile_id3v2["exthead"]["flag_raw"] & 32)
                    thisfile_id3v2["exthead"]["flags"]["restrictions"] = php_bool(thisfile_id3v2["exthead"]["flag_raw"] & 16)
                    if thisfile_id3v2["exthead"]["flags"]["update"]:
                        ext_header_chunk_length = getid3_lib.bigendian2int(php_substr(framedata, extended_header_offset, 1))
                        #// should be 0
                        extended_header_offset += 1
                    # end if
                    if thisfile_id3v2["exthead"]["flags"]["crc"]:
                        ext_header_chunk_length = getid3_lib.bigendian2int(php_substr(framedata, extended_header_offset, 1))
                        #// should be 5
                        extended_header_offset += 1
                        thisfile_id3v2["exthead"]["flag_data"]["crc"] = getid3_lib.bigendian2int(php_substr(framedata, extended_header_offset, ext_header_chunk_length), True, False)
                        extended_header_offset += ext_header_chunk_length
                    # end if
                    if thisfile_id3v2["exthead"]["flags"]["restrictions"]:
                        ext_header_chunk_length = getid3_lib.bigendian2int(php_substr(framedata, extended_header_offset, 1))
                        #// should be 1
                        extended_header_offset += 1
                        #// %ppqrrstt
                        restrictions_raw = getid3_lib.bigendian2int(php_substr(framedata, extended_header_offset, 1))
                        extended_header_offset += 1
                        thisfile_id3v2["exthead"]["flags"]["restrictions"]["tagsize"] = restrictions_raw & 192 >> 6
                        #// p - Tag size restrictions
                        thisfile_id3v2["exthead"]["flags"]["restrictions"]["textenc"] = restrictions_raw & 32 >> 5
                        #// q - Text encoding restrictions
                        thisfile_id3v2["exthead"]["flags"]["restrictions"]["textsize"] = restrictions_raw & 24 >> 3
                        #// r - Text fields size restrictions
                        thisfile_id3v2["exthead"]["flags"]["restrictions"]["imgenc"] = restrictions_raw & 4 >> 2
                        #// s - Image encoding restrictions
                        thisfile_id3v2["exthead"]["flags"]["restrictions"]["imgsize"] = restrictions_raw & 3 >> 0
                        #// t - Image size restrictions
                        thisfile_id3v2["exthead"]["flags"]["restrictions_text"]["tagsize"] = self.lookupextendedheaderrestrictionstagsizelimits(thisfile_id3v2["exthead"]["flags"]["restrictions"]["tagsize"])
                        thisfile_id3v2["exthead"]["flags"]["restrictions_text"]["textenc"] = self.lookupextendedheaderrestrictionstextencodings(thisfile_id3v2["exthead"]["flags"]["restrictions"]["textenc"])
                        thisfile_id3v2["exthead"]["flags"]["restrictions_text"]["textsize"] = self.lookupextendedheaderrestrictionstextfieldsize(thisfile_id3v2["exthead"]["flags"]["restrictions"]["textsize"])
                        thisfile_id3v2["exthead"]["flags"]["restrictions_text"]["imgenc"] = self.lookupextendedheaderrestrictionsimageencoding(thisfile_id3v2["exthead"]["flags"]["restrictions"]["imgenc"])
                        thisfile_id3v2["exthead"]["flags"]["restrictions_text"]["imgsize"] = self.lookupextendedheaderrestrictionsimagesizesize(thisfile_id3v2["exthead"]["flags"]["restrictions"]["imgsize"])
                    # end if
                    if thisfile_id3v2["exthead"]["length"] != extended_header_offset:
                        self.warning("ID3v2.4 extended header length mismatch (expecting " + php_intval(thisfile_id3v2["exthead"]["length"]) + ", found " + php_intval(extended_header_offset) + ")")
                    # end if
                # end if
                framedataoffset += extended_header_offset
                framedata = php_substr(framedata, extended_header_offset)
            # end if
            #// end extended header
            while True:
                
                if not ((php_isset(lambda : framedata)) and php_strlen(framedata) > 0):
                    break
                # end if
                #// cycle through until no more frame data is left to parse
                if php_strlen(framedata) <= self.id3v2headerlength(id3v2_majorversion):
                    #// insufficient room left in ID3v2 header for actual data - must be padding
                    thisfile_id3v2["padding"]["start"] = framedataoffset
                    thisfile_id3v2["padding"]["length"] = php_strlen(framedata)
                    thisfile_id3v2["padding"]["valid"] = True
                    i = 0
                    while i < thisfile_id3v2["padding"]["length"]:
                        
                        if framedata[i] != " ":
                            thisfile_id3v2["padding"]["valid"] = False
                            thisfile_id3v2["padding"]["errorpos"] = thisfile_id3v2["padding"]["start"] + i
                            self.warning("Invalid ID3v2 padding found at offset " + thisfile_id3v2["padding"]["errorpos"] + " (the remaining " + thisfile_id3v2["padding"]["length"] - i + " bytes are considered invalid)")
                            break
                        # end if
                        i += 1
                    # end while
                    break
                    pass
                # end if
                frame_header = None
                frame_name = None
                frame_size = None
                frame_flags = None
                if id3v2_majorversion == 2:
                    #// Frame ID  $xx xx xx (three characters)
                    #// Size      $xx xx xx (24-bit integer)
                    #// Flags     $xx xx
                    frame_header = php_substr(framedata, 0, 6)
                    #// take next 6 bytes for header
                    framedata = php_substr(framedata, 6)
                    #// and leave the rest in $framedata
                    frame_name = php_substr(frame_header, 0, 3)
                    frame_size = getid3_lib.bigendian2int(php_substr(frame_header, 3, 3), 0)
                    frame_flags = 0
                    pass
                elif id3v2_majorversion > 2:
                    #// Frame ID  $xx xx xx xx (four characters)
                    #// Size      $xx xx xx xx (32-bit integer in v2.3, 28-bit synchsafe in v2.4+)
                    #// Flags     $xx xx
                    frame_header = php_substr(framedata, 0, 10)
                    #// take next 10 bytes for header
                    framedata = php_substr(framedata, 10)
                    #// and leave the rest in $framedata
                    frame_name = php_substr(frame_header, 0, 4)
                    if id3v2_majorversion == 3:
                        frame_size = getid3_lib.bigendian2int(php_substr(frame_header, 4, 4), 0)
                        pass
                    else:
                        #// ID3v2.4+
                        frame_size = getid3_lib.bigendian2int(php_substr(frame_header, 4, 4), 1)
                        pass
                    # end if
                    if frame_size < php_strlen(framedata) + 4:
                        nextFrameID = php_substr(framedata, frame_size, 4)
                        if self.isvalidid3v2framename(nextFrameID, id3v2_majorversion):
                            pass
                        elif frame_name == " " + "MP3" or frame_name == "  " + "MP" or frame_name == " MP3" or frame_name == "MP3e":
                            pass
                        elif id3v2_majorversion == 4 and self.isvalidid3v2framename(php_substr(framedata, getid3_lib.bigendian2int(php_substr(frame_header, 4, 4), 0), 4), 3):
                            self.warning("ID3v2 tag written as ID3v2.4, but with non-synchsafe integers (ID3v2.3 style). Older versions of (Helium2; iTunes) are known culprits of this. Tag has been parsed as ID3v2.3")
                            id3v2_majorversion = 3
                            frame_size = getid3_lib.bigendian2int(php_substr(frame_header, 4, 4), 0)
                            pass
                        # end if
                    # end if
                    frame_flags = getid3_lib.bigendian2int(php_substr(frame_header, 8, 2))
                # end if
                if id3v2_majorversion == 2 and frame_name == "   " or frame_name == "    ":
                    #// padding encountered
                    thisfile_id3v2["padding"]["start"] = framedataoffset
                    thisfile_id3v2["padding"]["length"] = php_strlen(frame_header) + php_strlen(framedata)
                    thisfile_id3v2["padding"]["valid"] = True
                    len = php_strlen(framedata)
                    i = 0
                    while i < len:
                        
                        if framedata[i] != " ":
                            thisfile_id3v2["padding"]["valid"] = False
                            thisfile_id3v2["padding"]["errorpos"] = thisfile_id3v2["padding"]["start"] + i
                            self.warning("Invalid ID3v2 padding found at offset " + thisfile_id3v2["padding"]["errorpos"] + " (the remaining " + thisfile_id3v2["padding"]["length"] - i + " bytes are considered invalid)")
                            break
                        # end if
                        i += 1
                    # end while
                    break
                    pass
                # end if
                iTunesBrokenFrameNameFixed = self.id3v22itunesbrokenframename(frame_name)
                if iTunesBrokenFrameNameFixed:
                    self.warning("error parsing \"" + frame_name + "\" (" + framedataoffset + " bytes into the ID3v2." + id3v2_majorversion + " tag). (ERROR: IsValidID3v2FrameName(\"" + php_str_replace(" ", " ", frame_name) + "\", " + id3v2_majorversion + "))). [Note: this particular error has been known to happen with tags edited by iTunes (versions \"X v2.0.3\", \"v3.0.1\", \"v7.0.0.70\" are known-guilty, probably others too)]. Translated frame name from \"" + php_str_replace(" ", " ", frame_name) + "\" to \"" + iTunesBrokenFrameNameFixed + "\" for parsing.")
                    frame_name = iTunesBrokenFrameNameFixed
                # end if
                if frame_size <= php_strlen(framedata) and self.isvalidid3v2framename(frame_name, id3v2_majorversion):
                    parsedFrame = None
                    parsedFrame["frame_name"] = frame_name
                    parsedFrame["frame_flags_raw"] = frame_flags
                    parsedFrame["data"] = php_substr(framedata, 0, frame_size)
                    parsedFrame["datalength"] = getid3_lib.castasint(frame_size)
                    parsedFrame["dataoffset"] = framedataoffset
                    self.parseid3v2frame(parsedFrame)
                    thisfile_id3v2[frame_name][-1] = parsedFrame
                    framedata = php_substr(framedata, frame_size)
                else:
                    #// invalid frame length or FrameID
                    if frame_size <= php_strlen(framedata):
                        if self.isvalidid3v2framename(php_substr(framedata, frame_size, 4), id3v2_majorversion):
                            #// next frame is valid, just skip the current frame
                            framedata = php_substr(framedata, frame_size)
                            self.warning("Next ID3v2 frame is valid, skipping current frame.")
                        else:
                            #// next frame is invalid too, abort processing
                            #// unset($framedata);
                            framedata = None
                            self.error("Next ID3v2 frame is also invalid, aborting processing.")
                        # end if
                    elif frame_size == php_strlen(framedata):
                        #// this is the last frame, just skip
                        self.warning("This was the last ID3v2 frame.")
                    else:
                        #// next frame is invalid too, abort processing
                        #// unset($framedata);
                        framedata = None
                        self.warning("Invalid ID3v2 frame size, aborting.")
                    # end if
                    if (not self.isvalidid3v2framename(frame_name, id3v2_majorversion)):
                        for case in Switch(frame_name):
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
                                self.warning("error parsing \"" + frame_name + "\" (" + framedataoffset + " bytes into the ID3v2." + id3v2_majorversion + " tag). (ERROR: !IsValidID3v2FrameName(\"" + php_str_replace(" ", " ", frame_name) + "\", " + id3v2_majorversion + "))). [Note: this particular error has been known to happen with tags edited by \"MP3ext (www.mutschler.de/mp3ext/)\"]")
                                break
                            # end if
                            if case():
                                self.warning("error parsing \"" + frame_name + "\" (" + framedataoffset + " bytes into the ID3v2." + id3v2_majorversion + " tag). (ERROR: !IsValidID3v2FrameName(\"" + php_str_replace(" ", " ", frame_name) + "\", " + id3v2_majorversion + "))).")
                                break
                            # end if
                        # end for
                    elif (not (php_isset(lambda : framedata))) or frame_size > php_strlen(framedata):
                        self.error("error parsing \"" + frame_name + "\" (" + framedataoffset + " bytes into the ID3v2." + id3v2_majorversion + " tag). (ERROR: $frame_size (" + frame_size + ") > strlen($framedata) (" + php_strlen(framedata) if (php_isset(lambda : framedata)) else "null" + ")).")
                    else:
                        self.error("error parsing \"" + frame_name + "\" (" + framedataoffset + " bytes into the ID3v2." + id3v2_majorversion + " tag).")
                    # end if
                # end if
                framedataoffset += frame_size + self.id3v2headerlength(id3v2_majorversion)
            # end while
        # end if
        #// Footer
        #// The footer is a copy of the header, but with a different identifier.
        #// ID3v2 identifier           "3DI"
        #// ID3v2 version              $04 00
        #// ID3v2 flags                %abcd0000
        #// ID3v2 size             4 * %0xxxxxxx
        if (php_isset(lambda : thisfile_id3v2_flags["isfooter"])) and thisfile_id3v2_flags["isfooter"]:
            footer = self.fread(10)
            if php_substr(footer, 0, 3) == "3DI":
                thisfile_id3v2["footer"] = True
                thisfile_id3v2["majorversion_footer"] = php_ord(footer[3])
                thisfile_id3v2["minorversion_footer"] = php_ord(footer[4])
            # end if
            if thisfile_id3v2["majorversion_footer"] <= 4:
                id3_flags = php_ord(footer[5])
                thisfile_id3v2_flags["unsynch_footer"] = php_bool(id3_flags & 128)
                thisfile_id3v2_flags["extfoot_footer"] = php_bool(id3_flags & 64)
                thisfile_id3v2_flags["experim_footer"] = php_bool(id3_flags & 32)
                thisfile_id3v2_flags["isfooter_footer"] = php_bool(id3_flags & 16)
                thisfile_id3v2["footerlength"] = getid3_lib.bigendian2int(php_substr(footer, 6, 4), 1)
            # end if
        # end if
        #// end footer
        if (php_isset(lambda : thisfile_id3v2["comments"]["genre"])):
            genres = Array()
            for key,value in thisfile_id3v2["comments"]["genre"]:
                for genre in self.parseid3v2genrestring(value):
                    genres[-1] = genre
                # end for
            # end for
            thisfile_id3v2["comments"]["genre"] = array_unique(genres)
            key = None
            value = None
            genres = None
            genre = None
        # end if
        if (php_isset(lambda : thisfile_id3v2["comments"]["track_number"])):
            for key,value in thisfile_id3v2["comments"]["track_number"]:
                if php_strstr(value, "/"):
                    thisfile_id3v2["comments"]["track_number"][key], thisfile_id3v2["comments"]["totaltracks"][key] = php_explode("/", thisfile_id3v2["comments"]["track_number"][key])
                # end if
            # end for
        # end if
        if (not (php_isset(lambda : thisfile_id3v2["comments"]["year"]))) and (not php_empty(lambda : thisfile_id3v2["comments"]["recording_time"][0])) and php_preg_match("#^([0-9]{4})#", php_trim(thisfile_id3v2["comments"]["recording_time"][0]), matches):
            thisfile_id3v2["comments"]["year"] = Array(matches[1])
        # end if
        if (not php_empty(lambda : thisfile_id3v2["TXXX"])):
            #// MediaMonkey does this, maybe others: write a blank RGAD frame, but put replay-gain adjustment values in TXXX frames
            for txxx_array in thisfile_id3v2["TXXX"]:
                for case in Switch(txxx_array["description"]):
                    if case("replaygain_track_gain"):
                        if php_empty(lambda : info["replay_gain"]["track"]["adjustment"]) and (not php_empty(lambda : txxx_array["data"])):
                            info["replay_gain"]["track"]["adjustment"] = floatval(php_trim(php_str_replace("dB", "", txxx_array["data"])))
                        # end if
                        break
                    # end if
                    if case("replaygain_track_peak"):
                        if php_empty(lambda : info["replay_gain"]["track"]["peak"]) and (not php_empty(lambda : txxx_array["data"])):
                            info["replay_gain"]["track"]["peak"] = floatval(txxx_array["data"])
                        # end if
                        break
                    # end if
                    if case("replaygain_album_gain"):
                        if php_empty(lambda : info["replay_gain"]["album"]["adjustment"]) and (not php_empty(lambda : txxx_array["data"])):
                            info["replay_gain"]["album"]["adjustment"] = floatval(php_trim(php_str_replace("dB", "", txxx_array["data"])))
                        # end if
                        break
                    # end if
                # end for
            # end for
        # end if
        #// Set avdataoffset
        info["avdataoffset"] = thisfile_id3v2["headerlength"]
        if (php_isset(lambda : thisfile_id3v2["footer"])):
            info["avdataoffset"] += 10
        # end if
        return True
    # end def analyze
    #// 
    #// @param string $genrestring
    #// 
    #// @return array
    #//
    def parseid3v2genrestring(self, genrestring=None):
        
        #// Parse genres into arrays of genreName and genreID
        #// ID3v2.2.x, ID3v2.3.x: '(21)' or '(4)Eurodisco' or '(51)(39)' or '(55)((I think...)'
        #// ID3v2.4.x: '21' $00 'Eurodisco' $00
        clean_genres = Array()
        #// hack-fixes for some badly-written ID3v2.3 taggers, while trying not to break correctly-written tags
        if self.getid3.info["id3v2"]["majorversion"] == 3 and (not php_preg_match("#[\\x00]#", genrestring)):
            #// note: MusicBrainz Picard incorrectly stores plaintext genres separated by "/" when writing in ID3v2.3 mode, hack-fix here:
            #// replace / with NULL, then replace back the two ID3v1 genres that legitimately have "/" as part of the single genre name
            if php_preg_match("#/#", genrestring):
                genrestring = php_str_replace("/", " ", genrestring)
                genrestring = php_str_replace("Pop" + " " + "Funk", "Pop/Funk", genrestring)
                genrestring = php_str_replace("Rock" + " " + "Rock", "Folk/Rock", genrestring)
            # end if
            #// some other taggers separate multiple genres with semicolon, e.g. "Heavy Metal;Thrash Metal;Metal"
            if php_preg_match("#;#", genrestring):
                genrestring = php_str_replace(";", " ", genrestring)
            # end if
        # end if
        if php_strpos(genrestring, " ") == False:
            genrestring = php_preg_replace("#\\(([0-9]{1,3})\\)#", "$1" + " ", genrestring)
        # end if
        genre_elements = php_explode(" ", genrestring)
        for element in genre_elements:
            element = php_trim(element)
            if element:
                if php_preg_match("#^[0-9]{1,3}$#", element):
                    clean_genres[-1] = getid3_id3v1.lookupgenrename(element)
                else:
                    clean_genres[-1] = php_str_replace("((", "(", element)
                # end if
            # end if
        # end for
        return clean_genres
    # end def parseid3v2genrestring
    #// 
    #// @param array $parsedFrame
    #// 
    #// @return bool
    #//
    def parseid3v2frame(self, parsedFrame=None):
        
        #// shortcuts
        info = self.getid3.info
        id3v2_majorversion = info["id3v2"]["majorversion"]
        parsedFrame["framenamelong"] = self.framenamelonglookup(parsedFrame["frame_name"])
        if php_empty(lambda : parsedFrame["framenamelong"]):
            parsedFrame["framenamelong"] = None
        # end if
        parsedFrame["framenameshort"] = self.framenameshortlookup(parsedFrame["frame_name"])
        if php_empty(lambda : parsedFrame["framenameshort"]):
            parsedFrame["framenameshort"] = None
        # end if
        if id3v2_majorversion >= 3:
            #// frame flags are not part of the ID3v2.2 standard
            if id3v2_majorversion == 3:
                #// Frame Header Flags
                #// %abc00000 %ijk00000
                parsedFrame["flags"]["TagAlterPreservation"] = php_bool(parsedFrame["frame_flags_raw"] & 32768)
                #// a - Tag alter preservation
                parsedFrame["flags"]["FileAlterPreservation"] = php_bool(parsedFrame["frame_flags_raw"] & 16384)
                #// b - File alter preservation
                parsedFrame["flags"]["ReadOnly"] = php_bool(parsedFrame["frame_flags_raw"] & 8192)
                #// c - Read only
                parsedFrame["flags"]["compression"] = php_bool(parsedFrame["frame_flags_raw"] & 128)
                #// i - Compression
                parsedFrame["flags"]["Encryption"] = php_bool(parsedFrame["frame_flags_raw"] & 64)
                #// j - Encryption
                parsedFrame["flags"]["GroupingIdentity"] = php_bool(parsedFrame["frame_flags_raw"] & 32)
                pass
            elif id3v2_majorversion == 4:
                #// Frame Header Flags
                #// %0abc0000 %0h00kmnp
                parsedFrame["flags"]["TagAlterPreservation"] = php_bool(parsedFrame["frame_flags_raw"] & 16384)
                #// a - Tag alter preservation
                parsedFrame["flags"]["FileAlterPreservation"] = php_bool(parsedFrame["frame_flags_raw"] & 8192)
                #// b - File alter preservation
                parsedFrame["flags"]["ReadOnly"] = php_bool(parsedFrame["frame_flags_raw"] & 4096)
                #// c - Read only
                parsedFrame["flags"]["GroupingIdentity"] = php_bool(parsedFrame["frame_flags_raw"] & 64)
                #// h - Grouping identity
                parsedFrame["flags"]["compression"] = php_bool(parsedFrame["frame_flags_raw"] & 8)
                #// k - Compression
                parsedFrame["flags"]["Encryption"] = php_bool(parsedFrame["frame_flags_raw"] & 4)
                #// m - Encryption
                parsedFrame["flags"]["Unsynchronisation"] = php_bool(parsedFrame["frame_flags_raw"] & 2)
                #// n - Unsynchronisation
                parsedFrame["flags"]["DataLengthIndicator"] = php_bool(parsedFrame["frame_flags_raw"] & 1)
                #// p - Data length indicator
                #// Frame-level de-unsynchronisation - ID3v2.4
                if parsedFrame["flags"]["Unsynchronisation"]:
                    parsedFrame["data"] = self.deunsynchronise(parsedFrame["data"])
                # end if
                if parsedFrame["flags"]["DataLengthIndicator"]:
                    parsedFrame["data_length_indicator"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], 0, 4), 1)
                    parsedFrame["data"] = php_substr(parsedFrame["data"], 4)
                # end if
            # end if
            #// Frame-level de-compression
            if parsedFrame["flags"]["compression"]:
                parsedFrame["decompressed_size"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], 0, 4))
                if (not php_function_exists("gzuncompress")):
                    self.warning("gzuncompress() support required to decompress ID3v2 frame \"" + parsedFrame["frame_name"] + "\"")
                else:
                    decompresseddata = php_no_error(lambda: gzuncompress(php_substr(parsedFrame["data"], 4)))
                    if decompresseddata:
                        #// if ($decompresseddata = @gzuncompress($parsedFrame['data'])) {
                        parsedFrame["data"] = decompresseddata
                        decompresseddata = None
                    else:
                        self.warning("gzuncompress() failed on compressed contents of ID3v2 frame \"" + parsedFrame["frame_name"] + "\"")
                    # end if
                # end if
            # end if
        # end if
        if (not php_empty(lambda : parsedFrame["flags"]["DataLengthIndicator"])):
            if parsedFrame["data_length_indicator"] != php_strlen(parsedFrame["data"]):
                self.warning("ID3v2 frame \"" + parsedFrame["frame_name"] + "\" should be " + parsedFrame["data_length_indicator"] + " bytes long according to DataLengthIndicator, but found " + php_strlen(parsedFrame["data"]) + " bytes of data")
            # end if
        # end if
        if (php_isset(lambda : parsedFrame["datalength"])) and parsedFrame["datalength"] == 0:
            warning = "Frame \"" + parsedFrame["frame_name"] + "\" at offset " + parsedFrame["dataoffset"] + " has no data portion"
            for case in Switch(parsedFrame["frame_name"]):
                if case("WCOM"):
                    warning += " (this is known to happen with files tagged by RioPort)"
                    break
                # end if
                if case():
                    break
                # end if
            # end for
            self.warning(warning)
        elif id3v2_majorversion >= 3 and parsedFrame["frame_name"] == "UFID" or id3v2_majorversion == 2 and parsedFrame["frame_name"] == "UFI":
            #// 4.1   UFI  Unique file identifier
            #// There may be more than one 'UFID' frame in a tag,
            #// but only one with the same 'Owner identifier'.
            #// <Header for 'Unique file identifier', ID: 'UFID'>
            #// Owner identifier        <text string> $00
            #// Identifier              <up to 64 bytes binary data>
            exploded = php_explode(" ", parsedFrame["data"], 2)
            parsedFrame["ownerid"] = exploded[0] if (php_isset(lambda : exploded[0])) else ""
            parsedFrame["data"] = exploded[1] if (php_isset(lambda : exploded[1])) else ""
        elif id3v2_majorversion >= 3 and parsedFrame["frame_name"] == "TXXX" or id3v2_majorversion == 2 and parsedFrame["frame_name"] == "TXX":
            #// 4.2.2 TXX  User defined text information frame
            #// There may be more than one 'TXXX' frame in each tag,
            #// but only one with the same description.
            #// <Header for 'User defined text information frame', ID: 'TXXX'>
            #// Text encoding     $xx
            #// Description       <text string according to encoding> $00 (00)
            #// Value             <text string according to encoding>
            frame_offset = 0
            frame_textencoding = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            frame_textencoding_terminator = self.textencodingterminatorlookup(frame_textencoding)
            if id3v2_majorversion <= 3 and frame_textencoding > 1 or id3v2_majorversion == 4 and frame_textencoding > 3:
                self.warning("Invalid text encoding byte (" + frame_textencoding + ") in frame \"" + parsedFrame["frame_name"] + "\" - defaulting to ISO-8859-1 encoding")
                frame_textencoding_terminator = " "
            # end if
            frame_terminatorpos = php_strpos(parsedFrame["data"], frame_textencoding_terminator, frame_offset)
            if php_ord(php_substr(parsedFrame["data"], frame_terminatorpos + php_strlen(frame_textencoding_terminator), 1)) == 0:
                frame_terminatorpos += 1
                pass
            # end if
            parsedFrame["description"] = php_substr(parsedFrame["data"], frame_offset, frame_terminatorpos - frame_offset)
            parsedFrame["description"] = self.makeutf16emptystringempty(parsedFrame["description"])
            parsedFrame["encodingid"] = frame_textencoding
            parsedFrame["encoding"] = self.textencodingnamelookup(frame_textencoding)
            parsedFrame["description"] = php_trim(getid3_lib.iconv_fallback(parsedFrame["encoding"], info["id3v2"]["encoding"], parsedFrame["description"]))
            parsedFrame["data"] = php_substr(parsedFrame["data"], frame_terminatorpos + php_strlen(frame_textencoding_terminator))
            parsedFrame["data"] = self.removestringterminator(parsedFrame["data"], frame_textencoding_terminator)
            if (not php_empty(lambda : parsedFrame["framenameshort"])) and (not php_empty(lambda : parsedFrame["data"])):
                commentkey = parsedFrame["description"] if parsedFrame["description"] else php_count(info["id3v2"]["comments"][parsedFrame["framenameshort"]]) if (php_isset(lambda : info["id3v2"]["comments"][parsedFrame["framenameshort"]])) else 0
                if (not (php_isset(lambda : info["id3v2"]["comments"][parsedFrame["framenameshort"]]))) or (not php_array_key_exists(commentkey, info["id3v2"]["comments"][parsedFrame["framenameshort"]])):
                    info["id3v2"]["comments"][parsedFrame["framenameshort"]][commentkey] = php_trim(getid3_lib.iconv_fallback(parsedFrame["encoding"], info["id3v2"]["encoding"], parsedFrame["data"]))
                else:
                    info["id3v2"]["comments"][parsedFrame["framenameshort"]][-1] = php_trim(getid3_lib.iconv_fallback(parsedFrame["encoding"], info["id3v2"]["encoding"], parsedFrame["data"]))
                # end if
            # end if
            pass
        elif parsedFrame["frame_name"][0] == "T":
            #// 4.2. T??[?] Text information frame
            #// There may only be one text information frame of its kind in an tag.
            #// <Header for 'Text information frame', ID: 'T000' - 'TZZZ',
            #// excluding 'TXXX' described in 4.2.6.>
            #// Text encoding                $xx
            #// Information                  <text string(s) according to encoding>
            frame_offset = 0
            frame_textencoding = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            if id3v2_majorversion <= 3 and frame_textencoding > 1 or id3v2_majorversion == 4 and frame_textencoding > 3:
                self.warning("Invalid text encoding byte (" + frame_textencoding + ") in frame \"" + parsedFrame["frame_name"] + "\" - defaulting to ISO-8859-1 encoding")
            # end if
            parsedFrame["data"] = php_str(php_substr(parsedFrame["data"], frame_offset))
            parsedFrame["data"] = self.removestringterminator(parsedFrame["data"], self.textencodingterminatorlookup(frame_textencoding))
            parsedFrame["encodingid"] = frame_textencoding
            parsedFrame["encoding"] = self.textencodingnamelookup(frame_textencoding)
            if (not php_empty(lambda : parsedFrame["framenameshort"])) and (not php_empty(lambda : parsedFrame["data"])):
                #// ID3v2.3 specs say that TPE1 (and others) can contain multiple artist values separated with
                #// This of course breaks when an artist name contains slash character, e.g. "AC/DC"
                #// MP3tag (maybe others) implement alternative system where multiple artists are null-separated, which makes more sense
                #// getID3 will split null-separated artists into multiple artists and leave slash-separated ones to the user
                for case in Switch(parsedFrame["encoding"]):
                    if case("UTF-16"):
                        pass
                    # end if
                    if case("UTF-16BE"):
                        pass
                    # end if
                    if case("UTF-16LE"):
                        wordsize = 2
                        break
                    # end if
                    if case("ISO-8859-1"):
                        pass
                    # end if
                    if case("UTF-8"):
                        pass
                    # end if
                    if case():
                        wordsize = 1
                        break
                    # end if
                # end for
                Txxx_elements = Array()
                Txxx_elements_start_offset = 0
                i = 0
                while i < php_strlen(parsedFrame["data"]):
                    
                    if php_substr(parsedFrame["data"], i, wordsize) == php_str_repeat(" ", wordsize):
                        Txxx_elements[-1] = php_substr(parsedFrame["data"], Txxx_elements_start_offset, i - Txxx_elements_start_offset)
                        Txxx_elements_start_offset = i + wordsize
                    # end if
                    i += wordsize
                # end while
                Txxx_elements[-1] = php_substr(parsedFrame["data"], Txxx_elements_start_offset, i - Txxx_elements_start_offset)
                for Txxx_element in Txxx_elements:
                    string = getid3_lib.iconv_fallback(parsedFrame["encoding"], info["id3v2"]["encoding"], Txxx_element)
                    if (not php_empty(lambda : string)):
                        info["id3v2"]["comments"][parsedFrame["framenameshort"]][-1] = string
                    # end if
                # end for
                string = None
                wordsize = None
                i = None
                Txxx_elements = None
                Txxx_element = None
                Txxx_elements_start_offset = None
            # end if
        elif id3v2_majorversion >= 3 and parsedFrame["frame_name"] == "WXXX" or id3v2_majorversion == 2 and parsedFrame["frame_name"] == "WXX":
            #// 4.3.2 WXX  User defined URL link frame
            #// There may be more than one 'WXXX' frame in each tag,
            #// but only one with the same description
            #// <Header for 'User defined URL link frame', ID: 'WXXX'>
            #// Text encoding     $xx
            #// Description       <text string according to encoding> $00 (00)
            #// URL               <text string>
            frame_offset = 0
            frame_textencoding = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            frame_textencoding_terminator = self.textencodingterminatorlookup(frame_textencoding)
            if id3v2_majorversion <= 3 and frame_textencoding > 1 or id3v2_majorversion == 4 and frame_textencoding > 3:
                self.warning("Invalid text encoding byte (" + frame_textencoding + ") in frame \"" + parsedFrame["frame_name"] + "\" - defaulting to ISO-8859-1 encoding")
                frame_textencoding_terminator = " "
            # end if
            frame_terminatorpos = php_strpos(parsedFrame["data"], frame_textencoding_terminator, frame_offset)
            if php_ord(php_substr(parsedFrame["data"], frame_terminatorpos + php_strlen(frame_textencoding_terminator), 1)) == 0:
                frame_terminatorpos += 1
                pass
            # end if
            parsedFrame["encodingid"] = frame_textencoding
            parsedFrame["encoding"] = self.textencodingnamelookup(frame_textencoding)
            parsedFrame["description"] = php_substr(parsedFrame["data"], frame_offset, frame_terminatorpos - frame_offset)
            #// according to the frame text encoding
            parsedFrame["url"] = php_substr(parsedFrame["data"], frame_terminatorpos + php_strlen(frame_textencoding_terminator))
            #// always ISO-8859-1
            parsedFrame["description"] = self.removestringterminator(parsedFrame["description"], frame_textencoding_terminator)
            parsedFrame["description"] = self.makeutf16emptystringempty(parsedFrame["description"])
            if (not php_empty(lambda : parsedFrame["framenameshort"])) and parsedFrame["url"]:
                info["id3v2"]["comments"][parsedFrame["framenameshort"]][-1] = getid3_lib.iconv_fallback("ISO-8859-1", info["id3v2"]["encoding"], parsedFrame["url"])
            # end if
            parsedFrame["data"] = None
        elif parsedFrame["frame_name"][0] == "W":
            #// 4.3. W??? URL link frames
            #// There may only be one URL link frame of its kind in a tag,
            #// except when stated otherwise in the frame description
            #// <Header for 'URL link frame', ID: 'W000' - 'WZZZ', excluding 'WXXX'
            #// described in 4.3.2.>
            #// URL              <text string>
            parsedFrame["url"] = php_trim(parsedFrame["data"])
            #// always ISO-8859-1
            if (not php_empty(lambda : parsedFrame["framenameshort"])) and parsedFrame["url"]:
                info["id3v2"]["comments"][parsedFrame["framenameshort"]][-1] = getid3_lib.iconv_fallback("ISO-8859-1", info["id3v2"]["encoding"], parsedFrame["url"])
            # end if
            parsedFrame["data"] = None
        elif id3v2_majorversion == 3 and parsedFrame["frame_name"] == "IPLS" or id3v2_majorversion == 2 and parsedFrame["frame_name"] == "IPL":
            #// 4.4  IPL  Involved people list (ID3v2.2 only)
            #// http://id3.org/id3v2.3.0#sec4.4
            #// There may only be one 'IPL' frame in each tag
            #// <Header for 'User defined URL link frame', ID: 'IPL'>
            #// Text encoding     $xx
            #// People list strings    <textstrings>
            frame_offset = 0
            frame_textencoding = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            if id3v2_majorversion <= 3 and frame_textencoding > 1 or id3v2_majorversion == 4 and frame_textencoding > 3:
                self.warning("Invalid text encoding byte (" + frame_textencoding + ") in frame \"" + parsedFrame["frame_name"] + "\" - defaulting to ISO-8859-1 encoding")
            # end if
            parsedFrame["encodingid"] = frame_textencoding
            parsedFrame["encoding"] = self.textencodingnamelookup(parsedFrame["encodingid"])
            parsedFrame["data_raw"] = php_str(php_substr(parsedFrame["data"], frame_offset))
            #// https://www.getid3.org/phpBB3/viewtopic.php?t=1369
            #// "this tag typically contains null terminated strings, which are associated in pairs"
            #// "there are users that use the tag incorrectly"
            IPLS_parts = Array()
            if php_strpos(parsedFrame["data_raw"], " ") != False:
                IPLS_parts_unsorted = Array()
                if php_strlen(parsedFrame["data_raw"]) % 2 == 0 and php_substr(parsedFrame["data_raw"], 0, 2) == "ÿþ" or php_substr(parsedFrame["data_raw"], 0, 2) == "þÿ":
                    #// UTF-16, be careful looking for null bytes since most 2-byte characters may contain one; you need to find twin null bytes, and on even padding
                    thisILPS = ""
                    i = 0
                    while i < php_strlen(parsedFrame["data_raw"]):
                        
                        twobytes = php_substr(parsedFrame["data_raw"], i, 2)
                        if twobytes == "  ":
                            IPLS_parts_unsorted[-1] = getid3_lib.iconv_fallback(parsedFrame["encoding"], info["id3v2"]["encoding"], thisILPS)
                            thisILPS = ""
                        else:
                            thisILPS += twobytes
                        # end if
                        i += 2
                    # end while
                    if php_strlen(thisILPS) > 2:
                        #// 2-byte BOM
                        IPLS_parts_unsorted[-1] = getid3_lib.iconv_fallback(parsedFrame["encoding"], info["id3v2"]["encoding"], thisILPS)
                    # end if
                else:
                    #// ISO-8859-1 or UTF-8 or other single-byte-null character set
                    IPLS_parts_unsorted = php_explode(" ", parsedFrame["data_raw"])
                # end if
                if php_count(IPLS_parts_unsorted) == 1:
                    #// just a list of names, e.g. "Dino Baptiste, Jimmy Copley, John Gordon, Bernie Marsden, Sharon Watson"
                    for key,value in IPLS_parts_unsorted:
                        IPLS_parts_sorted = php_preg_split("#[;,\\r\\n\\t]#", value)
                        position = ""
                        for person in IPLS_parts_sorted:
                            IPLS_parts[-1] = Array({"position": position, "person": person})
                        # end for
                    # end for
                elif php_count(IPLS_parts_unsorted) % 2 == 0:
                    position = ""
                    person = ""
                    for key,value in IPLS_parts_unsorted:
                        if key % 2 == 0:
                            position = value
                        else:
                            person = value
                            IPLS_parts[-1] = Array({"position": position, "person": person})
                            position = ""
                            person = ""
                        # end if
                    # end for
                else:
                    for key,value in IPLS_parts_unsorted:
                        IPLS_parts[-1] = Array(value)
                    # end for
                # end if
            else:
                IPLS_parts = php_preg_split("#[;,\\r\\n\\t]#", parsedFrame["data_raw"])
            # end if
            parsedFrame["data"] = IPLS_parts
            if (not php_empty(lambda : parsedFrame["framenameshort"])) and (not php_empty(lambda : parsedFrame["data"])):
                info["id3v2"]["comments"][parsedFrame["framenameshort"]][-1] = parsedFrame["data"]
            # end if
        elif id3v2_majorversion >= 3 and parsedFrame["frame_name"] == "MCDI" or id3v2_majorversion == 2 and parsedFrame["frame_name"] == "MCI":
            #// 4.5   MCI  Music CD identifier
            #// There may only be one 'MCDI' frame in each tag
            #// <Header for 'Music CD identifier', ID: 'MCDI'>
            #// CD TOC                <binary data>
            if (not php_empty(lambda : parsedFrame["framenameshort"])) and (not php_empty(lambda : parsedFrame["data"])):
                info["id3v2"]["comments"][parsedFrame["framenameshort"]][-1] = parsedFrame["data"]
            # end if
        elif id3v2_majorversion >= 3 and parsedFrame["frame_name"] == "ETCO" or id3v2_majorversion == 2 and parsedFrame["frame_name"] == "ETC":
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
            frame_offset = 0
            parsedFrame["timestampformat"] = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            while True:
                
                if not (frame_offset < php_strlen(parsedFrame["data"])):
                    break
                # end if
                parsedFrame["typeid"] = php_substr(parsedFrame["data"], frame_offset, 1)
                frame_offset += 1
                parsedFrame["type"] = self.etcoeventlookup(parsedFrame["typeid"])
                parsedFrame["timestamp"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], frame_offset, 4))
                frame_offset += 4
            # end while
            parsedFrame["data"] = None
        elif id3v2_majorversion >= 3 and parsedFrame["frame_name"] == "MLLT" or id3v2_majorversion == 2 and parsedFrame["frame_name"] == "MLL":
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
            frame_offset = 0
            parsedFrame["framesbetweenreferences"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], 0, 2))
            parsedFrame["bytesbetweenreferences"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], 2, 3))
            parsedFrame["msbetweenreferences"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], 5, 3))
            parsedFrame["bitsforbytesdeviation"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], 8, 1))
            parsedFrame["bitsformsdeviation"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], 9, 1))
            parsedFrame["data"] = php_substr(parsedFrame["data"], 10)
            deviationbitstream = ""
            while True:
                
                if not (frame_offset < php_strlen(parsedFrame["data"])):
                    break
                # end if
                deviationbitstream += getid3_lib.bigendian2bin(php_substr(parsedFrame["data"], frame_offset, 1))
                frame_offset += 1
            # end while
            reference_counter = 0
            while True:
                
                if not (php_strlen(deviationbitstream) > 0):
                    break
                # end if
                parsedFrame[reference_counter]["bytedeviation"] = bindec(php_substr(deviationbitstream, 0, parsedFrame["bitsforbytesdeviation"]))
                parsedFrame[reference_counter]["msdeviation"] = bindec(php_substr(deviationbitstream, parsedFrame["bitsforbytesdeviation"], parsedFrame["bitsformsdeviation"]))
                deviationbitstream = php_substr(deviationbitstream, parsedFrame["bitsforbytesdeviation"] + parsedFrame["bitsformsdeviation"])
                reference_counter += 1
            # end while
            parsedFrame["data"] = None
        elif id3v2_majorversion >= 3 and parsedFrame["frame_name"] == "SYTC" or id3v2_majorversion == 2 and parsedFrame["frame_name"] == "STC":
            #// 4.8   STC  Synchronised tempo codes
            #// There may only be one 'SYTC' frame in each tag
            #// <Header for 'Synchronised tempo codes', ID: 'SYTC'>
            #// Time stamp format   $xx
            #// Tempo data          <binary data>
            #// Where time stamp format is:
            #// $01  (32-bit value) MPEG frames from beginning of file
            #// $02  (32-bit value) milliseconds from beginning of file
            frame_offset = 0
            parsedFrame["timestampformat"] = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            timestamp_counter = 0
            while True:
                
                if not (frame_offset < php_strlen(parsedFrame["data"])):
                    break
                # end if
                parsedFrame[timestamp_counter]["tempo"] = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
                frame_offset += 1
                if parsedFrame[timestamp_counter]["tempo"] == 255:
                    parsedFrame[timestamp_counter]["tempo"] += php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
                    frame_offset += 1
                # end if
                parsedFrame[timestamp_counter]["timestamp"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], frame_offset, 4))
                frame_offset += 4
                timestamp_counter += 1
            # end while
            parsedFrame["data"] = None
        elif id3v2_majorversion >= 3 and parsedFrame["frame_name"] == "USLT" or id3v2_majorversion == 2 and parsedFrame["frame_name"] == "ULT":
            #// 4.9   ULT  Unsynchronised lyric/text transcription
            #// There may be more than one 'Unsynchronised lyrics/text transcription' frame
            #// in each tag, but only one with the same language and content descriptor.
            #// <Header for 'Unsynchronised lyrics/text transcription', ID: 'USLT'>
            #// Text encoding        $xx
            #// Language             $xx xx xx
            #// Content descriptor   <text string according to encoding> $00 (00)
            #// Lyrics/text          <full text string according to encoding>
            frame_offset = 0
            frame_textencoding = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            frame_textencoding_terminator = self.textencodingterminatorlookup(frame_textencoding)
            if id3v2_majorversion <= 3 and frame_textencoding > 1 or id3v2_majorversion == 4 and frame_textencoding > 3:
                self.warning("Invalid text encoding byte (" + frame_textencoding + ") in frame \"" + parsedFrame["frame_name"] + "\" - defaulting to ISO-8859-1 encoding")
                frame_textencoding_terminator = " "
            # end if
            frame_language = php_substr(parsedFrame["data"], frame_offset, 3)
            frame_offset += 3
            frame_terminatorpos = php_strpos(parsedFrame["data"], frame_textencoding_terminator, frame_offset)
            if php_ord(php_substr(parsedFrame["data"], frame_terminatorpos + php_strlen(frame_textencoding_terminator), 1)) == 0:
                frame_terminatorpos += 1
                pass
            # end if
            parsedFrame["description"] = php_substr(parsedFrame["data"], frame_offset, frame_terminatorpos - frame_offset)
            parsedFrame["description"] = self.makeutf16emptystringempty(parsedFrame["description"])
            parsedFrame["data"] = php_substr(parsedFrame["data"], frame_terminatorpos + php_strlen(frame_textencoding_terminator))
            parsedFrame["data"] = self.removestringterminator(parsedFrame["data"], frame_textencoding_terminator)
            parsedFrame["encodingid"] = frame_textencoding
            parsedFrame["encoding"] = self.textencodingnamelookup(frame_textencoding)
            parsedFrame["language"] = frame_language
            parsedFrame["languagename"] = self.languagelookup(frame_language, False)
            if (not php_empty(lambda : parsedFrame["framenameshort"])) and (not php_empty(lambda : parsedFrame["data"])):
                info["id3v2"]["comments"][parsedFrame["framenameshort"]][-1] = getid3_lib.iconv_fallback(parsedFrame["encoding"], info["id3v2"]["encoding"], parsedFrame["data"])
            # end if
            parsedFrame["data"] = None
        elif id3v2_majorversion >= 3 and parsedFrame["frame_name"] == "SYLT" or id3v2_majorversion == 2 and parsedFrame["frame_name"] == "SLT":
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
            frame_offset = 0
            frame_textencoding = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            frame_textencoding_terminator = self.textencodingterminatorlookup(frame_textencoding)
            if id3v2_majorversion <= 3 and frame_textencoding > 1 or id3v2_majorversion == 4 and frame_textencoding > 3:
                self.warning("Invalid text encoding byte (" + frame_textencoding + ") in frame \"" + parsedFrame["frame_name"] + "\" - defaulting to ISO-8859-1 encoding")
                frame_textencoding_terminator = " "
            # end if
            frame_language = php_substr(parsedFrame["data"], frame_offset, 3)
            frame_offset += 3
            parsedFrame["timestampformat"] = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            parsedFrame["contenttypeid"] = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            parsedFrame["contenttype"] = self.sytlcontenttypelookup(parsedFrame["contenttypeid"])
            parsedFrame["encodingid"] = frame_textencoding
            parsedFrame["encoding"] = self.textencodingnamelookup(frame_textencoding)
            parsedFrame["language"] = frame_language
            parsedFrame["languagename"] = self.languagelookup(frame_language, False)
            timestampindex = 0
            frame_remainingdata = php_substr(parsedFrame["data"], frame_offset)
            while True:
                
                if not (php_strlen(frame_remainingdata)):
                    break
                # end if
                frame_offset = 0
                frame_terminatorpos = php_strpos(frame_remainingdata, frame_textencoding_terminator)
                if frame_terminatorpos == False:
                    frame_remainingdata = ""
                else:
                    if php_ord(php_substr(frame_remainingdata, frame_terminatorpos + php_strlen(frame_textencoding_terminator), 1)) == 0:
                        frame_terminatorpos += 1
                        pass
                    # end if
                    parsedFrame["lyrics"][timestampindex]["data"] = php_substr(frame_remainingdata, frame_offset, frame_terminatorpos - frame_offset)
                    frame_remainingdata = php_substr(frame_remainingdata, frame_terminatorpos + php_strlen(frame_textencoding_terminator))
                    if timestampindex == 0 and php_ord(frame_remainingdata[0]) != 0:
                        pass
                    else:
                        parsedFrame["lyrics"][timestampindex]["timestamp"] = getid3_lib.bigendian2int(php_substr(frame_remainingdata, 0, 4))
                        frame_remainingdata = php_substr(frame_remainingdata, 4)
                    # end if
                    timestampindex += 1
                # end if
            # end while
            parsedFrame["data"] = None
        elif id3v2_majorversion >= 3 and parsedFrame["frame_name"] == "COMM" or id3v2_majorversion == 2 and parsedFrame["frame_name"] == "COM":
            #// 4.11  COM  Comments
            #// There may be more than one comment frame in each tag,
            #// but only one with the same language and content descriptor.
            #// <Header for 'Comment', ID: 'COMM'>
            #// Text encoding          $xx
            #// Language               $xx xx xx
            #// Short content descrip. <text string according to encoding> $00 (00)
            #// The actual text        <full text string according to encoding>
            if php_strlen(parsedFrame["data"]) < 5:
                self.warning("Invalid data (too short) for \"" + parsedFrame["frame_name"] + "\" frame at offset " + parsedFrame["dataoffset"])
            else:
                frame_offset = 0
                frame_textencoding = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
                frame_offset += 1
                frame_textencoding_terminator = self.textencodingterminatorlookup(frame_textencoding)
                if id3v2_majorversion <= 3 and frame_textencoding > 1 or id3v2_majorversion == 4 and frame_textencoding > 3:
                    self.warning("Invalid text encoding byte (" + frame_textencoding + ") in frame \"" + parsedFrame["frame_name"] + "\" - defaulting to ISO-8859-1 encoding")
                    frame_textencoding_terminator = " "
                # end if
                frame_language = php_substr(parsedFrame["data"], frame_offset, 3)
                frame_offset += 3
                frame_terminatorpos = php_strpos(parsedFrame["data"], frame_textencoding_terminator, frame_offset)
                if php_ord(php_substr(parsedFrame["data"], frame_terminatorpos + php_strlen(frame_textencoding_terminator), 1)) == 0:
                    frame_terminatorpos += 1
                    pass
                # end if
                parsedFrame["description"] = php_substr(parsedFrame["data"], frame_offset, frame_terminatorpos - frame_offset)
                parsedFrame["description"] = self.makeutf16emptystringempty(parsedFrame["description"])
                frame_text = php_str(php_substr(parsedFrame["data"], frame_terminatorpos + php_strlen(frame_textencoding_terminator)))
                frame_text = self.removestringterminator(frame_text, frame_textencoding_terminator)
                parsedFrame["encodingid"] = frame_textencoding
                parsedFrame["encoding"] = self.textencodingnamelookup(frame_textencoding)
                parsedFrame["language"] = frame_language
                parsedFrame["languagename"] = self.languagelookup(frame_language, False)
                parsedFrame["data"] = frame_text
                if (not php_empty(lambda : parsedFrame["framenameshort"])) and (not php_empty(lambda : parsedFrame["data"])):
                    commentkey = parsedFrame["description"] if parsedFrame["description"] else php_count(info["id3v2"]["comments"][parsedFrame["framenameshort"]]) if (not php_empty(lambda : info["id3v2"]["comments"][parsedFrame["framenameshort"]])) else 0
                    if (not (php_isset(lambda : info["id3v2"]["comments"][parsedFrame["framenameshort"]]))) or (not php_array_key_exists(commentkey, info["id3v2"]["comments"][parsedFrame["framenameshort"]])):
                        info["id3v2"]["comments"][parsedFrame["framenameshort"]][commentkey] = getid3_lib.iconv_fallback(parsedFrame["encoding"], info["id3v2"]["encoding"], parsedFrame["data"])
                    else:
                        info["id3v2"]["comments"][parsedFrame["framenameshort"]][-1] = getid3_lib.iconv_fallback(parsedFrame["encoding"], info["id3v2"]["encoding"], parsedFrame["data"])
                    # end if
                # end if
            # end if
        elif id3v2_majorversion >= 4 and parsedFrame["frame_name"] == "RVA2":
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
            frame_terminatorpos = php_strpos(parsedFrame["data"], " ")
            frame_idstring = php_substr(parsedFrame["data"], 0, frame_terminatorpos)
            if php_ord(frame_idstring) == 0:
                frame_idstring = ""
            # end if
            frame_remainingdata = php_substr(parsedFrame["data"], frame_terminatorpos + php_strlen(" "))
            parsedFrame["description"] = frame_idstring
            RVA2channelcounter = 0
            while True:
                
                if not (php_strlen(frame_remainingdata) >= 5):
                    break
                # end if
                frame_offset = 0
                frame_channeltypeid = php_ord(php_substr(frame_remainingdata, frame_offset, 1))
                frame_offset += 1
                parsedFrame[RVA2channelcounter]["channeltypeid"] = frame_channeltypeid
                parsedFrame[RVA2channelcounter]["channeltype"] = self.rva2channeltypelookup(frame_channeltypeid)
                parsedFrame[RVA2channelcounter]["volumeadjust"] = getid3_lib.bigendian2int(php_substr(frame_remainingdata, frame_offset, 2), False, True)
                #// 16-bit signed
                frame_offset += 2
                parsedFrame[RVA2channelcounter]["bitspeakvolume"] = php_ord(php_substr(frame_remainingdata, frame_offset, 1))
                frame_offset += 1
                if parsedFrame[RVA2channelcounter]["bitspeakvolume"] < 1 or parsedFrame[RVA2channelcounter]["bitspeakvolume"] > 4:
                    self.warning("ID3v2::RVA2 frame[" + RVA2channelcounter + "] contains invalid " + parsedFrame[RVA2channelcounter]["bitspeakvolume"] + "-byte bits-representing-peak value")
                    break
                # end if
                frame_bytespeakvolume = ceil(parsedFrame[RVA2channelcounter]["bitspeakvolume"] / 8)
                parsedFrame[RVA2channelcounter]["peakvolume"] = getid3_lib.bigendian2int(php_substr(frame_remainingdata, frame_offset, frame_bytespeakvolume))
                frame_remainingdata = php_substr(frame_remainingdata, frame_offset + frame_bytespeakvolume)
                RVA2channelcounter += 1
            # end while
            parsedFrame["data"] = None
        elif id3v2_majorversion == 3 and parsedFrame["frame_name"] == "RVAD" or id3v2_majorversion == 2 and parsedFrame["frame_name"] == "RVA":
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
            frame_offset = 0
            frame_incrdecrflags = getid3_lib.bigendian2bin(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            parsedFrame["incdec"]["right"] = php_bool(php_substr(frame_incrdecrflags, 6, 1))
            parsedFrame["incdec"]["left"] = php_bool(php_substr(frame_incrdecrflags, 7, 1))
            parsedFrame["bitsvolume"] = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            frame_bytesvolume = ceil(parsedFrame["bitsvolume"] / 8)
            parsedFrame["volumechange"]["right"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], frame_offset, frame_bytesvolume))
            if parsedFrame["incdec"]["right"] == False:
                parsedFrame["volumechange"]["right"] *= -1
            # end if
            frame_offset += frame_bytesvolume
            parsedFrame["volumechange"]["left"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], frame_offset, frame_bytesvolume))
            if parsedFrame["incdec"]["left"] == False:
                parsedFrame["volumechange"]["left"] *= -1
            # end if
            frame_offset += frame_bytesvolume
            parsedFrame["peakvolume"]["right"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], frame_offset, frame_bytesvolume))
            frame_offset += frame_bytesvolume
            parsedFrame["peakvolume"]["left"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], frame_offset, frame_bytesvolume))
            frame_offset += frame_bytesvolume
            if id3v2_majorversion == 3:
                parsedFrame["data"] = php_substr(parsedFrame["data"], frame_offset)
                if php_strlen(parsedFrame["data"]) > 0:
                    parsedFrame["incdec"]["rightrear"] = php_bool(php_substr(frame_incrdecrflags, 4, 1))
                    parsedFrame["incdec"]["leftrear"] = php_bool(php_substr(frame_incrdecrflags, 5, 1))
                    parsedFrame["volumechange"]["rightrear"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], frame_offset, frame_bytesvolume))
                    if parsedFrame["incdec"]["rightrear"] == False:
                        parsedFrame["volumechange"]["rightrear"] *= -1
                    # end if
                    frame_offset += frame_bytesvolume
                    parsedFrame["volumechange"]["leftrear"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], frame_offset, frame_bytesvolume))
                    if parsedFrame["incdec"]["leftrear"] == False:
                        parsedFrame["volumechange"]["leftrear"] *= -1
                    # end if
                    frame_offset += frame_bytesvolume
                    parsedFrame["peakvolume"]["rightrear"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], frame_offset, frame_bytesvolume))
                    frame_offset += frame_bytesvolume
                    parsedFrame["peakvolume"]["leftrear"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], frame_offset, frame_bytesvolume))
                    frame_offset += frame_bytesvolume
                # end if
                parsedFrame["data"] = php_substr(parsedFrame["data"], frame_offset)
                if php_strlen(parsedFrame["data"]) > 0:
                    parsedFrame["incdec"]["center"] = php_bool(php_substr(frame_incrdecrflags, 3, 1))
                    parsedFrame["volumechange"]["center"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], frame_offset, frame_bytesvolume))
                    if parsedFrame["incdec"]["center"] == False:
                        parsedFrame["volumechange"]["center"] *= -1
                    # end if
                    frame_offset += frame_bytesvolume
                    parsedFrame["peakvolume"]["center"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], frame_offset, frame_bytesvolume))
                    frame_offset += frame_bytesvolume
                # end if
                parsedFrame["data"] = php_substr(parsedFrame["data"], frame_offset)
                if php_strlen(parsedFrame["data"]) > 0:
                    parsedFrame["incdec"]["bass"] = php_bool(php_substr(frame_incrdecrflags, 2, 1))
                    parsedFrame["volumechange"]["bass"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], frame_offset, frame_bytesvolume))
                    if parsedFrame["incdec"]["bass"] == False:
                        parsedFrame["volumechange"]["bass"] *= -1
                    # end if
                    frame_offset += frame_bytesvolume
                    parsedFrame["peakvolume"]["bass"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], frame_offset, frame_bytesvolume))
                    frame_offset += frame_bytesvolume
                # end if
            # end if
            parsedFrame["data"] = None
        elif id3v2_majorversion >= 4 and parsedFrame["frame_name"] == "EQU2":
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
            frame_offset = 0
            frame_interpolationmethod = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            frame_terminatorpos = php_strpos(parsedFrame["data"], " ", frame_offset)
            frame_idstring = php_substr(parsedFrame["data"], frame_offset, frame_terminatorpos - frame_offset)
            if php_ord(frame_idstring) == 0:
                frame_idstring = ""
            # end if
            parsedFrame["description"] = frame_idstring
            frame_remainingdata = php_substr(parsedFrame["data"], frame_terminatorpos + php_strlen(" "))
            while True:
                
                if not (php_strlen(frame_remainingdata)):
                    break
                # end if
                frame_frequency = getid3_lib.bigendian2int(php_substr(frame_remainingdata, 0, 2)) / 2
                parsedFrame["data"][frame_frequency] = getid3_lib.bigendian2int(php_substr(frame_remainingdata, 2, 2), False, True)
                frame_remainingdata = php_substr(frame_remainingdata, 4)
            # end while
            parsedFrame["interpolationmethod"] = frame_interpolationmethod
            parsedFrame["data"] = None
        elif id3v2_majorversion == 3 and parsedFrame["frame_name"] == "EQUA" or id3v2_majorversion == 2 and parsedFrame["frame_name"] == "EQU":
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
            frame_offset = 0
            parsedFrame["adjustmentbits"] = php_substr(parsedFrame["data"], frame_offset, 1)
            frame_offset += 1
            frame_adjustmentbytes = ceil(parsedFrame["adjustmentbits"] / 8)
            frame_remainingdata = php_str(php_substr(parsedFrame["data"], frame_offset))
            while True:
                
                if not (php_strlen(frame_remainingdata) > 0):
                    break
                # end if
                frame_frequencystr = getid3_lib.bigendian2bin(php_substr(frame_remainingdata, 0, 2))
                frame_incdec = php_bool(php_substr(frame_frequencystr, 0, 1))
                frame_frequency = bindec(php_substr(frame_frequencystr, 1, 15))
                parsedFrame[frame_frequency]["incdec"] = frame_incdec
                parsedFrame[frame_frequency]["adjustment"] = getid3_lib.bigendian2int(php_substr(frame_remainingdata, 2, frame_adjustmentbytes))
                if parsedFrame[frame_frequency]["incdec"] == False:
                    parsedFrame[frame_frequency]["adjustment"] *= -1
                # end if
                frame_remainingdata = php_substr(frame_remainingdata, 2 + frame_adjustmentbytes)
            # end while
            parsedFrame["data"] = None
        elif id3v2_majorversion >= 3 and parsedFrame["frame_name"] == "RVRB" or id3v2_majorversion == 2 and parsedFrame["frame_name"] == "REV":
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
            frame_offset = 0
            parsedFrame["left"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], frame_offset, 2))
            frame_offset += 2
            parsedFrame["right"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], frame_offset, 2))
            frame_offset += 2
            parsedFrame["bouncesL"] = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            parsedFrame["bouncesR"] = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            parsedFrame["feedbackLL"] = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            parsedFrame["feedbackLR"] = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            parsedFrame["feedbackRR"] = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            parsedFrame["feedbackRL"] = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            parsedFrame["premixLR"] = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            parsedFrame["premixRL"] = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            parsedFrame["data"] = None
        elif id3v2_majorversion >= 3 and parsedFrame["frame_name"] == "APIC" or id3v2_majorversion == 2 and parsedFrame["frame_name"] == "PIC":
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
            frame_offset = 0
            frame_textencoding = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            frame_textencoding_terminator = self.textencodingterminatorlookup(frame_textencoding)
            if id3v2_majorversion <= 3 and frame_textencoding > 1 or id3v2_majorversion == 4 and frame_textencoding > 3:
                self.warning("Invalid text encoding byte (" + frame_textencoding + ") in frame \"" + parsedFrame["frame_name"] + "\" - defaulting to ISO-8859-1 encoding")
                frame_textencoding_terminator = " "
            # end if
            if id3v2_majorversion == 2 and php_strlen(parsedFrame["data"]) > frame_offset:
                frame_imagetype = php_substr(parsedFrame["data"], frame_offset, 3)
                if php_strtolower(frame_imagetype) == "ima":
                    #// complete hack for mp3Rage (www.chaoticsoftware.com) that puts ID3v2.3-formatted
                    #// MIME type instead of 3-char ID3v2.2-format image type  (thanks xbhoffØpacbell*net)
                    frame_terminatorpos = php_strpos(parsedFrame["data"], " ", frame_offset)
                    frame_mimetype = php_substr(parsedFrame["data"], frame_offset, frame_terminatorpos - frame_offset)
                    if php_ord(frame_mimetype) == 0:
                        frame_mimetype = ""
                    # end if
                    frame_imagetype = php_strtoupper(php_str_replace("image/", "", php_strtolower(frame_mimetype)))
                    if frame_imagetype == "JPEG":
                        frame_imagetype = "JPG"
                    # end if
                    frame_offset = frame_terminatorpos + php_strlen(" ")
                else:
                    frame_offset += 3
                # end if
            # end if
            if id3v2_majorversion > 2 and php_strlen(parsedFrame["data"]) > frame_offset:
                frame_terminatorpos = php_strpos(parsedFrame["data"], " ", frame_offset)
                frame_mimetype = php_substr(parsedFrame["data"], frame_offset, frame_terminatorpos - frame_offset)
                if php_ord(frame_mimetype) == 0:
                    frame_mimetype = ""
                # end if
                frame_offset = frame_terminatorpos + php_strlen(" ")
            # end if
            frame_picturetype = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            if frame_offset >= parsedFrame["datalength"]:
                self.warning("data portion of APIC frame is missing at offset " + parsedFrame["dataoffset"] + 8 + frame_offset)
            else:
                frame_terminatorpos = php_strpos(parsedFrame["data"], frame_textencoding_terminator, frame_offset)
                if php_ord(php_substr(parsedFrame["data"], frame_terminatorpos + php_strlen(frame_textencoding_terminator), 1)) == 0:
                    frame_terminatorpos += 1
                    pass
                # end if
                parsedFrame["description"] = php_substr(parsedFrame["data"], frame_offset, frame_terminatorpos - frame_offset)
                parsedFrame["description"] = self.makeutf16emptystringempty(parsedFrame["description"])
                parsedFrame["encodingid"] = frame_textencoding
                parsedFrame["encoding"] = self.textencodingnamelookup(frame_textencoding)
                if id3v2_majorversion == 2:
                    parsedFrame["imagetype"] = frame_imagetype if (php_isset(lambda : frame_imagetype)) else None
                else:
                    parsedFrame["mime"] = frame_mimetype if (php_isset(lambda : frame_mimetype)) else None
                # end if
                parsedFrame["picturetypeid"] = frame_picturetype
                parsedFrame["picturetype"] = self.apicpicturetypelookup(frame_picturetype)
                parsedFrame["data"] = php_substr(parsedFrame["data"], frame_terminatorpos + php_strlen(frame_textencoding_terminator))
                parsedFrame["datalength"] = php_strlen(parsedFrame["data"])
                parsedFrame["image_mime"] = ""
                imageinfo = Array()
                imagechunkcheck = getid3_lib.getdataimagesize(parsedFrame["data"], imageinfo)
                if imagechunkcheck:
                    if imagechunkcheck[2] >= 1 and imagechunkcheck[2] <= 3:
                        parsedFrame["image_mime"] = image_type_to_mime_type(imagechunkcheck[2])
                        if imagechunkcheck[0]:
                            parsedFrame["image_width"] = imagechunkcheck[0]
                        # end if
                        if imagechunkcheck[1]:
                            parsedFrame["image_height"] = imagechunkcheck[1]
                        # end if
                    # end if
                # end if
                while True:
                    if self.getid3.option_save_attachments == False:
                        parsedFrame["data"] = None
                        break
                    # end if
                    dir = ""
                    if self.getid3.option_save_attachments == True:
                        pass
                    elif php_is_string(self.getid3.option_save_attachments):
                        dir = php_rtrim(php_str_replace(Array("/", "\\"), DIRECTORY_SEPARATOR, self.getid3.option_save_attachments), DIRECTORY_SEPARATOR)
                        if (not php_is_dir(dir)) or (not getID3.is_writable(dir)):
                            #// cannot write, skip
                            self.warning("attachment at " + frame_offset + " cannot be saved to \"" + dir + "\" (not writable)")
                            parsedFrame["data"] = None
                            break
                        # end if
                    # end if
                    #// if we get this far, must be OK
                    if php_is_string(self.getid3.option_save_attachments):
                        destination_filename = dir + DIRECTORY_SEPARATOR + php_md5(info["filenamepath"]) + "_" + frame_offset
                        if (not php_file_exists(destination_filename)) or getID3.is_writable(destination_filename):
                            file_put_contents(destination_filename, parsedFrame["data"])
                        else:
                            self.warning("attachment at " + frame_offset + " cannot be saved to \"" + destination_filename + "\" (not writable)")
                        # end if
                        parsedFrame["data_filename"] = destination_filename
                        parsedFrame["data"] = None
                    else:
                        if (not php_empty(lambda : parsedFrame["framenameshort"])) and (not php_empty(lambda : parsedFrame["data"])):
                            if (not (php_isset(lambda : info["id3v2"]["comments"]["picture"]))):
                                info["id3v2"]["comments"]["picture"] = Array()
                            # end if
                            comments_picture_data = Array()
                            for picture_key in Array("data", "image_mime", "image_width", "image_height", "imagetype", "picturetype", "description", "datalength"):
                                if (php_isset(lambda : parsedFrame[picture_key])):
                                    comments_picture_data[picture_key] = parsedFrame[picture_key]
                                # end if
                            # end for
                            info["id3v2"]["comments"]["picture"][-1] = comments_picture_data
                            comments_picture_data = None
                        # end if
                    # end if
                    
                    if False:
                        break
                    # end if
                # end while
            # end if
        elif id3v2_majorversion >= 3 and parsedFrame["frame_name"] == "GEOB" or id3v2_majorversion == 2 and parsedFrame["frame_name"] == "GEO":
            #// 4.16  GEO  General encapsulated object
            #// There may be more than one 'GEOB' frame in each tag,
            #// but only one with the same content descriptor
            #// <Header for 'General encapsulated object', ID: 'GEOB'>
            #// Text encoding          $xx
            #// MIME type              <text string> $00
            #// Filename               <text string according to encoding> $00 (00)
            #// Content description    <text string according to encoding> $00 (00)
            #// Encapsulated object    <binary data>
            frame_offset = 0
            frame_textencoding = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            frame_textencoding_terminator = self.textencodingterminatorlookup(frame_textencoding)
            if id3v2_majorversion <= 3 and frame_textencoding > 1 or id3v2_majorversion == 4 and frame_textencoding > 3:
                self.warning("Invalid text encoding byte (" + frame_textencoding + ") in frame \"" + parsedFrame["frame_name"] + "\" - defaulting to ISO-8859-1 encoding")
                frame_textencoding_terminator = " "
            # end if
            frame_terminatorpos = php_strpos(parsedFrame["data"], " ", frame_offset)
            frame_mimetype = php_substr(parsedFrame["data"], frame_offset, frame_terminatorpos - frame_offset)
            if php_ord(frame_mimetype) == 0:
                frame_mimetype = ""
            # end if
            frame_offset = frame_terminatorpos + php_strlen(" ")
            frame_terminatorpos = php_strpos(parsedFrame["data"], frame_textencoding_terminator, frame_offset)
            if php_ord(php_substr(parsedFrame["data"], frame_terminatorpos + php_strlen(frame_textencoding_terminator), 1)) == 0:
                frame_terminatorpos += 1
                pass
            # end if
            frame_filename = php_substr(parsedFrame["data"], frame_offset, frame_terminatorpos - frame_offset)
            if php_ord(frame_filename) == 0:
                frame_filename = ""
            # end if
            frame_offset = frame_terminatorpos + php_strlen(frame_textencoding_terminator)
            frame_terminatorpos = php_strpos(parsedFrame["data"], frame_textencoding_terminator, frame_offset)
            if php_ord(php_substr(parsedFrame["data"], frame_terminatorpos + php_strlen(frame_textencoding_terminator), 1)) == 0:
                frame_terminatorpos += 1
                pass
            # end if
            parsedFrame["description"] = php_substr(parsedFrame["data"], frame_offset, frame_terminatorpos - frame_offset)
            parsedFrame["description"] = self.makeutf16emptystringempty(parsedFrame["description"])
            frame_offset = frame_terminatorpos + php_strlen(frame_textencoding_terminator)
            parsedFrame["objectdata"] = php_str(php_substr(parsedFrame["data"], frame_offset))
            parsedFrame["encodingid"] = frame_textencoding
            parsedFrame["encoding"] = self.textencodingnamelookup(frame_textencoding)
            parsedFrame["mime"] = frame_mimetype
            parsedFrame["filename"] = frame_filename
            parsedFrame["data"] = None
        elif id3v2_majorversion >= 3 and parsedFrame["frame_name"] == "PCNT" or id3v2_majorversion == 2 and parsedFrame["frame_name"] == "CNT":
            #// 4.17  CNT  Play counter
            #// There may only be one 'PCNT' frame in each tag.
            #// When the counter reaches all one's, one byte is inserted in
            #// front of the counter thus making the counter eight bits bigger
            #// <Header for 'Play counter', ID: 'PCNT'>
            #// Counter        $xx xx xx xx (xx ...)
            parsedFrame["data"] = getid3_lib.bigendian2int(parsedFrame["data"])
        elif id3v2_majorversion >= 3 and parsedFrame["frame_name"] == "POPM" or id3v2_majorversion == 2 and parsedFrame["frame_name"] == "POP":
            #// 4.18  POP  Popularimeter
            #// There may be more than one 'POPM' frame in each tag,
            #// but only one with the same email address
            #// <Header for 'Popularimeter', ID: 'POPM'>
            #// Email to user   <text string> $00
            #// Rating          $xx
            #// Counter         $xx xx xx xx (xx ...)
            frame_offset = 0
            frame_terminatorpos = php_strpos(parsedFrame["data"], " ", frame_offset)
            frame_emailaddress = php_substr(parsedFrame["data"], frame_offset, frame_terminatorpos - frame_offset)
            if php_ord(frame_emailaddress) == 0:
                frame_emailaddress = ""
            # end if
            frame_offset = frame_terminatorpos + php_strlen(" ")
            frame_rating = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            parsedFrame["counter"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], frame_offset))
            parsedFrame["email"] = frame_emailaddress
            parsedFrame["rating"] = frame_rating
            parsedFrame["data"] = None
        elif id3v2_majorversion >= 3 and parsedFrame["frame_name"] == "RBUF" or id3v2_majorversion == 2 and parsedFrame["frame_name"] == "BUF":
            #// 4.19  BUF  Recommended buffer size
            #// There may only be one 'RBUF' frame in each tag
            #// <Header for 'Recommended buffer size', ID: 'RBUF'>
            #// Buffer size               $xx xx xx
            #// Embedded info flag        %0000000x
            #// Offset to next tag        $xx xx xx xx
            frame_offset = 0
            parsedFrame["buffersize"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], frame_offset, 3))
            frame_offset += 3
            frame_embeddedinfoflags = getid3_lib.bigendian2bin(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            parsedFrame["flags"]["embededinfo"] = php_bool(php_substr(frame_embeddedinfoflags, 7, 1))
            parsedFrame["nexttagoffset"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], frame_offset, 4))
            parsedFrame["data"] = None
        elif id3v2_majorversion == 2 and parsedFrame["frame_name"] == "CRM":
            #// 4.20  Encrypted meta frame (ID3v2.2 only)
            #// There may be more than one 'CRM' frame in a tag,
            #// but only one with the same 'owner identifier'
            #// <Header for 'Encrypted meta frame', ID: 'CRM'>
            #// Owner identifier      <textstring> $00 (00)
            #// Content/explanation   <textstring> $00 (00)
            #// Encrypted datablock   <binary data>
            frame_offset = 0
            frame_terminatorpos = php_strpos(parsedFrame["data"], " ", frame_offset)
            frame_ownerid = php_substr(parsedFrame["data"], frame_offset, frame_terminatorpos - frame_offset)
            frame_offset = frame_terminatorpos + php_strlen(" ")
            frame_terminatorpos = php_strpos(parsedFrame["data"], " ", frame_offset)
            parsedFrame["description"] = php_substr(parsedFrame["data"], frame_offset, frame_terminatorpos - frame_offset)
            parsedFrame["description"] = self.makeutf16emptystringempty(parsedFrame["description"])
            frame_offset = frame_terminatorpos + php_strlen(" ")
            parsedFrame["ownerid"] = frame_ownerid
            parsedFrame["data"] = php_str(php_substr(parsedFrame["data"], frame_offset))
            parsedFrame["data"] = None
        elif id3v2_majorversion >= 3 and parsedFrame["frame_name"] == "AENC" or id3v2_majorversion == 2 and parsedFrame["frame_name"] == "CRA":
            #// 4.21  CRA  Audio encryption
            #// There may be more than one 'AENC' frames in a tag,
            #// but only one with the same 'Owner identifier'
            #// <Header for 'Audio encryption', ID: 'AENC'>
            #// Owner identifier   <text string> $00
            #// Preview start      $xx xx
            #// Preview length     $xx xx
            #// Encryption info    <binary data>
            frame_offset = 0
            frame_terminatorpos = php_strpos(parsedFrame["data"], " ", frame_offset)
            frame_ownerid = php_substr(parsedFrame["data"], frame_offset, frame_terminatorpos - frame_offset)
            if php_ord(frame_ownerid) == 0:
                frame_ownerid = ""
            # end if
            frame_offset = frame_terminatorpos + php_strlen(" ")
            parsedFrame["ownerid"] = frame_ownerid
            parsedFrame["previewstart"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], frame_offset, 2))
            frame_offset += 2
            parsedFrame["previewlength"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], frame_offset, 2))
            frame_offset += 2
            parsedFrame["encryptioninfo"] = php_str(php_substr(parsedFrame["data"], frame_offset))
            parsedFrame["data"] = None
        elif id3v2_majorversion >= 3 and parsedFrame["frame_name"] == "LINK" or id3v2_majorversion == 2 and parsedFrame["frame_name"] == "LNK":
            #// 4.22  LNK  Linked information
            #// There may be more than one 'LINK' frame in a tag,
            #// but only one with the same contents
            #// <Header for 'Linked information', ID: 'LINK'>
            #// ID3v2.3+ => Frame identifier   $xx xx xx xx
            #// ID3v2.2  => Frame identifier   $xx xx xx
            #// URL                            <text string> $00
            #// ID and additional data         <text string(s)>
            frame_offset = 0
            if id3v2_majorversion == 2:
                parsedFrame["frameid"] = php_substr(parsedFrame["data"], frame_offset, 3)
                frame_offset += 3
            else:
                parsedFrame["frameid"] = php_substr(parsedFrame["data"], frame_offset, 4)
                frame_offset += 4
            # end if
            frame_terminatorpos = php_strpos(parsedFrame["data"], " ", frame_offset)
            frame_url = php_substr(parsedFrame["data"], frame_offset, frame_terminatorpos - frame_offset)
            if php_ord(frame_url) == 0:
                frame_url = ""
            # end if
            frame_offset = frame_terminatorpos + php_strlen(" ")
            parsedFrame["url"] = frame_url
            parsedFrame["additionaldata"] = php_str(php_substr(parsedFrame["data"], frame_offset))
            if (not php_empty(lambda : parsedFrame["framenameshort"])) and parsedFrame["url"]:
                info["id3v2"]["comments"][parsedFrame["framenameshort"]][-1] = getid3_lib.iconv_fallback_iso88591_utf8(parsedFrame["url"])
            # end if
            parsedFrame["data"] = None
        elif id3v2_majorversion >= 3 and parsedFrame["frame_name"] == "POSS":
            #// 4.21  POSS Position synchronisation frame (ID3v2.3+ only)
            #// There may only be one 'POSS' frame in each tag
            #// <Head for 'Position synchronisation', ID: 'POSS'>
            #// Time stamp format         $xx
            #// Position                  $xx (xx ...)
            frame_offset = 0
            parsedFrame["timestampformat"] = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            parsedFrame["position"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], frame_offset))
            parsedFrame["data"] = None
        elif id3v2_majorversion >= 3 and parsedFrame["frame_name"] == "USER":
            #// 4.22  USER Terms of use (ID3v2.3+ only)
            #// There may be more than one 'Terms of use' frame in a tag,
            #// but only one with the same 'Language'
            #// <Header for 'Terms of use frame', ID: 'USER'>
            #// Text encoding        $xx
            #// Language             $xx xx xx
            #// The actual text      <text string according to encoding>
            frame_offset = 0
            frame_textencoding = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            if id3v2_majorversion <= 3 and frame_textencoding > 1 or id3v2_majorversion == 4 and frame_textencoding > 3:
                self.warning("Invalid text encoding byte (" + frame_textencoding + ") in frame \"" + parsedFrame["frame_name"] + "\" - defaulting to ISO-8859-1 encoding")
            # end if
            frame_language = php_substr(parsedFrame["data"], frame_offset, 3)
            frame_offset += 3
            parsedFrame["language"] = frame_language
            parsedFrame["languagename"] = self.languagelookup(frame_language, False)
            parsedFrame["encodingid"] = frame_textencoding
            parsedFrame["encoding"] = self.textencodingnamelookup(frame_textencoding)
            parsedFrame["data"] = php_str(php_substr(parsedFrame["data"], frame_offset))
            parsedFrame["data"] = self.removestringterminator(parsedFrame["data"], self.textencodingterminatorlookup(frame_textencoding))
            if (not php_empty(lambda : parsedFrame["framenameshort"])) and (not php_empty(lambda : parsedFrame["data"])):
                info["id3v2"]["comments"][parsedFrame["framenameshort"]][-1] = getid3_lib.iconv_fallback(parsedFrame["encoding"], info["id3v2"]["encoding"], parsedFrame["data"])
            # end if
            parsedFrame["data"] = None
        elif id3v2_majorversion >= 3 and parsedFrame["frame_name"] == "OWNE":
            #// 4.23  OWNE Ownership frame (ID3v2.3+ only)
            #// There may only be one 'OWNE' frame in a tag
            #// <Header for 'Ownership frame', ID: 'OWNE'>
            #// Text encoding     $xx
            #// Price paid        <text string> $00
            #// Date of purch.    <text string>
            #// Seller            <text string according to encoding>
            frame_offset = 0
            frame_textencoding = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            if id3v2_majorversion <= 3 and frame_textencoding > 1 or id3v2_majorversion == 4 and frame_textencoding > 3:
                self.warning("Invalid text encoding byte (" + frame_textencoding + ") in frame \"" + parsedFrame["frame_name"] + "\" - defaulting to ISO-8859-1 encoding")
            # end if
            parsedFrame["encodingid"] = frame_textencoding
            parsedFrame["encoding"] = self.textencodingnamelookup(frame_textencoding)
            frame_terminatorpos = php_strpos(parsedFrame["data"], " ", frame_offset)
            frame_pricepaid = php_substr(parsedFrame["data"], frame_offset, frame_terminatorpos - frame_offset)
            frame_offset = frame_terminatorpos + php_strlen(" ")
            parsedFrame["pricepaid"]["currencyid"] = php_substr(frame_pricepaid, 0, 3)
            parsedFrame["pricepaid"]["currency"] = self.lookupcurrencyunits(parsedFrame["pricepaid"]["currencyid"])
            parsedFrame["pricepaid"]["value"] = php_substr(frame_pricepaid, 3)
            parsedFrame["purchasedate"] = php_substr(parsedFrame["data"], frame_offset, 8)
            if self.isvaliddatestampstring(parsedFrame["purchasedate"]):
                parsedFrame["purchasedateunix"] = mktime(0, 0, 0, php_substr(parsedFrame["purchasedate"], 4, 2), php_substr(parsedFrame["purchasedate"], 6, 2), php_substr(parsedFrame["purchasedate"], 0, 4))
            # end if
            frame_offset += 8
            parsedFrame["seller"] = php_str(php_substr(parsedFrame["data"], frame_offset))
            parsedFrame["seller"] = self.removestringterminator(parsedFrame["seller"], self.textencodingterminatorlookup(frame_textencoding))
            parsedFrame["data"] = None
        elif id3v2_majorversion >= 3 and parsedFrame["frame_name"] == "COMR":
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
            frame_offset = 0
            frame_textencoding = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            frame_textencoding_terminator = self.textencodingterminatorlookup(frame_textencoding)
            if id3v2_majorversion <= 3 and frame_textencoding > 1 or id3v2_majorversion == 4 and frame_textencoding > 3:
                self.warning("Invalid text encoding byte (" + frame_textencoding + ") in frame \"" + parsedFrame["frame_name"] + "\" - defaulting to ISO-8859-1 encoding")
                frame_textencoding_terminator = " "
            # end if
            frame_terminatorpos = php_strpos(parsedFrame["data"], " ", frame_offset)
            frame_pricestring = php_substr(parsedFrame["data"], frame_offset, frame_terminatorpos - frame_offset)
            frame_offset = frame_terminatorpos + php_strlen(" ")
            frame_rawpricearray = php_explode("/", frame_pricestring)
            for key,val in frame_rawpricearray:
                frame_currencyid = php_substr(val, 0, 3)
                parsedFrame["price"][frame_currencyid]["currency"] = self.lookupcurrencyunits(frame_currencyid)
                parsedFrame["price"][frame_currencyid]["value"] = php_substr(val, 3)
            # end for
            frame_datestring = php_substr(parsedFrame["data"], frame_offset, 8)
            frame_offset += 8
            frame_terminatorpos = php_strpos(parsedFrame["data"], " ", frame_offset)
            frame_contacturl = php_substr(parsedFrame["data"], frame_offset, frame_terminatorpos - frame_offset)
            frame_offset = frame_terminatorpos + php_strlen(" ")
            frame_receivedasid = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            frame_terminatorpos = php_strpos(parsedFrame["data"], frame_textencoding_terminator, frame_offset)
            if php_ord(php_substr(parsedFrame["data"], frame_terminatorpos + php_strlen(frame_textencoding_terminator), 1)) == 0:
                frame_terminatorpos += 1
                pass
            # end if
            frame_sellername = php_substr(parsedFrame["data"], frame_offset, frame_terminatorpos - frame_offset)
            if php_ord(frame_sellername) == 0:
                frame_sellername = ""
            # end if
            frame_offset = frame_terminatorpos + php_strlen(frame_textencoding_terminator)
            frame_terminatorpos = php_strpos(parsedFrame["data"], frame_textencoding_terminator, frame_offset)
            if php_ord(php_substr(parsedFrame["data"], frame_terminatorpos + php_strlen(frame_textencoding_terminator), 1)) == 0:
                frame_terminatorpos += 1
                pass
            # end if
            parsedFrame["description"] = php_substr(parsedFrame["data"], frame_offset, frame_terminatorpos - frame_offset)
            parsedFrame["description"] = self.makeutf16emptystringempty(parsedFrame["description"])
            frame_offset = frame_terminatorpos + php_strlen(frame_textencoding_terminator)
            frame_terminatorpos = php_strpos(parsedFrame["data"], " ", frame_offset)
            frame_mimetype = php_substr(parsedFrame["data"], frame_offset, frame_terminatorpos - frame_offset)
            frame_offset = frame_terminatorpos + php_strlen(" ")
            frame_sellerlogo = php_substr(parsedFrame["data"], frame_offset)
            parsedFrame["encodingid"] = frame_textencoding
            parsedFrame["encoding"] = self.textencodingnamelookup(frame_textencoding)
            parsedFrame["pricevaliduntil"] = frame_datestring
            parsedFrame["contacturl"] = frame_contacturl
            parsedFrame["receivedasid"] = frame_receivedasid
            parsedFrame["receivedas"] = self.comrreceivedaslookup(frame_receivedasid)
            parsedFrame["sellername"] = frame_sellername
            parsedFrame["mime"] = frame_mimetype
            parsedFrame["logo"] = frame_sellerlogo
            parsedFrame["data"] = None
        elif id3v2_majorversion >= 3 and parsedFrame["frame_name"] == "ENCR":
            #// 4.25  ENCR Encryption method registration (ID3v2.3+ only)
            #// There may be several 'ENCR' frames in a tag,
            #// but only one containing the same symbol
            #// and only one containing the same owner identifier
            #// <Header for 'Encryption method registration', ID: 'ENCR'>
            #// Owner identifier    <text string> $00
            #// Method symbol       $xx
            #// Encryption data     <binary data>
            frame_offset = 0
            frame_terminatorpos = php_strpos(parsedFrame["data"], " ", frame_offset)
            frame_ownerid = php_substr(parsedFrame["data"], frame_offset, frame_terminatorpos - frame_offset)
            if php_ord(frame_ownerid) == 0:
                frame_ownerid = ""
            # end if
            frame_offset = frame_terminatorpos + php_strlen(" ")
            parsedFrame["ownerid"] = frame_ownerid
            parsedFrame["methodsymbol"] = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            parsedFrame["data"] = php_str(php_substr(parsedFrame["data"], frame_offset))
        elif id3v2_majorversion >= 3 and parsedFrame["frame_name"] == "GRID":
            #// 4.26  GRID Group identification registration (ID3v2.3+ only)
            #// There may be several 'GRID' frames in a tag,
            #// but only one containing the same symbol
            #// and only one containing the same owner identifier
            #// <Header for 'Group ID registration', ID: 'GRID'>
            #// Owner identifier      <text string> $00
            #// Group symbol          $xx
            #// Group dependent data  <binary data>
            frame_offset = 0
            frame_terminatorpos = php_strpos(parsedFrame["data"], " ", frame_offset)
            frame_ownerid = php_substr(parsedFrame["data"], frame_offset, frame_terminatorpos - frame_offset)
            if php_ord(frame_ownerid) == 0:
                frame_ownerid = ""
            # end if
            frame_offset = frame_terminatorpos + php_strlen(" ")
            parsedFrame["ownerid"] = frame_ownerid
            parsedFrame["groupsymbol"] = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            parsedFrame["data"] = php_str(php_substr(parsedFrame["data"], frame_offset))
        elif id3v2_majorversion >= 3 and parsedFrame["frame_name"] == "PRIV":
            #// 4.27  PRIV Private frame (ID3v2.3+ only)
            #// The tag may contain more than one 'PRIV' frame
            #// but only with different contents
            #// <Header for 'Private frame', ID: 'PRIV'>
            #// Owner identifier      <text string> $00
            #// The private data      <binary data>
            frame_offset = 0
            frame_terminatorpos = php_strpos(parsedFrame["data"], " ", frame_offset)
            frame_ownerid = php_substr(parsedFrame["data"], frame_offset, frame_terminatorpos - frame_offset)
            if php_ord(frame_ownerid) == 0:
                frame_ownerid = ""
            # end if
            frame_offset = frame_terminatorpos + php_strlen(" ")
            parsedFrame["ownerid"] = frame_ownerid
            parsedFrame["data"] = php_str(php_substr(parsedFrame["data"], frame_offset))
        elif id3v2_majorversion >= 4 and parsedFrame["frame_name"] == "SIGN":
            #// 4.28  SIGN Signature frame (ID3v2.4+ only)
            #// There may be more than one 'signature frame' in a tag,
            #// but no two may be identical
            #// <Header for 'Signature frame', ID: 'SIGN'>
            #// Group symbol      $xx
            #// Signature         <binary data>
            frame_offset = 0
            parsedFrame["groupsymbol"] = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            parsedFrame["data"] = php_str(php_substr(parsedFrame["data"], frame_offset))
        elif id3v2_majorversion >= 4 and parsedFrame["frame_name"] == "SEEK":
            #// 4.29  SEEK Seek frame (ID3v2.4+ only)
            #// There may only be one 'seek frame' in a tag
            #// <Header for 'Seek frame', ID: 'SEEK'>
            #// Minimum offset to next tag       $xx xx xx xx
            frame_offset = 0
            parsedFrame["data"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], frame_offset, 4))
        elif id3v2_majorversion >= 4 and parsedFrame["frame_name"] == "ASPI":
            #// 4.30  ASPI Audio seek point index (ID3v2.4+ only)
            #// There may only be one 'audio seek point index' frame in a tag
            #// <Header for 'Seek Point Index', ID: 'ASPI'>
            #// Indexed data start (S)         $xx xx xx xx
            #// Indexed data length (L)        $xx xx xx xx
            #// Number of index points (N)     $xx xx
            #// Bits per index point (b)       $xx
            #// Then for every index point the following data is included:
            #// Fraction at index (Fi)          $xx (xx)
            frame_offset = 0
            parsedFrame["datastart"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], frame_offset, 4))
            frame_offset += 4
            parsedFrame["indexeddatalength"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], frame_offset, 4))
            frame_offset += 4
            parsedFrame["indexpoints"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], frame_offset, 2))
            frame_offset += 2
            parsedFrame["bitsperpoint"] = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            frame_bytesperpoint = ceil(parsedFrame["bitsperpoint"] / 8)
            i = 0
            while i < parsedFrame["indexpoints"]:
                
                parsedFrame["indexes"][i] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], frame_offset, frame_bytesperpoint))
                frame_offset += frame_bytesperpoint
                i += 1
            # end while
            parsedFrame["data"] = None
        elif id3v2_majorversion >= 3 and parsedFrame["frame_name"] == "RGAD":
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
            frame_offset = 0
            parsedFrame["peakamplitude"] = getid3_lib.bigendian2float(php_substr(parsedFrame["data"], frame_offset, 4))
            frame_offset += 4
            rg_track_adjustment = getid3_lib.dec2bin(php_substr(parsedFrame["data"], frame_offset, 2))
            frame_offset += 2
            rg_album_adjustment = getid3_lib.dec2bin(php_substr(parsedFrame["data"], frame_offset, 2))
            frame_offset += 2
            parsedFrame["raw"]["track"]["name"] = getid3_lib.bin2dec(php_substr(rg_track_adjustment, 0, 3))
            parsedFrame["raw"]["track"]["originator"] = getid3_lib.bin2dec(php_substr(rg_track_adjustment, 3, 3))
            parsedFrame["raw"]["track"]["signbit"] = getid3_lib.bin2dec(php_substr(rg_track_adjustment, 6, 1))
            parsedFrame["raw"]["track"]["adjustment"] = getid3_lib.bin2dec(php_substr(rg_track_adjustment, 7, 9))
            parsedFrame["raw"]["album"]["name"] = getid3_lib.bin2dec(php_substr(rg_album_adjustment, 0, 3))
            parsedFrame["raw"]["album"]["originator"] = getid3_lib.bin2dec(php_substr(rg_album_adjustment, 3, 3))
            parsedFrame["raw"]["album"]["signbit"] = getid3_lib.bin2dec(php_substr(rg_album_adjustment, 6, 1))
            parsedFrame["raw"]["album"]["adjustment"] = getid3_lib.bin2dec(php_substr(rg_album_adjustment, 7, 9))
            parsedFrame["track"]["name"] = getid3_lib.rgadnamelookup(parsedFrame["raw"]["track"]["name"])
            parsedFrame["track"]["originator"] = getid3_lib.rgadoriginatorlookup(parsedFrame["raw"]["track"]["originator"])
            parsedFrame["track"]["adjustment"] = getid3_lib.rgadadjustmentlookup(parsedFrame["raw"]["track"]["adjustment"], parsedFrame["raw"]["track"]["signbit"])
            parsedFrame["album"]["name"] = getid3_lib.rgadnamelookup(parsedFrame["raw"]["album"]["name"])
            parsedFrame["album"]["originator"] = getid3_lib.rgadoriginatorlookup(parsedFrame["raw"]["album"]["originator"])
            parsedFrame["album"]["adjustment"] = getid3_lib.rgadadjustmentlookup(parsedFrame["raw"]["album"]["adjustment"], parsedFrame["raw"]["album"]["signbit"])
            info["replay_gain"]["track"]["peak"] = parsedFrame["peakamplitude"]
            info["replay_gain"]["track"]["originator"] = parsedFrame["track"]["originator"]
            info["replay_gain"]["track"]["adjustment"] = parsedFrame["track"]["adjustment"]
            info["replay_gain"]["album"]["originator"] = parsedFrame["album"]["originator"]
            info["replay_gain"]["album"]["adjustment"] = parsedFrame["album"]["adjustment"]
            parsedFrame["data"] = None
        elif id3v2_majorversion >= 3 and parsedFrame["frame_name"] == "CHAP":
            #// CHAP Chapters frame (ID3v2.3+ only)
            #// http://id3.org/id3v2-chapters-1.0
            #// <ID3v2.3 or ID3v2.4 frame header, ID: "CHAP">           (10 bytes)
            #// Element ID      <text string> $00
            #// Start time      $xx xx xx xx
            #// End time        $xx xx xx xx
            #// Start offset    $xx xx xx xx
            #// End offset      $xx xx xx xx
            #// <Optional embedded sub-frames>
            frame_offset = 0
            php_no_error(lambda: parsedFrame["element_id"] = php_explode(" ", parsedFrame["data"], 2))
            frame_offset += php_strlen(parsedFrame["element_id"] + " ")
            parsedFrame["time_begin"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], frame_offset, 4))
            frame_offset += 4
            parsedFrame["time_end"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], frame_offset, 4))
            frame_offset += 4
            if php_substr(parsedFrame["data"], frame_offset, 4) != "ÿÿÿÿ":
                #// "If these bytes are all set to 0xFF then the value should be ignored and the start time value should be utilized."
                parsedFrame["offset_begin"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], frame_offset, 4))
            # end if
            frame_offset += 4
            if php_substr(parsedFrame["data"], frame_offset, 4) != "ÿÿÿÿ":
                #// "If these bytes are all set to 0xFF then the value should be ignored and the start time value should be utilized."
                parsedFrame["offset_end"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], frame_offset, 4))
            # end if
            frame_offset += 4
            if frame_offset < php_strlen(parsedFrame["data"]):
                parsedFrame["subframes"] = Array()
                while True:
                    
                    if not (frame_offset < php_strlen(parsedFrame["data"])):
                        break
                    # end if
                    #// <Optional embedded sub-frames>
                    subframe = Array()
                    subframe["name"] = php_substr(parsedFrame["data"], frame_offset, 4)
                    frame_offset += 4
                    subframe["size"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], frame_offset, 4))
                    frame_offset += 4
                    subframe["flags_raw"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], frame_offset, 2))
                    frame_offset += 2
                    if subframe["size"] > php_strlen(parsedFrame["data"]) - frame_offset:
                        self.warning("CHAP subframe \"" + subframe["name"] + "\" at frame offset " + frame_offset + " claims to be \"" + subframe["size"] + "\" bytes, which is more than the available data (" + php_strlen(parsedFrame["data"]) - frame_offset + " bytes)")
                        break
                    # end if
                    subframe_rawdata = php_substr(parsedFrame["data"], frame_offset, subframe["size"])
                    frame_offset += subframe["size"]
                    subframe["encodingid"] = php_ord(php_substr(subframe_rawdata, 0, 1))
                    subframe["text"] = php_substr(subframe_rawdata, 1)
                    subframe["encoding"] = self.textencodingnamelookup(subframe["encodingid"])
                    encoding_converted_text = php_trim(getid3_lib.iconv_fallback(subframe["encoding"], info["encoding"], subframe["text"]))
                    for case in Switch(php_substr(encoding_converted_text, 0, 2)):
                        if case("ÿþ"):
                            pass
                        # end if
                        if case("þÿ"):
                            for case in Switch(php_strtoupper(info["id3v2"]["encoding"])):
                                if case("ISO-8859-1"):
                                    pass
                                # end if
                                if case("UTF-8"):
                                    encoding_converted_text = php_substr(encoding_converted_text, 2)
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
                    for case in Switch(subframe["name"]):
                        if case("TIT2"):
                            parsedFrame["chapter_name"] = encoding_converted_text
                            parsedFrame["subframes"][-1] = subframe
                            break
                        # end if
                        if case("TIT3"):
                            parsedFrame["chapter_description"] = encoding_converted_text
                            parsedFrame["subframes"][-1] = subframe
                            break
                        # end if
                        if case("WXXX"):
                            subframe["chapter_url_description"], subframe["chapter_url"] = php_explode(" ", encoding_converted_text, 2)
                            parsedFrame["chapter_url"][subframe["chapter_url_description"]] = subframe["chapter_url"]
                            parsedFrame["subframes"][-1] = subframe
                            break
                        # end if
                        if case("APIC"):
                            if php_preg_match("#^([^\\x00]+)*\\x00(.)([^\\x00]+)*\\x00(.+)$#s", subframe["text"], matches):
                                dummy, subframe_apic_mime, subframe_apic_picturetype, subframe_apic_description, subframe_apic_picturedata = matches
                                subframe["image_mime"] = php_trim(getid3_lib.iconv_fallback(subframe["encoding"], info["encoding"], subframe_apic_mime))
                                subframe["picture_type"] = self.apicpicturetypelookup(subframe_apic_picturetype)
                                subframe["description"] = php_trim(getid3_lib.iconv_fallback(subframe["encoding"], info["encoding"], subframe_apic_description))
                                if php_strlen(self.textencodingterminatorlookup(subframe["encoding"])) == 2:
                                    #// the null terminator between "description" and "picture data" could be either 1 byte (ISO-8859-1, UTF-8) or two bytes (UTF-16)
                                    #// the above regex assumes one byte, if it's actually two then strip the second one here
                                    subframe_apic_picturedata = php_substr(subframe_apic_picturedata, 1)
                                # end if
                                subframe["data"] = subframe_apic_picturedata
                                dummy = None
                                subframe_apic_mime = None
                                subframe_apic_picturetype = None
                                subframe_apic_description = None
                                subframe_apic_picturedata = None
                                subframe["text"] = None
                                parsedFrame["text"] = None
                                parsedFrame["subframes"][-1] = subframe
                                parsedFrame["picture_present"] = True
                            else:
                                self.warning("ID3v2.CHAP subframe #" + php_count(parsedFrame["subframes"]) + 1 + " \"" + subframe["name"] + "\" not in expected format")
                            # end if
                            break
                        # end if
                        if case():
                            self.warning("ID3v2.CHAP subframe \"" + subframe["name"] + "\" not handled (supported: TIT2, TIT3, WXXX, APIC)")
                            break
                        # end if
                    # end for
                # end while
                subframe_rawdata = None
                subframe = None
                encoding_converted_text = None
                parsedFrame["data"] = None
                pass
            # end if
            id3v2_chapter_entry = Array()
            for id3v2_chapter_key in Array("id", "time_begin", "time_end", "offset_begin", "offset_end", "chapter_name", "chapter_description", "chapter_url", "picture_present"):
                if (php_isset(lambda : parsedFrame[id3v2_chapter_key])):
                    id3v2_chapter_entry[id3v2_chapter_key] = parsedFrame[id3v2_chapter_key]
                # end if
            # end for
            if (not (php_isset(lambda : info["id3v2"]["chapters"]))):
                info["id3v2"]["chapters"] = Array()
            # end if
            info["id3v2"]["chapters"][-1] = id3v2_chapter_entry
            id3v2_chapter_entry = None
            id3v2_chapter_key = None
        elif id3v2_majorversion >= 3 and parsedFrame["frame_name"] == "CTOC":
            #// CTOC Chapters Table Of Contents frame (ID3v2.3+ only)
            #// http://id3.org/id3v2-chapters-1.0
            #// <ID3v2.3 or ID3v2.4 frame header, ID: "CTOC">           (10 bytes)
            #// Element ID      <text string> $00
            #// CTOC flags        %xx
            #// Entry count       $xx
            #// Child Element ID  <string>$00   /* zero or more child CHAP or CTOC entries
            #// <Optional embedded sub-frames>
            frame_offset = 0
            php_no_error(lambda: parsedFrame["element_id"] = php_explode(" ", parsedFrame["data"], 2))
            frame_offset += php_strlen(parsedFrame["element_id"] + " ")
            ctoc_flags_raw = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            parsedFrame["entry_count"] = php_ord(php_substr(parsedFrame["data"], frame_offset, 1))
            frame_offset += 1
            terminator_position = None
            i = 0
            while i < parsedFrame["entry_count"]:
                
                terminator_position = php_strpos(parsedFrame["data"], " ", frame_offset)
                parsedFrame["child_element_ids"][i] = php_substr(parsedFrame["data"], frame_offset, terminator_position - frame_offset)
                frame_offset = terminator_position + 1
                i += 1
            # end while
            parsedFrame["ctoc_flags"]["ordered"] = php_bool(ctoc_flags_raw & 1)
            parsedFrame["ctoc_flags"]["top_level"] = php_bool(ctoc_flags_raw & 3)
            ctoc_flags_raw = None
            terminator_position = None
            if frame_offset < php_strlen(parsedFrame["data"]):
                parsedFrame["subframes"] = Array()
                while True:
                    
                    if not (frame_offset < php_strlen(parsedFrame["data"])):
                        break
                    # end if
                    #// <Optional embedded sub-frames>
                    subframe = Array()
                    subframe["name"] = php_substr(parsedFrame["data"], frame_offset, 4)
                    frame_offset += 4
                    subframe["size"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], frame_offset, 4))
                    frame_offset += 4
                    subframe["flags_raw"] = getid3_lib.bigendian2int(php_substr(parsedFrame["data"], frame_offset, 2))
                    frame_offset += 2
                    if subframe["size"] > php_strlen(parsedFrame["data"]) - frame_offset:
                        self.warning("CTOS subframe \"" + subframe["name"] + "\" at frame offset " + frame_offset + " claims to be \"" + subframe["size"] + "\" bytes, which is more than the available data (" + php_strlen(parsedFrame["data"]) - frame_offset + " bytes)")
                        break
                    # end if
                    subframe_rawdata = php_substr(parsedFrame["data"], frame_offset, subframe["size"])
                    frame_offset += subframe["size"]
                    subframe["encodingid"] = php_ord(php_substr(subframe_rawdata, 0, 1))
                    subframe["text"] = php_substr(subframe_rawdata, 1)
                    subframe["encoding"] = self.textencodingnamelookup(subframe["encodingid"])
                    encoding_converted_text = php_trim(getid3_lib.iconv_fallback(subframe["encoding"], info["encoding"], subframe["text"]))
                    for case in Switch(php_substr(encoding_converted_text, 0, 2)):
                        if case("ÿþ"):
                            pass
                        # end if
                        if case("þÿ"):
                            for case in Switch(php_strtoupper(info["id3v2"]["encoding"])):
                                if case("ISO-8859-1"):
                                    pass
                                # end if
                                if case("UTF-8"):
                                    encoding_converted_text = php_substr(encoding_converted_text, 2)
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
                    if subframe["name"] == "TIT2" or subframe["name"] == "TIT3":
                        if subframe["name"] == "TIT2":
                            parsedFrame["toc_name"] = encoding_converted_text
                        elif subframe["name"] == "TIT3":
                            parsedFrame["toc_description"] = encoding_converted_text
                        # end if
                        parsedFrame["subframes"][-1] = subframe
                    else:
                        self.warning("ID3v2.CTOC subframe \"" + subframe["name"] + "\" not handled (only TIT2 and TIT3)")
                    # end if
                # end while
                subframe_rawdata = None
                subframe = None
                encoding_converted_text = None
            # end if
        # end if
        return True
    # end def parseid3v2frame
    #// 
    #// @param string $data
    #// 
    #// @return string
    #//
    def deunsynchronise(self, data=None):
        
        return php_str_replace("ÿ ", "ÿ", data)
    # end def deunsynchronise
    #// 
    #// @param int $index
    #// 
    #// @return string
    #//
    def lookupextendedheaderrestrictionstagsizelimits(self, index=None):
        
        LookupExtendedHeaderRestrictionsTagSizeLimits = Array({0: "No more than 128 frames and 1 MB total tag size", 1: "No more than 64 frames and 128 KB total tag size", 2: "No more than 32 frames and 40 KB total tag size", 3: "No more than 32 frames and 4 KB total tag size"})
        return LookupExtendedHeaderRestrictionsTagSizeLimits[index] if (php_isset(lambda : LookupExtendedHeaderRestrictionsTagSizeLimits[index])) else ""
    # end def lookupextendedheaderrestrictionstagsizelimits
    #// 
    #// @param int $index
    #// 
    #// @return string
    #//
    def lookupextendedheaderrestrictionstextencodings(self, index=None):
        
        LookupExtendedHeaderRestrictionsTextEncodings = Array({0: "No restrictions", 1: "Strings are only encoded with ISO-8859-1 or UTF-8"})
        return LookupExtendedHeaderRestrictionsTextEncodings[index] if (php_isset(lambda : LookupExtendedHeaderRestrictionsTextEncodings[index])) else ""
    # end def lookupextendedheaderrestrictionstextencodings
    #// 
    #// @param int $index
    #// 
    #// @return string
    #//
    def lookupextendedheaderrestrictionstextfieldsize(self, index=None):
        
        LookupExtendedHeaderRestrictionsTextFieldSize = Array({0: "No restrictions", 1: "No string is longer than 1024 characters", 2: "No string is longer than 128 characters", 3: "No string is longer than 30 characters"})
        return LookupExtendedHeaderRestrictionsTextFieldSize[index] if (php_isset(lambda : LookupExtendedHeaderRestrictionsTextFieldSize[index])) else ""
    # end def lookupextendedheaderrestrictionstextfieldsize
    #// 
    #// @param int $index
    #// 
    #// @return string
    #//
    def lookupextendedheaderrestrictionsimageencoding(self, index=None):
        
        LookupExtendedHeaderRestrictionsImageEncoding = Array({0: "No restrictions", 1: "Images are encoded only with PNG or JPEG"})
        return LookupExtendedHeaderRestrictionsImageEncoding[index] if (php_isset(lambda : LookupExtendedHeaderRestrictionsImageEncoding[index])) else ""
    # end def lookupextendedheaderrestrictionsimageencoding
    #// 
    #// @param int $index
    #// 
    #// @return string
    #//
    def lookupextendedheaderrestrictionsimagesizesize(self, index=None):
        
        LookupExtendedHeaderRestrictionsImageSizeSize = Array({0: "No restrictions", 1: "All images are 256x256 pixels or smaller", 2: "All images are 64x64 pixels or smaller", 3: "All images are exactly 64x64 pixels, unless required otherwise"})
        return LookupExtendedHeaderRestrictionsImageSizeSize[index] if (php_isset(lambda : LookupExtendedHeaderRestrictionsImageSizeSize[index])) else ""
    # end def lookupextendedheaderrestrictionsimagesizesize
    #// 
    #// @param string $currencyid
    #// 
    #// @return string
    #//
    def lookupcurrencyunits(self, currencyid=None):
        
        begin = 0
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
        return getid3_lib.embeddedlookup(currencyid, begin, 0, __FILE__, "id3v2-currency-units")
    # end def lookupcurrencyunits
    #// 
    #// @param string $currencyid
    #// 
    #// @return string
    #//
    def lookupcurrencycountry(self, currencyid=None):
        
        begin = 0
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
        return getid3_lib.embeddedlookup(currencyid, begin, 0, __FILE__, "id3v2-currency-country")
    # end def lookupcurrencycountry
    #// 
    #// @param string $languagecode
    #// @param bool   $casesensitive
    #// 
    #// @return string
    #//
    @classmethod
    def languagelookup(self, languagecode=None, casesensitive=False):
        
        if (not casesensitive):
            languagecode = php_strtolower(languagecode)
        # end if
        #// http://www.id3.org/id3v2.4.0-structure.txt
        #// [4.   ID3v2 frame overview]
        #// The three byte language field, present in several frames, is used to
        #// describe the language of the frame's content, according to ISO-639-2
        #// [ISO-639-2]. The language should be represented in lower case. If the
        #// language is not known the string "XXX" should be used.
        #// ISO 639-2 - http://www.id3.org/iso639-2.html
        begin = 0
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
        return getid3_lib.embeddedlookup(languagecode, begin, 0, __FILE__, "id3v2-languagecode")
    # end def languagelookup
    #// 
    #// @param int $index
    #// 
    #// @return string
    #//
    @classmethod
    def etcoeventlookup(self, index=None):
        
        if index >= 23 and index <= 223:
            return "reserved for future use"
        # end if
        if index >= 224 and index <= 239:
            return "not predefined synch 0-F"
        # end if
        if index >= 240 and index <= 252:
            return "reserved for future use"
        # end if
        EventLookup = Array({0: "padding (has no meaning)", 1: "end of initial silence", 2: "intro start", 3: "main part start", 4: "outro start", 5: "outro end", 6: "verse start", 7: "refrain start", 8: "interlude start", 9: "theme start", 10: "variation start", 11: "key change", 12: "time change", 13: "momentary unwanted noise (Snap, Crackle & Pop)", 14: "sustained noise", 15: "sustained noise end", 16: "intro end", 17: "main part end", 18: "verse end", 19: "refrain end", 20: "theme end", 21: "profanity", 22: "profanity end", 253: "audio end (start of silence)", 254: "audio file ends", 255: "one more byte of events follows"})
        return EventLookup[index] if (php_isset(lambda : EventLookup[index])) else ""
    # end def etcoeventlookup
    #// 
    #// @param int $index
    #// 
    #// @return string
    #//
    @classmethod
    def sytlcontenttypelookup(self, index=None):
        
        SYTLContentTypeLookup = Array({0: "other", 1: "lyrics", 2: "text transcription", 3: "movement/part name", 4: "events", 5: "chord", 6: "trivia/'pop up' information", 7: "URLs to webpages", 8: "URLs to images"})
        return SYTLContentTypeLookup[index] if (php_isset(lambda : SYTLContentTypeLookup[index])) else ""
    # end def sytlcontenttypelookup
    #// 
    #// @param int   $index
    #// @param bool $returnarray
    #// 
    #// @return array|string
    #//
    @classmethod
    def apicpicturetypelookup(self, index=None, returnarray=False):
        
        APICPictureTypeLookup = Array({0: "Other", 1: "32x32 pixels 'file icon' (PNG only)", 2: "Other file icon", 3: "Cover (front)", 4: "Cover (back)", 5: "Leaflet page", 6: "Media (e.g. label side of CD)", 7: "Lead artist/lead performer/soloist", 8: "Artist/performer", 9: "Conductor", 10: "Band/Orchestra", 11: "Composer", 12: "Lyricist/text writer", 13: "Recording Location", 14: "During recording", 15: "During performance", 16: "Movie/video screen capture", 17: "A bright coloured fish", 18: "Illustration", 19: "Band/artist logotype", 20: "Publisher/Studio logotype"})
        if returnarray:
            return APICPictureTypeLookup
        # end if
        return APICPictureTypeLookup[index] if (php_isset(lambda : APICPictureTypeLookup[index])) else ""
    # end def apicpicturetypelookup
    #// 
    #// @param int $index
    #// 
    #// @return string
    #//
    @classmethod
    def comrreceivedaslookup(self, index=None):
        
        COMRReceivedAsLookup = Array({0: "Other", 1: "Standard CD album with other songs", 2: "Compressed audio on CD", 3: "File over the Internet", 4: "Stream over the Internet", 5: "As note sheets", 6: "As note sheets in a book with other sheets", 7: "Music on other media", 8: "Non-musical merchandise"})
        return COMRReceivedAsLookup[index] if (php_isset(lambda : COMRReceivedAsLookup[index])) else ""
    # end def comrreceivedaslookup
    #// 
    #// @param int $index
    #// 
    #// @return string
    #//
    @classmethod
    def rva2channeltypelookup(self, index=None):
        
        RVA2ChannelTypeLookup = Array({0: "Other", 1: "Master volume", 2: "Front right", 3: "Front left", 4: "Back right", 5: "Back left", 6: "Front centre", 7: "Back centre", 8: "Subwoofer"})
        return RVA2ChannelTypeLookup[index] if (php_isset(lambda : RVA2ChannelTypeLookup[index])) else ""
    # end def rva2channeltypelookup
    #// 
    #// @param string $framename
    #// 
    #// @return string
    #//
    @classmethod
    def framenamelonglookup(self, framename=None):
        
        begin = 0
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
        return getid3_lib.embeddedlookup(framename, begin, 0, __FILE__, "id3v2-framename_long")
        pass
    # end def framenamelonglookup
    #// 
    #// @param string $framename
    #// 
    #// @return string
    #//
    @classmethod
    def framenameshortlookup(self, framename=None):
        
        begin = 0
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
        return getid3_lib.embeddedlookup(framename, begin, 0, __FILE__, "id3v2-framename_short")
    # end def framenameshortlookup
    #// 
    #// @param string $encoding
    #// 
    #// @return string
    #//
    @classmethod
    def textencodingterminatorlookup(self, encoding=None):
        
        TextEncodingTerminatorLookup = Array({0: " ", 1: "  ", 2: "  ", 3: " ", 255: "  "})
        return TextEncodingTerminatorLookup[encoding] if (php_isset(lambda : TextEncodingTerminatorLookup[encoding])) else " "
    # end def textencodingterminatorlookup
    #// 
    #// @param int $encoding
    #// 
    #// @return string
    #//
    @classmethod
    def textencodingnamelookup(self, encoding=None):
        
        TextEncodingNameLookup = Array({0: "ISO-8859-1", 1: "UTF-16", 2: "UTF-16BE", 3: "UTF-8", 255: "UTF-16BE"})
        return TextEncodingNameLookup[encoding] if (php_isset(lambda : TextEncodingNameLookup[encoding])) else "ISO-8859-1"
    # end def textencodingnamelookup
    #// 
    #// @param string $string
    #// @param string $terminator
    #// 
    #// @return string
    #//
    @classmethod
    def removestringterminator(self, string=None, terminator=None):
        
        #// Null terminator at end of comment string is somewhat ambiguous in the specification, may or may not be implemented by various taggers. Remove terminator only if present.
        #// https://github.com/JamesHeinrich/getID3/issues/121
        #// https://community.mp3tag.de/t/x-trailing-nulls-in-id3v2-comments/19227
        if php_substr(string, -php_strlen(terminator), php_strlen(terminator)) == terminator:
            string = php_substr(string, 0, -php_strlen(terminator))
        # end if
        return string
    # end def removestringterminator
    #// 
    #// @param string $string
    #// 
    #// @return string
    #//
    @classmethod
    def makeutf16emptystringempty(self, string=None):
        
        if php_in_array(string, Array(" ", "  ", "ÿþ", "þÿ")):
            #// if string only contains a BOM or terminator then make it actually an empty string
            string = ""
        # end if
        return string
    # end def makeutf16emptystringempty
    #// 
    #// @param string $framename
    #// @param int    $id3v2majorversion
    #// 
    #// @return bool|int
    #//
    @classmethod
    def isvalidid3v2framename(self, framename=None, id3v2majorversion=None):
        
        for case in Switch(id3v2majorversion):
            if case(2):
                return php_preg_match("#[A-Z][A-Z0-9]{2}#", framename)
                break
            # end if
            if case(3):
                pass
            # end if
            if case(4):
                return php_preg_match("#[A-Z][A-Z0-9]{3}#", framename)
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
    def isanumber(self, numberstring=None, allowdecimal=False, allownegative=False):
        
        i = 0
        while i < php_strlen(numberstring):
            
            if chr(numberstring[i]) < chr("0") or chr(numberstring[i]) > chr("9"):
                if numberstring[i] == "." and allowdecimal:
                    pass
                elif numberstring[i] == "-" and allownegative and i == 0:
                    pass
                else:
                    return False
                # end if
            # end if
            i += 1
        # end while
        return True
    # end def isanumber
    #// 
    #// @param string $datestamp
    #// 
    #// @return bool
    #//
    @classmethod
    def isvaliddatestampstring(self, datestamp=None):
        
        if php_strlen(datestamp) != 8:
            return False
        # end if
        if (not self.isanumber(datestamp, False)):
            return False
        # end if
        year = php_substr(datestamp, 0, 4)
        month = php_substr(datestamp, 4, 2)
        day = php_substr(datestamp, 6, 2)
        if year == 0 or month == 0 or day == 0:
            return False
        # end if
        if month > 12:
            return False
        # end if
        if day > 31:
            return False
        # end if
        if day > 30 and month == 4 or month == 6 or month == 9 or month == 11:
            return False
        # end if
        if day > 29 and month == 2:
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
    def id3v2headerlength(self, majorversion=None):
        
        return 6 if majorversion == 2 else 10
    # end def id3v2headerlength
    #// 
    #// @param string $frame_name
    #// 
    #// @return string|false
    #//
    @classmethod
    def id3v22itunesbrokenframename(self, frame_name=None):
        
        ID3v22_iTunes_BrokenFrames = Array({"BUF": "RBUF", "CNT": "PCNT", "COM": "COMM", "CRA": "AENC", "EQU": "EQUA", "ETC": "ETCO", "GEO": "GEOB", "IPL": "IPLS", "LNK": "LINK", "MCI": "MCDI", "MLL": "MLLT", "PIC": "APIC", "POP": "POPM", "REV": "RVRB", "RVA": "RVAD", "SLT": "SYLT", "STC": "SYTC", "TAL": "TALB", "TBP": "TBPM", "TCM": "TCOM", "TCO": "TCON", "TCP": "TCMP", "TCR": "TCOP", "TDA": "TDAT", "TDY": "TDLY", "TEN": "TENC", "TFT": "TFLT", "TIM": "TIME", "TKE": "TKEY", "TLA": "TLAN", "TLE": "TLEN", "TMT": "TMED", "TOA": "TOPE", "TOF": "TOFN", "TOL": "TOLY", "TOR": "TORY", "TOT": "TOAL", "TP1": "TPE1", "TP2": "TPE2", "TP3": "TPE3", "TP4": "TPE4", "TPA": "TPOS", "TPB": "TPUB", "TRC": "TSRC", "TRD": "TRDA", "TRK": "TRCK", "TS2": "TSO2", "TSA": "TSOA", "TSC": "TSOC", "TSI": "TSIZ", "TSP": "TSOP", "TSS": "TSSE", "TST": "TSOT", "TT1": "TIT1", "TT2": "TIT2", "TT3": "TIT3", "TXT": "TEXT", "TXX": "TXXX", "TYE": "TYER", "UFI": "UFID", "ULT": "USLT", "WAF": "WOAF", "WAR": "WOAR", "WAS": "WOAS", "WCM": "WCOM", "WCP": "WCOP", "WPB": "WPUB", "WXX": "WXXX"})
        if php_strlen(frame_name) == 4:
            if php_substr(frame_name, 3, 1) == " " or php_substr(frame_name, 3, 1) == " ":
                if (php_isset(lambda : ID3v22_iTunes_BrokenFrames[php_substr(frame_name, 0, 3)])):
                    return ID3v22_iTunes_BrokenFrames[php_substr(frame_name, 0, 3)]
                # end if
            # end if
        # end if
        return False
    # end def id3v22itunesbrokenframename
# end class getid3_id3v2
