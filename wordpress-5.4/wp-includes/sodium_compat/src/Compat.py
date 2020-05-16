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
#// Libsodium compatibility layer
#// 
#// This is the only class you should be interfacing with, as a user of
#// sodium_compat.
#// 
#// If the PHP extension for libsodium is installed, it will always use that
#// instead of our implementations. You get better performance and stronger
#// guarantees against side-channels that way.
#// 
#// However, if your users don't have the PHP extension installed, we offer a
#// compatible interface here. It will give you the correct results as if the
#// PHP extension was installed. It won't be as fast, of course.
#// 
#// CAUTION * CAUTION * CAUTION * CAUTION * CAUTION * CAUTION * CAUTION * CAUTION
#// 
#// Until audited, this is probably not safe to use! DANGER WILL ROBINSON
#// 
#// CAUTION * CAUTION * CAUTION * CAUTION * CAUTION * CAUTION * CAUTION * CAUTION
#//
if php_class_exists("ParagonIE_Sodium_Compat", False):
    sys.exit(-1)
# end if
class ParagonIE_Sodium_Compat():
    disableFallbackForUnitTests = False
    fastMult = False
    LIBRARY_VERSION_MAJOR = 9
    LIBRARY_VERSION_MINOR = 1
    VERSION_STRING = "polyfill-1.0.8"
    BASE64_VARIANT_ORIGINAL = 1
    BASE64_VARIANT_ORIGINAL_NO_PADDING = 3
    BASE64_VARIANT_URLSAFE = 5
    BASE64_VARIANT_URLSAFE_NO_PADDING = 7
    CRYPTO_AEAD_AES256GCM_KEYBYTES = 32
    CRYPTO_AEAD_AES256GCM_NSECBYTES = 0
    CRYPTO_AEAD_AES256GCM_NPUBBYTES = 12
    CRYPTO_AEAD_AES256GCM_ABYTES = 16
    CRYPTO_AEAD_CHACHA20POLY1305_KEYBYTES = 32
    CRYPTO_AEAD_CHACHA20POLY1305_NSECBYTES = 0
    CRYPTO_AEAD_CHACHA20POLY1305_NPUBBYTES = 8
    CRYPTO_AEAD_CHACHA20POLY1305_ABYTES = 16
    CRYPTO_AEAD_CHACHA20POLY1305_IETF_KEYBYTES = 32
    CRYPTO_AEAD_CHACHA20POLY1305_IETF_NSECBYTES = 0
    CRYPTO_AEAD_CHACHA20POLY1305_IETF_NPUBBYTES = 12
    CRYPTO_AEAD_CHACHA20POLY1305_IETF_ABYTES = 16
    CRYPTO_AEAD_XCHACHA20POLY1305_IETF_KEYBYTES = 32
    CRYPTO_AEAD_XCHACHA20POLY1305_IETF_NSECBYTES = 0
    CRYPTO_AEAD_XCHACHA20POLY1305_IETF_NPUBBYTES = 24
    CRYPTO_AEAD_XCHACHA20POLY1305_IETF_ABYTES = 16
    CRYPTO_AUTH_BYTES = 32
    CRYPTO_AUTH_KEYBYTES = 32
    CRYPTO_BOX_SEALBYTES = 16
    CRYPTO_BOX_SECRETKEYBYTES = 32
    CRYPTO_BOX_PUBLICKEYBYTES = 32
    CRYPTO_BOX_KEYPAIRBYTES = 64
    CRYPTO_BOX_MACBYTES = 16
    CRYPTO_BOX_NONCEBYTES = 24
    CRYPTO_BOX_SEEDBYTES = 32
    CRYPTO_KDF_BYTES_MIN = 16
    CRYPTO_KDF_BYTES_MAX = 64
    CRYPTO_KDF_CONTEXTBYTES = 8
    CRYPTO_KDF_KEYBYTES = 32
    CRYPTO_KX_BYTES = 32
    CRYPTO_KX_PRIMITIVE = "x25519blake2b"
    CRYPTO_KX_SEEDBYTES = 32
    CRYPTO_KX_KEYPAIRBYTES = 64
    CRYPTO_KX_PUBLICKEYBYTES = 32
    CRYPTO_KX_SECRETKEYBYTES = 32
    CRYPTO_KX_SESSIONKEYBYTES = 32
    CRYPTO_GENERICHASH_BYTES = 32
    CRYPTO_GENERICHASH_BYTES_MIN = 16
    CRYPTO_GENERICHASH_BYTES_MAX = 64
    CRYPTO_GENERICHASH_KEYBYTES = 32
    CRYPTO_GENERICHASH_KEYBYTES_MIN = 16
    CRYPTO_GENERICHASH_KEYBYTES_MAX = 64
    CRYPTO_PWHASH_SALTBYTES = 16
    CRYPTO_PWHASH_STRPREFIX = "$argon2id$"
    CRYPTO_PWHASH_ALG_ARGON2I13 = 1
    CRYPTO_PWHASH_ALG_ARGON2ID13 = 2
    CRYPTO_PWHASH_MEMLIMIT_INTERACTIVE = 33554432
    CRYPTO_PWHASH_OPSLIMIT_INTERACTIVE = 4
    CRYPTO_PWHASH_MEMLIMIT_MODERATE = 134217728
    CRYPTO_PWHASH_OPSLIMIT_MODERATE = 6
    CRYPTO_PWHASH_MEMLIMIT_SENSITIVE = 536870912
    CRYPTO_PWHASH_OPSLIMIT_SENSITIVE = 8
    CRYPTO_PWHASH_SCRYPTSALSA208SHA256_SALTBYTES = 32
    CRYPTO_PWHASH_SCRYPTSALSA208SHA256_STRPREFIX = "$7$"
    CRYPTO_PWHASH_SCRYPTSALSA208SHA256_OPSLIMIT_INTERACTIVE = 534288
    CRYPTO_PWHASH_SCRYPTSALSA208SHA256_MEMLIMIT_INTERACTIVE = 16777216
    CRYPTO_PWHASH_SCRYPTSALSA208SHA256_OPSLIMIT_SENSITIVE = 33554432
    CRYPTO_PWHASH_SCRYPTSALSA208SHA256_MEMLIMIT_SENSITIVE = 1073741824
    CRYPTO_SCALARMULT_BYTES = 32
    CRYPTO_SCALARMULT_SCALARBYTES = 32
    CRYPTO_SHORTHASH_BYTES = 8
    CRYPTO_SHORTHASH_KEYBYTES = 16
    CRYPTO_SECRETBOX_KEYBYTES = 32
    CRYPTO_SECRETBOX_MACBYTES = 16
    CRYPTO_SECRETBOX_NONCEBYTES = 24
    CRYPTO_SECRETSTREAM_XCHACHA20POLY1305_ABYTES = 17
    CRYPTO_SECRETSTREAM_XCHACHA20POLY1305_HEADERBYTES = 24
    CRYPTO_SECRETSTREAM_XCHACHA20POLY1305_KEYBYTES = 32
    CRYPTO_SECRETSTREAM_XCHACHA20POLY1305_TAG_PUSH = 0
    CRYPTO_SECRETSTREAM_XCHACHA20POLY1305_TAG_PULL = 1
    CRYPTO_SECRETSTREAM_XCHACHA20POLY1305_TAG_REKEY = 2
    CRYPTO_SECRETSTREAM_XCHACHA20POLY1305_TAG_FINAL = 3
    CRYPTO_SECRETSTREAM_XCHACHA20POLY1305_MESSAGEBYTES_MAX = 274877906816
    CRYPTO_SIGN_BYTES = 64
    CRYPTO_SIGN_SEEDBYTES = 32
    CRYPTO_SIGN_PUBLICKEYBYTES = 32
    CRYPTO_SIGN_SECRETKEYBYTES = 64
    CRYPTO_SIGN_KEYPAIRBYTES = 96
    CRYPTO_STREAM_KEYBYTES = 32
    CRYPTO_STREAM_NONCEBYTES = 24
    #// 
    #// Add two numbers (little-endian unsigned), storing the value in the first
    #// parameter.
    #// 
    #// This mutates $val.
    #// 
    #// @param string $val
    #// @param string $addv
    #// @return void
    #// @throws SodiumException
    #//
    @classmethod
    def add(self, val=None, addv=None):
        
        val_len = ParagonIE_Sodium_Core_Util.strlen(val)
        addv_len = ParagonIE_Sodium_Core_Util.strlen(addv)
        if val_len != addv_len:
            raise php_new_class("SodiumException", lambda : SodiumException("values must have the same length"))
        # end if
        A = ParagonIE_Sodium_Core_Util.stringtointarray(val)
        B = ParagonIE_Sodium_Core_Util.stringtointarray(addv)
        c = 0
        i = 0
        while i < val_len:
            
            c += A[i] + B[i]
            A[i] = c & 255
            c >>= 8
            i += 1
        # end while
        val = ParagonIE_Sodium_Core_Util.intarraytostring(A)
    # end def add
    #// 
    #// @param string $encoded
    #// @param int $variant
    #// @param string $ignore
    #// @return string
    #// @throws SodiumException
    #//
    @classmethod
    def base642bin(self, encoded=None, variant=None, ignore=""):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(encoded, "string", 1)
        #// @var string $encoded
        encoded = php_str(encoded)
        if ParagonIE_Sodium_Core_Util.strlen(encoded) == 0:
            return ""
        # end if
        #// Just strip before decoding
        if (not php_empty(lambda : ignore)):
            encoded = php_str_replace(ignore, "", encoded)
        # end if
        try: 
            for case in Switch(variant):
                if case(self.BASE64_VARIANT_ORIGINAL):
                    return ParagonIE_Sodium_Core_Base64_Original.decode(encoded, True)
                # end if
                if case(self.BASE64_VARIANT_ORIGINAL_NO_PADDING):
                    return ParagonIE_Sodium_Core_Base64_Original.decode(encoded, False)
                # end if
                if case(self.BASE64_VARIANT_URLSAFE):
                    return ParagonIE_Sodium_Core_Base64_UrlSafe.decode(encoded, True)
                # end if
                if case(self.BASE64_VARIANT_URLSAFE_NO_PADDING):
                    return ParagonIE_Sodium_Core_Base64_UrlSafe.decode(encoded, False)
                # end if
                if case():
                    raise php_new_class("SodiumException", lambda : SodiumException("invalid base64 variant identifier"))
                # end if
            # end for
        except Exception as ex:
            if type(ex).__name__ == "SodiumException":
                raise ex
            # end if
            raise php_new_class("SodiumException", lambda : SodiumException("invalid base64 string"))
        # end try
    # end def base642bin
    #// 
    #// @param string $decoded
    #// @param int $variant
    #// @return string
    #// @throws SodiumException
    #//
    @classmethod
    def bin2base64(self, decoded=None, variant=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(decoded, "string", 1)
        #// @var string $decoded
        decoded = php_str(decoded)
        if ParagonIE_Sodium_Core_Util.strlen(decoded) == 0:
            return ""
        # end if
        for case in Switch(variant):
            if case(self.BASE64_VARIANT_ORIGINAL):
                return ParagonIE_Sodium_Core_Base64_Original.encode(decoded)
            # end if
            if case(self.BASE64_VARIANT_ORIGINAL_NO_PADDING):
                return ParagonIE_Sodium_Core_Base64_Original.encodeunpadded(decoded)
            # end if
            if case(self.BASE64_VARIANT_URLSAFE):
                return ParagonIE_Sodium_Core_Base64_UrlSafe.encode(decoded)
            # end if
            if case(self.BASE64_VARIANT_URLSAFE_NO_PADDING):
                return ParagonIE_Sodium_Core_Base64_UrlSafe.encodeunpadded(decoded)
            # end if
            if case():
                raise php_new_class("SodiumException", lambda : SodiumException("invalid base64 variant identifier"))
            # end if
        # end for
    # end def bin2base64
    #// 
    #// Cache-timing-safe implementation of bin2hex().
    #// 
    #// @param string $string A string (probably raw binary)
    #// @return string        A hexadecimal-encoded string
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def bin2hex(self, string=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(string, "string", 1)
        if self.usenewsodiumapi():
            return php_str(sodium_bin2hex(string))
        # end if
        if self.use_fallback("bin2hex"):
            return php_str(php_call_user_func("\\Sodium\\bin2hex", string))
        # end if
        return ParagonIE_Sodium_Core_Util.bin2hex(string)
    # end def bin2hex
    #// 
    #// Compare two strings, in constant-time.
    #// Compared to memcmp(), compare() is more useful for sorting.
    #// 
    #// @param string $left  The left operand; must be a string
    #// @param string $right The right operand; must be a string
    #// @return int          If < 0 if the left operand is less than the right
    #// If = 0 if both strings are equal
    #// If > 0 if the right operand is less than the left
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def compare(self, left=None, right=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(left, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(right, "string", 2)
        if self.usenewsodiumapi():
            return php_int(sodium_compare(left, right))
        # end if
        if self.use_fallback("compare"):
            return php_int(php_call_user_func("\\Sodium\\compare", left, right))
        # end if
        return ParagonIE_Sodium_Core_Util.compare(left, right)
    # end def compare
    #// 
    #// Is AES-256-GCM even available to use?
    #// 
    #// @return bool
    #// @psalm-suppress UndefinedFunction
    #// @psalm-suppress MixedInferredReturnType
    #// @psalm-suppress MixedReturnStatement
    #//
    @classmethod
    def crypto_aead_aes256gcm_is_available(self):
        
        if self.usenewsodiumapi():
            return sodium_crypto_aead_aes256gcm_is_available()
        # end if
        if self.use_fallback("crypto_aead_aes256gcm_is_available"):
            return php_call_user_func("\\Sodium\\crypto_aead_aes256gcm_is_available")
        # end if
        if PHP_VERSION_ID < 70100:
            #// OpenSSL doesn't support AEAD before 7.1.0
            return False
        # end if
        if (not php_is_callable("openssl_encrypt")) or (not php_is_callable("openssl_decrypt")):
            #// OpenSSL isn't installed
            return False
        # end if
        return php_bool(php_in_array("aes-256-gcm", openssl_get_cipher_methods()))
    # end def crypto_aead_aes256gcm_is_available
    #// 
    #// Authenticated Encryption with Associated Data: Decryption
    #// 
    #// Algorithm:
    #// AES-256-GCM
    #// 
    #// This mode uses a 64-bit random nonce with a 64-bit counter.
    #// IETF mode uses a 96-bit random nonce with a 32-bit counter.
    #// 
    #// @param string $ciphertext Encrypted message (with Poly1305 MAC appended)
    #// @param string $assocData  Authenticated Associated Data (unencrypted)
    #// @param string $nonce      Number to be used only Once; must be 8 bytes
    #// @param string $key        Encryption key
    #// 
    #// @return string|bool       The original plaintext message
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #// @psalm-suppress MixedInferredReturnType
    #// @psalm-suppress MixedReturnStatement
    #//
    @classmethod
    def crypto_aead_aes256gcm_decrypt(self, ciphertext="", assocData="", nonce="", key=""):
        
        if (not self.crypto_aead_aes256gcm_is_available()):
            raise php_new_class("SodiumException", lambda : SodiumException("AES-256-GCM is not available"))
        # end if
        ParagonIE_Sodium_Core_Util.declarescalartype(ciphertext, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(assocData, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(nonce, "string", 3)
        ParagonIE_Sodium_Core_Util.declarescalartype(key, "string", 4)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(nonce) != self.CRYPTO_AEAD_AES256GCM_NPUBBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Nonce must be CRYPTO_AEAD_AES256GCM_NPUBBYTES long"))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(key) != self.CRYPTO_AEAD_AES256GCM_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Key must be CRYPTO_AEAD_AES256GCM_KEYBYTES long"))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(ciphertext) < self.CRYPTO_AEAD_AES256GCM_ABYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Message must be at least CRYPTO_AEAD_AES256GCM_ABYTES long"))
        # end if
        if (not php_is_callable("openssl_decrypt")):
            raise php_new_class("SodiumException", lambda : SodiumException("The OpenSSL extension is not installed, or openssl_decrypt() is not available"))
        # end if
        #// @var string $ctext
        ctext = ParagonIE_Sodium_Core_Util.substr(ciphertext, 0, -self.CRYPTO_AEAD_AES256GCM_ABYTES)
        #// @var string $authTag
        authTag = ParagonIE_Sodium_Core_Util.substr(ciphertext, -self.CRYPTO_AEAD_AES256GCM_ABYTES, 16)
        return openssl_decrypt(ctext, "aes-256-gcm", key, OPENSSL_RAW_DATA, nonce, authTag, assocData)
    # end def crypto_aead_aes256gcm_decrypt
    #// 
    #// Authenticated Encryption with Associated Data: Encryption
    #// 
    #// Algorithm:
    #// AES-256-GCM
    #// 
    #// @param string $plaintext Message to be encrypted
    #// @param string $assocData Authenticated Associated Data (unencrypted)
    #// @param string $nonce     Number to be used only Once; must be 8 bytes
    #// @param string $key       Encryption key
    #// 
    #// @return string           Ciphertext with a 16-byte GCM message
    #// authentication code appended
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_aead_aes256gcm_encrypt(self, plaintext="", assocData="", nonce="", key=""):
        
        if (not self.crypto_aead_aes256gcm_is_available()):
            raise php_new_class("SodiumException", lambda : SodiumException("AES-256-GCM is not available"))
        # end if
        ParagonIE_Sodium_Core_Util.declarescalartype(plaintext, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(assocData, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(nonce, "string", 3)
        ParagonIE_Sodium_Core_Util.declarescalartype(key, "string", 4)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(nonce) != self.CRYPTO_AEAD_AES256GCM_NPUBBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Nonce must be CRYPTO_AEAD_AES256GCM_NPUBBYTES long"))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(key) != self.CRYPTO_AEAD_AES256GCM_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Key must be CRYPTO_AEAD_AES256GCM_KEYBYTES long"))
        # end if
        if (not php_is_callable("openssl_encrypt")):
            raise php_new_class("SodiumException", lambda : SodiumException("The OpenSSL extension is not installed, or openssl_encrypt() is not available"))
        # end if
        authTag = ""
        ciphertext = openssl_encrypt(plaintext, "aes-256-gcm", key, OPENSSL_RAW_DATA, nonce, authTag, assocData)
        return ciphertext + authTag
    # end def crypto_aead_aes256gcm_encrypt
    #// 
    #// Return a secure random key for use with the AES-256-GCM
    #// symmetric AEAD interface.
    #// 
    #// @return string
    #// @throws Exception
    #// @throws Error
    #//
    @classmethod
    def crypto_aead_aes256gcm_keygen(self):
        
        return random_bytes(self.CRYPTO_AEAD_AES256GCM_KEYBYTES)
    # end def crypto_aead_aes256gcm_keygen
    #// 
    #// Authenticated Encryption with Associated Data: Decryption
    #// 
    #// Algorithm:
    #// ChaCha20-Poly1305
    #// 
    #// This mode uses a 64-bit random nonce with a 64-bit counter.
    #// IETF mode uses a 96-bit random nonce with a 32-bit counter.
    #// 
    #// @param string $ciphertext Encrypted message (with Poly1305 MAC appended)
    #// @param string $assocData  Authenticated Associated Data (unencrypted)
    #// @param string $nonce      Number to be used only Once; must be 8 bytes
    #// @param string $key        Encryption key
    #// 
    #// @return string            The original plaintext message
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #// @psalm-suppress MixedInferredReturnType
    #// @psalm-suppress MixedReturnStatement
    #//
    @classmethod
    def crypto_aead_chacha20poly1305_decrypt(self, ciphertext="", assocData="", nonce="", key=""):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(ciphertext, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(assocData, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(nonce, "string", 3)
        ParagonIE_Sodium_Core_Util.declarescalartype(key, "string", 4)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(nonce) != self.CRYPTO_AEAD_CHACHA20POLY1305_NPUBBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Nonce must be CRYPTO_AEAD_CHACHA20POLY1305_NPUBBYTES long"))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(key) != self.CRYPTO_AEAD_CHACHA20POLY1305_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Key must be CRYPTO_AEAD_CHACHA20POLY1305_KEYBYTES long"))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(ciphertext) < self.CRYPTO_AEAD_CHACHA20POLY1305_ABYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Message must be at least CRYPTO_AEAD_CHACHA20POLY1305_ABYTES long"))
        # end if
        if self.usenewsodiumapi():
            #// 
            #// @psalm-suppress InvalidReturnStatement
            #// @psalm-suppress FalsableReturnStatement
            #//
            return sodium_crypto_aead_chacha20poly1305_decrypt(ciphertext, assocData, nonce, key)
        # end if
        if self.use_fallback("crypto_aead_chacha20poly1305_decrypt"):
            return php_call_user_func("\\Sodium\\crypto_aead_chacha20poly1305_decrypt", ciphertext, assocData, nonce, key)
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.aead_chacha20poly1305_decrypt(ciphertext, assocData, nonce, key)
        # end if
        return ParagonIE_Sodium_Crypto.aead_chacha20poly1305_decrypt(ciphertext, assocData, nonce, key)
    # end def crypto_aead_chacha20poly1305_decrypt
    #// 
    #// Authenticated Encryption with Associated Data
    #// 
    #// Algorithm:
    #// ChaCha20-Poly1305
    #// 
    #// This mode uses a 64-bit random nonce with a 64-bit counter.
    #// IETF mode uses a 96-bit random nonce with a 32-bit counter.
    #// 
    #// @param string $plaintext Message to be encrypted
    #// @param string $assocData Authenticated Associated Data (unencrypted)
    #// @param string $nonce     Number to be used only Once; must be 8 bytes
    #// @param string $key       Encryption key
    #// 
    #// @return string           Ciphertext with a 16-byte Poly1305 message
    #// authentication code appended
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_aead_chacha20poly1305_encrypt(self, plaintext="", assocData="", nonce="", key=""):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(plaintext, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(assocData, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(nonce, "string", 3)
        ParagonIE_Sodium_Core_Util.declarescalartype(key, "string", 4)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(nonce) != self.CRYPTO_AEAD_CHACHA20POLY1305_NPUBBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Nonce must be CRYPTO_AEAD_CHACHA20POLY1305_NPUBBYTES long"))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(key) != self.CRYPTO_AEAD_CHACHA20POLY1305_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Key must be CRYPTO_AEAD_CHACHA20POLY1305_KEYBYTES long"))
        # end if
        if self.usenewsodiumapi():
            return php_str(sodium_crypto_aead_chacha20poly1305_encrypt(plaintext, assocData, nonce, key))
        # end if
        if self.use_fallback("crypto_aead_chacha20poly1305_encrypt"):
            return php_str(php_call_user_func("\\Sodium\\crypto_aead_chacha20poly1305_encrypt", plaintext, assocData, nonce, key))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.aead_chacha20poly1305_encrypt(plaintext, assocData, nonce, key)
        # end if
        return ParagonIE_Sodium_Crypto.aead_chacha20poly1305_encrypt(plaintext, assocData, nonce, key)
    # end def crypto_aead_chacha20poly1305_encrypt
    #// 
    #// Authenticated Encryption with Associated Data: Decryption
    #// 
    #// Algorithm:
    #// ChaCha20-Poly1305
    #// 
    #// IETF mode uses a 96-bit random nonce with a 32-bit counter.
    #// Regular mode uses a 64-bit random nonce with a 64-bit counter.
    #// 
    #// @param string $ciphertext Encrypted message (with Poly1305 MAC appended)
    #// @param string $assocData  Authenticated Associated Data (unencrypted)
    #// @param string $nonce      Number to be used only Once; must be 12 bytes
    #// @param string $key        Encryption key
    #// 
    #// @return string            The original plaintext message
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #// @psalm-suppress MixedInferredReturnType
    #// @psalm-suppress MixedReturnStatement
    #//
    @classmethod
    def crypto_aead_chacha20poly1305_ietf_decrypt(self, ciphertext="", assocData="", nonce="", key=""):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(ciphertext, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(assocData, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(nonce, "string", 3)
        ParagonIE_Sodium_Core_Util.declarescalartype(key, "string", 4)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(nonce) != self.CRYPTO_AEAD_CHACHA20POLY1305_IETF_NPUBBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Nonce must be CRYPTO_AEAD_CHACHA20POLY1305_IETF_NPUBBYTES long"))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(key) != self.CRYPTO_AEAD_CHACHA20POLY1305_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Key must be CRYPTO_AEAD_CHACHA20POLY1305_KEYBYTES long"))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(ciphertext) < self.CRYPTO_AEAD_CHACHA20POLY1305_ABYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Message must be at least CRYPTO_AEAD_CHACHA20POLY1305_ABYTES long"))
        # end if
        if self.usenewsodiumapi():
            #// 
            #// @psalm-suppress InvalidReturnStatement
            #// @psalm-suppress FalsableReturnStatement
            #//
            return sodium_crypto_aead_chacha20poly1305_ietf_decrypt(ciphertext, assocData, nonce, key)
        # end if
        if self.use_fallback("crypto_aead_chacha20poly1305_ietf_decrypt"):
            return php_call_user_func("\\Sodium\\crypto_aead_chacha20poly1305_ietf_decrypt", ciphertext, assocData, nonce, key)
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.aead_chacha20poly1305_ietf_decrypt(ciphertext, assocData, nonce, key)
        # end if
        return ParagonIE_Sodium_Crypto.aead_chacha20poly1305_ietf_decrypt(ciphertext, assocData, nonce, key)
    # end def crypto_aead_chacha20poly1305_ietf_decrypt
    #// 
    #// Return a secure random key for use with the ChaCha20-Poly1305
    #// symmetric AEAD interface.
    #// 
    #// @return string
    #// @throws Exception
    #// @throws Error
    #//
    @classmethod
    def crypto_aead_chacha20poly1305_keygen(self):
        
        return random_bytes(self.CRYPTO_AEAD_CHACHA20POLY1305_KEYBYTES)
    # end def crypto_aead_chacha20poly1305_keygen
    #// 
    #// Authenticated Encryption with Associated Data
    #// 
    #// Algorithm:
    #// ChaCha20-Poly1305
    #// 
    #// IETF mode uses a 96-bit random nonce with a 32-bit counter.
    #// Regular mode uses a 64-bit random nonce with a 64-bit counter.
    #// 
    #// @param string $plaintext Message to be encrypted
    #// @param string $assocData Authenticated Associated Data (unencrypted)
    #// @param string $nonce Number to be used only Once; must be 8 bytes
    #// @param string $key Encryption key
    #// 
    #// @return string           Ciphertext with a 16-byte Poly1305 message
    #// authentication code appended
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_aead_chacha20poly1305_ietf_encrypt(self, plaintext="", assocData="", nonce="", key=""):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(plaintext, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(assocData, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(nonce, "string", 3)
        ParagonIE_Sodium_Core_Util.declarescalartype(key, "string", 4)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(nonce) != self.CRYPTO_AEAD_CHACHA20POLY1305_IETF_NPUBBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Nonce must be CRYPTO_AEAD_CHACHA20POLY1305_IETF_NPUBBYTES long"))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(key) != self.CRYPTO_AEAD_CHACHA20POLY1305_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Key must be CRYPTO_AEAD_CHACHA20POLY1305_KEYBYTES long"))
        # end if
        if self.usenewsodiumapi():
            return php_str(sodium_crypto_aead_chacha20poly1305_ietf_encrypt(plaintext, assocData, nonce, key))
        # end if
        if self.use_fallback("crypto_aead_chacha20poly1305_ietf_encrypt"):
            return php_str(php_call_user_func("\\Sodium\\crypto_aead_chacha20poly1305_ietf_encrypt", plaintext, assocData, nonce, key))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.aead_chacha20poly1305_ietf_encrypt(plaintext, assocData, nonce, key)
        # end if
        return ParagonIE_Sodium_Crypto.aead_chacha20poly1305_ietf_encrypt(plaintext, assocData, nonce, key)
    # end def crypto_aead_chacha20poly1305_ietf_encrypt
    #// 
    #// Return a secure random key for use with the ChaCha20-Poly1305
    #// symmetric AEAD interface. (IETF version)
    #// 
    #// @return string
    #// @throws Exception
    #// @throws Error
    #//
    @classmethod
    def crypto_aead_chacha20poly1305_ietf_keygen(self):
        
        return random_bytes(self.CRYPTO_AEAD_CHACHA20POLY1305_IETF_KEYBYTES)
    # end def crypto_aead_chacha20poly1305_ietf_keygen
    #// 
    #// Authenticated Encryption with Associated Data: Decryption
    #// 
    #// Algorithm:
    #// XChaCha20-Poly1305
    #// 
    #// This mode uses a 64-bit random nonce with a 64-bit counter.
    #// IETF mode uses a 96-bit random nonce with a 32-bit counter.
    #// 
    #// @param string $ciphertext   Encrypted message (with Poly1305 MAC appended)
    #// @param string $assocData    Authenticated Associated Data (unencrypted)
    #// @param string $nonce        Number to be used only Once; must be 8 bytes
    #// @param string $key          Encryption key
    #// @param bool   $dontFallback Don't fallback to ext/sodium
    #// 
    #// @return string|bool         The original plaintext message
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_aead_xchacha20poly1305_ietf_decrypt(self, ciphertext="", assocData="", nonce="", key="", dontFallback=False):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(ciphertext, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(assocData, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(nonce, "string", 3)
        ParagonIE_Sodium_Core_Util.declarescalartype(key, "string", 4)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(nonce) != self.CRYPTO_AEAD_XCHACHA20POLY1305_IETF_NPUBBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Nonce must be CRYPTO_AEAD_XCHACHA20POLY1305_IETF_NPUBBYTES long"))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(key) != self.CRYPTO_AEAD_XCHACHA20POLY1305_IETF_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Key must be CRYPTO_AEAD_XCHACHA20POLY1305_IETF_KEYBYTES long"))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(ciphertext) < self.CRYPTO_AEAD_XCHACHA20POLY1305_IETF_ABYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Message must be at least CRYPTO_AEAD_XCHACHA20POLY1305_IETF_ABYTES long"))
        # end if
        if self.usenewsodiumapi() and (not dontFallback):
            if php_is_callable("sodium_crypto_aead_xchacha20poly1305_ietf_decrypt"):
                return sodium_crypto_aead_xchacha20poly1305_ietf_decrypt(ciphertext, assocData, nonce, key)
            # end if
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.aead_xchacha20poly1305_ietf_decrypt(ciphertext, assocData, nonce, key)
        # end if
        return ParagonIE_Sodium_Crypto.aead_xchacha20poly1305_ietf_decrypt(ciphertext, assocData, nonce, key)
    # end def crypto_aead_xchacha20poly1305_ietf_decrypt
    #// 
    #// Authenticated Encryption with Associated Data
    #// 
    #// Algorithm:
    #// XChaCha20-Poly1305
    #// 
    #// This mode uses a 64-bit random nonce with a 64-bit counter.
    #// IETF mode uses a 96-bit random nonce with a 32-bit counter.
    #// 
    #// @param string $plaintext    Message to be encrypted
    #// @param string $assocData    Authenticated Associated Data (unencrypted)
    #// @param string $nonce        Number to be used only Once; must be 8 bytes
    #// @param string $key          Encryption key
    #// @param bool   $dontFallback Don't fallback to ext/sodium
    #// 
    #// @return string           Ciphertext with a 16-byte Poly1305 message
    #// authentication code appended
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_aead_xchacha20poly1305_ietf_encrypt(self, plaintext="", assocData="", nonce="", key="", dontFallback=False):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(plaintext, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(assocData, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(nonce, "string", 3)
        ParagonIE_Sodium_Core_Util.declarescalartype(key, "string", 4)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(nonce) != self.CRYPTO_AEAD_XCHACHA20POLY1305_IETF_NPUBBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Nonce must be CRYPTO_AEAD_XCHACHA20POLY1305_NPUBBYTES long"))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(key) != self.CRYPTO_AEAD_XCHACHA20POLY1305_IETF_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Key must be CRYPTO_AEAD_XCHACHA20POLY1305_KEYBYTES long"))
        # end if
        if self.usenewsodiumapi() and (not dontFallback):
            if php_is_callable("sodium_crypto_aead_xchacha20poly1305_ietf_encrypt"):
                return sodium_crypto_aead_xchacha20poly1305_ietf_encrypt(plaintext, assocData, nonce, key)
            # end if
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.aead_xchacha20poly1305_ietf_encrypt(plaintext, assocData, nonce, key)
        # end if
        return ParagonIE_Sodium_Crypto.aead_xchacha20poly1305_ietf_encrypt(plaintext, assocData, nonce, key)
    # end def crypto_aead_xchacha20poly1305_ietf_encrypt
    #// 
    #// Return a secure random key for use with the XChaCha20-Poly1305
    #// symmetric AEAD interface.
    #// 
    #// @return string
    #// @throws Exception
    #// @throws Error
    #//
    @classmethod
    def crypto_aead_xchacha20poly1305_ietf_keygen(self):
        
        return random_bytes(self.CRYPTO_AEAD_XCHACHA20POLY1305_IETF_KEYBYTES)
    # end def crypto_aead_xchacha20poly1305_ietf_keygen
    #// 
    #// Authenticate a message. Uses symmetric-key cryptography.
    #// 
    #// Algorithm:
    #// HMAC-SHA512-256. Which is HMAC-SHA-512 truncated to 256 bits.
    #// Not to be confused with HMAC-SHA-512/256 which would use the
    #// SHA-512/256 hash function (uses different initial parameters
    #// but still truncates to 256 bits to sidestep length-extension
    #// attacks).
    #// 
    #// @param string $message Message to be authenticated
    #// @param string $key Symmetric authentication key
    #// @return string         Message authentication code
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_auth(self, message=None, key=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(message, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(key, "string", 2)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(key) != self.CRYPTO_AUTH_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_AUTH_KEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return php_str(sodium_crypto_auth(message, key))
        # end if
        if self.use_fallback("crypto_auth"):
            return php_str(php_call_user_func("\\Sodium\\crypto_auth", message, key))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.auth(message, key)
        # end if
        return ParagonIE_Sodium_Crypto.auth(message, key)
    # end def crypto_auth
    #// 
    #// @return string
    #// @throws Exception
    #// @throws Error
    #//
    @classmethod
    def crypto_auth_keygen(self):
        
        return random_bytes(self.CRYPTO_AUTH_KEYBYTES)
    # end def crypto_auth_keygen
    #// 
    #// Verify the MAC of a message previously authenticated with crypto_auth.
    #// 
    #// @param string $mac Message authentication code
    #// @param string $message Message whose authenticity you are attempting to
    #// verify (with a given MAC and key)
    #// @param string $key Symmetric authentication key
    #// @return bool           TRUE if authenticated, FALSE otherwise
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_auth_verify(self, mac=None, message=None, key=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(mac, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(message, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(key, "string", 3)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(mac) != self.CRYPTO_AUTH_BYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 1 must be CRYPTO_AUTH_BYTES long."))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(key) != self.CRYPTO_AUTH_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 3 must be CRYPTO_AUTH_KEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return php_bool(sodium_crypto_auth_verify(mac, message, key))
        # end if
        if self.use_fallback("crypto_auth_verify"):
            return php_bool(php_call_user_func("\\Sodium\\crypto_auth_verify", mac, message, key))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.auth_verify(mac, message, key)
        # end if
        return ParagonIE_Sodium_Crypto.auth_verify(mac, message, key)
    # end def crypto_auth_verify
    #// 
    #// Authenticated asymmetric-key encryption. Both the sender and recipient
    #// may decrypt messages.
    #// 
    #// Algorithm: X25519-XSalsa20-Poly1305.
    #// X25519: Elliptic-Curve Diffie Hellman over Curve25519.
    #// XSalsa20: Extended-nonce variant of salsa20.
    #// Poyl1305: Polynomial MAC for one-time message authentication.
    #// 
    #// @param string $plaintext The message to be encrypted
    #// @param string $nonce A Number to only be used Once; must be 24 bytes
    #// @param string $keypair Your secret key and your recipient's public key
    #// @return string           Ciphertext with 16-byte Poly1305 MAC
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_box(self, plaintext=None, nonce=None, keypair=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(plaintext, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(nonce, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(keypair, "string", 3)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(nonce) != self.CRYPTO_BOX_NONCEBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_BOX_NONCEBYTES long."))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(keypair) != self.CRYPTO_BOX_KEYPAIRBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 3 must be CRYPTO_BOX_KEYPAIRBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return php_str(sodium_crypto_box(plaintext, nonce, keypair))
        # end if
        if self.use_fallback("crypto_box"):
            return php_str(php_call_user_func("\\Sodium\\crypto_box", plaintext, nonce, keypair))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.box(plaintext, nonce, keypair)
        # end if
        return ParagonIE_Sodium_Crypto.box(plaintext, nonce, keypair)
    # end def crypto_box
    #// 
    #// Anonymous public-key encryption. Only the recipient may decrypt messages.
    #// 
    #// Algorithm: X25519-XSalsa20-Poly1305, as with crypto_box.
    #// The sender's X25519 keypair is ephemeral.
    #// Nonce is generated from the BLAKE2b hash of both public keys.
    #// 
    #// This provides ciphertext integrity.
    #// 
    #// @param string $plaintext Message to be sealed
    #// @param string $publicKey Your recipient's public key
    #// @return string           Sealed message that only your recipient can
    #// decrypt
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_box_seal(self, plaintext=None, publicKey=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(plaintext, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(publicKey, "string", 2)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(publicKey) != self.CRYPTO_BOX_PUBLICKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_BOX_PUBLICKEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return php_str(sodium_crypto_box_seal(plaintext, publicKey))
        # end if
        if self.use_fallback("crypto_box_seal"):
            return php_str(php_call_user_func("\\Sodium\\crypto_box_seal", plaintext, publicKey))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.box_seal(plaintext, publicKey)
        # end if
        return ParagonIE_Sodium_Crypto.box_seal(plaintext, publicKey)
    # end def crypto_box_seal
    #// 
    #// Opens a message encrypted with crypto_box_seal(). Requires
    #// the recipient's keypair (sk || pk) to decrypt successfully.
    #// 
    #// This validates ciphertext integrity.
    #// 
    #// @param string $ciphertext Sealed message to be opened
    #// @param string $keypair    Your crypto_box keypair
    #// @return string            The original plaintext message
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #// @psalm-suppress MixedInferredReturnType
    #// @psalm-suppress MixedReturnStatement
    #//
    @classmethod
    def crypto_box_seal_open(self, ciphertext=None, keypair=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(ciphertext, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(keypair, "string", 2)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(keypair) != self.CRYPTO_BOX_KEYPAIRBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_BOX_KEYPAIRBYTES long."))
        # end if
        if self.usenewsodiumapi():
            #// 
            #// @psalm-suppress InvalidReturnStatement
            #// @psalm-suppress FalsableReturnStatement
            #//
            return sodium_crypto_box_seal_open(ciphertext, keypair)
        # end if
        if self.use_fallback("crypto_box_seal_open"):
            return php_call_user_func("\\Sodium\\crypto_box_seal_open", ciphertext, keypair)
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.box_seal_open(ciphertext, keypair)
        # end if
        return ParagonIE_Sodium_Crypto.box_seal_open(ciphertext, keypair)
    # end def crypto_box_seal_open
    #// 
    #// Generate a new random X25519 keypair.
    #// 
    #// @return string A 64-byte string; the first 32 are your secret key, while
    #// the last 32 are your public key. crypto_box_secretkey()
    #// and crypto_box_publickey() exist to separate them so you
    #// don't accidentally get them mixed up!
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_box_keypair(self):
        
        if self.usenewsodiumapi():
            return php_str(sodium_crypto_box_keypair())
        # end if
        if self.use_fallback("crypto_box_keypair"):
            return php_str(php_call_user_func("\\Sodium\\crypto_box_keypair"))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.box_keypair()
        # end if
        return ParagonIE_Sodium_Crypto.box_keypair()
    # end def crypto_box_keypair
    #// 
    #// Combine two keys into a keypair for use in library methods that expect
    #// a keypair. This doesn't necessarily have to be the same person's keys.
    #// 
    #// @param string $secretKey Secret key
    #// @param string $publicKey Public key
    #// @return string    Keypair
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_box_keypair_from_secretkey_and_publickey(self, secretKey=None, publicKey=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(secretKey, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(publicKey, "string", 2)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(secretKey) != self.CRYPTO_BOX_SECRETKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 1 must be CRYPTO_BOX_SECRETKEYBYTES long."))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(publicKey) != self.CRYPTO_BOX_PUBLICKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_BOX_PUBLICKEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return php_str(sodium_crypto_box_keypair_from_secretkey_and_publickey(secretKey, publicKey))
        # end if
        if self.use_fallback("crypto_box_keypair_from_secretkey_and_publickey"):
            return php_str(php_call_user_func("\\Sodium\\crypto_box_keypair_from_secretkey_and_publickey", secretKey, publicKey))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.box_keypair_from_secretkey_and_publickey(secretKey, publicKey)
        # end if
        return ParagonIE_Sodium_Crypto.box_keypair_from_secretkey_and_publickey(secretKey, publicKey)
    # end def crypto_box_keypair_from_secretkey_and_publickey
    #// 
    #// Decrypt a message previously encrypted with crypto_box().
    #// 
    #// @param string $ciphertext Encrypted message
    #// @param string $nonce      Number to only be used Once; must be 24 bytes
    #// @param string $keypair    Your secret key and the sender's public key
    #// @return string            The original plaintext message
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #// @psalm-suppress MixedInferredReturnType
    #// @psalm-suppress MixedReturnStatement
    #//
    @classmethod
    def crypto_box_open(self, ciphertext=None, nonce=None, keypair=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(ciphertext, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(nonce, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(keypair, "string", 3)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(ciphertext) < self.CRYPTO_BOX_MACBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 1 must be at least CRYPTO_BOX_MACBYTES long."))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(nonce) != self.CRYPTO_BOX_NONCEBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_BOX_NONCEBYTES long."))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(keypair) != self.CRYPTO_BOX_KEYPAIRBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 3 must be CRYPTO_BOX_KEYPAIRBYTES long."))
        # end if
        if self.usenewsodiumapi():
            #// 
            #// @psalm-suppress InvalidReturnStatement
            #// @psalm-suppress FalsableReturnStatement
            #//
            return sodium_crypto_box_open(ciphertext, nonce, keypair)
        # end if
        if self.use_fallback("crypto_box_open"):
            return php_call_user_func("\\Sodium\\crypto_box_open", ciphertext, nonce, keypair)
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.box_open(ciphertext, nonce, keypair)
        # end if
        return ParagonIE_Sodium_Crypto.box_open(ciphertext, nonce, keypair)
    # end def crypto_box_open
    #// 
    #// Extract the public key from a crypto_box keypair.
    #// 
    #// @param string $keypair Keypair containing secret and public key
    #// @return string         Your crypto_box public key
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_box_publickey(self, keypair=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(keypair, "string", 1)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(keypair) != self.CRYPTO_BOX_KEYPAIRBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 1 must be CRYPTO_BOX_KEYPAIRBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return php_str(sodium_crypto_box_publickey(keypair))
        # end if
        if self.use_fallback("crypto_box_publickey"):
            return php_str(php_call_user_func("\\Sodium\\crypto_box_publickey", keypair))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.box_publickey(keypair)
        # end if
        return ParagonIE_Sodium_Crypto.box_publickey(keypair)
    # end def crypto_box_publickey
    #// 
    #// Calculate the X25519 public key from a given X25519 secret key.
    #// 
    #// @param string $secretKey Any X25519 secret key
    #// @return string           The corresponding X25519 public key
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_box_publickey_from_secretkey(self, secretKey=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(secretKey, "string", 1)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(secretKey) != self.CRYPTO_BOX_SECRETKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 1 must be CRYPTO_BOX_SECRETKEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return php_str(sodium_crypto_box_publickey_from_secretkey(secretKey))
        # end if
        if self.use_fallback("crypto_box_publickey_from_secretkey"):
            return php_str(php_call_user_func("\\Sodium\\crypto_box_publickey_from_secretkey", secretKey))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.box_publickey_from_secretkey(secretKey)
        # end if
        return ParagonIE_Sodium_Crypto.box_publickey_from_secretkey(secretKey)
    # end def crypto_box_publickey_from_secretkey
    #// 
    #// Extract the secret key from a crypto_box keypair.
    #// 
    #// @param string $keypair
    #// @return string         Your crypto_box secret key
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_box_secretkey(self, keypair=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(keypair, "string", 1)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(keypair) != self.CRYPTO_BOX_KEYPAIRBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 1 must be CRYPTO_BOX_KEYPAIRBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return php_str(sodium_crypto_box_secretkey(keypair))
        # end if
        if self.use_fallback("crypto_box_secretkey"):
            return php_str(php_call_user_func("\\Sodium\\crypto_box_secretkey", keypair))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.box_secretkey(keypair)
        # end if
        return ParagonIE_Sodium_Crypto.box_secretkey(keypair)
    # end def crypto_box_secretkey
    #// 
    #// Generate an X25519 keypair from a seed.
    #// 
    #// @param string $seed
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #// @psalm-suppress UndefinedFunction
    #//
    @classmethod
    def crypto_box_seed_keypair(self, seed=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(seed, "string", 1)
        if self.usenewsodiumapi():
            return php_str(sodium_crypto_box_seed_keypair(seed))
        # end if
        if self.use_fallback("crypto_box_seed_keypair"):
            return php_str(php_call_user_func("\\Sodium\\crypto_box_seed_keypair", seed))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.box_seed_keypair(seed)
        # end if
        return ParagonIE_Sodium_Crypto.box_seed_keypair(seed)
    # end def crypto_box_seed_keypair
    #// 
    #// Calculates a BLAKE2b hash, with an optional key.
    #// 
    #// @param string      $message The message to be hashed
    #// @param string|null $key     If specified, must be a string between 16
    #// and 64 bytes long
    #// @param int         $length  Output length in bytes; must be between 16
    #// and 64 (default = 32)
    #// @return string              Raw binary
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_generichash(self, message=None, key="", length=self.CRYPTO_GENERICHASH_BYTES):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(message, "string", 1)
        if is_null(key):
            key = ""
        # end if
        ParagonIE_Sodium_Core_Util.declarescalartype(key, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(length, "int", 3)
        #// Input validation:
        if (not php_empty(lambda : key)):
            if ParagonIE_Sodium_Core_Util.strlen(key) < self.CRYPTO_GENERICHASH_KEYBYTES_MIN:
                raise php_new_class("SodiumException", lambda : SodiumException("Unsupported key size. Must be at least CRYPTO_GENERICHASH_KEYBYTES_MIN bytes long."))
            # end if
            if ParagonIE_Sodium_Core_Util.strlen(key) > self.CRYPTO_GENERICHASH_KEYBYTES_MAX:
                raise php_new_class("SodiumException", lambda : SodiumException("Unsupported key size. Must be at most CRYPTO_GENERICHASH_KEYBYTES_MAX bytes long."))
            # end if
        # end if
        if self.usenewsodiumapi():
            return php_str(sodium_crypto_generichash(message, key, length))
        # end if
        if self.use_fallback("crypto_generichash"):
            return php_str(php_call_user_func("\\Sodium\\crypto_generichash", message, key, length))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.generichash(message, key, length)
        # end if
        return ParagonIE_Sodium_Crypto.generichash(message, key, length)
    # end def crypto_generichash
    #// 
    #// Get the final BLAKE2b hash output for a given context.
    #// 
    #// @param string $ctx BLAKE2 hashing context. Generated by crypto_generichash_init().
    #// @param int $length Hash output size.
    #// @return string     Final BLAKE2b hash.
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #// @psalm-suppress ReferenceConstraintViolation
    #// @psalm-suppress ConflictingReferenceConstraint
    #//
    @classmethod
    def crypto_generichash_final(self, ctx=None, length=self.CRYPTO_GENERICHASH_BYTES):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(ctx, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(length, "int", 2)
        if self.usenewsodiumapi():
            return sodium_crypto_generichash_final(ctx, length)
        # end if
        if self.use_fallback("crypto_generichash_final"):
            func = "\\Sodium\\crypto_generichash_final"
            return php_str(func(ctx, length))
        # end if
        if length < 1:
            try: 
                self.memzero(ctx)
            except SodiumException as ex:
                ctx = None
            # end try
            return ""
        # end if
        if PHP_INT_SIZE == 4:
            result = ParagonIE_Sodium_Crypto32.generichash_final(ctx, length)
        else:
            result = ParagonIE_Sodium_Crypto.generichash_final(ctx, length)
        # end if
        try: 
            self.memzero(ctx)
        except SodiumException as ex:
            ctx = None
        # end try
        return result
    # end def crypto_generichash_final
    #// 
    #// Initialize a BLAKE2b hashing context, for use in a streaming interface.
    #// 
    #// @param string|null $key If specified must be a string between 16 and 64 bytes
    #// @param int $length      The size of the desired hash output
    #// @return string          A BLAKE2 hashing context, encoded as a string
    #// (To be 100% compatible with ext/libsodium)
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_generichash_init(self, key="", length=self.CRYPTO_GENERICHASH_BYTES):
        
        #// Type checks:
        if is_null(key):
            key = ""
        # end if
        ParagonIE_Sodium_Core_Util.declarescalartype(key, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(length, "int", 2)
        #// Input validation:
        if (not php_empty(lambda : key)):
            if ParagonIE_Sodium_Core_Util.strlen(key) < self.CRYPTO_GENERICHASH_KEYBYTES_MIN:
                raise php_new_class("SodiumException", lambda : SodiumException("Unsupported key size. Must be at least CRYPTO_GENERICHASH_KEYBYTES_MIN bytes long."))
            # end if
            if ParagonIE_Sodium_Core_Util.strlen(key) > self.CRYPTO_GENERICHASH_KEYBYTES_MAX:
                raise php_new_class("SodiumException", lambda : SodiumException("Unsupported key size. Must be at most CRYPTO_GENERICHASH_KEYBYTES_MAX bytes long."))
            # end if
        # end if
        if self.usenewsodiumapi():
            return sodium_crypto_generichash_init(key, length)
        # end if
        if self.use_fallback("crypto_generichash_init"):
            return php_str(php_call_user_func("\\Sodium\\crypto_generichash_init", key, length))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.generichash_init(key, length)
        # end if
        return ParagonIE_Sodium_Crypto.generichash_init(key, length)
    # end def crypto_generichash_init
    #// 
    #// Initialize a BLAKE2b hashing context, for use in a streaming interface.
    #// 
    #// @param string|null $key If specified must be a string between 16 and 64 bytes
    #// @param int $length      The size of the desired hash output
    #// @param string $salt     Salt (up to 16 bytes)
    #// @param string $personal Personalization string (up to 16 bytes)
    #// @return string          A BLAKE2 hashing context, encoded as a string
    #// (To be 100% compatible with ext/libsodium)
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_generichash_init_salt_personal(self, key="", length=self.CRYPTO_GENERICHASH_BYTES, salt="", personal=""):
        
        #// Type checks:
        if is_null(key):
            key = ""
        # end if
        ParagonIE_Sodium_Core_Util.declarescalartype(key, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(length, "int", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(salt, "string", 3)
        ParagonIE_Sodium_Core_Util.declarescalartype(personal, "string", 4)
        salt = php_str_pad(salt, 16, " ", STR_PAD_RIGHT)
        personal = php_str_pad(personal, 16, " ", STR_PAD_RIGHT)
        #// Input validation:
        if (not php_empty(lambda : key)):
            #// 
            #// if (ParagonIE_Sodium_Core_Util::strlen($key) < self::CRYPTO_GENERICHASH_KEYBYTES_MIN) {
            #// throw new SodiumException('Unsupported key size. Must be at least CRYPTO_GENERICHASH_KEYBYTES_MIN bytes long.');
            #// }
            #//
            if ParagonIE_Sodium_Core_Util.strlen(key) > self.CRYPTO_GENERICHASH_KEYBYTES_MAX:
                raise php_new_class("SodiumException", lambda : SodiumException("Unsupported key size. Must be at most CRYPTO_GENERICHASH_KEYBYTES_MAX bytes long."))
            # end if
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.generichash_init_salt_personal(key, length, salt, personal)
        # end if
        return ParagonIE_Sodium_Crypto.generichash_init_salt_personal(key, length, salt, personal)
    # end def crypto_generichash_init_salt_personal
    #// 
    #// Update a BLAKE2b hashing context with additional data.
    #// 
    #// @param string $ctx    BLAKE2 hashing context. Generated by crypto_generichash_init().
    #// $ctx is passed by reference and gets updated in-place.
    #// @param-out string $ctx
    #// @param string $message The message to append to the existing hash state.
    #// @return void
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #// @psalm-suppress ReferenceConstraintViolation
    #//
    @classmethod
    def crypto_generichash_update(self, ctx=None, message=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(ctx, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(message, "string", 2)
        if self.usenewsodiumapi():
            sodium_crypto_generichash_update(ctx, message)
            return
        # end if
        if self.use_fallback("crypto_generichash_update"):
            func = "\\Sodium\\crypto_generichash_update"
            func(ctx, message)
            return
        # end if
        if PHP_INT_SIZE == 4:
            ctx = ParagonIE_Sodium_Crypto32.generichash_update(ctx, message)
        else:
            ctx = ParagonIE_Sodium_Crypto.generichash_update(ctx, message)
        # end if
    # end def crypto_generichash_update
    #// 
    #// @return string
    #// @throws Exception
    #// @throws Error
    #//
    @classmethod
    def crypto_generichash_keygen(self):
        
        return random_bytes(self.CRYPTO_GENERICHASH_KEYBYTES)
    # end def crypto_generichash_keygen
    #// 
    #// @param int $subkey_len
    #// @param int $subkey_id
    #// @param string $context
    #// @param string $key
    #// @return string
    #// @throws SodiumException
    #//
    @classmethod
    def crypto_kdf_derive_from_key(self, subkey_len=None, subkey_id=None, context=None, key=None):
        
        ParagonIE_Sodium_Core_Util.declarescalartype(subkey_len, "int", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(subkey_id, "int", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(context, "string", 3)
        ParagonIE_Sodium_Core_Util.declarescalartype(key, "string", 4)
        subkey_id = php_int(subkey_id)
        subkey_len = php_int(subkey_len)
        context = php_str(context)
        key = php_str(key)
        if subkey_len < self.CRYPTO_KDF_BYTES_MIN:
            raise php_new_class("SodiumException", lambda : SodiumException("subkey cannot be smaller than SODIUM_CRYPTO_KDF_BYTES_MIN"))
        # end if
        if subkey_len > self.CRYPTO_KDF_BYTES_MAX:
            raise php_new_class("SodiumException", lambda : SodiumException("subkey cannot be larger than SODIUM_CRYPTO_KDF_BYTES_MAX"))
        # end if
        if subkey_id < 0:
            raise php_new_class("SodiumException", lambda : SodiumException("subkey_id cannot be negative"))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(context) != self.CRYPTO_KDF_CONTEXTBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("context should be SODIUM_CRYPTO_KDF_CONTEXTBYTES bytes"))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(key) != self.CRYPTO_KDF_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("key should be SODIUM_CRYPTO_KDF_KEYBYTES bytes"))
        # end if
        salt = ParagonIE_Sodium_Core_Util.store64_le(subkey_id)
        state = self.crypto_generichash_init_salt_personal(key, subkey_len, salt, context)
        return self.crypto_generichash_final(state, subkey_len)
    # end def crypto_kdf_derive_from_key
    #// 
    #// @return string
    #// @throws Exception
    #// @throws Error
    #//
    @classmethod
    def crypto_kdf_keygen(self):
        
        return random_bytes(self.CRYPTO_KDF_KEYBYTES)
    # end def crypto_kdf_keygen
    #// 
    #// Perform a key exchange, between a designated client and a server.
    #// 
    #// Typically, you would designate one machine to be the client and the
    #// other to be the server. The first two keys are what you'd expect for
    #// scalarmult() below, but the latter two public keys don't swap places.
    #// 
    #// | ALICE                          | BOB                                 |
    #// | Client                         | Server                              |
    #// |--------------------------------|-------------------------------------|
    #// | shared = crypto_kx(            | shared = crypto_kx(                 |
    #// |     alice_sk,                  |     bob_sk,                         | <- contextual
    #// |     bob_pk,                    |     alice_pk,                       | <- contextual
    #// |     alice_pk,                  |     alice_pk,                       | <----- static
    #// |     bob_pk                     |     bob_pk                          | <----- static
    #// | )                              | )                                   |
    #// 
    #// They are used along with the scalarmult product to generate a 256-bit
    #// BLAKE2b hash unique to the client and server keys.
    #// 
    #// @param string $my_secret
    #// @param string $their_public
    #// @param string $client_public
    #// @param string $server_public
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_kx(self, my_secret=None, their_public=None, client_public=None, server_public=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(my_secret, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(their_public, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(client_public, "string", 3)
        ParagonIE_Sodium_Core_Util.declarescalartype(server_public, "string", 4)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(my_secret) != self.CRYPTO_BOX_SECRETKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 1 must be CRYPTO_BOX_SECRETKEYBYTES long."))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(their_public) != self.CRYPTO_BOX_PUBLICKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_BOX_PUBLICKEYBYTES long."))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(client_public) != self.CRYPTO_BOX_PUBLICKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 3 must be CRYPTO_BOX_PUBLICKEYBYTES long."))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(server_public) != self.CRYPTO_BOX_PUBLICKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 4 must be CRYPTO_BOX_PUBLICKEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            if php_is_callable("sodium_crypto_kx"):
                return php_str(sodium_crypto_kx(my_secret, their_public, client_public, server_public))
            # end if
        # end if
        if self.use_fallback("crypto_kx"):
            return php_str(php_call_user_func("\\Sodium\\crypto_kx", my_secret, their_public, client_public, server_public))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.keyexchange(my_secret, their_public, client_public, server_public)
        # end if
        return ParagonIE_Sodium_Crypto.keyexchange(my_secret, their_public, client_public, server_public)
    # end def crypto_kx
    #// 
    #// @param string $seed
    #// @return string
    #// @throws SodiumException
    #//
    @classmethod
    def crypto_kx_seed_keypair(self, seed=None):
        
        ParagonIE_Sodium_Core_Util.declarescalartype(seed, "string", 1)
        seed = php_str(seed)
        if ParagonIE_Sodium_Core_Util.strlen(seed) != self.CRYPTO_KX_SEEDBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("seed must be SODIUM_CRYPTO_KX_SEEDBYTES bytes"))
        # end if
        sk = self.crypto_generichash(seed, "", self.CRYPTO_KX_SECRETKEYBYTES)
        pk = self.crypto_scalarmult_base(sk)
        return sk + pk
    # end def crypto_kx_seed_keypair
    #// 
    #// @return string
    #// @throws Exception
    #//
    @classmethod
    def crypto_kx_keypair(self):
        
        sk = self.randombytes_buf(self.CRYPTO_KX_SECRETKEYBYTES)
        pk = self.crypto_scalarmult_base(sk)
        return sk + pk
    # end def crypto_kx_keypair
    #// 
    #// @param string $keypair
    #// @param string $serverPublicKey
    #// @return array{0: string, 1: string}
    #// @throws SodiumException
    #//
    @classmethod
    def crypto_kx_client_session_keys(self, keypair=None, serverPublicKey=None):
        
        ParagonIE_Sodium_Core_Util.declarescalartype(keypair, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(serverPublicKey, "string", 2)
        keypair = php_str(keypair)
        serverPublicKey = php_str(serverPublicKey)
        if ParagonIE_Sodium_Core_Util.strlen(keypair) != self.CRYPTO_KX_KEYPAIRBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("keypair should be SODIUM_CRYPTO_KX_KEYPAIRBYTES bytes"))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(serverPublicKey) != self.CRYPTO_KX_PUBLICKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("public keys must be SODIUM_CRYPTO_KX_PUBLICKEYBYTES bytes"))
        # end if
        sk = self.crypto_kx_secretkey(keypair)
        pk = self.crypto_kx_publickey(keypair)
        h = self.crypto_generichash_init(None, self.CRYPTO_KX_SESSIONKEYBYTES * 2)
        self.crypto_generichash_update(h, self.crypto_scalarmult(sk, serverPublicKey))
        self.crypto_generichash_update(h, pk)
        self.crypto_generichash_update(h, serverPublicKey)
        sessionKeys = self.crypto_generichash_final(h, self.CRYPTO_KX_SESSIONKEYBYTES * 2)
        return Array(ParagonIE_Sodium_Core_Util.substr(sessionKeys, 0, self.CRYPTO_KX_SESSIONKEYBYTES), ParagonIE_Sodium_Core_Util.substr(sessionKeys, self.CRYPTO_KX_SESSIONKEYBYTES, self.CRYPTO_KX_SESSIONKEYBYTES))
    # end def crypto_kx_client_session_keys
    #// 
    #// @param string $keypair
    #// @param string $clientPublicKey
    #// @return array{0: string, 1: string}
    #// @throws SodiumException
    #//
    @classmethod
    def crypto_kx_server_session_keys(self, keypair=None, clientPublicKey=None):
        
        ParagonIE_Sodium_Core_Util.declarescalartype(keypair, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(clientPublicKey, "string", 2)
        keypair = php_str(keypair)
        clientPublicKey = php_str(clientPublicKey)
        if ParagonIE_Sodium_Core_Util.strlen(keypair) != self.CRYPTO_KX_KEYPAIRBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("keypair should be SODIUM_CRYPTO_KX_KEYPAIRBYTES bytes"))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(clientPublicKey) != self.CRYPTO_KX_PUBLICKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("public keys must be SODIUM_CRYPTO_KX_PUBLICKEYBYTES bytes"))
        # end if
        sk = self.crypto_kx_secretkey(keypair)
        pk = self.crypto_kx_publickey(keypair)
        h = self.crypto_generichash_init(None, self.CRYPTO_KX_SESSIONKEYBYTES * 2)
        self.crypto_generichash_update(h, self.crypto_scalarmult(sk, clientPublicKey))
        self.crypto_generichash_update(h, clientPublicKey)
        self.crypto_generichash_update(h, pk)
        sessionKeys = self.crypto_generichash_final(h, self.CRYPTO_KX_SESSIONKEYBYTES * 2)
        return Array(ParagonIE_Sodium_Core_Util.substr(sessionKeys, self.CRYPTO_KX_SESSIONKEYBYTES, self.CRYPTO_KX_SESSIONKEYBYTES), ParagonIE_Sodium_Core_Util.substr(sessionKeys, 0, self.CRYPTO_KX_SESSIONKEYBYTES))
    # end def crypto_kx_server_session_keys
    #// 
    #// @param string $kp
    #// @return string
    #// @throws SodiumException
    #//
    @classmethod
    def crypto_kx_secretkey(self, kp=None):
        
        return ParagonIE_Sodium_Core_Util.substr(kp, 0, self.CRYPTO_KX_SECRETKEYBYTES)
    # end def crypto_kx_secretkey
    #// 
    #// @param string $kp
    #// @return string
    #// @throws SodiumException
    #//
    @classmethod
    def crypto_kx_publickey(self, kp=None):
        
        return ParagonIE_Sodium_Core_Util.substr(kp, self.CRYPTO_KX_SECRETKEYBYTES, self.CRYPTO_KX_PUBLICKEYBYTES)
    # end def crypto_kx_publickey
    #// 
    #// @param int $outlen
    #// @param string $passwd
    #// @param string $salt
    #// @param int $opslimit
    #// @param int $memlimit
    #// @param int|null $alg
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_pwhash(self, outlen=None, passwd=None, salt=None, opslimit=None, memlimit=None, alg=None):
        
        ParagonIE_Sodium_Core_Util.declarescalartype(outlen, "int", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(passwd, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(salt, "string", 3)
        ParagonIE_Sodium_Core_Util.declarescalartype(opslimit, "int", 4)
        ParagonIE_Sodium_Core_Util.declarescalartype(memlimit, "int", 5)
        if self.usenewsodiumapi():
            if (not is_null(alg)):
                ParagonIE_Sodium_Core_Util.declarescalartype(alg, "int", 6)
                return sodium_crypto_pwhash(outlen, passwd, salt, opslimit, memlimit, alg)
            # end if
            return sodium_crypto_pwhash(outlen, passwd, salt, opslimit, memlimit)
        # end if
        if self.use_fallback("crypto_pwhash"):
            return php_str(php_call_user_func("\\Sodium\\crypto_pwhash", outlen, passwd, salt, opslimit, memlimit))
        # end if
        raise php_new_class("SodiumException", lambda : SodiumException("This is not implemented, as it is not possible to implement Argon2i with acceptable performance in pure-PHP"))
    # end def crypto_pwhash
    #// 
    #// !Exclusive to sodium_compat!
    #// 
    #// This returns TRUE if the native crypto_pwhash API is available by libsodium.
    #// This returns FALSE if only sodium_compat is available.
    #// 
    #// @return bool
    #//
    @classmethod
    def crypto_pwhash_is_available(self):
        
        if self.usenewsodiumapi():
            return True
        # end if
        if self.use_fallback("crypto_pwhash"):
            return True
        # end if
        return False
    # end def crypto_pwhash_is_available
    #// 
    #// @param string $passwd
    #// @param int $opslimit
    #// @param int $memlimit
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_pwhash_str(self, passwd=None, opslimit=None, memlimit=None):
        
        ParagonIE_Sodium_Core_Util.declarescalartype(passwd, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(opslimit, "int", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(memlimit, "int", 3)
        if self.usenewsodiumapi():
            return sodium_crypto_pwhash_str(passwd, opslimit, memlimit)
        # end if
        if self.use_fallback("crypto_pwhash_str"):
            return php_str(php_call_user_func("\\Sodium\\crypto_pwhash_str", passwd, opslimit, memlimit))
        # end if
        raise php_new_class("SodiumException", lambda : SodiumException("This is not implemented, as it is not possible to implement Argon2i with acceptable performance in pure-PHP"))
    # end def crypto_pwhash_str
    #// 
    #// Do we need to rehash this password?
    #// 
    #// @param string $hash
    #// @param int $opslimit
    #// @param int $memlimit
    #// @return bool
    #// @throws SodiumException
    #//
    @classmethod
    def crypto_pwhash_str_needs_rehash(self, hash=None, opslimit=None, memlimit=None):
        
        ParagonIE_Sodium_Core_Util.declarescalartype(hash, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(opslimit, "int", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(memlimit, "int", 3)
        #// Just grab the first 4 pieces.
        pieces = php_explode("$", php_str(hash))
        prefix = php_implode("$", php_array_slice(pieces, 0, 4))
        #// Rebuild the expected header.
        #// @var int $ops
        ops = php_int(opslimit)
        #// @var int $mem
        mem = php_int(memlimit) >> 10
        encoded = self.CRYPTO_PWHASH_STRPREFIX + "v=19$m=" + mem + ",t=" + ops + ",p=1"
        #// Do they match? If so, we don't need to rehash, so return false.
        return (not ParagonIE_Sodium_Core_Util.hashequals(encoded, prefix))
    # end def crypto_pwhash_str_needs_rehash
    #// 
    #// @param string $passwd
    #// @param string $hash
    #// @return bool
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_pwhash_str_verify(self, passwd=None, hash=None):
        
        ParagonIE_Sodium_Core_Util.declarescalartype(passwd, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(hash, "string", 2)
        if self.usenewsodiumapi():
            return php_bool(sodium_crypto_pwhash_str_verify(passwd, hash))
        # end if
        if self.use_fallback("crypto_pwhash_str_verify"):
            return php_bool(php_call_user_func("\\Sodium\\crypto_pwhash_str_verify", passwd, hash))
        # end if
        raise php_new_class("SodiumException", lambda : SodiumException("This is not implemented, as it is not possible to implement Argon2i with acceptable performance in pure-PHP"))
    # end def crypto_pwhash_str_verify
    #// 
    #// @param int $outlen
    #// @param string $passwd
    #// @param string $salt
    #// @param int $opslimit
    #// @param int $memlimit
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def crypto_pwhash_scryptsalsa208sha256(self, outlen=None, passwd=None, salt=None, opslimit=None, memlimit=None):
        
        ParagonIE_Sodium_Core_Util.declarescalartype(outlen, "int", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(passwd, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(salt, "string", 3)
        ParagonIE_Sodium_Core_Util.declarescalartype(opslimit, "int", 4)
        ParagonIE_Sodium_Core_Util.declarescalartype(memlimit, "int", 5)
        if self.usenewsodiumapi():
            return php_str(sodium_crypto_pwhash_scryptsalsa208sha256(php_int(outlen), php_str(passwd), php_str(salt), php_int(opslimit), php_int(memlimit)))
        # end if
        if self.use_fallback("crypto_pwhash_scryptsalsa208sha256"):
            return php_str(php_call_user_func("\\Sodium\\crypto_pwhash_scryptsalsa208sha256", php_int(outlen), php_str(passwd), php_str(salt), php_int(opslimit), php_int(memlimit)))
        # end if
        raise php_new_class("SodiumException", lambda : SodiumException("This is not implemented, as it is not possible to implement Scrypt with acceptable performance in pure-PHP"))
    # end def crypto_pwhash_scryptsalsa208sha256
    #// 
    #// !Exclusive to sodium_compat!
    #// 
    #// This returns TRUE if the native crypto_pwhash API is available by libsodium.
    #// This returns FALSE if only sodium_compat is available.
    #// 
    #// @return bool
    #//
    @classmethod
    def crypto_pwhash_scryptsalsa208sha256_is_available(self):
        
        if self.usenewsodiumapi():
            return True
        # end if
        if self.use_fallback("crypto_pwhash_scryptsalsa208sha256"):
            return True
        # end if
        return False
    # end def crypto_pwhash_scryptsalsa208sha256_is_available
    #// 
    #// @param string $passwd
    #// @param int $opslimit
    #// @param int $memlimit
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def crypto_pwhash_scryptsalsa208sha256_str(self, passwd=None, opslimit=None, memlimit=None):
        
        ParagonIE_Sodium_Core_Util.declarescalartype(passwd, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(opslimit, "int", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(memlimit, "int", 3)
        if self.usenewsodiumapi():
            return php_str(sodium_crypto_pwhash_scryptsalsa208sha256_str(php_str(passwd), php_int(opslimit), php_int(memlimit)))
        # end if
        if self.use_fallback("crypto_pwhash_scryptsalsa208sha256_str"):
            return php_str(php_call_user_func("\\Sodium\\crypto_pwhash_scryptsalsa208sha256_str", php_str(passwd), php_int(opslimit), php_int(memlimit)))
        # end if
        raise php_new_class("SodiumException", lambda : SodiumException("This is not implemented, as it is not possible to implement Scrypt with acceptable performance in pure-PHP"))
    # end def crypto_pwhash_scryptsalsa208sha256_str
    #// 
    #// @param string $passwd
    #// @param string $hash
    #// @return bool
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def crypto_pwhash_scryptsalsa208sha256_str_verify(self, passwd=None, hash=None):
        
        ParagonIE_Sodium_Core_Util.declarescalartype(passwd, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(hash, "string", 2)
        if self.usenewsodiumapi():
            return php_bool(sodium_crypto_pwhash_scryptsalsa208sha256_str_verify(php_str(passwd), php_str(hash)))
        # end if
        if self.use_fallback("crypto_pwhash_scryptsalsa208sha256_str_verify"):
            return php_bool(php_call_user_func("\\Sodium\\crypto_pwhash_scryptsalsa208sha256_str_verify", php_str(passwd), php_str(hash)))
        # end if
        raise php_new_class("SodiumException", lambda : SodiumException("This is not implemented, as it is not possible to implement Scrypt with acceptable performance in pure-PHP"))
    # end def crypto_pwhash_scryptsalsa208sha256_str_verify
    #// 
    #// Calculate the shared secret between your secret key and your
    #// recipient's public key.
    #// 
    #// Algorithm: X25519 (ECDH over Curve25519)
    #// 
    #// @param string $secretKey
    #// @param string $publicKey
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_scalarmult(self, secretKey=None, publicKey=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(secretKey, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(publicKey, "string", 2)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(secretKey) != self.CRYPTO_BOX_SECRETKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 1 must be CRYPTO_BOX_SECRETKEYBYTES long."))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(publicKey) != self.CRYPTO_BOX_PUBLICKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_BOX_PUBLICKEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return sodium_crypto_scalarmult(secretKey, publicKey)
        # end if
        if self.use_fallback("crypto_scalarmult"):
            return php_str(php_call_user_func("\\Sodium\\crypto_scalarmult", secretKey, publicKey))
        # end if
        #// Output validation: Forbid all-zero keys
        if ParagonIE_Sodium_Core_Util.hashequals(secretKey, php_str_repeat(" ", self.CRYPTO_BOX_SECRETKEYBYTES)):
            raise php_new_class("SodiumException", lambda : SodiumException("Zero secret key is not allowed"))
        # end if
        if ParagonIE_Sodium_Core_Util.hashequals(publicKey, php_str_repeat(" ", self.CRYPTO_BOX_PUBLICKEYBYTES)):
            raise php_new_class("SodiumException", lambda : SodiumException("Zero public key is not allowed"))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.scalarmult(secretKey, publicKey)
        # end if
        return ParagonIE_Sodium_Crypto.scalarmult(secretKey, publicKey)
    # end def crypto_scalarmult
    #// 
    #// Calculate an X25519 public key from an X25519 secret key.
    #// 
    #// @param string $secretKey
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress TooFewArguments
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_scalarmult_base(self, secretKey=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(secretKey, "string", 1)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(secretKey) != self.CRYPTO_BOX_SECRETKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 1 must be CRYPTO_BOX_SECRETKEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return sodium_crypto_scalarmult_base(secretKey)
        # end if
        if self.use_fallback("crypto_scalarmult_base"):
            return php_str(php_call_user_func("\\Sodium\\crypto_scalarmult_base", secretKey))
        # end if
        if ParagonIE_Sodium_Core_Util.hashequals(secretKey, php_str_repeat(" ", self.CRYPTO_BOX_SECRETKEYBYTES)):
            raise php_new_class("SodiumException", lambda : SodiumException("Zero secret key is not allowed"))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.scalarmult_base(secretKey)
        # end if
        return ParagonIE_Sodium_Crypto.scalarmult_base(secretKey)
    # end def crypto_scalarmult_base
    #// 
    #// Authenticated symmetric-key encryption.
    #// 
    #// Algorithm: XSalsa20-Poly1305
    #// 
    #// @param string $plaintext The message you're encrypting
    #// @param string $nonce A Number to be used Once; must be 24 bytes
    #// @param string $key Symmetric encryption key
    #// @return string           Ciphertext with Poly1305 MAC
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_secretbox(self, plaintext=None, nonce=None, key=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(plaintext, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(nonce, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(key, "string", 3)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(nonce) != self.CRYPTO_SECRETBOX_NONCEBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_SECRETBOX_NONCEBYTES long."))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(key) != self.CRYPTO_SECRETBOX_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 3 must be CRYPTO_SECRETBOX_KEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return sodium_crypto_secretbox(plaintext, nonce, key)
        # end if
        if self.use_fallback("crypto_secretbox"):
            return php_str(php_call_user_func("\\Sodium\\crypto_secretbox", plaintext, nonce, key))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.secretbox(plaintext, nonce, key)
        # end if
        return ParagonIE_Sodium_Crypto.secretbox(plaintext, nonce, key)
    # end def crypto_secretbox
    #// 
    #// Decrypts a message previously encrypted with crypto_secretbox().
    #// 
    #// @param string $ciphertext Ciphertext with Poly1305 MAC
    #// @param string $nonce      A Number to be used Once; must be 24 bytes
    #// @param string $key        Symmetric encryption key
    #// @return string            Original plaintext message
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #// @psalm-suppress MixedInferredReturnType
    #// @psalm-suppress MixedReturnStatement
    #//
    @classmethod
    def crypto_secretbox_open(self, ciphertext=None, nonce=None, key=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(ciphertext, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(nonce, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(key, "string", 3)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(nonce) != self.CRYPTO_SECRETBOX_NONCEBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_SECRETBOX_NONCEBYTES long."))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(key) != self.CRYPTO_SECRETBOX_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 3 must be CRYPTO_SECRETBOX_KEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            #// 
            #// @psalm-suppress InvalidReturnStatement
            #// @psalm-suppress FalsableReturnStatement
            #//
            return sodium_crypto_secretbox_open(ciphertext, nonce, key)
        # end if
        if self.use_fallback("crypto_secretbox_open"):
            return php_call_user_func("\\Sodium\\crypto_secretbox_open", ciphertext, nonce, key)
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.secretbox_open(ciphertext, nonce, key)
        # end if
        return ParagonIE_Sodium_Crypto.secretbox_open(ciphertext, nonce, key)
    # end def crypto_secretbox_open
    #// 
    #// Return a secure random key for use with crypto_secretbox
    #// 
    #// @return string
    #// @throws Exception
    #// @throws Error
    #//
    @classmethod
    def crypto_secretbox_keygen(self):
        
        return random_bytes(self.CRYPTO_SECRETBOX_KEYBYTES)
    # end def crypto_secretbox_keygen
    #// 
    #// Authenticated symmetric-key encryption.
    #// 
    #// Algorithm: XChaCha20-Poly1305
    #// 
    #// @param string $plaintext The message you're encrypting
    #// @param string $nonce     A Number to be used Once; must be 24 bytes
    #// @param string $key       Symmetric encryption key
    #// @return string           Ciphertext with Poly1305 MAC
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_secretbox_xchacha20poly1305(self, plaintext=None, nonce=None, key=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(plaintext, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(nonce, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(key, "string", 3)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(nonce) != self.CRYPTO_SECRETBOX_NONCEBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_SECRETBOX_NONCEBYTES long."))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(key) != self.CRYPTO_SECRETBOX_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 3 must be CRYPTO_SECRETBOX_KEYBYTES long."))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.secretbox_xchacha20poly1305(plaintext, nonce, key)
        # end if
        return ParagonIE_Sodium_Crypto.secretbox_xchacha20poly1305(plaintext, nonce, key)
    # end def crypto_secretbox_xchacha20poly1305
    #// 
    #// Decrypts a message previously encrypted with crypto_secretbox_xchacha20poly1305().
    #// 
    #// @param string $ciphertext Ciphertext with Poly1305 MAC
    #// @param string $nonce      A Number to be used Once; must be 24 bytes
    #// @param string $key        Symmetric encryption key
    #// @return string            Original plaintext message
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_secretbox_xchacha20poly1305_open(self, ciphertext=None, nonce=None, key=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(ciphertext, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(nonce, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(key, "string", 3)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(nonce) != self.CRYPTO_SECRETBOX_NONCEBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_SECRETBOX_NONCEBYTES long."))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(key) != self.CRYPTO_SECRETBOX_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 3 must be CRYPTO_SECRETBOX_KEYBYTES long."))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.secretbox_xchacha20poly1305_open(ciphertext, nonce, key)
        # end if
        return ParagonIE_Sodium_Crypto.secretbox_xchacha20poly1305_open(ciphertext, nonce, key)
    # end def crypto_secretbox_xchacha20poly1305_open
    #// 
    #// @param string $key
    #// @return array<int, string> Returns a state and a header.
    #// @throws Exception
    #// @throws SodiumException
    #//
    @classmethod
    def crypto_secretstream_xchacha20poly1305_init_push(self, key=None):
        
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.secretstream_xchacha20poly1305_init_push(key)
        # end if
        return ParagonIE_Sodium_Crypto.secretstream_xchacha20poly1305_init_push(key)
    # end def crypto_secretstream_xchacha20poly1305_init_push
    #// 
    #// @param string $header
    #// @param string $key
    #// @return string Returns a state.
    #// @throws Exception
    #//
    @classmethod
    def crypto_secretstream_xchacha20poly1305_init_pull(self, header=None, key=None):
        
        if ParagonIE_Sodium_Core_Util.strlen(header) < self.CRYPTO_SECRETSTREAM_XCHACHA20POLY1305_HEADERBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("header size should be SODIUM_CRYPTO_SECRETSTREAM_XCHACHA20POLY1305_HEADERBYTES bytes"))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.secretstream_xchacha20poly1305_init_pull(key, header)
        # end if
        return ParagonIE_Sodium_Crypto.secretstream_xchacha20poly1305_init_pull(key, header)
    # end def crypto_secretstream_xchacha20poly1305_init_pull
    #// 
    #// @param string $state
    #// @param string $msg
    #// @param string $aad
    #// @param int $tag
    #// @return string
    #// @throws SodiumException
    #//
    @classmethod
    def crypto_secretstream_xchacha20poly1305_push(self, state=None, msg=None, aad="", tag=0):
        
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.secretstream_xchacha20poly1305_push(state, msg, aad, tag)
        # end if
        return ParagonIE_Sodium_Crypto.secretstream_xchacha20poly1305_push(state, msg, aad, tag)
    # end def crypto_secretstream_xchacha20poly1305_push
    #// 
    #// @param string $state
    #// @param string $msg
    #// @param string $aad
    #// @return bool|array{0: string, 1: int}
    #// @throws SodiumException
    #//
    @classmethod
    def crypto_secretstream_xchacha20poly1305_pull(self, state=None, msg=None, aad=""):
        
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.secretstream_xchacha20poly1305_pull(state, msg, aad)
        # end if
        return ParagonIE_Sodium_Crypto.secretstream_xchacha20poly1305_pull(state, msg, aad)
    # end def crypto_secretstream_xchacha20poly1305_pull
    #// 
    #// @return string
    #// @throws Exception
    #//
    @classmethod
    def crypto_secretstream_xchacha20poly1305_keygen(self):
        
        return random_bytes(self.CRYPTO_SECRETSTREAM_XCHACHA20POLY1305_KEYBYTES)
    # end def crypto_secretstream_xchacha20poly1305_keygen
    #// 
    #// @param string $state
    #// @return void
    #// @throws SodiumException
    #//
    @classmethod
    def crypto_secretstream_xchacha20poly1305_rekey(self, state=None):
        
        if PHP_INT_SIZE == 4:
            ParagonIE_Sodium_Crypto32.secretstream_xchacha20poly1305_rekey(state)
        else:
            ParagonIE_Sodium_Crypto.secretstream_xchacha20poly1305_rekey(state)
        # end if
    # end def crypto_secretstream_xchacha20poly1305_rekey
    #// 
    #// Calculates a SipHash-2-4 hash of a message for a given key.
    #// 
    #// @param string $message Input message
    #// @param string $key SipHash-2-4 key
    #// @return string         Hash
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #// @psalm-suppress MixedInferredReturnType
    #// @psalm-suppress MixedReturnStatement
    #//
    @classmethod
    def crypto_shorthash(self, message=None, key=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(message, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(key, "string", 2)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(key) != self.CRYPTO_SHORTHASH_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_SHORTHASH_KEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return sodium_crypto_shorthash(message, key)
        # end if
        if self.use_fallback("crypto_shorthash"):
            return php_str(php_call_user_func("\\Sodium\\crypto_shorthash", message, key))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Core32_SipHash.siphash24(message, key)
        # end if
        return ParagonIE_Sodium_Core_SipHash.siphash24(message, key)
    # end def crypto_shorthash
    #// 
    #// Return a secure random key for use with crypto_shorthash
    #// 
    #// @return string
    #// @throws Exception
    #// @throws Error
    #//
    @classmethod
    def crypto_shorthash_keygen(self):
        
        return random_bytes(self.CRYPTO_SHORTHASH_KEYBYTES)
    # end def crypto_shorthash_keygen
    #// 
    #// Returns a signed message. You probably want crypto_sign_detached()
    #// instead, which only returns the signature.
    #// 
    #// Algorithm: Ed25519 (EdDSA over Curve25519)
    #// 
    #// @param string $message Message to be signed.
    #// @param string $secretKey Secret signing key.
    #// @return string           Signed message (signature is prefixed).
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #// @psalm-suppress MixedInferredReturnType
    #// @psalm-suppress MixedReturnStatement
    #//
    @classmethod
    def crypto_sign(self, message=None, secretKey=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(message, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(secretKey, "string", 2)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(secretKey) != self.CRYPTO_SIGN_SECRETKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_SIGN_SECRETKEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return sodium_crypto_sign(message, secretKey)
        # end if
        if self.use_fallback("crypto_sign"):
            return php_str(php_call_user_func("\\Sodium\\crypto_sign", message, secretKey))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.sign(message, secretKey)
        # end if
        return ParagonIE_Sodium_Crypto.sign(message, secretKey)
    # end def crypto_sign
    #// 
    #// Validates a signed message then returns the message.
    #// 
    #// @param string $signedMessage A signed message
    #// @param string $publicKey A public key
    #// @return string               The original message (if the signature is
    #// valid for this public key)
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #// @psalm-suppress MixedInferredReturnType
    #// @psalm-suppress MixedReturnStatement
    #//
    @classmethod
    def crypto_sign_open(self, signedMessage=None, publicKey=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(signedMessage, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(publicKey, "string", 2)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(signedMessage) < self.CRYPTO_SIGN_BYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 1 must be at least CRYPTO_SIGN_BYTES long."))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(publicKey) != self.CRYPTO_SIGN_PUBLICKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_SIGN_PUBLICKEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            #// 
            #// @psalm-suppress InvalidReturnStatement
            #// @psalm-suppress FalsableReturnStatement
            #//
            return sodium_crypto_sign_open(signedMessage, publicKey)
        # end if
        if self.use_fallback("crypto_sign_open"):
            return php_call_user_func("\\Sodium\\crypto_sign_open", signedMessage, publicKey)
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.sign_open(signedMessage, publicKey)
        # end if
        return ParagonIE_Sodium_Crypto.sign_open(signedMessage, publicKey)
    # end def crypto_sign_open
    #// 
    #// Generate a new random Ed25519 keypair.
    #// 
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def crypto_sign_keypair(self):
        
        if self.usenewsodiumapi():
            return sodium_crypto_sign_keypair()
        # end if
        if self.use_fallback("crypto_sign_keypair"):
            return php_str(php_call_user_func("\\Sodium\\crypto_sign_keypair"))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Core32_Ed25519.keypair()
        # end if
        return ParagonIE_Sodium_Core_Ed25519.keypair()
    # end def crypto_sign_keypair
    #// 
    #// @param string $sk
    #// @param string $pk
    #// @return string
    #// @throws SodiumException
    #//
    @classmethod
    def crypto_sign_keypair_from_secretkey_and_publickey(self, sk=None, pk=None):
        
        ParagonIE_Sodium_Core_Util.declarescalartype(sk, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(pk, "string", 1)
        sk = php_str(sk)
        pk = php_str(pk)
        if ParagonIE_Sodium_Core_Util.strlen(sk) != self.CRYPTO_SIGN_SECRETKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("secretkey should be SODIUM_CRYPTO_SIGN_SECRETKEYBYTES bytes"))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(pk) != self.CRYPTO_SIGN_PUBLICKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("publickey should be SODIUM_CRYPTO_SIGN_PUBLICKEYBYTES bytes"))
        # end if
        if self.usenewsodiumapi():
            return sodium_crypto_sign_keypair_from_secretkey_and_publickey(sk, pk)
        # end if
        return sk + pk
    # end def crypto_sign_keypair_from_secretkey_and_publickey
    #// 
    #// Generate an Ed25519 keypair from a seed.
    #// 
    #// @param string $seed Input seed
    #// @return string      Keypair
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_sign_seed_keypair(self, seed=None):
        
        ParagonIE_Sodium_Core_Util.declarescalartype(seed, "string", 1)
        if self.usenewsodiumapi():
            return sodium_crypto_sign_seed_keypair(seed)
        # end if
        if self.use_fallback("crypto_sign_keypair"):
            return php_str(php_call_user_func("\\Sodium\\crypto_sign_seed_keypair", seed))
        # end if
        publicKey = ""
        secretKey = ""
        if PHP_INT_SIZE == 4:
            ParagonIE_Sodium_Core32_Ed25519.seed_keypair(publicKey, secretKey, seed)
        else:
            ParagonIE_Sodium_Core_Ed25519.seed_keypair(publicKey, secretKey, seed)
        # end if
        return secretKey + publicKey
    # end def crypto_sign_seed_keypair
    #// 
    #// Extract an Ed25519 public key from an Ed25519 keypair.
    #// 
    #// @param string $keypair Keypair
    #// @return string         Public key
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_sign_publickey(self, keypair=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(keypair, "string", 1)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(keypair) != self.CRYPTO_SIGN_KEYPAIRBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 1 must be CRYPTO_SIGN_KEYPAIRBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return sodium_crypto_sign_publickey(keypair)
        # end if
        if self.use_fallback("crypto_sign_publickey"):
            return php_str(php_call_user_func("\\Sodium\\crypto_sign_publickey", keypair))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Core32_Ed25519.publickey(keypair)
        # end if
        return ParagonIE_Sodium_Core_Ed25519.publickey(keypair)
    # end def crypto_sign_publickey
    #// 
    #// Calculate an Ed25519 public key from an Ed25519 secret key.
    #// 
    #// @param string $secretKey Your Ed25519 secret key
    #// @return string           The corresponding Ed25519 public key
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_sign_publickey_from_secretkey(self, secretKey=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(secretKey, "string", 1)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(secretKey) != self.CRYPTO_SIGN_SECRETKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 1 must be CRYPTO_SIGN_SECRETKEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return sodium_crypto_sign_publickey_from_secretkey(secretKey)
        # end if
        if self.use_fallback("crypto_sign_publickey_from_secretkey"):
            return php_str(php_call_user_func("\\Sodium\\crypto_sign_publickey_from_secretkey", secretKey))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Core32_Ed25519.publickey_from_secretkey(secretKey)
        # end if
        return ParagonIE_Sodium_Core_Ed25519.publickey_from_secretkey(secretKey)
    # end def crypto_sign_publickey_from_secretkey
    #// 
    #// Extract an Ed25519 secret key from an Ed25519 keypair.
    #// 
    #// @param string $keypair Keypair
    #// @return string         Secret key
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_sign_secretkey(self, keypair=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(keypair, "string", 1)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(keypair) != self.CRYPTO_SIGN_KEYPAIRBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 1 must be CRYPTO_SIGN_KEYPAIRBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return sodium_crypto_sign_secretkey(keypair)
        # end if
        if self.use_fallback("crypto_sign_secretkey"):
            return php_str(php_call_user_func("\\Sodium\\crypto_sign_secretkey", keypair))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Core32_Ed25519.secretkey(keypair)
        # end if
        return ParagonIE_Sodium_Core_Ed25519.secretkey(keypair)
    # end def crypto_sign_secretkey
    #// 
    #// Calculate the Ed25519 signature of a message and return ONLY the signature.
    #// 
    #// Algorithm: Ed25519 (EdDSA over Curve25519)
    #// 
    #// @param string $message Message to be signed
    #// @param string $secretKey Secret signing key
    #// @return string           Digital signature
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_sign_detached(self, message=None, secretKey=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(message, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(secretKey, "string", 2)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(secretKey) != self.CRYPTO_SIGN_SECRETKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_SIGN_SECRETKEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return sodium_crypto_sign_detached(message, secretKey)
        # end if
        if self.use_fallback("crypto_sign_detached"):
            return php_str(php_call_user_func("\\Sodium\\crypto_sign_detached", message, secretKey))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.sign_detached(message, secretKey)
        # end if
        return ParagonIE_Sodium_Crypto.sign_detached(message, secretKey)
    # end def crypto_sign_detached
    #// 
    #// Verify the Ed25519 signature of a message.
    #// 
    #// @param string $signature Digital sginature
    #// @param string $message Message to be verified
    #// @param string $publicKey Public key
    #// @return bool             TRUE if this signature is good for this public key;
    #// FALSE otherwise
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_sign_verify_detached(self, signature=None, message=None, publicKey=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(signature, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(message, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(publicKey, "string", 3)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(signature) != self.CRYPTO_SIGN_BYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 1 must be CRYPTO_SIGN_BYTES long."))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(publicKey) != self.CRYPTO_SIGN_PUBLICKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 3 must be CRYPTO_SIGN_PUBLICKEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return sodium_crypto_sign_verify_detached(signature, message, publicKey)
        # end if
        if self.use_fallback("crypto_sign_verify_detached"):
            return php_bool(php_call_user_func("\\Sodium\\crypto_sign_verify_detached", signature, message, publicKey))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.sign_verify_detached(signature, message, publicKey)
        # end if
        return ParagonIE_Sodium_Crypto.sign_verify_detached(signature, message, publicKey)
    # end def crypto_sign_verify_detached
    #// 
    #// Convert an Ed25519 public key to a Curve25519 public key
    #// 
    #// @param string $pk
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_sign_ed25519_pk_to_curve25519(self, pk=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(pk, "string", 1)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(pk) < self.CRYPTO_SIGN_PUBLICKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 1 must be at least CRYPTO_SIGN_PUBLICKEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            if php_is_callable("crypto_sign_ed25519_pk_to_curve25519"):
                return php_str(sodium_crypto_sign_ed25519_pk_to_curve25519(pk))
            # end if
        # end if
        if self.use_fallback("crypto_sign_ed25519_pk_to_curve25519"):
            return php_str(php_call_user_func("\\Sodium\\crypto_sign_ed25519_pk_to_curve25519", pk))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Core32_Ed25519.pk_to_curve25519(pk)
        # end if
        return ParagonIE_Sodium_Core_Ed25519.pk_to_curve25519(pk)
    # end def crypto_sign_ed25519_pk_to_curve25519
    #// 
    #// Convert an Ed25519 secret key to a Curve25519 secret key
    #// 
    #// @param string $sk
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_sign_ed25519_sk_to_curve25519(self, sk=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(sk, "string", 1)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(sk) < self.CRYPTO_SIGN_SEEDBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 1 must be at least CRYPTO_SIGN_SEEDBYTES long."))
        # end if
        if self.usenewsodiumapi():
            if php_is_callable("crypto_sign_ed25519_sk_to_curve25519"):
                return sodium_crypto_sign_ed25519_sk_to_curve25519(sk)
            # end if
        # end if
        if self.use_fallback("crypto_sign_ed25519_sk_to_curve25519"):
            return php_str(php_call_user_func("\\Sodium\\crypto_sign_ed25519_sk_to_curve25519", sk))
        # end if
        h = hash("sha512", ParagonIE_Sodium_Core_Util.substr(sk, 0, 32), True)
        h[0] = ParagonIE_Sodium_Core_Util.inttochr(ParagonIE_Sodium_Core_Util.chrtoint(h[0]) & 248)
        h[31] = ParagonIE_Sodium_Core_Util.inttochr(ParagonIE_Sodium_Core_Util.chrtoint(h[31]) & 127 | 64)
        return ParagonIE_Sodium_Core_Util.substr(h, 0, 32)
    # end def crypto_sign_ed25519_sk_to_curve25519
    #// 
    #// Expand a key and nonce into a keystream of pseudorandom bytes.
    #// 
    #// @param int $len Number of bytes desired
    #// @param string $nonce Number to be used Once; must be 24 bytes
    #// @param string $key XSalsa20 key
    #// @return string       Pseudorandom stream that can be XORed with messages
    #// to provide encryption (but not authentication; see
    #// Poly1305 or crypto_auth() for that, which is not
    #// optional for security)
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_stream(self, len=None, nonce=None, key=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(len, "int", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(nonce, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(key, "string", 3)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(nonce) != self.CRYPTO_STREAM_NONCEBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_SECRETBOX_NONCEBYTES long."))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(key) != self.CRYPTO_STREAM_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 3 must be CRYPTO_STREAM_KEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return sodium_crypto_stream(len, nonce, key)
        # end if
        if self.use_fallback("crypto_stream"):
            return php_str(php_call_user_func("\\Sodium\\crypto_stream", len, nonce, key))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Core32_XSalsa20.xsalsa20(len, nonce, key)
        # end if
        return ParagonIE_Sodium_Core_XSalsa20.xsalsa20(len, nonce, key)
    # end def crypto_stream
    #// 
    #// DANGER! UNAUTHENTICATED ENCRYPTION!
    #// 
    #// Unless you are following expert advice, do not used this feature.
    #// 
    #// Algorithm: XSalsa20
    #// 
    #// This DOES NOT provide ciphertext integrity.
    #// 
    #// @param string $message Plaintext message
    #// @param string $nonce Number to be used Once; must be 24 bytes
    #// @param string $key Encryption key
    #// @return string         Encrypted text which is vulnerable to chosen-
    #// ciphertext attacks unless you implement some
    #// other mitigation to the ciphertext (i.e.
    #// Encrypt then MAC)
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def crypto_stream_xor(self, message=None, nonce=None, key=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(message, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(nonce, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(key, "string", 3)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(nonce) != self.CRYPTO_STREAM_NONCEBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_SECRETBOX_NONCEBYTES long."))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(key) != self.CRYPTO_STREAM_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 3 must be CRYPTO_SECRETBOX_KEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return sodium_crypto_stream_xor(message, nonce, key)
        # end if
        if self.use_fallback("crypto_stream_xor"):
            return php_str(php_call_user_func("\\Sodium\\crypto_stream_xor", message, nonce, key))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Core32_XSalsa20.xsalsa20_xor(message, nonce, key)
        # end if
        return ParagonIE_Sodium_Core_XSalsa20.xsalsa20_xor(message, nonce, key)
    # end def crypto_stream_xor
    #// 
    #// Return a secure random key for use with crypto_stream
    #// 
    #// @return string
    #// @throws Exception
    #// @throws Error
    #//
    @classmethod
    def crypto_stream_keygen(self):
        
        return random_bytes(self.CRYPTO_STREAM_KEYBYTES)
    # end def crypto_stream_keygen
    #// 
    #// Cache-timing-safe implementation of hex2bin().
    #// 
    #// @param string $string Hexadecimal string
    #// @return string        Raw binary string
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress TooFewArguments
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def hex2bin(self, string=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(string, "string", 1)
        if self.usenewsodiumapi():
            if php_is_callable("sodium_hex2bin"):
                return php_str(sodium_hex2bin(string))
            # end if
        # end if
        if self.use_fallback("hex2bin"):
            return php_str(php_call_user_func("\\Sodium\\hex2bin", string))
        # end if
        return ParagonIE_Sodium_Core_Util.hex2bin(string)
    # end def hex2bin
    #// 
    #// Increase a string (little endian)
    #// 
    #// @param string $var
    #// 
    #// @return void
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def increment(self, var=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(var, "string", 1)
        if self.usenewsodiumapi():
            sodium_increment(var)
            return
        # end if
        if self.use_fallback("increment"):
            func = "\\Sodium\\increment"
            func(var)
            return
        # end if
        len = ParagonIE_Sodium_Core_Util.strlen(var)
        c = 1
        copy = ""
        i = 0
        while i < len:
            
            c += ParagonIE_Sodium_Core_Util.chrtoint(ParagonIE_Sodium_Core_Util.substr(var, i, 1))
            copy += ParagonIE_Sodium_Core_Util.inttochr(c)
            c >>= 8
            i += 1
        # end while
        var = copy
    # end def increment
    #// 
    #// The equivalent to the libsodium minor version we aim to be compatible
    #// with (sans pwhash and memzero).
    #// 
    #// @return int
    #// @psalm-suppress MixedInferredReturnType
    #// @psalm-suppress UndefinedFunction
    #//
    @classmethod
    def library_version_major(self):
        
        if self.usenewsodiumapi():
            return sodium_library_version_major()
        # end if
        if self.use_fallback("library_version_major"):
            return php_int(php_call_user_func("\\Sodium\\library_version_major"))
        # end if
        return self.LIBRARY_VERSION_MAJOR
    # end def library_version_major
    #// 
    #// The equivalent to the libsodium minor version we aim to be compatible
    #// with (sans pwhash and memzero).
    #// 
    #// @return int
    #// @psalm-suppress MixedInferredReturnType
    #// @psalm-suppress UndefinedFunction
    #//
    @classmethod
    def library_version_minor(self):
        
        if self.usenewsodiumapi():
            return sodium_library_version_minor()
        # end if
        if self.use_fallback("library_version_minor"):
            return php_int(php_call_user_func("\\Sodium\\library_version_minor"))
        # end if
        return self.LIBRARY_VERSION_MINOR
    # end def library_version_minor
    #// 
    #// Compare two strings.
    #// 
    #// @param string $left
    #// @param string $right
    #// @return int
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def memcmp(self, left=None, right=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(left, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(right, "string", 2)
        if self.usenewsodiumapi():
            return sodium_memcmp(left, right)
        # end if
        if self.use_fallback("memcmp"):
            return php_int(php_call_user_func("\\Sodium\\memcmp", left, right))
        # end if
        #// @var string $left
        #// @var string $right
        return ParagonIE_Sodium_Core_Util.memcmp(left, right)
    # end def memcmp
    #// 
    #// It's actually not possible to zero memory buffers in PHP. You need the
    #// native library for that.
    #// 
    #// @param string|null $var
    #// @param-out string|null $var
    #// 
    #// @return void
    #// @throws SodiumException (Unless libsodium is installed)
    #// @throws TypeError
    #// @psalm-suppress TooFewArguments
    #//
    @classmethod
    def memzero(self, var=None):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(var, "string", 1)
        if self.usenewsodiumapi():
            #// @psalm-suppress MixedArgument
            sodium_memzero(var)
            return
        # end if
        if self.use_fallback("memzero"):
            func = "\\Sodium\\memzero"
            func(var)
            if var == None:
                return
            # end if
        # end if
        raise php_new_class("SodiumException", lambda : SodiumException("This is not implemented in sodium_compat, as it is not possible to securely wipe memory from PHP. " + "To fix this error, make sure libsodium is installed and the PHP extension is enabled."))
    # end def memzero
    #// 
    #// @param string $unpadded
    #// @param int $blockSize
    #// @param bool $dontFallback
    #// @return string
    #// @throws SodiumException
    #//
    @classmethod
    def pad(self, unpadded=None, blockSize=None, dontFallback=False):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(unpadded, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(blockSize, "int", 2)
        unpadded = php_str(unpadded)
        blockSize = php_int(blockSize)
        if self.usenewsodiumapi() and (not dontFallback):
            return php_str(sodium_pad(unpadded, blockSize))
        # end if
        if blockSize <= 0:
            raise php_new_class("SodiumException", lambda : SodiumException("block size cannot be less than 1"))
        # end if
        unpadded_len = ParagonIE_Sodium_Core_Util.strlen(unpadded)
        xpadlen = blockSize - 1
        if blockSize & blockSize - 1 == 0:
            xpadlen -= unpadded_len & blockSize - 1
        else:
            xpadlen -= unpadded_len % blockSize
        # end if
        xpadded_len = unpadded_len + xpadlen
        padded = php_str_repeat(" ", xpadded_len - 1)
        if unpadded_len > 0:
            st = 1
            i = 0
            k = unpadded_len
            j = 0
            while j <= xpadded_len:
                
                i = php_int(i)
                k = php_int(k)
                st = php_int(st)
                if j >= unpadded_len:
                    padded[j] = " "
                else:
                    padded[j] = unpadded[j]
                # end if
                #// @var int $k
                k -= st
                st = php_int((1 << (k >> 48 | k >> 32 | k >> 16 | k - 1 >> 16).bit_length()) - 1 - k >> 48 | k >> 32 | k >> 16 | k - 1 >> 16) & 1
                i += st
                j += 1
            # end while
        # end if
        mask = 0
        tail = xpadded_len
        i = 0
        while i < blockSize:
            
            #// # barrier_mask = (unsigned char)
            #// #     (((i ^ xpadlen) - 1U) >> ((sizeof(size_t) - 1U) * CHAR_BIT));
            barrier_mask = i ^ xpadlen - 1 >> PHP_INT_SIZE << 3 - 1
            #// # tail[-i] = (tail[-i] & mask) | (0x80 & barrier_mask);
            padded[tail - i] = ParagonIE_Sodium_Core_Util.inttochr(ParagonIE_Sodium_Core_Util.chrtoint(padded[tail - i]) & mask | 128 & barrier_mask)
            #// # mask |= barrier_mask;
            mask |= barrier_mask
            i += 1
        # end while
        return padded
    # end def pad
    #// 
    #// @param string $padded
    #// @param int $blockSize
    #// @param bool $dontFallback
    #// @return string
    #// @throws SodiumException
    #//
    @classmethod
    def unpad(self, padded=None, blockSize=None, dontFallback=False):
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(padded, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(blockSize, "int", 2)
        padded = php_str(padded)
        blockSize = php_int(blockSize)
        if self.usenewsodiumapi() and (not dontFallback):
            return php_str(sodium_unpad(padded, blockSize))
        # end if
        if blockSize <= 0:
            raise php_new_class("SodiumException", lambda : SodiumException("block size cannot be less than 1"))
        # end if
        padded_len = ParagonIE_Sodium_Core_Util.strlen(padded)
        if padded_len < blockSize:
            raise php_new_class("SodiumException", lambda : SodiumException("invalid padding"))
        # end if
        #// # tail = &padded[padded_len - 1U];
        tail = padded_len - 1
        acc = 0
        valid = 0
        pad_len = 0
        found = 0
        i = 0
        while i < blockSize:
            
            #// # c = tail[-i];
            c = ParagonIE_Sodium_Core_Util.chrtoint(padded[tail - i])
            #// # is_barrier =
            #// #     (( (acc - 1U) & (pad_len - 1U) & ((c ^ 0x80) - 1U) ) >> 8) & 1U;
            is_barrier = acc - 1 & pad_len - 1 & c ^ 80 - 1 >> 7 & 1
            is_barrier &= (1 << (found).bit_length()) - 1 - found
            found |= is_barrier
            #// # acc |= c;
            acc |= c
            #// # pad_len |= i & (1U + ~is_barrier);
            pad_len |= i & 1 + (1 << (is_barrier).bit_length()) - 1 - is_barrier
            #// # valid |= (unsigned char) is_barrier;
            valid |= is_barrier & 255
            i += 1
        # end while
        #// # unpadded_len = padded_len - 1U - pad_len;
        unpadded_len = padded_len - 1 - pad_len
        if valid != 1:
            raise php_new_class("SodiumException", lambda : SodiumException("invalid padding"))
        # end if
        return ParagonIE_Sodium_Core_Util.substr(padded, 0, unpadded_len)
    # end def unpad
    #// 
    #// Will sodium_compat run fast on the current hardware and PHP configuration?
    #// 
    #// @return bool
    #//
    @classmethod
    def polyfill_is_fast(self):
        
        if php_extension_loaded("sodium"):
            return True
        # end if
        if php_extension_loaded("libsodium"):
            return True
        # end if
        return PHP_INT_SIZE == 8
    # end def polyfill_is_fast
    #// 
    #// Generate a string of bytes from the kernel's CSPRNG.
    #// Proudly uses /dev/urandom (if getrandom(2) is not available).
    #// 
    #// @param int $numBytes
    #// @return string
    #// @throws Exception
    #// @throws TypeError
    #//
    @classmethod
    def randombytes_buf(self, numBytes=None):
        
        #// Type checks:
        if (not php_is_int(numBytes)):
            if php_is_numeric(numBytes):
                numBytes = php_int(numBytes)
            else:
                raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be an integer, " + gettype(numBytes) + " given."))
            # end if
        # end if
        if self.use_fallback("randombytes_buf"):
            return php_str(php_call_user_func("\\Sodium\\randombytes_buf", numBytes))
        # end if
        return random_bytes(numBytes)
    # end def randombytes_buf
    #// 
    #// Generate an integer between 0 and $range (non-inclusive).
    #// 
    #// @param int $range
    #// @return int
    #// @throws Exception
    #// @throws Error
    #// @throws TypeError
    #//
    @classmethod
    def randombytes_uniform(self, range=None):
        
        #// Type checks:
        if (not php_is_int(range)):
            if php_is_numeric(range):
                range = php_int(range)
            else:
                raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be an integer, " + gettype(range) + " given."))
            # end if
        # end if
        if self.use_fallback("randombytes_uniform"):
            return php_int(php_call_user_func("\\Sodium\\randombytes_uniform", range))
        # end if
        return random_int(0, range - 1)
    # end def randombytes_uniform
    #// 
    #// Generate a random 16-bit integer.
    #// 
    #// @return int
    #// @throws Exception
    #// @throws Error
    #// @throws TypeError
    #//
    @classmethod
    def randombytes_random16(self):
        
        if self.use_fallback("randombytes_random16"):
            return php_int(php_call_user_func("\\Sodium\\randombytes_random16"))
        # end if
        return random_int(0, 65535)
    # end def randombytes_random16
    #// 
    #// Runtime testing method for 32-bit platforms.
    #// 
    #// Usage: If runtime_speed_test() returns FALSE, then our 32-bit
    #// implementation is to slow to use safely without risking timeouts.
    #// If this happens, install sodium from PECL to get acceptable
    #// performance.
    #// 
    #// @param int $iterations Number of multiplications to attempt
    #// @param int $maxTimeout Milliseconds
    #// @return bool           TRUE if we're fast enough, FALSE is not
    #// @throws SodiumException
    #//
    @classmethod
    def runtime_speed_test(self, iterations=None, maxTimeout=None):
        
        if self.polyfill_is_fast():
            return True
        # end if
        #// @var float $end
        end_ = 0
        #// @var float $start
        start = php_microtime(True)
        #// @var ParagonIE_Sodium_Core32_Int64 $a
        a = ParagonIE_Sodium_Core32_Int64.fromint(random_int(3, 1 << 16))
        i = 0
        while i < iterations:
            
            #// @var ParagonIE_Sodium_Core32_Int64 $b
            b = ParagonIE_Sodium_Core32_Int64.fromint(random_int(3, 1 << 16))
            a.mulint64(b)
            i += 1
        # end while
        #// @var float $end
        end_ = php_microtime(True)
        #// @var int $diff
        diff = php_int(ceil(end_ - start * 1000))
        return diff < maxTimeout
    # end def runtime_speed_test
    #// 
    #// This emulates libsodium's version_string() function, except ours is
    #// prefixed with 'polyfill-'.
    #// 
    #// @return string
    #// @psalm-suppress MixedInferredReturnType
    #// @psalm-suppress UndefinedFunction
    #//
    @classmethod
    def version_string(self):
        
        if self.usenewsodiumapi():
            return php_str(sodium_version_string())
        # end if
        if self.use_fallback("version_string"):
            return php_str(php_call_user_func("\\Sodium\\version_string"))
        # end if
        return php_str(self.VERSION_STRING)
    # end def version_string
    #// 
    #// Should we use the libsodium core function instead?
    #// This is always a good idea, if it's available. (Unless we're in the
    #// middle of running our unit test suite.)
    #// 
    #// If ext/libsodium is available, use it. Return TRUE.
    #// Otherwise, we have to use the code provided herein. Return FALSE.
    #// 
    #// @param string $sodium_func_name
    #// 
    #// @return bool
    #//
    def use_fallback(self, sodium_func_name=""):
        
        use_fallback.res = None
        if use_fallback.res == None:
            use_fallback.res = php_extension_loaded("libsodium") and PHP_VERSION_ID >= 50300
        # end if
        if use_fallback.res == False:
            #// No libsodium installed
            return False
        # end if
        if self.disableFallbackForUnitTests:
            #// Don't fallback. Use the PHP implementation.
            return False
        # end if
        if (not php_empty(lambda : sodium_func_name)):
            return php_is_callable("\\Sodium\\" + sodium_func_name)
        # end if
        return True
    # end def use_fallback
    #// 
    #// Libsodium as implemented in PHP 7.2
    #// and/or ext/sodium (via PECL)
    #// 
    #// @ref https://wiki.php.net/rfc/libsodium
    #// @return bool
    #//
    def usenewsodiumapi(self):
        
        usenewsodiumapi.res = None
        if usenewsodiumapi.res == None:
            usenewsodiumapi.res = PHP_VERSION_ID >= 70000 and php_extension_loaded("sodium")
        # end if
        if self.disableFallbackForUnitTests:
            #// Don't fallback. Use the PHP implementation.
            return False
        # end if
        return php_bool(usenewsodiumapi.res)
    # end def usenewsodiumapi
# end class ParagonIE_Sodium_Compat
