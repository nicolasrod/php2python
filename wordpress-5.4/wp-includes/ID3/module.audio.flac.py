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
#// module.audio.flac.php
#// module for analyzing FLAC and OggFLAC audio files
#// dependencies: module.audio.ogg.php
#// 
#//
getid3_lib.includedependency(GETID3_INCLUDEPATH + "module.audio.ogg.php", __FILE__, True)
#// 
#// @tutorial http://flac.sourceforge.net/format.html
#//
class getid3_flac(getid3_handler):
    syncword = "fLaC"
    #// 
    #// @return bool
    #//
    def analyze(self):
        
        info = self.getid3.info
        self.fseek(info["avdataoffset"])
        StreamMarker = self.fread(4)
        if StreamMarker != self.syncword:
            return self.error("Expecting \"" + getid3_lib.printhexbytes(self.syncword) + "\" at offset " + info["avdataoffset"] + ", found \"" + getid3_lib.printhexbytes(StreamMarker) + "\"")
        # end if
        info["fileformat"] = "flac"
        info["audio"]["dataformat"] = "flac"
        info["audio"]["bitrate_mode"] = "vbr"
        info["audio"]["lossless"] = True
        #// parse flac container
        return self.parsemetadata()
    # end def analyze
    #// 
    #// @return bool
    #//
    def parsemetadata(self):
        
        info = self.getid3.info
        while True:
            BlockOffset = self.ftell()
            BlockHeader = self.fread(4)
            LBFBT = getid3_lib.bigendian2int(php_substr(BlockHeader, 0, 1))
            #// LBFBT = LastBlockFlag + BlockType
            LastBlockFlag = bool(LBFBT & 128)
            BlockType = LBFBT & 127
            BlockLength = getid3_lib.bigendian2int(php_substr(BlockHeader, 1, 3))
            BlockTypeText = self.metablocktypelookup(BlockType)
            if BlockOffset + 4 + BlockLength > info["avdataend"]:
                self.warning("METADATA_BLOCK_HEADER.BLOCK_TYPE (" + BlockTypeText + ") at offset " + BlockOffset + " extends beyond end of file")
                break
            # end if
            if BlockLength < 1:
                if BlockTypeText != "reserved":
                    #// probably supposed to be zero-length
                    self.warning("METADATA_BLOCK_HEADER.BLOCK_LENGTH (" + BlockTypeText + ") at offset " + BlockOffset + " is zero bytes")
                    continue
                # end if
                self.error("METADATA_BLOCK_HEADER.BLOCK_LENGTH (" + BlockLength + ") at offset " + BlockOffset + " is invalid")
                break
            # end if
            info["flac"][BlockTypeText]["raw"] = Array()
            BlockTypeText_raw = info["flac"][BlockTypeText]["raw"]
            BlockTypeText_raw["offset"] = BlockOffset
            BlockTypeText_raw["last_meta_block"] = LastBlockFlag
            BlockTypeText_raw["block_type"] = BlockType
            BlockTypeText_raw["block_type_text"] = BlockTypeText
            BlockTypeText_raw["block_length"] = BlockLength
            if BlockTypeText_raw["block_type"] != 6:
                #// do not read attachment data automatically
                BlockTypeText_raw["block_data"] = self.fread(BlockLength)
            # end if
            for case in Switch(BlockTypeText):
                if case("STREAMINFO"):
                    #// 0x00
                    if (not self.parsestreaminfo(BlockTypeText_raw["block_data"])):
                        return False
                    # end if
                    break
                # end if
                if case("PADDING"):
                    info["flac"]["PADDING"] = None
                    break
                # end if
                if case("APPLICATION"):
                    #// 0x02
                    if (not self.parseapplication(BlockTypeText_raw["block_data"])):
                        return False
                    # end if
                    break
                # end if
                if case("SEEKTABLE"):
                    #// 0x03
                    if (not self.parseseektable(BlockTypeText_raw["block_data"])):
                        return False
                    # end if
                    break
                # end if
                if case("VORBIS_COMMENT"):
                    #// 0x04
                    if (not self.parsevorbis_comment(BlockTypeText_raw["block_data"])):
                        return False
                    # end if
                    break
                # end if
                if case("CUESHEET"):
                    #// 0x05
                    if (not self.parsecuesheet(BlockTypeText_raw["block_data"])):
                        return False
                    # end if
                    break
                # end if
                if case("PICTURE"):
                    #// 0x06
                    if (not self.parsepicture()):
                        return False
                    # end if
                    break
                # end if
                if case():
                    self.warning("Unhandled METADATA_BLOCK_HEADER.BLOCK_TYPE (" + BlockType + ") at offset " + BlockOffset)
                # end if
            # end for
            info["flac"][BlockTypeText]["raw"] = None
            info["avdataoffset"] = self.ftell()
            
            if LastBlockFlag == False:
                break
            # end if
        # end while
        #// handle tags
        if (not php_empty(lambda : info["flac"]["VORBIS_COMMENT"]["comments"])):
            info["flac"]["comments"] = info["flac"]["VORBIS_COMMENT"]["comments"]
        # end if
        if (not php_empty(lambda : info["flac"]["VORBIS_COMMENT"]["vendor"])):
            info["audio"]["encoder"] = php_str_replace("reference ", "", info["flac"]["VORBIS_COMMENT"]["vendor"])
        # end if
        #// copy attachments to 'comments' array if nesesary
        if (php_isset(lambda : info["flac"]["PICTURE"])) and self.getid3.option_save_attachments != getID3.ATTACHMENTS_NONE:
            for entry in info["flac"]["PICTURE"]:
                if (not php_empty(lambda : entry["data"])):
                    if (not (php_isset(lambda : info["flac"]["comments"]["picture"]))):
                        info["flac"]["comments"]["picture"] = Array()
                    # end if
                    comments_picture_data = Array()
                    for picture_key in Array("data", "image_mime", "image_width", "image_height", "imagetype", "picturetype", "description", "datalength"):
                        if (php_isset(lambda : entry[picture_key])):
                            comments_picture_data[picture_key] = entry[picture_key]
                        # end if
                    # end for
                    info["flac"]["comments"]["picture"][-1] = comments_picture_data
                    comments_picture_data = None
                # end if
            # end for
        # end if
        if (php_isset(lambda : info["flac"]["STREAMINFO"])):
            if (not self.isdependencyfor("matroska")):
                info["flac"]["compressed_audio_bytes"] = info["avdataend"] - info["avdataoffset"]
            # end if
            info["flac"]["uncompressed_audio_bytes"] = info["flac"]["STREAMINFO"]["samples_stream"] * info["flac"]["STREAMINFO"]["channels"] * info["flac"]["STREAMINFO"]["bits_per_sample"] / 8
            if info["flac"]["uncompressed_audio_bytes"] == 0:
                return self.error("Corrupt FLAC file: uncompressed_audio_bytes == zero")
            # end if
            if (not php_empty(lambda : info["flac"]["compressed_audio_bytes"])):
                info["flac"]["compression_ratio"] = info["flac"]["compressed_audio_bytes"] / info["flac"]["uncompressed_audio_bytes"]
            # end if
        # end if
        #// set md5_data_source - built into flac 0.5+
        if (php_isset(lambda : info["flac"]["STREAMINFO"]["audio_signature"])):
            if info["flac"]["STREAMINFO"]["audio_signature"] == php_str_repeat(" ", 16):
                self.warning("FLAC STREAMINFO.audio_signature is null (known issue with libOggFLAC)")
            else:
                info["md5_data_source"] = ""
                md5 = info["flac"]["STREAMINFO"]["audio_signature"]
                i = 0
                while i < php_strlen(md5):
                    
                    info["md5_data_source"] += php_str_pad(dechex(php_ord(md5[i])), 2, "00", STR_PAD_LEFT)
                    i += 1
                # end while
                if (not php_preg_match("/^[0-9a-f]{32}$/", info["md5_data_source"])):
                    info["md5_data_source"] = None
                # end if
            # end if
        # end if
        if (php_isset(lambda : info["flac"]["STREAMINFO"]["bits_per_sample"])):
            info["audio"]["bits_per_sample"] = info["flac"]["STREAMINFO"]["bits_per_sample"]
            if info["audio"]["bits_per_sample"] == 8:
                #// special case
                #// must invert sign bit on all data bytes before MD5'ing to match FLAC's calculated value
                #// MD5sum calculates on unsigned bytes, but FLAC calculated MD5 on 8-bit audio data as signed
                self.warning("FLAC calculates MD5 data strangely on 8-bit audio, so the stored md5_data_source value will not match the decoded WAV file")
            # end if
        # end if
        return True
    # end def parsemetadata
    #// 
    #// @param string $BlockData
    #// 
    #// @return array
    #//
    @classmethod
    def parsestreaminfodata(self, BlockData=None):
        
        streaminfo = Array()
        streaminfo["min_block_size"] = getid3_lib.bigendian2int(php_substr(BlockData, 0, 2))
        streaminfo["max_block_size"] = getid3_lib.bigendian2int(php_substr(BlockData, 2, 2))
        streaminfo["min_frame_size"] = getid3_lib.bigendian2int(php_substr(BlockData, 4, 3))
        streaminfo["max_frame_size"] = getid3_lib.bigendian2int(php_substr(BlockData, 7, 3))
        SRCSBSS = getid3_lib.bigendian2bin(php_substr(BlockData, 10, 8))
        streaminfo["sample_rate"] = getid3_lib.bin2dec(php_substr(SRCSBSS, 0, 20))
        streaminfo["channels"] = getid3_lib.bin2dec(php_substr(SRCSBSS, 20, 3)) + 1
        streaminfo["bits_per_sample"] = getid3_lib.bin2dec(php_substr(SRCSBSS, 23, 5)) + 1
        streaminfo["samples_stream"] = getid3_lib.bin2dec(php_substr(SRCSBSS, 28, 36))
        streaminfo["audio_signature"] = php_substr(BlockData, 18, 16)
        return streaminfo
    # end def parsestreaminfodata
    #// 
    #// @param string $BlockData
    #// 
    #// @return bool
    #//
    def parsestreaminfo(self, BlockData=None):
        
        info = self.getid3.info
        info["flac"]["STREAMINFO"] = self.parsestreaminfodata(BlockData)
        if (not php_empty(lambda : info["flac"]["STREAMINFO"]["sample_rate"])):
            info["audio"]["bitrate_mode"] = "vbr"
            info["audio"]["sample_rate"] = info["flac"]["STREAMINFO"]["sample_rate"]
            info["audio"]["channels"] = info["flac"]["STREAMINFO"]["channels"]
            info["audio"]["bits_per_sample"] = info["flac"]["STREAMINFO"]["bits_per_sample"]
            info["playtime_seconds"] = info["flac"]["STREAMINFO"]["samples_stream"] / info["flac"]["STREAMINFO"]["sample_rate"]
            if info["playtime_seconds"] > 0:
                if (not self.isdependencyfor("matroska")):
                    info["audio"]["bitrate"] = info["avdataend"] - info["avdataoffset"] * 8 / info["playtime_seconds"]
                else:
                    self.warning("Cannot determine audio bitrate because total stream size is unknown")
                # end if
            # end if
        else:
            return self.error("Corrupt METAdata block: STREAMINFO")
        # end if
        return True
    # end def parsestreaminfo
    #// 
    #// @param string $BlockData
    #// 
    #// @return bool
    #//
    def parseapplication(self, BlockData=None):
        
        info = self.getid3.info
        ApplicationID = getid3_lib.bigendian2int(php_substr(BlockData, 0, 4))
        info["flac"]["APPLICATION"][ApplicationID]["name"] = self.applicationidlookup(ApplicationID)
        info["flac"]["APPLICATION"][ApplicationID]["data"] = php_substr(BlockData, 4)
        return True
    # end def parseapplication
    #// 
    #// @param string $BlockData
    #// 
    #// @return bool
    #//
    def parseseektable(self, BlockData=None):
        
        info = self.getid3.info
        offset = 0
        BlockLength = php_strlen(BlockData)
        placeholderpattern = php_str_repeat("ÿ", 8)
        while True:
            
            if not (offset < BlockLength):
                break
            # end if
            SampleNumberString = php_substr(BlockData, offset, 8)
            offset += 8
            if SampleNumberString == placeholderpattern:
                #// placeholder point
                getid3_lib.safe_inc(info["flac"]["SEEKTABLE"]["placeholders"], 1)
                offset += 10
            else:
                SampleNumber = getid3_lib.bigendian2int(SampleNumberString)
                info["flac"]["SEEKTABLE"][SampleNumber]["offset"] = getid3_lib.bigendian2int(php_substr(BlockData, offset, 8))
                offset += 8
                info["flac"]["SEEKTABLE"][SampleNumber]["samples"] = getid3_lib.bigendian2int(php_substr(BlockData, offset, 2))
                offset += 2
            # end if
        # end while
        return True
    # end def parseseektable
    #// 
    #// @param string $BlockData
    #// 
    #// @return bool
    #//
    def parsevorbis_comment(self, BlockData=None):
        
        info = self.getid3.info
        getid3_ogg = php_new_class("getid3_ogg", lambda : getid3_ogg(self.getid3))
        if self.isdependencyfor("matroska"):
            getid3_ogg.setstringmode(self.data_string)
        # end if
        getid3_ogg.parsevorbiscomments()
        if (php_isset(lambda : info["ogg"])):
            info["ogg"]["comments_raw"] = None
            info["flac"]["VORBIS_COMMENT"] = info["ogg"]
            info["ogg"] = None
        # end if
        getid3_ogg = None
        return True
    # end def parsevorbis_comment
    #// 
    #// @param string $BlockData
    #// 
    #// @return bool
    #//
    def parsecuesheet(self, BlockData=None):
        
        info = self.getid3.info
        offset = 0
        info["flac"]["CUESHEET"]["media_catalog_number"] = php_trim(php_substr(BlockData, offset, 128), " ")
        offset += 128
        info["flac"]["CUESHEET"]["lead_in_samples"] = getid3_lib.bigendian2int(php_substr(BlockData, offset, 8))
        offset += 8
        info["flac"]["CUESHEET"]["flags"]["is_cd"] = bool(getid3_lib.bigendian2int(php_substr(BlockData, offset, 1)) & 128)
        offset += 1
        offset += 258
        #// reserved
        info["flac"]["CUESHEET"]["number_tracks"] = getid3_lib.bigendian2int(php_substr(BlockData, offset, 1))
        offset += 1
        track = 0
        while track < info["flac"]["CUESHEET"]["number_tracks"]:
            
            TrackSampleOffset = getid3_lib.bigendian2int(php_substr(BlockData, offset, 8))
            offset += 8
            TrackNumber = getid3_lib.bigendian2int(php_substr(BlockData, offset, 1))
            offset += 1
            info["flac"]["CUESHEET"]["tracks"][TrackNumber]["sample_offset"] = TrackSampleOffset
            info["flac"]["CUESHEET"]["tracks"][TrackNumber]["isrc"] = php_substr(BlockData, offset, 12)
            offset += 12
            TrackFlagsRaw = getid3_lib.bigendian2int(php_substr(BlockData, offset, 1))
            offset += 1
            info["flac"]["CUESHEET"]["tracks"][TrackNumber]["flags"]["is_audio"] = bool(TrackFlagsRaw & 128)
            info["flac"]["CUESHEET"]["tracks"][TrackNumber]["flags"]["pre_emphasis"] = bool(TrackFlagsRaw & 64)
            offset += 13
            #// reserved
            info["flac"]["CUESHEET"]["tracks"][TrackNumber]["index_points"] = getid3_lib.bigendian2int(php_substr(BlockData, offset, 1))
            offset += 1
            index = 0
            while index < info["flac"]["CUESHEET"]["tracks"][TrackNumber]["index_points"]:
                
                IndexSampleOffset = getid3_lib.bigendian2int(php_substr(BlockData, offset, 8))
                offset += 8
                IndexNumber = getid3_lib.bigendian2int(php_substr(BlockData, offset, 1))
                offset += 1
                offset += 3
                #// reserved
                info["flac"]["CUESHEET"]["tracks"][TrackNumber]["indexes"][IndexNumber] = IndexSampleOffset
                index += 1
            # end while
            track += 1
        # end while
        return True
    # end def parsecuesheet
    #// 
    #// Parse METADATA_BLOCK_PICTURE flac structure and extract attachment
    #// External usage: audio.ogg
    #// 
    #// @return bool
    #//
    def parsepicture(self):
        
        info = self.getid3.info
        picture["typeid"] = getid3_lib.bigendian2int(self.fread(4))
        picture["picturetype"] = self.picturetypelookup(picture["typeid"])
        picture["image_mime"] = self.fread(getid3_lib.bigendian2int(self.fread(4)))
        descr_length = getid3_lib.bigendian2int(self.fread(4))
        if descr_length:
            picture["description"] = self.fread(descr_length)
        # end if
        picture["image_width"] = getid3_lib.bigendian2int(self.fread(4))
        picture["image_height"] = getid3_lib.bigendian2int(self.fread(4))
        picture["color_depth"] = getid3_lib.bigendian2int(self.fread(4))
        picture["colors_indexed"] = getid3_lib.bigendian2int(self.fread(4))
        picture["datalength"] = getid3_lib.bigendian2int(self.fread(4))
        if picture["image_mime"] == "-->":
            picture["data"] = self.fread(picture["datalength"])
        else:
            picture["data"] = self.saveattachment(php_str_replace("/", "_", picture["picturetype"]) + "_" + self.ftell(), self.ftell(), picture["datalength"], picture["image_mime"])
        # end if
        info["flac"]["PICTURE"][-1] = picture
        return True
    # end def parsepicture
    #// 
    #// @param int $blocktype
    #// 
    #// @return string
    #//
    @classmethod
    def metablocktypelookup(self, blocktype=None):
        
        lookup = Array({0: "STREAMINFO", 1: "PADDING", 2: "APPLICATION", 3: "SEEKTABLE", 4: "VORBIS_COMMENT", 5: "CUESHEET", 6: "PICTURE"})
        return lookup[blocktype] if (php_isset(lambda : lookup[blocktype])) else "reserved"
    # end def metablocktypelookup
    #// 
    #// @param int $applicationid
    #// 
    #// @return string
    #//
    @classmethod
    def applicationidlookup(self, applicationid=None):
        
        lookup = Array({1096041288: "FlacFile", 1112756044: "beSolo", 1112885075: "Bugs Player", 1131767155: "GoldWave cue points (specification)", 1181311841: "CUE Splitter", 1182035820: "flac-tools", 1297044546: "MOTB MetaCzar", 1297109829: "MP3 Stream Editor", 1299533132: "MusicML: Music Metadata Language", 1380533830: "Sound Devices RIFF chunk storage", 1397114444: "Sound Font FLAC", 1397706329: "Sony Creative Software", 1397835098: "flacsqueeze", 1416910710: "TwistedWave", 1430869075: "UITS Embedding tools", 1634297446: "FLAC AIFF chunk storage", 1768776039: "flac-image application for storing arbitrary files in APPLICATION metadata blocks", 1885693293: "Parseable Embedded Extensible Metadata (specification)", 1902539636: "QFLAC Studio", 1919510118: "FLAC RIFF chunk storage", 1953853029: "TagTuner", 2019713396: "XBAT", 2020434788: "xmcd"})
        return lookup[applicationid] if (php_isset(lambda : lookup[applicationid])) else "reserved"
    # end def applicationidlookup
    #// 
    #// @param int $type_id
    #// 
    #// @return string
    #//
    @classmethod
    def picturetypelookup(self, type_id=None):
        
        lookup = Array({0: "Other", 1: "32x32 pixels 'file icon' (PNG only)", 2: "Other file icon", 3: "Cover (front)", 4: "Cover (back)", 5: "Leaflet page", 6: "Media (e.g. label side of CD)", 7: "Lead artist/lead performer/soloist", 8: "Artist/performer", 9: "Conductor", 10: "Band/Orchestra", 11: "Composer", 12: "Lyricist/text writer", 13: "Recording Location", 14: "During recording", 15: "During performance", 16: "Movie/video screen capture", 17: "A bright coloured fish", 18: "Illustration", 19: "Band/artist logotype", 20: "Publisher/Studio logotype"})
        return lookup[type_id] if (php_isset(lambda : lookup[type_id])) else "reserved"
    # end def picturetypelookup
# end class getid3_flac
