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
#// module.audio-video.matriska.php
#// module for analyzing Matroska containers
#// dependencies: NONE
#// 
#//
php_define("EBML_ID_CHAPTERS", 4433776)
#// [10][43][A7][70] -- A system to define basic menus and partition data. For more detailed information, look at the Chapters Explanation.
php_define("EBML_ID_SEEKHEAD", 21863284)
#// [11][4D][9B][74] -- Contains the position of other level 1 elements.
php_define("EBML_ID_TAGS", 39109479)
#// [12][54][C3][67] -- Element containing elements specific to Tracks/Chapters. A list of valid tags can be found <http://www.matroska.org/technical/specs/tagging/index.html>.
php_define("EBML_ID_INFO", 88713574)
#// [15][49][A9][66] -- Contains miscellaneous general information and statistics on the file.
php_define("EBML_ID_TRACKS", 106212971)
#// [16][54][AE][6B] -- A top-level block of information with many tracks described.
php_define("EBML_ID_SEGMENT", 139690087)
#// [18][53][80][67] -- This element contains all other top-level (level 1) elements. Typically a Matroska file is composed of 1 segment.
php_define("EBML_ID_ATTACHMENTS", 155296873)
#// [19][41][A4][69] -- Contain attached files.
php_define("EBML_ID_EBML", 172351395)
#// [1A][45][DF][A3] -- Set the EBML characteristics of the data to follow. Each EBML document has to start with this.
php_define("EBML_ID_CUES", 206814059)
#// [1C][53][BB][6B] -- A top-level element to speed seeking access. All entries are local to the segment.
php_define("EBML_ID_CLUSTER", 256095861)
#// [1F][43][B6][75] -- The lower level element containing the (monolithic) Block structure.
php_define("EBML_ID_LANGUAGE", 177564)
#// [22][B5][9C] -- Specifies the language of the track in the Matroska languages form.
php_define("EBML_ID_TRACKTIMECODESCALE", 209231)
#// [23][31][4F] -- The scale to apply on this track to work at normal speed in relation with other tracks (mostly used to adjust video speed when the audio length differs).
php_define("EBML_ID_DEFAULTDURATION", 254851)
#// [23][E3][83] -- Number of nanoseconds (i.e. not scaled) per frame.
php_define("EBML_ID_CODECNAME", 362120)
#// [25][86][88] -- A human-readable string specifying the codec.
php_define("EBML_ID_CODECDOWNLOADURL", 438848)
#// [26][B2][40] -- A URL to download about the codec used.
php_define("EBML_ID_TIMECODESCALE", 710577)
#// [2A][D7][B1] -- Timecode scale in nanoseconds (1.000.000 means all timecodes in the segment are expressed in milliseconds).
php_define("EBML_ID_COLOURSPACE", 963876)
#// [2E][B5][24] -- Same value as in AVI (32 bits).
php_define("EBML_ID_GAMMAVALUE", 1029411)
#// [2F][B5][23] -- Gamma Value.
php_define("EBML_ID_CODECSETTINGS", 1742487)
#// [3A][96][97] -- A string describing the encoding setting used.
php_define("EBML_ID_CODECINFOURL", 1785920)
#// [3B][40][40] -- A URL to find information about the codec used.
php_define("EBML_ID_PREVFILENAME", 1868715)
#// [3C][83][AB] -- An escaped filename corresponding to the previous segment.
php_define("EBML_ID_PREVUID", 1882403)
#// [3C][B9][23] -- A unique ID to identify the previous chained segment (128 bits).
php_define("EBML_ID_NEXTFILENAME", 1999803)
#// [3E][83][BB] -- An escaped filename corresponding to the next segment.
php_define("EBML_ID_NEXTUID", 2013475)
#// [3E][B9][23] -- A unique ID to identify the next chained segment (128 bits).
php_define("EBML_ID_CONTENTCOMPALGO", 596)
#// [42][54] -- The compression algorithm used. Algorithms that have been specified so far are:
php_define("EBML_ID_CONTENTCOMPSETTINGS", 597)
#// [42][55] -- Settings that might be needed by the decompressor. For Header Stripping (ContentCompAlgo=3), the bytes that were removed from the beggining of each frames of the track.
php_define("EBML_ID_DOCTYPE", 642)
#// [42][82] -- A string that describes the type of document that follows this EBML header ('matroska' in our case).
php_define("EBML_ID_DOCTYPEREADVERSION", 645)
#// [42][85] -- The minimum DocType version an interpreter has to support to read this file.
php_define("EBML_ID_EBMLVERSION", 646)
#// [42][86] -- The version of EBML parser used to create the file.
php_define("EBML_ID_DOCTYPEVERSION", 647)
#// [42][87] -- The version of DocType interpreter used to create the file.
php_define("EBML_ID_EBMLMAXIDLENGTH", 754)
#// [42][F2] -- The maximum length of the IDs you'll find in this file (4 or less in Matroska).
php_define("EBML_ID_EBMLMAXSIZELENGTH", 755)
#// [42][F3] -- The maximum length of the sizes you'll find in this file (8 or less in Matroska). This does not override the element size indicated at the beginning of an element. Elements that have an indicated size which is larger than what is allowed by EBMLMaxSizeLength shall be considered invalid.
php_define("EBML_ID_EBMLREADVERSION", 759)
#// [42][F7] -- The minimum EBML version a parser has to support to read this file.
php_define("EBML_ID_CHAPLANGUAGE", 892)
#// [43][7C] -- The languages corresponding to the string, in the bibliographic ISO-639-2 form.
php_define("EBML_ID_CHAPCOUNTRY", 894)
#// [43][7E] -- The countries corresponding to the string, same 2 octets as in Internet domains.
php_define("EBML_ID_SEGMENTFAMILY", 1092)
#// [44][44] -- A randomly generated unique ID that all segments related to each other must use (128 bits).
php_define("EBML_ID_DATEUTC", 1121)
#// [44][61] -- Date of the origin of timecode (value 0), i.e. production date.
php_define("EBML_ID_TAGLANGUAGE", 1146)
#// [44][7A] -- Specifies the language of the tag specified, in the Matroska languages form.
php_define("EBML_ID_TAGDEFAULT", 1156)
#// [44][84] -- Indication to know if this is the default/original language to use for the given tag.
php_define("EBML_ID_TAGBINARY", 1157)
#// [44][85] -- The values of the Tag if it is binary. Note that this cannot be used in the same SimpleTag as TagString.
php_define("EBML_ID_TAGSTRING", 1159)
#// [44][87] -- The value of the Tag.
php_define("EBML_ID_DURATION", 1161)
#// [44][89] -- Duration of the segment (based on TimecodeScale).
php_define("EBML_ID_CHAPPROCESSPRIVATE", 1293)
#// [45][0D] -- Some optional data attached to the ChapProcessCodecID information. For ChapProcessCodecID = 1, it is the "DVD level" equivalent.
php_define("EBML_ID_CHAPTERFLAGENABLED", 1432)
#// [45][98] -- Specify wether the chapter is enabled. It can be enabled/disabled by a Control Track. When disabled, the movie should skip all the content between the TimeStart and TimeEnd of this chapter.
php_define("EBML_ID_TAGNAME", 1443)
#// [45][A3] -- The name of the Tag that is going to be stored.
php_define("EBML_ID_EDITIONENTRY", 1465)
#// [45][B9] -- Contains all information about a segment edition.
php_define("EBML_ID_EDITIONUID", 1468)
#// [45][BC] -- A unique ID to identify the edition. It's useful for tagging an edition.
php_define("EBML_ID_EDITIONFLAGHIDDEN", 1469)
#// [45][BD] -- If an edition is hidden (1), it should not be available to the user interface (but still to Control Tracks).
php_define("EBML_ID_EDITIONFLAGDEFAULT", 1499)
#// [45][DB] -- If a flag is set (1) the edition should be used as the default one.
php_define("EBML_ID_EDITIONFLAGORDERED", 1501)
#// [45][DD] -- Specify if the chapters can be defined multiple times and the order to play them is enforced.
php_define("EBML_ID_FILEDATA", 1628)
#// [46][5C] -- The data of the file.
php_define("EBML_ID_FILEMIMETYPE", 1632)
#// [46][60] -- MIME type of the file.
php_define("EBML_ID_FILENAME", 1646)
#// [46][6E] -- Filename of the attached file.
php_define("EBML_ID_FILEREFERRAL", 1653)
#// [46][75] -- A binary value that a track/codec can refer to when the attachment is needed.
php_define("EBML_ID_FILEDESCRIPTION", 1662)
#// [46][7E] -- A human-friendly name for the attached file.
php_define("EBML_ID_FILEUID", 1710)
#// [46][AE] -- Unique ID representing the file, as random as possible.
php_define("EBML_ID_CONTENTENCALGO", 2017)
#// [47][E1] -- The encryption algorithm used. The value '0' means that the contents have not been encrypted but only signed. Predefined values:
php_define("EBML_ID_CONTENTENCKEYID", 2018)
#// [47][E2] -- For public key algorithms this is the ID of the public key the data was encrypted with.
php_define("EBML_ID_CONTENTSIGNATURE", 2019)
#// [47][E3] -- A cryptographic signature of the contents.
php_define("EBML_ID_CONTENTSIGKEYID", 2020)
#// [47][E4] -- This is the ID of the private key the data was signed with.
php_define("EBML_ID_CONTENTSIGALGO", 2021)
#// [47][E5] -- The algorithm used for the signature. A value of '0' means that the contents have not been signed but only encrypted. Predefined values:
php_define("EBML_ID_CONTENTSIGHASHALGO", 2022)
#// [47][E6] -- The hash algorithm used for the signature. A value of '0' means that the contents have not been signed but only encrypted. Predefined values:
php_define("EBML_ID_MUXINGAPP", 3456)
#// [4D][80] -- Muxing application or library ("libmatroska-0.4.3").
php_define("EBML_ID_SEEK", 3515)
#// [4D][BB] -- Contains a single seek entry to an EBML element.
php_define("EBML_ID_CONTENTENCODINGORDER", 4145)
#// [50][31] -- Tells when this modification was used during encoding/muxing starting with 0 and counting upwards. The decoder/demuxer has to start with the highest order number it finds and work its way down. This value has to be unique over all ContentEncodingOrder elements in the segment.
php_define("EBML_ID_CONTENTENCODINGSCOPE", 4146)
#// [50][32] -- A bit field that describes which elements have been modified in this way. Values (big endian) can be OR'ed. Possible values:
php_define("EBML_ID_CONTENTENCODINGTYPE", 4147)
#// [50][33] -- A value describing what kind of transformation has been done. Possible values:
php_define("EBML_ID_CONTENTCOMPRESSION", 4148)
#// [50][34] -- Settings describing the compression used. Must be present if the value of ContentEncodingType is 0 and absent otherwise. Each block must be decompressable even if no previous block is available in order not to prevent seeking.
php_define("EBML_ID_CONTENTENCRYPTION", 4149)
#// [50][35] -- Settings describing the encryption used. Must be present if the value of ContentEncodingType is 1 and absent otherwise.
php_define("EBML_ID_CUEREFNUMBER", 4959)
#// [53][5F] -- Number of the referenced Block of Track X in the specified Cluster.
php_define("EBML_ID_NAME", 4974)
#// [53][6E] -- A human-readable track name.
php_define("EBML_ID_CUEBLOCKNUMBER", 4984)
#// [53][78] -- Number of the Block in the specified Cluster.
php_define("EBML_ID_TRACKOFFSET", 4991)
#// [53][7F] -- A value to add to the Block's Timecode. This can be used to adjust the playback offset of a track.
php_define("EBML_ID_SEEKID", 5035)
#// [53][AB] -- The binary ID corresponding to the element name.
php_define("EBML_ID_SEEKPOSITION", 5036)
#// [53][AC] -- The position of the element in the segment in octets (0 = first level 1 element).
php_define("EBML_ID_STEREOMODE", 5048)
#// [53][B8] -- Stereo-3D video mode.
php_define("EBML_ID_OLDSTEREOMODE", 5049)
#// [53][B9] -- Bogus StereoMode value used in old versions of libmatroska. DO NOT USE. (0: mono, 1: right eye, 2: left eye, 3: both eyes).
php_define("EBML_ID_PIXELCROPBOTTOM", 5290)
#// [54][AA] -- The number of video pixels to remove at the bottom of the image (for HDTV content).
php_define("EBML_ID_DISPLAYWIDTH", 5296)
#// [54][B0] -- Width of the video frames to display.
php_define("EBML_ID_DISPLAYUNIT", 5298)
#// [54][B2] -- Type of the unit for DisplayWidth/Height (0: pixels, 1: centimeters, 2: inches).
php_define("EBML_ID_ASPECTRATIOTYPE", 5299)
#// [54][B3] -- Specify the possible modifications to the aspect ratio (0: free resizing, 1: keep aspect ratio, 2: fixed).
php_define("EBML_ID_DISPLAYHEIGHT", 5306)
#// [54][BA] -- Height of the video frames to display.
php_define("EBML_ID_PIXELCROPTOP", 5307)
#// [54][BB] -- The number of video pixels to remove at the top of the image.
php_define("EBML_ID_PIXELCROPLEFT", 5324)
#// [54][CC] -- The number of video pixels to remove on the left of the image.
php_define("EBML_ID_PIXELCROPRIGHT", 5341)
#// [54][DD] -- The number of video pixels to remove on the right of the image.
php_define("EBML_ID_FLAGFORCED", 5546)
#// [55][AA] -- Set if that track MUST be used during playback. There can be many forced track for a kind (audio, video or subs), the player should select the one which language matches the user preference or the default + forced track. Overlay MAY happen between a forced and non-forced track of the same kind.
php_define("EBML_ID_MAXBLOCKADDITIONID", 5614)
#// [55][EE] -- The maximum value of BlockAddID. A value 0 means there is no BlockAdditions for this track.
php_define("EBML_ID_WRITINGAPP", 5953)
#// [57][41] -- Writing application ("mkvmerge-0.3.3").
php_define("EBML_ID_CLUSTERSILENTTRACKS", 6228)
#// [58][54] -- The list of tracks that are not used in that part of the stream. It is useful when using overlay tracks on seeking. Then you should decide what track to use.
php_define("EBML_ID_CLUSTERSILENTTRACKNUMBER", 6359)
#// [58][D7] -- One of the track number that are not used from now on in the stream. It could change later if not specified as silent in a further Cluster.
php_define("EBML_ID_ATTACHEDFILE", 8615)
#// [61][A7] -- An attached file.
php_define("EBML_ID_CONTENTENCODING", 8768)
#// [62][40] -- Settings for one content encoding like compression or encryption.
php_define("EBML_ID_BITDEPTH", 8804)
#// [62][64] -- Bits per sample, mostly used for PCM.
php_define("EBML_ID_CODECPRIVATE", 9122)
#// [63][A2] -- Private data only known to the codec.
php_define("EBML_ID_TARGETS", 9152)
#// [63][C0] -- Contain all UIDs where the specified meta data apply. It is void to describe everything in the segment.
php_define("EBML_ID_CHAPTERPHYSICALEQUIV", 9155)
#// [63][C3] -- Specify the physical equivalent of this ChapterAtom like "DVD" (60) or "SIDE" (50), see complete list of values.
php_define("EBML_ID_TAGCHAPTERUID", 9156)
#// [63][C4] -- A unique ID to identify the Chapter(s) the tags belong to. If the value is 0 at this level, the tags apply to all chapters in the Segment.
php_define("EBML_ID_TAGTRACKUID", 9157)
#// [63][C5] -- A unique ID to identify the Track(s) the tags belong to. If the value is 0 at this level, the tags apply to all tracks in the Segment.
php_define("EBML_ID_TAGATTACHMENTUID", 9158)
#// [63][C6] -- A unique ID to identify the Attachment(s) the tags belong to. If the value is 0 at this level, the tags apply to all the attachments in the Segment.
php_define("EBML_ID_TAGEDITIONUID", 9161)
#// [63][C9] -- A unique ID to identify the EditionEntry(s) the tags belong to. If the value is 0 at this level, the tags apply to all editions in the Segment.
php_define("EBML_ID_TARGETTYPE", 9162)
#// [63][CA] -- An informational string that can be used to display the logical level of the target like "ALBUM", "TRACK", "MOVIE", "CHAPTER", etc (see TargetType).
php_define("EBML_ID_TRACKTRANSLATE", 9764)
#// [66][24] -- The track identification for the given Chapter Codec.
php_define("EBML_ID_TRACKTRANSLATETRACKID", 9893)
#// [66][A5] -- The binary value used to represent this track in the chapter codec data. The format depends on the ChapProcessCodecID used.
php_define("EBML_ID_TRACKTRANSLATECODEC", 9919)
#// [66][BF] -- The chapter codec using this ID (0: Matroska Script, 1: DVD-menu).
php_define("EBML_ID_TRACKTRANSLATEEDITIONUID", 9980)
#// [66][FC] -- Specify an edition UID on which this translation applies. When not specified, it means for all editions found in the segment.
php_define("EBML_ID_SIMPLETAG", 10184)
#// [67][C8] -- Contains general information about the target.
php_define("EBML_ID_TARGETTYPEVALUE", 10442)
#// [68][CA] -- A number to indicate the logical level of the target (see TargetType).
php_define("EBML_ID_CHAPPROCESSCOMMAND", 10513)
#// [69][11] -- Contains all the commands associated to the Atom.
php_define("EBML_ID_CHAPPROCESSTIME", 10530)
#// [69][22] -- Defines when the process command should be handled (0: during the whole chapter, 1: before starting playback, 2: after playback of the chapter).
php_define("EBML_ID_CHAPTERTRANSLATE", 10532)
#// [69][24] -- A tuple of corresponding ID used by chapter codecs to represent this segment.
php_define("EBML_ID_CHAPPROCESSDATA", 10547)
#// [69][33] -- Contains the command information. The data should be interpreted depending on the ChapProcessCodecID value. For ChapProcessCodecID = 1, the data correspond to the binary DVD cell pre/post commands.
php_define("EBML_ID_CHAPPROCESS", 10564)
#// [69][44] -- Contains all the commands associated to the Atom.
php_define("EBML_ID_CHAPPROCESSCODECID", 10581)
#// [69][55] -- Contains the type of the codec used for the processing. A value of 0 means native Matroska processing (to be defined), a value of 1 means the DVD command set is used. More codec IDs can be added later.
php_define("EBML_ID_CHAPTERTRANSLATEID", 10661)
#// [69][A5] -- The binary value used to represent this segment in the chapter codec data. The format depends on the ChapProcessCodecID used.
php_define("EBML_ID_CHAPTERTRANSLATECODEC", 10687)
#// [69][BF] -- The chapter codec using this ID (0: Matroska Script, 1: DVD-menu).
php_define("EBML_ID_CHAPTERTRANSLATEEDITIONUID", 10748)
#// [69][FC] -- Specify an edition UID on which this correspondance applies. When not specified, it means for all editions found in the segment.
php_define("EBML_ID_CONTENTENCODINGS", 11648)
#// [6D][80] -- Settings for several content encoding mechanisms like compression or encryption.
php_define("EBML_ID_MINCACHE", 11751)
#// [6D][E7] -- The minimum number of frames a player should be able to cache during playback. If set to 0, the reference pseudo-cache system is not used.
php_define("EBML_ID_MAXCACHE", 11768)
#// [6D][F8] -- The maximum cache size required to store referenced frames in and the current frame. 0 means no cache is needed.
php_define("EBML_ID_CHAPTERSEGMENTUID", 11879)
#// [6E][67] -- A segment to play in place of this chapter. Edition ChapterSegmentEditionUID should be used for this segment, otherwise no edition is used.
php_define("EBML_ID_CHAPTERSEGMENTEDITIONUID", 11964)
#// [6E][BC] -- The edition to play from the segment linked in ChapterSegmentUID.
php_define("EBML_ID_TRACKOVERLAY", 12203)
#// [6F][AB] -- Specify that this track is an overlay track for the Track specified (in the u-integer). That means when this track has a gap (see SilentTracks) the overlay track should be used instead. The order of multiple TrackOverlay matters, the first one is the one that should be used. If not found it should be the second, etc.
php_define("EBML_ID_TAG", 13171)
#// [73][73] -- Element containing elements specific to Tracks/Chapters.
php_define("EBML_ID_SEGMENTFILENAME", 13188)
#// [73][84] -- A filename corresponding to this segment.
php_define("EBML_ID_SEGMENTUID", 13220)
#// [73][A4] -- A randomly generated unique ID to identify the current segment between many others (128 bits).
php_define("EBML_ID_CHAPTERUID", 13252)
#// [73][C4] -- A unique ID to identify the Chapter.
php_define("EBML_ID_TRACKUID", 13253)
#// [73][C5] -- A unique ID to identify the Track. This should be kept the same when making a direct stream copy of the Track to another file.
php_define("EBML_ID_ATTACHMENTLINK", 13382)
#// [74][46] -- The UID of an attachment that is used by this codec.
php_define("EBML_ID_CLUSTERBLOCKADDITIONS", 13729)
#// [75][A1] -- Contain additional blocks to complete the main one. An EBML parser that has no knowledge of the Block structure could still see and use/skip these data.
php_define("EBML_ID_CHANNELPOSITIONS", 13435)
#// [7D][7B] -- Table of horizontal angles for each successive channel, see appendix.
php_define("EBML_ID_OUTPUTSAMPLINGFREQUENCY", 14517)
#// [78][B5] -- Real output sampling frequency in Hz (used for SBR techniques).
php_define("EBML_ID_TITLE", 15273)
#// [7B][A9] -- General name of the segment.
php_define("EBML_ID_CHAPTERDISPLAY", 0)
#// [80] -- Contains all possible strings to use for the chapter display.
php_define("EBML_ID_TRACKTYPE", 3)
#// [83] -- A set of track types coded on 8 bits (1: video, 2: audio, 3: complex, 0x10: logo, 0x11: subtitle, 0x12: buttons, 0x20: control).
php_define("EBML_ID_CHAPSTRING", 5)
#// [85] -- Contains the string to use as the chapter atom.
php_define("EBML_ID_CODECID", 6)
#// [86] -- An ID corresponding to the codec, see the codec page for more info.
php_define("EBML_ID_FLAGDEFAULT", 8)
#// [88] -- Set if that track (audio, video or subs) SHOULD be used if no language found matches the user preference.
php_define("EBML_ID_CHAPTERTRACKNUMBER", 9)
#// [89] -- UID of the Track to apply this chapter too. In the absense of a control track, choosing this chapter will select the listed Tracks and deselect unlisted tracks. Absense of this element indicates that the Chapter should be applied to any currently used Tracks.
php_define("EBML_ID_CLUSTERSLICES", 14)
#// [8E] -- Contains slices description.
php_define("EBML_ID_CHAPTERTRACK", 15)
#// [8F] -- List of tracks on which the chapter applies. If this element is not present, all tracks apply
php_define("EBML_ID_CHAPTERTIMESTART", 17)
#// [91] -- Timecode of the start of Chapter (not scaled).
php_define("EBML_ID_CHAPTERTIMEEND", 18)
#// [92] -- Timecode of the end of Chapter (timecode excluded, not scaled).
php_define("EBML_ID_CUEREFTIME", 22)
#// [96] -- Timecode of the referenced Block.
php_define("EBML_ID_CUEREFCLUSTER", 23)
#// [97] -- Position of the Cluster containing the referenced Block.
php_define("EBML_ID_CHAPTERFLAGHIDDEN", 24)
#// [98] -- If a chapter is hidden (1), it should not be available to the user interface (but still to Control Tracks).
php_define("EBML_ID_FLAGINTERLACED", 26)
#// [9A] -- Set if the video is interlaced.
php_define("EBML_ID_CLUSTERBLOCKDURATION", 27)
#// [9B] -- The duration of the Block (based on TimecodeScale). This element is mandatory when DefaultDuration is set for the track. When not written and with no DefaultDuration, the value is assumed to be the difference between the timecode of this Block and the timecode of the next Block in "display" order (not coding order). This element can be useful at the end of a Track (as there is not other Block available), or when there is a break in a track like for subtitle tracks.
php_define("EBML_ID_FLAGLACING", 28)
#// [9C] -- Set if the track may contain blocks using lacing.
php_define("EBML_ID_CHANNELS", 31)
#// [9F] -- Numbers of channels in the track.
php_define("EBML_ID_CLUSTERBLOCKGROUP", 32)
#// [A0] -- Basic container of information containing a single Block or BlockVirtual, and information specific to that Block/VirtualBlock.
php_define("EBML_ID_CLUSTERBLOCK", 33)
#// [A1] -- Block containing the actual data to be rendered and a timecode relative to the Cluster Timecode.
php_define("EBML_ID_CLUSTERBLOCKVIRTUAL", 34)
#// [A2] -- A Block with no data. It must be stored in the stream at the place the real Block should be in display order.
php_define("EBML_ID_CLUSTERSIMPLEBLOCK", 35)
#// [A3] -- Similar to Block but without all the extra information, mostly used to reduced overhead when no extra feature is needed.
php_define("EBML_ID_CLUSTERCODECSTATE", 36)
#// [A4] -- The new codec state to use. Data interpretation is private to the codec. This information should always be referenced by a seek entry.
php_define("EBML_ID_CLUSTERBLOCKADDITIONAL", 37)
#// [A5] -- Interpreted by the codec as it wishes (using the BlockAddID).
php_define("EBML_ID_CLUSTERBLOCKMORE", 38)
#// [A6] -- Contain the BlockAdditional and some parameters.
php_define("EBML_ID_CLUSTERPOSITION", 39)
#// [A7] -- Position of the Cluster in the segment (0 in live broadcast streams). It might help to resynchronise offset on damaged streams.
php_define("EBML_ID_CODECDECODEALL", 42)
#// [AA] -- The codec can decode potentially damaged data.
php_define("EBML_ID_CLUSTERPREVSIZE", 43)
#// [AB] -- Size of the previous Cluster, in octets. Can be useful for backward playing.
php_define("EBML_ID_TRACKENTRY", 46)
#// [AE] -- Describes a track with all elements.
php_define("EBML_ID_CLUSTERENCRYPTEDBLOCK", 47)
#// [AF] -- Similar to SimpleBlock but the data inside the Block are Transformed (encrypt and/or signed).
php_define("EBML_ID_PIXELWIDTH", 48)
#// [B0] -- Width of the encoded video frames in pixels.
php_define("EBML_ID_CUETIME", 51)
#// [B3] -- Absolute timecode according to the segment time base.
php_define("EBML_ID_SAMPLINGFREQUENCY", 53)
#// [B5] -- Sampling frequency in Hz.
php_define("EBML_ID_CHAPTERATOM", 54)
#// [B6] -- Contains the atom information to use as the chapter atom (apply to all tracks).
php_define("EBML_ID_CUETRACKPOSITIONS", 55)
#// [B7] -- Contain positions for different tracks corresponding to the timecode.
php_define("EBML_ID_FLAGENABLED", 57)
#// [B9] -- Set if the track is used.
php_define("EBML_ID_PIXELHEIGHT", 58)
#// [BA] -- Height of the encoded video frames in pixels.
php_define("EBML_ID_CUEPOINT", 59)
#// [BB] -- Contains all information relative to a seek point in the segment.
php_define("EBML_ID_CRC32", 63)
#// [BF] -- The CRC is computed on all the data of the Master element it's in, regardless of its position. It's recommended to put the CRC value at the beggining of the Master element for easier reading. All level 1 elements should include a CRC-32.
php_define("EBML_ID_CLUSTERBLOCKADDITIONID", 75)
#// [CB] -- The ID of the BlockAdditional element (0 is the main Block).
php_define("EBML_ID_CLUSTERLACENUMBER", 76)
#// [CC] -- The reverse number of the frame in the lace (0 is the last frame, 1 is the next to last, etc). While there are a few files in the wild with this element, it is no longer in use and has been deprecated. Being able to interpret this element is not required for playback.
php_define("EBML_ID_CLUSTERFRAMENUMBER", 77)
#// [CD] -- The number of the frame to generate from this lace with this delay (allow you to generate many frames from the same Block/Frame).
php_define("EBML_ID_CLUSTERDELAY", 78)
#// [CE] -- The (scaled) delay to apply to the element.
php_define("EBML_ID_CLUSTERDURATION", 79)
#// [CF] -- The (scaled) duration to apply to the element.
php_define("EBML_ID_TRACKNUMBER", 87)
#// [D7] -- The track number as used in the Block Header (using more than 127 tracks is not encouraged, though the design allows an unlimited number).
php_define("EBML_ID_CUEREFERENCE", 91)
#// [DB] -- The Clusters containing the required referenced Blocks.
php_define("EBML_ID_VIDEO", 96)
#// [E0] -- Video settings.
php_define("EBML_ID_AUDIO", 97)
#// [E1] -- Audio settings.
php_define("EBML_ID_CLUSTERTIMESLICE", 104)
#// [E8] -- Contains extra time information about the data contained in the Block. While there are a few files in the wild with this element, it is no longer in use and has been deprecated. Being able to interpret this element is not required for playback.
php_define("EBML_ID_CUECODECSTATE", 106)
#// [EA] -- The position of the Codec State corresponding to this Cue element. 0 means that the data is taken from the initial Track Entry.
php_define("EBML_ID_CUEREFCODECSTATE", 107)
#// [EB] -- The position of the Codec State corresponding to this referenced element. 0 means that the data is taken from the initial Track Entry.
php_define("EBML_ID_VOID", 108)
#// [EC] -- Used to void damaged data, to avoid unexpected behaviors when using damaged data. The content is discarded. Also used to reserve space in a sub-element for later use.
php_define("EBML_ID_CLUSTERTIMECODE", 103)
#// [E7] -- Absolute timecode of the cluster (based on TimecodeScale).
php_define("EBML_ID_CLUSTERBLOCKADDID", 110)
#// [EE] -- An ID to identify the BlockAdditional level.
php_define("EBML_ID_CUECLUSTERPOSITION", 113)
#// [F1] -- The position of the Cluster containing the required Block.
php_define("EBML_ID_CUETRACK", 119)
#// [F7] -- The track for which a position is given.
php_define("EBML_ID_CLUSTERREFERENCEPRIORITY", 122)
#// [FA] -- This frame is referenced and has the specified cache priority. In cache only a frame of the same or higher priority can replace this frame. A value of 0 means the frame is not referenced.
php_define("EBML_ID_CLUSTERREFERENCEBLOCK", 123)
#// [FB] -- Timecode of another frame used as a reference (ie: B or P frame). The timecode is relative to the block it's attached to.
php_define("EBML_ID_CLUSTERREFERENCEVIRTUAL", 125)
#// [FD] -- Relative position of the data that should be in position of the virtual block.
#// 
#// @tutorial http://www.matroska.org/technical/specs/index.html
#// 
#// @todo Rewrite EBML parser to reduce it's size and honor default element values
#// @todo After rewrite implement stream size calculation, that will provide additional useful info and enable AAC/FLAC audio bitrate detection
#//
class getid3_matroska(getid3_handler):
    hide_clusters = True
    parse_whole_file = False
    EBMLbuffer = ""
    EBMLbuffer_offset = 0
    EBMLbuffer_length = 0
    current_offset = 0
    unuseful_elements = Array(EBML_ID_CRC32, EBML_ID_VOID)
    #// 
    #// @return bool
    #//
    def analyze(self):
        
        info = self.getid3.info
        #// parse container
        try: 
            self.parseebml(info)
        except Exception as e:
            self.error("EBML parser: " + e.getmessage())
        # end try
        #// calculate playtime
        if (php_isset(lambda : info["matroska"]["info"])) and php_is_array(info["matroska"]["info"]):
            for key,infoarray in info["matroska"]["info"]:
                if (php_isset(lambda : infoarray["Duration"])):
                    #// TimecodeScale is how many nanoseconds each Duration unit is
                    info["playtime_seconds"] = infoarray["Duration"] * infoarray["TimecodeScale"] if (php_isset(lambda : infoarray["TimecodeScale"])) else 1000000 / 1000000000
                    break
                # end if
            # end for
        # end if
        #// extract tags
        if (php_isset(lambda : info["matroska"]["tags"])) and php_is_array(info["matroska"]["tags"]):
            for key,infoarray in info["matroska"]["tags"]:
                self.extractcommentssimpletag(infoarray)
            # end for
        # end if
        #// process tracks
        if (php_isset(lambda : info["matroska"]["tracks"]["tracks"])) and php_is_array(info["matroska"]["tracks"]["tracks"]):
            for key,trackarray in info["matroska"]["tracks"]["tracks"]:
                track_info = Array()
                track_info["dataformat"] = self.codecidtocommonname(trackarray["CodecID"])
                track_info["default"] = trackarray["FlagDefault"] if (php_isset(lambda : trackarray["FlagDefault"])) else True
                if (php_isset(lambda : trackarray["Name"])):
                    track_info["name"] = trackarray["Name"]
                # end if
                for case in Switch(trackarray["TrackType"]):
                    if case(1):
                        #// Video
                        track_info["resolution_x"] = trackarray["PixelWidth"]
                        track_info["resolution_y"] = trackarray["PixelHeight"]
                        track_info["display_unit"] = self.displayunit(trackarray["DisplayUnit"] if (php_isset(lambda : trackarray["DisplayUnit"])) else 0)
                        track_info["display_x"] = trackarray["DisplayWidth"] if (php_isset(lambda : trackarray["DisplayWidth"])) else trackarray["PixelWidth"]
                        track_info["display_y"] = trackarray["DisplayHeight"] if (php_isset(lambda : trackarray["DisplayHeight"])) else trackarray["PixelHeight"]
                        if (php_isset(lambda : trackarray["PixelCropBottom"])):
                            track_info["crop_bottom"] = trackarray["PixelCropBottom"]
                        # end if
                        if (php_isset(lambda : trackarray["PixelCropTop"])):
                            track_info["crop_top"] = trackarray["PixelCropTop"]
                        # end if
                        if (php_isset(lambda : trackarray["PixelCropLeft"])):
                            track_info["crop_left"] = trackarray["PixelCropLeft"]
                        # end if
                        if (php_isset(lambda : trackarray["PixelCropRight"])):
                            track_info["crop_right"] = trackarray["PixelCropRight"]
                        # end if
                        if (php_isset(lambda : trackarray["DefaultDuration"])):
                            track_info["frame_rate"] = round(1000000000 / trackarray["DefaultDuration"], 3)
                        # end if
                        if (php_isset(lambda : trackarray["CodecName"])):
                            track_info["codec"] = trackarray["CodecName"]
                        # end if
                        for case in Switch(trackarray["CodecID"]):
                            if case("V_MS/VFW/FOURCC"):
                                getid3_lib.includedependency(GETID3_INCLUDEPATH + "module.audio-video.riff.php", __FILE__, True)
                                parsed = getid3_riff.parsebitmapinfoheader(trackarray["CodecPrivate"])
                                track_info["codec"] = getid3_riff.fourcclookup(parsed["fourcc"])
                                info["matroska"]["track_codec_parsed"][trackarray["TrackNumber"]] = parsed
                                break
                            # end if
                        # end for
                        info["video"]["streams"][-1] = track_info
                        break
                    # end if
                    if case(2):
                        #// Audio
                        track_info["sample_rate"] = trackarray["SamplingFrequency"] if (php_isset(lambda : trackarray["SamplingFrequency"])) else 8000
                        track_info["channels"] = trackarray["Channels"] if (php_isset(lambda : trackarray["Channels"])) else 1
                        track_info["language"] = trackarray["Language"] if (php_isset(lambda : trackarray["Language"])) else "eng"
                        if (php_isset(lambda : trackarray["BitDepth"])):
                            track_info["bits_per_sample"] = trackarray["BitDepth"]
                        # end if
                        if (php_isset(lambda : trackarray["CodecName"])):
                            track_info["codec"] = trackarray["CodecName"]
                        # end if
                        for case in Switch(trackarray["CodecID"]):
                            if case("A_PCM/INT/LIT"):
                                pass
                            # end if
                            if case("A_PCM/INT/BIG"):
                                track_info["bitrate"] = track_info["sample_rate"] * track_info["channels"] * trackarray["BitDepth"]
                                break
                            # end if
                            if case("A_AC3"):
                                pass
                            # end if
                            if case("A_EAC3"):
                                pass
                            # end if
                            if case("A_DTS"):
                                pass
                            # end if
                            if case("A_MPEG/L3"):
                                pass
                            # end if
                            if case("A_MPEG/L2"):
                                pass
                            # end if
                            if case("A_FLAC"):
                                module_dataformat = "mp3" if track_info["dataformat"] == "mp2" else "ac3" if track_info["dataformat"] == "eac3" else track_info["dataformat"]
                                getid3_lib.includedependency(GETID3_INCLUDEPATH + "module.audio." + module_dataformat + ".php", __FILE__, True)
                                if (not (php_isset(lambda : info["matroska"]["track_data_offsets"][trackarray["TrackNumber"]]))):
                                    self.warning("Unable to parse audio data [" + php_basename(__FILE__) + ":" + 0 + "] because $info[matroska][track_data_offsets][" + trackarray["TrackNumber"] + "] not set")
                                    break
                                # end if
                                #// create temp instance
                                getid3_temp = php_new_class("getID3", lambda : getID3())
                                if track_info["dataformat"] != "flac":
                                    getid3_temp.openfile(self.getid3.filename)
                                # end if
                                getid3_temp.info["avdataoffset"] = info["matroska"]["track_data_offsets"][trackarray["TrackNumber"]]["offset"]
                                if track_info["dataformat"][0] == "m" or track_info["dataformat"] == "flac":
                                    getid3_temp.info["avdataend"] = info["matroska"]["track_data_offsets"][trackarray["TrackNumber"]]["offset"] + info["matroska"]["track_data_offsets"][trackarray["TrackNumber"]]["length"]
                                # end if
                                #// analyze
                                class_ = "getid3_" + module_dataformat
                                header_data_key = "mpeg" if track_info["dataformat"][0] == "m" else track_info["dataformat"]
                                getid3_audio = php_new_class(class_, lambda : {**locals(), **globals()}[class_](getid3_temp, __CLASS__))
                                if track_info["dataformat"] == "flac":
                                    getid3_audio.analyzestring(trackarray["CodecPrivate"])
                                else:
                                    getid3_audio.analyze()
                                # end if
                                if (not php_empty(lambda : getid3_temp.info[header_data_key])):
                                    info["matroska"]["track_codec_parsed"][trackarray["TrackNumber"]] = getid3_temp.info[header_data_key]
                                    if (php_isset(lambda : getid3_temp.info["audio"])) and php_is_array(getid3_temp.info["audio"]):
                                        for sub_key,value in getid3_temp.info["audio"]:
                                            track_info[sub_key] = value
                                        # end for
                                    # end if
                                else:
                                    self.warning("Unable to parse audio data [" + php_basename(__FILE__) + ":" + 0 + "] because " + class_ + "::Analyze() failed at offset " + getid3_temp.info["avdataoffset"])
                                # end if
                                #// copy errors and warnings
                                if (not php_empty(lambda : getid3_temp.info["error"])):
                                    for newerror in getid3_temp.info["error"]:
                                        self.warning(class_ + "() says: [" + newerror + "]")
                                    # end for
                                # end if
                                if (not php_empty(lambda : getid3_temp.info["warning"])):
                                    for newerror in getid3_temp.info["warning"]:
                                        self.warning(class_ + "() says: [" + newerror + "]")
                                    # end for
                                # end if
                                getid3_temp = None
                                getid3_audio = None
                                break
                            # end if
                            if case("A_AAC"):
                                pass
                            # end if
                            if case("A_AAC/MPEG2/LC"):
                                pass
                            # end if
                            if case("A_AAC/MPEG2/LC/SBR"):
                                pass
                            # end if
                            if case("A_AAC/MPEG4/LC"):
                                pass
                            # end if
                            if case("A_AAC/MPEG4/LC/SBR"):
                                self.warning(trackarray["CodecID"] + " audio data contains no header, audio/video bitrates can't be calculated")
                                break
                            # end if
                            if case("A_VORBIS"):
                                if (not (php_isset(lambda : trackarray["CodecPrivate"]))):
                                    self.warning("Unable to parse audio data [" + php_basename(__FILE__) + ":" + 0 + "] because CodecPrivate data not set")
                                    break
                                # end if
                                vorbis_offset = php_strpos(trackarray["CodecPrivate"], "vorbis", 1)
                                if vorbis_offset == False:
                                    self.warning("Unable to parse audio data [" + php_basename(__FILE__) + ":" + 0 + "] because CodecPrivate data does not contain \"vorbis\" keyword")
                                    break
                                # end if
                                vorbis_offset -= 1
                                getid3_lib.includedependency(GETID3_INCLUDEPATH + "module.audio.ogg.php", __FILE__, True)
                                #// create temp instance
                                getid3_temp = php_new_class("getID3", lambda : getID3())
                                #// analyze
                                getid3_ogg = php_new_class("getid3_ogg", lambda : getid3_ogg(getid3_temp))
                                oggpageinfo["page_seqno"] = 0
                                getid3_ogg.parsevorbispageheader(trackarray["CodecPrivate"], vorbis_offset, oggpageinfo)
                                if (not php_empty(lambda : getid3_temp.info["ogg"])):
                                    info["matroska"]["track_codec_parsed"][trackarray["TrackNumber"]] = getid3_temp.info["ogg"]
                                    if (php_isset(lambda : getid3_temp.info["audio"])) and php_is_array(getid3_temp.info["audio"]):
                                        for sub_key,value in getid3_temp.info["audio"]:
                                            track_info[sub_key] = value
                                        # end for
                                    # end if
                                # end if
                                #// copy errors and warnings
                                if (not php_empty(lambda : getid3_temp.info["error"])):
                                    for newerror in getid3_temp.info["error"]:
                                        self.warning("getid3_ogg() says: [" + newerror + "]")
                                    # end for
                                # end if
                                if (not php_empty(lambda : getid3_temp.info["warning"])):
                                    for newerror in getid3_temp.info["warning"]:
                                        self.warning("getid3_ogg() says: [" + newerror + "]")
                                    # end for
                                # end if
                                if (not php_empty(lambda : getid3_temp.info["ogg"]["bitrate_nominal"])):
                                    track_info["bitrate"] = getid3_temp.info["ogg"]["bitrate_nominal"]
                                # end if
                                getid3_temp = None
                                getid3_ogg = None
                                oggpageinfo = None
                                vorbis_offset = None
                                break
                            # end if
                            if case("A_MS/ACM"):
                                getid3_lib.includedependency(GETID3_INCLUDEPATH + "module.audio-video.riff.php", __FILE__, True)
                                parsed = getid3_riff.parsewaveformatex(trackarray["CodecPrivate"])
                                for sub_key,value in parsed:
                                    if sub_key != "raw":
                                        track_info[sub_key] = value
                                    # end if
                                # end for
                                info["matroska"]["track_codec_parsed"][trackarray["TrackNumber"]] = parsed
                                break
                            # end if
                            if case():
                                self.warning("Unhandled audio type \"" + trackarray["CodecID"] if (php_isset(lambda : trackarray["CodecID"])) else "" + "\"")
                                break
                            # end if
                        # end for
                        info["audio"]["streams"][-1] = track_info
                        break
                    # end if
                # end for
            # end for
            if (not php_empty(lambda : info["video"]["streams"])):
                info["video"] = self.getdefaultstreaminfo(info["video"]["streams"])
            # end if
            if (not php_empty(lambda : info["audio"]["streams"])):
                info["audio"] = self.getdefaultstreaminfo(info["audio"]["streams"])
            # end if
        # end if
        #// process attachments
        if (php_isset(lambda : info["matroska"]["attachments"])) and self.getid3.option_save_attachments != getID3.ATTACHMENTS_NONE:
            for i,entry in info["matroska"]["attachments"]:
                if php_strpos(entry["FileMimeType"], "image/") == 0 and (not php_empty(lambda : entry["FileData"])):
                    info["matroska"]["comments"]["picture"][-1] = Array({"data": entry["FileData"], "image_mime": entry["FileMimeType"], "filename": entry["FileName"]})
                # end if
            # end for
        # end if
        #// determine mime type
        if (not php_empty(lambda : info["video"]["streams"])):
            info["mime_type"] = "video/webm" if info["matroska"]["doctype"] == "webm" else "video/x-matroska"
        elif (not php_empty(lambda : info["audio"]["streams"])):
            info["mime_type"] = "audio/webm" if info["matroska"]["doctype"] == "webm" else "audio/x-matroska"
        elif (php_isset(lambda : info["mime_type"])):
            info["mime_type"] = None
        # end if
        return True
    # end def analyze
    #// 
    #// @param array $info
    #//
    def parseebml(self, info=None):
        
        #// http://www.matroska.org/technical/specs/index.html#EBMLBasics
        self.current_offset = info["avdataoffset"]
        while True:
            
            if not (self.getebmlelement(top_element, info["avdataend"])):
                break
            # end if
            for case in Switch(top_element["id"]):
                if case(EBML_ID_EBML):
                    info["matroska"]["header"]["offset"] = top_element["offset"]
                    info["matroska"]["header"]["length"] = top_element["length"]
                    while True:
                        
                        if not (self.getebmlelement(element_data, top_element["end"], True)):
                            break
                        # end if
                        for case in Switch(element_data["id"]):
                            if case(EBML_ID_EBMLVERSION):
                                pass
                            # end if
                            if case(EBML_ID_EBMLREADVERSION):
                                pass
                            # end if
                            if case(EBML_ID_EBMLMAXIDLENGTH):
                                pass
                            # end if
                            if case(EBML_ID_EBMLMAXSIZELENGTH):
                                pass
                            # end if
                            if case(EBML_ID_DOCTYPEVERSION):
                                pass
                            # end if
                            if case(EBML_ID_DOCTYPEREADVERSION):
                                element_data["data"] = getid3_lib.bigendian2int(element_data["data"])
                                break
                            # end if
                            if case(EBML_ID_DOCTYPE):
                                element_data["data"] = getid3_lib.trimnullbyte(element_data["data"])
                                info["matroska"]["doctype"] = element_data["data"]
                                info["fileformat"] = element_data["data"]
                                break
                            # end if
                            if case():
                                self.unhandledelement("header", 0, element_data)
                                break
                            # end if
                        # end for
                        element_data["offset"] = None
                        element_data["end"] = None
                        info["matroska"]["header"]["elements"][-1] = element_data
                    # end while
                    break
                # end if
                if case(EBML_ID_SEGMENT):
                    info["matroska"]["segment"][0]["offset"] = top_element["offset"]
                    info["matroska"]["segment"][0]["length"] = top_element["length"]
                    while True:
                        
                        if not (self.getebmlelement(element_data, top_element["end"])):
                            break
                        # end if
                        if element_data["id"] != EBML_ID_CLUSTER or (not self.hide_clusters):
                            #// collect clusters only if required
                            info["matroska"]["segments"][-1] = element_data
                        # end if
                        for case in Switch(element_data["id"]):
                            if case(EBML_ID_SEEKHEAD):
                                #// Contains the position of other level 1 elements.
                                while True:
                                    
                                    if not (self.getebmlelement(seek_entry, element_data["end"])):
                                        break
                                    # end if
                                    for case in Switch(seek_entry["id"]):
                                        if case(EBML_ID_SEEK):
                                            #// Contains a single seek entry to an EBML element
                                            while True:
                                                
                                                if not (self.getebmlelement(sub_seek_entry, seek_entry["end"], True)):
                                                    break
                                                # end if
                                                for case in Switch(sub_seek_entry["id"]):
                                                    if case(EBML_ID_SEEKID):
                                                        seek_entry["target_id"] = self.ebml2int(sub_seek_entry["data"])
                                                        seek_entry["target_name"] = self.ebmlidname(seek_entry["target_id"])
                                                        break
                                                    # end if
                                                    if case(EBML_ID_SEEKPOSITION):
                                                        seek_entry["target_offset"] = element_data["offset"] + getid3_lib.bigendian2int(sub_seek_entry["data"])
                                                        break
                                                    # end if
                                                    if case():
                                                        self.unhandledelement("seekhead.seek", 0, sub_seek_entry)
                                                    # end if
                                                # end for
                                                break
                                            # end while
                                            if (not (php_isset(lambda : seek_entry["target_id"]))):
                                                self.warning("seek_entry[target_id] unexpectedly not set at " + seek_entry["offset"])
                                                break
                                            # end if
                                            if seek_entry["target_id"] != EBML_ID_CLUSTER or (not self.hide_clusters):
                                                #// collect clusters only if required
                                                info["matroska"]["seek"][-1] = seek_entry
                                            # end if
                                            break
                                        # end if
                                        if case():
                                            self.unhandledelement("seekhead", 0, seek_entry)
                                            break
                                        # end if
                                    # end for
                                # end while
                                break
                            # end if
                            if case(EBML_ID_TRACKS):
                                #// A top-level block of information with many tracks described.
                                info["matroska"]["tracks"] = element_data
                                while True:
                                    
                                    if not (self.getebmlelement(track_entry, element_data["end"])):
                                        break
                                    # end if
                                    for case in Switch(track_entry["id"]):
                                        if case(EBML_ID_TRACKENTRY):
                                            #// subelements: Describes a track with all elements.
                                            while True:
                                                
                                                if not (self.getebmlelement(subelement, track_entry["end"], Array(EBML_ID_VIDEO, EBML_ID_AUDIO, EBML_ID_CONTENTENCODINGS, EBML_ID_CODECPRIVATE))):
                                                    break
                                                # end if
                                                for case in Switch(subelement["id"]):
                                                    if case(EBML_ID_TRACKNUMBER):
                                                        pass
                                                    # end if
                                                    if case(EBML_ID_TRACKUID):
                                                        pass
                                                    # end if
                                                    if case(EBML_ID_TRACKTYPE):
                                                        pass
                                                    # end if
                                                    if case(EBML_ID_MINCACHE):
                                                        pass
                                                    # end if
                                                    if case(EBML_ID_MAXCACHE):
                                                        pass
                                                    # end if
                                                    if case(EBML_ID_MAXBLOCKADDITIONID):
                                                        pass
                                                    # end if
                                                    if case(EBML_ID_DEFAULTDURATION):
                                                        #// nanoseconds per frame
                                                        track_entry[subelement["id_name"]] = getid3_lib.bigendian2int(subelement["data"])
                                                        break
                                                    # end if
                                                    if case(EBML_ID_TRACKTIMECODESCALE):
                                                        track_entry[subelement["id_name"]] = getid3_lib.bigendian2float(subelement["data"])
                                                        break
                                                    # end if
                                                    if case(EBML_ID_CODECID):
                                                        pass
                                                    # end if
                                                    if case(EBML_ID_LANGUAGE):
                                                        pass
                                                    # end if
                                                    if case(EBML_ID_NAME):
                                                        pass
                                                    # end if
                                                    if case(EBML_ID_CODECNAME):
                                                        track_entry[subelement["id_name"]] = getid3_lib.trimnullbyte(subelement["data"])
                                                        break
                                                    # end if
                                                    if case(EBML_ID_CODECPRIVATE):
                                                        track_entry[subelement["id_name"]] = self.readebmlelementdata(subelement["length"], True)
                                                        break
                                                    # end if
                                                    if case(EBML_ID_FLAGENABLED):
                                                        pass
                                                    # end if
                                                    if case(EBML_ID_FLAGDEFAULT):
                                                        pass
                                                    # end if
                                                    if case(EBML_ID_FLAGFORCED):
                                                        pass
                                                    # end if
                                                    if case(EBML_ID_FLAGLACING):
                                                        pass
                                                    # end if
                                                    if case(EBML_ID_CODECDECODEALL):
                                                        track_entry[subelement["id_name"]] = php_bool(getid3_lib.bigendian2int(subelement["data"]))
                                                        break
                                                    # end if
                                                    if case(EBML_ID_VIDEO):
                                                        while True:
                                                            
                                                            if not (self.getebmlelement(sub_subelement, subelement["end"], True)):
                                                                break
                                                            # end if
                                                            for case in Switch(sub_subelement["id"]):
                                                                if case(EBML_ID_PIXELWIDTH):
                                                                    pass
                                                                # end if
                                                                if case(EBML_ID_PIXELHEIGHT):
                                                                    pass
                                                                # end if
                                                                if case(EBML_ID_PIXELCROPBOTTOM):
                                                                    pass
                                                                # end if
                                                                if case(EBML_ID_PIXELCROPTOP):
                                                                    pass
                                                                # end if
                                                                if case(EBML_ID_PIXELCROPLEFT):
                                                                    pass
                                                                # end if
                                                                if case(EBML_ID_PIXELCROPRIGHT):
                                                                    pass
                                                                # end if
                                                                if case(EBML_ID_DISPLAYWIDTH):
                                                                    pass
                                                                # end if
                                                                if case(EBML_ID_DISPLAYHEIGHT):
                                                                    pass
                                                                # end if
                                                                if case(EBML_ID_DISPLAYUNIT):
                                                                    pass
                                                                # end if
                                                                if case(EBML_ID_ASPECTRATIOTYPE):
                                                                    pass
                                                                # end if
                                                                if case(EBML_ID_STEREOMODE):
                                                                    pass
                                                                # end if
                                                                if case(EBML_ID_OLDSTEREOMODE):
                                                                    track_entry[sub_subelement["id_name"]] = getid3_lib.bigendian2int(sub_subelement["data"])
                                                                    break
                                                                # end if
                                                                if case(EBML_ID_FLAGINTERLACED):
                                                                    track_entry[sub_subelement["id_name"]] = php_bool(getid3_lib.bigendian2int(sub_subelement["data"]))
                                                                    break
                                                                # end if
                                                                if case(EBML_ID_GAMMAVALUE):
                                                                    track_entry[sub_subelement["id_name"]] = getid3_lib.bigendian2float(sub_subelement["data"])
                                                                    break
                                                                # end if
                                                                if case(EBML_ID_COLOURSPACE):
                                                                    track_entry[sub_subelement["id_name"]] = getid3_lib.trimnullbyte(sub_subelement["data"])
                                                                    break
                                                                # end if
                                                                if case():
                                                                    self.unhandledelement("track.video", 0, sub_subelement)
                                                                    break
                                                                # end if
                                                            # end for
                                                        # end while
                                                        break
                                                    # end if
                                                    if case(EBML_ID_AUDIO):
                                                        while True:
                                                            
                                                            if not (self.getebmlelement(sub_subelement, subelement["end"], True)):
                                                                break
                                                            # end if
                                                            for case in Switch(sub_subelement["id"]):
                                                                if case(EBML_ID_CHANNELS):
                                                                    pass
                                                                # end if
                                                                if case(EBML_ID_BITDEPTH):
                                                                    track_entry[sub_subelement["id_name"]] = getid3_lib.bigendian2int(sub_subelement["data"])
                                                                    break
                                                                # end if
                                                                if case(EBML_ID_SAMPLINGFREQUENCY):
                                                                    pass
                                                                # end if
                                                                if case(EBML_ID_OUTPUTSAMPLINGFREQUENCY):
                                                                    track_entry[sub_subelement["id_name"]] = getid3_lib.bigendian2float(sub_subelement["data"])
                                                                    break
                                                                # end if
                                                                if case(EBML_ID_CHANNELPOSITIONS):
                                                                    track_entry[sub_subelement["id_name"]] = getid3_lib.trimnullbyte(sub_subelement["data"])
                                                                    break
                                                                # end if
                                                                if case():
                                                                    self.unhandledelement("track.audio", 0, sub_subelement)
                                                                    break
                                                                # end if
                                                            # end for
                                                        # end while
                                                        break
                                                    # end if
                                                    if case(EBML_ID_CONTENTENCODINGS):
                                                        while True:
                                                            
                                                            if not (self.getebmlelement(sub_subelement, subelement["end"])):
                                                                break
                                                            # end if
                                                            for case in Switch(sub_subelement["id"]):
                                                                if case(EBML_ID_CONTENTENCODING):
                                                                    while True:
                                                                        
                                                                        if not (self.getebmlelement(sub_sub_subelement, sub_subelement["end"], Array(EBML_ID_CONTENTCOMPRESSION, EBML_ID_CONTENTENCRYPTION))):
                                                                            break
                                                                        # end if
                                                                        for case in Switch(sub_sub_subelement["id"]):
                                                                            if case(EBML_ID_CONTENTENCODINGORDER):
                                                                                pass
                                                                            # end if
                                                                            if case(EBML_ID_CONTENTENCODINGSCOPE):
                                                                                pass
                                                                            # end if
                                                                            if case(EBML_ID_CONTENTENCODINGTYPE):
                                                                                track_entry[sub_subelement["id_name"]][sub_sub_subelement["id_name"]] = getid3_lib.bigendian2int(sub_sub_subelement["data"])
                                                                                break
                                                                            # end if
                                                                            if case(EBML_ID_CONTENTCOMPRESSION):
                                                                                while True:
                                                                                    
                                                                                    if not (self.getebmlelement(sub_sub_sub_subelement, sub_sub_subelement["end"], True)):
                                                                                        break
                                                                                    # end if
                                                                                    for case in Switch(sub_sub_sub_subelement["id"]):
                                                                                        if case(EBML_ID_CONTENTCOMPALGO):
                                                                                            track_entry[sub_subelement["id_name"]][sub_sub_subelement["id_name"]][sub_sub_sub_subelement["id_name"]] = getid3_lib.bigendian2int(sub_sub_sub_subelement["data"])
                                                                                            break
                                                                                        # end if
                                                                                        if case(EBML_ID_CONTENTCOMPSETTINGS):
                                                                                            track_entry[sub_subelement["id_name"]][sub_sub_subelement["id_name"]][sub_sub_sub_subelement["id_name"]] = sub_sub_sub_subelement["data"]
                                                                                            break
                                                                                        # end if
                                                                                        if case():
                                                                                            self.unhandledelement("track.contentencodings.contentencoding.contentcompression", 0, sub_sub_sub_subelement)
                                                                                            break
                                                                                        # end if
                                                                                    # end for
                                                                                # end while
                                                                                break
                                                                            # end if
                                                                            if case(EBML_ID_CONTENTENCRYPTION):
                                                                                while True:
                                                                                    
                                                                                    if not (self.getebmlelement(sub_sub_sub_subelement, sub_sub_subelement["end"], True)):
                                                                                        break
                                                                                    # end if
                                                                                    for case in Switch(sub_sub_sub_subelement["id"]):
                                                                                        if case(EBML_ID_CONTENTENCALGO):
                                                                                            pass
                                                                                        # end if
                                                                                        if case(EBML_ID_CONTENTSIGALGO):
                                                                                            pass
                                                                                        # end if
                                                                                        if case(EBML_ID_CONTENTSIGHASHALGO):
                                                                                            track_entry[sub_subelement["id_name"]][sub_sub_subelement["id_name"]][sub_sub_sub_subelement["id_name"]] = getid3_lib.bigendian2int(sub_sub_sub_subelement["data"])
                                                                                            break
                                                                                        # end if
                                                                                        if case(EBML_ID_CONTENTENCKEYID):
                                                                                            pass
                                                                                        # end if
                                                                                        if case(EBML_ID_CONTENTSIGNATURE):
                                                                                            pass
                                                                                        # end if
                                                                                        if case(EBML_ID_CONTENTSIGKEYID):
                                                                                            track_entry[sub_subelement["id_name"]][sub_sub_subelement["id_name"]][sub_sub_sub_subelement["id_name"]] = sub_sub_sub_subelement["data"]
                                                                                            break
                                                                                        # end if
                                                                                        if case():
                                                                                            self.unhandledelement("track.contentencodings.contentencoding.contentcompression", 0, sub_sub_sub_subelement)
                                                                                            break
                                                                                        # end if
                                                                                    # end for
                                                                                # end while
                                                                                break
                                                                            # end if
                                                                            if case():
                                                                                self.unhandledelement("track.contentencodings.contentencoding", 0, sub_sub_subelement)
                                                                                break
                                                                            # end if
                                                                        # end for
                                                                    # end while
                                                                    break
                                                                # end if
                                                                if case():
                                                                    self.unhandledelement("track.contentencodings", 0, sub_subelement)
                                                                    break
                                                                # end if
                                                            # end for
                                                        # end while
                                                        break
                                                    # end if
                                                    if case():
                                                        self.unhandledelement("track", 0, subelement)
                                                        break
                                                    # end if
                                                # end for
                                            # end while
                                            info["matroska"]["tracks"]["tracks"][-1] = track_entry
                                            break
                                        # end if
                                        if case():
                                            self.unhandledelement("tracks", 0, track_entry)
                                            break
                                        # end if
                                    # end for
                                # end while
                                break
                            # end if
                            if case(EBML_ID_INFO):
                                #// Contains miscellaneous general information and statistics on the file.
                                info_entry = Array()
                                while True:
                                    
                                    if not (self.getebmlelement(subelement, element_data["end"], True)):
                                        break
                                    # end if
                                    for case in Switch(subelement["id"]):
                                        if case(EBML_ID_TIMECODESCALE):
                                            info_entry[subelement["id_name"]] = getid3_lib.bigendian2int(subelement["data"])
                                            break
                                        # end if
                                        if case(EBML_ID_DURATION):
                                            info_entry[subelement["id_name"]] = getid3_lib.bigendian2float(subelement["data"])
                                            break
                                        # end if
                                        if case(EBML_ID_DATEUTC):
                                            info_entry[subelement["id_name"]] = getid3_lib.bigendian2int(subelement["data"])
                                            info_entry[subelement["id_name"] + "_unix"] = self.ebmldate2unix(info_entry[subelement["id_name"]])
                                            break
                                        # end if
                                        if case(EBML_ID_SEGMENTUID):
                                            pass
                                        # end if
                                        if case(EBML_ID_PREVUID):
                                            pass
                                        # end if
                                        if case(EBML_ID_NEXTUID):
                                            info_entry[subelement["id_name"]] = getid3_lib.trimnullbyte(subelement["data"])
                                            break
                                        # end if
                                        if case(EBML_ID_SEGMENTFAMILY):
                                            info_entry[subelement["id_name"]][-1] = getid3_lib.trimnullbyte(subelement["data"])
                                            break
                                        # end if
                                        if case(EBML_ID_SEGMENTFILENAME):
                                            pass
                                        # end if
                                        if case(EBML_ID_PREVFILENAME):
                                            pass
                                        # end if
                                        if case(EBML_ID_NEXTFILENAME):
                                            pass
                                        # end if
                                        if case(EBML_ID_TITLE):
                                            pass
                                        # end if
                                        if case(EBML_ID_MUXINGAPP):
                                            pass
                                        # end if
                                        if case(EBML_ID_WRITINGAPP):
                                            info_entry[subelement["id_name"]] = getid3_lib.trimnullbyte(subelement["data"])
                                            info["matroska"]["comments"][php_strtolower(subelement["id_name"])][-1] = info_entry[subelement["id_name"]]
                                            break
                                        # end if
                                        if case(EBML_ID_CHAPTERTRANSLATE):
                                            chaptertranslate_entry = Array()
                                            while True:
                                                
                                                if not (self.getebmlelement(sub_subelement, subelement["end"], True)):
                                                    break
                                                # end if
                                                for case in Switch(sub_subelement["id"]):
                                                    if case(EBML_ID_CHAPTERTRANSLATEEDITIONUID):
                                                        chaptertranslate_entry[sub_subelement["id_name"]][-1] = getid3_lib.bigendian2int(sub_subelement["data"])
                                                        break
                                                    # end if
                                                    if case(EBML_ID_CHAPTERTRANSLATECODEC):
                                                        chaptertranslate_entry[sub_subelement["id_name"]] = getid3_lib.bigendian2int(sub_subelement["data"])
                                                        break
                                                    # end if
                                                    if case(EBML_ID_CHAPTERTRANSLATEID):
                                                        chaptertranslate_entry[sub_subelement["id_name"]] = getid3_lib.trimnullbyte(sub_subelement["data"])
                                                        break
                                                    # end if
                                                    if case():
                                                        self.unhandledelement("info.chaptertranslate", 0, sub_subelement)
                                                        break
                                                    # end if
                                                # end for
                                            # end while
                                            info_entry[subelement["id_name"]] = chaptertranslate_entry
                                            break
                                        # end if
                                        if case():
                                            self.unhandledelement("info", 0, subelement)
                                            break
                                        # end if
                                    # end for
                                # end while
                                info["matroska"]["info"][-1] = info_entry
                                break
                            # end if
                            if case(EBML_ID_CUES):
                                #// A top-level element to speed seeking access. All entries are local to the segment. Should be mandatory for non "live" streams.
                                if self.hide_clusters:
                                    #// do not parse cues if hide clusters is "ON" till they point to clusters anyway
                                    self.current_offset = element_data["end"]
                                    break
                                # end if
                                cues_entry = Array()
                                while True:
                                    
                                    if not (self.getebmlelement(subelement, element_data["end"])):
                                        break
                                    # end if
                                    for case in Switch(subelement["id"]):
                                        if case(EBML_ID_CUEPOINT):
                                            cuepoint_entry = Array()
                                            while True:
                                                
                                                if not (self.getebmlelement(sub_subelement, subelement["end"], Array(EBML_ID_CUETRACKPOSITIONS))):
                                                    break
                                                # end if
                                                for case in Switch(sub_subelement["id"]):
                                                    if case(EBML_ID_CUETRACKPOSITIONS):
                                                        cuetrackpositions_entry = Array()
                                                        while True:
                                                            
                                                            if not (self.getebmlelement(sub_sub_subelement, sub_subelement["end"], True)):
                                                                break
                                                            # end if
                                                            for case in Switch(sub_sub_subelement["id"]):
                                                                if case(EBML_ID_CUETRACK):
                                                                    pass
                                                                # end if
                                                                if case(EBML_ID_CUECLUSTERPOSITION):
                                                                    pass
                                                                # end if
                                                                if case(EBML_ID_CUEBLOCKNUMBER):
                                                                    pass
                                                                # end if
                                                                if case(EBML_ID_CUECODECSTATE):
                                                                    cuetrackpositions_entry[sub_sub_subelement["id_name"]] = getid3_lib.bigendian2int(sub_sub_subelement["data"])
                                                                    break
                                                                # end if
                                                                if case():
                                                                    self.unhandledelement("cues.cuepoint.cuetrackpositions", 0, sub_sub_subelement)
                                                                    break
                                                                # end if
                                                            # end for
                                                        # end while
                                                        cuepoint_entry[sub_subelement["id_name"]][-1] = cuetrackpositions_entry
                                                        break
                                                    # end if
                                                    if case(EBML_ID_CUETIME):
                                                        cuepoint_entry[sub_subelement["id_name"]] = getid3_lib.bigendian2int(sub_subelement["data"])
                                                        break
                                                    # end if
                                                    if case():
                                                        self.unhandledelement("cues.cuepoint", 0, sub_subelement)
                                                        break
                                                    # end if
                                                # end for
                                            # end while
                                            cues_entry[-1] = cuepoint_entry
                                            break
                                        # end if
                                        if case():
                                            self.unhandledelement("cues", 0, subelement)
                                            break
                                        # end if
                                    # end for
                                # end while
                                info["matroska"]["cues"] = cues_entry
                                break
                            # end if
                            if case(EBML_ID_TAGS):
                                #// Element containing elements specific to Tracks/Chapters.
                                tags_entry = Array()
                                while True:
                                    
                                    if not (self.getebmlelement(subelement, element_data["end"], False)):
                                        break
                                    # end if
                                    for case in Switch(subelement["id"]):
                                        if case(EBML_ID_TAG):
                                            tag_entry = Array()
                                            while True:
                                                
                                                if not (self.getebmlelement(sub_subelement, subelement["end"], False)):
                                                    break
                                                # end if
                                                for case in Switch(sub_subelement["id"]):
                                                    if case(EBML_ID_TARGETS):
                                                        targets_entry = Array()
                                                        while True:
                                                            
                                                            if not (self.getebmlelement(sub_sub_subelement, sub_subelement["end"], True)):
                                                                break
                                                            # end if
                                                            for case in Switch(sub_sub_subelement["id"]):
                                                                if case(EBML_ID_TARGETTYPEVALUE):
                                                                    targets_entry[sub_sub_subelement["id_name"]] = getid3_lib.bigendian2int(sub_sub_subelement["data"])
                                                                    targets_entry[php_strtolower(sub_sub_subelement["id_name"]) + "_long"] = self.targettypevalue(targets_entry[sub_sub_subelement["id_name"]])
                                                                    break
                                                                # end if
                                                                if case(EBML_ID_TARGETTYPE):
                                                                    targets_entry[sub_sub_subelement["id_name"]] = sub_sub_subelement["data"]
                                                                    break
                                                                # end if
                                                                if case(EBML_ID_TAGTRACKUID):
                                                                    pass
                                                                # end if
                                                                if case(EBML_ID_TAGEDITIONUID):
                                                                    pass
                                                                # end if
                                                                if case(EBML_ID_TAGCHAPTERUID):
                                                                    pass
                                                                # end if
                                                                if case(EBML_ID_TAGATTACHMENTUID):
                                                                    targets_entry[sub_sub_subelement["id_name"]][-1] = getid3_lib.bigendian2int(sub_sub_subelement["data"])
                                                                    break
                                                                # end if
                                                                if case():
                                                                    self.unhandledelement("tags.tag.targets", 0, sub_sub_subelement)
                                                                    break
                                                                # end if
                                                            # end for
                                                        # end while
                                                        tag_entry[sub_subelement["id_name"]] = targets_entry
                                                        break
                                                    # end if
                                                    if case(EBML_ID_SIMPLETAG):
                                                        tag_entry[sub_subelement["id_name"]][-1] = self.handleemblsimpletag(sub_subelement["end"])
                                                        break
                                                    # end if
                                                    if case():
                                                        self.unhandledelement("tags.tag", 0, sub_subelement)
                                                        break
                                                    # end if
                                                # end for
                                            # end while
                                            tags_entry[-1] = tag_entry
                                            break
                                        # end if
                                        if case():
                                            self.unhandledelement("tags", 0, subelement)
                                            break
                                        # end if
                                    # end for
                                # end while
                                info["matroska"]["tags"] = tags_entry
                                break
                            # end if
                            if case(EBML_ID_ATTACHMENTS):
                                #// Contain attached files.
                                while True:
                                    
                                    if not (self.getebmlelement(subelement, element_data["end"])):
                                        break
                                    # end if
                                    for case in Switch(subelement["id"]):
                                        if case(EBML_ID_ATTACHEDFILE):
                                            attachedfile_entry = Array()
                                            while True:
                                                
                                                if not (self.getebmlelement(sub_subelement, subelement["end"], Array(EBML_ID_FILEDATA))):
                                                    break
                                                # end if
                                                for case in Switch(sub_subelement["id"]):
                                                    if case(EBML_ID_FILEDESCRIPTION):
                                                        pass
                                                    # end if
                                                    if case(EBML_ID_FILENAME):
                                                        pass
                                                    # end if
                                                    if case(EBML_ID_FILEMIMETYPE):
                                                        attachedfile_entry[sub_subelement["id_name"]] = sub_subelement["data"]
                                                        break
                                                    # end if
                                                    if case(EBML_ID_FILEDATA):
                                                        attachedfile_entry["data_offset"] = self.current_offset
                                                        attachedfile_entry["data_length"] = sub_subelement["length"]
                                                        attachedfile_entry[sub_subelement["id_name"]] = self.saveattachment(attachedfile_entry["FileName"], attachedfile_entry["data_offset"], attachedfile_entry["data_length"])
                                                        self.current_offset = sub_subelement["end"]
                                                        break
                                                    # end if
                                                    if case(EBML_ID_FILEUID):
                                                        attachedfile_entry[sub_subelement["id_name"]] = getid3_lib.bigendian2int(sub_subelement["data"])
                                                        break
                                                    # end if
                                                    if case():
                                                        self.unhandledelement("attachments.attachedfile", 0, sub_subelement)
                                                        break
                                                    # end if
                                                # end for
                                            # end while
                                            info["matroska"]["attachments"][-1] = attachedfile_entry
                                            break
                                        # end if
                                        if case():
                                            self.unhandledelement("attachments", 0, subelement)
                                            break
                                        # end if
                                    # end for
                                # end while
                                break
                            # end if
                            if case(EBML_ID_CHAPTERS):
                                while True:
                                    
                                    if not (self.getebmlelement(subelement, element_data["end"])):
                                        break
                                    # end if
                                    for case in Switch(subelement["id"]):
                                        if case(EBML_ID_EDITIONENTRY):
                                            editionentry_entry = Array()
                                            while True:
                                                
                                                if not (self.getebmlelement(sub_subelement, subelement["end"], Array(EBML_ID_CHAPTERATOM))):
                                                    break
                                                # end if
                                                for case in Switch(sub_subelement["id"]):
                                                    if case(EBML_ID_EDITIONUID):
                                                        editionentry_entry[sub_subelement["id_name"]] = getid3_lib.bigendian2int(sub_subelement["data"])
                                                        break
                                                    # end if
                                                    if case(EBML_ID_EDITIONFLAGHIDDEN):
                                                        pass
                                                    # end if
                                                    if case(EBML_ID_EDITIONFLAGDEFAULT):
                                                        pass
                                                    # end if
                                                    if case(EBML_ID_EDITIONFLAGORDERED):
                                                        editionentry_entry[sub_subelement["id_name"]] = php_bool(getid3_lib.bigendian2int(sub_subelement["data"]))
                                                        break
                                                    # end if
                                                    if case(EBML_ID_CHAPTERATOM):
                                                        chapteratom_entry = Array()
                                                        while True:
                                                            
                                                            if not (self.getebmlelement(sub_sub_subelement, sub_subelement["end"], Array(EBML_ID_CHAPTERTRACK, EBML_ID_CHAPTERDISPLAY))):
                                                                break
                                                            # end if
                                                            for case in Switch(sub_sub_subelement["id"]):
                                                                if case(EBML_ID_CHAPTERSEGMENTUID):
                                                                    pass
                                                                # end if
                                                                if case(EBML_ID_CHAPTERSEGMENTEDITIONUID):
                                                                    chapteratom_entry[sub_sub_subelement["id_name"]] = sub_sub_subelement["data"]
                                                                    break
                                                                # end if
                                                                if case(EBML_ID_CHAPTERFLAGENABLED):
                                                                    pass
                                                                # end if
                                                                if case(EBML_ID_CHAPTERFLAGHIDDEN):
                                                                    chapteratom_entry[sub_sub_subelement["id_name"]] = php_bool(getid3_lib.bigendian2int(sub_sub_subelement["data"]))
                                                                    break
                                                                # end if
                                                                if case(EBML_ID_CHAPTERUID):
                                                                    pass
                                                                # end if
                                                                if case(EBML_ID_CHAPTERTIMESTART):
                                                                    pass
                                                                # end if
                                                                if case(EBML_ID_CHAPTERTIMEEND):
                                                                    chapteratom_entry[sub_sub_subelement["id_name"]] = getid3_lib.bigendian2int(sub_sub_subelement["data"])
                                                                    break
                                                                # end if
                                                                if case(EBML_ID_CHAPTERTRACK):
                                                                    chaptertrack_entry = Array()
                                                                    while True:
                                                                        
                                                                        if not (self.getebmlelement(sub_sub_sub_subelement, sub_sub_subelement["end"], True)):
                                                                            break
                                                                        # end if
                                                                        for case in Switch(sub_sub_sub_subelement["id"]):
                                                                            if case(EBML_ID_CHAPTERTRACKNUMBER):
                                                                                chaptertrack_entry[sub_sub_sub_subelement["id_name"]] = getid3_lib.bigendian2int(sub_sub_sub_subelement["data"])
                                                                                break
                                                                            # end if
                                                                            if case():
                                                                                self.unhandledelement("chapters.editionentry.chapteratom.chaptertrack", 0, sub_sub_sub_subelement)
                                                                                break
                                                                            # end if
                                                                        # end for
                                                                    # end while
                                                                    chapteratom_entry[sub_sub_subelement["id_name"]][-1] = chaptertrack_entry
                                                                    break
                                                                # end if
                                                                if case(EBML_ID_CHAPTERDISPLAY):
                                                                    chapterdisplay_entry = Array()
                                                                    while True:
                                                                        
                                                                        if not (self.getebmlelement(sub_sub_sub_subelement, sub_sub_subelement["end"], True)):
                                                                            break
                                                                        # end if
                                                                        for case in Switch(sub_sub_sub_subelement["id"]):
                                                                            if case(EBML_ID_CHAPSTRING):
                                                                                pass
                                                                            # end if
                                                                            if case(EBML_ID_CHAPLANGUAGE):
                                                                                pass
                                                                            # end if
                                                                            if case(EBML_ID_CHAPCOUNTRY):
                                                                                chapterdisplay_entry[sub_sub_sub_subelement["id_name"]] = sub_sub_sub_subelement["data"]
                                                                                break
                                                                            # end if
                                                                            if case():
                                                                                self.unhandledelement("chapters.editionentry.chapteratom.chapterdisplay", 0, sub_sub_sub_subelement)
                                                                                break
                                                                            # end if
                                                                        # end for
                                                                    # end while
                                                                    chapteratom_entry[sub_sub_subelement["id_name"]][-1] = chapterdisplay_entry
                                                                    break
                                                                # end if
                                                                if case():
                                                                    self.unhandledelement("chapters.editionentry.chapteratom", 0, sub_sub_subelement)
                                                                    break
                                                                # end if
                                                            # end for
                                                        # end while
                                                        editionentry_entry[sub_subelement["id_name"]][-1] = chapteratom_entry
                                                        break
                                                    # end if
                                                    if case():
                                                        self.unhandledelement("chapters.editionentry", 0, sub_subelement)
                                                        break
                                                    # end if
                                                # end for
                                            # end while
                                            info["matroska"]["chapters"][-1] = editionentry_entry
                                            break
                                        # end if
                                        if case():
                                            self.unhandledelement("chapters", 0, subelement)
                                            break
                                        # end if
                                    # end for
                                # end while
                                break
                            # end if
                            if case(EBML_ID_CLUSTER):
                                #// The lower level element containing the (monolithic) Block structure.
                                cluster_entry = Array()
                                while True:
                                    
                                    if not (self.getebmlelement(subelement, element_data["end"], Array(EBML_ID_CLUSTERSILENTTRACKS, EBML_ID_CLUSTERBLOCKGROUP, EBML_ID_CLUSTERSIMPLEBLOCK))):
                                        break
                                    # end if
                                    for case in Switch(subelement["id"]):
                                        if case(EBML_ID_CLUSTERTIMECODE):
                                            pass
                                        # end if
                                        if case(EBML_ID_CLUSTERPOSITION):
                                            pass
                                        # end if
                                        if case(EBML_ID_CLUSTERPREVSIZE):
                                            cluster_entry[subelement["id_name"]] = getid3_lib.bigendian2int(subelement["data"])
                                            break
                                        # end if
                                        if case(EBML_ID_CLUSTERSILENTTRACKS):
                                            cluster_silent_tracks = Array()
                                            while True:
                                                
                                                if not (self.getebmlelement(sub_subelement, subelement["end"], True)):
                                                    break
                                                # end if
                                                for case in Switch(sub_subelement["id"]):
                                                    if case(EBML_ID_CLUSTERSILENTTRACKNUMBER):
                                                        cluster_silent_tracks[-1] = getid3_lib.bigendian2int(sub_subelement["data"])
                                                        break
                                                    # end if
                                                    if case():
                                                        self.unhandledelement("cluster.silenttracks", 0, sub_subelement)
                                                        break
                                                    # end if
                                                # end for
                                            # end while
                                            cluster_entry[subelement["id_name"]][-1] = cluster_silent_tracks
                                            break
                                        # end if
                                        if case(EBML_ID_CLUSTERBLOCKGROUP):
                                            cluster_block_group = Array({"offset": self.current_offset})
                                            while True:
                                                
                                                if not (self.getebmlelement(sub_subelement, subelement["end"], Array(EBML_ID_CLUSTERBLOCK))):
                                                    break
                                                # end if
                                                for case in Switch(sub_subelement["id"]):
                                                    if case(EBML_ID_CLUSTERBLOCK):
                                                        cluster_block_group[sub_subelement["id_name"]] = self.handleemblclusterblock(sub_subelement, EBML_ID_CLUSTERBLOCK, info)
                                                        break
                                                    # end if
                                                    if case(EBML_ID_CLUSTERREFERENCEPRIORITY):
                                                        pass
                                                    # end if
                                                    if case(EBML_ID_CLUSTERBLOCKDURATION):
                                                        #// unsigned-int
                                                        cluster_block_group[sub_subelement["id_name"]] = getid3_lib.bigendian2int(sub_subelement["data"])
                                                        break
                                                    # end if
                                                    if case(EBML_ID_CLUSTERREFERENCEBLOCK):
                                                        #// signed-int
                                                        cluster_block_group[sub_subelement["id_name"]][-1] = getid3_lib.bigendian2int(sub_subelement["data"], False, True)
                                                        break
                                                    # end if
                                                    if case(EBML_ID_CLUSTERCODECSTATE):
                                                        cluster_block_group[sub_subelement["id_name"]] = getid3_lib.trimnullbyte(sub_subelement["data"])
                                                        break
                                                    # end if
                                                    if case():
                                                        self.unhandledelement("clusters.blockgroup", 0, sub_subelement)
                                                        break
                                                    # end if
                                                # end for
                                            # end while
                                            cluster_entry[subelement["id_name"]][-1] = cluster_block_group
                                            break
                                        # end if
                                        if case(EBML_ID_CLUSTERSIMPLEBLOCK):
                                            cluster_entry[subelement["id_name"]][-1] = self.handleemblclusterblock(subelement, EBML_ID_CLUSTERSIMPLEBLOCK, info)
                                            break
                                        # end if
                                        if case():
                                            self.unhandledelement("cluster", 0, subelement)
                                            break
                                        # end if
                                    # end for
                                    self.current_offset = subelement["end"]
                                # end while
                                if (not self.hide_clusters):
                                    info["matroska"]["cluster"][-1] = cluster_entry
                                # end if
                                #// check to see if all the data we need exists already, if so, break out of the loop
                                if (not self.parse_whole_file):
                                    if (php_isset(lambda : info["matroska"]["info"])) and php_is_array(info["matroska"]["info"]):
                                        if (php_isset(lambda : info["matroska"]["tracks"]["tracks"])) and php_is_array(info["matroska"]["tracks"]["tracks"]):
                                            if php_count(info["matroska"]["track_data_offsets"]) == php_count(info["matroska"]["tracks"]["tracks"]):
                                                return
                                            # end if
                                        # end if
                                    # end if
                                # end if
                                break
                            # end if
                            if case():
                                self.unhandledelement("segment", 0, element_data)
                                break
                            # end if
                        # end for
                    # end while
                    break
                # end if
                if case():
                    self.unhandledelement("root", 0, top_element)
                    break
                # end if
            # end for
        # end while
    # end def parseebml
    #// 
    #// @param int $min_data
    #// 
    #// @return bool
    #//
    def ensurebufferhasenoughdata(self, min_data=1024):
        
        if self.current_offset - self.EBMLbuffer_offset >= self.EBMLbuffer_length - min_data:
            read_bytes = php_max(min_data, self.getid3.fread_buffer_size())
            try: 
                self.fseek(self.current_offset)
                self.EBMLbuffer_offset = self.current_offset
                self.EBMLbuffer = self.fread(read_bytes)
                self.EBMLbuffer_length = php_strlen(self.EBMLbuffer)
            except getid3_exception as e:
                self.warning("EBML parser: " + e.getmessage())
                return False
            # end try
            if self.EBMLbuffer_length == 0 and self.feof():
                return self.error("EBML parser: ran out of file at offset " + self.current_offset)
            # end if
        # end if
        return True
    # end def ensurebufferhasenoughdata
    #// 
    #// @return int|float|false
    #//
    def readebmlint(self):
        
        actual_offset = self.current_offset - self.EBMLbuffer_offset
        #// get length of integer
        first_byte_int = php_ord(self.EBMLbuffer[actual_offset])
        if 128 & first_byte_int:
            length = 1
        elif 64 & first_byte_int:
            length = 2
        elif 32 & first_byte_int:
            length = 3
        elif 16 & first_byte_int:
            length = 4
        elif 8 & first_byte_int:
            length = 5
        elif 4 & first_byte_int:
            length = 6
        elif 2 & first_byte_int:
            length = 7
        elif 1 & first_byte_int:
            length = 8
        else:
            raise php_new_class("Exception", lambda : Exception("invalid EBML integer (leading 0x00) at " + self.current_offset))
        # end if
        #// read
        int_value = self.ebml2int(php_substr(self.EBMLbuffer, actual_offset, length))
        self.current_offset += length
        return int_value
    # end def readebmlint
    #// 
    #// @param int  $length
    #// @param bool $check_buffer
    #// 
    #// @return string|false
    #//
    def readebmlelementdata(self, length=None, check_buffer=False):
        
        if check_buffer and (not self.ensurebufferhasenoughdata(length)):
            return False
        # end if
        data = php_substr(self.EBMLbuffer, self.current_offset - self.EBMLbuffer_offset, length)
        self.current_offset += length
        return data
    # end def readebmlelementdata
    #// 
    #// @param array      $element
    #// @param int        $parent_end
    #// @param array|bool $get_data
    #// 
    #// @return bool
    #//
    def getebmlelement(self, element=None, parent_end=None, get_data=False):
        
        if self.current_offset >= parent_end:
            return False
        # end if
        if (not self.ensurebufferhasenoughdata()):
            self.current_offset = PHP_INT_MAX
            #// do not exit parser right now, allow to finish current loop to gather maximum information
            return False
        # end if
        element = Array()
        #// set offset
        element["offset"] = self.current_offset
        #// get ID
        element["id"] = self.readebmlint()
        #// get name
        element["id_name"] = self.ebmlidname(element["id"])
        #// get length
        element["length"] = self.readebmlint()
        #// get end offset
        element["end"] = self.current_offset + element["length"]
        #// get raw data
        dont_parse = php_in_array(element["id"], self.unuseful_elements) or element["id_name"] == dechex(element["id"])
        if get_data == True or php_is_array(get_data) and (not php_in_array(element["id"], get_data)) and (not dont_parse):
            element["data"] = self.readebmlelementdata(element["length"], element)
        # end if
        return True
    # end def getebmlelement
    #// 
    #// @param string $type
    #// @param int    $line
    #// @param array  $element
    #//
    def unhandledelement(self, type=None, line=None, element=None):
        
        #// warn only about unknown and missed elements, not about unuseful
        if (not php_in_array(element["id"], self.unuseful_elements)):
            self.warning("Unhandled " + type + " element [" + php_basename(__FILE__) + ":" + line + "] (" + element["id"] + "::" + element["id_name"] + " [" + element["length"] + " bytes]) at " + element["offset"])
        # end if
        #// increase offset for unparsed elements
        if (not (php_isset(lambda : element["data"]))):
            self.current_offset = element["end"]
        # end if
    # end def unhandledelement
    #// 
    #// @param array $SimpleTagArray
    #// 
    #// @return bool
    #//
    def extractcommentssimpletag(self, SimpleTagArray=None):
        
        if (not php_empty(lambda : SimpleTagArray["SimpleTag"])):
            for SimpleTagKey,SimpleTagData in SimpleTagArray["SimpleTag"]:
                if (not php_empty(lambda : SimpleTagData["TagName"])) and (not php_empty(lambda : SimpleTagData["TagString"])):
                    self.getid3.info["matroska"]["comments"][php_strtolower(SimpleTagData["TagName"])][-1] = SimpleTagData["TagString"]
                # end if
                if (not php_empty(lambda : SimpleTagData["SimpleTag"])):
                    self.extractcommentssimpletag(SimpleTagData)
                # end if
            # end for
        # end if
        return True
    # end def extractcommentssimpletag
    #// 
    #// @param int $parent_end
    #// 
    #// @return array
    #//
    def handleemblsimpletag(self, parent_end=None):
        
        simpletag_entry = Array()
        while True:
            
            if not (self.getebmlelement(element, parent_end, Array(EBML_ID_SIMPLETAG))):
                break
            # end if
            for case in Switch(element["id"]):
                if case(EBML_ID_TAGNAME):
                    pass
                # end if
                if case(EBML_ID_TAGLANGUAGE):
                    pass
                # end if
                if case(EBML_ID_TAGSTRING):
                    pass
                # end if
                if case(EBML_ID_TAGBINARY):
                    simpletag_entry[element["id_name"]] = element["data"]
                    break
                # end if
                if case(EBML_ID_SIMPLETAG):
                    simpletag_entry[element["id_name"]][-1] = self.handleemblsimpletag(element["end"])
                    break
                # end if
                if case(EBML_ID_TAGDEFAULT):
                    simpletag_entry[element["id_name"]] = php_bool(getid3_lib.bigendian2int(element["data"]))
                    break
                # end if
                if case():
                    self.unhandledelement("tag.simpletag", 0, element)
                    break
                # end if
            # end for
        # end while
        return simpletag_entry
    # end def handleemblsimpletag
    #// 
    #// @param array $element
    #// @param int   $block_type
    #// @param array $info
    #// 
    #// @return array
    #//
    def handleemblclusterblock(self, element=None, block_type=None, info=None):
        
        #// http://www.matroska.org/technical/specs/index.html#block_structure
        #// http://www.matroska.org/technical/specs/index.html#simpleblock_structure
        block_data = Array()
        block_data["tracknumber"] = self.readebmlint()
        block_data["timecode"] = getid3_lib.bigendian2int(self.readebmlelementdata(2), False, True)
        block_data["flags_raw"] = getid3_lib.bigendian2int(self.readebmlelementdata(1))
        if block_type == EBML_ID_CLUSTERSIMPLEBLOCK:
            block_data["flags"]["keyframe"] = block_data["flags_raw"] & 128 >> 7
            pass
        else:
            pass
        # end if
        block_data["flags"]["invisible"] = php_bool(block_data["flags_raw"] & 8 >> 3)
        block_data["flags"]["lacing"] = block_data["flags_raw"] & 6 >> 1
        #// 00=no lacing; 01=Xiph lacing; 11=EBML lacing; 10=fixed-size lacing
        if block_type == EBML_ID_CLUSTERSIMPLEBLOCK:
            block_data["flags"]["discardable"] = block_data["flags_raw"] & 1
        else:
            pass
        # end if
        block_data["flags"]["lacing_type"] = self.blocklacingtype(block_data["flags"]["lacing"])
        #// Lace (when lacing bit is set)
        if block_data["flags"]["lacing"] > 0:
            block_data["lace_frames"] = getid3_lib.bigendian2int(self.readebmlelementdata(1)) + 1
            #// Number of frames in the lace-1 (uint8)
            if block_data["flags"]["lacing"] != 2:
                i = 1
                while i < block_data["lace_frames"]:
                    
                    #// Lace-coded size of each frame of the lace, except for the last one (multiple uint8). *This is not used with Fixed-size lacing as it is calculated automatically from (total size of lace) / (number of frames in lace).
                    if block_data["flags"]["lacing"] == 3:
                        #// EBML lacing
                        block_data["lace_frames_size"][i] = self.readebmlint()
                        pass
                    else:
                        #// Xiph lacing
                        block_data["lace_frames_size"][i] = 0
                        while True:
                            size = getid3_lib.bigendian2int(self.readebmlelementdata(1))
                            block_data["lace_frames_size"][i] += size
                            
                            if size == 255:
                                break
                            # end if
                        # end while
                    # end if
                    i += 1
                # end while
                if block_data["flags"]["lacing"] == 1:
                    #// calc size of the last frame only for Xiph lacing, till EBML sizes are now anyway determined incorrectly
                    block_data["lace_frames_size"][-1] = element["end"] - self.current_offset - array_sum(block_data["lace_frames_size"])
                # end if
            # end if
        # end if
        if (not (php_isset(lambda : info["matroska"]["track_data_offsets"][block_data["tracknumber"]]))):
            info["matroska"]["track_data_offsets"][block_data["tracknumber"]]["offset"] = self.current_offset
            info["matroska"]["track_data_offsets"][block_data["tracknumber"]]["length"] = element["end"] - self.current_offset
            pass
        # end if
        #// $info['matroska']['track_data_offsets'][$block_data['tracknumber']]['total_length'] += $info['matroska']['track_data_offsets'][$block_data['tracknumber']]['length'];
        #// $info['matroska']['track_data_offsets'][$block_data['tracknumber']]['duration']      = $block_data['timecode'] * ((isset($info['matroska']['info'][0]['TimecodeScale']) ? $info['matroska']['info'][0]['TimecodeScale'] : 1000000) / 1000000000);
        #// set offset manually
        self.current_offset = element["end"]
        return block_data
    # end def handleemblclusterblock
    #// 
    #// @param string $EBMLstring
    #// 
    #// @return int|float|false
    #//
    def ebml2int(self, EBMLstring=None):
        
        #// http://matroska.org/specs
        #// Element ID coded with an UTF-8 like system:
        #// 1xxx xxxx                                  - Class A IDs (2^7 -2 possible values) (base 0x8X)
        #// 01xx xxxx  xxxx xxxx                       - Class B IDs (2^14-2 possible values) (base 0x4X 0xXX)
        #// 001x xxxx  xxxx xxxx  xxxx xxxx            - Class C IDs (2^21-2 possible values) (base 0x2X 0xXX 0xXX)
        #// 0001 xxxx  xxxx xxxx  xxxx xxxx  xxxx xxxx - Class D IDs (2^28-2 possible values) (base 0x1X 0xXX 0xXX 0xXX)
        #// Values with all x at 0 and 1 are reserved (hence the -2).
        #// Data size, in octets, is also coded with an UTF-8 like system :
        #// 1xxx xxxx                                                                              - value 0 to  2^7-2
        #// 01xx xxxx  xxxx xxxx                                                                   - value 0 to 2^14-2
        #// 001x xxxx  xxxx xxxx  xxxx xxxx                                                        - value 0 to 2^21-2
        #// 0001 xxxx  xxxx xxxx  xxxx xxxx  xxxx xxxx                                             - value 0 to 2^28-2
        #// 0000 1xxx  xxxx xxxx  xxxx xxxx  xxxx xxxx  xxxx xxxx                                  - value 0 to 2^35-2
        #// 0000 01xx  xxxx xxxx  xxxx xxxx  xxxx xxxx  xxxx xxxx  xxxx xxxx                       - value 0 to 2^42-2
        #// 0000 001x  xxxx xxxx  xxxx xxxx  xxxx xxxx  xxxx xxxx  xxxx xxxx  xxxx xxxx            - value 0 to 2^49-2
        #// 0000 0001  xxxx xxxx  xxxx xxxx  xxxx xxxx  xxxx xxxx  xxxx xxxx  xxxx xxxx  xxxx xxxx - value 0 to 2^56-2
        first_byte_int = php_ord(EBMLstring[0])
        if 128 & first_byte_int:
            EBMLstring[0] = chr(first_byte_int & 127)
        elif 64 & first_byte_int:
            EBMLstring[0] = chr(first_byte_int & 63)
        elif 32 & first_byte_int:
            EBMLstring[0] = chr(first_byte_int & 31)
        elif 16 & first_byte_int:
            EBMLstring[0] = chr(first_byte_int & 15)
        elif 8 & first_byte_int:
            EBMLstring[0] = chr(first_byte_int & 7)
        elif 4 & first_byte_int:
            EBMLstring[0] = chr(first_byte_int & 3)
        elif 2 & first_byte_int:
            EBMLstring[0] = chr(first_byte_int & 1)
        elif 1 & first_byte_int:
            EBMLstring[0] = chr(first_byte_int & 0)
        # end if
        return getid3_lib.bigendian2int(EBMLstring)
    # end def ebml2int
    #// 
    #// @param int $EBMLdatestamp
    #// 
    #// @return float
    #//
    def ebmldate2unix(self, EBMLdatestamp=None):
        
        #// Date - signed 8 octets integer in nanoseconds with 0 indicating the precise beginning of the millennium (at 2001-01-01T00:00:00,000000000 UTC)
        #// 978307200 == mktime(0, 0, 0, 1, 1, 2001) == January 1, 2001 12:00:00am UTC
        return round(EBMLdatestamp / 1000000000 + 978307200)
    # end def ebmldate2unix
    #// 
    #// @param int $target_type
    #// 
    #// @return string|int
    #//
    @classmethod
    def targettypevalue(self, target_type=None):
        
        TargetTypeValue = Array()
        if php_empty(lambda : TargetTypeValue):
            TargetTypeValue[10] = "A: ~ V:shot"
            #// the lowest hierarchy found in music or movies
            TargetTypeValue[20] = "A:subtrack/part/movement ~ V:scene"
            #// corresponds to parts of a track for audio (like a movement)
            TargetTypeValue[30] = "A:track/song ~ V:chapter"
            #// the common parts of an album or a movie
            TargetTypeValue[40] = "A:part/session ~ V:part/session"
            #// when an album or episode has different logical parts
            TargetTypeValue[50] = "A:album/opera/concert ~ V:movie/episode/concert"
            #// the most common grouping level of music and video (equals to an episode for TV series)
            TargetTypeValue[60] = "A:edition/issue/volume/opus ~ V:season/sequel/volume"
            #// a list of lower levels grouped together
            TargetTypeValue[70] = "A:collection ~ V:collection"
            pass
        # end if
        return TargetTypeValue[target_type] if (php_isset(lambda : TargetTypeValue[target_type])) else target_type
    # end def targettypevalue
    #// 
    #// @param int $lacingtype
    #// 
    #// @return string|int
    #//
    @classmethod
    def blocklacingtype(self, lacingtype=None):
        
        BlockLacingType = Array()
        if php_empty(lambda : BlockLacingType):
            BlockLacingType[0] = "no lacing"
            BlockLacingType[1] = "Xiph lacing"
            BlockLacingType[2] = "fixed-size lacing"
            BlockLacingType[3] = "EBML lacing"
        # end if
        return BlockLacingType[lacingtype] if (php_isset(lambda : BlockLacingType[lacingtype])) else lacingtype
    # end def blocklacingtype
    #// 
    #// @param string $codecid
    #// 
    #// @return string
    #//
    @classmethod
    def codecidtocommonname(self, codecid=None):
        
        CodecIDlist = Array()
        if php_empty(lambda : CodecIDlist):
            CodecIDlist["A_AAC"] = "aac"
            CodecIDlist["A_AAC/MPEG2/LC"] = "aac"
            CodecIDlist["A_AC3"] = "ac3"
            CodecIDlist["A_EAC3"] = "eac3"
            CodecIDlist["A_DTS"] = "dts"
            CodecIDlist["A_FLAC"] = "flac"
            CodecIDlist["A_MPEG/L1"] = "mp1"
            CodecIDlist["A_MPEG/L2"] = "mp2"
            CodecIDlist["A_MPEG/L3"] = "mp3"
            CodecIDlist["A_PCM/INT/LIT"] = "pcm"
            #// PCM Integer Little Endian
            CodecIDlist["A_PCM/INT/BIG"] = "pcm"
            #// PCM Integer Big Endian
            CodecIDlist["A_QUICKTIME/QDMC"] = "quicktime"
            #// Quicktime: QDesign Music
            CodecIDlist["A_QUICKTIME/QDM2"] = "quicktime"
            #// Quicktime: QDesign Music v2
            CodecIDlist["A_VORBIS"] = "vorbis"
            CodecIDlist["V_MPEG1"] = "mpeg"
            CodecIDlist["V_THEORA"] = "theora"
            CodecIDlist["V_REAL/RV40"] = "real"
            CodecIDlist["V_REAL/RV10"] = "real"
            CodecIDlist["V_REAL/RV20"] = "real"
            CodecIDlist["V_REAL/RV30"] = "real"
            CodecIDlist["V_QUICKTIME"] = "quicktime"
            #// Quicktime
            CodecIDlist["V_MPEG4/ISO/AP"] = "mpeg4"
            CodecIDlist["V_MPEG4/ISO/ASP"] = "mpeg4"
            CodecIDlist["V_MPEG4/ISO/AVC"] = "h264"
            CodecIDlist["V_MPEG4/ISO/SP"] = "mpeg4"
            CodecIDlist["V_VP8"] = "vp8"
            CodecIDlist["V_MS/VFW/FOURCC"] = "vcm"
            #// Microsoft (TM) Video Codec Manager (VCM)
            CodecIDlist["A_MS/ACM"] = "acm"
            pass
        # end if
        return CodecIDlist[codecid] if (php_isset(lambda : CodecIDlist[codecid])) else codecid
    # end def codecidtocommonname
    #// 
    #// @param int $value
    #// 
    #// @return string
    #//
    def ebmlidname(self, value=None):
        
        EBMLidList = Array()
        if php_empty(lambda : EBMLidList):
            EBMLidList[EBML_ID_ASPECTRATIOTYPE] = "AspectRatioType"
            EBMLidList[EBML_ID_ATTACHEDFILE] = "AttachedFile"
            EBMLidList[EBML_ID_ATTACHMENTLINK] = "AttachmentLink"
            EBMLidList[EBML_ID_ATTACHMENTS] = "Attachments"
            EBMLidList[EBML_ID_AUDIO] = "Audio"
            EBMLidList[EBML_ID_BITDEPTH] = "BitDepth"
            EBMLidList[EBML_ID_CHANNELPOSITIONS] = "ChannelPositions"
            EBMLidList[EBML_ID_CHANNELS] = "Channels"
            EBMLidList[EBML_ID_CHAPCOUNTRY] = "ChapCountry"
            EBMLidList[EBML_ID_CHAPLANGUAGE] = "ChapLanguage"
            EBMLidList[EBML_ID_CHAPPROCESS] = "ChapProcess"
            EBMLidList[EBML_ID_CHAPPROCESSCODECID] = "ChapProcessCodecID"
            EBMLidList[EBML_ID_CHAPPROCESSCOMMAND] = "ChapProcessCommand"
            EBMLidList[EBML_ID_CHAPPROCESSDATA] = "ChapProcessData"
            EBMLidList[EBML_ID_CHAPPROCESSPRIVATE] = "ChapProcessPrivate"
            EBMLidList[EBML_ID_CHAPPROCESSTIME] = "ChapProcessTime"
            EBMLidList[EBML_ID_CHAPSTRING] = "ChapString"
            EBMLidList[EBML_ID_CHAPTERATOM] = "ChapterAtom"
            EBMLidList[EBML_ID_CHAPTERDISPLAY] = "ChapterDisplay"
            EBMLidList[EBML_ID_CHAPTERFLAGENABLED] = "ChapterFlagEnabled"
            EBMLidList[EBML_ID_CHAPTERFLAGHIDDEN] = "ChapterFlagHidden"
            EBMLidList[EBML_ID_CHAPTERPHYSICALEQUIV] = "ChapterPhysicalEquiv"
            EBMLidList[EBML_ID_CHAPTERS] = "Chapters"
            EBMLidList[EBML_ID_CHAPTERSEGMENTEDITIONUID] = "ChapterSegmentEditionUID"
            EBMLidList[EBML_ID_CHAPTERSEGMENTUID] = "ChapterSegmentUID"
            EBMLidList[EBML_ID_CHAPTERTIMEEND] = "ChapterTimeEnd"
            EBMLidList[EBML_ID_CHAPTERTIMESTART] = "ChapterTimeStart"
            EBMLidList[EBML_ID_CHAPTERTRACK] = "ChapterTrack"
            EBMLidList[EBML_ID_CHAPTERTRACKNUMBER] = "ChapterTrackNumber"
            EBMLidList[EBML_ID_CHAPTERTRANSLATE] = "ChapterTranslate"
            EBMLidList[EBML_ID_CHAPTERTRANSLATECODEC] = "ChapterTranslateCodec"
            EBMLidList[EBML_ID_CHAPTERTRANSLATEEDITIONUID] = "ChapterTranslateEditionUID"
            EBMLidList[EBML_ID_CHAPTERTRANSLATEID] = "ChapterTranslateID"
            EBMLidList[EBML_ID_CHAPTERUID] = "ChapterUID"
            EBMLidList[EBML_ID_CLUSTER] = "Cluster"
            EBMLidList[EBML_ID_CLUSTERBLOCK] = "ClusterBlock"
            EBMLidList[EBML_ID_CLUSTERBLOCKADDID] = "ClusterBlockAddID"
            EBMLidList[EBML_ID_CLUSTERBLOCKADDITIONAL] = "ClusterBlockAdditional"
            EBMLidList[EBML_ID_CLUSTERBLOCKADDITIONID] = "ClusterBlockAdditionID"
            EBMLidList[EBML_ID_CLUSTERBLOCKADDITIONS] = "ClusterBlockAdditions"
            EBMLidList[EBML_ID_CLUSTERBLOCKDURATION] = "ClusterBlockDuration"
            EBMLidList[EBML_ID_CLUSTERBLOCKGROUP] = "ClusterBlockGroup"
            EBMLidList[EBML_ID_CLUSTERBLOCKMORE] = "ClusterBlockMore"
            EBMLidList[EBML_ID_CLUSTERBLOCKVIRTUAL] = "ClusterBlockVirtual"
            EBMLidList[EBML_ID_CLUSTERCODECSTATE] = "ClusterCodecState"
            EBMLidList[EBML_ID_CLUSTERDELAY] = "ClusterDelay"
            EBMLidList[EBML_ID_CLUSTERDURATION] = "ClusterDuration"
            EBMLidList[EBML_ID_CLUSTERENCRYPTEDBLOCK] = "ClusterEncryptedBlock"
            EBMLidList[EBML_ID_CLUSTERFRAMENUMBER] = "ClusterFrameNumber"
            EBMLidList[EBML_ID_CLUSTERLACENUMBER] = "ClusterLaceNumber"
            EBMLidList[EBML_ID_CLUSTERPOSITION] = "ClusterPosition"
            EBMLidList[EBML_ID_CLUSTERPREVSIZE] = "ClusterPrevSize"
            EBMLidList[EBML_ID_CLUSTERREFERENCEBLOCK] = "ClusterReferenceBlock"
            EBMLidList[EBML_ID_CLUSTERREFERENCEPRIORITY] = "ClusterReferencePriority"
            EBMLidList[EBML_ID_CLUSTERREFERENCEVIRTUAL] = "ClusterReferenceVirtual"
            EBMLidList[EBML_ID_CLUSTERSILENTTRACKNUMBER] = "ClusterSilentTrackNumber"
            EBMLidList[EBML_ID_CLUSTERSILENTTRACKS] = "ClusterSilentTracks"
            EBMLidList[EBML_ID_CLUSTERSIMPLEBLOCK] = "ClusterSimpleBlock"
            EBMLidList[EBML_ID_CLUSTERTIMECODE] = "ClusterTimecode"
            EBMLidList[EBML_ID_CLUSTERTIMESLICE] = "ClusterTimeSlice"
            EBMLidList[EBML_ID_CODECDECODEALL] = "CodecDecodeAll"
            EBMLidList[EBML_ID_CODECDOWNLOADURL] = "CodecDownloadURL"
            EBMLidList[EBML_ID_CODECID] = "CodecID"
            EBMLidList[EBML_ID_CODECINFOURL] = "CodecInfoURL"
            EBMLidList[EBML_ID_CODECNAME] = "CodecName"
            EBMLidList[EBML_ID_CODECPRIVATE] = "CodecPrivate"
            EBMLidList[EBML_ID_CODECSETTINGS] = "CodecSettings"
            EBMLidList[EBML_ID_COLOURSPACE] = "ColourSpace"
            EBMLidList[EBML_ID_CONTENTCOMPALGO] = "ContentCompAlgo"
            EBMLidList[EBML_ID_CONTENTCOMPRESSION] = "ContentCompression"
            EBMLidList[EBML_ID_CONTENTCOMPSETTINGS] = "ContentCompSettings"
            EBMLidList[EBML_ID_CONTENTENCALGO] = "ContentEncAlgo"
            EBMLidList[EBML_ID_CONTENTENCKEYID] = "ContentEncKeyID"
            EBMLidList[EBML_ID_CONTENTENCODING] = "ContentEncoding"
            EBMLidList[EBML_ID_CONTENTENCODINGORDER] = "ContentEncodingOrder"
            EBMLidList[EBML_ID_CONTENTENCODINGS] = "ContentEncodings"
            EBMLidList[EBML_ID_CONTENTENCODINGSCOPE] = "ContentEncodingScope"
            EBMLidList[EBML_ID_CONTENTENCODINGTYPE] = "ContentEncodingType"
            EBMLidList[EBML_ID_CONTENTENCRYPTION] = "ContentEncryption"
            EBMLidList[EBML_ID_CONTENTSIGALGO] = "ContentSigAlgo"
            EBMLidList[EBML_ID_CONTENTSIGHASHALGO] = "ContentSigHashAlgo"
            EBMLidList[EBML_ID_CONTENTSIGKEYID] = "ContentSigKeyID"
            EBMLidList[EBML_ID_CONTENTSIGNATURE] = "ContentSignature"
            EBMLidList[EBML_ID_CRC32] = "CRC32"
            EBMLidList[EBML_ID_CUEBLOCKNUMBER] = "CueBlockNumber"
            EBMLidList[EBML_ID_CUECLUSTERPOSITION] = "CueClusterPosition"
            EBMLidList[EBML_ID_CUECODECSTATE] = "CueCodecState"
            EBMLidList[EBML_ID_CUEPOINT] = "CuePoint"
            EBMLidList[EBML_ID_CUEREFCLUSTER] = "CueRefCluster"
            EBMLidList[EBML_ID_CUEREFCODECSTATE] = "CueRefCodecState"
            EBMLidList[EBML_ID_CUEREFERENCE] = "CueReference"
            EBMLidList[EBML_ID_CUEREFNUMBER] = "CueRefNumber"
            EBMLidList[EBML_ID_CUEREFTIME] = "CueRefTime"
            EBMLidList[EBML_ID_CUES] = "Cues"
            EBMLidList[EBML_ID_CUETIME] = "CueTime"
            EBMLidList[EBML_ID_CUETRACK] = "CueTrack"
            EBMLidList[EBML_ID_CUETRACKPOSITIONS] = "CueTrackPositions"
            EBMLidList[EBML_ID_DATEUTC] = "DateUTC"
            EBMLidList[EBML_ID_DEFAULTDURATION] = "DefaultDuration"
            EBMLidList[EBML_ID_DISPLAYHEIGHT] = "DisplayHeight"
            EBMLidList[EBML_ID_DISPLAYUNIT] = "DisplayUnit"
            EBMLidList[EBML_ID_DISPLAYWIDTH] = "DisplayWidth"
            EBMLidList[EBML_ID_DOCTYPE] = "DocType"
            EBMLidList[EBML_ID_DOCTYPEREADVERSION] = "DocTypeReadVersion"
            EBMLidList[EBML_ID_DOCTYPEVERSION] = "DocTypeVersion"
            EBMLidList[EBML_ID_DURATION] = "Duration"
            EBMLidList[EBML_ID_EBML] = "EBML"
            EBMLidList[EBML_ID_EBMLMAXIDLENGTH] = "EBMLMaxIDLength"
            EBMLidList[EBML_ID_EBMLMAXSIZELENGTH] = "EBMLMaxSizeLength"
            EBMLidList[EBML_ID_EBMLREADVERSION] = "EBMLReadVersion"
            EBMLidList[EBML_ID_EBMLVERSION] = "EBMLVersion"
            EBMLidList[EBML_ID_EDITIONENTRY] = "EditionEntry"
            EBMLidList[EBML_ID_EDITIONFLAGDEFAULT] = "EditionFlagDefault"
            EBMLidList[EBML_ID_EDITIONFLAGHIDDEN] = "EditionFlagHidden"
            EBMLidList[EBML_ID_EDITIONFLAGORDERED] = "EditionFlagOrdered"
            EBMLidList[EBML_ID_EDITIONUID] = "EditionUID"
            EBMLidList[EBML_ID_FILEDATA] = "FileData"
            EBMLidList[EBML_ID_FILEDESCRIPTION] = "FileDescription"
            EBMLidList[EBML_ID_FILEMIMETYPE] = "FileMimeType"
            EBMLidList[EBML_ID_FILENAME] = "FileName"
            EBMLidList[EBML_ID_FILEREFERRAL] = "FileReferral"
            EBMLidList[EBML_ID_FILEUID] = "FileUID"
            EBMLidList[EBML_ID_FLAGDEFAULT] = "FlagDefault"
            EBMLidList[EBML_ID_FLAGENABLED] = "FlagEnabled"
            EBMLidList[EBML_ID_FLAGFORCED] = "FlagForced"
            EBMLidList[EBML_ID_FLAGINTERLACED] = "FlagInterlaced"
            EBMLidList[EBML_ID_FLAGLACING] = "FlagLacing"
            EBMLidList[EBML_ID_GAMMAVALUE] = "GammaValue"
            EBMLidList[EBML_ID_INFO] = "Info"
            EBMLidList[EBML_ID_LANGUAGE] = "Language"
            EBMLidList[EBML_ID_MAXBLOCKADDITIONID] = "MaxBlockAdditionID"
            EBMLidList[EBML_ID_MAXCACHE] = "MaxCache"
            EBMLidList[EBML_ID_MINCACHE] = "MinCache"
            EBMLidList[EBML_ID_MUXINGAPP] = "MuxingApp"
            EBMLidList[EBML_ID_NAME] = "Name"
            EBMLidList[EBML_ID_NEXTFILENAME] = "NextFilename"
            EBMLidList[EBML_ID_NEXTUID] = "NextUID"
            EBMLidList[EBML_ID_OUTPUTSAMPLINGFREQUENCY] = "OutputSamplingFrequency"
            EBMLidList[EBML_ID_PIXELCROPBOTTOM] = "PixelCropBottom"
            EBMLidList[EBML_ID_PIXELCROPLEFT] = "PixelCropLeft"
            EBMLidList[EBML_ID_PIXELCROPRIGHT] = "PixelCropRight"
            EBMLidList[EBML_ID_PIXELCROPTOP] = "PixelCropTop"
            EBMLidList[EBML_ID_PIXELHEIGHT] = "PixelHeight"
            EBMLidList[EBML_ID_PIXELWIDTH] = "PixelWidth"
            EBMLidList[EBML_ID_PREVFILENAME] = "PrevFilename"
            EBMLidList[EBML_ID_PREVUID] = "PrevUID"
            EBMLidList[EBML_ID_SAMPLINGFREQUENCY] = "SamplingFrequency"
            EBMLidList[EBML_ID_SEEK] = "Seek"
            EBMLidList[EBML_ID_SEEKHEAD] = "SeekHead"
            EBMLidList[EBML_ID_SEEKID] = "SeekID"
            EBMLidList[EBML_ID_SEEKPOSITION] = "SeekPosition"
            EBMLidList[EBML_ID_SEGMENT] = "Segment"
            EBMLidList[EBML_ID_SEGMENTFAMILY] = "SegmentFamily"
            EBMLidList[EBML_ID_SEGMENTFILENAME] = "SegmentFilename"
            EBMLidList[EBML_ID_SEGMENTUID] = "SegmentUID"
            EBMLidList[EBML_ID_SIMPLETAG] = "SimpleTag"
            EBMLidList[EBML_ID_CLUSTERSLICES] = "ClusterSlices"
            EBMLidList[EBML_ID_STEREOMODE] = "StereoMode"
            EBMLidList[EBML_ID_OLDSTEREOMODE] = "OldStereoMode"
            EBMLidList[EBML_ID_TAG] = "Tag"
            EBMLidList[EBML_ID_TAGATTACHMENTUID] = "TagAttachmentUID"
            EBMLidList[EBML_ID_TAGBINARY] = "TagBinary"
            EBMLidList[EBML_ID_TAGCHAPTERUID] = "TagChapterUID"
            EBMLidList[EBML_ID_TAGDEFAULT] = "TagDefault"
            EBMLidList[EBML_ID_TAGEDITIONUID] = "TagEditionUID"
            EBMLidList[EBML_ID_TAGLANGUAGE] = "TagLanguage"
            EBMLidList[EBML_ID_TAGNAME] = "TagName"
            EBMLidList[EBML_ID_TAGTRACKUID] = "TagTrackUID"
            EBMLidList[EBML_ID_TAGS] = "Tags"
            EBMLidList[EBML_ID_TAGSTRING] = "TagString"
            EBMLidList[EBML_ID_TARGETS] = "Targets"
            EBMLidList[EBML_ID_TARGETTYPE] = "TargetType"
            EBMLidList[EBML_ID_TARGETTYPEVALUE] = "TargetTypeValue"
            EBMLidList[EBML_ID_TIMECODESCALE] = "TimecodeScale"
            EBMLidList[EBML_ID_TITLE] = "Title"
            EBMLidList[EBML_ID_TRACKENTRY] = "TrackEntry"
            EBMLidList[EBML_ID_TRACKNUMBER] = "TrackNumber"
            EBMLidList[EBML_ID_TRACKOFFSET] = "TrackOffset"
            EBMLidList[EBML_ID_TRACKOVERLAY] = "TrackOverlay"
            EBMLidList[EBML_ID_TRACKS] = "Tracks"
            EBMLidList[EBML_ID_TRACKTIMECODESCALE] = "TrackTimecodeScale"
            EBMLidList[EBML_ID_TRACKTRANSLATE] = "TrackTranslate"
            EBMLidList[EBML_ID_TRACKTRANSLATECODEC] = "TrackTranslateCodec"
            EBMLidList[EBML_ID_TRACKTRANSLATEEDITIONUID] = "TrackTranslateEditionUID"
            EBMLidList[EBML_ID_TRACKTRANSLATETRACKID] = "TrackTranslateTrackID"
            EBMLidList[EBML_ID_TRACKTYPE] = "TrackType"
            EBMLidList[EBML_ID_TRACKUID] = "TrackUID"
            EBMLidList[EBML_ID_VIDEO] = "Video"
            EBMLidList[EBML_ID_VOID] = "Void"
            EBMLidList[EBML_ID_WRITINGAPP] = "WritingApp"
        # end if
        return EBMLidList[value] if (php_isset(lambda : EBMLidList[value])) else dechex(value)
    # end def ebmlidname
    #// 
    #// @param int $value
    #// 
    #// @return string
    #//
    @classmethod
    def displayunit(self, value=None):
        
        units = Array({0: "pixels", 1: "centimeters", 2: "inches", 3: "Display Aspect Ratio"})
        return units[value] if (php_isset(lambda : units[value])) else "unknown"
    # end def displayunit
    #// 
    #// @param array $streams
    #// 
    #// @return array
    #//
    def getdefaultstreaminfo(self, streams=None):
        
        stream = Array()
        for stream in array_reverse(streams):
            if stream["default"]:
                break
            # end if
        # end for
        unset = Array("default", "name")
        for u in unset:
            if (php_isset(lambda : stream[u])):
                stream[u] = None
            # end if
        # end for
        info = stream
        info["streams"] = streams
        return info
    # end def getdefaultstreaminfo
# end class getid3_matroska
