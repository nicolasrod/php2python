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
    #// 
    #// This parameter prevents the use of the PECL extension.
    #// It should only be used for unit testing.
    #// 
    #// @var bool
    #//
    disableFallbackForUnitTests = False
    #// 
    #// Use fast multiplication rather than our constant-time multiplication
    #// implementation. Can be enabled at runtime. Only enable this if you
    #// are absolutely certain that there is no timing leak on your platform.
    #// 
    #// @var bool
    #//
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
    def add(self, val_=None, addv_=None):
        
        
        val_len_ = ParagonIE_Sodium_Core_Util.strlen(val_)
        addv_len_ = ParagonIE_Sodium_Core_Util.strlen(addv_)
        if val_len_ != addv_len_:
            raise php_new_class("SodiumException", lambda : SodiumException("values must have the same length"))
        # end if
        A_ = ParagonIE_Sodium_Core_Util.stringtointarray(val_)
        B_ = ParagonIE_Sodium_Core_Util.stringtointarray(addv_)
        c_ = 0
        i_ = 0
        while i_ < val_len_:
            
            c_ += A_[i_] + B_[i_]
            A_[i_] = c_ & 255
            c_ >>= 8
            i_ += 1
        # end while
        val_ = ParagonIE_Sodium_Core_Util.intarraytostring(A_)
    # end def add
    #// 
    #// @param string $encoded
    #// @param int $variant
    #// @param string $ignore
    #// @return string
    #// @throws SodiumException
    #//
    @classmethod
    def base642bin(self, encoded_=None, variant_=None, ignore_=""):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(encoded_, "string", 1)
        #// @var string $encoded
        encoded_ = php_str(encoded_)
        if ParagonIE_Sodium_Core_Util.strlen(encoded_) == 0:
            return ""
        # end if
        #// Just strip before decoding
        if (not php_empty(lambda : ignore_)):
            encoded_ = php_str_replace(ignore_, "", encoded_)
        # end if
        try: 
            for case in Switch(variant_):
                if case(self.BASE64_VARIANT_ORIGINAL):
                    return ParagonIE_Sodium_Core_Base64_Original.decode(encoded_, True)
                # end if
                if case(self.BASE64_VARIANT_ORIGINAL_NO_PADDING):
                    return ParagonIE_Sodium_Core_Base64_Original.decode(encoded_, False)
                # end if
                if case(self.BASE64_VARIANT_URLSAFE):
                    return ParagonIE_Sodium_Core_Base64_UrlSafe.decode(encoded_, True)
                # end if
                if case(self.BASE64_VARIANT_URLSAFE_NO_PADDING):
                    return ParagonIE_Sodium_Core_Base64_UrlSafe.decode(encoded_, False)
                # end if
                if case():
                    raise php_new_class("SodiumException", lambda : SodiumException("invalid base64 variant identifier"))
                # end if
            # end for
        except Exception as ex_:
            if type(ex_).__name__ == "SodiumException":
                raise ex_
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
    def bin2base64(self, decoded_=None, variant_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(decoded_, "string", 1)
        #// @var string $decoded
        decoded_ = php_str(decoded_)
        if ParagonIE_Sodium_Core_Util.strlen(decoded_) == 0:
            return ""
        # end if
        for case in Switch(variant_):
            if case(self.BASE64_VARIANT_ORIGINAL):
                return ParagonIE_Sodium_Core_Base64_Original.encode(decoded_)
            # end if
            if case(self.BASE64_VARIANT_ORIGINAL_NO_PADDING):
                return ParagonIE_Sodium_Core_Base64_Original.encodeunpadded(decoded_)
            # end if
            if case(self.BASE64_VARIANT_URLSAFE):
                return ParagonIE_Sodium_Core_Base64_UrlSafe.encode(decoded_)
            # end if
            if case(self.BASE64_VARIANT_URLSAFE_NO_PADDING):
                return ParagonIE_Sodium_Core_Base64_UrlSafe.encodeunpadded(decoded_)
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
    def bin2hex(self, string_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(string_, "string", 1)
        if self.usenewsodiumapi():
            return php_str(sodium_bin2hex(string_))
        # end if
        if self.use_fallback("bin2hex"):
            return php_str(php_call_user_func("\\Sodium\\bin2hex", string_))
        # end if
        return ParagonIE_Sodium_Core_Util.bin2hex(string_)
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
    def compare(self, left_=None, right_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(left_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(right_, "string", 2)
        if self.usenewsodiumapi():
            return php_int(sodium_compare(left_, right_))
        # end if
        if self.use_fallback("compare"):
            return php_int(php_call_user_func("\\Sodium\\compare", left_, right_))
        # end if
        return ParagonIE_Sodium_Core_Util.compare(left_, right_)
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
    def crypto_aead_aes256gcm_decrypt(self, ciphertext_="", assocData_="", nonce_="", key_=""):
        
        
        if (not self.crypto_aead_aes256gcm_is_available()):
            raise php_new_class("SodiumException", lambda : SodiumException("AES-256-GCM is not available"))
        # end if
        ParagonIE_Sodium_Core_Util.declarescalartype(ciphertext_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(assocData_, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(nonce_, "string", 3)
        ParagonIE_Sodium_Core_Util.declarescalartype(key_, "string", 4)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(nonce_) != self.CRYPTO_AEAD_AES256GCM_NPUBBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Nonce must be CRYPTO_AEAD_AES256GCM_NPUBBYTES long"))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(key_) != self.CRYPTO_AEAD_AES256GCM_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Key must be CRYPTO_AEAD_AES256GCM_KEYBYTES long"))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(ciphertext_) < self.CRYPTO_AEAD_AES256GCM_ABYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Message must be at least CRYPTO_AEAD_AES256GCM_ABYTES long"))
        # end if
        if (not php_is_callable("openssl_decrypt")):
            raise php_new_class("SodiumException", lambda : SodiumException("The OpenSSL extension is not installed, or openssl_decrypt() is not available"))
        # end if
        #// @var string $ctext
        ctext_ = ParagonIE_Sodium_Core_Util.substr(ciphertext_, 0, -self.CRYPTO_AEAD_AES256GCM_ABYTES)
        #// @var string $authTag
        authTag_ = ParagonIE_Sodium_Core_Util.substr(ciphertext_, -self.CRYPTO_AEAD_AES256GCM_ABYTES, 16)
        return openssl_decrypt(ctext_, "aes-256-gcm", key_, OPENSSL_RAW_DATA, nonce_, authTag_, assocData_)
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
    def crypto_aead_aes256gcm_encrypt(self, plaintext_="", assocData_="", nonce_="", key_=""):
        
        
        if (not self.crypto_aead_aes256gcm_is_available()):
            raise php_new_class("SodiumException", lambda : SodiumException("AES-256-GCM is not available"))
        # end if
        ParagonIE_Sodium_Core_Util.declarescalartype(plaintext_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(assocData_, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(nonce_, "string", 3)
        ParagonIE_Sodium_Core_Util.declarescalartype(key_, "string", 4)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(nonce_) != self.CRYPTO_AEAD_AES256GCM_NPUBBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Nonce must be CRYPTO_AEAD_AES256GCM_NPUBBYTES long"))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(key_) != self.CRYPTO_AEAD_AES256GCM_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Key must be CRYPTO_AEAD_AES256GCM_KEYBYTES long"))
        # end if
        if (not php_is_callable("openssl_encrypt")):
            raise php_new_class("SodiumException", lambda : SodiumException("The OpenSSL extension is not installed, or openssl_encrypt() is not available"))
        # end if
        authTag_ = ""
        ciphertext_ = openssl_encrypt(plaintext_, "aes-256-gcm", key_, OPENSSL_RAW_DATA, nonce_, authTag_, assocData_)
        return ciphertext_ + authTag_
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
    def crypto_aead_chacha20poly1305_decrypt(self, ciphertext_="", assocData_="", nonce_="", key_=""):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(ciphertext_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(assocData_, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(nonce_, "string", 3)
        ParagonIE_Sodium_Core_Util.declarescalartype(key_, "string", 4)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(nonce_) != self.CRYPTO_AEAD_CHACHA20POLY1305_NPUBBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Nonce must be CRYPTO_AEAD_CHACHA20POLY1305_NPUBBYTES long"))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(key_) != self.CRYPTO_AEAD_CHACHA20POLY1305_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Key must be CRYPTO_AEAD_CHACHA20POLY1305_KEYBYTES long"))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(ciphertext_) < self.CRYPTO_AEAD_CHACHA20POLY1305_ABYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Message must be at least CRYPTO_AEAD_CHACHA20POLY1305_ABYTES long"))
        # end if
        if self.usenewsodiumapi():
            #// 
            #// @psalm-suppress InvalidReturnStatement
            #// @psalm-suppress FalsableReturnStatement
            #//
            return sodium_crypto_aead_chacha20poly1305_decrypt(ciphertext_, assocData_, nonce_, key_)
        # end if
        if self.use_fallback("crypto_aead_chacha20poly1305_decrypt"):
            return php_call_user_func("\\Sodium\\crypto_aead_chacha20poly1305_decrypt", ciphertext_, assocData_, nonce_, key_)
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.aead_chacha20poly1305_decrypt(ciphertext_, assocData_, nonce_, key_)
        # end if
        return ParagonIE_Sodium_Crypto.aead_chacha20poly1305_decrypt(ciphertext_, assocData_, nonce_, key_)
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
    def crypto_aead_chacha20poly1305_encrypt(self, plaintext_="", assocData_="", nonce_="", key_=""):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(plaintext_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(assocData_, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(nonce_, "string", 3)
        ParagonIE_Sodium_Core_Util.declarescalartype(key_, "string", 4)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(nonce_) != self.CRYPTO_AEAD_CHACHA20POLY1305_NPUBBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Nonce must be CRYPTO_AEAD_CHACHA20POLY1305_NPUBBYTES long"))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(key_) != self.CRYPTO_AEAD_CHACHA20POLY1305_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Key must be CRYPTO_AEAD_CHACHA20POLY1305_KEYBYTES long"))
        # end if
        if self.usenewsodiumapi():
            return php_str(sodium_crypto_aead_chacha20poly1305_encrypt(plaintext_, assocData_, nonce_, key_))
        # end if
        if self.use_fallback("crypto_aead_chacha20poly1305_encrypt"):
            return php_str(php_call_user_func("\\Sodium\\crypto_aead_chacha20poly1305_encrypt", plaintext_, assocData_, nonce_, key_))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.aead_chacha20poly1305_encrypt(plaintext_, assocData_, nonce_, key_)
        # end if
        return ParagonIE_Sodium_Crypto.aead_chacha20poly1305_encrypt(plaintext_, assocData_, nonce_, key_)
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
    def crypto_aead_chacha20poly1305_ietf_decrypt(self, ciphertext_="", assocData_="", nonce_="", key_=""):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(ciphertext_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(assocData_, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(nonce_, "string", 3)
        ParagonIE_Sodium_Core_Util.declarescalartype(key_, "string", 4)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(nonce_) != self.CRYPTO_AEAD_CHACHA20POLY1305_IETF_NPUBBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Nonce must be CRYPTO_AEAD_CHACHA20POLY1305_IETF_NPUBBYTES long"))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(key_) != self.CRYPTO_AEAD_CHACHA20POLY1305_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Key must be CRYPTO_AEAD_CHACHA20POLY1305_KEYBYTES long"))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(ciphertext_) < self.CRYPTO_AEAD_CHACHA20POLY1305_ABYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Message must be at least CRYPTO_AEAD_CHACHA20POLY1305_ABYTES long"))
        # end if
        if self.usenewsodiumapi():
            #// 
            #// @psalm-suppress InvalidReturnStatement
            #// @psalm-suppress FalsableReturnStatement
            #//
            return sodium_crypto_aead_chacha20poly1305_ietf_decrypt(ciphertext_, assocData_, nonce_, key_)
        # end if
        if self.use_fallback("crypto_aead_chacha20poly1305_ietf_decrypt"):
            return php_call_user_func("\\Sodium\\crypto_aead_chacha20poly1305_ietf_decrypt", ciphertext_, assocData_, nonce_, key_)
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.aead_chacha20poly1305_ietf_decrypt(ciphertext_, assocData_, nonce_, key_)
        # end if
        return ParagonIE_Sodium_Crypto.aead_chacha20poly1305_ietf_decrypt(ciphertext_, assocData_, nonce_, key_)
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
    def crypto_aead_chacha20poly1305_ietf_encrypt(self, plaintext_="", assocData_="", nonce_="", key_=""):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(plaintext_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(assocData_, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(nonce_, "string", 3)
        ParagonIE_Sodium_Core_Util.declarescalartype(key_, "string", 4)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(nonce_) != self.CRYPTO_AEAD_CHACHA20POLY1305_IETF_NPUBBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Nonce must be CRYPTO_AEAD_CHACHA20POLY1305_IETF_NPUBBYTES long"))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(key_) != self.CRYPTO_AEAD_CHACHA20POLY1305_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Key must be CRYPTO_AEAD_CHACHA20POLY1305_KEYBYTES long"))
        # end if
        if self.usenewsodiumapi():
            return php_str(sodium_crypto_aead_chacha20poly1305_ietf_encrypt(plaintext_, assocData_, nonce_, key_))
        # end if
        if self.use_fallback("crypto_aead_chacha20poly1305_ietf_encrypt"):
            return php_str(php_call_user_func("\\Sodium\\crypto_aead_chacha20poly1305_ietf_encrypt", plaintext_, assocData_, nonce_, key_))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.aead_chacha20poly1305_ietf_encrypt(plaintext_, assocData_, nonce_, key_)
        # end if
        return ParagonIE_Sodium_Crypto.aead_chacha20poly1305_ietf_encrypt(plaintext_, assocData_, nonce_, key_)
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
    def crypto_aead_xchacha20poly1305_ietf_decrypt(self, ciphertext_="", assocData_="", nonce_="", key_="", dontFallback_=None):
        if dontFallback_ is None:
            dontFallback_ = False
        # end if
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(ciphertext_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(assocData_, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(nonce_, "string", 3)
        ParagonIE_Sodium_Core_Util.declarescalartype(key_, "string", 4)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(nonce_) != self.CRYPTO_AEAD_XCHACHA20POLY1305_IETF_NPUBBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Nonce must be CRYPTO_AEAD_XCHACHA20POLY1305_IETF_NPUBBYTES long"))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(key_) != self.CRYPTO_AEAD_XCHACHA20POLY1305_IETF_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Key must be CRYPTO_AEAD_XCHACHA20POLY1305_IETF_KEYBYTES long"))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(ciphertext_) < self.CRYPTO_AEAD_XCHACHA20POLY1305_IETF_ABYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Message must be at least CRYPTO_AEAD_XCHACHA20POLY1305_IETF_ABYTES long"))
        # end if
        if self.usenewsodiumapi() and (not dontFallback_):
            if php_is_callable("sodium_crypto_aead_xchacha20poly1305_ietf_decrypt"):
                return sodium_crypto_aead_xchacha20poly1305_ietf_decrypt(ciphertext_, assocData_, nonce_, key_)
            # end if
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.aead_xchacha20poly1305_ietf_decrypt(ciphertext_, assocData_, nonce_, key_)
        # end if
        return ParagonIE_Sodium_Crypto.aead_xchacha20poly1305_ietf_decrypt(ciphertext_, assocData_, nonce_, key_)
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
    def crypto_aead_xchacha20poly1305_ietf_encrypt(self, plaintext_="", assocData_="", nonce_="", key_="", dontFallback_=None):
        if dontFallback_ is None:
            dontFallback_ = False
        # end if
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(plaintext_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(assocData_, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(nonce_, "string", 3)
        ParagonIE_Sodium_Core_Util.declarescalartype(key_, "string", 4)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(nonce_) != self.CRYPTO_AEAD_XCHACHA20POLY1305_IETF_NPUBBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Nonce must be CRYPTO_AEAD_XCHACHA20POLY1305_NPUBBYTES long"))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(key_) != self.CRYPTO_AEAD_XCHACHA20POLY1305_IETF_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Key must be CRYPTO_AEAD_XCHACHA20POLY1305_KEYBYTES long"))
        # end if
        if self.usenewsodiumapi() and (not dontFallback_):
            if php_is_callable("sodium_crypto_aead_xchacha20poly1305_ietf_encrypt"):
                return sodium_crypto_aead_xchacha20poly1305_ietf_encrypt(plaintext_, assocData_, nonce_, key_)
            # end if
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.aead_xchacha20poly1305_ietf_encrypt(plaintext_, assocData_, nonce_, key_)
        # end if
        return ParagonIE_Sodium_Crypto.aead_xchacha20poly1305_ietf_encrypt(plaintext_, assocData_, nonce_, key_)
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
    def crypto_auth(self, message_=None, key_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(message_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(key_, "string", 2)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(key_) != self.CRYPTO_AUTH_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_AUTH_KEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return php_str(sodium_crypto_auth(message_, key_))
        # end if
        if self.use_fallback("crypto_auth"):
            return php_str(php_call_user_func("\\Sodium\\crypto_auth", message_, key_))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.auth(message_, key_)
        # end if
        return ParagonIE_Sodium_Crypto.auth(message_, key_)
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
    def crypto_auth_verify(self, mac_=None, message_=None, key_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(mac_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(message_, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(key_, "string", 3)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(mac_) != self.CRYPTO_AUTH_BYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 1 must be CRYPTO_AUTH_BYTES long."))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(key_) != self.CRYPTO_AUTH_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 3 must be CRYPTO_AUTH_KEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return php_bool(sodium_crypto_auth_verify(mac_, message_, key_))
        # end if
        if self.use_fallback("crypto_auth_verify"):
            return php_bool(php_call_user_func("\\Sodium\\crypto_auth_verify", mac_, message_, key_))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.auth_verify(mac_, message_, key_)
        # end if
        return ParagonIE_Sodium_Crypto.auth_verify(mac_, message_, key_)
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
    def crypto_box(self, plaintext_=None, nonce_=None, keypair_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(plaintext_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(nonce_, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(keypair_, "string", 3)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(nonce_) != self.CRYPTO_BOX_NONCEBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_BOX_NONCEBYTES long."))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(keypair_) != self.CRYPTO_BOX_KEYPAIRBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 3 must be CRYPTO_BOX_KEYPAIRBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return php_str(php_sodium_crypto_box(plaintext_, nonce_, keypair_))
        # end if
        if self.use_fallback("crypto_box"):
            return php_str(php_call_user_func("\\Sodium\\crypto_box", plaintext_, nonce_, keypair_))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.box(plaintext_, nonce_, keypair_)
        # end if
        return ParagonIE_Sodium_Crypto.box(plaintext_, nonce_, keypair_)
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
    def crypto_box_seal(self, plaintext_=None, publicKey_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(plaintext_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(publicKey_, "string", 2)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(publicKey_) != self.CRYPTO_BOX_PUBLICKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_BOX_PUBLICKEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return php_str(sodium_crypto_box_seal(plaintext_, publicKey_))
        # end if
        if self.use_fallback("crypto_box_seal"):
            return php_str(php_call_user_func("\\Sodium\\crypto_box_seal", plaintext_, publicKey_))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.box_seal(plaintext_, publicKey_)
        # end if
        return ParagonIE_Sodium_Crypto.box_seal(plaintext_, publicKey_)
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
    def crypto_box_seal_open(self, ciphertext_=None, keypair_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(ciphertext_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(keypair_, "string", 2)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(keypair_) != self.CRYPTO_BOX_KEYPAIRBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_BOX_KEYPAIRBYTES long."))
        # end if
        if self.usenewsodiumapi():
            #// 
            #// @psalm-suppress InvalidReturnStatement
            #// @psalm-suppress FalsableReturnStatement
            #//
            return sodium_crypto_box_seal_open(ciphertext_, keypair_)
        # end if
        if self.use_fallback("crypto_box_seal_open"):
            return php_call_user_func("\\Sodium\\crypto_box_seal_open", ciphertext_, keypair_)
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.box_seal_open(ciphertext_, keypair_)
        # end if
        return ParagonIE_Sodium_Crypto.box_seal_open(ciphertext_, keypair_)
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
    def crypto_box_keypair_from_secretkey_and_publickey(self, secretKey_=None, publicKey_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(secretKey_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(publicKey_, "string", 2)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(secretKey_) != self.CRYPTO_BOX_SECRETKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 1 must be CRYPTO_BOX_SECRETKEYBYTES long."))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(publicKey_) != self.CRYPTO_BOX_PUBLICKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_BOX_PUBLICKEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return php_str(sodium_crypto_box_keypair_from_secretkey_and_publickey(secretKey_, publicKey_))
        # end if
        if self.use_fallback("crypto_box_keypair_from_secretkey_and_publickey"):
            return php_str(php_call_user_func("\\Sodium\\crypto_box_keypair_from_secretkey_and_publickey", secretKey_, publicKey_))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.box_keypair_from_secretkey_and_publickey(secretKey_, publicKey_)
        # end if
        return ParagonIE_Sodium_Crypto.box_keypair_from_secretkey_and_publickey(secretKey_, publicKey_)
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
    def crypto_box_open(self, ciphertext_=None, nonce_=None, keypair_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(ciphertext_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(nonce_, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(keypair_, "string", 3)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(ciphertext_) < self.CRYPTO_BOX_MACBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 1 must be at least CRYPTO_BOX_MACBYTES long."))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(nonce_) != self.CRYPTO_BOX_NONCEBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_BOX_NONCEBYTES long."))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(keypair_) != self.CRYPTO_BOX_KEYPAIRBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 3 must be CRYPTO_BOX_KEYPAIRBYTES long."))
        # end if
        if self.usenewsodiumapi():
            #// 
            #// @psalm-suppress InvalidReturnStatement
            #// @psalm-suppress FalsableReturnStatement
            #//
            return sodium_crypto_box_open(ciphertext_, nonce_, keypair_)
        # end if
        if self.use_fallback("crypto_box_open"):
            return php_call_user_func("\\Sodium\\crypto_box_open", ciphertext_, nonce_, keypair_)
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.box_open(ciphertext_, nonce_, keypair_)
        # end if
        return ParagonIE_Sodium_Crypto.box_open(ciphertext_, nonce_, keypair_)
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
    def crypto_box_publickey(self, keypair_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(keypair_, "string", 1)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(keypair_) != self.CRYPTO_BOX_KEYPAIRBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 1 must be CRYPTO_BOX_KEYPAIRBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return php_str(sodium_crypto_box_publickey(keypair_))
        # end if
        if self.use_fallback("crypto_box_publickey"):
            return php_str(php_call_user_func("\\Sodium\\crypto_box_publickey", keypair_))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.box_publickey(keypair_)
        # end if
        return ParagonIE_Sodium_Crypto.box_publickey(keypair_)
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
    def crypto_box_publickey_from_secretkey(self, secretKey_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(secretKey_, "string", 1)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(secretKey_) != self.CRYPTO_BOX_SECRETKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 1 must be CRYPTO_BOX_SECRETKEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return php_str(sodium_crypto_box_publickey_from_secretkey(secretKey_))
        # end if
        if self.use_fallback("crypto_box_publickey_from_secretkey"):
            return php_str(php_call_user_func("\\Sodium\\crypto_box_publickey_from_secretkey", secretKey_))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.box_publickey_from_secretkey(secretKey_)
        # end if
        return ParagonIE_Sodium_Crypto.box_publickey_from_secretkey(secretKey_)
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
    def crypto_box_secretkey(self, keypair_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(keypair_, "string", 1)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(keypair_) != self.CRYPTO_BOX_KEYPAIRBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 1 must be CRYPTO_BOX_KEYPAIRBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return php_str(sodium_crypto_box_secretkey(keypair_))
        # end if
        if self.use_fallback("crypto_box_secretkey"):
            return php_str(php_call_user_func("\\Sodium\\crypto_box_secretkey", keypair_))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.box_secretkey(keypair_)
        # end if
        return ParagonIE_Sodium_Crypto.box_secretkey(keypair_)
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
    def crypto_box_seed_keypair(self, seed_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(seed_, "string", 1)
        if self.usenewsodiumapi():
            return php_str(sodium_crypto_box_seed_keypair(seed_))
        # end if
        if self.use_fallback("crypto_box_seed_keypair"):
            return php_str(php_call_user_func("\\Sodium\\crypto_box_seed_keypair", seed_))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.box_seed_keypair(seed_)
        # end if
        return ParagonIE_Sodium_Crypto.box_seed_keypair(seed_)
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
    def crypto_generichash(self, message_=None, key_="", length_=None):
        if length_ is None:
            length_ = self.CRYPTO_GENERICHASH_BYTES
        # end if
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(message_, "string", 1)
        if is_null(key_):
            key_ = ""
        # end if
        ParagonIE_Sodium_Core_Util.declarescalartype(key_, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(length_, "int", 3)
        #// Input validation:
        if (not php_empty(lambda : key_)):
            if ParagonIE_Sodium_Core_Util.strlen(key_) < self.CRYPTO_GENERICHASH_KEYBYTES_MIN:
                raise php_new_class("SodiumException", lambda : SodiumException("Unsupported key size. Must be at least CRYPTO_GENERICHASH_KEYBYTES_MIN bytes long."))
            # end if
            if ParagonIE_Sodium_Core_Util.strlen(key_) > self.CRYPTO_GENERICHASH_KEYBYTES_MAX:
                raise php_new_class("SodiumException", lambda : SodiumException("Unsupported key size. Must be at most CRYPTO_GENERICHASH_KEYBYTES_MAX bytes long."))
            # end if
        # end if
        if self.usenewsodiumapi():
            return php_str(sodium_crypto_generichash(message_, key_, length_))
        # end if
        if self.use_fallback("crypto_generichash"):
            return php_str(php_call_user_func("\\Sodium\\crypto_generichash", message_, key_, length_))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.generichash(message_, key_, length_)
        # end if
        return ParagonIE_Sodium_Crypto.generichash(message_, key_, length_)
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
    def crypto_generichash_final(self, ctx_=None, length_=None):
        if length_ is None:
            length_ = self.CRYPTO_GENERICHASH_BYTES
        # end if
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(ctx_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(length_, "int", 2)
        if self.usenewsodiumapi():
            return sodium_crypto_generichash_final(ctx_, length_)
        # end if
        if self.use_fallback("crypto_generichash_final"):
            func_ = "\\Sodium\\crypto_generichash_final"
            return php_str(func_(ctx_, length_))
        # end if
        if length_ < 1:
            try: 
                self.memzero(ctx_)
            except SodiumException as ex_:
                ctx_ = None
            # end try
            return ""
        # end if
        if PHP_INT_SIZE == 4:
            result_ = ParagonIE_Sodium_Crypto32.generichash_final(ctx_, length_)
        else:
            result_ = ParagonIE_Sodium_Crypto.generichash_final(ctx_, length_)
        # end if
        try: 
            self.memzero(ctx_)
        except SodiumException as ex_:
            ctx_ = None
        # end try
        return result_
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
    def crypto_generichash_init(self, key_="", length_=None):
        if length_ is None:
            length_ = self.CRYPTO_GENERICHASH_BYTES
        # end if
        
        #// Type checks:
        if is_null(key_):
            key_ = ""
        # end if
        ParagonIE_Sodium_Core_Util.declarescalartype(key_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(length_, "int", 2)
        #// Input validation:
        if (not php_empty(lambda : key_)):
            if ParagonIE_Sodium_Core_Util.strlen(key_) < self.CRYPTO_GENERICHASH_KEYBYTES_MIN:
                raise php_new_class("SodiumException", lambda : SodiumException("Unsupported key size. Must be at least CRYPTO_GENERICHASH_KEYBYTES_MIN bytes long."))
            # end if
            if ParagonIE_Sodium_Core_Util.strlen(key_) > self.CRYPTO_GENERICHASH_KEYBYTES_MAX:
                raise php_new_class("SodiumException", lambda : SodiumException("Unsupported key size. Must be at most CRYPTO_GENERICHASH_KEYBYTES_MAX bytes long."))
            # end if
        # end if
        if self.usenewsodiumapi():
            return sodium_crypto_generichash_init(key_, length_)
        # end if
        if self.use_fallback("crypto_generichash_init"):
            return php_str(php_call_user_func("\\Sodium\\crypto_generichash_init", key_, length_))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.generichash_init(key_, length_)
        # end if
        return ParagonIE_Sodium_Crypto.generichash_init(key_, length_)
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
    def crypto_generichash_init_salt_personal(self, key_="", length_=None, salt_="", personal_=""):
        if length_ is None:
            length_ = self.CRYPTO_GENERICHASH_BYTES
        # end if
        
        #// Type checks:
        if is_null(key_):
            key_ = ""
        # end if
        ParagonIE_Sodium_Core_Util.declarescalartype(key_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(length_, "int", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(salt_, "string", 3)
        ParagonIE_Sodium_Core_Util.declarescalartype(personal_, "string", 4)
        salt_ = php_str_pad(salt_, 16, " ", STR_PAD_RIGHT)
        personal_ = php_str_pad(personal_, 16, " ", STR_PAD_RIGHT)
        #// Input validation:
        if (not php_empty(lambda : key_)):
            #// 
            #// if (ParagonIE_Sodium_Core_Util::strlen($key) < self::CRYPTO_GENERICHASH_KEYBYTES_MIN) {
            #// throw new SodiumException('Unsupported key size. Must be at least CRYPTO_GENERICHASH_KEYBYTES_MIN bytes long.');
            #// }
            #//
            if ParagonIE_Sodium_Core_Util.strlen(key_) > self.CRYPTO_GENERICHASH_KEYBYTES_MAX:
                raise php_new_class("SodiumException", lambda : SodiumException("Unsupported key size. Must be at most CRYPTO_GENERICHASH_KEYBYTES_MAX bytes long."))
            # end if
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.generichash_init_salt_personal(key_, length_, salt_, personal_)
        # end if
        return ParagonIE_Sodium_Crypto.generichash_init_salt_personal(key_, length_, salt_, personal_)
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
    def crypto_generichash_update(self, ctx_=None, message_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(ctx_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(message_, "string", 2)
        if self.usenewsodiumapi():
            sodium_crypto_generichash_update(ctx_, message_)
            return
        # end if
        if self.use_fallback("crypto_generichash_update"):
            func_ = "\\Sodium\\crypto_generichash_update"
            func_(ctx_, message_)
            return
        # end if
        if PHP_INT_SIZE == 4:
            ctx_ = ParagonIE_Sodium_Crypto32.generichash_update(ctx_, message_)
        else:
            ctx_ = ParagonIE_Sodium_Crypto.generichash_update(ctx_, message_)
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
    def crypto_kdf_derive_from_key(self, subkey_len_=None, subkey_id_=None, context_=None, key_=None):
        
        
        ParagonIE_Sodium_Core_Util.declarescalartype(subkey_len_, "int", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(subkey_id_, "int", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(context_, "string", 3)
        ParagonIE_Sodium_Core_Util.declarescalartype(key_, "string", 4)
        subkey_id_ = php_int(subkey_id_)
        subkey_len_ = php_int(subkey_len_)
        context_ = php_str(context_)
        key_ = php_str(key_)
        if subkey_len_ < self.CRYPTO_KDF_BYTES_MIN:
            raise php_new_class("SodiumException", lambda : SodiumException("subkey cannot be smaller than SODIUM_CRYPTO_KDF_BYTES_MIN"))
        # end if
        if subkey_len_ > self.CRYPTO_KDF_BYTES_MAX:
            raise php_new_class("SodiumException", lambda : SodiumException("subkey cannot be larger than SODIUM_CRYPTO_KDF_BYTES_MAX"))
        # end if
        if subkey_id_ < 0:
            raise php_new_class("SodiumException", lambda : SodiumException("subkey_id cannot be negative"))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(context_) != self.CRYPTO_KDF_CONTEXTBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("context should be SODIUM_CRYPTO_KDF_CONTEXTBYTES bytes"))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(key_) != self.CRYPTO_KDF_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("key should be SODIUM_CRYPTO_KDF_KEYBYTES bytes"))
        # end if
        salt_ = ParagonIE_Sodium_Core_Util.store64_le(subkey_id_)
        state_ = self.crypto_generichash_init_salt_personal(key_, subkey_len_, salt_, context_)
        return self.crypto_generichash_final(state_, subkey_len_)
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
    def crypto_kx(self, my_secret_=None, their_public_=None, client_public_=None, server_public_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(my_secret_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(their_public_, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(client_public_, "string", 3)
        ParagonIE_Sodium_Core_Util.declarescalartype(server_public_, "string", 4)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(my_secret_) != self.CRYPTO_BOX_SECRETKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 1 must be CRYPTO_BOX_SECRETKEYBYTES long."))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(their_public_) != self.CRYPTO_BOX_PUBLICKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_BOX_PUBLICKEYBYTES long."))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(client_public_) != self.CRYPTO_BOX_PUBLICKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 3 must be CRYPTO_BOX_PUBLICKEYBYTES long."))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(server_public_) != self.CRYPTO_BOX_PUBLICKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 4 must be CRYPTO_BOX_PUBLICKEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            if php_is_callable("sodium_crypto_kx"):
                return php_str(sodium_crypto_kx(my_secret_, their_public_, client_public_, server_public_))
            # end if
        # end if
        if self.use_fallback("crypto_kx"):
            return php_str(php_call_user_func("\\Sodium\\crypto_kx", my_secret_, their_public_, client_public_, server_public_))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.keyexchange(my_secret_, their_public_, client_public_, server_public_)
        # end if
        return ParagonIE_Sodium_Crypto.keyexchange(my_secret_, their_public_, client_public_, server_public_)
    # end def crypto_kx
    #// 
    #// @param string $seed
    #// @return string
    #// @throws SodiumException
    #//
    @classmethod
    def crypto_kx_seed_keypair(self, seed_=None):
        
        
        ParagonIE_Sodium_Core_Util.declarescalartype(seed_, "string", 1)
        seed_ = php_str(seed_)
        if ParagonIE_Sodium_Core_Util.strlen(seed_) != self.CRYPTO_KX_SEEDBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("seed must be SODIUM_CRYPTO_KX_SEEDBYTES bytes"))
        # end if
        sk_ = self.crypto_generichash(seed_, "", self.CRYPTO_KX_SECRETKEYBYTES)
        pk_ = self.crypto_scalarmult_base(sk_)
        return sk_ + pk_
    # end def crypto_kx_seed_keypair
    #// 
    #// @return string
    #// @throws Exception
    #//
    @classmethod
    def crypto_kx_keypair(self):
        
        
        sk_ = self.randombytes_buf(self.CRYPTO_KX_SECRETKEYBYTES)
        pk_ = self.crypto_scalarmult_base(sk_)
        return sk_ + pk_
    # end def crypto_kx_keypair
    #// 
    #// @param string $keypair
    #// @param string $serverPublicKey
    #// @return array{0: string, 1: string}
    #// @throws SodiumException
    #//
    @classmethod
    def crypto_kx_client_session_keys(self, keypair_=None, serverPublicKey_=None):
        
        
        ParagonIE_Sodium_Core_Util.declarescalartype(keypair_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(serverPublicKey_, "string", 2)
        keypair_ = php_str(keypair_)
        serverPublicKey_ = php_str(serverPublicKey_)
        if ParagonIE_Sodium_Core_Util.strlen(keypair_) != self.CRYPTO_KX_KEYPAIRBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("keypair should be SODIUM_CRYPTO_KX_KEYPAIRBYTES bytes"))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(serverPublicKey_) != self.CRYPTO_KX_PUBLICKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("public keys must be SODIUM_CRYPTO_KX_PUBLICKEYBYTES bytes"))
        # end if
        sk_ = self.crypto_kx_secretkey(keypair_)
        pk_ = self.crypto_kx_publickey(keypair_)
        h_ = self.crypto_generichash_init(None, self.CRYPTO_KX_SESSIONKEYBYTES * 2)
        self.crypto_generichash_update(h_, self.crypto_scalarmult(sk_, serverPublicKey_))
        self.crypto_generichash_update(h_, pk_)
        self.crypto_generichash_update(h_, serverPublicKey_)
        sessionKeys_ = self.crypto_generichash_final(h_, self.CRYPTO_KX_SESSIONKEYBYTES * 2)
        return Array(ParagonIE_Sodium_Core_Util.substr(sessionKeys_, 0, self.CRYPTO_KX_SESSIONKEYBYTES), ParagonIE_Sodium_Core_Util.substr(sessionKeys_, self.CRYPTO_KX_SESSIONKEYBYTES, self.CRYPTO_KX_SESSIONKEYBYTES))
    # end def crypto_kx_client_session_keys
    #// 
    #// @param string $keypair
    #// @param string $clientPublicKey
    #// @return array{0: string, 1: string}
    #// @throws SodiumException
    #//
    @classmethod
    def crypto_kx_server_session_keys(self, keypair_=None, clientPublicKey_=None):
        
        
        ParagonIE_Sodium_Core_Util.declarescalartype(keypair_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(clientPublicKey_, "string", 2)
        keypair_ = php_str(keypair_)
        clientPublicKey_ = php_str(clientPublicKey_)
        if ParagonIE_Sodium_Core_Util.strlen(keypair_) != self.CRYPTO_KX_KEYPAIRBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("keypair should be SODIUM_CRYPTO_KX_KEYPAIRBYTES bytes"))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(clientPublicKey_) != self.CRYPTO_KX_PUBLICKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("public keys must be SODIUM_CRYPTO_KX_PUBLICKEYBYTES bytes"))
        # end if
        sk_ = self.crypto_kx_secretkey(keypair_)
        pk_ = self.crypto_kx_publickey(keypair_)
        h_ = self.crypto_generichash_init(None, self.CRYPTO_KX_SESSIONKEYBYTES * 2)
        self.crypto_generichash_update(h_, self.crypto_scalarmult(sk_, clientPublicKey_))
        self.crypto_generichash_update(h_, clientPublicKey_)
        self.crypto_generichash_update(h_, pk_)
        sessionKeys_ = self.crypto_generichash_final(h_, self.CRYPTO_KX_SESSIONKEYBYTES * 2)
        return Array(ParagonIE_Sodium_Core_Util.substr(sessionKeys_, self.CRYPTO_KX_SESSIONKEYBYTES, self.CRYPTO_KX_SESSIONKEYBYTES), ParagonIE_Sodium_Core_Util.substr(sessionKeys_, 0, self.CRYPTO_KX_SESSIONKEYBYTES))
    # end def crypto_kx_server_session_keys
    #// 
    #// @param string $kp
    #// @return string
    #// @throws SodiumException
    #//
    @classmethod
    def crypto_kx_secretkey(self, kp_=None):
        
        
        return ParagonIE_Sodium_Core_Util.substr(kp_, 0, self.CRYPTO_KX_SECRETKEYBYTES)
    # end def crypto_kx_secretkey
    #// 
    #// @param string $kp
    #// @return string
    #// @throws SodiumException
    #//
    @classmethod
    def crypto_kx_publickey(self, kp_=None):
        
        
        return ParagonIE_Sodium_Core_Util.substr(kp_, self.CRYPTO_KX_SECRETKEYBYTES, self.CRYPTO_KX_PUBLICKEYBYTES)
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
    def crypto_pwhash(self, outlen_=None, passwd_=None, salt_=None, opslimit_=None, memlimit_=None, alg_=None):
        
        
        ParagonIE_Sodium_Core_Util.declarescalartype(outlen_, "int", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(passwd_, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(salt_, "string", 3)
        ParagonIE_Sodium_Core_Util.declarescalartype(opslimit_, "int", 4)
        ParagonIE_Sodium_Core_Util.declarescalartype(memlimit_, "int", 5)
        if self.usenewsodiumapi():
            if (not is_null(alg_)):
                ParagonIE_Sodium_Core_Util.declarescalartype(alg_, "int", 6)
                return sodium_crypto_pwhash(outlen_, passwd_, salt_, opslimit_, memlimit_, alg_)
            # end if
            return sodium_crypto_pwhash(outlen_, passwd_, salt_, opslimit_, memlimit_)
        # end if
        if self.use_fallback("crypto_pwhash"):
            return php_str(php_call_user_func("\\Sodium\\crypto_pwhash", outlen_, passwd_, salt_, opslimit_, memlimit_))
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
    def crypto_pwhash_str(self, passwd_=None, opslimit_=None, memlimit_=None):
        
        
        ParagonIE_Sodium_Core_Util.declarescalartype(passwd_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(opslimit_, "int", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(memlimit_, "int", 3)
        if self.usenewsodiumapi():
            return sodium_crypto_pwhash_str(passwd_, opslimit_, memlimit_)
        # end if
        if self.use_fallback("crypto_pwhash_str"):
            return php_str(php_call_user_func("\\Sodium\\crypto_pwhash_str", passwd_, opslimit_, memlimit_))
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
    def crypto_pwhash_str_needs_rehash(self, hash_=None, opslimit_=None, memlimit_=None):
        
        
        ParagonIE_Sodium_Core_Util.declarescalartype(hash_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(opslimit_, "int", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(memlimit_, "int", 3)
        #// Just grab the first 4 pieces.
        pieces_ = php_explode("$", php_str(hash_))
        prefix_ = php_implode("$", php_array_slice(pieces_, 0, 4))
        #// Rebuild the expected header.
        #// @var int $ops
        ops_ = php_int(opslimit_)
        #// @var int $mem
        mem_ = php_int(memlimit_) >> 10
        encoded_ = self.CRYPTO_PWHASH_STRPREFIX + "v=19$m=" + mem_ + ",t=" + ops_ + ",p=1"
        #// Do they match? If so, we don't need to rehash, so return false.
        return (not ParagonIE_Sodium_Core_Util.hashequals(encoded_, prefix_))
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
    def crypto_pwhash_str_verify(self, passwd_=None, hash_=None):
        
        
        ParagonIE_Sodium_Core_Util.declarescalartype(passwd_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(hash_, "string", 2)
        if self.usenewsodiumapi():
            return php_bool(sodium_crypto_pwhash_str_verify(passwd_, hash_))
        # end if
        if self.use_fallback("crypto_pwhash_str_verify"):
            return php_bool(php_call_user_func("\\Sodium\\crypto_pwhash_str_verify", passwd_, hash_))
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
    def crypto_pwhash_scryptsalsa208sha256(self, outlen_=None, passwd_=None, salt_=None, opslimit_=None, memlimit_=None):
        
        
        ParagonIE_Sodium_Core_Util.declarescalartype(outlen_, "int", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(passwd_, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(salt_, "string", 3)
        ParagonIE_Sodium_Core_Util.declarescalartype(opslimit_, "int", 4)
        ParagonIE_Sodium_Core_Util.declarescalartype(memlimit_, "int", 5)
        if self.usenewsodiumapi():
            return php_str(sodium_crypto_pwhash_scryptsalsa208sha256(php_int(outlen_), php_str(passwd_), php_str(salt_), php_int(opslimit_), php_int(memlimit_)))
        # end if
        if self.use_fallback("crypto_pwhash_scryptsalsa208sha256"):
            return php_str(php_call_user_func("\\Sodium\\crypto_pwhash_scryptsalsa208sha256", php_int(outlen_), php_str(passwd_), php_str(salt_), php_int(opslimit_), php_int(memlimit_)))
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
    def crypto_pwhash_scryptsalsa208sha256_str(self, passwd_=None, opslimit_=None, memlimit_=None):
        
        
        ParagonIE_Sodium_Core_Util.declarescalartype(passwd_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(opslimit_, "int", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(memlimit_, "int", 3)
        if self.usenewsodiumapi():
            return php_str(sodium_crypto_pwhash_scryptsalsa208sha256_str(php_str(passwd_), php_int(opslimit_), php_int(memlimit_)))
        # end if
        if self.use_fallback("crypto_pwhash_scryptsalsa208sha256_str"):
            return php_str(php_call_user_func("\\Sodium\\crypto_pwhash_scryptsalsa208sha256_str", php_str(passwd_), php_int(opslimit_), php_int(memlimit_)))
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
    def crypto_pwhash_scryptsalsa208sha256_str_verify(self, passwd_=None, hash_=None):
        
        
        ParagonIE_Sodium_Core_Util.declarescalartype(passwd_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(hash_, "string", 2)
        if self.usenewsodiumapi():
            return php_bool(sodium_crypto_pwhash_scryptsalsa208sha256_str_verify(php_str(passwd_), php_str(hash_)))
        # end if
        if self.use_fallback("crypto_pwhash_scryptsalsa208sha256_str_verify"):
            return php_bool(php_call_user_func("\\Sodium\\crypto_pwhash_scryptsalsa208sha256_str_verify", php_str(passwd_), php_str(hash_)))
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
    def crypto_scalarmult(self, secretKey_=None, publicKey_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(secretKey_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(publicKey_, "string", 2)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(secretKey_) != self.CRYPTO_BOX_SECRETKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 1 must be CRYPTO_BOX_SECRETKEYBYTES long."))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(publicKey_) != self.CRYPTO_BOX_PUBLICKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_BOX_PUBLICKEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return sodium_crypto_scalarmult(secretKey_, publicKey_)
        # end if
        if self.use_fallback("crypto_scalarmult"):
            return php_str(php_call_user_func("\\Sodium\\crypto_scalarmult", secretKey_, publicKey_))
        # end if
        #// Output validation: Forbid all-zero keys
        if ParagonIE_Sodium_Core_Util.hashequals(secretKey_, php_str_repeat(" ", self.CRYPTO_BOX_SECRETKEYBYTES)):
            raise php_new_class("SodiumException", lambda : SodiumException("Zero secret key is not allowed"))
        # end if
        if ParagonIE_Sodium_Core_Util.hashequals(publicKey_, php_str_repeat(" ", self.CRYPTO_BOX_PUBLICKEYBYTES)):
            raise php_new_class("SodiumException", lambda : SodiumException("Zero public key is not allowed"))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.scalarmult(secretKey_, publicKey_)
        # end if
        return ParagonIE_Sodium_Crypto.scalarmult(secretKey_, publicKey_)
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
    def crypto_scalarmult_base(self, secretKey_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(secretKey_, "string", 1)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(secretKey_) != self.CRYPTO_BOX_SECRETKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 1 must be CRYPTO_BOX_SECRETKEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return sodium_crypto_scalarmult_base(secretKey_)
        # end if
        if self.use_fallback("crypto_scalarmult_base"):
            return php_str(php_call_user_func("\\Sodium\\crypto_scalarmult_base", secretKey_))
        # end if
        if ParagonIE_Sodium_Core_Util.hashequals(secretKey_, php_str_repeat(" ", self.CRYPTO_BOX_SECRETKEYBYTES)):
            raise php_new_class("SodiumException", lambda : SodiumException("Zero secret key is not allowed"))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.scalarmult_base(secretKey_)
        # end if
        return ParagonIE_Sodium_Crypto.scalarmult_base(secretKey_)
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
    def crypto_secretbox(self, plaintext_=None, nonce_=None, key_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(plaintext_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(nonce_, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(key_, "string", 3)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(nonce_) != self.CRYPTO_SECRETBOX_NONCEBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_SECRETBOX_NONCEBYTES long."))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(key_) != self.CRYPTO_SECRETBOX_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 3 must be CRYPTO_SECRETBOX_KEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return sodium_crypto_secretbox(plaintext_, nonce_, key_)
        # end if
        if self.use_fallback("crypto_secretbox"):
            return php_str(php_call_user_func("\\Sodium\\crypto_secretbox", plaintext_, nonce_, key_))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.secretbox(plaintext_, nonce_, key_)
        # end if
        return ParagonIE_Sodium_Crypto.secretbox(plaintext_, nonce_, key_)
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
    def crypto_secretbox_open(self, ciphertext_=None, nonce_=None, key_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(ciphertext_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(nonce_, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(key_, "string", 3)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(nonce_) != self.CRYPTO_SECRETBOX_NONCEBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_SECRETBOX_NONCEBYTES long."))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(key_) != self.CRYPTO_SECRETBOX_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 3 must be CRYPTO_SECRETBOX_KEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            #// 
            #// @psalm-suppress InvalidReturnStatement
            #// @psalm-suppress FalsableReturnStatement
            #//
            return sodium_crypto_secretbox_open(ciphertext_, nonce_, key_)
        # end if
        if self.use_fallback("crypto_secretbox_open"):
            return php_call_user_func("\\Sodium\\crypto_secretbox_open", ciphertext_, nonce_, key_)
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.secretbox_open(ciphertext_, nonce_, key_)
        # end if
        return ParagonIE_Sodium_Crypto.secretbox_open(ciphertext_, nonce_, key_)
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
    def crypto_secretbox_xchacha20poly1305(self, plaintext_=None, nonce_=None, key_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(plaintext_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(nonce_, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(key_, "string", 3)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(nonce_) != self.CRYPTO_SECRETBOX_NONCEBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_SECRETBOX_NONCEBYTES long."))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(key_) != self.CRYPTO_SECRETBOX_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 3 must be CRYPTO_SECRETBOX_KEYBYTES long."))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.secretbox_xchacha20poly1305(plaintext_, nonce_, key_)
        # end if
        return ParagonIE_Sodium_Crypto.secretbox_xchacha20poly1305(plaintext_, nonce_, key_)
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
    def crypto_secretbox_xchacha20poly1305_open(self, ciphertext_=None, nonce_=None, key_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(ciphertext_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(nonce_, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(key_, "string", 3)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(nonce_) != self.CRYPTO_SECRETBOX_NONCEBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_SECRETBOX_NONCEBYTES long."))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(key_) != self.CRYPTO_SECRETBOX_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 3 must be CRYPTO_SECRETBOX_KEYBYTES long."))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.secretbox_xchacha20poly1305_open(ciphertext_, nonce_, key_)
        # end if
        return ParagonIE_Sodium_Crypto.secretbox_xchacha20poly1305_open(ciphertext_, nonce_, key_)
    # end def crypto_secretbox_xchacha20poly1305_open
    #// 
    #// @param string $key
    #// @return array<int, string> Returns a state and a header.
    #// @throws Exception
    #// @throws SodiumException
    #//
    @classmethod
    def crypto_secretstream_xchacha20poly1305_init_push(self, key_=None):
        
        
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.secretstream_xchacha20poly1305_init_push(key_)
        # end if
        return ParagonIE_Sodium_Crypto.secretstream_xchacha20poly1305_init_push(key_)
    # end def crypto_secretstream_xchacha20poly1305_init_push
    #// 
    #// @param string $header
    #// @param string $key
    #// @return string Returns a state.
    #// @throws Exception
    #//
    @classmethod
    def crypto_secretstream_xchacha20poly1305_init_pull(self, header_=None, key_=None):
        
        
        if ParagonIE_Sodium_Core_Util.strlen(header_) < self.CRYPTO_SECRETSTREAM_XCHACHA20POLY1305_HEADERBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("header size should be SODIUM_CRYPTO_SECRETSTREAM_XCHACHA20POLY1305_HEADERBYTES bytes"))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.secretstream_xchacha20poly1305_init_pull(key_, header_)
        # end if
        return ParagonIE_Sodium_Crypto.secretstream_xchacha20poly1305_init_pull(key_, header_)
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
    def crypto_secretstream_xchacha20poly1305_push(self, state_=None, msg_=None, aad_="", tag_=0):
        
        
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.secretstream_xchacha20poly1305_push(state_, msg_, aad_, tag_)
        # end if
        return ParagonIE_Sodium_Crypto.secretstream_xchacha20poly1305_push(state_, msg_, aad_, tag_)
    # end def crypto_secretstream_xchacha20poly1305_push
    #// 
    #// @param string $state
    #// @param string $msg
    #// @param string $aad
    #// @return bool|array{0: string, 1: int}
    #// @throws SodiumException
    #//
    @classmethod
    def crypto_secretstream_xchacha20poly1305_pull(self, state_=None, msg_=None, aad_=""):
        
        
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.secretstream_xchacha20poly1305_pull(state_, msg_, aad_)
        # end if
        return ParagonIE_Sodium_Crypto.secretstream_xchacha20poly1305_pull(state_, msg_, aad_)
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
    def crypto_secretstream_xchacha20poly1305_rekey(self, state_=None):
        
        
        if PHP_INT_SIZE == 4:
            ParagonIE_Sodium_Crypto32.secretstream_xchacha20poly1305_rekey(state_)
        else:
            ParagonIE_Sodium_Crypto.secretstream_xchacha20poly1305_rekey(state_)
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
    def crypto_shorthash(self, message_=None, key_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(message_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(key_, "string", 2)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(key_) != self.CRYPTO_SHORTHASH_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_SHORTHASH_KEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return sodium_crypto_shorthash(message_, key_)
        # end if
        if self.use_fallback("crypto_shorthash"):
            return php_str(php_call_user_func("\\Sodium\\crypto_shorthash", message_, key_))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Core32_SipHash.siphash24(message_, key_)
        # end if
        return ParagonIE_Sodium_Core_SipHash.siphash24(message_, key_)
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
    def crypto_sign(self, message_=None, secretKey_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(message_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(secretKey_, "string", 2)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(secretKey_) != self.CRYPTO_SIGN_SECRETKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_SIGN_SECRETKEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return sodium_crypto_sign(message_, secretKey_)
        # end if
        if self.use_fallback("crypto_sign"):
            return php_str(php_call_user_func("\\Sodium\\crypto_sign", message_, secretKey_))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.sign(message_, secretKey_)
        # end if
        return ParagonIE_Sodium_Crypto.sign(message_, secretKey_)
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
    def crypto_sign_open(self, signedMessage_=None, publicKey_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(signedMessage_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(publicKey_, "string", 2)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(signedMessage_) < self.CRYPTO_SIGN_BYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 1 must be at least CRYPTO_SIGN_BYTES long."))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(publicKey_) != self.CRYPTO_SIGN_PUBLICKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_SIGN_PUBLICKEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            #// 
            #// @psalm-suppress InvalidReturnStatement
            #// @psalm-suppress FalsableReturnStatement
            #//
            return sodium_crypto_sign_open(signedMessage_, publicKey_)
        # end if
        if self.use_fallback("crypto_sign_open"):
            return php_call_user_func("\\Sodium\\crypto_sign_open", signedMessage_, publicKey_)
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.sign_open(signedMessage_, publicKey_)
        # end if
        return ParagonIE_Sodium_Crypto.sign_open(signedMessage_, publicKey_)
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
    def crypto_sign_keypair_from_secretkey_and_publickey(self, sk_=None, pk_=None):
        
        
        ParagonIE_Sodium_Core_Util.declarescalartype(sk_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(pk_, "string", 1)
        sk_ = php_str(sk_)
        pk_ = php_str(pk_)
        if ParagonIE_Sodium_Core_Util.strlen(sk_) != self.CRYPTO_SIGN_SECRETKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("secretkey should be SODIUM_CRYPTO_SIGN_SECRETKEYBYTES bytes"))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(pk_) != self.CRYPTO_SIGN_PUBLICKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("publickey should be SODIUM_CRYPTO_SIGN_PUBLICKEYBYTES bytes"))
        # end if
        if self.usenewsodiumapi():
            return sodium_crypto_sign_keypair_from_secretkey_and_publickey(sk_, pk_)
        # end if
        return sk_ + pk_
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
    def crypto_sign_seed_keypair(self, seed_=None):
        
        
        ParagonIE_Sodium_Core_Util.declarescalartype(seed_, "string", 1)
        if self.usenewsodiumapi():
            return sodium_crypto_sign_seed_keypair(seed_)
        # end if
        if self.use_fallback("crypto_sign_keypair"):
            return php_str(php_call_user_func("\\Sodium\\crypto_sign_seed_keypair", seed_))
        # end if
        publicKey_ = ""
        secretKey_ = ""
        if PHP_INT_SIZE == 4:
            ParagonIE_Sodium_Core32_Ed25519.seed_keypair(publicKey_, secretKey_, seed_)
        else:
            ParagonIE_Sodium_Core_Ed25519.seed_keypair(publicKey_, secretKey_, seed_)
        # end if
        return secretKey_ + publicKey_
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
    def crypto_sign_publickey(self, keypair_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(keypair_, "string", 1)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(keypair_) != self.CRYPTO_SIGN_KEYPAIRBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 1 must be CRYPTO_SIGN_KEYPAIRBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return sodium_crypto_sign_publickey(keypair_)
        # end if
        if self.use_fallback("crypto_sign_publickey"):
            return php_str(php_call_user_func("\\Sodium\\crypto_sign_publickey", keypair_))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Core32_Ed25519.publickey(keypair_)
        # end if
        return ParagonIE_Sodium_Core_Ed25519.publickey(keypair_)
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
    def crypto_sign_publickey_from_secretkey(self, secretKey_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(secretKey_, "string", 1)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(secretKey_) != self.CRYPTO_SIGN_SECRETKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 1 must be CRYPTO_SIGN_SECRETKEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return sodium_crypto_sign_publickey_from_secretkey(secretKey_)
        # end if
        if self.use_fallback("crypto_sign_publickey_from_secretkey"):
            return php_str(php_call_user_func("\\Sodium\\crypto_sign_publickey_from_secretkey", secretKey_))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Core32_Ed25519.publickey_from_secretkey(secretKey_)
        # end if
        return ParagonIE_Sodium_Core_Ed25519.publickey_from_secretkey(secretKey_)
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
    def crypto_sign_secretkey(self, keypair_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(keypair_, "string", 1)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(keypair_) != self.CRYPTO_SIGN_KEYPAIRBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 1 must be CRYPTO_SIGN_KEYPAIRBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return sodium_crypto_sign_secretkey(keypair_)
        # end if
        if self.use_fallback("crypto_sign_secretkey"):
            return php_str(php_call_user_func("\\Sodium\\crypto_sign_secretkey", keypair_))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Core32_Ed25519.secretkey(keypair_)
        # end if
        return ParagonIE_Sodium_Core_Ed25519.secretkey(keypair_)
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
    def crypto_sign_detached(self, message_=None, secretKey_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(message_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(secretKey_, "string", 2)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(secretKey_) != self.CRYPTO_SIGN_SECRETKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_SIGN_SECRETKEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return sodium_crypto_sign_detached(message_, secretKey_)
        # end if
        if self.use_fallback("crypto_sign_detached"):
            return php_str(php_call_user_func("\\Sodium\\crypto_sign_detached", message_, secretKey_))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.sign_detached(message_, secretKey_)
        # end if
        return ParagonIE_Sodium_Crypto.sign_detached(message_, secretKey_)
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
    def crypto_sign_verify_detached(self, signature_=None, message_=None, publicKey_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(signature_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(message_, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(publicKey_, "string", 3)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(signature_) != self.CRYPTO_SIGN_BYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 1 must be CRYPTO_SIGN_BYTES long."))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(publicKey_) != self.CRYPTO_SIGN_PUBLICKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 3 must be CRYPTO_SIGN_PUBLICKEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return sodium_crypto_sign_verify_detached(signature_, message_, publicKey_)
        # end if
        if self.use_fallback("crypto_sign_verify_detached"):
            return php_bool(php_call_user_func("\\Sodium\\crypto_sign_verify_detached", signature_, message_, publicKey_))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Crypto32.sign_verify_detached(signature_, message_, publicKey_)
        # end if
        return ParagonIE_Sodium_Crypto.sign_verify_detached(signature_, message_, publicKey_)
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
    def crypto_sign_ed25519_pk_to_curve25519(self, pk_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(pk_, "string", 1)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(pk_) < self.CRYPTO_SIGN_PUBLICKEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 1 must be at least CRYPTO_SIGN_PUBLICKEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            if php_is_callable("crypto_sign_ed25519_pk_to_curve25519"):
                return php_str(sodium_crypto_sign_ed25519_pk_to_curve25519(pk_))
            # end if
        # end if
        if self.use_fallback("crypto_sign_ed25519_pk_to_curve25519"):
            return php_str(php_call_user_func("\\Sodium\\crypto_sign_ed25519_pk_to_curve25519", pk_))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Core32_Ed25519.pk_to_curve25519(pk_)
        # end if
        return ParagonIE_Sodium_Core_Ed25519.pk_to_curve25519(pk_)
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
    def crypto_sign_ed25519_sk_to_curve25519(self, sk_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(sk_, "string", 1)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(sk_) < self.CRYPTO_SIGN_SEEDBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 1 must be at least CRYPTO_SIGN_SEEDBYTES long."))
        # end if
        if self.usenewsodiumapi():
            if php_is_callable("crypto_sign_ed25519_sk_to_curve25519"):
                return sodium_crypto_sign_ed25519_sk_to_curve25519(sk_)
            # end if
        # end if
        if self.use_fallback("crypto_sign_ed25519_sk_to_curve25519"):
            return php_str(php_call_user_func("\\Sodium\\crypto_sign_ed25519_sk_to_curve25519", sk_))
        # end if
        h_ = hash("sha512", ParagonIE_Sodium_Core_Util.substr(sk_, 0, 32), True)
        h_[0] = ParagonIE_Sodium_Core_Util.inttochr(ParagonIE_Sodium_Core_Util.chrtoint(h_[0]) & 248)
        h_[31] = ParagonIE_Sodium_Core_Util.inttochr(ParagonIE_Sodium_Core_Util.chrtoint(h_[31]) & 127 | 64)
        return ParagonIE_Sodium_Core_Util.substr(h_, 0, 32)
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
    def crypto_stream(self, len_=None, nonce_=None, key_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(len_, "int", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(nonce_, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(key_, "string", 3)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(nonce_) != self.CRYPTO_STREAM_NONCEBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_SECRETBOX_NONCEBYTES long."))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(key_) != self.CRYPTO_STREAM_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 3 must be CRYPTO_STREAM_KEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return sodium_crypto_stream(len_, nonce_, key_)
        # end if
        if self.use_fallback("crypto_stream"):
            return php_str(php_call_user_func("\\Sodium\\crypto_stream", len_, nonce_, key_))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Core32_XSalsa20.xsalsa20(len_, nonce_, key_)
        # end if
        return ParagonIE_Sodium_Core_XSalsa20.xsalsa20(len_, nonce_, key_)
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
    def crypto_stream_xor(self, message_=None, nonce_=None, key_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(message_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(nonce_, "string", 2)
        ParagonIE_Sodium_Core_Util.declarescalartype(key_, "string", 3)
        #// Input validation:
        if ParagonIE_Sodium_Core_Util.strlen(nonce_) != self.CRYPTO_STREAM_NONCEBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 2 must be CRYPTO_SECRETBOX_NONCEBYTES long."))
        # end if
        if ParagonIE_Sodium_Core_Util.strlen(key_) != self.CRYPTO_STREAM_KEYBYTES:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 3 must be CRYPTO_SECRETBOX_KEYBYTES long."))
        # end if
        if self.usenewsodiumapi():
            return sodium_crypto_stream_xor(message_, nonce_, key_)
        # end if
        if self.use_fallback("crypto_stream_xor"):
            return php_str(php_call_user_func("\\Sodium\\crypto_stream_xor", message_, nonce_, key_))
        # end if
        if PHP_INT_SIZE == 4:
            return ParagonIE_Sodium_Core32_XSalsa20.xsalsa20_xor(message_, nonce_, key_)
        # end if
        return ParagonIE_Sodium_Core_XSalsa20.xsalsa20_xor(message_, nonce_, key_)
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
    def hex2bin(self, string_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(string_, "string", 1)
        if self.usenewsodiumapi():
            if php_is_callable("sodium_hex2bin"):
                return php_str(sodium_hex2bin(string_))
            # end if
        # end if
        if self.use_fallback("hex2bin"):
            return php_str(php_call_user_func("\\Sodium\\hex2bin", string_))
        # end if
        return ParagonIE_Sodium_Core_Util.hex2bin(string_)
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
    def increment(self, var_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(var_, "string", 1)
        if self.usenewsodiumapi():
            sodium_increment(var_)
            return
        # end if
        if self.use_fallback("increment"):
            func_ = "\\Sodium\\increment"
            func_(var_)
            return
        # end if
        len_ = ParagonIE_Sodium_Core_Util.strlen(var_)
        c_ = 1
        copy_ = ""
        i_ = 0
        while i_ < len_:
            
            c_ += ParagonIE_Sodium_Core_Util.chrtoint(ParagonIE_Sodium_Core_Util.substr(var_, i_, 1))
            copy_ += ParagonIE_Sodium_Core_Util.inttochr(c_)
            c_ >>= 8
            i_ += 1
        # end while
        var_ = copy_
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
    def memcmp(self, left_=None, right_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(left_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(right_, "string", 2)
        if self.usenewsodiumapi():
            return sodium_memcmp(left_, right_)
        # end if
        if self.use_fallback("memcmp"):
            return php_int(php_call_user_func("\\Sodium\\memcmp", left_, right_))
        # end if
        #// @var string $left
        #// @var string $right
        return ParagonIE_Sodium_Core_Util.memcmp(left_, right_)
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
    def memzero(self, var_=None):
        
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(var_, "string", 1)
        if self.usenewsodiumapi():
            #// @psalm-suppress MixedArgument
            sodium_memzero(var_)
            return
        # end if
        if self.use_fallback("memzero"):
            func_ = "\\Sodium\\memzero"
            func_(var_)
            if var_ == None:
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
    def pad(self, unpadded_=None, blockSize_=None, dontFallback_=None):
        if dontFallback_ is None:
            dontFallback_ = False
        # end if
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(unpadded_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(blockSize_, "int", 2)
        unpadded_ = php_str(unpadded_)
        blockSize_ = php_int(blockSize_)
        if self.usenewsodiumapi() and (not dontFallback_):
            return php_str(sodium_pad(unpadded_, blockSize_))
        # end if
        if blockSize_ <= 0:
            raise php_new_class("SodiumException", lambda : SodiumException("block size cannot be less than 1"))
        # end if
        unpadded_len_ = ParagonIE_Sodium_Core_Util.strlen(unpadded_)
        xpadlen_ = blockSize_ - 1
        if blockSize_ & blockSize_ - 1 == 0:
            xpadlen_ -= unpadded_len_ & blockSize_ - 1
        else:
            xpadlen_ -= unpadded_len_ % blockSize_
        # end if
        xpadded_len_ = unpadded_len_ + xpadlen_
        padded_ = php_str_repeat(" ", xpadded_len_ - 1)
        if unpadded_len_ > 0:
            st_ = 1
            i_ = 0
            k_ = unpadded_len_
            j_ = 0
            while j_ <= xpadded_len_:
                
                i_ = php_int(i_)
                k_ = php_int(k_)
                st_ = php_int(st_)
                if j_ >= unpadded_len_:
                    padded_[j_] = " "
                else:
                    padded_[j_] = unpadded_[j_]
                # end if
                #// @var int $k
                k_ -= st_
                st_ = php_int((1 << (k_ >> 48 | k_ >> 32 | k_ >> 16 | k_ - 1 >> 16).bit_length()) - 1 - k_ >> 48 | k_ >> 32 | k_ >> 16 | k_ - 1 >> 16) & 1
                i_ += st_
                j_ += 1
            # end while
        # end if
        mask_ = 0
        tail_ = xpadded_len_
        i_ = 0
        while i_ < blockSize_:
            
            #// # barrier_mask = (unsigned char)
            #// #     (((i ^ xpadlen) - 1U) >> ((sizeof(size_t) - 1U) * CHAR_BIT));
            barrier_mask_ = i_ ^ xpadlen_ - 1 >> PHP_INT_SIZE << 3 - 1
            #// # tail[-i] = (tail[-i] & mask) | (0x80 & barrier_mask);
            padded_[tail_ - i_] = ParagonIE_Sodium_Core_Util.inttochr(ParagonIE_Sodium_Core_Util.chrtoint(padded_[tail_ - i_]) & mask_ | 128 & barrier_mask_)
            #// # mask |= barrier_mask;
            mask_ |= barrier_mask_
            i_ += 1
        # end while
        return padded_
    # end def pad
    #// 
    #// @param string $padded
    #// @param int $blockSize
    #// @param bool $dontFallback
    #// @return string
    #// @throws SodiumException
    #//
    @classmethod
    def unpad(self, padded_=None, blockSize_=None, dontFallback_=None):
        if dontFallback_ is None:
            dontFallback_ = False
        # end if
        
        #// Type checks:
        ParagonIE_Sodium_Core_Util.declarescalartype(padded_, "string", 1)
        ParagonIE_Sodium_Core_Util.declarescalartype(blockSize_, "int", 2)
        padded_ = php_str(padded_)
        blockSize_ = php_int(blockSize_)
        if self.usenewsodiumapi() and (not dontFallback_):
            return php_str(sodium_unpad(padded_, blockSize_))
        # end if
        if blockSize_ <= 0:
            raise php_new_class("SodiumException", lambda : SodiumException("block size cannot be less than 1"))
        # end if
        padded_len_ = ParagonIE_Sodium_Core_Util.strlen(padded_)
        if padded_len_ < blockSize_:
            raise php_new_class("SodiumException", lambda : SodiumException("invalid padding"))
        # end if
        #// # tail = &padded[padded_len - 1U];
        tail_ = padded_len_ - 1
        acc_ = 0
        valid_ = 0
        pad_len_ = 0
        found_ = 0
        i_ = 0
        while i_ < blockSize_:
            
            #// # c = tail[-i];
            c_ = ParagonIE_Sodium_Core_Util.chrtoint(padded_[tail_ - i_])
            #// # is_barrier =
            #// #     (( (acc - 1U) & (pad_len - 1U) & ((c ^ 0x80) - 1U) ) >> 8) & 1U;
            is_barrier_ = acc_ - 1 & pad_len_ - 1 & c_ ^ 80 - 1 >> 7 & 1
            is_barrier_ &= (1 << (found_).bit_length()) - 1 - found_
            found_ |= is_barrier_
            #// # acc |= c;
            acc_ |= c_
            #// # pad_len |= i & (1U + ~is_barrier);
            pad_len_ |= i_ & 1 + (1 << (is_barrier_).bit_length()) - 1 - is_barrier_
            #// # valid |= (unsigned char) is_barrier;
            valid_ |= is_barrier_ & 255
            i_ += 1
        # end while
        #// # unpadded_len = padded_len - 1U - pad_len;
        unpadded_len_ = padded_len_ - 1 - pad_len_
        if valid_ != 1:
            raise php_new_class("SodiumException", lambda : SodiumException("invalid padding"))
        # end if
        return ParagonIE_Sodium_Core_Util.substr(padded_, 0, unpadded_len_)
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
    def randombytes_buf(self, numBytes_=None):
        
        
        #// Type checks:
        if (not php_is_int(numBytes_)):
            if php_is_numeric(numBytes_):
                numBytes_ = php_int(numBytes_)
            else:
                raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be an integer, " + gettype(numBytes_) + " given."))
            # end if
        # end if
        if self.use_fallback("randombytes_buf"):
            return php_str(php_call_user_func("\\Sodium\\randombytes_buf", numBytes_))
        # end if
        return random_bytes(numBytes_)
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
    def randombytes_uniform(self, range_=None):
        
        
        #// Type checks:
        if (not php_is_int(range_)):
            if php_is_numeric(range_):
                range_ = php_int(range_)
            else:
                raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be an integer, " + gettype(range_) + " given."))
            # end if
        # end if
        if self.use_fallback("randombytes_uniform"):
            return php_int(php_call_user_func("\\Sodium\\randombytes_uniform", range_))
        # end if
        return php_random_int(0, range_ - 1)
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
        return php_random_int(0, 65535)
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
    def runtime_speed_test(self, iterations_=None, maxTimeout_=None):
        
        
        if self.polyfill_is_fast():
            return True
        # end if
        #// @var float $end
        end_ = 0
        #// @var float $start
        start_ = php_microtime(True)
        #// @var ParagonIE_Sodium_Core32_Int64 $a
        a_ = ParagonIE_Sodium_Core32_Int64.fromint(php_random_int(3, 1 << 16))
        i_ = 0
        while i_ < iterations_:
            
            #// @var ParagonIE_Sodium_Core32_Int64 $b
            b_ = ParagonIE_Sodium_Core32_Int64.fromint(php_random_int(3, 1 << 16))
            a_.mulint64(b_)
            i_ += 1
        # end while
        #// @var float $end
        end_ = php_microtime(True)
        #// @var int $diff
        diff_ = php_int(ceil(end_ - start_ * 1000))
        return diff_ < maxTimeout_
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
    def use_fallback(self, sodium_func_name_=""):
        
        
        res_ = None
        if res_ == None:
            res_ = php_extension_loaded("libsodium") and PHP_VERSION_ID >= 50300
        # end if
        if res_ == False:
            #// No libsodium installed
            return False
        # end if
        if self.disableFallbackForUnitTests:
            #// Don't fallback. Use the PHP implementation.
            return False
        # end if
        if (not php_empty(lambda : sodium_func_name_)):
            return php_is_callable("\\Sodium\\" + sodium_func_name_)
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
        
        
        res_ = None
        if res_ == None:
            res_ = PHP_VERSION_ID >= 70000 and php_extension_loaded("sodium")
        # end if
        if self.disableFallbackForUnitTests:
            #// Don't fallback. Use the PHP implementation.
            return False
        # end if
        return php_bool(res_)
    # end def usenewsodiumapi
# end class ParagonIE_Sodium_Compat
