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
#// module.audio-video.asf.php
#// module for analyzing ASF, WMA and WMV files
#// dependencies: module.audio-video.riff.php
#// 
#//
getid3_lib.includedependency(GETID3_INCLUDEPATH + "module.audio-video.riff.php", __FILE__, True)
class getid3_asf(getid3_handler):
    #// 
    #// @param getID3 $getid3
    #//
    def __init__(self, getid3=None):
        
        super().__init__(getid3)
        #// extends getid3_handler::__construct()
        #// initialize all GUID constants
        GUIDarray = self.knownguids()
        for GUIDname,hexstringvalue in GUIDarray:
            if (not php_defined(GUIDname)):
                php_define(GUIDname, self.guidtobytestring(hexstringvalue))
            # end if
        # end for
    # end def __init__
    #// 
    #// @return bool
    #//
    def analyze(self):
        
        info = self.getid3.info
        #// Shortcuts
        thisfile_audio = info["audio"]
        thisfile_video = info["video"]
        info["asf"] = Array()
        thisfile_asf = info["asf"]
        thisfile_asf["comments"] = Array()
        thisfile_asf_comments = thisfile_asf["comments"]
        thisfile_asf["header_object"] = Array()
        thisfile_asf_headerobject = thisfile_asf["header_object"]
        #// ASF structure:
        #// Header Object [required]
        #// File Properties Object [required]   (global file attributes)
        #// Stream Properties Object [required] (defines media stream & characteristics)
        #// Header Extension Object [required]  (additional functionality)
        #// Content Description Object          (bibliographic information)
        #// Script Command Object               (commands for during playback)
        #// Marker Object                       (named jumped points within the file)
        #// Data Object [required]
        #// Data Packets
        #// Index Object
        #// Header Object: (mandatory, one only)
        #// Field Name                   Field Type   Size (bits)
        #// Object ID                    GUID         128             // GUID for header object - GETID3_ASF_Header_Object
        #// Object Size                  QWORD        64              // size of header object, including 30 bytes of Header Object header
        #// Number of Header Objects     DWORD        32              // number of objects in header object
        #// Reserved1                    BYTE         8               // hardcoded: 0x01
        #// Reserved2                    BYTE         8               // hardcoded: 0x02
        info["fileformat"] = "asf"
        self.fseek(info["avdataoffset"])
        HeaderObjectData = self.fread(30)
        thisfile_asf_headerobject["objectid"] = php_substr(HeaderObjectData, 0, 16)
        thisfile_asf_headerobject["objectid_guid"] = self.bytestringtoguid(thisfile_asf_headerobject["objectid"])
        if thisfile_asf_headerobject["objectid"] != GETID3_ASF_Header_Object:
            info["fileformat"] = None
            info["asf"] = None
            return self.error("ASF header GUID {" + self.bytestringtoguid(thisfile_asf_headerobject["objectid"]) + "} does not match expected \"GETID3_ASF_Header_Object\" GUID {" + self.bytestringtoguid(GETID3_ASF_Header_Object) + "}")
        # end if
        thisfile_asf_headerobject["objectsize"] = getid3_lib.littleendian2int(php_substr(HeaderObjectData, 16, 8))
        thisfile_asf_headerobject["headerobjects"] = getid3_lib.littleendian2int(php_substr(HeaderObjectData, 24, 4))
        thisfile_asf_headerobject["reserved1"] = getid3_lib.littleendian2int(php_substr(HeaderObjectData, 28, 1))
        thisfile_asf_headerobject["reserved2"] = getid3_lib.littleendian2int(php_substr(HeaderObjectData, 29, 1))
        NextObjectOffset = self.ftell()
        ASFHeaderData = self.fread(thisfile_asf_headerobject["objectsize"] - 30)
        offset = 0
        thisfile_asf_streambitratepropertiesobject = Array()
        thisfile_asf_codeclistobject = Array()
        HeaderObjectsCounter = 0
        while HeaderObjectsCounter < thisfile_asf_headerobject["headerobjects"]:
            
            NextObjectGUID = php_substr(ASFHeaderData, offset, 16)
            offset += 16
            NextObjectGUIDtext = self.bytestringtoguid(NextObjectGUID)
            NextObjectSize = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 8))
            offset += 8
            for case in Switch(NextObjectGUID):
                if case(GETID3_ASF_File_Properties_Object):
                    #// File Properties Object: (mandatory, one only)
                    #// Field Name                   Field Type   Size (bits)
                    #// Object ID                    GUID         128             // GUID for file properties object - GETID3_ASF_File_Properties_Object
                    #// Object Size                  QWORD        64              // size of file properties object, including 104 bytes of File Properties Object header
                    #// File ID                      GUID         128             // unique ID - identical to File ID in Data Object
                    #// File Size                    QWORD        64              // entire file in bytes. Invalid if Broadcast Flag == 1
                    #// Creation Date                QWORD        64              // date & time of file creation. Maybe invalid if Broadcast Flag == 1
                    #// Data Packets Count           QWORD        64              // number of data packets in Data Object. Invalid if Broadcast Flag == 1
                    #// Play Duration                QWORD        64              // playtime, in 100-nanosecond units. Invalid if Broadcast Flag == 1
                    #// Send Duration                QWORD        64              // time needed to send file, in 100-nanosecond units. Players can ignore this value. Invalid if Broadcast Flag == 1
                    #// Preroll                      QWORD        64              // time to buffer data before starting to play file, in 1-millisecond units. If <> 0, PlayDuration and PresentationTime have been offset by this amount
                    #// Flags                        DWORD        32
                    #// Broadcast Flag             bits         1  (0x01)       // file is currently being written, some header values are invalid
                    #// Seekable Flag              bits         1  (0x02)       // is file seekable
                    #// Reserved                   bits         30 (0xFFFFFFFC) // reserved - set to zero
                    #// Minimum Data Packet Size     DWORD        32              // in bytes. should be same as Maximum Data Packet Size. Invalid if Broadcast Flag == 1
                    #// Maximum Data Packet Size     DWORD        32              // in bytes. should be same as Minimum Data Packet Size. Invalid if Broadcast Flag == 1
                    #// Maximum Bitrate              DWORD        32              // maximum instantaneous bitrate in bits per second for entire file, including all data streams and ASF overhead
                    #// shortcut
                    thisfile_asf["file_properties_object"] = Array()
                    thisfile_asf_filepropertiesobject = thisfile_asf["file_properties_object"]
                    thisfile_asf_filepropertiesobject["offset"] = NextObjectOffset + offset
                    thisfile_asf_filepropertiesobject["objectid"] = NextObjectGUID
                    thisfile_asf_filepropertiesobject["objectid_guid"] = NextObjectGUIDtext
                    thisfile_asf_filepropertiesobject["objectsize"] = NextObjectSize
                    thisfile_asf_filepropertiesobject["fileid"] = php_substr(ASFHeaderData, offset, 16)
                    offset += 16
                    thisfile_asf_filepropertiesobject["fileid_guid"] = self.bytestringtoguid(thisfile_asf_filepropertiesobject["fileid"])
                    thisfile_asf_filepropertiesobject["filesize"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 8))
                    offset += 8
                    thisfile_asf_filepropertiesobject["creation_date"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 8))
                    thisfile_asf_filepropertiesobject["creation_date_unix"] = self.filetimetounixtime(thisfile_asf_filepropertiesobject["creation_date"])
                    offset += 8
                    thisfile_asf_filepropertiesobject["data_packets"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 8))
                    offset += 8
                    thisfile_asf_filepropertiesobject["play_duration"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 8))
                    offset += 8
                    thisfile_asf_filepropertiesobject["send_duration"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 8))
                    offset += 8
                    thisfile_asf_filepropertiesobject["preroll"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 8))
                    offset += 8
                    thisfile_asf_filepropertiesobject["flags_raw"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 4))
                    offset += 4
                    thisfile_asf_filepropertiesobject["flags"]["broadcast"] = php_bool(thisfile_asf_filepropertiesobject["flags_raw"] & 1)
                    thisfile_asf_filepropertiesobject["flags"]["seekable"] = php_bool(thisfile_asf_filepropertiesobject["flags_raw"] & 2)
                    thisfile_asf_filepropertiesobject["min_packet_size"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 4))
                    offset += 4
                    thisfile_asf_filepropertiesobject["max_packet_size"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 4))
                    offset += 4
                    thisfile_asf_filepropertiesobject["max_bitrate"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 4))
                    offset += 4
                    if thisfile_asf_filepropertiesobject["flags"]["broadcast"]:
                        thisfile_asf_filepropertiesobject["filesize"] = None
                        thisfile_asf_filepropertiesobject["data_packets"] = None
                        thisfile_asf_filepropertiesobject["play_duration"] = None
                        thisfile_asf_filepropertiesobject["send_duration"] = None
                        thisfile_asf_filepropertiesobject["min_packet_size"] = None
                        thisfile_asf_filepropertiesobject["max_packet_size"] = None
                    else:
                        #// broadcast flag NOT set, perform calculations
                        info["playtime_seconds"] = thisfile_asf_filepropertiesobject["play_duration"] / 10000000 - thisfile_asf_filepropertiesobject["preroll"] / 1000
                        #// $info['bitrate'] = $thisfile_asf_filepropertiesobject['max_bitrate'];
                        info["bitrate"] = thisfile_asf_filepropertiesobject["filesize"] if (php_isset(lambda : thisfile_asf_filepropertiesobject["filesize"])) else info["filesize"] * 8 / info["playtime_seconds"]
                    # end if
                    break
                # end if
                if case(GETID3_ASF_Stream_Properties_Object):
                    #// Stream Properties Object: (mandatory, one per media stream)
                    #// Field Name                   Field Type   Size (bits)
                    #// Object ID                    GUID         128             // GUID for stream properties object - GETID3_ASF_Stream_Properties_Object
                    #// Object Size                  QWORD        64              // size of stream properties object, including 78 bytes of Stream Properties Object header
                    #// Stream Type                  GUID         128             // GETID3_ASF_Audio_Media, GETID3_ASF_Video_Media or GETID3_ASF_Command_Media
                    #// Error Correction Type        GUID         128             // GETID3_ASF_Audio_Spread for audio-only streams, GETID3_ASF_No_Error_Correction for other stream types
                    #// Time Offset                  QWORD        64              // 100-nanosecond units. typically zero. added to all timestamps of samples in the stream
                    #// Type-Specific Data Length    DWORD        32              // number of bytes for Type-Specific Data field
                    #// Error Correction Data Length DWORD        32              // number of bytes for Error Correction Data field
                    #// Flags                        WORD         16
                    #// Stream Number              bits         7 (0x007F)      // number of this stream.  1 <= valid <= 127
                    #// Reserved                   bits         8 (0x7F80)      // reserved - set to zero
                    #// Encrypted Content Flag     bits         1 (0x8000)      // stream contents encrypted if set
                    #// Reserved                     DWORD        32              // reserved - set to zero
                    #// Type-Specific Data           BYTESTREAM   variable        // type-specific format data, depending on value of Stream Type
                    #// Error Correction Data        BYTESTREAM   variable        // error-correction-specific format data, depending on value of Error Correct Type
                    #// There is one GETID3_ASF_Stream_Properties_Object for each stream (audio, video) but the
                    #// stream number isn't known until halfway through decoding the structure, hence it
                    #// it is decoded to a temporary variable and then stuck in the appropriate index later
                    StreamPropertiesObjectData["offset"] = NextObjectOffset + offset
                    StreamPropertiesObjectData["objectid"] = NextObjectGUID
                    StreamPropertiesObjectData["objectid_guid"] = NextObjectGUIDtext
                    StreamPropertiesObjectData["objectsize"] = NextObjectSize
                    StreamPropertiesObjectData["stream_type"] = php_substr(ASFHeaderData, offset, 16)
                    offset += 16
                    StreamPropertiesObjectData["stream_type_guid"] = self.bytestringtoguid(StreamPropertiesObjectData["stream_type"])
                    StreamPropertiesObjectData["error_correct_type"] = php_substr(ASFHeaderData, offset, 16)
                    offset += 16
                    StreamPropertiesObjectData["error_correct_guid"] = self.bytestringtoguid(StreamPropertiesObjectData["error_correct_type"])
                    StreamPropertiesObjectData["time_offset"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 8))
                    offset += 8
                    StreamPropertiesObjectData["type_data_length"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 4))
                    offset += 4
                    StreamPropertiesObjectData["error_data_length"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 4))
                    offset += 4
                    StreamPropertiesObjectData["flags_raw"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 2))
                    offset += 2
                    StreamPropertiesObjectStreamNumber = StreamPropertiesObjectData["flags_raw"] & 127
                    StreamPropertiesObjectData["flags"]["encrypted"] = php_bool(StreamPropertiesObjectData["flags_raw"] & 32768)
                    offset += 4
                    #// reserved - DWORD
                    StreamPropertiesObjectData["type_specific_data"] = php_substr(ASFHeaderData, offset, StreamPropertiesObjectData["type_data_length"])
                    offset += StreamPropertiesObjectData["type_data_length"]
                    StreamPropertiesObjectData["error_correct_data"] = php_substr(ASFHeaderData, offset, StreamPropertiesObjectData["error_data_length"])
                    offset += StreamPropertiesObjectData["error_data_length"]
                    for case in Switch(StreamPropertiesObjectData["stream_type"]):
                        if case(GETID3_ASF_Audio_Media):
                            thisfile_audio["dataformat"] = thisfile_audio["dataformat"] if (not php_empty(lambda : thisfile_audio["dataformat"])) else "asf"
                            thisfile_audio["bitrate_mode"] = thisfile_audio["bitrate_mode"] if (not php_empty(lambda : thisfile_audio["bitrate_mode"])) else "cbr"
                            audiodata = getid3_riff.parsewaveformatex(php_substr(StreamPropertiesObjectData["type_specific_data"], 0, 16))
                            audiodata["raw"] = None
                            thisfile_audio = getid3_lib.array_merge_noclobber(audiodata, thisfile_audio)
                            break
                        # end if
                        if case(GETID3_ASF_Video_Media):
                            thisfile_video["dataformat"] = thisfile_video["dataformat"] if (not php_empty(lambda : thisfile_video["dataformat"])) else "asf"
                            thisfile_video["bitrate_mode"] = thisfile_video["bitrate_mode"] if (not php_empty(lambda : thisfile_video["bitrate_mode"])) else "cbr"
                            break
                        # end if
                        if case(GETID3_ASF_Command_Media):
                            pass
                        # end if
                        if case():
                            break
                        # end if
                    # end for
                    thisfile_asf["stream_properties_object"][StreamPropertiesObjectStreamNumber] = StreamPropertiesObjectData
                    StreamPropertiesObjectData = None
                    break
                # end if
                if case(GETID3_ASF_Header_Extension_Object):
                    #// Header Extension Object: (mandatory, one only)
                    #// Field Name                   Field Type   Size (bits)
                    #// Object ID                    GUID         128             // GUID for Header Extension object - GETID3_ASF_Header_Extension_Object
                    #// Object Size                  QWORD        64              // size of Header Extension object, including 46 bytes of Header Extension Object header
                    #// Reserved Field 1             GUID         128             // hardcoded: GETID3_ASF_Reserved_1
                    #// Reserved Field 2             WORD         16              // hardcoded: 0x00000006
                    #// Header Extension Data Size   DWORD        32              // in bytes. valid: 0, or > 24. equals object size minus 46
                    #// Header Extension Data        BYTESTREAM   variable        // array of zero or more extended header objects
                    #// shortcut
                    thisfile_asf["header_extension_object"] = Array()
                    thisfile_asf_headerextensionobject = thisfile_asf["header_extension_object"]
                    thisfile_asf_headerextensionobject["offset"] = NextObjectOffset + offset
                    thisfile_asf_headerextensionobject["objectid"] = NextObjectGUID
                    thisfile_asf_headerextensionobject["objectid_guid"] = NextObjectGUIDtext
                    thisfile_asf_headerextensionobject["objectsize"] = NextObjectSize
                    thisfile_asf_headerextensionobject["reserved_1"] = php_substr(ASFHeaderData, offset, 16)
                    offset += 16
                    thisfile_asf_headerextensionobject["reserved_1_guid"] = self.bytestringtoguid(thisfile_asf_headerextensionobject["reserved_1"])
                    if thisfile_asf_headerextensionobject["reserved_1"] != GETID3_ASF_Reserved_1:
                        self.warning("header_extension_object.reserved_1 GUID (" + self.bytestringtoguid(thisfile_asf_headerextensionobject["reserved_1"]) + ") does not match expected \"GETID3_ASF_Reserved_1\" GUID (" + self.bytestringtoguid(GETID3_ASF_Reserved_1) + ")")
                        break
                    # end if
                    thisfile_asf_headerextensionobject["reserved_2"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 2))
                    offset += 2
                    if thisfile_asf_headerextensionobject["reserved_2"] != 6:
                        self.warning("header_extension_object.reserved_2 (" + getid3_lib.printhexbytes(thisfile_asf_headerextensionobject["reserved_2"]) + ") does not match expected value of \"6\"")
                        break
                    # end if
                    thisfile_asf_headerextensionobject["extension_data_size"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 4))
                    offset += 4
                    thisfile_asf_headerextensionobject["extension_data"] = php_substr(ASFHeaderData, offset, thisfile_asf_headerextensionobject["extension_data_size"])
                    unhandled_sections = 0
                    thisfile_asf_headerextensionobject["extension_data_parsed"] = self.headerextensionobjectdataparse(thisfile_asf_headerextensionobject["extension_data"], unhandled_sections)
                    if unhandled_sections == 0:
                        thisfile_asf_headerextensionobject["extension_data"] = None
                    # end if
                    offset += thisfile_asf_headerextensionobject["extension_data_size"]
                    break
                # end if
                if case(GETID3_ASF_Codec_List_Object):
                    #// Codec List Object: (optional, one only)
                    #// Field Name                   Field Type   Size (bits)
                    #// Object ID                    GUID         128             // GUID for Codec List object - GETID3_ASF_Codec_List_Object
                    #// Object Size                  QWORD        64              // size of Codec List object, including 44 bytes of Codec List Object header
                    #// Reserved                     GUID         128             // hardcoded: 86D15241-311D-11D0-A3A4-00A0C90348F6
                    #// Codec Entries Count          DWORD        32              // number of entries in Codec Entries array
                    #// Codec Entries                array of:    variable
                    #// Type                       WORD         16              // 0x0001 = Video Codec, 0x0002 = Audio Codec, 0xFFFF = Unknown Codec
                    #// Codec Name Length          WORD         16              // number of Unicode characters stored in the Codec Name field
                    #// Codec Name                 WCHAR        variable        // array of Unicode characters - name of codec used to create the content
                    #// Codec Description Length   WORD         16              // number of Unicode characters stored in the Codec Description field
                    #// Codec Description          WCHAR        variable        // array of Unicode characters - description of format used to create the content
                    #// Codec Information Length   WORD         16              // number of Unicode characters stored in the Codec Information field
                    #// Codec Information          BYTESTREAM   variable        // opaque array of information bytes about the codec used to create the content
                    #// shortcut
                    thisfile_asf["codec_list_object"] = Array()
                    thisfile_asf_codeclistobject = thisfile_asf["codec_list_object"]
                    thisfile_asf_codeclistobject["offset"] = NextObjectOffset + offset
                    thisfile_asf_codeclistobject["objectid"] = NextObjectGUID
                    thisfile_asf_codeclistobject["objectid_guid"] = NextObjectGUIDtext
                    thisfile_asf_codeclistobject["objectsize"] = NextObjectSize
                    thisfile_asf_codeclistobject["reserved"] = php_substr(ASFHeaderData, offset, 16)
                    offset += 16
                    thisfile_asf_codeclistobject["reserved_guid"] = self.bytestringtoguid(thisfile_asf_codeclistobject["reserved"])
                    if thisfile_asf_codeclistobject["reserved"] != self.guidtobytestring("86D15241-311D-11D0-A3A4-00A0C90348F6"):
                        self.warning("codec_list_object.reserved GUID {" + self.bytestringtoguid(thisfile_asf_codeclistobject["reserved"]) + "} does not match expected \"GETID3_ASF_Reserved_1\" GUID {86D15241-311D-11D0-A3A4-00A0C90348F6}")
                        break
                    # end if
                    thisfile_asf_codeclistobject["codec_entries_count"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 4))
                    offset += 4
                    CodecEntryCounter = 0
                    while CodecEntryCounter < thisfile_asf_codeclistobject["codec_entries_count"]:
                        
                        #// shortcut
                        thisfile_asf_codeclistobject["codec_entries"][CodecEntryCounter] = Array()
                        thisfile_asf_codeclistobject_codecentries_current = thisfile_asf_codeclistobject["codec_entries"][CodecEntryCounter]
                        thisfile_asf_codeclistobject_codecentries_current["type_raw"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 2))
                        offset += 2
                        thisfile_asf_codeclistobject_codecentries_current["type"] = self.codeclistobjecttypelookup(thisfile_asf_codeclistobject_codecentries_current["type_raw"])
                        CodecNameLength = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 2)) * 2
                        #// 2 bytes per character
                        offset += 2
                        thisfile_asf_codeclistobject_codecentries_current["name"] = php_substr(ASFHeaderData, offset, CodecNameLength)
                        offset += CodecNameLength
                        CodecDescriptionLength = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 2)) * 2
                        #// 2 bytes per character
                        offset += 2
                        thisfile_asf_codeclistobject_codecentries_current["description"] = php_substr(ASFHeaderData, offset, CodecDescriptionLength)
                        offset += CodecDescriptionLength
                        CodecInformationLength = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 2))
                        offset += 2
                        thisfile_asf_codeclistobject_codecentries_current["information"] = php_substr(ASFHeaderData, offset, CodecInformationLength)
                        offset += CodecInformationLength
                        if thisfile_asf_codeclistobject_codecentries_current["type_raw"] == 2:
                            #// audio codec
                            if php_strpos(thisfile_asf_codeclistobject_codecentries_current["description"], ",") == False:
                                self.warning("[asf][codec_list_object][codec_entries][" + CodecEntryCounter + "][description] expected to contain comma-separated list of parameters: \"" + thisfile_asf_codeclistobject_codecentries_current["description"] + "\"")
                            else:
                                AudioCodecBitrate, AudioCodecFrequency, AudioCodecChannels = php_explode(",", self.trimconvert(thisfile_asf_codeclistobject_codecentries_current["description"]))
                                thisfile_audio["codec"] = self.trimconvert(thisfile_asf_codeclistobject_codecentries_current["name"])
                                if (not (php_isset(lambda : thisfile_audio["bitrate"]))) and php_strstr(AudioCodecBitrate, "kbps"):
                                    thisfile_audio["bitrate"] = php_int(php_trim(php_str_replace("kbps", "", AudioCodecBitrate)) * 1000)
                                # end if
                                #// if (!isset($thisfile_video['bitrate']) && isset($thisfile_audio['bitrate']) && isset($thisfile_asf['file_properties_object']['max_bitrate']) && ($thisfile_asf_codeclistobject['codec_entries_count'] > 1)) {
                                if php_empty(lambda : thisfile_video["bitrate"]) and (not php_empty(lambda : thisfile_audio["bitrate"])) and (not php_empty(lambda : info["bitrate"])):
                                    #// $thisfile_video['bitrate'] = $thisfile_asf['file_properties_object']['max_bitrate'] - $thisfile_audio['bitrate'];
                                    thisfile_video["bitrate"] = info["bitrate"] - thisfile_audio["bitrate"]
                                # end if
                                AudioCodecFrequency = php_int(php_trim(php_str_replace("kHz", "", AudioCodecFrequency)))
                                for case in Switch(AudioCodecFrequency):
                                    if case(8):
                                        pass
                                    # end if
                                    if case(8000):
                                        thisfile_audio["sample_rate"] = 8000
                                        break
                                    # end if
                                    if case(11):
                                        pass
                                    # end if
                                    if case(11025):
                                        thisfile_audio["sample_rate"] = 11025
                                        break
                                    # end if
                                    if case(12):
                                        pass
                                    # end if
                                    if case(12000):
                                        thisfile_audio["sample_rate"] = 12000
                                        break
                                    # end if
                                    if case(16):
                                        pass
                                    # end if
                                    if case(16000):
                                        thisfile_audio["sample_rate"] = 16000
                                        break
                                    # end if
                                    if case(22):
                                        pass
                                    # end if
                                    if case(22050):
                                        thisfile_audio["sample_rate"] = 22050
                                        break
                                    # end if
                                    if case(24):
                                        pass
                                    # end if
                                    if case(24000):
                                        thisfile_audio["sample_rate"] = 24000
                                        break
                                    # end if
                                    if case(32):
                                        pass
                                    # end if
                                    if case(32000):
                                        thisfile_audio["sample_rate"] = 32000
                                        break
                                    # end if
                                    if case(44):
                                        pass
                                    # end if
                                    if case(441000):
                                        thisfile_audio["sample_rate"] = 44100
                                        break
                                    # end if
                                    if case(48):
                                        pass
                                    # end if
                                    if case(48000):
                                        thisfile_audio["sample_rate"] = 48000
                                        break
                                    # end if
                                    if case():
                                        self.warning("unknown frequency: \"" + AudioCodecFrequency + "\" (" + self.trimconvert(thisfile_asf_codeclistobject_codecentries_current["description"]) + ")")
                                        break
                                    # end if
                                # end for
                                if (not (php_isset(lambda : thisfile_audio["channels"]))):
                                    if php_strstr(AudioCodecChannels, "stereo"):
                                        thisfile_audio["channels"] = 2
                                    elif php_strstr(AudioCodecChannels, "mono"):
                                        thisfile_audio["channels"] = 1
                                    # end if
                                # end if
                            # end if
                        # end if
                        CodecEntryCounter += 1
                    # end while
                    break
                # end if
                if case(GETID3_ASF_Script_Command_Object):
                    #// Script Command Object: (optional, one only)
                    #// Field Name                   Field Type   Size (bits)
                    #// Object ID                    GUID         128             // GUID for Script Command object - GETID3_ASF_Script_Command_Object
                    #// Object Size                  QWORD        64              // size of Script Command object, including 44 bytes of Script Command Object header
                    #// Reserved                     GUID         128             // hardcoded: 4B1ACBE3-100B-11D0-A39B-00A0C90348F6
                    #// Commands Count               WORD         16              // number of Commands structures in the Script Commands Objects
                    #// Command Types Count          WORD         16              // number of Command Types structures in the Script Commands Objects
                    #// Command Types                array of:    variable
                    #// Command Type Name Length   WORD         16              // number of Unicode characters for Command Type Name
                    #// Command Type Name          WCHAR        variable        // array of Unicode characters - name of a type of command
                    #// Commands                     array of:    variable
                    #// Presentation Time          DWORD        32              // presentation time of that command, in milliseconds
                    #// Type Index                 WORD         16              // type of this command, as a zero-based index into the array of Command Types of this object
                    #// Command Name Length        WORD         16              // number of Unicode characters for Command Name
                    #// Command Name               WCHAR        variable        // array of Unicode characters - name of this command
                    #// shortcut
                    thisfile_asf["script_command_object"] = Array()
                    thisfile_asf_scriptcommandobject = thisfile_asf["script_command_object"]
                    thisfile_asf_scriptcommandobject["offset"] = NextObjectOffset + offset
                    thisfile_asf_scriptcommandobject["objectid"] = NextObjectGUID
                    thisfile_asf_scriptcommandobject["objectid_guid"] = NextObjectGUIDtext
                    thisfile_asf_scriptcommandobject["objectsize"] = NextObjectSize
                    thisfile_asf_scriptcommandobject["reserved"] = php_substr(ASFHeaderData, offset, 16)
                    offset += 16
                    thisfile_asf_scriptcommandobject["reserved_guid"] = self.bytestringtoguid(thisfile_asf_scriptcommandobject["reserved"])
                    if thisfile_asf_scriptcommandobject["reserved"] != self.guidtobytestring("4B1ACBE3-100B-11D0-A39B-00A0C90348F6"):
                        self.warning("script_command_object.reserved GUID {" + self.bytestringtoguid(thisfile_asf_scriptcommandobject["reserved"]) + "} does not match expected \"GETID3_ASF_Reserved_1\" GUID {4B1ACBE3-100B-11D0-A39B-00A0C90348F6}")
                        break
                    # end if
                    thisfile_asf_scriptcommandobject["commands_count"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 2))
                    offset += 2
                    thisfile_asf_scriptcommandobject["command_types_count"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 2))
                    offset += 2
                    CommandTypesCounter = 0
                    while CommandTypesCounter < thisfile_asf_scriptcommandobject["command_types_count"]:
                        
                        CommandTypeNameLength = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 2)) * 2
                        #// 2 bytes per character
                        offset += 2
                        thisfile_asf_scriptcommandobject["command_types"][CommandTypesCounter]["name"] = php_substr(ASFHeaderData, offset, CommandTypeNameLength)
                        offset += CommandTypeNameLength
                        CommandTypesCounter += 1
                    # end while
                    CommandsCounter = 0
                    while CommandsCounter < thisfile_asf_scriptcommandobject["commands_count"]:
                        
                        thisfile_asf_scriptcommandobject["commands"][CommandsCounter]["presentation_time"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 4))
                        offset += 4
                        thisfile_asf_scriptcommandobject["commands"][CommandsCounter]["type_index"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 2))
                        offset += 2
                        CommandTypeNameLength = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 2)) * 2
                        #// 2 bytes per character
                        offset += 2
                        thisfile_asf_scriptcommandobject["commands"][CommandsCounter]["name"] = php_substr(ASFHeaderData, offset, CommandTypeNameLength)
                        offset += CommandTypeNameLength
                        CommandsCounter += 1
                    # end while
                    break
                # end if
                if case(GETID3_ASF_Marker_Object):
                    #// Marker Object: (optional, one only)
                    #// Field Name                   Field Type   Size (bits)
                    #// Object ID                    GUID         128             // GUID for Marker object - GETID3_ASF_Marker_Object
                    #// Object Size                  QWORD        64              // size of Marker object, including 48 bytes of Marker Object header
                    #// Reserved                     GUID         128             // hardcoded: 4CFEDB20-75F6-11CF-9C0F-00A0C90349CB
                    #// Markers Count                DWORD        32              // number of Marker structures in Marker Object
                    #// Reserved                     WORD         16              // hardcoded: 0x0000
                    #// Name Length                  WORD         16              // number of bytes in the Name field
                    #// Name                         WCHAR        variable        // name of the Marker Object
                    #// Markers                      array of:    variable
                    #// Offset                     QWORD        64              // byte offset into Data Object
                    #// Presentation Time          QWORD        64              // in 100-nanosecond units
                    #// Entry Length               WORD         16              // length in bytes of (Send Time + Flags + Marker Description Length + Marker Description + Padding)
                    #// Send Time                  DWORD        32              // in milliseconds
                    #// Flags                      DWORD        32              // hardcoded: 0x00000000
                    #// Marker Description Length  DWORD        32              // number of bytes in Marker Description field
                    #// Marker Description         WCHAR        variable        // array of Unicode characters - description of marker entry
                    #// Padding                    BYTESTREAM   variable        // optional padding bytes
                    #// shortcut
                    thisfile_asf["marker_object"] = Array()
                    thisfile_asf_markerobject = thisfile_asf["marker_object"]
                    thisfile_asf_markerobject["offset"] = NextObjectOffset + offset
                    thisfile_asf_markerobject["objectid"] = NextObjectGUID
                    thisfile_asf_markerobject["objectid_guid"] = NextObjectGUIDtext
                    thisfile_asf_markerobject["objectsize"] = NextObjectSize
                    thisfile_asf_markerobject["reserved"] = php_substr(ASFHeaderData, offset, 16)
                    offset += 16
                    thisfile_asf_markerobject["reserved_guid"] = self.bytestringtoguid(thisfile_asf_markerobject["reserved"])
                    if thisfile_asf_markerobject["reserved"] != self.guidtobytestring("4CFEDB20-75F6-11CF-9C0F-00A0C90349CB"):
                        self.warning("marker_object.reserved GUID {" + self.bytestringtoguid(thisfile_asf_markerobject["reserved_1"]) + "} does not match expected \"GETID3_ASF_Reserved_1\" GUID {4CFEDB20-75F6-11CF-9C0F-00A0C90349CB}")
                        break
                    # end if
                    thisfile_asf_markerobject["markers_count"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 4))
                    offset += 4
                    thisfile_asf_markerobject["reserved_2"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 2))
                    offset += 2
                    if thisfile_asf_markerobject["reserved_2"] != 0:
                        self.warning("marker_object.reserved_2 (" + getid3_lib.printhexbytes(thisfile_asf_markerobject["reserved_2"]) + ") does not match expected value of \"0\"")
                        break
                    # end if
                    thisfile_asf_markerobject["name_length"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 2))
                    offset += 2
                    thisfile_asf_markerobject["name"] = php_substr(ASFHeaderData, offset, thisfile_asf_markerobject["name_length"])
                    offset += thisfile_asf_markerobject["name_length"]
                    MarkersCounter = 0
                    while MarkersCounter < thisfile_asf_markerobject["markers_count"]:
                        
                        thisfile_asf_markerobject["markers"][MarkersCounter]["offset"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 8))
                        offset += 8
                        thisfile_asf_markerobject["markers"][MarkersCounter]["presentation_time"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 8))
                        offset += 8
                        thisfile_asf_markerobject["markers"][MarkersCounter]["entry_length"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 2))
                        offset += 2
                        thisfile_asf_markerobject["markers"][MarkersCounter]["send_time"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 4))
                        offset += 4
                        thisfile_asf_markerobject["markers"][MarkersCounter]["flags"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 4))
                        offset += 4
                        thisfile_asf_markerobject["markers"][MarkersCounter]["marker_description_length"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 4))
                        offset += 4
                        thisfile_asf_markerobject["markers"][MarkersCounter]["marker_description"] = php_substr(ASFHeaderData, offset, thisfile_asf_markerobject["markers"][MarkersCounter]["marker_description_length"])
                        offset += thisfile_asf_markerobject["markers"][MarkersCounter]["marker_description_length"]
                        PaddingLength = thisfile_asf_markerobject["markers"][MarkersCounter]["entry_length"] - 4 - 4 - 4 - thisfile_asf_markerobject["markers"][MarkersCounter]["marker_description_length"]
                        if PaddingLength > 0:
                            thisfile_asf_markerobject["markers"][MarkersCounter]["padding"] = php_substr(ASFHeaderData, offset, PaddingLength)
                            offset += PaddingLength
                        # end if
                        MarkersCounter += 1
                    # end while
                    break
                # end if
                if case(GETID3_ASF_Bitrate_Mutual_Exclusion_Object):
                    #// Bitrate Mutual Exclusion Object: (optional)
                    #// Field Name                   Field Type   Size (bits)
                    #// Object ID                    GUID         128             // GUID for Bitrate Mutual Exclusion object - GETID3_ASF_Bitrate_Mutual_Exclusion_Object
                    #// Object Size                  QWORD        64              // size of Bitrate Mutual Exclusion object, including 42 bytes of Bitrate Mutual Exclusion Object header
                    #// Exlusion Type                GUID         128             // nature of mutual exclusion relationship. one of: (GETID3_ASF_Mutex_Bitrate, GETID3_ASF_Mutex_Unknown)
                    #// Stream Numbers Count         WORD         16              // number of video streams
                    #// Stream Numbers               WORD         variable        // array of mutually exclusive video stream numbers. 1 <= valid <= 127
                    #// shortcut
                    thisfile_asf["bitrate_mutual_exclusion_object"] = Array()
                    thisfile_asf_bitratemutualexclusionobject = thisfile_asf["bitrate_mutual_exclusion_object"]
                    thisfile_asf_bitratemutualexclusionobject["offset"] = NextObjectOffset + offset
                    thisfile_asf_bitratemutualexclusionobject["objectid"] = NextObjectGUID
                    thisfile_asf_bitratemutualexclusionobject["objectid_guid"] = NextObjectGUIDtext
                    thisfile_asf_bitratemutualexclusionobject["objectsize"] = NextObjectSize
                    thisfile_asf_bitratemutualexclusionobject["reserved"] = php_substr(ASFHeaderData, offset, 16)
                    thisfile_asf_bitratemutualexclusionobject["reserved_guid"] = self.bytestringtoguid(thisfile_asf_bitratemutualexclusionobject["reserved"])
                    offset += 16
                    if thisfile_asf_bitratemutualexclusionobject["reserved"] != GETID3_ASF_Mutex_Bitrate and thisfile_asf_bitratemutualexclusionobject["reserved"] != GETID3_ASF_Mutex_Unknown:
                        self.warning("bitrate_mutual_exclusion_object.reserved GUID {" + self.bytestringtoguid(thisfile_asf_bitratemutualexclusionobject["reserved"]) + "} does not match expected \"GETID3_ASF_Mutex_Bitrate\" GUID {" + self.bytestringtoguid(GETID3_ASF_Mutex_Bitrate) + "} or  \"GETID3_ASF_Mutex_Unknown\" GUID {" + self.bytestringtoguid(GETID3_ASF_Mutex_Unknown) + "}")
                        break
                    # end if
                    thisfile_asf_bitratemutualexclusionobject["stream_numbers_count"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 2))
                    offset += 2
                    StreamNumberCounter = 0
                    while StreamNumberCounter < thisfile_asf_bitratemutualexclusionobject["stream_numbers_count"]:
                        
                        thisfile_asf_bitratemutualexclusionobject["stream_numbers"][StreamNumberCounter] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 2))
                        offset += 2
                        StreamNumberCounter += 1
                    # end while
                    break
                # end if
                if case(GETID3_ASF_Error_Correction_Object):
                    #// Error Correction Object: (optional, one only)
                    #// Field Name                   Field Type   Size (bits)
                    #// Object ID                    GUID         128             // GUID for Error Correction object - GETID3_ASF_Error_Correction_Object
                    #// Object Size                  QWORD        64              // size of Error Correction object, including 44 bytes of Error Correction Object header
                    #// Error Correction Type        GUID         128             // type of error correction. one of: (GETID3_ASF_No_Error_Correction, GETID3_ASF_Audio_Spread)
                    #// Error Correction Data Length DWORD        32              // number of bytes in Error Correction Data field
                    #// Error Correction Data        BYTESTREAM   variable        // structure depends on value of Error Correction Type field
                    #// shortcut
                    thisfile_asf["error_correction_object"] = Array()
                    thisfile_asf_errorcorrectionobject = thisfile_asf["error_correction_object"]
                    thisfile_asf_errorcorrectionobject["offset"] = NextObjectOffset + offset
                    thisfile_asf_errorcorrectionobject["objectid"] = NextObjectGUID
                    thisfile_asf_errorcorrectionobject["objectid_guid"] = NextObjectGUIDtext
                    thisfile_asf_errorcorrectionobject["objectsize"] = NextObjectSize
                    thisfile_asf_errorcorrectionobject["error_correction_type"] = php_substr(ASFHeaderData, offset, 16)
                    offset += 16
                    thisfile_asf_errorcorrectionobject["error_correction_guid"] = self.bytestringtoguid(thisfile_asf_errorcorrectionobject["error_correction_type"])
                    thisfile_asf_errorcorrectionobject["error_correction_data_length"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 4))
                    offset += 4
                    for case in Switch(thisfile_asf_errorcorrectionobject["error_correction_type"]):
                        if case(GETID3_ASF_No_Error_Correction):
                            #// should be no data, but just in case there is, skip to the end of the field
                            offset += thisfile_asf_errorcorrectionobject["error_correction_data_length"]
                            break
                        # end if
                        if case(GETID3_ASF_Audio_Spread):
                            #// Field Name                   Field Type   Size (bits)
                            #// Span                         BYTE         8               // number of packets over which audio will be spread.
                            #// Virtual Packet Length        WORD         16              // size of largest audio payload found in audio stream
                            #// Virtual Chunk Length         WORD         16              // size of largest audio payload found in audio stream
                            #// Silence Data Length          WORD         16              // number of bytes in Silence Data field
                            #// Silence Data                 BYTESTREAM   variable        // hardcoded: 0x00 * (Silence Data Length) bytes
                            thisfile_asf_errorcorrectionobject["span"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 1))
                            offset += 1
                            thisfile_asf_errorcorrectionobject["virtual_packet_length"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 2))
                            offset += 2
                            thisfile_asf_errorcorrectionobject["virtual_chunk_length"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 2))
                            offset += 2
                            thisfile_asf_errorcorrectionobject["silence_data_length"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 2))
                            offset += 2
                            thisfile_asf_errorcorrectionobject["silence_data"] = php_substr(ASFHeaderData, offset, thisfile_asf_errorcorrectionobject["silence_data_length"])
                            offset += thisfile_asf_errorcorrectionobject["silence_data_length"]
                            break
                        # end if
                        if case():
                            self.warning("error_correction_object.error_correction_type GUID {" + self.bytestringtoguid(thisfile_asf_errorcorrectionobject["reserved"]) + "} does not match expected \"GETID3_ASF_No_Error_Correction\" GUID {" + self.bytestringtoguid(GETID3_ASF_No_Error_Correction) + "} or  \"GETID3_ASF_Audio_Spread\" GUID {" + self.bytestringtoguid(GETID3_ASF_Audio_Spread) + "}")
                            break
                        # end if
                    # end for
                    break
                # end if
                if case(GETID3_ASF_Content_Description_Object):
                    #// Content Description Object: (optional, one only)
                    #// Field Name                   Field Type   Size (bits)
                    #// Object ID                    GUID         128             // GUID for Content Description object - GETID3_ASF_Content_Description_Object
                    #// Object Size                  QWORD        64              // size of Content Description object, including 34 bytes of Content Description Object header
                    #// Title Length                 WORD         16              // number of bytes in Title field
                    #// Author Length                WORD         16              // number of bytes in Author field
                    #// Copyright Length             WORD         16              // number of bytes in Copyright field
                    #// Description Length           WORD         16              // number of bytes in Description field
                    #// Rating Length                WORD         16              // number of bytes in Rating field
                    #// Title                        WCHAR        16              // array of Unicode characters - Title
                    #// Author                       WCHAR        16              // array of Unicode characters - Author
                    #// Copyright                    WCHAR        16              // array of Unicode characters - Copyright
                    #// Description                  WCHAR        16              // array of Unicode characters - Description
                    #// Rating                       WCHAR        16              // array of Unicode characters - Rating
                    #// shortcut
                    thisfile_asf["content_description_object"] = Array()
                    thisfile_asf_contentdescriptionobject = thisfile_asf["content_description_object"]
                    thisfile_asf_contentdescriptionobject["offset"] = NextObjectOffset + offset
                    thisfile_asf_contentdescriptionobject["objectid"] = NextObjectGUID
                    thisfile_asf_contentdescriptionobject["objectid_guid"] = NextObjectGUIDtext
                    thisfile_asf_contentdescriptionobject["objectsize"] = NextObjectSize
                    thisfile_asf_contentdescriptionobject["title_length"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 2))
                    offset += 2
                    thisfile_asf_contentdescriptionobject["author_length"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 2))
                    offset += 2
                    thisfile_asf_contentdescriptionobject["copyright_length"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 2))
                    offset += 2
                    thisfile_asf_contentdescriptionobject["description_length"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 2))
                    offset += 2
                    thisfile_asf_contentdescriptionobject["rating_length"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 2))
                    offset += 2
                    thisfile_asf_contentdescriptionobject["title"] = php_substr(ASFHeaderData, offset, thisfile_asf_contentdescriptionobject["title_length"])
                    offset += thisfile_asf_contentdescriptionobject["title_length"]
                    thisfile_asf_contentdescriptionobject["author"] = php_substr(ASFHeaderData, offset, thisfile_asf_contentdescriptionobject["author_length"])
                    offset += thisfile_asf_contentdescriptionobject["author_length"]
                    thisfile_asf_contentdescriptionobject["copyright"] = php_substr(ASFHeaderData, offset, thisfile_asf_contentdescriptionobject["copyright_length"])
                    offset += thisfile_asf_contentdescriptionobject["copyright_length"]
                    thisfile_asf_contentdescriptionobject["description"] = php_substr(ASFHeaderData, offset, thisfile_asf_contentdescriptionobject["description_length"])
                    offset += thisfile_asf_contentdescriptionobject["description_length"]
                    thisfile_asf_contentdescriptionobject["rating"] = php_substr(ASFHeaderData, offset, thisfile_asf_contentdescriptionobject["rating_length"])
                    offset += thisfile_asf_contentdescriptionobject["rating_length"]
                    ASFcommentKeysToCopy = Array({"title": "title", "author": "artist", "copyright": "copyright", "description": "comment", "rating": "rating"})
                    for keytocopyfrom,keytocopyto in ASFcommentKeysToCopy:
                        if (not php_empty(lambda : thisfile_asf_contentdescriptionobject[keytocopyfrom])):
                            thisfile_asf_comments[keytocopyto][-1] = self.trimterm(thisfile_asf_contentdescriptionobject[keytocopyfrom])
                        # end if
                    # end for
                    break
                # end if
                if case(GETID3_ASF_Extended_Content_Description_Object):
                    #// Extended Content Description Object: (optional, one only)
                    #// Field Name                   Field Type   Size (bits)
                    #// Object ID                    GUID         128             // GUID for Extended Content Description object - GETID3_ASF_Extended_Content_Description_Object
                    #// Object Size                  QWORD        64              // size of ExtendedContent Description object, including 26 bytes of Extended Content Description Object header
                    #// Content Descriptors Count    WORD         16              // number of entries in Content Descriptors list
                    #// Content Descriptors          array of:    variable
                    #// Descriptor Name Length     WORD         16              // size in bytes of Descriptor Name field
                    #// Descriptor Name            WCHAR        variable        // array of Unicode characters - Descriptor Name
                    #// Descriptor Value Data Type WORD         16              // Lookup array:
                    #// 0x0000 = Unicode String (variable length)
                    #// 0x0001 = BYTE array     (variable length)
                    #// 0x0002 = BOOL           (DWORD, 32 bits)
                    #// 0x0003 = DWORD          (DWORD, 32 bits)
                    #// 0x0004 = QWORD          (QWORD, 64 bits)
                    #// 0x0005 = WORD           (WORD,  16 bits)
                    #// Descriptor Value Length    WORD         16              // number of bytes stored in Descriptor Value field
                    #// Descriptor Value           variable     variable        // value for Content Descriptor
                    #// shortcut
                    thisfile_asf["extended_content_description_object"] = Array()
                    thisfile_asf_extendedcontentdescriptionobject = thisfile_asf["extended_content_description_object"]
                    thisfile_asf_extendedcontentdescriptionobject["offset"] = NextObjectOffset + offset
                    thisfile_asf_extendedcontentdescriptionobject["objectid"] = NextObjectGUID
                    thisfile_asf_extendedcontentdescriptionobject["objectid_guid"] = NextObjectGUIDtext
                    thisfile_asf_extendedcontentdescriptionobject["objectsize"] = NextObjectSize
                    thisfile_asf_extendedcontentdescriptionobject["content_descriptors_count"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 2))
                    offset += 2
                    ExtendedContentDescriptorsCounter = 0
                    while ExtendedContentDescriptorsCounter < thisfile_asf_extendedcontentdescriptionobject["content_descriptors_count"]:
                        
                        #// shortcut
                        thisfile_asf_extendedcontentdescriptionobject["content_descriptors"][ExtendedContentDescriptorsCounter] = Array()
                        thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current = thisfile_asf_extendedcontentdescriptionobject["content_descriptors"][ExtendedContentDescriptorsCounter]
                        thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["base_offset"] = offset + 30
                        thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["name_length"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 2))
                        offset += 2
                        thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["name"] = php_substr(ASFHeaderData, offset, thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["name_length"])
                        offset += thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["name_length"]
                        thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["value_type"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 2))
                        offset += 2
                        thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["value_length"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 2))
                        offset += 2
                        thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["value"] = php_substr(ASFHeaderData, offset, thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["value_length"])
                        offset += thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["value_length"]
                        for case in Switch(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["value_type"]):
                            if case(0):
                                break
                            # end if
                            if case(1):
                                break
                            # end if
                            if case(2):
                                #// BOOL
                                thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["value"] = php_bool(getid3_lib.littleendian2int(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["value"]))
                                break
                            # end if
                            if case(3):
                                pass
                            # end if
                            if case(4):
                                pass
                            # end if
                            if case(5):
                                #// WORD
                                thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["value"] = getid3_lib.littleendian2int(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["value"])
                                break
                            # end if
                            if case():
                                self.warning("extended_content_description.content_descriptors." + ExtendedContentDescriptorsCounter + ".value_type is invalid (" + thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["value_type"] + ")")
                                break
                            # end if
                        # end for
                        for case in Switch(self.trimconvert(php_strtolower(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["name"]))):
                            if case("wm/albumartist"):
                                pass
                            # end if
                            if case("artist"):
                                #// Note: not 'artist', that comes from 'author' tag
                                thisfile_asf_comments["albumartist"] = Array(self.trimterm(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["value"]))
                                break
                            # end if
                            if case("wm/albumtitle"):
                                pass
                            # end if
                            if case("album"):
                                thisfile_asf_comments["album"] = Array(self.trimterm(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["value"]))
                                break
                            # end if
                            if case("wm/genre"):
                                pass
                            # end if
                            if case("genre"):
                                thisfile_asf_comments["genre"] = Array(self.trimterm(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["value"]))
                                break
                            # end if
                            if case("wm/partofset"):
                                thisfile_asf_comments["partofset"] = Array(self.trimterm(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["value"]))
                                break
                            # end if
                            if case("wm/tracknumber"):
                                pass
                            # end if
                            if case("tracknumber"):
                                #// be careful casting to int: casting unicode strings to int gives unexpected results (stops parsing at first non-numeric character)
                                thisfile_asf_comments["track_number"] = Array(self.trimterm(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["value"]))
                                for key,value in thisfile_asf_comments["track_number"]:
                                    if php_preg_match("/^[0-9\\x00]+$/", value):
                                        thisfile_asf_comments["track_number"][key] = php_intval(php_str_replace(" ", "", value))
                                    # end if
                                # end for
                                break
                            # end if
                            if case("wm/track"):
                                if php_empty(lambda : thisfile_asf_comments["track_number"]):
                                    thisfile_asf_comments["track_number"] = Array(1 + self.trimconvert(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["value"]))
                                # end if
                                break
                            # end if
                            if case("wm/year"):
                                pass
                            # end if
                            if case("year"):
                                pass
                            # end if
                            if case("date"):
                                thisfile_asf_comments["year"] = Array(self.trimterm(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["value"]))
                                break
                            # end if
                            if case("wm/lyrics"):
                                pass
                            # end if
                            if case("lyrics"):
                                thisfile_asf_comments["lyrics"] = Array(self.trimterm(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["value"]))
                                break
                            # end if
                            if case("isvbr"):
                                if thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["value"]:
                                    thisfile_audio["bitrate_mode"] = "vbr"
                                    thisfile_video["bitrate_mode"] = "vbr"
                                # end if
                                break
                            # end if
                            if case("id3"):
                                self.getid3.include_module("tag.id3v2")
                                getid3_id3v2 = php_new_class("getid3_id3v2", lambda : getid3_id3v2(self.getid3))
                                getid3_id3v2.analyzestring(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["value"])
                                getid3_id3v2 = None
                                if thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["value_length"] > 1024:
                                    thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["value"] = "<value too large to display>"
                                # end if
                                break
                            # end if
                            if case("wm/encodingtime"):
                                thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["encoding_time_unix"] = self.filetimetounixtime(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["value"])
                                thisfile_asf_comments["encoding_time_unix"] = Array(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["encoding_time_unix"])
                                break
                            # end if
                            if case("wm/picture"):
                                WMpicture = self.asf_wmpicture(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["value"])
                                for key,value in WMpicture:
                                    thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current[key] = value
                                # end for
                                WMpicture = None
                                break
                            # end if
                            if case():
                                for case in Switch(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["value_type"]):
                                    if case(0):
                                        #// Unicode string
                                        if php_substr(self.trimconvert(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["name"]), 0, 3) == "WM/":
                                            thisfile_asf_comments[php_str_replace("wm/", "", php_strtolower(self.trimconvert(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["name"])))] = Array(self.trimterm(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current["value"]))
                                        # end if
                                        break
                                    # end if
                                    if case(1):
                                        break
                                    # end if
                                # end for
                                break
                            # end if
                        # end for
                        ExtendedContentDescriptorsCounter += 1
                    # end while
                    break
                # end if
                if case(GETID3_ASF_Stream_Bitrate_Properties_Object):
                    #// Stream Bitrate Properties Object: (optional, one only)
                    #// Field Name                   Field Type   Size (bits)
                    #// Object ID                    GUID         128             // GUID for Stream Bitrate Properties object - GETID3_ASF_Stream_Bitrate_Properties_Object
                    #// Object Size                  QWORD        64              // size of Extended Content Description object, including 26 bytes of Stream Bitrate Properties Object header
                    #// Bitrate Records Count        WORD         16              // number of records in Bitrate Records
                    #// Bitrate Records              array of:    variable
                    #// Flags                      WORD         16
                    #// Stream Number            bits         7  (0x007F)     // number of this stream
                    #// Reserved                 bits         9  (0xFF80)     // hardcoded: 0
                    #// Average Bitrate            DWORD        32              // in bits per second
                    #// shortcut
                    thisfile_asf["stream_bitrate_properties_object"] = Array()
                    thisfile_asf_streambitratepropertiesobject = thisfile_asf["stream_bitrate_properties_object"]
                    thisfile_asf_streambitratepropertiesobject["offset"] = NextObjectOffset + offset
                    thisfile_asf_streambitratepropertiesobject["objectid"] = NextObjectGUID
                    thisfile_asf_streambitratepropertiesobject["objectid_guid"] = NextObjectGUIDtext
                    thisfile_asf_streambitratepropertiesobject["objectsize"] = NextObjectSize
                    thisfile_asf_streambitratepropertiesobject["bitrate_records_count"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 2))
                    offset += 2
                    BitrateRecordsCounter = 0
                    while BitrateRecordsCounter < thisfile_asf_streambitratepropertiesobject["bitrate_records_count"]:
                        
                        thisfile_asf_streambitratepropertiesobject["bitrate_records"][BitrateRecordsCounter]["flags_raw"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 2))
                        offset += 2
                        thisfile_asf_streambitratepropertiesobject["bitrate_records"][BitrateRecordsCounter]["flags"]["stream_number"] = thisfile_asf_streambitratepropertiesobject["bitrate_records"][BitrateRecordsCounter]["flags_raw"] & 127
                        thisfile_asf_streambitratepropertiesobject["bitrate_records"][BitrateRecordsCounter]["bitrate"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData, offset, 4))
                        offset += 4
                        BitrateRecordsCounter += 1
                    # end while
                    break
                # end if
                if case(GETID3_ASF_Padding_Object):
                    #// Padding Object: (optional)
                    #// Field Name                   Field Type   Size (bits)
                    #// Object ID                    GUID         128             // GUID for Padding object - GETID3_ASF_Padding_Object
                    #// Object Size                  QWORD        64              // size of Padding object, including 24 bytes of ASF Padding Object header
                    #// Padding Data                 BYTESTREAM   variable        // ignore
                    #// shortcut
                    thisfile_asf["padding_object"] = Array()
                    thisfile_asf_paddingobject = thisfile_asf["padding_object"]
                    thisfile_asf_paddingobject["offset"] = NextObjectOffset + offset
                    thisfile_asf_paddingobject["objectid"] = NextObjectGUID
                    thisfile_asf_paddingobject["objectid_guid"] = NextObjectGUIDtext
                    thisfile_asf_paddingobject["objectsize"] = NextObjectSize
                    thisfile_asf_paddingobject["padding_length"] = thisfile_asf_paddingobject["objectsize"] - 16 - 8
                    thisfile_asf_paddingobject["padding"] = php_substr(ASFHeaderData, offset, thisfile_asf_paddingobject["padding_length"])
                    offset += NextObjectSize - 16 - 8
                    break
                # end if
                if case(GETID3_ASF_Extended_Content_Encryption_Object):
                    pass
                # end if
                if case(GETID3_ASF_Content_Encryption_Object):
                    #// WMA DRM - just ignore
                    offset += NextObjectSize - 16 - 8
                    break
                # end if
                if case():
                    #// Implementations shall ignore any standard or non-standard object that they do not know how to handle.
                    if self.guidname(NextObjectGUIDtext):
                        self.warning("unhandled GUID \"" + self.guidname(NextObjectGUIDtext) + "\" {" + NextObjectGUIDtext + "} in ASF header at offset " + offset - 16 - 8)
                    else:
                        self.warning("unknown GUID {" + NextObjectGUIDtext + "} in ASF header at offset " + offset - 16 - 8)
                    # end if
                    offset += NextObjectSize - 16 - 8
                    break
                # end if
            # end for
            HeaderObjectsCounter += 1
        # end while
        if (php_isset(lambda : thisfile_asf_streambitratepropertiesobject["bitrate_records_count"])):
            ASFbitrateAudio = 0
            ASFbitrateVideo = 0
            BitrateRecordsCounter = 0
            while BitrateRecordsCounter < thisfile_asf_streambitratepropertiesobject["bitrate_records_count"]:
                
                if (php_isset(lambda : thisfile_asf_codeclistobject["codec_entries"][BitrateRecordsCounter])):
                    for case in Switch(thisfile_asf_codeclistobject["codec_entries"][BitrateRecordsCounter]["type_raw"]):
                        if case(1):
                            ASFbitrateVideo += thisfile_asf_streambitratepropertiesobject["bitrate_records"][BitrateRecordsCounter]["bitrate"]
                            break
                        # end if
                        if case(2):
                            ASFbitrateAudio += thisfile_asf_streambitratepropertiesobject["bitrate_records"][BitrateRecordsCounter]["bitrate"]
                            break
                        # end if
                        if case():
                            break
                        # end if
                    # end for
                # end if
                BitrateRecordsCounter += 1
            # end while
            if ASFbitrateAudio > 0:
                thisfile_audio["bitrate"] = ASFbitrateAudio
            # end if
            if ASFbitrateVideo > 0:
                thisfile_video["bitrate"] = ASFbitrateVideo
            # end if
        # end if
        if (php_isset(lambda : thisfile_asf["stream_properties_object"])) and php_is_array(thisfile_asf["stream_properties_object"]):
            thisfile_audio["bitrate"] = 0
            thisfile_video["bitrate"] = 0
            for streamnumber,streamdata in thisfile_asf["stream_properties_object"]:
                for case in Switch(streamdata["stream_type"]):
                    if case(GETID3_ASF_Audio_Media):
                        #// Field Name                   Field Type   Size (bits)
                        #// Codec ID / Format Tag        WORD         16              // unique ID of audio codec - defined as wFormatTag field of WAVEFORMATEX structure
                        #// Number of Channels           WORD         16              // number of channels of audio - defined as nChannels field of WAVEFORMATEX structure
                        #// Samples Per Second           DWORD        32              // in Hertz - defined as nSamplesPerSec field of WAVEFORMATEX structure
                        #// Average number of Bytes/sec  DWORD        32              // bytes/sec of audio stream  - defined as nAvgBytesPerSec field of WAVEFORMATEX structure
                        #// Block Alignment              WORD         16              // block size in bytes of audio codec - defined as nBlockAlign field of WAVEFORMATEX structure
                        #// Bits per sample              WORD         16              // bits per sample of mono data. set to zero for variable bitrate codecs. defined as wBitsPerSample field of WAVEFORMATEX structure
                        #// Codec Specific Data Size     WORD         16              // size in bytes of Codec Specific Data buffer - defined as cbSize field of WAVEFORMATEX structure
                        #// Codec Specific Data          BYTESTREAM   variable        // array of codec-specific data bytes
                        #// shortcut
                        thisfile_asf["audio_media"][streamnumber] = Array()
                        thisfile_asf_audiomedia_currentstream = thisfile_asf["audio_media"][streamnumber]
                        audiomediaoffset = 0
                        thisfile_asf_audiomedia_currentstream = getid3_riff.parsewaveformatex(php_substr(streamdata["type_specific_data"], audiomediaoffset, 16))
                        audiomediaoffset += 16
                        thisfile_audio["lossless"] = False
                        for case in Switch(thisfile_asf_audiomedia_currentstream["raw"]["wFormatTag"]):
                            if case(1):
                                pass
                            # end if
                            if case(355):
                                #// WMA9 Lossless
                                thisfile_audio["lossless"] = True
                                break
                            # end if
                        # end for
                        if (not php_empty(lambda : thisfile_asf["stream_bitrate_properties_object"]["bitrate_records"])):
                            for dummy,dataarray in thisfile_asf["stream_bitrate_properties_object"]["bitrate_records"]:
                                if (php_isset(lambda : dataarray["flags"]["stream_number"])) and dataarray["flags"]["stream_number"] == streamnumber:
                                    thisfile_asf_audiomedia_currentstream["bitrate"] = dataarray["bitrate"]
                                    thisfile_audio["bitrate"] += dataarray["bitrate"]
                                    break
                                # end if
                            # end for
                        else:
                            if (not php_empty(lambda : thisfile_asf_audiomedia_currentstream["bytes_sec"])):
                                thisfile_audio["bitrate"] += thisfile_asf_audiomedia_currentstream["bytes_sec"] * 8
                            elif (not php_empty(lambda : thisfile_asf_audiomedia_currentstream["bitrate"])):
                                thisfile_audio["bitrate"] += thisfile_asf_audiomedia_currentstream["bitrate"]
                            # end if
                        # end if
                        thisfile_audio["streams"][streamnumber] = thisfile_asf_audiomedia_currentstream
                        thisfile_audio["streams"][streamnumber]["wformattag"] = thisfile_asf_audiomedia_currentstream["raw"]["wFormatTag"]
                        thisfile_audio["streams"][streamnumber]["lossless"] = thisfile_audio["lossless"]
                        thisfile_audio["streams"][streamnumber]["bitrate"] = thisfile_audio["bitrate"]
                        thisfile_audio["streams"][streamnumber]["dataformat"] = "wma"
                        thisfile_audio["streams"][streamnumber]["raw"] = None
                        thisfile_asf_audiomedia_currentstream["codec_data_size"] = getid3_lib.littleendian2int(php_substr(streamdata["type_specific_data"], audiomediaoffset, 2))
                        audiomediaoffset += 2
                        thisfile_asf_audiomedia_currentstream["codec_data"] = php_substr(streamdata["type_specific_data"], audiomediaoffset, thisfile_asf_audiomedia_currentstream["codec_data_size"])
                        audiomediaoffset += thisfile_asf_audiomedia_currentstream["codec_data_size"]
                        break
                    # end if
                    if case(GETID3_ASF_Video_Media):
                        #// Field Name                   Field Type   Size (bits)
                        #// Encoded Image Width          DWORD        32              // width of image in pixels
                        #// Encoded Image Height         DWORD        32              // height of image in pixels
                        #// Reserved Flags               BYTE         8               // hardcoded: 0x02
                        #// Format Data Size             WORD         16              // size of Format Data field in bytes
                        #// Format Data                  array of:    variable
                        #// Format Data Size           DWORD        32              // number of bytes in Format Data field, in bytes - defined as biSize field of BITMAPINFOHEADER structure
                        #// Image Width                LONG         32              // width of encoded image in pixels - defined as biWidth field of BITMAPINFOHEADER structure
                        #// Image Height               LONG         32              // height of encoded image in pixels - defined as biHeight field of BITMAPINFOHEADER structure
                        #// Reserved                   WORD         16              // hardcoded: 0x0001 - defined as biPlanes field of BITMAPINFOHEADER structure
                        #// Bits Per Pixel Count       WORD         16              // bits per pixel - defined as biBitCount field of BITMAPINFOHEADER structure
                        #// Compression ID             FOURCC       32              // fourcc of video codec - defined as biCompression field of BITMAPINFOHEADER structure
                        #// Image Size                 DWORD        32              // image size in bytes - defined as biSizeImage field of BITMAPINFOHEADER structure
                        #// Horizontal Pixels / Meter  DWORD        32              // horizontal resolution of target device in pixels per meter - defined as biXPelsPerMeter field of BITMAPINFOHEADER structure
                        #// Vertical Pixels / Meter    DWORD        32              // vertical resolution of target device in pixels per meter - defined as biYPelsPerMeter field of BITMAPINFOHEADER structure
                        #// Colors Used Count          DWORD        32              // number of color indexes in the color table that are actually used - defined as biClrUsed field of BITMAPINFOHEADER structure
                        #// Important Colors Count     DWORD        32              // number of color index required for displaying bitmap. if zero, all colors are required. defined as biClrImportant field of BITMAPINFOHEADER structure
                        #// Codec Specific Data        BYTESTREAM   variable        // array of codec-specific data bytes
                        #// shortcut
                        thisfile_asf["video_media"][streamnumber] = Array()
                        thisfile_asf_videomedia_currentstream = thisfile_asf["video_media"][streamnumber]
                        videomediaoffset = 0
                        thisfile_asf_videomedia_currentstream["image_width"] = getid3_lib.littleendian2int(php_substr(streamdata["type_specific_data"], videomediaoffset, 4))
                        videomediaoffset += 4
                        thisfile_asf_videomedia_currentstream["image_height"] = getid3_lib.littleendian2int(php_substr(streamdata["type_specific_data"], videomediaoffset, 4))
                        videomediaoffset += 4
                        thisfile_asf_videomedia_currentstream["flags"] = getid3_lib.littleendian2int(php_substr(streamdata["type_specific_data"], videomediaoffset, 1))
                        videomediaoffset += 1
                        thisfile_asf_videomedia_currentstream["format_data_size"] = getid3_lib.littleendian2int(php_substr(streamdata["type_specific_data"], videomediaoffset, 2))
                        videomediaoffset += 2
                        thisfile_asf_videomedia_currentstream["format_data"]["format_data_size"] = getid3_lib.littleendian2int(php_substr(streamdata["type_specific_data"], videomediaoffset, 4))
                        videomediaoffset += 4
                        thisfile_asf_videomedia_currentstream["format_data"]["image_width"] = getid3_lib.littleendian2int(php_substr(streamdata["type_specific_data"], videomediaoffset, 4))
                        videomediaoffset += 4
                        thisfile_asf_videomedia_currentstream["format_data"]["image_height"] = getid3_lib.littleendian2int(php_substr(streamdata["type_specific_data"], videomediaoffset, 4))
                        videomediaoffset += 4
                        thisfile_asf_videomedia_currentstream["format_data"]["reserved"] = getid3_lib.littleendian2int(php_substr(streamdata["type_specific_data"], videomediaoffset, 2))
                        videomediaoffset += 2
                        thisfile_asf_videomedia_currentstream["format_data"]["bits_per_pixel"] = getid3_lib.littleendian2int(php_substr(streamdata["type_specific_data"], videomediaoffset, 2))
                        videomediaoffset += 2
                        thisfile_asf_videomedia_currentstream["format_data"]["codec_fourcc"] = php_substr(streamdata["type_specific_data"], videomediaoffset, 4)
                        videomediaoffset += 4
                        thisfile_asf_videomedia_currentstream["format_data"]["image_size"] = getid3_lib.littleendian2int(php_substr(streamdata["type_specific_data"], videomediaoffset, 4))
                        videomediaoffset += 4
                        thisfile_asf_videomedia_currentstream["format_data"]["horizontal_pels"] = getid3_lib.littleendian2int(php_substr(streamdata["type_specific_data"], videomediaoffset, 4))
                        videomediaoffset += 4
                        thisfile_asf_videomedia_currentstream["format_data"]["vertical_pels"] = getid3_lib.littleendian2int(php_substr(streamdata["type_specific_data"], videomediaoffset, 4))
                        videomediaoffset += 4
                        thisfile_asf_videomedia_currentstream["format_data"]["colors_used"] = getid3_lib.littleendian2int(php_substr(streamdata["type_specific_data"], videomediaoffset, 4))
                        videomediaoffset += 4
                        thisfile_asf_videomedia_currentstream["format_data"]["colors_important"] = getid3_lib.littleendian2int(php_substr(streamdata["type_specific_data"], videomediaoffset, 4))
                        videomediaoffset += 4
                        thisfile_asf_videomedia_currentstream["format_data"]["codec_data"] = php_substr(streamdata["type_specific_data"], videomediaoffset)
                        if (not php_empty(lambda : thisfile_asf["stream_bitrate_properties_object"]["bitrate_records"])):
                            for dummy,dataarray in thisfile_asf["stream_bitrate_properties_object"]["bitrate_records"]:
                                if (php_isset(lambda : dataarray["flags"]["stream_number"])) and dataarray["flags"]["stream_number"] == streamnumber:
                                    thisfile_asf_videomedia_currentstream["bitrate"] = dataarray["bitrate"]
                                    thisfile_video["streams"][streamnumber]["bitrate"] = dataarray["bitrate"]
                                    thisfile_video["bitrate"] += dataarray["bitrate"]
                                    break
                                # end if
                            # end for
                        # end if
                        thisfile_asf_videomedia_currentstream["format_data"]["codec"] = getid3_riff.fourcclookup(thisfile_asf_videomedia_currentstream["format_data"]["codec_fourcc"])
                        thisfile_video["streams"][streamnumber]["fourcc"] = thisfile_asf_videomedia_currentstream["format_data"]["codec_fourcc"]
                        thisfile_video["streams"][streamnumber]["codec"] = thisfile_asf_videomedia_currentstream["format_data"]["codec"]
                        thisfile_video["streams"][streamnumber]["resolution_x"] = thisfile_asf_videomedia_currentstream["image_width"]
                        thisfile_video["streams"][streamnumber]["resolution_y"] = thisfile_asf_videomedia_currentstream["image_height"]
                        thisfile_video["streams"][streamnumber]["bits_per_sample"] = thisfile_asf_videomedia_currentstream["format_data"]["bits_per_pixel"]
                        break
                    # end if
                    if case():
                        break
                    # end if
                # end for
            # end for
        # end if
        while True:
            
            if not (self.ftell() < info["avdataend"]):
                break
            # end if
            NextObjectDataHeader = self.fread(24)
            offset = 0
            NextObjectGUID = php_substr(NextObjectDataHeader, 0, 16)
            offset += 16
            NextObjectGUIDtext = self.bytestringtoguid(NextObjectGUID)
            NextObjectSize = getid3_lib.littleendian2int(php_substr(NextObjectDataHeader, offset, 8))
            offset += 8
            for case in Switch(NextObjectGUID):
                if case(GETID3_ASF_Data_Object):
                    #// Data Object: (mandatory, one only)
                    #// Field Name                       Field Type   Size (bits)
                    #// Object ID                        GUID         128             // GUID for Data object - GETID3_ASF_Data_Object
                    #// Object Size                      QWORD        64              // size of Data object, including 50 bytes of Data Object header. may be 0 if FilePropertiesObject.BroadcastFlag == 1
                    #// File ID                          GUID         128             // unique identifier. identical to File ID field in Header Object
                    #// Total Data Packets               QWORD        64              // number of Data Packet entries in Data Object. invalid if FilePropertiesObject.BroadcastFlag == 1
                    #// Reserved                         WORD         16              // hardcoded: 0x0101
                    #// shortcut
                    thisfile_asf["data_object"] = Array()
                    thisfile_asf_dataobject = thisfile_asf["data_object"]
                    DataObjectData = NextObjectDataHeader + self.fread(50 - 24)
                    offset = 24
                    thisfile_asf_dataobject["objectid"] = NextObjectGUID
                    thisfile_asf_dataobject["objectid_guid"] = NextObjectGUIDtext
                    thisfile_asf_dataobject["objectsize"] = NextObjectSize
                    thisfile_asf_dataobject["fileid"] = php_substr(DataObjectData, offset, 16)
                    offset += 16
                    thisfile_asf_dataobject["fileid_guid"] = self.bytestringtoguid(thisfile_asf_dataobject["fileid"])
                    thisfile_asf_dataobject["total_data_packets"] = getid3_lib.littleendian2int(php_substr(DataObjectData, offset, 8))
                    offset += 8
                    thisfile_asf_dataobject["reserved"] = getid3_lib.littleendian2int(php_substr(DataObjectData, offset, 2))
                    offset += 2
                    if thisfile_asf_dataobject["reserved"] != 257:
                        self.warning("data_object.reserved (" + getid3_lib.printhexbytes(thisfile_asf_dataobject["reserved"]) + ") does not match expected value of \"0x0101\"")
                        break
                    # end if
                    #// Data Packets                     array of:    variable
                    #// Error Correction Flags         BYTE         8
                    #// Error Correction Data Length bits         4               // if Error Correction Length Type == 00, size of Error Correction Data in bytes, else hardcoded: 0000
                    #// Opaque Data Present          bits         1
                    #// Error Correction Length Type bits         2               // number of bits for size of the error correction data. hardcoded: 00
                    #// Error Correction Present     bits         1               // If set, use Opaque Data Packet structure, else use Payload structure
                    #// Error Correction Data
                    info["avdataoffset"] = self.ftell()
                    self.fseek(thisfile_asf_dataobject["objectsize"] - 50, SEEK_CUR)
                    #// skip actual audio/video data
                    info["avdataend"] = self.ftell()
                    break
                # end if
                if case(GETID3_ASF_Simple_Index_Object):
                    #// Simple Index Object: (optional, recommended, one per video stream)
                    #// Field Name                       Field Type   Size (bits)
                    #// Object ID                        GUID         128             // GUID for Simple Index object - GETID3_ASF_Data_Object
                    #// Object Size                      QWORD        64              // size of Simple Index object, including 56 bytes of Simple Index Object header
                    #// File ID                          GUID         128             // unique identifier. may be zero or identical to File ID field in Data Object and Header Object
                    #// Index Entry Time Interval        QWORD        64              // interval between index entries in 100-nanosecond units
                    #// Maximum Packet Count             DWORD        32              // maximum packet count for all index entries
                    #// Index Entries Count              DWORD        32              // number of Index Entries structures
                    #// Index Entries                    array of:    variable
                    #// Packet Number                  DWORD        32              // number of the Data Packet associated with this index entry
                    #// Packet Count                   WORD         16              // number of Data Packets to sent at this index entry
                    #// shortcut
                    thisfile_asf["simple_index_object"] = Array()
                    thisfile_asf_simpleindexobject = thisfile_asf["simple_index_object"]
                    SimpleIndexObjectData = NextObjectDataHeader + self.fread(56 - 24)
                    offset = 24
                    thisfile_asf_simpleindexobject["objectid"] = NextObjectGUID
                    thisfile_asf_simpleindexobject["objectid_guid"] = NextObjectGUIDtext
                    thisfile_asf_simpleindexobject["objectsize"] = NextObjectSize
                    thisfile_asf_simpleindexobject["fileid"] = php_substr(SimpleIndexObjectData, offset, 16)
                    offset += 16
                    thisfile_asf_simpleindexobject["fileid_guid"] = self.bytestringtoguid(thisfile_asf_simpleindexobject["fileid"])
                    thisfile_asf_simpleindexobject["index_entry_time_interval"] = getid3_lib.littleendian2int(php_substr(SimpleIndexObjectData, offset, 8))
                    offset += 8
                    thisfile_asf_simpleindexobject["maximum_packet_count"] = getid3_lib.littleendian2int(php_substr(SimpleIndexObjectData, offset, 4))
                    offset += 4
                    thisfile_asf_simpleindexobject["index_entries_count"] = getid3_lib.littleendian2int(php_substr(SimpleIndexObjectData, offset, 4))
                    offset += 4
                    IndexEntriesData = SimpleIndexObjectData + self.fread(6 * thisfile_asf_simpleindexobject["index_entries_count"])
                    IndexEntriesCounter = 0
                    while IndexEntriesCounter < thisfile_asf_simpleindexobject["index_entries_count"]:
                        
                        thisfile_asf_simpleindexobject["index_entries"][IndexEntriesCounter]["packet_number"] = getid3_lib.littleendian2int(php_substr(IndexEntriesData, offset, 4))
                        offset += 4
                        thisfile_asf_simpleindexobject["index_entries"][IndexEntriesCounter]["packet_count"] = getid3_lib.littleendian2int(php_substr(IndexEntriesData, offset, 4))
                        offset += 2
                        IndexEntriesCounter += 1
                    # end while
                    break
                # end if
                if case(GETID3_ASF_Index_Object):
                    #// 6.2 ASF top-level Index Object (optional but recommended when appropriate, 0 or 1)
                    #// Field Name                       Field Type   Size (bits)
                    #// Object ID                        GUID         128             // GUID for the Index Object - GETID3_ASF_Index_Object
                    #// Object Size                      QWORD        64              // Specifies the size, in bytes, of the Index Object, including at least 34 bytes of Index Object header
                    #// Index Entry Time Interval        DWORD        32              // Specifies the time interval between each index entry in ms.
                    #// Index Specifiers Count           WORD         16              // Specifies the number of Index Specifiers structures in this Index Object.
                    #// Index Blocks Count               DWORD        32              // Specifies the number of Index Blocks structures in this Index Object.
                    #// Index Entry Time Interval        DWORD        32              // Specifies the time interval between index entries in milliseconds.  This value cannot be 0.
                    #// Index Specifiers Count           WORD         16              // Specifies the number of entries in the Index Specifiers list.  Valid values are 1 and greater.
                    #// Index Specifiers                 array of:    varies
                    #// Stream Number                  WORD         16              // Specifies the stream number that the Index Specifiers refer to. Valid values are between 1 and 127.
                    #// Index Type                     WORD         16              // Specifies Index Type values as follows:
                    #// 1 = Nearest Past Data Packet - indexes point to the data packet whose presentation time is closest to the index entry time.
                    #// 2 = Nearest Past Media Object - indexes point to the closest data packet containing an entire object or first fragment of an object.
                    #// 3 = Nearest Past Cleanpoint. - indexes point to the closest data packet containing an entire object (or first fragment of an object) that has the Cleanpoint Flag set.
                    #// Nearest Past Cleanpoint is the most common type of index.
                    #// Index Entry Count                DWORD        32              // Specifies the number of Index Entries in the block.
                    #// Block Positions                QWORD        varies          // Specifies a list of byte offsets of the beginnings of the blocks relative to the beginning of the first Data Packet (i.e., the beginning of the Data Object + 50 bytes). The number of entries in this list is specified by the value of the Index Specifiers Count field. The order of those byte offsets is tied to the order in which Index Specifiers are listed.
                    #// Index Entries                  array of:    varies
                    #// Offsets                      DWORD        varies          // An offset value of 0xffffffff indicates an invalid offset value
                    #// shortcut
                    thisfile_asf["asf_index_object"] = Array()
                    thisfile_asf_asfindexobject = thisfile_asf["asf_index_object"]
                    ASFIndexObjectData = NextObjectDataHeader + self.fread(34 - 24)
                    offset = 24
                    thisfile_asf_asfindexobject["objectid"] = NextObjectGUID
                    thisfile_asf_asfindexobject["objectid_guid"] = NextObjectGUIDtext
                    thisfile_asf_asfindexobject["objectsize"] = NextObjectSize
                    thisfile_asf_asfindexobject["entry_time_interval"] = getid3_lib.littleendian2int(php_substr(ASFIndexObjectData, offset, 4))
                    offset += 4
                    thisfile_asf_asfindexobject["index_specifiers_count"] = getid3_lib.littleendian2int(php_substr(ASFIndexObjectData, offset, 2))
                    offset += 2
                    thisfile_asf_asfindexobject["index_blocks_count"] = getid3_lib.littleendian2int(php_substr(ASFIndexObjectData, offset, 4))
                    offset += 4
                    ASFIndexObjectData += self.fread(4 * thisfile_asf_asfindexobject["index_specifiers_count"])
                    IndexSpecifiersCounter = 0
                    while IndexSpecifiersCounter < thisfile_asf_asfindexobject["index_specifiers_count"]:
                        
                        IndexSpecifierStreamNumber = getid3_lib.littleendian2int(php_substr(ASFIndexObjectData, offset, 2))
                        offset += 2
                        thisfile_asf_asfindexobject["index_specifiers"][IndexSpecifiersCounter]["stream_number"] = IndexSpecifierStreamNumber
                        thisfile_asf_asfindexobject["index_specifiers"][IndexSpecifiersCounter]["index_type"] = getid3_lib.littleendian2int(php_substr(ASFIndexObjectData, offset, 2))
                        offset += 2
                        thisfile_asf_asfindexobject["index_specifiers"][IndexSpecifiersCounter]["index_type_text"] = self.asfindexobjectindextypelookup(thisfile_asf_asfindexobject["index_specifiers"][IndexSpecifiersCounter]["index_type"])
                        IndexSpecifiersCounter += 1
                    # end while
                    ASFIndexObjectData += self.fread(4)
                    thisfile_asf_asfindexobject["index_entry_count"] = getid3_lib.littleendian2int(php_substr(ASFIndexObjectData, offset, 4))
                    offset += 4
                    ASFIndexObjectData += self.fread(8 * thisfile_asf_asfindexobject["index_specifiers_count"])
                    IndexSpecifiersCounter = 0
                    while IndexSpecifiersCounter < thisfile_asf_asfindexobject["index_specifiers_count"]:
                        
                        thisfile_asf_asfindexobject["block_positions"][IndexSpecifiersCounter] = getid3_lib.littleendian2int(php_substr(ASFIndexObjectData, offset, 8))
                        offset += 8
                        IndexSpecifiersCounter += 1
                    # end while
                    ASFIndexObjectData += self.fread(4 * thisfile_asf_asfindexobject["index_specifiers_count"] * thisfile_asf_asfindexobject["index_entry_count"])
                    IndexEntryCounter = 0
                    while IndexEntryCounter < thisfile_asf_asfindexobject["index_entry_count"]:
                        
                        IndexSpecifiersCounter = 0
                        while IndexSpecifiersCounter < thisfile_asf_asfindexobject["index_specifiers_count"]:
                            
                            thisfile_asf_asfindexobject["offsets"][IndexSpecifiersCounter][IndexEntryCounter] = getid3_lib.littleendian2int(php_substr(ASFIndexObjectData, offset, 4))
                            offset += 4
                            IndexSpecifiersCounter += 1
                        # end while
                        IndexEntryCounter += 1
                    # end while
                    break
                # end if
                if case():
                    #// Implementations shall ignore any standard or non-standard object that they do not know how to handle.
                    if self.guidname(NextObjectGUIDtext):
                        self.warning("unhandled GUID \"" + self.guidname(NextObjectGUIDtext) + "\" {" + NextObjectGUIDtext + "} in ASF body at offset " + offset - 16 - 8)
                    else:
                        self.warning("unknown GUID {" + NextObjectGUIDtext + "} in ASF body at offset " + self.ftell() - 16 - 8)
                    # end if
                    self.fseek(NextObjectSize - 16 - 8, SEEK_CUR)
                    break
                # end if
            # end for
        # end while
        if (php_isset(lambda : thisfile_asf_codeclistobject["codec_entries"])) and php_is_array(thisfile_asf_codeclistobject["codec_entries"]):
            for streamnumber,streamdata in thisfile_asf_codeclistobject["codec_entries"]:
                for case in Switch(streamdata["information"]):
                    if case("WMV1"):
                        pass
                    # end if
                    if case("WMV2"):
                        pass
                    # end if
                    if case("WMV3"):
                        pass
                    # end if
                    if case("MSS1"):
                        pass
                    # end if
                    if case("MSS2"):
                        pass
                    # end if
                    if case("WMVA"):
                        pass
                    # end if
                    if case("WVC1"):
                        pass
                    # end if
                    if case("WMVP"):
                        pass
                    # end if
                    if case("WVP2"):
                        thisfile_video["dataformat"] = "wmv"
                        info["mime_type"] = "video/x-ms-wmv"
                        break
                    # end if
                    if case("MP42"):
                        pass
                    # end if
                    if case("MP43"):
                        pass
                    # end if
                    if case("MP4S"):
                        pass
                    # end if
                    if case("mp4s"):
                        thisfile_video["dataformat"] = "asf"
                        info["mime_type"] = "video/x-ms-asf"
                        break
                    # end if
                    if case():
                        for case in Switch(streamdata["type_raw"]):
                            if case(1):
                                if php_strstr(self.trimconvert(streamdata["name"]), "Windows Media"):
                                    thisfile_video["dataformat"] = "wmv"
                                    if info["mime_type"] == "video/x-ms-asf":
                                        info["mime_type"] = "video/x-ms-wmv"
                                    # end if
                                # end if
                                break
                            # end if
                            if case(2):
                                if php_strstr(self.trimconvert(streamdata["name"]), "Windows Media"):
                                    thisfile_audio["dataformat"] = "wma"
                                    if info["mime_type"] == "video/x-ms-asf":
                                        info["mime_type"] = "audio/x-ms-wma"
                                    # end if
                                # end if
                                break
                            # end if
                        # end for
                        break
                    # end if
                # end for
            # end for
        # end if
        for case in Switch(thisfile_audio["codec"] if (php_isset(lambda : thisfile_audio["codec"])) else ""):
            if case("MPEG Layer-3"):
                thisfile_audio["dataformat"] = "mp3"
                break
            # end if
            if case():
                break
            # end if
        # end for
        if (php_isset(lambda : thisfile_asf_codeclistobject["codec_entries"])):
            for streamnumber,streamdata in thisfile_asf_codeclistobject["codec_entries"]:
                for case in Switch(streamdata["type_raw"]):
                    if case(1):
                        #// video
                        thisfile_video["encoder"] = self.trimconvert(thisfile_asf_codeclistobject["codec_entries"][streamnumber]["name"])
                        break
                    # end if
                    if case(2):
                        #// audio
                        thisfile_audio["encoder"] = self.trimconvert(thisfile_asf_codeclistobject["codec_entries"][streamnumber]["name"])
                        #// AH 2003-10-01
                        thisfile_audio["encoder_options"] = self.trimconvert(thisfile_asf_codeclistobject["codec_entries"][0]["description"])
                        thisfile_audio["codec"] = thisfile_audio["encoder"]
                        break
                    # end if
                    if case():
                        self.warning("Unknown streamtype: [codec_list_object][codec_entries][" + streamnumber + "][type_raw] == " + streamdata["type_raw"])
                        break
                    # end if
                # end for
            # end for
        # end if
        if (php_isset(lambda : info["audio"])):
            thisfile_audio["lossless"] = thisfile_audio["lossless"] if (php_isset(lambda : thisfile_audio["lossless"])) else False
            thisfile_audio["dataformat"] = thisfile_audio["dataformat"] if (not php_empty(lambda : thisfile_audio["dataformat"])) else "asf"
        # end if
        if (not php_empty(lambda : thisfile_video["dataformat"])):
            thisfile_video["lossless"] = thisfile_audio["lossless"] if (php_isset(lambda : thisfile_audio["lossless"])) else False
            thisfile_video["pixel_aspect_ratio"] = thisfile_audio["pixel_aspect_ratio"] if (php_isset(lambda : thisfile_audio["pixel_aspect_ratio"])) else php_float(1)
            thisfile_video["dataformat"] = thisfile_video["dataformat"] if (not php_empty(lambda : thisfile_video["dataformat"])) else "asf"
        # end if
        if (not php_empty(lambda : thisfile_video["streams"])):
            thisfile_video["resolution_x"] = 0
            thisfile_video["resolution_y"] = 0
            for key,valuearray in thisfile_video["streams"]:
                if valuearray["resolution_x"] > thisfile_video["resolution_x"] or valuearray["resolution_y"] > thisfile_video["resolution_y"]:
                    thisfile_video["resolution_x"] = valuearray["resolution_x"]
                    thisfile_video["resolution_y"] = valuearray["resolution_y"]
                # end if
            # end for
        # end if
        info["bitrate"] = thisfile_audio["bitrate"] if (php_isset(lambda : thisfile_audio["bitrate"])) else 0 + thisfile_video["bitrate"] if (php_isset(lambda : thisfile_video["bitrate"])) else 0
        if (not (php_isset(lambda : info["playtime_seconds"]))) or info["playtime_seconds"] <= 0 and info["bitrate"] > 0:
            info["playtime_seconds"] = info["filesize"] - info["avdataoffset"] / info["bitrate"] / 8
        # end if
        return True
    # end def analyze
    #// 
    #// @param int $CodecListType
    #// 
    #// @return string
    #//
    @classmethod
    def codeclistobjecttypelookup(self, CodecListType=None):
        
        codeclistobjecttypelookup.lookup = Array({1: "Video Codec", 2: "Audio Codec", 65535: "Unknown Codec"})
        return codeclistobjecttypelookup.lookup[CodecListType] if (php_isset(lambda : codeclistobjecttypelookup.lookup[CodecListType])) else "Invalid Codec Type"
    # end def codeclistobjecttypelookup
    #// 
    #// @return array
    #//
    @classmethod
    def knownguids(self):
        
        knownguids.GUIDarray = Array({"GETID3_ASF_Extended_Stream_Properties_Object": "14E6A5CB-C672-4332-8399-A96952065B5A", "GETID3_ASF_Padding_Object": "1806D474-CADF-4509-A4BA-9AABCB96AAE8", "GETID3_ASF_Payload_Ext_Syst_Pixel_Aspect_Ratio": "1B1EE554-F9EA-4BC8-821A-376B74E4C4B8", "GETID3_ASF_Script_Command_Object": "1EFB1A30-0B62-11D0-A39B-00A0C90348F6", "GETID3_ASF_No_Error_Correction": "20FB5700-5B55-11CF-A8FD-00805F5C442B", "GETID3_ASF_Content_Branding_Object": "2211B3FA-BD23-11D2-B4B7-00A0C955FC6E", "GETID3_ASF_Content_Encryption_Object": "2211B3FB-BD23-11D2-B4B7-00A0C955FC6E", "GETID3_ASF_Digital_Signature_Object": "2211B3FC-BD23-11D2-B4B7-00A0C955FC6E", "GETID3_ASF_Extended_Content_Encryption_Object": "298AE614-2622-4C17-B935-DAE07EE9289C", "GETID3_ASF_Simple_Index_Object": "33000890-E5B1-11CF-89F4-00A0C90349CB", "GETID3_ASF_Degradable_JPEG_Media": "35907DE0-E415-11CF-A917-00805F5C442B", "GETID3_ASF_Payload_Extension_System_Timecode": "399595EC-8667-4E2D-8FDB-98814CE76C1E", "GETID3_ASF_Binary_Media": "3AFB65E2-47EF-40F2-AC2C-70A90D71D343", "GETID3_ASF_Timecode_Index_Object": "3CB73FD0-0C4A-4803-953D-EDF7B6228F0C", "GETID3_ASF_Metadata_Library_Object": "44231C94-9498-49D1-A141-1D134E457054", "GETID3_ASF_Reserved_3": "4B1ACBE3-100B-11D0-A39B-00A0C90348F6", "GETID3_ASF_Reserved_4": "4CFEDB20-75F6-11CF-9C0F-00A0C90349CB", "GETID3_ASF_Command_Media": "59DACFC0-59E6-11D0-A3AC-00A0C90348F6", "GETID3_ASF_Header_Extension_Object": "5FBF03B5-A92E-11CF-8EE3-00C00C205365", "GETID3_ASF_Media_Object_Index_Parameters_Obj": "6B203BAD-3F11-4E84-ACA8-D7613DE2CFA7", "GETID3_ASF_Header_Object": "75B22630-668E-11CF-A6D9-00AA0062CE6C", "GETID3_ASF_Content_Description_Object": "75B22633-668E-11CF-A6D9-00AA0062CE6C", "GETID3_ASF_Error_Correction_Object": "75B22635-668E-11CF-A6D9-00AA0062CE6C", "GETID3_ASF_Data_Object": "75B22636-668E-11CF-A6D9-00AA0062CE6C", "GETID3_ASF_Web_Stream_Media_Subtype": "776257D4-C627-41CB-8F81-7AC7FF1C40CC", "GETID3_ASF_Stream_Bitrate_Properties_Object": "7BF875CE-468D-11D1-8D82-006097C9A2B2", "GETID3_ASF_Language_List_Object": "7C4346A9-EFE0-4BFC-B229-393EDE415C85", "GETID3_ASF_Codec_List_Object": "86D15240-311D-11D0-A3A4-00A0C90348F6", "GETID3_ASF_Reserved_2": "86D15241-311D-11D0-A3A4-00A0C90348F6", "GETID3_ASF_File_Properties_Object": "8CABDCA1-A947-11CF-8EE4-00C00C205365", "GETID3_ASF_File_Transfer_Media": "91BD222C-F21C-497A-8B6D-5AA86BFC0185", "GETID3_ASF_Old_RTP_Extension_Data": "96800C63-4C94-11D1-837B-0080C7A37F95", "GETID3_ASF_Advanced_Mutual_Exclusion_Object": "A08649CF-4775-4670-8A16-6E35357566CD", "GETID3_ASF_Bandwidth_Sharing_Object": "A69609E6-517B-11D2-B6AF-00C04FD908E9", "GETID3_ASF_Reserved_1": "ABD3D211-A9BA-11cf-8EE6-00C00C205365", "GETID3_ASF_Bandwidth_Sharing_Exclusive": "AF6060AA-5197-11D2-B6AF-00C04FD908E9", "GETID3_ASF_Bandwidth_Sharing_Partial": "AF6060AB-5197-11D2-B6AF-00C04FD908E9", "GETID3_ASF_JFIF_Media": "B61BE100-5B4E-11CF-A8FD-00805F5C442B", "GETID3_ASF_Stream_Properties_Object": "B7DC0791-A9B7-11CF-8EE6-00C00C205365", "GETID3_ASF_Video_Media": "BC19EFC0-5B4D-11CF-A8FD-00805F5C442B", "GETID3_ASF_Audio_Spread": "BFC3CD50-618F-11CF-8BB2-00AA00B4E220", "GETID3_ASF_Metadata_Object": "C5F8CBEA-5BAF-4877-8467-AA8C44FA4CCA", "GETID3_ASF_Payload_Ext_Syst_Sample_Duration": "C6BD9450-867F-4907-83A3-C77921B733AD", "GETID3_ASF_Group_Mutual_Exclusion_Object": "D1465A40-5A79-4338-B71B-E36B8FD6C249", "GETID3_ASF_Extended_Content_Description_Object": "D2D0A440-E307-11D2-97F0-00A0C95EA850", "GETID3_ASF_Stream_Prioritization_Object": "D4FED15B-88D3-454F-81F0-ED5C45999E24", "GETID3_ASF_Payload_Ext_System_Content_Type": "D590DC20-07BC-436C-9CF7-F3BBFBF1A4DC", "GETID3_ASF_Old_File_Properties_Object": "D6E229D0-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_ASF_Header_Object": "D6E229D1-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_ASF_Data_Object": "D6E229D2-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Index_Object": "D6E229D3-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Stream_Properties_Object": "D6E229D4-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Content_Description_Object": "D6E229D5-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Script_Command_Object": "D6E229D6-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Marker_Object": "D6E229D7-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Component_Download_Object": "D6E229D8-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Stream_Group_Object": "D6E229D9-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Scalable_Object": "D6E229DA-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Prioritization_Object": "D6E229DB-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Bitrate_Mutual_Exclusion_Object": "D6E229DC-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Inter_Media_Dependency_Object": "D6E229DD-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Rating_Object": "D6E229DE-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Index_Parameters_Object": "D6E229DF-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Color_Table_Object": "D6E229E0-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Language_List_Object": "D6E229E1-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Audio_Media": "D6E229E2-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Video_Media": "D6E229E3-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Image_Media": "D6E229E4-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Timecode_Media": "D6E229E5-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Text_Media": "D6E229E6-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_MIDI_Media": "D6E229E7-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Command_Media": "D6E229E8-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_No_Error_Concealment": "D6E229EA-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Scrambled_Audio": "D6E229EB-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_No_Color_Table": "D6E229EC-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_SMPTE_Time": "D6E229ED-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_ASCII_Text": "D6E229EE-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Unicode_Text": "D6E229EF-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_HTML_Text": "D6E229F0-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_URL_Command": "D6E229F1-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Filename_Command": "D6E229F2-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_ACM_Codec": "D6E229F3-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_VCM_Codec": "D6E229F4-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_QuickTime_Codec": "D6E229F5-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_DirectShow_Transform_Filter": "D6E229F6-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_DirectShow_Rendering_Filter": "D6E229F7-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_No_Enhancement": "D6E229F8-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Unknown_Enhancement_Type": "D6E229F9-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Temporal_Enhancement": "D6E229FA-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Spatial_Enhancement": "D6E229FB-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Quality_Enhancement": "D6E229FC-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Number_of_Channels_Enhancement": "D6E229FD-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Frequency_Response_Enhancement": "D6E229FE-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Media_Object": "D6E229FF-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Mutex_Language": "D6E22A00-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Mutex_Bitrate": "D6E22A01-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Mutex_Unknown": "D6E22A02-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_ASF_Placeholder_Object": "D6E22A0E-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Data_Unit_Extension_Object": "D6E22A0F-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Web_Stream_Format": "DA1E6B13-8359-4050-B398-388E965BF00C", "GETID3_ASF_Payload_Ext_System_File_Name": "E165EC0E-19ED-45D7-B4A7-25CBD1E28E9B", "GETID3_ASF_Marker_Object": "F487CD01-A951-11CF-8EE6-00C00C205365", "GETID3_ASF_Timecode_Index_Parameters_Object": "F55E496D-9797-4B5D-8C8B-604DFE9BFB24", "GETID3_ASF_Audio_Media": "F8699E40-5B4D-11CF-A8FD-00805F5C442B", "GETID3_ASF_Media_Object_Index_Object": "FEB103F8-12AD-4C64-840F-2A1D2F7AD48C", "GETID3_ASF_Alt_Extended_Content_Encryption_Obj": "FF889EF1-ADEE-40DA-9E71-98704BB928CE", "GETID3_ASF_Index_Placeholder_Object": "D9AADE20-7C17-4F9C-BC28-8555DD98E2A2", "GETID3_ASF_Compatibility_Object": "26F18B5D-4584-47EC-9F5F-0E651F0452C9"})
        return knownguids.GUIDarray
    # end def knownguids
    #// 
    #// @param string $GUIDstring
    #// 
    #// @return string|false
    #//
    @classmethod
    def guidname(self, GUIDstring=None):
        
        guidname.GUIDarray = Array()
        if php_empty(lambda : guidname.GUIDarray):
            guidname.GUIDarray = self.knownguids()
        # end if
        return php_array_search(GUIDstring, guidname.GUIDarray)
    # end def guidname
    #// 
    #// @param int $id
    #// 
    #// @return string
    #//
    @classmethod
    def asfindexobjectindextypelookup(self, id=None):
        
        asfindexobjectindextypelookup.ASFIndexObjectIndexTypeLookup = Array()
        if php_empty(lambda : asfindexobjectindextypelookup.ASFIndexObjectIndexTypeLookup):
            asfindexobjectindextypelookup.ASFIndexObjectIndexTypeLookup[1] = "Nearest Past Data Packet"
            asfindexobjectindextypelookup.ASFIndexObjectIndexTypeLookup[2] = "Nearest Past Media Object"
            asfindexobjectindextypelookup.ASFIndexObjectIndexTypeLookup[3] = "Nearest Past Cleanpoint"
        # end if
        return asfindexobjectindextypelookup.ASFIndexObjectIndexTypeLookup[id] if (php_isset(lambda : asfindexobjectindextypelookup.ASFIndexObjectIndexTypeLookup[id])) else "invalid"
    # end def asfindexobjectindextypelookup
    #// 
    #// @param string $GUIDstring
    #// 
    #// @return string
    #//
    @classmethod
    def guidtobytestring(self, GUIDstring=None):
        
        #// Microsoft defines these 16-byte (128-bit) GUIDs in the strangest way:
        #// first 4 bytes are in little-endian order
        #// next 2 bytes are appended in little-endian order
        #// next 2 bytes are appended in little-endian order
        #// next 2 bytes are appended in big-endian order
        #// next 6 bytes are appended in big-endian order
        #// AaBbCcDd-EeFf-GgHh-IiJj-KkLlMmNnOoPp is stored as this 16-byte string:
        #// $Dd $Cc $Bb $Aa $Ff $Ee $Hh $Gg $Ii $Jj $Kk $Ll $Mm $Nn $Oo $Pp
        hexbytecharstring = chr(hexdec(php_substr(GUIDstring, 6, 2)))
        hexbytecharstring += chr(hexdec(php_substr(GUIDstring, 4, 2)))
        hexbytecharstring += chr(hexdec(php_substr(GUIDstring, 2, 2)))
        hexbytecharstring += chr(hexdec(php_substr(GUIDstring, 0, 2)))
        hexbytecharstring += chr(hexdec(php_substr(GUIDstring, 11, 2)))
        hexbytecharstring += chr(hexdec(php_substr(GUIDstring, 9, 2)))
        hexbytecharstring += chr(hexdec(php_substr(GUIDstring, 16, 2)))
        hexbytecharstring += chr(hexdec(php_substr(GUIDstring, 14, 2)))
        hexbytecharstring += chr(hexdec(php_substr(GUIDstring, 19, 2)))
        hexbytecharstring += chr(hexdec(php_substr(GUIDstring, 21, 2)))
        hexbytecharstring += chr(hexdec(php_substr(GUIDstring, 24, 2)))
        hexbytecharstring += chr(hexdec(php_substr(GUIDstring, 26, 2)))
        hexbytecharstring += chr(hexdec(php_substr(GUIDstring, 28, 2)))
        hexbytecharstring += chr(hexdec(php_substr(GUIDstring, 30, 2)))
        hexbytecharstring += chr(hexdec(php_substr(GUIDstring, 32, 2)))
        hexbytecharstring += chr(hexdec(php_substr(GUIDstring, 34, 2)))
        return hexbytecharstring
    # end def guidtobytestring
    #// 
    #// @param string $Bytestring
    #// 
    #// @return string
    #//
    @classmethod
    def bytestringtoguid(self, Bytestring=None):
        
        GUIDstring = php_str_pad(dechex(php_ord(Bytestring[3])), 2, "0", STR_PAD_LEFT)
        GUIDstring += php_str_pad(dechex(php_ord(Bytestring[2])), 2, "0", STR_PAD_LEFT)
        GUIDstring += php_str_pad(dechex(php_ord(Bytestring[1])), 2, "0", STR_PAD_LEFT)
        GUIDstring += php_str_pad(dechex(php_ord(Bytestring[0])), 2, "0", STR_PAD_LEFT)
        GUIDstring += "-"
        GUIDstring += php_str_pad(dechex(php_ord(Bytestring[5])), 2, "0", STR_PAD_LEFT)
        GUIDstring += php_str_pad(dechex(php_ord(Bytestring[4])), 2, "0", STR_PAD_LEFT)
        GUIDstring += "-"
        GUIDstring += php_str_pad(dechex(php_ord(Bytestring[7])), 2, "0", STR_PAD_LEFT)
        GUIDstring += php_str_pad(dechex(php_ord(Bytestring[6])), 2, "0", STR_PAD_LEFT)
        GUIDstring += "-"
        GUIDstring += php_str_pad(dechex(php_ord(Bytestring[8])), 2, "0", STR_PAD_LEFT)
        GUIDstring += php_str_pad(dechex(php_ord(Bytestring[9])), 2, "0", STR_PAD_LEFT)
        GUIDstring += "-"
        GUIDstring += php_str_pad(dechex(php_ord(Bytestring[10])), 2, "0", STR_PAD_LEFT)
        GUIDstring += php_str_pad(dechex(php_ord(Bytestring[11])), 2, "0", STR_PAD_LEFT)
        GUIDstring += php_str_pad(dechex(php_ord(Bytestring[12])), 2, "0", STR_PAD_LEFT)
        GUIDstring += php_str_pad(dechex(php_ord(Bytestring[13])), 2, "0", STR_PAD_LEFT)
        GUIDstring += php_str_pad(dechex(php_ord(Bytestring[14])), 2, "0", STR_PAD_LEFT)
        GUIDstring += php_str_pad(dechex(php_ord(Bytestring[15])), 2, "0", STR_PAD_LEFT)
        return php_strtoupper(GUIDstring)
    # end def bytestringtoguid
    #// 
    #// @param int  $FILETIME
    #// @param bool $round
    #// 
    #// @return float|int
    #//
    @classmethod
    def filetimetounixtime(self, FILETIME=None, round=True):
        
        #// FILETIME is a 64-bit unsigned integer representing
        #// the number of 100-nanosecond intervals since January 1, 1601
        #// UNIX timestamp is number of seconds since January 1, 1970
        #// 116444736000000000 = 10000000 * 60 * 60 * 24 * 365 * 369 + 89 leap days
        if round:
            return php_intval(round(FILETIME - 116444736000000000 / 10000000))
        # end if
        return FILETIME - 116444736000000000 / 10000000
    # end def filetimetounixtime
    #// 
    #// @param int $WMpictureType
    #// 
    #// @return string
    #//
    @classmethod
    def wmpicturetypelookup(self, WMpictureType=None):
        
        wmpicturetypelookup.lookup = None
        if wmpicturetypelookup.lookup == None:
            wmpicturetypelookup.lookup = Array({3: "Front Cover", 4: "Back Cover", 0: "User Defined", 5: "Leaflet Page", 6: "Media Label", 7: "Lead Artist", 8: "Artist", 9: "Conductor", 10: "Band", 11: "Composer", 12: "Lyricist", 13: "Recording Location", 14: "During Recording", 15: "During Performance", 16: "Video Screen Capture", 18: "Illustration", 19: "Band Logotype", 20: "Publisher Logotype"})
            wmpicturetypelookup.lookup = php_array_map((lambda str = None:  getid3_lib.iconv_fallback("UTF-8", "UTF-16LE", str)), wmpicturetypelookup.lookup)
        # end if
        return wmpicturetypelookup.lookup[WMpictureType] if (php_isset(lambda : wmpicturetypelookup.lookup[WMpictureType])) else ""
    # end def wmpicturetypelookup
    #// 
    #// @param string $asf_header_extension_object_data
    #// @param int    $unhandled_sections
    #// 
    #// @return array
    #//
    def headerextensionobjectdataparse(self, asf_header_extension_object_data=None, unhandled_sections=None):
        
        #// http://msdn.microsoft.com/en-us/library/bb643323.aspx
        offset = 0
        objectOffset = 0
        HeaderExtensionObjectParsed = Array()
        while True:
            
            if not (objectOffset < php_strlen(asf_header_extension_object_data)):
                break
            # end if
            offset = objectOffset
            thisObject = Array()
            thisObject["guid"] = php_substr(asf_header_extension_object_data, offset, 16)
            offset += 16
            thisObject["guid_text"] = self.bytestringtoguid(thisObject["guid"])
            thisObject["guid_name"] = self.guidname(thisObject["guid_text"])
            thisObject["size"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, 8))
            offset += 8
            if thisObject["size"] <= 0:
                break
            # end if
            for case in Switch(thisObject["guid"]):
                if case(GETID3_ASF_Extended_Stream_Properties_Object):
                    thisObject["start_time"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, 8))
                    offset += 8
                    thisObject["start_time_unix"] = self.filetimetounixtime(thisObject["start_time"])
                    thisObject["end_time"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, 8))
                    offset += 8
                    thisObject["end_time_unix"] = self.filetimetounixtime(thisObject["end_time"])
                    thisObject["data_bitrate"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, 4))
                    offset += 4
                    thisObject["buffer_size"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, 4))
                    offset += 4
                    thisObject["initial_buffer_fullness"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, 4))
                    offset += 4
                    thisObject["alternate_data_bitrate"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, 4))
                    offset += 4
                    thisObject["alternate_buffer_size"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, 4))
                    offset += 4
                    thisObject["alternate_initial_buffer_fullness"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, 4))
                    offset += 4
                    thisObject["maximum_object_size"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, 4))
                    offset += 4
                    thisObject["flags_raw"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, 4))
                    offset += 4
                    thisObject["flags"]["reliable"] = php_bool(thisObject["flags_raw"]) & 1
                    thisObject["flags"]["seekable"] = php_bool(thisObject["flags_raw"]) & 2
                    thisObject["flags"]["no_cleanpoints"] = php_bool(thisObject["flags_raw"]) & 4
                    thisObject["flags"]["resend_live_cleanpoints"] = php_bool(thisObject["flags_raw"]) & 8
                    thisObject["stream_number"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, 2))
                    offset += 2
                    thisObject["stream_language_id_index"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, 2))
                    offset += 2
                    thisObject["average_time_per_frame"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, 4))
                    offset += 4
                    thisObject["stream_name_count"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, 2))
                    offset += 2
                    thisObject["payload_extension_system_count"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, 2))
                    offset += 2
                    i = 0
                    while i < thisObject["stream_name_count"]:
                        
                        streamName = Array()
                        streamName["language_id_index"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, 2))
                        offset += 2
                        streamName["stream_name_length"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, 2))
                        offset += 2
                        streamName["stream_name"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, streamName["stream_name_length"]))
                        offset += streamName["stream_name_length"]
                        thisObject["stream_names"][i] = streamName
                        i += 1
                    # end while
                    i = 0
                    while i < thisObject["payload_extension_system_count"]:
                        
                        payloadExtensionSystem = Array()
                        payloadExtensionSystem["extension_system_id"] = php_substr(asf_header_extension_object_data, offset, 16)
                        offset += 16
                        payloadExtensionSystem["extension_system_id_text"] = self.bytestringtoguid(payloadExtensionSystem["extension_system_id"])
                        payloadExtensionSystem["extension_system_size"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, 2))
                        offset += 2
                        if payloadExtensionSystem["extension_system_size"] <= 0:
                            break
                        # end if
                        payloadExtensionSystem["extension_system_info_length"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, 4))
                        offset += 4
                        payloadExtensionSystem["extension_system_info_length"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, payloadExtensionSystem["extension_system_info_length"]))
                        offset += payloadExtensionSystem["extension_system_info_length"]
                        thisObject["payload_extension_systems"][i] = payloadExtensionSystem
                        i += 1
                    # end while
                    break
                # end if
                if case(GETID3_ASF_Padding_Object):
                    break
                # end if
                if case(GETID3_ASF_Metadata_Object):
                    thisObject["description_record_counts"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, 2))
                    offset += 2
                    i = 0
                    while i < thisObject["description_record_counts"]:
                        
                        descriptionRecord = Array()
                        descriptionRecord["reserved_1"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, 2))
                        #// must be zero
                        offset += 2
                        descriptionRecord["stream_number"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, 2))
                        offset += 2
                        descriptionRecord["name_length"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, 2))
                        offset += 2
                        descriptionRecord["data_type"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, 2))
                        offset += 2
                        descriptionRecord["data_type_text"] = self.metadatalibraryobjectdatatypelookup(descriptionRecord["data_type"])
                        descriptionRecord["data_length"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, 4))
                        offset += 4
                        descriptionRecord["name"] = php_substr(asf_header_extension_object_data, offset, descriptionRecord["name_length"])
                        offset += descriptionRecord["name_length"]
                        descriptionRecord["data"] = php_substr(asf_header_extension_object_data, offset, descriptionRecord["data_length"])
                        offset += descriptionRecord["data_length"]
                        for case in Switch(descriptionRecord["data_type"]):
                            if case(0):
                                break
                            # end if
                            if case(1):
                                break
                            # end if
                            if case(2):
                                #// BOOL
                                descriptionRecord["data"] = php_bool(getid3_lib.littleendian2int(descriptionRecord["data"]))
                                break
                            # end if
                            if case(3):
                                pass
                            # end if
                            if case(4):
                                pass
                            # end if
                            if case(5):
                                #// WORD
                                descriptionRecord["data"] = getid3_lib.littleendian2int(descriptionRecord["data"])
                                break
                            # end if
                            if case(6):
                                #// GUID
                                descriptionRecord["data_text"] = self.bytestringtoguid(descriptionRecord["data"])
                                break
                            # end if
                        # end for
                        thisObject["description_record"][i] = descriptionRecord
                        i += 1
                    # end while
                    break
                # end if
                if case(GETID3_ASF_Language_List_Object):
                    thisObject["language_id_record_counts"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, 2))
                    offset += 2
                    i = 0
                    while i < thisObject["language_id_record_counts"]:
                        
                        languageIDrecord = Array()
                        languageIDrecord["language_id_length"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, 1))
                        offset += 1
                        languageIDrecord["language_id"] = php_substr(asf_header_extension_object_data, offset, languageIDrecord["language_id_length"])
                        offset += languageIDrecord["language_id_length"]
                        thisObject["language_id_record"][i] = languageIDrecord
                        i += 1
                    # end while
                    break
                # end if
                if case(GETID3_ASF_Metadata_Library_Object):
                    thisObject["description_records_count"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, 2))
                    offset += 2
                    i = 0
                    while i < thisObject["description_records_count"]:
                        
                        descriptionRecord = Array()
                        descriptionRecord["language_list_index"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, 2))
                        offset += 2
                        descriptionRecord["stream_number"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, 2))
                        offset += 2
                        descriptionRecord["name_length"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, 2))
                        offset += 2
                        descriptionRecord["data_type"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, 2))
                        offset += 2
                        descriptionRecord["data_type_text"] = self.metadatalibraryobjectdatatypelookup(descriptionRecord["data_type"])
                        descriptionRecord["data_length"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data, offset, 4))
                        offset += 4
                        descriptionRecord["name"] = php_substr(asf_header_extension_object_data, offset, descriptionRecord["name_length"])
                        offset += descriptionRecord["name_length"]
                        descriptionRecord["data"] = php_substr(asf_header_extension_object_data, offset, descriptionRecord["data_length"])
                        offset += descriptionRecord["data_length"]
                        if php_preg_match("#^WM/Picture$#", php_str_replace(" ", "", php_trim(descriptionRecord["name"]))):
                            WMpicture = self.asf_wmpicture(descriptionRecord["data"])
                            for key,value in WMpicture:
                                descriptionRecord["data"] = WMpicture
                            # end for
                            WMpicture = None
                        # end if
                        thisObject["description_record"][i] = descriptionRecord
                        i += 1
                    # end while
                    break
                # end if
                if case():
                    unhandled_sections += 1
                    if self.guidname(thisObject["guid_text"]):
                        self.warning("unhandled Header Extension Object GUID \"" + self.guidname(thisObject["guid_text"]) + "\" {" + thisObject["guid_text"] + "} at offset " + offset - 16 - 8)
                    else:
                        self.warning("unknown Header Extension Object GUID {" + thisObject["guid_text"] + "} in at offset " + offset - 16 - 8)
                    # end if
                    break
                # end if
            # end for
            HeaderExtensionObjectParsed[-1] = thisObject
            objectOffset += thisObject["size"]
        # end while
        return HeaderExtensionObjectParsed
    # end def headerextensionobjectdataparse
    #// 
    #// @param int $id
    #// 
    #// @return string
    #//
    @classmethod
    def metadatalibraryobjectdatatypelookup(self, id=None):
        
        metadatalibraryobjectdatatypelookup.lookup = Array({0: "Unicode string", 1: "BYTE array", 2: "BOOL", 3: "DWORD", 4: "QWORD", 5: "WORD", 6: "GUID"})
        return metadatalibraryobjectdatatypelookup.lookup[id] if (php_isset(lambda : metadatalibraryobjectdatatypelookup.lookup[id])) else "invalid"
    # end def metadatalibraryobjectdatatypelookup
    #// 
    #// @param string $data
    #// 
    #// @return array
    #//
    def asf_wmpicture(self, data=None):
        
        #// typedef struct _WMPicture{
        #// LPWSTR  pwszMIMEType;
        #// BYTE  bPictureType;
        #// LPWSTR  pwszDescription;
        #// DWORD  dwDataLen;
        #// BYTE*  pbData;
        #// } WM_PICTURE;
        WMpicture = Array()
        offset = 0
        WMpicture["image_type_id"] = getid3_lib.littleendian2int(php_substr(data, offset, 1))
        offset += 1
        WMpicture["image_type"] = self.wmpicturetypelookup(WMpicture["image_type_id"])
        WMpicture["image_size"] = getid3_lib.littleendian2int(php_substr(data, offset, 4))
        offset += 4
        WMpicture["image_mime"] = ""
        while True:
            next_byte_pair = php_substr(data, offset, 2)
            offset += 2
            WMpicture["image_mime"] += next_byte_pair
            
            if next_byte_pair != "  ":
                break
            # end if
        # end while
        WMpicture["image_description"] = ""
        while True:
            next_byte_pair = php_substr(data, offset, 2)
            offset += 2
            WMpicture["image_description"] += next_byte_pair
            
            if next_byte_pair != "  ":
                break
            # end if
        # end while
        WMpicture["dataoffset"] = offset
        WMpicture["data"] = php_substr(data, offset)
        imageinfo = Array()
        WMpicture["image_mime"] = ""
        imagechunkcheck = getid3_lib.getdataimagesize(WMpicture["data"], imageinfo)
        imageinfo = None
        if (not php_empty(lambda : imagechunkcheck)):
            WMpicture["image_mime"] = image_type_to_mime_type(imagechunkcheck[2])
        # end if
        if (not (php_isset(lambda : self.getid3.info["asf"]["comments"]["picture"]))):
            self.getid3.info["asf"]["comments"]["picture"] = Array()
        # end if
        self.getid3.info["asf"]["comments"]["picture"][-1] = Array({"data": WMpicture["data"], "image_mime": WMpicture["image_mime"]})
        return WMpicture
    # end def asf_wmpicture
    #// 
    #// Remove terminator 00 00 and convert UTF-16LE to Latin-1.
    #// 
    #// @param string $string
    #// 
    #// @return string
    #//
    @classmethod
    def trimconvert(self, string=None):
        
        return php_trim(getid3_lib.iconv_fallback("UTF-16LE", "ISO-8859-1", self.trimterm(string)), " ")
    # end def trimconvert
    #// 
    #// Remove terminator 00 00.
    #// 
    #// @param string $string
    #// 
    #// @return string
    #//
    @classmethod
    def trimterm(self, string=None):
        
        #// remove terminator, only if present (it should be, but...)
        if php_substr(string, -2) == "  ":
            string = php_substr(string, 0, -2)
        # end if
        return string
    # end def trimterm
# end class getid3_asf
