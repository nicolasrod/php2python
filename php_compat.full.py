def gmdate(x): pass
def php_php_addcslashes(_str, _charlist="\\'\!\0"): pass
def php_array_merge_recursive(*args): pass
def php_array_reduce(_array,_callback,_initial=None,_carry=None,_item=None): pass
def php_array_replace_recursive(_array1, *args): pass
def php_array_reverse(_array, _preserve_keys=False): pass
def php_array_splice(_input, _offset, _length=None, _replacement=[]): pass
def php_array_sum(_array): pass
def php_array_unique(_array, _sort_flags=SORT_STRING): pass
def php_array_unshift(_array, *args): pass
def php_array_walk(_array, _callback, _userdata=None): pass
def php_arsort(_array, _sort_flags=SORT_REGULAR): pass
def php_asort(_array, _sort_flags=SORT_REGULAR): pass
def php_assert(_assertion, _description): pass
def php_base_convert(_number, _frombase, _tobase): pass
def php_bin2hex(_str): pass
def php_bindec(_binary_string): pass
def php_ceil(_value): pass
def php_chgrp(_filename, _group): pass
def php_chmod(_filename, _mode): pass
def php_chown(_filename, _user): pass
def php_chr(_bytevalue): pass
def php_chunk_split(_body, _chunklen=76, _end="\r\n"): pass
def php_class_exists(_class_name, _autoload=True): pass
def php_clearstatcache(_clear_realpath_cache=False, _filename=None): pass
def php_constant(_name): pass
def php_copy(_source, _dest, _context): pass
def php_count_chars(_string, _mode=0): pass
def php_crc32(_str): pass
def php_crypt(_str, _salt): pass
def php_ctype_alnum(_text): pass
def php_ctype_digit(_text): pass
def php_curl_close(_ch): pass
def php_curl_errno(_ch): pass
def php_curl_error(_ch): pass
def php_curl_exec(_ch): pass
def php_curl_getinfo(_ch, _opt): pass
def php_curl_init(_url=None): pass
def php_curl_multi_add_handle(_mh, _ch): pass
def php_curl_multi_close(_mh): pass
def php_curl_multi_exec(_mh, _still_running): pass
def php_curl_multi_info_read(_mh, _msgs_in_queue=None): pass
def php_curl_multi_init(): pass
def php_curl_multi_remove_handle(_mh, _ch): pass
def php_curl_setopt(_ch, _option, _value): pass
def php_curl_version(_age=CURLVERSION_NOW): pass
def php_current(_array): pass
def php_date(_format, _timestamp=None): pass
def php_debug_backtrace(_options=DEBUG_BACKTRACE_PROVIDE_OBJECT, _limit=0): pass
def php_decbin(_number): pass
def php_dechex(_number): pass
def php_decoct(_number): pass
def php_dir(_directory, _context): pass
def php_disk_free_space(_directory): pass
def php_error_get_last(): pass
def php_error_log(_message,_message_type=0,_destination=None,_extra_headers=None): pass
def php_escapeshellarg(_arg): pass
def php_escapeshellcmd(_command): pass
def php_exif_imagetype(_filename): pass
def php_exif_read_data(_stream,_sections=None,_arrays=False,_thumbnail=False): pass
def php_extract(_array, _flags=EXTR_OVERWRITE, _prefix=None): pass
def php_fastcgi_finish_request(): pass
def php_file(_filename, _flags=0, _context=None): pass
def php_fileatime(_filename): pass
def php_filegroup(_filename): pass
def php_filemtime(_filename): pass
def php_fileowner(_filename): pass
def php_fileperms(_filename): pass
def php_file_put_contents(_filename, _data, _flags=0, _context=None): pass
def php_filesize(_filename): pass
def php_filter_var(_variable, _filter=FILTER_DEFAULT, _options=None): pass
def php_finfo_close(_finfo): pass
def php_finfo_file(_finfo, _file_name, _options=FILEINFO_NONE, _context=None): pass
def php_finfo_open(_options=FILEINFO_NONE, _magic_file=""): pass
def php_floatval(_var): pass
def php_flock(_handle, _operation, _wouldblock): pass
def php_floor(_value): pass
def php_flush(): pass
def php_fopen(_filename, _mode, _use_include_path=False, _context=None): pass
def php_fread(_handle, _length): pass
def php_fseek(_handle, _offset, _whence=SEEK_SET): pass
def php_fsockopen(_hostname,_port=-1,_errno=None,_errstr=None,_timeout=None): pass
def php_fstat(_handle): pass
def php_ftell(_handle): pass
def php_ftp_chdir(_ftp_stream, _directory): pass
def php_ftp_chmod(_ftp_stream, _mode, _filename): pass
def php_ftp_close(_ftp_stream): pass
def php_ftp_connect(_host, _port=21, _timeout=90): pass
def php_ftp_delete(_ftp_stream, _path): pass
def php_ftp_fget(_ftp_stream,_handle,_remote_file,_mode=FTP_BINARY,_resumepos=0): pass
def php_ftp_fput(_ftp_stream,_remote_file,_handle,_mode=FTP_BINARY,_startpos=0): pass
def php_ftp_get_option(_ftp_stream, _option): pass
def php_ftp_login(_ftp_stream, _username, _password): pass
def php_ftp_mdtm(_ftp_stream, _remote_file): pass
def php_ftp_mkdir(_ftp_stream, _directory): pass
def php_ftp_nlist(_ftp_stream, _directory): pass
def php_ftp_pasv(_ftp_stream, _pasv): pass
def php_ftp_pwd(_ftp_stream): pass
def php_ftp_rawlist(_ftp_stream, _directory, _recursive=False): pass
def php_ftp_rename(_ftp_stream, _oldname, _newname): pass
def php_ftp_rmdir(_ftp_stream, _directory): pass
def php_ftp_set_option(_ftp_stream, _option, _value): pass
def php_ftp_site(_ftp_stream, _command): pass
def php_ftp_size(_ftp_stream, _remote_file): pass
def php_ftp_ssl_connect(_host, _port=21, _timeout=90): pass
def php_ftp_systype(_ftp_stream): pass
def php_ftruncate(_handle, _size):passdef php_fwrite(_handle, _string, _length): pass
def php_gc_enabled(): pass
def php_gd_info(): pass
def php_get_class(_object): pass
def php_get_class_methods(_class_name): pass
def php_getdate(_timestamp=None): pass
def php_get_defined_constants(_categorize=False): pass
def php_gethostbyaddr(_ip_address): pass
def php_gethostbyname(_hostname): pass
def php_gethostbynamel(_hostname): pass
def php_gethostname(): pass
def php_get_html_translation_table(_table=HTML_SPECIALCHARS,_flags=ENT_COMPAT | ENT_HTML401,_encoding="UTF-8"): pass
def php_getimagesize(_filename, _imageinfo): pass
def php_get_magic_quotes_runtime(): pass
def php_get_object_vars(_object): pass
def php_get_resource_type(_handle): pass
def php_gettype(_var): pass
def php_glob(_pattern, _flags=0): pass
def php_gmdate(_format, _timestamp=None): pass
def php_gmmktime(_hour=gmdate("H"),_minute=gmdate("i"),_second=gmdate("s"),_month=gmdate("n"),_day=gmdate("j"),_year=gmdate("Y"),_is_dst=-1): pass
def php_gzclose(_zp): pass
def php_gzdecode(_data, _length): pass
def php_gzdeflate(_data, _level=-1, _encoding=ZLIB_ENCODING_RAW): pass
def php_gzencode(_data, _level=-1, _encoding_mode=FORCE_GZIP): pass
def php_gzinflate(_data, _length=0): pass
def php_gzopen(_filename, _mode, _use_include_path=0): pass
def php_gzread(_zp, _length): pass
def php_gzuncompress(_data, _length=0): pass
def php_gzwrite(_zp, _string, _length): pass
def php_hash(_algo, _data, _raw_output=False): pass
def php_hash_algos(): pass
def php_hash_equals(_known_string, _user_string): pass
def php_hash_file(_algo, _filename, _raw_output=False): pass
def php_hash_final(_context, _raw_output=False): pass
def php_hash_hmac(_algo, _data, _key, _raw_output=False): pass
def php_hash_init(_algo, _options=0, _key=None): pass
def php_hash_update(_context, _data): pass
def php_hexdec(_hex_string): pass
def php_htmlentities(_string,_flags=ENT_COMPAT | ENT_HTML401,_encoding="UTF-8",_double_encode=True): pass
def php_html_entity_decode(_string,_flags=ENT_COMPAT | ENT_HTML401,_encoding="UTF-8"): pass
def php_htmlspecialchars(_string,_flags=ENT_COMPAT | ENT_HTML401,_encoding="UTF-8",_double_encode=True): pass
def php_htmlspecialchars_decode(_string, _flags=ENT_COMPAT | ENT_HTML401): pass
def php_http_build_query(_query_data,_numeric_prefix,_arg_separator,_enc_type=PHP_QUERY_RFC1738): pass
def php_iconv(_in_charset, _out_charset, _str): pass
def php_iconv_mime_decode(_encoded_header, _mode=0, _charset="UTF-8"): pass
def php_idn_to_ascii(_domain,_options=IDNA_DEFAULT,_variant=INTL_IDNA_VARIANT_UTS46,_idna_info=None): pass
def php_ignore_user_abort(_value): pass
def php_imagealphablending(_image, _blendmode): pass
def php_imageantialias(_image, _enabled): pass
def php_imagecolorallocatealpha(_image, _red, _green, _blue, _alpha): pass
def php_imagecolorstotal(_image): pass
def php_imagecopy(_dst_im, _src_im, _dst_x, _dst_y, _src_x, _src_y, _src_w,_src_h): pass
def php_imagecopyresampled(_dst_image, _src_image, _dst_x, _dst_y, _src_x,_src_y, _dst_w, _dst_h, _src_w, _src_h): pass
def php_imagecreatefromgif(_filename): pass
def php_imagecreatefromjpeg(_filename): pass
def php_imagecreatefrompng(_filename): pass
def php_imagecreatefromstring(_image): pass
def php_imagecreatetruecolor(_width, _height): pass
def php_imagedestroy(_image): pass
def php_imagegif(_image, _to=None): pass
def php_imageistruecolor(_image): pass
def php_imagejpeg(_image, _to=None, _quality=-1): pass
def php_imagepng(_image, _to=None, _quality=-1, _filters=-1): pass
def php_imagerotate(_image, _angle, _bgd_color, _ignore_transparent=0): pass
def php_imagesavealpha(_image, _saveflag): pass
def php_imagesx(_image): pass
def php_imagesy(_image): pass
def php_imagetruecolortopalette(_image, _dither, _ncolors): pass
def php_imagetypes(): pass
def php_image_type_to_mime_type(_imagetype): pass
def php_imap_rfc822_parse_adrlist(_address, _default_host): pass
def php_inet_ntop(_in_addr): pass
def php_inet_pton(_address): pass
def php_ip2long(_ip_address): pass
def php_iptcparse(_iptcblock): pass
def php_is_a(_object, _class_name, _allow_string=False): pass
def php_is_executable(_filename): pass
def php_is_nan(_val): pass
def php_is_resource(_var): pass
def php_is_scalar(_var): pass
def php_is_subclass_of(_object, _class_name, _allow_string=True): pass
def php_is_uploaded_file(_filename): pass
def php_json_last_error_msg(): pass
def php_key(_array): pass
def php_krsort(_array, _sort_flags=SORT_REGULAR): pass
def php_ksort(_array, _sort_flags=SORT_REGULAR): pass
def php_libxml_clear_errors(): pass
def php_libxml_disable_entity_loader(_disable=True): pass
def php_libxml_get_last_error(): pass
def php_libxml_use_internal_errors(_use_errors=False): pass
def php_log(_arg, _base=M_E): pass
def php_log10(_arg): pass
def php_long2ip(_proper_address): pass
def php_mail(_to, _subject, _message, _additional_headers,_additional_parameters): pass
def php_mb_check_encoding(_var=None, _encoding="UTF-8"): pass
def php_mb_convert_encoding(_val, _to_encoding, _from_encoding="UTF-8"): pass
def php_mb_detect_encoding(_str, _encoding_list=None, _strict=False): pass
def php_mb_detect_order(_encoding_list=None): pass
def php_mb_get_info(_type="all"): pass
def php_mb_internal_encoding(_encoding="UTF-8"): pass
def php_mb_list_encodings(): pass
def php_mcrypt_create_iv(_size, _source=MCRYPT_DEV_URANDOM): pass
def php_mime_content_type(_filename): pass
def php_mkdir(_pathname, _mode=0o777, _recursive=False, _context=None): pass
def php_mktime(_hour=date("H"), _minute=date("i"), _second=date("s"),_month=date("n"), _day=date("j"), _year=date("Y"),_is_dst=-1): pass
def php_move_uploaded_file(_filename, _destination): pass
def php_mt_rand(_min=None, _max=None): pass
def php_mysql_client_encoding(_link_identifier=None): pass
def php_mysql_close(_link_identifier=None): pass
def php_mysql_ping(_link_identifier=None): pass
def php_mysql_set_charset(_charset, _link_identifier=None): pass
def php_natcasesort(_array): pass
def php_natsort(_array): pass
def php_next(_array): pass
def php_number_format(_number=None, _decimals=0,_dec_point=".", _thousands_sep=","): pass
def php_ob_clean(): pass
def php_ob_end_clean(): pass
def php_ob_end_flush(): pass
def php_ob_get_clean(): pass
def php_ob_get_contents(): pass
def php_ob_get_flush(): pass
def php_ob_get_length(): pass
def php_ob_get_level(): pass
def php_ob_start(_output_callback=None, _chunk_size=0, _flags=PHP_OUTPUT_HANDLER_STDFLAGS,_buffer=None,_phase=None): pass
def php_opcache_invalidate(_script, _force=False): pass
def php_openssl_decrypt(_data,_method,_key,_options=0,_iv="",_tag="",_aad=""): pass
def php_openssl_encrypt(_data,_method,_key,_options=0,_iv="",_tag=None,_aad="",_tag_length=16): pass
def php_openssl_error_string(): pass
def php_openssl_get_cipher_methods(_aliases=False): pass
def php_openssl_get_md_methods(_aliases=False): pass
def php_openssl_pkcs7_sign(_infilename,_outfilename,_signcert,_privkey,_headers,_flags=PKCS7_DETACHED,_extracerts=None): pass
def php_openssl_pkey_free(_key): pass
def php_openssl_pkey_get_details(_key): pass
def php_openssl_pkey_get_private(_key, _passphrase=""): pass
def php_openssl_private_encrypt(_data, _crypted, _key,_padding=OPENSSL_PKCS1_PADDING): pass
def php_openssl_sign(_data, _signature, _priv_key_id,_signature_alg=OPENSSL_ALGO_SHA1):pass
def php_openssl_x509_parse(_x509cert, _shortnames=True): pass
def php_pack(_format, *args): pass
def php_parse_str(_encoded_string, _result): pass
def php_pathinfo(_path,_options=PATHINFO_DIRNAME | PATHINFO_BASENAME| PATHINFO_EXTENSION | PATHINFO_FILENAME): pass
def php_pclose(_handle): pass
def php_phpinfo(_what=INFO_ALL): pass
def php_php_uname(_mode="a"): pass
def php_popen(_command, _mode): pass
def php_posix_getgrgid(_gid): pass
def php_posix_getpwuid(_uid): pass
def php_pow(_base, _exp): pass
def php_preg_match_all(_pattern, _subject, _matches, _flags=PREG_PATTERN_ORDER,_offset=0): pass
def php_preg_quote(_str, _delimiter=None): pass
def php_preg_replace_callback(_pattern, _callback, _subject,_limit=-1, _count=None,_matches=None): pass
def php_printf(_format, *args): pass
def php_print_r(_expression, _return=False): pass
def php_property_exists(_class, _property): pass
def php_quoted_printable_decode(_str): pass
def php_quoted_printable_encode(_str): pass
def php_rand(_min=None, _max=None): pass
def php_random_bytes(_length): pass
def php_random_int(_min, _max): pass
def php_range(_start, _end, _step=1): pass
def php_rawurldecode(_str): pass
def php_rawurlencode(_str): pass
def php_readfile(_filename, _use_include_path=False, _context=None): pass
def php_register_shutdown_function(_callback, *args): pass
def php_rename(_oldname, _newname, _context): pass
def php_reset(_array): pass
def php_restore_error_handler(): pass
def php_rewind(_handle): pass
def php_rmdir(_dirname, _context): pass
def php_round(_val, _precision=0, _mode=PHP_ROUND_HALF_UP): pass
def php_rsort(_array, _sort_flags=SORT_REGULAR): pass
def php_scandir(_directory, _sorting_order=SCANDIR_SORT_ASCENDING, _context=None): pass
def php_serialize(_value): pass
def php_setcookie(_name, _value="",_expires=0,_path="",_domain="",_secure=False,_httponly=False): pass
def php_set_error_handler(_error_handler,_error_types=None,_errno=None,_errstr=None,_errfile=None,_errline=None,_errcontext=None):pass
def php_setlocale(_category, _locale, *args): pass
def php_set_magic_quotes_runtime(_new_setting): pass
def php_set_time_limit(_seconds): pass
def php_settype(_var, _type): pass
def php_sha1(_str, _raw_output=False): pass
def php_sha1_file(_filename, _raw_output=False): pass
def php_shuffle(_array): pass
def php_simplexml_import_dom(_node, _class_name="SimpleXMLElement"): pass
def php_simplexml_load_string(_data,_class_name="SimpleXMLElement",_options=0,_ns="",_is_prefix=False): pass
def php_sleep(_seconds): pass
def php_socket_accept(_socket): pass
def php_socket_bind(_socket, _address, _port=0): pass
def php_socket_close(_socket): pass
def php_socket_connect(_socket, _address, _port=0): pass
def php_socket_create(_domain, _type, _protocol): pass
def php_socket_getsockname(_socket, _addr, _port): pass
def php_socket_last_error(_socket): pass
def php_socket_listen(_socket, _backlog=0): pass
def php_socket_read(_socket, _length, _type=PHP_BINARY_READ): pass
def php_socket_set_option(_socket, _level, _optname, _optval): pass
def php_socket_strerror(_errno): pass
def php_socket_write(_socket, _buffer, _length=0): pass
def php_sodium_bin2hex(_bin): pass
def php_sodium_compare(_buf1, _buf2): pass
def php_sodium_crypto_aead_aes256gcm_is_available(): pass
def php_sodium_crypto_aead_chacha20poly1305_decrypt(_ciphertext, _ad, _nonce,_key): pass
def php_sodium_crypto_aead_chacha20poly1305_encrypt(_msg, _ad, _nonce, _key): pass
def php_sodium_crypto_aead_chacha20poly1305_ietf_decrypt(   _ciphertext, _ad, _nonce, _key): pass
def php_sodium_crypto_aead_chacha20poly1305_ietf_encrypt( _msg, _ad, _nonce, _key): pass
def php_sodium_crypto_aead_xchacha20poly1305_ietf_decrypt( _ciphertext, _ad, _nonce, _key): pass
def php_sodium_crypto_aead_xchacha20poly1305_ietf_encrypt(_msg, _ad, _nonce, _key): pass
def php_sodium_crypto_auth(_msg, _key): pass
def php_sodium_crypto_auth_verify(_signature, _msg, _key): pass
def php_sodium_crypto_box(_msg, _nonce, _key): pass
def php_sodium_crypto_box_keypair(): pass
def php_sodium_crypto_box_keypair_from_secretkey_and_publickey( _secret_key, _public_key): pass
def php_sodium_crypto_box_open(_ciphertext, _nonce, _key): pass
def php_sodium_crypto_box_publickey(_key): pass
def php_sodium_crypto_box_publickey_from_secretkey(_key): pass
def php_sodium_crypto_box_seal(_msg, _key): pass
def php_sodium_crypto_box_seal_open(_ciphertext, _key): pass
def php_sodium_crypto_box_secretkey(_key): pass
def php_sodium_crypto_box_seed_keypair(_key): pass
def php_sodium_crypto_generichash(_msg, _key,_length=SODIUM_CRYPTO_GENERICHASH_BYTES): pass
def php_sodium_crypto_generichash_final(_state,_length=SODIUM_CRYPTO_GENERICHASH_BYTES): pass
def php_sodium_crypto_generichash_init(_key,_length=SODIUM_CRYPTO_GENERICHASH_BYTES): pass
def php_sodium_crypto_generichash_update(_state, _msg): pass
def php_sodium_crypto_pwhash(_length, _password, _salt, _opslimit, _memlimit,_alg): pass
def php_sodium_crypto_pwhash_scryptsalsa208sha256(_length, _password, _salt,_opslimit, _memlimit): pass
def php_sodium_crypto_pwhash_scryptsalsa208sha256_str(_password, _opslimit,_memlimit): pass
def php_sodium_crypto_pwhash_scryptsalsa208sha256_str_verify(_hash, _password): pass
def php_sodium_crypto_pwhash_str(_password, _opslimit, _memlimit): pass
def php_sodium_crypto_pwhash_str_verify(_hash, _password): pass
def php_sodium_crypto_scalarmult(_n, _p): pass
def php_sodium_crypto_secretbox(_string, _nonce, _key): pass
def php_sodium_crypto_secretbox_open(_ciphertext, _nonce, _key): pass
def php_sodium_crypto_shorthash(_msg, _key): pass
def php_sodium_crypto_sign(_msg, _secret_key): pass
def php_sodium_crypto_sign_detached(_msg, _secretkey): pass
def php_sodium_crypto_sign_ed25519_pk_to_curve25519(_key): pass
def php_sodium_crypto_sign_ed25519_sk_to_curve25519(_key): pass
def php_sodium_crypto_sign_keypair(): pass
def php_sodium_crypto_sign_keypair_from_secretkey_and_publickey(_secret_key, _public_key): pass
def php_sodium_crypto_sign_open(_string, _public_key): pass
def php_sodium_crypto_sign_publickey(_keypair): pass
def php_sodium_crypto_sign_publickey_from_secretkey(_key): pass
def php_sodium_crypto_sign_secretkey(_key): pass
def php_sodium_crypto_sign_seed_keypair(_key): pass
def php_sodium_crypto_sign_verify_detached(_signature, _msg, _public_key): pass
def php_sodium_crypto_stream(_length, _nonce, _key): pass
def php_sodium_crypto_stream_xor(_msg, _nonce, _key): pass
def php_sodium_hex2bin(_hex, _ignore): pass
def php_sodium_increment(_val): pass
def php_sodium_memcmp(_buf1, _buf2): pass
def php_sodium_memzero(_buf): pass
def php_sodium_pad(_unpadded, _length): pass
def php_sodium_unpad(_padded, _length): pass
def php_sort(_array, _sort_flags=SORT_REGULAR): pass
def php_spl_object_hash(_obj): pass
def php_sscanf(_str, _format, *args): pass
def php_ssh2_auth_password(_session, _username, _password): pass
def php_ssh2_auth_pubkey_file(_session, _username, _pubkeyfile, _privkeyfile,_passphrase): pass
def php_ssh2_connect(_host, _port=22, _methods=None, _callbacks=None): pass
def php_ssh2_exec(_session,_command,_pty,_env,_width=80,_height=25,_width_height_type=SSH2_TERM_UNIT_CHARS): pass
def php_ssh2_sftp(_session): pass
def php_ssh2_sftp_mkdir(_sftp, _dirname, _mode=0o777, _recursive=False): pass
def php_ssh2_sftp_realpath(_sftp, _filename): pass
def php_ssh2_sftp_rename(_sftp, _from, _to): pass
def php_ssh2_sftp_rmdir(_sftp, _dirname): pass
def php_ssh2_sftp_unlink(_sftp, _filename): pass
def php_stat(_filename): pass
def php_strcasecmp(_str1, _str2): pass
def php_strcmp(_str1, _str2): pass
def php_strcspn(_subject, _mask, _start, _length): pass
def php_stream_context_create(_options, _params): pass
def php_stream_context_get_options(_stream_or_context): pass
def php_stream_context_set_option(_stream_or_context, *args): pass
def php_stream_get_contents(_handle, _maxlength=-1, _offset=-1): pass
def php_stream_get_meta_data(_stream): pass
def php_stream_get_wrappers(): pass
def php_stream_set_blocking(_stream, _mode): pass
def php_stream_set_chunk_size(_fp, _chunk_size): pass
def php_stream_set_read_buffer(_stream, _buffer): pass
def php_stream_set_timeout(_stream, _seconds, _microseconds=0): pass
def php_stream_socket_client(_remote_socket,_errno,_errstr,_timeout=None,_flags=STREAM_CLIENT_CONNECT,_context=None): pass
def php_stream_socket_enable_crypto(_stream, _enable, _crypto_type,_session_stream): pass
def php_strftime(_format, _timestamp=None): pass
def php_stripcslashes(_str): pass
def php_stripos(_haystack, _needle, _offset=0): pass
def php_stripslashes(_str): pass
def php_strip_tags(_str, _allowable_tags): pass
def php_str_ireplace(_search, _replace, _subject, _count): pass
def php_stristr(_haystack, _needle, _before_needle=False): pass
def php_strlen(_string): pass
def php_strnatcasecmp(_str1, _str2): pass
def php_strncmp(_str1, _str2, _len): pass
def php_str_pad(_input, _pad_length, _pad_string=" ", _pad_type=STR_PAD_RIGHT): pass
def php_strpbrk(_haystack, _char_list): pass
def php_strpos(_haystack, _needle, _offset=0): pass
def php_strrchr(_haystack, _needle): pass
def php_str_split(_string, _split_length=1): pass
def php_strspn(_subject, _mask, _start, _length): pass
def php_strtok(*args): pass
def php_strtotime(_time, _now=None): pass
def php_strtr(_str, *args): pass
def php_substr_replace(_string, _replacement, _start, _length): pass
def php_time(): pass
def php_token_get_all(_source, _flags=0): pass
def php_touch(_filename, _time=None, _atime=None): pass
def php_trigger_error(_error_msg, _error_type=E_USER_NOTICE): pass
def php_uasort(_array, _value_compare_func): pass
def php_ucfirst(_str): pass
def php_ucwords(_str, _delimiters=" \t\r\n\f\v"): pass
def php_uksort(_array, _key_compare_func, _a, _b): pass
def php_umask(_mask=None): pass
def php_uniqid(_prefix="", _more_entropy=False): pass
def php_unlink(_filename, _context): pass
def php_unpack(_format, _data, _offset=0): pass
def php_unserialize(_str, _options): pass
def php_urldecode(_str): pass
def php_urlencode(_str): pass
def php_usort(_array, _value_compare_func, _a, _b): pass
def php_utf8_decode(_data): pass
def php_utf8_encode(_data): pass
def php_var_export(_expression, _return=False): pass
def php_version_compare(_version1, _version2, _operator=None): pass
def php_vsprintf(_format, _args): pass
def php_wordwrap(_str, _width=75, _break="\n", _cut=False): pass
def php_xdiff_string_diff(_old_data, _new_data, _context=3, _minimal=False): pass
def php_xml_error_string(_code): pass
def php_xml_get_current_byte_index(_parser): pass
def php_xml_get_current_column_number(_parser): pass
def php_xml_get_current_line_number(_parser): pass
def php_xml_get_error_code(_parser): pass
def php_xml_parse(_parser, _data, _is_final=False): pass
def php_xml_parse_into_struct(_parser, _data, _values, _index): pass
def php_xml_parser_create(_encoding): pass
def php_xml_parser_create_ns(_encoding, _separator=":"): pass
def php_xml_parser_free(_parser): pass
def php_xml_parser_set_option(_parser, _option, _value): pass
def php_xml_set_character_data_handler(_parser, _handler): pass
def php_xml_set_default_handler(_parser, _handler): pass
def php_xml_set_element_handler(_parser, _start_element_handler,_end_element_handler): pass
def php_xml_set_end_namespace_decl_handler(_parser, _handler): pass
def php_xml_set_object(_parser, _object): pass
def php_xml_set_start_namespace_decl_handler(_parser, _handler): pass
def php_session_name(name): pass
def php_session_set_cookie_params(p1, p2, p3, p4, p5): pass
def php_session_start(): pass
