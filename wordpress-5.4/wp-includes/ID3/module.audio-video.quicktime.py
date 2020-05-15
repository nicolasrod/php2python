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
        
        info = self.getid3.info
        info["fileformat"] = "quicktime"
        info["quicktime"]["hinting"] = False
        info["quicktime"]["controller"] = "standard"
        #// may be overridden if 'ctyp' atom is present
        self.fseek(info["avdataoffset"])
        offset = 0
        atomcounter = 0
        atom_data_read_buffer_size = round(info["php_memory_limit"] / 4) if info["php_memory_limit"] else self.getid3.option_fread_buffer_size * 1024
        #// set read buffer to 25% of PHP memory limit (if one is specified), otherwise use option_fread_buffer_size [default: 32MB]
        while True:
            
            if not (offset < info["avdataend"]):
                break
            # end if
            if (not getid3_lib.intvaluesupported(offset)):
                self.error("Unable to parse atom at offset " + offset + " because beyond " + round(PHP_INT_MAX / 1073741824) + "GB limit of PHP filesystem functions")
                break
            # end if
            self.fseek(offset)
            AtomHeader = self.fread(8)
            atomsize = getid3_lib.bigendian2int(php_substr(AtomHeader, 0, 4))
            atomname = php_substr(AtomHeader, 4, 4)
            #// 64-bit MOV patch by jlegateØktnc*com
            if atomsize == 1:
                atomsize = getid3_lib.bigendian2int(self.fread(8))
            # end if
            info["quicktime"][atomname]["name"] = atomname
            info["quicktime"][atomname]["size"] = atomsize
            info["quicktime"][atomname]["offset"] = offset
            if offset + atomsize > info["avdataend"]:
                self.error("Atom at offset " + offset + " claims to go beyond end-of-file (length: " + atomsize + " bytes)")
                return False
            # end if
            if atomsize == 0:
                break
            # end if
            atomHierarchy = Array()
            info["quicktime"][atomname] = self.quicktimeparseatom(atomname, atomsize, self.fread(php_min(atomsize, atom_data_read_buffer_size)), offset, atomHierarchy, self.ParseAllPossibleAtoms)
            offset += atomsize
            atomcounter += 1
        # end while
        if (not php_empty(lambda : info["avdataend_tmp"])):
            #// this value is assigned to a temp value and then erased because
            #// otherwise any atoms beyond the 'mdat' atom would not get parsed
            info["avdataend"] = info["avdataend_tmp"]
            info["avdataend_tmp"] = None
        # end if
        if (not php_empty(lambda : info["quicktime"]["comments"]["chapters"])) and php_is_array(info["quicktime"]["comments"]["chapters"]) and php_count(info["quicktime"]["comments"]["chapters"]) > 0:
            durations = self.quicktime_time_to_sample_table(info)
            i = 0
            while i < php_count(info["quicktime"]["comments"]["chapters"]):
                
                bookmark = Array()
                bookmark["title"] = info["quicktime"]["comments"]["chapters"][i]
                if (php_isset(lambda : durations[i])):
                    bookmark["duration_sample"] = durations[i]["sample_duration"]
                    if i > 0:
                        bookmark["start_sample"] = info["quicktime"]["bookmarks"][i - 1]["start_sample"] + info["quicktime"]["bookmarks"][i - 1]["duration_sample"]
                    else:
                        bookmark["start_sample"] = 0
                    # end if
                    time_scale = self.quicktime_bookmark_time_scale(info)
                    if time_scale:
                        bookmark["duration_seconds"] = bookmark["duration_sample"] / time_scale
                        bookmark["start_seconds"] = bookmark["start_sample"] / time_scale
                    # end if
                # end if
                info["quicktime"]["bookmarks"][-1] = bookmark
                i += 1
            # end while
        # end if
        if (php_isset(lambda : info["quicktime"]["temp_meta_key_names"])):
            info["quicktime"]["temp_meta_key_names"] = None
        # end if
        if (not php_empty(lambda : info["quicktime"]["comments"]["location.ISO6709"])):
            #// https://en.wikipedia.org/wiki/ISO_6709
            for ISO6709string in info["quicktime"]["comments"]["location.ISO6709"]:
                latitude = False
                longitude = False
                altitude = False
                if php_preg_match("#^([\\+\\-])([0-9]{2}|[0-9]{4}|[0-9]{6})(\\.[0-9]+)?([\\+\\-])([0-9]{3}|[0-9]{5}|[0-9]{7})(\\.[0-9]+)?(([\\+\\-])([0-9]{3}|[0-9]{5}|[0-9]{7})(\\.[0-9]+)?)?/$#", ISO6709string, matches):
                    php_no_error(lambda: dummy, lat_sign, lat_deg, lat_deg_dec, lon_sign, lon_deg, lon_deg_dec, dummy, alt_sign, alt_deg, alt_deg_dec = matches)
                    if php_strlen(lat_deg) == 2:
                        #// [+-]DD.D
                        latitude = floatval(php_ltrim(lat_deg, "0") + lat_deg_dec)
                    elif php_strlen(lat_deg) == 4:
                        #// [+-]DDMM.M
                        latitude = floatval(php_ltrim(php_substr(lat_deg, 0, 2), "0")) + floatval(php_ltrim(php_substr(lat_deg, 2, 2), "0") + lat_deg_dec / 60)
                    elif php_strlen(lat_deg) == 6:
                        #// [+-]DDMMSS.S
                        latitude = floatval(php_ltrim(php_substr(lat_deg, 0, 2), "0")) + floatval(php_ltrim(php_substr(lat_deg, 2, 2), "0") / 60) + floatval(php_ltrim(php_substr(lat_deg, 4, 2), "0") + lat_deg_dec / 3600)
                    # end if
                    if php_strlen(lon_deg) == 3:
                        #// [+-]DDD.D
                        longitude = floatval(php_ltrim(lon_deg, "0") + lon_deg_dec)
                    elif php_strlen(lon_deg) == 5:
                        #// [+-]DDDMM.M
                        longitude = floatval(php_ltrim(php_substr(lon_deg, 0, 2), "0")) + floatval(php_ltrim(php_substr(lon_deg, 2, 2), "0") + lon_deg_dec / 60)
                    elif php_strlen(lon_deg) == 7:
                        #// [+-]DDDMMSS.S
                        longitude = floatval(php_ltrim(php_substr(lon_deg, 0, 2), "0")) + floatval(php_ltrim(php_substr(lon_deg, 2, 2), "0") / 60) + floatval(php_ltrim(php_substr(lon_deg, 4, 2), "0") + lon_deg_dec / 3600)
                    # end if
                    if php_strlen(alt_deg) == 3:
                        #// [+-]DDD.D
                        altitude = floatval(php_ltrim(alt_deg, "0") + alt_deg_dec)
                    elif php_strlen(alt_deg) == 5:
                        #// [+-]DDDMM.M
                        altitude = floatval(php_ltrim(php_substr(alt_deg, 0, 2), "0")) + floatval(php_ltrim(php_substr(alt_deg, 2, 2), "0") + alt_deg_dec / 60)
                    elif php_strlen(alt_deg) == 7:
                        #// [+-]DDDMMSS.S
                        altitude = floatval(php_ltrim(php_substr(alt_deg, 0, 2), "0")) + floatval(php_ltrim(php_substr(alt_deg, 2, 2), "0") / 60) + floatval(php_ltrim(php_substr(alt_deg, 4, 2), "0") + alt_deg_dec / 3600)
                    # end if
                    if latitude != False:
                        info["quicktime"]["comments"]["gps_latitude"][-1] = -1 if lat_sign == "-" else 1 * floatval(latitude)
                    # end if
                    if longitude != False:
                        info["quicktime"]["comments"]["gps_longitude"][-1] = -1 if lon_sign == "-" else 1 * floatval(longitude)
                    # end if
                    if altitude != False:
                        info["quicktime"]["comments"]["gps_altitude"][-1] = -1 if alt_sign == "-" else 1 * floatval(altitude)
                    # end if
                # end if
                if latitude == False:
                    self.warning("location.ISO6709 string not parsed correctly: \"" + ISO6709string + "\", please submit as a bug")
                # end if
                break
            # end for
        # end if
        if (not (php_isset(lambda : info["bitrate"]))) and (php_isset(lambda : info["playtime_seconds"])):
            info["bitrate"] = info["avdataend"] - info["avdataoffset"] * 8 / info["playtime_seconds"]
        # end if
        if (php_isset(lambda : info["bitrate"])) and (not (php_isset(lambda : info["audio"]["bitrate"]))) and (not (php_isset(lambda : info["quicktime"]["video"]))):
            info["audio"]["bitrate"] = info["bitrate"]
        # end if
        if (not php_empty(lambda : info["bitrate"])) and (not php_empty(lambda : info["audio"]["bitrate"])) and php_empty(lambda : info["video"]["bitrate"]) and (not php_empty(lambda : info["video"]["frame_rate"])) and (not php_empty(lambda : info["video"]["resolution_x"])) and info["bitrate"] > info["audio"]["bitrate"]:
            info["video"]["bitrate"] = info["bitrate"] - info["audio"]["bitrate"]
        # end if
        if (not php_empty(lambda : info["playtime_seconds"])) and (not (php_isset(lambda : info["video"]["frame_rate"]))) and (not php_empty(lambda : info["quicktime"]["stts_framecount"])):
            for key,samples_count in info["quicktime"]["stts_framecount"]:
                samples_per_second = samples_count / info["playtime_seconds"]
                if samples_per_second > 240:
                    pass
                else:
                    info["video"]["frame_rate"] = samples_per_second
                    break
                # end if
            # end for
        # end if
        if info["audio"]["dataformat"] == "mp4":
            info["fileformat"] = "mp4"
            if php_empty(lambda : info["video"]["resolution_x"]):
                info["mime_type"] = "audio/mp4"
                info["video"]["dataformat"] = None
            else:
                info["mime_type"] = "video/mp4"
            # end if
        # end if
        if (not self.ReturnAtomData):
            info["quicktime"]["moov"] = None
        # end if
        if php_empty(lambda : info["audio"]["dataformat"]) and (not php_empty(lambda : info["quicktime"]["audio"])):
            info["audio"]["dataformat"] = "quicktime"
        # end if
        if php_empty(lambda : info["video"]["dataformat"]) and (not php_empty(lambda : info["quicktime"]["video"])):
            info["video"]["dataformat"] = "quicktime"
        # end if
        if (php_isset(lambda : info["video"])) and info["mime_type"] == "audio/mp4" and php_empty(lambda : info["video"]["resolution_x"]) and php_empty(lambda : info["video"]["resolution_y"]):
            info["video"] = None
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
    def quicktimeparseatom(self, atomname=None, atomsize=None, atom_data=None, baseoffset=None, atomHierarchy=None, ParseAllPossibleAtoms=None):
        
        #// http://developer.apple.com/techpubs/quicktime/qtdevdocs/APIREF/INDEX/atomalphaindex.htm
        #// https://code.google.com/p/mp4v2/wiki/iTunesMetadata
        info = self.getid3.info
        atom_parent = php_end(atomHierarchy)
        #// not array_pop($atomHierarchy); see https://www.getid3.org/phpBB3/viewtopic.php?t=1717
        php_array_push(atomHierarchy, atomname)
        atom_structure["hierarchy"] = php_implode(" ", atomHierarchy)
        atom_structure["name"] = atomname
        atom_structure["size"] = atomsize
        atom_structure["offset"] = baseoffset
        if php_substr(atomname, 0, 3) == "   ":
            #// https://github.com/JamesHeinrich/getID3/issues/139
            atomname = getid3_lib.bigendian2int(atomname)
            atom_structure["name"] = atomname
            atom_structure["subatoms"] = self.quicktimeparsecontaineratom(atom_data, baseoffset + 8, atomHierarchy, ParseAllPossibleAtoms)
        else:
            for case in Switch(atomname):
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
                    atom_structure["subatoms"] = self.quicktimeparsecontaineratom(atom_data, baseoffset + 8, atomHierarchy, ParseAllPossibleAtoms)
                    break
                # end if
                if case("ilst"):
                    #// Item LiST container atom
                    atom_structure["subatoms"] = self.quicktimeparsecontaineratom(atom_data, baseoffset + 8, atomHierarchy, ParseAllPossibleAtoms)
                    if atom_structure["subatoms"]:
                        #// some "ilst" atoms contain data atoms that have a numeric name, and the data is far more accessible if the returned array is compacted
                        allnumericnames = True
                        for subatomarray in atom_structure["subatoms"]:
                            if (not is_integer(subatomarray["name"])) or php_count(subatomarray["subatoms"]) != 1:
                                allnumericnames = False
                                break
                            # end if
                        # end for
                        if allnumericnames:
                            newData = Array()
                            for subatomarray in atom_structure["subatoms"]:
                                for newData_subatomarray in subatomarray["subatoms"]:
                                    newData_subatomarray["hierarchy"] = None
                                    newData_subatomarray["name"] = None
                                    newData[subatomarray["name"]] = newData_subatomarray
                                    break
                                # end for
                            # end for
                            atom_structure["data"] = newData
                            atom_structure["subatoms"] = None
                        # end if
                    # end if
                    break
                # end if
                if case("stbl"):
                    #// Sample TaBLe container atom
                    atom_structure["subatoms"] = self.quicktimeparsecontaineratom(atom_data, baseoffset + 8, atomHierarchy, ParseAllPossibleAtoms)
                    isVideo = False
                    framerate = 0
                    framecount = 0
                    for key,value_array in atom_structure["subatoms"]:
                        if (php_isset(lambda : value_array["sample_description_table"])):
                            for key2,value_array2 in value_array["sample_description_table"]:
                                if (php_isset(lambda : value_array2["data_format"])):
                                    for case in Switch(value_array2["data_format"]):
                                        if case("avc1"):
                                            pass
                                        # end if
                                        if case("mp4v"):
                                            #// video data
                                            isVideo = True
                                            break
                                        # end if
                                        if case("mp4a"):
                                            break
                                        # end if
                                    # end for
                                # end if
                            # end for
                        elif (php_isset(lambda : value_array["time_to_sample_table"])):
                            for key2,value_array2 in value_array["time_to_sample_table"]:
                                if (php_isset(lambda : value_array2["sample_count"])) and (php_isset(lambda : value_array2["sample_duration"])) and value_array2["sample_duration"] > 0:
                                    framerate = round(info["quicktime"]["time_scale"] / value_array2["sample_duration"], 3)
                                    framecount = value_array2["sample_count"]
                                # end if
                            # end for
                        # end if
                    # end for
                    if isVideo and framerate:
                        info["quicktime"]["video"]["frame_rate"] = framerate
                        info["video"]["frame_rate"] = info["quicktime"]["video"]["frame_rate"]
                    # end if
                    if isVideo and framecount:
                        info["quicktime"]["video"]["frame_count"] = framecount
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
                    if atom_parent == "udta":
                        #// User data atom handler
                        atom_structure["data_length"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 2))
                        atom_structure["language_id"] = getid3_lib.bigendian2int(php_substr(atom_data, 2, 2))
                        atom_structure["data"] = php_substr(atom_data, 4)
                        atom_structure["language"] = self.quicktimelanguagelookup(atom_structure["language_id"])
                        if php_empty(lambda : info["comments"]["language"]) or (not php_in_array(atom_structure["language"], info["comments"]["language"])):
                            info["comments"]["language"][-1] = atom_structure["language"]
                        # end if
                    else:
                        #// Apple item list box atom handler
                        atomoffset = 0
                        if php_substr(atom_data, 2, 2) == "µ":
                            #// not sure what it means, but observed on iPhone4 data.
                            #// Each $atom_data has 2 bytes of datasize, plus 0x10B5, then data
                            while True:
                                
                                if not (atomoffset < php_strlen(atom_data)):
                                    break
                                # end if
                                boxsmallsize = getid3_lib.bigendian2int(php_substr(atom_data, atomoffset, 2))
                                boxsmalltype = php_substr(atom_data, atomoffset + 2, 2)
                                boxsmalldata = php_substr(atom_data, atomoffset + 4, boxsmallsize)
                                if boxsmallsize <= 1:
                                    self.warning("Invalid QuickTime atom smallbox size \"" + boxsmallsize + "\" in atom \"" + php_preg_replace("#[^a-zA-Z0-9 _\\-]#", "?", atomname) + "\" at offset: " + atom_structure["offset"] + atomoffset)
                                    atom_structure["data"] = None
                                    atomoffset = php_strlen(atom_data)
                                    break
                                # end if
                                for case in Switch(boxsmalltype):
                                    if case("µ"):
                                        atom_structure["data"] = boxsmalldata
                                        break
                                    # end if
                                    if case():
                                        self.warning("Unknown QuickTime smallbox type: \"" + php_preg_replace("#[^a-zA-Z0-9 _\\-]#", "?", boxsmalltype) + "\" (" + php_trim(getid3_lib.printhexbytes(boxsmalltype)) + ") at offset " + baseoffset)
                                        atom_structure["data"] = atom_data
                                        break
                                    # end if
                                # end for
                                atomoffset += 4 + boxsmallsize
                            # end while
                        else:
                            while True:
                                
                                if not (atomoffset < php_strlen(atom_data)):
                                    break
                                # end if
                                boxsize = getid3_lib.bigendian2int(php_substr(atom_data, atomoffset, 4))
                                boxtype = php_substr(atom_data, atomoffset + 4, 4)
                                boxdata = php_substr(atom_data, atomoffset + 8, boxsize - 8)
                                if boxsize <= 1:
                                    self.warning("Invalid QuickTime atom box size \"" + boxsize + "\" in atom \"" + php_preg_replace("#[^a-zA-Z0-9 _\\-]#", "?", atomname) + "\" at offset: " + atom_structure["offset"] + atomoffset)
                                    atom_structure["data"] = None
                                    atomoffset = php_strlen(atom_data)
                                    break
                                # end if
                                atomoffset += boxsize
                                for case in Switch(boxtype):
                                    if case("mean"):
                                        pass
                                    # end if
                                    if case("name"):
                                        atom_structure[boxtype] = php_substr(boxdata, 4)
                                        break
                                    # end if
                                    if case("data"):
                                        atom_structure["version"] = getid3_lib.bigendian2int(php_substr(boxdata, 0, 1))
                                        atom_structure["flags_raw"] = getid3_lib.bigendian2int(php_substr(boxdata, 1, 3))
                                        for case in Switch(atom_structure["flags_raw"]):
                                            if case(0):
                                                pass
                                            # end if
                                            if case(21):
                                                #// tmpo/cpil flag
                                                for case in Switch(atomname):
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
                                                        atom_structure["data"] = getid3_lib.bigendian2int(php_substr(boxdata, 8, 1))
                                                        break
                                                    # end if
                                                    if case("tmpo"):
                                                        #// 16-bit integer
                                                        atom_structure["data"] = getid3_lib.bigendian2int(php_substr(boxdata, 8, 2))
                                                        break
                                                    # end if
                                                    if case("disk"):
                                                        pass
                                                    # end if
                                                    if case("trkn"):
                                                        #// binary
                                                        num = getid3_lib.bigendian2int(php_substr(boxdata, 10, 2))
                                                        num_total = getid3_lib.bigendian2int(php_substr(boxdata, 12, 2))
                                                        atom_structure["data"] = "" if php_empty(lambda : num) else num
                                                        atom_structure["data"] += "" if php_empty(lambda : num_total) else "/" + num_total
                                                        break
                                                    # end if
                                                    if case("gnre"):
                                                        #// enum
                                                        GenreID = getid3_lib.bigendian2int(php_substr(boxdata, 8, 4))
                                                        atom_structure["data"] = getid3_id3v1.lookupgenrename(GenreID - 1)
                                                        break
                                                    # end if
                                                    if case("rtng"):
                                                        #// 8-bit integer
                                                        atom_structure[atomname] = getid3_lib.bigendian2int(php_substr(boxdata, 8, 1))
                                                        atom_structure["data"] = self.quicktimecontentratinglookup(atom_structure[atomname])
                                                        break
                                                    # end if
                                                    if case("stik"):
                                                        #// 8-bit integer (enum)
                                                        atom_structure[atomname] = getid3_lib.bigendian2int(php_substr(boxdata, 8, 1))
                                                        atom_structure["data"] = self.quicktimestiklookup(atom_structure[atomname])
                                                        break
                                                    # end if
                                                    if case("sfID"):
                                                        #// 32-bit integer
                                                        atom_structure[atomname] = getid3_lib.bigendian2int(php_substr(boxdata, 8, 4))
                                                        atom_structure["data"] = self.quicktimestorefrontcodelookup(atom_structure[atomname])
                                                        break
                                                    # end if
                                                    if case("egid"):
                                                        pass
                                                    # end if
                                                    if case("purl"):
                                                        atom_structure["data"] = php_substr(boxdata, 8)
                                                        break
                                                    # end if
                                                    if case("plID"):
                                                        #// 64-bit integer
                                                        atom_structure["data"] = getid3_lib.bigendian2int(php_substr(boxdata, 8, 8))
                                                        break
                                                    # end if
                                                    if case("covr"):
                                                        atom_structure["data"] = php_substr(boxdata, 8)
                                                        #// not a foolproof check, but better than nothing
                                                        if php_preg_match("#^\\xFF\\xD8\\xFF#", atom_structure["data"]):
                                                            atom_structure["image_mime"] = "image/jpeg"
                                                        elif php_preg_match("#^\\x89\\x50\\x4E\\x47\\x0D\\x0A\\x1A\\x0A#", atom_structure["data"]):
                                                            atom_structure["image_mime"] = "image/png"
                                                        elif php_preg_match("#^GIF#", atom_structure["data"]):
                                                            atom_structure["image_mime"] = "image/gif"
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
                                                        atom_structure["data"] = getid3_lib.bigendian2int(php_substr(boxdata, 8, 4))
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
                                                atom_structure["data"] = php_substr(boxdata, 8)
                                                if atomname == "covr":
                                                    #// not a foolproof check, but better than nothing
                                                    if php_preg_match("#^\\xFF\\xD8\\xFF#", atom_structure["data"]):
                                                        atom_structure["image_mime"] = "image/jpeg"
                                                    elif php_preg_match("#^\\x89\\x50\\x4E\\x47\\x0D\\x0A\\x1A\\x0A#", atom_structure["data"]):
                                                        atom_structure["image_mime"] = "image/png"
                                                    elif php_preg_match("#^GIF#", atom_structure["data"]):
                                                        atom_structure["image_mime"] = "image/gif"
                                                    # end if
                                                # end if
                                                break
                                            # end if
                                        # end for
                                        break
                                    # end if
                                    if case():
                                        self.warning("Unknown QuickTime box type: \"" + php_preg_replace("#[^a-zA-Z0-9 _\\-]#", "?", boxtype) + "\" (" + php_trim(getid3_lib.printhexbytes(boxtype)) + ") at offset " + baseoffset)
                                        atom_structure["data"] = atom_data
                                    # end if
                                # end for
                            # end while
                        # end if
                    # end if
                    self.copytoappropriatecommentssection(atomname, atom_structure["data"], atom_structure["name"])
                    break
                # end if
                if case("play"):
                    #// auto-PLAY atom
                    atom_structure["autoplay"] = bool(getid3_lib.bigendian2int(php_substr(atom_data, 0, 1)))
                    info["quicktime"]["autoplay"] = atom_structure["autoplay"]
                    break
                # end if
                if case("WLOC"):
                    #// Window LOCation atom
                    atom_structure["location_x"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 2))
                    atom_structure["location_y"] = getid3_lib.bigendian2int(php_substr(atom_data, 2, 2))
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
                    atom_structure["data"] = getid3_lib.bigendian2int(atom_data)
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
                    atom_structure["data"] = atom_data
                    break
                # end if
                if case("cmvd"):
                    #// Compressed MooV Data atom
                    #// Code by ubergeekØubergeek*tv based on information from
                    #// http://developer.apple.com/quicktime/icefloe/dispatch012.html
                    atom_structure["unCompressedSize"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 4))
                    CompressedFileData = php_substr(atom_data, 4)
                    UncompressedHeader = php_no_error(lambda: gzuncompress(CompressedFileData))
                    if UncompressedHeader:
                        atom_structure["subatoms"] = self.quicktimeparsecontaineratom(UncompressedHeader, 0, atomHierarchy, ParseAllPossibleAtoms)
                    else:
                        self.warning("Error decompressing compressed MOV atom at offset " + atom_structure["offset"])
                    # end if
                    break
                # end if
                if case("dcom"):
                    #// Data COMpression atom
                    atom_structure["compression_id"] = atom_data
                    atom_structure["compression_text"] = self.quicktimedcomlookup(atom_data)
                    break
                # end if
                if case("rdrf"):
                    #// Reference movie Data ReFerence atom
                    atom_structure["version"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 1))
                    atom_structure["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data, 1, 3))
                    atom_structure["flags"]["internal_data"] = bool(atom_structure["flags_raw"] & 1)
                    atom_structure["reference_type_name"] = php_substr(atom_data, 4, 4)
                    atom_structure["reference_length"] = getid3_lib.bigendian2int(php_substr(atom_data, 8, 4))
                    for case in Switch(atom_structure["reference_type_name"]):
                        if case("url "):
                            atom_structure["url"] = self.nonullstring(php_substr(atom_data, 12))
                            break
                        # end if
                        if case("alis"):
                            atom_structure["file_alias"] = php_substr(atom_data, 12)
                            break
                        # end if
                        if case("rsrc"):
                            atom_structure["resource_alias"] = php_substr(atom_data, 12)
                            break
                        # end if
                        if case():
                            atom_structure["data"] = php_substr(atom_data, 12)
                            break
                        # end if
                    # end for
                    break
                # end if
                if case("rmqu"):
                    #// Reference Movie QUality atom
                    atom_structure["movie_quality"] = getid3_lib.bigendian2int(atom_data)
                    break
                # end if
                if case("rmcs"):
                    #// Reference Movie Cpu Speed atom
                    atom_structure["version"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 1))
                    atom_structure["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data, 1, 3))
                    #// hardcoded: 0x0000
                    atom_structure["cpu_speed_rating"] = getid3_lib.bigendian2int(php_substr(atom_data, 4, 2))
                    break
                # end if
                if case("rmvc"):
                    #// Reference Movie Version Check atom
                    atom_structure["version"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 1))
                    atom_structure["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data, 1, 3))
                    #// hardcoded: 0x0000
                    atom_structure["gestalt_selector"] = php_substr(atom_data, 4, 4)
                    atom_structure["gestalt_value_mask"] = getid3_lib.bigendian2int(php_substr(atom_data, 8, 4))
                    atom_structure["gestalt_value"] = getid3_lib.bigendian2int(php_substr(atom_data, 12, 4))
                    atom_structure["gestalt_check_type"] = getid3_lib.bigendian2int(php_substr(atom_data, 14, 2))
                    break
                # end if
                if case("rmcd"):
                    #// Reference Movie Component check atom
                    atom_structure["version"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 1))
                    atom_structure["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data, 1, 3))
                    #// hardcoded: 0x0000
                    atom_structure["component_type"] = php_substr(atom_data, 4, 4)
                    atom_structure["component_subtype"] = php_substr(atom_data, 8, 4)
                    atom_structure["component_manufacturer"] = php_substr(atom_data, 12, 4)
                    atom_structure["component_flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data, 16, 4))
                    atom_structure["component_flags_mask"] = getid3_lib.bigendian2int(php_substr(atom_data, 20, 4))
                    atom_structure["component_min_version"] = getid3_lib.bigendian2int(php_substr(atom_data, 24, 4))
                    break
                # end if
                if case("rmdr"):
                    #// Reference Movie Data Rate atom
                    atom_structure["version"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 1))
                    atom_structure["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data, 1, 3))
                    #// hardcoded: 0x0000
                    atom_structure["data_rate"] = getid3_lib.bigendian2int(php_substr(atom_data, 4, 4))
                    atom_structure["data_rate_bps"] = atom_structure["data_rate"] * 10
                    break
                # end if
                if case("rmla"):
                    #// Reference Movie Language Atom
                    atom_structure["version"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 1))
                    atom_structure["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data, 1, 3))
                    #// hardcoded: 0x0000
                    atom_structure["language_id"] = getid3_lib.bigendian2int(php_substr(atom_data, 4, 2))
                    atom_structure["language"] = self.quicktimelanguagelookup(atom_structure["language_id"])
                    if php_empty(lambda : info["comments"]["language"]) or (not php_in_array(atom_structure["language"], info["comments"]["language"])):
                        info["comments"]["language"][-1] = atom_structure["language"]
                    # end if
                    break
                # end if
                if case("ptv "):
                    #// Print To Video - defines a movie's full screen mode
                    #// http://developer.apple.com/documentation/QuickTime/APIREF/SOURCESIV/at_ptv-_pg.htm
                    atom_structure["display_size_raw"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 2))
                    atom_structure["reserved_1"] = getid3_lib.bigendian2int(php_substr(atom_data, 2, 2))
                    #// hardcoded: 0x0000
                    atom_structure["reserved_2"] = getid3_lib.bigendian2int(php_substr(atom_data, 4, 2))
                    #// hardcoded: 0x0000
                    atom_structure["slide_show_flag"] = getid3_lib.bigendian2int(php_substr(atom_data, 6, 1))
                    atom_structure["play_on_open_flag"] = getid3_lib.bigendian2int(php_substr(atom_data, 7, 1))
                    atom_structure["flags"]["play_on_open"] = bool(atom_structure["play_on_open_flag"])
                    atom_structure["flags"]["slide_show"] = bool(atom_structure["slide_show_flag"])
                    ptv_lookup[0] = "normal"
                    ptv_lookup[1] = "double"
                    ptv_lookup[2] = "half"
                    ptv_lookup[3] = "full"
                    ptv_lookup[4] = "current"
                    if (php_isset(lambda : ptv_lookup[atom_structure["display_size_raw"]])):
                        atom_structure["display_size"] = ptv_lookup[atom_structure["display_size_raw"]]
                    else:
                        self.warning("unknown \"ptv \" display constant (" + atom_structure["display_size_raw"] + ")")
                    # end if
                    break
                # end if
                if case("stsd"):
                    #// Sample Table Sample Description atom
                    atom_structure["version"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 1))
                    atom_structure["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data, 1, 3))
                    #// hardcoded: 0x0000
                    atom_structure["number_entries"] = getid3_lib.bigendian2int(php_substr(atom_data, 4, 4))
                    #// see: https://github.com/JamesHeinrich/getID3/issues/111
                    #// Some corrupt files have been known to have high bits set in the number_entries field
                    #// This field shouldn't really need to be 32-bits, values stores are likely in the range 1-100000
                    #// Workaround: mask off the upper byte and throw a warning if it's nonzero
                    if atom_structure["number_entries"] > 1048575:
                        if atom_structure["number_entries"] > 16777215:
                            self.warning("\"stsd\" atom contains improbably large number_entries (0x" + getid3_lib.printhexbytes(php_substr(atom_data, 4, 4), True, False) + " = " + atom_structure["number_entries"] + "), probably in error. Ignoring upper byte and interpreting this as 0x" + getid3_lib.printhexbytes(php_substr(atom_data, 5, 3), True, False) + " = " + atom_structure["number_entries"] & 16777215)
                            atom_structure["number_entries"] = atom_structure["number_entries"] & 16777215
                        else:
                            self.warning("\"stsd\" atom contains improbably large number_entries (0x" + getid3_lib.printhexbytes(php_substr(atom_data, 4, 4), True, False) + " = " + atom_structure["number_entries"] + "), probably in error. Please report this to info@getid3.org referencing bug report #111")
                        # end if
                    # end if
                    stsdEntriesDataOffset = 8
                    i = 0
                    while i < atom_structure["number_entries"]:
                        
                        atom_structure["sample_description_table"][i]["size"] = getid3_lib.bigendian2int(php_substr(atom_data, stsdEntriesDataOffset, 4))
                        stsdEntriesDataOffset += 4
                        atom_structure["sample_description_table"][i]["data_format"] = php_substr(atom_data, stsdEntriesDataOffset, 4)
                        stsdEntriesDataOffset += 4
                        atom_structure["sample_description_table"][i]["reserved"] = getid3_lib.bigendian2int(php_substr(atom_data, stsdEntriesDataOffset, 6))
                        stsdEntriesDataOffset += 6
                        atom_structure["sample_description_table"][i]["reference_index"] = getid3_lib.bigendian2int(php_substr(atom_data, stsdEntriesDataOffset, 2))
                        stsdEntriesDataOffset += 2
                        atom_structure["sample_description_table"][i]["data"] = php_substr(atom_data, stsdEntriesDataOffset, atom_structure["sample_description_table"][i]["size"] - 4 - 4 - 6 - 2)
                        stsdEntriesDataOffset += atom_structure["sample_description_table"][i]["size"] - 4 - 4 - 6 - 2
                        atom_structure["sample_description_table"][i]["encoder_version"] = getid3_lib.bigendian2int(php_substr(atom_structure["sample_description_table"][i]["data"], 0, 2))
                        atom_structure["sample_description_table"][i]["encoder_revision"] = getid3_lib.bigendian2int(php_substr(atom_structure["sample_description_table"][i]["data"], 2, 2))
                        atom_structure["sample_description_table"][i]["encoder_vendor"] = php_substr(atom_structure["sample_description_table"][i]["data"], 4, 4)
                        for case in Switch(atom_structure["sample_description_table"][i]["encoder_vendor"]):
                            if case("    "):
                                #// audio tracks
                                atom_structure["sample_description_table"][i]["audio_channels"] = getid3_lib.bigendian2int(php_substr(atom_structure["sample_description_table"][i]["data"], 8, 2))
                                atom_structure["sample_description_table"][i]["audio_bit_depth"] = getid3_lib.bigendian2int(php_substr(atom_structure["sample_description_table"][i]["data"], 10, 2))
                                atom_structure["sample_description_table"][i]["audio_compression_id"] = getid3_lib.bigendian2int(php_substr(atom_structure["sample_description_table"][i]["data"], 12, 2))
                                atom_structure["sample_description_table"][i]["audio_packet_size"] = getid3_lib.bigendian2int(php_substr(atom_structure["sample_description_table"][i]["data"], 14, 2))
                                atom_structure["sample_description_table"][i]["audio_sample_rate"] = getid3_lib.fixedpoint16_16(php_substr(atom_structure["sample_description_table"][i]["data"], 16, 4))
                                #// video tracks
                                #// http://developer.apple.com/library/mac/#documentation/QuickTime/QTFF/QTFFChap3/qtff3.html
                                atom_structure["sample_description_table"][i]["temporal_quality"] = getid3_lib.bigendian2int(php_substr(atom_structure["sample_description_table"][i]["data"], 8, 4))
                                atom_structure["sample_description_table"][i]["spatial_quality"] = getid3_lib.bigendian2int(php_substr(atom_structure["sample_description_table"][i]["data"], 12, 4))
                                atom_structure["sample_description_table"][i]["width"] = getid3_lib.bigendian2int(php_substr(atom_structure["sample_description_table"][i]["data"], 16, 2))
                                atom_structure["sample_description_table"][i]["height"] = getid3_lib.bigendian2int(php_substr(atom_structure["sample_description_table"][i]["data"], 18, 2))
                                atom_structure["sample_description_table"][i]["resolution_x"] = getid3_lib.fixedpoint16_16(php_substr(atom_structure["sample_description_table"][i]["data"], 24, 4))
                                atom_structure["sample_description_table"][i]["resolution_y"] = getid3_lib.fixedpoint16_16(php_substr(atom_structure["sample_description_table"][i]["data"], 28, 4))
                                atom_structure["sample_description_table"][i]["data_size"] = getid3_lib.bigendian2int(php_substr(atom_structure["sample_description_table"][i]["data"], 32, 4))
                                atom_structure["sample_description_table"][i]["frame_count"] = getid3_lib.bigendian2int(php_substr(atom_structure["sample_description_table"][i]["data"], 36, 2))
                                atom_structure["sample_description_table"][i]["compressor_name"] = php_substr(atom_structure["sample_description_table"][i]["data"], 38, 4)
                                atom_structure["sample_description_table"][i]["pixel_depth"] = getid3_lib.bigendian2int(php_substr(atom_structure["sample_description_table"][i]["data"], 42, 2))
                                atom_structure["sample_description_table"][i]["color_table_id"] = getid3_lib.bigendian2int(php_substr(atom_structure["sample_description_table"][i]["data"], 44, 2))
                                for case in Switch(atom_structure["sample_description_table"][i]["data_format"]):
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
                                        info["fileformat"] = "mp4"
                                        info["video"]["fourcc"] = atom_structure["sample_description_table"][i]["data_format"]
                                        if self.quicktimevideocodeclookup(info["video"]["fourcc"]):
                                            info["video"]["fourcc_lookup"] = self.quicktimevideocodeclookup(info["video"]["fourcc"])
                                        # end if
                                        #// https://www.getid3.org/phpBB3/viewtopic.php?t=1550
                                        #// if ((!empty($atom_structure['sample_description_table'][$i]['width']) && !empty($atom_structure['sample_description_table'][$i]['width'])) && (empty($info['video']['resolution_x']) || empty($info['video']['resolution_y']) || (number_format($info['video']['resolution_x'], 6) != number_format(round($info['video']['resolution_x']), 6)) || (number_format($info['video']['resolution_y'], 6) != number_format(round($info['video']['resolution_y']), 6)))) { // ugly check for floating point numbers
                                        if (not php_empty(lambda : atom_structure["sample_description_table"][i]["width"])) and (not php_empty(lambda : atom_structure["sample_description_table"][i]["height"])):
                                            #// assume that values stored here are more important than values stored in [tkhd] atom
                                            info["video"]["resolution_x"] = atom_structure["sample_description_table"][i]["width"]
                                            info["video"]["resolution_y"] = atom_structure["sample_description_table"][i]["height"]
                                            info["quicktime"]["video"]["resolution_x"] = info["video"]["resolution_x"]
                                            info["quicktime"]["video"]["resolution_y"] = info["video"]["resolution_y"]
                                        # end if
                                        break
                                    # end if
                                    if case("qtvr"):
                                        info["video"]["dataformat"] = "quicktimevr"
                                        break
                                    # end if
                                    if case("mp4a"):
                                        pass
                                    # end if
                                    if case():
                                        info["quicktime"]["audio"]["codec"] = self.quicktimeaudiocodeclookup(atom_structure["sample_description_table"][i]["data_format"])
                                        info["quicktime"]["audio"]["sample_rate"] = atom_structure["sample_description_table"][i]["audio_sample_rate"]
                                        info["quicktime"]["audio"]["channels"] = atom_structure["sample_description_table"][i]["audio_channels"]
                                        info["quicktime"]["audio"]["bit_depth"] = atom_structure["sample_description_table"][i]["audio_bit_depth"]
                                        info["audio"]["codec"] = info["quicktime"]["audio"]["codec"]
                                        info["audio"]["sample_rate"] = info["quicktime"]["audio"]["sample_rate"]
                                        info["audio"]["channels"] = info["quicktime"]["audio"]["channels"]
                                        info["audio"]["bits_per_sample"] = info["quicktime"]["audio"]["bit_depth"]
                                        for case in Switch(atom_structure["sample_description_table"][i]["data_format"]):
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
                                                info["audio"]["lossless"] = info["quicktime"]["audio"]["lossless"]
                                                info["audio"]["bitrate"] = info["quicktime"]["audio"]["bitrate"]
                                                break
                                            # end if
                                            if case():
                                                info["audio"]["lossless"] = False
                                                break
                                            # end if
                                        # end for
                                        break
                                    # end if
                                # end for
                                break
                            # end if
                            if case():
                                for case in Switch(atom_structure["sample_description_table"][i]["data_format"]):
                                    if case("mp4s"):
                                        info["fileformat"] = "mp4"
                                        break
                                    # end if
                                    if case():
                                        #// video atom
                                        atom_structure["sample_description_table"][i]["video_temporal_quality"] = getid3_lib.bigendian2int(php_substr(atom_structure["sample_description_table"][i]["data"], 8, 4))
                                        atom_structure["sample_description_table"][i]["video_spatial_quality"] = getid3_lib.bigendian2int(php_substr(atom_structure["sample_description_table"][i]["data"], 12, 4))
                                        atom_structure["sample_description_table"][i]["video_frame_width"] = getid3_lib.bigendian2int(php_substr(atom_structure["sample_description_table"][i]["data"], 16, 2))
                                        atom_structure["sample_description_table"][i]["video_frame_height"] = getid3_lib.bigendian2int(php_substr(atom_structure["sample_description_table"][i]["data"], 18, 2))
                                        atom_structure["sample_description_table"][i]["video_resolution_x"] = getid3_lib.fixedpoint16_16(php_substr(atom_structure["sample_description_table"][i]["data"], 20, 4))
                                        atom_structure["sample_description_table"][i]["video_resolution_y"] = getid3_lib.fixedpoint16_16(php_substr(atom_structure["sample_description_table"][i]["data"], 24, 4))
                                        atom_structure["sample_description_table"][i]["video_data_size"] = getid3_lib.bigendian2int(php_substr(atom_structure["sample_description_table"][i]["data"], 28, 4))
                                        atom_structure["sample_description_table"][i]["video_frame_count"] = getid3_lib.bigendian2int(php_substr(atom_structure["sample_description_table"][i]["data"], 32, 2))
                                        atom_structure["sample_description_table"][i]["video_encoder_name_len"] = getid3_lib.bigendian2int(php_substr(atom_structure["sample_description_table"][i]["data"], 34, 1))
                                        atom_structure["sample_description_table"][i]["video_encoder_name"] = php_substr(atom_structure["sample_description_table"][i]["data"], 35, atom_structure["sample_description_table"][i]["video_encoder_name_len"])
                                        atom_structure["sample_description_table"][i]["video_pixel_color_depth"] = getid3_lib.bigendian2int(php_substr(atom_structure["sample_description_table"][i]["data"], 66, 2))
                                        atom_structure["sample_description_table"][i]["video_color_table_id"] = getid3_lib.bigendian2int(php_substr(atom_structure["sample_description_table"][i]["data"], 68, 2))
                                        atom_structure["sample_description_table"][i]["video_pixel_color_type"] = "grayscale" if atom_structure["sample_description_table"][i]["video_pixel_color_depth"] > 32 else "color"
                                        atom_structure["sample_description_table"][i]["video_pixel_color_name"] = self.quicktimecolornamelookup(atom_structure["sample_description_table"][i]["video_pixel_color_depth"])
                                        if atom_structure["sample_description_table"][i]["video_pixel_color_name"] != "invalid":
                                            info["quicktime"]["video"]["codec_fourcc"] = atom_structure["sample_description_table"][i]["data_format"]
                                            info["quicktime"]["video"]["codec_fourcc_lookup"] = self.quicktimevideocodeclookup(atom_structure["sample_description_table"][i]["data_format"])
                                            info["quicktime"]["video"]["codec"] = atom_structure["sample_description_table"][i]["video_encoder_name"] if atom_structure["sample_description_table"][i]["video_encoder_name_len"] > 0 else atom_structure["sample_description_table"][i]["data_format"]
                                            info["quicktime"]["video"]["color_depth"] = atom_structure["sample_description_table"][i]["video_pixel_color_depth"]
                                            info["quicktime"]["video"]["color_depth_name"] = atom_structure["sample_description_table"][i]["video_pixel_color_name"]
                                            info["video"]["codec"] = info["quicktime"]["video"]["codec"]
                                            info["video"]["bits_per_sample"] = info["quicktime"]["video"]["color_depth"]
                                        # end if
                                        info["video"]["lossless"] = False
                                        info["video"]["pixel_aspect_ratio"] = float(1)
                                        break
                                    # end if
                                # end for
                                break
                            # end if
                        # end for
                        for case in Switch(php_strtolower(atom_structure["sample_description_table"][i]["data_format"])):
                            if case("mp4a"):
                                info["audio"]["dataformat"] = "mp4"
                                info["quicktime"]["audio"]["codec"] = "mp4"
                                break
                            # end if
                            if case("3ivx"):
                                pass
                            # end if
                            if case("3iv1"):
                                pass
                            # end if
                            if case("3iv2"):
                                info["video"]["dataformat"] = "3ivx"
                                break
                            # end if
                            if case("xvid"):
                                info["video"]["dataformat"] = "xvid"
                                break
                            # end if
                            if case("mp4v"):
                                info["video"]["dataformat"] = "mpeg4"
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
                                info["video"]["dataformat"] = "divx"
                                break
                            # end if
                            if case():
                                break
                            # end if
                        # end for
                        atom_structure["sample_description_table"][i]["data"] = None
                        i += 1
                    # end while
                    break
                # end if
                if case("stts"):
                    #// Sample Table Time-to-Sample atom
                    atom_structure["version"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 1))
                    atom_structure["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data, 1, 3))
                    #// hardcoded: 0x0000
                    atom_structure["number_entries"] = getid3_lib.bigendian2int(php_substr(atom_data, 4, 4))
                    sttsEntriesDataOffset = 8
                    #// $FrameRateCalculatorArray = array();
                    frames_count = 0
                    max_stts_entries_to_scan = php_min(floor(self.getid3.memory_limit / 10000), atom_structure["number_entries"]) if info["php_memory_limit"] else atom_structure["number_entries"]
                    if max_stts_entries_to_scan < atom_structure["number_entries"]:
                        self.warning("QuickTime atom \"stts\" has " + atom_structure["number_entries"] + " but only scanning the first " + max_stts_entries_to_scan + " entries due to limited PHP memory available (" + floor(self.getid3.memory_limit / 1048576) + "MB).")
                    # end if
                    i = 0
                    while i < max_stts_entries_to_scan:
                        
                        atom_structure["time_to_sample_table"][i]["sample_count"] = getid3_lib.bigendian2int(php_substr(atom_data, sttsEntriesDataOffset, 4))
                        sttsEntriesDataOffset += 4
                        atom_structure["time_to_sample_table"][i]["sample_duration"] = getid3_lib.bigendian2int(php_substr(atom_data, sttsEntriesDataOffset, 4))
                        sttsEntriesDataOffset += 4
                        frames_count += atom_structure["time_to_sample_table"][i]["sample_count"]
                        pass
                        i += 1
                    # end while
                    info["quicktime"]["stts_framecount"][-1] = frames_count
                    break
                # end if
                if case("stss"):
                    #// Sample Table Sync Sample (key frames) atom
                    if ParseAllPossibleAtoms:
                        atom_structure["version"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 1))
                        atom_structure["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data, 1, 3))
                        #// hardcoded: 0x0000
                        atom_structure["number_entries"] = getid3_lib.bigendian2int(php_substr(atom_data, 4, 4))
                        stssEntriesDataOffset = 8
                        i = 0
                        while i < atom_structure["number_entries"]:
                            
                            atom_structure["time_to_sample_table"][i] = getid3_lib.bigendian2int(php_substr(atom_data, stssEntriesDataOffset, 4))
                            stssEntriesDataOffset += 4
                            i += 1
                        # end while
                    # end if
                    break
                # end if
                if case("stsc"):
                    #// Sample Table Sample-to-Chunk atom
                    if ParseAllPossibleAtoms:
                        atom_structure["version"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 1))
                        atom_structure["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data, 1, 3))
                        #// hardcoded: 0x0000
                        atom_structure["number_entries"] = getid3_lib.bigendian2int(php_substr(atom_data, 4, 4))
                        stscEntriesDataOffset = 8
                        i = 0
                        while i < atom_structure["number_entries"]:
                            
                            atom_structure["sample_to_chunk_table"][i]["first_chunk"] = getid3_lib.bigendian2int(php_substr(atom_data, stscEntriesDataOffset, 4))
                            stscEntriesDataOffset += 4
                            atom_structure["sample_to_chunk_table"][i]["samples_per_chunk"] = getid3_lib.bigendian2int(php_substr(atom_data, stscEntriesDataOffset, 4))
                            stscEntriesDataOffset += 4
                            atom_structure["sample_to_chunk_table"][i]["sample_description"] = getid3_lib.bigendian2int(php_substr(atom_data, stscEntriesDataOffset, 4))
                            stscEntriesDataOffset += 4
                            i += 1
                        # end while
                    # end if
                    break
                # end if
                if case("stsz"):
                    #// Sample Table SiZe atom
                    if ParseAllPossibleAtoms:
                        atom_structure["version"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 1))
                        atom_structure["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data, 1, 3))
                        #// hardcoded: 0x0000
                        atom_structure["sample_size"] = getid3_lib.bigendian2int(php_substr(atom_data, 4, 4))
                        atom_structure["number_entries"] = getid3_lib.bigendian2int(php_substr(atom_data, 8, 4))
                        stszEntriesDataOffset = 12
                        if atom_structure["sample_size"] == 0:
                            i = 0
                            while i < atom_structure["number_entries"]:
                                
                                atom_structure["sample_size_table"][i] = getid3_lib.bigendian2int(php_substr(atom_data, stszEntriesDataOffset, 4))
                                stszEntriesDataOffset += 4
                                i += 1
                            # end while
                        # end if
                    # end if
                    break
                # end if
                if case("stco"):
                    #// Sample Table Chunk Offset atom
                    if ParseAllPossibleAtoms:
                        atom_structure["version"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 1))
                        atom_structure["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data, 1, 3))
                        #// hardcoded: 0x0000
                        atom_structure["number_entries"] = getid3_lib.bigendian2int(php_substr(atom_data, 4, 4))
                        stcoEntriesDataOffset = 8
                        i = 0
                        while i < atom_structure["number_entries"]:
                            
                            atom_structure["chunk_offset_table"][i] = getid3_lib.bigendian2int(php_substr(atom_data, stcoEntriesDataOffset, 4))
                            stcoEntriesDataOffset += 4
                            i += 1
                        # end while
                    # end if
                    break
                # end if
                if case("co64"):
                    #// Chunk Offset 64-bit (version of "stco" that supports > 2GB files)
                    if ParseAllPossibleAtoms:
                        atom_structure["version"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 1))
                        atom_structure["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data, 1, 3))
                        #// hardcoded: 0x0000
                        atom_structure["number_entries"] = getid3_lib.bigendian2int(php_substr(atom_data, 4, 4))
                        stcoEntriesDataOffset = 8
                        i = 0
                        while i < atom_structure["number_entries"]:
                            
                            atom_structure["chunk_offset_table"][i] = getid3_lib.bigendian2int(php_substr(atom_data, stcoEntriesDataOffset, 8))
                            stcoEntriesDataOffset += 8
                            i += 1
                        # end while
                    # end if
                    break
                # end if
                if case("dref"):
                    #// Data REFerence atom
                    atom_structure["version"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 1))
                    atom_structure["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data, 1, 3))
                    #// hardcoded: 0x0000
                    atom_structure["number_entries"] = getid3_lib.bigendian2int(php_substr(atom_data, 4, 4))
                    drefDataOffset = 8
                    i = 0
                    while i < atom_structure["number_entries"]:
                        
                        atom_structure["data_references"][i]["size"] = getid3_lib.bigendian2int(php_substr(atom_data, drefDataOffset, 4))
                        drefDataOffset += 4
                        atom_structure["data_references"][i]["type"] = php_substr(atom_data, drefDataOffset, 4)
                        drefDataOffset += 4
                        atom_structure["data_references"][i]["version"] = getid3_lib.bigendian2int(php_substr(atom_data, drefDataOffset, 1))
                        drefDataOffset += 1
                        atom_structure["data_references"][i]["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data, drefDataOffset, 3))
                        #// hardcoded: 0x0000
                        drefDataOffset += 3
                        atom_structure["data_references"][i]["data"] = php_substr(atom_data, drefDataOffset, atom_structure["data_references"][i]["size"] - 4 - 4 - 1 - 3)
                        drefDataOffset += atom_structure["data_references"][i]["size"] - 4 - 4 - 1 - 3
                        atom_structure["data_references"][i]["flags"]["self_reference"] = bool(atom_structure["data_references"][i]["flags_raw"] & 1)
                        i += 1
                    # end while
                    break
                # end if
                if case("gmin"):
                    #// base Media INformation atom
                    atom_structure["version"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 1))
                    atom_structure["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data, 1, 3))
                    #// hardcoded: 0x0000
                    atom_structure["graphics_mode"] = getid3_lib.bigendian2int(php_substr(atom_data, 4, 2))
                    atom_structure["opcolor_red"] = getid3_lib.bigendian2int(php_substr(atom_data, 6, 2))
                    atom_structure["opcolor_green"] = getid3_lib.bigendian2int(php_substr(atom_data, 8, 2))
                    atom_structure["opcolor_blue"] = getid3_lib.bigendian2int(php_substr(atom_data, 10, 2))
                    atom_structure["balance"] = getid3_lib.bigendian2int(php_substr(atom_data, 12, 2))
                    atom_structure["reserved"] = getid3_lib.bigendian2int(php_substr(atom_data, 14, 2))
                    break
                # end if
                if case("smhd"):
                    #// Sound Media information HeaDer atom
                    atom_structure["version"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 1))
                    atom_structure["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data, 1, 3))
                    #// hardcoded: 0x0000
                    atom_structure["balance"] = getid3_lib.bigendian2int(php_substr(atom_data, 4, 2))
                    atom_structure["reserved"] = getid3_lib.bigendian2int(php_substr(atom_data, 6, 2))
                    break
                # end if
                if case("vmhd"):
                    #// Video Media information HeaDer atom
                    atom_structure["version"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 1))
                    atom_structure["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data, 1, 3))
                    atom_structure["graphics_mode"] = getid3_lib.bigendian2int(php_substr(atom_data, 4, 2))
                    atom_structure["opcolor_red"] = getid3_lib.bigendian2int(php_substr(atom_data, 6, 2))
                    atom_structure["opcolor_green"] = getid3_lib.bigendian2int(php_substr(atom_data, 8, 2))
                    atom_structure["opcolor_blue"] = getid3_lib.bigendian2int(php_substr(atom_data, 10, 2))
                    atom_structure["flags"]["no_lean_ahead"] = bool(atom_structure["flags_raw"] & 1)
                    break
                # end if
                if case("hdlr"):
                    #// HanDLeR reference atom
                    atom_structure["version"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 1))
                    atom_structure["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data, 1, 3))
                    #// hardcoded: 0x0000
                    atom_structure["component_type"] = php_substr(atom_data, 4, 4)
                    atom_structure["component_subtype"] = php_substr(atom_data, 8, 4)
                    atom_structure["component_manufacturer"] = php_substr(atom_data, 12, 4)
                    atom_structure["component_flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data, 16, 4))
                    atom_structure["component_flags_mask"] = getid3_lib.bigendian2int(php_substr(atom_data, 20, 4))
                    atom_structure["component_name"] = self.pascal2string(php_substr(atom_data, 24))
                    if atom_structure["component_subtype"] == "STpn" and atom_structure["component_manufacturer"] == "zzzz":
                        info["video"]["dataformat"] = "quicktimevr"
                    # end if
                    break
                # end if
                if case("mdhd"):
                    #// MeDia HeaDer atom
                    atom_structure["version"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 1))
                    atom_structure["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data, 1, 3))
                    #// hardcoded: 0x0000
                    atom_structure["creation_time"] = getid3_lib.bigendian2int(php_substr(atom_data, 4, 4))
                    atom_structure["modify_time"] = getid3_lib.bigendian2int(php_substr(atom_data, 8, 4))
                    atom_structure["time_scale"] = getid3_lib.bigendian2int(php_substr(atom_data, 12, 4))
                    atom_structure["duration"] = getid3_lib.bigendian2int(php_substr(atom_data, 16, 4))
                    atom_structure["language_id"] = getid3_lib.bigendian2int(php_substr(atom_data, 20, 2))
                    atom_structure["quality"] = getid3_lib.bigendian2int(php_substr(atom_data, 22, 2))
                    if atom_structure["time_scale"] == 0:
                        self.error("Corrupt Quicktime file: mdhd.time_scale == zero")
                        return False
                    # end if
                    info["quicktime"]["time_scale"] = php_max(info["quicktime"]["time_scale"], atom_structure["time_scale"]) if (php_isset(lambda : info["quicktime"]["time_scale"])) and info["quicktime"]["time_scale"] < 1000 else atom_structure["time_scale"]
                    atom_structure["creation_time_unix"] = getid3_lib.datemac2unix(atom_structure["creation_time"])
                    atom_structure["modify_time_unix"] = getid3_lib.datemac2unix(atom_structure["modify_time"])
                    atom_structure["playtime_seconds"] = atom_structure["duration"] / atom_structure["time_scale"]
                    atom_structure["language"] = self.quicktimelanguagelookup(atom_structure["language_id"])
                    if php_empty(lambda : info["comments"]["language"]) or (not php_in_array(atom_structure["language"], info["comments"]["language"])):
                        info["comments"]["language"][-1] = atom_structure["language"]
                    # end if
                    break
                # end if
                if case("pnot"):
                    #// Preview atom
                    atom_structure["modification_date"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 4))
                    #// "standard Macintosh format"
                    atom_structure["version_number"] = getid3_lib.bigendian2int(php_substr(atom_data, 4, 2))
                    #// hardcoded: 0x00
                    atom_structure["atom_type"] = php_substr(atom_data, 6, 4)
                    #// usually: 'PICT'
                    atom_structure["atom_index"] = getid3_lib.bigendian2int(php_substr(atom_data, 10, 2))
                    #// usually: 0x01
                    atom_structure["modification_date_unix"] = getid3_lib.datemac2unix(atom_structure["modification_date"])
                    break
                # end if
                if case("crgn"):
                    #// Clipping ReGioN atom
                    atom_structure["region_size"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 2))
                    #// The Region size, Region boundary box,
                    atom_structure["boundary_box"] = getid3_lib.bigendian2int(php_substr(atom_data, 2, 8))
                    #// and Clipping region data fields
                    atom_structure["clipping_data"] = php_substr(atom_data, 10)
                    break
                # end if
                if case("load"):
                    #// track LOAD settings atom
                    atom_structure["preload_start_time"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 4))
                    atom_structure["preload_duration"] = getid3_lib.bigendian2int(php_substr(atom_data, 4, 4))
                    atom_structure["preload_flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data, 8, 4))
                    atom_structure["default_hints_raw"] = getid3_lib.bigendian2int(php_substr(atom_data, 12, 4))
                    atom_structure["default_hints"]["double_buffer"] = bool(atom_structure["default_hints_raw"] & 32)
                    atom_structure["default_hints"]["high_quality"] = bool(atom_structure["default_hints_raw"] & 256)
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
                    i = 0
                    while i < php_strlen(atom_data):
                        
                        php_no_error(lambda: atom_structure["track_id"][-1] = getid3_lib.bigendian2int(php_substr(atom_data, i, 4)))
                        i += 4
                    # end while
                    break
                # end if
                if case("elst"):
                    #// Edit LiST atom
                    atom_structure["version"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 1))
                    atom_structure["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data, 1, 3))
                    #// hardcoded: 0x0000
                    atom_structure["number_entries"] = getid3_lib.bigendian2int(php_substr(atom_data, 4, 4))
                    i = 0
                    while i < atom_structure["number_entries"]:
                        
                        atom_structure["edit_list"][i]["track_duration"] = getid3_lib.bigendian2int(php_substr(atom_data, 8 + i * 12 + 0, 4))
                        atom_structure["edit_list"][i]["media_time"] = getid3_lib.bigendian2int(php_substr(atom_data, 8 + i * 12 + 4, 4))
                        atom_structure["edit_list"][i]["media_rate"] = getid3_lib.fixedpoint16_16(php_substr(atom_data, 8 + i * 12 + 8, 4))
                        i += 1
                    # end while
                    break
                # end if
                if case("kmat"):
                    #// compressed MATte atom
                    atom_structure["version"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 1))
                    atom_structure["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data, 1, 3))
                    #// hardcoded: 0x0000
                    atom_structure["matte_data_raw"] = php_substr(atom_data, 4)
                    break
                # end if
                if case("ctab"):
                    #// Color TABle atom
                    atom_structure["color_table_seed"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 4))
                    #// hardcoded: 0x00000000
                    atom_structure["color_table_flags"] = getid3_lib.bigendian2int(php_substr(atom_data, 4, 2))
                    #// hardcoded: 0x8000
                    atom_structure["color_table_size"] = getid3_lib.bigendian2int(php_substr(atom_data, 6, 2)) + 1
                    colortableentry = 0
                    while colortableentry < atom_structure["color_table_size"]:
                        
                        atom_structure["color_table"][colortableentry]["alpha"] = getid3_lib.bigendian2int(php_substr(atom_data, 8 + colortableentry * 8 + 0, 2))
                        atom_structure["color_table"][colortableentry]["red"] = getid3_lib.bigendian2int(php_substr(atom_data, 8 + colortableentry * 8 + 2, 2))
                        atom_structure["color_table"][colortableentry]["green"] = getid3_lib.bigendian2int(php_substr(atom_data, 8 + colortableentry * 8 + 4, 2))
                        atom_structure["color_table"][colortableentry]["blue"] = getid3_lib.bigendian2int(php_substr(atom_data, 8 + colortableentry * 8 + 6, 2))
                        colortableentry += 1
                    # end while
                    break
                # end if
                if case("mvhd"):
                    #// MoVie HeaDer atom
                    atom_structure["version"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 1))
                    atom_structure["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data, 1, 3))
                    atom_structure["creation_time"] = getid3_lib.bigendian2int(php_substr(atom_data, 4, 4))
                    atom_structure["modify_time"] = getid3_lib.bigendian2int(php_substr(atom_data, 8, 4))
                    atom_structure["time_scale"] = getid3_lib.bigendian2int(php_substr(atom_data, 12, 4))
                    atom_structure["duration"] = getid3_lib.bigendian2int(php_substr(atom_data, 16, 4))
                    atom_structure["preferred_rate"] = getid3_lib.fixedpoint16_16(php_substr(atom_data, 20, 4))
                    atom_structure["preferred_volume"] = getid3_lib.fixedpoint8_8(php_substr(atom_data, 24, 2))
                    atom_structure["reserved"] = php_substr(atom_data, 26, 10)
                    atom_structure["matrix_a"] = getid3_lib.fixedpoint16_16(php_substr(atom_data, 36, 4))
                    atom_structure["matrix_b"] = getid3_lib.fixedpoint16_16(php_substr(atom_data, 40, 4))
                    atom_structure["matrix_u"] = getid3_lib.fixedpoint2_30(php_substr(atom_data, 44, 4))
                    atom_structure["matrix_c"] = getid3_lib.fixedpoint16_16(php_substr(atom_data, 48, 4))
                    atom_structure["matrix_d"] = getid3_lib.fixedpoint16_16(php_substr(atom_data, 52, 4))
                    atom_structure["matrix_v"] = getid3_lib.fixedpoint2_30(php_substr(atom_data, 56, 4))
                    atom_structure["matrix_x"] = getid3_lib.fixedpoint16_16(php_substr(atom_data, 60, 4))
                    atom_structure["matrix_y"] = getid3_lib.fixedpoint16_16(php_substr(atom_data, 64, 4))
                    atom_structure["matrix_w"] = getid3_lib.fixedpoint2_30(php_substr(atom_data, 68, 4))
                    atom_structure["preview_time"] = getid3_lib.bigendian2int(php_substr(atom_data, 72, 4))
                    atom_structure["preview_duration"] = getid3_lib.bigendian2int(php_substr(atom_data, 76, 4))
                    atom_structure["poster_time"] = getid3_lib.bigendian2int(php_substr(atom_data, 80, 4))
                    atom_structure["selection_time"] = getid3_lib.bigendian2int(php_substr(atom_data, 84, 4))
                    atom_structure["selection_duration"] = getid3_lib.bigendian2int(php_substr(atom_data, 88, 4))
                    atom_structure["current_time"] = getid3_lib.bigendian2int(php_substr(atom_data, 92, 4))
                    atom_structure["next_track_id"] = getid3_lib.bigendian2int(php_substr(atom_data, 96, 4))
                    if atom_structure["time_scale"] == 0:
                        self.error("Corrupt Quicktime file: mvhd.time_scale == zero")
                        return False
                    # end if
                    atom_structure["creation_time_unix"] = getid3_lib.datemac2unix(atom_structure["creation_time"])
                    atom_structure["modify_time_unix"] = getid3_lib.datemac2unix(atom_structure["modify_time"])
                    info["quicktime"]["time_scale"] = php_max(info["quicktime"]["time_scale"], atom_structure["time_scale"]) if (php_isset(lambda : info["quicktime"]["time_scale"])) and info["quicktime"]["time_scale"] < 1000 else atom_structure["time_scale"]
                    info["quicktime"]["display_scale"] = atom_structure["matrix_a"]
                    info["playtime_seconds"] = atom_structure["duration"] / atom_structure["time_scale"]
                    break
                # end if
                if case("tkhd"):
                    #// TracK HeaDer atom
                    atom_structure["version"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 1))
                    atom_structure["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data, 1, 3))
                    atom_structure["creation_time"] = getid3_lib.bigendian2int(php_substr(atom_data, 4, 4))
                    atom_structure["modify_time"] = getid3_lib.bigendian2int(php_substr(atom_data, 8, 4))
                    atom_structure["trackid"] = getid3_lib.bigendian2int(php_substr(atom_data, 12, 4))
                    atom_structure["reserved1"] = getid3_lib.bigendian2int(php_substr(atom_data, 16, 4))
                    atom_structure["duration"] = getid3_lib.bigendian2int(php_substr(atom_data, 20, 4))
                    atom_structure["reserved2"] = getid3_lib.bigendian2int(php_substr(atom_data, 24, 8))
                    atom_structure["layer"] = getid3_lib.bigendian2int(php_substr(atom_data, 32, 2))
                    atom_structure["alternate_group"] = getid3_lib.bigendian2int(php_substr(atom_data, 34, 2))
                    atom_structure["volume"] = getid3_lib.fixedpoint8_8(php_substr(atom_data, 36, 2))
                    atom_structure["reserved3"] = getid3_lib.bigendian2int(php_substr(atom_data, 38, 2))
                    #// http://developer.apple.com/library/mac/#documentation/QuickTime/RM/MovieBasics/MTEditing/K-Chapter/11MatrixFunctions.html
                    #// http://developer.apple.com/library/mac/#documentation/QuickTime/qtff/QTFFChap4/qtff4.html#//apple_ref/doc/uid/TP40000939-CH206-18737
                    atom_structure["matrix_a"] = getid3_lib.fixedpoint16_16(php_substr(atom_data, 40, 4))
                    atom_structure["matrix_b"] = getid3_lib.fixedpoint16_16(php_substr(atom_data, 44, 4))
                    atom_structure["matrix_u"] = getid3_lib.fixedpoint2_30(php_substr(atom_data, 48, 4))
                    atom_structure["matrix_c"] = getid3_lib.fixedpoint16_16(php_substr(atom_data, 52, 4))
                    atom_structure["matrix_d"] = getid3_lib.fixedpoint16_16(php_substr(atom_data, 56, 4))
                    atom_structure["matrix_v"] = getid3_lib.fixedpoint2_30(php_substr(atom_data, 60, 4))
                    atom_structure["matrix_x"] = getid3_lib.fixedpoint16_16(php_substr(atom_data, 64, 4))
                    atom_structure["matrix_y"] = getid3_lib.fixedpoint16_16(php_substr(atom_data, 68, 4))
                    atom_structure["matrix_w"] = getid3_lib.fixedpoint2_30(php_substr(atom_data, 72, 4))
                    atom_structure["width"] = getid3_lib.fixedpoint16_16(php_substr(atom_data, 76, 4))
                    atom_structure["height"] = getid3_lib.fixedpoint16_16(php_substr(atom_data, 80, 4))
                    atom_structure["flags"]["enabled"] = bool(atom_structure["flags_raw"] & 1)
                    atom_structure["flags"]["in_movie"] = bool(atom_structure["flags_raw"] & 2)
                    atom_structure["flags"]["in_preview"] = bool(atom_structure["flags_raw"] & 4)
                    atom_structure["flags"]["in_poster"] = bool(atom_structure["flags_raw"] & 8)
                    atom_structure["creation_time_unix"] = getid3_lib.datemac2unix(atom_structure["creation_time"])
                    atom_structure["modify_time_unix"] = getid3_lib.datemac2unix(atom_structure["modify_time"])
                    #// https://www.getid3.org/phpBB3/viewtopic.php?t=1908
                    #// attempt to compute rotation from matrix values
                    #// 2017-Dec-28: uncertain if 90/270 are correctly oriented; values returned by FixedPoint16_16 should perhaps be -1 instead of 65535(?)
                    matrixRotation = 0
                    for case in Switch(atom_structure["matrix_a"] + ":" + atom_structure["matrix_b"] + ":" + atom_structure["matrix_c"] + ":" + atom_structure["matrix_d"]):
                        if case("1:0:0:1"):
                            matrixRotation = 0
                            break
                        # end if
                        if case("0:1:65535:0"):
                            matrixRotation = 90
                            break
                        # end if
                        if case("65535:0:0:65535"):
                            matrixRotation = 180
                            break
                        # end if
                        if case("0:65535:1:0"):
                            matrixRotation = 270
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
                    if (not (php_isset(lambda : info["video"]["rotate"]))) or info["video"]["rotate"] == 0 and matrixRotation > 0:
                        info["quicktime"]["video"]["rotate"] = info["video"]["rotate"]
                    # end if
                    if atom_structure["flags"]["enabled"] == 1:
                        if (not (php_isset(lambda : info["video"]["resolution_x"]))) or (not (php_isset(lambda : info["video"]["resolution_y"]))):
                            info["video"]["resolution_x"] = atom_structure["width"]
                            info["video"]["resolution_y"] = atom_structure["height"]
                        # end if
                        info["video"]["resolution_x"] = php_max(info["video"]["resolution_x"], atom_structure["width"])
                        info["video"]["resolution_y"] = php_max(info["video"]["resolution_y"], atom_structure["height"])
                        info["quicktime"]["video"]["resolution_x"] = info["video"]["resolution_x"]
                        info["quicktime"]["video"]["resolution_y"] = info["video"]["resolution_y"]
                    else:
                        pass
                    # end if
                    break
                # end if
                if case("iods"):
                    #// Initial Object DeScriptor atom
                    #// http://www.koders.com/c/fid1FAB3E762903DC482D8A246D4A4BF9F28E049594.aspx?s=windows.h
                    #// http://libquicktime.sourcearchive.com/documentation/1.0.2plus-pdebian/iods_8c-source.html
                    offset = 0
                    atom_structure["version"] = getid3_lib.bigendian2int(php_substr(atom_data, offset, 1))
                    offset += 1
                    atom_structure["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data, offset, 3))
                    offset += 3
                    atom_structure["mp4_iod_tag"] = getid3_lib.bigendian2int(php_substr(atom_data, offset, 1))
                    offset += 1
                    atom_structure["length"] = self.quicktime_read_mp4_descr_length(atom_data, offset)
                    #// $offset already adjusted by quicktime_read_mp4_descr_length()
                    atom_structure["object_descriptor_id"] = getid3_lib.bigendian2int(php_substr(atom_data, offset, 2))
                    offset += 2
                    atom_structure["od_profile_level"] = getid3_lib.bigendian2int(php_substr(atom_data, offset, 1))
                    offset += 1
                    atom_structure["scene_profile_level"] = getid3_lib.bigendian2int(php_substr(atom_data, offset, 1))
                    offset += 1
                    atom_structure["audio_profile_id"] = getid3_lib.bigendian2int(php_substr(atom_data, offset, 1))
                    offset += 1
                    atom_structure["video_profile_id"] = getid3_lib.bigendian2int(php_substr(atom_data, offset, 1))
                    offset += 1
                    atom_structure["graphics_profile_level"] = getid3_lib.bigendian2int(php_substr(atom_data, offset, 1))
                    offset += 1
                    atom_structure["num_iods_tracks"] = atom_structure["length"] - 7 / 6
                    #// 6 bytes would only be right if all tracks use 1-byte length fields
                    i = 0
                    while i < atom_structure["num_iods_tracks"]:
                        
                        atom_structure["track"][i]["ES_ID_IncTag"] = getid3_lib.bigendian2int(php_substr(atom_data, offset, 1))
                        offset += 1
                        atom_structure["track"][i]["length"] = self.quicktime_read_mp4_descr_length(atom_data, offset)
                        #// $offset already adjusted by quicktime_read_mp4_descr_length()
                        atom_structure["track"][i]["track_id"] = getid3_lib.bigendian2int(php_substr(atom_data, offset, 4))
                        offset += 4
                        i += 1
                    # end while
                    atom_structure["audio_profile_name"] = self.quicktimeiodsaudioprofilename(atom_structure["audio_profile_id"])
                    atom_structure["video_profile_name"] = self.quicktimeiodsvideoprofilename(atom_structure["video_profile_id"])
                    break
                # end if
                if case("ftyp"):
                    #// FileTYPe (?) atom (for MP4 it seems)
                    atom_structure["signature"] = php_substr(atom_data, 0, 4)
                    atom_structure["unknown_1"] = getid3_lib.bigendian2int(php_substr(atom_data, 4, 4))
                    atom_structure["fourcc"] = php_substr(atom_data, 8, 4)
                    break
                # end if
                if case("mdat"):
                    #// Media DATa atom
                    #// 'mdat' contains the actual data for the audio/video, possibly also subtitles
                    #// due to lack of known documentation, this is a kludge implementation. If you know of documentation on how mdat is properly structed, please send it to info@getid3.org
                    #// first, skip any 'wide' padding, and second 'mdat' header (with specified size of zero?)
                    mdat_offset = 0
                    while True:
                        
                        if not (True):
                            break
                        # end if
                        if php_substr(atom_data, mdat_offset, 8) == "   " + "wide":
                            mdat_offset += 8
                        elif php_substr(atom_data, mdat_offset, 8) == "    " + "mdat":
                            mdat_offset += 8
                        else:
                            break
                        # end if
                    # end while
                    if php_substr(atom_data, mdat_offset, 4) == "GPRO":
                        GOPRO_chunk_length = getid3_lib.littleendian2int(php_substr(atom_data, mdat_offset + 4, 4))
                        GOPRO_offset = 8
                        atom_structure["GPRO"]["raw"] = php_substr(atom_data, mdat_offset + 8, GOPRO_chunk_length - 8)
                        atom_structure["GPRO"]["firmware"] = php_substr(atom_structure["GPRO"]["raw"], 0, 15)
                        atom_structure["GPRO"]["unknown1"] = php_substr(atom_structure["GPRO"]["raw"], 15, 16)
                        atom_structure["GPRO"]["unknown2"] = php_substr(atom_structure["GPRO"]["raw"], 31, 32)
                        atom_structure["GPRO"]["unknown3"] = php_substr(atom_structure["GPRO"]["raw"], 63, 16)
                        atom_structure["GPRO"]["camera"] = php_substr(atom_structure["GPRO"]["raw"], 79, 32)
                        info["quicktime"]["camera"]["model"] = php_rtrim(atom_structure["GPRO"]["camera"], " ")
                    # end if
                    #// check to see if it looks like chapter titles, in the form of unterminated strings with a leading 16-bit size field
                    while True:
                        chapter_string_length = getid3_lib.bigendian2int(php_substr(atom_data, mdat_offset, 2))
                        if not (mdat_offset < php_strlen(atom_data) - 8 and chapter_string_length and chapter_string_length < 1000 and chapter_string_length <= php_strlen(atom_data) - mdat_offset - 2 and php_preg_match("#^([\\x00-\\xFF]{2})([\\x20-\\xFF]+)$#", php_substr(atom_data, mdat_offset, chapter_string_length + 2), chapter_matches)):
                            break
                        # end if
                        dummy, chapter_string_length_hex, chapter_string = chapter_matches
                        mdat_offset += 2 + chapter_string_length
                        php_no_error(lambda: info["quicktime"]["comments"]["chapters"][-1] = chapter_string)
                        #// "encd" atom specifies encoding. In theory could be anything, almost always UTF-8, but may be UTF-16 with BOM (not currently handled)
                        if php_substr(atom_data, mdat_offset, 12) == "   encd   ":
                            #// UTF-8
                            mdat_offset += 12
                        # end if
                    # end while
                    if atomsize > 8 and (not (php_isset(lambda : info["avdataend_tmp"]))) or info["quicktime"][atomname]["size"] > info["avdataend_tmp"] - info["avdataoffset"]:
                        info["avdataoffset"] = atom_structure["offset"] + 8
                        #// $info['quicktime'][$atomname]['offset'] + 8;
                        OldAVDataEnd = info["avdataend"]
                        info["avdataend"] = atom_structure["offset"] + atom_structure["size"]
                        #// $info['quicktime'][$atomname]['offset'] + $info['quicktime'][$atomname]['size'];
                        getid3_temp = php_new_class("getID3", lambda : getID3())
                        getid3_temp.openfile(self.getid3.filename)
                        getid3_temp.info["avdataoffset"] = info["avdataoffset"]
                        getid3_temp.info["avdataend"] = info["avdataend"]
                        getid3_mp3 = php_new_class("getid3_mp3", lambda : getid3_mp3(getid3_temp))
                        if getid3_mp3.mpegaudioheadervalid(getid3_mp3.mpegaudioheaderdecode(self.fread(4))):
                            getid3_mp3.getonlympegaudioinfo(getid3_temp.info["avdataoffset"], False)
                            if (not php_empty(lambda : getid3_temp.info["warning"])):
                                for value in getid3_temp.info["warning"]:
                                    self.warning(value)
                                # end for
                            # end if
                            if (not php_empty(lambda : getid3_temp.info["mpeg"])):
                                info["mpeg"] = getid3_temp.info["mpeg"]
                                if (php_isset(lambda : info["mpeg"]["audio"])):
                                    info["audio"]["dataformat"] = "mp3"
                                    info["audio"]["codec"] = info["mpeg"]["audio"]["encoder"] if (not php_empty(lambda : info["mpeg"]["audio"]["encoder"])) else info["mpeg"]["audio"]["codec"] if (not php_empty(lambda : info["mpeg"]["audio"]["codec"])) else "LAME" if (not php_empty(lambda : info["mpeg"]["audio"]["LAME"])) else "mp3"
                                    info["audio"]["sample_rate"] = info["mpeg"]["audio"]["sample_rate"]
                                    info["audio"]["channels"] = info["mpeg"]["audio"]["channels"]
                                    info["audio"]["bitrate"] = info["mpeg"]["audio"]["bitrate"]
                                    info["audio"]["bitrate_mode"] = php_strtolower(info["mpeg"]["audio"]["bitrate_mode"])
                                    info["bitrate"] = info["audio"]["bitrate"]
                                # end if
                            # end if
                        # end if
                        getid3_mp3 = None
                        getid3_temp = None
                        info["avdataend"] = OldAVDataEnd
                        OldAVDataEnd = None
                    # end if
                    mdat_offset = None
                    chapter_string_length = None
                    chapter_matches = None
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
                    atom_structure["data"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 4))
                    break
                # end if
                if case("ctyp"):
                    #// Controller TYPe atom (seen on QTVR)
                    #// http://homepages.slingshot.co.nz/~helmboy/quicktime/formats/qtm-layout.txt
                    #// some controller names are:
                    #// 0x00 + 'std' for linear movie
                    #// 'none' for no controls
                    atom_structure["ctyp"] = php_substr(atom_data, 0, 4)
                    info["quicktime"]["controller"] = atom_structure["ctyp"]
                    for case in Switch(atom_structure["ctyp"]):
                        if case("qtvr"):
                            info["video"]["dataformat"] = "quicktimevr"
                            break
                        # end if
                    # end for
                    break
                # end if
                if case("pano"):
                    #// PANOrama track (seen on QTVR)
                    atom_structure["pano"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 4))
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
                    info["quicktime"]["hinting"] = True
                    break
                # end if
                if case("imgt"):
                    #// IMaGe Track reference (kQTVRImageTrackRefType) (seen on QTVR)
                    i = 0
                    while i < atom_structure["size"] - 8:
                        
                        atom_structure["imgt"][-1] = getid3_lib.bigendian2int(php_substr(atom_data, i, 4))
                        i += 4
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
                    atom_structure["data"] = atom_data
                    if php_preg_match("#([\\+\\-][0-9\\.]+)([\\+\\-][0-9\\.]+)([\\+\\-][0-9\\.]+)?/$#i", atom_data, matches):
                        php_no_error(lambda: all, latitude, longitude, altitude = matches)
                        info["quicktime"]["comments"]["gps_latitude"][-1] = floatval(latitude)
                        info["quicktime"]["comments"]["gps_longitude"][-1] = floatval(longitude)
                        if (not php_empty(lambda : altitude)):
                            info["quicktime"]["comments"]["gps_altitude"][-1] = floatval(altitude)
                        # end if
                    else:
                        self.warning("QuickTime atom \"Â©xyz\" data does not match expected data pattern at offset " + baseoffset + ". Please report as getID3() bug.")
                    # end if
                    break
                # end if
                if case("NCDT"):
                    #// http://www.sno.phy.queensu.ca/~phil/exiftool/TagNames/Nikon.html
                    #// Nikon-specific QuickTime tags found in the NCDT atom of MOV videos from some Nikon cameras such as the Coolpix S8000 and D5100
                    atom_structure["subatoms"] = self.quicktimeparsecontaineratom(atom_data, baseoffset + 4, atomHierarchy, ParseAllPossibleAtoms)
                    break
                # end if
                if case("NCTH"):
                    pass
                # end if
                if case("NCVW"):
                    #// Nikon Camera preVieW image
                    #// http://www.sno.phy.queensu.ca/~phil/exiftool/TagNames/Nikon.html
                    if php_preg_match("/^\\xFF\\xD8\\xFF/", atom_data):
                        atom_structure["data"] = atom_data
                        atom_structure["image_mime"] = "image/jpeg"
                        atom_structure["description"] = "Nikon Camera Thumbnail Image" if atomname == "NCTH" else "Nikon Camera Preview Image" if atomname == "NCVW" else "Nikon preview image"
                        info["quicktime"]["comments"]["picture"][-1] = Array({"image_mime": atom_structure["image_mime"], "data": atom_data, "description": atom_structure["description"]})
                    # end if
                    break
                # end if
                if case("NCTG"):
                    #// Nikon - http://www.sno.phy.queensu.ca/~phil/exiftool/TagNames/Nikon.html#NCTG
                    atom_structure["data"] = self.quicktimeparsenikonnctg(atom_data)
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
                    atom_structure["data"] = atom_data
                    break
                # end if
                if case("    "):
                    #// some kind of metacontainer, may contain a big data dump such as:
                    #// mdta keys \005 mdtacom.apple.quicktime.make (mdtacom.apple.quicktime.creationdate ,mdtacom.apple.quicktime.location.ISO6709 $mdtacom.apple.quicktime.software !mdtacom.apple.quicktime.model ilst \01D \001 \015data \001DE\010Apple 0 \002 (data \001DE\0102011-05-11T17:54:04+0200 2 \003 *data \001DE\010+52.4936+013.3897+040.247/ \01D \004 \015data \001DE\0104.3.1 \005 \018data \001DE\010iPhone 4
                    #// http://www.geocities.com/xhelmboyx/quicktime/formats/qti-layout.txt
                    atom_structure["version"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 1))
                    atom_structure["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data, 1, 3))
                    atom_structure["subatoms"] = self.quicktimeparsecontaineratom(php_substr(atom_data, 4), baseoffset + 8, atomHierarchy, ParseAllPossibleAtoms)
                    break
                # end if
                if case("meta"):
                    #// METAdata atom
                    #// https://developer.apple.com/library/mac/documentation/QuickTime/QTFF/Metadata/Metadata.html
                    atom_structure["version"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 1))
                    atom_structure["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data, 1, 3))
                    atom_structure["subatoms"] = self.quicktimeparsecontaineratom(atom_data, baseoffset + 8, atomHierarchy, ParseAllPossibleAtoms)
                    break
                # end if
                if case("data"):
                    metaDATAkey = 1
                    #// real ugly, but so is the QuickTime structure that stores keys and values in different multinested locations that are hard to relate to each other
                    #// seems to be 2 bytes language code (ASCII), 2 bytes unknown (set to 0x10B5 in sample I have), remainder is useful data
                    atom_structure["language"] = php_substr(atom_data, 4 + 0, 2)
                    atom_structure["unknown"] = getid3_lib.bigendian2int(php_substr(atom_data, 4 + 2, 2))
                    atom_structure["data"] = php_substr(atom_data, 4 + 4)
                    atom_structure["key_name"] = php_no_error(lambda: info["quicktime"]["temp_meta_key_names"][metaDATAkey])
                    metaDATAkey += 1
                    if atom_structure["key_name"] and atom_structure["data"]:
                        php_no_error(lambda: info["quicktime"]["comments"][php_str_replace("com.apple.quicktime.", "", atom_structure["key_name"])][-1] = atom_structure["data"])
                    # end if
                    break
                # end if
                if case("keys"):
                    #// KEYS that may be present in the metadata atom.
                    #// https://developer.apple.com/library/mac/documentation/QuickTime/QTFF/Metadata/Metadata.html#//apple_ref/doc/uid/TP40000939-CH1-SW21
                    #// The metadata item keys atom holds a list of the metadata keys that may be present in the metadata atom.
                    #// This list is indexed starting with 1; 0 is a reserved index value. The metadata item keys atom is a full atom with an atom type of "keys".
                    atom_structure["version"] = getid3_lib.bigendian2int(php_substr(atom_data, 0, 1))
                    atom_structure["flags_raw"] = getid3_lib.bigendian2int(php_substr(atom_data, 1, 3))
                    atom_structure["entry_count"] = getid3_lib.bigendian2int(php_substr(atom_data, 4, 4))
                    keys_atom_offset = 8
                    i = 1
                    while i <= atom_structure["entry_count"]:
                        
                        atom_structure["keys"][i]["key_size"] = getid3_lib.bigendian2int(php_substr(atom_data, keys_atom_offset + 0, 4))
                        atom_structure["keys"][i]["key_namespace"] = php_substr(atom_data, keys_atom_offset + 4, 4)
                        atom_structure["keys"][i]["key_value"] = php_substr(atom_data, keys_atom_offset + 8, atom_structure["keys"][i]["key_size"] - 8)
                        keys_atom_offset += atom_structure["keys"][i]["key_size"]
                        #// key_size includes the 4+4 bytes for key_size and key_namespace
                        info["quicktime"]["temp_meta_key_names"][i] = atom_structure["keys"][i]["key_value"]
                        i += 1
                    # end while
                    break
                # end if
                if case("gps "):
                    #// https://dashcamtalk.com/forum/threads/script-to-extract-gps-data-from-novatek-mp4.20808/page-2#post-291730
                    #// The 'gps ' contains simple look up table made up of 8byte rows, that point to the 'free' atoms that contains the actual GPS data.
                    #// The first row is version/metadata/notsure, I skip that.
                    #// The following rows consist of 4byte address (absolute) and 4byte size (0x1000), these point to the GPS data in the file.
                    GPS_rowsize = 8
                    #// 4 bytes for offset, 4 bytes for size
                    if php_strlen(atom_data) > 0:
                        if php_strlen(atom_data) % GPS_rowsize == 0:
                            atom_structure["gps_toc"] = Array()
                            for counter,datapair in str_split(atom_data, GPS_rowsize):
                                atom_structure["gps_toc"][-1] = unpack("Noffset/Nsize", php_substr(atom_data, counter * GPS_rowsize, GPS_rowsize))
                            # end for
                            atom_structure["gps_entries"] = Array()
                            previous_offset = self.ftell()
                            for key,gps_pointer in atom_structure["gps_toc"]:
                                if key == 0:
                                    continue
                                # end if
                                self.fseek(gps_pointer["offset"])
                                GPS_free_data = self.fread(gps_pointer["size"])
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
                                if php_preg_match("#\\$GPRMC,([0-9\\.]*),([AV]),([0-9\\.]*),([NS]),([0-9\\.]*),([EW]),([0-9\\.]*),([0-9\\.]*),([0-9]*),([0-9\\.]*),([EW]?)(,[A])?(\\*[0-9A-F]{2})#", GPS_free_data, matches):
                                    GPS_this_GPRMC = Array()
                                    GPS_this_GPRMC["raw"]["gprmc"], GPS_this_GPRMC["raw"]["timestamp"], GPS_this_GPRMC["raw"]["status"], GPS_this_GPRMC["raw"]["latitude"], GPS_this_GPRMC["raw"]["latitude_direction"], GPS_this_GPRMC["raw"]["longitude"], GPS_this_GPRMC["raw"]["longitude_direction"], GPS_this_GPRMC["raw"]["knots"], GPS_this_GPRMC["raw"]["angle"], GPS_this_GPRMC["raw"]["datestamp"], GPS_this_GPRMC["raw"]["variation"], GPS_this_GPRMC["raw"]["variation_direction"], dummy, GPS_this_GPRMC["raw"]["checksum"] = matches
                                    hour = php_substr(GPS_this_GPRMC["raw"]["timestamp"], 0, 2)
                                    minute = php_substr(GPS_this_GPRMC["raw"]["timestamp"], 2, 2)
                                    second = php_substr(GPS_this_GPRMC["raw"]["timestamp"], 4, 2)
                                    ms = php_substr(GPS_this_GPRMC["raw"]["timestamp"], 6)
                                    #// may contain decimal seconds
                                    day = php_substr(GPS_this_GPRMC["raw"]["datestamp"], 0, 2)
                                    month = php_substr(GPS_this_GPRMC["raw"]["datestamp"], 2, 2)
                                    year = php_substr(GPS_this_GPRMC["raw"]["datestamp"], 4, 2)
                                    year += 1900 if year > 90 else 2000
                                    #// complete lack of foresight: datestamps are stored with 2-digit years, take best guess
                                    GPS_this_GPRMC["timestamp"] = year + "-" + month + "-" + day + " " + hour + ":" + minute + ":" + second + ms
                                    GPS_this_GPRMC["active"] = GPS_this_GPRMC["raw"]["status"] == "A"
                                    #// A=Active,V=Void
                                    for latlon in Array("latitude", "longitude"):
                                        php_preg_match("#^([0-9]{1,3})([0-9]{2}\\.[0-9]+)$#", GPS_this_GPRMC["raw"][latlon], matches)
                                        dummy, deg, min = matches
                                        GPS_this_GPRMC[latlon] = deg + min / 60
                                    # end for
                                    GPS_this_GPRMC["latitude"] *= -1 if GPS_this_GPRMC["raw"]["latitude_direction"] == "S" else 1
                                    GPS_this_GPRMC["longitude"] *= -1 if GPS_this_GPRMC["raw"]["longitude_direction"] == "W" else 1
                                    GPS_this_GPRMC["heading"] = GPS_this_GPRMC["raw"]["angle"]
                                    GPS_this_GPRMC["speed_knot"] = GPS_this_GPRMC["raw"]["knots"]
                                    GPS_this_GPRMC["speed_kmh"] = GPS_this_GPRMC["raw"]["knots"] * 1.852
                                    if GPS_this_GPRMC["raw"]["variation"]:
                                        GPS_this_GPRMC["variation"] = GPS_this_GPRMC["raw"]["variation"]
                                        GPS_this_GPRMC["variation"] *= -1 if GPS_this_GPRMC["raw"]["variation_direction"] == "W" else 1
                                    # end if
                                    atom_structure["gps_entries"][key] = GPS_this_GPRMC
                                    php_no_error(lambda: info["quicktime"]["gps_track"][GPS_this_GPRMC["timestamp"]] = Array({"latitude": float(GPS_this_GPRMC["latitude"]), "longitude": float(GPS_this_GPRMC["longitude"]), "speed_kmh": float(GPS_this_GPRMC["speed_kmh"]), "heading": float(GPS_this_GPRMC["heading"])}))
                                else:
                                    self.warning("Unhandled GPS format in \"free\" atom at offset " + gps_pointer["offset"])
                                # end if
                            # end for
                            self.fseek(previous_offset)
                        else:
                            self.warning("QuickTime atom \"" + atomname + "\" is not mod-8 bytes long (" + atomsize + " bytes) at offset " + baseoffset)
                        # end if
                    else:
                        self.warning("QuickTime atom \"" + atomname + "\" is zero bytes long at offset " + baseoffset)
                    # end if
                    break
                # end if
                if case("loci"):
                    #// 3GP location (El Loco)
                    loffset = 0
                    info["quicktime"]["comments"]["gps_flags"] = Array(getid3_lib.bigendian2int(php_substr(atom_data, 0, 4)))
                    info["quicktime"]["comments"]["gps_lang"] = Array(getid3_lib.bigendian2int(php_substr(atom_data, 4, 2)))
                    info["quicktime"]["comments"]["gps_location"] = Array(self.locistring(php_substr(atom_data, 6), loffset))
                    loci_data = php_substr(atom_data, 6 + loffset)
                    info["quicktime"]["comments"]["gps_role"] = Array(getid3_lib.bigendian2int(php_substr(loci_data, 0, 1)))
                    info["quicktime"]["comments"]["gps_longitude"] = Array(getid3_lib.fixedpoint16_16(php_substr(loci_data, 1, 4)))
                    info["quicktime"]["comments"]["gps_latitude"] = Array(getid3_lib.fixedpoint16_16(php_substr(loci_data, 5, 4)))
                    info["quicktime"]["comments"]["gps_altitude"] = Array(getid3_lib.fixedpoint16_16(php_substr(loci_data, 9, 4)))
                    info["quicktime"]["comments"]["gps_body"] = Array(self.locistring(php_substr(loci_data, 13), loffset))
                    info["quicktime"]["comments"]["gps_notes"] = Array(self.locistring(php_substr(loci_data, 13 + loffset), loffset))
                    break
                # end if
                if case("chpl"):
                    #// CHaPter List
                    #// https://www.adobe.com/content/dam/Adobe/en/devnet/flv/pdfs/video_file_format_spec_v10.pdf
                    chpl_version = getid3_lib.bigendian2int(php_substr(atom_data, 4, 1))
                    #// Expected to be 0
                    chpl_flags = getid3_lib.bigendian2int(php_substr(atom_data, 5, 3))
                    #// Reserved, set to 0
                    chpl_count = getid3_lib.bigendian2int(php_substr(atom_data, 8, 1))
                    chpl_offset = 9
                    i = 0
                    while i < chpl_count:
                        
                        if chpl_offset + 9 >= php_strlen(atom_data):
                            self.warning("QuickTime chapter " + i + " extends beyond end of \"chpl\" atom")
                            break
                        # end if
                        info["quicktime"]["chapters"][i]["timestamp"] = getid3_lib.bigendian2int(php_substr(atom_data, chpl_offset, 8)) / 10000000
                        #// timestamps are stored as 100-nanosecond units
                        chpl_offset += 8
                        chpl_title_size = getid3_lib.bigendian2int(php_substr(atom_data, chpl_offset, 1))
                        chpl_offset += 1
                        info["quicktime"]["chapters"][i]["title"] = php_substr(atom_data, chpl_offset, chpl_title_size)
                        chpl_offset += chpl_title_size
                        i += 1
                    # end while
                    break
                # end if
                if case("FIRM"):
                    #// FIRMware version(?), seen on GoPro Hero4
                    info["quicktime"]["camera"]["firmware"] = atom_data
                    break
                # end if
                if case("CAME"):
                    #// FIRMware version(?), seen on GoPro Hero4
                    info["quicktime"]["camera"]["serial_hash"] = unpack("H*", atom_data)
                    break
                # end if
                if case("dscp"):
                    pass
                # end if
                if case("rcif"):
                    #// https://www.getid3.org/phpBB3/viewtopic.php?t=1908
                    if php_substr(atom_data, 0, 7) == "    UÄ" + "{":
                        json_decoded = php_no_error(lambda: php_json_decode(php_rtrim(php_substr(atom_data, 6), " "), True))
                        if json_decoded:
                            info["quicktime"]["camera"][atomname] = json_decoded
                            if atomname == "rcif" and (php_isset(lambda : info["quicktime"]["camera"]["rcif"]["wxcamera"]["rotate"])):
                                info["video"]["rotate"] = info["quicktime"]["video"]["rotate"]
                            # end if
                        else:
                            self.warning("Failed to JSON decode atom \"" + atomname + "\"")
                            atom_structure["data"] = atom_data
                        # end if
                        json_decoded = None
                    else:
                        self.warning("Expecting 55 C4 7B at start of atom \"" + atomname + "\", found " + getid3_lib.printhexbytes(php_substr(atom_data, 4, 3)) + " instead")
                        atom_structure["data"] = atom_data
                    # end if
                    break
                # end if
                if case("frea"):
                    #// https://www.sno.phy.queensu.ca/~phil/exiftool/TagNames/Kodak.html#frea
                    #// may contain "scra" (PreviewImage) and/or "thma" (ThumbnailImage)
                    atom_structure["subatoms"] = self.quicktimeparsecontaineratom(atom_data, baseoffset + 4, atomHierarchy, ParseAllPossibleAtoms)
                    break
                # end if
                if case("tima"):
                    #// subatom to "frea"
                    #// no idea what this does, the one sample file I've seen has a value of 0x00000027
                    atom_structure["data"] = atom_data
                    break
                # end if
                if case("ver "):
                    #// subatom to "frea"
                    #// some kind of version number, the one sample file I've seen has a value of "3.00.073"
                    atom_structure["data"] = atom_data
                    break
                # end if
                if case("thma"):
                    #// subatom to "frea" -- "ThumbnailImage"
                    #// https://www.sno.phy.queensu.ca/~phil/exiftool/TagNames/Kodak.html#frea
                    if php_strlen(atom_data) > 0:
                        info["quicktime"]["comments"]["picture"][-1] = Array({"data": atom_data, "image_mime": "image/jpeg"})
                    # end if
                    break
                # end if
                if case("scra"):
                    #// subatom to "frea" -- "PreviewImage"
                    #// https://www.sno.phy.queensu.ca/~phil/exiftool/TagNames/Kodak.html#frea
                    #// but the only sample file I've seen has no useful data here
                    if php_strlen(atom_data) > 0:
                        info["quicktime"]["comments"]["picture"][-1] = Array({"data": atom_data, "image_mime": "image/jpeg"})
                    # end if
                    break
                # end if
                if case():
                    self.warning("Unknown QuickTime atom type: \"" + php_preg_replace("#[^a-zA-Z0-9 _\\-]#", "?", atomname) + "\" (" + php_trim(getid3_lib.printhexbytes(atomname)) + "), " + atomsize + " bytes at offset " + baseoffset)
                    atom_structure["data"] = atom_data
                    break
                # end if
            # end for
        # end if
        php_array_pop(atomHierarchy)
        return atom_structure
    # end def quicktimeparseatom
    #// 
    #// @param string $atom_data
    #// @param int    $baseoffset
    #// @param array  $atomHierarchy
    #// @param bool   $ParseAllPossibleAtoms
    #// 
    #// @return array|false
    #//
    def quicktimeparsecontaineratom(self, atom_data=None, baseoffset=None, atomHierarchy=None, ParseAllPossibleAtoms=None):
        
        atom_structure = False
        subatomoffset = 0
        subatomcounter = 0
        if php_strlen(atom_data) == 4 and getid3_lib.bigendian2int(atom_data) == 0:
            return False
        # end if
        while True:
            
            if not (subatomoffset < php_strlen(atom_data)):
                break
            # end if
            subatomsize = getid3_lib.bigendian2int(php_substr(atom_data, subatomoffset + 0, 4))
            subatomname = php_substr(atom_data, subatomoffset + 4, 4)
            subatomdata = php_substr(atom_data, subatomoffset + 8, subatomsize - 8)
            if subatomsize == 0:
                #// Furthermore, for historical reasons the list of atoms is optionally
                #// terminated by a 32-bit integer set to 0. If you are writing a program
                #// to read user data atoms, you should allow for the terminating 0.
                if php_strlen(atom_data) > 12:
                    subatomoffset += 4
                    continue
                # end if
                return atom_structure
            # end if
            atom_structure[subatomcounter] = self.quicktimeparseatom(subatomname, subatomsize, subatomdata, baseoffset + subatomoffset, atomHierarchy, ParseAllPossibleAtoms)
            subatomcounter += 1
            subatomoffset += subatomsize
        # end while
        return atom_structure
    # end def quicktimeparsecontaineratom
    subatomcounter += 1
    #// 
    #// @param string $data
    #// @param int    $offset
    #// 
    #// @return int
    #//
    def quicktime_read_mp4_descr_length(self, data=None, offset=None):
        
        #// http://libquicktime.sourcearchive.com/documentation/2:1.0.2plus-pdebian-2build1/esds_8c-source.html
        num_bytes = 0
        length = 0
        while True:
            b = php_ord(php_substr(data, offset, 1))
            offset += 1
            length = length << 7 | b & 127
            
            if b & 128 and num_bytes < 4:
                break
            # end if
        # end while
        num_bytes += 1
        return length
    # end def quicktime_read_mp4_descr_length
    #// 
    #// @param int $languageid
    #// 
    #// @return string
    #//
    def quicktimelanguagelookup(self, languageid=None):
        
        QuicktimeLanguageLookup = Array()
        if php_empty(lambda : QuicktimeLanguageLookup):
            QuicktimeLanguageLookup[0] = "English"
            QuicktimeLanguageLookup[1] = "French"
            QuicktimeLanguageLookup[2] = "German"
            QuicktimeLanguageLookup[3] = "Italian"
            QuicktimeLanguageLookup[4] = "Dutch"
            QuicktimeLanguageLookup[5] = "Swedish"
            QuicktimeLanguageLookup[6] = "Spanish"
            QuicktimeLanguageLookup[7] = "Danish"
            QuicktimeLanguageLookup[8] = "Portuguese"
            QuicktimeLanguageLookup[9] = "Norwegian"
            QuicktimeLanguageLookup[10] = "Hebrew"
            QuicktimeLanguageLookup[11] = "Japanese"
            QuicktimeLanguageLookup[12] = "Arabic"
            QuicktimeLanguageLookup[13] = "Finnish"
            QuicktimeLanguageLookup[14] = "Greek"
            QuicktimeLanguageLookup[15] = "Icelandic"
            QuicktimeLanguageLookup[16] = "Maltese"
            QuicktimeLanguageLookup[17] = "Turkish"
            QuicktimeLanguageLookup[18] = "Croatian"
            QuicktimeLanguageLookup[19] = "Chinese (Traditional)"
            QuicktimeLanguageLookup[20] = "Urdu"
            QuicktimeLanguageLookup[21] = "Hindi"
            QuicktimeLanguageLookup[22] = "Thai"
            QuicktimeLanguageLookup[23] = "Korean"
            QuicktimeLanguageLookup[24] = "Lithuanian"
            QuicktimeLanguageLookup[25] = "Polish"
            QuicktimeLanguageLookup[26] = "Hungarian"
            QuicktimeLanguageLookup[27] = "Estonian"
            QuicktimeLanguageLookup[28] = "Lettish"
            QuicktimeLanguageLookup[28] = "Latvian"
            QuicktimeLanguageLookup[29] = "Saamisk"
            QuicktimeLanguageLookup[29] = "Lappish"
            QuicktimeLanguageLookup[30] = "Faeroese"
            QuicktimeLanguageLookup[31] = "Farsi"
            QuicktimeLanguageLookup[31] = "Persian"
            QuicktimeLanguageLookup[32] = "Russian"
            QuicktimeLanguageLookup[33] = "Chinese (Simplified)"
            QuicktimeLanguageLookup[34] = "Flemish"
            QuicktimeLanguageLookup[35] = "Irish"
            QuicktimeLanguageLookup[36] = "Albanian"
            QuicktimeLanguageLookup[37] = "Romanian"
            QuicktimeLanguageLookup[38] = "Czech"
            QuicktimeLanguageLookup[39] = "Slovak"
            QuicktimeLanguageLookup[40] = "Slovenian"
            QuicktimeLanguageLookup[41] = "Yiddish"
            QuicktimeLanguageLookup[42] = "Serbian"
            QuicktimeLanguageLookup[43] = "Macedonian"
            QuicktimeLanguageLookup[44] = "Bulgarian"
            QuicktimeLanguageLookup[45] = "Ukrainian"
            QuicktimeLanguageLookup[46] = "Byelorussian"
            QuicktimeLanguageLookup[47] = "Uzbek"
            QuicktimeLanguageLookup[48] = "Kazakh"
            QuicktimeLanguageLookup[49] = "Azerbaijani"
            QuicktimeLanguageLookup[50] = "AzerbaijanAr"
            QuicktimeLanguageLookup[51] = "Armenian"
            QuicktimeLanguageLookup[52] = "Georgian"
            QuicktimeLanguageLookup[53] = "Moldavian"
            QuicktimeLanguageLookup[54] = "Kirghiz"
            QuicktimeLanguageLookup[55] = "Tajiki"
            QuicktimeLanguageLookup[56] = "Turkmen"
            QuicktimeLanguageLookup[57] = "Mongolian"
            QuicktimeLanguageLookup[58] = "MongolianCyr"
            QuicktimeLanguageLookup[59] = "Pashto"
            QuicktimeLanguageLookup[60] = "Kurdish"
            QuicktimeLanguageLookup[61] = "Kashmiri"
            QuicktimeLanguageLookup[62] = "Sindhi"
            QuicktimeLanguageLookup[63] = "Tibetan"
            QuicktimeLanguageLookup[64] = "Nepali"
            QuicktimeLanguageLookup[65] = "Sanskrit"
            QuicktimeLanguageLookup[66] = "Marathi"
            QuicktimeLanguageLookup[67] = "Bengali"
            QuicktimeLanguageLookup[68] = "Assamese"
            QuicktimeLanguageLookup[69] = "Gujarati"
            QuicktimeLanguageLookup[70] = "Punjabi"
            QuicktimeLanguageLookup[71] = "Oriya"
            QuicktimeLanguageLookup[72] = "Malayalam"
            QuicktimeLanguageLookup[73] = "Kannada"
            QuicktimeLanguageLookup[74] = "Tamil"
            QuicktimeLanguageLookup[75] = "Telugu"
            QuicktimeLanguageLookup[76] = "Sinhalese"
            QuicktimeLanguageLookup[77] = "Burmese"
            QuicktimeLanguageLookup[78] = "Khmer"
            QuicktimeLanguageLookup[79] = "Lao"
            QuicktimeLanguageLookup[80] = "Vietnamese"
            QuicktimeLanguageLookup[81] = "Indonesian"
            QuicktimeLanguageLookup[82] = "Tagalog"
            QuicktimeLanguageLookup[83] = "MalayRoman"
            QuicktimeLanguageLookup[84] = "MalayArabic"
            QuicktimeLanguageLookup[85] = "Amharic"
            QuicktimeLanguageLookup[86] = "Tigrinya"
            QuicktimeLanguageLookup[87] = "Galla"
            QuicktimeLanguageLookup[87] = "Oromo"
            QuicktimeLanguageLookup[88] = "Somali"
            QuicktimeLanguageLookup[89] = "Swahili"
            QuicktimeLanguageLookup[90] = "Ruanda"
            QuicktimeLanguageLookup[91] = "Rundi"
            QuicktimeLanguageLookup[92] = "Chewa"
            QuicktimeLanguageLookup[93] = "Malagasy"
            QuicktimeLanguageLookup[94] = "Esperanto"
            QuicktimeLanguageLookup[128] = "Welsh"
            QuicktimeLanguageLookup[129] = "Basque"
            QuicktimeLanguageLookup[130] = "Catalan"
            QuicktimeLanguageLookup[131] = "Latin"
            QuicktimeLanguageLookup[132] = "Quechua"
            QuicktimeLanguageLookup[133] = "Guarani"
            QuicktimeLanguageLookup[134] = "Aymara"
            QuicktimeLanguageLookup[135] = "Tatar"
            QuicktimeLanguageLookup[136] = "Uighur"
            QuicktimeLanguageLookup[137] = "Dzongkha"
            QuicktimeLanguageLookup[138] = "JavaneseRom"
            QuicktimeLanguageLookup[32767] = "Unspecified"
        # end if
        if languageid > 138 and languageid < 32767:
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
            iso_language_id = ""
            iso_language_id += chr(languageid & 31744 >> 10 + 96)
            iso_language_id += chr(languageid & 992 >> 5 + 96)
            iso_language_id += chr(languageid & 31 >> 0 + 96)
            QuicktimeLanguageLookup[languageid] = getid3_id3v2.languagelookup(iso_language_id)
        # end if
        return QuicktimeLanguageLookup[languageid] if (php_isset(lambda : QuicktimeLanguageLookup[languageid])) else "invalid"
    # end def quicktimelanguagelookup
    #// 
    #// @param string $codecid
    #// 
    #// @return string
    #//
    def quicktimevideocodeclookup(self, codecid=None):
        
        QuicktimeVideoCodecLookup = Array()
        if php_empty(lambda : QuicktimeVideoCodecLookup):
            QuicktimeVideoCodecLookup[".SGI"] = "SGI"
            QuicktimeVideoCodecLookup["3IV1"] = "3ivx MPEG-4 v1"
            QuicktimeVideoCodecLookup["3IV2"] = "3ivx MPEG-4 v2"
            QuicktimeVideoCodecLookup["3IVX"] = "3ivx MPEG-4"
            QuicktimeVideoCodecLookup["8BPS"] = "Planar RGB"
            QuicktimeVideoCodecLookup["avc1"] = "H.264/MPEG-4 AVC"
            QuicktimeVideoCodecLookup["avr "] = "AVR-JPEG"
            QuicktimeVideoCodecLookup["b16g"] = "16Gray"
            QuicktimeVideoCodecLookup["b32a"] = "32AlphaGray"
            QuicktimeVideoCodecLookup["b48r"] = "48RGB"
            QuicktimeVideoCodecLookup["b64a"] = "64ARGB"
            QuicktimeVideoCodecLookup["base"] = "Base"
            QuicktimeVideoCodecLookup["clou"] = "Cloud"
            QuicktimeVideoCodecLookup["cmyk"] = "CMYK"
            QuicktimeVideoCodecLookup["cvid"] = "Cinepak"
            QuicktimeVideoCodecLookup["dmb1"] = "OpenDML JPEG"
            QuicktimeVideoCodecLookup["dvc "] = "DVC-NTSC"
            QuicktimeVideoCodecLookup["dvcp"] = "DVC-PAL"
            QuicktimeVideoCodecLookup["dvpn"] = "DVCPro-NTSC"
            QuicktimeVideoCodecLookup["dvpp"] = "DVCPro-PAL"
            QuicktimeVideoCodecLookup["fire"] = "Fire"
            QuicktimeVideoCodecLookup["flic"] = "FLC"
            QuicktimeVideoCodecLookup["gif "] = "GIF"
            QuicktimeVideoCodecLookup["h261"] = "H261"
            QuicktimeVideoCodecLookup["h263"] = "H263"
            QuicktimeVideoCodecLookup["IV41"] = "Indeo4"
            QuicktimeVideoCodecLookup["jpeg"] = "JPEG"
            QuicktimeVideoCodecLookup["kpcd"] = "PhotoCD"
            QuicktimeVideoCodecLookup["mjpa"] = "Motion JPEG-A"
            QuicktimeVideoCodecLookup["mjpb"] = "Motion JPEG-B"
            QuicktimeVideoCodecLookup["msvc"] = "Microsoft Video1"
            QuicktimeVideoCodecLookup["myuv"] = "MPEG YUV420"
            QuicktimeVideoCodecLookup["path"] = "Vector"
            QuicktimeVideoCodecLookup["png "] = "PNG"
            QuicktimeVideoCodecLookup["PNTG"] = "MacPaint"
            QuicktimeVideoCodecLookup["qdgx"] = "QuickDrawGX"
            QuicktimeVideoCodecLookup["qdrw"] = "QuickDraw"
            QuicktimeVideoCodecLookup["raw "] = "RAW"
            QuicktimeVideoCodecLookup["ripl"] = "WaterRipple"
            QuicktimeVideoCodecLookup["rpza"] = "Video"
            QuicktimeVideoCodecLookup["smc "] = "Graphics"
            QuicktimeVideoCodecLookup["SVQ1"] = "Sorenson Video 1"
            QuicktimeVideoCodecLookup["SVQ1"] = "Sorenson Video 3"
            QuicktimeVideoCodecLookup["syv9"] = "Sorenson YUV9"
            QuicktimeVideoCodecLookup["tga "] = "Targa"
            QuicktimeVideoCodecLookup["tiff"] = "TIFF"
            QuicktimeVideoCodecLookup["WRAW"] = "Windows RAW"
            QuicktimeVideoCodecLookup["WRLE"] = "BMP"
            QuicktimeVideoCodecLookup["y420"] = "YUV420"
            QuicktimeVideoCodecLookup["yuv2"] = "ComponentVideo"
            QuicktimeVideoCodecLookup["yuvs"] = "ComponentVideoUnsigned"
            QuicktimeVideoCodecLookup["yuvu"] = "ComponentVideoSigned"
        # end if
        return QuicktimeVideoCodecLookup[codecid] if (php_isset(lambda : QuicktimeVideoCodecLookup[codecid])) else ""
    # end def quicktimevideocodeclookup
    #// 
    #// @param string $codecid
    #// 
    #// @return mixed|string
    #//
    def quicktimeaudiocodeclookup(self, codecid=None):
        
        QuicktimeAudioCodecLookup = Array()
        if php_empty(lambda : QuicktimeAudioCodecLookup):
            QuicktimeAudioCodecLookup[".mp3"] = "Fraunhofer MPEG Layer-III alias"
            QuicktimeAudioCodecLookup["aac "] = "ISO/IEC 14496-3 AAC"
            QuicktimeAudioCodecLookup["agsm"] = "Apple GSM 10:1"
            QuicktimeAudioCodecLookup["alac"] = "Apple Lossless Audio Codec"
            QuicktimeAudioCodecLookup["alaw"] = "A-law 2:1"
            QuicktimeAudioCodecLookup["conv"] = "Sample Format"
            QuicktimeAudioCodecLookup["dvca"] = "DV"
            QuicktimeAudioCodecLookup["dvi "] = "DV 4:1"
            QuicktimeAudioCodecLookup["eqal"] = "Frequency Equalizer"
            QuicktimeAudioCodecLookup["fl32"] = "32-bit Floating Point"
            QuicktimeAudioCodecLookup["fl64"] = "64-bit Floating Point"
            QuicktimeAudioCodecLookup["ima4"] = "Interactive Multimedia Association 4:1"
            QuicktimeAudioCodecLookup["in24"] = "24-bit Integer"
            QuicktimeAudioCodecLookup["in32"] = "32-bit Integer"
            QuicktimeAudioCodecLookup["lpc "] = "LPC 23:1"
            QuicktimeAudioCodecLookup["MAC3"] = "Macintosh Audio Compression/Expansion (MACE) 3:1"
            QuicktimeAudioCodecLookup["MAC6"] = "Macintosh Audio Compression/Expansion (MACE) 6:1"
            QuicktimeAudioCodecLookup["mixb"] = "8-bit Mixer"
            QuicktimeAudioCodecLookup["mixw"] = "16-bit Mixer"
            QuicktimeAudioCodecLookup["mp4a"] = "ISO/IEC 14496-3 AAC"
            QuicktimeAudioCodecLookup["MS" + " "] = "Microsoft ADPCM"
            QuicktimeAudioCodecLookup["MS" + " "] = "DV IMA"
            QuicktimeAudioCodecLookup["MS" + " U"] = "Fraunhofer MPEG Layer III"
            QuicktimeAudioCodecLookup["NONE"] = "No Encoding"
            QuicktimeAudioCodecLookup["Qclp"] = "Qualcomm PureVoice"
            QuicktimeAudioCodecLookup["QDM2"] = "QDesign Music 2"
            QuicktimeAudioCodecLookup["QDMC"] = "QDesign Music 1"
            QuicktimeAudioCodecLookup["ratb"] = "8-bit Rate"
            QuicktimeAudioCodecLookup["ratw"] = "16-bit Rate"
            QuicktimeAudioCodecLookup["raw "] = "raw PCM"
            QuicktimeAudioCodecLookup["sour"] = "Sound Source"
            QuicktimeAudioCodecLookup["sowt"] = "signed/two's complement (Little Endian)"
            QuicktimeAudioCodecLookup["str1"] = "Iomega MPEG layer II"
            QuicktimeAudioCodecLookup["str2"] = "Iomega MPEG *layer II"
            QuicktimeAudioCodecLookup["str3"] = "Iomega MPEG **layer II"
            QuicktimeAudioCodecLookup["str4"] = "Iomega MPEG ***layer II"
            QuicktimeAudioCodecLookup["twos"] = "signed/two's complement (Big Endian)"
            QuicktimeAudioCodecLookup["ulaw"] = "mu-law 2:1"
        # end if
        return QuicktimeAudioCodecLookup[codecid] if (php_isset(lambda : QuicktimeAudioCodecLookup[codecid])) else ""
    # end def quicktimeaudiocodeclookup
    #// 
    #// @param string $compressionid
    #// 
    #// @return string
    #//
    def quicktimedcomlookup(self, compressionid=None):
        
        QuicktimeDCOMLookup = Array()
        if php_empty(lambda : QuicktimeDCOMLookup):
            QuicktimeDCOMLookup["zlib"] = "ZLib Deflate"
            QuicktimeDCOMLookup["adec"] = "Apple Compression"
        # end if
        return QuicktimeDCOMLookup[compressionid] if (php_isset(lambda : QuicktimeDCOMLookup[compressionid])) else ""
    # end def quicktimedcomlookup
    #// 
    #// @param int $colordepthid
    #// 
    #// @return string
    #//
    def quicktimecolornamelookup(self, colordepthid=None):
        
        QuicktimeColorNameLookup = Array()
        if php_empty(lambda : QuicktimeColorNameLookup):
            QuicktimeColorNameLookup[1] = "2-color (monochrome)"
            QuicktimeColorNameLookup[2] = "4-color"
            QuicktimeColorNameLookup[4] = "16-color"
            QuicktimeColorNameLookup[8] = "256-color"
            QuicktimeColorNameLookup[16] = "thousands (16-bit color)"
            QuicktimeColorNameLookup[24] = "millions (24-bit color)"
            QuicktimeColorNameLookup[32] = "millions+ (32-bit color)"
            QuicktimeColorNameLookup[33] = "black & white"
            QuicktimeColorNameLookup[34] = "4-gray"
            QuicktimeColorNameLookup[36] = "16-gray"
            QuicktimeColorNameLookup[40] = "256-gray"
        # end if
        return QuicktimeColorNameLookup[colordepthid] if (php_isset(lambda : QuicktimeColorNameLookup[colordepthid])) else "invalid"
    # end def quicktimecolornamelookup
    #// 
    #// @param int $stik
    #// 
    #// @return string
    #//
    def quicktimestiklookup(self, stik=None):
        
        QuicktimeSTIKLookup = Array()
        if php_empty(lambda : QuicktimeSTIKLookup):
            QuicktimeSTIKLookup[0] = "Movie"
            QuicktimeSTIKLookup[1] = "Normal"
            QuicktimeSTIKLookup[2] = "Audiobook"
            QuicktimeSTIKLookup[5] = "Whacked Bookmark"
            QuicktimeSTIKLookup[6] = "Music Video"
            QuicktimeSTIKLookup[9] = "Short Film"
            QuicktimeSTIKLookup[10] = "TV Show"
            QuicktimeSTIKLookup[11] = "Booklet"
            QuicktimeSTIKLookup[14] = "Ringtone"
            QuicktimeSTIKLookup[21] = "Podcast"
        # end if
        return QuicktimeSTIKLookup[stik] if (php_isset(lambda : QuicktimeSTIKLookup[stik])) else "invalid"
    # end def quicktimestiklookup
    #// 
    #// @param int $audio_profile_id
    #// 
    #// @return string
    #//
    def quicktimeiodsaudioprofilename(self, audio_profile_id=None):
        
        QuicktimeIODSaudioProfileNameLookup = Array()
        if php_empty(lambda : QuicktimeIODSaudioProfileNameLookup):
            QuicktimeIODSaudioProfileNameLookup = Array({0: "ISO Reserved (0x00)", 1: "Main Audio Profile @ Level 1", 2: "Main Audio Profile @ Level 2", 3: "Main Audio Profile @ Level 3", 4: "Main Audio Profile @ Level 4", 5: "Scalable Audio Profile @ Level 1", 6: "Scalable Audio Profile @ Level 2", 7: "Scalable Audio Profile @ Level 3", 8: "Scalable Audio Profile @ Level 4", 9: "Speech Audio Profile @ Level 1", 10: "Speech Audio Profile @ Level 2", 11: "Synthetic Audio Profile @ Level 1", 12: "Synthetic Audio Profile @ Level 2", 13: "Synthetic Audio Profile @ Level 3", 14: "High Quality Audio Profile @ Level 1", 15: "High Quality Audio Profile @ Level 2", 16: "High Quality Audio Profile @ Level 3", 17: "High Quality Audio Profile @ Level 4", 18: "High Quality Audio Profile @ Level 5", 19: "High Quality Audio Profile @ Level 6", 20: "High Quality Audio Profile @ Level 7", 21: "High Quality Audio Profile @ Level 8", 22: "Low Delay Audio Profile @ Level 1", 23: "Low Delay Audio Profile @ Level 2", 24: "Low Delay Audio Profile @ Level 3", 25: "Low Delay Audio Profile @ Level 4", 26: "Low Delay Audio Profile @ Level 5", 27: "Low Delay Audio Profile @ Level 6", 28: "Low Delay Audio Profile @ Level 7", 29: "Low Delay Audio Profile @ Level 8", 30: "Natural Audio Profile @ Level 1", 31: "Natural Audio Profile @ Level 2", 32: "Natural Audio Profile @ Level 3", 33: "Natural Audio Profile @ Level 4", 34: "Mobile Audio Internetworking Profile @ Level 1", 35: "Mobile Audio Internetworking Profile @ Level 2", 36: "Mobile Audio Internetworking Profile @ Level 3", 37: "Mobile Audio Internetworking Profile @ Level 4", 38: "Mobile Audio Internetworking Profile @ Level 5", 39: "Mobile Audio Internetworking Profile @ Level 6", 40: "AAC Profile @ Level 1", 41: "AAC Profile @ Level 2", 42: "AAC Profile @ Level 4", 43: "AAC Profile @ Level 5", 44: "High Efficiency AAC Profile @ Level 2", 45: "High Efficiency AAC Profile @ Level 3", 46: "High Efficiency AAC Profile @ Level 4", 47: "High Efficiency AAC Profile @ Level 5", 254: "Not part of MPEG-4 audio profiles", 255: "No audio capability required"})
        # end if
        return QuicktimeIODSaudioProfileNameLookup[audio_profile_id] if (php_isset(lambda : QuicktimeIODSaudioProfileNameLookup[audio_profile_id])) else "ISO Reserved / User Private"
    # end def quicktimeiodsaudioprofilename
    #// 
    #// @param int $video_profile_id
    #// 
    #// @return string
    #//
    def quicktimeiodsvideoprofilename(self, video_profile_id=None):
        
        QuicktimeIODSvideoProfileNameLookup = Array()
        if php_empty(lambda : QuicktimeIODSvideoProfileNameLookup):
            QuicktimeIODSvideoProfileNameLookup = Array({0: "Reserved (0x00) Profile", 1: "Simple Profile @ Level 1", 2: "Simple Profile @ Level 2", 3: "Simple Profile @ Level 3", 8: "Simple Profile @ Level 0", 16: "Simple Scalable Profile @ Level 0", 17: "Simple Scalable Profile @ Level 1", 18: "Simple Scalable Profile @ Level 2", 21: "AVC/H264 Profile", 33: "Core Profile @ Level 1", 34: "Core Profile @ Level 2", 50: "Main Profile @ Level 2", 51: "Main Profile @ Level 3", 52: "Main Profile @ Level 4", 66: "N-bit Profile @ Level 2", 81: "Scalable Texture Profile @ Level 1", 97: "Simple Face Animation Profile @ Level 1", 98: "Simple Face Animation Profile @ Level 2", 99: "Simple FBA Profile @ Level 1", 100: "Simple FBA Profile @ Level 2", 113: "Basic Animated Texture Profile @ Level 1", 114: "Basic Animated Texture Profile @ Level 2", 129: "Hybrid Profile @ Level 1", 130: "Hybrid Profile @ Level 2", 145: "Advanced Real Time Simple Profile @ Level 1", 146: "Advanced Real Time Simple Profile @ Level 2", 147: "Advanced Real Time Simple Profile @ Level 3", 148: "Advanced Real Time Simple Profile @ Level 4", 161: "Core Scalable Profile @ Level1", 162: "Core Scalable Profile @ Level2", 163: "Core Scalable Profile @ Level3", 177: "Advanced Coding Efficiency Profile @ Level 1", 178: "Advanced Coding Efficiency Profile @ Level 2", 179: "Advanced Coding Efficiency Profile @ Level 3", 180: "Advanced Coding Efficiency Profile @ Level 4", 193: "Advanced Core Profile @ Level 1", 194: "Advanced Core Profile @ Level 2", 209: "Advanced Scalable Texture @ Level1", 210: "Advanced Scalable Texture @ Level2", 225: "Simple Studio Profile @ Level 1", 226: "Simple Studio Profile @ Level 2", 227: "Simple Studio Profile @ Level 3", 228: "Simple Studio Profile @ Level 4", 229: "Core Studio Profile @ Level 1", 230: "Core Studio Profile @ Level 2", 231: "Core Studio Profile @ Level 3", 232: "Core Studio Profile @ Level 4", 240: "Advanced Simple Profile @ Level 0", 241: "Advanced Simple Profile @ Level 1", 242: "Advanced Simple Profile @ Level 2", 243: "Advanced Simple Profile @ Level 3", 244: "Advanced Simple Profile @ Level 4", 245: "Advanced Simple Profile @ Level 5", 247: "Advanced Simple Profile @ Level 3b", 248: "Fine Granularity Scalable Profile @ Level 0", 249: "Fine Granularity Scalable Profile @ Level 1", 250: "Fine Granularity Scalable Profile @ Level 2", 251: "Fine Granularity Scalable Profile @ Level 3", 252: "Fine Granularity Scalable Profile @ Level 4", 253: "Fine Granularity Scalable Profile @ Level 5", 254: "Not part of MPEG-4 Visual profiles", 255: "No visual capability required"})
        # end if
        return QuicktimeIODSvideoProfileNameLookup[video_profile_id] if (php_isset(lambda : QuicktimeIODSvideoProfileNameLookup[video_profile_id])) else "ISO Reserved Profile"
    # end def quicktimeiodsvideoprofilename
    #// 
    #// @param int $rtng
    #// 
    #// @return string
    #//
    def quicktimecontentratinglookup(self, rtng=None):
        
        QuicktimeContentRatingLookup = Array()
        if php_empty(lambda : QuicktimeContentRatingLookup):
            QuicktimeContentRatingLookup[0] = "None"
            QuicktimeContentRatingLookup[2] = "Clean"
            QuicktimeContentRatingLookup[4] = "Explicit"
        # end if
        return QuicktimeContentRatingLookup[rtng] if (php_isset(lambda : QuicktimeContentRatingLookup[rtng])) else "invalid"
    # end def quicktimecontentratinglookup
    #// 
    #// @param int $akid
    #// 
    #// @return string
    #//
    def quicktimestoreaccounttypelookup(self, akid=None):
        
        QuicktimeStoreAccountTypeLookup = Array()
        if php_empty(lambda : QuicktimeStoreAccountTypeLookup):
            QuicktimeStoreAccountTypeLookup[0] = "iTunes"
            QuicktimeStoreAccountTypeLookup[1] = "AOL"
        # end if
        return QuicktimeStoreAccountTypeLookup[akid] if (php_isset(lambda : QuicktimeStoreAccountTypeLookup[akid])) else "invalid"
    # end def quicktimestoreaccounttypelookup
    #// 
    #// @param int $sfid
    #// 
    #// @return string
    #//
    def quicktimestorefrontcodelookup(self, sfid=None):
        
        QuicktimeStoreFrontCodeLookup = Array()
        if php_empty(lambda : QuicktimeStoreFrontCodeLookup):
            QuicktimeStoreFrontCodeLookup[143460] = "Australia"
            QuicktimeStoreFrontCodeLookup[143445] = "Austria"
            QuicktimeStoreFrontCodeLookup[143446] = "Belgium"
            QuicktimeStoreFrontCodeLookup[143455] = "Canada"
            QuicktimeStoreFrontCodeLookup[143458] = "Denmark"
            QuicktimeStoreFrontCodeLookup[143447] = "Finland"
            QuicktimeStoreFrontCodeLookup[143442] = "France"
            QuicktimeStoreFrontCodeLookup[143443] = "Germany"
            QuicktimeStoreFrontCodeLookup[143448] = "Greece"
            QuicktimeStoreFrontCodeLookup[143449] = "Ireland"
            QuicktimeStoreFrontCodeLookup[143450] = "Italy"
            QuicktimeStoreFrontCodeLookup[143462] = "Japan"
            QuicktimeStoreFrontCodeLookup[143451] = "Luxembourg"
            QuicktimeStoreFrontCodeLookup[143452] = "Netherlands"
            QuicktimeStoreFrontCodeLookup[143461] = "New Zealand"
            QuicktimeStoreFrontCodeLookup[143457] = "Norway"
            QuicktimeStoreFrontCodeLookup[143453] = "Portugal"
            QuicktimeStoreFrontCodeLookup[143454] = "Spain"
            QuicktimeStoreFrontCodeLookup[143456] = "Sweden"
            QuicktimeStoreFrontCodeLookup[143459] = "Switzerland"
            QuicktimeStoreFrontCodeLookup[143444] = "United Kingdom"
            QuicktimeStoreFrontCodeLookup[143441] = "United States"
        # end if
        return QuicktimeStoreFrontCodeLookup[sfid] if (php_isset(lambda : QuicktimeStoreFrontCodeLookup[sfid])) else "invalid"
    # end def quicktimestorefrontcodelookup
    #// 
    #// @param string $atom_data
    #// 
    #// @return array
    #//
    def quicktimeparsenikonnctg(self, atom_data=None):
        
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
        NCTGtagName = Array({1: "Make", 2: "Model", 3: "Software", 17: "CreateDate", 18: "DateTimeOriginal", 19: "FrameCount", 22: "FrameRate", 34: "FrameWidth", 35: "FrameHeight", 50: "AudioChannels", 51: "AudioBitsPerSample", 52: "AudioSampleRate", 33554433: "MakerNoteVersion", 33554437: "WhiteBalance", 33554443: "WhiteBalanceFineTune", 33554462: "ColorSpace", 33554467: "PictureControlData", 33554468: "WorldTime", 33554482: "UnknownInfo", 33554563: "LensType", 33554564: "Lens"})
        offset = 0
        data = None
        datalength = php_strlen(atom_data)
        parsed = Array()
        while True:
            
            if not (offset < datalength):
                break
            # end if
            record_type = getid3_lib.bigendian2int(php_substr(atom_data, offset, 4))
            offset += 4
            data_size_type = getid3_lib.bigendian2int(php_substr(atom_data, offset, 2))
            offset += 2
            data_size = getid3_lib.bigendian2int(php_substr(atom_data, offset, 2))
            offset += 2
            for case in Switch(data_size_type):
                if case(1):
                    #// 0x0001 = flag   (size field *= 1-byte)
                    data = getid3_lib.bigendian2int(php_substr(atom_data, offset, data_size * 1))
                    offset += data_size * 1
                    break
                # end if
                if case(2):
                    #// 0x0002 = char   (size field *= 1-byte)
                    data = php_substr(atom_data, offset, data_size * 1)
                    offset += data_size * 1
                    data = php_rtrim(data, " ")
                    break
                # end if
                if case(3):
                    #// 0x0003 = DWORD+ (size field *= 2-byte), values are stored CDAB
                    data = ""
                    i = data_size - 1
                    while i >= 0:
                        
                        data += php_substr(atom_data, offset + i * 2, 2)
                        i -= 1
                    # end while
                    data = getid3_lib.bigendian2int(data)
                    offset += data_size * 2
                    break
                # end if
                if case(4):
                    #// 0x0004 = QWORD+ (size field *= 4-byte), values are stored EFGHABCD
                    data = ""
                    i = data_size - 1
                    while i >= 0:
                        
                        data += php_substr(atom_data, offset + i * 4, 4)
                        i -= 1
                    # end while
                    data = getid3_lib.bigendian2int(data)
                    offset += data_size * 4
                    break
                # end if
                if case(5):
                    #// 0x0005 = float  (size field *= 8-byte), values are stored aaaabbbb where value is aaaa/bbbb; possibly multiple sets of values appended together
                    data = Array()
                    i = 0
                    while i < data_size:
                        
                        numerator = getid3_lib.bigendian2int(php_substr(atom_data, offset + i * 8 + 0, 4))
                        denomninator = getid3_lib.bigendian2int(php_substr(atom_data, offset + i * 8 + 4, 4))
                        if denomninator == 0:
                            data[i] = False
                        else:
                            data[i] = float(numerator) / denomninator
                        # end if
                        i += 1
                    # end while
                    offset += 8 * data_size
                    if php_count(data) == 1:
                        data = data[0]
                    # end if
                    break
                # end if
                if case(7):
                    #// 0x0007 = bytes  (size field *= 1-byte), values are stored as ??????
                    data = php_substr(atom_data, offset, data_size * 1)
                    offset += data_size * 1
                    break
                # end if
                if case(8):
                    #// 0x0008 = ?????  (size field *= 2-byte), values are stored as ??????
                    data = php_substr(atom_data, offset, data_size * 2)
                    offset += data_size * 2
                    break
                # end if
                if case():
                    php_print("QuicktimeParseNikonNCTG()::unknown $data_size_type: " + data_size_type + "<br>")
                    break
                # end if
            # end for
            for case in Switch(record_type):
                if case(17):
                    pass
                # end if
                if case(18):
                    #// DateTimeOriginal
                    data = strtotime(data)
                    break
                # end if
                if case(33554462):
                    #// ColorSpace
                    for case in Switch(data):
                        if case(1):
                            data = "sRGB"
                            break
                        # end if
                        if case(2):
                            data = "Adobe RGB"
                            break
                        # end if
                    # end for
                    break
                # end if
                if case(33554467):
                    #// PictureControlData
                    PictureControlAdjust = Array({0: "default", 1: "quick", 2: "full"})
                    FilterEffect = Array({128: "off", 129: "yellow", 130: "orange", 131: "red", 132: "green", 255: "n/a"})
                    ToningEffect = Array({128: "b&w", 129: "sepia", 130: "cyanotype", 131: "red", 132: "yellow", 133: "green", 134: "blue-green", 135: "blue", 136: "purple-blue", 137: "red-purple", 255: "n/a"})
                    data = Array({"PictureControlVersion": php_substr(data, 0, 4), "PictureControlName": php_rtrim(php_substr(data, 4, 20), " "), "PictureControlBase": php_rtrim(php_substr(data, 24, 20), " "), "PictureControlAdjust": PictureControlAdjust[php_ord(php_substr(data, 48, 1))], "PictureControlQuickAdjust": php_ord(php_substr(data, 49, 1)), "Sharpness": php_ord(php_substr(data, 50, 1)), "Contrast": php_ord(php_substr(data, 51, 1)), "Brightness": php_ord(php_substr(data, 52, 1)), "Saturation": php_ord(php_substr(data, 53, 1)), "HueAdjustment": php_ord(php_substr(data, 54, 1)), "FilterEffect": FilterEffect[php_ord(php_substr(data, 55, 1))], "ToningEffect": ToningEffect[php_ord(php_substr(data, 56, 1))], "ToningSaturation": php_ord(php_substr(data, 57, 1))})
                    break
                # end if
                if case(33554468):
                    #// WorldTime
                    #// http://www.sno.phy.queensu.ca/~phil/exiftool/TagNames/Nikon.html#WorldTime
                    #// timezone is stored as offset from GMT in minutes
                    timezone = getid3_lib.bigendian2int(php_substr(data, 0, 2))
                    if timezone & 32768:
                        timezone = 0 - 65536 - timezone
                    # end if
                    timezone /= 60
                    dst = bool(getid3_lib.bigendian2int(php_substr(data, 2, 1)))
                    for case in Switch(getid3_lib.bigendian2int(php_substr(data, 3, 1))):
                        if case(2):
                            datedisplayformat = "D/M/Y"
                            break
                        # end if
                        if case(1):
                            datedisplayformat = "M/D/Y"
                            break
                        # end if
                        if case(0):
                            pass
                        # end if
                        if case():
                            datedisplayformat = "Y/M/D"
                            break
                        # end if
                    # end for
                    data = Array({"timezone": floatval(timezone), "dst": dst, "display": datedisplayformat})
                    break
                # end if
                if case(33554563):
                    #// LensType
                    data = Array({"mf": bool(data & 1), "d": bool(data & 2), "g": bool(data & 4), "vr": bool(data & 8)})
                    break
                # end if
            # end for
            tag_name = NCTGtagName[record_type] if (php_isset(lambda : NCTGtagName[record_type])) else "0x" + php_str_pad(dechex(record_type), 8, "0", STR_PAD_LEFT)
            parsed[tag_name] = data
        # end while
        return parsed
    # end def quicktimeparsenikonnctg
    #// 
    #// @param string $keyname
    #// @param string|array $data
    #// @param string $boxname
    #// 
    #// @return bool
    #//
    def copytoappropriatecommentssection(self, keyname=None, data=None, boxname=""):
        
        handyatomtranslatorarray = Array()
        if php_empty(lambda : handyatomtranslatorarray):
            #// http://www.geocities.com/xhelmboyx/quicktime/formats/qtm-layout.txt
            #// http://www.geocities.com/xhelmboyx/quicktime/formats/mp4-layout.txt
            #// http://atomicparsley.sourceforge.net/mpeg-4files.html
            #// https://code.google.com/p/mp4v2/wiki/iTunesMetadata
            handyatomtranslatorarray["©" + "alb"] = "album"
            #// iTunes 4.0
            handyatomtranslatorarray["©" + "ART"] = "artist"
            handyatomtranslatorarray["©" + "art"] = "artist"
            #// iTunes 4.0
            handyatomtranslatorarray["©" + "aut"] = "author"
            handyatomtranslatorarray["©" + "cmt"] = "comment"
            #// iTunes 4.0
            handyatomtranslatorarray["©" + "com"] = "comment"
            handyatomtranslatorarray["©" + "cpy"] = "copyright"
            handyatomtranslatorarray["©" + "day"] = "creation_date"
            #// iTunes 4.0
            handyatomtranslatorarray["©" + "dir"] = "director"
            handyatomtranslatorarray["©" + "ed1"] = "edit1"
            handyatomtranslatorarray["©" + "ed2"] = "edit2"
            handyatomtranslatorarray["©" + "ed3"] = "edit3"
            handyatomtranslatorarray["©" + "ed4"] = "edit4"
            handyatomtranslatorarray["©" + "ed5"] = "edit5"
            handyatomtranslatorarray["©" + "ed6"] = "edit6"
            handyatomtranslatorarray["©" + "ed7"] = "edit7"
            handyatomtranslatorarray["©" + "ed8"] = "edit8"
            handyatomtranslatorarray["©" + "ed9"] = "edit9"
            handyatomtranslatorarray["©" + "enc"] = "encoded_by"
            handyatomtranslatorarray["©" + "fmt"] = "format"
            handyatomtranslatorarray["©" + "gen"] = "genre"
            #// iTunes 4.0
            handyatomtranslatorarray["©" + "grp"] = "grouping"
            #// iTunes 4.2
            handyatomtranslatorarray["©" + "hst"] = "host_computer"
            handyatomtranslatorarray["©" + "inf"] = "information"
            handyatomtranslatorarray["©" + "lyr"] = "lyrics"
            #// iTunes 5.0
            handyatomtranslatorarray["©" + "mak"] = "make"
            handyatomtranslatorarray["©" + "mod"] = "model"
            handyatomtranslatorarray["©" + "nam"] = "title"
            #// iTunes 4.0
            handyatomtranslatorarray["©" + "ope"] = "composer"
            handyatomtranslatorarray["©" + "prd"] = "producer"
            handyatomtranslatorarray["©" + "PRD"] = "product"
            handyatomtranslatorarray["©" + "prf"] = "performers"
            handyatomtranslatorarray["©" + "req"] = "system_requirements"
            handyatomtranslatorarray["©" + "src"] = "source_credit"
            handyatomtranslatorarray["©" + "swr"] = "software"
            handyatomtranslatorarray["©" + "too"] = "encoding_tool"
            #// iTunes 4.0
            handyatomtranslatorarray["©" + "trk"] = "track_number"
            handyatomtranslatorarray["©" + "url"] = "url"
            handyatomtranslatorarray["©" + "wrn"] = "warning"
            handyatomtranslatorarray["©" + "wrt"] = "composer"
            handyatomtranslatorarray["aART"] = "album_artist"
            handyatomtranslatorarray["apID"] = "purchase_account"
            handyatomtranslatorarray["catg"] = "category"
            #// iTunes 4.9
            handyatomtranslatorarray["covr"] = "picture"
            #// iTunes 4.0
            handyatomtranslatorarray["cpil"] = "compilation"
            #// iTunes 4.0
            handyatomtranslatorarray["cprt"] = "copyright"
            #// iTunes 4.0?
            handyatomtranslatorarray["desc"] = "description"
            #// iTunes 5.0
            handyatomtranslatorarray["disk"] = "disc_number"
            #// iTunes 4.0
            handyatomtranslatorarray["egid"] = "episode_guid"
            #// iTunes 4.9
            handyatomtranslatorarray["gnre"] = "genre"
            #// iTunes 4.0
            handyatomtranslatorarray["hdvd"] = "hd_video"
            #// iTunes 4.0
            handyatomtranslatorarray["ldes"] = "description_long"
            #//
            handyatomtranslatorarray["keyw"] = "keyword"
            #// iTunes 4.9
            handyatomtranslatorarray["pcst"] = "podcast"
            #// iTunes 4.9
            handyatomtranslatorarray["pgap"] = "gapless_playback"
            #// iTunes 7.0
            handyatomtranslatorarray["purd"] = "purchase_date"
            #// iTunes 6.0.2
            handyatomtranslatorarray["purl"] = "podcast_url"
            #// iTunes 4.9
            handyatomtranslatorarray["rtng"] = "rating"
            #// iTunes 4.0
            handyatomtranslatorarray["soaa"] = "sort_album_artist"
            #//
            handyatomtranslatorarray["soal"] = "sort_album"
            #//
            handyatomtranslatorarray["soar"] = "sort_artist"
            #//
            handyatomtranslatorarray["soco"] = "sort_composer"
            #//
            handyatomtranslatorarray["sonm"] = "sort_title"
            #//
            handyatomtranslatorarray["sosn"] = "sort_show"
            #//
            handyatomtranslatorarray["stik"] = "stik"
            #// iTunes 4.9
            handyatomtranslatorarray["tmpo"] = "bpm"
            #// iTunes 4.0
            handyatomtranslatorarray["trkn"] = "track_number"
            #// iTunes 4.0
            handyatomtranslatorarray["tven"] = "tv_episode_id"
            #//
            handyatomtranslatorarray["tves"] = "tv_episode"
            #// iTunes 6.0
            handyatomtranslatorarray["tvnn"] = "tv_network_name"
            #// iTunes 6.0
            handyatomtranslatorarray["tvsh"] = "tv_show_name"
            #// iTunes 6.0
            handyatomtranslatorarray["tvsn"] = "tv_season"
            pass
        # end if
        info = self.getid3.info
        comment_key = ""
        if boxname and boxname != keyname:
            comment_key = handyatomtranslatorarray[boxname] if (php_isset(lambda : handyatomtranslatorarray[boxname])) else boxname
        elif (php_isset(lambda : handyatomtranslatorarray[keyname])):
            comment_key = handyatomtranslatorarray[keyname]
        # end if
        if comment_key:
            if comment_key == "picture":
                if (not php_is_array(data)):
                    image_mime = ""
                    if php_preg_match("#^\\x89\\x50\\x4E\\x47\\x0D\\x0A\\x1A\\x0A#", data):
                        image_mime = "image/png"
                    elif php_preg_match("#^\\xFF\\xD8\\xFF#", data):
                        image_mime = "image/jpeg"
                    elif php_preg_match("#^GIF#", data):
                        image_mime = "image/gif"
                    elif php_preg_match("#^BM#", data):
                        image_mime = "image/bmp"
                    # end if
                    data = Array({"data": data, "image_mime": image_mime})
                # end if
            # end if
            gooddata = Array(data)
            if comment_key == "genre":
                #// some other taggers separate multiple genres with semicolon, e.g. "Heavy Metal;Thrash Metal;Metal"
                gooddata = php_explode(";", data)
            # end if
            for data in gooddata:
                info["quicktime"]["comments"][comment_key][-1] = data
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
    def locistring(self, lstring=None, count=None):
        
        #// Loci strings are UTF-8 or UTF-16 and null (x00/x0000) terminated. UTF-16 has a BOM
        #// Also need to return the number of bytes the string occupied so additional fields can be extracted
        len = php_strlen(lstring)
        if len == 0:
            count = 0
            return ""
        # end if
        if lstring[0] == " ":
            count = 1
            return ""
        # end if
        #// check for BOM
        if len > 2 and lstring[0] == "þ" and lstring[1] == "ÿ" or lstring[0] == "ÿ" and lstring[1] == "þ":
            #// UTF-16
            if php_preg_match("/(.*)\\x00/", lstring, lmatches):
                count = php_strlen(lmatches[1]) * 2 + 2
                #// account for 2 byte characters and trailing \x0000
                return getid3_lib.iconv_fallback_utf16_utf8(lmatches[1])
            else:
                return ""
            # end if
        # end if
        #// UTF-8
        if php_preg_match("/(.*)\\x00/", lstring, lmatches):
            count = php_strlen(lmatches[1]) + 1
            #// account for trailing \x00
            return lmatches[1]
        # end if
        return ""
    # end def locistring
    #// 
    #// @param string $nullterminatedstring
    #// 
    #// @return string
    #//
    def nonullstring(self, nullterminatedstring=None):
        
        #// remove the single null terminator on null terminated strings
        if php_substr(nullterminatedstring, php_strlen(nullterminatedstring) - 1, 1) == " ":
            return php_substr(nullterminatedstring, 0, php_strlen(nullterminatedstring) - 1)
        # end if
        return nullterminatedstring
    # end def nonullstring
    #// 
    #// @param string $pascalstring
    #// 
    #// @return string
    #//
    def pascal2string(self, pascalstring=None):
        
        #// Pascal strings have 1 unsigned byte at the beginning saying how many chars (1-255) are in the string
        return php_substr(pascalstring, 1)
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
    def search_tag_by_key(self, info=None, tag=None, history=None, result=None):
        
        for key,value in info:
            key_history = history + "/" + key
            if key == tag:
                result[-1] = Array(key_history, info)
            else:
                if php_is_array(value):
                    self.search_tag_by_key(value, tag, key_history, result)
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
    def search_tag_by_pair(self, info=None, k=None, v=None, history=None, result=None):
        
        for key,value in info:
            key_history = history + "/" + key
            if key == k and value == v:
                result[-1] = Array(key_history, info)
            else:
                if php_is_array(value):
                    self.search_tag_by_pair(value, k, v, key_history, result)
                # end if
            # end if
        # end for
    # end def search_tag_by_pair
    #// 
    #// @param array $info
    #// 
    #// @return array
    #//
    def quicktime_time_to_sample_table(self, info=None):
        
        res = Array()
        self.search_tag_by_pair(info["quicktime"]["moov"], "name", "stbl", "quicktime/moov", res)
        for value in res:
            stbl_res = Array()
            self.search_tag_by_pair(value[1], "data_format", "text", value[0], stbl_res)
            if php_count(stbl_res) > 0:
                stts_res = Array()
                self.search_tag_by_key(value[1], "time_to_sample_table", value[0], stts_res)
                if php_count(stts_res) > 0:
                    return stts_res[0][1]["time_to_sample_table"]
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
    def quicktime_bookmark_time_scale(self, info=None):
        
        time_scale = ""
        ts_prefix_len = 0
        res = Array()
        self.search_tag_by_pair(info["quicktime"]["moov"], "name", "stbl", "quicktime/moov", res)
        for value in res:
            stbl_res = Array()
            self.search_tag_by_pair(value[1], "data_format", "text", value[0], stbl_res)
            if php_count(stbl_res) > 0:
                ts_res = Array()
                self.search_tag_by_key(info["quicktime"]["moov"], "time_scale", "quicktime/moov", ts_res)
                for sub_value in ts_res:
                    prefix = php_substr(sub_value[0], 0, -12)
                    if php_substr(stbl_res[0][0], 0, php_strlen(prefix)) == prefix and ts_prefix_len < php_strlen(prefix):
                        time_scale = sub_value[1]["time_scale"]
                        ts_prefix_len = php_strlen(prefix)
                    # end if
                # end for
            # end if
        # end for
        return time_scale
    # end def quicktime_bookmark_time_scale
    pass
# end class getid3_quicktime
