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
    def __init__(self, getid3_=None):
        
        
        super().__init__(getid3_)
        #// extends getid3_handler::__construct()
        #// initialize all GUID constants
        GUIDarray_ = self.knownguids()
        for GUIDname_,hexstringvalue_ in GUIDarray_.items():
            if (not php_defined(GUIDname_)):
                php_define(GUIDname_, self.guidtobytestring(hexstringvalue_))
            # end if
        # end for
    # end def __init__
    #// 
    #// @return bool
    #//
    def analyze(self):
        
        
        info_ = self.getid3.info
        #// Shortcuts
        thisfile_audio_ = info_["audio"]
        thisfile_video_ = info_["video"]
        info_["asf"] = Array()
        thisfile_asf_ = info_["asf"]
        thisfile_asf_["comments"] = Array()
        thisfile_asf_comments_ = thisfile_asf_["comments"]
        thisfile_asf_["header_object"] = Array()
        thisfile_asf_headerobject_ = thisfile_asf_["header_object"]
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
        info_["fileformat"] = "asf"
        self.fseek(info_["avdataoffset"])
        HeaderObjectData_ = self.fread(30)
        thisfile_asf_headerobject_["objectid"] = php_substr(HeaderObjectData_, 0, 16)
        thisfile_asf_headerobject_["objectid_guid"] = self.bytestringtoguid(thisfile_asf_headerobject_["objectid"])
        if thisfile_asf_headerobject_["objectid"] != GETID3_ASF_Header_Object:
            info_["fileformat"] = None
            info_["asf"] = None
            return self.error("ASF header GUID {" + self.bytestringtoguid(thisfile_asf_headerobject_["objectid"]) + "} does not match expected \"GETID3_ASF_Header_Object\" GUID {" + self.bytestringtoguid(GETID3_ASF_Header_Object) + "}")
        # end if
        thisfile_asf_headerobject_["objectsize"] = getid3_lib.littleendian2int(php_substr(HeaderObjectData_, 16, 8))
        thisfile_asf_headerobject_["headerobjects"] = getid3_lib.littleendian2int(php_substr(HeaderObjectData_, 24, 4))
        thisfile_asf_headerobject_["reserved1"] = getid3_lib.littleendian2int(php_substr(HeaderObjectData_, 28, 1))
        thisfile_asf_headerobject_["reserved2"] = getid3_lib.littleendian2int(php_substr(HeaderObjectData_, 29, 1))
        NextObjectOffset_ = self.ftell()
        ASFHeaderData_ = self.fread(thisfile_asf_headerobject_["objectsize"] - 30)
        offset_ = 0
        thisfile_asf_streambitratepropertiesobject_ = Array()
        thisfile_asf_codeclistobject_ = Array()
        HeaderObjectsCounter_ = 0
        while HeaderObjectsCounter_ < thisfile_asf_headerobject_["headerobjects"]:
            
            NextObjectGUID_ = php_substr(ASFHeaderData_, offset_, 16)
            offset_ += 16
            NextObjectGUIDtext_ = self.bytestringtoguid(NextObjectGUID_)
            NextObjectSize_ = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 8))
            offset_ += 8
            for case in Switch(NextObjectGUID_):
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
                    thisfile_asf_["file_properties_object"] = Array()
                    thisfile_asf_filepropertiesobject_ = thisfile_asf_["file_properties_object"]
                    thisfile_asf_filepropertiesobject_["offset"] = NextObjectOffset_ + offset_
                    thisfile_asf_filepropertiesobject_["objectid"] = NextObjectGUID_
                    thisfile_asf_filepropertiesobject_["objectid_guid"] = NextObjectGUIDtext_
                    thisfile_asf_filepropertiesobject_["objectsize"] = NextObjectSize_
                    thisfile_asf_filepropertiesobject_["fileid"] = php_substr(ASFHeaderData_, offset_, 16)
                    offset_ += 16
                    thisfile_asf_filepropertiesobject_["fileid_guid"] = self.bytestringtoguid(thisfile_asf_filepropertiesobject_["fileid"])
                    thisfile_asf_filepropertiesobject_["filesize"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 8))
                    offset_ += 8
                    thisfile_asf_filepropertiesobject_["creation_date"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 8))
                    thisfile_asf_filepropertiesobject_["creation_date_unix"] = self.filetimetounixtime(thisfile_asf_filepropertiesobject_["creation_date"])
                    offset_ += 8
                    thisfile_asf_filepropertiesobject_["data_packets"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 8))
                    offset_ += 8
                    thisfile_asf_filepropertiesobject_["play_duration"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 8))
                    offset_ += 8
                    thisfile_asf_filepropertiesobject_["send_duration"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 8))
                    offset_ += 8
                    thisfile_asf_filepropertiesobject_["preroll"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 8))
                    offset_ += 8
                    thisfile_asf_filepropertiesobject_["flags_raw"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 4))
                    offset_ += 4
                    thisfile_asf_filepropertiesobject_["flags"]["broadcast"] = php_bool(thisfile_asf_filepropertiesobject_["flags_raw"] & 1)
                    thisfile_asf_filepropertiesobject_["flags"]["seekable"] = php_bool(thisfile_asf_filepropertiesobject_["flags_raw"] & 2)
                    thisfile_asf_filepropertiesobject_["min_packet_size"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 4))
                    offset_ += 4
                    thisfile_asf_filepropertiesobject_["max_packet_size"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 4))
                    offset_ += 4
                    thisfile_asf_filepropertiesobject_["max_bitrate"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 4))
                    offset_ += 4
                    if thisfile_asf_filepropertiesobject_["flags"]["broadcast"]:
                        thisfile_asf_filepropertiesobject_["filesize"] = None
                        thisfile_asf_filepropertiesobject_["data_packets"] = None
                        thisfile_asf_filepropertiesobject_["play_duration"] = None
                        thisfile_asf_filepropertiesobject_["send_duration"] = None
                        thisfile_asf_filepropertiesobject_["min_packet_size"] = None
                        thisfile_asf_filepropertiesobject_["max_packet_size"] = None
                    else:
                        #// broadcast flag NOT set, perform calculations
                        info_["playtime_seconds"] = thisfile_asf_filepropertiesobject_["play_duration"] / 10000000 - thisfile_asf_filepropertiesobject_["preroll"] / 1000
                        #// $info['bitrate'] = $thisfile_asf_filepropertiesobject['max_bitrate'];
                        info_["bitrate"] = thisfile_asf_filepropertiesobject_["filesize"] if (php_isset(lambda : thisfile_asf_filepropertiesobject_["filesize"])) else info_["filesize"] * 8 / info_["playtime_seconds"]
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
                    StreamPropertiesObjectData_["offset"] = NextObjectOffset_ + offset_
                    StreamPropertiesObjectData_["objectid"] = NextObjectGUID_
                    StreamPropertiesObjectData_["objectid_guid"] = NextObjectGUIDtext_
                    StreamPropertiesObjectData_["objectsize"] = NextObjectSize_
                    StreamPropertiesObjectData_["stream_type"] = php_substr(ASFHeaderData_, offset_, 16)
                    offset_ += 16
                    StreamPropertiesObjectData_["stream_type_guid"] = self.bytestringtoguid(StreamPropertiesObjectData_["stream_type"])
                    StreamPropertiesObjectData_["error_correct_type"] = php_substr(ASFHeaderData_, offset_, 16)
                    offset_ += 16
                    StreamPropertiesObjectData_["error_correct_guid"] = self.bytestringtoguid(StreamPropertiesObjectData_["error_correct_type"])
                    StreamPropertiesObjectData_["time_offset"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 8))
                    offset_ += 8
                    StreamPropertiesObjectData_["type_data_length"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 4))
                    offset_ += 4
                    StreamPropertiesObjectData_["error_data_length"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 4))
                    offset_ += 4
                    StreamPropertiesObjectData_["flags_raw"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 2))
                    offset_ += 2
                    StreamPropertiesObjectStreamNumber_ = StreamPropertiesObjectData_["flags_raw"] & 127
                    StreamPropertiesObjectData_["flags"]["encrypted"] = php_bool(StreamPropertiesObjectData_["flags_raw"] & 32768)
                    offset_ += 4
                    #// reserved - DWORD
                    StreamPropertiesObjectData_["type_specific_data"] = php_substr(ASFHeaderData_, offset_, StreamPropertiesObjectData_["type_data_length"])
                    offset_ += StreamPropertiesObjectData_["type_data_length"]
                    StreamPropertiesObjectData_["error_correct_data"] = php_substr(ASFHeaderData_, offset_, StreamPropertiesObjectData_["error_data_length"])
                    offset_ += StreamPropertiesObjectData_["error_data_length"]
                    for case in Switch(StreamPropertiesObjectData_["stream_type"]):
                        if case(GETID3_ASF_Audio_Media):
                            thisfile_audio_["dataformat"] = thisfile_audio_["dataformat"] if (not php_empty(lambda : thisfile_audio_["dataformat"])) else "asf"
                            thisfile_audio_["bitrate_mode"] = thisfile_audio_["bitrate_mode"] if (not php_empty(lambda : thisfile_audio_["bitrate_mode"])) else "cbr"
                            audiodata_ = getid3_riff.parsewaveformatex(php_substr(StreamPropertiesObjectData_["type_specific_data"], 0, 16))
                            audiodata_["raw"] = None
                            thisfile_audio_ = getid3_lib.array_merge_noclobber(audiodata_, thisfile_audio_)
                            break
                        # end if
                        if case(GETID3_ASF_Video_Media):
                            thisfile_video_["dataformat"] = thisfile_video_["dataformat"] if (not php_empty(lambda : thisfile_video_["dataformat"])) else "asf"
                            thisfile_video_["bitrate_mode"] = thisfile_video_["bitrate_mode"] if (not php_empty(lambda : thisfile_video_["bitrate_mode"])) else "cbr"
                            break
                        # end if
                        if case(GETID3_ASF_Command_Media):
                            pass
                        # end if
                        if case():
                            break
                        # end if
                    # end for
                    thisfile_asf_["stream_properties_object"][StreamPropertiesObjectStreamNumber_] = StreamPropertiesObjectData_
                    StreamPropertiesObjectData_ = None
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
                    thisfile_asf_["header_extension_object"] = Array()
                    thisfile_asf_headerextensionobject_ = thisfile_asf_["header_extension_object"]
                    thisfile_asf_headerextensionobject_["offset"] = NextObjectOffset_ + offset_
                    thisfile_asf_headerextensionobject_["objectid"] = NextObjectGUID_
                    thisfile_asf_headerextensionobject_["objectid_guid"] = NextObjectGUIDtext_
                    thisfile_asf_headerextensionobject_["objectsize"] = NextObjectSize_
                    thisfile_asf_headerextensionobject_["reserved_1"] = php_substr(ASFHeaderData_, offset_, 16)
                    offset_ += 16
                    thisfile_asf_headerextensionobject_["reserved_1_guid"] = self.bytestringtoguid(thisfile_asf_headerextensionobject_["reserved_1"])
                    if thisfile_asf_headerextensionobject_["reserved_1"] != GETID3_ASF_Reserved_1:
                        self.warning("header_extension_object.reserved_1 GUID (" + self.bytestringtoguid(thisfile_asf_headerextensionobject_["reserved_1"]) + ") does not match expected \"GETID3_ASF_Reserved_1\" GUID (" + self.bytestringtoguid(GETID3_ASF_Reserved_1) + ")")
                        break
                    # end if
                    thisfile_asf_headerextensionobject_["reserved_2"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 2))
                    offset_ += 2
                    if thisfile_asf_headerextensionobject_["reserved_2"] != 6:
                        self.warning("header_extension_object.reserved_2 (" + getid3_lib.printhexbytes(thisfile_asf_headerextensionobject_["reserved_2"]) + ") does not match expected value of \"6\"")
                        break
                    # end if
                    thisfile_asf_headerextensionobject_["extension_data_size"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 4))
                    offset_ += 4
                    thisfile_asf_headerextensionobject_["extension_data"] = php_substr(ASFHeaderData_, offset_, thisfile_asf_headerextensionobject_["extension_data_size"])
                    unhandled_sections_ = 0
                    thisfile_asf_headerextensionobject_["extension_data_parsed"] = self.headerextensionobjectdataparse(thisfile_asf_headerextensionobject_["extension_data"], unhandled_sections_)
                    if unhandled_sections_ == 0:
                        thisfile_asf_headerextensionobject_["extension_data"] = None
                    # end if
                    offset_ += thisfile_asf_headerextensionobject_["extension_data_size"]
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
                    thisfile_asf_["codec_list_object"] = Array()
                    thisfile_asf_codeclistobject_ = thisfile_asf_["codec_list_object"]
                    thisfile_asf_codeclistobject_["offset"] = NextObjectOffset_ + offset_
                    thisfile_asf_codeclistobject_["objectid"] = NextObjectGUID_
                    thisfile_asf_codeclistobject_["objectid_guid"] = NextObjectGUIDtext_
                    thisfile_asf_codeclistobject_["objectsize"] = NextObjectSize_
                    thisfile_asf_codeclistobject_["reserved"] = php_substr(ASFHeaderData_, offset_, 16)
                    offset_ += 16
                    thisfile_asf_codeclistobject_["reserved_guid"] = self.bytestringtoguid(thisfile_asf_codeclistobject_["reserved"])
                    if thisfile_asf_codeclistobject_["reserved"] != self.guidtobytestring("86D15241-311D-11D0-A3A4-00A0C90348F6"):
                        self.warning("codec_list_object.reserved GUID {" + self.bytestringtoguid(thisfile_asf_codeclistobject_["reserved"]) + "} does not match expected \"GETID3_ASF_Reserved_1\" GUID {86D15241-311D-11D0-A3A4-00A0C90348F6}")
                        break
                    # end if
                    thisfile_asf_codeclistobject_["codec_entries_count"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 4))
                    offset_ += 4
                    CodecEntryCounter_ = 0
                    while CodecEntryCounter_ < thisfile_asf_codeclistobject_["codec_entries_count"]:
                        
                        #// shortcut
                        thisfile_asf_codeclistobject_["codec_entries"][CodecEntryCounter_] = Array()
                        thisfile_asf_codeclistobject_codecentries_current_ = thisfile_asf_codeclistobject_["codec_entries"][CodecEntryCounter_]
                        thisfile_asf_codeclistobject_codecentries_current_["type_raw"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 2))
                        offset_ += 2
                        thisfile_asf_codeclistobject_codecentries_current_["type"] = self.codeclistobjecttypelookup(thisfile_asf_codeclistobject_codecentries_current_["type_raw"])
                        CodecNameLength_ = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 2)) * 2
                        #// 2 bytes per character
                        offset_ += 2
                        thisfile_asf_codeclistobject_codecentries_current_["name"] = php_substr(ASFHeaderData_, offset_, CodecNameLength_)
                        offset_ += CodecNameLength_
                        CodecDescriptionLength_ = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 2)) * 2
                        #// 2 bytes per character
                        offset_ += 2
                        thisfile_asf_codeclistobject_codecentries_current_["description"] = php_substr(ASFHeaderData_, offset_, CodecDescriptionLength_)
                        offset_ += CodecDescriptionLength_
                        CodecInformationLength_ = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 2))
                        offset_ += 2
                        thisfile_asf_codeclistobject_codecentries_current_["information"] = php_substr(ASFHeaderData_, offset_, CodecInformationLength_)
                        offset_ += CodecInformationLength_
                        if thisfile_asf_codeclistobject_codecentries_current_["type_raw"] == 2:
                            #// audio codec
                            if php_strpos(thisfile_asf_codeclistobject_codecentries_current_["description"], ",") == False:
                                self.warning("[asf][codec_list_object][codec_entries][" + CodecEntryCounter_ + "][description] expected to contain comma-separated list of parameters: \"" + thisfile_asf_codeclistobject_codecentries_current_["description"] + "\"")
                            else:
                                AudioCodecBitrate_, AudioCodecFrequency_, AudioCodecChannels_ = php_explode(",", self.trimconvert(thisfile_asf_codeclistobject_codecentries_current_["description"]))
                                thisfile_audio_["codec"] = self.trimconvert(thisfile_asf_codeclistobject_codecentries_current_["name"])
                                if (not (php_isset(lambda : thisfile_audio_["bitrate"]))) and php_strstr(AudioCodecBitrate_, "kbps"):
                                    thisfile_audio_["bitrate"] = php_int(php_trim(php_str_replace("kbps", "", AudioCodecBitrate_)) * 1000)
                                # end if
                                #// if (!isset($thisfile_video['bitrate']) && isset($thisfile_audio['bitrate']) && isset($thisfile_asf['file_properties_object']['max_bitrate']) && ($thisfile_asf_codeclistobject['codec_entries_count'] > 1)) {
                                if php_empty(lambda : thisfile_video_["bitrate"]) and (not php_empty(lambda : thisfile_audio_["bitrate"])) and (not php_empty(lambda : info_["bitrate"])):
                                    #// $thisfile_video['bitrate'] = $thisfile_asf['file_properties_object']['max_bitrate'] - $thisfile_audio['bitrate'];
                                    thisfile_video_["bitrate"] = info_["bitrate"] - thisfile_audio_["bitrate"]
                                # end if
                                AudioCodecFrequency_ = php_int(php_trim(php_str_replace("kHz", "", AudioCodecFrequency_)))
                                for case in Switch(AudioCodecFrequency_):
                                    if case(8):
                                        pass
                                    # end if
                                    if case(8000):
                                        thisfile_audio_["sample_rate"] = 8000
                                        break
                                    # end if
                                    if case(11):
                                        pass
                                    # end if
                                    if case(11025):
                                        thisfile_audio_["sample_rate"] = 11025
                                        break
                                    # end if
                                    if case(12):
                                        pass
                                    # end if
                                    if case(12000):
                                        thisfile_audio_["sample_rate"] = 12000
                                        break
                                    # end if
                                    if case(16):
                                        pass
                                    # end if
                                    if case(16000):
                                        thisfile_audio_["sample_rate"] = 16000
                                        break
                                    # end if
                                    if case(22):
                                        pass
                                    # end if
                                    if case(22050):
                                        thisfile_audio_["sample_rate"] = 22050
                                        break
                                    # end if
                                    if case(24):
                                        pass
                                    # end if
                                    if case(24000):
                                        thisfile_audio_["sample_rate"] = 24000
                                        break
                                    # end if
                                    if case(32):
                                        pass
                                    # end if
                                    if case(32000):
                                        thisfile_audio_["sample_rate"] = 32000
                                        break
                                    # end if
                                    if case(44):
                                        pass
                                    # end if
                                    if case(441000):
                                        thisfile_audio_["sample_rate"] = 44100
                                        break
                                    # end if
                                    if case(48):
                                        pass
                                    # end if
                                    if case(48000):
                                        thisfile_audio_["sample_rate"] = 48000
                                        break
                                    # end if
                                    if case():
                                        self.warning("unknown frequency: \"" + AudioCodecFrequency_ + "\" (" + self.trimconvert(thisfile_asf_codeclistobject_codecentries_current_["description"]) + ")")
                                        break
                                    # end if
                                # end for
                                if (not (php_isset(lambda : thisfile_audio_["channels"]))):
                                    if php_strstr(AudioCodecChannels_, "stereo"):
                                        thisfile_audio_["channels"] = 2
                                    elif php_strstr(AudioCodecChannels_, "mono"):
                                        thisfile_audio_["channels"] = 1
                                    # end if
                                # end if
                            # end if
                        # end if
                        CodecEntryCounter_ += 1
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
                    thisfile_asf_["script_command_object"] = Array()
                    thisfile_asf_scriptcommandobject_ = thisfile_asf_["script_command_object"]
                    thisfile_asf_scriptcommandobject_["offset"] = NextObjectOffset_ + offset_
                    thisfile_asf_scriptcommandobject_["objectid"] = NextObjectGUID_
                    thisfile_asf_scriptcommandobject_["objectid_guid"] = NextObjectGUIDtext_
                    thisfile_asf_scriptcommandobject_["objectsize"] = NextObjectSize_
                    thisfile_asf_scriptcommandobject_["reserved"] = php_substr(ASFHeaderData_, offset_, 16)
                    offset_ += 16
                    thisfile_asf_scriptcommandobject_["reserved_guid"] = self.bytestringtoguid(thisfile_asf_scriptcommandobject_["reserved"])
                    if thisfile_asf_scriptcommandobject_["reserved"] != self.guidtobytestring("4B1ACBE3-100B-11D0-A39B-00A0C90348F6"):
                        self.warning("script_command_object.reserved GUID {" + self.bytestringtoguid(thisfile_asf_scriptcommandobject_["reserved"]) + "} does not match expected \"GETID3_ASF_Reserved_1\" GUID {4B1ACBE3-100B-11D0-A39B-00A0C90348F6}")
                        break
                    # end if
                    thisfile_asf_scriptcommandobject_["commands_count"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 2))
                    offset_ += 2
                    thisfile_asf_scriptcommandobject_["command_types_count"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 2))
                    offset_ += 2
                    CommandTypesCounter_ = 0
                    while CommandTypesCounter_ < thisfile_asf_scriptcommandobject_["command_types_count"]:
                        
                        CommandTypeNameLength_ = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 2)) * 2
                        #// 2 bytes per character
                        offset_ += 2
                        thisfile_asf_scriptcommandobject_["command_types"][CommandTypesCounter_]["name"] = php_substr(ASFHeaderData_, offset_, CommandTypeNameLength_)
                        offset_ += CommandTypeNameLength_
                        CommandTypesCounter_ += 1
                    # end while
                    CommandsCounter_ = 0
                    while CommandsCounter_ < thisfile_asf_scriptcommandobject_["commands_count"]:
                        
                        thisfile_asf_scriptcommandobject_["commands"][CommandsCounter_]["presentation_time"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 4))
                        offset_ += 4
                        thisfile_asf_scriptcommandobject_["commands"][CommandsCounter_]["type_index"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 2))
                        offset_ += 2
                        CommandTypeNameLength_ = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 2)) * 2
                        #// 2 bytes per character
                        offset_ += 2
                        thisfile_asf_scriptcommandobject_["commands"][CommandsCounter_]["name"] = php_substr(ASFHeaderData_, offset_, CommandTypeNameLength_)
                        offset_ += CommandTypeNameLength_
                        CommandsCounter_ += 1
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
                    thisfile_asf_["marker_object"] = Array()
                    thisfile_asf_markerobject_ = thisfile_asf_["marker_object"]
                    thisfile_asf_markerobject_["offset"] = NextObjectOffset_ + offset_
                    thisfile_asf_markerobject_["objectid"] = NextObjectGUID_
                    thisfile_asf_markerobject_["objectid_guid"] = NextObjectGUIDtext_
                    thisfile_asf_markerobject_["objectsize"] = NextObjectSize_
                    thisfile_asf_markerobject_["reserved"] = php_substr(ASFHeaderData_, offset_, 16)
                    offset_ += 16
                    thisfile_asf_markerobject_["reserved_guid"] = self.bytestringtoguid(thisfile_asf_markerobject_["reserved"])
                    if thisfile_asf_markerobject_["reserved"] != self.guidtobytestring("4CFEDB20-75F6-11CF-9C0F-00A0C90349CB"):
                        self.warning("marker_object.reserved GUID {" + self.bytestringtoguid(thisfile_asf_markerobject_["reserved_1"]) + "} does not match expected \"GETID3_ASF_Reserved_1\" GUID {4CFEDB20-75F6-11CF-9C0F-00A0C90349CB}")
                        break
                    # end if
                    thisfile_asf_markerobject_["markers_count"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 4))
                    offset_ += 4
                    thisfile_asf_markerobject_["reserved_2"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 2))
                    offset_ += 2
                    if thisfile_asf_markerobject_["reserved_2"] != 0:
                        self.warning("marker_object.reserved_2 (" + getid3_lib.printhexbytes(thisfile_asf_markerobject_["reserved_2"]) + ") does not match expected value of \"0\"")
                        break
                    # end if
                    thisfile_asf_markerobject_["name_length"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 2))
                    offset_ += 2
                    thisfile_asf_markerobject_["name"] = php_substr(ASFHeaderData_, offset_, thisfile_asf_markerobject_["name_length"])
                    offset_ += thisfile_asf_markerobject_["name_length"]
                    MarkersCounter_ = 0
                    while MarkersCounter_ < thisfile_asf_markerobject_["markers_count"]:
                        
                        thisfile_asf_markerobject_["markers"][MarkersCounter_]["offset"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 8))
                        offset_ += 8
                        thisfile_asf_markerobject_["markers"][MarkersCounter_]["presentation_time"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 8))
                        offset_ += 8
                        thisfile_asf_markerobject_["markers"][MarkersCounter_]["entry_length"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 2))
                        offset_ += 2
                        thisfile_asf_markerobject_["markers"][MarkersCounter_]["send_time"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 4))
                        offset_ += 4
                        thisfile_asf_markerobject_["markers"][MarkersCounter_]["flags"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 4))
                        offset_ += 4
                        thisfile_asf_markerobject_["markers"][MarkersCounter_]["marker_description_length"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 4))
                        offset_ += 4
                        thisfile_asf_markerobject_["markers"][MarkersCounter_]["marker_description"] = php_substr(ASFHeaderData_, offset_, thisfile_asf_markerobject_["markers"][MarkersCounter_]["marker_description_length"])
                        offset_ += thisfile_asf_markerobject_["markers"][MarkersCounter_]["marker_description_length"]
                        PaddingLength_ = thisfile_asf_markerobject_["markers"][MarkersCounter_]["entry_length"] - 4 - 4 - 4 - thisfile_asf_markerobject_["markers"][MarkersCounter_]["marker_description_length"]
                        if PaddingLength_ > 0:
                            thisfile_asf_markerobject_["markers"][MarkersCounter_]["padding"] = php_substr(ASFHeaderData_, offset_, PaddingLength_)
                            offset_ += PaddingLength_
                        # end if
                        MarkersCounter_ += 1
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
                    thisfile_asf_["bitrate_mutual_exclusion_object"] = Array()
                    thisfile_asf_bitratemutualexclusionobject_ = thisfile_asf_["bitrate_mutual_exclusion_object"]
                    thisfile_asf_bitratemutualexclusionobject_["offset"] = NextObjectOffset_ + offset_
                    thisfile_asf_bitratemutualexclusionobject_["objectid"] = NextObjectGUID_
                    thisfile_asf_bitratemutualexclusionobject_["objectid_guid"] = NextObjectGUIDtext_
                    thisfile_asf_bitratemutualexclusionobject_["objectsize"] = NextObjectSize_
                    thisfile_asf_bitratemutualexclusionobject_["reserved"] = php_substr(ASFHeaderData_, offset_, 16)
                    thisfile_asf_bitratemutualexclusionobject_["reserved_guid"] = self.bytestringtoguid(thisfile_asf_bitratemutualexclusionobject_["reserved"])
                    offset_ += 16
                    if thisfile_asf_bitratemutualexclusionobject_["reserved"] != GETID3_ASF_Mutex_Bitrate and thisfile_asf_bitratemutualexclusionobject_["reserved"] != GETID3_ASF_Mutex_Unknown:
                        self.warning("bitrate_mutual_exclusion_object.reserved GUID {" + self.bytestringtoguid(thisfile_asf_bitratemutualexclusionobject_["reserved"]) + "} does not match expected \"GETID3_ASF_Mutex_Bitrate\" GUID {" + self.bytestringtoguid(GETID3_ASF_Mutex_Bitrate) + "} or  \"GETID3_ASF_Mutex_Unknown\" GUID {" + self.bytestringtoguid(GETID3_ASF_Mutex_Unknown) + "}")
                        break
                    # end if
                    thisfile_asf_bitratemutualexclusionobject_["stream_numbers_count"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 2))
                    offset_ += 2
                    StreamNumberCounter_ = 0
                    while StreamNumberCounter_ < thisfile_asf_bitratemutualexclusionobject_["stream_numbers_count"]:
                        
                        thisfile_asf_bitratemutualexclusionobject_["stream_numbers"][StreamNumberCounter_] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 2))
                        offset_ += 2
                        StreamNumberCounter_ += 1
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
                    thisfile_asf_["error_correction_object"] = Array()
                    thisfile_asf_errorcorrectionobject_ = thisfile_asf_["error_correction_object"]
                    thisfile_asf_errorcorrectionobject_["offset"] = NextObjectOffset_ + offset_
                    thisfile_asf_errorcorrectionobject_["objectid"] = NextObjectGUID_
                    thisfile_asf_errorcorrectionobject_["objectid_guid"] = NextObjectGUIDtext_
                    thisfile_asf_errorcorrectionobject_["objectsize"] = NextObjectSize_
                    thisfile_asf_errorcorrectionobject_["error_correction_type"] = php_substr(ASFHeaderData_, offset_, 16)
                    offset_ += 16
                    thisfile_asf_errorcorrectionobject_["error_correction_guid"] = self.bytestringtoguid(thisfile_asf_errorcorrectionobject_["error_correction_type"])
                    thisfile_asf_errorcorrectionobject_["error_correction_data_length"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 4))
                    offset_ += 4
                    for case in Switch(thisfile_asf_errorcorrectionobject_["error_correction_type"]):
                        if case(GETID3_ASF_No_Error_Correction):
                            #// should be no data, but just in case there is, skip to the end of the field
                            offset_ += thisfile_asf_errorcorrectionobject_["error_correction_data_length"]
                            break
                        # end if
                        if case(GETID3_ASF_Audio_Spread):
                            #// Field Name                   Field Type   Size (bits)
                            #// Span                         BYTE         8               // number of packets over which audio will be spread.
                            #// Virtual Packet Length        WORD         16              // size of largest audio payload found in audio stream
                            #// Virtual Chunk Length         WORD         16              // size of largest audio payload found in audio stream
                            #// Silence Data Length          WORD         16              // number of bytes in Silence Data field
                            #// Silence Data                 BYTESTREAM   variable        // hardcoded: 0x00 * (Silence Data Length) bytes
                            thisfile_asf_errorcorrectionobject_["span"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 1))
                            offset_ += 1
                            thisfile_asf_errorcorrectionobject_["virtual_packet_length"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 2))
                            offset_ += 2
                            thisfile_asf_errorcorrectionobject_["virtual_chunk_length"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 2))
                            offset_ += 2
                            thisfile_asf_errorcorrectionobject_["silence_data_length"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 2))
                            offset_ += 2
                            thisfile_asf_errorcorrectionobject_["silence_data"] = php_substr(ASFHeaderData_, offset_, thisfile_asf_errorcorrectionobject_["silence_data_length"])
                            offset_ += thisfile_asf_errorcorrectionobject_["silence_data_length"]
                            break
                        # end if
                        if case():
                            self.warning("error_correction_object.error_correction_type GUID {" + self.bytestringtoguid(thisfile_asf_errorcorrectionobject_["reserved"]) + "} does not match expected \"GETID3_ASF_No_Error_Correction\" GUID {" + self.bytestringtoguid(GETID3_ASF_No_Error_Correction) + "} or  \"GETID3_ASF_Audio_Spread\" GUID {" + self.bytestringtoguid(GETID3_ASF_Audio_Spread) + "}")
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
                    thisfile_asf_["content_description_object"] = Array()
                    thisfile_asf_contentdescriptionobject_ = thisfile_asf_["content_description_object"]
                    thisfile_asf_contentdescriptionobject_["offset"] = NextObjectOffset_ + offset_
                    thisfile_asf_contentdescriptionobject_["objectid"] = NextObjectGUID_
                    thisfile_asf_contentdescriptionobject_["objectid_guid"] = NextObjectGUIDtext_
                    thisfile_asf_contentdescriptionobject_["objectsize"] = NextObjectSize_
                    thisfile_asf_contentdescriptionobject_["title_length"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 2))
                    offset_ += 2
                    thisfile_asf_contentdescriptionobject_["author_length"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 2))
                    offset_ += 2
                    thisfile_asf_contentdescriptionobject_["copyright_length"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 2))
                    offset_ += 2
                    thisfile_asf_contentdescriptionobject_["description_length"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 2))
                    offset_ += 2
                    thisfile_asf_contentdescriptionobject_["rating_length"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 2))
                    offset_ += 2
                    thisfile_asf_contentdescriptionobject_["title"] = php_substr(ASFHeaderData_, offset_, thisfile_asf_contentdescriptionobject_["title_length"])
                    offset_ += thisfile_asf_contentdescriptionobject_["title_length"]
                    thisfile_asf_contentdescriptionobject_["author"] = php_substr(ASFHeaderData_, offset_, thisfile_asf_contentdescriptionobject_["author_length"])
                    offset_ += thisfile_asf_contentdescriptionobject_["author_length"]
                    thisfile_asf_contentdescriptionobject_["copyright"] = php_substr(ASFHeaderData_, offset_, thisfile_asf_contentdescriptionobject_["copyright_length"])
                    offset_ += thisfile_asf_contentdescriptionobject_["copyright_length"]
                    thisfile_asf_contentdescriptionobject_["description"] = php_substr(ASFHeaderData_, offset_, thisfile_asf_contentdescriptionobject_["description_length"])
                    offset_ += thisfile_asf_contentdescriptionobject_["description_length"]
                    thisfile_asf_contentdescriptionobject_["rating"] = php_substr(ASFHeaderData_, offset_, thisfile_asf_contentdescriptionobject_["rating_length"])
                    offset_ += thisfile_asf_contentdescriptionobject_["rating_length"]
                    ASFcommentKeysToCopy_ = Array({"title": "title", "author": "artist", "copyright": "copyright", "description": "comment", "rating": "rating"})
                    for keytocopyfrom_,keytocopyto_ in ASFcommentKeysToCopy_.items():
                        if (not php_empty(lambda : thisfile_asf_contentdescriptionobject_[keytocopyfrom_])):
                            thisfile_asf_comments_[keytocopyto_][-1] = self.trimterm(thisfile_asf_contentdescriptionobject_[keytocopyfrom_])
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
                    thisfile_asf_["extended_content_description_object"] = Array()
                    thisfile_asf_extendedcontentdescriptionobject_ = thisfile_asf_["extended_content_description_object"]
                    thisfile_asf_extendedcontentdescriptionobject_["offset"] = NextObjectOffset_ + offset_
                    thisfile_asf_extendedcontentdescriptionobject_["objectid"] = NextObjectGUID_
                    thisfile_asf_extendedcontentdescriptionobject_["objectid_guid"] = NextObjectGUIDtext_
                    thisfile_asf_extendedcontentdescriptionobject_["objectsize"] = NextObjectSize_
                    thisfile_asf_extendedcontentdescriptionobject_["content_descriptors_count"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 2))
                    offset_ += 2
                    ExtendedContentDescriptorsCounter_ = 0
                    while ExtendedContentDescriptorsCounter_ < thisfile_asf_extendedcontentdescriptionobject_["content_descriptors_count"]:
                        
                        #// shortcut
                        thisfile_asf_extendedcontentdescriptionobject_["content_descriptors"][ExtendedContentDescriptorsCounter_] = Array()
                        thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_ = thisfile_asf_extendedcontentdescriptionobject_["content_descriptors"][ExtendedContentDescriptorsCounter_]
                        thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["base_offset"] = offset_ + 30
                        thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["name_length"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 2))
                        offset_ += 2
                        thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["name"] = php_substr(ASFHeaderData_, offset_, thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["name_length"])
                        offset_ += thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["name_length"]
                        thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["value_type"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 2))
                        offset_ += 2
                        thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["value_length"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 2))
                        offset_ += 2
                        thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["value"] = php_substr(ASFHeaderData_, offset_, thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["value_length"])
                        offset_ += thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["value_length"]
                        for case in Switch(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["value_type"]):
                            if case(0):
                                break
                            # end if
                            if case(1):
                                break
                            # end if
                            if case(2):
                                #// BOOL
                                thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["value"] = php_bool(getid3_lib.littleendian2int(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["value"]))
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
                                thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["value"] = getid3_lib.littleendian2int(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["value"])
                                break
                            # end if
                            if case():
                                self.warning("extended_content_description.content_descriptors." + ExtendedContentDescriptorsCounter_ + ".value_type is invalid (" + thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["value_type"] + ")")
                                break
                            # end if
                        # end for
                        for case in Switch(self.trimconvert(php_strtolower(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["name"]))):
                            if case("wm/albumartist"):
                                pass
                            # end if
                            if case("artist"):
                                #// Note: not 'artist', that comes from 'author' tag
                                thisfile_asf_comments_["albumartist"] = Array(self.trimterm(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["value"]))
                                break
                            # end if
                            if case("wm/albumtitle"):
                                pass
                            # end if
                            if case("album"):
                                thisfile_asf_comments_["album"] = Array(self.trimterm(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["value"]))
                                break
                            # end if
                            if case("wm/genre"):
                                pass
                            # end if
                            if case("genre"):
                                thisfile_asf_comments_["genre"] = Array(self.trimterm(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["value"]))
                                break
                            # end if
                            if case("wm/partofset"):
                                thisfile_asf_comments_["partofset"] = Array(self.trimterm(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["value"]))
                                break
                            # end if
                            if case("wm/tracknumber"):
                                pass
                            # end if
                            if case("tracknumber"):
                                #// be careful casting to int: casting unicode strings to int gives unexpected results (stops parsing at first non-numeric character)
                                thisfile_asf_comments_["track_number"] = Array(self.trimterm(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["value"]))
                                for key_,value_ in thisfile_asf_comments_["track_number"].items():
                                    if php_preg_match("/^[0-9\\x00]+$/", value_):
                                        thisfile_asf_comments_["track_number"][key_] = php_intval(php_str_replace(" ", "", value_))
                                    # end if
                                # end for
                                break
                            # end if
                            if case("wm/track"):
                                if php_empty(lambda : thisfile_asf_comments_["track_number"]):
                                    thisfile_asf_comments_["track_number"] = Array(1 + self.trimconvert(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["value"]))
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
                                thisfile_asf_comments_["year"] = Array(self.trimterm(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["value"]))
                                break
                            # end if
                            if case("wm/lyrics"):
                                pass
                            # end if
                            if case("lyrics"):
                                thisfile_asf_comments_["lyrics"] = Array(self.trimterm(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["value"]))
                                break
                            # end if
                            if case("isvbr"):
                                if thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["value"]:
                                    thisfile_audio_["bitrate_mode"] = "vbr"
                                    thisfile_video_["bitrate_mode"] = "vbr"
                                # end if
                                break
                            # end if
                            if case("id3"):
                                self.getid3.include_module("tag.id3v2")
                                getid3_id3v2_ = php_new_class("getid3_id3v2", lambda : getid3_id3v2(self.getid3))
                                getid3_id3v2_.analyzestring(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["value"])
                                getid3_id3v2_ = None
                                if thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["value_length"] > 1024:
                                    thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["value"] = "<value too large to display>"
                                # end if
                                break
                            # end if
                            if case("wm/encodingtime"):
                                thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["encoding_time_unix"] = self.filetimetounixtime(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["value"])
                                thisfile_asf_comments_["encoding_time_unix"] = Array(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["encoding_time_unix"])
                                break
                            # end if
                            if case("wm/picture"):
                                WMpicture_ = self.asf_wmpicture(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["value"])
                                for key_,value_ in WMpicture_.items():
                                    thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_[key_] = value_
                                # end for
                                WMpicture_ = None
                                break
                            # end if
                            if case():
                                for case in Switch(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["value_type"]):
                                    if case(0):
                                        #// Unicode string
                                        if php_substr(self.trimconvert(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["name"]), 0, 3) == "WM/":
                                            thisfile_asf_comments_[php_str_replace("wm/", "", php_strtolower(self.trimconvert(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["name"])))] = Array(self.trimterm(thisfile_asf_extendedcontentdescriptionobject_contentdescriptor_current_["value"]))
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
                        ExtendedContentDescriptorsCounter_ += 1
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
                    thisfile_asf_["stream_bitrate_properties_object"] = Array()
                    thisfile_asf_streambitratepropertiesobject_ = thisfile_asf_["stream_bitrate_properties_object"]
                    thisfile_asf_streambitratepropertiesobject_["offset"] = NextObjectOffset_ + offset_
                    thisfile_asf_streambitratepropertiesobject_["objectid"] = NextObjectGUID_
                    thisfile_asf_streambitratepropertiesobject_["objectid_guid"] = NextObjectGUIDtext_
                    thisfile_asf_streambitratepropertiesobject_["objectsize"] = NextObjectSize_
                    thisfile_asf_streambitratepropertiesobject_["bitrate_records_count"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 2))
                    offset_ += 2
                    BitrateRecordsCounter_ = 0
                    while BitrateRecordsCounter_ < thisfile_asf_streambitratepropertiesobject_["bitrate_records_count"]:
                        
                        thisfile_asf_streambitratepropertiesobject_["bitrate_records"][BitrateRecordsCounter_]["flags_raw"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 2))
                        offset_ += 2
                        thisfile_asf_streambitratepropertiesobject_["bitrate_records"][BitrateRecordsCounter_]["flags"]["stream_number"] = thisfile_asf_streambitratepropertiesobject_["bitrate_records"][BitrateRecordsCounter_]["flags_raw"] & 127
                        thisfile_asf_streambitratepropertiesobject_["bitrate_records"][BitrateRecordsCounter_]["bitrate"] = getid3_lib.littleendian2int(php_substr(ASFHeaderData_, offset_, 4))
                        offset_ += 4
                        BitrateRecordsCounter_ += 1
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
                    thisfile_asf_["padding_object"] = Array()
                    thisfile_asf_paddingobject_ = thisfile_asf_["padding_object"]
                    thisfile_asf_paddingobject_["offset"] = NextObjectOffset_ + offset_
                    thisfile_asf_paddingobject_["objectid"] = NextObjectGUID_
                    thisfile_asf_paddingobject_["objectid_guid"] = NextObjectGUIDtext_
                    thisfile_asf_paddingobject_["objectsize"] = NextObjectSize_
                    thisfile_asf_paddingobject_["padding_length"] = thisfile_asf_paddingobject_["objectsize"] - 16 - 8
                    thisfile_asf_paddingobject_["padding"] = php_substr(ASFHeaderData_, offset_, thisfile_asf_paddingobject_["padding_length"])
                    offset_ += NextObjectSize_ - 16 - 8
                    break
                # end if
                if case(GETID3_ASF_Extended_Content_Encryption_Object):
                    pass
                # end if
                if case(GETID3_ASF_Content_Encryption_Object):
                    #// WMA DRM - just ignore
                    offset_ += NextObjectSize_ - 16 - 8
                    break
                # end if
                if case():
                    #// Implementations shall ignore any standard or non-standard object that they do not know how to handle.
                    if self.guidname(NextObjectGUIDtext_):
                        self.warning("unhandled GUID \"" + self.guidname(NextObjectGUIDtext_) + "\" {" + NextObjectGUIDtext_ + "} in ASF header at offset " + offset_ - 16 - 8)
                    else:
                        self.warning("unknown GUID {" + NextObjectGUIDtext_ + "} in ASF header at offset " + offset_ - 16 - 8)
                    # end if
                    offset_ += NextObjectSize_ - 16 - 8
                    break
                # end if
            # end for
            HeaderObjectsCounter_ += 1
        # end while
        if (php_isset(lambda : thisfile_asf_streambitratepropertiesobject_["bitrate_records_count"])):
            ASFbitrateAudio_ = 0
            ASFbitrateVideo_ = 0
            BitrateRecordsCounter_ = 0
            while BitrateRecordsCounter_ < thisfile_asf_streambitratepropertiesobject_["bitrate_records_count"]:
                
                if (php_isset(lambda : thisfile_asf_codeclistobject_["codec_entries"][BitrateRecordsCounter_])):
                    for case in Switch(thisfile_asf_codeclistobject_["codec_entries"][BitrateRecordsCounter_]["type_raw"]):
                        if case(1):
                            ASFbitrateVideo_ += thisfile_asf_streambitratepropertiesobject_["bitrate_records"][BitrateRecordsCounter_]["bitrate"]
                            break
                        # end if
                        if case(2):
                            ASFbitrateAudio_ += thisfile_asf_streambitratepropertiesobject_["bitrate_records"][BitrateRecordsCounter_]["bitrate"]
                            break
                        # end if
                        if case():
                            break
                        # end if
                    # end for
                # end if
                BitrateRecordsCounter_ += 1
            # end while
            if ASFbitrateAudio_ > 0:
                thisfile_audio_["bitrate"] = ASFbitrateAudio_
            # end if
            if ASFbitrateVideo_ > 0:
                thisfile_video_["bitrate"] = ASFbitrateVideo_
            # end if
        # end if
        if (php_isset(lambda : thisfile_asf_["stream_properties_object"])) and php_is_array(thisfile_asf_["stream_properties_object"]):
            thisfile_audio_["bitrate"] = 0
            thisfile_video_["bitrate"] = 0
            for streamnumber_,streamdata_ in thisfile_asf_["stream_properties_object"].items():
                for case in Switch(streamdata_["stream_type"]):
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
                        thisfile_asf_["audio_media"][streamnumber_] = Array()
                        thisfile_asf_audiomedia_currentstream_ = thisfile_asf_["audio_media"][streamnumber_]
                        audiomediaoffset_ = 0
                        thisfile_asf_audiomedia_currentstream_ = getid3_riff.parsewaveformatex(php_substr(streamdata_["type_specific_data"], audiomediaoffset_, 16))
                        audiomediaoffset_ += 16
                        thisfile_audio_["lossless"] = False
                        for case in Switch(thisfile_asf_audiomedia_currentstream_["raw"]["wFormatTag"]):
                            if case(1):
                                pass
                            # end if
                            if case(355):
                                #// WMA9 Lossless
                                thisfile_audio_["lossless"] = True
                                break
                            # end if
                        # end for
                        if (not php_empty(lambda : thisfile_asf_["stream_bitrate_properties_object"]["bitrate_records"])):
                            for dummy_,dataarray_ in thisfile_asf_["stream_bitrate_properties_object"]["bitrate_records"].items():
                                if (php_isset(lambda : dataarray_["flags"]["stream_number"])) and dataarray_["flags"]["stream_number"] == streamnumber_:
                                    thisfile_asf_audiomedia_currentstream_["bitrate"] = dataarray_["bitrate"]
                                    thisfile_audio_["bitrate"] += dataarray_["bitrate"]
                                    break
                                # end if
                            # end for
                        else:
                            if (not php_empty(lambda : thisfile_asf_audiomedia_currentstream_["bytes_sec"])):
                                thisfile_audio_["bitrate"] += thisfile_asf_audiomedia_currentstream_["bytes_sec"] * 8
                            elif (not php_empty(lambda : thisfile_asf_audiomedia_currentstream_["bitrate"])):
                                thisfile_audio_["bitrate"] += thisfile_asf_audiomedia_currentstream_["bitrate"]
                            # end if
                        # end if
                        thisfile_audio_["streams"][streamnumber_] = thisfile_asf_audiomedia_currentstream_
                        thisfile_audio_["streams"][streamnumber_]["wformattag"] = thisfile_asf_audiomedia_currentstream_["raw"]["wFormatTag"]
                        thisfile_audio_["streams"][streamnumber_]["lossless"] = thisfile_audio_["lossless"]
                        thisfile_audio_["streams"][streamnumber_]["bitrate"] = thisfile_audio_["bitrate"]
                        thisfile_audio_["streams"][streamnumber_]["dataformat"] = "wma"
                        thisfile_audio_["streams"][streamnumber_]["raw"] = None
                        thisfile_asf_audiomedia_currentstream_["codec_data_size"] = getid3_lib.littleendian2int(php_substr(streamdata_["type_specific_data"], audiomediaoffset_, 2))
                        audiomediaoffset_ += 2
                        thisfile_asf_audiomedia_currentstream_["codec_data"] = php_substr(streamdata_["type_specific_data"], audiomediaoffset_, thisfile_asf_audiomedia_currentstream_["codec_data_size"])
                        audiomediaoffset_ += thisfile_asf_audiomedia_currentstream_["codec_data_size"]
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
                        thisfile_asf_["video_media"][streamnumber_] = Array()
                        thisfile_asf_videomedia_currentstream_ = thisfile_asf_["video_media"][streamnumber_]
                        videomediaoffset_ = 0
                        thisfile_asf_videomedia_currentstream_["image_width"] = getid3_lib.littleendian2int(php_substr(streamdata_["type_specific_data"], videomediaoffset_, 4))
                        videomediaoffset_ += 4
                        thisfile_asf_videomedia_currentstream_["image_height"] = getid3_lib.littleendian2int(php_substr(streamdata_["type_specific_data"], videomediaoffset_, 4))
                        videomediaoffset_ += 4
                        thisfile_asf_videomedia_currentstream_["flags"] = getid3_lib.littleendian2int(php_substr(streamdata_["type_specific_data"], videomediaoffset_, 1))
                        videomediaoffset_ += 1
                        thisfile_asf_videomedia_currentstream_["format_data_size"] = getid3_lib.littleendian2int(php_substr(streamdata_["type_specific_data"], videomediaoffset_, 2))
                        videomediaoffset_ += 2
                        thisfile_asf_videomedia_currentstream_["format_data"]["format_data_size"] = getid3_lib.littleendian2int(php_substr(streamdata_["type_specific_data"], videomediaoffset_, 4))
                        videomediaoffset_ += 4
                        thisfile_asf_videomedia_currentstream_["format_data"]["image_width"] = getid3_lib.littleendian2int(php_substr(streamdata_["type_specific_data"], videomediaoffset_, 4))
                        videomediaoffset_ += 4
                        thisfile_asf_videomedia_currentstream_["format_data"]["image_height"] = getid3_lib.littleendian2int(php_substr(streamdata_["type_specific_data"], videomediaoffset_, 4))
                        videomediaoffset_ += 4
                        thisfile_asf_videomedia_currentstream_["format_data"]["reserved"] = getid3_lib.littleendian2int(php_substr(streamdata_["type_specific_data"], videomediaoffset_, 2))
                        videomediaoffset_ += 2
                        thisfile_asf_videomedia_currentstream_["format_data"]["bits_per_pixel"] = getid3_lib.littleendian2int(php_substr(streamdata_["type_specific_data"], videomediaoffset_, 2))
                        videomediaoffset_ += 2
                        thisfile_asf_videomedia_currentstream_["format_data"]["codec_fourcc"] = php_substr(streamdata_["type_specific_data"], videomediaoffset_, 4)
                        videomediaoffset_ += 4
                        thisfile_asf_videomedia_currentstream_["format_data"]["image_size"] = getid3_lib.littleendian2int(php_substr(streamdata_["type_specific_data"], videomediaoffset_, 4))
                        videomediaoffset_ += 4
                        thisfile_asf_videomedia_currentstream_["format_data"]["horizontal_pels"] = getid3_lib.littleendian2int(php_substr(streamdata_["type_specific_data"], videomediaoffset_, 4))
                        videomediaoffset_ += 4
                        thisfile_asf_videomedia_currentstream_["format_data"]["vertical_pels"] = getid3_lib.littleendian2int(php_substr(streamdata_["type_specific_data"], videomediaoffset_, 4))
                        videomediaoffset_ += 4
                        thisfile_asf_videomedia_currentstream_["format_data"]["colors_used"] = getid3_lib.littleendian2int(php_substr(streamdata_["type_specific_data"], videomediaoffset_, 4))
                        videomediaoffset_ += 4
                        thisfile_asf_videomedia_currentstream_["format_data"]["colors_important"] = getid3_lib.littleendian2int(php_substr(streamdata_["type_specific_data"], videomediaoffset_, 4))
                        videomediaoffset_ += 4
                        thisfile_asf_videomedia_currentstream_["format_data"]["codec_data"] = php_substr(streamdata_["type_specific_data"], videomediaoffset_)
                        if (not php_empty(lambda : thisfile_asf_["stream_bitrate_properties_object"]["bitrate_records"])):
                            for dummy_,dataarray_ in thisfile_asf_["stream_bitrate_properties_object"]["bitrate_records"].items():
                                if (php_isset(lambda : dataarray_["flags"]["stream_number"])) and dataarray_["flags"]["stream_number"] == streamnumber_:
                                    thisfile_asf_videomedia_currentstream_["bitrate"] = dataarray_["bitrate"]
                                    thisfile_video_["streams"][streamnumber_]["bitrate"] = dataarray_["bitrate"]
                                    thisfile_video_["bitrate"] += dataarray_["bitrate"]
                                    break
                                # end if
                            # end for
                        # end if
                        thisfile_asf_videomedia_currentstream_["format_data"]["codec"] = getid3_riff.fourcclookup(thisfile_asf_videomedia_currentstream_["format_data"]["codec_fourcc"])
                        thisfile_video_["streams"][streamnumber_]["fourcc"] = thisfile_asf_videomedia_currentstream_["format_data"]["codec_fourcc"]
                        thisfile_video_["streams"][streamnumber_]["codec"] = thisfile_asf_videomedia_currentstream_["format_data"]["codec"]
                        thisfile_video_["streams"][streamnumber_]["resolution_x"] = thisfile_asf_videomedia_currentstream_["image_width"]
                        thisfile_video_["streams"][streamnumber_]["resolution_y"] = thisfile_asf_videomedia_currentstream_["image_height"]
                        thisfile_video_["streams"][streamnumber_]["bits_per_sample"] = thisfile_asf_videomedia_currentstream_["format_data"]["bits_per_pixel"]
                        break
                    # end if
                    if case():
                        break
                    # end if
                # end for
            # end for
        # end if
        while True:
            
            if not (self.ftell() < info_["avdataend"]):
                break
            # end if
            NextObjectDataHeader_ = self.fread(24)
            offset_ = 0
            NextObjectGUID_ = php_substr(NextObjectDataHeader_, 0, 16)
            offset_ += 16
            NextObjectGUIDtext_ = self.bytestringtoguid(NextObjectGUID_)
            NextObjectSize_ = getid3_lib.littleendian2int(php_substr(NextObjectDataHeader_, offset_, 8))
            offset_ += 8
            for case in Switch(NextObjectGUID_):
                if case(GETID3_ASF_Data_Object):
                    #// Data Object: (mandatory, one only)
                    #// Field Name                       Field Type   Size (bits)
                    #// Object ID                        GUID         128             // GUID for Data object - GETID3_ASF_Data_Object
                    #// Object Size                      QWORD        64              // size of Data object, including 50 bytes of Data Object header. may be 0 if FilePropertiesObject.BroadcastFlag == 1
                    #// File ID                          GUID         128             // unique identifier. identical to File ID field in Header Object
                    #// Total Data Packets               QWORD        64              // number of Data Packet entries in Data Object. invalid if FilePropertiesObject.BroadcastFlag == 1
                    #// Reserved                         WORD         16              // hardcoded: 0x0101
                    #// shortcut
                    thisfile_asf_["data_object"] = Array()
                    thisfile_asf_dataobject_ = thisfile_asf_["data_object"]
                    DataObjectData_ = NextObjectDataHeader_ + self.fread(50 - 24)
                    offset_ = 24
                    thisfile_asf_dataobject_["objectid"] = NextObjectGUID_
                    thisfile_asf_dataobject_["objectid_guid"] = NextObjectGUIDtext_
                    thisfile_asf_dataobject_["objectsize"] = NextObjectSize_
                    thisfile_asf_dataobject_["fileid"] = php_substr(DataObjectData_, offset_, 16)
                    offset_ += 16
                    thisfile_asf_dataobject_["fileid_guid"] = self.bytestringtoguid(thisfile_asf_dataobject_["fileid"])
                    thisfile_asf_dataobject_["total_data_packets"] = getid3_lib.littleendian2int(php_substr(DataObjectData_, offset_, 8))
                    offset_ += 8
                    thisfile_asf_dataobject_["reserved"] = getid3_lib.littleendian2int(php_substr(DataObjectData_, offset_, 2))
                    offset_ += 2
                    if thisfile_asf_dataobject_["reserved"] != 257:
                        self.warning("data_object.reserved (" + getid3_lib.printhexbytes(thisfile_asf_dataobject_["reserved"]) + ") does not match expected value of \"0x0101\"")
                        break
                    # end if
                    #// Data Packets                     array of:    variable
                    #// Error Correction Flags         BYTE         8
                    #// Error Correction Data Length bits         4               // if Error Correction Length Type == 00, size of Error Correction Data in bytes, else hardcoded: 0000
                    #// Opaque Data Present          bits         1
                    #// Error Correction Length Type bits         2               // number of bits for size of the error correction data. hardcoded: 00
                    #// Error Correction Present     bits         1               // If set, use Opaque Data Packet structure, else use Payload structure
                    #// Error Correction Data
                    info_["avdataoffset"] = self.ftell()
                    self.fseek(thisfile_asf_dataobject_["objectsize"] - 50, SEEK_CUR)
                    #// skip actual audio/video data
                    info_["avdataend"] = self.ftell()
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
                    thisfile_asf_["simple_index_object"] = Array()
                    thisfile_asf_simpleindexobject_ = thisfile_asf_["simple_index_object"]
                    SimpleIndexObjectData_ = NextObjectDataHeader_ + self.fread(56 - 24)
                    offset_ = 24
                    thisfile_asf_simpleindexobject_["objectid"] = NextObjectGUID_
                    thisfile_asf_simpleindexobject_["objectid_guid"] = NextObjectGUIDtext_
                    thisfile_asf_simpleindexobject_["objectsize"] = NextObjectSize_
                    thisfile_asf_simpleindexobject_["fileid"] = php_substr(SimpleIndexObjectData_, offset_, 16)
                    offset_ += 16
                    thisfile_asf_simpleindexobject_["fileid_guid"] = self.bytestringtoguid(thisfile_asf_simpleindexobject_["fileid"])
                    thisfile_asf_simpleindexobject_["index_entry_time_interval"] = getid3_lib.littleendian2int(php_substr(SimpleIndexObjectData_, offset_, 8))
                    offset_ += 8
                    thisfile_asf_simpleindexobject_["maximum_packet_count"] = getid3_lib.littleendian2int(php_substr(SimpleIndexObjectData_, offset_, 4))
                    offset_ += 4
                    thisfile_asf_simpleindexobject_["index_entries_count"] = getid3_lib.littleendian2int(php_substr(SimpleIndexObjectData_, offset_, 4))
                    offset_ += 4
                    IndexEntriesData_ = SimpleIndexObjectData_ + self.fread(6 * thisfile_asf_simpleindexobject_["index_entries_count"])
                    IndexEntriesCounter_ = 0
                    while IndexEntriesCounter_ < thisfile_asf_simpleindexobject_["index_entries_count"]:
                        
                        thisfile_asf_simpleindexobject_["index_entries"][IndexEntriesCounter_]["packet_number"] = getid3_lib.littleendian2int(php_substr(IndexEntriesData_, offset_, 4))
                        offset_ += 4
                        thisfile_asf_simpleindexobject_["index_entries"][IndexEntriesCounter_]["packet_count"] = getid3_lib.littleendian2int(php_substr(IndexEntriesData_, offset_, 4))
                        offset_ += 2
                        IndexEntriesCounter_ += 1
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
                    thisfile_asf_["asf_index_object"] = Array()
                    thisfile_asf_asfindexobject_ = thisfile_asf_["asf_index_object"]
                    ASFIndexObjectData_ = NextObjectDataHeader_ + self.fread(34 - 24)
                    offset_ = 24
                    thisfile_asf_asfindexobject_["objectid"] = NextObjectGUID_
                    thisfile_asf_asfindexobject_["objectid_guid"] = NextObjectGUIDtext_
                    thisfile_asf_asfindexobject_["objectsize"] = NextObjectSize_
                    thisfile_asf_asfindexobject_["entry_time_interval"] = getid3_lib.littleendian2int(php_substr(ASFIndexObjectData_, offset_, 4))
                    offset_ += 4
                    thisfile_asf_asfindexobject_["index_specifiers_count"] = getid3_lib.littleendian2int(php_substr(ASFIndexObjectData_, offset_, 2))
                    offset_ += 2
                    thisfile_asf_asfindexobject_["index_blocks_count"] = getid3_lib.littleendian2int(php_substr(ASFIndexObjectData_, offset_, 4))
                    offset_ += 4
                    ASFIndexObjectData_ += self.fread(4 * thisfile_asf_asfindexobject_["index_specifiers_count"])
                    IndexSpecifiersCounter_ = 0
                    while IndexSpecifiersCounter_ < thisfile_asf_asfindexobject_["index_specifiers_count"]:
                        
                        IndexSpecifierStreamNumber_ = getid3_lib.littleendian2int(php_substr(ASFIndexObjectData_, offset_, 2))
                        offset_ += 2
                        thisfile_asf_asfindexobject_["index_specifiers"][IndexSpecifiersCounter_]["stream_number"] = IndexSpecifierStreamNumber_
                        thisfile_asf_asfindexobject_["index_specifiers"][IndexSpecifiersCounter_]["index_type"] = getid3_lib.littleendian2int(php_substr(ASFIndexObjectData_, offset_, 2))
                        offset_ += 2
                        thisfile_asf_asfindexobject_["index_specifiers"][IndexSpecifiersCounter_]["index_type_text"] = self.asfindexobjectindextypelookup(thisfile_asf_asfindexobject_["index_specifiers"][IndexSpecifiersCounter_]["index_type"])
                        IndexSpecifiersCounter_ += 1
                    # end while
                    ASFIndexObjectData_ += self.fread(4)
                    thisfile_asf_asfindexobject_["index_entry_count"] = getid3_lib.littleendian2int(php_substr(ASFIndexObjectData_, offset_, 4))
                    offset_ += 4
                    ASFIndexObjectData_ += self.fread(8 * thisfile_asf_asfindexobject_["index_specifiers_count"])
                    IndexSpecifiersCounter_ = 0
                    while IndexSpecifiersCounter_ < thisfile_asf_asfindexobject_["index_specifiers_count"]:
                        
                        thisfile_asf_asfindexobject_["block_positions"][IndexSpecifiersCounter_] = getid3_lib.littleendian2int(php_substr(ASFIndexObjectData_, offset_, 8))
                        offset_ += 8
                        IndexSpecifiersCounter_ += 1
                    # end while
                    ASFIndexObjectData_ += self.fread(4 * thisfile_asf_asfindexobject_["index_specifiers_count"] * thisfile_asf_asfindexobject_["index_entry_count"])
                    IndexEntryCounter_ = 0
                    while IndexEntryCounter_ < thisfile_asf_asfindexobject_["index_entry_count"]:
                        
                        IndexSpecifiersCounter_ = 0
                        while IndexSpecifiersCounter_ < thisfile_asf_asfindexobject_["index_specifiers_count"]:
                            
                            thisfile_asf_asfindexobject_["offsets"][IndexSpecifiersCounter_][IndexEntryCounter_] = getid3_lib.littleendian2int(php_substr(ASFIndexObjectData_, offset_, 4))
                            offset_ += 4
                            IndexSpecifiersCounter_ += 1
                        # end while
                        IndexEntryCounter_ += 1
                    # end while
                    break
                # end if
                if case():
                    #// Implementations shall ignore any standard or non-standard object that they do not know how to handle.
                    if self.guidname(NextObjectGUIDtext_):
                        self.warning("unhandled GUID \"" + self.guidname(NextObjectGUIDtext_) + "\" {" + NextObjectGUIDtext_ + "} in ASF body at offset " + offset_ - 16 - 8)
                    else:
                        self.warning("unknown GUID {" + NextObjectGUIDtext_ + "} in ASF body at offset " + self.ftell() - 16 - 8)
                    # end if
                    self.fseek(NextObjectSize_ - 16 - 8, SEEK_CUR)
                    break
                # end if
            # end for
        # end while
        if (php_isset(lambda : thisfile_asf_codeclistobject_["codec_entries"])) and php_is_array(thisfile_asf_codeclistobject_["codec_entries"]):
            for streamnumber_,streamdata_ in thisfile_asf_codeclistobject_["codec_entries"].items():
                for case in Switch(streamdata_["information"]):
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
                        thisfile_video_["dataformat"] = "wmv"
                        info_["mime_type"] = "video/x-ms-wmv"
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
                        thisfile_video_["dataformat"] = "asf"
                        info_["mime_type"] = "video/x-ms-asf"
                        break
                    # end if
                    if case():
                        for case in Switch(streamdata_["type_raw"]):
                            if case(1):
                                if php_strstr(self.trimconvert(streamdata_["name"]), "Windows Media"):
                                    thisfile_video_["dataformat"] = "wmv"
                                    if info_["mime_type"] == "video/x-ms-asf":
                                        info_["mime_type"] = "video/x-ms-wmv"
                                    # end if
                                # end if
                                break
                            # end if
                            if case(2):
                                if php_strstr(self.trimconvert(streamdata_["name"]), "Windows Media"):
                                    thisfile_audio_["dataformat"] = "wma"
                                    if info_["mime_type"] == "video/x-ms-asf":
                                        info_["mime_type"] = "audio/x-ms-wma"
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
        for case in Switch(thisfile_audio_["codec"] if (php_isset(lambda : thisfile_audio_["codec"])) else ""):
            if case("MPEG Layer-3"):
                thisfile_audio_["dataformat"] = "mp3"
                break
            # end if
            if case():
                break
            # end if
        # end for
        if (php_isset(lambda : thisfile_asf_codeclistobject_["codec_entries"])):
            for streamnumber_,streamdata_ in thisfile_asf_codeclistobject_["codec_entries"].items():
                for case in Switch(streamdata_["type_raw"]):
                    if case(1):
                        #// video
                        thisfile_video_["encoder"] = self.trimconvert(thisfile_asf_codeclistobject_["codec_entries"][streamnumber_]["name"])
                        break
                    # end if
                    if case(2):
                        #// audio
                        thisfile_audio_["encoder"] = self.trimconvert(thisfile_asf_codeclistobject_["codec_entries"][streamnumber_]["name"])
                        #// AH 2003-10-01
                        thisfile_audio_["encoder_options"] = self.trimconvert(thisfile_asf_codeclistobject_["codec_entries"][0]["description"])
                        thisfile_audio_["codec"] = thisfile_audio_["encoder"]
                        break
                    # end if
                    if case():
                        self.warning("Unknown streamtype: [codec_list_object][codec_entries][" + streamnumber_ + "][type_raw] == " + streamdata_["type_raw"])
                        break
                    # end if
                # end for
            # end for
        # end if
        if (php_isset(lambda : info_["audio"])):
            thisfile_audio_["lossless"] = thisfile_audio_["lossless"] if (php_isset(lambda : thisfile_audio_["lossless"])) else False
            thisfile_audio_["dataformat"] = thisfile_audio_["dataformat"] if (not php_empty(lambda : thisfile_audio_["dataformat"])) else "asf"
        # end if
        if (not php_empty(lambda : thisfile_video_["dataformat"])):
            thisfile_video_["lossless"] = thisfile_audio_["lossless"] if (php_isset(lambda : thisfile_audio_["lossless"])) else False
            thisfile_video_["pixel_aspect_ratio"] = thisfile_audio_["pixel_aspect_ratio"] if (php_isset(lambda : thisfile_audio_["pixel_aspect_ratio"])) else php_float(1)
            thisfile_video_["dataformat"] = thisfile_video_["dataformat"] if (not php_empty(lambda : thisfile_video_["dataformat"])) else "asf"
        # end if
        if (not php_empty(lambda : thisfile_video_["streams"])):
            thisfile_video_["resolution_x"] = 0
            thisfile_video_["resolution_y"] = 0
            for key_,valuearray_ in thisfile_video_["streams"].items():
                if valuearray_["resolution_x"] > thisfile_video_["resolution_x"] or valuearray_["resolution_y"] > thisfile_video_["resolution_y"]:
                    thisfile_video_["resolution_x"] = valuearray_["resolution_x"]
                    thisfile_video_["resolution_y"] = valuearray_["resolution_y"]
                # end if
            # end for
        # end if
        info_["bitrate"] = thisfile_audio_["bitrate"] if (php_isset(lambda : thisfile_audio_["bitrate"])) else 0 + thisfile_video_["bitrate"] if (php_isset(lambda : thisfile_video_["bitrate"])) else 0
        if (not (php_isset(lambda : info_["playtime_seconds"]))) or info_["playtime_seconds"] <= 0 and info_["bitrate"] > 0:
            info_["playtime_seconds"] = info_["filesize"] - info_["avdataoffset"] / info_["bitrate"] / 8
        # end if
        return True
    # end def analyze
    #// 
    #// @param int $CodecListType
    #// 
    #// @return string
    #//
    @classmethod
    def codeclistobjecttypelookup(self, CodecListType_=None):
        
        
        lookup_ = Array({1: "Video Codec", 2: "Audio Codec", 65535: "Unknown Codec"})
        return lookup_[CodecListType_] if (php_isset(lambda : lookup_[CodecListType_])) else "Invalid Codec Type"
    # end def codeclistobjecttypelookup
    #// 
    #// @return array
    #//
    @classmethod
    def knownguids(self):
        
        
        GUIDarray_ = Array({"GETID3_ASF_Extended_Stream_Properties_Object": "14E6A5CB-C672-4332-8399-A96952065B5A", "GETID3_ASF_Padding_Object": "1806D474-CADF-4509-A4BA-9AABCB96AAE8", "GETID3_ASF_Payload_Ext_Syst_Pixel_Aspect_Ratio": "1B1EE554-F9EA-4BC8-821A-376B74E4C4B8", "GETID3_ASF_Script_Command_Object": "1EFB1A30-0B62-11D0-A39B-00A0C90348F6", "GETID3_ASF_No_Error_Correction": "20FB5700-5B55-11CF-A8FD-00805F5C442B", "GETID3_ASF_Content_Branding_Object": "2211B3FA-BD23-11D2-B4B7-00A0C955FC6E", "GETID3_ASF_Content_Encryption_Object": "2211B3FB-BD23-11D2-B4B7-00A0C955FC6E", "GETID3_ASF_Digital_Signature_Object": "2211B3FC-BD23-11D2-B4B7-00A0C955FC6E", "GETID3_ASF_Extended_Content_Encryption_Object": "298AE614-2622-4C17-B935-DAE07EE9289C", "GETID3_ASF_Simple_Index_Object": "33000890-E5B1-11CF-89F4-00A0C90349CB", "GETID3_ASF_Degradable_JPEG_Media": "35907DE0-E415-11CF-A917-00805F5C442B", "GETID3_ASF_Payload_Extension_System_Timecode": "399595EC-8667-4E2D-8FDB-98814CE76C1E", "GETID3_ASF_Binary_Media": "3AFB65E2-47EF-40F2-AC2C-70A90D71D343", "GETID3_ASF_Timecode_Index_Object": "3CB73FD0-0C4A-4803-953D-EDF7B6228F0C", "GETID3_ASF_Metadata_Library_Object": "44231C94-9498-49D1-A141-1D134E457054", "GETID3_ASF_Reserved_3": "4B1ACBE3-100B-11D0-A39B-00A0C90348F6", "GETID3_ASF_Reserved_4": "4CFEDB20-75F6-11CF-9C0F-00A0C90349CB", "GETID3_ASF_Command_Media": "59DACFC0-59E6-11D0-A3AC-00A0C90348F6", "GETID3_ASF_Header_Extension_Object": "5FBF03B5-A92E-11CF-8EE3-00C00C205365", "GETID3_ASF_Media_Object_Index_Parameters_Obj": "6B203BAD-3F11-4E84-ACA8-D7613DE2CFA7", "GETID3_ASF_Header_Object": "75B22630-668E-11CF-A6D9-00AA0062CE6C", "GETID3_ASF_Content_Description_Object": "75B22633-668E-11CF-A6D9-00AA0062CE6C", "GETID3_ASF_Error_Correction_Object": "75B22635-668E-11CF-A6D9-00AA0062CE6C", "GETID3_ASF_Data_Object": "75B22636-668E-11CF-A6D9-00AA0062CE6C", "GETID3_ASF_Web_Stream_Media_Subtype": "776257D4-C627-41CB-8F81-7AC7FF1C40CC", "GETID3_ASF_Stream_Bitrate_Properties_Object": "7BF875CE-468D-11D1-8D82-006097C9A2B2", "GETID3_ASF_Language_List_Object": "7C4346A9-EFE0-4BFC-B229-393EDE415C85", "GETID3_ASF_Codec_List_Object": "86D15240-311D-11D0-A3A4-00A0C90348F6", "GETID3_ASF_Reserved_2": "86D15241-311D-11D0-A3A4-00A0C90348F6", "GETID3_ASF_File_Properties_Object": "8CABDCA1-A947-11CF-8EE4-00C00C205365", "GETID3_ASF_File_Transfer_Media": "91BD222C-F21C-497A-8B6D-5AA86BFC0185", "GETID3_ASF_Old_RTP_Extension_Data": "96800C63-4C94-11D1-837B-0080C7A37F95", "GETID3_ASF_Advanced_Mutual_Exclusion_Object": "A08649CF-4775-4670-8A16-6E35357566CD", "GETID3_ASF_Bandwidth_Sharing_Object": "A69609E6-517B-11D2-B6AF-00C04FD908E9", "GETID3_ASF_Reserved_1": "ABD3D211-A9BA-11cf-8EE6-00C00C205365", "GETID3_ASF_Bandwidth_Sharing_Exclusive": "AF6060AA-5197-11D2-B6AF-00C04FD908E9", "GETID3_ASF_Bandwidth_Sharing_Partial": "AF6060AB-5197-11D2-B6AF-00C04FD908E9", "GETID3_ASF_JFIF_Media": "B61BE100-5B4E-11CF-A8FD-00805F5C442B", "GETID3_ASF_Stream_Properties_Object": "B7DC0791-A9B7-11CF-8EE6-00C00C205365", "GETID3_ASF_Video_Media": "BC19EFC0-5B4D-11CF-A8FD-00805F5C442B", "GETID3_ASF_Audio_Spread": "BFC3CD50-618F-11CF-8BB2-00AA00B4E220", "GETID3_ASF_Metadata_Object": "C5F8CBEA-5BAF-4877-8467-AA8C44FA4CCA", "GETID3_ASF_Payload_Ext_Syst_Sample_Duration": "C6BD9450-867F-4907-83A3-C77921B733AD", "GETID3_ASF_Group_Mutual_Exclusion_Object": "D1465A40-5A79-4338-B71B-E36B8FD6C249", "GETID3_ASF_Extended_Content_Description_Object": "D2D0A440-E307-11D2-97F0-00A0C95EA850", "GETID3_ASF_Stream_Prioritization_Object": "D4FED15B-88D3-454F-81F0-ED5C45999E24", "GETID3_ASF_Payload_Ext_System_Content_Type": "D590DC20-07BC-436C-9CF7-F3BBFBF1A4DC", "GETID3_ASF_Old_File_Properties_Object": "D6E229D0-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_ASF_Header_Object": "D6E229D1-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_ASF_Data_Object": "D6E229D2-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Index_Object": "D6E229D3-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Stream_Properties_Object": "D6E229D4-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Content_Description_Object": "D6E229D5-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Script_Command_Object": "D6E229D6-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Marker_Object": "D6E229D7-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Component_Download_Object": "D6E229D8-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Stream_Group_Object": "D6E229D9-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Scalable_Object": "D6E229DA-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Prioritization_Object": "D6E229DB-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Bitrate_Mutual_Exclusion_Object": "D6E229DC-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Inter_Media_Dependency_Object": "D6E229DD-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Rating_Object": "D6E229DE-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Index_Parameters_Object": "D6E229DF-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Color_Table_Object": "D6E229E0-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Language_List_Object": "D6E229E1-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Audio_Media": "D6E229E2-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Video_Media": "D6E229E3-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Image_Media": "D6E229E4-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Timecode_Media": "D6E229E5-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Text_Media": "D6E229E6-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_MIDI_Media": "D6E229E7-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Command_Media": "D6E229E8-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_No_Error_Concealment": "D6E229EA-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Scrambled_Audio": "D6E229EB-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_No_Color_Table": "D6E229EC-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_SMPTE_Time": "D6E229ED-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_ASCII_Text": "D6E229EE-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Unicode_Text": "D6E229EF-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_HTML_Text": "D6E229F0-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_URL_Command": "D6E229F1-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Filename_Command": "D6E229F2-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_ACM_Codec": "D6E229F3-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_VCM_Codec": "D6E229F4-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_QuickTime_Codec": "D6E229F5-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_DirectShow_Transform_Filter": "D6E229F6-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_DirectShow_Rendering_Filter": "D6E229F7-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_No_Enhancement": "D6E229F8-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Unknown_Enhancement_Type": "D6E229F9-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Temporal_Enhancement": "D6E229FA-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Spatial_Enhancement": "D6E229FB-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Quality_Enhancement": "D6E229FC-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Number_of_Channels_Enhancement": "D6E229FD-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Frequency_Response_Enhancement": "D6E229FE-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Media_Object": "D6E229FF-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Mutex_Language": "D6E22A00-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Mutex_Bitrate": "D6E22A01-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Mutex_Unknown": "D6E22A02-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_ASF_Placeholder_Object": "D6E22A0E-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Old_Data_Unit_Extension_Object": "D6E22A0F-35DA-11D1-9034-00A0C90349BE", "GETID3_ASF_Web_Stream_Format": "DA1E6B13-8359-4050-B398-388E965BF00C", "GETID3_ASF_Payload_Ext_System_File_Name": "E165EC0E-19ED-45D7-B4A7-25CBD1E28E9B", "GETID3_ASF_Marker_Object": "F487CD01-A951-11CF-8EE6-00C00C205365", "GETID3_ASF_Timecode_Index_Parameters_Object": "F55E496D-9797-4B5D-8C8B-604DFE9BFB24", "GETID3_ASF_Audio_Media": "F8699E40-5B4D-11CF-A8FD-00805F5C442B", "GETID3_ASF_Media_Object_Index_Object": "FEB103F8-12AD-4C64-840F-2A1D2F7AD48C", "GETID3_ASF_Alt_Extended_Content_Encryption_Obj": "FF889EF1-ADEE-40DA-9E71-98704BB928CE", "GETID3_ASF_Index_Placeholder_Object": "D9AADE20-7C17-4F9C-BC28-8555DD98E2A2", "GETID3_ASF_Compatibility_Object": "26F18B5D-4584-47EC-9F5F-0E651F0452C9"})
        return GUIDarray_
    # end def knownguids
    #// 
    #// @param string $GUIDstring
    #// 
    #// @return string|false
    #//
    @classmethod
    def guidname(self, GUIDstring_=None):
        
        
        GUIDarray_ = Array()
        if php_empty(lambda : GUIDarray_):
            GUIDarray_ = self.knownguids()
        # end if
        return php_array_search(GUIDstring_, GUIDarray_)
    # end def guidname
    #// 
    #// @param int $id
    #// 
    #// @return string
    #//
    @classmethod
    def asfindexobjectindextypelookup(self, id_=None):
        
        
        ASFIndexObjectIndexTypeLookup_ = Array()
        if php_empty(lambda : ASFIndexObjectIndexTypeLookup_):
            ASFIndexObjectIndexTypeLookup_[1] = "Nearest Past Data Packet"
            ASFIndexObjectIndexTypeLookup_[2] = "Nearest Past Media Object"
            ASFIndexObjectIndexTypeLookup_[3] = "Nearest Past Cleanpoint"
        # end if
        return ASFIndexObjectIndexTypeLookup_[id_] if (php_isset(lambda : ASFIndexObjectIndexTypeLookup_[id_])) else "invalid"
    # end def asfindexobjectindextypelookup
    #// 
    #// @param string $GUIDstring
    #// 
    #// @return string
    #//
    @classmethod
    def guidtobytestring(self, GUIDstring_=None):
        
        
        #// Microsoft defines these 16-byte (128-bit) GUIDs in the strangest way:
        #// first 4 bytes are in little-endian order
        #// next 2 bytes are appended in little-endian order
        #// next 2 bytes are appended in little-endian order
        #// next 2 bytes are appended in big-endian order
        #// next 6 bytes are appended in big-endian order
        #// AaBbCcDd-EeFf-GgHh-IiJj-KkLlMmNnOoPp is stored as this 16-byte string:
        #// $Dd $Cc $Bb $Aa $Ff $Ee $Hh $Gg $Ii $Jj $Kk $Ll $Mm $Nn $Oo $Pp
        hexbytecharstring_ = chr(hexdec(php_substr(GUIDstring_, 6, 2)))
        hexbytecharstring_ += chr(hexdec(php_substr(GUIDstring_, 4, 2)))
        hexbytecharstring_ += chr(hexdec(php_substr(GUIDstring_, 2, 2)))
        hexbytecharstring_ += chr(hexdec(php_substr(GUIDstring_, 0, 2)))
        hexbytecharstring_ += chr(hexdec(php_substr(GUIDstring_, 11, 2)))
        hexbytecharstring_ += chr(hexdec(php_substr(GUIDstring_, 9, 2)))
        hexbytecharstring_ += chr(hexdec(php_substr(GUIDstring_, 16, 2)))
        hexbytecharstring_ += chr(hexdec(php_substr(GUIDstring_, 14, 2)))
        hexbytecharstring_ += chr(hexdec(php_substr(GUIDstring_, 19, 2)))
        hexbytecharstring_ += chr(hexdec(php_substr(GUIDstring_, 21, 2)))
        hexbytecharstring_ += chr(hexdec(php_substr(GUIDstring_, 24, 2)))
        hexbytecharstring_ += chr(hexdec(php_substr(GUIDstring_, 26, 2)))
        hexbytecharstring_ += chr(hexdec(php_substr(GUIDstring_, 28, 2)))
        hexbytecharstring_ += chr(hexdec(php_substr(GUIDstring_, 30, 2)))
        hexbytecharstring_ += chr(hexdec(php_substr(GUIDstring_, 32, 2)))
        hexbytecharstring_ += chr(hexdec(php_substr(GUIDstring_, 34, 2)))
        return hexbytecharstring_
    # end def guidtobytestring
    #// 
    #// @param string $Bytestring
    #// 
    #// @return string
    #//
    @classmethod
    def bytestringtoguid(self, Bytestring_=None):
        
        
        GUIDstring_ = php_str_pad(dechex(php_ord(Bytestring_[3])), 2, "0", STR_PAD_LEFT)
        GUIDstring_ += php_str_pad(dechex(php_ord(Bytestring_[2])), 2, "0", STR_PAD_LEFT)
        GUIDstring_ += php_str_pad(dechex(php_ord(Bytestring_[1])), 2, "0", STR_PAD_LEFT)
        GUIDstring_ += php_str_pad(dechex(php_ord(Bytestring_[0])), 2, "0", STR_PAD_LEFT)
        GUIDstring_ += "-"
        GUIDstring_ += php_str_pad(dechex(php_ord(Bytestring_[5])), 2, "0", STR_PAD_LEFT)
        GUIDstring_ += php_str_pad(dechex(php_ord(Bytestring_[4])), 2, "0", STR_PAD_LEFT)
        GUIDstring_ += "-"
        GUIDstring_ += php_str_pad(dechex(php_ord(Bytestring_[7])), 2, "0", STR_PAD_LEFT)
        GUIDstring_ += php_str_pad(dechex(php_ord(Bytestring_[6])), 2, "0", STR_PAD_LEFT)
        GUIDstring_ += "-"
        GUIDstring_ += php_str_pad(dechex(php_ord(Bytestring_[8])), 2, "0", STR_PAD_LEFT)
        GUIDstring_ += php_str_pad(dechex(php_ord(Bytestring_[9])), 2, "0", STR_PAD_LEFT)
        GUIDstring_ += "-"
        GUIDstring_ += php_str_pad(dechex(php_ord(Bytestring_[10])), 2, "0", STR_PAD_LEFT)
        GUIDstring_ += php_str_pad(dechex(php_ord(Bytestring_[11])), 2, "0", STR_PAD_LEFT)
        GUIDstring_ += php_str_pad(dechex(php_ord(Bytestring_[12])), 2, "0", STR_PAD_LEFT)
        GUIDstring_ += php_str_pad(dechex(php_ord(Bytestring_[13])), 2, "0", STR_PAD_LEFT)
        GUIDstring_ += php_str_pad(dechex(php_ord(Bytestring_[14])), 2, "0", STR_PAD_LEFT)
        GUIDstring_ += php_str_pad(dechex(php_ord(Bytestring_[15])), 2, "0", STR_PAD_LEFT)
        return php_strtoupper(GUIDstring_)
    # end def bytestringtoguid
    #// 
    #// @param int  $FILETIME
    #// @param bool $round
    #// 
    #// @return float|int
    #//
    @classmethod
    def filetimetounixtime(self, FILETIME_=None, round_=None):
        if round_ is None:
            round_ = True
        # end if
        
        #// FILETIME is a 64-bit unsigned integer representing
        #// the number of 100-nanosecond intervals since January 1, 1601
        #// UNIX timestamp is number of seconds since January 1, 1970
        #// 116444736000000000 = 10000000 * 60 * 60 * 24 * 365 * 369 + 89 leap days
        if round_:
            return php_intval(round(FILETIME_ - 116444736000000000 / 10000000))
        # end if
        return FILETIME_ - 116444736000000000 / 10000000
    # end def filetimetounixtime
    #// 
    #// @param int $WMpictureType
    #// 
    #// @return string
    #//
    @classmethod
    def wmpicturetypelookup(self, WMpictureType_=None):
        
        
        lookup_ = None
        if lookup_ == None:
            lookup_ = Array({3: "Front Cover", 4: "Back Cover", 0: "User Defined", 5: "Leaflet Page", 6: "Media Label", 7: "Lead Artist", 8: "Artist", 9: "Conductor", 10: "Band", 11: "Composer", 12: "Lyricist", 13: "Recording Location", 14: "During Recording", 15: "During Performance", 16: "Video Screen Capture", 18: "Illustration", 19: "Band Logotype", 20: "Publisher Logotype"})
            lookup_ = php_array_map((lambda str_=None:  getid3_lib.iconv_fallback("UTF-8", "UTF-16LE", str_)), lookup_)
        # end if
        return lookup_[WMpictureType_] if (php_isset(lambda : lookup_[WMpictureType_])) else ""
    # end def wmpicturetypelookup
    #// 
    #// @param string $asf_header_extension_object_data
    #// @param int    $unhandled_sections
    #// 
    #// @return array
    #//
    def headerextensionobjectdataparse(self, asf_header_extension_object_data_=None, unhandled_sections_=None):
        
        
        #// http://msdn.microsoft.com/en-us/library/bb643323.aspx
        offset_ = 0
        objectOffset_ = 0
        HeaderExtensionObjectParsed_ = Array()
        while True:
            
            if not (objectOffset_ < php_strlen(asf_header_extension_object_data_)):
                break
            # end if
            offset_ = objectOffset_
            thisObject_ = Array()
            thisObject_["guid"] = php_substr(asf_header_extension_object_data_, offset_, 16)
            offset_ += 16
            thisObject_["guid_text"] = self.bytestringtoguid(thisObject_["guid"])
            thisObject_["guid_name"] = self.guidname(thisObject_["guid_text"])
            thisObject_["size"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, 8))
            offset_ += 8
            if thisObject_["size"] <= 0:
                break
            # end if
            for case in Switch(thisObject_["guid"]):
                if case(GETID3_ASF_Extended_Stream_Properties_Object):
                    thisObject_["start_time"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, 8))
                    offset_ += 8
                    thisObject_["start_time_unix"] = self.filetimetounixtime(thisObject_["start_time"])
                    thisObject_["end_time"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, 8))
                    offset_ += 8
                    thisObject_["end_time_unix"] = self.filetimetounixtime(thisObject_["end_time"])
                    thisObject_["data_bitrate"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, 4))
                    offset_ += 4
                    thisObject_["buffer_size"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, 4))
                    offset_ += 4
                    thisObject_["initial_buffer_fullness"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, 4))
                    offset_ += 4
                    thisObject_["alternate_data_bitrate"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, 4))
                    offset_ += 4
                    thisObject_["alternate_buffer_size"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, 4))
                    offset_ += 4
                    thisObject_["alternate_initial_buffer_fullness"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, 4))
                    offset_ += 4
                    thisObject_["maximum_object_size"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, 4))
                    offset_ += 4
                    thisObject_["flags_raw"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, 4))
                    offset_ += 4
                    thisObject_["flags"]["reliable"] = php_bool(thisObject_["flags_raw"]) & 1
                    thisObject_["flags"]["seekable"] = php_bool(thisObject_["flags_raw"]) & 2
                    thisObject_["flags"]["no_cleanpoints"] = php_bool(thisObject_["flags_raw"]) & 4
                    thisObject_["flags"]["resend_live_cleanpoints"] = php_bool(thisObject_["flags_raw"]) & 8
                    thisObject_["stream_number"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, 2))
                    offset_ += 2
                    thisObject_["stream_language_id_index"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, 2))
                    offset_ += 2
                    thisObject_["average_time_per_frame"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, 4))
                    offset_ += 4
                    thisObject_["stream_name_count"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, 2))
                    offset_ += 2
                    thisObject_["payload_extension_system_count"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, 2))
                    offset_ += 2
                    i_ = 0
                    while i_ < thisObject_["stream_name_count"]:
                        
                        streamName_ = Array()
                        streamName_["language_id_index"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, 2))
                        offset_ += 2
                        streamName_["stream_name_length"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, 2))
                        offset_ += 2
                        streamName_["stream_name"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, streamName_["stream_name_length"]))
                        offset_ += streamName_["stream_name_length"]
                        thisObject_["stream_names"][i_] = streamName_
                        i_ += 1
                    # end while
                    i_ = 0
                    while i_ < thisObject_["payload_extension_system_count"]:
                        
                        payloadExtensionSystem_ = Array()
                        payloadExtensionSystem_["extension_system_id"] = php_substr(asf_header_extension_object_data_, offset_, 16)
                        offset_ += 16
                        payloadExtensionSystem_["extension_system_id_text"] = self.bytestringtoguid(payloadExtensionSystem_["extension_system_id"])
                        payloadExtensionSystem_["extension_system_size"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, 2))
                        offset_ += 2
                        if payloadExtensionSystem_["extension_system_size"] <= 0:
                            break
                        # end if
                        payloadExtensionSystem_["extension_system_info_length"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, 4))
                        offset_ += 4
                        payloadExtensionSystem_["extension_system_info_length"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, payloadExtensionSystem_["extension_system_info_length"]))
                        offset_ += payloadExtensionSystem_["extension_system_info_length"]
                        thisObject_["payload_extension_systems"][i_] = payloadExtensionSystem_
                        i_ += 1
                    # end while
                    break
                # end if
                if case(GETID3_ASF_Padding_Object):
                    break
                # end if
                if case(GETID3_ASF_Metadata_Object):
                    thisObject_["description_record_counts"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, 2))
                    offset_ += 2
                    i_ = 0
                    while i_ < thisObject_["description_record_counts"]:
                        
                        descriptionRecord_ = Array()
                        descriptionRecord_["reserved_1"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, 2))
                        #// must be zero
                        offset_ += 2
                        descriptionRecord_["stream_number"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, 2))
                        offset_ += 2
                        descriptionRecord_["name_length"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, 2))
                        offset_ += 2
                        descriptionRecord_["data_type"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, 2))
                        offset_ += 2
                        descriptionRecord_["data_type_text"] = self.metadatalibraryobjectdatatypelookup(descriptionRecord_["data_type"])
                        descriptionRecord_["data_length"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, 4))
                        offset_ += 4
                        descriptionRecord_["name"] = php_substr(asf_header_extension_object_data_, offset_, descriptionRecord_["name_length"])
                        offset_ += descriptionRecord_["name_length"]
                        descriptionRecord_["data"] = php_substr(asf_header_extension_object_data_, offset_, descriptionRecord_["data_length"])
                        offset_ += descriptionRecord_["data_length"]
                        for case in Switch(descriptionRecord_["data_type"]):
                            if case(0):
                                break
                            # end if
                            if case(1):
                                break
                            # end if
                            if case(2):
                                #// BOOL
                                descriptionRecord_["data"] = php_bool(getid3_lib.littleendian2int(descriptionRecord_["data"]))
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
                                descriptionRecord_["data"] = getid3_lib.littleendian2int(descriptionRecord_["data"])
                                break
                            # end if
                            if case(6):
                                #// GUID
                                descriptionRecord_["data_text"] = self.bytestringtoguid(descriptionRecord_["data"])
                                break
                            # end if
                        # end for
                        thisObject_["description_record"][i_] = descriptionRecord_
                        i_ += 1
                    # end while
                    break
                # end if
                if case(GETID3_ASF_Language_List_Object):
                    thisObject_["language_id_record_counts"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, 2))
                    offset_ += 2
                    i_ = 0
                    while i_ < thisObject_["language_id_record_counts"]:
                        
                        languageIDrecord_ = Array()
                        languageIDrecord_["language_id_length"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, 1))
                        offset_ += 1
                        languageIDrecord_["language_id"] = php_substr(asf_header_extension_object_data_, offset_, languageIDrecord_["language_id_length"])
                        offset_ += languageIDrecord_["language_id_length"]
                        thisObject_["language_id_record"][i_] = languageIDrecord_
                        i_ += 1
                    # end while
                    break
                # end if
                if case(GETID3_ASF_Metadata_Library_Object):
                    thisObject_["description_records_count"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, 2))
                    offset_ += 2
                    i_ = 0
                    while i_ < thisObject_["description_records_count"]:
                        
                        descriptionRecord_ = Array()
                        descriptionRecord_["language_list_index"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, 2))
                        offset_ += 2
                        descriptionRecord_["stream_number"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, 2))
                        offset_ += 2
                        descriptionRecord_["name_length"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, 2))
                        offset_ += 2
                        descriptionRecord_["data_type"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, 2))
                        offset_ += 2
                        descriptionRecord_["data_type_text"] = self.metadatalibraryobjectdatatypelookup(descriptionRecord_["data_type"])
                        descriptionRecord_["data_length"] = getid3_lib.littleendian2int(php_substr(asf_header_extension_object_data_, offset_, 4))
                        offset_ += 4
                        descriptionRecord_["name"] = php_substr(asf_header_extension_object_data_, offset_, descriptionRecord_["name_length"])
                        offset_ += descriptionRecord_["name_length"]
                        descriptionRecord_["data"] = php_substr(asf_header_extension_object_data_, offset_, descriptionRecord_["data_length"])
                        offset_ += descriptionRecord_["data_length"]
                        if php_preg_match("#^WM/Picture$#", php_str_replace(" ", "", php_trim(descriptionRecord_["name"]))):
                            WMpicture_ = self.asf_wmpicture(descriptionRecord_["data"])
                            for key_,value_ in WMpicture_.items():
                                descriptionRecord_["data"] = WMpicture_
                            # end for
                            WMpicture_ = None
                        # end if
                        thisObject_["description_record"][i_] = descriptionRecord_
                        i_ += 1
                    # end while
                    break
                # end if
                if case():
                    unhandled_sections_ += 1
                    if self.guidname(thisObject_["guid_text"]):
                        self.warning("unhandled Header Extension Object GUID \"" + self.guidname(thisObject_["guid_text"]) + "\" {" + thisObject_["guid_text"] + "} at offset " + offset_ - 16 - 8)
                    else:
                        self.warning("unknown Header Extension Object GUID {" + thisObject_["guid_text"] + "} in at offset " + offset_ - 16 - 8)
                    # end if
                    break
                # end if
            # end for
            HeaderExtensionObjectParsed_[-1] = thisObject_
            objectOffset_ += thisObject_["size"]
        # end while
        return HeaderExtensionObjectParsed_
    # end def headerextensionobjectdataparse
    #// 
    #// @param int $id
    #// 
    #// @return string
    #//
    @classmethod
    def metadatalibraryobjectdatatypelookup(self, id_=None):
        
        
        lookup_ = Array({0: "Unicode string", 1: "BYTE array", 2: "BOOL", 3: "DWORD", 4: "QWORD", 5: "WORD", 6: "GUID"})
        return lookup_[id_] if (php_isset(lambda : lookup_[id_])) else "invalid"
    # end def metadatalibraryobjectdatatypelookup
    #// 
    #// @param string $data
    #// 
    #// @return array
    #//
    def asf_wmpicture(self, data_=None):
        
        
        #// typedef struct _WMPicture{
        #// LPWSTR  pwszMIMEType;
        #// BYTE  bPictureType;
        #// LPWSTR  pwszDescription;
        #// DWORD  dwDataLen;
        #// BYTE*  pbData;
        #// } WM_PICTURE;
        WMpicture_ = Array()
        offset_ = 0
        WMpicture_["image_type_id"] = getid3_lib.littleendian2int(php_substr(data_, offset_, 1))
        offset_ += 1
        WMpicture_["image_type"] = self.wmpicturetypelookup(WMpicture_["image_type_id"])
        WMpicture_["image_size"] = getid3_lib.littleendian2int(php_substr(data_, offset_, 4))
        offset_ += 4
        WMpicture_["image_mime"] = ""
        while True:
            next_byte_pair_ = php_substr(data_, offset_, 2)
            offset_ += 2
            WMpicture_["image_mime"] += next_byte_pair_
            
            if next_byte_pair_ != "  ":
                break
            # end if
        # end while
        WMpicture_["image_description"] = ""
        while True:
            next_byte_pair_ = php_substr(data_, offset_, 2)
            offset_ += 2
            WMpicture_["image_description"] += next_byte_pair_
            
            if next_byte_pair_ != "  ":
                break
            # end if
        # end while
        WMpicture_["dataoffset"] = offset_
        WMpicture_["data"] = php_substr(data_, offset_)
        imageinfo_ = Array()
        WMpicture_["image_mime"] = ""
        imagechunkcheck_ = getid3_lib.getdataimagesize(WMpicture_["data"], imageinfo_)
        imageinfo_ = None
        if (not php_empty(lambda : imagechunkcheck_)):
            WMpicture_["image_mime"] = image_type_to_mime_type(imagechunkcheck_[2])
        # end if
        if (not (php_isset(lambda : self.getid3.info["asf"]["comments"]["picture"]))):
            self.getid3.info["asf"]["comments"]["picture"] = Array()
        # end if
        self.getid3.info["asf"]["comments"]["picture"][-1] = Array({"data": WMpicture_["data"], "image_mime": WMpicture_["image_mime"]})
        return WMpicture_
    # end def asf_wmpicture
    #// 
    #// Remove terminator 00 00 and convert UTF-16LE to Latin-1.
    #// 
    #// @param string $string
    #// 
    #// @return string
    #//
    @classmethod
    def trimconvert(self, string_=None):
        
        
        return php_trim(getid3_lib.iconv_fallback("UTF-16LE", "ISO-8859-1", self.trimterm(string_)), " ")
    # end def trimconvert
    #// 
    #// Remove terminator 00 00.
    #// 
    #// @param string $string
    #// 
    #// @return string
    #//
    @classmethod
    def trimterm(self, string_=None):
        
        
        #// remove terminator, only if present (it should be, but...)
        if php_substr(string_, -2) == "  ":
            string_ = php_substr(string_, 0, -2)
        # end if
        return string_
    # end def trimterm
# end class getid3_asf
