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
    max_frames = 100000
    #// 
    #// @return bool
    #//
    def analyze(self):
        
        info = self.getid3.info
        self.fseek(info["avdataoffset"])
        FLVdataLength = info["avdataend"] - info["avdataoffset"]
        FLVheader = self.fread(5)
        info["fileformat"] = "flv"
        info["flv"]["header"]["signature"] = php_substr(FLVheader, 0, 3)
        info["flv"]["header"]["version"] = getid3_lib.bigendian2int(php_substr(FLVheader, 3, 1))
        TypeFlags = getid3_lib.bigendian2int(php_substr(FLVheader, 4, 1))
        if info["flv"]["header"]["signature"] != self.magic:
            self.error("Expecting \"" + getid3_lib.printhexbytes(self.magic) + "\" at offset " + info["avdataoffset"] + ", found \"" + getid3_lib.printhexbytes(info["flv"]["header"]["signature"]) + "\"")
            info["flv"] = None
            info["fileformat"] = None
            return False
        # end if
        info["flv"]["header"]["hasAudio"] = php_bool(TypeFlags & 4)
        info["flv"]["header"]["hasVideo"] = php_bool(TypeFlags & 1)
        FrameSizeDataLength = getid3_lib.bigendian2int(self.fread(4))
        FLVheaderFrameLength = 9
        if FrameSizeDataLength > FLVheaderFrameLength:
            self.fseek(FrameSizeDataLength - FLVheaderFrameLength, SEEK_CUR)
        # end if
        Duration = 0
        found_video = False
        found_audio = False
        found_meta = False
        found_valid_meta_playtime = False
        tagParseCount = 0
        info["flv"]["framecount"] = Array({"total": 0, "audio": 0, "video": 0})
        flv_framecount = info["flv"]["framecount"]
        while True:
            
            if not (self.ftell() + 16 < info["avdataend"] and tagParseCount <= self.max_frames or (not found_valid_meta_playtime)):
                break
            # end if
            ThisTagHeader = self.fread(16)
            tagParseCount += 1
            PreviousTagLength = getid3_lib.bigendian2int(php_substr(ThisTagHeader, 0, 4))
            TagType = getid3_lib.bigendian2int(php_substr(ThisTagHeader, 4, 1))
            DataLength = getid3_lib.bigendian2int(php_substr(ThisTagHeader, 5, 3))
            Timestamp = getid3_lib.bigendian2int(php_substr(ThisTagHeader, 8, 3))
            LastHeaderByte = getid3_lib.bigendian2int(php_substr(ThisTagHeader, 15, 1))
            NextOffset = self.ftell() - 1 + DataLength
            if Timestamp > Duration:
                Duration = Timestamp
            # end if
            flv_framecount["total"] += 1
            for case in Switch(TagType):
                if case(GETID3_FLV_TAG_AUDIO):
                    flv_framecount["audio"] += 1
                    if (not found_audio):
                        found_audio = True
                        info["flv"]["audio"]["audioFormat"] = LastHeaderByte >> 4 & 15
                        info["flv"]["audio"]["audioRate"] = LastHeaderByte >> 2 & 3
                        info["flv"]["audio"]["audioSampleSize"] = LastHeaderByte >> 1 & 1
                        info["flv"]["audio"]["audioType"] = LastHeaderByte & 1
                    # end if
                    break
                # end if
                if case(GETID3_FLV_TAG_VIDEO):
                    flv_framecount["video"] += 1
                    if (not found_video):
                        found_video = True
                        info["flv"]["video"]["videoCodec"] = LastHeaderByte & 7
                        FLVvideoHeader = self.fread(11)
                        if info["flv"]["video"]["videoCodec"] == GETID3_FLV_VIDEO_H264:
                            #// this code block contributed by: moysevichØgmail*com
                            AVCPacketType = getid3_lib.bigendian2int(php_substr(FLVvideoHeader, 0, 1))
                            if AVCPacketType == H264_AVC_SEQUENCE_HEADER:
                                #// read AVCDecoderConfigurationRecord
                                configurationVersion = getid3_lib.bigendian2int(php_substr(FLVvideoHeader, 4, 1))
                                AVCProfileIndication = getid3_lib.bigendian2int(php_substr(FLVvideoHeader, 5, 1))
                                profile_compatibility = getid3_lib.bigendian2int(php_substr(FLVvideoHeader, 6, 1))
                                lengthSizeMinusOne = getid3_lib.bigendian2int(php_substr(FLVvideoHeader, 7, 1))
                                numOfSequenceParameterSets = getid3_lib.bigendian2int(php_substr(FLVvideoHeader, 8, 1))
                                if numOfSequenceParameterSets & 31 != 0:
                                    #// there is at least one SequenceParameterSet
                                    #// read size of the first SequenceParameterSet
                                    #// $spsSize = getid3_lib::BigEndian2Int(substr($FLVvideoHeader, 9, 2));
                                    spsSize = getid3_lib.littleendian2int(php_substr(FLVvideoHeader, 9, 2))
                                    #// read the first SequenceParameterSet
                                    sps = self.fread(spsSize)
                                    if php_strlen(sps) == spsSize:
                                        #// make sure that whole SequenceParameterSet was red
                                        spsReader = php_new_class("AVCSequenceParameterSetReader", lambda : AVCSequenceParameterSetReader(sps))
                                        spsReader.readdata()
                                        info["video"]["resolution_x"] = spsReader.getwidth()
                                        info["video"]["resolution_y"] = spsReader.getheight()
                                    # end if
                                # end if
                            # end if
                            pass
                        elif info["flv"]["video"]["videoCodec"] == GETID3_FLV_VIDEO_H263:
                            PictureSizeType = getid3_lib.bigendian2int(php_substr(FLVvideoHeader, 3, 2)) >> 7
                            PictureSizeType = PictureSizeType & 7
                            info["flv"]["header"]["videoSizeType"] = PictureSizeType
                            for case in Switch(PictureSizeType):
                                if case(0):
                                    #// $PictureSizeEnc = getid3_lib::BigEndian2Int(substr($FLVvideoHeader, 5, 2));
                                    #// $PictureSizeEnc <<= 1;
                                    #// $info['video']['resolution_x'] = ($PictureSizeEnc & 0xFF00) >> 8;
                                    #// $PictureSizeEnc = getid3_lib::BigEndian2Int(substr($FLVvideoHeader, 6, 2));
                                    #// $PictureSizeEnc <<= 1;
                                    #// $info['video']['resolution_y'] = ($PictureSizeEnc & 0xFF00) >> 8;
                                    PictureSizeEnc["x"] = getid3_lib.bigendian2int(php_substr(FLVvideoHeader, 4, 2)) >> 7
                                    PictureSizeEnc["y"] = getid3_lib.bigendian2int(php_substr(FLVvideoHeader, 5, 2)) >> 7
                                    info["video"]["resolution_x"] = PictureSizeEnc["x"] & 255
                                    info["video"]["resolution_y"] = PictureSizeEnc["y"] & 255
                                    break
                                # end if
                                if case(1):
                                    PictureSizeEnc["x"] = getid3_lib.bigendian2int(php_substr(FLVvideoHeader, 4, 3)) >> 7
                                    PictureSizeEnc["y"] = getid3_lib.bigendian2int(php_substr(FLVvideoHeader, 6, 3)) >> 7
                                    info["video"]["resolution_x"] = PictureSizeEnc["x"] & 65535
                                    info["video"]["resolution_y"] = PictureSizeEnc["y"] & 65535
                                    break
                                # end if
                                if case(2):
                                    info["video"]["resolution_x"] = 352
                                    info["video"]["resolution_y"] = 288
                                    break
                                # end if
                                if case(3):
                                    info["video"]["resolution_x"] = 176
                                    info["video"]["resolution_y"] = 144
                                    break
                                # end if
                                if case(4):
                                    info["video"]["resolution_x"] = 128
                                    info["video"]["resolution_y"] = 96
                                    break
                                # end if
                                if case(5):
                                    info["video"]["resolution_x"] = 320
                                    info["video"]["resolution_y"] = 240
                                    break
                                # end if
                                if case(6):
                                    info["video"]["resolution_x"] = 160
                                    info["video"]["resolution_y"] = 120
                                    break
                                # end if
                                if case():
                                    info["video"]["resolution_x"] = 0
                                    info["video"]["resolution_y"] = 0
                                    break
                                # end if
                            # end for
                        elif info["flv"]["video"]["videoCodec"] == GETID3_FLV_VIDEO_VP6FLV_ALPHA:
                            #// contributed by schouwerwouØgmail*com
                            if (not (php_isset(lambda : info["video"]["resolution_x"]))):
                                #// only when meta data isn't set
                                PictureSizeEnc["x"] = getid3_lib.bigendian2int(php_substr(FLVvideoHeader, 6, 2))
                                PictureSizeEnc["y"] = getid3_lib.bigendian2int(php_substr(FLVvideoHeader, 7, 2))
                                info["video"]["resolution_x"] = PictureSizeEnc["x"] & 255 << 3
                                info["video"]["resolution_y"] = PictureSizeEnc["y"] & 255 << 3
                            # end if
                            pass
                        # end if
                        if (not php_empty(lambda : info["video"]["resolution_x"])) and (not php_empty(lambda : info["video"]["resolution_y"])):
                            info["video"]["pixel_aspect_ratio"] = info["video"]["resolution_x"] / info["video"]["resolution_y"]
                        # end if
                    # end if
                    break
                # end if
                if case(GETID3_FLV_TAG_META):
                    if (not found_meta):
                        found_meta = True
                        self.fseek(-1, SEEK_CUR)
                        datachunk = self.fread(DataLength)
                        AMFstream = php_new_class("AMFStream", lambda : AMFStream(datachunk))
                        reader = php_new_class("AMFReader", lambda : AMFReader(AMFstream))
                        eventName = reader.readdata()
                        info["flv"]["meta"][eventName] = reader.readdata()
                        reader = None
                        copykeys = Array({"framerate": "frame_rate", "width": "resolution_x", "height": "resolution_y", "audiodatarate": "bitrate", "videodatarate": "bitrate"})
                        for sourcekey,destkey in copykeys:
                            if (php_isset(lambda : info["flv"]["meta"]["onMetaData"][sourcekey])):
                                for case in Switch(sourcekey):
                                    if case("width"):
                                        pass
                                    # end if
                                    if case("height"):
                                        info["video"][destkey] = php_intval(round(info["flv"]["meta"]["onMetaData"][sourcekey]))
                                        break
                                    # end if
                                    if case("audiodatarate"):
                                        info["audio"][destkey] = getid3_lib.castasint(round(info["flv"]["meta"]["onMetaData"][sourcekey] * 1000))
                                        break
                                    # end if
                                    if case("videodatarate"):
                                        pass
                                    # end if
                                    if case("frame_rate"):
                                        pass
                                    # end if
                                    if case():
                                        info["video"][destkey] = info["flv"]["meta"]["onMetaData"][sourcekey]
                                        break
                                    # end if
                                # end for
                            # end if
                        # end for
                        if (not php_empty(lambda : info["flv"]["meta"]["onMetaData"]["duration"])):
                            found_valid_meta_playtime = True
                        # end if
                    # end if
                    break
                # end if
                if case():
                    break
                # end if
            # end for
            self.fseek(NextOffset)
        # end while
        info["playtime_seconds"] = Duration / 1000
        if info["playtime_seconds"] > 0:
            info["bitrate"] = info["avdataend"] - info["avdataoffset"] * 8 / info["playtime_seconds"]
        # end if
        if info["flv"]["header"]["hasAudio"]:
            info["audio"]["codec"] = self.audioformatlookup(info["flv"]["audio"]["audioFormat"])
            info["audio"]["sample_rate"] = self.audioratelookup(info["flv"]["audio"]["audioRate"])
            info["audio"]["bits_per_sample"] = self.audiobitdepthlookup(info["flv"]["audio"]["audioSampleSize"])
            info["audio"]["channels"] = info["flv"]["audio"]["audioType"] + 1
            #// 0=mono,1=stereo
            info["audio"]["lossless"] = False if info["flv"]["audio"]["audioFormat"] else True
            #// 0=uncompressed
            info["audio"]["dataformat"] = "flv"
        # end if
        if (not php_empty(lambda : info["flv"]["header"]["hasVideo"])):
            info["video"]["codec"] = self.videocodeclookup(info["flv"]["video"]["videoCodec"])
            info["video"]["dataformat"] = "flv"
            info["video"]["lossless"] = False
        # end if
        #// Set information from meta
        if (not php_empty(lambda : info["flv"]["meta"]["onMetaData"]["duration"])):
            info["playtime_seconds"] = info["flv"]["meta"]["onMetaData"]["duration"]
            info["bitrate"] = info["avdataend"] - info["avdataoffset"] * 8 / info["playtime_seconds"]
        # end if
        if (php_isset(lambda : info["flv"]["meta"]["onMetaData"]["audiocodecid"])):
            info["audio"]["codec"] = self.audioformatlookup(info["flv"]["meta"]["onMetaData"]["audiocodecid"])
        # end if
        if (php_isset(lambda : info["flv"]["meta"]["onMetaData"]["videocodecid"])):
            info["video"]["codec"] = self.videocodeclookup(info["flv"]["meta"]["onMetaData"]["videocodecid"])
        # end if
        return True
    # end def analyze
    #// 
    #// @param int $id
    #// 
    #// @return string|false
    #//
    @classmethod
    def audioformatlookup(self, id=None):
        
        audioformatlookup.lookup = Array({0: "Linear PCM, platform endian", 1: "ADPCM", 2: "mp3", 3: "Linear PCM, little endian", 4: "Nellymoser 16kHz mono", 5: "Nellymoser 8kHz mono", 6: "Nellymoser", 7: "G.711A-law logarithmic PCM", 8: "G.711 mu-law logarithmic PCM", 9: "reserved", 10: "AAC", 11: "Speex", 12: False, 13: False, 14: "mp3 8kHz", 15: "Device-specific sound"})
        return audioformatlookup.lookup[id] if (php_isset(lambda : audioformatlookup.lookup[id])) else False
    # end def audioformatlookup
    #// 
    #// @param int $id
    #// 
    #// @return int|false
    #//
    @classmethod
    def audioratelookup(self, id=None):
        
        audioratelookup.lookup = Array({0: 5500, 1: 11025, 2: 22050, 3: 44100})
        return audioratelookup.lookup[id] if (php_isset(lambda : audioratelookup.lookup[id])) else False
    # end def audioratelookup
    #// 
    #// @param int $id
    #// 
    #// @return int|false
    #//
    @classmethod
    def audiobitdepthlookup(self, id=None):
        
        audiobitdepthlookup.lookup = Array({0: 8, 1: 16})
        return audiobitdepthlookup.lookup[id] if (php_isset(lambda : audiobitdepthlookup.lookup[id])) else False
    # end def audiobitdepthlookup
    #// 
    #// @param int $id
    #// 
    #// @return string|false
    #//
    @classmethod
    def videocodeclookup(self, id=None):
        
        videocodeclookup.lookup = Array({GETID3_FLV_VIDEO_H263: "Sorenson H.263", GETID3_FLV_VIDEO_SCREEN: "Screen video", GETID3_FLV_VIDEO_VP6FLV: "On2 VP6", GETID3_FLV_VIDEO_VP6FLV_ALPHA: "On2 VP6 with alpha channel", GETID3_FLV_VIDEO_SCREENV2: "Screen video v2", GETID3_FLV_VIDEO_H264: "Sorenson H.264"})
        return videocodeclookup.lookup[id] if (php_isset(lambda : videocodeclookup.lookup[id])) else False
    # end def videocodeclookup
# end class getid3_flv
class AMFStream():
    bytes = Array()
    pos = Array()
    #// 
    #// @param string $bytes
    #//
    def __init__(self, bytes=None):
        
        self.bytes = bytes
        self.pos = 0
    # end def __init__
    #// 
    #// @return int
    #//
    def readbyte(self):
        
        #// 8-bit
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
        
        length = self.readint()
        return self.read(length)
    # end def readutf
    #// 
    #// @return string
    #//
    def readlongutf(self):
        
        length = self.readlong()
        return self.read(length)
    # end def readlongutf
    #// 
    #// @param int $length
    #// 
    #// @return string
    #//
    def read(self, length=None):
        
        val = php_substr(self.bytes, self.pos, length)
        self.pos += length
        return val
    # end def read
    #// 
    #// @return int
    #//
    def peekbyte(self):
        
        pos = self.pos
        val = self.readbyte()
        self.pos = pos
        return val
    # end def peekbyte
    #// 
    #// @return int
    #//
    def peekint(self):
        
        pos = self.pos
        val = self.readint()
        self.pos = pos
        return val
    # end def peekint
    #// 
    #// @return int
    #//
    def peeklong(self):
        
        pos = self.pos
        val = self.readlong()
        self.pos = pos
        return val
    # end def peeklong
    #// 
    #// @return float|false
    #//
    def peekdouble(self):
        
        pos = self.pos
        val = self.readdouble()
        self.pos = pos
        return val
    # end def peekdouble
    #// 
    #// @return string
    #//
    def peekutf(self):
        
        pos = self.pos
        val = self.readutf()
        self.pos = pos
        return val
    # end def peekutf
    #// 
    #// @return string
    #//
    def peeklongutf(self):
        
        pos = self.pos
        val = self.readlongutf()
        self.pos = pos
        return val
    # end def peeklongutf
# end class AMFStream
class AMFReader():
    stream = Array()
    #// 
    #// @param AMFStream $stream
    #//
    def __init__(self, stream=None):
        
        self.stream = stream
    # end def __init__
    #// 
    #// @return mixed
    #//
    def readdata(self):
        
        value = None
        type = self.stream.readbyte()
        for case in Switch(type):
            if case(0):
                value = self.readdouble()
                break
            # end if
            if case(1):
                value = self.readboolean()
                break
            # end if
            if case(2):
                value = self.readstring()
                break
            # end if
            if case(3):
                value = self.readobject()
                break
            # end if
            if case(6):
                return None
                break
            # end if
            if case(8):
                value = self.readmixedarray()
                break
            # end if
            if case(10):
                value = self.readarray()
                break
            # end if
            if case(11):
                value = self.readdate()
                break
            # end if
            if case(13):
                value = self.readlongstring()
                break
            # end if
            if case(15):
                value = self.readxml()
                break
            # end if
            if case(16):
                value = self.readtypedobject()
                break
            # end if
            if case():
                value = "(unknown or unsupported data type)"
                break
            # end if
        # end for
        return value
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
        data = Array()
        key = None
        while True:
            key = self.stream.readutf()
            if not (key):
                break
            # end if
            data[key] = self.readdata()
        # end while
        #// Mixed array record ends with empty string (0x00 0x00) and 0x09
        if key == "" and self.stream.peekbyte() == 9:
            #// Consume byte
            self.stream.readbyte()
        # end if
        return data
    # end def readobject
    #// 
    #// @return array
    #//
    def readmixedarray(self):
        
        #// Get highest numerical index - ignored
        highestIndex = self.stream.readlong()
        data = Array()
        key = None
        while True:
            key = self.stream.readutf()
            if not (key):
                break
            # end if
            if php_is_numeric(key):
                key = php_int(key)
            # end if
            data[key] = self.readdata()
        # end while
        #// Mixed array record ends with empty string (0x00 0x00) and 0x09
        if key == "" and self.stream.peekbyte() == 9:
            #// Consume byte
            self.stream.readbyte()
        # end if
        return data
    # end def readmixedarray
    #// 
    #// @return array
    #//
    def readarray(self):
        
        length = self.stream.readlong()
        data = Array()
        i = 0
        while i < length:
            
            data[-1] = self.readdata()
            i += 1
        # end while
        return data
    # end def readarray
    #// 
    #// @return float|false
    #//
    def readdate(self):
        
        timestamp = self.stream.readdouble()
        timezone = self.stream.readint()
        return timestamp
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
        
        className = self.stream.readutf()
        return self.readobject()
    # end def readtypedobject
# end class AMFReader
class AVCSequenceParameterSetReader():
    sps = Array()
    start = 0
    currentBytes = 0
    currentBits = 0
    width = Array()
    height = Array()
    #// 
    #// @param string $sps
    #//
    def __init__(self, sps=None):
        
        self.sps = sps
    # end def __init__
    def readdata(self):
        
        self.skipbits(8)
        self.skipbits(8)
        profile = self.getbits(8)
        #// read profile
        if profile > 0:
            self.skipbits(8)
            level_idc = self.getbits(8)
            #// level_idc
            self.expgolombue()
            #// seq_parameter_set_id // sps
            self.expgolombue()
            #// log2_max_frame_num_minus4
            picOrderType = self.expgolombue()
            #// pic_order_cnt_type
            if picOrderType == 0:
                self.expgolombue()
                pass
            elif picOrderType == 1:
                self.skipbits(1)
                #// delta_pic_order_always_zero_flag
                self.expgolombse()
                #// offset_for_non_ref_pic
                self.expgolombse()
                #// offset_for_top_to_bottom_field
                num_ref_frames_in_pic_order_cnt_cycle = self.expgolombue()
                #// num_ref_frames_in_pic_order_cnt_cycle
                i = 0
                while i < num_ref_frames_in_pic_order_cnt_cycle:
                    
                    self.expgolombse()
                    pass
                    i += 1
                # end while
            # end if
            self.expgolombue()
            #// num_ref_frames
            self.skipbits(1)
            #// gaps_in_frame_num_value_allowed_flag
            pic_width_in_mbs_minus1 = self.expgolombue()
            #// pic_width_in_mbs_minus1
            pic_height_in_map_units_minus1 = self.expgolombue()
            #// pic_height_in_map_units_minus1
            frame_mbs_only_flag = self.getbits(1)
            #// frame_mbs_only_flag
            if frame_mbs_only_flag == 0:
                self.skipbits(1)
                pass
            # end if
            self.skipbits(1)
            #// direct_8x8_inference_flag
            frame_cropping_flag = self.getbits(1)
            #// frame_cropping_flag
            frame_crop_left_offset = 0
            frame_crop_right_offset = 0
            frame_crop_top_offset = 0
            frame_crop_bottom_offset = 0
            if frame_cropping_flag:
                frame_crop_left_offset = self.expgolombue()
                #// frame_crop_left_offset
                frame_crop_right_offset = self.expgolombue()
                #// frame_crop_right_offset
                frame_crop_top_offset = self.expgolombue()
                #// frame_crop_top_offset
                frame_crop_bottom_offset = self.expgolombue()
                pass
            # end if
            self.skipbits(1)
            #// vui_parameters_present_flag
            #// etc
            self.width = pic_width_in_mbs_minus1 + 1 * 16 - frame_crop_left_offset * 2 - frame_crop_right_offset * 2
            self.height = 2 - frame_mbs_only_flag * pic_height_in_map_units_minus1 + 1 * 16 - frame_crop_top_offset * 2 - frame_crop_bottom_offset * 2
        # end if
    # end def readdata
    #// 
    #// @param int $bits
    #//
    def skipbits(self, bits=None):
        
        newBits = self.currentBits + bits
        self.currentBytes += php_int(floor(newBits / 8))
        self.currentBits = newBits % 8
    # end def skipbits
    #// 
    #// @return int
    #//
    def getbit(self):
        
        result = getid3_lib.bigendian2int(php_substr(self.sps, self.currentBytes, 1)) >> 7 - self.currentBits & 1
        self.skipbits(1)
        return result
    # end def getbit
    #// 
    #// @param int $bits
    #// 
    #// @return int
    #//
    def getbits(self, bits=None):
        
        result = 0
        i = 0
        while i < bits:
            
            result = result << 1 + self.getbit()
            i += 1
        # end while
        return result
    # end def getbits
    #// 
    #// @return int
    #//
    def expgolombue(self):
        
        significantBits = 0
        bit = self.getbit()
        while True:
            
            if not (bit == 0):
                break
            # end if
            significantBits += 1
            bit = self.getbit()
            if significantBits > 31:
                #// something is broken, this is an emergency escape to prevent infinite loops
                return 0
            # end if
        # end while
        return 1 << significantBits + self.getbits(significantBits) - 1
    # end def expgolombue
    #// 
    #// @return int
    #//
    def expgolombse(self):
        
        result = self.expgolombue()
        if result & 1 == 0:
            return -result >> 1
        else:
            return result + 1 >> 1
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
