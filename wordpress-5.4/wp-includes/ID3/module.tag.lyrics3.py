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
        
        info = self.getid3.info
        #// http://www.volweb.cz/str/tags.htm
        if (not getid3_lib.intvaluesupported(info["filesize"])):
            self.warning("Unable to check for Lyrics3 because file is larger than " + round(PHP_INT_MAX / 1073741824) + "GB")
            return False
        # end if
        self.fseek(0 - 128 - 9 - 6, SEEK_END)
        #// end - ID3v1 - "LYRICSEND" - [Lyrics3size]
        lyrics3_id3v1 = self.fread(128 + 9 + 6)
        lyrics3lsz = php_substr(lyrics3_id3v1, 0, 6)
        #// Lyrics3size
        lyrics3end = php_substr(lyrics3_id3v1, 6, 9)
        #// LYRICSEND or LYRICS200
        id3v1tag = php_substr(lyrics3_id3v1, 15, 128)
        #// ID3v1
        if lyrics3end == "LYRICSEND":
            #// Lyrics3v1, ID3v1, no APE
            lyrics3size = 5100
            lyrics3offset = info["filesize"] - 128 - lyrics3size
            lyrics3version = 1
        elif lyrics3end == "LYRICS200":
            #// Lyrics3v2, ID3v1, no APE
            #// LSZ = lyrics + 'LYRICSBEGIN'; add 6-byte size field; add 'LYRICS200'
            lyrics3size = lyrics3lsz + 6 + php_strlen("LYRICS200")
            lyrics3offset = info["filesize"] - 128 - lyrics3size
            lyrics3version = 2
        elif php_substr(php_strrev(lyrics3_id3v1), 0, 9) == php_strrev("LYRICSEND"):
            #// Lyrics3v1, no ID3v1, no APE
            lyrics3size = 5100
            lyrics3offset = info["filesize"] - lyrics3size
            lyrics3version = 1
            lyrics3offset = info["filesize"] - lyrics3size
        elif php_substr(php_strrev(lyrics3_id3v1), 0, 9) == php_strrev("LYRICS200"):
            #// Lyrics3v2, no ID3v1, no APE
            lyrics3size = php_int(php_strrev(php_substr(php_strrev(lyrics3_id3v1), 9, 6))) + 6 + php_strlen("LYRICS200")
            #// LSZ = lyrics + 'LYRICSBEGIN'; add 6-byte size field; add 'LYRICS200'
            lyrics3offset = info["filesize"] - lyrics3size
            lyrics3version = 2
        else:
            if (php_isset(lambda : info["ape"]["tag_offset_start"])) and info["ape"]["tag_offset_start"] > 15:
                self.fseek(info["ape"]["tag_offset_start"] - 15)
                lyrics3lsz = self.fread(6)
                lyrics3end = self.fread(9)
                if lyrics3end == "LYRICSEND":
                    #// Lyrics3v1, APE, maybe ID3v1
                    lyrics3size = 5100
                    lyrics3offset = info["ape"]["tag_offset_start"] - lyrics3size
                    info["avdataend"] = lyrics3offset
                    lyrics3version = 1
                    self.warning("APE tag located after Lyrics3, will probably break Lyrics3 compatability")
                elif lyrics3end == "LYRICS200":
                    #// Lyrics3v2, APE, maybe ID3v1
                    lyrics3size = lyrics3lsz + 6 + php_strlen("LYRICS200")
                    #// LSZ = lyrics + 'LYRICSBEGIN'; add 6-byte size field; add 'LYRICS200'
                    lyrics3offset = info["ape"]["tag_offset_start"] - lyrics3size
                    lyrics3version = 2
                    self.warning("APE tag located after Lyrics3, will probably break Lyrics3 compatability")
                # end if
            # end if
        # end if
        if (php_isset(lambda : lyrics3offset)) and (php_isset(lambda : lyrics3version)) and (php_isset(lambda : lyrics3size)):
            info["avdataend"] = lyrics3offset
            self.getlyrics3data(lyrics3offset, lyrics3version, lyrics3size)
            if (not (php_isset(lambda : info["ape"]))):
                if (php_isset(lambda : info["lyrics3"]["tag_offset_start"])):
                    GETID3_ERRORARRAY = info["warning"]
                    getid3_lib.includedependency(GETID3_INCLUDEPATH + "module.tag.apetag.php", __FILE__, True)
                    getid3_temp = php_new_class("getID3", lambda : getID3())
                    getid3_temp.openfile(self.getid3.filename)
                    getid3_apetag = php_new_class("getid3_apetag", lambda : getid3_apetag(getid3_temp))
                    getid3_apetag.overrideendoffset = info["lyrics3"]["tag_offset_start"]
                    getid3_apetag.analyze()
                    if (not php_empty(lambda : getid3_temp.info["ape"])):
                        info["ape"] = getid3_temp.info["ape"]
                    # end if
                    if (not php_empty(lambda : getid3_temp.info["replay_gain"])):
                        info["replay_gain"] = getid3_temp.info["replay_gain"]
                    # end if
                    getid3_temp = None
                    getid3_apetag = None
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
    def getlyrics3data(self, endoffset=None, version=None, length=None):
        
        #// http://www.volweb.cz/str/tags.htm
        info = self.getid3.info
        if (not getid3_lib.intvaluesupported(endoffset)):
            self.warning("Unable to check for Lyrics3 because file is larger than " + round(PHP_INT_MAX / 1073741824) + "GB")
            return False
        # end if
        self.fseek(endoffset)
        if length <= 0:
            return False
        # end if
        rawdata = self.fread(length)
        ParsedLyrics3 = Array()
        ParsedLyrics3["raw"]["lyrics3version"] = version
        ParsedLyrics3["raw"]["lyrics3tagsize"] = length
        ParsedLyrics3["tag_offset_start"] = endoffset
        ParsedLyrics3["tag_offset_end"] = endoffset + length - 1
        if php_substr(rawdata, 0, 11) != "LYRICSBEGIN":
            if php_strpos(rawdata, "LYRICSBEGIN") != False:
                self.warning("\"LYRICSBEGIN\" expected at " + endoffset + " but actually found at " + endoffset + php_strpos(rawdata, "LYRICSBEGIN") + " - this is invalid for Lyrics3 v" + version)
                info["avdataend"] = endoffset + php_strpos(rawdata, "LYRICSBEGIN")
                rawdata = php_substr(rawdata, php_strpos(rawdata, "LYRICSBEGIN"))
                length = php_strlen(rawdata)
                ParsedLyrics3["tag_offset_start"] = info["avdataend"]
                ParsedLyrics3["raw"]["lyrics3tagsize"] = length
            else:
                self.error("\"LYRICSBEGIN\" expected at " + endoffset + " but found \"" + php_substr(rawdata, 0, 11) + "\" instead")
                return False
            # end if
        # end if
        for case in Switch(version):
            if case(1):
                if php_substr(rawdata, php_strlen(rawdata) - 9, 9) == "LYRICSEND":
                    ParsedLyrics3["raw"]["LYR"] = php_trim(php_substr(rawdata, 11, php_strlen(rawdata) - 11 - 9))
                    self.lyrics3lyricstimestampparse(ParsedLyrics3)
                else:
                    self.error("\"LYRICSEND\" expected at " + self.ftell() - 11 + length - 9 + " but found \"" + php_substr(rawdata, php_strlen(rawdata) - 9, 9) + "\" instead")
                    return False
                # end if
                break
            # end if
            if case(2):
                if php_substr(rawdata, php_strlen(rawdata) - 9, 9) == "LYRICS200":
                    ParsedLyrics3["raw"]["unparsed"] = php_substr(rawdata, 11, php_strlen(rawdata) - 11 - 9 - 6)
                    #// LYRICSBEGIN + LYRICS200 + LSZ
                    rawdata = ParsedLyrics3["raw"]["unparsed"]
                    while True:
                        
                        if not (php_strlen(rawdata) > 0):
                            break
                        # end if
                        fieldname = php_substr(rawdata, 0, 3)
                        fieldsize = php_int(php_substr(rawdata, 3, 5))
                        ParsedLyrics3["raw"][fieldname] = php_substr(rawdata, 8, fieldsize)
                        rawdata = php_substr(rawdata, 3 + 5 + fieldsize)
                    # end while
                    if (php_isset(lambda : ParsedLyrics3["raw"]["IND"])):
                        i = 0
                        flagnames = Array("lyrics", "timestamps", "inhibitrandom")
                        for flagname in flagnames:
                            if php_strlen(ParsedLyrics3["raw"]["IND"]) > i:
                                ParsedLyrics3["flags"][flagname] = self.intstring2bool(php_substr(ParsedLyrics3["raw"]["IND"], i, 1 - 1))
                            # end if
                            i += 1
                        # end for
                    # end if
                    fieldnametranslation = Array({"ETT": "title", "EAR": "artist", "EAL": "album", "INF": "comment", "AUT": "author"})
                    for key,value in fieldnametranslation:
                        if (php_isset(lambda : ParsedLyrics3["raw"][key])):
                            ParsedLyrics3["comments"][value][-1] = php_trim(ParsedLyrics3["raw"][key])
                        # end if
                    # end for
                    if (php_isset(lambda : ParsedLyrics3["raw"]["IMG"])):
                        imagestrings = php_explode("\r\n", ParsedLyrics3["raw"]["IMG"])
                        for key,imagestring in imagestrings:
                            if php_strpos(imagestring, "||") != False:
                                imagearray = php_explode("||", imagestring)
                                ParsedLyrics3["images"][key]["filename"] = imagearray[0] if (php_isset(lambda : imagearray[0])) else ""
                                ParsedLyrics3["images"][key]["description"] = imagearray[1] if (php_isset(lambda : imagearray[1])) else ""
                                ParsedLyrics3["images"][key]["timestamp"] = self.lyrics3timestamp2seconds(imagearray[2] if (php_isset(lambda : imagearray[2])) else "")
                            # end if
                        # end for
                    # end if
                    if (php_isset(lambda : ParsedLyrics3["raw"]["LYR"])):
                        self.lyrics3lyricstimestampparse(ParsedLyrics3)
                    # end if
                else:
                    self.error("\"LYRICS200\" expected at " + self.ftell() - 11 + length - 9 + " but found \"" + php_substr(rawdata, php_strlen(rawdata) - 9, 9) + "\" instead")
                    return False
                # end if
                break
            # end if
            if case():
                self.error("Cannot process Lyrics3 version " + version + " (only v1 and v2)")
                return False
                break
            # end if
        # end for
        if (php_isset(lambda : info["id3v1"]["tag_offset_start"])) and info["id3v1"]["tag_offset_start"] <= ParsedLyrics3["tag_offset_end"]:
            self.warning("ID3v1 tag information ignored since it appears to be a false synch in Lyrics3 tag data")
            info["id3v1"] = None
            for key,value in info["warning"]:
                if value == "Some ID3v1 fields do not use NULL characters for padding":
                    info["warning"][key] = None
                    sort(info["warning"])
                    break
                # end if
            # end for
        # end if
        info["lyrics3"] = ParsedLyrics3
        return True
    # end def getlyrics3data
    #// 
    #// @param string $rawtimestamp
    #// 
    #// @return int|false
    #//
    def lyrics3timestamp2seconds(self, rawtimestamp=None):
        
        if php_preg_match("#^\\[([0-9]{2}):([0-9]{2})\\]$#", rawtimestamp, regs):
            return php_int(regs[1] * 60 + regs[2])
        # end if
        return False
    # end def lyrics3timestamp2seconds
    #// 
    #// @param array $Lyrics3data
    #// 
    #// @return bool
    #//
    def lyrics3lyricstimestampparse(self, Lyrics3data=None):
        
        lyricsarray = php_explode("\r\n", Lyrics3data["raw"]["LYR"])
        notimestamplyricsarray = Array()
        for key,lyricline in lyricsarray:
            regs = Array()
            thislinetimestamps = None
            while True:
                
                if not (php_preg_match("#^(\\[[0-9]{2}:[0-9]{2}\\])#", lyricline, regs)):
                    break
                # end if
                thislinetimestamps[-1] = self.lyrics3timestamp2seconds(regs[0])
                lyricline = php_str_replace(regs[0], "", lyricline)
            # end while
            notimestamplyricsarray[key] = lyricline
            if (php_isset(lambda : thislinetimestamps)) and php_is_array(thislinetimestamps):
                sort(thislinetimestamps)
                for timestampkey,timestamp in thislinetimestamps:
                    if (php_isset(lambda : Lyrics3data["synchedlyrics"][timestamp])):
                        #// timestamps only have a 1-second resolution, it's possible that multiple lines
                        #// could have the same timestamp, if so, append
                        Lyrics3data["synchedlyrics"][timestamp] += "\r\n" + lyricline
                    else:
                        Lyrics3data["synchedlyrics"][timestamp] = lyricline
                    # end if
                # end for
            # end if
        # end for
        Lyrics3data["unsynchedlyrics"] = php_implode("\r\n", notimestamplyricsarray)
        if (php_isset(lambda : Lyrics3data["synchedlyrics"])) and php_is_array(Lyrics3data["synchedlyrics"]):
            ksort(Lyrics3data["synchedlyrics"])
        # end if
        return True
    # end def lyrics3lyricstimestampparse
    #// 
    #// @param string $char
    #// 
    #// @return bool|null
    #//
    def intstring2bool(self, char=None):
        
        if char == "1":
            return True
        elif char == "0":
            return False
        # end if
        return None
    # end def intstring2bool
# end class getid3_lyrics3
