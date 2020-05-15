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
if not php_defined("Sodium"):
    class Sodium:
        pass
    # end class
# end if
class Sodium(Sodium):
    _namespace__ = "Sodium"
    php_include_file(php_dirname(php_dirname(__FILE__)) + "/autoload.php", once=True)
    php_new_class("P", lambda *args, **kwargs: P(*args, **kwargs))
    #// 
    #// This file will monkey patch the pure-PHP implementation in place of the
    #// PECL functions, but only if they do not already exist.
    #// 
    #// Thus, the functions just proxy to the appropriate ParagonIE_Sodium_Compat
    #// method.
    #//
    if (not php_is_callable("\\Sodium\\bin2hex")):
        #// 
        #// @see ParagonIE_Sodium_Compat::bin2hex()
        #// @param string $string
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def bin2hex(string=None, *args_):
            
            return ParagonIE_Sodium_Compat.bin2hex(string)
        # end def bin2hex
    # end if
    if (not php_is_callable("\\Sodium\\compare")):
        #// 
        #// @see ParagonIE_Sodium_Compat::compare()
        #// @param string $a
        #// @param string $b
        #// @return int
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def compare(a=None, b=None, *args_):
            
            return ParagonIE_Sodium_Compat.compare(a, b)
        # end def compare
    # end if
    if (not php_is_callable("\\Sodium\\crypto_aead_aes256gcm_decrypt")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_aead_aes256gcm_decrypt()
        #// @param string $message
        #// @param string $assocData
        #// @param string $nonce
        #// @param string $key
        #// @return string|bool
        #//
        def crypto_aead_aes256gcm_decrypt(message=None, assocData=None, nonce=None, key=None, *args_):
            
            try: 
                return ParagonIE_Sodium_Compat.crypto_aead_aes256gcm_decrypt(message, assocData, nonce, key)
            except TypeError as ex:
                return False
            except SodiumException as ex:
                return False
            # end try
        # end def crypto_aead_aes256gcm_decrypt
    # end if
    if (not php_is_callable("\\Sodium\\crypto_aead_aes256gcm_encrypt")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_aead_aes256gcm_encrypt()
        #// @param string $message
        #// @param string $assocData
        #// @param string $nonce
        #// @param string $key
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_aead_aes256gcm_encrypt(message=None, assocData=None, nonce=None, key=None, *args_):
            
            return ParagonIE_Sodium_Compat.crypto_aead_aes256gcm_encrypt(message, assocData, nonce, key)
        # end def crypto_aead_aes256gcm_encrypt
    # end if
    if (not php_is_callable("\\Sodium\\crypto_aead_aes256gcm_is_available")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_aead_aes256gcm_is_available()
        #// @return bool
        #//
        def crypto_aead_aes256gcm_is_available(*args_):
            
            return ParagonIE_Sodium_Compat.crypto_aead_aes256gcm_is_available()
        # end def crypto_aead_aes256gcm_is_available
    # end if
    if (not php_is_callable("\\Sodium\\crypto_aead_chacha20poly1305_decrypt")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_aead_chacha20poly1305_decrypt()
        #// @param string $message
        #// @param string $assocData
        #// @param string $nonce
        #// @param string $key
        #// @return string|bool
        #//
        def crypto_aead_chacha20poly1305_decrypt(message=None, assocData=None, nonce=None, key=None, *args_):
            
            try: 
                return ParagonIE_Sodium_Compat.crypto_aead_chacha20poly1305_decrypt(message, assocData, nonce, key)
            except TypeError as ex:
                return False
            except SodiumException as ex:
                return False
            # end try
        # end def crypto_aead_chacha20poly1305_decrypt
    # end if
    if (not php_is_callable("\\Sodium\\crypto_aead_chacha20poly1305_encrypt")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_aead_chacha20poly1305_encrypt()
        #// @param string $message
        #// @param string $assocData
        #// @param string $nonce
        #// @param string $key
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_aead_chacha20poly1305_encrypt(message=None, assocData=None, nonce=None, key=None, *args_):
            
            return ParagonIE_Sodium_Compat.crypto_aead_chacha20poly1305_encrypt(message, assocData, nonce, key)
        # end def crypto_aead_chacha20poly1305_encrypt
    # end if
    if (not php_is_callable("\\Sodium\\crypto_aead_chacha20poly1305_ietf_decrypt")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_aead_chacha20poly1305_ietf_decrypt()
        #// @param string $message
        #// @param string $assocData
        #// @param string $nonce
        #// @param string $key
        #// @return string|bool
        #//
        def crypto_aead_chacha20poly1305_ietf_decrypt(message=None, assocData=None, nonce=None, key=None, *args_):
            
            try: 
                return ParagonIE_Sodium_Compat.crypto_aead_chacha20poly1305_ietf_decrypt(message, assocData, nonce, key)
            except TypeError as ex:
                return False
            except SodiumException as ex:
                return False
            # end try
        # end def crypto_aead_chacha20poly1305_ietf_decrypt
    # end if
    if (not php_is_callable("\\Sodium\\crypto_aead_chacha20poly1305_ietf_encrypt")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_aead_chacha20poly1305_ietf_encrypt()
        #// @param string $message
        #// @param string $assocData
        #// @param string $nonce
        #// @param string $key
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_aead_chacha20poly1305_ietf_encrypt(message=None, assocData=None, nonce=None, key=None, *args_):
            
            return ParagonIE_Sodium_Compat.crypto_aead_chacha20poly1305_ietf_encrypt(message, assocData, nonce, key)
        # end def crypto_aead_chacha20poly1305_ietf_encrypt
    # end if
    if (not php_is_callable("\\Sodium\\crypto_auth")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_auth()
        #// @param string $message
        #// @param string $key
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_auth(message=None, key=None, *args_):
            
            return ParagonIE_Sodium_Compat.crypto_auth(message, key)
        # end def crypto_auth
    # end if
    if (not php_is_callable("\\Sodium\\crypto_auth_verify")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_auth_verify()
        #// @param string $mac
        #// @param string $message
        #// @param string $key
        #// @return bool
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_auth_verify(mac=None, message=None, key=None, *args_):
            
            return ParagonIE_Sodium_Compat.crypto_auth_verify(mac, message, key)
        # end def crypto_auth_verify
    # end if
    if (not php_is_callable("\\Sodium\\crypto_box")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_box()
        #// @param string $message
        #// @param string $nonce
        #// @param string $kp
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_box(message=None, nonce=None, kp=None, *args_):
            
            return ParagonIE_Sodium_Compat.crypto_box(message, nonce, kp)
        # end def crypto_box
    # end if
    if (not php_is_callable("\\Sodium\\crypto_box_keypair")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_box_keypair()
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_box_keypair(*args_):
            
            return ParagonIE_Sodium_Compat.crypto_box_keypair()
        # end def crypto_box_keypair
    # end if
    if (not php_is_callable("\\Sodium\\crypto_box_keypair_from_secretkey_and_publickey")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_box_keypair_from_secretkey_and_publickey()
        #// @param string $sk
        #// @param string $pk
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_box_keypair_from_secretkey_and_publickey(sk=None, pk=None, *args_):
            
            return ParagonIE_Sodium_Compat.crypto_box_keypair_from_secretkey_and_publickey(sk, pk)
        # end def crypto_box_keypair_from_secretkey_and_publickey
    # end if
    if (not php_is_callable("\\Sodium\\crypto_box_open")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_box_open()
        #// @param string $message
        #// @param string $nonce
        #// @param string $kp
        #// @return string|bool
        #//
        def crypto_box_open(message=None, nonce=None, kp=None, *args_):
            
            try: 
                return ParagonIE_Sodium_Compat.crypto_box_open(message, nonce, kp)
            except TypeError as ex:
                return False
            except SodiumException as ex:
                return False
            # end try
        # end def crypto_box_open
    # end if
    if (not php_is_callable("\\Sodium\\crypto_box_publickey")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_box_publickey()
        #// @param string $keypair
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_box_publickey(keypair=None, *args_):
            
            return ParagonIE_Sodium_Compat.crypto_box_publickey(keypair)
        # end def crypto_box_publickey
    # end if
    if (not php_is_callable("\\Sodium\\crypto_box_publickey_from_secretkey")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_box_publickey_from_secretkey()
        #// @param string $sk
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_box_publickey_from_secretkey(sk=None, *args_):
            
            return ParagonIE_Sodium_Compat.crypto_box_publickey_from_secretkey(sk)
        # end def crypto_box_publickey_from_secretkey
    # end if
    if (not php_is_callable("\\Sodium\\crypto_box_seal")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_box_seal_open()
        #// @param string $message
        #// @param string $publicKey
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_box_seal(message=None, publicKey=None, *args_):
            
            return ParagonIE_Sodium_Compat.crypto_box_seal(message, publicKey)
        # end def crypto_box_seal
    # end if
    if (not php_is_callable("\\Sodium\\crypto_box_seal_open")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_box_seal_open()
        #// @param string $message
        #// @param string $kp
        #// @return string|bool
        #//
        def crypto_box_seal_open(message=None, kp=None, *args_):
            
            try: 
                return ParagonIE_Sodium_Compat.crypto_box_seal_open(message, kp)
            except TypeError as ex:
                return False
            except SodiumException as ex:
                return False
            # end try
        # end def crypto_box_seal_open
    # end if
    if (not php_is_callable("\\Sodium\\crypto_box_secretkey")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_box_secretkey()
        #// @param string $keypair
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_box_secretkey(keypair=None, *args_):
            
            return ParagonIE_Sodium_Compat.crypto_box_secretkey(keypair)
        # end def crypto_box_secretkey
    # end if
    if (not php_is_callable("\\Sodium\\crypto_generichash")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_generichash()
        #// @param string $message
        #// @param string|null $key
        #// @param int $outLen
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_generichash(message=None, key=None, outLen=32, *args_):
            
            return ParagonIE_Sodium_Compat.crypto_generichash(message, key, outLen)
        # end def crypto_generichash
    # end if
    if (not php_is_callable("\\Sodium\\crypto_generichash_final")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_generichash_final()
        #// @param string|null $ctx
        #// @param int $outputLength
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_generichash_final(ctx=None, outputLength=32, *args_):
            
            return ParagonIE_Sodium_Compat.crypto_generichash_final(ctx, outputLength)
        # end def crypto_generichash_final
    # end if
    if (not php_is_callable("\\Sodium\\crypto_generichash_init")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_generichash_init()
        #// @param string|null $key
        #// @param int $outLen
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_generichash_init(key=None, outLen=32, *args_):
            
            return ParagonIE_Sodium_Compat.crypto_generichash_init(key, outLen)
        # end def crypto_generichash_init
    # end if
    if (not php_is_callable("\\Sodium\\crypto_generichash_update")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_generichash_update()
        #// @param string|null $ctx
        #// @param string $message
        #// @return void
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_generichash_update(ctx=None, message="", *args_):
            
            ParagonIE_Sodium_Compat.crypto_generichash_update(ctx, message)
        # end def crypto_generichash_update
    # end if
    if (not php_is_callable("\\Sodium\\crypto_kx")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_kx()
        #// @param string $my_secret
        #// @param string $their_public
        #// @param string $client_public
        #// @param string $server_public
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_kx(my_secret=None, their_public=None, client_public=None, server_public=None, *args_):
            
            return ParagonIE_Sodium_Compat.crypto_kx(my_secret, their_public, client_public, server_public)
        # end def crypto_kx
    # end if
    if (not php_is_callable("\\Sodium\\crypto_pwhash")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_pwhash()
        #// @param int $outlen
        #// @param string $passwd
        #// @param string $salt
        #// @param int $opslimit
        #// @param int $memlimit
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_pwhash(outlen=None, passwd=None, salt=None, opslimit=None, memlimit=None, *args_):
            
            return ParagonIE_Sodium_Compat.crypto_pwhash(outlen, passwd, salt, opslimit, memlimit)
        # end def crypto_pwhash
    # end if
    if (not php_is_callable("\\Sodium\\crypto_pwhash_str")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_pwhash_str()
        #// @param string $passwd
        #// @param int $opslimit
        #// @param int $memlimit
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_pwhash_str(passwd=None, opslimit=None, memlimit=None, *args_):
            
            return ParagonIE_Sodium_Compat.crypto_pwhash_str(passwd, opslimit, memlimit)
        # end def crypto_pwhash_str
    # end if
    if (not php_is_callable("\\Sodium\\crypto_pwhash_str_verify")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_pwhash_str_verify()
        #// @param string $passwd
        #// @param string $hash
        #// @return bool
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_pwhash_str_verify(passwd=None, hash=None, *args_):
            
            return ParagonIE_Sodium_Compat.crypto_pwhash_str_verify(passwd, hash)
        # end def crypto_pwhash_str_verify
    # end if
    if (not php_is_callable("\\Sodium\\crypto_pwhash_scryptsalsa208sha256")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_pwhash_scryptsalsa208sha256()
        #// @param int $outlen
        #// @param string $passwd
        #// @param string $salt
        #// @param int $opslimit
        #// @param int $memlimit
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_pwhash_scryptsalsa208sha256(outlen=None, passwd=None, salt=None, opslimit=None, memlimit=None, *args_):
            
            return ParagonIE_Sodium_Compat.crypto_pwhash_scryptsalsa208sha256(outlen, passwd, salt, opslimit, memlimit)
        # end def crypto_pwhash_scryptsalsa208sha256
    # end if
    if (not php_is_callable("\\Sodium\\crypto_pwhash_scryptsalsa208sha256_str")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_pwhash_scryptsalsa208sha256_str()
        #// @param string $passwd
        #// @param int $opslimit
        #// @param int $memlimit
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_pwhash_scryptsalsa208sha256_str(passwd=None, opslimit=None, memlimit=None, *args_):
            
            return ParagonIE_Sodium_Compat.crypto_pwhash_scryptsalsa208sha256_str(passwd, opslimit, memlimit)
        # end def crypto_pwhash_scryptsalsa208sha256_str
    # end if
    if (not php_is_callable("\\Sodium\\crypto_pwhash_scryptsalsa208sha256_str_verify")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_pwhash_scryptsalsa208sha256_str_verify()
        #// @param string $passwd
        #// @param string $hash
        #// @return bool
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_pwhash_scryptsalsa208sha256_str_verify(passwd=None, hash=None, *args_):
            
            return ParagonIE_Sodium_Compat.crypto_pwhash_scryptsalsa208sha256_str_verify(passwd, hash)
        # end def crypto_pwhash_scryptsalsa208sha256_str_verify
    # end if
    if (not php_is_callable("\\Sodium\\crypto_scalarmult")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_scalarmult()
        #// @param string $n
        #// @param string $p
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_scalarmult(n=None, p=None, *args_):
            
            return ParagonIE_Sodium_Compat.crypto_scalarmult(n, p)
        # end def crypto_scalarmult
    # end if
    if (not php_is_callable("\\Sodium\\crypto_scalarmult_base")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_scalarmult_base()
        #// @param string $n
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_scalarmult_base(n=None, *args_):
            
            return ParagonIE_Sodium_Compat.crypto_scalarmult_base(n)
        # end def crypto_scalarmult_base
    # end if
    if (not php_is_callable("\\Sodium\\crypto_secretbox")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_secretbox()
        #// @param string $message
        #// @param string $nonce
        #// @param string $key
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_secretbox(message=None, nonce=None, key=None, *args_):
            
            return ParagonIE_Sodium_Compat.crypto_secretbox(message, nonce, key)
        # end def crypto_secretbox
    # end if
    if (not php_is_callable("\\Sodium\\crypto_secretbox_open")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_secretbox_open()
        #// @param string $message
        #// @param string $nonce
        #// @param string $key
        #// @return string|bool
        #//
        def crypto_secretbox_open(message=None, nonce=None, key=None, *args_):
            
            try: 
                return ParagonIE_Sodium_Compat.crypto_secretbox_open(message, nonce, key)
            except TypeError as ex:
                return False
            except SodiumException as ex:
                return False
            # end try
        # end def crypto_secretbox_open
    # end if
    if (not php_is_callable("\\Sodium\\crypto_shorthash")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_shorthash()
        #// @param string $message
        #// @param string $key
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_shorthash(message=None, key="", *args_):
            
            return ParagonIE_Sodium_Compat.crypto_shorthash(message, key)
        # end def crypto_shorthash
    # end if
    if (not php_is_callable("\\Sodium\\crypto_sign")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_sign()
        #// @param string $message
        #// @param string $sk
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_sign(message=None, sk=None, *args_):
            
            return ParagonIE_Sodium_Compat.crypto_sign(message, sk)
        # end def crypto_sign
    # end if
    if (not php_is_callable("\\Sodium\\crypto_sign_detached")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_sign_detached()
        #// @param string $message
        #// @param string $sk
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_sign_detached(message=None, sk=None, *args_):
            
            return ParagonIE_Sodium_Compat.crypto_sign_detached(message, sk)
        # end def crypto_sign_detached
    # end if
    if (not php_is_callable("\\Sodium\\crypto_sign_keypair")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_sign_keypair()
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_sign_keypair(*args_):
            
            return ParagonIE_Sodium_Compat.crypto_sign_keypair()
        # end def crypto_sign_keypair
    # end if
    if (not php_is_callable("\\Sodium\\crypto_sign_open")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_sign_open()
        #// @param string $signedMessage
        #// @param string $pk
        #// @return string|bool
        #//
        def crypto_sign_open(signedMessage=None, pk=None, *args_):
            
            try: 
                return ParagonIE_Sodium_Compat.crypto_sign_open(signedMessage, pk)
            except TypeError as ex:
                return False
            except SodiumException as ex:
                return False
            # end try
        # end def crypto_sign_open
    # end if
    if (not php_is_callable("\\Sodium\\crypto_sign_publickey")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_sign_publickey()
        #// @param string $keypair
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_sign_publickey(keypair=None, *args_):
            
            return ParagonIE_Sodium_Compat.crypto_sign_publickey(keypair)
        # end def crypto_sign_publickey
    # end if
    if (not php_is_callable("\\Sodium\\crypto_sign_publickey_from_secretkey")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_sign_publickey_from_secretkey()
        #// @param string $sk
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_sign_publickey_from_secretkey(sk=None, *args_):
            
            return ParagonIE_Sodium_Compat.crypto_sign_publickey_from_secretkey(sk)
        # end def crypto_sign_publickey_from_secretkey
    # end if
    if (not php_is_callable("\\Sodium\\crypto_sign_secretkey")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_sign_secretkey()
        #// @param string $keypair
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_sign_secretkey(keypair=None, *args_):
            
            return ParagonIE_Sodium_Compat.crypto_sign_secretkey(keypair)
        # end def crypto_sign_secretkey
    # end if
    if (not php_is_callable("\\Sodium\\crypto_sign_seed_keypair")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_sign_seed_keypair()
        #// @param string $seed
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_sign_seed_keypair(seed=None, *args_):
            
            return ParagonIE_Sodium_Compat.crypto_sign_seed_keypair(seed)
        # end def crypto_sign_seed_keypair
    # end if
    if (not php_is_callable("\\Sodium\\crypto_sign_verify_detached")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_sign_verify_detached()
        #// @param string $signature
        #// @param string $message
        #// @param string $pk
        #// @return bool
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_sign_verify_detached(signature=None, message=None, pk=None, *args_):
            
            return ParagonIE_Sodium_Compat.crypto_sign_verify_detached(signature, message, pk)
        # end def crypto_sign_verify_detached
    # end if
    if (not php_is_callable("\\Sodium\\crypto_sign_ed25519_pk_to_curve25519")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_sign_ed25519_pk_to_curve25519()
        #// @param string $pk
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_sign_ed25519_pk_to_curve25519(pk=None, *args_):
            
            return ParagonIE_Sodium_Compat.crypto_sign_ed25519_pk_to_curve25519(pk)
        # end def crypto_sign_ed25519_pk_to_curve25519
    # end if
    if (not php_is_callable("\\Sodium\\crypto_sign_ed25519_sk_to_curve25519")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_sign_ed25519_sk_to_curve25519()
        #// @param string $sk
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_sign_ed25519_sk_to_curve25519(sk=None, *args_):
            
            return ParagonIE_Sodium_Compat.crypto_sign_ed25519_sk_to_curve25519(sk)
        # end def crypto_sign_ed25519_sk_to_curve25519
    # end if
    if (not php_is_callable("\\Sodium\\crypto_stream")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_stream()
        #// @param int $len
        #// @param string $nonce
        #// @param string $key
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_stream(len=None, nonce=None, key=None, *args_):
            
            return ParagonIE_Sodium_Compat.crypto_stream(len, nonce, key)
        # end def crypto_stream
    # end if
    if (not php_is_callable("\\Sodium\\crypto_stream_xor")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_stream_xor()
        #// @param string $message
        #// @param string $nonce
        #// @param string $key
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_stream_xor(message=None, nonce=None, key=None, *args_):
            
            return ParagonIE_Sodium_Compat.crypto_stream_xor(message, nonce, key)
        # end def crypto_stream_xor
    # end if
    if (not php_is_callable("\\Sodium\\hex2bin")):
        #// 
        #// @see ParagonIE_Sodium_Compat::hex2bin()
        #// @param string $string
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def hex2bin(string=None, *args_):
            
            return ParagonIE_Sodium_Compat.hex2bin(string)
        # end def hex2bin
    # end if
    if (not php_is_callable("\\Sodium\\memcmp")):
        #// 
        #// @see ParagonIE_Sodium_Compat::memcmp()
        #// @param string $a
        #// @param string $b
        #// @return int
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def memcmp(a=None, b=None, *args_):
            
            return ParagonIE_Sodium_Compat.memcmp(a, b)
        # end def memcmp
    # end if
    if (not php_is_callable("\\Sodium\\memzero")):
        #// 
        #// @see ParagonIE_Sodium_Compat::memzero()
        #// @param string $str
        #// @return void
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def memzero(str=None, *args_):
            
            ParagonIE_Sodium_Compat.memzero(str)
        # end def memzero
    # end if
    if (not php_is_callable("\\Sodium\\randombytes_buf")):
        #// 
        #// @see ParagonIE_Sodium_Compat::randombytes_buf()
        #// @param int $amount
        #// @return string
        #// @throws \TypeError
        #//
        def randombytes_buf(amount=None, *args_):
            
            return ParagonIE_Sodium_Compat.randombytes_buf(amount)
        # end def randombytes_buf
    # end if
    if (not php_is_callable("\\Sodium\\randombytes_uniform")):
        #// 
        #// @see ParagonIE_Sodium_Compat::randombytes_uniform()
        #// @param int $upperLimit
        #// @return int
        #// @throws \SodiumException
        #// @throws \Error
        #//
        def randombytes_uniform(upperLimit=None, *args_):
            
            return ParagonIE_Sodium_Compat.randombytes_uniform(upperLimit)
        # end def randombytes_uniform
    # end if
    if (not php_is_callable("\\Sodium\\randombytes_random16")):
        #// 
        #// @see ParagonIE_Sodium_Compat::randombytes_random16()
        #// @return int
        #//
        def randombytes_random16(*args_):
            
            return ParagonIE_Sodium_Compat.randombytes_random16()
        # end def randombytes_random16
    # end if
    if (not php_defined("\\Sodium\\CRYPTO_AUTH_BYTES")):
        php_include_file(php_dirname(__FILE__) + "/constants.php", once=True)
    # end if
# end class
