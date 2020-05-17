#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
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
    ParagonIE_Sodium_Compat = php_new_class("ParagonIE_Sodium_Compat", lambda *args, **kwargs: ParagonIE_Sodium_Compat(*args, **kwargs))
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
        def bin2hex(string_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.bin2hex(string_)
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
        def compare(a_=None, b_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.compare(a_, b_)
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
        def crypto_aead_aes256gcm_decrypt(message_=None, assocData_=None, nonce_=None, key_=None, *_args_):
            
            
            try: 
                return ParagonIE_Sodium_Compat.crypto_aead_aes256gcm_decrypt(message_, assocData_, nonce_, key_)
            except TypeError as ex_:
                return False
            except SodiumException as ex_:
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
        def crypto_aead_aes256gcm_encrypt(message_=None, assocData_=None, nonce_=None, key_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_aead_aes256gcm_encrypt(message_, assocData_, nonce_, key_)
        # end def crypto_aead_aes256gcm_encrypt
    # end if
    if (not php_is_callable("\\Sodium\\crypto_aead_aes256gcm_is_available")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_aead_aes256gcm_is_available()
        #// @return bool
        #//
        def crypto_aead_aes256gcm_is_available(*_args_):
            
            
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
        def crypto_aead_chacha20poly1305_decrypt(message_=None, assocData_=None, nonce_=None, key_=None, *_args_):
            
            
            try: 
                return ParagonIE_Sodium_Compat.crypto_aead_chacha20poly1305_decrypt(message_, assocData_, nonce_, key_)
            except TypeError as ex_:
                return False
            except SodiumException as ex_:
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
        def crypto_aead_chacha20poly1305_encrypt(message_=None, assocData_=None, nonce_=None, key_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_aead_chacha20poly1305_encrypt(message_, assocData_, nonce_, key_)
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
        def crypto_aead_chacha20poly1305_ietf_decrypt(message_=None, assocData_=None, nonce_=None, key_=None, *_args_):
            
            
            try: 
                return ParagonIE_Sodium_Compat.crypto_aead_chacha20poly1305_ietf_decrypt(message_, assocData_, nonce_, key_)
            except TypeError as ex_:
                return False
            except SodiumException as ex_:
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
        def crypto_aead_chacha20poly1305_ietf_encrypt(message_=None, assocData_=None, nonce_=None, key_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_aead_chacha20poly1305_ietf_encrypt(message_, assocData_, nonce_, key_)
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
        def crypto_auth(message_=None, key_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_auth(message_, key_)
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
        def crypto_auth_verify(mac_=None, message_=None, key_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_auth_verify(mac_, message_, key_)
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
        def crypto_box(message_=None, nonce_=None, kp_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_box(message_, nonce_, kp_)
        # end def crypto_box
    # end if
    if (not php_is_callable("\\Sodium\\crypto_box_keypair")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_box_keypair()
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_box_keypair(*_args_):
            
            
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
        def crypto_box_keypair_from_secretkey_and_publickey(sk_=None, pk_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_box_keypair_from_secretkey_and_publickey(sk_, pk_)
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
        def crypto_box_open(message_=None, nonce_=None, kp_=None, *_args_):
            
            
            try: 
                return ParagonIE_Sodium_Compat.crypto_box_open(message_, nonce_, kp_)
            except TypeError as ex_:
                return False
            except SodiumException as ex_:
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
        def crypto_box_publickey(keypair_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_box_publickey(keypair_)
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
        def crypto_box_publickey_from_secretkey(sk_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_box_publickey_from_secretkey(sk_)
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
        def crypto_box_seal(message_=None, publicKey_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_box_seal(message_, publicKey_)
        # end def crypto_box_seal
    # end if
    if (not php_is_callable("\\Sodium\\crypto_box_seal_open")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_box_seal_open()
        #// @param string $message
        #// @param string $kp
        #// @return string|bool
        #//
        def crypto_box_seal_open(message_=None, kp_=None, *_args_):
            
            
            try: 
                return ParagonIE_Sodium_Compat.crypto_box_seal_open(message_, kp_)
            except TypeError as ex_:
                return False
            except SodiumException as ex_:
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
        def crypto_box_secretkey(keypair_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_box_secretkey(keypair_)
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
        def crypto_generichash(message_=None, key_=None, outLen_=32, *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_generichash(message_, key_, outLen_)
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
        def crypto_generichash_final(ctx_=None, outputLength_=32, *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_generichash_final(ctx_, outputLength_)
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
        def crypto_generichash_init(key_=None, outLen_=32, *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_generichash_init(key_, outLen_)
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
        def crypto_generichash_update(ctx_=None, message_="", *_args_):
            
            
            ParagonIE_Sodium_Compat.crypto_generichash_update(ctx_, message_)
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
        def crypto_kx(my_secret_=None, their_public_=None, client_public_=None, server_public_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_kx(my_secret_, their_public_, client_public_, server_public_)
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
        def crypto_pwhash(outlen_=None, passwd_=None, salt_=None, opslimit_=None, memlimit_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_pwhash(outlen_, passwd_, salt_, opslimit_, memlimit_)
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
        def crypto_pwhash_str(passwd_=None, opslimit_=None, memlimit_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_pwhash_str(passwd_, opslimit_, memlimit_)
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
        def crypto_pwhash_str_verify(passwd_=None, hash_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_pwhash_str_verify(passwd_, hash_)
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
        def crypto_pwhash_scryptsalsa208sha256(outlen_=None, passwd_=None, salt_=None, opslimit_=None, memlimit_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_pwhash_scryptsalsa208sha256(outlen_, passwd_, salt_, opslimit_, memlimit_)
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
        def crypto_pwhash_scryptsalsa208sha256_str(passwd_=None, opslimit_=None, memlimit_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_pwhash_scryptsalsa208sha256_str(passwd_, opslimit_, memlimit_)
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
        def crypto_pwhash_scryptsalsa208sha256_str_verify(passwd_=None, hash_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_pwhash_scryptsalsa208sha256_str_verify(passwd_, hash_)
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
        def crypto_scalarmult(n_=None, p_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_scalarmult(n_, p_)
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
        def crypto_scalarmult_base(n_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_scalarmult_base(n_)
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
        def crypto_secretbox(message_=None, nonce_=None, key_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_secretbox(message_, nonce_, key_)
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
        def crypto_secretbox_open(message_=None, nonce_=None, key_=None, *_args_):
            
            
            try: 
                return ParagonIE_Sodium_Compat.crypto_secretbox_open(message_, nonce_, key_)
            except TypeError as ex_:
                return False
            except SodiumException as ex_:
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
        def crypto_shorthash(message_=None, key_="", *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_shorthash(message_, key_)
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
        def crypto_sign(message_=None, sk_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_sign(message_, sk_)
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
        def crypto_sign_detached(message_=None, sk_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_sign_detached(message_, sk_)
        # end def crypto_sign_detached
    # end if
    if (not php_is_callable("\\Sodium\\crypto_sign_keypair")):
        #// 
        #// @see ParagonIE_Sodium_Compat::crypto_sign_keypair()
        #// @return string
        #// @throws \SodiumException
        #// @throws \TypeError
        #//
        def crypto_sign_keypair(*_args_):
            
            
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
        def crypto_sign_open(signedMessage_=None, pk_=None, *_args_):
            
            
            try: 
                return ParagonIE_Sodium_Compat.crypto_sign_open(signedMessage_, pk_)
            except TypeError as ex_:
                return False
            except SodiumException as ex_:
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
        def crypto_sign_publickey(keypair_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_sign_publickey(keypair_)
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
        def crypto_sign_publickey_from_secretkey(sk_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_sign_publickey_from_secretkey(sk_)
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
        def crypto_sign_secretkey(keypair_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_sign_secretkey(keypair_)
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
        def crypto_sign_seed_keypair(seed_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_sign_seed_keypair(seed_)
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
        def crypto_sign_verify_detached(signature_=None, message_=None, pk_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_sign_verify_detached(signature_, message_, pk_)
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
        def crypto_sign_ed25519_pk_to_curve25519(pk_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_sign_ed25519_pk_to_curve25519(pk_)
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
        def crypto_sign_ed25519_sk_to_curve25519(sk_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_sign_ed25519_sk_to_curve25519(sk_)
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
        def crypto_stream(len_=None, nonce_=None, key_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_stream(len_, nonce_, key_)
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
        def crypto_stream_xor(message_=None, nonce_=None, key_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.crypto_stream_xor(message_, nonce_, key_)
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
        def hex2bin(string_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.hex2bin(string_)
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
        def memcmp(a_=None, b_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.memcmp(a_, b_)
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
        def memzero(str_=None, *_args_):
            
            
            ParagonIE_Sodium_Compat.memzero(str_)
        # end def memzero
    # end if
    if (not php_is_callable("\\Sodium\\randombytes_buf")):
        #// 
        #// @see ParagonIE_Sodium_Compat::randombytes_buf()
        #// @param int $amount
        #// @return string
        #// @throws \TypeError
        #//
        def randombytes_buf(amount_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.randombytes_buf(amount_)
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
        def randombytes_uniform(upperLimit_=None, *_args_):
            
            
            return ParagonIE_Sodium_Compat.randombytes_uniform(upperLimit_)
        # end def randombytes_uniform
    # end if
    if (not php_is_callable("\\Sodium\\randombytes_random16")):
        #// 
        #// @see ParagonIE_Sodium_Compat::randombytes_random16()
        #// @return int
        #//
        def randombytes_random16(*_args_):
            
            
            return ParagonIE_Sodium_Compat.randombytes_random16()
        # end def randombytes_random16
    # end if
    if (not php_defined("\\Sodium\\CRYPTO_AUTH_BYTES")):
        php_include_file(php_dirname(__FILE__) + "/constants.php", once=True)
    # end if
# end class
