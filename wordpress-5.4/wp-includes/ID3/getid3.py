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
#// 
#// Please see readme.txt for more information
#// 
#// 
#// define a constant rather than looking up every time it is needed
if (not php_defined("GETID3_OS_ISWINDOWS")):
    php_define("GETID3_OS_ISWINDOWS", php_stripos(PHP_OS, "WIN") == 0)
# end if
#// Get base path of getID3() - ONCE
if (not php_defined("GETID3_INCLUDEPATH")):
    php_define("GETID3_INCLUDEPATH", php_dirname(__FILE__) + DIRECTORY_SEPARATOR)
# end if
#// Workaround Bug #39923 (https://bugs.php.net/bug.php?id=39923)
if (not php_defined("IMG_JPG")) and php_defined("IMAGETYPE_JPEG"):
    php_define("IMG_JPG", IMAGETYPE_JPEG)
# end if
if (not php_defined("ENT_SUBSTITUTE")):
    #// PHP5.3 adds ENT_IGNORE, PHP5.4 adds ENT_SUBSTITUTE
    php_define("ENT_SUBSTITUTE", ENT_IGNORE if php_defined("ENT_IGNORE") else 8)
# end if
#// 
#// https://www.getid3.org/phpBB3/viewtopic.php?t=2114
#// If you are running into a the problem where filenames with special characters are being handled
#// incorrectly by external helper programs (e.g. metaflac), notably with the special characters removed,
#// and you are passing in the filename in UTF8 (typically via a HTML form), try uncommenting this line:
#// 
#// setlocale(LC_CTYPE, 'en_US.UTF-8');
#// attempt to define temp dir as something flexible but reliable
temp_dir = php_ini_get("upload_tmp_dir")
if temp_dir and (not php_is_dir(temp_dir)) or (not php_is_readable(temp_dir)):
    temp_dir = ""
# end if
if (not temp_dir) and php_function_exists("sys_get_temp_dir"):
    #// sys_get_temp_dir added in PHP v5.2.1
    #// sys_get_temp_dir() may give inaccessible temp dir, e.g. with open_basedir on virtual hosts
    temp_dir = php_sys_get_temp_dir()
# end if
temp_dir = php_no_error(lambda: php_realpath(temp_dir))
#// see https://github.com/JamesHeinrich/getID3/pull/10
open_basedir = php_ini_get("open_basedir")
if open_basedir:
    #// e.g. "/var/www/vhosts/getid3.org/httpdocs/:/tmp/"
    temp_dir = php_str_replace(Array("/", "\\"), DIRECTORY_SEPARATOR, temp_dir)
    open_basedir = php_str_replace(Array("/", "\\"), DIRECTORY_SEPARATOR, open_basedir)
    if php_substr(temp_dir, -1, 1) != DIRECTORY_SEPARATOR:
        temp_dir += DIRECTORY_SEPARATOR
    # end if
    found_valid_tempdir = False
    open_basedirs = php_explode(PATH_SEPARATOR, open_basedir)
    for basedir in open_basedirs:
        if php_substr(basedir, -1, 1) != DIRECTORY_SEPARATOR:
            basedir += DIRECTORY_SEPARATOR
        # end if
        if php_preg_match("#^" + preg_quote(basedir) + "#", temp_dir):
            found_valid_tempdir = True
            break
        # end if
    # end for
    if (not found_valid_tempdir):
        temp_dir = ""
    # end if
    open_basedirs = None
    found_valid_tempdir = None
    basedir = None
# end if
if (not temp_dir):
    temp_dir = "*"
    pass
# end if
#// $temp_dir = '/something/else/';  // feel free to override temp dir here if it works better for your system
if (not php_defined("GETID3_TEMP_DIR")):
    php_define("GETID3_TEMP_DIR", temp_dir)
# end if
open_basedir = None
temp_dir = None
#// End: Defines
class getID3():
    encoding = "UTF-8"
    encoding_id3v1 = "ISO-8859-1"
    option_tag_id3v1 = True
    option_tag_id3v2 = True
    option_tag_lyrics3 = True
    option_tag_apetag = True
    option_tags_process = True
    option_tags_html = True
    option_extra_info = True
    option_save_attachments = True
    option_md5_data = False
    option_md5_data_source = False
    option_sha1_data = False
    option_max_2gb_check = Array()
    option_fread_buffer_size = 32768
    filename = Array()
    fp = Array()
    info = Array()
    tempdir = GETID3_TEMP_DIR
    memory_limit = 0
    startup_error = ""
    startup_warning = ""
    VERSION = "1.9.18-201907240906"
    FREAD_BUFFER_SIZE = 32768
    ATTACHMENTS_NONE = False
    ATTACHMENTS_INLINE = True
    def __init__(self):
        
        #// Check for PHP version
        required_php_version = "5.3.0"
        if php_version_compare(PHP_VERSION, required_php_version, "<"):
            self.startup_error += "getID3() requires PHP v" + required_php_version + " or higher - you are running v" + PHP_VERSION + "\n"
            return
        # end if
        #// Check memory
        self.memory_limit = php_ini_get("memory_limit")
        if php_preg_match("#([0-9]+) ?M#i", self.memory_limit, matches):
            #// could be stored as "16M" rather than 16777216 for example
            self.memory_limit = matches[1] * 1048576
        elif php_preg_match("#([0-9]+) ?G#i", self.memory_limit, matches):
            #// The 'G' modifier is available since PHP 5.1.0
            #// could be stored as "2G" rather than 2147483648 for example
            self.memory_limit = matches[1] * 1073741824
        # end if
        if self.memory_limit <= 0:
            pass
        elif self.memory_limit <= 4194304:
            self.startup_error += "PHP has less than 4MB available memory and will very likely run out. Increase memory_limit in php.ini" + "\n"
        elif self.memory_limit <= 12582912:
            self.startup_warning += "PHP has less than 12MB available memory and might run out if all modules are loaded. Increase memory_limit in php.ini" + "\n"
        # end if
        #// Check safe_mode off
        if php_preg_match("#(1|ON)#i", php_ini_get("safe_mode")):
            self.warning("WARNING: Safe mode is on, shorten support disabled, md5data/sha1data for ogg vorbis disabled, ogg vorbos/flac tag writing disabled.")
        # end if
        mbstring_func_overload = php_ini_get("mbstring.func_overload")
        if mbstring_func_overload and mbstring_func_overload & 2:
            #// http://php.net/manual/en/mbstring.overload.php
            #// "mbstring.func_overload in php.ini is a positive value that represents a combination of bitmasks specifying the categories of functions to be overloaded. It should be set to 1 to overload the mail() function. 2 for string functions, 4 for regular expression functions"
            #// getID3 cannot run when string functions are overloaded. It doesn't matter if mail() or ereg* functions are overloaded since getID3 does not use those.
            self.startup_error += "WARNING: php.ini contains \"mbstring.func_overload = " + php_ini_get("mbstring.func_overload") + "\", getID3 cannot run with this setting (bitmask 2 (string functions) cannot be set). Recommended to disable entirely." + "\n"
        # end if
        #// WORDPRESS CHANGE FROM UPSTREAM
        #// Comment out deprecated function
        #// 
        #// Check for magic_quotes_runtime
        #// if (function_exists('get_magic_quotes_runtime')) {
        #// if (get_magic_quotes_runtime()) {
        #// $this->startup_error .= 'magic_quotes_runtime must be disabled before running getID3(). Surround getid3 block by set_magic_quotes_runtime(0) and set_magic_quotes_runtime(1).'."\n";
        #// }
        #// }
        #// Check for magic_quotes_gpc
        #// if (function_exists('magic_quotes_gpc')) {
        #// if (get_magic_quotes_gpc()) {
        #// $this->startup_error .= 'magic_quotes_gpc must be disabled before running getID3(). Surround getid3 block by set_magic_quotes_gpc(0) and set_magic_quotes_gpc(1).'."\n";
        #// }
        #// }
        #// 
        #// Load support library
        if (not php_include_file(GETID3_INCLUDEPATH + "getid3.lib.php", once=False)):
            self.startup_error += "getid3.lib.php is missing or corrupt" + "\n"
        # end if
        if self.option_max_2gb_check == None:
            self.option_max_2gb_check = PHP_INT_MAX <= 2147483647
        # end if
        #// Needed for Windows only:
        #// Define locations of helper applications for Shorten, VorbisComment, MetaFLAC
        #// as well as other helper functions such as head, etc
        #// This path cannot contain spaces, but the below code will attempt to get the
        #// 8.3-equivalent path automatically
        #// IMPORTANT: This path must include the trailing slash
        if GETID3_OS_ISWINDOWS and (not php_defined("GETID3_HELPERAPPSDIR")):
            helperappsdir = GETID3_INCLUDEPATH + ".." + DIRECTORY_SEPARATOR + "helperapps"
            #// must not have any space in this path
            if (not php_is_dir(helperappsdir)):
                self.startup_warning += "\"" + helperappsdir + "\" cannot be defined as GETID3_HELPERAPPSDIR because it does not exist" + "\n"
            elif php_strpos(php_realpath(helperappsdir), " ") != False:
                DirPieces = php_explode(DIRECTORY_SEPARATOR, php_realpath(helperappsdir))
                path_so_far = Array()
                for key,value in DirPieces:
                    if php_strpos(value, " ") != False:
                        if (not php_empty(lambda : path_so_far)):
                            commandline = "dir /x " + escapeshellarg(php_implode(DIRECTORY_SEPARATOR, path_so_far))
                            dir_listing = os.system("commandline")
                            lines = php_explode("\n", dir_listing)
                            for line in lines:
                                line = php_trim(line)
                                if php_preg_match("#^([0-9/]{10}) +([0-9:]{4,5}( [AP]M)?) +(<DIR>|[0-9,]+) +([^ ]{0,11}) +(.+)$#", line, matches):
                                    dummy, date, time, ampm, filesize, shortname, filename = matches
                                    if php_strtoupper(filesize) == "<DIR>" and php_strtolower(filename) == php_strtolower(value):
                                        value = shortname
                                    # end if
                                # end if
                            # end for
                        else:
                            self.startup_warning += "GETID3_HELPERAPPSDIR must not have any spaces in it - use 8dot3 naming convention if neccesary. You can run \"dir /x\" from the commandline to see the correct 8.3-style names." + "\n"
                        # end if
                    # end if
                    path_so_far[-1] = value
                # end for
                helperappsdir = php_implode(DIRECTORY_SEPARATOR, path_so_far)
            # end if
            php_define("GETID3_HELPERAPPSDIR", helperappsdir + DIRECTORY_SEPARATOR)
        # end if
        if (not php_empty(lambda : self.startup_error)):
            php_print(self.startup_error)
            raise php_new_class("getid3_exception", lambda : getid3_exception(self.startup_error))
        # end if
    # end def __init__
    #// 
    #// @return string
    #//
    def version(self):
        
        return self.VERSION
    # end def version
    #// 
    #// @return int
    #//
    def fread_buffer_size(self):
        
        return self.option_fread_buffer_size
    # end def fread_buffer_size
    #// 
    #// @param array $optArray
    #// 
    #// @return bool
    #//
    def setoption(self, optArray=None):
        
        if (not php_is_array(optArray)) or php_empty(lambda : optArray):
            return False
        # end if
        for opt,val in optArray:
            if (php_isset(lambda : self.opt)) == False:
                continue
            # end if
            self.opt = val
        # end for
        return True
    # end def setoption
    #// 
    #// @param string $filename
    #// @param int    $filesize
    #// 
    #// @return bool
    #// 
    #// @throws getid3_exception
    #//
    def openfile(self, filename=None, filesize=None, fp=None):
        
        try: 
            if (not php_empty(lambda : self.startup_error)):
                raise php_new_class("getid3_exception", lambda : getid3_exception(self.startup_error))
            # end if
            if (not php_empty(lambda : self.startup_warning)):
                for startup_warning in php_explode("\n", self.startup_warning):
                    self.warning(startup_warning)
                # end for
            # end if
            #// init result array and set parameters
            self.filename = filename
            self.info = Array()
            self.info["GETID3_VERSION"] = self.version()
            self.info["php_memory_limit"] = self.memory_limit if self.memory_limit > 0 else False
            #// remote files not supported
            if php_preg_match("#^(ht|f)tp://#", filename):
                raise php_new_class("getid3_exception", lambda : getid3_exception("Remote files are not supported - please copy the file locally first"))
            # end if
            filename = php_str_replace("/", DIRECTORY_SEPARATOR, filename)
            #// $filename = preg_replace('#(?<!gs:)('.preg_quote(DIRECTORY_SEPARATOR).'{2,})#', DIRECTORY_SEPARATOR, $filename);
            #// open local file
            #// if (is_readable($filename) && is_file($filename) && ($this->fp = fopen($filename, 'rb'))) { // see https://www.getid3.org/phpBB3/viewtopic.php?t=1720
            if fp != None and get_resource_type(fp) == "file" or get_resource_type(fp) == "stream":
                self.fp = fp
            elif php_is_readable(filename) or php_file_exists(filename) and php_is_file(filename) and fopen(filename, "rb"):
                self.fp = fopen(filename, "rb")
                pass
            else:
                errormessagelist = Array()
                if (not php_is_readable(filename)):
                    errormessagelist[-1] = "!is_readable"
                # end if
                if (not php_is_file(filename)):
                    errormessagelist[-1] = "!is_file"
                # end if
                if (not php_file_exists(filename)):
                    errormessagelist[-1] = "!file_exists"
                # end if
                if php_empty(lambda : errormessagelist):
                    errormessagelist[-1] = "fopen failed"
                # end if
                raise php_new_class("getid3_exception", lambda : getid3_exception("Could not open \"" + filename + "\" (" + php_implode("; ", errormessagelist) + ")"))
            # end if
            self.info["filesize"] = filesize if (not php_is_null(filesize)) else filesize(filename)
            #// set redundant parameters - might be needed in some include file
            #// filenames / filepaths in getID3 are always expressed with forward slashes (unix-style) for both Windows and other to try and minimize confusion
            filename = php_str_replace("\\", "/", filename)
            self.info["filepath"] = php_str_replace("\\", "/", php_realpath(php_dirname(filename)))
            self.info["filename"] = getid3_lib.mb_basename(filename)
            self.info["filenamepath"] = self.info["filepath"] + "/" + self.info["filename"]
            #// set more parameters
            self.info["avdataoffset"] = 0
            self.info["avdataend"] = self.info["filesize"]
            self.info["fileformat"] = ""
            #// filled in later
            self.info["audio"]["dataformat"] = ""
            #// filled in later, unset if not used
            self.info["video"]["dataformat"] = ""
            #// filled in later, unset if not used
            self.info["tags"] = Array()
            #// filled in later, unset if not used
            self.info["error"] = Array()
            #// filled in later, unset if not used
            self.info["warning"] = Array()
            #// filled in later, unset if not used
            self.info["comments"] = Array()
            #// filled in later, unset if not used
            self.info["encoding"] = self.encoding
            #// required by id3v2 and iso modules - can be unset at the end if desired
            #// option_max_2gb_check
            if self.option_max_2gb_check:
                #// PHP (32-bit all, and 64-bit Windows) doesn't support integers larger than 2^31 (~2GB)
                #// filesize() simply returns (filesize % (pow(2, 32)), no matter the actual filesize
                #// ftell() returns 0 if seeking to the end is beyond the range of unsigned integer
                fseek = fseek(self.fp, 0, SEEK_END)
                if fseek < 0 or self.info["filesize"] != 0 and ftell(self.fp) == 0 or self.info["filesize"] < 0 or ftell(self.fp) < 0:
                    real_filesize = getid3_lib.getfilesizesyscall(self.info["filenamepath"])
                    if real_filesize == False:
                        self.info["filesize"] = None
                        php_fclose(self.fp)
                        raise php_new_class("getid3_exception", lambda : getid3_exception("Unable to determine actual filesize. File is most likely larger than " + round(PHP_INT_MAX / 1073741824) + "GB and is not supported by PHP."))
                    elif getid3_lib.intvaluesupported(real_filesize):
                        self.info["filesize"] = None
                        php_fclose(self.fp)
                        raise php_new_class("getid3_exception", lambda : getid3_exception("PHP seems to think the file is larger than " + round(PHP_INT_MAX / 1073741824) + "GB, but filesystem reports it as " + number_format(real_filesize / 1073741824, 3) + "GB, please report to info@getid3.org"))
                    # end if
                    self.info["filesize"] = real_filesize
                    self.warning("File is larger than " + round(PHP_INT_MAX / 1073741824) + "GB (filesystem reports it as " + number_format(real_filesize / 1073741824, 3) + "GB) and is not properly supported by PHP.")
                # end if
            # end if
            return True
        except Exception as e:
            self.error(e.getmessage())
        # end try
        return False
    # end def openfile
    #// 
    #// analyze file
    #// 
    #// @param string $filename
    #// @param int    $filesize
    #// @param string $original_filename
    #// 
    #// @return array
    #//
    def analyze(self, filename=None, filesize=None, original_filename="", fp=None):
        
        try: 
            if (not self.openfile(filename, filesize, fp)):
                return self.info
            # end if
            #// Handle tags
            for tag_name,tag_key in Array({"id3v2": "id3v2", "id3v1": "id3v1", "apetag": "ape", "lyrics3": "lyrics3"}):
                option_tag = "option_tag_" + tag_name
                if self.option_tag:
                    self.include_module("tag." + tag_name)
                    try: 
                        tag_class = "getid3_" + tag_name
                        tag = php_new_class(tag_class, lambda : {**locals(), **globals()}[tag_class](self))
                        tag.analyze()
                    except getid3_exception as e:
                        raise e
                    # end try
                # end if
            # end for
            if (php_isset(lambda : self.info["id3v2"]["tag_offset_start"])):
                self.info["avdataoffset"] = php_max(self.info["avdataoffset"], self.info["id3v2"]["tag_offset_end"])
            # end if
            for tag_name,tag_key in Array({"id3v1": "id3v1", "apetag": "ape", "lyrics3": "lyrics3"}):
                if (php_isset(lambda : self.info[tag_key]["tag_offset_start"])):
                    self.info["avdataend"] = php_min(self.info["avdataend"], self.info[tag_key]["tag_offset_start"])
                # end if
            # end for
            #// ID3v2 detection (NOT parsing), even if ($this->option_tag_id3v2 == false) done to make fileformat easier
            if (not self.option_tag_id3v2):
                fseek(self.fp, 0)
                header = fread(self.fp, 10)
                if php_substr(header, 0, 3) == "ID3" and php_strlen(header) == 10:
                    self.info["id3v2"]["header"] = True
                    self.info["id3v2"]["majorversion"] = php_ord(header[3])
                    self.info["id3v2"]["minorversion"] = php_ord(header[4])
                    self.info["avdataoffset"] += getid3_lib.bigendian2int(php_substr(header, 6, 4), 1) + 10
                    pass
                # end if
            # end if
            #// read 32 kb file data
            fseek(self.fp, self.info["avdataoffset"])
            formattest = fread(self.fp, 32774)
            #// determine format
            determined_format = self.getfileformat(formattest, original_filename if original_filename else filename)
            #// unable to determine file format
            if (not determined_format):
                php_fclose(self.fp)
                return self.error("unable to determine file format")
            # end if
            #// check for illegal ID3 tags
            if (php_isset(lambda : determined_format["fail_id3"])) and php_in_array("id3v1", self.info["tags"]) or php_in_array("id3v2", self.info["tags"]):
                if determined_format["fail_id3"] == "ERROR":
                    php_fclose(self.fp)
                    return self.error("ID3 tags not allowed on this file type.")
                elif determined_format["fail_id3"] == "WARNING":
                    self.warning("ID3 tags not allowed on this file type.")
                # end if
            # end if
            #// check for illegal APE tags
            if (php_isset(lambda : determined_format["fail_ape"])) and php_in_array("ape", self.info["tags"]):
                if determined_format["fail_ape"] == "ERROR":
                    php_fclose(self.fp)
                    return self.error("APE tags not allowed on this file type.")
                elif determined_format["fail_ape"] == "WARNING":
                    self.warning("APE tags not allowed on this file type.")
                # end if
            # end if
            #// set mime type
            self.info["mime_type"] = determined_format["mime_type"]
            #// supported format signature pattern detected, but module deleted
            if (not php_file_exists(GETID3_INCLUDEPATH + determined_format["include"])):
                php_fclose(self.fp)
                return self.error("Format not supported, module \"" + determined_format["include"] + "\" was removed.")
            # end if
            #// module requires mb_convert_encoding/iconv support
            #// Check encoding/iconv support
            if (not php_empty(lambda : determined_format["iconv_req"])) and (not php_function_exists("mb_convert_encoding")) and (not php_function_exists("iconv")) and (not php_in_array(self.encoding, Array("ISO-8859-1", "UTF-8", "UTF-16LE", "UTF-16BE", "UTF-16"))):
                errormessage = "mb_convert_encoding() or iconv() support is required for this module (" + determined_format["include"] + ") for encodings other than ISO-8859-1, UTF-8, UTF-16LE, UTF16-BE, UTF-16. "
                if GETID3_OS_ISWINDOWS:
                    errormessage += "PHP does not have mb_convert_encoding() or iconv() support. Please enable php_mbstring.dll / php_iconv.dll in php.ini, and copy php_mbstring.dll / iconv.dll from c:/php/dlls to c:/windows/system32"
                else:
                    errormessage += "PHP is not compiled with mb_convert_encoding() or iconv() support. Please recompile with the --enable-mbstring / --with-iconv switch"
                # end if
                return self.error(errormessage)
            # end if
            #// include module
            php_include_file(GETID3_INCLUDEPATH + determined_format["include"], once=False)
            #// instantiate module class
            class_name = "getid3_" + determined_format["module"]
            if (not php_class_exists(class_name)):
                return self.error("Format not supported, module \"" + determined_format["include"] + "\" is corrupt.")
            # end if
            class_ = php_new_class(class_name, lambda : {**locals(), **globals()}[class_name](self))
            class_.analyze()
            class_ = None
            #// close file
            php_fclose(self.fp)
            #// process all tags - copy to 'tags' and convert charsets
            if self.option_tags_process:
                self.handlealltags()
            # end if
            #// perform more calculations
            if self.option_extra_info:
                self.channelsbitrateplaytimecalculations()
                self.calculatecompressionratiovideo()
                self.calculatecompressionratioaudio()
                self.calculatereplaygain()
                self.processaudiostreams()
            # end if
            #// get the MD5 sum of the audio/video portion of the file - without ID3/APE/Lyrics3/etc header/footer tags
            if self.option_md5_data:
                #// do not calc md5_data if md5_data_source is present - set by flac only - future MPC/SV8 too
                if (not self.option_md5_data_source) or php_empty(lambda : self.info["md5_data_source"]):
                    self.gethashdata("md5")
                # end if
            # end if
            #// get the SHA1 sum of the audio/video portion of the file - without ID3/APE/Lyrics3/etc header/footer tags
            if self.option_sha1_data:
                self.gethashdata("sha1")
            # end if
            #// remove undesired keys
            self.cleanup()
        except Exception as e:
            self.error("Caught exception: " + e.getmessage())
        # end try
        #// return info array
        return self.info
    # end def analyze
    #// 
    #// Error handling.
    #// 
    #// @param string $message
    #// 
    #// @return array
    #//
    def error(self, message=None):
        
        self.cleanup()
        if (not (php_isset(lambda : self.info["error"]))):
            self.info["error"] = Array()
        # end if
        self.info["error"][-1] = message
        return self.info
    # end def error
    #// 
    #// Warning handling.
    #// 
    #// @param string $message
    #// 
    #// @return bool
    #//
    def warning(self, message=None):
        
        self.info["warning"][-1] = message
        return True
    # end def warning
    #// 
    #// @return bool
    #//
    def cleanup(self):
        
        #// remove possible empty keys
        AVpossibleEmptyKeys = Array("dataformat", "bits_per_sample", "encoder_options", "streams", "bitrate")
        for dummy,key in AVpossibleEmptyKeys:
            if php_empty(lambda : self.info["audio"][key]) and (php_isset(lambda : self.info["audio"][key])):
                self.info["audio"][key] = None
            # end if
            if php_empty(lambda : self.info["video"][key]) and (php_isset(lambda : self.info["video"][key])):
                self.info["video"][key] = None
            # end if
        # end for
        #// remove empty root keys
        if (not php_empty(lambda : self.info)):
            for key,value in self.info:
                if php_empty(lambda : self.info[key]) and self.info[key] != 0 and self.info[key] != "0":
                    self.info[key] = None
                # end if
            # end for
        # end if
        #// remove meaningless entries from unknown-format files
        if php_empty(lambda : self.info["fileformat"]):
            if (php_isset(lambda : self.info["avdataoffset"])):
                self.info["avdataoffset"] = None
            # end if
            if (php_isset(lambda : self.info["avdataend"])):
                self.info["avdataend"] = None
            # end if
        # end if
        #// remove possible duplicated identical entries
        if (not php_empty(lambda : self.info["error"])):
            self.info["error"] = php_array_values(array_unique(self.info["error"]))
        # end if
        if (not php_empty(lambda : self.info["warning"])):
            self.info["warning"] = php_array_values(array_unique(self.info["warning"]))
        # end if
        self.info["php_memory_limit"] = None
        return True
    # end def cleanup
    #// 
    #// Return array containing information about all supported formats.
    #// 
    #// @return array
    #//
    def getfileformatarray(self):
        
        format_info = Array()
        if php_empty(lambda : format_info):
            format_info = Array({"ac3": Array({"pattern": "^\\x0B\\x77", "group": "audio", "module": "ac3", "mime_type": "audio/ac3"})}, {"adif": Array({"pattern": "^ADIF", "group": "audio", "module": "aac", "mime_type": "audio/aac", "fail_ape": "WARNING"})}, {"adts": Array({"pattern": "^\\xFF[\\xF0-\\xF1\\xF8-\\xF9]", "group": "audio", "module": "aac", "mime_type": "audio/aac", "fail_ape": "WARNING"})}, {"au": Array({"pattern": "^\\.snd", "group": "audio", "module": "au", "mime_type": "audio/basic"})}, {"amr": Array({"pattern": "^\\x23\\x21AMR\\x0A", "group": "audio", "module": "amr", "mime_type": "audio/amr"})}, {"avr": Array({"pattern": "^2BIT", "group": "audio", "module": "avr", "mime_type": "application/octet-stream"})}, {"bonk": Array({"pattern": "^\\x00(BONK|INFO|META| ID3)", "group": "audio", "module": "bonk", "mime_type": "audio/xmms-bonk"})}, {"dsf": Array({"pattern": "^DSD ", "group": "audio", "module": "dsf", "mime_type": "audio/dsd"})}, {"dss": Array({"pattern": "^[\\x02-\\x08]ds[s2]", "group": "audio", "module": "dss", "mime_type": "application/octet-stream"})}, {"dts": Array({"pattern": "^\\x7F\\xFE\\x80\\x01", "group": "audio", "module": "dts", "mime_type": "audio/dts"})}, {"flac": Array({"pattern": "^fLaC", "group": "audio", "module": "flac", "mime_type": "audio/flac"})}, {"la": Array({"pattern": "^LA0[2-4]", "group": "audio", "module": "la", "mime_type": "application/octet-stream"})}, {"lpac": Array({"pattern": "^LPAC", "group": "audio", "module": "lpac", "mime_type": "application/octet-stream"})}, {"midi": Array({"pattern": "^MThd", "group": "audio", "module": "midi", "mime_type": "audio/midi"})}, {"mac": Array({"pattern": "^MAC ", "group": "audio", "module": "monkey", "mime_type": "audio/x-monkeys-audio"})}, {"it": Array({"pattern": "^IMPM", "group": "audio", "module": "mod", "mime_type": "audio/it"})}, {"xm": Array({"pattern": "^Extended Module", "group": "audio", "module": "mod", "mime_type": "audio/xm"})}, {"s3m": Array({"pattern": "^.{44}SCRM"}, {"group": "audio", "module": "mod", "mime_type": "audio/s3m"})}, {"mpc": Array({"pattern": "^(MPCK|MP\\+|[\\x00\\x01\\x10\\x11\\x40\\x41\\x50\\x51\\x80\\x81\\x90\\x91\\xC0\\xC1\\xD0\\xD1][\\x20-\\x37][\\x00\\x20\\x40\\x60\\x80\\xA0\\xC0\\xE0])", "group": "audio", "module": "mpc", "mime_type": "audio/x-musepack"})}, {"mp3": Array({"pattern": "^\\xFF[\\xE2-\\xE7\\xF2-\\xF7\\xFA-\\xFF][\\x00-\\x0B\\x10-\\x1B\\x20-\\x2B\\x30-\\x3B\\x40-\\x4B\\x50-\\x5B\\x60-\\x6B\\x70-\\x7B\\x80-\\x8B\\x90-\\x9B\\xA0-\\xAB\\xB0-\\xBB\\xC0-\\xCB\\xD0-\\xDB\\xE0-\\xEB\\xF0-\\xFB]", "group": "audio", "module": "mp3", "mime_type": "audio/mpeg"})}, {"ofr": Array({"pattern": "^(\\*RIFF|OFR)", "group": "audio", "module": "optimfrog", "mime_type": "application/octet-stream"})}, {"rkau": Array({"pattern": "^RKA", "group": "audio", "module": "rkau", "mime_type": "application/octet-stream"})}, {"shn": Array({"pattern": "^ajkg", "group": "audio", "module": "shorten", "mime_type": "audio/xmms-shn", "fail_id3": "ERROR", "fail_ape": "ERROR"})}, {"tta": Array({"pattern": "^TTA", "group": "audio", "module": "tta", "mime_type": "application/octet-stream"})}, {"voc": Array({"pattern": "^Creative Voice File", "group": "audio", "module": "voc", "mime_type": "audio/voc"})}, {"vqf": Array({"pattern": "^TWIN", "group": "audio", "module": "vqf", "mime_type": "application/octet-stream"})}, {"wv": Array({"pattern": "^wvpk", "group": "audio", "module": "wavpack", "mime_type": "application/octet-stream"})}, {"asf": Array({"pattern": "^\\x30\\x26\\xB2\\x75\\x8E\\x66\\xCF\\x11\\xA6\\xD9\\x00\\xAA\\x00\\x62\\xCE\\x6C", "group": "audio-video", "module": "asf", "mime_type": "video/x-ms-asf", "iconv_req": False})}, {"bink": Array({"pattern": "^(BIK|SMK)", "group": "audio-video", "module": "bink", "mime_type": "application/octet-stream"})}, {"flv": Array({"pattern": "^FLV[\\x01]", "group": "audio-video", "module": "flv", "mime_type": "video/x-flv"})}, {"matroska": Array({"pattern": "^\\x1A\\x45\\xDF\\xA3", "group": "audio-video", "module": "matroska", "mime_type": "video/x-matroska"})}, {"mpeg": Array({"pattern": "^\\x00\\x00\\x01[\\xB3\\xBA]", "group": "audio-video", "module": "mpeg", "mime_type": "video/mpeg"})}, {"nsv": Array({"pattern": "^NSV[sf]", "group": "audio-video", "module": "nsv", "mime_type": "application/octet-stream"})}, {"ogg": Array({"pattern": "^OggS", "group": "audio", "module": "ogg", "mime_type": "application/ogg", "fail_id3": "WARNING", "fail_ape": "WARNING"})}, {"quicktime": Array({"pattern": "^.{4}(cmov|free|ftyp|mdat|moov|pnot|skip|wide)"}, {"group": "audio-video", "module": "quicktime", "mime_type": "video/quicktime"})}, {"riff": Array({"pattern": "^(RIFF|SDSS|FORM)", "group": "audio-video", "module": "riff", "mime_type": "audio/wav", "fail_ape": "WARNING"})}, {"real": Array({"pattern": "^\\.(RMF|ra)", "group": "audio-video", "module": "real", "mime_type": "audio/x-realaudio"})}, {"swf": Array({"pattern": "^(F|C)WS", "group": "audio-video", "module": "swf", "mime_type": "application/x-shockwave-flash"})}, {"ts": Array({"pattern": "^(\\x47.{187}){10,}"}, {"group": "audio-video", "module": "ts", "mime_type": "video/MP2T"})}, {"bmp": Array({"pattern": "^BM", "group": "graphic", "module": "bmp", "mime_type": "image/bmp", "fail_id3": "ERROR", "fail_ape": "ERROR"})}, {"gif": Array({"pattern": "^GIF", "group": "graphic", "module": "gif", "mime_type": "image/gif", "fail_id3": "ERROR", "fail_ape": "ERROR"})}, {"jpg": Array({"pattern": "^\\xFF\\xD8\\xFF", "group": "graphic", "module": "jpg", "mime_type": "image/jpeg", "fail_id3": "ERROR", "fail_ape": "ERROR"})}, {"pcd": Array({"pattern": "^.{2048}PCD_IPI\\x00"}, {"group": "graphic", "module": "pcd", "mime_type": "image/x-photo-cd", "fail_id3": "ERROR", "fail_ape": "ERROR"})}, {"png": Array({"pattern": "^\\x89\\x50\\x4E\\x47\\x0D\\x0A\\x1A\\x0A", "group": "graphic", "module": "png", "mime_type": "image/png", "fail_id3": "ERROR", "fail_ape": "ERROR"})}, {"svg": Array({"pattern": "(<!DOCTYPE svg PUBLIC |xmlns=\"http://www\\.w3\\.org/2000/svg\")", "group": "graphic", "module": "svg", "mime_type": "image/svg+xml", "fail_id3": "ERROR", "fail_ape": "ERROR"})}, {"tiff": Array({"pattern": "^(II\\x2A\\x00|MM\\x00\\x2A)", "group": "graphic", "module": "tiff", "mime_type": "image/tiff", "fail_id3": "ERROR", "fail_ape": "ERROR"})}, {"efax": Array({"pattern": "^\\xDC\\xFE", "group": "graphic", "module": "efax", "mime_type": "image/efax", "fail_id3": "ERROR", "fail_ape": "ERROR"})}, {"iso": Array({"pattern": "^.{32769}CD001"}, {"group": "misc", "module": "iso", "mime_type": "application/octet-stream", "fail_id3": "ERROR", "fail_ape": "ERROR", "iconv_req": False})}, {"rar": Array({"pattern": "^Rar\\!", "group": "archive", "module": "rar", "mime_type": "application/octet-stream", "fail_id3": "ERROR", "fail_ape": "ERROR"})}, {"szip": Array({"pattern": "^SZ\\x0A\\x04", "group": "archive", "module": "szip", "mime_type": "application/octet-stream", "fail_id3": "ERROR", "fail_ape": "ERROR"})}, {"tar": Array({"pattern": "^.{100}[0-9\\x20]{7}\\x00[0-9\\x20]{7}\\x00[0-9\\x20]{7}\\x00[0-9\\x20\\x00]{12}[0-9\\x20\\x00]{12}"}, {"group": "archive", "module": "tar", "mime_type": "application/x-tar", "fail_id3": "ERROR", "fail_ape": "ERROR"})}, {"gz": Array({"pattern": "^\\x1F\\x8B\\x08", "group": "archive", "module": "gzip", "mime_type": "application/gzip", "fail_id3": "ERROR", "fail_ape": "ERROR"})}, {"zip": Array({"pattern": "^PK\\x03\\x04", "group": "archive", "module": "zip", "mime_type": "application/zip", "fail_id3": "ERROR", "fail_ape": "ERROR"})}, {"xz": Array({"pattern": "^\\xFD7zXZ\\x00", "group": "archive", "module": "xz", "mime_type": "application/x-xz", "fail_id3": "ERROR", "fail_ape": "ERROR"})}, {"par2": Array({"pattern": "^PAR2\\x00PKT", "group": "misc", "module": "par2", "mime_type": "application/octet-stream", "fail_id3": "ERROR", "fail_ape": "ERROR"})}, {"pdf": Array({"pattern": "^\\x25PDF", "group": "misc", "module": "pdf", "mime_type": "application/pdf", "fail_id3": "ERROR", "fail_ape": "ERROR"})}, {"msoffice": Array({"pattern": "^\\xD0\\xCF\\x11\\xE0\\xA1\\xB1\\x1A\\xE1", "group": "misc", "module": "msoffice", "mime_type": "application/octet-stream", "fail_id3": "ERROR", "fail_ape": "ERROR"})}, {"cue": Array({"pattern": "", "group": "misc", "module": "cue", "mime_type": "application/octet-stream"})})
        # end if
        return format_info
    # end def getfileformatarray
    #// 
    #// @param string $filedata
    #// @param string $filename
    #// 
    #// @return mixed|false
    #//
    def getfileformat(self, filedata=None, filename=""):
        
        #// this function will determine the format of a file based on usually
        #// the first 2-4 bytes of the file (8 bytes for PNG, 16 bytes for JPG,
        #// and in the case of ISO CD image, 6 bytes offset 32kb from the start
        #// of the file).
        #// Identify file format - loop through $format_info and detect with reg expr
        for format_name,info in self.getfileformatarray():
            #// The /s switch on preg_match() forces preg_match() NOT to treat
            #// newline (0x0A) characters as special chars but do a binary match
            if (not php_empty(lambda : info["pattern"])) and php_preg_match("#" + info["pattern"] + "#s", filedata):
                info["include"] = "module." + info["group"] + "." + info["module"] + ".php"
                return info
            # end if
        # end for
        if php_preg_match("#\\.mp[123a]$#i", filename):
            #// Too many mp3 encoders on the market put garbage in front of mpeg files
            #// use assume format on these if format detection failed
            GetFileFormatArray = self.getfileformatarray()
            info = GetFileFormatArray["mp3"]
            info["include"] = "module." + info["group"] + "." + info["module"] + ".php"
            return info
        elif php_preg_match("#\\.cue$#i", filename) and php_preg_match("#FILE \"[^\"]+\" (BINARY|MOTOROLA|AIFF|WAVE|MP3)#", filedata):
            #// there's not really a useful consistent "magic" at the beginning of .cue files to identify them
            #// so until I think of something better, just go by filename if all other format checks fail
            #// and verify there's at least one instance of "TRACK xx AUDIO" in the file
            GetFileFormatArray = self.getfileformatarray()
            info = GetFileFormatArray["cue"]
            info["include"] = "module." + info["group"] + "." + info["module"] + ".php"
            return info
        # end if
        return False
    # end def getfileformat
    #// 
    #// Converts array to $encoding charset from $this->encoding.
    #// 
    #// @param array  $array
    #// @param string $encoding
    #//
    def charconvert(self, array=None, encoding=None):
        
        #// identical encoding - end here
        if encoding == self.encoding:
            return
        # end if
        #// loop thru array
        for key,value in array:
            #// go recursive
            if php_is_array(value):
                self.charconvert(array[key], encoding)
                #// convert string
            elif php_is_string(value):
                array[key] = php_trim(getid3_lib.iconv_fallback(encoding, self.encoding, value))
            # end if
        # end for
    # end def charconvert
    #// 
    #// @return bool
    #//
    def handlealltags(self):
        
        tags = None
        if php_empty(lambda : tags):
            tags = Array({"asf": Array("asf", "UTF-16LE"), "midi": Array("midi", "ISO-8859-1"), "nsv": Array("nsv", "ISO-8859-1"), "ogg": Array("vorbiscomment", "UTF-8"), "png": Array("png", "UTF-8"), "tiff": Array("tiff", "ISO-8859-1"), "quicktime": Array("quicktime", "UTF-8"), "real": Array("real", "ISO-8859-1"), "vqf": Array("vqf", "ISO-8859-1"), "zip": Array("zip", "ISO-8859-1"), "riff": Array("riff", "ISO-8859-1"), "lyrics3": Array("lyrics3", "ISO-8859-1"), "id3v1": Array("id3v1", self.encoding_id3v1), "id3v2": Array("id3v2", "UTF-8"), "ape": Array("ape", "UTF-8"), "cue": Array("cue", "ISO-8859-1"), "matroska": Array("matroska", "UTF-8"), "flac": Array("vorbiscomment", "UTF-8"), "divxtag": Array("divx", "ISO-8859-1"), "iptc": Array("iptc", "ISO-8859-1")})
        # end if
        #// loop through comments array
        for comment_name,tagname_encoding_array in tags:
            tag_name, encoding = tagname_encoding_array
            #// fill in default encoding type if not already present
            if (php_isset(lambda : self.info[comment_name])) and (not (php_isset(lambda : self.info[comment_name]["encoding"]))):
                self.info[comment_name]["encoding"] = encoding
            # end if
            #// copy comments if key name set
            if (not php_empty(lambda : self.info[comment_name]["comments"])):
                for tag_key,valuearray in self.info[comment_name]["comments"]:
                    for key,value in valuearray:
                        if php_is_string(value):
                            value = php_trim(value, " \r\n  ")
                            pass
                        # end if
                        if value:
                            if (not php_is_numeric(key)):
                                self.info["tags"][php_trim(tag_name)][php_trim(tag_key)][key] = value
                            else:
                                self.info["tags"][php_trim(tag_name)][php_trim(tag_key)][-1] = value
                            # end if
                        # end if
                    # end for
                    if tag_key == "picture":
                        self.info[comment_name]["comments"][tag_key] = None
                    # end if
                # end for
                if (not (php_isset(lambda : self.info["tags"][tag_name]))):
                    continue
                # end if
                self.charconvert(self.info["tags"][tag_name], self.info[comment_name]["encoding"])
                #// only copy gets converted!
                if self.option_tags_html:
                    for tag_key,valuearray in self.info["tags"][tag_name]:
                        if tag_key == "picture":
                            continue
                        # end if
                        self.info["tags_html"][tag_name][tag_key] = getid3_lib.recursivemultibytecharstring2html(valuearray, self.info[comment_name]["encoding"])
                    # end for
                # end if
            # end if
        # end for
        #// pictures can take up a lot of space, and we don't need multiple copies of them; let there be a single copy in [comments][picture], and not elsewhere
        if (not php_empty(lambda : self.info["tags"])):
            unset_keys = Array("tags", "tags_html")
            for tagtype,tagarray in self.info["tags"]:
                for tagname,tagdata in tagarray:
                    if tagname == "picture":
                        for key,tagarray in tagdata:
                            self.info["comments"]["picture"][-1] = tagarray
                            if (php_isset(lambda : tagarray["data"])) and (php_isset(lambda : tagarray["image_mime"])):
                                if (php_isset(lambda : self.info["tags"][tagtype][tagname][key])):
                                    self.info["tags"][tagtype][tagname][key] = None
                                # end if
                                if (php_isset(lambda : self.info["tags_html"][tagtype][tagname][key])):
                                    self.info["tags_html"][tagtype][tagname][key] = None
                                # end if
                            # end if
                        # end for
                    # end if
                # end for
                for unset_key in unset_keys:
                    #// remove possible empty keys from (e.g. [tags][id3v2][picture])
                    if php_empty(lambda : self.info[unset_key][tagtype]["picture"]):
                        self.info[unset_key][tagtype]["picture"] = None
                    # end if
                    if php_empty(lambda : self.info[unset_key][tagtype]):
                        self.info[unset_key][tagtype] = None
                    # end if
                    if php_empty(lambda : self.info[unset_key]):
                        self.info[unset_key] = None
                    # end if
                # end for
                #// remove duplicate copy of picture data from (e.g. [id3v2][comments][picture])
                if (php_isset(lambda : self.info[tagtype]["comments"]["picture"])):
                    self.info[tagtype]["comments"]["picture"] = None
                # end if
                if php_empty(lambda : self.info[tagtype]["comments"]):
                    self.info[tagtype]["comments"] = None
                # end if
                if php_empty(lambda : self.info[tagtype]):
                    self.info[tagtype] = None
                # end if
            # end for
        # end if
        return True
    # end def handlealltags
    #// 
    #// @param string $algorithm
    #// 
    #// @return array|bool
    #//
    def gethashdata(self, algorithm=None):
        
        for case in Switch(algorithm):
            if case("md5"):
                pass
            # end if
            if case("sha1"):
                break
            # end if
            if case():
                return self.error("bad algorithm \"" + algorithm + "\" in getHashdata()")
                break
            # end if
        # end for
        if (not php_empty(lambda : self.info["fileformat"])) and (not php_empty(lambda : self.info["dataformat"])) and self.info["fileformat"] == "ogg" and self.info["audio"]["dataformat"] == "vorbis":
            #// We cannot get an identical md5_data value for Ogg files where the comments
            #// span more than 1 Ogg page (compared to the same audio data with smaller
            #// comments) using the normal getID3() method of MD5'ing the data between the
            #// end of the comments and the end of the file (minus any trailing tags),
            #// because the page sequence numbers of the pages that the audio data is on
            #// do not match. Under normal circumstances, where comments are smaller than
            #// the nominal 4-8kB page size, then this is not a problem, but if there are
            #// very large comments, the only way around it is to strip off the comment
            #// tags with vorbiscomment and MD5 that file.
            #// This procedure must be applied to ALL Ogg files, not just the ones with
            #// comments larger than 1 page, because the below method simply MD5's the
            #// whole file with the comments stripped, not just the portion after the
            #// comments block (which is the standard getID3() method.
            #// The above-mentioned problem of comments spanning multiple pages and changing
            #// page sequence numbers likely happens for OggSpeex and OggFLAC as well, but
            #// currently vorbiscomment only works on OggVorbis files.
            if php_preg_match("#(1|ON)#i", php_ini_get("safe_mode")):
                self.warning("Failed making system call to vorbiscomment.exe - " + algorithm + "_data is incorrect - error returned: PHP running in Safe Mode (backtick operator not available)")
                self.info[algorithm + "_data"] = False
            else:
                #// Prevent user from aborting script
                old_abort = ignore_user_abort(True)
                #// Create empty file
                empty = php_tempnam(GETID3_TEMP_DIR, "getID3")
                touch(empty)
                #// Use vorbiscomment to make temp file without comments
                temp = php_tempnam(GETID3_TEMP_DIR, "getID3")
                file = self.info["filenamepath"]
                if GETID3_OS_ISWINDOWS:
                    if php_file_exists(GETID3_HELPERAPPSDIR + "vorbiscomment.exe"):
                        commandline = "\"" + GETID3_HELPERAPPSDIR + "vorbiscomment.exe\" -w -c \"" + empty + "\" \"" + file + "\" \"" + temp + "\""
                        VorbisCommentError = os.system("commandline")
                    else:
                        VorbisCommentError = "vorbiscomment.exe not found in " + GETID3_HELPERAPPSDIR
                    # end if
                else:
                    commandline = "vorbiscomment -w -c " + escapeshellarg(empty) + " " + escapeshellarg(file) + " " + escapeshellarg(temp) + " 2>&1"
                    VorbisCommentError = os.system("commandline")
                # end if
                if (not php_empty(lambda : VorbisCommentError)):
                    self.warning("Failed making system call to vorbiscomment(.exe) - " + algorithm + "_data will be incorrect. If vorbiscomment is unavailable, please download from http://www.vorbis.com/download.psp and put in the getID3() directory. Error returned: " + VorbisCommentError)
                    self.info[algorithm + "_data"] = False
                else:
                    #// Get hash of newly created file
                    for case in Switch(algorithm):
                        if case("md5"):
                            self.info[algorithm + "_data"] = php_md5_file(temp)
                            break
                        # end if
                        if case("sha1"):
                            self.info[algorithm + "_data"] = sha1_file(temp)
                            break
                        # end if
                    # end for
                # end if
                #// Clean up
                unlink(empty)
                unlink(temp)
                #// Reset abort setting
                ignore_user_abort(old_abort)
            # end if
        else:
            if (not php_empty(lambda : self.info["avdataoffset"])) or (php_isset(lambda : self.info["avdataend"])) and self.info["avdataend"] < self.info["filesize"]:
                #// get hash from part of file
                self.info[algorithm + "_data"] = getid3_lib.hash_data(self.info["filenamepath"], self.info["avdataoffset"], self.info["avdataend"], algorithm)
            else:
                #// get hash from whole file
                for case in Switch(algorithm):
                    if case("md5"):
                        self.info[algorithm + "_data"] = php_md5_file(self.info["filenamepath"])
                        break
                    # end if
                    if case("sha1"):
                        self.info[algorithm + "_data"] = sha1_file(self.info["filenamepath"])
                        break
                    # end if
                # end for
            # end if
        # end if
        return True
    # end def gethashdata
    def channelsbitrateplaytimecalculations(self):
        
        #// set channelmode on audio
        if (not php_empty(lambda : self.info["audio"]["channelmode"])) or (not (php_isset(lambda : self.info["audio"]["channels"]))):
            pass
        elif self.info["audio"]["channels"] == 1:
            self.info["audio"]["channelmode"] = "mono"
        elif self.info["audio"]["channels"] == 2:
            self.info["audio"]["channelmode"] = "stereo"
        # end if
        #// Calculate combined bitrate - audio + video
        CombinedBitrate = 0
        CombinedBitrate += self.info["audio"]["bitrate"] if (php_isset(lambda : self.info["audio"]["bitrate"])) else 0
        CombinedBitrate += self.info["video"]["bitrate"] if (php_isset(lambda : self.info["video"]["bitrate"])) else 0
        if CombinedBitrate > 0 and php_empty(lambda : self.info["bitrate"]):
            self.info["bitrate"] = CombinedBitrate
        # end if
        #// if ((isset($this->info['video']) && !isset($this->info['video']['bitrate'])) || (isset($this->info['audio']) && !isset($this->info['audio']['bitrate']))) {
        #// for example, VBR MPEG video files cannot determine video bitrate:
        #// should not set overall bitrate and playtime from audio bitrate only
        #// unset($this->info['bitrate']);
        #// }
        #// video bitrate undetermined, but calculable
        if (php_isset(lambda : self.info["video"]["dataformat"])) and self.info["video"]["dataformat"] and (not (php_isset(lambda : self.info["video"]["bitrate"]))) or self.info["video"]["bitrate"] == 0:
            #// if video bitrate not set
            if (php_isset(lambda : self.info["audio"]["bitrate"])) and self.info["audio"]["bitrate"] > 0 and self.info["audio"]["bitrate"] == self.info["bitrate"]:
                #// AND if audio bitrate is set to same as overall bitrate
                if (php_isset(lambda : self.info["playtime_seconds"])) and self.info["playtime_seconds"] > 0:
                    #// AND if playtime is set
                    if (php_isset(lambda : self.info["avdataend"])) and (php_isset(lambda : self.info["avdataoffset"])):
                        #// AND if AV data offset start/end is known
                        #// THEN we can calculate the video bitrate
                        self.info["bitrate"] = round(self.info["avdataend"] - self.info["avdataoffset"] * 8 / self.info["playtime_seconds"])
                        self.info["video"]["bitrate"] = self.info["bitrate"] - self.info["audio"]["bitrate"]
                    # end if
                # end if
            # end if
        # end if
        if (not (php_isset(lambda : self.info["playtime_seconds"]))) or self.info["playtime_seconds"] <= 0 and (not php_empty(lambda : self.info["bitrate"])):
            self.info["playtime_seconds"] = self.info["avdataend"] - self.info["avdataoffset"] * 8 / self.info["bitrate"]
        # end if
        if (not (php_isset(lambda : self.info["bitrate"]))) and (not php_empty(lambda : self.info["playtime_seconds"])):
            self.info["bitrate"] = self.info["avdataend"] - self.info["avdataoffset"] * 8 / self.info["playtime_seconds"]
        # end if
        if (php_isset(lambda : self.info["bitrate"])) and php_empty(lambda : self.info["audio"]["bitrate"]) and php_empty(lambda : self.info["video"]["bitrate"]):
            if (php_isset(lambda : self.info["audio"]["dataformat"])) and php_empty(lambda : self.info["video"]["resolution_x"]):
                #// audio only
                self.info["audio"]["bitrate"] = self.info["bitrate"]
            elif (php_isset(lambda : self.info["video"]["resolution_x"])) and php_empty(lambda : self.info["audio"]["dataformat"]):
                #// video only
                self.info["video"]["bitrate"] = self.info["bitrate"]
            # end if
        # end if
        #// Set playtime string
        if (not php_empty(lambda : self.info["playtime_seconds"])) and php_empty(lambda : self.info["playtime_string"]):
            self.info["playtime_string"] = getid3_lib.playtimestring(self.info["playtime_seconds"])
        # end if
    # end def channelsbitrateplaytimecalculations
    #// 
    #// @return bool
    #//
    def calculatecompressionratiovideo(self):
        
        if php_empty(lambda : self.info["video"]):
            return False
        # end if
        if php_empty(lambda : self.info["video"]["resolution_x"]) or php_empty(lambda : self.info["video"]["resolution_y"]):
            return False
        # end if
        if php_empty(lambda : self.info["video"]["bits_per_sample"]):
            return False
        # end if
        for case in Switch(self.info["video"]["dataformat"]):
            if case("bmp"):
                pass
            # end if
            if case("gif"):
                pass
            # end if
            if case("jpeg"):
                pass
            # end if
            if case("jpg"):
                pass
            # end if
            if case("png"):
                pass
            # end if
            if case("tiff"):
                FrameRate = 1
                PlaytimeSeconds = 1
                BitrateCompressed = self.info["filesize"] * 8
                break
            # end if
            if case():
                if (not php_empty(lambda : self.info["video"]["frame_rate"])):
                    FrameRate = self.info["video"]["frame_rate"]
                else:
                    return False
                # end if
                if (not php_empty(lambda : self.info["playtime_seconds"])):
                    PlaytimeSeconds = self.info["playtime_seconds"]
                else:
                    return False
                # end if
                if (not php_empty(lambda : self.info["video"]["bitrate"])):
                    BitrateCompressed = self.info["video"]["bitrate"]
                else:
                    return False
                # end if
                break
            # end if
        # end for
        BitrateUncompressed = self.info["video"]["resolution_x"] * self.info["video"]["resolution_y"] * self.info["video"]["bits_per_sample"] * FrameRate
        self.info["video"]["compression_ratio"] = BitrateCompressed / BitrateUncompressed
        return True
    # end def calculatecompressionratiovideo
    #// 
    #// @return bool
    #//
    def calculatecompressionratioaudio(self):
        
        if php_empty(lambda : self.info["audio"]["bitrate"]) or php_empty(lambda : self.info["audio"]["channels"]) or php_empty(lambda : self.info["audio"]["sample_rate"]) or (not php_is_numeric(self.info["audio"]["sample_rate"])):
            return False
        # end if
        self.info["audio"]["compression_ratio"] = self.info["audio"]["bitrate"] / self.info["audio"]["channels"] * self.info["audio"]["sample_rate"] * self.info["audio"]["bits_per_sample"] if (not php_empty(lambda : self.info["audio"]["bits_per_sample"])) else 16
        if (not php_empty(lambda : self.info["audio"]["streams"])):
            for streamnumber,streamdata in self.info["audio"]["streams"]:
                if (not php_empty(lambda : streamdata["bitrate"])) and (not php_empty(lambda : streamdata["channels"])) and (not php_empty(lambda : streamdata["sample_rate"])):
                    self.info["audio"]["streams"][streamnumber]["compression_ratio"] = streamdata["bitrate"] / streamdata["channels"] * streamdata["sample_rate"] * streamdata["bits_per_sample"] if (not php_empty(lambda : streamdata["bits_per_sample"])) else 16
                # end if
            # end for
        # end if
        return True
    # end def calculatecompressionratioaudio
    #// 
    #// @return bool
    #//
    def calculatereplaygain(self):
        
        if (php_isset(lambda : self.info["replay_gain"])):
            if (not (php_isset(lambda : self.info["replay_gain"]["reference_volume"]))):
                self.info["replay_gain"]["reference_volume"] = 89
            # end if
            if (php_isset(lambda : self.info["replay_gain"]["track"]["adjustment"])):
                self.info["replay_gain"]["track"]["volume"] = self.info["replay_gain"]["reference_volume"] - self.info["replay_gain"]["track"]["adjustment"]
            # end if
            if (php_isset(lambda : self.info["replay_gain"]["album"]["adjustment"])):
                self.info["replay_gain"]["album"]["volume"] = self.info["replay_gain"]["reference_volume"] - self.info["replay_gain"]["album"]["adjustment"]
            # end if
            if (php_isset(lambda : self.info["replay_gain"]["track"]["peak"])):
                self.info["replay_gain"]["track"]["max_noclip_gain"] = 0 - getid3_lib.rgadamplitude2db(self.info["replay_gain"]["track"]["peak"])
            # end if
            if (php_isset(lambda : self.info["replay_gain"]["album"]["peak"])):
                self.info["replay_gain"]["album"]["max_noclip_gain"] = 0 - getid3_lib.rgadamplitude2db(self.info["replay_gain"]["album"]["peak"])
            # end if
        # end if
        return True
    # end def calculatereplaygain
    #// 
    #// @return bool
    #//
    def processaudiostreams(self):
        
        if (not php_empty(lambda : self.info["audio"]["bitrate"])) or (not php_empty(lambda : self.info["audio"]["channels"])) or (not php_empty(lambda : self.info["audio"]["sample_rate"])):
            if (not (php_isset(lambda : self.info["audio"]["streams"]))):
                for key,value in self.info["audio"]:
                    if key != "streams":
                        self.info["audio"]["streams"][0][key] = value
                    # end if
                # end for
            # end if
        # end if
        return True
    # end def processaudiostreams
    #// 
    #// @return string|bool
    #//
    def getid3_tempnam(self):
        
        return php_tempnam(self.tempdir, "gI3")
    # end def getid3_tempnam
    #// 
    #// @param string $name
    #// 
    #// @return bool
    #// 
    #// @throws getid3_exception
    #//
    def include_module(self, name=None):
        
        #// if (!file_exists($this->include_path.'module.'.$name.'.php')) {
        if (not php_file_exists(GETID3_INCLUDEPATH + "module." + name + ".php")):
            raise php_new_class("getid3_exception", lambda : getid3_exception("Required module." + name + ".php is missing."))
        # end if
        php_include_file(GETID3_INCLUDEPATH + "module." + name + ".php", once=False)
        return True
    # end def include_module
    #// 
    #// @param string $filename
    #// 
    #// @return bool
    #//
    @classmethod
    def is_writable(self, filename=None):
        
        ret = php_is_writable(filename)
        if (not ret):
            perms = fileperms(filename)
            ret = perms & 128 or perms & 16 or perms & 2
        # end if
        return ret
    # end def is_writable
# end class getID3
class getid3_handler():
    getid3 = Array()
    data_string_flag = False
    data_string = ""
    data_string_position = 0
    data_string_length = 0
    dependency_to = Array()
    #// 
    #// getid3_handler constructor.
    #// 
    #// @param getID3 $getid3
    #// @param string $call_module
    #//
    def __init__(self, getid3=None, call_module=None):
        
        self.getid3 = getid3
        if call_module:
            self.dependency_to = php_str_replace("getid3_", "", call_module)
        # end if
    # end def __init__
    #// 
    #// Analyze from file pointer.
    #// 
    #// @return bool
    #//
    def analyze(self):
        
        pass
    # end def analyze
    #// 
    #// Analyze from string instead.
    #// 
    #// @param string $string
    #//
    def analyzestring(self, string=None):
        
        #// Enter string mode
        self.setstringmode(string)
        #// Save info
        saved_avdataoffset = self.getid3.info["avdataoffset"]
        saved_avdataend = self.getid3.info["avdataend"]
        saved_filesize = self.getid3.info["filesize"] if (php_isset(lambda : self.getid3.info["filesize"])) else None
        #// may be not set if called as dependency without openfile() call
        #// Reset some info
        self.getid3.info["avdataoffset"] = 0
        self.getid3.info["avdataend"] = self.getid3.info["filesize"] = self.data_string_length
        #// Analyze
        self.analyze()
        #// Restore some info
        self.getid3.info["avdataoffset"] = saved_avdataoffset
        self.getid3.info["avdataend"] = saved_avdataend
        self.getid3.info["filesize"] = saved_filesize
        #// Exit string mode
        self.data_string_flag = False
    # end def analyzestring
    #// 
    #// @param string $string
    #//
    def setstringmode(self, string=None):
        
        self.data_string_flag = True
        self.data_string = string
        self.data_string_length = php_strlen(string)
    # end def setstringmode
    #// 
    #// @return int|bool
    #//
    def ftell(self):
        
        if self.data_string_flag:
            return self.data_string_position
        # end if
        return ftell(self.getid3.fp)
    # end def ftell
    #// 
    #// @param int $bytes
    #// 
    #// @return string|false
    #// 
    #// @throws getid3_exception
    #//
    def fread(self, bytes=None):
        
        if self.data_string_flag:
            self.data_string_position += bytes
            return php_substr(self.data_string, self.data_string_position - bytes, bytes)
        # end if
        pos = self.ftell() + bytes
        if (not getid3_lib.intvaluesupported(pos)):
            raise php_new_class("getid3_exception", lambda : getid3_exception("cannot fread(" + bytes + " from " + self.ftell() + ") because beyond PHP filesystem limit", 10))
        # end if
        #// return fread($this->getid3->fp, $bytes);
        #// 
        #// https://www.getid3.org/phpBB3/viewtopic.php?t=1930
        #// "I found out that the root cause for the problem was how getID3 uses the PHP system function fread().
        #// It seems to assume that fread() would always return as many bytes as were requested.
        #// However, according the PHP manual (http://php.net/manual/en/function.fread.php), this is the case only with regular local files, but not e.g. with Linux pipes.
        #// The call may return only part of the requested data and a new call is needed to get more."
        #//
        contents = ""
        while True:
            #// if (($this->getid3->memory_limit > 0) && ($bytes > $this->getid3->memory_limit)) {
            if self.getid3.memory_limit > 0 and bytes / self.getid3.memory_limit > 0.99:
                raise php_new_class("getid3_exception", lambda : getid3_exception("cannot fread(" + bytes + " from " + self.ftell() + ") that is more than available PHP memory (" + self.getid3.memory_limit + ")", 10))
            # end if
            part = fread(self.getid3.fp, bytes)
            partLength = php_strlen(part)
            bytes -= partLength
            contents += part
            
            if bytes > 0 and partLength > 0:
                break
            # end if
        # end while
        return contents
    # end def fread
    #// 
    #// @param int $bytes
    #// @param int $whence
    #// 
    #// @return int
    #// 
    #// @throws getid3_exception
    #//
    def fseek(self, bytes=None, whence=SEEK_SET):
        
        if self.data_string_flag:
            for case in Switch(whence):
                if case(SEEK_SET):
                    self.data_string_position = bytes
                    break
                # end if
                if case(SEEK_CUR):
                    self.data_string_position += bytes
                    break
                # end if
                if case(SEEK_END):
                    self.data_string_position = self.data_string_length + bytes
                    break
                # end if
            # end for
            return 0
        else:
            pos = bytes
            if whence == SEEK_CUR:
                pos = self.ftell() + bytes
            elif whence == SEEK_END:
                pos = self.getid3.info["filesize"] + bytes
            # end if
            if (not getid3_lib.intvaluesupported(pos)):
                raise php_new_class("getid3_exception", lambda : getid3_exception("cannot fseek(" + pos + ") because beyond PHP filesystem limit", 10))
            # end if
        # end if
        return fseek(self.getid3.fp, bytes, whence)
    # end def fseek
    #// 
    #// @return bool
    #//
    def feof(self):
        
        if self.data_string_flag:
            return self.data_string_position >= self.data_string_length
        # end if
        return php_feof(self.getid3.fp)
    # end def feof
    #// 
    #// @param string $module
    #// 
    #// @return bool
    #//
    def isdependencyfor(self, module=None):
        
        return self.dependency_to == module
    # end def isdependencyfor
    #// 
    #// @param string $text
    #// 
    #// @return bool
    #//
    def error(self, text=None):
        
        self.getid3.info["error"][-1] = text
        return False
    # end def error
    #// 
    #// @param string $text
    #// 
    #// @return bool
    #//
    def warning(self, text=None):
        
        return self.getid3.warning(text)
    # end def warning
    #// 
    #// @param string $text
    #//
    def notice(self, text=None):
        
        pass
    # end def notice
    #// 
    #// @param string $name
    #// @param int    $offset
    #// @param int    $length
    #// @param string $image_mime
    #// 
    #// @return string|null
    #// 
    #// @throws Exception
    #// @throws getid3_exception
    #//
    def saveattachment(self, name=None, offset=None, length=None, image_mime=None):
        
        try: 
            #// do not extract at all
            if self.getid3.option_save_attachments == getID3.ATTACHMENTS_NONE:
                attachment = None
                pass
            elif self.getid3.option_save_attachments == getID3.ATTACHMENTS_INLINE:
                self.fseek(offset)
                attachment = self.fread(length)
                #// get whole data in one pass, till it is anyway stored in memory
                if attachment == False or php_strlen(attachment) != length:
                    raise php_new_class("Exception", lambda : Exception("failed to read attachment data"))
                # end if
                pass
            else:
                #// set up destination path
                dir = php_rtrim(php_str_replace(Array("/", "\\"), DIRECTORY_SEPARATOR, self.getid3.option_save_attachments), DIRECTORY_SEPARATOR)
                if (not php_is_dir(dir)) or (not getID3.is_writable(dir)):
                    raise php_new_class("Exception", lambda : Exception("supplied path (" + dir + ") does not exist, or is not writable"))
                # end if
                dest = dir + DIRECTORY_SEPARATOR + name + "." + getid3_lib.imageextfrommime(image_mime) if image_mime else ""
                #// create dest file
                fp_dest = fopen(dest, "wb")
                if fp_dest == False:
                    raise php_new_class("Exception", lambda : Exception("failed to create file " + dest))
                # end if
                #// copy data
                self.fseek(offset)
                buffersize = length if self.data_string_flag else self.getid3.fread_buffer_size()
                bytesleft = length
                while True:
                    
                    if not (bytesleft > 0):
                        break
                    # end if
                    buffer = self.fread(php_min(buffersize, bytesleft))
                    byteswritten = fwrite(fp_dest, buffer)
                    if buffer == False or byteswritten == False or byteswritten == 0:
                        raise php_new_class("Exception", lambda : Exception("not enough data to read" if buffer == False else "failed to write to destination file, may be not enough disk space"))
                    # end if
                    bytesleft -= byteswritten
                # end while
                php_fclose(fp_dest)
                attachment = dest
            # end if
        except Exception as e:
            #// close and remove dest file if created
            if (php_isset(lambda : fp_dest)) and is_resource(fp_dest):
                php_fclose(fp_dest)
            # end if
            if (php_isset(lambda : dest)) and php_file_exists(dest):
                unlink(dest)
            # end if
            #// do not set any is case of error
            attachment = None
            self.warning("Failed to extract attachment " + name + ": " + e.getmessage())
        # end try
        #// seek to the end of attachment
        self.fseek(offset + length)
        return attachment
    # end def saveattachment
# end class getid3_handler
class getid3_exception(Exception):
    message = Array()
# end class getid3_exception
