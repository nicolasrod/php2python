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
        
        
        info_ = self.getid3.info
        info_["fileformat"] = "ogg"
        #// Warn about illegal tags - only vorbiscomments are allowed
        if (php_isset(lambda : info_["id3v2"])):
            self.warning("Illegal ID3v2 tag present.")
        # end if
        if (php_isset(lambda : info_["id3v1"])):
            self.warning("Illegal ID3v1 tag present.")
        # end if
        if (php_isset(lambda : info_["ape"])):
            self.warning("Illegal APE tag present.")
        # end if
        #// Page 1 - Stream Header
        self.fseek(info_["avdataoffset"])
        oggpageinfo_ = self.parseoggpageheader()
        info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]] = oggpageinfo_
        if self.ftell() >= self.getid3.fread_buffer_size():
            self.error("Could not find start of Ogg page in the first " + self.getid3.fread_buffer_size() + " bytes (this might not be an Ogg-Vorbis file?)")
            info_["fileformat"] = None
            info_["ogg"] = None
            return False
        # end if
        filedata_ = self.fread(oggpageinfo_["page_length"])
        filedataoffset_ = 0
        if php_substr(filedata_, 0, 4) == "fLaC":
            info_["audio"]["dataformat"] = "flac"
            info_["audio"]["bitrate_mode"] = "vbr"
            info_["audio"]["lossless"] = True
        elif php_substr(filedata_, 1, 6) == "vorbis":
            self.parsevorbispageheader(filedata_, filedataoffset_, oggpageinfo_)
        elif php_substr(filedata_, 0, 8) == "OpusHead":
            if self.parseopuspageheader(filedata_, filedataoffset_, oggpageinfo_) == False:
                return False
            # end if
        elif php_substr(filedata_, 0, 8) == "Speex   ":
            #// http://www.speex.org/manual/node10.html
            info_["audio"]["dataformat"] = "speex"
            info_["mime_type"] = "audio/speex"
            info_["audio"]["bitrate_mode"] = "abr"
            info_["audio"]["lossless"] = False
            info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]]["speex_string"] = php_substr(filedata_, filedataoffset_, 8)
            #// hard-coded to 'Speex   '
            filedataoffset_ += 8
            info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]]["speex_version"] = php_substr(filedata_, filedataoffset_, 20)
            filedataoffset_ += 20
            info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]]["speex_version_id"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 4))
            filedataoffset_ += 4
            info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]]["header_size"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 4))
            filedataoffset_ += 4
            info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]]["rate"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 4))
            filedataoffset_ += 4
            info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]]["mode"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 4))
            filedataoffset_ += 4
            info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]]["mode_bitstream_version"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 4))
            filedataoffset_ += 4
            info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]]["nb_channels"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 4))
            filedataoffset_ += 4
            info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]]["bitrate"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 4))
            filedataoffset_ += 4
            info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]]["framesize"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 4))
            filedataoffset_ += 4
            info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]]["vbr"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 4))
            filedataoffset_ += 4
            info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]]["frames_per_packet"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 4))
            filedataoffset_ += 4
            info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]]["extra_headers"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 4))
            filedataoffset_ += 4
            info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]]["reserved1"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 4))
            filedataoffset_ += 4
            info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]]["reserved2"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 4))
            filedataoffset_ += 4
            info_["speex"]["speex_version"] = php_trim(info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]]["speex_version"])
            info_["speex"]["sample_rate"] = info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]]["rate"]
            info_["speex"]["channels"] = info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]]["nb_channels"]
            info_["speex"]["vbr"] = php_bool(info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]]["vbr"])
            info_["speex"]["band_type"] = self.speexbandmodelookup(info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]]["mode"])
            info_["audio"]["sample_rate"] = info_["speex"]["sample_rate"]
            info_["audio"]["channels"] = info_["speex"]["channels"]
            if info_["speex"]["vbr"]:
                info_["audio"]["bitrate_mode"] = "vbr"
            # end if
        elif php_substr(filedata_, 0, 7) == "" + "theora":
            #// http://www.theora.org/doc/Theora.pdf (section 6.2)
            info_["ogg"]["pageheader"]["theora"]["theora_magic"] = php_substr(filedata_, filedataoffset_, 7)
            #// hard-coded to "\x80.'theora'
            filedataoffset_ += 7
            info_["ogg"]["pageheader"]["theora"]["version_major"] = getid3_lib.bigendian2int(php_substr(filedata_, filedataoffset_, 1))
            filedataoffset_ += 1
            info_["ogg"]["pageheader"]["theora"]["version_minor"] = getid3_lib.bigendian2int(php_substr(filedata_, filedataoffset_, 1))
            filedataoffset_ += 1
            info_["ogg"]["pageheader"]["theora"]["version_revision"] = getid3_lib.bigendian2int(php_substr(filedata_, filedataoffset_, 1))
            filedataoffset_ += 1
            info_["ogg"]["pageheader"]["theora"]["frame_width_macroblocks"] = getid3_lib.bigendian2int(php_substr(filedata_, filedataoffset_, 2))
            filedataoffset_ += 2
            info_["ogg"]["pageheader"]["theora"]["frame_height_macroblocks"] = getid3_lib.bigendian2int(php_substr(filedata_, filedataoffset_, 2))
            filedataoffset_ += 2
            info_["ogg"]["pageheader"]["theora"]["resolution_x"] = getid3_lib.bigendian2int(php_substr(filedata_, filedataoffset_, 3))
            filedataoffset_ += 3
            info_["ogg"]["pageheader"]["theora"]["resolution_y"] = getid3_lib.bigendian2int(php_substr(filedata_, filedataoffset_, 3))
            filedataoffset_ += 3
            info_["ogg"]["pageheader"]["theora"]["picture_offset_x"] = getid3_lib.bigendian2int(php_substr(filedata_, filedataoffset_, 1))
            filedataoffset_ += 1
            info_["ogg"]["pageheader"]["theora"]["picture_offset_y"] = getid3_lib.bigendian2int(php_substr(filedata_, filedataoffset_, 1))
            filedataoffset_ += 1
            info_["ogg"]["pageheader"]["theora"]["frame_rate_numerator"] = getid3_lib.bigendian2int(php_substr(filedata_, filedataoffset_, 4))
            filedataoffset_ += 4
            info_["ogg"]["pageheader"]["theora"]["frame_rate_denominator"] = getid3_lib.bigendian2int(php_substr(filedata_, filedataoffset_, 4))
            filedataoffset_ += 4
            info_["ogg"]["pageheader"]["theora"]["pixel_aspect_numerator"] = getid3_lib.bigendian2int(php_substr(filedata_, filedataoffset_, 3))
            filedataoffset_ += 3
            info_["ogg"]["pageheader"]["theora"]["pixel_aspect_denominator"] = getid3_lib.bigendian2int(php_substr(filedata_, filedataoffset_, 3))
            filedataoffset_ += 3
            info_["ogg"]["pageheader"]["theora"]["color_space_id"] = getid3_lib.bigendian2int(php_substr(filedata_, filedataoffset_, 1))
            filedataoffset_ += 1
            info_["ogg"]["pageheader"]["theora"]["nominal_bitrate"] = getid3_lib.bigendian2int(php_substr(filedata_, filedataoffset_, 3))
            filedataoffset_ += 3
            info_["ogg"]["pageheader"]["theora"]["flags"] = getid3_lib.bigendian2int(php_substr(filedata_, filedataoffset_, 2))
            filedataoffset_ += 2
            info_["ogg"]["pageheader"]["theora"]["quality"] = info_["ogg"]["pageheader"]["theora"]["flags"] & 64512 >> 10
            info_["ogg"]["pageheader"]["theora"]["kfg_shift"] = info_["ogg"]["pageheader"]["theora"]["flags"] & 992 >> 5
            info_["ogg"]["pageheader"]["theora"]["pixel_format_id"] = info_["ogg"]["pageheader"]["theora"]["flags"] & 24 >> 3
            info_["ogg"]["pageheader"]["theora"]["reserved"] = info_["ogg"]["pageheader"]["theora"]["flags"] & 7 >> 0
            #// should be 0
            info_["ogg"]["pageheader"]["theora"]["color_space"] = self.theoracolorspace(info_["ogg"]["pageheader"]["theora"]["color_space_id"])
            info_["ogg"]["pageheader"]["theora"]["pixel_format"] = self.theorapixelformat(info_["ogg"]["pageheader"]["theora"]["pixel_format_id"])
            info_["video"]["dataformat"] = "theora"
            info_["mime_type"] = "video/ogg"
            #// $info['audio']['bitrate_mode'] = 'abr';
            #// $info['audio']['lossless']     = false;
            info_["video"]["resolution_x"] = info_["ogg"]["pageheader"]["theora"]["resolution_x"]
            info_["video"]["resolution_y"] = info_["ogg"]["pageheader"]["theora"]["resolution_y"]
            if info_["ogg"]["pageheader"]["theora"]["frame_rate_denominator"] > 0:
                info_["video"]["frame_rate"] = php_float(info_["ogg"]["pageheader"]["theora"]["frame_rate_numerator"]) / info_["ogg"]["pageheader"]["theora"]["frame_rate_denominator"]
            # end if
            if info_["ogg"]["pageheader"]["theora"]["pixel_aspect_denominator"] > 0:
                info_["video"]["pixel_aspect_ratio"] = php_float(info_["ogg"]["pageheader"]["theora"]["pixel_aspect_numerator"]) / info_["ogg"]["pageheader"]["theora"]["pixel_aspect_denominator"]
            # end if
            self.warning("Ogg Theora (v3) not fully supported in this version of getID3 [" + self.getid3.version() + "] -- bitrate, playtime and all audio data are currently unavailable")
        elif php_substr(filedata_, 0, 8) == "fishead ":
            #// Ogg Skeleton version 3.0 Format Specification
            #// http://xiph.org/ogg/doc/skeleton.html
            filedataoffset_ += 8
            info_["ogg"]["skeleton"]["fishead"]["raw"]["version_major"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 2))
            filedataoffset_ += 2
            info_["ogg"]["skeleton"]["fishead"]["raw"]["version_minor"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 2))
            filedataoffset_ += 2
            info_["ogg"]["skeleton"]["fishead"]["raw"]["presentationtime_numerator"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 8))
            filedataoffset_ += 8
            info_["ogg"]["skeleton"]["fishead"]["raw"]["presentationtime_denominator"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 8))
            filedataoffset_ += 8
            info_["ogg"]["skeleton"]["fishead"]["raw"]["basetime_numerator"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 8))
            filedataoffset_ += 8
            info_["ogg"]["skeleton"]["fishead"]["raw"]["basetime_denominator"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 8))
            filedataoffset_ += 8
            info_["ogg"]["skeleton"]["fishead"]["raw"]["utc"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 20))
            filedataoffset_ += 20
            info_["ogg"]["skeleton"]["fishead"]["version"] = info_["ogg"]["skeleton"]["fishead"]["raw"]["version_major"] + "." + info_["ogg"]["skeleton"]["fishead"]["raw"]["version_minor"]
            info_["ogg"]["skeleton"]["fishead"]["presentationtime"] = info_["ogg"]["skeleton"]["fishead"]["raw"]["presentationtime_numerator"] / info_["ogg"]["skeleton"]["fishead"]["raw"]["presentationtime_denominator"]
            info_["ogg"]["skeleton"]["fishead"]["basetime"] = info_["ogg"]["skeleton"]["fishead"]["raw"]["basetime_numerator"] / info_["ogg"]["skeleton"]["fishead"]["raw"]["basetime_denominator"]
            info_["ogg"]["skeleton"]["fishead"]["utc"] = info_["ogg"]["skeleton"]["fishead"]["raw"]["utc"]
            counter_ = 0
            while True:
                oggpageinfo_ = self.parseoggpageheader()
                info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"] + "." + counter_] = oggpageinfo_
                counter_ += 1
                filedata_ = self.fread(oggpageinfo_["page_length"])
                self.fseek(oggpageinfo_["page_end_offset"])
                if php_substr(filedata_, 0, 8) == "fisbone ":
                    filedataoffset_ = 8
                    info_["ogg"]["skeleton"]["fisbone"]["raw"]["message_header_offset"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 4))
                    filedataoffset_ += 4
                    info_["ogg"]["skeleton"]["fisbone"]["raw"]["serial_number"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 4))
                    filedataoffset_ += 4
                    info_["ogg"]["skeleton"]["fisbone"]["raw"]["number_header_packets"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 4))
                    filedataoffset_ += 4
                    info_["ogg"]["skeleton"]["fisbone"]["raw"]["granulerate_numerator"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 8))
                    filedataoffset_ += 8
                    info_["ogg"]["skeleton"]["fisbone"]["raw"]["granulerate_denominator"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 8))
                    filedataoffset_ += 8
                    info_["ogg"]["skeleton"]["fisbone"]["raw"]["basegranule"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 8))
                    filedataoffset_ += 8
                    info_["ogg"]["skeleton"]["fisbone"]["raw"]["preroll"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 4))
                    filedataoffset_ += 4
                    info_["ogg"]["skeleton"]["fisbone"]["raw"]["granuleshift"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 1))
                    filedataoffset_ += 1
                    info_["ogg"]["skeleton"]["fisbone"]["raw"]["padding"] = php_substr(filedata_, filedataoffset_, 3)
                    filedataoffset_ += 3
                elif php_substr(filedata_, 1, 6) == "theora":
                    info_["video"]["dataformat"] = "theora1"
                    self.error("Ogg Theora (v1) not correctly handled in this version of getID3 [" + self.getid3.version() + "]")
                    pass
                elif php_substr(filedata_, 1, 6) == "vorbis":
                    self.parsevorbispageheader(filedata_, filedataoffset_, oggpageinfo_)
                else:
                    self.error("unexpected")
                    pass
                # end if
                pass
                
                if oggpageinfo_["page_seqno"] == 0 and php_substr(filedata_, 0, 8) != "fisbone ":
                    break
                # end if
            # end while
            self.fseek(oggpageinfo_["page_start_offset"])
            self.error("Ogg Skeleton not correctly handled in this version of getID3 [" + self.getid3.version() + "]")
            pass
        elif php_substr(filedata_, 0, 5) == "" + "FLAC":
            #// https://xiph.org/flac/ogg_mapping.html
            info_["audio"]["dataformat"] = "flac"
            info_["audio"]["bitrate_mode"] = "vbr"
            info_["audio"]["lossless"] = True
            info_["ogg"]["flac"]["header"]["version_major"] = php_ord(php_substr(filedata_, 5, 1))
            info_["ogg"]["flac"]["header"]["version_minor"] = php_ord(php_substr(filedata_, 6, 1))
            info_["ogg"]["flac"]["header"]["header_packets"] = getid3_lib.bigendian2int(php_substr(filedata_, 7, 2)) + 1
            #// "A two-byte, big-endian binary number signifying the number of header (non-audio) packets, not including this one. This number may be zero (0x0000) to signify 'unknown' but be aware that some decoders may not be able to handle such streams."
            info_["ogg"]["flac"]["header"]["magic"] = php_substr(filedata_, 9, 4)
            if info_["ogg"]["flac"]["header"]["magic"] != "fLaC":
                self.error("Ogg-FLAC expecting \"fLaC\", found \"" + info_["ogg"]["flac"]["header"]["magic"] + "\" (" + php_trim(getid3_lib.printhexbytes(info_["ogg"]["flac"]["header"]["magic"])) + ")")
                return False
            # end if
            info_["ogg"]["flac"]["header"]["STREAMINFO_bytes"] = getid3_lib.bigendian2int(php_substr(filedata_, 13, 4))
            info_["flac"]["STREAMINFO"] = getid3_flac.parsestreaminfodata(php_substr(filedata_, 17, 34))
            if (not php_empty(lambda : info_["flac"]["STREAMINFO"]["sample_rate"])):
                info_["audio"]["bitrate_mode"] = "vbr"
                info_["audio"]["sample_rate"] = info_["flac"]["STREAMINFO"]["sample_rate"]
                info_["audio"]["channels"] = info_["flac"]["STREAMINFO"]["channels"]
                info_["audio"]["bits_per_sample"] = info_["flac"]["STREAMINFO"]["bits_per_sample"]
                info_["playtime_seconds"] = info_["flac"]["STREAMINFO"]["samples_stream"] / info_["flac"]["STREAMINFO"]["sample_rate"]
            # end if
        else:
            self.error("Expecting one of \"vorbis\", \"Speex\", \"OpusHead\", \"vorbis\", \"fishhead\", \"theora\", \"fLaC\" identifier strings, found \"" + php_substr(filedata_, 0, 8) + "\"")
            info_["ogg"] = None
            info_["mime_type"] = None
            return False
        # end if
        #// Page 2 - Comment Header
        oggpageinfo_ = self.parseoggpageheader()
        info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]] = oggpageinfo_
        for case in Switch(info_["audio"]["dataformat"]):
            if case("vorbis"):
                filedata_ = self.fread(info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]]["page_length"])
                info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]]["packet_type"] = getid3_lib.littleendian2int(php_substr(filedata_, 0, 1))
                info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]]["stream_type"] = php_substr(filedata_, 1, 6)
                #// hard-coded to 'vorbis'
                self.parsevorbiscomments()
                break
            # end if
            if case("flac"):
                flac_ = php_new_class("getid3_flac", lambda : getid3_flac(self.getid3))
                if (not flac_.parsemetadata()):
                    self.error("Failed to parse FLAC headers")
                    return False
                # end if
                flac_ = None
                break
            # end if
            if case("speex"):
                self.fseek(info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]]["page_length"], SEEK_CUR)
                self.parsevorbiscomments()
                break
            # end if
            if case("opus"):
                filedata_ = self.fread(info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]]["page_length"])
                info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]]["stream_type"] = php_substr(filedata_, 0, 8)
                #// hard-coded to 'OpusTags'
                if php_substr(filedata_, 0, 8) != "OpusTags":
                    self.error("Expected \"OpusTags\" as header but got \"" + php_substr(filedata_, 0, 8) + "\"")
                    return False
                # end if
                self.parsevorbiscomments()
                break
            # end if
        # end for
        #// Last Page - Number of Samples
        if (not getid3_lib.intvaluesupported(info_["avdataend"])):
            self.warning("Unable to parse Ogg end chunk file (PHP does not support file operations beyond " + round(PHP_INT_MAX / 1073741824) + "GB)")
        else:
            self.fseek(php_max(info_["avdataend"] - self.getid3.fread_buffer_size(), 0))
            LastChunkOfOgg_ = php_strrev(self.fread(self.getid3.fread_buffer_size()))
            LastOggSpostion_ = php_strpos(LastChunkOfOgg_, "SggO")
            if LastOggSpostion_:
                self.fseek(info_["avdataend"] - LastOggSpostion_ + php_strlen("SggO"))
                info_["avdataend"] = self.ftell()
                info_["ogg"]["pageheader"]["eos"] = self.parseoggpageheader()
                info_["ogg"]["samples"] = info_["ogg"]["pageheader"]["eos"]["pcm_abs_position"]
                if info_["ogg"]["samples"] == 0:
                    self.error("Corrupt Ogg file: eos.number of samples == zero")
                    return False
                # end if
                if (not php_empty(lambda : info_["audio"]["sample_rate"])):
                    info_["ogg"]["bitrate_average"] = info_["avdataend"] - info_["avdataoffset"] * 8 / info_["ogg"]["samples"] / info_["audio"]["sample_rate"]
                # end if
            # end if
        # end if
        if (not php_empty(lambda : info_["ogg"]["bitrate_average"])):
            info_["audio"]["bitrate"] = info_["ogg"]["bitrate_average"]
        elif (not php_empty(lambda : info_["ogg"]["bitrate_nominal"])):
            info_["audio"]["bitrate"] = info_["ogg"]["bitrate_nominal"]
        elif (not php_empty(lambda : info_["ogg"]["bitrate_min"])) and (not php_empty(lambda : info_["ogg"]["bitrate_max"])):
            info_["audio"]["bitrate"] = info_["ogg"]["bitrate_min"] + info_["ogg"]["bitrate_max"] / 2
        # end if
        if (php_isset(lambda : info_["audio"]["bitrate"])) and (not (php_isset(lambda : info_["playtime_seconds"]))):
            if info_["audio"]["bitrate"] == 0:
                self.error("Corrupt Ogg file: bitrate_audio == zero")
                return False
            # end if
            info_["playtime_seconds"] = php_float(info_["avdataend"] - info_["avdataoffset"] * 8 / info_["audio"]["bitrate"])
        # end if
        if (php_isset(lambda : info_["ogg"]["vendor"])):
            info_["audio"]["encoder"] = php_preg_replace("/^Encoded with /", "", info_["ogg"]["vendor"])
            #// Vorbis only
            if info_["audio"]["dataformat"] == "vorbis":
                #// Vorbis 1.0 starts with Xiph.Org
                if php_preg_match("/^Xiph.Org/", info_["audio"]["encoder"]):
                    if info_["audio"]["bitrate_mode"] == "abr":
                        #// Set -b 128 on abr files
                        info_["audio"]["encoder_options"] = "-b " + round(info_["ogg"]["bitrate_nominal"] / 1000)
                    elif info_["audio"]["bitrate_mode"] == "vbr" and info_["audio"]["channels"] == 2 and info_["audio"]["sample_rate"] >= 44100 and info_["audio"]["sample_rate"] <= 48000:
                        #// Set -q N on vbr files
                        info_["audio"]["encoder_options"] = "-q " + self.get_quality_from_nominal_bitrate(info_["ogg"]["bitrate_nominal"])
                    # end if
                # end if
                if php_empty(lambda : info_["audio"]["encoder_options"]) and (not php_empty(lambda : info_["ogg"]["bitrate_nominal"])):
                    info_["audio"]["encoder_options"] = "Nominal bitrate: " + php_intval(round(info_["ogg"]["bitrate_nominal"] / 1000)) + "kbps"
                # end if
            # end if
        # end if
        return True
    # end def analyze
    counter_ += 1
    #// 
    #// @param string $filedata
    #// @param int    $filedataoffset
    #// @param array  $oggpageinfo
    #// 
    #// @return bool
    #//
    def parsevorbispageheader(self, filedata_=None, filedataoffset_=None, oggpageinfo_=None):
        
        
        info_ = self.getid3.info
        info_["audio"]["dataformat"] = "vorbis"
        info_["audio"]["lossless"] = False
        info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]]["packet_type"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 1))
        filedataoffset_ += 1
        info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]]["stream_type"] = php_substr(filedata_, filedataoffset_, 6)
        #// hard-coded to 'vorbis'
        filedataoffset_ += 6
        info_["ogg"]["bitstreamversion"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 4))
        filedataoffset_ += 4
        info_["ogg"]["numberofchannels"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 1))
        filedataoffset_ += 1
        info_["audio"]["channels"] = info_["ogg"]["numberofchannels"]
        info_["ogg"]["samplerate"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 4))
        filedataoffset_ += 4
        if info_["ogg"]["samplerate"] == 0:
            self.error("Corrupt Ogg file: sample rate == zero")
            return False
        # end if
        info_["audio"]["sample_rate"] = info_["ogg"]["samplerate"]
        info_["ogg"]["samples"] = 0
        #// filled in later
        info_["ogg"]["bitrate_average"] = 0
        #// filled in later
        info_["ogg"]["bitrate_max"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 4))
        filedataoffset_ += 4
        info_["ogg"]["bitrate_nominal"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 4))
        filedataoffset_ += 4
        info_["ogg"]["bitrate_min"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 4))
        filedataoffset_ += 4
        info_["ogg"]["blocksize_small"] = pow(2, getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 1)) & 15)
        info_["ogg"]["blocksize_large"] = pow(2, getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 1)) & 240 >> 4)
        info_["ogg"]["stop_bit"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 1))
        #// must be 1, marks end of packet
        info_["audio"]["bitrate_mode"] = "vbr"
        #// overridden if actually abr
        if info_["ogg"]["bitrate_max"] == 4294967295:
            info_["ogg"]["bitrate_max"] = None
            info_["audio"]["bitrate_mode"] = "abr"
        # end if
        if info_["ogg"]["bitrate_nominal"] == 4294967295:
            info_["ogg"]["bitrate_nominal"] = None
        # end if
        if info_["ogg"]["bitrate_min"] == 4294967295:
            info_["ogg"]["bitrate_min"] = None
            info_["audio"]["bitrate_mode"] = "abr"
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
    def parseopuspageheader(self, filedata_=None, filedataoffset_=None, oggpageinfo_=None):
        
        
        info_ = self.getid3.info
        info_["audio"]["dataformat"] = "opus"
        info_["mime_type"] = "audio/ogg; codecs=opus"
        #// @todo find a usable way to detect abr (vbr that is padded to be abr)
        info_["audio"]["bitrate_mode"] = "vbr"
        info_["audio"]["lossless"] = False
        info_["ogg"]["pageheader"]["opus"]["opus_magic"] = php_substr(filedata_, filedataoffset_, 8)
        #// hard-coded to 'OpusHead'
        filedataoffset_ += 8
        info_["ogg"]["pageheader"]["opus"]["version"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 1))
        filedataoffset_ += 1
        if info_["ogg"]["pageheader"]["opus"]["version"] < 1 or info_["ogg"]["pageheader"]["opus"]["version"] > 15:
            self.error("Unknown opus version number (only accepting 1-15)")
            return False
        # end if
        info_["ogg"]["pageheader"]["opus"]["out_channel_count"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 1))
        filedataoffset_ += 1
        if info_["ogg"]["pageheader"]["opus"]["out_channel_count"] == 0:
            self.error("Invalid channel count in opus header (must not be zero)")
            return False
        # end if
        info_["ogg"]["pageheader"]["opus"]["pre_skip"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 2))
        filedataoffset_ += 2
        info_["ogg"]["pageheader"]["opus"]["input_sample_rate"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 4))
        filedataoffset_ += 4
        #// $info['ogg']['pageheader']['opus']['output_gain'] = getid3_lib::LittleEndian2Int(substr($filedata, $filedataoffset,  2));
        #// $filedataoffset += 2;
        #// $info['ogg']['pageheader']['opus']['channel_mapping_family'] = getid3_lib::LittleEndian2Int(substr($filedata, $filedataoffset,  1));
        #// $filedataoffset += 1;
        info_["opus"]["opus_version"] = info_["ogg"]["pageheader"]["opus"]["version"]
        info_["opus"]["sample_rate_input"] = info_["ogg"]["pageheader"]["opus"]["input_sample_rate"]
        info_["opus"]["out_channel_count"] = info_["ogg"]["pageheader"]["opus"]["out_channel_count"]
        info_["audio"]["channels"] = info_["opus"]["out_channel_count"]
        info_["audio"]["sample_rate_input"] = info_["opus"]["sample_rate_input"]
        info_["audio"]["sample_rate"] = 48000
        #// "All Opus audio is coded at 48 kHz, and should also be decoded at 48 kHz for playback (unless the target hardware does not support this sampling rate). However, this field may be used to resample the audio back to the original sampling rate, for example, when saving the output to a file." -- https://mf4.xiph.org/jenkins/view/opus/job/opusfile-unix/ws/doc/html/structOpusHead.html
        return True
    # end def parseopuspageheader
    #// 
    #// @return array|false
    #//
    def parseoggpageheader(self):
        
        
        #// http://xiph.org/ogg/vorbis/doc/framing.html
        oggheader_["page_start_offset"] = self.ftell()
        #// where we started from in the file
        filedata_ = self.fread(self.getid3.fread_buffer_size())
        filedataoffset_ = 0
        while True:
            filedataoffset_ += 1
            if not (php_substr(filedata_, filedataoffset_, 4) != "OggS"):
                break
            # end if
            if self.ftell() - oggheader_["page_start_offset"] >= self.getid3.fread_buffer_size():
                #// should be found before here
                return False
                filedataoffset_ += 1
            # end if
            if filedataoffset_ + 28 > php_strlen(filedata_) or php_strlen(filedata_) < 28:
                if self.feof() or filedata_ += self.fread(self.getid3.fread_buffer_size()) == "":
                    #// get some more data, unless eof, in which case fail
                    return False
                # end if
            # end if
        # end while
        filedataoffset_ += php_strlen("OggS") - 1
        #// page, delimited by 'OggS'
        oggheader_["stream_structver"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 1))
        filedataoffset_ += 1
        oggheader_["flags_raw"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 1))
        filedataoffset_ += 1
        oggheader_["flags"]["fresh"] = php_bool(oggheader_["flags_raw"] & 1)
        #// fresh packet
        oggheader_["flags"]["bos"] = php_bool(oggheader_["flags_raw"] & 2)
        #// first page of logical bitstream (bos)
        oggheader_["flags"]["eos"] = php_bool(oggheader_["flags_raw"] & 4)
        #// last page of logical bitstream (eos)
        oggheader_["pcm_abs_position"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 8))
        filedataoffset_ += 8
        oggheader_["stream_serialno"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 4))
        filedataoffset_ += 4
        oggheader_["page_seqno"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 4))
        filedataoffset_ += 4
        oggheader_["page_checksum"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 4))
        filedataoffset_ += 4
        oggheader_["page_segments"] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 1))
        filedataoffset_ += 1
        oggheader_["page_length"] = 0
        i_ = 0
        while i_ < oggheader_["page_segments"]:
            
            oggheader_["segment_table"][i_] = getid3_lib.littleendian2int(php_substr(filedata_, filedataoffset_, 1))
            filedataoffset_ += 1
            oggheader_["page_length"] += oggheader_["segment_table"][i_]
            i_ += 1
        # end while
        oggheader_["header_end_offset"] = oggheader_["page_start_offset"] + filedataoffset_
        oggheader_["page_end_offset"] = oggheader_["header_end_offset"] + oggheader_["page_length"]
        self.fseek(oggheader_["header_end_offset"])
        return oggheader_
    # end def parseoggpageheader
    #// 
    #// @link http://xiph.org/vorbis/doc/Vorbis_I_spec.html#x1-810005
    #// 
    #// @return bool
    #//
    def parsevorbiscomments(self):
        
        
        info_ = self.getid3.info
        OriginalOffset_ = self.ftell()
        commentdata_ = None
        commentdataoffset_ = 0
        VorbisCommentPage_ = 1
        CommentStartOffset_ = 0
        for case in Switch(info_["audio"]["dataformat"]):
            if case("vorbis"):
                pass
            # end if
            if case("speex"):
                pass
            # end if
            if case("opus"):
                CommentStartOffset_ = info_["ogg"]["pageheader"][VorbisCommentPage_]["page_start_offset"]
                #// Second Ogg page, after header block
                self.fseek(CommentStartOffset_)
                commentdataoffset_ = 27 + info_["ogg"]["pageheader"][VorbisCommentPage_]["page_segments"]
                commentdata_ = self.fread(self.oggpagesegmentlength(info_["ogg"]["pageheader"][VorbisCommentPage_], 1) + commentdataoffset_)
                if info_["audio"]["dataformat"] == "vorbis":
                    commentdataoffset_ += php_strlen("vorbis") + 1
                else:
                    if info_["audio"]["dataformat"] == "opus":
                        commentdataoffset_ += php_strlen("OpusTags")
                    # end if
                # end if
                break
            # end if
            if case("flac"):
                CommentStartOffset_ = info_["flac"]["VORBIS_COMMENT"]["raw"]["offset"] + 4
                self.fseek(CommentStartOffset_)
                commentdata_ = self.fread(info_["flac"]["VORBIS_COMMENT"]["raw"]["block_length"])
                break
            # end if
            if case():
                return False
                break
            # end if
        # end for
        VendorSize_ = getid3_lib.littleendian2int(php_substr(commentdata_, commentdataoffset_, 4))
        commentdataoffset_ += 4
        info_["ogg"]["vendor"] = php_substr(commentdata_, commentdataoffset_, VendorSize_)
        commentdataoffset_ += VendorSize_
        CommentsCount_ = getid3_lib.littleendian2int(php_substr(commentdata_, commentdataoffset_, 4))
        commentdataoffset_ += 4
        info_["avdataoffset"] = CommentStartOffset_ + commentdataoffset_
        basicfields_ = Array("TITLE", "ARTIST", "ALBUM", "TRACKNUMBER", "GENRE", "DATE", "DESCRIPTION", "COMMENT")
        ThisFileInfo_ogg_comments_raw_ = info_["ogg"]["comments_raw"]
        i_ = 0
        while i_ < CommentsCount_:
            
            if i_ >= 10000:
                #// https://github.com/owncloud/music/issues/212#issuecomment-43082336
                self.warning("Unexpectedly large number (" + CommentsCount_ + ") of Ogg comments - breaking after reading " + i_ + " comments")
                break
            # end if
            ThisFileInfo_ogg_comments_raw_[i_]["dataoffset"] = CommentStartOffset_ + commentdataoffset_
            if self.ftell() < ThisFileInfo_ogg_comments_raw_[i_]["dataoffset"] + 4:
                oggpageinfo_ = self.parseoggpageheader()
                if oggpageinfo_:
                    info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]] = oggpageinfo_
                    VorbisCommentPage_ += 1
                    #// First, save what we haven't read yet
                    AsYetUnusedData_ = php_substr(commentdata_, commentdataoffset_)
                    #// Then take that data off the end
                    commentdata_ = php_substr(commentdata_, 0, commentdataoffset_)
                    #// Add [headerlength] bytes of dummy data for the Ogg Page Header, just to keep absolute offsets correct
                    commentdata_ += php_str_repeat(" ", 27 + info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]]["page_segments"])
                    commentdataoffset_ += 27 + info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]]["page_segments"]
                    #// Finally, stick the unused data back on the end
                    commentdata_ += AsYetUnusedData_
                    #// $commentdata .= $this->fread($info['ogg']['pageheader'][$oggpageinfo['page_seqno']]['page_length']);
                    commentdata_ += self.fread(self.oggpagesegmentlength(info_["ogg"]["pageheader"][VorbisCommentPage_], 1))
                # end if
            # end if
            ThisFileInfo_ogg_comments_raw_[i_]["size"] = getid3_lib.littleendian2int(php_substr(commentdata_, commentdataoffset_, 4))
            #// replace avdataoffset with position just after the last vorbiscomment
            info_["avdataoffset"] = ThisFileInfo_ogg_comments_raw_[i_]["dataoffset"] + ThisFileInfo_ogg_comments_raw_[i_]["size"] + 4
            commentdataoffset_ += 4
            while True:
                
                if not (php_strlen(commentdata_) - commentdataoffset_ < ThisFileInfo_ogg_comments_raw_[i_]["size"]):
                    break
                # end if
                if ThisFileInfo_ogg_comments_raw_[i_]["size"] > info_["avdataend"] or ThisFileInfo_ogg_comments_raw_[i_]["size"] < 0:
                    self.warning("Invalid Ogg comment size (comment #" + i_ + ", claims to be " + number_format(ThisFileInfo_ogg_comments_raw_[i_]["size"]) + " bytes) - aborting reading comments")
                    break
                # end if
                VorbisCommentPage_ += 1
                oggpageinfo_ = self.parseoggpageheader()
                info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]] = oggpageinfo_
                #// First, save what we haven't read yet
                AsYetUnusedData_ = php_substr(commentdata_, commentdataoffset_)
                #// Then take that data off the end
                commentdata_ = php_substr(commentdata_, 0, commentdataoffset_)
                #// Add [headerlength] bytes of dummy data for the Ogg Page Header, just to keep absolute offsets correct
                commentdata_ += php_str_repeat(" ", 27 + info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]]["page_segments"])
                commentdataoffset_ += 27 + info_["ogg"]["pageheader"][oggpageinfo_["page_seqno"]]["page_segments"]
                #// Finally, stick the unused data back on the end
                commentdata_ += AsYetUnusedData_
                #// $commentdata .= $this->fread($info['ogg']['pageheader'][$oggpageinfo['page_seqno']]['page_length']);
                if (not (php_isset(lambda : info_["ogg"]["pageheader"][VorbisCommentPage_]))):
                    self.warning("undefined Vorbis Comment page \"" + VorbisCommentPage_ + "\" at offset " + self.ftell())
                    break
                # end if
                readlength_ = self.oggpagesegmentlength(info_["ogg"]["pageheader"][VorbisCommentPage_], 1)
                if readlength_ <= 0:
                    self.warning("invalid length Vorbis Comment page \"" + VorbisCommentPage_ + "\" at offset " + self.ftell())
                    break
                # end if
                commentdata_ += self.fread(readlength_)
                pass
            # end while
            ThisFileInfo_ogg_comments_raw_[i_]["offset"] = commentdataoffset_
            commentstring_ = php_substr(commentdata_, commentdataoffset_, ThisFileInfo_ogg_comments_raw_[i_]["size"])
            commentdataoffset_ += ThisFileInfo_ogg_comments_raw_[i_]["size"]
            if (not commentstring_):
                #// no comment?
                self.warning("Blank Ogg comment [" + i_ + "]")
            elif php_strstr(commentstring_, "="):
                commentexploded_ = php_explode("=", commentstring_, 2)
                ThisFileInfo_ogg_comments_raw_[i_]["key"] = php_strtoupper(commentexploded_[0])
                ThisFileInfo_ogg_comments_raw_[i_]["value"] = commentexploded_[1] if (php_isset(lambda : commentexploded_[1])) else ""
                if ThisFileInfo_ogg_comments_raw_[i_]["key"] == "METADATA_BLOCK_PICTURE":
                    #// http://wiki.xiph.org/VorbisComment#METADATA_BLOCK_PICTURE
                    #// The unencoded format is that of the FLAC picture block. The fields are stored in big endian order as in FLAC, picture data is stored according to the relevant standard.
                    #// http://flac.sourceforge.net/format.html#metadata_block_picture
                    flac_ = php_new_class("getid3_flac", lambda : getid3_flac(self.getid3))
                    flac_.setstringmode(php_base64_decode(ThisFileInfo_ogg_comments_raw_[i_]["value"]))
                    flac_.parsepicture()
                    info_["ogg"]["comments"]["picture"][-1] = flac_.getid3.info["flac"]["PICTURE"][0]
                    flac_ = None
                elif ThisFileInfo_ogg_comments_raw_[i_]["key"] == "COVERART":
                    data_ = php_base64_decode(ThisFileInfo_ogg_comments_raw_[i_]["value"])
                    self.notice("Found deprecated COVERART tag, it should be replaced in honor of METADATA_BLOCK_PICTURE structure")
                    #// @todo use 'coverartmime' where available
                    imageinfo_ = getid3_lib.getdataimagesize(data_)
                    if imageinfo_ == False or (not (php_isset(lambda : imageinfo_["mime"]))):
                        self.warning("COVERART vorbiscomment tag contains invalid image")
                        continue
                    # end if
                    ogg_ = php_new_class("self", lambda : self(self.getid3))
                    ogg_.setstringmode(data_)
                    info_["ogg"]["comments"]["picture"][-1] = Array({"image_mime": imageinfo_["mime"], "datalength": php_strlen(data_), "picturetype": "cover art", "image_height": imageinfo_["height"], "image_width": imageinfo_["width"], "data": ogg_.saveattachment("coverart", 0, php_strlen(data_), imageinfo_["mime"])})
                    ogg_ = None
                else:
                    info_["ogg"]["comments"][php_strtolower(ThisFileInfo_ogg_comments_raw_[i_]["key"])][-1] = ThisFileInfo_ogg_comments_raw_[i_]["value"]
                # end if
            else:
                self.warning("[known problem with CDex >= v1.40, < v1.50b7] Invalid Ogg comment name/value pair [" + i_ + "]: " + commentstring_)
            # end if
            ThisFileInfo_ogg_comments_raw_[i_] = None
            i_ += 1
        # end while
        ThisFileInfo_ogg_comments_raw_ = None
        #// Replay Gain Adjustment
        #// http://privatewww.essex.ac.uk/~djmrob/replaygain
        if (php_isset(lambda : info_["ogg"]["comments"])) and php_is_array(info_["ogg"]["comments"]):
            for index_,commentvalue_ in info_["ogg"]["comments"]:
                for case in Switch(index_):
                    if case("rg_audiophile"):
                        pass
                    # end if
                    if case("replaygain_album_gain"):
                        info_["replay_gain"]["album"]["adjustment"] = php_float(commentvalue_[0])
                        info_["ogg"]["comments"][index_] = None
                        break
                    # end if
                    if case("rg_radio"):
                        pass
                    # end if
                    if case("replaygain_track_gain"):
                        info_["replay_gain"]["track"]["adjustment"] = php_float(commentvalue_[0])
                        info_["ogg"]["comments"][index_] = None
                        break
                    # end if
                    if case("replaygain_album_peak"):
                        info_["replay_gain"]["album"]["peak"] = php_float(commentvalue_[0])
                        info_["ogg"]["comments"][index_] = None
                        break
                    # end if
                    if case("rg_peak"):
                        pass
                    # end if
                    if case("replaygain_track_peak"):
                        info_["replay_gain"]["track"]["peak"] = php_float(commentvalue_[0])
                        info_["ogg"]["comments"][index_] = None
                        break
                    # end if
                    if case("replaygain_reference_loudness"):
                        info_["replay_gain"]["reference_volume"] = php_float(commentvalue_[0])
                        info_["ogg"]["comments"][index_] = None
                        break
                    # end if
                    if case():
                        break
                    # end if
                # end for
            # end for
        # end if
        self.fseek(OriginalOffset_)
        return True
    # end def parsevorbiscomments
    #// 
    #// @param int $mode
    #// 
    #// @return string|null
    #//
    @classmethod
    def speexbandmodelookup(self, mode_=None):
        
        
        SpeexBandModeLookup_ = Array()
        if php_empty(lambda : SpeexBandModeLookup_):
            SpeexBandModeLookup_[0] = "narrow"
            SpeexBandModeLookup_[1] = "wide"
            SpeexBandModeLookup_[2] = "ultra-wide"
        # end if
        return SpeexBandModeLookup_[mode_] if (php_isset(lambda : SpeexBandModeLookup_[mode_])) else None
    # end def speexbandmodelookup
    #// 
    #// @param array $OggInfoArray
    #// @param int   $SegmentNumber
    #// 
    #// @return int
    #//
    @classmethod
    def oggpagesegmentlength(self, OggInfoArray_=None, SegmentNumber_=1):
        
        
        segmentlength_ = 0
        i_ = 0
        while i_ < SegmentNumber_:
            
            segmentlength_ = 0
            for key_,value_ in OggInfoArray_["segment_table"]:
                segmentlength_ += value_
                if value_ < 255:
                    break
                # end if
            # end for
            i_ += 1
        # end while
        return segmentlength_
    # end def oggpagesegmentlength
    #// 
    #// @param int $nominal_bitrate
    #// 
    #// @return float
    #//
    @classmethod
    def get_quality_from_nominal_bitrate(self, nominal_bitrate_=None):
        
        
        #// decrease precision
        nominal_bitrate_ = nominal_bitrate_ / 1000
        if nominal_bitrate_ < 128:
            #// q-1 to q4
            qval_ = nominal_bitrate_ - 64 / 16
        elif nominal_bitrate_ < 256:
            #// q4 to q8
            qval_ = nominal_bitrate_ / 32
        elif nominal_bitrate_ < 320:
            #// q8 to q9
            qval_ = nominal_bitrate_ + 256 / 64
        else:
            #// q9 to q10
            qval_ = nominal_bitrate_ + 1300 / 180
        # end if
        #// return $qval; // 5.031324
        #// return intval($qval); // 5
        return round(qval_, 1)
        pass
    # end def get_quality_from_nominal_bitrate
    #// 
    #// @param int $colorspace_id
    #// 
    #// @return string|null
    #//
    @classmethod
    def theoracolorspace(self, colorspace_id_=None):
        
        
        TheoraColorSpaceLookup_ = Array()
        if php_empty(lambda : TheoraColorSpaceLookup_):
            TheoraColorSpaceLookup_[0] = "Undefined"
            TheoraColorSpaceLookup_[1] = "Rec. 470M"
            TheoraColorSpaceLookup_[2] = "Rec. 470BG"
            TheoraColorSpaceLookup_[3] = "Reserved"
        # end if
        return TheoraColorSpaceLookup_[colorspace_id_] if (php_isset(lambda : TheoraColorSpaceLookup_[colorspace_id_])) else None
    # end def theoracolorspace
    #// 
    #// @param int $pixelformat_id
    #// 
    #// @return string|null
    #//
    @classmethod
    def theorapixelformat(self, pixelformat_id_=None):
        
        
        TheoraPixelFormatLookup_ = Array()
        if php_empty(lambda : TheoraPixelFormatLookup_):
            TheoraPixelFormatLookup_[0] = "4:2:0"
            TheoraPixelFormatLookup_[1] = "Reserved"
            TheoraPixelFormatLookup_[2] = "4:2:2"
            TheoraPixelFormatLookup_[3] = "4:4:4"
        # end if
        return TheoraPixelFormatLookup_[pixelformat_id_] if (php_isset(lambda : TheoraPixelFormatLookup_[pixelformat_id_])) else None
    # end def theorapixelformat
# end class getid3_ogg
