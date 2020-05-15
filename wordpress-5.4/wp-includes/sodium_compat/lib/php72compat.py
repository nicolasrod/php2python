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
php_include_file(php_dirname(php_dirname(__FILE__)) + "/autoload.php", once=True)
#// 
#// This file will monkey patch the pure-PHP implementation in place of the
#// PECL functions and constants, but only if they do not already exist.
#// 
#// Thus, the functions or constants just proxy to the appropriate
#// ParagonIE_Sodium_Compat method or class constant, respectively.
#//
for constant in Array("BASE64_VARIANT_ORIGINAL", "BASE64_VARIANT_ORIGINAL_NO_PADDING", "BASE64_VARIANT_URLSAFE", "BASE64_VARIANT_URLSAFE_NO_PADDING", "CRYPTO_AEAD_CHACHA20POLY1305_KEYBYTES", "CRYPTO_AEAD_CHACHA20POLY1305_NSECBYTES", "CRYPTO_AEAD_CHACHA20POLY1305_NPUBBYTES", "CRYPTO_AEAD_CHACHA20POLY1305_ABYTES", "CRYPTO_AEAD_AES256GCM_KEYBYTES", "CRYPTO_AEAD_AES256GCM_NSECBYTES", "CRYPTO_AEAD_AES256GCM_NPUBBYTES", "CRYPTO_AEAD_AES256GCM_ABYTES", "CRYPTO_AEAD_CHACHA20POLY1305_IETF_KEYBYTES", "CRYPTO_AEAD_CHACHA20POLY1305_IETF_NSECBYTES", "CRYPTO_AEAD_CHACHA20POLY1305_IETF_NPUBBYTES", "CRYPTO_AEAD_CHACHA20POLY1305_IETF_ABYTES", "CRYPTO_AUTH_BYTES", "CRYPTO_AUTH_KEYBYTES", "CRYPTO_BOX_SEALBYTES", "CRYPTO_BOX_SECRETKEYBYTES", "CRYPTO_BOX_PUBLICKEYBYTES", "CRYPTO_BOX_KEYPAIRBYTES", "CRYPTO_BOX_MACBYTES", "CRYPTO_BOX_NONCEBYTES", "CRYPTO_BOX_SEEDBYTES", "CRYPTO_KDF_BYTES_MIN", "CRYPTO_KDF_BYTES_MAX", "CRYPTO_KDF_CONTEXTBYTES", "CRYPTO_KDF_KEYBYTES", "CRYPTO_KX_BYTES", "CRYPTO_KX_KEYPAIRBYTES", "CRYPTO_KX_PRIMITIVE", "CRYPTO_KX_SEEDBYTES", "CRYPTO_KX_PUBLICKEYBYTES", "CRYPTO_KX_SECRETKEYBYTES", "CRYPTO_KX_SESSIONKEYBYTES", "CRYPTO_GENERICHASH_BYTES", "CRYPTO_GENERICHASH_BYTES_MIN", "CRYPTO_GENERICHASH_BYTES_MAX", "CRYPTO_GENERICHASH_KEYBYTES", "CRYPTO_GENERICHASH_KEYBYTES_MIN", "CRYPTO_GENERICHASH_KEYBYTES_MAX", "CRYPTO_PWHASH_SALTBYTES", "CRYPTO_PWHASH_STRPREFIX", "CRYPTO_PWHASH_ALG_ARGON2I13", "CRYPTO_PWHASH_ALG_ARGON2ID13", "CRYPTO_PWHASH_MEMLIMIT_INTERACTIVE", "CRYPTO_PWHASH_OPSLIMIT_INTERACTIVE", "CRYPTO_PWHASH_MEMLIMIT_MODERATE", "CRYPTO_PWHASH_OPSLIMIT_MODERATE", "CRYPTO_PWHASH_MEMLIMIT_SENSITIVE", "CRYPTO_PWHASH_OPSLIMIT_SENSITIVE", "CRYPTO_SCALARMULT_BYTES", "CRYPTO_SCALARMULT_SCALARBYTES", "CRYPTO_SHORTHASH_BYTES", "CRYPTO_SHORTHASH_KEYBYTES", "CRYPTO_SECRETBOX_KEYBYTES", "CRYPTO_SECRETBOX_MACBYTES", "CRYPTO_SECRETBOX_NONCEBYTES", "CRYPTO_SECRETSTREAM_XCHACHA20POLY1305_ABYTES", "CRYPTO_SECRETSTREAM_XCHACHA20POLY1305_HEADERBYTES", "CRYPTO_SECRETSTREAM_XCHACHA20POLY1305_KEYBYTES", "CRYPTO_SECRETSTREAM_XCHACHA20POLY1305_TAG_PUSH", "CRYPTO_SECRETSTREAM_XCHACHA20POLY1305_TAG_PULL", "CRYPTO_SECRETSTREAM_XCHACHA20POLY1305_TAG_REKEY", "CRYPTO_SECRETSTREAM_XCHACHA20POLY1305_TAG_FINAL", "CRYPTO_SECRETSTREAM_XCHACHA20POLY1305_MESSAGEBYTES_MAX", "CRYPTO_SIGN_BYTES", "CRYPTO_SIGN_SEEDBYTES", "CRYPTO_SIGN_PUBLICKEYBYTES", "CRYPTO_SIGN_SECRETKEYBYTES", "CRYPTO_SIGN_KEYPAIRBYTES", "CRYPTO_STREAM_KEYBYTES", "CRYPTO_STREAM_NONCEBYTES", "LIBRARY_VERSION_MAJOR", "LIBRARY_VERSION_MINOR", "VERSION_STRING"):
    if (not php_defined(str("SODIUM_") + str(constant))) and php_defined(str("ParagonIE_Sodium_Compat::") + str(constant)):
        php_define(str("SODIUM_") + str(constant), constant(str("ParagonIE_Sodium_Compat::") + str(constant)))
    # end if
# end for
if (not php_is_callable("sodium_add")):
    #// 
    #// @see ParagonIE_Sodium_Compat::add()
    #// @param string $val
    #// @param string $addv
    #// @return void
    #// @throws SodiumException
    #//
    def sodium_add(val=None, addv=None, *args_):
        
        ParagonIE_Sodium_Compat.add(val, addv)
    # end def sodium_add
# end if
if (not php_is_callable("sodium_base642bin")):
    #// 
    #// @see ParagonIE_Sodium_Compat::bin2base64()
    #// @param string $string
    #// @param int $variant
    #// @param string $ignore
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_base642bin(string=None, variant=None, ignore="", *args_):
        
        return ParagonIE_Sodium_Compat.base642bin(string, variant, ignore)
    # end def sodium_base642bin
# end if
if (not php_is_callable("sodium_bin2base64")):
    #// 
    #// @see ParagonIE_Sodium_Compat::bin2base64()
    #// @param string $string
    #// @param int $variant
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_bin2base64(string=None, variant=None, *args_):
        
        return ParagonIE_Sodium_Compat.bin2base64(string, variant)
    # end def sodium_bin2base64
# end if
if (not php_is_callable("sodium_bin2hex")):
    #// 
    #// @see ParagonIE_Sodium_Compat::hex2bin()
    #// @param string $string
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_bin2hex(string=None, *args_):
        
        return ParagonIE_Sodium_Compat.bin2hex(string)
    # end def sodium_bin2hex
# end if
if (not php_is_callable("sodium_compare")):
    #// 
    #// @see ParagonIE_Sodium_Compat::compare()
    #// @param string $a
    #// @param string $b
    #// @return int
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_compare(a=None, b=None, *args_):
        
        return ParagonIE_Sodium_Compat.compare(a, b)
    # end def sodium_compare
# end if
if (not php_is_callable("sodium_crypto_aead_aes256gcm_decrypt")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_aead_aes256gcm_decrypt()
    #// @param string $message
    #// @param string $assocData
    #// @param string $nonce
    #// @param string $key
    #// @return string|bool
    #//
    def sodium_crypto_aead_aes256gcm_decrypt(message=None, assocData=None, nonce=None, key=None, *args_):
        
        try: 
            return ParagonIE_Sodium_Compat.crypto_aead_aes256gcm_decrypt(message, assocData, nonce, key)
        except Error as ex:
            return False
        except Exception as ex:
            return False
        # end try
    # end def sodium_crypto_aead_aes256gcm_decrypt
# end if
if (not php_is_callable("sodium_crypto_aead_aes256gcm_encrypt")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_aead_aes256gcm_encrypt()
    #// @param string $message
    #// @param string $assocData
    #// @param string $nonce
    #// @param string $key
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_aead_aes256gcm_encrypt(message=None, assocData=None, nonce=None, key=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_aead_aes256gcm_encrypt(message, assocData, nonce, key)
    # end def sodium_crypto_aead_aes256gcm_encrypt
# end if
if (not php_is_callable("sodium_crypto_aead_aes256gcm_is_available")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_aead_aes256gcm_is_available()
    #// @return bool
    #//
    def sodium_crypto_aead_aes256gcm_is_available(*args_):
        
        return ParagonIE_Sodium_Compat.crypto_aead_aes256gcm_is_available()
    # end def sodium_crypto_aead_aes256gcm_is_available
# end if
if (not php_is_callable("sodium_crypto_aead_chacha20poly1305_decrypt")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_aead_chacha20poly1305_decrypt()
    #// @param string $message
    #// @param string $assocData
    #// @param string $nonce
    #// @param string $key
    #// @return string|bool
    #//
    def sodium_crypto_aead_chacha20poly1305_decrypt(message=None, assocData=None, nonce=None, key=None, *args_):
        
        try: 
            return ParagonIE_Sodium_Compat.crypto_aead_chacha20poly1305_decrypt(message, assocData, nonce, key)
        except Error as ex:
            return False
        except Exception as ex:
            return False
        # end try
    # end def sodium_crypto_aead_chacha20poly1305_decrypt
# end if
if (not php_is_callable("sodium_crypto_aead_chacha20poly1305_encrypt")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_aead_chacha20poly1305_encrypt()
    #// @param string $message
    #// @param string $assocData
    #// @param string $nonce
    #// @param string $key
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_aead_chacha20poly1305_encrypt(message=None, assocData=None, nonce=None, key=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_aead_chacha20poly1305_encrypt(message, assocData, nonce, key)
    # end def sodium_crypto_aead_chacha20poly1305_encrypt
# end if
if (not php_is_callable("sodium_crypto_aead_chacha20poly1305_keygen")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_aead_chacha20poly1305_keygen()
    #// @return string
    #// @throws Exception
    #//
    def sodium_crypto_aead_chacha20poly1305_keygen(*args_):
        
        return ParagonIE_Sodium_Compat.crypto_aead_chacha20poly1305_keygen()
    # end def sodium_crypto_aead_chacha20poly1305_keygen
# end if
if (not php_is_callable("sodium_crypto_aead_chacha20poly1305_ietf_decrypt")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_aead_chacha20poly1305_ietf_decrypt()
    #// @param string $message
    #// @param string $assocData
    #// @param string $nonce
    #// @param string $key
    #// @return string|bool
    #//
    def sodium_crypto_aead_chacha20poly1305_ietf_decrypt(message=None, assocData=None, nonce=None, key=None, *args_):
        
        try: 
            return ParagonIE_Sodium_Compat.crypto_aead_chacha20poly1305_ietf_decrypt(message, assocData, nonce, key)
        except Error as ex:
            return False
        except Exception as ex:
            return False
        # end try
    # end def sodium_crypto_aead_chacha20poly1305_ietf_decrypt
# end if
if (not php_is_callable("sodium_crypto_aead_chacha20poly1305_ietf_encrypt")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_aead_chacha20poly1305_ietf_encrypt()
    #// @param string $message
    #// @param string $assocData
    #// @param string $nonce
    #// @param string $key
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_aead_chacha20poly1305_ietf_encrypt(message=None, assocData=None, nonce=None, key=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_aead_chacha20poly1305_ietf_encrypt(message, assocData, nonce, key)
    # end def sodium_crypto_aead_chacha20poly1305_ietf_encrypt
# end if
if (not php_is_callable("sodium_crypto_aead_chacha20poly1305_ietf_keygen")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_aead_chacha20poly1305_ietf_keygen()
    #// @return string
    #// @throws Exception
    #//
    def sodium_crypto_aead_chacha20poly1305_ietf_keygen(*args_):
        
        return ParagonIE_Sodium_Compat.crypto_aead_chacha20poly1305_ietf_keygen()
    # end def sodium_crypto_aead_chacha20poly1305_ietf_keygen
# end if
if (not php_is_callable("sodium_crypto_aead_xchacha20poly1305_ietf_decrypt")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_aead_xchacha20poly1305_ietf_decrypt()
    #// @param string $message
    #// @param string $assocData
    #// @param string $nonce
    #// @param string $key
    #// @return string|bool
    #//
    def sodium_crypto_aead_xchacha20poly1305_ietf_decrypt(message=None, assocData=None, nonce=None, key=None, *args_):
        
        try: 
            return ParagonIE_Sodium_Compat.crypto_aead_xchacha20poly1305_ietf_decrypt(message, assocData, nonce, key, True)
        except Error as ex:
            return False
        except Exception as ex:
            return False
        # end try
    # end def sodium_crypto_aead_xchacha20poly1305_ietf_decrypt
# end if
if (not php_is_callable("sodium_crypto_aead_xchacha20poly1305_ietf_encrypt")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_aead_xchacha20poly1305_ietf_encrypt()
    #// @param string $message
    #// @param string $assocData
    #// @param string $nonce
    #// @param string $key
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_aead_xchacha20poly1305_ietf_encrypt(message=None, assocData=None, nonce=None, key=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_aead_xchacha20poly1305_ietf_encrypt(message, assocData, nonce, key, True)
    # end def sodium_crypto_aead_xchacha20poly1305_ietf_encrypt
# end if
if (not php_is_callable("sodium_crypto_aead_xchacha20poly1305_ietf_keygen")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_aead_xchacha20poly1305_ietf_keygen()
    #// @return string
    #// @throws Exception
    #//
    def sodium_crypto_aead_xchacha20poly1305_ietf_keygen(*args_):
        
        return ParagonIE_Sodium_Compat.crypto_aead_xchacha20poly1305_ietf_keygen()
    # end def sodium_crypto_aead_xchacha20poly1305_ietf_keygen
# end if
if (not php_is_callable("sodium_crypto_auth")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_auth()
    #// @param string $message
    #// @param string $key
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_auth(message=None, key=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_auth(message, key)
    # end def sodium_crypto_auth
# end if
if (not php_is_callable("sodium_crypto_auth_keygen")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_auth_keygen()
    #// @return string
    #// @throws Exception
    #//
    def sodium_crypto_auth_keygen(*args_):
        
        return ParagonIE_Sodium_Compat.crypto_auth_keygen()
    # end def sodium_crypto_auth_keygen
# end if
if (not php_is_callable("sodium_crypto_auth_verify")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_auth_verify()
    #// @param string $mac
    #// @param string $message
    #// @param string $key
    #// @return bool
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_auth_verify(mac=None, message=None, key=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_auth_verify(mac, message, key)
    # end def sodium_crypto_auth_verify
# end if
if (not php_is_callable("sodium_crypto_box")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_box()
    #// @param string $message
    #// @param string $nonce
    #// @param string $kp
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_box(message=None, nonce=None, kp=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_box(message, nonce, kp)
    # end def sodium_crypto_box
# end if
if (not php_is_callable("sodium_crypto_box_keypair")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_box_keypair()
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_box_keypair(*args_):
        
        return ParagonIE_Sodium_Compat.crypto_box_keypair()
    # end def sodium_crypto_box_keypair
# end if
if (not php_is_callable("sodium_crypto_box_keypair_from_secretkey_and_publickey")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_box_keypair_from_secretkey_and_publickey()
    #// @param string $sk
    #// @param string $pk
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_box_keypair_from_secretkey_and_publickey(sk=None, pk=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_box_keypair_from_secretkey_and_publickey(sk, pk)
    # end def sodium_crypto_box_keypair_from_secretkey_and_publickey
# end if
if (not php_is_callable("sodium_crypto_box_open")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_box_open()
    #// @param string $message
    #// @param string $nonce
    #// @param string $kp
    #// @return string|bool
    #//
    def sodium_crypto_box_open(message=None, nonce=None, kp=None, *args_):
        
        try: 
            return ParagonIE_Sodium_Compat.crypto_box_open(message, nonce, kp)
        except Error as ex:
            return False
        except Exception as ex:
            return False
        # end try
    # end def sodium_crypto_box_open
# end if
if (not php_is_callable("sodium_crypto_box_publickey")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_box_publickey()
    #// @param string $keypair
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_box_publickey(keypair=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_box_publickey(keypair)
    # end def sodium_crypto_box_publickey
# end if
if (not php_is_callable("sodium_crypto_box_publickey_from_secretkey")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_box_publickey_from_secretkey()
    #// @param string $sk
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_box_publickey_from_secretkey(sk=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_box_publickey_from_secretkey(sk)
    # end def sodium_crypto_box_publickey_from_secretkey
# end if
if (not php_is_callable("sodium_crypto_box_seal")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_box_seal()
    #// @param string $message
    #// @param string $publicKey
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_box_seal(message=None, publicKey=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_box_seal(message, publicKey)
    # end def sodium_crypto_box_seal
# end if
if (not php_is_callable("sodium_crypto_box_seal_open")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_box_seal_open()
    #// @param string $message
    #// @param string $kp
    #// @return string|bool
    #// @throws SodiumException
    #//
    def sodium_crypto_box_seal_open(message=None, kp=None, *args_):
        
        try: 
            return ParagonIE_Sodium_Compat.crypto_box_seal_open(message, kp)
        except SodiumException as ex:
            if ex.getmessage() == "Argument 2 must be CRYPTO_BOX_KEYPAIRBYTES long.":
                raise ex
            # end if
            return False
        # end try
    # end def sodium_crypto_box_seal_open
# end if
if (not php_is_callable("sodium_crypto_box_secretkey")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_box_secretkey()
    #// @param string $keypair
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_box_secretkey(keypair=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_box_secretkey(keypair)
    # end def sodium_crypto_box_secretkey
# end if
if (not php_is_callable("sodium_crypto_box_seed_keypair")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_box_seed_keypair()
    #// @param string $seed
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_box_seed_keypair(seed=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_box_seed_keypair(seed)
    # end def sodium_crypto_box_seed_keypair
# end if
if (not php_is_callable("sodium_crypto_generichash")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_generichash()
    #// @param string $message
    #// @param string|null $key
    #// @param int $outLen
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_generichash(message=None, key=None, outLen=32, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_generichash(message, key, outLen)
    # end def sodium_crypto_generichash
# end if
if (not php_is_callable("sodium_crypto_generichash_final")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_generichash_final()
    #// @param string|null $ctx
    #// @param int $outputLength
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_generichash_final(ctx=None, outputLength=32, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_generichash_final(ctx, outputLength)
    # end def sodium_crypto_generichash_final
# end if
if (not php_is_callable("sodium_crypto_generichash_init")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_generichash_init()
    #// @param string|null $key
    #// @param int $outLen
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_generichash_init(key=None, outLen=32, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_generichash_init(key, outLen)
    # end def sodium_crypto_generichash_init
# end if
if (not php_is_callable("sodium_crypto_generichash_keygen")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_generichash_keygen()
    #// @return string
    #// @throws Exception
    #//
    def sodium_crypto_generichash_keygen(*args_):
        
        return ParagonIE_Sodium_Compat.crypto_generichash_keygen()
    # end def sodium_crypto_generichash_keygen
# end if
if (not php_is_callable("sodium_crypto_generichash_update")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_generichash_update()
    #// @param string|null $ctx
    #// @param string $message
    #// @return void
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_generichash_update(ctx=None, message="", *args_):
        
        ParagonIE_Sodium_Compat.crypto_generichash_update(ctx, message)
    # end def sodium_crypto_generichash_update
# end if
if (not php_is_callable("sodium_crypto_kdf_keygen")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_kdf_keygen()
    #// @return string
    #// @throws Exception
    #//
    def sodium_crypto_kdf_keygen(*args_):
        
        return ParagonIE_Sodium_Compat.crypto_kdf_keygen()
    # end def sodium_crypto_kdf_keygen
# end if
if (not php_is_callable("sodium_crypto_kdf_derive_from_key")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_kdf_derive_from_key()
    #// @param int $subkey_len
    #// @param int $subkey_id
    #// @param string $context
    #// @param string $key
    #// @return string
    #// @throws Exception
    #//
    def sodium_crypto_kdf_derive_from_key(subkey_len=None, subkey_id=None, context=None, key=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_kdf_derive_from_key(subkey_len, subkey_id, context, key)
    # end def sodium_crypto_kdf_derive_from_key
# end if
if (not php_is_callable("sodium_crypto_kx")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_kx()
    #// @param string $my_secret
    #// @param string $their_public
    #// @param string $client_public
    #// @param string $server_public
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_kx(my_secret=None, their_public=None, client_public=None, server_public=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_kx(my_secret, their_public, client_public, server_public)
    # end def sodium_crypto_kx
# end if
if (not php_is_callable("sodium_crypto_kx_seed_keypair")):
    #// 
    #// @param string $seed
    #// @return string
    #// @throws Exception
    #//
    def sodium_crypto_kx_seed_keypair(seed=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_kx_seed_keypair(seed)
    # end def sodium_crypto_kx_seed_keypair
# end if
if (not php_is_callable("sodium_crypto_kx_keypair")):
    #// 
    #// @return string
    #// @throws Exception
    #//
    def sodium_crypto_kx_keypair(*args_):
        
        return ParagonIE_Sodium_Compat.crypto_kx_keypair()
    # end def sodium_crypto_kx_keypair
# end if
if (not php_is_callable("sodium_crypto_kx_client_session_keys")):
    #// 
    #// @param string $keypair
    #// @param string $serverPublicKey
    #// @return array{0: string, 1: string}
    #// @throws SodiumException
    #//
    def sodium_crypto_kx_client_session_keys(keypair=None, serverPublicKey=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_kx_client_session_keys(keypair, serverPublicKey)
    # end def sodium_crypto_kx_client_session_keys
# end if
if (not php_is_callable("sodium_crypto_kx_server_session_keys")):
    #// 
    #// @param string $keypair
    #// @param string $clientPublicKey
    #// @return array{0: string, 1: string}
    #// @throws SodiumException
    #//
    def sodium_crypto_kx_server_session_keys(keypair=None, clientPublicKey=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_kx_server_session_keys(keypair, clientPublicKey)
    # end def sodium_crypto_kx_server_session_keys
# end if
if (not php_is_callable("sodium_crypto_kx_secretkey")):
    #// 
    #// @param string $keypair
    #// @return string
    #// @throws Exception
    #//
    def sodium_crypto_kx_secretkey(keypair=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_kx_secretkey(keypair)
    # end def sodium_crypto_kx_secretkey
# end if
if (not php_is_callable("sodium_crypto_kx_publickey")):
    #// 
    #// @param string $keypair
    #// @return string
    #// @throws Exception
    #//
    def sodium_crypto_kx_publickey(keypair=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_kx_publickey(keypair)
    # end def sodium_crypto_kx_publickey
# end if
if (not php_is_callable("sodium_crypto_pwhash")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_pwhash()
    #// @param int $outlen
    #// @param string $passwd
    #// @param string $salt
    #// @param int $opslimit
    #// @param int $memlimit
    #// @param int|null $algo
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_pwhash(outlen=None, passwd=None, salt=None, opslimit=None, memlimit=None, algo=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_pwhash(outlen, passwd, salt, opslimit, memlimit, algo)
    # end def sodium_crypto_pwhash
# end if
if (not php_is_callable("sodium_crypto_pwhash_str")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_pwhash_str()
    #// @param string $passwd
    #// @param int $opslimit
    #// @param int $memlimit
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_pwhash_str(passwd=None, opslimit=None, memlimit=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_pwhash_str(passwd, opslimit, memlimit)
    # end def sodium_crypto_pwhash_str
# end if
if (not php_is_callable("sodium_crypto_pwhash_str_needs_rehash")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_pwhash_str_needs_rehash()
    #// @param string $hash
    #// @param int $opslimit
    #// @param int $memlimit
    #// @return bool
    #// 
    #// @throws SodiumException
    #//
    def sodium_crypto_pwhash_str_needs_rehash(hash=None, opslimit=None, memlimit=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_pwhash_str_needs_rehash(hash, opslimit, memlimit)
    # end def sodium_crypto_pwhash_str_needs_rehash
# end if
if (not php_is_callable("sodium_crypto_pwhash_str_verify")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_pwhash_str_verify()
    #// @param string $passwd
    #// @param string $hash
    #// @return bool
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_pwhash_str_verify(passwd=None, hash=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_pwhash_str_verify(passwd, hash)
    # end def sodium_crypto_pwhash_str_verify
# end if
if (not php_is_callable("sodium_crypto_pwhash_scryptsalsa208sha256")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_pwhash_scryptsalsa208sha256()
    #// @param int $outlen
    #// @param string $passwd
    #// @param string $salt
    #// @param int $opslimit
    #// @param int $memlimit
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_pwhash_scryptsalsa208sha256(outlen=None, passwd=None, salt=None, opslimit=None, memlimit=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_pwhash_scryptsalsa208sha256(outlen, passwd, salt, opslimit, memlimit)
    # end def sodium_crypto_pwhash_scryptsalsa208sha256
# end if
if (not php_is_callable("sodium_crypto_pwhash_scryptsalsa208sha256_str")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_pwhash_scryptsalsa208sha256_str()
    #// @param string $passwd
    #// @param int $opslimit
    #// @param int $memlimit
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_pwhash_scryptsalsa208sha256_str(passwd=None, opslimit=None, memlimit=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_pwhash_scryptsalsa208sha256_str(passwd, opslimit, memlimit)
    # end def sodium_crypto_pwhash_scryptsalsa208sha256_str
# end if
if (not php_is_callable("sodium_crypto_pwhash_scryptsalsa208sha256_str_verify")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_pwhash_scryptsalsa208sha256_str_verify()
    #// @param string $passwd
    #// @param string $hash
    #// @return bool
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_pwhash_scryptsalsa208sha256_str_verify(passwd=None, hash=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_pwhash_scryptsalsa208sha256_str_verify(passwd, hash)
    # end def sodium_crypto_pwhash_scryptsalsa208sha256_str_verify
# end if
if (not php_is_callable("sodium_crypto_scalarmult")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_scalarmult()
    #// @param string $n
    #// @param string $p
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_scalarmult(n=None, p=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_scalarmult(n, p)
    # end def sodium_crypto_scalarmult
# end if
if (not php_is_callable("sodium_crypto_scalarmult_base")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_scalarmult_base()
    #// @param string $n
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_scalarmult_base(n=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_scalarmult_base(n)
    # end def sodium_crypto_scalarmult_base
# end if
if (not php_is_callable("sodium_crypto_secretbox")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_secretbox()
    #// @param string $message
    #// @param string $nonce
    #// @param string $key
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_secretbox(message=None, nonce=None, key=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_secretbox(message, nonce, key)
    # end def sodium_crypto_secretbox
# end if
if (not php_is_callable("sodium_crypto_secretbox_keygen")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_secretbox_keygen()
    #// @return string
    #// @throws Exception
    #//
    def sodium_crypto_secretbox_keygen(*args_):
        
        return ParagonIE_Sodium_Compat.crypto_secretbox_keygen()
    # end def sodium_crypto_secretbox_keygen
# end if
if (not php_is_callable("sodium_crypto_secretbox_open")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_secretbox_open()
    #// @param string $message
    #// @param string $nonce
    #// @param string $key
    #// @return string|bool
    #//
    def sodium_crypto_secretbox_open(message=None, nonce=None, key=None, *args_):
        
        try: 
            return ParagonIE_Sodium_Compat.crypto_secretbox_open(message, nonce, key)
        except Error as ex:
            return False
        except Exception as ex:
            return False
        # end try
    # end def sodium_crypto_secretbox_open
# end if
if (not php_is_callable("sodium_crypto_secretstream_xchacha20poly1305_init_push")):
    #// 
    #// @param string $key
    #// @return array<int, string>
    #// @throws SodiumException
    #//
    def sodium_crypto_secretstream_xchacha20poly1305_init_push(key=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_secretstream_xchacha20poly1305_init_push(key)
    # end def sodium_crypto_secretstream_xchacha20poly1305_init_push
# end if
if (not php_is_callable("sodium_crypto_secretstream_xchacha20poly1305_push")):
    #// 
    #// @param string $state
    #// @param string $msg
    #// @param string $aad
    #// @param int $tag
    #// @return string
    #// @throws SodiumException
    #//
    def sodium_crypto_secretstream_xchacha20poly1305_push(state=None, msg=None, aad="", tag=0, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_secretstream_xchacha20poly1305_push(state, msg, aad, tag)
    # end def sodium_crypto_secretstream_xchacha20poly1305_push
# end if
if (not php_is_callable("sodium_crypto_secretstream_xchacha20poly1305_init_pull")):
    #// 
    #// @param string $header
    #// @param string $key
    #// @return string
    #// @throws Exception
    #//
    def sodium_crypto_secretstream_xchacha20poly1305_init_pull(header=None, key=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_secretstream_xchacha20poly1305_init_pull(header, key)
    # end def sodium_crypto_secretstream_xchacha20poly1305_init_pull
# end if
if (not php_is_callable("sodium_crypto_secretstream_xchacha20poly1305_pull")):
    #// 
    #// @param string $state
    #// @param string $cipher
    #// @param string $aad
    #// @return bool|array{0: string, 1: int}
    #// @throws SodiumException
    #//
    def sodium_crypto_secretstream_xchacha20poly1305_pull(state=None, cipher=None, aad="", *args_):
        
        return ParagonIE_Sodium_Compat.crypto_secretstream_xchacha20poly1305_pull(state, cipher, aad)
    # end def sodium_crypto_secretstream_xchacha20poly1305_pull
# end if
if (not php_is_callable("sodium_crypto_secretstream_xchacha20poly1305_rekey")):
    #// 
    #// @param string $state
    #// @return void
    #// @throws SodiumException
    #//
    def sodium_crypto_secretstream_xchacha20poly1305_rekey(state=None, *args_):
        
        ParagonIE_Sodium_Compat.crypto_secretstream_xchacha20poly1305_rekey(state)
    # end def sodium_crypto_secretstream_xchacha20poly1305_rekey
# end if
if (not php_is_callable("sodium_crypto_secretstream_xchacha20poly1305_keygen")):
    #// 
    #// @return string
    #// @throws Exception
    #//
    def sodium_crypto_secretstream_xchacha20poly1305_keygen(*args_):
        
        return ParagonIE_Sodium_Compat.crypto_secretstream_xchacha20poly1305_keygen()
    # end def sodium_crypto_secretstream_xchacha20poly1305_keygen
# end if
if (not php_is_callable("sodium_crypto_shorthash")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_shorthash()
    #// @param string $message
    #// @param string $key
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_shorthash(message=None, key="", *args_):
        
        return ParagonIE_Sodium_Compat.crypto_shorthash(message, key)
    # end def sodium_crypto_shorthash
# end if
if (not php_is_callable("sodium_crypto_shorthash_keygen")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_shorthash_keygen()
    #// @return string
    #// @throws Exception
    #//
    def sodium_crypto_shorthash_keygen(*args_):
        
        return ParagonIE_Sodium_Compat.crypto_shorthash_keygen()
    # end def sodium_crypto_shorthash_keygen
# end if
if (not php_is_callable("sodium_crypto_sign")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_sign()
    #// @param string $message
    #// @param string $sk
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_sign(message=None, sk=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_sign(message, sk)
    # end def sodium_crypto_sign
# end if
if (not php_is_callable("sodium_crypto_sign_detached")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_sign_detached()
    #// @param string $message
    #// @param string $sk
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_sign_detached(message=None, sk=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_sign_detached(message, sk)
    # end def sodium_crypto_sign_detached
# end if
if (not php_is_callable("sodium_crypto_sign_keypair_from_secretkey_and_publickey")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_sign_keypair_from_secretkey_and_publickey()
    #// @param string $sk
    #// @param string $pk
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_sign_keypair_from_secretkey_and_publickey(sk=None, pk=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_sign_keypair_from_secretkey_and_publickey(sk, pk)
    # end def sodium_crypto_sign_keypair_from_secretkey_and_publickey
# end if
if (not php_is_callable("sodium_crypto_sign_keypair")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_sign_keypair()
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_sign_keypair(*args_):
        
        return ParagonIE_Sodium_Compat.crypto_sign_keypair()
    # end def sodium_crypto_sign_keypair
# end if
if (not php_is_callable("sodium_crypto_sign_open")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_sign_open()
    #// @param string $signedMessage
    #// @param string $pk
    #// @return string|bool
    #//
    def sodium_crypto_sign_open(signedMessage=None, pk=None, *args_):
        
        try: 
            return ParagonIE_Sodium_Compat.crypto_sign_open(signedMessage, pk)
        except Error as ex:
            return False
        except Exception as ex:
            return False
        # end try
    # end def sodium_crypto_sign_open
# end if
if (not php_is_callable("sodium_crypto_sign_publickey")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_sign_publickey()
    #// @param string $keypair
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_sign_publickey(keypair=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_sign_publickey(keypair)
    # end def sodium_crypto_sign_publickey
# end if
if (not php_is_callable("sodium_crypto_sign_publickey_from_secretkey")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_sign_publickey_from_secretkey()
    #// @param string $sk
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_sign_publickey_from_secretkey(sk=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_sign_publickey_from_secretkey(sk)
    # end def sodium_crypto_sign_publickey_from_secretkey
# end if
if (not php_is_callable("sodium_crypto_sign_secretkey")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_sign_secretkey()
    #// @param string $keypair
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_sign_secretkey(keypair=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_sign_secretkey(keypair)
    # end def sodium_crypto_sign_secretkey
# end if
if (not php_is_callable("sodium_crypto_sign_seed_keypair")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_sign_seed_keypair()
    #// @param string $seed
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_sign_seed_keypair(seed=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_sign_seed_keypair(seed)
    # end def sodium_crypto_sign_seed_keypair
# end if
if (not php_is_callable("sodium_crypto_sign_verify_detached")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_sign_verify_detached()
    #// @param string $signature
    #// @param string $message
    #// @param string $pk
    #// @return bool
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_sign_verify_detached(signature=None, message=None, pk=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_sign_verify_detached(signature, message, pk)
    # end def sodium_crypto_sign_verify_detached
# end if
if (not php_is_callable("sodium_crypto_sign_ed25519_pk_to_curve25519")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_sign_ed25519_pk_to_curve25519()
    #// @param string $pk
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_sign_ed25519_pk_to_curve25519(pk=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_sign_ed25519_pk_to_curve25519(pk)
    # end def sodium_crypto_sign_ed25519_pk_to_curve25519
# end if
if (not php_is_callable("sodium_crypto_sign_ed25519_sk_to_curve25519")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_sign_ed25519_sk_to_curve25519()
    #// @param string $sk
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_sign_ed25519_sk_to_curve25519(sk=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_sign_ed25519_sk_to_curve25519(sk)
    # end def sodium_crypto_sign_ed25519_sk_to_curve25519
# end if
if (not php_is_callable("sodium_crypto_stream")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_stream()
    #// @param int $len
    #// @param string $nonce
    #// @param string $key
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_stream(len=None, nonce=None, key=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_stream(len, nonce, key)
    # end def sodium_crypto_stream
# end if
if (not php_is_callable("sodium_crypto_stream_keygen")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_stream_keygen()
    #// @return string
    #// @throws Exception
    #//
    def sodium_crypto_stream_keygen(*args_):
        
        return ParagonIE_Sodium_Compat.crypto_stream_keygen()
    # end def sodium_crypto_stream_keygen
# end if
if (not php_is_callable("sodium_crypto_stream_xor")):
    #// 
    #// @see ParagonIE_Sodium_Compat::crypto_stream_xor()
    #// @param string $message
    #// @param string $nonce
    #// @param string $key
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_crypto_stream_xor(message=None, nonce=None, key=None, *args_):
        
        return ParagonIE_Sodium_Compat.crypto_stream_xor(message, nonce, key)
    # end def sodium_crypto_stream_xor
# end if
if (not php_is_callable("sodium_hex2bin")):
    #// 
    #// @see ParagonIE_Sodium_Compat::hex2bin()
    #// @param string $string
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_hex2bin(string=None, *args_):
        
        return ParagonIE_Sodium_Compat.hex2bin(string)
    # end def sodium_hex2bin
# end if
if (not php_is_callable("sodium_increment")):
    #// 
    #// @see ParagonIE_Sodium_Compat::increment()
    #// @param string $string
    #// @return void
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_increment(string=None, *args_):
        
        ParagonIE_Sodium_Compat.increment(string)
    # end def sodium_increment
# end if
if (not php_is_callable("sodium_library_version_major")):
    #// 
    #// @see ParagonIE_Sodium_Compat::library_version_major()
    #// @return int
    #//
    def sodium_library_version_major(*args_):
        
        return ParagonIE_Sodium_Compat.library_version_major()
    # end def sodium_library_version_major
# end if
if (not php_is_callable("sodium_library_version_minor")):
    #// 
    #// @see ParagonIE_Sodium_Compat::library_version_minor()
    #// @return int
    #//
    def sodium_library_version_minor(*args_):
        
        return ParagonIE_Sodium_Compat.library_version_minor()
    # end def sodium_library_version_minor
# end if
if (not php_is_callable("sodium_version_string")):
    #// 
    #// @see ParagonIE_Sodium_Compat::version_string()
    #// @return string
    #//
    def sodium_version_string(*args_):
        
        return ParagonIE_Sodium_Compat.version_string()
    # end def sodium_version_string
# end if
if (not php_is_callable("sodium_memcmp")):
    #// 
    #// @see ParagonIE_Sodium_Compat::memcmp()
    #// @param string $a
    #// @param string $b
    #// @return int
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_memcmp(a=None, b=None, *args_):
        
        return ParagonIE_Sodium_Compat.memcmp(a, b)
    # end def sodium_memcmp
# end if
if (not php_is_callable("sodium_memzero")):
    #// 
    #// @see ParagonIE_Sodium_Compat::memzero()
    #// @param string $str
    #// @return void
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_memzero(str=None, *args_):
        
        ParagonIE_Sodium_Compat.memzero(str)
    # end def sodium_memzero
# end if
if (not php_is_callable("sodium_pad")):
    #// 
    #// @see ParagonIE_Sodium_Compat::pad()
    #// @param string $unpadded
    #// @param int $blockSize
    #// @return int
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_pad(unpadded=None, blockSize=None, *args_):
        
        return ParagonIE_Sodium_Compat.pad(unpadded, blockSize, True)
    # end def sodium_pad
# end if
if (not php_is_callable("sodium_unpad")):
    #// 
    #// @see ParagonIE_Sodium_Compat::pad()
    #// @param string $padded
    #// @param int $blockSize
    #// @return int
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sodium_unpad(padded=None, blockSize=None, *args_):
        
        return ParagonIE_Sodium_Compat.unpad(padded, blockSize, True)
    # end def sodium_unpad
# end if
if (not php_is_callable("sodium_randombytes_buf")):
    #// 
    #// @see ParagonIE_Sodium_Compat::randombytes_buf()
    #// @param int $amount
    #// @return string
    #// @throws Exception
    #//
    def sodium_randombytes_buf(amount=None, *args_):
        
        return ParagonIE_Sodium_Compat.randombytes_buf(amount)
    # end def sodium_randombytes_buf
# end if
if (not php_is_callable("sodium_randombytes_uniform")):
    #// 
    #// @see ParagonIE_Sodium_Compat::randombytes_uniform()
    #// @param int $upperLimit
    #// @return int
    #// @throws Exception
    #//
    def sodium_randombytes_uniform(upperLimit=None, *args_):
        
        return ParagonIE_Sodium_Compat.randombytes_uniform(upperLimit)
    # end def sodium_randombytes_uniform
# end if
if (not php_is_callable("sodium_randombytes_random16")):
    #// 
    #// @see ParagonIE_Sodium_Compat::randombytes_random16()
    #// @return int
    #// @throws Exception
    #//
    def sodium_randombytes_random16(*args_):
        
        return ParagonIE_Sodium_Compat.randombytes_random16()
    # end def sodium_randombytes_random16
# end if
