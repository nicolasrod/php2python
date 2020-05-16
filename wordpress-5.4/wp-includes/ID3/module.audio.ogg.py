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
#// module.audio.ogg.php
#// module for analyzing Ogg Vorbis, OggFLAC and Speex files
#// dependencies: module.audio.flac.php
#// 
#//
getid3_lib.includedependency(GETID3_INCLUDEPATH + "module.audio.flac.php", __FILE__, True)
class getid3_ogg(getid3_handler):
    #// 
    #// @link http://xiph.org/vorbis/doc/Vorbis_I_spec.html
    #// 
    #// @return bool
    #//
    def analyze(self):
        
        info = self.getid3.info
        info["fileformat"] = "ogg"
        #// Warn about illegal tags - only vorbiscomments are allowed
        if (php_isset(lambda : info["id3v2"])):
            self.warning("Illegal ID3v2 tag present.")
        # end if
        if (php_isset(lambda : info["id3v1"])):
            self.warning("Illegal ID3v1 tag present.")
        # end if
        if (php_isset(lambda : info["ape"])):
            self.warning("Illegal APE tag present.")
        # end if
        #// Page 1 - Stream Header
        self.fseek(info["avdataoffset"])
        oggpageinfo = self.parseoggpageheader()
        info["ogg"]["pageheader"][oggpageinfo["page_seqno"]] = oggpageinfo
        if self.ftell() >= self.getid3.fread_buffer_size():
            self.error("Could not find start of Ogg page in the first " + self.getid3.fread_buffer_size() + " bytes (this might not be an Ogg-Vorbis file?)")
            info["fileformat"] = None
            info["ogg"] = None
            return False
        # end if
        filedata = self.fread(oggpageinfo["page_length"])
        filedataoffset = 0
        if php_substr(filedata, 0, 4) == "fLaC":
            info["audio"]["dataformat"] = "flac"
            info["audio"]["bitrate_mode"] = "vbr"
            info["audio"]["lossless"] = True
        elif php_substr(filedata, 1, 6) == "vorbis":
            self.parsevorbispageheader(filedata, filedataoffset, oggpageinfo)
        elif php_substr(filedata, 0, 8) == "OpusHead":
            if self.parseopuspageheader(filedata, filedataoffset, oggpageinfo) == False:
                return False
            # end if
        elif php_substr(filedata, 0, 8) == "Speex   ":
            #// http://www.speex.org/manual/node10.html
            info["audio"]["dataformat"] = "speex"
            info["mime_type"] = "audio/speex"
            info["audio"]["bitrate_mode"] = "abr"
            info["audio"]["lossless"] = False
            info["ogg"]["pageheader"][oggpageinfo["page_seqno"]]["speex_string"] = php_substr(filedata, filedataoffset, 8)
            #// hard-coded to 'Speex   '
            filedataoffset += 8
            info["ogg"]["pageheader"][oggpageinfo["page_seqno"]]["speex_version"] = php_substr(filedata, filedataoffset, 20)
            filedataoffset += 20
            info["ogg"]["pageheader"][oggpageinfo["page_seqno"]]["speex_version_id"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 4))
            filedataoffset += 4
            info["ogg"]["pageheader"][oggpageinfo["page_seqno"]]["header_size"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 4))
            filedataoffset += 4
            info["ogg"]["pageheader"][oggpageinfo["page_seqno"]]["rate"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 4))
            filedataoffset += 4
            info["ogg"]["pageheader"][oggpageinfo["page_seqno"]]["mode"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 4))
            filedataoffset += 4
            info["ogg"]["pageheader"][oggpageinfo["page_seqno"]]["mode_bitstream_version"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 4))
            filedataoffset += 4
            info["ogg"]["pageheader"][oggpageinfo["page_seqno"]]["nb_channels"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 4))
            filedataoffset += 4
            info["ogg"]["pageheader"][oggpageinfo["page_seqno"]]["bitrate"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 4))
            filedataoffset += 4
            info["ogg"]["pageheader"][oggpageinfo["page_seqno"]]["framesize"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 4))
            filedataoffset += 4
            info["ogg"]["pageheader"][oggpageinfo["page_seqno"]]["vbr"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 4))
            filedataoffset += 4
            info["ogg"]["pageheader"][oggpageinfo["page_seqno"]]["frames_per_packet"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 4))
            filedataoffset += 4
            info["ogg"]["pageheader"][oggpageinfo["page_seqno"]]["extra_headers"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 4))
            filedataoffset += 4
            info["ogg"]["pageheader"][oggpageinfo["page_seqno"]]["reserved1"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 4))
            filedataoffset += 4
            info["ogg"]["pageheader"][oggpageinfo["page_seqno"]]["reserved2"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 4))
            filedataoffset += 4
            info["speex"]["speex_version"] = php_trim(info["ogg"]["pageheader"][oggpageinfo["page_seqno"]]["speex_version"])
            info["speex"]["sample_rate"] = info["ogg"]["pageheader"][oggpageinfo["page_seqno"]]["rate"]
            info["speex"]["channels"] = info["ogg"]["pageheader"][oggpageinfo["page_seqno"]]["nb_channels"]
            info["speex"]["vbr"] = php_bool(info["ogg"]["pageheader"][oggpageinfo["page_seqno"]]["vbr"])
            info["speex"]["band_type"] = self.speexbandmodelookup(info["ogg"]["pageheader"][oggpageinfo["page_seqno"]]["mode"])
            info["audio"]["sample_rate"] = info["speex"]["sample_rate"]
            info["audio"]["channels"] = info["speex"]["channels"]
            if info["speex"]["vbr"]:
                info["audio"]["bitrate_mode"] = "vbr"
            # end if
        elif php_substr(filedata, 0, 7) == "" + "theora":
            #// http://www.theora.org/doc/Theora.pdf (section 6.2)
            info["ogg"]["pageheader"]["theora"]["theora_magic"] = php_substr(filedata, filedataoffset, 7)
            #// hard-coded to "\x80.'theora'
            filedataoffset += 7
            info["ogg"]["pageheader"]["theora"]["version_major"] = getid3_lib.bigendian2int(php_substr(filedata, filedataoffset, 1))
            filedataoffset += 1
            info["ogg"]["pageheader"]["theora"]["version_minor"] = getid3_lib.bigendian2int(php_substr(filedata, filedataoffset, 1))
            filedataoffset += 1
            info["ogg"]["pageheader"]["theora"]["version_revision"] = getid3_lib.bigendian2int(php_substr(filedata, filedataoffset, 1))
            filedataoffset += 1
            info["ogg"]["pageheader"]["theora"]["frame_width_macroblocks"] = getid3_lib.bigendian2int(php_substr(filedata, filedataoffset, 2))
            filedataoffset += 2
            info["ogg"]["pageheader"]["theora"]["frame_height_macroblocks"] = getid3_lib.bigendian2int(php_substr(filedata, filedataoffset, 2))
            filedataoffset += 2
            info["ogg"]["pageheader"]["theora"]["resolution_x"] = getid3_lib.bigendian2int(php_substr(filedata, filedataoffset, 3))
            filedataoffset += 3
            info["ogg"]["pageheader"]["theora"]["resolution_y"] = getid3_lib.bigendian2int(php_substr(filedata, filedataoffset, 3))
            filedataoffset += 3
            info["ogg"]["pageheader"]["theora"]["picture_offset_x"] = getid3_lib.bigendian2int(php_substr(filedata, filedataoffset, 1))
            filedataoffset += 1
            info["ogg"]["pageheader"]["theora"]["picture_offset_y"] = getid3_lib.bigendian2int(php_substr(filedata, filedataoffset, 1))
            filedataoffset += 1
            info["ogg"]["pageheader"]["theora"]["frame_rate_numerator"] = getid3_lib.bigendian2int(php_substr(filedata, filedataoffset, 4))
            filedataoffset += 4
            info["ogg"]["pageheader"]["theora"]["frame_rate_denominator"] = getid3_lib.bigendian2int(php_substr(filedata, filedataoffset, 4))
            filedataoffset += 4
            info["ogg"]["pageheader"]["theora"]["pixel_aspect_numerator"] = getid3_lib.bigendian2int(php_substr(filedata, filedataoffset, 3))
            filedataoffset += 3
            info["ogg"]["pageheader"]["theora"]["pixel_aspect_denominator"] = getid3_lib.bigendian2int(php_substr(filedata, filedataoffset, 3))
            filedataoffset += 3
            info["ogg"]["pageheader"]["theora"]["color_space_id"] = getid3_lib.bigendian2int(php_substr(filedata, filedataoffset, 1))
            filedataoffset += 1
            info["ogg"]["pageheader"]["theora"]["nominal_bitrate"] = getid3_lib.bigendian2int(php_substr(filedata, filedataoffset, 3))
            filedataoffset += 3
            info["ogg"]["pageheader"]["theora"]["flags"] = getid3_lib.bigendian2int(php_substr(filedata, filedataoffset, 2))
            filedataoffset += 2
            info["ogg"]["pageheader"]["theora"]["quality"] = info["ogg"]["pageheader"]["theora"]["flags"] & 64512 >> 10
            info["ogg"]["pageheader"]["theora"]["kfg_shift"] = info["ogg"]["pageheader"]["theora"]["flags"] & 992 >> 5
            info["ogg"]["pageheader"]["theora"]["pixel_format_id"] = info["ogg"]["pageheader"]["theora"]["flags"] & 24 >> 3
            info["ogg"]["pageheader"]["theora"]["reserved"] = info["ogg"]["pageheader"]["theora"]["flags"] & 7 >> 0
            #// should be 0
            info["ogg"]["pageheader"]["theora"]["color_space"] = self.theoracolorspace(info["ogg"]["pageheader"]["theora"]["color_space_id"])
            info["ogg"]["pageheader"]["theora"]["pixel_format"] = self.theorapixelformat(info["ogg"]["pageheader"]["theora"]["pixel_format_id"])
            info["video"]["dataformat"] = "theora"
            info["mime_type"] = "video/ogg"
            #// $info['audio']['bitrate_mode'] = 'abr';
            #// $info['audio']['lossless']     = false;
            info["video"]["resolution_x"] = info["ogg"]["pageheader"]["theora"]["resolution_x"]
            info["video"]["resolution_y"] = info["ogg"]["pageheader"]["theora"]["resolution_y"]
            if info["ogg"]["pageheader"]["theora"]["frame_rate_denominator"] > 0:
                info["video"]["frame_rate"] = php_float(info["ogg"]["pageheader"]["theora"]["frame_rate_numerator"]) / info["ogg"]["pageheader"]["theora"]["frame_rate_denominator"]
            # end if
            if info["ogg"]["pageheader"]["theora"]["pixel_aspect_denominator"] > 0:
                info["video"]["pixel_aspect_ratio"] = php_float(info["ogg"]["pageheader"]["theora"]["pixel_aspect_numerator"]) / info["ogg"]["pageheader"]["theora"]["pixel_aspect_denominator"]
            # end if
            self.warning("Ogg Theora (v3) not fully supported in this version of getID3 [" + self.getid3.version() + "] -- bitrate, playtime and all audio data are currently unavailable")
        elif php_substr(filedata, 0, 8) == "fishead ":
            #// Ogg Skeleton version 3.0 Format Specification
            #// http://xiph.org/ogg/doc/skeleton.html
            filedataoffset += 8
            info["ogg"]["skeleton"]["fishead"]["raw"]["version_major"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 2))
            filedataoffset += 2
            info["ogg"]["skeleton"]["fishead"]["raw"]["version_minor"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 2))
            filedataoffset += 2
            info["ogg"]["skeleton"]["fishead"]["raw"]["presentationtime_numerator"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 8))
            filedataoffset += 8
            info["ogg"]["skeleton"]["fishead"]["raw"]["presentationtime_denominator"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 8))
            filedataoffset += 8
            info["ogg"]["skeleton"]["fishead"]["raw"]["basetime_numerator"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 8))
            filedataoffset += 8
            info["ogg"]["skeleton"]["fishead"]["raw"]["basetime_denominator"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 8))
            filedataoffset += 8
            info["ogg"]["skeleton"]["fishead"]["raw"]["utc"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 20))
            filedataoffset += 20
            info["ogg"]["skeleton"]["fishead"]["version"] = info["ogg"]["skeleton"]["fishead"]["raw"]["version_major"] + "." + info["ogg"]["skeleton"]["fishead"]["raw"]["version_minor"]
            info["ogg"]["skeleton"]["fishead"]["presentationtime"] = info["ogg"]["skeleton"]["fishead"]["raw"]["presentationtime_numerator"] / info["ogg"]["skeleton"]["fishead"]["raw"]["presentationtime_denominator"]
            info["ogg"]["skeleton"]["fishead"]["basetime"] = info["ogg"]["skeleton"]["fishead"]["raw"]["basetime_numerator"] / info["ogg"]["skeleton"]["fishead"]["raw"]["basetime_denominator"]
            info["ogg"]["skeleton"]["fishead"]["utc"] = info["ogg"]["skeleton"]["fishead"]["raw"]["utc"]
            counter = 0
            while True:
                oggpageinfo = self.parseoggpageheader()
                info["ogg"]["pageheader"][oggpageinfo["page_seqno"] + "." + counter] = oggpageinfo
                counter += 1
                filedata = self.fread(oggpageinfo["page_length"])
                self.fseek(oggpageinfo["page_end_offset"])
                if php_substr(filedata, 0, 8) == "fisbone ":
                    filedataoffset = 8
                    info["ogg"]["skeleton"]["fisbone"]["raw"]["message_header_offset"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 4))
                    filedataoffset += 4
                    info["ogg"]["skeleton"]["fisbone"]["raw"]["serial_number"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 4))
                    filedataoffset += 4
                    info["ogg"]["skeleton"]["fisbone"]["raw"]["number_header_packets"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 4))
                    filedataoffset += 4
                    info["ogg"]["skeleton"]["fisbone"]["raw"]["granulerate_numerator"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 8))
                    filedataoffset += 8
                    info["ogg"]["skeleton"]["fisbone"]["raw"]["granulerate_denominator"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 8))
                    filedataoffset += 8
                    info["ogg"]["skeleton"]["fisbone"]["raw"]["basegranule"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 8))
                    filedataoffset += 8
                    info["ogg"]["skeleton"]["fisbone"]["raw"]["preroll"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 4))
                    filedataoffset += 4
                    info["ogg"]["skeleton"]["fisbone"]["raw"]["granuleshift"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 1))
                    filedataoffset += 1
                    info["ogg"]["skeleton"]["fisbone"]["raw"]["padding"] = php_substr(filedata, filedataoffset, 3)
                    filedataoffset += 3
                elif php_substr(filedata, 1, 6) == "theora":
                    info["video"]["dataformat"] = "theora1"
                    self.error("Ogg Theora (v1) not correctly handled in this version of getID3 [" + self.getid3.version() + "]")
                    pass
                elif php_substr(filedata, 1, 6) == "vorbis":
                    self.parsevorbispageheader(filedata, filedataoffset, oggpageinfo)
                else:
                    self.error("unexpected")
                    pass
                # end if
                pass
                
                if oggpageinfo["page_seqno"] == 0 and php_substr(filedata, 0, 8) != "fisbone ":
                    break
                # end if
            # end while
            self.fseek(oggpageinfo["page_start_offset"])
            self.error("Ogg Skeleton not correctly handled in this version of getID3 [" + self.getid3.version() + "]")
            pass
        elif php_substr(filedata, 0, 5) == "" + "FLAC":
            #// https://xiph.org/flac/ogg_mapping.html
            info["audio"]["dataformat"] = "flac"
            info["audio"]["bitrate_mode"] = "vbr"
            info["audio"]["lossless"] = True
            info["ogg"]["flac"]["header"]["version_major"] = php_ord(php_substr(filedata, 5, 1))
            info["ogg"]["flac"]["header"]["version_minor"] = php_ord(php_substr(filedata, 6, 1))
            info["ogg"]["flac"]["header"]["header_packets"] = getid3_lib.bigendian2int(php_substr(filedata, 7, 2)) + 1
            #// "A two-byte, big-endian binary number signifying the number of header (non-audio) packets, not including this one. This number may be zero (0x0000) to signify 'unknown' but be aware that some decoders may not be able to handle such streams."
            info["ogg"]["flac"]["header"]["magic"] = php_substr(filedata, 9, 4)
            if info["ogg"]["flac"]["header"]["magic"] != "fLaC":
                self.error("Ogg-FLAC expecting \"fLaC\", found \"" + info["ogg"]["flac"]["header"]["magic"] + "\" (" + php_trim(getid3_lib.printhexbytes(info["ogg"]["flac"]["header"]["magic"])) + ")")
                return False
            # end if
            info["ogg"]["flac"]["header"]["STREAMINFO_bytes"] = getid3_lib.bigendian2int(php_substr(filedata, 13, 4))
            info["flac"]["STREAMINFO"] = getid3_flac.parsestreaminfodata(php_substr(filedata, 17, 34))
            if (not php_empty(lambda : info["flac"]["STREAMINFO"]["sample_rate"])):
                info["audio"]["bitrate_mode"] = "vbr"
                info["audio"]["sample_rate"] = info["flac"]["STREAMINFO"]["sample_rate"]
                info["audio"]["channels"] = info["flac"]["STREAMINFO"]["channels"]
                info["audio"]["bits_per_sample"] = info["flac"]["STREAMINFO"]["bits_per_sample"]
                info["playtime_seconds"] = info["flac"]["STREAMINFO"]["samples_stream"] / info["flac"]["STREAMINFO"]["sample_rate"]
            # end if
        else:
            self.error("Expecting one of \"vorbis\", \"Speex\", \"OpusHead\", \"vorbis\", \"fishhead\", \"theora\", \"fLaC\" identifier strings, found \"" + php_substr(filedata, 0, 8) + "\"")
            info["ogg"] = None
            info["mime_type"] = None
            return False
        # end if
        #// Page 2 - Comment Header
        oggpageinfo = self.parseoggpageheader()
        info["ogg"]["pageheader"][oggpageinfo["page_seqno"]] = oggpageinfo
        for case in Switch(info["audio"]["dataformat"]):
            if case("vorbis"):
                filedata = self.fread(info["ogg"]["pageheader"][oggpageinfo["page_seqno"]]["page_length"])
                info["ogg"]["pageheader"][oggpageinfo["page_seqno"]]["packet_type"] = getid3_lib.littleendian2int(php_substr(filedata, 0, 1))
                info["ogg"]["pageheader"][oggpageinfo["page_seqno"]]["stream_type"] = php_substr(filedata, 1, 6)
                #// hard-coded to 'vorbis'
                self.parsevorbiscomments()
                break
            # end if
            if case("flac"):
                flac = php_new_class("getid3_flac", lambda : getid3_flac(self.getid3))
                if (not flac.parsemetadata()):
                    self.error("Failed to parse FLAC headers")
                    return False
                # end if
                flac = None
                break
            # end if
            if case("speex"):
                self.fseek(info["ogg"]["pageheader"][oggpageinfo["page_seqno"]]["page_length"], SEEK_CUR)
                self.parsevorbiscomments()
                break
            # end if
            if case("opus"):
                filedata = self.fread(info["ogg"]["pageheader"][oggpageinfo["page_seqno"]]["page_length"])
                info["ogg"]["pageheader"][oggpageinfo["page_seqno"]]["stream_type"] = php_substr(filedata, 0, 8)
                #// hard-coded to 'OpusTags'
                if php_substr(filedata, 0, 8) != "OpusTags":
                    self.error("Expected \"OpusTags\" as header but got \"" + php_substr(filedata, 0, 8) + "\"")
                    return False
                # end if
                self.parsevorbiscomments()
                break
            # end if
        # end for
        #// Last Page - Number of Samples
        if (not getid3_lib.intvaluesupported(info["avdataend"])):
            self.warning("Unable to parse Ogg end chunk file (PHP does not support file operations beyond " + round(PHP_INT_MAX / 1073741824) + "GB)")
        else:
            self.fseek(php_max(info["avdataend"] - self.getid3.fread_buffer_size(), 0))
            LastChunkOfOgg = php_strrev(self.fread(self.getid3.fread_buffer_size()))
            LastOggSpostion = php_strpos(LastChunkOfOgg, "SggO")
            if LastOggSpostion:
                self.fseek(info["avdataend"] - LastOggSpostion + php_strlen("SggO"))
                info["avdataend"] = self.ftell()
                info["ogg"]["pageheader"]["eos"] = self.parseoggpageheader()
                info["ogg"]["samples"] = info["ogg"]["pageheader"]["eos"]["pcm_abs_position"]
                if info["ogg"]["samples"] == 0:
                    self.error("Corrupt Ogg file: eos.number of samples == zero")
                    return False
                # end if
                if (not php_empty(lambda : info["audio"]["sample_rate"])):
                    info["ogg"]["bitrate_average"] = info["avdataend"] - info["avdataoffset"] * 8 / info["ogg"]["samples"] / info["audio"]["sample_rate"]
                # end if
            # end if
        # end if
        if (not php_empty(lambda : info["ogg"]["bitrate_average"])):
            info["audio"]["bitrate"] = info["ogg"]["bitrate_average"]
        elif (not php_empty(lambda : info["ogg"]["bitrate_nominal"])):
            info["audio"]["bitrate"] = info["ogg"]["bitrate_nominal"]
        elif (not php_empty(lambda : info["ogg"]["bitrate_min"])) and (not php_empty(lambda : info["ogg"]["bitrate_max"])):
            info["audio"]["bitrate"] = info["ogg"]["bitrate_min"] + info["ogg"]["bitrate_max"] / 2
        # end if
        if (php_isset(lambda : info["audio"]["bitrate"])) and (not (php_isset(lambda : info["playtime_seconds"]))):
            if info["audio"]["bitrate"] == 0:
                self.error("Corrupt Ogg file: bitrate_audio == zero")
                return False
            # end if
            info["playtime_seconds"] = php_float(info["avdataend"] - info["avdataoffset"] * 8 / info["audio"]["bitrate"])
        # end if
        if (php_isset(lambda : info["ogg"]["vendor"])):
            info["audio"]["encoder"] = php_preg_replace("/^Encoded with /", "", info["ogg"]["vendor"])
            #// Vorbis only
            if info["audio"]["dataformat"] == "vorbis":
                #// Vorbis 1.0 starts with Xiph.Org
                if php_preg_match("/^Xiph.Org/", info["audio"]["encoder"]):
                    if info["audio"]["bitrate_mode"] == "abr":
                        #// Set -b 128 on abr files
                        info["audio"]["encoder_options"] = "-b " + round(info["ogg"]["bitrate_nominal"] / 1000)
                    elif info["audio"]["bitrate_mode"] == "vbr" and info["audio"]["channels"] == 2 and info["audio"]["sample_rate"] >= 44100 and info["audio"]["sample_rate"] <= 48000:
                        #// Set -q N on vbr files
                        info["audio"]["encoder_options"] = "-q " + self.get_quality_from_nominal_bitrate(info["ogg"]["bitrate_nominal"])
                    # end if
                # end if
                if php_empty(lambda : info["audio"]["encoder_options"]) and (not php_empty(lambda : info["ogg"]["bitrate_nominal"])):
                    info["audio"]["encoder_options"] = "Nominal bitrate: " + php_intval(round(info["ogg"]["bitrate_nominal"] / 1000)) + "kbps"
                # end if
            # end if
        # end if
        return True
    # end def analyze
    counter += 1
    #// 
    #// @param string $filedata
    #// @param int    $filedataoffset
    #// @param array  $oggpageinfo
    #// 
    #// @return bool
    #//
    def parsevorbispageheader(self, filedata=None, filedataoffset=None, oggpageinfo=None):
        
        info = self.getid3.info
        info["audio"]["dataformat"] = "vorbis"
        info["audio"]["lossless"] = False
        info["ogg"]["pageheader"][oggpageinfo["page_seqno"]]["packet_type"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 1))
        filedataoffset += 1
        info["ogg"]["pageheader"][oggpageinfo["page_seqno"]]["stream_type"] = php_substr(filedata, filedataoffset, 6)
        #// hard-coded to 'vorbis'
        filedataoffset += 6
        info["ogg"]["bitstreamversion"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 4))
        filedataoffset += 4
        info["ogg"]["numberofchannels"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 1))
        filedataoffset += 1
        info["audio"]["channels"] = info["ogg"]["numberofchannels"]
        info["ogg"]["samplerate"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 4))
        filedataoffset += 4
        if info["ogg"]["samplerate"] == 0:
            self.error("Corrupt Ogg file: sample rate == zero")
            return False
        # end if
        info["audio"]["sample_rate"] = info["ogg"]["samplerate"]
        info["ogg"]["samples"] = 0
        #// filled in later
        info["ogg"]["bitrate_average"] = 0
        #// filled in later
        info["ogg"]["bitrate_max"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 4))
        filedataoffset += 4
        info["ogg"]["bitrate_nominal"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 4))
        filedataoffset += 4
        info["ogg"]["bitrate_min"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 4))
        filedataoffset += 4
        info["ogg"]["blocksize_small"] = pow(2, getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 1)) & 15)
        info["ogg"]["blocksize_large"] = pow(2, getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 1)) & 240 >> 4)
        info["ogg"]["stop_bit"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 1))
        #// must be 1, marks end of packet
        info["audio"]["bitrate_mode"] = "vbr"
        #// overridden if actually abr
        if info["ogg"]["bitrate_max"] == 4294967295:
            info["ogg"]["bitrate_max"] = None
            info["audio"]["bitrate_mode"] = "abr"
        # end if
        if info["ogg"]["bitrate_nominal"] == 4294967295:
            info["ogg"]["bitrate_nominal"] = None
        # end if
        if info["ogg"]["bitrate_min"] == 4294967295:
            info["ogg"]["bitrate_min"] = None
            info["audio"]["bitrate_mode"] = "abr"
        # end if
        return True
    # end def parsevorbispageheader
    #// 
    #// @link http://tools.ietf.org/html/draft-ietf-codec-oggopus-03
    #// 
    #// @param string $filedata
    #// @param int    $filedataoffset
    #// @param array  $oggpageinfo
    #// 
    #// @return bool
    #//
    def parseopuspageheader(self, filedata=None, filedataoffset=None, oggpageinfo=None):
        
        info = self.getid3.info
        info["audio"]["dataformat"] = "opus"
        info["mime_type"] = "audio/ogg; codecs=opus"
        #// @todo find a usable way to detect abr (vbr that is padded to be abr)
        info["audio"]["bitrate_mode"] = "vbr"
        info["audio"]["lossless"] = False
        info["ogg"]["pageheader"]["opus"]["opus_magic"] = php_substr(filedata, filedataoffset, 8)
        #// hard-coded to 'OpusHead'
        filedataoffset += 8
        info["ogg"]["pageheader"]["opus"]["version"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 1))
        filedataoffset += 1
        if info["ogg"]["pageheader"]["opus"]["version"] < 1 or info["ogg"]["pageheader"]["opus"]["version"] > 15:
            self.error("Unknown opus version number (only accepting 1-15)")
            return False
        # end if
        info["ogg"]["pageheader"]["opus"]["out_channel_count"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 1))
        filedataoffset += 1
        if info["ogg"]["pageheader"]["opus"]["out_channel_count"] == 0:
            self.error("Invalid channel count in opus header (must not be zero)")
            return False
        # end if
        info["ogg"]["pageheader"]["opus"]["pre_skip"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 2))
        filedataoffset += 2
        info["ogg"]["pageheader"]["opus"]["input_sample_rate"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 4))
        filedataoffset += 4
        #// $info['ogg']['pageheader']['opus']['output_gain'] = getid3_lib::LittleEndian2Int(substr($filedata, $filedataoffset,  2));
        #// $filedataoffset += 2;
        #// $info['ogg']['pageheader']['opus']['channel_mapping_family'] = getid3_lib::LittleEndian2Int(substr($filedata, $filedataoffset,  1));
        #// $filedataoffset += 1;
        info["opus"]["opus_version"] = info["ogg"]["pageheader"]["opus"]["version"]
        info["opus"]["sample_rate_input"] = info["ogg"]["pageheader"]["opus"]["input_sample_rate"]
        info["opus"]["out_channel_count"] = info["ogg"]["pageheader"]["opus"]["out_channel_count"]
        info["audio"]["channels"] = info["opus"]["out_channel_count"]
        info["audio"]["sample_rate_input"] = info["opus"]["sample_rate_input"]
        info["audio"]["sample_rate"] = 48000
        #// "All Opus audio is coded at 48 kHz, and should also be decoded at 48 kHz for playback (unless the target hardware does not support this sampling rate). However, this field may be used to resample the audio back to the original sampling rate, for example, when saving the output to a file." -- https://mf4.xiph.org/jenkins/view/opus/job/opusfile-unix/ws/doc/html/structOpusHead.html
        return True
    # end def parseopuspageheader
    #// 
    #// @return array|false
    #//
    def parseoggpageheader(self):
        
        #// http://xiph.org/ogg/vorbis/doc/framing.html
        oggheader["page_start_offset"] = self.ftell()
        #// where we started from in the file
        filedata = self.fread(self.getid3.fread_buffer_size())
        filedataoffset = 0
        while True:
            
            if not (php_substr(filedata, filedataoffset, 4) != "OggS"):
                break
            # end if
            if self.ftell() - oggheader["page_start_offset"] >= self.getid3.fread_buffer_size():
                #// should be found before here
                return False
                filedataoffset += 1
            # end if
            if filedataoffset + 28 > php_strlen(filedata) or php_strlen(filedata) < 28:
                filedata += self.fread(self.getid3.fread_buffer_size())
                if self.feof() or filedata == "":
                    #// get some more data, unless eof, in which case fail
                    return False
                # end if
            # end if
        # end while
        filedataoffset += php_strlen("OggS") - 1
        #// page, delimited by 'OggS'
        oggheader["stream_structver"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 1))
        filedataoffset += 1
        oggheader["flags_raw"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 1))
        filedataoffset += 1
        oggheader["flags"]["fresh"] = php_bool(oggheader["flags_raw"] & 1)
        #// fresh packet
        oggheader["flags"]["bos"] = php_bool(oggheader["flags_raw"] & 2)
        #// first page of logical bitstream (bos)
        oggheader["flags"]["eos"] = php_bool(oggheader["flags_raw"] & 4)
        #// last page of logical bitstream (eos)
        oggheader["pcm_abs_position"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 8))
        filedataoffset += 8
        oggheader["stream_serialno"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 4))
        filedataoffset += 4
        oggheader["page_seqno"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 4))
        filedataoffset += 4
        oggheader["page_checksum"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 4))
        filedataoffset += 4
        oggheader["page_segments"] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 1))
        filedataoffset += 1
        oggheader["page_length"] = 0
        i = 0
        while i < oggheader["page_segments"]:
            
            oggheader["segment_table"][i] = getid3_lib.littleendian2int(php_substr(filedata, filedataoffset, 1))
            filedataoffset += 1
            oggheader["page_length"] += oggheader["segment_table"][i]
            i += 1
        # end while
        oggheader["header_end_offset"] = oggheader["page_start_offset"] + filedataoffset
        oggheader["page_end_offset"] = oggheader["header_end_offset"] + oggheader["page_length"]
        self.fseek(oggheader["header_end_offset"])
        return oggheader
    # end def parseoggpageheader
    #// 
    #// @link http://xiph.org/vorbis/doc/Vorbis_I_spec.html#x1-810005
    #// 
    #// @return bool
    #//
    def parsevorbiscomments(self):
        
        info = self.getid3.info
        OriginalOffset = self.ftell()
        commentdata = None
        commentdataoffset = 0
        VorbisCommentPage = 1
        CommentStartOffset = 0
        for case in Switch(info["audio"]["dataformat"]):
            if case("vorbis"):
                pass
            # end if
            if case("speex"):
                pass
            # end if
            if case("opus"):
                CommentStartOffset = info["ogg"]["pageheader"][VorbisCommentPage]["page_start_offset"]
                #// Second Ogg page, after header block
                self.fseek(CommentStartOffset)
                commentdataoffset = 27 + info["ogg"]["pageheader"][VorbisCommentPage]["page_segments"]
                commentdata = self.fread(self.oggpagesegmentlength(info["ogg"]["pageheader"][VorbisCommentPage], 1) + commentdataoffset)
                if info["audio"]["dataformat"] == "vorbis":
                    commentdataoffset += php_strlen("vorbis") + 1
                else:
                    if info["audio"]["dataformat"] == "opus":
                        commentdataoffset += php_strlen("OpusTags")
                    # end if
                # end if
                break
            # end if
            if case("flac"):
                CommentStartOffset = info["flac"]["VORBIS_COMMENT"]["raw"]["offset"] + 4
                self.fseek(CommentStartOffset)
                commentdata = self.fread(info["flac"]["VORBIS_COMMENT"]["raw"]["block_length"])
                break
            # end if
            if case():
                return False
                break
            # end if
        # end for
        VendorSize = getid3_lib.littleendian2int(php_substr(commentdata, commentdataoffset, 4))
        commentdataoffset += 4
        info["ogg"]["vendor"] = php_substr(commentdata, commentdataoffset, VendorSize)
        commentdataoffset += VendorSize
        CommentsCount = getid3_lib.littleendian2int(php_substr(commentdata, commentdataoffset, 4))
        commentdataoffset += 4
        info["avdataoffset"] = CommentStartOffset + commentdataoffset
        basicfields = Array("TITLE", "ARTIST", "ALBUM", "TRACKNUMBER", "GENRE", "DATE", "DESCRIPTION", "COMMENT")
        ThisFileInfo_ogg_comments_raw = info["ogg"]["comments_raw"]
        i = 0
        while i < CommentsCount:
            
            if i >= 10000:
                #// https://github.com/owncloud/music/issues/212#issuecomment-43082336
                self.warning("Unexpectedly large number (" + CommentsCount + ") of Ogg comments - breaking after reading " + i + " comments")
                break
            # end if
            ThisFileInfo_ogg_comments_raw[i]["dataoffset"] = CommentStartOffset + commentdataoffset
            if self.ftell() < ThisFileInfo_ogg_comments_raw[i]["dataoffset"] + 4:
                oggpageinfo = self.parseoggpageheader()
                if oggpageinfo:
                    info["ogg"]["pageheader"][oggpageinfo["page_seqno"]] = oggpageinfo
                    VorbisCommentPage += 1
                    #// First, save what we haven't read yet
                    AsYetUnusedData = php_substr(commentdata, commentdataoffset)
                    #// Then take that data off the end
                    commentdata = php_substr(commentdata, 0, commentdataoffset)
                    #// Add [headerlength] bytes of dummy data for the Ogg Page Header, just to keep absolute offsets correct
                    commentdata += php_str_repeat(" ", 27 + info["ogg"]["pageheader"][oggpageinfo["page_seqno"]]["page_segments"])
                    commentdataoffset += 27 + info["ogg"]["pageheader"][oggpageinfo["page_seqno"]]["page_segments"]
                    #// Finally, stick the unused data back on the end
                    commentdata += AsYetUnusedData
                    #// $commentdata .= $this->fread($info['ogg']['pageheader'][$oggpageinfo['page_seqno']]['page_length']);
                    commentdata += self.fread(self.oggpagesegmentlength(info["ogg"]["pageheader"][VorbisCommentPage], 1))
                # end if
            # end if
            ThisFileInfo_ogg_comments_raw[i]["size"] = getid3_lib.littleendian2int(php_substr(commentdata, commentdataoffset, 4))
            #// replace avdataoffset with position just after the last vorbiscomment
            info["avdataoffset"] = ThisFileInfo_ogg_comments_raw[i]["dataoffset"] + ThisFileInfo_ogg_comments_raw[i]["size"] + 4
            commentdataoffset += 4
            while True:
                
                if not (php_strlen(commentdata) - commentdataoffset < ThisFileInfo_ogg_comments_raw[i]["size"]):
                    break
                # end if
                if ThisFileInfo_ogg_comments_raw[i]["size"] > info["avdataend"] or ThisFileInfo_ogg_comments_raw[i]["size"] < 0:
                    self.warning("Invalid Ogg comment size (comment #" + i + ", claims to be " + number_format(ThisFileInfo_ogg_comments_raw[i]["size"]) + " bytes) - aborting reading comments")
                    break
                # end if
                VorbisCommentPage += 1
                oggpageinfo = self.parseoggpageheader()
                info["ogg"]["pageheader"][oggpageinfo["page_seqno"]] = oggpageinfo
                #// First, save what we haven't read yet
                AsYetUnusedData = php_substr(commentdata, commentdataoffset)
                #// Then take that data off the end
                commentdata = php_substr(commentdata, 0, commentdataoffset)
                #// Add [headerlength] bytes of dummy data for the Ogg Page Header, just to keep absolute offsets correct
                commentdata += php_str_repeat(" ", 27 + info["ogg"]["pageheader"][oggpageinfo["page_seqno"]]["page_segments"])
                commentdataoffset += 27 + info["ogg"]["pageheader"][oggpageinfo["page_seqno"]]["page_segments"]
                #// Finally, stick the unused data back on the end
                commentdata += AsYetUnusedData
                #// $commentdata .= $this->fread($info['ogg']['pageheader'][$oggpageinfo['page_seqno']]['page_length']);
                if (not (php_isset(lambda : info["ogg"]["pageheader"][VorbisCommentPage]))):
                    self.warning("undefined Vorbis Comment page \"" + VorbisCommentPage + "\" at offset " + self.ftell())
                    break
                # end if
                readlength = self.oggpagesegmentlength(info["ogg"]["pageheader"][VorbisCommentPage], 1)
                if readlength <= 0:
                    self.warning("invalid length Vorbis Comment page \"" + VorbisCommentPage + "\" at offset " + self.ftell())
                    break
                # end if
                commentdata += self.fread(readlength)
                pass
            # end while
            ThisFileInfo_ogg_comments_raw[i]["offset"] = commentdataoffset
            commentstring = php_substr(commentdata, commentdataoffset, ThisFileInfo_ogg_comments_raw[i]["size"])
            commentdataoffset += ThisFileInfo_ogg_comments_raw[i]["size"]
            if (not commentstring):
                #// no comment?
                self.warning("Blank Ogg comment [" + i + "]")
            elif php_strstr(commentstring, "="):
                commentexploded = php_explode("=", commentstring, 2)
                ThisFileInfo_ogg_comments_raw[i]["key"] = php_strtoupper(commentexploded[0])
                ThisFileInfo_ogg_comments_raw[i]["value"] = commentexploded[1] if (php_isset(lambda : commentexploded[1])) else ""
                if ThisFileInfo_ogg_comments_raw[i]["key"] == "METADATA_BLOCK_PICTURE":
                    #// http://wiki.xiph.org/VorbisComment#METADATA_BLOCK_PICTURE
                    #// The unencoded format is that of the FLAC picture block. The fields are stored in big endian order as in FLAC, picture data is stored according to the relevant standard.
                    #// http://flac.sourceforge.net/format.html#metadata_block_picture
                    flac = php_new_class("getid3_flac", lambda : getid3_flac(self.getid3))
                    flac.setstringmode(php_base64_decode(ThisFileInfo_ogg_comments_raw[i]["value"]))
                    flac.parsepicture()
                    info["ogg"]["comments"]["picture"][-1] = flac.getid3.info["flac"]["PICTURE"][0]
                    flac = None
                elif ThisFileInfo_ogg_comments_raw[i]["key"] == "COVERART":
                    data = php_base64_decode(ThisFileInfo_ogg_comments_raw[i]["value"])
                    self.notice("Found deprecated COVERART tag, it should be replaced in honor of METADATA_BLOCK_PICTURE structure")
                    #// @todo use 'coverartmime' where available
                    imageinfo = getid3_lib.getdataimagesize(data)
                    if imageinfo == False or (not (php_isset(lambda : imageinfo["mime"]))):
                        self.warning("COVERART vorbiscomment tag contains invalid image")
                        continue
                    # end if
                    ogg = php_new_class("self", lambda : self(self.getid3))
                    ogg.setstringmode(data)
                    info["ogg"]["comments"]["picture"][-1] = Array({"image_mime": imageinfo["mime"], "datalength": php_strlen(data), "picturetype": "cover art", "image_height": imageinfo["height"], "image_width": imageinfo["width"], "data": ogg.saveattachment("coverart", 0, php_strlen(data), imageinfo["mime"])})
                    ogg = None
                else:
                    info["ogg"]["comments"][php_strtolower(ThisFileInfo_ogg_comments_raw[i]["key"])][-1] = ThisFileInfo_ogg_comments_raw[i]["value"]
                # end if
            else:
                self.warning("[known problem with CDex >= v1.40, < v1.50b7] Invalid Ogg comment name/value pair [" + i + "]: " + commentstring)
            # end if
            ThisFileInfo_ogg_comments_raw[i] = None
            i += 1
        # end while
        ThisFileInfo_ogg_comments_raw = None
        #// Replay Gain Adjustment
        #// http://privatewww.essex.ac.uk/~djmrob/replaygain
        if (php_isset(lambda : info["ogg"]["comments"])) and php_is_array(info["ogg"]["comments"]):
            for index,commentvalue in info["ogg"]["comments"]:
                for case in Switch(index):
                    if case("rg_audiophile"):
                        pass
                    # end if
                    if case("replaygain_album_gain"):
                        info["replay_gain"]["album"]["adjustment"] = php_float(commentvalue[0])
                        info["ogg"]["comments"][index] = None
                        break
                    # end if
                    if case("rg_radio"):
                        pass
                    # end if
                    if case("replaygain_track_gain"):
                        info["replay_gain"]["track"]["adjustment"] = php_float(commentvalue[0])
                        info["ogg"]["comments"][index] = None
                        break
                    # end if
                    if case("replaygain_album_peak"):
                        info["replay_gain"]["album"]["peak"] = php_float(commentvalue[0])
                        info["ogg"]["comments"][index] = None
                        break
                    # end if
                    if case("rg_peak"):
                        pass
                    # end if
                    if case("replaygain_track_peak"):
                        info["replay_gain"]["track"]["peak"] = php_float(commentvalue[0])
                        info["ogg"]["comments"][index] = None
                        break
                    # end if
                    if case("replaygain_reference_loudness"):
                        info["replay_gain"]["reference_volume"] = php_float(commentvalue[0])
                        info["ogg"]["comments"][index] = None
                        break
                    # end if
                    if case():
                        break
                    # end if
                # end for
            # end for
        # end if
        self.fseek(OriginalOffset)
        return True
    # end def parsevorbiscomments
    #// 
    #// @param int $mode
    #// 
    #// @return string|null
    #//
    @classmethod
    def speexbandmodelookup(self, mode=None):
        
        SpeexBandModeLookup = Array()
        if php_empty(lambda : SpeexBandModeLookup):
            SpeexBandModeLookup[0] = "narrow"
            SpeexBandModeLookup[1] = "wide"
            SpeexBandModeLookup[2] = "ultra-wide"
        # end if
        return SpeexBandModeLookup[mode] if (php_isset(lambda : SpeexBandModeLookup[mode])) else None
    # end def speexbandmodelookup
    #// 
    #// @param array $OggInfoArray
    #// @param int   $SegmentNumber
    #// 
    #// @return int
    #//
    @classmethod
    def oggpagesegmentlength(self, OggInfoArray=None, SegmentNumber=1):
        
        segmentlength = 0
        i = 0
        while i < SegmentNumber:
            
            segmentlength = 0
            for key,value in OggInfoArray["segment_table"]:
                segmentlength += value
                if value < 255:
                    break
                # end if
            # end for
            i += 1
        # end while
        return segmentlength
    # end def oggpagesegmentlength
    #// 
    #// @param int $nominal_bitrate
    #// 
    #// @return float
    #//
    @classmethod
    def get_quality_from_nominal_bitrate(self, nominal_bitrate=None):
        
        #// decrease precision
        nominal_bitrate = nominal_bitrate / 1000
        if nominal_bitrate < 128:
            #// q-1 to q4
            qval = nominal_bitrate - 64 / 16
        elif nominal_bitrate < 256:
            #// q4 to q8
            qval = nominal_bitrate / 32
        elif nominal_bitrate < 320:
            #// q8 to q9
            qval = nominal_bitrate + 256 / 64
        else:
            #// q9 to q10
            qval = nominal_bitrate + 1300 / 180
        # end if
        #// return $qval; // 5.031324
        #// return intval($qval); // 5
        return round(qval, 1)
        pass
    # end def get_quality_from_nominal_bitrate
    #// 
    #// @param int $colorspace_id
    #// 
    #// @return string|null
    #//
    @classmethod
    def theoracolorspace(self, colorspace_id=None):
        
        TheoraColorSpaceLookup = Array()
        if php_empty(lambda : TheoraColorSpaceLookup):
            TheoraColorSpaceLookup[0] = "Undefined"
            TheoraColorSpaceLookup[1] = "Rec. 470M"
            TheoraColorSpaceLookup[2] = "Rec. 470BG"
            TheoraColorSpaceLookup[3] = "Reserved"
        # end if
        return TheoraColorSpaceLookup[colorspace_id] if (php_isset(lambda : TheoraColorSpaceLookup[colorspace_id])) else None
    # end def theoracolorspace
    #// 
    #// @param int $pixelformat_id
    #// 
    #// @return string|null
    #//
    @classmethod
    def theorapixelformat(self, pixelformat_id=None):
        
        TheoraPixelFormatLookup = Array()
        if php_empty(lambda : TheoraPixelFormatLookup):
            TheoraPixelFormatLookup[0] = "4:2:0"
            TheoraPixelFormatLookup[1] = "Reserved"
            TheoraPixelFormatLookup[2] = "4:2:2"
            TheoraPixelFormatLookup[3] = "4:4:4"
        # end if
        return TheoraPixelFormatLookup[pixelformat_id] if (php_isset(lambda : TheoraPixelFormatLookup[pixelformat_id])) else None
    # end def theorapixelformat
# end class getid3_ogg
