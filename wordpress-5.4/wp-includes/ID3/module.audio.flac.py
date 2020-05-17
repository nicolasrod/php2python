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
        
        
        info_ = self.getid3.info
        self.fseek(info_["avdataoffset"])
        StreamMarker_ = self.fread(4)
        if StreamMarker_ != self.syncword:
            return self.error("Expecting \"" + getid3_lib.printhexbytes(self.syncword) + "\" at offset " + info_["avdataoffset"] + ", found \"" + getid3_lib.printhexbytes(StreamMarker_) + "\"")
        # end if
        info_["fileformat"] = "flac"
        info_["audio"]["dataformat"] = "flac"
        info_["audio"]["bitrate_mode"] = "vbr"
        info_["audio"]["lossless"] = True
        #// parse flac container
        return self.parsemetadata()
    # end def analyze
    #// 
    #// @return bool
    #//
    def parsemetadata(self):
        
        
        info_ = self.getid3.info
        while True:
            BlockOffset_ = self.ftell()
            BlockHeader_ = self.fread(4)
            LBFBT_ = getid3_lib.bigendian2int(php_substr(BlockHeader_, 0, 1))
            #// LBFBT = LastBlockFlag + BlockType
            LastBlockFlag_ = php_bool(LBFBT_ & 128)
            BlockType_ = LBFBT_ & 127
            BlockLength_ = getid3_lib.bigendian2int(php_substr(BlockHeader_, 1, 3))
            BlockTypeText_ = self.metablocktypelookup(BlockType_)
            if BlockOffset_ + 4 + BlockLength_ > info_["avdataend"]:
                self.warning("METADATA_BLOCK_HEADER.BLOCK_TYPE (" + BlockTypeText_ + ") at offset " + BlockOffset_ + " extends beyond end of file")
                break
            # end if
            if BlockLength_ < 1:
                if BlockTypeText_ != "reserved":
                    #// probably supposed to be zero-length
                    self.warning("METADATA_BLOCK_HEADER.BLOCK_LENGTH (" + BlockTypeText_ + ") at offset " + BlockOffset_ + " is zero bytes")
                    continue
                # end if
                self.error("METADATA_BLOCK_HEADER.BLOCK_LENGTH (" + BlockLength_ + ") at offset " + BlockOffset_ + " is invalid")
                break
            # end if
            info_["flac"][BlockTypeText_]["raw"] = Array()
            BlockTypeText_raw_ = info_["flac"][BlockTypeText_]["raw"]
            BlockTypeText_raw_["offset"] = BlockOffset_
            BlockTypeText_raw_["last_meta_block"] = LastBlockFlag_
            BlockTypeText_raw_["block_type"] = BlockType_
            BlockTypeText_raw_["block_type_text"] = BlockTypeText_
            BlockTypeText_raw_["block_length"] = BlockLength_
            if BlockTypeText_raw_["block_type"] != 6:
                #// do not read attachment data automatically
                BlockTypeText_raw_["block_data"] = self.fread(BlockLength_)
            # end if
            for case in Switch(BlockTypeText_):
                if case("STREAMINFO"):
                    #// 0x00
                    if (not self.parsestreaminfo(BlockTypeText_raw_["block_data"])):
                        return False
                    # end if
                    break
                # end if
                if case("PADDING"):
                    info_["flac"]["PADDING"] = None
                    break
                # end if
                if case("APPLICATION"):
                    #// 0x02
                    if (not self.parseapplication(BlockTypeText_raw_["block_data"])):
                        return False
                    # end if
                    break
                # end if
                if case("SEEKTABLE"):
                    #// 0x03
                    if (not self.parseseektable(BlockTypeText_raw_["block_data"])):
                        return False
                    # end if
                    break
                # end if
                if case("VORBIS_COMMENT"):
                    #// 0x04
                    if (not self.parsevorbis_comment(BlockTypeText_raw_["block_data"])):
                        return False
                    # end if
                    break
                # end if
                if case("CUESHEET"):
                    #// 0x05
                    if (not self.parsecuesheet(BlockTypeText_raw_["block_data"])):
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
                    self.warning("Unhandled METADATA_BLOCK_HEADER.BLOCK_TYPE (" + BlockType_ + ") at offset " + BlockOffset_)
                # end if
            # end for
            info_["flac"][BlockTypeText_]["raw"] = None
            info_["avdataoffset"] = self.ftell()
            
            if LastBlockFlag_ == False:
                break
            # end if
        # end while
        #// handle tags
        if (not php_empty(lambda : info_["flac"]["VORBIS_COMMENT"]["comments"])):
            info_["flac"]["comments"] = info_["flac"]["VORBIS_COMMENT"]["comments"]
        # end if
        if (not php_empty(lambda : info_["flac"]["VORBIS_COMMENT"]["vendor"])):
            info_["audio"]["encoder"] = php_str_replace("reference ", "", info_["flac"]["VORBIS_COMMENT"]["vendor"])
        # end if
        #// copy attachments to 'comments' array if nesesary
        if (php_isset(lambda : info_["flac"]["PICTURE"])) and self.getid3.option_save_attachments != getID3.ATTACHMENTS_NONE:
            for entry_ in info_["flac"]["PICTURE"]:
                if (not php_empty(lambda : entry_["data"])):
                    if (not (php_isset(lambda : info_["flac"]["comments"]["picture"]))):
                        info_["flac"]["comments"]["picture"] = Array()
                    # end if
                    comments_picture_data_ = Array()
                    for picture_key_ in Array("data", "image_mime", "image_width", "image_height", "imagetype", "picturetype", "description", "datalength"):
                        if (php_isset(lambda : entry_[picture_key_])):
                            comments_picture_data_[picture_key_] = entry_[picture_key_]
                        # end if
                    # end for
                    info_["flac"]["comments"]["picture"][-1] = comments_picture_data_
                    comments_picture_data_ = None
                # end if
            # end for
        # end if
        if (php_isset(lambda : info_["flac"]["STREAMINFO"])):
            if (not self.isdependencyfor("matroska")):
                info_["flac"]["compressed_audio_bytes"] = info_["avdataend"] - info_["avdataoffset"]
            # end if
            info_["flac"]["uncompressed_audio_bytes"] = info_["flac"]["STREAMINFO"]["samples_stream"] * info_["flac"]["STREAMINFO"]["channels"] * info_["flac"]["STREAMINFO"]["bits_per_sample"] / 8
            if info_["flac"]["uncompressed_audio_bytes"] == 0:
                return self.error("Corrupt FLAC file: uncompressed_audio_bytes == zero")
            # end if
            if (not php_empty(lambda : info_["flac"]["compressed_audio_bytes"])):
                info_["flac"]["compression_ratio"] = info_["flac"]["compressed_audio_bytes"] / info_["flac"]["uncompressed_audio_bytes"]
            # end if
        # end if
        #// set md5_data_source - built into flac 0.5+
        if (php_isset(lambda : info_["flac"]["STREAMINFO"]["audio_signature"])):
            if info_["flac"]["STREAMINFO"]["audio_signature"] == php_str_repeat(" ", 16):
                self.warning("FLAC STREAMINFO.audio_signature is null (known issue with libOggFLAC)")
            else:
                info_["md5_data_source"] = ""
                md5_ = info_["flac"]["STREAMINFO"]["audio_signature"]
                i_ = 0
                while i_ < php_strlen(md5_):
                    
                    info_["md5_data_source"] += php_str_pad(dechex(php_ord(md5_[i_])), 2, "00", STR_PAD_LEFT)
                    i_ += 1
                # end while
                if (not php_preg_match("/^[0-9a-f]{32}$/", info_["md5_data_source"])):
                    info_["md5_data_source"] = None
                # end if
            # end if
        # end if
        if (php_isset(lambda : info_["flac"]["STREAMINFO"]["bits_per_sample"])):
            info_["audio"]["bits_per_sample"] = info_["flac"]["STREAMINFO"]["bits_per_sample"]
            if info_["audio"]["bits_per_sample"] == 8:
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
    def parsestreaminfodata(self, BlockData_=None):
        
        
        streaminfo_ = Array()
        streaminfo_["min_block_size"] = getid3_lib.bigendian2int(php_substr(BlockData_, 0, 2))
        streaminfo_["max_block_size"] = getid3_lib.bigendian2int(php_substr(BlockData_, 2, 2))
        streaminfo_["min_frame_size"] = getid3_lib.bigendian2int(php_substr(BlockData_, 4, 3))
        streaminfo_["max_frame_size"] = getid3_lib.bigendian2int(php_substr(BlockData_, 7, 3))
        SRCSBSS_ = getid3_lib.bigendian2bin(php_substr(BlockData_, 10, 8))
        streaminfo_["sample_rate"] = getid3_lib.bin2dec(php_substr(SRCSBSS_, 0, 20))
        streaminfo_["channels"] = getid3_lib.bin2dec(php_substr(SRCSBSS_, 20, 3)) + 1
        streaminfo_["bits_per_sample"] = getid3_lib.bin2dec(php_substr(SRCSBSS_, 23, 5)) + 1
        streaminfo_["samples_stream"] = getid3_lib.bin2dec(php_substr(SRCSBSS_, 28, 36))
        streaminfo_["audio_signature"] = php_substr(BlockData_, 18, 16)
        return streaminfo_
    # end def parsestreaminfodata
    #// 
    #// @param string $BlockData
    #// 
    #// @return bool
    #//
    def parsestreaminfo(self, BlockData_=None):
        
        
        info_ = self.getid3.info
        info_["flac"]["STREAMINFO"] = self.parsestreaminfodata(BlockData_)
        if (not php_empty(lambda : info_["flac"]["STREAMINFO"]["sample_rate"])):
            info_["audio"]["bitrate_mode"] = "vbr"
            info_["audio"]["sample_rate"] = info_["flac"]["STREAMINFO"]["sample_rate"]
            info_["audio"]["channels"] = info_["flac"]["STREAMINFO"]["channels"]
            info_["audio"]["bits_per_sample"] = info_["flac"]["STREAMINFO"]["bits_per_sample"]
            info_["playtime_seconds"] = info_["flac"]["STREAMINFO"]["samples_stream"] / info_["flac"]["STREAMINFO"]["sample_rate"]
            if info_["playtime_seconds"] > 0:
                if (not self.isdependencyfor("matroska")):
                    info_["audio"]["bitrate"] = info_["avdataend"] - info_["avdataoffset"] * 8 / info_["playtime_seconds"]
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
    def parseapplication(self, BlockData_=None):
        
        
        info_ = self.getid3.info
        ApplicationID_ = getid3_lib.bigendian2int(php_substr(BlockData_, 0, 4))
        info_["flac"]["APPLICATION"][ApplicationID_]["name"] = self.applicationidlookup(ApplicationID_)
        info_["flac"]["APPLICATION"][ApplicationID_]["data"] = php_substr(BlockData_, 4)
        return True
    # end def parseapplication
    #// 
    #// @param string $BlockData
    #// 
    #// @return bool
    #//
    def parseseektable(self, BlockData_=None):
        
        
        info_ = self.getid3.info
        offset_ = 0
        BlockLength_ = php_strlen(BlockData_)
        placeholderpattern_ = php_str_repeat("ÿ", 8)
        while True:
            
            if not (offset_ < BlockLength_):
                break
            # end if
            SampleNumberString_ = php_substr(BlockData_, offset_, 8)
            offset_ += 8
            if SampleNumberString_ == placeholderpattern_:
                #// placeholder point
                getid3_lib.safe_inc(info_["flac"]["SEEKTABLE"]["placeholders"], 1)
                offset_ += 10
            else:
                SampleNumber_ = getid3_lib.bigendian2int(SampleNumberString_)
                info_["flac"]["SEEKTABLE"][SampleNumber_]["offset"] = getid3_lib.bigendian2int(php_substr(BlockData_, offset_, 8))
                offset_ += 8
                info_["flac"]["SEEKTABLE"][SampleNumber_]["samples"] = getid3_lib.bigendian2int(php_substr(BlockData_, offset_, 2))
                offset_ += 2
            # end if
        # end while
        return True
    # end def parseseektable
    #// 
    #// @param string $BlockData
    #// 
    #// @return bool
    #//
    def parsevorbis_comment(self, BlockData_=None):
        
        
        info_ = self.getid3.info
        getid3_ogg_ = php_new_class("getid3_ogg", lambda : getid3_ogg(self.getid3))
        if self.isdependencyfor("matroska"):
            getid3_ogg_.setstringmode(self.data_string)
        # end if
        getid3_ogg_.parsevorbiscomments()
        if (php_isset(lambda : info_["ogg"])):
            info_["ogg"]["comments_raw"] = None
            info_["flac"]["VORBIS_COMMENT"] = info_["ogg"]
            info_["ogg"] = None
        # end if
        getid3_ogg_ = None
        return True
    # end def parsevorbis_comment
    #// 
    #// @param string $BlockData
    #// 
    #// @return bool
    #//
    def parsecuesheet(self, BlockData_=None):
        
        
        info_ = self.getid3.info
        offset_ = 0
        info_["flac"]["CUESHEET"]["media_catalog_number"] = php_trim(php_substr(BlockData_, offset_, 128), " ")
        offset_ += 128
        info_["flac"]["CUESHEET"]["lead_in_samples"] = getid3_lib.bigendian2int(php_substr(BlockData_, offset_, 8))
        offset_ += 8
        info_["flac"]["CUESHEET"]["flags"]["is_cd"] = php_bool(getid3_lib.bigendian2int(php_substr(BlockData_, offset_, 1)) & 128)
        offset_ += 1
        offset_ += 258
        #// reserved
        info_["flac"]["CUESHEET"]["number_tracks"] = getid3_lib.bigendian2int(php_substr(BlockData_, offset_, 1))
        offset_ += 1
        track_ = 0
        while track_ < info_["flac"]["CUESHEET"]["number_tracks"]:
            
            TrackSampleOffset_ = getid3_lib.bigendian2int(php_substr(BlockData_, offset_, 8))
            offset_ += 8
            TrackNumber_ = getid3_lib.bigendian2int(php_substr(BlockData_, offset_, 1))
            offset_ += 1
            info_["flac"]["CUESHEET"]["tracks"][TrackNumber_]["sample_offset"] = TrackSampleOffset_
            info_["flac"]["CUESHEET"]["tracks"][TrackNumber_]["isrc"] = php_substr(BlockData_, offset_, 12)
            offset_ += 12
            TrackFlagsRaw_ = getid3_lib.bigendian2int(php_substr(BlockData_, offset_, 1))
            offset_ += 1
            info_["flac"]["CUESHEET"]["tracks"][TrackNumber_]["flags"]["is_audio"] = php_bool(TrackFlagsRaw_ & 128)
            info_["flac"]["CUESHEET"]["tracks"][TrackNumber_]["flags"]["pre_emphasis"] = php_bool(TrackFlagsRaw_ & 64)
            offset_ += 13
            #// reserved
            info_["flac"]["CUESHEET"]["tracks"][TrackNumber_]["index_points"] = getid3_lib.bigendian2int(php_substr(BlockData_, offset_, 1))
            offset_ += 1
            index_ = 0
            while index_ < info_["flac"]["CUESHEET"]["tracks"][TrackNumber_]["index_points"]:
                
                IndexSampleOffset_ = getid3_lib.bigendian2int(php_substr(BlockData_, offset_, 8))
                offset_ += 8
                IndexNumber_ = getid3_lib.bigendian2int(php_substr(BlockData_, offset_, 1))
                offset_ += 1
                offset_ += 3
                #// reserved
                info_["flac"]["CUESHEET"]["tracks"][TrackNumber_]["indexes"][IndexNumber_] = IndexSampleOffset_
                index_ += 1
            # end while
            track_ += 1
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
        
        
        info_ = self.getid3.info
        picture_["typeid"] = getid3_lib.bigendian2int(self.fread(4))
        picture_["picturetype"] = self.picturetypelookup(picture_["typeid"])
        picture_["image_mime"] = self.fread(getid3_lib.bigendian2int(self.fread(4)))
        descr_length_ = getid3_lib.bigendian2int(self.fread(4))
        if descr_length_:
            picture_["description"] = self.fread(descr_length_)
        # end if
        picture_["image_width"] = getid3_lib.bigendian2int(self.fread(4))
        picture_["image_height"] = getid3_lib.bigendian2int(self.fread(4))
        picture_["color_depth"] = getid3_lib.bigendian2int(self.fread(4))
        picture_["colors_indexed"] = getid3_lib.bigendian2int(self.fread(4))
        picture_["datalength"] = getid3_lib.bigendian2int(self.fread(4))
        if picture_["image_mime"] == "-->":
            picture_["data"] = self.fread(picture_["datalength"])
        else:
            picture_["data"] = self.saveattachment(php_str_replace("/", "_", picture_["picturetype"]) + "_" + self.ftell(), self.ftell(), picture_["datalength"], picture_["image_mime"])
        # end if
        info_["flac"]["PICTURE"][-1] = picture_
        return True
    # end def parsepicture
    #// 
    #// @param int $blocktype
    #// 
    #// @return string
    #//
    @classmethod
    def metablocktypelookup(self, blocktype_=None):
        
        
        lookup_ = Array({0: "STREAMINFO", 1: "PADDING", 2: "APPLICATION", 3: "SEEKTABLE", 4: "VORBIS_COMMENT", 5: "CUESHEET", 6: "PICTURE"})
        return lookup_[blocktype_] if (php_isset(lambda : lookup_[blocktype_])) else "reserved"
    # end def metablocktypelookup
    #// 
    #// @param int $applicationid
    #// 
    #// @return string
    #//
    @classmethod
    def applicationidlookup(self, applicationid_=None):
        
        
        lookup_ = Array({1096041288: "FlacFile", 1112756044: "beSolo", 1112885075: "Bugs Player", 1131767155: "GoldWave cue points (specification)", 1181311841: "CUE Splitter", 1182035820: "flac-tools", 1297044546: "MOTB MetaCzar", 1297109829: "MP3 Stream Editor", 1299533132: "MusicML: Music Metadata Language", 1380533830: "Sound Devices RIFF chunk storage", 1397114444: "Sound Font FLAC", 1397706329: "Sony Creative Software", 1397835098: "flacsqueeze", 1416910710: "TwistedWave", 1430869075: "UITS Embedding tools", 1634297446: "FLAC AIFF chunk storage", 1768776039: "flac-image application for storing arbitrary files in APPLICATION metadata blocks", 1885693293: "Parseable Embedded Extensible Metadata (specification)", 1902539636: "QFLAC Studio", 1919510118: "FLAC RIFF chunk storage", 1953853029: "TagTuner", 2019713396: "XBAT", 2020434788: "xmcd"})
        return lookup_[applicationid_] if (php_isset(lambda : lookup_[applicationid_])) else "reserved"
    # end def applicationidlookup
    #// 
    #// @param int $type_id
    #// 
    #// @return string
    #//
    @classmethod
    def picturetypelookup(self, type_id_=None):
        
        
        lookup_ = Array({0: "Other", 1: "32x32 pixels 'file icon' (PNG only)", 2: "Other file icon", 3: "Cover (front)", 4: "Cover (back)", 5: "Leaflet page", 6: "Media (e.g. label side of CD)", 7: "Lead artist/lead performer/soloist", 8: "Artist/performer", 9: "Conductor", 10: "Band/Orchestra", 11: "Composer", 12: "Lyricist/text writer", 13: "Recording Location", 14: "During recording", 15: "During performance", 16: "Movie/video screen capture", 17: "A bright coloured fish", 18: "Illustration", 19: "Band/artist logotype", 20: "Publisher/Studio logotype"})
        return lookup_[type_id_] if (php_isset(lambda : lookup_[type_id_])) else "reserved"
    # end def picturetypelookup
# end class getid3_flac
