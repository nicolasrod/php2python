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
#// module.audio-video.flv.php
#// module for analyzing Shockwave Flash Video files
#// dependencies: NONE
#// 
#// 
#// 
#// FLV module by Seth Kaufman <sethØwhirl-i-gig*com>
#// 
#// version 0.1 (26 June 2005)
#// 
#// version 0.1.1 (15 July 2005)
#// minor modifications by James Heinrich <info@getid3.org>
#// 
#// version 0.2 (22 February 2006)
#// Support for On2 VP6 codec and meta information
#// by Steve Webster <steve.websterØfeaturecreep*com>
#// 
#// version 0.3 (15 June 2006)
#// Modified to not read entire file into memory
#// by James Heinrich <info@getid3.org>
#// 
#// version 0.4 (07 December 2007)
#// Bugfixes for incorrectly parsed FLV dimensions
#// and incorrect parsing of onMetaTag
#// by Evgeny Moysevich <moysevichØgmail*com>
#// 
#// version 0.5 (21 May 2009)
#// Fixed parsing of audio tags and added additional codec
#// details. The duration is now read from onMetaTag (if
#// exists), rather than parsing whole file
#// by Nigel Barnes <ngbarnesØhotmail*com>
#// 
#// version 0.6 (24 May 2009)
#// Better parsing of files with h264 video
#// by Evgeny Moysevich <moysevichØgmail*com>
#// 
#// version 0.6.1 (30 May 2011)
#// prevent infinite loops in expGolombUe()
#// 
#// version 0.7.0 (16 Jul 2013)
#// handle GETID3_FLV_VIDEO_VP6FLV_ALPHA
#// improved AVCSequenceParameterSetReader::readData()
#// by Xander Schouwerwou <schouwerwouØgmail*com>
#// 
#//
php_define("GETID3_FLV_TAG_AUDIO", 8)
php_define("GETID3_FLV_TAG_VIDEO", 9)
php_define("GETID3_FLV_TAG_META", 18)
php_define("GETID3_FLV_VIDEO_H263", 2)
php_define("GETID3_FLV_VIDEO_SCREEN", 3)
php_define("GETID3_FLV_VIDEO_VP6FLV", 4)
php_define("GETID3_FLV_VIDEO_VP6FLV_ALPHA", 5)
php_define("GETID3_FLV_VIDEO_SCREENV2", 6)
php_define("GETID3_FLV_VIDEO_H264", 7)
php_define("H264_AVC_SEQUENCE_HEADER", 0)
php_define("H264_PROFILE_BASELINE", 66)
php_define("H264_PROFILE_MAIN", 77)
php_define("H264_PROFILE_EXTENDED", 88)
php_define("H264_PROFILE_HIGH", 100)
php_define("H264_PROFILE_HIGH10", 110)
php_define("H264_PROFILE_HIGH422", 122)
php_define("H264_PROFILE_HIGH444", 144)
php_define("H264_PROFILE_HIGH444_PREDICTIVE", 244)
class getid3_flv(getid3_handler):
    magic = "FLV"
    #// 
    #// Break out of the loop if too many frames have been scanned; only scan this
    #// many if meta frame does not contain useful duration.
    #// 
    #// @var int
    #//
    max_frames = 100000
    #// 
    #// @return bool
    #//
    def analyze(self):
        
        
        info_ = self.getid3.info
        self.fseek(info_["avdataoffset"])
        FLVdataLength_ = info_["avdataend"] - info_["avdataoffset"]
        FLVheader_ = self.fread(5)
        info_["fileformat"] = "flv"
        info_["flv"]["header"]["signature"] = php_substr(FLVheader_, 0, 3)
        info_["flv"]["header"]["version"] = getid3_lib.bigendian2int(php_substr(FLVheader_, 3, 1))
        TypeFlags_ = getid3_lib.bigendian2int(php_substr(FLVheader_, 4, 1))
        if info_["flv"]["header"]["signature"] != self.magic:
            self.error("Expecting \"" + getid3_lib.printhexbytes(self.magic) + "\" at offset " + info_["avdataoffset"] + ", found \"" + getid3_lib.printhexbytes(info_["flv"]["header"]["signature"]) + "\"")
            info_["flv"] = None
            info_["fileformat"] = None
            return False
        # end if
        info_["flv"]["header"]["hasAudio"] = php_bool(TypeFlags_ & 4)
        info_["flv"]["header"]["hasVideo"] = php_bool(TypeFlags_ & 1)
        FrameSizeDataLength_ = getid3_lib.bigendian2int(self.fread(4))
        FLVheaderFrameLength_ = 9
        if FrameSizeDataLength_ > FLVheaderFrameLength_:
            self.fseek(FrameSizeDataLength_ - FLVheaderFrameLength_, SEEK_CUR)
        # end if
        Duration_ = 0
        found_video_ = False
        found_audio_ = False
        found_meta_ = False
        found_valid_meta_playtime_ = False
        tagParseCount_ = 0
        info_["flv"]["framecount"] = Array({"total": 0, "audio": 0, "video": 0})
        flv_framecount_ = info_["flv"]["framecount"]
        while True:
            tagParseCount_ += 1
            if not (self.ftell() + 16 < info_["avdataend"] and tagParseCount_ <= self.max_frames or (not found_valid_meta_playtime_)):
                break
            # end if
            ThisTagHeader_ = self.fread(16)
            tagParseCount_ += 1
            PreviousTagLength_ = getid3_lib.bigendian2int(php_substr(ThisTagHeader_, 0, 4))
            TagType_ = getid3_lib.bigendian2int(php_substr(ThisTagHeader_, 4, 1))
            DataLength_ = getid3_lib.bigendian2int(php_substr(ThisTagHeader_, 5, 3))
            Timestamp_ = getid3_lib.bigendian2int(php_substr(ThisTagHeader_, 8, 3))
            LastHeaderByte_ = getid3_lib.bigendian2int(php_substr(ThisTagHeader_, 15, 1))
            NextOffset_ = self.ftell() - 1 + DataLength_
            if Timestamp_ > Duration_:
                Duration_ = Timestamp_
            # end if
            flv_framecount_["total"] += 1
            for case in Switch(TagType_):
                if case(GETID3_FLV_TAG_AUDIO):
                    flv_framecount_["audio"] += 1
                    if (not found_audio_):
                        found_audio_ = True
                        info_["flv"]["audio"]["audioFormat"] = LastHeaderByte_ >> 4 & 15
                        info_["flv"]["audio"]["audioRate"] = LastHeaderByte_ >> 2 & 3
                        info_["flv"]["audio"]["audioSampleSize"] = LastHeaderByte_ >> 1 & 1
                        info_["flv"]["audio"]["audioType"] = LastHeaderByte_ & 1
                    # end if
                    break
                # end if
                if case(GETID3_FLV_TAG_VIDEO):
                    flv_framecount_["video"] += 1
                    if (not found_video_):
                        found_video_ = True
                        info_["flv"]["video"]["videoCodec"] = LastHeaderByte_ & 7
                        FLVvideoHeader_ = self.fread(11)
                        if info_["flv"]["video"]["videoCodec"] == GETID3_FLV_VIDEO_H264:
                            #// this code block contributed by: moysevichØgmail*com
                            AVCPacketType_ = getid3_lib.bigendian2int(php_substr(FLVvideoHeader_, 0, 1))
                            if AVCPacketType_ == H264_AVC_SEQUENCE_HEADER:
                                #// read AVCDecoderConfigurationRecord
                                configurationVersion_ = getid3_lib.bigendian2int(php_substr(FLVvideoHeader_, 4, 1))
                                AVCProfileIndication_ = getid3_lib.bigendian2int(php_substr(FLVvideoHeader_, 5, 1))
                                profile_compatibility_ = getid3_lib.bigendian2int(php_substr(FLVvideoHeader_, 6, 1))
                                lengthSizeMinusOne_ = getid3_lib.bigendian2int(php_substr(FLVvideoHeader_, 7, 1))
                                numOfSequenceParameterSets_ = getid3_lib.bigendian2int(php_substr(FLVvideoHeader_, 8, 1))
                                if numOfSequenceParameterSets_ & 31 != 0:
                                    #// there is at least one SequenceParameterSet
                                    #// read size of the first SequenceParameterSet
                                    #// $spsSize = getid3_lib::BigEndian2Int(substr($FLVvideoHeader, 9, 2));
                                    spsSize_ = getid3_lib.littleendian2int(php_substr(FLVvideoHeader_, 9, 2))
                                    #// read the first SequenceParameterSet
                                    sps_ = self.fread(spsSize_)
                                    if php_strlen(sps_) == spsSize_:
                                        #// make sure that whole SequenceParameterSet was red
                                        spsReader_ = php_new_class("AVCSequenceParameterSetReader", lambda : AVCSequenceParameterSetReader(sps_))
                                        spsReader_.readdata()
                                        info_["video"]["resolution_x"] = spsReader_.getwidth()
                                        info_["video"]["resolution_y"] = spsReader_.getheight()
                                    # end if
                                # end if
                            # end if
                            pass
                        elif info_["flv"]["video"]["videoCodec"] == GETID3_FLV_VIDEO_H263:
                            PictureSizeType_ = getid3_lib.bigendian2int(php_substr(FLVvideoHeader_, 3, 2)) >> 7
                            PictureSizeType_ = PictureSizeType_ & 7
                            info_["flv"]["header"]["videoSizeType"] = PictureSizeType_
                            for case in Switch(PictureSizeType_):
                                if case(0):
                                    #// $PictureSizeEnc = getid3_lib::BigEndian2Int(substr($FLVvideoHeader, 5, 2));
                                    #// $PictureSizeEnc <<= 1;
                                    #// $info['video']['resolution_x'] = ($PictureSizeEnc & 0xFF00) >> 8;
                                    #// $PictureSizeEnc = getid3_lib::BigEndian2Int(substr($FLVvideoHeader, 6, 2));
                                    #// $PictureSizeEnc <<= 1;
                                    #// $info['video']['resolution_y'] = ($PictureSizeEnc & 0xFF00) >> 8;
                                    PictureSizeEnc_["x"] = getid3_lib.bigendian2int(php_substr(FLVvideoHeader_, 4, 2)) >> 7
                                    PictureSizeEnc_["y"] = getid3_lib.bigendian2int(php_substr(FLVvideoHeader_, 5, 2)) >> 7
                                    info_["video"]["resolution_x"] = PictureSizeEnc_["x"] & 255
                                    info_["video"]["resolution_y"] = PictureSizeEnc_["y"] & 255
                                    break
                                # end if
                                if case(1):
                                    PictureSizeEnc_["x"] = getid3_lib.bigendian2int(php_substr(FLVvideoHeader_, 4, 3)) >> 7
                                    PictureSizeEnc_["y"] = getid3_lib.bigendian2int(php_substr(FLVvideoHeader_, 6, 3)) >> 7
                                    info_["video"]["resolution_x"] = PictureSizeEnc_["x"] & 65535
                                    info_["video"]["resolution_y"] = PictureSizeEnc_["y"] & 65535
                                    break
                                # end if
                                if case(2):
                                    info_["video"]["resolution_x"] = 352
                                    info_["video"]["resolution_y"] = 288
                                    break
                                # end if
                                if case(3):
                                    info_["video"]["resolution_x"] = 176
                                    info_["video"]["resolution_y"] = 144
                                    break
                                # end if
                                if case(4):
                                    info_["video"]["resolution_x"] = 128
                                    info_["video"]["resolution_y"] = 96
                                    break
                                # end if
                                if case(5):
                                    info_["video"]["resolution_x"] = 320
                                    info_["video"]["resolution_y"] = 240
                                    break
                                # end if
                                if case(6):
                                    info_["video"]["resolution_x"] = 160
                                    info_["video"]["resolution_y"] = 120
                                    break
                                # end if
                                if case():
                                    info_["video"]["resolution_x"] = 0
                                    info_["video"]["resolution_y"] = 0
                                    break
                                # end if
                            # end for
                        elif info_["flv"]["video"]["videoCodec"] == GETID3_FLV_VIDEO_VP6FLV_ALPHA:
                            #// contributed by schouwerwouØgmail*com
                            if (not (php_isset(lambda : info_["video"]["resolution_x"]))):
                                #// only when meta data isn't set
                                PictureSizeEnc_["x"] = getid3_lib.bigendian2int(php_substr(FLVvideoHeader_, 6, 2))
                                PictureSizeEnc_["y"] = getid3_lib.bigendian2int(php_substr(FLVvideoHeader_, 7, 2))
                                info_["video"]["resolution_x"] = PictureSizeEnc_["x"] & 255 << 3
                                info_["video"]["resolution_y"] = PictureSizeEnc_["y"] & 255 << 3
                            # end if
                            pass
                        # end if
                        if (not php_empty(lambda : info_["video"]["resolution_x"])) and (not php_empty(lambda : info_["video"]["resolution_y"])):
                            info_["video"]["pixel_aspect_ratio"] = info_["video"]["resolution_x"] / info_["video"]["resolution_y"]
                        # end if
                    # end if
                    break
                # end if
                if case(GETID3_FLV_TAG_META):
                    if (not found_meta_):
                        found_meta_ = True
                        self.fseek(-1, SEEK_CUR)
                        datachunk_ = self.fread(DataLength_)
                        AMFstream_ = php_new_class("AMFStream", lambda : AMFStream(datachunk_))
                        reader_ = php_new_class("AMFReader", lambda : AMFReader(AMFstream_))
                        eventName_ = reader_.readdata()
                        info_["flv"]["meta"][eventName_] = reader_.readdata()
                        reader_ = None
                        copykeys_ = Array({"framerate": "frame_rate", "width": "resolution_x", "height": "resolution_y", "audiodatarate": "bitrate", "videodatarate": "bitrate"})
                        for sourcekey_,destkey_ in copykeys_.items():
                            if (php_isset(lambda : info_["flv"]["meta"]["onMetaData"][sourcekey_])):
                                for case in Switch(sourcekey_):
                                    if case("width"):
                                        pass
                                    # end if
                                    if case("height"):
                                        info_["video"][destkey_] = php_intval(round(info_["flv"]["meta"]["onMetaData"][sourcekey_]))
                                        break
                                    # end if
                                    if case("audiodatarate"):
                                        info_["audio"][destkey_] = getid3_lib.castasint(round(info_["flv"]["meta"]["onMetaData"][sourcekey_] * 1000))
                                        break
                                    # end if
                                    if case("videodatarate"):
                                        pass
                                    # end if
                                    if case("frame_rate"):
                                        pass
                                    # end if
                                    if case():
                                        info_["video"][destkey_] = info_["flv"]["meta"]["onMetaData"][sourcekey_]
                                        break
                                    # end if
                                # end for
                            # end if
                        # end for
                        if (not php_empty(lambda : info_["flv"]["meta"]["onMetaData"]["duration"])):
                            found_valid_meta_playtime_ = True
                        # end if
                    # end if
                    break
                # end if
                if case():
                    break
                # end if
            # end for
            self.fseek(NextOffset_)
        # end while
        info_["playtime_seconds"] = Duration_ / 1000
        if info_["playtime_seconds"] > 0:
            info_["bitrate"] = info_["avdataend"] - info_["avdataoffset"] * 8 / info_["playtime_seconds"]
        # end if
        if info_["flv"]["header"]["hasAudio"]:
            info_["audio"]["codec"] = self.audioformatlookup(info_["flv"]["audio"]["audioFormat"])
            info_["audio"]["sample_rate"] = self.audioratelookup(info_["flv"]["audio"]["audioRate"])
            info_["audio"]["bits_per_sample"] = self.audiobitdepthlookup(info_["flv"]["audio"]["audioSampleSize"])
            info_["audio"]["channels"] = info_["flv"]["audio"]["audioType"] + 1
            #// 0=mono,1=stereo
            info_["audio"]["lossless"] = False if info_["flv"]["audio"]["audioFormat"] else True
            #// 0=uncompressed
            info_["audio"]["dataformat"] = "flv"
        # end if
        if (not php_empty(lambda : info_["flv"]["header"]["hasVideo"])):
            info_["video"]["codec"] = self.videocodeclookup(info_["flv"]["video"]["videoCodec"])
            info_["video"]["dataformat"] = "flv"
            info_["video"]["lossless"] = False
        # end if
        #// Set information from meta
        if (not php_empty(lambda : info_["flv"]["meta"]["onMetaData"]["duration"])):
            info_["playtime_seconds"] = info_["flv"]["meta"]["onMetaData"]["duration"]
            info_["bitrate"] = info_["avdataend"] - info_["avdataoffset"] * 8 / info_["playtime_seconds"]
        # end if
        if (php_isset(lambda : info_["flv"]["meta"]["onMetaData"]["audiocodecid"])):
            info_["audio"]["codec"] = self.audioformatlookup(info_["flv"]["meta"]["onMetaData"]["audiocodecid"])
        # end if
        if (php_isset(lambda : info_["flv"]["meta"]["onMetaData"]["videocodecid"])):
            info_["video"]["codec"] = self.videocodeclookup(info_["flv"]["meta"]["onMetaData"]["videocodecid"])
        # end if
        return True
    # end def analyze
    #// 
    #// @param int $id
    #// 
    #// @return string|false
    #//
    @classmethod
    def audioformatlookup(self, id_=None):
        
        
        lookup_ = Array({0: "Linear PCM, platform endian", 1: "ADPCM", 2: "mp3", 3: "Linear PCM, little endian", 4: "Nellymoser 16kHz mono", 5: "Nellymoser 8kHz mono", 6: "Nellymoser", 7: "G.711A-law logarithmic PCM", 8: "G.711 mu-law logarithmic PCM", 9: "reserved", 10: "AAC", 11: "Speex", 12: False, 13: False, 14: "mp3 8kHz", 15: "Device-specific sound"})
        return lookup_[id_] if (php_isset(lambda : lookup_[id_])) else False
    # end def audioformatlookup
    #// 
    #// @param int $id
    #// 
    #// @return int|false
    #//
    @classmethod
    def audioratelookup(self, id_=None):
        
        
        lookup_ = Array({0: 5500, 1: 11025, 2: 22050, 3: 44100})
        return lookup_[id_] if (php_isset(lambda : lookup_[id_])) else False
    # end def audioratelookup
    #// 
    #// @param int $id
    #// 
    #// @return int|false
    #//
    @classmethod
    def audiobitdepthlookup(self, id_=None):
        
        
        lookup_ = Array({0: 8, 1: 16})
        return lookup_[id_] if (php_isset(lambda : lookup_[id_])) else False
    # end def audiobitdepthlookup
    #// 
    #// @param int $id
    #// 
    #// @return string|false
    #//
    @classmethod
    def videocodeclookup(self, id_=None):
        
        
        lookup_ = Array({GETID3_FLV_VIDEO_H263: "Sorenson H.263", GETID3_FLV_VIDEO_SCREEN: "Screen video", GETID3_FLV_VIDEO_VP6FLV: "On2 VP6", GETID3_FLV_VIDEO_VP6FLV_ALPHA: "On2 VP6 with alpha channel", GETID3_FLV_VIDEO_SCREENV2: "Screen video v2", GETID3_FLV_VIDEO_H264: "Sorenson H.264"})
        return lookup_[id_] if (php_isset(lambda : lookup_[id_])) else False
    # end def videocodeclookup
# end class getid3_flv
class AMFStream():
    #// 
    #// @var string
    #//
    bytes = Array()
    #// 
    #// @var int
    #//
    pos = Array()
    #// 
    #// @param string $bytes
    #//
    def __init__(self, bytes_=None):
        
        
        self.bytes = bytes_
        self.pos = 0
    # end def __init__
    #// 
    #// @return int
    #//
    def readbyte(self):
        
        
        #// 8-bit
        self.pos += 1
        return php_ord(php_substr(self.bytes, self.pos, 1))
        self.pos += 1
    # end def readbyte
    #// 
    #// @return int
    #//
    def readint(self):
        
        
        #// 16-bit
        return self.readbyte() << 8 + self.readbyte()
    # end def readint
    #// 
    #// @return int
    #//
    def readlong(self):
        
        
        #// 32-bit
        return self.readbyte() << 24 + self.readbyte() << 16 + self.readbyte() << 8 + self.readbyte()
    # end def readlong
    #// 
    #// @return float|false
    #//
    def readdouble(self):
        
        
        return getid3_lib.bigendian2float(self.read(8))
    # end def readdouble
    #// 
    #// @return string
    #//
    def readutf(self):
        
        
        length_ = self.readint()
        return self.read(length_)
    # end def readutf
    #// 
    #// @return string
    #//
    def readlongutf(self):
        
        
        length_ = self.readlong()
        return self.read(length_)
    # end def readlongutf
    #// 
    #// @param int $length
    #// 
    #// @return string
    #//
    def read(self, length_=None):
        
        
        val_ = php_substr(self.bytes, self.pos, length_)
        self.pos += length_
        return val_
    # end def read
    #// 
    #// @return int
    #//
    def peekbyte(self):
        
        
        pos_ = self.pos
        val_ = self.readbyte()
        self.pos = pos_
        return val_
    # end def peekbyte
    #// 
    #// @return int
    #//
    def peekint(self):
        
        
        pos_ = self.pos
        val_ = self.readint()
        self.pos = pos_
        return val_
    # end def peekint
    #// 
    #// @return int
    #//
    def peeklong(self):
        
        
        pos_ = self.pos
        val_ = self.readlong()
        self.pos = pos_
        return val_
    # end def peeklong
    #// 
    #// @return float|false
    #//
    def peekdouble(self):
        
        
        pos_ = self.pos
        val_ = self.readdouble()
        self.pos = pos_
        return val_
    # end def peekdouble
    #// 
    #// @return string
    #//
    def peekutf(self):
        
        
        pos_ = self.pos
        val_ = self.readutf()
        self.pos = pos_
        return val_
    # end def peekutf
    #// 
    #// @return string
    #//
    def peeklongutf(self):
        
        
        pos_ = self.pos
        val_ = self.readlongutf()
        self.pos = pos_
        return val_
    # end def peeklongutf
# end class AMFStream
class AMFReader():
    #// 
    #// @var AMFStream
    #//
    stream = Array()
    #// 
    #// @param AMFStream $stream
    #//
    def __init__(self, stream_=None):
        
        
        self.stream = stream_
    # end def __init__
    #// 
    #// @return mixed
    #//
    def readdata(self):
        
        
        value_ = None
        type_ = self.stream.readbyte()
        for case in Switch(type_):
            if case(0):
                value_ = self.readdouble()
                break
            # end if
            if case(1):
                value_ = self.readboolean()
                break
            # end if
            if case(2):
                value_ = self.readstring()
                break
            # end if
            if case(3):
                value_ = self.readobject()
                break
            # end if
            if case(6):
                return None
                break
            # end if
            if case(8):
                value_ = self.readmixedarray()
                break
            # end if
            if case(10):
                value_ = self.readarray()
                break
            # end if
            if case(11):
                value_ = self.readdate()
                break
            # end if
            if case(13):
                value_ = self.readlongstring()
                break
            # end if
            if case(15):
                value_ = self.readxml()
                break
            # end if
            if case(16):
                value_ = self.readtypedobject()
                break
            # end if
            if case():
                value_ = "(unknown or unsupported data type)"
                break
            # end if
        # end for
        return value_
    # end def readdata
    #// 
    #// @return float|false
    #//
    def readdouble(self):
        
        
        return self.stream.readdouble()
    # end def readdouble
    #// 
    #// @return bool
    #//
    def readboolean(self):
        
        
        return self.stream.readbyte() == 1
    # end def readboolean
    #// 
    #// @return string
    #//
    def readstring(self):
        
        
        return self.stream.readutf()
    # end def readstring
    #// 
    #// @return array
    #//
    def readobject(self):
        
        
        #// Get highest numerical index - ignored
        #// $highestIndex = $this->stream->readLong();
        data_ = Array()
        key_ = None
        while True:
            key_ = self.stream.readutf()
            if not (key_):
                break
            # end if
            data_[key_] = self.readdata()
        # end while
        #// Mixed array record ends with empty string (0x00 0x00) and 0x09
        if key_ == "" and self.stream.peekbyte() == 9:
            #// Consume byte
            self.stream.readbyte()
        # end if
        return data_
    # end def readobject
    #// 
    #// @return array
    #//
    def readmixedarray(self):
        
        
        #// Get highest numerical index - ignored
        highestIndex_ = self.stream.readlong()
        data_ = Array()
        key_ = None
        while True:
            key_ = self.stream.readutf()
            if not (key_):
                break
            # end if
            if php_is_numeric(key_):
                key_ = php_int(key_)
            # end if
            data_[key_] = self.readdata()
        # end while
        #// Mixed array record ends with empty string (0x00 0x00) and 0x09
        if key_ == "" and self.stream.peekbyte() == 9:
            #// Consume byte
            self.stream.readbyte()
        # end if
        return data_
    # end def readmixedarray
    #// 
    #// @return array
    #//
    def readarray(self):
        
        
        length_ = self.stream.readlong()
        data_ = Array()
        i_ = 0
        while i_ < length_:
            
            data_[-1] = self.readdata()
            i_ += 1
        # end while
        return data_
    # end def readarray
    #// 
    #// @return float|false
    #//
    def readdate(self):
        
        
        timestamp_ = self.stream.readdouble()
        timezone_ = self.stream.readint()
        return timestamp_
    # end def readdate
    #// 
    #// @return string
    #//
    def readlongstring(self):
        
        
        return self.stream.readlongutf()
    # end def readlongstring
    #// 
    #// @return string
    #//
    def readxml(self):
        
        
        return self.stream.readlongutf()
    # end def readxml
    #// 
    #// @return array
    #//
    def readtypedobject(self):
        
        
        className_ = self.stream.readutf()
        return self.readobject()
    # end def readtypedobject
# end class AMFReader
class AVCSequenceParameterSetReader():
    #// 
    #// @var string
    #//
    sps = Array()
    start = 0
    currentBytes = 0
    currentBits = 0
    #// 
    #// @var int
    #//
    width = Array()
    #// 
    #// @var int
    #//
    height = Array()
    #// 
    #// @param string $sps
    #//
    def __init__(self, sps_=None):
        
        
        self.sps = sps_
    # end def __init__
    def readdata(self):
        
        
        self.skipbits(8)
        self.skipbits(8)
        profile_ = self.getbits(8)
        #// read profile
        if profile_ > 0:
            self.skipbits(8)
            level_idc_ = self.getbits(8)
            #// level_idc
            self.expgolombue()
            #// seq_parameter_set_id // sps
            self.expgolombue()
            #// log2_max_frame_num_minus4
            picOrderType_ = self.expgolombue()
            #// pic_order_cnt_type
            if picOrderType_ == 0:
                self.expgolombue()
                pass
            elif picOrderType_ == 1:
                self.skipbits(1)
                #// delta_pic_order_always_zero_flag
                self.expgolombse()
                #// offset_for_non_ref_pic
                self.expgolombse()
                #// offset_for_top_to_bottom_field
                num_ref_frames_in_pic_order_cnt_cycle_ = self.expgolombue()
                #// num_ref_frames_in_pic_order_cnt_cycle
                i_ = 0
                while i_ < num_ref_frames_in_pic_order_cnt_cycle_:
                    
                    self.expgolombse()
                    pass
                    i_ += 1
                # end while
            # end if
            self.expgolombue()
            #// num_ref_frames
            self.skipbits(1)
            #// gaps_in_frame_num_value_allowed_flag
            pic_width_in_mbs_minus1_ = self.expgolombue()
            #// pic_width_in_mbs_minus1
            pic_height_in_map_units_minus1_ = self.expgolombue()
            #// pic_height_in_map_units_minus1
            frame_mbs_only_flag_ = self.getbits(1)
            #// frame_mbs_only_flag
            if frame_mbs_only_flag_ == 0:
                self.skipbits(1)
                pass
            # end if
            self.skipbits(1)
            #// direct_8x8_inference_flag
            frame_cropping_flag_ = self.getbits(1)
            #// frame_cropping_flag
            frame_crop_left_offset_ = 0
            frame_crop_right_offset_ = 0
            frame_crop_top_offset_ = 0
            frame_crop_bottom_offset_ = 0
            if frame_cropping_flag_:
                frame_crop_left_offset_ = self.expgolombue()
                #// frame_crop_left_offset
                frame_crop_right_offset_ = self.expgolombue()
                #// frame_crop_right_offset
                frame_crop_top_offset_ = self.expgolombue()
                #// frame_crop_top_offset
                frame_crop_bottom_offset_ = self.expgolombue()
                pass
            # end if
            self.skipbits(1)
            #// vui_parameters_present_flag
            #// etc
            self.width = pic_width_in_mbs_minus1_ + 1 * 16 - frame_crop_left_offset_ * 2 - frame_crop_right_offset_ * 2
            self.height = 2 - frame_mbs_only_flag_ * pic_height_in_map_units_minus1_ + 1 * 16 - frame_crop_top_offset_ * 2 - frame_crop_bottom_offset_ * 2
        # end if
    # end def readdata
    #// 
    #// @param int $bits
    #//
    def skipbits(self, bits_=None):
        
        
        newBits_ = self.currentBits + bits_
        self.currentBytes += php_int(floor(newBits_ / 8))
        self.currentBits = newBits_ % 8
    # end def skipbits
    #// 
    #// @return int
    #//
    def getbit(self):
        
        
        result_ = getid3_lib.bigendian2int(php_substr(self.sps, self.currentBytes, 1)) >> 7 - self.currentBits & 1
        self.skipbits(1)
        return result_
    # end def getbit
    #// 
    #// @param int $bits
    #// 
    #// @return int
    #//
    def getbits(self, bits_=None):
        
        
        result_ = 0
        i_ = 0
        while i_ < bits_:
            
            result_ = result_ << 1 + self.getbit()
            i_ += 1
        # end while
        return result_
    # end def getbits
    #// 
    #// @return int
    #//
    def expgolombue(self):
        
        
        significantBits_ = 0
        bit_ = self.getbit()
        while True:
            
            if not (bit_ == 0):
                break
            # end if
            significantBits_ += 1
            bit_ = self.getbit()
            if significantBits_ > 31:
                #// something is broken, this is an emergency escape to prevent infinite loops
                return 0
            # end if
        # end while
        return 1 << significantBits_ + self.getbits(significantBits_) - 1
    # end def expgolombue
    #// 
    #// @return int
    #//
    def expgolombse(self):
        
        
        result_ = self.expgolombue()
        if result_ & 1 == 0:
            return -result_ >> 1
        else:
            return result_ + 1 >> 1
        # end if
    # end def expgolombse
    #// 
    #// @return int
    #//
    def getwidth(self):
        
        
        return self.width
    # end def getwidth
    #// 
    #// @return int
    #//
    def getheight(self):
        
        
        return self.height
    # end def getheight
# end class AVCSequenceParameterSetReader
