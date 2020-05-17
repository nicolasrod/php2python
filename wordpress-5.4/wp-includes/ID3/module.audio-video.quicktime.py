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
#// module.audio-video.quicktime.php
#// module for analyzing Quicktime and MP3-in-MP4 files
#// dependencies: module.audio.mp3.php
#// dependencies: module.tag.id3v2.php
#// 
#//
getid3_lib.includedependency(GETID3_INCLUDEPATH + "module.audio.mp3.php", __FILE__, True)
getid3_lib.includedependency(GETID3_INCLUDEPATH + "module.tag.id3v2.php", __FILE__, True)
#// needed for ISO 639-2 language code lookup
class getid3_quicktime(getid3_handler):
    ReturnAtomData = True
    ParseAllPossibleAtoms = False
    #// 
    #// @return bool
    #//
    def analyze(self):
        
        
        info_ = self.getid3.info
        info_["fileformat"] = "quicktime"
        info_["quicktime"]["hinting"] = False
        info_["quicktime"]["controller"] = "standard"
        #// may be overridden if 'ctyp' atom is present
        self.fseek(info_["avdataoffset"])
        offset_ = 0
        atomcounter_ = 0
        atom_data_read_buffer_size_ = round(info_["php_memory_limit"] / 4) if info_["php_memory_limit"] else self.getid3.option_fread_buffer_size * 1024
        #// set read buffer to 25% of PHP memory limit (if one is specified), otherwise use option_fread_buffer_size [default: 32MB]
        while True:
            
            if not (offset_ < info_["avdataend"]):
                break
            # end if
            if (not getid3_lib.intvaluesupported(offset_)):
                self.error("Unable to parse atom at offset " + offset_ + " because beyond " + round(PHP_INT_MAX / 1073741824) + "GB limit of PHP filesystem functions")
                break
            # end if
            self.fseek(offset_)
            AtomHeader_ = self.fread(8)
            atomsize_ = getid3_lib.bigendian2int(php_substr(AtomHeader_, 0, 4))
            atomname_ = php_substr(AtomHeader_, 4, 4)
            #// 64-bit MOV patch by jlegateØktnc*com
            if atomsize_ == 1:
                atomsize_ = getid3_lib.bigendian2int(self.fread(8))
            # end if
            info_["quicktime"][atomname_]["name"] = atomname_
            info_["quicktime"][atomname_]["size"] = atomsize_
            info_["quicktime"][atomname_]["offset"] = offset_
            if offset_ + atomsize_ > info_["avdataend"]:
                self.error("Atom at offset " + offset_ + " claims to go beyond end-of-file (length: " + atomsize_ + " bytes)")
                return False
            # end if
            if atomsize_ == 0:
                break
            # end if
            atomHierarchy_ = Array()
            info_["quicktime"][atomname_] = self.quicktimeparseatom(atomname_, atomsize_, self.fread(php_min(atomsize_, atom_data_read_buffer_size_)), offset_, atomHierarchy_, self.ParseAllPossibleAtoms)
            offset_ += atomsize_
            atomcounter_ += 1
        # end while
        if (not php_empty(lambda : info_["avdataend_tmp"])):
            #// this value is assigned to a temp value and then erased because
            #// otherwise any atoms beyond the 'mdat' atom would not get parsed
            info_["avdataend"] = info_["avdataend_tmp"]
            info_["avdataend_tmp"] = None
        # end if
        if (not php_empty(lambda : info_["quicktime"]["comments"]["chapters"])) and php_is_array(info_["quicktime"]["comments"]["chapters"]) and php_count(info_["quicktime"]["comments"]["chapters"]) > 0:
            durations_ = self.quicktime_time_to_sample_table(info_)
            i_ = 0
            while i_ < php_count(info_["quicktime"]["comments"]["chapters"]):
                
                bookmark_ = Array()
                bookmark_["title"] = info_["quicktime"]["comments"]["chapters"][i_]
                if (php_isset(lambda : durations_[i_])):
                    bookmark_["duration_sample"] = durations_[i_]["sample_duration"]
                    if i_ > 0:
                        bookmark_["start_sample"] = info_["quicktime"]["bookmarks"][i_ - 1]["start_sample"] + info_["quicktime"]["bookmarks"][i_ - 1]["duration_sample"]
                    else:
                        bookmark_["start_sample"] = 0
                    # end if
                    time_scale_ = self.quicktime_bookmark_time_scale(info_)
                    if time_scale_:
                        bookmark_["duration_seconds"] = bookmark_["duration_sample"] / time_scale_
                        bookmark_["start_seconds"] = bookmark_["start_sample"] / time_scale_
                    # end if
                # end if
                info_["quicktime"]["bookmarks"][-1] = bookmark_
                i_ += 1
            # end while
        # end if
        if (php_isset(lambda : info_["quicktime"]["temp_meta_key_names"])):
            info_["quicktime"]["temp_meta_key_names"] = None
        # end if
        if (not php_empty(lambda : info_["quicktime"]["comments"]["location.ISO6709"])):
            #// https://en.wikipedia.org/wiki/ISO_6709
            for ISO6709string_ in info_["quicktime"]["comments"]["location.ISO6709"]:
                latitude_ = False
                longitude_ = False
                altitude_ = False
                if php_preg_match("#^([\\+\\-])([0-9]{2}|[0-9]{4}|[0-9]{6})(\\.[0-9]+)?([\\+\\-])([0-9]{3}|[0-9]{5}|[0-9]{7})(\\.[0-9]+)?(([\\+\\-])([0-9]{3}|[0-9]{5}|[0-9]{7})(\\.[0-9]+)?)?/$#", ISO6709string_, matches_):
                    php_no_error(lambda: dummy_, lat_sign_, lat_deg_, lat_deg_dec_, lon_sign_, lon_deg_, lon_deg_dec_, dummy_, alt_sign_, alt_deg_, alt_deg_dec_ = matches_)
                    if php_strlen(lat_deg_) == 2:
                        #// [+-]DD.D
                        latitude_ = floatval(php_ltrim(lat_deg_, "0") + lat_deg_dec_)
                    elif php_strlen(lat_deg_) == 4:
                        #// [+-]DDMM.M
                        latitude_ = floatval(php_ltrim(php_substr(lat_deg_, 0, 2), "0")) + floatval(php_ltrim(php_substr(lat_deg_, 2, 2), "0") + lat_deg_dec_ / 60)
                    elif php_strlen(lat_deg_) == 6:
                        #// [+-]DDMMSS.S
                        latitude_ = floatval(php_ltrim(php_substr(lat_deg_, 0, 2), "0")) + floatval(php_ltrim(php_substr(lat_deg_, 2, 2), "0") / 60) + floatval(php_ltrim(php_substr(lat_deg_, 4, 2), "0") + lat_deg_dec_ / 3600)
                    # end if
                    if php_strlen(lon_deg_) == 3:
                        #// [+-]DDD.D
                        longitude_ = floatval(php_ltrim(lon_deg_, "0") + lon_deg_dec_)
                    elif php_strlen(lon_deg_) == 5:
                        #// [+-]DDDMM.M
                        longitude_ = floatval(php_ltrim(php_substr(lon_deg_, 0, 2), "0")) + floatval(php_ltrim(php_substr(lon_deg_, 2, 2), "0") + lon_deg_dec_ / 60)
                    elif php_strlen(lon_deg_) == 7:
                        #// [+-]DDDMMSS.S
                        longitude_ = floatval(php_ltrim(php_substr(lon_deg_, 0, 2), "0")) + floatval(php_ltrim(php_substr(lon_deg_, 2, 2), "0") / 60) + floatval(php_ltrim(php_substr(lon_deg_, 4, 2), "0") + lon_deg_dec_ / 3600)
                    # end if
                    if php_strlen(alt_deg_) == 3:
                        #// [+-]DDD.D
                        altitude_ = floatval(php_ltrim(alt_deg_, "0") + alt_deg_dec_)
                    elif php_strlen(alt_deg_) == 5:
                        #// [+-]DDDMM.M
                        altitude_ = floatval(php_ltrim(php_substr(alt_deg_, 0, 2), "0")) + floatval(php_ltrim(php_substr(alt_deg_, 2, 2), "0") + alt_deg_dec_ / 60)
                    elif php_strlen(alt_deg_) == 7:
                        #// [+-]DDDMMSS.S
                        altitude_ = floatval(php_ltrim(php_substr(alt_deg_, 0, 2), "0")) + floatval(php_ltrim(php_substr(alt_deg_, 2, 2), "0") / 60) + floatval(php_ltrim(php_substr(alt_deg_, 4, 2), "0") + alt_deg_dec_ / 3600)
                    # end if
                    if latitude_ != False:
                        info_["quicktime"]["comments"]["gps_latitude"][-1] = -1 if lat_sign_ == "-" else 1 * floatval(latitude_)
                    # end if
                    if longitude_ != False:
                        info_["quicktime"]["comments"]["gps_longitude"][-1] = -1 if lon_sign_ == "-" else 1 * floatval(longitude_)
                    # end if
                    if altitude_ != False:
                        info_["quicktime"]["comments"]["gps_altitude"][-1] = -1 if alt_sign_ == "-" else 1 * floatval(altitude_)
                    # end if
                # end if
                if latitude_ == False:
                    self.warning("location.ISO6709 string not parsed correctly: \"" + ISO6709string_ + "\", please submit as a bug")
                # end if
                break
            # end for
        # end if
        if (not (php_isset(lambda : info_["bitrate"]))) and (php_isset(lambda : info_["playtime_seconds"])):
            info_["bitrate"] = info_["avdataend"] - info_["avdataoffset"] * 8 / info_["playtime_seconds"]
        # end if
        if (php_isset(lambda : info_["bitrate"])) and (not (php_isset(lambda : info_["audio"]["bitrate"]))) and (not (php_isset(lambda : info_["quicktime"]["video"]))):
            info_["audio"]["bitrate"] = info_["bitrate"]
        # end if
        if (not php_empty(lambda : info_["bitrate"])) and (not php_empty(lambda : info_["audio"]["bitrate"])) and php_empty(lambda : info_["video"]["bitrate"]) and (not php_empty(lambda : info_["video"]["frame_rate"])) and (not php_empty(lambda : info_["video"]["resolution_x"])) and info_["bitrate"] > info_["audio"]["bitrate"]:
            info_["video"]["bitrate"] = info_["bitrate"] - info_["audio"]["bitrate"]
        # end if
        if (not php_empty(lambda : info_["playtime_seconds"])) and (not (php_isset(lambda : info_["video"]["frame_rate"]))) and (not php_empty(lambda : info_["quicktime"]["stts_framecount"])):
            for key_,samples_count_ in info_["quicktime"]["stts_framecount"]:
                samples_per_second_ = samples_count_ / info_["playtime_seconds"]
                if samples_per_second_ > 240:
                    pass
                else:
                    info_["video"]["frame_rate"] = samples_per_second_
                    break
                # end if
            # end for
        # end if
        if info_["audio"]["dataformat"] == "mp4":
            info_["fileformat"] = "mp4"
            if php_empty(lambda : info_["video"]["resolution_x"]):
                info_["mime_type"] = "audio/mp4"
                info_["video"]["dataformat"] = None
            else:
                info_["mime_type"] = "video/mp4"
            # end if
        # end if
        if (not self.ReturnAtomData):
            info_["quicktime"]["moov"] = None
        # end if
        if php_empty(lambda : info_["audio"]["dataformat"]) and (not php_empty(lambda : info_["quicktime"]["audio"])):
            info_["audio"]["dataformat"] = "quicktime"
        # end if
        if php_empty(lambda : info_["video"]["dataformat"]) and (not php_empty(lambda : info_["quicktime"]["video"])):
            info_["video"]["dataformat"] = "quicktime"
        # end if
        if (php_isset(lambda : info_["video"])) and info_["mime_type"] == "audio/mp4" and php_empty(lambda : info_["video"]["resolution_x"]) and php_empty(lambda : info_["video"]["resolution_y"]):
            info_["video"] = None
        # end if
        return True
    # end def analyze
    #// 
    #// @param string $atomname
    #// @param int    $atomsize
    #// @param string $atom_data
    #// @param int    $baseoffset
    #// @param array  $atomHierarchy
    #// @param bool   $ParseAllPossibleAtoms
    #// 
    #// @return array|false
    #//
    def quicktimeparseatom(self, atomname_=None, atomsize_=None, atom_data_=None, baseoffset_=None, atomHierarchy_=None, ParseAllPossibleAtoms_=None):
        
        
        #// http://developer.apple.com/techpubs/quicktime/qtdevdocs/APIREF/INDEX/atomalphaindex.htm
        #// https://code.google.com/p/mp4v2/wiki/iTunesMetadata
        info_ = self.getid3.info
        atom_parent_ = php_end(atomHierarchy_)
        #// not array_pop($atomHierarchy); see https://www.getid3.org/phpBB3/viewtopic.php?t=1717
        php_array_push(atomHierarchy_, atomname_)
        atom_structure_["hierarchy"] = php_implode(" ", atomHierarchy_)
        atom_structure_["name"] = atomname_
        atom_structure_["size"] = atomsize_
        atom_structure_["offset"] = baseoffset_
        if php_substr(atomname_, 0, 3) == "   ":
            #// https://github.com/JamesHeinrich/getID3/issues/139
            atomname_ = getid3_lib.bigendian2int(atomname_)
            atom_structure_["name"] = atomname_
            atom_structure_["subatoms"] = self.quicktimeparsecontaineratom(atom_data_, baseoffset_ + 8, atomHierarchy_, ParseAllPossibleAtoms_)
        else:
            for case in Switch(atomname_):
                if case("moov"):
                    pass
                # end if
                if case("trak"):
                    pass
                # end if
                if case("clip"):
                    pass
                # end if
                if case("matt"):
                    pass
                # end if
                if case("edts"):
                    pass
                # end if
                if case("tref"):
                    pass
                # end if
                if case("mdia"):
                    pass
                # end if
                if case("minf"):
                    pass
                # end if
                if case("dinf"):
                    pass
                # end if
                if case("udta"):
                    pass
                # end if
                if case("cmov"):
                    pass
                # end if
                if case("rmra"):
                    pass
                # end if
                if case("rmda"):
                    pass
                # end if
                if case("gmhd"):
                    #// Generic Media info HeaDer atom (seen on QTVR)
                    atom_structure_["subatoms"] = self.quicktimeparsecontaineratom(atom_data_, baseoffset_ + 8, atomHierarchy_, ParseAllPossibleAtoms_)
                    break
                # end if
                if case("ilst"):
                    #// Item LiST container atom
                    atom_structure_["subatoms"] = self.quicktimeparsecontaineratom(atom_data_, baseoffset_ + 8, atomHierarchy_, ParseAllPossibleAtoms_)
                    if atom_structure_["subatoms"]:
                        #// some "ilst" atoms contain data atoms that have a numeric name, and the data is far more accessible if the returned array is compacted
                        allnumericnames_ = True
                        for subatomarray_ in atom_structure_["subatoms"]:
                            if (not is_integer(subatomarray_["name"])) or php_count(subatomarray_["subatoms"]) != 1:
                                allnumericnames_ = False
                                break
                            # end if
                        # end for
                        if allnumericnames_:
                            newData_ = Array()
                            for subatomarray_ in atom_structure_["subatoms"]:
                                for newData_subatomarray_ in subatomarray_["subatoms"]:
                                    newData_subatomarray_["hierarchy"] = None
                                    newData_subatomarray_["name"] = None
                                    newData_[subatomarray_["name"]] = newData_subatomarray_
                                    break
                                # end for
                            # end for
                            atom_structure_["data"] = newData_
                            atom_structure_["subatoms"] = None
                        # end if
                    # end if
                    break
                # end if
                if case("stbl"):
                    #// Sample TaBLe container atom
                    atom_structure_["subatoms"] = self.quicktimeparsecontaineratom(atom_data_, baseoffset_ + 8, atomHierarchy_, ParseAllPossibleAtoms_)
                    isVideo_ = False
                    framerate_ = 0
                    framecount_ = 0
                    for key_,value_array_ in atom_structure_["subatoms"]:
                        if (php_isset(lambda : value_array_["sample_description_table"])):
                            for key2_,value_array2_ in value_array_["sample_description_table"]:
                                if (php_isset(lambda : value_array2_["data_format"])):
                                    for case in Switch(value_array2_["data_format"]):
                                        if case("avc1"):
                                            pass
                                        # end if
                                        if case("mp4v"):
                                            #// video data
                                            isVideo_ = True
                                            break
                                        # end if
                                        if case("mp4a"):
                                            break
                                        # end if
                                    # end for
                                # end if
                            # end for
                        elif (php_isset(lambda : value_array_["time_to_sample_table"])):
                            for key2_,value_array2_ in value_array_["time_to_sample_table"]:
                                if (php_isset(lambda : value_array2_["sample_count"])) and (php_isset(lambda : value_array2_["sample_duration"])) and value_array2_["sample_duration"] > 0:
                                    framerate_ = round(info_["quicktime"]["time_scale"] / value_array2_["sample_duration"], 3)
                                    framecount_ = value_array2_["sample_count"]
                                # end if
                            # end for
                        # end if
                    # end for
                    if isVideo_ and framerate_:
                        info_["quicktime"]["video"]["frame_rate"] = framerate_
                        info_["video"]["frame_rate"] = info_["quicktime"]["video"]["frame_rate"]
                    # end if
                    if isVideo_ and framecount_:
                        info_["quicktime"]["video"]["frame_count"] = framecount_
                    # end if
                    break
                # end if
                if case("©" + "alb"):
                    pass
                # end if
                if case("©" + "ART"):
                    pass
                # end if
                if case("©" + "art"):
                    pass
                # end if
                if case("©" + "aut"):
                    pass
                # end if
                if case("©" + "cmt"):
                    pass
                # end if
                if case("©" + "com"):
                    pass
                # end if
                if case("©" + "cpy"):
                    pass
                # end if
                if case("©" + "day"):
                    pass
                # end if
                if case("©" + "dir"):
                    pass
                # end if
                if case("©" + "ed1"):
                    pass
                # end if
                if case("©" + "ed2"):
                    pass
                # end if
                if case("©" + "ed3"):
                    pass
                # end if
                if case("©" + "ed4"):
                    pass
                # end if
                if case("©" + "ed5"):
                    pass
                # end if
                if case("©" + "ed6"):
                    pass
                # end if
                if case("©" + "ed7"):
                    pass
                # end if
                if case("©" + "ed8"):
                    pass
                # end if
                if case("©" + "ed9"):
                    pass
                # end if
                if case("©" + "enc"):
                    pass
                # end if
                if case("©" + "fmt"):
                    pass
                # end if
                if case("©" + "gen"):
                    pass
                # end if
                if case("©" + "grp"):
                    pass
                # end if
                if case("©" + "hst"):
                    pass
                # end if
                if case("©" + "inf"):
                    pass
                # end if
                if case("©" + "lyr"):
                    pass
                # end if
                if case("©" + "mak"):
                    pass
                # end if
                if case("©" + "mod"):
                    pass
                # end if
                if case("©" + "nam"):
                    pass
                # end if
                if case("©" + "ope"):
                    pass
                # end if
                if case("©" + "PRD"):
                    pass
                # end if
                if case("©" + "prf"):
                    pass
                # end if
                if case("©" + "req"):
                    pass
                # end if
                if case("©" + "src"):
                    pass
                # end if
                if case("©" + "swr"):
                    pass
                # end if
                if case("©" + "too"):
                    pass
                # end if
                if case("©" + "trk"):
                    pass
                # end if
                if case("©" + "url"):
                    pass
                # end if
                if case("©" + "wrn"):
                    pass
                # end if
                if case("©" + "wrt"):
                    pass
                # end if
                if case("----"):
                    pass
                # end if
                if case("aART"):
                    pass
                # end if
                if case("akID"):
                    pass
                # end if
                if case("apID"):
                    pass
                # end if
                if case("atID"):
                    pass
                # end if
                if case("catg"):
                    pass
                # end if
                if case("cmID"):
                    pass
                # end if
                if case("cnID"):
                    pass
                # end if
                if case("covr"):
                    pass
                # end if
                if case("cpil"):
                    pass
                # end if
                if case("cprt"):
                    pass
                # end if
                if case("desc"):
                    pass
                # end if
                if case("disk"):
                    pass
                # end if
                if case("egid"):
                    pass
                # end if
                if case("geID"):
                    pass
                # end if
                if case("gnre"):
                    pass
                # end if
                if case("hdvd"):
                    pass
                # end if
                if case("keyw"):
                    pass
                # end if
                if case("ldes"):
                    pass
                # end if
                if case("pcst"):
                    pass
                # end if
                if case("pgap"):
                    pass
                # end if
                if case("plID"):
                    pass
                # end if
                if case("purd"):
                    pass
                # end if
                if case("purl"):
                    pass
                # end if
                if case("rati"):
                    pass
                # end if
                if case("rndu"):
                    pass
                # end if
                if case("rpdu"):
                    pass
                # end if
                if case("rtng"):
                    pass
                # end if
                if case("sfID"):
                    pass
                # end if
                if case("soaa"):
                    pass
                # end if
                if case("soal"):
                    pass
                # end if
                if case("soar"):
                    pass
                # end if
                if case("soco"):
                    pass
                # end if
                if case("sonm"):
                    pass
                # end if
                if case("sosn"):
                    pass
                # end if
                if case("stik"):
                    pass
                # end if
                if case("tmpo"):
                    pass
                # end if
                if case("trkn"):
                    pass
                # end if
                if case("tven"):
                    pass
                # end if
                if case("tves"):
                    pass
                # end if
                if case("tvnn"):
                    pass
                # end if
                if case("tvsh"):
                    pass
                # end if
                if case("tvsn"):
                    #// TV SeasoN
                    if atom_parent_ == "udta":
                        #// User data atom handler
                        atom_structure_["data_length"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 2))
                        atom_structure_["language_id"] = getid3_lib.bigendian2int(php_substr(atom_data_, 2, 2))
                        atom_structure_["data"] = php_substr(atom_data_, 4)
                        atom_structure_["language"] = self.quicktimelanguagelookup(atom_structure_["language_id"])
                        if php_empty(lambda : info_["comments"]["language"]) or (not php_in_array(atom_structure_["language"], info_["comments"]["language"])):
                            info_["comments"]["language"][-1] = atom_structure_["language"]
                        # end if
                    else:
                        #// Apple item list box atom handler
                        atomoffset_ = 0
                        if php_substr(atom_data_, 2, 2) == "µ":
                            #// not sure what it means, but observed on iPhone4 data.
                            #// Each $atom_data has 2 bytes of datasize, plus 0x10B5, then data
                            while True:
                                
                                if not (atomoffset_ < php_strlen(atom_data_)):
                                    break
                                # end if
                                boxsmallsize_ = getid3_lib.bigendian2int(php_substr(atom_data_, atomoffset_, 2))
                                boxsmalltype_ = php_substr(atom_data_, atomoffset_ + 2, 2)
                                boxsmalldata_ = php_substr(atom_data_, atomoffset_ + 4, boxsmallsize_)
                                if boxsmallsize_ <= 1:
                                    self.warning("Invalid QuickTime atom smallbox size \"" + boxsmallsize_ + "\" in atom \"" + php_preg_replace("#[^a-zA-Z0-9 _\\-]#", "?", atomname_) + "\" at offset: " + atom_structure_["offset"] + atomoffset_)
                                    atom_structure_["data"] = None
                                    atomoffset_ = php_strlen(atom_data_)
                                    break
                                # end if
                                for case in Switch(boxsmalltype_):
                                    if case("µ"):
                                        atom_structure_["data"] = boxsmalldata_
                                        break
                                    # end if
                                    if case():
                                        self.warning("Unknown QuickTime smallbox type: \"" + php_preg_replace("#[^a-zA-Z0-9 _\\-]#", "?", boxsmalltype_) + "\" (" + php_trim(getid3_lib.printhexbytes(boxsmalltype_)) + ") at offset " + baseoffset_)
                                        atom_structure_["data"] = atom_data_
                                        break
                                    # end if
                                # end for
                                atomoffset_ += 4 + boxsmallsize_
                            # end while
                        else:
                            while True:
                                
                                if not (atomoffset_ < php_strlen(atom_data_)):
                                    break
                                # end if
                                boxsize_ = getid3_lib.bigendian2int(php_substr(atom_data_, atomoffset_, 4))
                                boxtype_ = php_substr(atom_data_, atomoffset_ + 4, 4)
                                boxdata_ = php_substr(atom_data_, atomoffset_ + 8, boxsize_ - 8)
                                if boxsize_ <= 1:
                                    self.warning("Invalid QuickTime atom box size \"" + boxsize_ + "\" in atom \"" + php_preg_replace("#[^a-zA-Z0-9 _\\-]#", "?", atomname_) + "\" at offset: " + atom_structure_["offset"] + atomoffset_)
                                    atom_structure_["data"] = None
                                    atomoffset_ = php_strlen(atom_data_)
                                    break
                                # end if
                                atomoffset_ += boxsize_
                                for case in Switch(boxtype_):
                                    if case("mean"):
                                        pass
                                    # end if
                                    if case("name"):
                                        atom_structure_[boxtype_] = php_substr(boxdata_, 4)
                                        break
                                    # end if
                                    if case("data"):
                                        atom_structure_["version"] = getid3_lib.bigendian2int(php_substr(boxdata_, 0, 1))
                                        atom_structure_["flags_raw"] = getid3_lib.bigendian2int(php_substr(boxdata_, 1, 3))
                                        for case in Switch(atom_structure_["flags_raw"]):
                                            if case(0):
                                                pass
                                            # end if
                                            if case(21):
                                                #// tmpo/cpil flag
                                                for case in Switch(atomname_):
                                                    if case("cpil"):
                                                        pass
                                                    # end if
                                                    if case("hdvd"):
                                                        pass
                                                    # end if
                                                    if case("pcst"):
                                                        pass
                                                    # end if
                                                    if case("pgap"):
                                                        #// 8-bit integer (boolean)
                                                        atom_structure_["data"] = getid3_lib.bigendian2int(php_substr(boxdata_, 8, 1))
                                                        break
                                                    # end if
                                                    if case("tmpo"):
                                                        #// 16-bit integer
                                                        atom_structure_["data"] = getid3_lib.bigendian2int(php_substr(boxdata_, 8, 2))
                                                        break
                                                    # end if
                                                    if case("disk"):
                                                        pass
                                                    # end if
                                                    if case("trkn"):
                                                        #// binary
                                                        num_ = getid3_lib.bigendian2int(php_substr(boxdata_, 10, 2))
                                                        num_total_ = getid3_lib.bigendian2int(php_substr(boxdata_, 12, 2))
                                                        atom_structure_["data"] = "" if php_empty(lambda : num_) else num_
                                                        atom_structure_["data"] += "" if php_empty(lambda : num_total_) else "/" + num_total_
                                                        break
                                                    # end if
                                                    if case("gnre"):
                                                        #// enum
                                                        GenreID_ = getid3_lib.bigendian2int(php_substr(boxdata_, 8, 4))
                                                        atom_structure_["data"] = getid3_id3v1.lookupgenrename(GenreID_ - 1)
                                                        break
                                                    # end if
                                                    if case("rtng"):
                                                        #// 8-bit integer
                                                        atom_structure_[atomname_] = getid3_lib.bigendian2int(php_substr(boxdata_, 8, 1))
                                                        atom_structure_["data"] = self.quicktimecontentratinglookup(atom_structure_[atomname_])
                                                        break
                                                    # end if
                                                    if case("stik"):
                                                        #// 8-bit integer (enum)
                                                        atom_structure_[atomname_] = getid3_lib.bigendian2int(php_substr(boxdata_, 8, 1))
                                                        atom_structure_["data"] = self.quicktimestiklookup(atom_structure_[atomname_])
                                                        break
                                                    # end if
                                                    if case("sfID"):
                                                        #// 32-bit integer
                                                        atom_structure_[atomname_] = getid3_lib.bigendian2int(php_substr(boxdata_, 8, 4))
                                                        atom_structure_["data"] = self.quicktimestorefrontcodelookup(atom_structure_[atomname_])
                                                        break
                                                    # end if
                                                    if case("egid"):
                                                        pass
                                                    # end if
                                                    if case("purl"):
                                                        atom_structure_["data"] = php_substr(boxdata_, 8)
                                                        break
                                                    # end if
                                                    if case("plID"):
                                                        #// 64-bit integer
                                                        atom_structure_["data"] = getid3_lib.bigendian2int(php_substr(boxdata_, 8, 8))
                                                        break
                                                    # end if
                                                    if case("covr"):
                                                        atom_structure_["data"] = php_substr(boxdata_, 8)
                                                        #// not a foolproof check, but better than nothing
                                                        if php_preg_match("#^\\xFF\\xD8\\xFF#", atom_structure_["data"]):
                                                            atom_structure_["image_mime"] = "image/jpeg"
                                                        elif php_preg_match("#^\\x89\\x50\\x4E\\x47\\x0D\\x0A\\x1A\\x0A#", atom_structure_["data"]):
                                                            atom_structure_["image_mime"] = "image/png"
                                                        elif php_preg_match("#^GIF#", atom_structure_["data"]):
                                                            atom_structure_["image_mime"] = "image/gif"
                                                        # end if
                                                        break
                                                    # end if
                                                    if case("atID"):
                                                        pass
                                                    # end if
                                                    if case("cnID"):
                                                        pass
                                                    # end if
                                                    if case("geID"):
                                                        pass
                                                    # end if
                                                    if case("tves"):
                                                        pass
                                                    # end if
                                                    if case("tvsn"):
                                                        pass
                                                    # end if
                                                    if case():
                                                        #// 32-bit integer
                                                        atom_structure_["data"] = getid3_lib.bigendian2int(php_substr(boxdata_, 8, 4))
                                                    # end if
                                                # end for
                                                break
                                            # end if
                                            if case(1):
                                                pass
                                            # end if
                                            if case(13):
                                                pass
                                            # end if
                                            if case():
                                                atom_structure_["data"] = php_substr(boxdata_, 8)
                                                if atomname_ == "covr":
                                                    #// not a foolproof check, but better than nothing
                                                    if php_preg_match("#^\\xFF\\xD8\\xFF#", atom_structure_["data"]):
                                                        atom_structure_["image_mime"] = "image/jpeg"
                                                    elif php_preg_match("#^\\x89\\x50\\x4E\\x47\\x0D\\x0A\\x1A\\x0A#", atom_structure_["data"]):
                                                        atom_structure_["image_mime"] = "image/png"
                                                    elif php_preg_match("#^GIF#", atom_structure_["data"]):
                                                        atom_structure_["image_mime"] = "image/gif"
                                                    # end if
                                                # end if
                                                break
                                            # end if
                                        # end for
                                        break
                                    # end if
                                    if case():
                                        self.warning("Unknown QuickTime box type: \"" + php_preg_replace("#[^a-zA-Z0-9 _\\-]#", "?", boxtype_) + "\" (" + php_trim(getid3_lib.printhexbytes(boxtype_)) + ") at offset " + baseoffset_)
                                        atom_structure_["data"] = atom_data_
                                    # end if
                                # end for
                            # end while
                        # end if
                    # end if
                    self.copytoappropriatecommentssection(atomname_, atom_structure_["data"], atom_structure_["name"])
                    break
                # end if
                if case("play"):
                    #// auto-PLAY atom
                    atom_structure_["autoplay"] = php_bool(getid3_lib.bigendian2int(php_substr(atom_data_, 0, 1)))
                    info_["quicktime"]["autoplay"] = atom_structure_["autoplay"]
                    break
                # end if
                if case("WLOC"):
                    #// Window LOCation atom
                    atom_structure_["location_x"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 2))
                    atom_structure_["location_y"] = getid3_lib.bigendian2int(php_substr(atom_data_, 2, 2))
                    break
                # end if
                if case("LOOP"):
                    pass
                # end if
                if case("SelO"):
                    pass
                # end if
                if case("AllF"):
                    #// play ALL Frames atom
                    atom_structure_["data"] = getid3_lib.bigendian2int(atom_data_)
                    break
                # end if
                if case("name"):
                    pass
                # end if
                if case("MCPS"):
                    pass
                # end if
                if case("@PRM"):
                    pass
                # end if
                if case("@PRQ"):
                    #// adobe PRemiere Quicktime version
                    atom_structure_["data"] = atom_data_
                    break
                # end if
                if case("cmvd"):
                    #// Compressed MooV Data atom
                    #// Code by ubergeekØubergeek*tv based on information from
                    #// http://developer.apple.com/quicktime/icefloe/dispatch012.html
                    atom_structure_["unCompressedSize"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 4))
                    CompressedFileData_ = php_substr(atom_data_, 4)
                    UncompressedHeader_ = php_no_error(lambda: gzuncompress(CompressedFileData_))
                    if UncompressedHeader_:
                        atom_structure_["subatoms"] = self.quicktimeparsecontaineratom(UncompressedHeader_, 0, atomHierarchy_, ParseAllPossibleAtoms_)
                    else:
                        self.warning("Error decompressing compressed MOV atom at offset " + atom_structure_["offset"])
                    # end if
                    break
                # end if
                if case("dcom"):
                    #// Data COMpression atom
                    atom_structure_["compression_id"] = atom_data_
                    atom_structure_["compression_text"] = self.quicktimedcomlookup(atom_data_)
                    break
                # end if
                if case("rdrf"):
                    #// Reference movie Data ReFerence atom
                    atom_structure_["version"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 1))
                    atom_structure_["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data_, 1, 3))
                    atom_structure_["flags"]["internal_data"] = php_bool(atom_structure_["flags_raw"] & 1)
                    atom_structure_["reference_type_name"] = php_substr(atom_data_, 4, 4)
                    atom_structure_["reference_length"] = getid3_lib.bigendian2int(php_substr(atom_data_, 8, 4))
                    for case in Switch(atom_structure_["reference_type_name"]):
                        if case("url "):
                            atom_structure_["url"] = self.nonullstring(php_substr(atom_data_, 12))
                            break
                        # end if
                        if case("alis"):
                            atom_structure_["file_alias"] = php_substr(atom_data_, 12)
                            break
                        # end if
                        if case("rsrc"):
                            atom_structure_["resource_alias"] = php_substr(atom_data_, 12)
                            break
                        # end if
                        if case():
                            atom_structure_["data"] = php_substr(atom_data_, 12)
                            break
                        # end if
                    # end for
                    break
                # end if
                if case("rmqu"):
                    #// Reference Movie QUality atom
                    atom_structure_["movie_quality"] = getid3_lib.bigendian2int(atom_data_)
                    break
                # end if
                if case("rmcs"):
                    #// Reference Movie Cpu Speed atom
                    atom_structure_["version"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 1))
                    atom_structure_["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data_, 1, 3))
                    #// hardcoded: 0x0000
                    atom_structure_["cpu_speed_rating"] = getid3_lib.bigendian2int(php_substr(atom_data_, 4, 2))
                    break
                # end if
                if case("rmvc"):
                    #// Reference Movie Version Check atom
                    atom_structure_["version"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 1))
                    atom_structure_["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data_, 1, 3))
                    #// hardcoded: 0x0000
                    atom_structure_["gestalt_selector"] = php_substr(atom_data_, 4, 4)
                    atom_structure_["gestalt_value_mask"] = getid3_lib.bigendian2int(php_substr(atom_data_, 8, 4))
                    atom_structure_["gestalt_value"] = getid3_lib.bigendian2int(php_substr(atom_data_, 12, 4))
                    atom_structure_["gestalt_check_type"] = getid3_lib.bigendian2int(php_substr(atom_data_, 14, 2))
                    break
                # end if
                if case("rmcd"):
                    #// Reference Movie Component check atom
                    atom_structure_["version"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 1))
                    atom_structure_["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data_, 1, 3))
                    #// hardcoded: 0x0000
                    atom_structure_["component_type"] = php_substr(atom_data_, 4, 4)
                    atom_structure_["component_subtype"] = php_substr(atom_data_, 8, 4)
                    atom_structure_["component_manufacturer"] = php_substr(atom_data_, 12, 4)
                    atom_structure_["component_flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data_, 16, 4))
                    atom_structure_["component_flags_mask"] = getid3_lib.bigendian2int(php_substr(atom_data_, 20, 4))
                    atom_structure_["component_min_version"] = getid3_lib.bigendian2int(php_substr(atom_data_, 24, 4))
                    break
                # end if
                if case("rmdr"):
                    #// Reference Movie Data Rate atom
                    atom_structure_["version"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 1))
                    atom_structure_["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data_, 1, 3))
                    #// hardcoded: 0x0000
                    atom_structure_["data_rate"] = getid3_lib.bigendian2int(php_substr(atom_data_, 4, 4))
                    atom_structure_["data_rate_bps"] = atom_structure_["data_rate"] * 10
                    break
                # end if
                if case("rmla"):
                    #// Reference Movie Language Atom
                    atom_structure_["version"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 1))
                    atom_structure_["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data_, 1, 3))
                    #// hardcoded: 0x0000
                    atom_structure_["language_id"] = getid3_lib.bigendian2int(php_substr(atom_data_, 4, 2))
                    atom_structure_["language"] = self.quicktimelanguagelookup(atom_structure_["language_id"])
                    if php_empty(lambda : info_["comments"]["language"]) or (not php_in_array(atom_structure_["language"], info_["comments"]["language"])):
                        info_["comments"]["language"][-1] = atom_structure_["language"]
                    # end if
                    break
                # end if
                if case("ptv "):
                    #// Print To Video - defines a movie's full screen mode
                    #// http://developer.apple.com/documentation/QuickTime/APIREF/SOURCESIV/at_ptv-_pg.htm
                    atom_structure_["display_size_raw"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 2))
                    atom_structure_["reserved_1"] = getid3_lib.bigendian2int(php_substr(atom_data_, 2, 2))
                    #// hardcoded: 0x0000
                    atom_structure_["reserved_2"] = getid3_lib.bigendian2int(php_substr(atom_data_, 4, 2))
                    #// hardcoded: 0x0000
                    atom_structure_["slide_show_flag"] = getid3_lib.bigendian2int(php_substr(atom_data_, 6, 1))
                    atom_structure_["play_on_open_flag"] = getid3_lib.bigendian2int(php_substr(atom_data_, 7, 1))
                    atom_structure_["flags"]["play_on_open"] = php_bool(atom_structure_["play_on_open_flag"])
                    atom_structure_["flags"]["slide_show"] = php_bool(atom_structure_["slide_show_flag"])
                    ptv_lookup_[0] = "normal"
                    ptv_lookup_[1] = "double"
                    ptv_lookup_[2] = "half"
                    ptv_lookup_[3] = "full"
                    ptv_lookup_[4] = "current"
                    if (php_isset(lambda : ptv_lookup_[atom_structure_["display_size_raw"]])):
                        atom_structure_["display_size"] = ptv_lookup_[atom_structure_["display_size_raw"]]
                    else:
                        self.warning("unknown \"ptv \" display constant (" + atom_structure_["display_size_raw"] + ")")
                    # end if
                    break
                # end if
                if case("stsd"):
                    #// Sample Table Sample Description atom
                    atom_structure_["version"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 1))
                    atom_structure_["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data_, 1, 3))
                    #// hardcoded: 0x0000
                    atom_structure_["number_entries"] = getid3_lib.bigendian2int(php_substr(atom_data_, 4, 4))
                    #// see: https://github.com/JamesHeinrich/getID3/issues/111
                    #// Some corrupt files have been known to have high bits set in the number_entries field
                    #// This field shouldn't really need to be 32-bits, values stores are likely in the range 1-100000
                    #// Workaround: mask off the upper byte and throw a warning if it's nonzero
                    if atom_structure_["number_entries"] > 1048575:
                        if atom_structure_["number_entries"] > 16777215:
                            self.warning("\"stsd\" atom contains improbably large number_entries (0x" + getid3_lib.printhexbytes(php_substr(atom_data_, 4, 4), True, False) + " = " + atom_structure_["number_entries"] + "), probably in error. Ignoring upper byte and interpreting this as 0x" + getid3_lib.printhexbytes(php_substr(atom_data_, 5, 3), True, False) + " = " + atom_structure_["number_entries"] & 16777215)
                            atom_structure_["number_entries"] = atom_structure_["number_entries"] & 16777215
                        else:
                            self.warning("\"stsd\" atom contains improbably large number_entries (0x" + getid3_lib.printhexbytes(php_substr(atom_data_, 4, 4), True, False) + " = " + atom_structure_["number_entries"] + "), probably in error. Please report this to info@getid3.org referencing bug report #111")
                        # end if
                    # end if
                    stsdEntriesDataOffset_ = 8
                    i_ = 0
                    while i_ < atom_structure_["number_entries"]:
                        
                        atom_structure_["sample_description_table"][i_]["size"] = getid3_lib.bigendian2int(php_substr(atom_data_, stsdEntriesDataOffset_, 4))
                        stsdEntriesDataOffset_ += 4
                        atom_structure_["sample_description_table"][i_]["data_format"] = php_substr(atom_data_, stsdEntriesDataOffset_, 4)
                        stsdEntriesDataOffset_ += 4
                        atom_structure_["sample_description_table"][i_]["reserved"] = getid3_lib.bigendian2int(php_substr(atom_data_, stsdEntriesDataOffset_, 6))
                        stsdEntriesDataOffset_ += 6
                        atom_structure_["sample_description_table"][i_]["reference_index"] = getid3_lib.bigendian2int(php_substr(atom_data_, stsdEntriesDataOffset_, 2))
                        stsdEntriesDataOffset_ += 2
                        atom_structure_["sample_description_table"][i_]["data"] = php_substr(atom_data_, stsdEntriesDataOffset_, atom_structure_["sample_description_table"][i_]["size"] - 4 - 4 - 6 - 2)
                        stsdEntriesDataOffset_ += atom_structure_["sample_description_table"][i_]["size"] - 4 - 4 - 6 - 2
                        atom_structure_["sample_description_table"][i_]["encoder_version"] = getid3_lib.bigendian2int(php_substr(atom_structure_["sample_description_table"][i_]["data"], 0, 2))
                        atom_structure_["sample_description_table"][i_]["encoder_revision"] = getid3_lib.bigendian2int(php_substr(atom_structure_["sample_description_table"][i_]["data"], 2, 2))
                        atom_structure_["sample_description_table"][i_]["encoder_vendor"] = php_substr(atom_structure_["sample_description_table"][i_]["data"], 4, 4)
                        for case in Switch(atom_structure_["sample_description_table"][i_]["encoder_vendor"]):
                            if case("    "):
                                #// audio tracks
                                atom_structure_["sample_description_table"][i_]["audio_channels"] = getid3_lib.bigendian2int(php_substr(atom_structure_["sample_description_table"][i_]["data"], 8, 2))
                                atom_structure_["sample_description_table"][i_]["audio_bit_depth"] = getid3_lib.bigendian2int(php_substr(atom_structure_["sample_description_table"][i_]["data"], 10, 2))
                                atom_structure_["sample_description_table"][i_]["audio_compression_id"] = getid3_lib.bigendian2int(php_substr(atom_structure_["sample_description_table"][i_]["data"], 12, 2))
                                atom_structure_["sample_description_table"][i_]["audio_packet_size"] = getid3_lib.bigendian2int(php_substr(atom_structure_["sample_description_table"][i_]["data"], 14, 2))
                                atom_structure_["sample_description_table"][i_]["audio_sample_rate"] = getid3_lib.fixedpoint16_16(php_substr(atom_structure_["sample_description_table"][i_]["data"], 16, 4))
                                #// video tracks
                                #// http://developer.apple.com/library/mac/#documentation/QuickTime/QTFF/QTFFChap3/qtff3.html
                                atom_structure_["sample_description_table"][i_]["temporal_quality"] = getid3_lib.bigendian2int(php_substr(atom_structure_["sample_description_table"][i_]["data"], 8, 4))
                                atom_structure_["sample_description_table"][i_]["spatial_quality"] = getid3_lib.bigendian2int(php_substr(atom_structure_["sample_description_table"][i_]["data"], 12, 4))
                                atom_structure_["sample_description_table"][i_]["width"] = getid3_lib.bigendian2int(php_substr(atom_structure_["sample_description_table"][i_]["data"], 16, 2))
                                atom_structure_["sample_description_table"][i_]["height"] = getid3_lib.bigendian2int(php_substr(atom_structure_["sample_description_table"][i_]["data"], 18, 2))
                                atom_structure_["sample_description_table"][i_]["resolution_x"] = getid3_lib.fixedpoint16_16(php_substr(atom_structure_["sample_description_table"][i_]["data"], 24, 4))
                                atom_structure_["sample_description_table"][i_]["resolution_y"] = getid3_lib.fixedpoint16_16(php_substr(atom_structure_["sample_description_table"][i_]["data"], 28, 4))
                                atom_structure_["sample_description_table"][i_]["data_size"] = getid3_lib.bigendian2int(php_substr(atom_structure_["sample_description_table"][i_]["data"], 32, 4))
                                atom_structure_["sample_description_table"][i_]["frame_count"] = getid3_lib.bigendian2int(php_substr(atom_structure_["sample_description_table"][i_]["data"], 36, 2))
                                atom_structure_["sample_description_table"][i_]["compressor_name"] = php_substr(atom_structure_["sample_description_table"][i_]["data"], 38, 4)
                                atom_structure_["sample_description_table"][i_]["pixel_depth"] = getid3_lib.bigendian2int(php_substr(atom_structure_["sample_description_table"][i_]["data"], 42, 2))
                                atom_structure_["sample_description_table"][i_]["color_table_id"] = getid3_lib.bigendian2int(php_substr(atom_structure_["sample_description_table"][i_]["data"], 44, 2))
                                for case in Switch(atom_structure_["sample_description_table"][i_]["data_format"]):
                                    if case("2vuY"):
                                        pass
                                    # end if
                                    if case("avc1"):
                                        pass
                                    # end if
                                    if case("cvid"):
                                        pass
                                    # end if
                                    if case("dvc "):
                                        pass
                                    # end if
                                    if case("dvcp"):
                                        pass
                                    # end if
                                    if case("gif "):
                                        pass
                                    # end if
                                    if case("h263"):
                                        pass
                                    # end if
                                    if case("jpeg"):
                                        pass
                                    # end if
                                    if case("kpcd"):
                                        pass
                                    # end if
                                    if case("mjpa"):
                                        pass
                                    # end if
                                    if case("mjpb"):
                                        pass
                                    # end if
                                    if case("mp4v"):
                                        pass
                                    # end if
                                    if case("png "):
                                        pass
                                    # end if
                                    if case("raw "):
                                        pass
                                    # end if
                                    if case("rle "):
                                        pass
                                    # end if
                                    if case("rpza"):
                                        pass
                                    # end if
                                    if case("smc "):
                                        pass
                                    # end if
                                    if case("SVQ1"):
                                        pass
                                    # end if
                                    if case("SVQ3"):
                                        pass
                                    # end if
                                    if case("tiff"):
                                        pass
                                    # end if
                                    if case("v210"):
                                        pass
                                    # end if
                                    if case("v216"):
                                        pass
                                    # end if
                                    if case("v308"):
                                        pass
                                    # end if
                                    if case("v408"):
                                        pass
                                    # end if
                                    if case("v410"):
                                        pass
                                    # end if
                                    if case("yuv2"):
                                        info_["fileformat"] = "mp4"
                                        info_["video"]["fourcc"] = atom_structure_["sample_description_table"][i_]["data_format"]
                                        if self.quicktimevideocodeclookup(info_["video"]["fourcc"]):
                                            info_["video"]["fourcc_lookup"] = self.quicktimevideocodeclookup(info_["video"]["fourcc"])
                                        # end if
                                        #// https://www.getid3.org/phpBB3/viewtopic.php?t=1550
                                        #// if ((!empty($atom_structure['sample_description_table'][$i]['width']) && !empty($atom_structure['sample_description_table'][$i]['width'])) && (empty($info['video']['resolution_x']) || empty($info['video']['resolution_y']) || (number_format($info['video']['resolution_x'], 6) != number_format(round($info['video']['resolution_x']), 6)) || (number_format($info['video']['resolution_y'], 6) != number_format(round($info['video']['resolution_y']), 6)))) { // ugly check for floating point numbers
                                        if (not php_empty(lambda : atom_structure_["sample_description_table"][i_]["width"])) and (not php_empty(lambda : atom_structure_["sample_description_table"][i_]["height"])):
                                            #// assume that values stored here are more important than values stored in [tkhd] atom
                                            info_["video"]["resolution_x"] = atom_structure_["sample_description_table"][i_]["width"]
                                            info_["video"]["resolution_y"] = atom_structure_["sample_description_table"][i_]["height"]
                                            info_["quicktime"]["video"]["resolution_x"] = info_["video"]["resolution_x"]
                                            info_["quicktime"]["video"]["resolution_y"] = info_["video"]["resolution_y"]
                                        # end if
                                        break
                                    # end if
                                    if case("qtvr"):
                                        info_["video"]["dataformat"] = "quicktimevr"
                                        break
                                    # end if
                                    if case("mp4a"):
                                        pass
                                    # end if
                                    if case():
                                        info_["quicktime"]["audio"]["codec"] = self.quicktimeaudiocodeclookup(atom_structure_["sample_description_table"][i_]["data_format"])
                                        info_["quicktime"]["audio"]["sample_rate"] = atom_structure_["sample_description_table"][i_]["audio_sample_rate"]
                                        info_["quicktime"]["audio"]["channels"] = atom_structure_["sample_description_table"][i_]["audio_channels"]
                                        info_["quicktime"]["audio"]["bit_depth"] = atom_structure_["sample_description_table"][i_]["audio_bit_depth"]
                                        info_["audio"]["codec"] = info_["quicktime"]["audio"]["codec"]
                                        info_["audio"]["sample_rate"] = info_["quicktime"]["audio"]["sample_rate"]
                                        info_["audio"]["channels"] = info_["quicktime"]["audio"]["channels"]
                                        info_["audio"]["bits_per_sample"] = info_["quicktime"]["audio"]["bit_depth"]
                                        for case in Switch(atom_structure_["sample_description_table"][i_]["data_format"]):
                                            if case("raw "):
                                                pass
                                            # end if
                                            if case("alac"):
                                                pass
                                            # end if
                                            if case("sowt"):
                                                pass
                                            # end if
                                            if case("twos"):
                                                pass
                                            # end if
                                            if case("in24"):
                                                pass
                                            # end if
                                            if case("in32"):
                                                pass
                                            # end if
                                            if case("fl32"):
                                                pass
                                            # end if
                                            if case("fl64"):
                                                #// 64-bit Floating Point
                                                info_["audio"]["lossless"] = info_["quicktime"]["audio"]["lossless"]
                                                info_["audio"]["bitrate"] = info_["quicktime"]["audio"]["bitrate"]
                                                break
                                            # end if
                                            if case():
                                                info_["audio"]["lossless"] = False
                                                break
                                            # end if
                                        # end for
                                        break
                                    # end if
                                # end for
                                break
                            # end if
                            if case():
                                for case in Switch(atom_structure_["sample_description_table"][i_]["data_format"]):
                                    if case("mp4s"):
                                        info_["fileformat"] = "mp4"
                                        break
                                    # end if
                                    if case():
                                        #// video atom
                                        atom_structure_["sample_description_table"][i_]["video_temporal_quality"] = getid3_lib.bigendian2int(php_substr(atom_structure_["sample_description_table"][i_]["data"], 8, 4))
                                        atom_structure_["sample_description_table"][i_]["video_spatial_quality"] = getid3_lib.bigendian2int(php_substr(atom_structure_["sample_description_table"][i_]["data"], 12, 4))
                                        atom_structure_["sample_description_table"][i_]["video_frame_width"] = getid3_lib.bigendian2int(php_substr(atom_structure_["sample_description_table"][i_]["data"], 16, 2))
                                        atom_structure_["sample_description_table"][i_]["video_frame_height"] = getid3_lib.bigendian2int(php_substr(atom_structure_["sample_description_table"][i_]["data"], 18, 2))
                                        atom_structure_["sample_description_table"][i_]["video_resolution_x"] = getid3_lib.fixedpoint16_16(php_substr(atom_structure_["sample_description_table"][i_]["data"], 20, 4))
                                        atom_structure_["sample_description_table"][i_]["video_resolution_y"] = getid3_lib.fixedpoint16_16(php_substr(atom_structure_["sample_description_table"][i_]["data"], 24, 4))
                                        atom_structure_["sample_description_table"][i_]["video_data_size"] = getid3_lib.bigendian2int(php_substr(atom_structure_["sample_description_table"][i_]["data"], 28, 4))
                                        atom_structure_["sample_description_table"][i_]["video_frame_count"] = getid3_lib.bigendian2int(php_substr(atom_structure_["sample_description_table"][i_]["data"], 32, 2))
                                        atom_structure_["sample_description_table"][i_]["video_encoder_name_len"] = getid3_lib.bigendian2int(php_substr(atom_structure_["sample_description_table"][i_]["data"], 34, 1))
                                        atom_structure_["sample_description_table"][i_]["video_encoder_name"] = php_substr(atom_structure_["sample_description_table"][i_]["data"], 35, atom_structure_["sample_description_table"][i_]["video_encoder_name_len"])
                                        atom_structure_["sample_description_table"][i_]["video_pixel_color_depth"] = getid3_lib.bigendian2int(php_substr(atom_structure_["sample_description_table"][i_]["data"], 66, 2))
                                        atom_structure_["sample_description_table"][i_]["video_color_table_id"] = getid3_lib.bigendian2int(php_substr(atom_structure_["sample_description_table"][i_]["data"], 68, 2))
                                        atom_structure_["sample_description_table"][i_]["video_pixel_color_type"] = "grayscale" if atom_structure_["sample_description_table"][i_]["video_pixel_color_depth"] > 32 else "color"
                                        atom_structure_["sample_description_table"][i_]["video_pixel_color_name"] = self.quicktimecolornamelookup(atom_structure_["sample_description_table"][i_]["video_pixel_color_depth"])
                                        if atom_structure_["sample_description_table"][i_]["video_pixel_color_name"] != "invalid":
                                            info_["quicktime"]["video"]["codec_fourcc"] = atom_structure_["sample_description_table"][i_]["data_format"]
                                            info_["quicktime"]["video"]["codec_fourcc_lookup"] = self.quicktimevideocodeclookup(atom_structure_["sample_description_table"][i_]["data_format"])
                                            info_["quicktime"]["video"]["codec"] = atom_structure_["sample_description_table"][i_]["video_encoder_name"] if atom_structure_["sample_description_table"][i_]["video_encoder_name_len"] > 0 else atom_structure_["sample_description_table"][i_]["data_format"]
                                            info_["quicktime"]["video"]["color_depth"] = atom_structure_["sample_description_table"][i_]["video_pixel_color_depth"]
                                            info_["quicktime"]["video"]["color_depth_name"] = atom_structure_["sample_description_table"][i_]["video_pixel_color_name"]
                                            info_["video"]["codec"] = info_["quicktime"]["video"]["codec"]
                                            info_["video"]["bits_per_sample"] = info_["quicktime"]["video"]["color_depth"]
                                        # end if
                                        info_["video"]["lossless"] = False
                                        info_["video"]["pixel_aspect_ratio"] = php_float(1)
                                        break
                                    # end if
                                # end for
                                break
                            # end if
                        # end for
                        for case in Switch(php_strtolower(atom_structure_["sample_description_table"][i_]["data_format"])):
                            if case("mp4a"):
                                info_["audio"]["dataformat"] = "mp4"
                                info_["quicktime"]["audio"]["codec"] = "mp4"
                                break
                            # end if
                            if case("3ivx"):
                                pass
                            # end if
                            if case("3iv1"):
                                pass
                            # end if
                            if case("3iv2"):
                                info_["video"]["dataformat"] = "3ivx"
                                break
                            # end if
                            if case("xvid"):
                                info_["video"]["dataformat"] = "xvid"
                                break
                            # end if
                            if case("mp4v"):
                                info_["video"]["dataformat"] = "mpeg4"
                                break
                            # end if
                            if case("divx"):
                                pass
                            # end if
                            if case("div1"):
                                pass
                            # end if
                            if case("div2"):
                                pass
                            # end if
                            if case("div3"):
                                pass
                            # end if
                            if case("div4"):
                                pass
                            # end if
                            if case("div5"):
                                pass
                            # end if
                            if case("div6"):
                                info_["video"]["dataformat"] = "divx"
                                break
                            # end if
                            if case():
                                break
                            # end if
                        # end for
                        atom_structure_["sample_description_table"][i_]["data"] = None
                        i_ += 1
                    # end while
                    break
                # end if
                if case("stts"):
                    #// Sample Table Time-to-Sample atom
                    atom_structure_["version"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 1))
                    atom_structure_["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data_, 1, 3))
                    #// hardcoded: 0x0000
                    atom_structure_["number_entries"] = getid3_lib.bigendian2int(php_substr(atom_data_, 4, 4))
                    sttsEntriesDataOffset_ = 8
                    #// $FrameRateCalculatorArray = array();
                    frames_count_ = 0
                    max_stts_entries_to_scan_ = php_min(floor(self.getid3.memory_limit / 10000), atom_structure_["number_entries"]) if info_["php_memory_limit"] else atom_structure_["number_entries"]
                    if max_stts_entries_to_scan_ < atom_structure_["number_entries"]:
                        self.warning("QuickTime atom \"stts\" has " + atom_structure_["number_entries"] + " but only scanning the first " + max_stts_entries_to_scan_ + " entries due to limited PHP memory available (" + floor(self.getid3.memory_limit / 1048576) + "MB).")
                    # end if
                    i_ = 0
                    while i_ < max_stts_entries_to_scan_:
                        
                        atom_structure_["time_to_sample_table"][i_]["sample_count"] = getid3_lib.bigendian2int(php_substr(atom_data_, sttsEntriesDataOffset_, 4))
                        sttsEntriesDataOffset_ += 4
                        atom_structure_["time_to_sample_table"][i_]["sample_duration"] = getid3_lib.bigendian2int(php_substr(atom_data_, sttsEntriesDataOffset_, 4))
                        sttsEntriesDataOffset_ += 4
                        frames_count_ += atom_structure_["time_to_sample_table"][i_]["sample_count"]
                        pass
                        i_ += 1
                    # end while
                    info_["quicktime"]["stts_framecount"][-1] = frames_count_
                    break
                # end if
                if case("stss"):
                    #// Sample Table Sync Sample (key frames) atom
                    if ParseAllPossibleAtoms_:
                        atom_structure_["version"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 1))
                        atom_structure_["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data_, 1, 3))
                        #// hardcoded: 0x0000
                        atom_structure_["number_entries"] = getid3_lib.bigendian2int(php_substr(atom_data_, 4, 4))
                        stssEntriesDataOffset_ = 8
                        i_ = 0
                        while i_ < atom_structure_["number_entries"]:
                            
                            atom_structure_["time_to_sample_table"][i_] = getid3_lib.bigendian2int(php_substr(atom_data_, stssEntriesDataOffset_, 4))
                            stssEntriesDataOffset_ += 4
                            i_ += 1
                        # end while
                    # end if
                    break
                # end if
                if case("stsc"):
                    #// Sample Table Sample-to-Chunk atom
                    if ParseAllPossibleAtoms_:
                        atom_structure_["version"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 1))
                        atom_structure_["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data_, 1, 3))
                        #// hardcoded: 0x0000
                        atom_structure_["number_entries"] = getid3_lib.bigendian2int(php_substr(atom_data_, 4, 4))
                        stscEntriesDataOffset_ = 8
                        i_ = 0
                        while i_ < atom_structure_["number_entries"]:
                            
                            atom_structure_["sample_to_chunk_table"][i_]["first_chunk"] = getid3_lib.bigendian2int(php_substr(atom_data_, stscEntriesDataOffset_, 4))
                            stscEntriesDataOffset_ += 4
                            atom_structure_["sample_to_chunk_table"][i_]["samples_per_chunk"] = getid3_lib.bigendian2int(php_substr(atom_data_, stscEntriesDataOffset_, 4))
                            stscEntriesDataOffset_ += 4
                            atom_structure_["sample_to_chunk_table"][i_]["sample_description"] = getid3_lib.bigendian2int(php_substr(atom_data_, stscEntriesDataOffset_, 4))
                            stscEntriesDataOffset_ += 4
                            i_ += 1
                        # end while
                    # end if
                    break
                # end if
                if case("stsz"):
                    #// Sample Table SiZe atom
                    if ParseAllPossibleAtoms_:
                        atom_structure_["version"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 1))
                        atom_structure_["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data_, 1, 3))
                        #// hardcoded: 0x0000
                        atom_structure_["sample_size"] = getid3_lib.bigendian2int(php_substr(atom_data_, 4, 4))
                        atom_structure_["number_entries"] = getid3_lib.bigendian2int(php_substr(atom_data_, 8, 4))
                        stszEntriesDataOffset_ = 12
                        if atom_structure_["sample_size"] == 0:
                            i_ = 0
                            while i_ < atom_structure_["number_entries"]:
                                
                                atom_structure_["sample_size_table"][i_] = getid3_lib.bigendian2int(php_substr(atom_data_, stszEntriesDataOffset_, 4))
                                stszEntriesDataOffset_ += 4
                                i_ += 1
                            # end while
                        # end if
                    # end if
                    break
                # end if
                if case("stco"):
                    #// Sample Table Chunk Offset atom
                    if ParseAllPossibleAtoms_:
                        atom_structure_["version"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 1))
                        atom_structure_["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data_, 1, 3))
                        #// hardcoded: 0x0000
                        atom_structure_["number_entries"] = getid3_lib.bigendian2int(php_substr(atom_data_, 4, 4))
                        stcoEntriesDataOffset_ = 8
                        i_ = 0
                        while i_ < atom_structure_["number_entries"]:
                            
                            atom_structure_["chunk_offset_table"][i_] = getid3_lib.bigendian2int(php_substr(atom_data_, stcoEntriesDataOffset_, 4))
                            stcoEntriesDataOffset_ += 4
                            i_ += 1
                        # end while
                    # end if
                    break
                # end if
                if case("co64"):
                    #// Chunk Offset 64-bit (version of "stco" that supports > 2GB files)
                    if ParseAllPossibleAtoms_:
                        atom_structure_["version"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 1))
                        atom_structure_["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data_, 1, 3))
                        #// hardcoded: 0x0000
                        atom_structure_["number_entries"] = getid3_lib.bigendian2int(php_substr(atom_data_, 4, 4))
                        stcoEntriesDataOffset_ = 8
                        i_ = 0
                        while i_ < atom_structure_["number_entries"]:
                            
                            atom_structure_["chunk_offset_table"][i_] = getid3_lib.bigendian2int(php_substr(atom_data_, stcoEntriesDataOffset_, 8))
                            stcoEntriesDataOffset_ += 8
                            i_ += 1
                        # end while
                    # end if
                    break
                # end if
                if case("dref"):
                    #// Data REFerence atom
                    atom_structure_["version"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 1))
                    atom_structure_["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data_, 1, 3))
                    #// hardcoded: 0x0000
                    atom_structure_["number_entries"] = getid3_lib.bigendian2int(php_substr(atom_data_, 4, 4))
                    drefDataOffset_ = 8
                    i_ = 0
                    while i_ < atom_structure_["number_entries"]:
                        
                        atom_structure_["data_references"][i_]["size"] = getid3_lib.bigendian2int(php_substr(atom_data_, drefDataOffset_, 4))
                        drefDataOffset_ += 4
                        atom_structure_["data_references"][i_]["type"] = php_substr(atom_data_, drefDataOffset_, 4)
                        drefDataOffset_ += 4
                        atom_structure_["data_references"][i_]["version"] = getid3_lib.bigendian2int(php_substr(atom_data_, drefDataOffset_, 1))
                        drefDataOffset_ += 1
                        atom_structure_["data_references"][i_]["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data_, drefDataOffset_, 3))
                        #// hardcoded: 0x0000
                        drefDataOffset_ += 3
                        atom_structure_["data_references"][i_]["data"] = php_substr(atom_data_, drefDataOffset_, atom_structure_["data_references"][i_]["size"] - 4 - 4 - 1 - 3)
                        drefDataOffset_ += atom_structure_["data_references"][i_]["size"] - 4 - 4 - 1 - 3
                        atom_structure_["data_references"][i_]["flags"]["self_reference"] = php_bool(atom_structure_["data_references"][i_]["flags_raw"] & 1)
                        i_ += 1
                    # end while
                    break
                # end if
                if case("gmin"):
                    #// base Media INformation atom
                    atom_structure_["version"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 1))
                    atom_structure_["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data_, 1, 3))
                    #// hardcoded: 0x0000
                    atom_structure_["graphics_mode"] = getid3_lib.bigendian2int(php_substr(atom_data_, 4, 2))
                    atom_structure_["opcolor_red"] = getid3_lib.bigendian2int(php_substr(atom_data_, 6, 2))
                    atom_structure_["opcolor_green"] = getid3_lib.bigendian2int(php_substr(atom_data_, 8, 2))
                    atom_structure_["opcolor_blue"] = getid3_lib.bigendian2int(php_substr(atom_data_, 10, 2))
                    atom_structure_["balance"] = getid3_lib.bigendian2int(php_substr(atom_data_, 12, 2))
                    atom_structure_["reserved"] = getid3_lib.bigendian2int(php_substr(atom_data_, 14, 2))
                    break
                # end if
                if case("smhd"):
                    #// Sound Media information HeaDer atom
                    atom_structure_["version"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 1))
                    atom_structure_["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data_, 1, 3))
                    #// hardcoded: 0x0000
                    atom_structure_["balance"] = getid3_lib.bigendian2int(php_substr(atom_data_, 4, 2))
                    atom_structure_["reserved"] = getid3_lib.bigendian2int(php_substr(atom_data_, 6, 2))
                    break
                # end if
                if case("vmhd"):
                    #// Video Media information HeaDer atom
                    atom_structure_["version"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 1))
                    atom_structure_["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data_, 1, 3))
                    atom_structure_["graphics_mode"] = getid3_lib.bigendian2int(php_substr(atom_data_, 4, 2))
                    atom_structure_["opcolor_red"] = getid3_lib.bigendian2int(php_substr(atom_data_, 6, 2))
                    atom_structure_["opcolor_green"] = getid3_lib.bigendian2int(php_substr(atom_data_, 8, 2))
                    atom_structure_["opcolor_blue"] = getid3_lib.bigendian2int(php_substr(atom_data_, 10, 2))
                    atom_structure_["flags"]["no_lean_ahead"] = php_bool(atom_structure_["flags_raw"] & 1)
                    break
                # end if
                if case("hdlr"):
                    #// HanDLeR reference atom
                    atom_structure_["version"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 1))
                    atom_structure_["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data_, 1, 3))
                    #// hardcoded: 0x0000
                    atom_structure_["component_type"] = php_substr(atom_data_, 4, 4)
                    atom_structure_["component_subtype"] = php_substr(atom_data_, 8, 4)
                    atom_structure_["component_manufacturer"] = php_substr(atom_data_, 12, 4)
                    atom_structure_["component_flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data_, 16, 4))
                    atom_structure_["component_flags_mask"] = getid3_lib.bigendian2int(php_substr(atom_data_, 20, 4))
                    atom_structure_["component_name"] = self.pascal2string(php_substr(atom_data_, 24))
                    if atom_structure_["component_subtype"] == "STpn" and atom_structure_["component_manufacturer"] == "zzzz":
                        info_["video"]["dataformat"] = "quicktimevr"
                    # end if
                    break
                # end if
                if case("mdhd"):
                    #// MeDia HeaDer atom
                    atom_structure_["version"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 1))
                    atom_structure_["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data_, 1, 3))
                    #// hardcoded: 0x0000
                    atom_structure_["creation_time"] = getid3_lib.bigendian2int(php_substr(atom_data_, 4, 4))
                    atom_structure_["modify_time"] = getid3_lib.bigendian2int(php_substr(atom_data_, 8, 4))
                    atom_structure_["time_scale"] = getid3_lib.bigendian2int(php_substr(atom_data_, 12, 4))
                    atom_structure_["duration"] = getid3_lib.bigendian2int(php_substr(atom_data_, 16, 4))
                    atom_structure_["language_id"] = getid3_lib.bigendian2int(php_substr(atom_data_, 20, 2))
                    atom_structure_["quality"] = getid3_lib.bigendian2int(php_substr(atom_data_, 22, 2))
                    if atom_structure_["time_scale"] == 0:
                        self.error("Corrupt Quicktime file: mdhd.time_scale == zero")
                        return False
                    # end if
                    info_["quicktime"]["time_scale"] = php_max(info_["quicktime"]["time_scale"], atom_structure_["time_scale"]) if (php_isset(lambda : info_["quicktime"]["time_scale"])) and info_["quicktime"]["time_scale"] < 1000 else atom_structure_["time_scale"]
                    atom_structure_["creation_time_unix"] = getid3_lib.datemac2unix(atom_structure_["creation_time"])
                    atom_structure_["modify_time_unix"] = getid3_lib.datemac2unix(atom_structure_["modify_time"])
                    atom_structure_["playtime_seconds"] = atom_structure_["duration"] / atom_structure_["time_scale"]
                    atom_structure_["language"] = self.quicktimelanguagelookup(atom_structure_["language_id"])
                    if php_empty(lambda : info_["comments"]["language"]) or (not php_in_array(atom_structure_["language"], info_["comments"]["language"])):
                        info_["comments"]["language"][-1] = atom_structure_["language"]
                    # end if
                    break
                # end if
                if case("pnot"):
                    #// Preview atom
                    atom_structure_["modification_date"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 4))
                    #// "standard Macintosh format"
                    atom_structure_["version_number"] = getid3_lib.bigendian2int(php_substr(atom_data_, 4, 2))
                    #// hardcoded: 0x00
                    atom_structure_["atom_type"] = php_substr(atom_data_, 6, 4)
                    #// usually: 'PICT'
                    atom_structure_["atom_index"] = getid3_lib.bigendian2int(php_substr(atom_data_, 10, 2))
                    #// usually: 0x01
                    atom_structure_["modification_date_unix"] = getid3_lib.datemac2unix(atom_structure_["modification_date"])
                    break
                # end if
                if case("crgn"):
                    #// Clipping ReGioN atom
                    atom_structure_["region_size"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 2))
                    #// The Region size, Region boundary box,
                    atom_structure_["boundary_box"] = getid3_lib.bigendian2int(php_substr(atom_data_, 2, 8))
                    #// and Clipping region data fields
                    atom_structure_["clipping_data"] = php_substr(atom_data_, 10)
                    break
                # end if
                if case("load"):
                    #// track LOAD settings atom
                    atom_structure_["preload_start_time"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 4))
                    atom_structure_["preload_duration"] = getid3_lib.bigendian2int(php_substr(atom_data_, 4, 4))
                    atom_structure_["preload_flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data_, 8, 4))
                    atom_structure_["default_hints_raw"] = getid3_lib.bigendian2int(php_substr(atom_data_, 12, 4))
                    atom_structure_["default_hints"]["double_buffer"] = php_bool(atom_structure_["default_hints_raw"] & 32)
                    atom_structure_["default_hints"]["high_quality"] = php_bool(atom_structure_["default_hints_raw"] & 256)
                    break
                # end if
                if case("tmcd"):
                    pass
                # end if
                if case("chap"):
                    pass
                # end if
                if case("sync"):
                    pass
                # end if
                if case("scpt"):
                    pass
                # end if
                if case("ssrc"):
                    #// non-primary SouRCe atom
                    i_ = 0
                    while i_ < php_strlen(atom_data_):
                        
                        php_no_error(lambda: atom_structure_["track_id"][-1] = getid3_lib.bigendian2int(php_substr(atom_data_, i_, 4)))
                        i_ += 4
                    # end while
                    break
                # end if
                if case("elst"):
                    #// Edit LiST atom
                    atom_structure_["version"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 1))
                    atom_structure_["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data_, 1, 3))
                    #// hardcoded: 0x0000
                    atom_structure_["number_entries"] = getid3_lib.bigendian2int(php_substr(atom_data_, 4, 4))
                    i_ = 0
                    while i_ < atom_structure_["number_entries"]:
                        
                        atom_structure_["edit_list"][i_]["track_duration"] = getid3_lib.bigendian2int(php_substr(atom_data_, 8 + i_ * 12 + 0, 4))
                        atom_structure_["edit_list"][i_]["media_time"] = getid3_lib.bigendian2int(php_substr(atom_data_, 8 + i_ * 12 + 4, 4))
                        atom_structure_["edit_list"][i_]["media_rate"] = getid3_lib.fixedpoint16_16(php_substr(atom_data_, 8 + i_ * 12 + 8, 4))
                        i_ += 1
                    # end while
                    break
                # end if
                if case("kmat"):
                    #// compressed MATte atom
                    atom_structure_["version"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 1))
                    atom_structure_["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data_, 1, 3))
                    #// hardcoded: 0x0000
                    atom_structure_["matte_data_raw"] = php_substr(atom_data_, 4)
                    break
                # end if
                if case("ctab"):
                    #// Color TABle atom
                    atom_structure_["color_table_seed"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 4))
                    #// hardcoded: 0x00000000
                    atom_structure_["color_table_flags"] = getid3_lib.bigendian2int(php_substr(atom_data_, 4, 2))
                    #// hardcoded: 0x8000
                    atom_structure_["color_table_size"] = getid3_lib.bigendian2int(php_substr(atom_data_, 6, 2)) + 1
                    colortableentry_ = 0
                    while colortableentry_ < atom_structure_["color_table_size"]:
                        
                        atom_structure_["color_table"][colortableentry_]["alpha"] = getid3_lib.bigendian2int(php_substr(atom_data_, 8 + colortableentry_ * 8 + 0, 2))
                        atom_structure_["color_table"][colortableentry_]["red"] = getid3_lib.bigendian2int(php_substr(atom_data_, 8 + colortableentry_ * 8 + 2, 2))
                        atom_structure_["color_table"][colortableentry_]["green"] = getid3_lib.bigendian2int(php_substr(atom_data_, 8 + colortableentry_ * 8 + 4, 2))
                        atom_structure_["color_table"][colortableentry_]["blue"] = getid3_lib.bigendian2int(php_substr(atom_data_, 8 + colortableentry_ * 8 + 6, 2))
                        colortableentry_ += 1
                    # end while
                    break
                # end if
                if case("mvhd"):
                    #// MoVie HeaDer atom
                    atom_structure_["version"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 1))
                    atom_structure_["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data_, 1, 3))
                    atom_structure_["creation_time"] = getid3_lib.bigendian2int(php_substr(atom_data_, 4, 4))
                    atom_structure_["modify_time"] = getid3_lib.bigendian2int(php_substr(atom_data_, 8, 4))
                    atom_structure_["time_scale"] = getid3_lib.bigendian2int(php_substr(atom_data_, 12, 4))
                    atom_structure_["duration"] = getid3_lib.bigendian2int(php_substr(atom_data_, 16, 4))
                    atom_structure_["preferred_rate"] = getid3_lib.fixedpoint16_16(php_substr(atom_data_, 20, 4))
                    atom_structure_["preferred_volume"] = getid3_lib.fixedpoint8_8(php_substr(atom_data_, 24, 2))
                    atom_structure_["reserved"] = php_substr(atom_data_, 26, 10)
                    atom_structure_["matrix_a"] = getid3_lib.fixedpoint16_16(php_substr(atom_data_, 36, 4))
                    atom_structure_["matrix_b"] = getid3_lib.fixedpoint16_16(php_substr(atom_data_, 40, 4))
                    atom_structure_["matrix_u"] = getid3_lib.fixedpoint2_30(php_substr(atom_data_, 44, 4))
                    atom_structure_["matrix_c"] = getid3_lib.fixedpoint16_16(php_substr(atom_data_, 48, 4))
                    atom_structure_["matrix_d"] = getid3_lib.fixedpoint16_16(php_substr(atom_data_, 52, 4))
                    atom_structure_["matrix_v"] = getid3_lib.fixedpoint2_30(php_substr(atom_data_, 56, 4))
                    atom_structure_["matrix_x"] = getid3_lib.fixedpoint16_16(php_substr(atom_data_, 60, 4))
                    atom_structure_["matrix_y"] = getid3_lib.fixedpoint16_16(php_substr(atom_data_, 64, 4))
                    atom_structure_["matrix_w"] = getid3_lib.fixedpoint2_30(php_substr(atom_data_, 68, 4))
                    atom_structure_["preview_time"] = getid3_lib.bigendian2int(php_substr(atom_data_, 72, 4))
                    atom_structure_["preview_duration"] = getid3_lib.bigendian2int(php_substr(atom_data_, 76, 4))
                    atom_structure_["poster_time"] = getid3_lib.bigendian2int(php_substr(atom_data_, 80, 4))
                    atom_structure_["selection_time"] = getid3_lib.bigendian2int(php_substr(atom_data_, 84, 4))
                    atom_structure_["selection_duration"] = getid3_lib.bigendian2int(php_substr(atom_data_, 88, 4))
                    atom_structure_["current_time"] = getid3_lib.bigendian2int(php_substr(atom_data_, 92, 4))
                    atom_structure_["next_track_id"] = getid3_lib.bigendian2int(php_substr(atom_data_, 96, 4))
                    if atom_structure_["time_scale"] == 0:
                        self.error("Corrupt Quicktime file: mvhd.time_scale == zero")
                        return False
                    # end if
                    atom_structure_["creation_time_unix"] = getid3_lib.datemac2unix(atom_structure_["creation_time"])
                    atom_structure_["modify_time_unix"] = getid3_lib.datemac2unix(atom_structure_["modify_time"])
                    info_["quicktime"]["time_scale"] = php_max(info_["quicktime"]["time_scale"], atom_structure_["time_scale"]) if (php_isset(lambda : info_["quicktime"]["time_scale"])) and info_["quicktime"]["time_scale"] < 1000 else atom_structure_["time_scale"]
                    info_["quicktime"]["display_scale"] = atom_structure_["matrix_a"]
                    info_["playtime_seconds"] = atom_structure_["duration"] / atom_structure_["time_scale"]
                    break
                # end if
                if case("tkhd"):
                    #// TracK HeaDer atom
                    atom_structure_["version"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 1))
                    atom_structure_["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data_, 1, 3))
                    atom_structure_["creation_time"] = getid3_lib.bigendian2int(php_substr(atom_data_, 4, 4))
                    atom_structure_["modify_time"] = getid3_lib.bigendian2int(php_substr(atom_data_, 8, 4))
                    atom_structure_["trackid"] = getid3_lib.bigendian2int(php_substr(atom_data_, 12, 4))
                    atom_structure_["reserved1"] = getid3_lib.bigendian2int(php_substr(atom_data_, 16, 4))
                    atom_structure_["duration"] = getid3_lib.bigendian2int(php_substr(atom_data_, 20, 4))
                    atom_structure_["reserved2"] = getid3_lib.bigendian2int(php_substr(atom_data_, 24, 8))
                    atom_structure_["layer"] = getid3_lib.bigendian2int(php_substr(atom_data_, 32, 2))
                    atom_structure_["alternate_group"] = getid3_lib.bigendian2int(php_substr(atom_data_, 34, 2))
                    atom_structure_["volume"] = getid3_lib.fixedpoint8_8(php_substr(atom_data_, 36, 2))
                    atom_structure_["reserved3"] = getid3_lib.bigendian2int(php_substr(atom_data_, 38, 2))
                    #// http://developer.apple.com/library/mac/#documentation/QuickTime/RM/MovieBasics/MTEditing/K-Chapter/11MatrixFunctions.html
                    #// http://developer.apple.com/library/mac/#documentation/QuickTime/qtff/QTFFChap4/qtff4.html#//apple_ref/doc/uid/TP40000939-CH206-18737
                    atom_structure_["matrix_a"] = getid3_lib.fixedpoint16_16(php_substr(atom_data_, 40, 4))
                    atom_structure_["matrix_b"] = getid3_lib.fixedpoint16_16(php_substr(atom_data_, 44, 4))
                    atom_structure_["matrix_u"] = getid3_lib.fixedpoint2_30(php_substr(atom_data_, 48, 4))
                    atom_structure_["matrix_c"] = getid3_lib.fixedpoint16_16(php_substr(atom_data_, 52, 4))
                    atom_structure_["matrix_d"] = getid3_lib.fixedpoint16_16(php_substr(atom_data_, 56, 4))
                    atom_structure_["matrix_v"] = getid3_lib.fixedpoint2_30(php_substr(atom_data_, 60, 4))
                    atom_structure_["matrix_x"] = getid3_lib.fixedpoint16_16(php_substr(atom_data_, 64, 4))
                    atom_structure_["matrix_y"] = getid3_lib.fixedpoint16_16(php_substr(atom_data_, 68, 4))
                    atom_structure_["matrix_w"] = getid3_lib.fixedpoint2_30(php_substr(atom_data_, 72, 4))
                    atom_structure_["width"] = getid3_lib.fixedpoint16_16(php_substr(atom_data_, 76, 4))
                    atom_structure_["height"] = getid3_lib.fixedpoint16_16(php_substr(atom_data_, 80, 4))
                    atom_structure_["flags"]["enabled"] = php_bool(atom_structure_["flags_raw"] & 1)
                    atom_structure_["flags"]["in_movie"] = php_bool(atom_structure_["flags_raw"] & 2)
                    atom_structure_["flags"]["in_preview"] = php_bool(atom_structure_["flags_raw"] & 4)
                    atom_structure_["flags"]["in_poster"] = php_bool(atom_structure_["flags_raw"] & 8)
                    atom_structure_["creation_time_unix"] = getid3_lib.datemac2unix(atom_structure_["creation_time"])
                    atom_structure_["modify_time_unix"] = getid3_lib.datemac2unix(atom_structure_["modify_time"])
                    #// https://www.getid3.org/phpBB3/viewtopic.php?t=1908
                    #// attempt to compute rotation from matrix values
                    #// 2017-Dec-28: uncertain if 90/270 are correctly oriented; values returned by FixedPoint16_16 should perhaps be -1 instead of 65535(?)
                    matrixRotation_ = 0
                    for case in Switch(atom_structure_["matrix_a"] + ":" + atom_structure_["matrix_b"] + ":" + atom_structure_["matrix_c"] + ":" + atom_structure_["matrix_d"]):
                        if case("1:0:0:1"):
                            matrixRotation_ = 0
                            break
                        # end if
                        if case("0:1:65535:0"):
                            matrixRotation_ = 90
                            break
                        # end if
                        if case("65535:0:0:65535"):
                            matrixRotation_ = 180
                            break
                        # end if
                        if case("0:65535:1:0"):
                            matrixRotation_ = 270
                            break
                        # end if
                        if case():
                            break
                        # end if
                    # end for
                    #// https://www.getid3.org/phpBB3/viewtopic.php?t=2468
                    #// The rotation matrix can appear in the Quicktime file multiple times, at least once for each track,
                    #// and it's possible that only the video track (or, in theory, one of the video tracks) is flagged as
                    #// rotated while the other tracks (e.g. audio) is tagged as rotation=0 (behavior noted on iPhone 8 Plus)
                    #// The correct solution would be to check if the TrackID associated with the rotation matrix is indeed
                    #// a video track (or the main video track) and only set the rotation then, but since information about
                    #// what track is what is not trivially there to be examined, the lazy solution is to set the rotation
                    #// if it is found to be nonzero, on the assumption that tracks that don't need it will have rotation set
                    #// to zero (and be effectively ignored) and the video track will have rotation set correctly, which will
                    #// either be zero and automatically correct, or nonzero and be set correctly.
                    if (not (php_isset(lambda : info_["video"]["rotate"]))) or info_["video"]["rotate"] == 0 and matrixRotation_ > 0:
                        info_["quicktime"]["video"]["rotate"] = info_["video"]["rotate"]
                    # end if
                    if atom_structure_["flags"]["enabled"] == 1:
                        if (not (php_isset(lambda : info_["video"]["resolution_x"]))) or (not (php_isset(lambda : info_["video"]["resolution_y"]))):
                            info_["video"]["resolution_x"] = atom_structure_["width"]
                            info_["video"]["resolution_y"] = atom_structure_["height"]
                        # end if
                        info_["video"]["resolution_x"] = php_max(info_["video"]["resolution_x"], atom_structure_["width"])
                        info_["video"]["resolution_y"] = php_max(info_["video"]["resolution_y"], atom_structure_["height"])
                        info_["quicktime"]["video"]["resolution_x"] = info_["video"]["resolution_x"]
                        info_["quicktime"]["video"]["resolution_y"] = info_["video"]["resolution_y"]
                    else:
                        pass
                    # end if
                    break
                # end if
                if case("iods"):
                    #// Initial Object DeScriptor atom
                    #// http://www.koders.com/c/fid1FAB3E762903DC482D8A246D4A4BF9F28E049594.aspx?s=windows.h
                    #// http://libquicktime.sourcearchive.com/documentation/1.0.2plus-pdebian/iods_8c-source.html
                    offset_ = 0
                    atom_structure_["version"] = getid3_lib.bigendian2int(php_substr(atom_data_, offset_, 1))
                    offset_ += 1
                    atom_structure_["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data_, offset_, 3))
                    offset_ += 3
                    atom_structure_["mp4_iod_tag"] = getid3_lib.bigendian2int(php_substr(atom_data_, offset_, 1))
                    offset_ += 1
                    atom_structure_["length"] = self.quicktime_read_mp4_descr_length(atom_data_, offset_)
                    #// $offset already adjusted by quicktime_read_mp4_descr_length()
                    atom_structure_["object_descriptor_id"] = getid3_lib.bigendian2int(php_substr(atom_data_, offset_, 2))
                    offset_ += 2
                    atom_structure_["od_profile_level"] = getid3_lib.bigendian2int(php_substr(atom_data_, offset_, 1))
                    offset_ += 1
                    atom_structure_["scene_profile_level"] = getid3_lib.bigendian2int(php_substr(atom_data_, offset_, 1))
                    offset_ += 1
                    atom_structure_["audio_profile_id"] = getid3_lib.bigendian2int(php_substr(atom_data_, offset_, 1))
                    offset_ += 1
                    atom_structure_["video_profile_id"] = getid3_lib.bigendian2int(php_substr(atom_data_, offset_, 1))
                    offset_ += 1
                    atom_structure_["graphics_profile_level"] = getid3_lib.bigendian2int(php_substr(atom_data_, offset_, 1))
                    offset_ += 1
                    atom_structure_["num_iods_tracks"] = atom_structure_["length"] - 7 / 6
                    #// 6 bytes would only be right if all tracks use 1-byte length fields
                    i_ = 0
                    while i_ < atom_structure_["num_iods_tracks"]:
                        
                        atom_structure_["track"][i_]["ES_ID_IncTag"] = getid3_lib.bigendian2int(php_substr(atom_data_, offset_, 1))
                        offset_ += 1
                        atom_structure_["track"][i_]["length"] = self.quicktime_read_mp4_descr_length(atom_data_, offset_)
                        #// $offset already adjusted by quicktime_read_mp4_descr_length()
                        atom_structure_["track"][i_]["track_id"] = getid3_lib.bigendian2int(php_substr(atom_data_, offset_, 4))
                        offset_ += 4
                        i_ += 1
                    # end while
                    atom_structure_["audio_profile_name"] = self.quicktimeiodsaudioprofilename(atom_structure_["audio_profile_id"])
                    atom_structure_["video_profile_name"] = self.quicktimeiodsvideoprofilename(atom_structure_["video_profile_id"])
                    break
                # end if
                if case("ftyp"):
                    #// FileTYPe (?) atom (for MP4 it seems)
                    atom_structure_["signature"] = php_substr(atom_data_, 0, 4)
                    atom_structure_["unknown_1"] = getid3_lib.bigendian2int(php_substr(atom_data_, 4, 4))
                    atom_structure_["fourcc"] = php_substr(atom_data_, 8, 4)
                    break
                # end if
                if case("mdat"):
                    #// Media DATa atom
                    #// 'mdat' contains the actual data for the audio/video, possibly also subtitles
                    #// due to lack of known documentation, this is a kludge implementation. If you know of documentation on how mdat is properly structed, please send it to info@getid3.org
                    #// first, skip any 'wide' padding, and second 'mdat' header (with specified size of zero?)
                    mdat_offset_ = 0
                    while True:
                        
                        if not (True):
                            break
                        # end if
                        if php_substr(atom_data_, mdat_offset_, 8) == "   " + "wide":
                            mdat_offset_ += 8
                        elif php_substr(atom_data_, mdat_offset_, 8) == "    " + "mdat":
                            mdat_offset_ += 8
                        else:
                            break
                        # end if
                    # end while
                    if php_substr(atom_data_, mdat_offset_, 4) == "GPRO":
                        GOPRO_chunk_length_ = getid3_lib.littleendian2int(php_substr(atom_data_, mdat_offset_ + 4, 4))
                        GOPRO_offset_ = 8
                        atom_structure_["GPRO"]["raw"] = php_substr(atom_data_, mdat_offset_ + 8, GOPRO_chunk_length_ - 8)
                        atom_structure_["GPRO"]["firmware"] = php_substr(atom_structure_["GPRO"]["raw"], 0, 15)
                        atom_structure_["GPRO"]["unknown1"] = php_substr(atom_structure_["GPRO"]["raw"], 15, 16)
                        atom_structure_["GPRO"]["unknown2"] = php_substr(atom_structure_["GPRO"]["raw"], 31, 32)
                        atom_structure_["GPRO"]["unknown3"] = php_substr(atom_structure_["GPRO"]["raw"], 63, 16)
                        atom_structure_["GPRO"]["camera"] = php_substr(atom_structure_["GPRO"]["raw"], 79, 32)
                        info_["quicktime"]["camera"]["model"] = php_rtrim(atom_structure_["GPRO"]["camera"], " ")
                    # end if
                    #// check to see if it looks like chapter titles, in the form of unterminated strings with a leading 16-bit size field
                    while True:
                        chapter_string_length_ = getid3_lib.bigendian2int(php_substr(atom_data_, mdat_offset_, 2))
                        if not (mdat_offset_ < php_strlen(atom_data_) - 8 and chapter_string_length_ and chapter_string_length_ < 1000 and chapter_string_length_ <= php_strlen(atom_data_) - mdat_offset_ - 2 and php_preg_match("#^([\\x00-\\xFF]{2})([\\x20-\\xFF]+)$#", php_substr(atom_data_, mdat_offset_, chapter_string_length_ + 2), chapter_matches_)):
                            break
                        # end if
                        dummy_, chapter_string_length_hex_, chapter_string_ = chapter_matches_
                        mdat_offset_ += 2 + chapter_string_length_
                        php_no_error(lambda: info_["quicktime"]["comments"]["chapters"][-1] = chapter_string_)
                        #// "encd" atom specifies encoding. In theory could be anything, almost always UTF-8, but may be UTF-16 with BOM (not currently handled)
                        if php_substr(atom_data_, mdat_offset_, 12) == "   encd   ":
                            #// UTF-8
                            mdat_offset_ += 12
                        # end if
                    # end while
                    if atomsize_ > 8 and (not (php_isset(lambda : info_["avdataend_tmp"]))) or info_["quicktime"][atomname_]["size"] > info_["avdataend_tmp"] - info_["avdataoffset"]:
                        info_["avdataoffset"] = atom_structure_["offset"] + 8
                        #// $info['quicktime'][$atomname]['offset'] + 8;
                        OldAVDataEnd_ = info_["avdataend"]
                        info_["avdataend"] = atom_structure_["offset"] + atom_structure_["size"]
                        #// $info['quicktime'][$atomname]['offset'] + $info['quicktime'][$atomname]['size'];
                        getid3_temp_ = php_new_class("getID3", lambda : getID3())
                        getid3_temp_.openfile(self.getid3.filename)
                        getid3_temp_.info["avdataoffset"] = info_["avdataoffset"]
                        getid3_temp_.info["avdataend"] = info_["avdataend"]
                        getid3_mp3_ = php_new_class("getid3_mp3", lambda : getid3_mp3(getid3_temp_))
                        if getid3_mp3_.mpegaudioheadervalid(getid3_mp3_.mpegaudioheaderdecode(self.fread(4))):
                            getid3_mp3_.getonlympegaudioinfo(getid3_temp_.info["avdataoffset"], False)
                            if (not php_empty(lambda : getid3_temp_.info["warning"])):
                                for value_ in getid3_temp_.info["warning"]:
                                    self.warning(value_)
                                # end for
                            # end if
                            if (not php_empty(lambda : getid3_temp_.info["mpeg"])):
                                info_["mpeg"] = getid3_temp_.info["mpeg"]
                                if (php_isset(lambda : info_["mpeg"]["audio"])):
                                    info_["audio"]["dataformat"] = "mp3"
                                    info_["audio"]["codec"] = info_["mpeg"]["audio"]["encoder"] if (not php_empty(lambda : info_["mpeg"]["audio"]["encoder"])) else info_["mpeg"]["audio"]["codec"] if (not php_empty(lambda : info_["mpeg"]["audio"]["codec"])) else "LAME" if (not php_empty(lambda : info_["mpeg"]["audio"]["LAME"])) else "mp3"
                                    info_["audio"]["sample_rate"] = info_["mpeg"]["audio"]["sample_rate"]
                                    info_["audio"]["channels"] = info_["mpeg"]["audio"]["channels"]
                                    info_["audio"]["bitrate"] = info_["mpeg"]["audio"]["bitrate"]
                                    info_["audio"]["bitrate_mode"] = php_strtolower(info_["mpeg"]["audio"]["bitrate_mode"])
                                    info_["bitrate"] = info_["audio"]["bitrate"]
                                # end if
                            # end if
                        # end if
                        getid3_mp3_ = None
                        getid3_temp_ = None
                        info_["avdataend"] = OldAVDataEnd_
                        OldAVDataEnd_ = None
                    # end if
                    mdat_offset_ = None
                    chapter_string_length_ = None
                    chapter_matches_ = None
                    break
                # end if
                if case("free"):
                    pass
                # end if
                if case("skip"):
                    pass
                # end if
                if case("wide"):
                    break
                # end if
                if case("nsav"):
                    #// NoSAVe atom
                    #// http://developer.apple.com/technotes/tn/tn2038.html
                    atom_structure_["data"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 4))
                    break
                # end if
                if case("ctyp"):
                    #// Controller TYPe atom (seen on QTVR)
                    #// http://homepages.slingshot.co.nz/~helmboy/quicktime/formats/qtm-layout.txt
                    #// some controller names are:
                    #// 0x00 + 'std' for linear movie
                    #// 'none' for no controls
                    atom_structure_["ctyp"] = php_substr(atom_data_, 0, 4)
                    info_["quicktime"]["controller"] = atom_structure_["ctyp"]
                    for case in Switch(atom_structure_["ctyp"]):
                        if case("qtvr"):
                            info_["video"]["dataformat"] = "quicktimevr"
                            break
                        # end if
                    # end for
                    break
                # end if
                if case("pano"):
                    #// PANOrama track (seen on QTVR)
                    atom_structure_["pano"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 4))
                    break
                # end if
                if case("hint"):
                    pass
                # end if
                if case("hinf"):
                    pass
                # end if
                if case("hinv"):
                    pass
                # end if
                if case("hnti"):
                    #//
                    info_["quicktime"]["hinting"] = True
                    break
                # end if
                if case("imgt"):
                    #// IMaGe Track reference (kQTVRImageTrackRefType) (seen on QTVR)
                    i_ = 0
                    while i_ < atom_structure_["size"] - 8:
                        
                        atom_structure_["imgt"][-1] = getid3_lib.bigendian2int(php_substr(atom_data_, i_, 4))
                        i_ += 4
                    # end while
                    break
                # end if
                if case("FXTC"):
                    pass
                # end if
                if case("PrmA"):
                    pass
                # end if
                if case("code"):
                    pass
                # end if
                if case("FIEL"):
                    pass
                # end if
                if case("tapt"):
                    pass
                # end if
                if case("ctts"):
                    pass
                # end if
                if case("cslg"):
                    pass
                # end if
                if case("sdtp"):
                    pass
                # end if
                if case("stps"):
                    break
                # end if
                if case("©" + "xyz"):
                    #// GPS latitude+longitude+altitude
                    atom_structure_["data"] = atom_data_
                    if php_preg_match("#([\\+\\-][0-9\\.]+)([\\+\\-][0-9\\.]+)([\\+\\-][0-9\\.]+)?/$#i", atom_data_, matches_):
                        php_no_error(lambda: all_, latitude_, longitude_, altitude_ = matches_)
                        info_["quicktime"]["comments"]["gps_latitude"][-1] = floatval(latitude_)
                        info_["quicktime"]["comments"]["gps_longitude"][-1] = floatval(longitude_)
                        if (not php_empty(lambda : altitude_)):
                            info_["quicktime"]["comments"]["gps_altitude"][-1] = floatval(altitude_)
                        # end if
                    else:
                        self.warning("QuickTime atom \"Â©xyz\" data does not match expected data pattern at offset " + baseoffset_ + ". Please report as getID3() bug.")
                    # end if
                    break
                # end if
                if case("NCDT"):
                    #// http://www.sno.phy.queensu.ca/~phil/exiftool/TagNames/Nikon.html
                    #// Nikon-specific QuickTime tags found in the NCDT atom of MOV videos from some Nikon cameras such as the Coolpix S8000 and D5100
                    atom_structure_["subatoms"] = self.quicktimeparsecontaineratom(atom_data_, baseoffset_ + 4, atomHierarchy_, ParseAllPossibleAtoms_)
                    break
                # end if
                if case("NCTH"):
                    pass
                # end if
                if case("NCVW"):
                    #// Nikon Camera preVieW image
                    #// http://www.sno.phy.queensu.ca/~phil/exiftool/TagNames/Nikon.html
                    if php_preg_match("/^\\xFF\\xD8\\xFF/", atom_data_):
                        atom_structure_["data"] = atom_data_
                        atom_structure_["image_mime"] = "image/jpeg"
                        atom_structure_["description"] = "Nikon Camera Thumbnail Image" if atomname_ == "NCTH" else "Nikon Camera Preview Image" if atomname_ == "NCVW" else "Nikon preview image"
                        info_["quicktime"]["comments"]["picture"][-1] = Array({"image_mime": atom_structure_["image_mime"], "data": atom_data_, "description": atom_structure_["description"]})
                    # end if
                    break
                # end if
                if case("NCTG"):
                    #// Nikon - http://www.sno.phy.queensu.ca/~phil/exiftool/TagNames/Nikon.html#NCTG
                    atom_structure_["data"] = self.quicktimeparsenikonnctg(atom_data_)
                    break
                # end if
                if case("NCHD"):
                    pass
                # end if
                if case("NCDB"):
                    pass
                # end if
                if case("CNCV"):
                    #// Canon:CompressorVersion - http://www.sno.phy.queensu.ca/~phil/exiftool/TagNames/Canon.html
                    atom_structure_["data"] = atom_data_
                    break
                # end if
                if case("    "):
                    #// some kind of metacontainer, may contain a big data dump such as:
                    #// mdta keys \005 mdtacom.apple.quicktime.make (mdtacom.apple.quicktime.creationdate ,mdtacom.apple.quicktime.location.ISO6709 $mdtacom.apple.quicktime.software !mdtacom.apple.quicktime.model ilst \01D \001 \015data \001DE\010Apple 0 \002 (data \001DE\0102011-05-11T17:54:04+0200 2 \003 *data \001DE\010+52.4936+013.3897+040.247/ \01D \004 \015data \001DE\0104.3.1 \005 \018data \001DE\010iPhone 4
                    #// http://www.geocities.com/xhelmboyx/quicktime/formats/qti-layout.txt
                    atom_structure_["version"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 1))
                    atom_structure_["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data_, 1, 3))
                    atom_structure_["subatoms"] = self.quicktimeparsecontaineratom(php_substr(atom_data_, 4), baseoffset_ + 8, atomHierarchy_, ParseAllPossibleAtoms_)
                    break
                # end if
                if case("meta"):
                    #// METAdata atom
                    #// https://developer.apple.com/library/mac/documentation/QuickTime/QTFF/Metadata/Metadata.html
                    atom_structure_["version"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 1))
                    atom_structure_["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data_, 1, 3))
                    atom_structure_["subatoms"] = self.quicktimeparsecontaineratom(atom_data_, baseoffset_ + 8, atomHierarchy_, ParseAllPossibleAtoms_)
                    break
                # end if
                if case("data"):
                    metaDATAkey_ = 1
                    #// real ugly, but so is the QuickTime structure that stores keys and values in different multinested locations that are hard to relate to each other
                    #// seems to be 2 bytes language code (ASCII), 2 bytes unknown (set to 0x10B5 in sample I have), remainder is useful data
                    atom_structure_["language"] = php_substr(atom_data_, 4 + 0, 2)
                    atom_structure_["unknown"] = getid3_lib.bigendian2int(php_substr(atom_data_, 4 + 2, 2))
                    atom_structure_["data"] = php_substr(atom_data_, 4 + 4)
                    atom_structure_["key_name"] = php_no_error(lambda: info_["quicktime"]["temp_meta_key_names"][metaDATAkey_])
                    metaDATAkey_ += 1
                    metaDATAkey_ += 1
                    if atom_structure_["key_name"] and atom_structure_["data"]:
                        php_no_error(lambda: info_["quicktime"]["comments"][php_str_replace("com.apple.quicktime.", "", atom_structure_["key_name"])][-1] = atom_structure_["data"])
                    # end if
                    break
                # end if
                if case("keys"):
                    #// KEYS that may be present in the metadata atom.
                    #// https://developer.apple.com/library/mac/documentation/QuickTime/QTFF/Metadata/Metadata.html#//apple_ref/doc/uid/TP40000939-CH1-SW21
                    #// The metadata item keys atom holds a list of the metadata keys that may be present in the metadata atom.
                    #// This list is indexed starting with 1; 0 is a reserved index value. The metadata item keys atom is a full atom with an atom type of "keys".
                    atom_structure_["version"] = getid3_lib.bigendian2int(php_substr(atom_data_, 0, 1))
                    atom_structure_["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data_, 1, 3))
                    atom_structure_["entry_count"] = getid3_lib.bigendian2int(php_substr(atom_data_, 4, 4))
                    keys_atom_offset_ = 8
                    i_ = 1
                    while i_ <= atom_structure_["entry_count"]:
                        
                        atom_structure_["keys"][i_]["key_size"] = getid3_lib.bigendian2int(php_substr(atom_data_, keys_atom_offset_ + 0, 4))
                        atom_structure_["keys"][i_]["key_namespace"] = php_substr(atom_data_, keys_atom_offset_ + 4, 4)
                        atom_structure_["keys"][i_]["key_value"] = php_substr(atom_data_, keys_atom_offset_ + 8, atom_structure_["keys"][i_]["key_size"] - 8)
                        keys_atom_offset_ += atom_structure_["keys"][i_]["key_size"]
                        #// key_size includes the 4+4 bytes for key_size and key_namespace
                        info_["quicktime"]["temp_meta_key_names"][i_] = atom_structure_["keys"][i_]["key_value"]
                        i_ += 1
                    # end while
                    break
                # end if
                if case("gps "):
                    #// https://dashcamtalk.com/forum/threads/script-to-extract-gps-data-from-novatek-mp4.20808/page-2#post-291730
                    #// The 'gps ' contains simple look up table made up of 8byte rows, that point to the 'free' atoms that contains the actual GPS data.
                    #// The first row is version/metadata/notsure, I skip that.
                    #// The following rows consist of 4byte address (absolute) and 4byte size (0x1000), these point to the GPS data in the file.
                    GPS_rowsize_ = 8
                    #// 4 bytes for offset, 4 bytes for size
                    if php_strlen(atom_data_) > 0:
                        if php_strlen(atom_data_) % GPS_rowsize_ == 0:
                            atom_structure_["gps_toc"] = Array()
                            for counter_,datapair_ in str_split(atom_data_, GPS_rowsize_):
                                atom_structure_["gps_toc"][-1] = unpack("Noffset/Nsize", php_substr(atom_data_, counter_ * GPS_rowsize_, GPS_rowsize_))
                            # end for
                            atom_structure_["gps_entries"] = Array()
                            previous_offset_ = self.ftell()
                            for key_,gps_pointer_ in atom_structure_["gps_toc"]:
                                if key_ == 0:
                                    continue
                                # end if
                                self.fseek(gps_pointer_["offset"])
                                GPS_free_data_ = self.fread(gps_pointer_["size"])
                                #// 
                                #// 2017-05-10: I see some of the data, notably the Hour-Minute-Second, but cannot reconcile the rest of the data. However, the NMEA "GPRMC" line is there and relatively easy to parse, so I'm using that instead
                                #// https://dashcamtalk.com/forum/threads/script-to-extract-gps-data-from-novatek-mp4.20808/page-2#post-291730
                                #// The structure of the GPS data atom (the 'free' atoms mentioned above) is following:
                                #// hour,minute,second,year,month,day,active,latitude_b,longitude_b,unknown2,latitude,longitude,speed = struct.unpack_from('<IIIIIIssssfff',data, 48)
                                #// For those unfamiliar with python struct:
                                #// I = int
                                #// s = is string (size 1, in this case)
                                #// f = float
                                #// $atom_structure['gps_entries'][$key] = unpack('Vhour/Vminute/Vsecond/Vyear/Vmonth/Vday/Vactive/Vlatitude_b/Vlongitude_b/Vunknown2/flatitude/flongitude/fspeed', substr($GPS_free_data, 48));
                                #// 
                                #// $GPRMC,081836,A,3751.65,S,14507.36,E,000.0,360.0,130998,011.3,E*62
                                #// $GPRMC,183731,A,3907.482,N,12102.436,W,000.0,360.0,080301,015.5,E*67
                                #// $GPRMC,002454,A,3553.5295,N,13938.6570,E,0.0,43.1,180700,7.1,W,A*3F
                                #// $GPRMC,094347.000,A,5342.0061,N,00737.9908,W,0.01,156.75,140217,,,A*7D
                                if php_preg_match("#\\$GPRMC,([0-9\\.]*),([AV]),([0-9\\.]*),([NS]),([0-9\\.]*),([EW]),([0-9\\.]*),([0-9\\.]*),([0-9]*),([0-9\\.]*),([EW]?)(,[A])?(\\*[0-9A-F]{2})#", GPS_free_data_, matches_):
                                    GPS_this_GPRMC_ = Array()
                                    GPS_this_GPRMC_["raw"]["gprmc"], GPS_this_GPRMC_["raw"]["timestamp"], GPS_this_GPRMC_["raw"]["status"], GPS_this_GPRMC_["raw"]["latitude"], GPS_this_GPRMC_["raw"]["latitude_direction"], GPS_this_GPRMC_["raw"]["longitude"], GPS_this_GPRMC_["raw"]["longitude_direction"], GPS_this_GPRMC_["raw"]["knots"], GPS_this_GPRMC_["raw"]["angle"], GPS_this_GPRMC_["raw"]["datestamp"], GPS_this_GPRMC_["raw"]["variation"], GPS_this_GPRMC_["raw"]["variation_direction"], dummy_, GPS_this_GPRMC_["raw"]["checksum"] = matches_
                                    hour_ = php_substr(GPS_this_GPRMC_["raw"]["timestamp"], 0, 2)
                                    minute_ = php_substr(GPS_this_GPRMC_["raw"]["timestamp"], 2, 2)
                                    second_ = php_substr(GPS_this_GPRMC_["raw"]["timestamp"], 4, 2)
                                    ms_ = php_substr(GPS_this_GPRMC_["raw"]["timestamp"], 6)
                                    #// may contain decimal seconds
                                    day_ = php_substr(GPS_this_GPRMC_["raw"]["datestamp"], 0, 2)
                                    month_ = php_substr(GPS_this_GPRMC_["raw"]["datestamp"], 2, 2)
                                    year_ = php_substr(GPS_this_GPRMC_["raw"]["datestamp"], 4, 2)
                                    year_ += 1900 if year_ > 90 else 2000
                                    #// complete lack of foresight: datestamps are stored with 2-digit years, take best guess
                                    GPS_this_GPRMC_["timestamp"] = year_ + "-" + month_ + "-" + day_ + " " + hour_ + ":" + minute_ + ":" + second_ + ms_
                                    GPS_this_GPRMC_["active"] = GPS_this_GPRMC_["raw"]["status"] == "A"
                                    #// A=Active,V=Void
                                    for latlon_ in Array("latitude", "longitude"):
                                        php_preg_match("#^([0-9]{1,3})([0-9]{2}\\.[0-9]+)$#", GPS_this_GPRMC_["raw"][latlon_], matches_)
                                        dummy_, deg_, min_ = matches_
                                        GPS_this_GPRMC_[latlon_] = deg_ + min_ / 60
                                    # end for
                                    GPS_this_GPRMC_["latitude"] *= -1 if GPS_this_GPRMC_["raw"]["latitude_direction"] == "S" else 1
                                    GPS_this_GPRMC_["longitude"] *= -1 if GPS_this_GPRMC_["raw"]["longitude_direction"] == "W" else 1
                                    GPS_this_GPRMC_["heading"] = GPS_this_GPRMC_["raw"]["angle"]
                                    GPS_this_GPRMC_["speed_knot"] = GPS_this_GPRMC_["raw"]["knots"]
                                    GPS_this_GPRMC_["speed_kmh"] = GPS_this_GPRMC_["raw"]["knots"] * 1.852
                                    if GPS_this_GPRMC_["raw"]["variation"]:
                                        GPS_this_GPRMC_["variation"] = GPS_this_GPRMC_["raw"]["variation"]
                                        GPS_this_GPRMC_["variation"] *= -1 if GPS_this_GPRMC_["raw"]["variation_direction"] == "W" else 1
                                    # end if
                                    atom_structure_["gps_entries"][key_] = GPS_this_GPRMC_
                                    php_no_error(lambda: info_["quicktime"]["gps_track"][GPS_this_GPRMC_["timestamp"]] = Array({"latitude": php_float(GPS_this_GPRMC_["latitude"]), "longitude": php_float(GPS_this_GPRMC_["longitude"]), "speed_kmh": php_float(GPS_this_GPRMC_["speed_kmh"]), "heading": php_float(GPS_this_GPRMC_["heading"])}))
                                else:
                                    self.warning("Unhandled GPS format in \"free\" atom at offset " + gps_pointer_["offset"])
                                # end if
                            # end for
                            self.fseek(previous_offset_)
                        else:
                            self.warning("QuickTime atom \"" + atomname_ + "\" is not mod-8 bytes long (" + atomsize_ + " bytes) at offset " + baseoffset_)
                        # end if
                    else:
                        self.warning("QuickTime atom \"" + atomname_ + "\" is zero bytes long at offset " + baseoffset_)
                    # end if
                    break
                # end if
                if case("loci"):
                    #// 3GP location (El Loco)
                    loffset_ = 0
                    info_["quicktime"]["comments"]["gps_flags"] = Array(getid3_lib.bigendian2int(php_substr(atom_data_, 0, 4)))
                    info_["quicktime"]["comments"]["gps_lang"] = Array(getid3_lib.bigendian2int(php_substr(atom_data_, 4, 2)))
                    info_["quicktime"]["comments"]["gps_location"] = Array(self.locistring(php_substr(atom_data_, 6), loffset_))
                    loci_data_ = php_substr(atom_data_, 6 + loffset_)
                    info_["quicktime"]["comments"]["gps_role"] = Array(getid3_lib.bigendian2int(php_substr(loci_data_, 0, 1)))
                    info_["quicktime"]["comments"]["gps_longitude"] = Array(getid3_lib.fixedpoint16_16(php_substr(loci_data_, 1, 4)))
                    info_["quicktime"]["comments"]["gps_latitude"] = Array(getid3_lib.fixedpoint16_16(php_substr(loci_data_, 5, 4)))
                    info_["quicktime"]["comments"]["gps_altitude"] = Array(getid3_lib.fixedpoint16_16(php_substr(loci_data_, 9, 4)))
                    info_["quicktime"]["comments"]["gps_body"] = Array(self.locistring(php_substr(loci_data_, 13), loffset_))
                    info_["quicktime"]["comments"]["gps_notes"] = Array(self.locistring(php_substr(loci_data_, 13 + loffset_), loffset_))
                    break
                # end if
                if case("chpl"):
                    #// CHaPter List
                    #// https://www.adobe.com/content/dam/Adobe/en/devnet/flv/pdfs/video_file_format_spec_v10.pdf
                    chpl_version_ = getid3_lib.bigendian2int(php_substr(atom_data_, 4, 1))
                    #// Expected to be 0
                    chpl_flags_ = getid3_lib.bigendian2int(php_substr(atom_data_, 5, 3))
                    #// Reserved, set to 0
                    chpl_count_ = getid3_lib.bigendian2int(php_substr(atom_data_, 8, 1))
                    chpl_offset_ = 9
                    i_ = 0
                    while i_ < chpl_count_:
                        
                        if chpl_offset_ + 9 >= php_strlen(atom_data_):
                            self.warning("QuickTime chapter " + i_ + " extends beyond end of \"chpl\" atom")
                            break
                        # end if
                        info_["quicktime"]["chapters"][i_]["timestamp"] = getid3_lib.bigendian2int(php_substr(atom_data_, chpl_offset_, 8)) / 10000000
                        #// timestamps are stored as 100-nanosecond units
                        chpl_offset_ += 8
                        chpl_title_size_ = getid3_lib.bigendian2int(php_substr(atom_data_, chpl_offset_, 1))
                        chpl_offset_ += 1
                        info_["quicktime"]["chapters"][i_]["title"] = php_substr(atom_data_, chpl_offset_, chpl_title_size_)
                        chpl_offset_ += chpl_title_size_
                        i_ += 1
                    # end while
                    break
                # end if
                if case("FIRM"):
                    #// FIRMware version(?), seen on GoPro Hero4
                    info_["quicktime"]["camera"]["firmware"] = atom_data_
                    break
                # end if
                if case("CAME"):
                    #// FIRMware version(?), seen on GoPro Hero4
                    info_["quicktime"]["camera"]["serial_hash"] = unpack("H*", atom_data_)
                    break
                # end if
                if case("dscp"):
                    pass
                # end if
                if case("rcif"):
                    #// https://www.getid3.org/phpBB3/viewtopic.php?t=1908
                    if php_substr(atom_data_, 0, 7) == "    UÄ" + "{":
                        json_decoded_ = php_no_error(lambda: php_json_decode(php_rtrim(php_substr(atom_data_, 6), " "), True))
                        if json_decoded_:
                            info_["quicktime"]["camera"][atomname_] = json_decoded_
                            if atomname_ == "rcif" and (php_isset(lambda : info_["quicktime"]["camera"]["rcif"]["wxcamera"]["rotate"])):
                                info_["video"]["rotate"] = info_["quicktime"]["video"]["rotate"]
                            # end if
                        else:
                            self.warning("Failed to JSON decode atom \"" + atomname_ + "\"")
                            atom_structure_["data"] = atom_data_
                        # end if
                        json_decoded_ = None
                    else:
                        self.warning("Expecting 55 C4 7B at start of atom \"" + atomname_ + "\", found " + getid3_lib.printhexbytes(php_substr(atom_data_, 4, 3)) + " instead")
                        atom_structure_["data"] = atom_data_
                    # end if
                    break
                # end if
                if case("frea"):
                    #// https://www.sno.phy.queensu.ca/~phil/exiftool/TagNames/Kodak.html#frea
                    #// may contain "scra" (PreviewImage) and/or "thma" (ThumbnailImage)
                    atom_structure_["subatoms"] = self.quicktimeparsecontaineratom(atom_data_, baseoffset_ + 4, atomHierarchy_, ParseAllPossibleAtoms_)
                    break
                # end if
                if case("tima"):
                    #// subatom to "frea"
                    #// no idea what this does, the one sample file I've seen has a value of 0x00000027
                    atom_structure_["data"] = atom_data_
                    break
                # end if
                if case("ver "):
                    #// subatom to "frea"
                    #// some kind of version number, the one sample file I've seen has a value of "3.00.073"
                    atom_structure_["data"] = atom_data_
                    break
                # end if
                if case("thma"):
                    #// subatom to "frea" -- "ThumbnailImage"
                    #// https://www.sno.phy.queensu.ca/~phil/exiftool/TagNames/Kodak.html#frea
                    if php_strlen(atom_data_) > 0:
                        info_["quicktime"]["comments"]["picture"][-1] = Array({"data": atom_data_, "image_mime": "image/jpeg"})
                    # end if
                    break
                # end if
                if case("scra"):
                    #// subatom to "frea" -- "PreviewImage"
                    #// https://www.sno.phy.queensu.ca/~phil/exiftool/TagNames/Kodak.html#frea
                    #// but the only sample file I've seen has no useful data here
                    if php_strlen(atom_data_) > 0:
                        info_["quicktime"]["comments"]["picture"][-1] = Array({"data": atom_data_, "image_mime": "image/jpeg"})
                    # end if
                    break
                # end if
                if case():
                    self.warning("Unknown QuickTime atom type: \"" + php_preg_replace("#[^a-zA-Z0-9 _\\-]#", "?", atomname_) + "\" (" + php_trim(getid3_lib.printhexbytes(atomname_)) + "), " + atomsize_ + " bytes at offset " + baseoffset_)
                    atom_structure_["data"] = atom_data_
                    break
                # end if
            # end for
        # end if
        php_array_pop(atomHierarchy_)
        return atom_structure_
    # end def quicktimeparseatom
    #// 
    #// @param string $atom_data
    #// @param int    $baseoffset
    #// @param array  $atomHierarchy
    #// @param bool   $ParseAllPossibleAtoms
    #// 
    #// @return array|false
    #//
    def quicktimeparsecontaineratom(self, atom_data_=None, baseoffset_=None, atomHierarchy_=None, ParseAllPossibleAtoms_=None):
        
        
        atom_structure_ = False
        subatomoffset_ = 0
        subatomcounter_ = 0
        if php_strlen(atom_data_) == 4 and getid3_lib.bigendian2int(atom_data_) == 0:
            return False
        # end if
        while True:
            
            if not (subatomoffset_ < php_strlen(atom_data_)):
                break
            # end if
            subatomsize_ = getid3_lib.bigendian2int(php_substr(atom_data_, subatomoffset_ + 0, 4))
            subatomname_ = php_substr(atom_data_, subatomoffset_ + 4, 4)
            subatomdata_ = php_substr(atom_data_, subatomoffset_ + 8, subatomsize_ - 8)
            if subatomsize_ == 0:
                #// Furthermore, for historical reasons the list of atoms is optionally
                #// terminated by a 32-bit integer set to 0. If you are writing a program
                #// to read user data atoms, you should allow for the terminating 0.
                if php_strlen(atom_data_) > 12:
                    subatomoffset_ += 4
                    continue
                # end if
                return atom_structure_
            # end if
            atom_structure_[subatomcounter_] = self.quicktimeparseatom(subatomname_, subatomsize_, subatomdata_, baseoffset_ + subatomoffset_, atomHierarchy_, ParseAllPossibleAtoms_)
            subatomcounter_ += 1
            subatomoffset_ += subatomsize_
        # end while
        return atom_structure_
    # end def quicktimeparsecontaineratom
    subatomcounter_ += 1
    #// 
    #// @param string $data
    #// @param int    $offset
    #// 
    #// @return int
    #//
    def quicktime_read_mp4_descr_length(self, data_=None, offset_=None):
        
        
        #// http://libquicktime.sourcearchive.com/documentation/2:1.0.2plus-pdebian-2build1/esds_8c-source.html
        num_bytes_ = 0
        length_ = 0
        while True:
            b_ = php_ord(php_substr(data_, offset_, 1))
            offset_ += 1
            length_ = length_ << 7 | b_ & 127
            num_bytes_ += 1
            if b_ & 128 and num_bytes_ < 4:
                break
            # end if
        # end while
        num_bytes_ += 1
        return length_
    # end def quicktime_read_mp4_descr_length
    #// 
    #// @param int $languageid
    #// 
    #// @return string
    #//
    def quicktimelanguagelookup(self, languageid_=None):
        
        
        QuicktimeLanguageLookup_ = Array()
        if php_empty(lambda : QuicktimeLanguageLookup_):
            QuicktimeLanguageLookup_[0] = "English"
            QuicktimeLanguageLookup_[1] = "French"
            QuicktimeLanguageLookup_[2] = "German"
            QuicktimeLanguageLookup_[3] = "Italian"
            QuicktimeLanguageLookup_[4] = "Dutch"
            QuicktimeLanguageLookup_[5] = "Swedish"
            QuicktimeLanguageLookup_[6] = "Spanish"
            QuicktimeLanguageLookup_[7] = "Danish"
            QuicktimeLanguageLookup_[8] = "Portuguese"
            QuicktimeLanguageLookup_[9] = "Norwegian"
            QuicktimeLanguageLookup_[10] = "Hebrew"
            QuicktimeLanguageLookup_[11] = "Japanese"
            QuicktimeLanguageLookup_[12] = "Arabic"
            QuicktimeLanguageLookup_[13] = "Finnish"
            QuicktimeLanguageLookup_[14] = "Greek"
            QuicktimeLanguageLookup_[15] = "Icelandic"
            QuicktimeLanguageLookup_[16] = "Maltese"
            QuicktimeLanguageLookup_[17] = "Turkish"
            QuicktimeLanguageLookup_[18] = "Croatian"
            QuicktimeLanguageLookup_[19] = "Chinese (Traditional)"
            QuicktimeLanguageLookup_[20] = "Urdu"
            QuicktimeLanguageLookup_[21] = "Hindi"
            QuicktimeLanguageLookup_[22] = "Thai"
            QuicktimeLanguageLookup_[23] = "Korean"
            QuicktimeLanguageLookup_[24] = "Lithuanian"
            QuicktimeLanguageLookup_[25] = "Polish"
            QuicktimeLanguageLookup_[26] = "Hungarian"
            QuicktimeLanguageLookup_[27] = "Estonian"
            QuicktimeLanguageLookup_[28] = "Lettish"
            QuicktimeLanguageLookup_[28] = "Latvian"
            QuicktimeLanguageLookup_[29] = "Saamisk"
            QuicktimeLanguageLookup_[29] = "Lappish"
            QuicktimeLanguageLookup_[30] = "Faeroese"
            QuicktimeLanguageLookup_[31] = "Farsi"
            QuicktimeLanguageLookup_[31] = "Persian"
            QuicktimeLanguageLookup_[32] = "Russian"
            QuicktimeLanguageLookup_[33] = "Chinese (Simplified)"
            QuicktimeLanguageLookup_[34] = "Flemish"
            QuicktimeLanguageLookup_[35] = "Irish"
            QuicktimeLanguageLookup_[36] = "Albanian"
            QuicktimeLanguageLookup_[37] = "Romanian"
            QuicktimeLanguageLookup_[38] = "Czech"
            QuicktimeLanguageLookup_[39] = "Slovak"
            QuicktimeLanguageLookup_[40] = "Slovenian"
            QuicktimeLanguageLookup_[41] = "Yiddish"
            QuicktimeLanguageLookup_[42] = "Serbian"
            QuicktimeLanguageLookup_[43] = "Macedonian"
            QuicktimeLanguageLookup_[44] = "Bulgarian"
            QuicktimeLanguageLookup_[45] = "Ukrainian"
            QuicktimeLanguageLookup_[46] = "Byelorussian"
            QuicktimeLanguageLookup_[47] = "Uzbek"
            QuicktimeLanguageLookup_[48] = "Kazakh"
            QuicktimeLanguageLookup_[49] = "Azerbaijani"
            QuicktimeLanguageLookup_[50] = "AzerbaijanAr"
            QuicktimeLanguageLookup_[51] = "Armenian"
            QuicktimeLanguageLookup_[52] = "Georgian"
            QuicktimeLanguageLookup_[53] = "Moldavian"
            QuicktimeLanguageLookup_[54] = "Kirghiz"
            QuicktimeLanguageLookup_[55] = "Tajiki"
            QuicktimeLanguageLookup_[56] = "Turkmen"
            QuicktimeLanguageLookup_[57] = "Mongolian"
            QuicktimeLanguageLookup_[58] = "MongolianCyr"
            QuicktimeLanguageLookup_[59] = "Pashto"
            QuicktimeLanguageLookup_[60] = "Kurdish"
            QuicktimeLanguageLookup_[61] = "Kashmiri"
            QuicktimeLanguageLookup_[62] = "Sindhi"
            QuicktimeLanguageLookup_[63] = "Tibetan"
            QuicktimeLanguageLookup_[64] = "Nepali"
            QuicktimeLanguageLookup_[65] = "Sanskrit"
            QuicktimeLanguageLookup_[66] = "Marathi"
            QuicktimeLanguageLookup_[67] = "Bengali"
            QuicktimeLanguageLookup_[68] = "Assamese"
            QuicktimeLanguageLookup_[69] = "Gujarati"
            QuicktimeLanguageLookup_[70] = "Punjabi"
            QuicktimeLanguageLookup_[71] = "Oriya"
            QuicktimeLanguageLookup_[72] = "Malayalam"
            QuicktimeLanguageLookup_[73] = "Kannada"
            QuicktimeLanguageLookup_[74] = "Tamil"
            QuicktimeLanguageLookup_[75] = "Telugu"
            QuicktimeLanguageLookup_[76] = "Sinhalese"
            QuicktimeLanguageLookup_[77] = "Burmese"
            QuicktimeLanguageLookup_[78] = "Khmer"
            QuicktimeLanguageLookup_[79] = "Lao"
            QuicktimeLanguageLookup_[80] = "Vietnamese"
            QuicktimeLanguageLookup_[81] = "Indonesian"
            QuicktimeLanguageLookup_[82] = "Tagalog"
            QuicktimeLanguageLookup_[83] = "MalayRoman"
            QuicktimeLanguageLookup_[84] = "MalayArabic"
            QuicktimeLanguageLookup_[85] = "Amharic"
            QuicktimeLanguageLookup_[86] = "Tigrinya"
            QuicktimeLanguageLookup_[87] = "Galla"
            QuicktimeLanguageLookup_[87] = "Oromo"
            QuicktimeLanguageLookup_[88] = "Somali"
            QuicktimeLanguageLookup_[89] = "Swahili"
            QuicktimeLanguageLookup_[90] = "Ruanda"
            QuicktimeLanguageLookup_[91] = "Rundi"
            QuicktimeLanguageLookup_[92] = "Chewa"
            QuicktimeLanguageLookup_[93] = "Malagasy"
            QuicktimeLanguageLookup_[94] = "Esperanto"
            QuicktimeLanguageLookup_[128] = "Welsh"
            QuicktimeLanguageLookup_[129] = "Basque"
            QuicktimeLanguageLookup_[130] = "Catalan"
            QuicktimeLanguageLookup_[131] = "Latin"
            QuicktimeLanguageLookup_[132] = "Quechua"
            QuicktimeLanguageLookup_[133] = "Guarani"
            QuicktimeLanguageLookup_[134] = "Aymara"
            QuicktimeLanguageLookup_[135] = "Tatar"
            QuicktimeLanguageLookup_[136] = "Uighur"
            QuicktimeLanguageLookup_[137] = "Dzongkha"
            QuicktimeLanguageLookup_[138] = "JavaneseRom"
            QuicktimeLanguageLookup_[32767] = "Unspecified"
        # end if
        if languageid_ > 138 and languageid_ < 32767:
            #// 
            #// ISO Language Codes - http://www.loc.gov/standards/iso639-2/php/code_list.php
            #// Because the language codes specified by ISO 639-2/T are three characters long, they must be packed to fit into a 16-bit field.
            #// The packing algorithm must map each of the three characters, which are always lowercase, into a 5-bit integer and then concatenate
            #// these integers into the least significant 15 bits of a 16-bit integer, leaving the 16-bit integer's most significant bit set to zero.
            #// One algorithm for performing this packing is to treat each ISO character as a 16-bit integer. Subtract 0x60 from the first character
            #// and multiply by 2^10 (0x400), subtract 0x60 from the second character and multiply by 2^5 (0x20), subtract 0x60 from the third character,
            #// and add the three 16-bit values. This will result in a single 16-bit value with the three codes correctly packed into the 15 least
            #// significant bits and the most significant bit set to zero.
            #//
            iso_language_id_ = ""
            iso_language_id_ += chr(languageid_ & 31744 >> 10 + 96)
            iso_language_id_ += chr(languageid_ & 992 >> 5 + 96)
            iso_language_id_ += chr(languageid_ & 31 >> 0 + 96)
            QuicktimeLanguageLookup_[languageid_] = getid3_id3v2.languagelookup(iso_language_id_)
        # end if
        return QuicktimeLanguageLookup_[languageid_] if (php_isset(lambda : QuicktimeLanguageLookup_[languageid_])) else "invalid"
    # end def quicktimelanguagelookup
    #// 
    #// @param string $codecid
    #// 
    #// @return string
    #//
    def quicktimevideocodeclookup(self, codecid_=None):
        
        
        QuicktimeVideoCodecLookup_ = Array()
        if php_empty(lambda : QuicktimeVideoCodecLookup_):
            QuicktimeVideoCodecLookup_[".SGI"] = "SGI"
            QuicktimeVideoCodecLookup_["3IV1"] = "3ivx MPEG-4 v1"
            QuicktimeVideoCodecLookup_["3IV2"] = "3ivx MPEG-4 v2"
            QuicktimeVideoCodecLookup_["3IVX"] = "3ivx MPEG-4"
            QuicktimeVideoCodecLookup_["8BPS"] = "Planar RGB"
            QuicktimeVideoCodecLookup_["avc1"] = "H.264/MPEG-4 AVC"
            QuicktimeVideoCodecLookup_["avr "] = "AVR-JPEG"
            QuicktimeVideoCodecLookup_["b16g"] = "16Gray"
            QuicktimeVideoCodecLookup_["b32a"] = "32AlphaGray"
            QuicktimeVideoCodecLookup_["b48r"] = "48RGB"
            QuicktimeVideoCodecLookup_["b64a"] = "64ARGB"
            QuicktimeVideoCodecLookup_["base"] = "Base"
            QuicktimeVideoCodecLookup_["clou"] = "Cloud"
            QuicktimeVideoCodecLookup_["cmyk"] = "CMYK"
            QuicktimeVideoCodecLookup_["cvid"] = "Cinepak"
            QuicktimeVideoCodecLookup_["dmb1"] = "OpenDML JPEG"
            QuicktimeVideoCodecLookup_["dvc "] = "DVC-NTSC"
            QuicktimeVideoCodecLookup_["dvcp"] = "DVC-PAL"
            QuicktimeVideoCodecLookup_["dvpn"] = "DVCPro-NTSC"
            QuicktimeVideoCodecLookup_["dvpp"] = "DVCPro-PAL"
            QuicktimeVideoCodecLookup_["fire"] = "Fire"
            QuicktimeVideoCodecLookup_["flic"] = "FLC"
            QuicktimeVideoCodecLookup_["gif "] = "GIF"
            QuicktimeVideoCodecLookup_["h261"] = "H261"
            QuicktimeVideoCodecLookup_["h263"] = "H263"
            QuicktimeVideoCodecLookup_["IV41"] = "Indeo4"
            QuicktimeVideoCodecLookup_["jpeg"] = "JPEG"
            QuicktimeVideoCodecLookup_["kpcd"] = "PhotoCD"
            QuicktimeVideoCodecLookup_["mjpa"] = "Motion JPEG-A"
            QuicktimeVideoCodecLookup_["mjpb"] = "Motion JPEG-B"
            QuicktimeVideoCodecLookup_["msvc"] = "Microsoft Video1"
            QuicktimeVideoCodecLookup_["myuv"] = "MPEG YUV420"
            QuicktimeVideoCodecLookup_["path"] = "Vector"
            QuicktimeVideoCodecLookup_["png "] = "PNG"
            QuicktimeVideoCodecLookup_["PNTG"] = "MacPaint"
            QuicktimeVideoCodecLookup_["qdgx"] = "QuickDrawGX"
            QuicktimeVideoCodecLookup_["qdrw"] = "QuickDraw"
            QuicktimeVideoCodecLookup_["raw "] = "RAW"
            QuicktimeVideoCodecLookup_["ripl"] = "WaterRipple"
            QuicktimeVideoCodecLookup_["rpza"] = "Video"
            QuicktimeVideoCodecLookup_["smc "] = "Graphics"
            QuicktimeVideoCodecLookup_["SVQ1"] = "Sorenson Video 1"
            QuicktimeVideoCodecLookup_["SVQ1"] = "Sorenson Video 3"
            QuicktimeVideoCodecLookup_["syv9"] = "Sorenson YUV9"
            QuicktimeVideoCodecLookup_["tga "] = "Targa"
            QuicktimeVideoCodecLookup_["tiff"] = "TIFF"
            QuicktimeVideoCodecLookup_["WRAW"] = "Windows RAW"
            QuicktimeVideoCodecLookup_["WRLE"] = "BMP"
            QuicktimeVideoCodecLookup_["y420"] = "YUV420"
            QuicktimeVideoCodecLookup_["yuv2"] = "ComponentVideo"
            QuicktimeVideoCodecLookup_["yuvs"] = "ComponentVideoUnsigned"
            QuicktimeVideoCodecLookup_["yuvu"] = "ComponentVideoSigned"
        # end if
        return QuicktimeVideoCodecLookup_[codecid_] if (php_isset(lambda : QuicktimeVideoCodecLookup_[codecid_])) else ""
    # end def quicktimevideocodeclookup
    #// 
    #// @param string $codecid
    #// 
    #// @return mixed|string
    #//
    def quicktimeaudiocodeclookup(self, codecid_=None):
        
        
        QuicktimeAudioCodecLookup_ = Array()
        if php_empty(lambda : QuicktimeAudioCodecLookup_):
            QuicktimeAudioCodecLookup_[".mp3"] = "Fraunhofer MPEG Layer-III alias"
            QuicktimeAudioCodecLookup_["aac "] = "ISO/IEC 14496-3 AAC"
            QuicktimeAudioCodecLookup_["agsm"] = "Apple GSM 10:1"
            QuicktimeAudioCodecLookup_["alac"] = "Apple Lossless Audio Codec"
            QuicktimeAudioCodecLookup_["alaw"] = "A-law 2:1"
            QuicktimeAudioCodecLookup_["conv"] = "Sample Format"
            QuicktimeAudioCodecLookup_["dvca"] = "DV"
            QuicktimeAudioCodecLookup_["dvi "] = "DV 4:1"
            QuicktimeAudioCodecLookup_["eqal"] = "Frequency Equalizer"
            QuicktimeAudioCodecLookup_["fl32"] = "32-bit Floating Point"
            QuicktimeAudioCodecLookup_["fl64"] = "64-bit Floating Point"
            QuicktimeAudioCodecLookup_["ima4"] = "Interactive Multimedia Association 4:1"
            QuicktimeAudioCodecLookup_["in24"] = "24-bit Integer"
            QuicktimeAudioCodecLookup_["in32"] = "32-bit Integer"
            QuicktimeAudioCodecLookup_["lpc "] = "LPC 23:1"
            QuicktimeAudioCodecLookup_["MAC3"] = "Macintosh Audio Compression/Expansion (MACE) 3:1"
            QuicktimeAudioCodecLookup_["MAC6"] = "Macintosh Audio Compression/Expansion (MACE) 6:1"
            QuicktimeAudioCodecLookup_["mixb"] = "8-bit Mixer"
            QuicktimeAudioCodecLookup_["mixw"] = "16-bit Mixer"
            QuicktimeAudioCodecLookup_["mp4a"] = "ISO/IEC 14496-3 AAC"
            QuicktimeAudioCodecLookup_["MS" + " "] = "Microsoft ADPCM"
            QuicktimeAudioCodecLookup_["MS" + " "] = "DV IMA"
            QuicktimeAudioCodecLookup_["MS" + " U"] = "Fraunhofer MPEG Layer III"
            QuicktimeAudioCodecLookup_["NONE"] = "No Encoding"
            QuicktimeAudioCodecLookup_["Qclp"] = "Qualcomm PureVoice"
            QuicktimeAudioCodecLookup_["QDM2"] = "QDesign Music 2"
            QuicktimeAudioCodecLookup_["QDMC"] = "QDesign Music 1"
            QuicktimeAudioCodecLookup_["ratb"] = "8-bit Rate"
            QuicktimeAudioCodecLookup_["ratw"] = "16-bit Rate"
            QuicktimeAudioCodecLookup_["raw "] = "raw PCM"
            QuicktimeAudioCodecLookup_["sour"] = "Sound Source"
            QuicktimeAudioCodecLookup_["sowt"] = "signed/two's complement (Little Endian)"
            QuicktimeAudioCodecLookup_["str1"] = "Iomega MPEG layer II"
            QuicktimeAudioCodecLookup_["str2"] = "Iomega MPEG *layer II"
            QuicktimeAudioCodecLookup_["str3"] = "Iomega MPEG **layer II"
            QuicktimeAudioCodecLookup_["str4"] = "Iomega MPEG ***layer II"
            QuicktimeAudioCodecLookup_["twos"] = "signed/two's complement (Big Endian)"
            QuicktimeAudioCodecLookup_["ulaw"] = "mu-law 2:1"
        # end if
        return QuicktimeAudioCodecLookup_[codecid_] if (php_isset(lambda : QuicktimeAudioCodecLookup_[codecid_])) else ""
    # end def quicktimeaudiocodeclookup
    #// 
    #// @param string $compressionid
    #// 
    #// @return string
    #//
    def quicktimedcomlookup(self, compressionid_=None):
        
        
        QuicktimeDCOMLookup_ = Array()
        if php_empty(lambda : QuicktimeDCOMLookup_):
            QuicktimeDCOMLookup_["zlib"] = "ZLib Deflate"
            QuicktimeDCOMLookup_["adec"] = "Apple Compression"
        # end if
        return QuicktimeDCOMLookup_[compressionid_] if (php_isset(lambda : QuicktimeDCOMLookup_[compressionid_])) else ""
    # end def quicktimedcomlookup
    #// 
    #// @param int $colordepthid
    #// 
    #// @return string
    #//
    def quicktimecolornamelookup(self, colordepthid_=None):
        
        
        QuicktimeColorNameLookup_ = Array()
        if php_empty(lambda : QuicktimeColorNameLookup_):
            QuicktimeColorNameLookup_[1] = "2-color (monochrome)"
            QuicktimeColorNameLookup_[2] = "4-color"
            QuicktimeColorNameLookup_[4] = "16-color"
            QuicktimeColorNameLookup_[8] = "256-color"
            QuicktimeColorNameLookup_[16] = "thousands (16-bit color)"
            QuicktimeColorNameLookup_[24] = "millions (24-bit color)"
            QuicktimeColorNameLookup_[32] = "millions+ (32-bit color)"
            QuicktimeColorNameLookup_[33] = "black & white"
            QuicktimeColorNameLookup_[34] = "4-gray"
            QuicktimeColorNameLookup_[36] = "16-gray"
            QuicktimeColorNameLookup_[40] = "256-gray"
        # end if
        return QuicktimeColorNameLookup_[colordepthid_] if (php_isset(lambda : QuicktimeColorNameLookup_[colordepthid_])) else "invalid"
    # end def quicktimecolornamelookup
    #// 
    #// @param int $stik
    #// 
    #// @return string
    #//
    def quicktimestiklookup(self, stik_=None):
        
        
        QuicktimeSTIKLookup_ = Array()
        if php_empty(lambda : QuicktimeSTIKLookup_):
            QuicktimeSTIKLookup_[0] = "Movie"
            QuicktimeSTIKLookup_[1] = "Normal"
            QuicktimeSTIKLookup_[2] = "Audiobook"
            QuicktimeSTIKLookup_[5] = "Whacked Bookmark"
            QuicktimeSTIKLookup_[6] = "Music Video"
            QuicktimeSTIKLookup_[9] = "Short Film"
            QuicktimeSTIKLookup_[10] = "TV Show"
            QuicktimeSTIKLookup_[11] = "Booklet"
            QuicktimeSTIKLookup_[14] = "Ringtone"
            QuicktimeSTIKLookup_[21] = "Podcast"
        # end if
        return QuicktimeSTIKLookup_[stik_] if (php_isset(lambda : QuicktimeSTIKLookup_[stik_])) else "invalid"
    # end def quicktimestiklookup
    #// 
    #// @param int $audio_profile_id
    #// 
    #// @return string
    #//
    def quicktimeiodsaudioprofilename(self, audio_profile_id_=None):
        
        
        QuicktimeIODSaudioProfileNameLookup_ = Array()
        if php_empty(lambda : QuicktimeIODSaudioProfileNameLookup_):
            QuicktimeIODSaudioProfileNameLookup_ = Array({0: "ISO Reserved (0x00)", 1: "Main Audio Profile @ Level 1", 2: "Main Audio Profile @ Level 2", 3: "Main Audio Profile @ Level 3", 4: "Main Audio Profile @ Level 4", 5: "Scalable Audio Profile @ Level 1", 6: "Scalable Audio Profile @ Level 2", 7: "Scalable Audio Profile @ Level 3", 8: "Scalable Audio Profile @ Level 4", 9: "Speech Audio Profile @ Level 1", 10: "Speech Audio Profile @ Level 2", 11: "Synthetic Audio Profile @ Level 1", 12: "Synthetic Audio Profile @ Level 2", 13: "Synthetic Audio Profile @ Level 3", 14: "High Quality Audio Profile @ Level 1", 15: "High Quality Audio Profile @ Level 2", 16: "High Quality Audio Profile @ Level 3", 17: "High Quality Audio Profile @ Level 4", 18: "High Quality Audio Profile @ Level 5", 19: "High Quality Audio Profile @ Level 6", 20: "High Quality Audio Profile @ Level 7", 21: "High Quality Audio Profile @ Level 8", 22: "Low Delay Audio Profile @ Level 1", 23: "Low Delay Audio Profile @ Level 2", 24: "Low Delay Audio Profile @ Level 3", 25: "Low Delay Audio Profile @ Level 4", 26: "Low Delay Audio Profile @ Level 5", 27: "Low Delay Audio Profile @ Level 6", 28: "Low Delay Audio Profile @ Level 7", 29: "Low Delay Audio Profile @ Level 8", 30: "Natural Audio Profile @ Level 1", 31: "Natural Audio Profile @ Level 2", 32: "Natural Audio Profile @ Level 3", 33: "Natural Audio Profile @ Level 4", 34: "Mobile Audio Internetworking Profile @ Level 1", 35: "Mobile Audio Internetworking Profile @ Level 2", 36: "Mobile Audio Internetworking Profile @ Level 3", 37: "Mobile Audio Internetworking Profile @ Level 4", 38: "Mobile Audio Internetworking Profile @ Level 5", 39: "Mobile Audio Internetworking Profile @ Level 6", 40: "AAC Profile @ Level 1", 41: "AAC Profile @ Level 2", 42: "AAC Profile @ Level 4", 43: "AAC Profile @ Level 5", 44: "High Efficiency AAC Profile @ Level 2", 45: "High Efficiency AAC Profile @ Level 3", 46: "High Efficiency AAC Profile @ Level 4", 47: "High Efficiency AAC Profile @ Level 5", 254: "Not part of MPEG-4 audio profiles", 255: "No audio capability required"})
        # end if
        return QuicktimeIODSaudioProfileNameLookup_[audio_profile_id_] if (php_isset(lambda : QuicktimeIODSaudioProfileNameLookup_[audio_profile_id_])) else "ISO Reserved / User Private"
    # end def quicktimeiodsaudioprofilename
    #// 
    #// @param int $video_profile_id
    #// 
    #// @return string
    #//
    def quicktimeiodsvideoprofilename(self, video_profile_id_=None):
        
        
        QuicktimeIODSvideoProfileNameLookup_ = Array()
        if php_empty(lambda : QuicktimeIODSvideoProfileNameLookup_):
            QuicktimeIODSvideoProfileNameLookup_ = Array({0: "Reserved (0x00) Profile", 1: "Simple Profile @ Level 1", 2: "Simple Profile @ Level 2", 3: "Simple Profile @ Level 3", 8: "Simple Profile @ Level 0", 16: "Simple Scalable Profile @ Level 0", 17: "Simple Scalable Profile @ Level 1", 18: "Simple Scalable Profile @ Level 2", 21: "AVC/H264 Profile", 33: "Core Profile @ Level 1", 34: "Core Profile @ Level 2", 50: "Main Profile @ Level 2", 51: "Main Profile @ Level 3", 52: "Main Profile @ Level 4", 66: "N-bit Profile @ Level 2", 81: "Scalable Texture Profile @ Level 1", 97: "Simple Face Animation Profile @ Level 1", 98: "Simple Face Animation Profile @ Level 2", 99: "Simple FBA Profile @ Level 1", 100: "Simple FBA Profile @ Level 2", 113: "Basic Animated Texture Profile @ Level 1", 114: "Basic Animated Texture Profile @ Level 2", 129: "Hybrid Profile @ Level 1", 130: "Hybrid Profile @ Level 2", 145: "Advanced Real Time Simple Profile @ Level 1", 146: "Advanced Real Time Simple Profile @ Level 2", 147: "Advanced Real Time Simple Profile @ Level 3", 148: "Advanced Real Time Simple Profile @ Level 4", 161: "Core Scalable Profile @ Level1", 162: "Core Scalable Profile @ Level2", 163: "Core Scalable Profile @ Level3", 177: "Advanced Coding Efficiency Profile @ Level 1", 178: "Advanced Coding Efficiency Profile @ Level 2", 179: "Advanced Coding Efficiency Profile @ Level 3", 180: "Advanced Coding Efficiency Profile @ Level 4", 193: "Advanced Core Profile @ Level 1", 194: "Advanced Core Profile @ Level 2", 209: "Advanced Scalable Texture @ Level1", 210: "Advanced Scalable Texture @ Level2", 225: "Simple Studio Profile @ Level 1", 226: "Simple Studio Profile @ Level 2", 227: "Simple Studio Profile @ Level 3", 228: "Simple Studio Profile @ Level 4", 229: "Core Studio Profile @ Level 1", 230: "Core Studio Profile @ Level 2", 231: "Core Studio Profile @ Level 3", 232: "Core Studio Profile @ Level 4", 240: "Advanced Simple Profile @ Level 0", 241: "Advanced Simple Profile @ Level 1", 242: "Advanced Simple Profile @ Level 2", 243: "Advanced Simple Profile @ Level 3", 244: "Advanced Simple Profile @ Level 4", 245: "Advanced Simple Profile @ Level 5", 247: "Advanced Simple Profile @ Level 3b", 248: "Fine Granularity Scalable Profile @ Level 0", 249: "Fine Granularity Scalable Profile @ Level 1", 250: "Fine Granularity Scalable Profile @ Level 2", 251: "Fine Granularity Scalable Profile @ Level 3", 252: "Fine Granularity Scalable Profile @ Level 4", 253: "Fine Granularity Scalable Profile @ Level 5", 254: "Not part of MPEG-4 Visual profiles", 255: "No visual capability required"})
        # end if
        return QuicktimeIODSvideoProfileNameLookup_[video_profile_id_] if (php_isset(lambda : QuicktimeIODSvideoProfileNameLookup_[video_profile_id_])) else "ISO Reserved Profile"
    # end def quicktimeiodsvideoprofilename
    #// 
    #// @param int $rtng
    #// 
    #// @return string
    #//
    def quicktimecontentratinglookup(self, rtng_=None):
        
        
        QuicktimeContentRatingLookup_ = Array()
        if php_empty(lambda : QuicktimeContentRatingLookup_):
            QuicktimeContentRatingLookup_[0] = "None"
            QuicktimeContentRatingLookup_[2] = "Clean"
            QuicktimeContentRatingLookup_[4] = "Explicit"
        # end if
        return QuicktimeContentRatingLookup_[rtng_] if (php_isset(lambda : QuicktimeContentRatingLookup_[rtng_])) else "invalid"
    # end def quicktimecontentratinglookup
    #// 
    #// @param int $akid
    #// 
    #// @return string
    #//
    def quicktimestoreaccounttypelookup(self, akid_=None):
        
        
        QuicktimeStoreAccountTypeLookup_ = Array()
        if php_empty(lambda : QuicktimeStoreAccountTypeLookup_):
            QuicktimeStoreAccountTypeLookup_[0] = "iTunes"
            QuicktimeStoreAccountTypeLookup_[1] = "AOL"
        # end if
        return QuicktimeStoreAccountTypeLookup_[akid_] if (php_isset(lambda : QuicktimeStoreAccountTypeLookup_[akid_])) else "invalid"
    # end def quicktimestoreaccounttypelookup
    #// 
    #// @param int $sfid
    #// 
    #// @return string
    #//
    def quicktimestorefrontcodelookup(self, sfid_=None):
        
        
        QuicktimeStoreFrontCodeLookup_ = Array()
        if php_empty(lambda : QuicktimeStoreFrontCodeLookup_):
            QuicktimeStoreFrontCodeLookup_[143460] = "Australia"
            QuicktimeStoreFrontCodeLookup_[143445] = "Austria"
            QuicktimeStoreFrontCodeLookup_[143446] = "Belgium"
            QuicktimeStoreFrontCodeLookup_[143455] = "Canada"
            QuicktimeStoreFrontCodeLookup_[143458] = "Denmark"
            QuicktimeStoreFrontCodeLookup_[143447] = "Finland"
            QuicktimeStoreFrontCodeLookup_[143442] = "France"
            QuicktimeStoreFrontCodeLookup_[143443] = "Germany"
            QuicktimeStoreFrontCodeLookup_[143448] = "Greece"
            QuicktimeStoreFrontCodeLookup_[143449] = "Ireland"
            QuicktimeStoreFrontCodeLookup_[143450] = "Italy"
            QuicktimeStoreFrontCodeLookup_[143462] = "Japan"
            QuicktimeStoreFrontCodeLookup_[143451] = "Luxembourg"
            QuicktimeStoreFrontCodeLookup_[143452] = "Netherlands"
            QuicktimeStoreFrontCodeLookup_[143461] = "New Zealand"
            QuicktimeStoreFrontCodeLookup_[143457] = "Norway"
            QuicktimeStoreFrontCodeLookup_[143453] = "Portugal"
            QuicktimeStoreFrontCodeLookup_[143454] = "Spain"
            QuicktimeStoreFrontCodeLookup_[143456] = "Sweden"
            QuicktimeStoreFrontCodeLookup_[143459] = "Switzerland"
            QuicktimeStoreFrontCodeLookup_[143444] = "United Kingdom"
            QuicktimeStoreFrontCodeLookup_[143441] = "United States"
        # end if
        return QuicktimeStoreFrontCodeLookup_[sfid_] if (php_isset(lambda : QuicktimeStoreFrontCodeLookup_[sfid_])) else "invalid"
    # end def quicktimestorefrontcodelookup
    #// 
    #// @param string $atom_data
    #// 
    #// @return array
    #//
    def quicktimeparsenikonnctg(self, atom_data_=None):
        
        
        #// http://www.sno.phy.queensu.ca/~phil/exiftool/TagNames/Nikon.html#NCTG
        #// Nikon-specific QuickTime tags found in the NCDT atom of MOV videos from some Nikon cameras such as the Coolpix S8000 and D5100
        #// Data is stored as records of:
        #// 4 bytes record type
        #// 2 bytes size of data field type:
        #// 0x0001 = flag   (size field *= 1-byte)
        #// 0x0002 = char   (size field *= 1-byte)
        #// 0x0003 = DWORD+ (size field *= 2-byte), values are stored CDAB
        #// 0x0004 = QWORD+ (size field *= 4-byte), values are stored EFGHABCD
        #// 0x0005 = float  (size field *= 8-byte), values are stored aaaabbbb where value is aaaa/bbbb; possibly multiple sets of values appended together
        #// 0x0007 = bytes  (size field *= 1-byte), values are stored as ??????
        #// 0x0008 = ?????  (size field *= 2-byte), values are stored as ??????
        #// 2 bytes data size field
        #// ? bytes data (string data may be null-padded; datestamp fields are in the format "2011:05:25 20:24:15")
        #// all integers are stored BigEndian
        NCTGtagName_ = Array({1: "Make", 2: "Model", 3: "Software", 17: "CreateDate", 18: "DateTimeOriginal", 19: "FrameCount", 22: "FrameRate", 34: "FrameWidth", 35: "FrameHeight", 50: "AudioChannels", 51: "AudioBitsPerSample", 52: "AudioSampleRate", 33554433: "MakerNoteVersion", 33554437: "WhiteBalance", 33554443: "WhiteBalanceFineTune", 33554462: "ColorSpace", 33554467: "PictureControlData", 33554468: "WorldTime", 33554482: "UnknownInfo", 33554563: "LensType", 33554564: "Lens"})
        offset_ = 0
        data_ = None
        datalength_ = php_strlen(atom_data_)
        parsed_ = Array()
        while True:
            
            if not (offset_ < datalength_):
                break
            # end if
            record_type_ = getid3_lib.bigendian2int(php_substr(atom_data_, offset_, 4))
            offset_ += 4
            data_size_type_ = getid3_lib.bigendian2int(php_substr(atom_data_, offset_, 2))
            offset_ += 2
            data_size_ = getid3_lib.bigendian2int(php_substr(atom_data_, offset_, 2))
            offset_ += 2
            for case in Switch(data_size_type_):
                if case(1):
                    #// 0x0001 = flag   (size field *= 1-byte)
                    data_ = getid3_lib.bigendian2int(php_substr(atom_data_, offset_, data_size_ * 1))
                    offset_ += data_size_ * 1
                    break
                # end if
                if case(2):
                    #// 0x0002 = char   (size field *= 1-byte)
                    data_ = php_substr(atom_data_, offset_, data_size_ * 1)
                    offset_ += data_size_ * 1
                    data_ = php_rtrim(data_, " ")
                    break
                # end if
                if case(3):
                    #// 0x0003 = DWORD+ (size field *= 2-byte), values are stored CDAB
                    data_ = ""
                    i_ = data_size_ - 1
                    while i_ >= 0:
                        
                        data_ += php_substr(atom_data_, offset_ + i_ * 2, 2)
                        i_ -= 1
                    # end while
                    data_ = getid3_lib.bigendian2int(data_)
                    offset_ += data_size_ * 2
                    break
                # end if
                if case(4):
                    #// 0x0004 = QWORD+ (size field *= 4-byte), values are stored EFGHABCD
                    data_ = ""
                    i_ = data_size_ - 1
                    while i_ >= 0:
                        
                        data_ += php_substr(atom_data_, offset_ + i_ * 4, 4)
                        i_ -= 1
                    # end while
                    data_ = getid3_lib.bigendian2int(data_)
                    offset_ += data_size_ * 4
                    break
                # end if
                if case(5):
                    #// 0x0005 = float  (size field *= 8-byte), values are stored aaaabbbb where value is aaaa/bbbb; possibly multiple sets of values appended together
                    data_ = Array()
                    i_ = 0
                    while i_ < data_size_:
                        
                        numerator_ = getid3_lib.bigendian2int(php_substr(atom_data_, offset_ + i_ * 8 + 0, 4))
                        denomninator_ = getid3_lib.bigendian2int(php_substr(atom_data_, offset_ + i_ * 8 + 4, 4))
                        if denomninator_ == 0:
                            data_[i_] = False
                        else:
                            data_[i_] = php_float(numerator_) / denomninator_
                        # end if
                        i_ += 1
                    # end while
                    offset_ += 8 * data_size_
                    if php_count(data_) == 1:
                        data_ = data_[0]
                    # end if
                    break
                # end if
                if case(7):
                    #// 0x0007 = bytes  (size field *= 1-byte), values are stored as ??????
                    data_ = php_substr(atom_data_, offset_, data_size_ * 1)
                    offset_ += data_size_ * 1
                    break
                # end if
                if case(8):
                    #// 0x0008 = ?????  (size field *= 2-byte), values are stored as ??????
                    data_ = php_substr(atom_data_, offset_, data_size_ * 2)
                    offset_ += data_size_ * 2
                    break
                # end if
                if case():
                    php_print("QuicktimeParseNikonNCTG()::unknown $data_size_type: " + data_size_type_ + "<br>")
                    break
                # end if
            # end for
            for case in Switch(record_type_):
                if case(17):
                    pass
                # end if
                if case(18):
                    #// DateTimeOriginal
                    data_ = strtotime(data_)
                    break
                # end if
                if case(33554462):
                    #// ColorSpace
                    for case in Switch(data_):
                        if case(1):
                            data_ = "sRGB"
                            break
                        # end if
                        if case(2):
                            data_ = "Adobe RGB"
                            break
                        # end if
                    # end for
                    break
                # end if
                if case(33554467):
                    #// PictureControlData
                    PictureControlAdjust_ = Array({0: "default", 1: "quick", 2: "full"})
                    FilterEffect_ = Array({128: "off", 129: "yellow", 130: "orange", 131: "red", 132: "green", 255: "n/a"})
                    ToningEffect_ = Array({128: "b&w", 129: "sepia", 130: "cyanotype", 131: "red", 132: "yellow", 133: "green", 134: "blue-green", 135: "blue", 136: "purple-blue", 137: "red-purple", 255: "n/a"})
                    data_ = Array({"PictureControlVersion": php_substr(data_, 0, 4), "PictureControlName": php_rtrim(php_substr(data_, 4, 20), " "), "PictureControlBase": php_rtrim(php_substr(data_, 24, 20), " "), "PictureControlAdjust": PictureControlAdjust_[php_ord(php_substr(data_, 48, 1))], "PictureControlQuickAdjust": php_ord(php_substr(data_, 49, 1)), "Sharpness": php_ord(php_substr(data_, 50, 1)), "Contrast": php_ord(php_substr(data_, 51, 1)), "Brightness": php_ord(php_substr(data_, 52, 1)), "Saturation": php_ord(php_substr(data_, 53, 1)), "HueAdjustment": php_ord(php_substr(data_, 54, 1)), "FilterEffect": FilterEffect_[php_ord(php_substr(data_, 55, 1))], "ToningEffect": ToningEffect_[php_ord(php_substr(data_, 56, 1))], "ToningSaturation": php_ord(php_substr(data_, 57, 1))})
                    break
                # end if
                if case(33554468):
                    #// WorldTime
                    #// http://www.sno.phy.queensu.ca/~phil/exiftool/TagNames/Nikon.html#WorldTime
                    #// timezone is stored as offset from GMT in minutes
                    timezone_ = getid3_lib.bigendian2int(php_substr(data_, 0, 2))
                    if timezone_ & 32768:
                        timezone_ = 0 - 65536 - timezone_
                    # end if
                    timezone_ /= 60
                    dst_ = php_bool(getid3_lib.bigendian2int(php_substr(data_, 2, 1)))
                    for case in Switch(getid3_lib.bigendian2int(php_substr(data_, 3, 1))):
                        if case(2):
                            datedisplayformat_ = "D/M/Y"
                            break
                        # end if
                        if case(1):
                            datedisplayformat_ = "M/D/Y"
                            break
                        # end if
                        if case(0):
                            pass
                        # end if
                        if case():
                            datedisplayformat_ = "Y/M/D"
                            break
                        # end if
                    # end for
                    data_ = Array({"timezone": floatval(timezone_), "dst": dst_, "display": datedisplayformat_})
                    break
                # end if
                if case(33554563):
                    #// LensType
                    data_ = Array({"mf": php_bool(data_ & 1), "d": php_bool(data_ & 2), "g": php_bool(data_ & 4), "vr": php_bool(data_ & 8)})
                    break
                # end if
            # end for
            tag_name_ = NCTGtagName_[record_type_] if (php_isset(lambda : NCTGtagName_[record_type_])) else "0x" + php_str_pad(dechex(record_type_), 8, "0", STR_PAD_LEFT)
            parsed_[tag_name_] = data_
        # end while
        return parsed_
    # end def quicktimeparsenikonnctg
    #// 
    #// @param string $keyname
    #// @param string|array $data
    #// @param string $boxname
    #// 
    #// @return bool
    #//
    def copytoappropriatecommentssection(self, keyname_=None, data_=None, boxname_=""):
        
        
        handyatomtranslatorarray_ = Array()
        if php_empty(lambda : handyatomtranslatorarray_):
            #// http://www.geocities.com/xhelmboyx/quicktime/formats/qtm-layout.txt
            #// http://www.geocities.com/xhelmboyx/quicktime/formats/mp4-layout.txt
            #// http://atomicparsley.sourceforge.net/mpeg-4files.html
            #// https://code.google.com/p/mp4v2/wiki/iTunesMetadata
            handyatomtranslatorarray_["©" + "alb"] = "album"
            #// iTunes 4.0
            handyatomtranslatorarray_["©" + "ART"] = "artist"
            handyatomtranslatorarray_["©" + "art"] = "artist"
            #// iTunes 4.0
            handyatomtranslatorarray_["©" + "aut"] = "author"
            handyatomtranslatorarray_["©" + "cmt"] = "comment"
            #// iTunes 4.0
            handyatomtranslatorarray_["©" + "com"] = "comment"
            handyatomtranslatorarray_["©" + "cpy"] = "copyright"
            handyatomtranslatorarray_["©" + "day"] = "creation_date"
            #// iTunes 4.0
            handyatomtranslatorarray_["©" + "dir"] = "director"
            handyatomtranslatorarray_["©" + "ed1"] = "edit1"
            handyatomtranslatorarray_["©" + "ed2"] = "edit2"
            handyatomtranslatorarray_["©" + "ed3"] = "edit3"
            handyatomtranslatorarray_["©" + "ed4"] = "edit4"
            handyatomtranslatorarray_["©" + "ed5"] = "edit5"
            handyatomtranslatorarray_["©" + "ed6"] = "edit6"
            handyatomtranslatorarray_["©" + "ed7"] = "edit7"
            handyatomtranslatorarray_["©" + "ed8"] = "edit8"
            handyatomtranslatorarray_["©" + "ed9"] = "edit9"
            handyatomtranslatorarray_["©" + "enc"] = "encoded_by"
            handyatomtranslatorarray_["©" + "fmt"] = "format"
            handyatomtranslatorarray_["©" + "gen"] = "genre"
            #// iTunes 4.0
            handyatomtranslatorarray_["©" + "grp"] = "grouping"
            #// iTunes 4.2
            handyatomtranslatorarray_["©" + "hst"] = "host_computer"
            handyatomtranslatorarray_["©" + "inf"] = "information"
            handyatomtranslatorarray_["©" + "lyr"] = "lyrics"
            #// iTunes 5.0
            handyatomtranslatorarray_["©" + "mak"] = "make"
            handyatomtranslatorarray_["©" + "mod"] = "model"
            handyatomtranslatorarray_["©" + "nam"] = "title"
            #// iTunes 4.0
            handyatomtranslatorarray_["©" + "ope"] = "composer"
            handyatomtranslatorarray_["©" + "prd"] = "producer"
            handyatomtranslatorarray_["©" + "PRD"] = "product"
            handyatomtranslatorarray_["©" + "prf"] = "performers"
            handyatomtranslatorarray_["©" + "req"] = "system_requirements"
            handyatomtranslatorarray_["©" + "src"] = "source_credit"
            handyatomtranslatorarray_["©" + "swr"] = "software"
            handyatomtranslatorarray_["©" + "too"] = "encoding_tool"
            #// iTunes 4.0
            handyatomtranslatorarray_["©" + "trk"] = "track_number"
            handyatomtranslatorarray_["©" + "url"] = "url"
            handyatomtranslatorarray_["©" + "wrn"] = "warning"
            handyatomtranslatorarray_["©" + "wrt"] = "composer"
            handyatomtranslatorarray_["aART"] = "album_artist"
            handyatomtranslatorarray_["apID"] = "purchase_account"
            handyatomtranslatorarray_["catg"] = "category"
            #// iTunes 4.9
            handyatomtranslatorarray_["covr"] = "picture"
            #// iTunes 4.0
            handyatomtranslatorarray_["cpil"] = "compilation"
            #// iTunes 4.0
            handyatomtranslatorarray_["cprt"] = "copyright"
            #// iTunes 4.0?
            handyatomtranslatorarray_["desc"] = "description"
            #// iTunes 5.0
            handyatomtranslatorarray_["disk"] = "disc_number"
            #// iTunes 4.0
            handyatomtranslatorarray_["egid"] = "episode_guid"
            #// iTunes 4.9
            handyatomtranslatorarray_["gnre"] = "genre"
            #// iTunes 4.0
            handyatomtranslatorarray_["hdvd"] = "hd_video"
            #// iTunes 4.0
            handyatomtranslatorarray_["ldes"] = "description_long"
            #//
            handyatomtranslatorarray_["keyw"] = "keyword"
            #// iTunes 4.9
            handyatomtranslatorarray_["pcst"] = "podcast"
            #// iTunes 4.9
            handyatomtranslatorarray_["pgap"] = "gapless_playback"
            #// iTunes 7.0
            handyatomtranslatorarray_["purd"] = "purchase_date"
            #// iTunes 6.0.2
            handyatomtranslatorarray_["purl"] = "podcast_url"
            #// iTunes 4.9
            handyatomtranslatorarray_["rtng"] = "rating"
            #// iTunes 4.0
            handyatomtranslatorarray_["soaa"] = "sort_album_artist"
            #//
            handyatomtranslatorarray_["soal"] = "sort_album"
            #//
            handyatomtranslatorarray_["soar"] = "sort_artist"
            #//
            handyatomtranslatorarray_["soco"] = "sort_composer"
            #//
            handyatomtranslatorarray_["sonm"] = "sort_title"
            #//
            handyatomtranslatorarray_["sosn"] = "sort_show"
            #//
            handyatomtranslatorarray_["stik"] = "stik"
            #// iTunes 4.9
            handyatomtranslatorarray_["tmpo"] = "bpm"
            #// iTunes 4.0
            handyatomtranslatorarray_["trkn"] = "track_number"
            #// iTunes 4.0
            handyatomtranslatorarray_["tven"] = "tv_episode_id"
            #//
            handyatomtranslatorarray_["tves"] = "tv_episode"
            #// iTunes 6.0
            handyatomtranslatorarray_["tvnn"] = "tv_network_name"
            #// iTunes 6.0
            handyatomtranslatorarray_["tvsh"] = "tv_show_name"
            #// iTunes 6.0
            handyatomtranslatorarray_["tvsn"] = "tv_season"
            pass
        # end if
        info_ = self.getid3.info
        comment_key_ = ""
        if boxname_ and boxname_ != keyname_:
            comment_key_ = handyatomtranslatorarray_[boxname_] if (php_isset(lambda : handyatomtranslatorarray_[boxname_])) else boxname_
        elif (php_isset(lambda : handyatomtranslatorarray_[keyname_])):
            comment_key_ = handyatomtranslatorarray_[keyname_]
        # end if
        if comment_key_:
            if comment_key_ == "picture":
                if (not php_is_array(data_)):
                    image_mime_ = ""
                    if php_preg_match("#^\\x89\\x50\\x4E\\x47\\x0D\\x0A\\x1A\\x0A#", data_):
                        image_mime_ = "image/png"
                    elif php_preg_match("#^\\xFF\\xD8\\xFF#", data_):
                        image_mime_ = "image/jpeg"
                    elif php_preg_match("#^GIF#", data_):
                        image_mime_ = "image/gif"
                    elif php_preg_match("#^BM#", data_):
                        image_mime_ = "image/bmp"
                    # end if
                    data_ = Array({"data": data_, "image_mime": image_mime_})
                # end if
            # end if
            gooddata_ = Array(data_)
            if comment_key_ == "genre":
                #// some other taggers separate multiple genres with semicolon, e.g. "Heavy Metal;Thrash Metal;Metal"
                gooddata_ = php_explode(";", data_)
            # end if
            for data_ in gooddata_:
                info_["quicktime"]["comments"][comment_key_][-1] = data_
            # end for
        # end if
        return True
    # end def copytoappropriatecommentssection
    #// 
    #// @param string $lstring
    #// @param int    $count
    #// 
    #// @return string
    #//
    def locistring(self, lstring_=None, count_=None):
        
        
        #// Loci strings are UTF-8 or UTF-16 and null (x00/x0000) terminated. UTF-16 has a BOM
        #// Also need to return the number of bytes the string occupied so additional fields can be extracted
        len_ = php_strlen(lstring_)
        if len_ == 0:
            count_ = 0
            return ""
        # end if
        if lstring_[0] == " ":
            count_ = 1
            return ""
        # end if
        #// check for BOM
        if len_ > 2 and lstring_[0] == "þ" and lstring_[1] == "ÿ" or lstring_[0] == "ÿ" and lstring_[1] == "þ":
            #// UTF-16
            if php_preg_match("/(.*)\\x00/", lstring_, lmatches_):
                count_ = php_strlen(lmatches_[1]) * 2 + 2
                #// account for 2 byte characters and trailing \x0000
                return getid3_lib.iconv_fallback_utf16_utf8(lmatches_[1])
            else:
                return ""
            # end if
        # end if
        #// UTF-8
        if php_preg_match("/(.*)\\x00/", lstring_, lmatches_):
            count_ = php_strlen(lmatches_[1]) + 1
            #// account for trailing \x00
            return lmatches_[1]
        # end if
        return ""
    # end def locistring
    #// 
    #// @param string $nullterminatedstring
    #// 
    #// @return string
    #//
    def nonullstring(self, nullterminatedstring_=None):
        
        
        #// remove the single null terminator on null terminated strings
        if php_substr(nullterminatedstring_, php_strlen(nullterminatedstring_) - 1, 1) == " ":
            return php_substr(nullterminatedstring_, 0, php_strlen(nullterminatedstring_) - 1)
        # end if
        return nullterminatedstring_
    # end def nonullstring
    #// 
    #// @param string $pascalstring
    #// 
    #// @return string
    #//
    def pascal2string(self, pascalstring_=None):
        
        
        #// Pascal strings have 1 unsigned byte at the beginning saying how many chars (1-255) are in the string
        return php_substr(pascalstring_, 1)
    # end def pascal2string
    #// 
    #// Helper functions for m4b audiobook chapters
    #// code by Steffen Hartmann 2015-Nov-08.
    #// 
    #// @param array  $info
    #// @param string $tag
    #// @param string $history
    #// @param array  $result
    #//
    def search_tag_by_key(self, info_=None, tag_=None, history_=None, result_=None):
        
        
        for key_,value_ in info_:
            key_history_ = history_ + "/" + key_
            if key_ == tag_:
                result_[-1] = Array(key_history_, info_)
            else:
                if php_is_array(value_):
                    self.search_tag_by_key(value_, tag_, key_history_, result_)
                # end if
            # end if
        # end for
    # end def search_tag_by_key
    #// 
    #// @param array  $info
    #// @param string $k
    #// @param string $v
    #// @param string $history
    #// @param array  $result
    #//
    def search_tag_by_pair(self, info_=None, k_=None, v_=None, history_=None, result_=None):
        
        
        for key_,value_ in info_:
            key_history_ = history_ + "/" + key_
            if key_ == k_ and value_ == v_:
                result_[-1] = Array(key_history_, info_)
            else:
                if php_is_array(value_):
                    self.search_tag_by_pair(value_, k_, v_, key_history_, result_)
                # end if
            # end if
        # end for
    # end def search_tag_by_pair
    #// 
    #// @param array $info
    #// 
    #// @return array
    #//
    def quicktime_time_to_sample_table(self, info_=None):
        
        
        res_ = Array()
        self.search_tag_by_pair(info_["quicktime"]["moov"], "name", "stbl", "quicktime/moov", res_)
        for value_ in res_:
            stbl_res_ = Array()
            self.search_tag_by_pair(value_[1], "data_format", "text", value_[0], stbl_res_)
            if php_count(stbl_res_) > 0:
                stts_res_ = Array()
                self.search_tag_by_key(value_[1], "time_to_sample_table", value_[0], stts_res_)
                if php_count(stts_res_) > 0:
                    return stts_res_[0][1]["time_to_sample_table"]
                # end if
            # end if
        # end for
        return Array()
    # end def quicktime_time_to_sample_table
    #// 
    #// @param array $info
    #// 
    #// @return int
    #//
    def quicktime_bookmark_time_scale(self, info_=None):
        
        
        time_scale_ = ""
        ts_prefix_len_ = 0
        res_ = Array()
        self.search_tag_by_pair(info_["quicktime"]["moov"], "name", "stbl", "quicktime/moov", res_)
        for value_ in res_:
            stbl_res_ = Array()
            self.search_tag_by_pair(value_[1], "data_format", "text", value_[0], stbl_res_)
            if php_count(stbl_res_) > 0:
                ts_res_ = Array()
                self.search_tag_by_key(info_["quicktime"]["moov"], "time_scale", "quicktime/moov", ts_res_)
                for sub_value_ in ts_res_:
                    prefix_ = php_substr(sub_value_[0], 0, -12)
                    if php_substr(stbl_res_[0][0], 0, php_strlen(prefix_)) == prefix_ and ts_prefix_len_ < php_strlen(prefix_):
                        time_scale_ = sub_value_[1]["time_scale"]
                        ts_prefix_len_ = php_strlen(prefix_)
                    # end if
                # end for
            # end if
        # end for
        return time_scale_
    # end def quicktime_bookmark_time_scale
    pass
# end class getid3_quicktime
