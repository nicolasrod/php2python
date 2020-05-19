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
#// module.tag.lyrics3.php
#// module for analyzing Lyrics3 tags
#// dependencies: module.tag.apetag.php (optional)
#// 
#//
class getid3_lyrics3(getid3_handler):
    #// 
    #// @return bool
    #//
    def analyze(self):
        
        
        info_ = self.getid3.info
        #// http://www.volweb.cz/str/tags.htm
        if (not getid3_lib.intvaluesupported(info_["filesize"])):
            self.warning("Unable to check for Lyrics3 because file is larger than " + round(PHP_INT_MAX / 1073741824) + "GB")
            return False
        # end if
        self.fseek(0 - 128 - 9 - 6, SEEK_END)
        #// end - ID3v1 - "LYRICSEND" - [Lyrics3size]
        lyrics3_id3v1_ = self.fread(128 + 9 + 6)
        lyrics3lsz_ = php_substr(lyrics3_id3v1_, 0, 6)
        #// Lyrics3size
        lyrics3end_ = php_substr(lyrics3_id3v1_, 6, 9)
        #// LYRICSEND or LYRICS200
        id3v1tag_ = php_substr(lyrics3_id3v1_, 15, 128)
        #// ID3v1
        if lyrics3end_ == "LYRICSEND":
            #// Lyrics3v1, ID3v1, no APE
            lyrics3size_ = 5100
            lyrics3offset_ = info_["filesize"] - 128 - lyrics3size_
            lyrics3version_ = 1
        elif lyrics3end_ == "LYRICS200":
            #// Lyrics3v2, ID3v1, no APE
            #// LSZ = lyrics + 'LYRICSBEGIN'; add 6-byte size field; add 'LYRICS200'
            lyrics3size_ = lyrics3lsz_ + 6 + php_strlen("LYRICS200")
            lyrics3offset_ = info_["filesize"] - 128 - lyrics3size_
            lyrics3version_ = 2
        elif php_substr(php_strrev(lyrics3_id3v1_), 0, 9) == php_strrev("LYRICSEND"):
            #// Lyrics3v1, no ID3v1, no APE
            lyrics3size_ = 5100
            lyrics3offset_ = info_["filesize"] - lyrics3size_
            lyrics3version_ = 1
            lyrics3offset_ = info_["filesize"] - lyrics3size_
        elif php_substr(php_strrev(lyrics3_id3v1_), 0, 9) == php_strrev("LYRICS200"):
            #// Lyrics3v2, no ID3v1, no APE
            lyrics3size_ = php_int(php_strrev(php_substr(php_strrev(lyrics3_id3v1_), 9, 6))) + 6 + php_strlen("LYRICS200")
            #// LSZ = lyrics + 'LYRICSBEGIN'; add 6-byte size field; add 'LYRICS200'
            lyrics3offset_ = info_["filesize"] - lyrics3size_
            lyrics3version_ = 2
        else:
            if (php_isset(lambda : info_["ape"]["tag_offset_start"])) and info_["ape"]["tag_offset_start"] > 15:
                self.fseek(info_["ape"]["tag_offset_start"] - 15)
                lyrics3lsz_ = self.fread(6)
                lyrics3end_ = self.fread(9)
                if lyrics3end_ == "LYRICSEND":
                    #// Lyrics3v1, APE, maybe ID3v1
                    lyrics3size_ = 5100
                    lyrics3offset_ = info_["ape"]["tag_offset_start"] - lyrics3size_
                    info_["avdataend"] = lyrics3offset_
                    lyrics3version_ = 1
                    self.warning("APE tag located after Lyrics3, will probably break Lyrics3 compatability")
                elif lyrics3end_ == "LYRICS200":
                    #// Lyrics3v2, APE, maybe ID3v1
                    lyrics3size_ = lyrics3lsz_ + 6 + php_strlen("LYRICS200")
                    #// LSZ = lyrics + 'LYRICSBEGIN'; add 6-byte size field; add 'LYRICS200'
                    lyrics3offset_ = info_["ape"]["tag_offset_start"] - lyrics3size_
                    lyrics3version_ = 2
                    self.warning("APE tag located after Lyrics3, will probably break Lyrics3 compatability")
                # end if
            # end if
        # end if
        if (php_isset(lambda : lyrics3offset_)) and (php_isset(lambda : lyrics3version_)) and (php_isset(lambda : lyrics3size_)):
            info_["avdataend"] = lyrics3offset_
            self.getlyrics3data(lyrics3offset_, lyrics3version_, lyrics3size_)
            if (not (php_isset(lambda : info_["ape"]))):
                if (php_isset(lambda : info_["lyrics3"]["tag_offset_start"])):
                    GETID3_ERRORARRAY_ = info_["warning"]
                    getid3_lib.includedependency(GETID3_INCLUDEPATH + "module.tag.apetag.php", __FILE__, True)
                    getid3_temp_ = php_new_class("getID3", lambda : getID3())
                    getid3_temp_.openfile(self.getid3.filename)
                    getid3_apetag_ = php_new_class("getid3_apetag", lambda : getid3_apetag(getid3_temp_))
                    getid3_apetag_.overrideendoffset = info_["lyrics3"]["tag_offset_start"]
                    getid3_apetag_.analyze()
                    if (not php_empty(lambda : getid3_temp_.info["ape"])):
                        info_["ape"] = getid3_temp_.info["ape"]
                    # end if
                    if (not php_empty(lambda : getid3_temp_.info["replay_gain"])):
                        info_["replay_gain"] = getid3_temp_.info["replay_gain"]
                    # end if
                    getid3_temp_ = None
                    getid3_apetag_ = None
                else:
                    self.warning("Lyrics3 and APE tags appear to have become entangled (most likely due to updating the APE tags with a non-Lyrics3-aware tagger)")
                # end if
            # end if
        # end if
        return True
    # end def analyze
    #// 
    #// @param int $endoffset
    #// @param int $version
    #// @param int $length
    #// 
    #// @return bool
    #//
    def getlyrics3data(self, endoffset_=None, version_=None, length_=None):
        
        
        #// http://www.volweb.cz/str/tags.htm
        info_ = self.getid3.info
        if (not getid3_lib.intvaluesupported(endoffset_)):
            self.warning("Unable to check for Lyrics3 because file is larger than " + round(PHP_INT_MAX / 1073741824) + "GB")
            return False
        # end if
        self.fseek(endoffset_)
        if length_ <= 0:
            return False
        # end if
        rawdata_ = self.fread(length_)
        ParsedLyrics3_ = Array()
        ParsedLyrics3_["raw"]["lyrics3version"] = version_
        ParsedLyrics3_["raw"]["lyrics3tagsize"] = length_
        ParsedLyrics3_["tag_offset_start"] = endoffset_
        ParsedLyrics3_["tag_offset_end"] = endoffset_ + length_ - 1
        if php_substr(rawdata_, 0, 11) != "LYRICSBEGIN":
            if php_strpos(rawdata_, "LYRICSBEGIN") != False:
                self.warning("\"LYRICSBEGIN\" expected at " + endoffset_ + " but actually found at " + endoffset_ + php_strpos(rawdata_, "LYRICSBEGIN") + " - this is invalid for Lyrics3 v" + version_)
                info_["avdataend"] = endoffset_ + php_strpos(rawdata_, "LYRICSBEGIN")
                rawdata_ = php_substr(rawdata_, php_strpos(rawdata_, "LYRICSBEGIN"))
                length_ = php_strlen(rawdata_)
                ParsedLyrics3_["tag_offset_start"] = info_["avdataend"]
                ParsedLyrics3_["raw"]["lyrics3tagsize"] = length_
            else:
                self.error("\"LYRICSBEGIN\" expected at " + endoffset_ + " but found \"" + php_substr(rawdata_, 0, 11) + "\" instead")
                return False
            # end if
        # end if
        for case in Switch(version_):
            if case(1):
                if php_substr(rawdata_, php_strlen(rawdata_) - 9, 9) == "LYRICSEND":
                    ParsedLyrics3_["raw"]["LYR"] = php_trim(php_substr(rawdata_, 11, php_strlen(rawdata_) - 11 - 9))
                    self.lyrics3lyricstimestampparse(ParsedLyrics3_)
                else:
                    self.error("\"LYRICSEND\" expected at " + self.ftell() - 11 + length_ - 9 + " but found \"" + php_substr(rawdata_, php_strlen(rawdata_) - 9, 9) + "\" instead")
                    return False
                # end if
                break
            # end if
            if case(2):
                if php_substr(rawdata_, php_strlen(rawdata_) - 9, 9) == "LYRICS200":
                    ParsedLyrics3_["raw"]["unparsed"] = php_substr(rawdata_, 11, php_strlen(rawdata_) - 11 - 9 - 6)
                    #// LYRICSBEGIN + LYRICS200 + LSZ
                    rawdata_ = ParsedLyrics3_["raw"]["unparsed"]
                    while True:
                        
                        if not (php_strlen(rawdata_) > 0):
                            break
                        # end if
                        fieldname_ = php_substr(rawdata_, 0, 3)
                        fieldsize_ = php_int(php_substr(rawdata_, 3, 5))
                        ParsedLyrics3_["raw"][fieldname_] = php_substr(rawdata_, 8, fieldsize_)
                        rawdata_ = php_substr(rawdata_, 3 + 5 + fieldsize_)
                    # end while
                    if (php_isset(lambda : ParsedLyrics3_["raw"]["IND"])):
                        i_ = 0
                        flagnames_ = Array("lyrics", "timestamps", "inhibitrandom")
                        for flagname_ in flagnames_:
                            i_ += 1
                            if php_strlen(ParsedLyrics3_["raw"]["IND"]) > i_:
                                ParsedLyrics3_["flags"][flagname_] = self.intstring2bool(php_substr(ParsedLyrics3_["raw"]["IND"], i_, 1 - 1))
                            # end if
                            i_ += 1
                        # end for
                    # end if
                    fieldnametranslation_ = Array({"ETT": "title", "EAR": "artist", "EAL": "album", "INF": "comment", "AUT": "author"})
                    for key_,value_ in fieldnametranslation_.items():
                        if (php_isset(lambda : ParsedLyrics3_["raw"][key_])):
                            ParsedLyrics3_["comments"][value_][-1] = php_trim(ParsedLyrics3_["raw"][key_])
                        # end if
                    # end for
                    if (php_isset(lambda : ParsedLyrics3_["raw"]["IMG"])):
                        imagestrings_ = php_explode("\r\n", ParsedLyrics3_["raw"]["IMG"])
                        for key_,imagestring_ in imagestrings_.items():
                            if php_strpos(imagestring_, "||") != False:
                                imagearray_ = php_explode("||", imagestring_)
                                ParsedLyrics3_["images"][key_]["filename"] = imagearray_[0] if (php_isset(lambda : imagearray_[0])) else ""
                                ParsedLyrics3_["images"][key_]["description"] = imagearray_[1] if (php_isset(lambda : imagearray_[1])) else ""
                                ParsedLyrics3_["images"][key_]["timestamp"] = self.lyrics3timestamp2seconds(imagearray_[2] if (php_isset(lambda : imagearray_[2])) else "")
                            # end if
                        # end for
                    # end if
                    if (php_isset(lambda : ParsedLyrics3_["raw"]["LYR"])):
                        self.lyrics3lyricstimestampparse(ParsedLyrics3_)
                    # end if
                else:
                    self.error("\"LYRICS200\" expected at " + self.ftell() - 11 + length_ - 9 + " but found \"" + php_substr(rawdata_, php_strlen(rawdata_) - 9, 9) + "\" instead")
                    return False
                # end if
                break
            # end if
            if case():
                self.error("Cannot process Lyrics3 version " + version_ + " (only v1 and v2)")
                return False
                break
            # end if
        # end for
        if (php_isset(lambda : info_["id3v1"]["tag_offset_start"])) and info_["id3v1"]["tag_offset_start"] <= ParsedLyrics3_["tag_offset_end"]:
            self.warning("ID3v1 tag information ignored since it appears to be a false synch in Lyrics3 tag data")
            info_["id3v1"] = None
            for key_,value_ in info_["warning"].items():
                if value_ == "Some ID3v1 fields do not use NULL characters for padding":
                    info_["warning"][key_] = None
                    sort(info_["warning"])
                    break
                # end if
            # end for
        # end if
        info_["lyrics3"] = ParsedLyrics3_
        return True
    # end def getlyrics3data
    #// 
    #// @param string $rawtimestamp
    #// 
    #// @return int|false
    #//
    def lyrics3timestamp2seconds(self, rawtimestamp_=None):
        
        
        if php_preg_match("#^\\[([0-9]{2}):([0-9]{2})\\]$#", rawtimestamp_, regs_):
            return php_int(regs_[1] * 60 + regs_[2])
        # end if
        return False
    # end def lyrics3timestamp2seconds
    #// 
    #// @param array $Lyrics3data
    #// 
    #// @return bool
    #//
    def lyrics3lyricstimestampparse(self, Lyrics3data_=None):
        
        
        lyricsarray_ = php_explode("\r\n", Lyrics3data_["raw"]["LYR"])
        notimestamplyricsarray_ = Array()
        for key_,lyricline_ in lyricsarray_.items():
            regs_ = Array()
            thislinetimestamps_ = None
            while True:
                
                if not (php_preg_match("#^(\\[[0-9]{2}:[0-9]{2}\\])#", lyricline_, regs_)):
                    break
                # end if
                thislinetimestamps_[-1] = self.lyrics3timestamp2seconds(regs_[0])
                lyricline_ = php_str_replace(regs_[0], "", lyricline_)
            # end while
            notimestamplyricsarray_[key_] = lyricline_
            if (php_isset(lambda : thislinetimestamps_)) and php_is_array(thislinetimestamps_):
                sort(thislinetimestamps_)
                for timestampkey_,timestamp_ in thislinetimestamps_.items():
                    if (php_isset(lambda : Lyrics3data_["synchedlyrics"][timestamp_])):
                        #// timestamps only have a 1-second resolution, it's possible that multiple lines
                        #// could have the same timestamp, if so, append
                        Lyrics3data_["synchedlyrics"][timestamp_] += "\r\n" + lyricline_
                    else:
                        Lyrics3data_["synchedlyrics"][timestamp_] = lyricline_
                    # end if
                # end for
            # end if
        # end for
        Lyrics3data_["unsynchedlyrics"] = php_implode("\r\n", notimestamplyricsarray_)
        if (php_isset(lambda : Lyrics3data_["synchedlyrics"])) and php_is_array(Lyrics3data_["synchedlyrics"]):
            php_ksort(Lyrics3data_["synchedlyrics"])
        # end if
        return True
    # end def lyrics3lyricstimestampparse
    #// 
    #// @param string $char
    #// 
    #// @return bool|null
    #//
    def intstring2bool(self, char_=None):
        
        
        if char_ == "1":
            return True
        elif char_ == "0":
            return False
        # end if
        return None
    # end def intstring2bool
# end class getid3_lyrics3
