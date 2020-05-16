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
if php_class_exists("ParagonIE_Sodium_File", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_File
#//
class ParagonIE_Sodium_File(ParagonIE_Sodium_Core_Util):
    BUFFER_SIZE = 8192
    #// 
    #// Box a file (rather than a string). Uses less memory than
    #// ParagonIE_Sodium_Compat::crypto_box(), but produces
    #// the same result.
    #// 
    #// @param string $inputFile  Absolute path to a file on the filesystem
    #// @param string $outputFile Absolute path to a file on the filesystem
    #// @param string $nonce      Number to be used only once
    #// @param string $keyPair    ECDH secret key and ECDH public key concatenated
    #// 
    #// @return bool
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def box(self, inputFile=None, outputFile=None, nonce=None, keyPair=None):
        
        #// Type checks:
        if (not php_is_string(inputFile)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be a string, " + gettype(inputFile) + " given."))
        # end if
        if (not php_is_string(outputFile)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 2 must be a string, " + gettype(outputFile) + " given."))
        # end if
        if (not php_is_string(nonce)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 3 must be a string, " + gettype(nonce) + " given."))
        # end if
        #// Input validation:
        if (not php_is_string(keyPair)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 4 must be a string, " + gettype(keyPair) + " given."))
        # end if
        if self.strlen(nonce) != ParagonIE_Sodium_Compat.CRYPTO_BOX_NONCEBYTES:
            raise php_new_class("TypeError", lambda : TypeError("Argument 3 must be CRYPTO_BOX_NONCEBYTES bytes"))
        # end if
        if self.strlen(keyPair) != ParagonIE_Sodium_Compat.CRYPTO_BOX_KEYPAIRBYTES:
            raise php_new_class("TypeError", lambda : TypeError("Argument 4 must be CRYPTO_BOX_KEYPAIRBYTES bytes"))
        # end if
        #// @var int $size
        size = filesize(inputFile)
        if (not php_is_int(size)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not obtain the file size"))
        # end if
        #// @var resource $ifp
        ifp = fopen(inputFile, "rb")
        if (not is_resource(ifp)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not open input file for reading"))
        # end if
        #// @var resource $ofp
        ofp = fopen(outputFile, "wb")
        if (not is_resource(ofp)):
            php_fclose(ifp)
            raise php_new_class("SodiumException", lambda : SodiumException("Could not open output file for writing"))
        # end if
        res = self.box_encrypt(ifp, ofp, size, nonce, keyPair)
        php_fclose(ifp)
        php_fclose(ofp)
        return res
    # end def box
    #// 
    #// Open a boxed file (rather than a string). Uses less memory than
    #// ParagonIE_Sodium_Compat::crypto_box_open(), but produces
    #// the same result.
    #// 
    #// Warning: Does not protect against TOCTOU attacks. You should
    #// just load the file into memory and use crypto_box_open() if
    #// you are worried about those.
    #// 
    #// @param string $inputFile
    #// @param string $outputFile
    #// @param string $nonce
    #// @param string $keypair
    #// @return bool
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def box_open(self, inputFile=None, outputFile=None, nonce=None, keypair=None):
        
        #// Type checks:
        if (not php_is_string(inputFile)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be a string, " + gettype(inputFile) + " given."))
        # end if
        if (not php_is_string(outputFile)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 2 must be a string, " + gettype(outputFile) + " given."))
        # end if
        if (not php_is_string(nonce)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 3 must be a string, " + gettype(nonce) + " given."))
        # end if
        if (not php_is_string(keypair)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 4 must be a string, " + gettype(keypair) + " given."))
        # end if
        #// Input validation:
        if self.strlen(nonce) != ParagonIE_Sodium_Compat.CRYPTO_BOX_NONCEBYTES:
            raise php_new_class("TypeError", lambda : TypeError("Argument 4 must be CRYPTO_BOX_NONCEBYTES bytes"))
        # end if
        if self.strlen(keypair) != ParagonIE_Sodium_Compat.CRYPTO_BOX_KEYPAIRBYTES:
            raise php_new_class("TypeError", lambda : TypeError("Argument 4 must be CRYPTO_BOX_KEYPAIRBYTES bytes"))
        # end if
        #// @var int $size
        size = filesize(inputFile)
        if (not php_is_int(size)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not obtain the file size"))
        # end if
        #// @var resource $ifp
        ifp = fopen(inputFile, "rb")
        if (not is_resource(ifp)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not open input file for reading"))
        # end if
        #// @var resource $ofp
        ofp = fopen(outputFile, "wb")
        if (not is_resource(ofp)):
            php_fclose(ifp)
            raise php_new_class("SodiumException", lambda : SodiumException("Could not open output file for writing"))
        # end if
        res = self.box_decrypt(ifp, ofp, size, nonce, keypair)
        php_fclose(ifp)
        php_fclose(ofp)
        try: 
            ParagonIE_Sodium_Compat.memzero(nonce)
            ParagonIE_Sodium_Compat.memzero(ephKeypair)
        except SodiumException as ex:
            ephKeypair = None
        # end try
        return res
    # end def box_open
    #// 
    #// Seal a file (rather than a string). Uses less memory than
    #// ParagonIE_Sodium_Compat::crypto_box_seal(), but produces
    #// the same result.
    #// 
    #// @param string $inputFile  Absolute path to a file on the filesystem
    #// @param string $outputFile Absolute path to a file on the filesystem
    #// @param string $publicKey  ECDH public key
    #// 
    #// @return bool
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def box_seal(self, inputFile=None, outputFile=None, publicKey=None):
        
        #// Type checks:
        if (not php_is_string(inputFile)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be a string, " + gettype(inputFile) + " given."))
        # end if
        if (not php_is_string(outputFile)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 2 must be a string, " + gettype(outputFile) + " given."))
        # end if
        if (not php_is_string(publicKey)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 3 must be a string, " + gettype(publicKey) + " given."))
        # end if
        #// Input validation:
        if self.strlen(publicKey) != ParagonIE_Sodium_Compat.CRYPTO_BOX_PUBLICKEYBYTES:
            raise php_new_class("TypeError", lambda : TypeError("Argument 3 must be CRYPTO_BOX_PUBLICKEYBYTES bytes"))
        # end if
        #// @var int $size
        size = filesize(inputFile)
        if (not php_is_int(size)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not obtain the file size"))
        # end if
        #// @var resource $ifp
        ifp = fopen(inputFile, "rb")
        if (not is_resource(ifp)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not open input file for reading"))
        # end if
        #// @var resource $ofp
        ofp = fopen(outputFile, "wb")
        if (not is_resource(ofp)):
            php_fclose(ifp)
            raise php_new_class("SodiumException", lambda : SodiumException("Could not open output file for writing"))
        # end if
        #// @var string $ephKeypair
        ephKeypair = ParagonIE_Sodium_Compat.crypto_box_keypair()
        #// @var string $msgKeypair
        msgKeypair = ParagonIE_Sodium_Compat.crypto_box_keypair_from_secretkey_and_publickey(ParagonIE_Sodium_Compat.crypto_box_secretkey(ephKeypair), publicKey)
        #// @var string $ephemeralPK
        ephemeralPK = ParagonIE_Sodium_Compat.crypto_box_publickey(ephKeypair)
        #// @var string $nonce
        nonce = ParagonIE_Sodium_Compat.crypto_generichash(ephemeralPK + publicKey, "", 24)
        #// @var int $firstWrite
        firstWrite = fwrite(ofp, ephemeralPK, ParagonIE_Sodium_Compat.CRYPTO_BOX_PUBLICKEYBYTES)
        if (not php_is_int(firstWrite)):
            php_fclose(ifp)
            php_fclose(ofp)
            ParagonIE_Sodium_Compat.memzero(ephKeypair)
            raise php_new_class("SodiumException", lambda : SodiumException("Could not write to output file"))
        # end if
        if firstWrite != ParagonIE_Sodium_Compat.CRYPTO_BOX_PUBLICKEYBYTES:
            ParagonIE_Sodium_Compat.memzero(ephKeypair)
            php_fclose(ifp)
            php_fclose(ofp)
            raise php_new_class("SodiumException", lambda : SodiumException("Error writing public key to output file"))
        # end if
        res = self.box_encrypt(ifp, ofp, size, nonce, msgKeypair)
        php_fclose(ifp)
        php_fclose(ofp)
        try: 
            ParagonIE_Sodium_Compat.memzero(nonce)
            ParagonIE_Sodium_Compat.memzero(ephKeypair)
        except SodiumException as ex:
            ephKeypair = None
        # end try
        return res
    # end def box_seal
    #// 
    #// Open a sealed file (rather than a string). Uses less memory than
    #// ParagonIE_Sodium_Compat::crypto_box_seal_open(), but produces
    #// the same result.
    #// 
    #// Warning: Does not protect against TOCTOU attacks. You should
    #// just load the file into memory and use crypto_box_seal_open() if
    #// you are worried about those.
    #// 
    #// @param string $inputFile
    #// @param string $outputFile
    #// @param string $ecdhKeypair
    #// @return bool
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def box_seal_open(self, inputFile=None, outputFile=None, ecdhKeypair=None):
        
        #// Type checks:
        if (not php_is_string(inputFile)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be a string, " + gettype(inputFile) + " given."))
        # end if
        if (not php_is_string(outputFile)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 2 must be a string, " + gettype(outputFile) + " given."))
        # end if
        if (not php_is_string(ecdhKeypair)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 3 must be a string, " + gettype(ecdhKeypair) + " given."))
        # end if
        #// Input validation:
        if self.strlen(ecdhKeypair) != ParagonIE_Sodium_Compat.CRYPTO_BOX_KEYPAIRBYTES:
            raise php_new_class("TypeError", lambda : TypeError("Argument 3 must be CRYPTO_BOX_KEYPAIRBYTES bytes"))
        # end if
        publicKey = ParagonIE_Sodium_Compat.crypto_box_publickey(ecdhKeypair)
        #// @var int $size
        size = filesize(inputFile)
        if (not php_is_int(size)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not obtain the file size"))
        # end if
        #// @var resource $ifp
        ifp = fopen(inputFile, "rb")
        if (not is_resource(ifp)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not open input file for reading"))
        # end if
        #// @var resource $ofp
        ofp = fopen(outputFile, "wb")
        if (not is_resource(ofp)):
            php_fclose(ifp)
            raise php_new_class("SodiumException", lambda : SodiumException("Could not open output file for writing"))
        # end if
        ephemeralPK = fread(ifp, ParagonIE_Sodium_Compat.CRYPTO_BOX_PUBLICKEYBYTES)
        if (not php_is_string(ephemeralPK)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not read input file"))
        # end if
        if self.strlen(ephemeralPK) != ParagonIE_Sodium_Compat.CRYPTO_BOX_PUBLICKEYBYTES:
            php_fclose(ifp)
            php_fclose(ofp)
            raise php_new_class("SodiumException", lambda : SodiumException("Could not read public key from sealed file"))
        # end if
        nonce = ParagonIE_Sodium_Compat.crypto_generichash(ephemeralPK + publicKey, "", 24)
        msgKeypair = ParagonIE_Sodium_Compat.crypto_box_keypair_from_secretkey_and_publickey(ParagonIE_Sodium_Compat.crypto_box_secretkey(ecdhKeypair), ephemeralPK)
        res = self.box_decrypt(ifp, ofp, size, nonce, msgKeypair)
        php_fclose(ifp)
        php_fclose(ofp)
        try: 
            ParagonIE_Sodium_Compat.memzero(nonce)
            ParagonIE_Sodium_Compat.memzero(ephKeypair)
        except SodiumException as ex:
            ephKeypair = None
        # end try
        return res
    # end def box_seal_open
    #// 
    #// Calculate the BLAKE2b hash of a file.
    #// 
    #// @param string      $filePath     Absolute path to a file on the filesystem
    #// @param string|null $key          BLAKE2b key
    #// @param int         $outputLength Length of hash output
    #// 
    #// @return string                   BLAKE2b hash
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress FailedTypeResolution
    #//
    @classmethod
    def generichash(self, filePath=None, key="", outputLength=32):
        
        #// Type checks:
        if (not php_is_string(filePath)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be a string, " + gettype(filePath) + " given."))
        # end if
        if (not php_is_string(key)):
            if is_null(key):
                key = ""
            else:
                raise php_new_class("TypeError", lambda : TypeError("Argument 2 must be a string, " + gettype(key) + " given."))
            # end if
        # end if
        if (not php_is_int(outputLength)):
            if (not php_is_numeric(outputLength)):
                raise php_new_class("TypeError", lambda : TypeError("Argument 3 must be an integer, " + gettype(outputLength) + " given."))
            # end if
            outputLength = php_int(outputLength)
        # end if
        #// Input validation:
        if (not php_empty(lambda : key)):
            if self.strlen(key) < ParagonIE_Sodium_Compat.CRYPTO_GENERICHASH_KEYBYTES_MIN:
                raise php_new_class("TypeError", lambda : TypeError("Argument 2 must be at least CRYPTO_GENERICHASH_KEYBYTES_MIN bytes"))
            # end if
            if self.strlen(key) > ParagonIE_Sodium_Compat.CRYPTO_GENERICHASH_KEYBYTES_MAX:
                raise php_new_class("TypeError", lambda : TypeError("Argument 2 must be at most CRYPTO_GENERICHASH_KEYBYTES_MAX bytes"))
            # end if
        # end if
        if outputLength < ParagonIE_Sodium_Compat.CRYPTO_GENERICHASH_BYTES_MIN:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 3 must be at least CRYPTO_GENERICHASH_BYTES_MIN"))
        # end if
        if outputLength > ParagonIE_Sodium_Compat.CRYPTO_GENERICHASH_BYTES_MAX:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 3 must be at least CRYPTO_GENERICHASH_BYTES_MAX"))
        # end if
        #// @var int $size
        size = filesize(filePath)
        if (not php_is_int(size)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not obtain the file size"))
        # end if
        #// @var resource $fp
        fp = fopen(filePath, "rb")
        if (not is_resource(fp)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not open input file for reading"))
        # end if
        ctx = ParagonIE_Sodium_Compat.crypto_generichash_init(key, outputLength)
        while True:
            
            if not (size > 0):
                break
            # end if
            blockSize = 64 if size > 64 else size
            read = fread(fp, blockSize)
            if (not php_is_string(read)):
                raise php_new_class("SodiumException", lambda : SodiumException("Could not read input file"))
            # end if
            ParagonIE_Sodium_Compat.crypto_generichash_update(ctx, read)
            size -= blockSize
        # end while
        php_fclose(fp)
        return ParagonIE_Sodium_Compat.crypto_generichash_final(ctx, outputLength)
    # end def generichash
    #// 
    #// Encrypt a file (rather than a string). Uses less memory than
    #// ParagonIE_Sodium_Compat::crypto_secretbox(), but produces
    #// the same result.
    #// 
    #// @param string $inputFile  Absolute path to a file on the filesystem
    #// @param string $outputFile Absolute path to a file on the filesystem
    #// @param string $nonce      Number to be used only once
    #// @param string $key        Encryption key
    #// 
    #// @return bool
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def secretbox(self, inputFile=None, outputFile=None, nonce=None, key=None):
        
        #// Type checks:
        if (not php_is_string(inputFile)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be a string, " + gettype(inputFile) + " given.."))
        # end if
        if (not php_is_string(outputFile)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 2 must be a string, " + gettype(outputFile) + " given."))
        # end if
        if (not php_is_string(nonce)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 3 must be a string, " + gettype(nonce) + " given."))
        # end if
        #// Input validation:
        if self.strlen(nonce) != ParagonIE_Sodium_Compat.CRYPTO_SECRETBOX_NONCEBYTES:
            raise php_new_class("TypeError", lambda : TypeError("Argument 3 must be CRYPTO_SECRETBOX_NONCEBYTES bytes"))
        # end if
        if (not php_is_string(key)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 4 must be a string, " + gettype(key) + " given."))
        # end if
        if self.strlen(key) != ParagonIE_Sodium_Compat.CRYPTO_SECRETBOX_KEYBYTES:
            raise php_new_class("TypeError", lambda : TypeError("Argument 4 must be CRYPTO_SECRETBOX_KEYBYTES bytes"))
        # end if
        #// @var int $size
        size = filesize(inputFile)
        if (not php_is_int(size)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not obtain the file size"))
        # end if
        #// @var resource $ifp
        ifp = fopen(inputFile, "rb")
        if (not is_resource(ifp)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not open input file for reading"))
        # end if
        #// @var resource $ofp
        ofp = fopen(outputFile, "wb")
        if (not is_resource(ofp)):
            php_fclose(ifp)
            raise php_new_class("SodiumException", lambda : SodiumException("Could not open output file for writing"))
        # end if
        res = self.secretbox_encrypt(ifp, ofp, size, nonce, key)
        php_fclose(ifp)
        php_fclose(ofp)
        return res
    # end def secretbox
    #// 
    #// Seal a file (rather than a string). Uses less memory than
    #// ParagonIE_Sodium_Compat::crypto_secretbox_open(), but produces
    #// the same result.
    #// 
    #// Warning: Does not protect against TOCTOU attacks. You should
    #// just load the file into memory and use crypto_secretbox_open() if
    #// you are worried about those.
    #// 
    #// @param string $inputFile
    #// @param string $outputFile
    #// @param string $nonce
    #// @param string $key
    #// @return bool
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def secretbox_open(self, inputFile=None, outputFile=None, nonce=None, key=None):
        
        #// Type checks:
        if (not php_is_string(inputFile)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be a string, " + gettype(inputFile) + " given."))
        # end if
        if (not php_is_string(outputFile)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 2 must be a string, " + gettype(outputFile) + " given."))
        # end if
        if (not php_is_string(nonce)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 3 must be a string, " + gettype(nonce) + " given."))
        # end if
        if (not php_is_string(key)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 4 must be a string, " + gettype(key) + " given."))
        # end if
        #// Input validation:
        if self.strlen(nonce) != ParagonIE_Sodium_Compat.CRYPTO_SECRETBOX_NONCEBYTES:
            raise php_new_class("TypeError", lambda : TypeError("Argument 4 must be CRYPTO_SECRETBOX_NONCEBYTES bytes"))
        # end if
        if self.strlen(key) != ParagonIE_Sodium_Compat.CRYPTO_SECRETBOX_KEYBYTES:
            raise php_new_class("TypeError", lambda : TypeError("Argument 4 must be CRYPTO_SECRETBOXBOX_KEYBYTES bytes"))
        # end if
        #// @var int $size
        size = filesize(inputFile)
        if (not php_is_int(size)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not obtain the file size"))
        # end if
        #// @var resource $ifp
        ifp = fopen(inputFile, "rb")
        if (not is_resource(ifp)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not open input file for reading"))
        # end if
        #// @var resource $ofp
        ofp = fopen(outputFile, "wb")
        if (not is_resource(ofp)):
            php_fclose(ifp)
            raise php_new_class("SodiumException", lambda : SodiumException("Could not open output file for writing"))
        # end if
        res = self.secretbox_decrypt(ifp, ofp, size, nonce, key)
        php_fclose(ifp)
        php_fclose(ofp)
        try: 
            ParagonIE_Sodium_Compat.memzero(key)
        except SodiumException as ex:
            key = None
        # end try
        return res
    # end def secretbox_open
    #// 
    #// Sign a file (rather than a string). Uses less memory than
    #// ParagonIE_Sodium_Compat::crypto_sign_detached(), but produces
    #// the same result.
    #// 
    #// @param string $filePath  Absolute path to a file on the filesystem
    #// @param string $secretKey Secret signing key
    #// 
    #// @return string           Ed25519 signature
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def sign(self, filePath=None, secretKey=None):
        
        #// Type checks:
        if (not php_is_string(filePath)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be a string, " + gettype(filePath) + " given."))
        # end if
        if (not php_is_string(secretKey)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 2 must be a string, " + gettype(secretKey) + " given."))
        # end if
        #// Input validation:
        if self.strlen(secretKey) != ParagonIE_Sodium_Compat.CRYPTO_SIGN_SECRETKEYBYTES:
            raise php_new_class("TypeError", lambda : TypeError("Argument 2 must be CRYPTO_SIGN_SECRETKEYBYTES bytes"))
        # end if
        if PHP_INT_SIZE == 4:
            return self.sign_core32(filePath, secretKey)
        # end if
        #// @var int $size
        size = filesize(filePath)
        if (not php_is_int(size)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not obtain the file size"))
        # end if
        #// @var resource $fp
        fp = fopen(filePath, "rb")
        if (not is_resource(fp)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not open input file for reading"))
        # end if
        #// @var string $az
        az = hash("sha512", self.substr(secretKey, 0, 32), True)
        az[0] = self.inttochr(self.chrtoint(az[0]) & 248)
        az[31] = self.inttochr(self.chrtoint(az[31]) & 63 | 64)
        hs = hash_init("sha512")
        hash_update(hs, self.substr(az, 32, 32))
        #// @var resource $hs
        hs = self.updatehashwithfile(hs, fp, size)
        #// @var string $nonceHash
        nonceHash = hash_final(hs, True)
        #// @var string $pk
        pk = self.substr(secretKey, 32, 32)
        #// @var string $nonce
        nonce = ParagonIE_Sodium_Core_Ed25519.sc_reduce(nonceHash) + self.substr(nonceHash, 32)
        #// @var string $sig
        sig = ParagonIE_Sodium_Core_Ed25519.ge_p3_tobytes(ParagonIE_Sodium_Core_Ed25519.ge_scalarmult_base(nonce))
        hs = hash_init("sha512")
        hash_update(hs, self.substr(sig, 0, 32))
        hash_update(hs, self.substr(pk, 0, 32))
        #// @var resource $hs
        hs = self.updatehashwithfile(hs, fp, size)
        #// @var string $hramHash
        hramHash = hash_final(hs, True)
        #// @var string $hram
        hram = ParagonIE_Sodium_Core_Ed25519.sc_reduce(hramHash)
        #// @var string $sigAfter
        sigAfter = ParagonIE_Sodium_Core_Ed25519.sc_muladd(hram, az, nonce)
        #// @var string $sig
        sig = self.substr(sig, 0, 32) + self.substr(sigAfter, 0, 32)
        try: 
            ParagonIE_Sodium_Compat.memzero(az)
        except SodiumException as ex:
            az = None
        # end try
        php_fclose(fp)
        return sig
    # end def sign
    #// 
    #// Verify a file (rather than a string). Uses less memory than
    #// ParagonIE_Sodium_Compat::crypto_sign_verify_detached(), but
    #// produces the same result.
    #// 
    #// @param string $sig       Ed25519 signature
    #// @param string $filePath  Absolute path to a file on the filesystem
    #// @param string $publicKey Signing public key
    #// 
    #// @return bool
    #// @throws SodiumException
    #// @throws TypeError
    #// @throws Exception
    #//
    @classmethod
    def verify(self, sig=None, filePath=None, publicKey=None):
        
        #// Type checks:
        if (not php_is_string(sig)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be a string, " + gettype(sig) + " given."))
        # end if
        if (not php_is_string(filePath)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 2 must be a string, " + gettype(filePath) + " given."))
        # end if
        if (not php_is_string(publicKey)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 3 must be a string, " + gettype(publicKey) + " given."))
        # end if
        #// Input validation:
        if self.strlen(sig) != ParagonIE_Sodium_Compat.CRYPTO_SIGN_BYTES:
            raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be CRYPTO_SIGN_BYTES bytes"))
        # end if
        if self.strlen(publicKey) != ParagonIE_Sodium_Compat.CRYPTO_SIGN_PUBLICKEYBYTES:
            raise php_new_class("TypeError", lambda : TypeError("Argument 3 must be CRYPTO_SIGN_PUBLICKEYBYTES bytes"))
        # end if
        if self.strlen(sig) < 64:
            raise php_new_class("SodiumException", lambda : SodiumException("Signature is too short"))
        # end if
        if PHP_INT_SIZE == 4:
            return self.verify_core32(sig, filePath, publicKey)
        # end if
        #// Security checks
        if ParagonIE_Sodium_Core_Ed25519.chrtoint(sig[63]) & 240 and ParagonIE_Sodium_Core_Ed25519.check_s_lt_l(self.substr(sig, 32, 32)):
            raise php_new_class("SodiumException", lambda : SodiumException("S < L - Invalid signature"))
        # end if
        if ParagonIE_Sodium_Core_Ed25519.small_order(sig):
            raise php_new_class("SodiumException", lambda : SodiumException("Signature is on too small of an order"))
        # end if
        if self.chrtoint(sig[63]) & 224 != 0:
            raise php_new_class("SodiumException", lambda : SodiumException("Invalid signature"))
        # end if
        d = 0
        i = 0
        while i < 32:
            
            d |= self.chrtoint(publicKey[i])
            i += 1
        # end while
        if d == 0:
            raise php_new_class("SodiumException", lambda : SodiumException("All zero public key"))
        # end if
        #// @var int $size
        size = filesize(filePath)
        if (not php_is_int(size)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not obtain the file size"))
        # end if
        #// @var resource $fp
        fp = fopen(filePath, "rb")
        if (not is_resource(fp)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not open input file for reading"))
        # end if
        #// @var bool The original value of ParagonIE_Sodium_Compat::$fastMult
        orig = ParagonIE_Sodium_Compat.fastMult
        #// Set ParagonIE_Sodium_Compat::$fastMult to true to speed up verification.
        ParagonIE_Sodium_Compat.fastMult = True
        #// @var ParagonIE_Sodium_Core_Curve25519_Ge_P3 $A
        A = ParagonIE_Sodium_Core_Ed25519.ge_frombytes_negate_vartime(publicKey)
        hs = hash_init("sha512")
        hash_update(hs, self.substr(sig, 0, 32))
        hash_update(hs, self.substr(publicKey, 0, 32))
        #// @var resource $hs
        hs = self.updatehashwithfile(hs, fp, size)
        #// @var string $hDigest
        hDigest = hash_final(hs, True)
        #// @var string $h
        h = ParagonIE_Sodium_Core_Ed25519.sc_reduce(hDigest) + self.substr(hDigest, 32)
        #// @var ParagonIE_Sodium_Core_Curve25519_Ge_P2 $R
        R = ParagonIE_Sodium_Core_Ed25519.ge_double_scalarmult_vartime(h, A, self.substr(sig, 32))
        #// @var string $rcheck
        rcheck = ParagonIE_Sodium_Core_Ed25519.ge_tobytes(R)
        #// Close the file handle
        php_fclose(fp)
        #// Reset ParagonIE_Sodium_Compat::$fastMult to what it was before.
        ParagonIE_Sodium_Compat.fastMult = orig
        return self.verify_32(rcheck, self.substr(sig, 0, 32))
    # end def verify
    #// 
    #// @param resource $ifp
    #// @param resource $ofp
    #// @param int      $mlen
    #// @param string   $nonce
    #// @param string   $boxKeypair
    #// @return bool
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def box_encrypt(self, ifp=None, ofp=None, mlen=None, nonce=None, boxKeypair=None):
        
        if PHP_INT_SIZE == 4:
            return self.secretbox_encrypt(ifp, ofp, mlen, nonce, ParagonIE_Sodium_Crypto32.box_beforenm(ParagonIE_Sodium_Crypto32.box_secretkey(boxKeypair), ParagonIE_Sodium_Crypto32.box_publickey(boxKeypair)))
        # end if
        return self.secretbox_encrypt(ifp, ofp, mlen, nonce, ParagonIE_Sodium_Crypto.box_beforenm(ParagonIE_Sodium_Crypto.box_secretkey(boxKeypair), ParagonIE_Sodium_Crypto.box_publickey(boxKeypair)))
    # end def box_encrypt
    #// 
    #// @param resource $ifp
    #// @param resource $ofp
    #// @param int      $mlen
    #// @param string   $nonce
    #// @param string   $boxKeypair
    #// @return bool
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def box_decrypt(self, ifp=None, ofp=None, mlen=None, nonce=None, boxKeypair=None):
        
        if PHP_INT_SIZE == 4:
            return self.secretbox_decrypt(ifp, ofp, mlen, nonce, ParagonIE_Sodium_Crypto32.box_beforenm(ParagonIE_Sodium_Crypto32.box_secretkey(boxKeypair), ParagonIE_Sodium_Crypto32.box_publickey(boxKeypair)))
        # end if
        return self.secretbox_decrypt(ifp, ofp, mlen, nonce, ParagonIE_Sodium_Crypto.box_beforenm(ParagonIE_Sodium_Crypto.box_secretkey(boxKeypair), ParagonIE_Sodium_Crypto.box_publickey(boxKeypair)))
    # end def box_decrypt
    #// 
    #// Encrypt a file
    #// 
    #// @param resource $ifp
    #// @param resource $ofp
    #// @param int $mlen
    #// @param string $nonce
    #// @param string $key
    #// @return bool
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def secretbox_encrypt(self, ifp=None, ofp=None, mlen=None, nonce=None, key=None):
        
        if PHP_INT_SIZE == 4:
            return self.secretbox_encrypt_core32(ifp, ofp, mlen, nonce, key)
        # end if
        plaintext = fread(ifp, 32)
        if (not php_is_string(plaintext)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not read input file"))
        # end if
        first32 = self.ftell(ifp)
        #// @var string $subkey
        subkey = ParagonIE_Sodium_Core_HSalsa20.hsalsa20(nonce, key)
        #// @var string $realNonce
        realNonce = ParagonIE_Sodium_Core_Util.substr(nonce, 16, 8)
        #// @var string $block0
        block0 = php_str_repeat(" ", 32)
        #// @var int $mlen - Length of the plaintext message
        mlen0 = mlen
        if mlen0 > 64 - ParagonIE_Sodium_Crypto.secretbox_xsalsa20poly1305_ZEROBYTES:
            mlen0 = 64 - ParagonIE_Sodium_Crypto.secretbox_xsalsa20poly1305_ZEROBYTES
        # end if
        block0 += ParagonIE_Sodium_Core_Util.substr(plaintext, 0, mlen0)
        #// @var string $block0
        block0 = ParagonIE_Sodium_Core_Salsa20.salsa20_xor(block0, realNonce, subkey)
        state = php_new_class("ParagonIE_Sodium_Core_Poly1305_State", lambda : ParagonIE_Sodium_Core_Poly1305_State(ParagonIE_Sodium_Core_Util.substr(block0, 0, ParagonIE_Sodium_Crypto.onetimeauth_poly1305_KEYBYTES)))
        #// Pre-write 16 blank bytes for the Poly1305 tag
        start = self.ftell(ofp)
        fwrite(ofp, php_str_repeat(" ", 16))
        #// @var string $c
        cBlock = ParagonIE_Sodium_Core_Util.substr(block0, ParagonIE_Sodium_Crypto.secretbox_xsalsa20poly1305_ZEROBYTES)
        state.update(cBlock)
        fwrite(ofp, cBlock)
        mlen -= 32
        #// @var int $iter
        iter = 1
        #// @var int $incr
        incr = self.BUFFER_SIZE >> 6
        #// 
        #// Set the cursor to the end of the first half-block. All future bytes will
        #// generated from salsa20_xor_ic, starting from 1 (second block).
        #//
        fseek(ifp, first32, SEEK_SET)
        while True:
            
            if not (mlen > 0):
                break
            # end if
            blockSize = self.BUFFER_SIZE if mlen > self.BUFFER_SIZE else mlen
            plaintext = fread(ifp, blockSize)
            if (not php_is_string(plaintext)):
                raise php_new_class("SodiumException", lambda : SodiumException("Could not read input file"))
            # end if
            cBlock = ParagonIE_Sodium_Core_Salsa20.salsa20_xor_ic(plaintext, realNonce, iter, subkey)
            fwrite(ofp, cBlock, blockSize)
            state.update(cBlock)
            mlen -= blockSize
            iter += incr
        # end while
        try: 
            ParagonIE_Sodium_Compat.memzero(block0)
            ParagonIE_Sodium_Compat.memzero(subkey)
        except SodiumException as ex:
            block0 = None
            subkey = None
        # end try
        end_ = self.ftell(ofp)
        #// 
        #// Write the Poly1305 authentication tag that provides integrity
        #// over the ciphertext (encrypt-then-MAC)
        #//
        fseek(ofp, start, SEEK_SET)
        fwrite(ofp, state.finish(), ParagonIE_Sodium_Compat.CRYPTO_SECRETBOX_MACBYTES)
        fseek(ofp, end_, SEEK_SET)
        state = None
        return True
    # end def secretbox_encrypt
    #// 
    #// Decrypt a file
    #// 
    #// @param resource $ifp
    #// @param resource $ofp
    #// @param int $mlen
    #// @param string $nonce
    #// @param string $key
    #// @return bool
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def secretbox_decrypt(self, ifp=None, ofp=None, mlen=None, nonce=None, key=None):
        
        if PHP_INT_SIZE == 4:
            return self.secretbox_decrypt_core32(ifp, ofp, mlen, nonce, key)
        # end if
        tag = fread(ifp, 16)
        if (not php_is_string(tag)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not read input file"))
        # end if
        #// @var string $subkey
        subkey = ParagonIE_Sodium_Core_HSalsa20.hsalsa20(nonce, key)
        #// @var string $realNonce
        realNonce = ParagonIE_Sodium_Core_Util.substr(nonce, 16, 8)
        #// @var string $block0
        block0 = ParagonIE_Sodium_Core_Salsa20.salsa20(64, ParagonIE_Sodium_Core_Util.substr(nonce, 16, 8), subkey)
        #// Verify the Poly1305 MAC -before- attempting to decrypt!
        state = php_new_class("ParagonIE_Sodium_Core_Poly1305_State", lambda : ParagonIE_Sodium_Core_Poly1305_State(self.substr(block0, 0, 32)))
        if (not self.onetimeauth_verify(state, ifp, tag, mlen)):
            raise php_new_class("SodiumException", lambda : SodiumException("Invalid MAC"))
        # end if
        #// 
        #// Set the cursor to the end of the first half-block. All future bytes will
        #// generated from salsa20_xor_ic, starting from 1 (second block).
        #//
        first32 = fread(ifp, 32)
        if (not php_is_string(first32)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not read input file"))
        # end if
        first32len = self.strlen(first32)
        fwrite(ofp, self.xorstrings(self.substr(block0, 32, first32len), self.substr(first32, 0, first32len)))
        mlen -= 32
        #// @var int $iter
        iter = 1
        #// @var int $incr
        incr = self.BUFFER_SIZE >> 6
        #// Decrypts ciphertext, writes to output file.
        while True:
            
            if not (mlen > 0):
                break
            # end if
            blockSize = self.BUFFER_SIZE if mlen > self.BUFFER_SIZE else mlen
            ciphertext = fread(ifp, blockSize)
            if (not php_is_string(ciphertext)):
                raise php_new_class("SodiumException", lambda : SodiumException("Could not read input file"))
            # end if
            pBlock = ParagonIE_Sodium_Core_Salsa20.salsa20_xor_ic(ciphertext, realNonce, iter, subkey)
            fwrite(ofp, pBlock, blockSize)
            mlen -= blockSize
            iter += incr
        # end while
        return True
    # end def secretbox_decrypt
    #// 
    #// @param ParagonIE_Sodium_Core_Poly1305_State $state
    #// @param resource $ifp
    #// @param string $tag
    #// @param int $mlen
    #// @return bool
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def onetimeauth_verify(self, state=None, ifp=None, tag="", mlen=0):
        
        #// @var int $pos
        pos = self.ftell(ifp)
        #// @var int $iter
        iter = 1
        #// @var int $incr
        incr = self.BUFFER_SIZE >> 6
        while True:
            
            if not (mlen > 0):
                break
            # end if
            blockSize = self.BUFFER_SIZE if mlen > self.BUFFER_SIZE else mlen
            ciphertext = fread(ifp, blockSize)
            if (not php_is_string(ciphertext)):
                raise php_new_class("SodiumException", lambda : SodiumException("Could not read input file"))
            # end if
            state.update(ciphertext)
            mlen -= blockSize
            iter += incr
        # end while
        res = ParagonIE_Sodium_Core_Util.verify_16(tag, state.finish())
        fseek(ifp, pos, SEEK_SET)
        return res
    # end def onetimeauth_verify
    #// 
    #// Update a hash context with the contents of a file, without
    #// loading the entire file into memory.
    #// 
    #// @param resource|object $hash
    #// @param resource $fp
    #// @param int $size
    #// @return resource|object Resource on PHP < 7.2, HashContext object on PHP >= 7.2
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress PossiblyInvalidArgument
    #// PHP 7.2 changes from a resource to an object,
    #// which causes Psalm to complain about an error.
    #// @psalm-suppress TypeCoercion
    #// Ditto.
    #//
    @classmethod
    def updatehashwithfile(self, hash=None, fp=None, size=0):
        
        #// Type checks:
        if PHP_VERSION_ID < 70200:
            if (not is_resource(hash)):
                raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be a resource, " + gettype(hash) + " given."))
            # end if
        else:
            if (not php_is_object(hash)):
                raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be an object (PHP 7.2+), " + gettype(hash) + " given."))
            # end if
        # end if
        if (not is_resource(fp)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 2 must be a resource, " + gettype(fp) + " given."))
        # end if
        if (not php_is_int(size)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 3 must be an integer, " + gettype(size) + " given."))
        # end if
        #// @var int $originalPosition
        originalPosition = self.ftell(fp)
        #// Move file pointer to beginning of file
        fseek(fp, 0, SEEK_SET)
        i = 0
        while i < size:
            
            #// @var string|bool $message
            message = fread(fp, size - i if size - i > self.BUFFER_SIZE else self.BUFFER_SIZE)
            if (not php_is_string(message)):
                raise php_new_class("SodiumException", lambda : SodiumException("Unexpected error reading from file."))
            # end if
            #// @var string $message
            #// @psalm-suppress InvalidArgument
            hash_update(hash, message)
            i += self.BUFFER_SIZE
        # end while
        #// Reset file pointer's position
        fseek(fp, originalPosition, SEEK_SET)
        return hash
    # end def updatehashwithfile
    #// 
    #// Sign a file (rather than a string). Uses less memory than
    #// ParagonIE_Sodium_Compat::crypto_sign_detached(), but produces
    #// the same result. (32-bit)
    #// 
    #// @param string $filePath  Absolute path to a file on the filesystem
    #// @param string $secretKey Secret signing key
    #// 
    #// @return string           Ed25519 signature
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def sign_core32(self, filePath=None, secretKey=None):
        
        #// @var int|bool $size
        size = filesize(filePath)
        if (not php_is_int(size)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not obtain the file size"))
        # end if
        #// @var int $size
        #// @var resource|bool $fp
        fp = fopen(filePath, "rb")
        if (not is_resource(fp)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not open input file for reading"))
        # end if
        #// @var resource $fp
        #// @var string $az
        az = hash("sha512", self.substr(secretKey, 0, 32), True)
        az[0] = self.inttochr(self.chrtoint(az[0]) & 248)
        az[31] = self.inttochr(self.chrtoint(az[31]) & 63 | 64)
        hs = hash_init("sha512")
        hash_update(hs, self.substr(az, 32, 32))
        #// @var resource $hs
        hs = self.updatehashwithfile(hs, fp, size)
        #// @var string $nonceHash
        nonceHash = hash_final(hs, True)
        #// @var string $pk
        pk = self.substr(secretKey, 32, 32)
        #// @var string $nonce
        nonce = ParagonIE_Sodium_Core32_Ed25519.sc_reduce(nonceHash) + self.substr(nonceHash, 32)
        #// @var string $sig
        sig = ParagonIE_Sodium_Core32_Ed25519.ge_p3_tobytes(ParagonIE_Sodium_Core32_Ed25519.ge_scalarmult_base(nonce))
        hs = hash_init("sha512")
        hash_update(hs, self.substr(sig, 0, 32))
        hash_update(hs, self.substr(pk, 0, 32))
        #// @var resource $hs
        hs = self.updatehashwithfile(hs, fp, size)
        #// @var string $hramHash
        hramHash = hash_final(hs, True)
        #// @var string $hram
        hram = ParagonIE_Sodium_Core32_Ed25519.sc_reduce(hramHash)
        #// @var string $sigAfter
        sigAfter = ParagonIE_Sodium_Core32_Ed25519.sc_muladd(hram, az, nonce)
        #// @var string $sig
        sig = self.substr(sig, 0, 32) + self.substr(sigAfter, 0, 32)
        try: 
            ParagonIE_Sodium_Compat.memzero(az)
        except SodiumException as ex:
            az = None
        # end try
        php_fclose(fp)
        return sig
    # end def sign_core32
    #// 
    #// 
    #// Verify a file (rather than a string). Uses less memory than
    #// ParagonIE_Sodium_Compat::crypto_sign_verify_detached(), but
    #// produces the same result. (32-bit)
    #// 
    #// @param string $sig       Ed25519 signature
    #// @param string $filePath  Absolute path to a file on the filesystem
    #// @param string $publicKey Signing public key
    #// 
    #// @return bool
    #// @throws SodiumException
    #// @throws Exception
    #//
    @classmethod
    def verify_core32(self, sig=None, filePath=None, publicKey=None):
        
        #// Security checks
        if ParagonIE_Sodium_Core32_Ed25519.check_s_lt_l(self.substr(sig, 32, 32)):
            raise php_new_class("SodiumException", lambda : SodiumException("S < L - Invalid signature"))
        # end if
        if ParagonIE_Sodium_Core32_Ed25519.small_order(sig):
            raise php_new_class("SodiumException", lambda : SodiumException("Signature is on too small of an order"))
        # end if
        if self.chrtoint(sig[63]) & 224 != 0:
            raise php_new_class("SodiumException", lambda : SodiumException("Invalid signature"))
        # end if
        d = 0
        i = 0
        while i < 32:
            
            d |= self.chrtoint(publicKey[i])
            i += 1
        # end while
        if d == 0:
            raise php_new_class("SodiumException", lambda : SodiumException("All zero public key"))
        # end if
        #// @var int|bool $size
        size = filesize(filePath)
        if (not php_is_int(size)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not obtain the file size"))
        # end if
        #// @var int $size
        #// @var resource|bool $fp
        fp = fopen(filePath, "rb")
        if (not is_resource(fp)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not open input file for reading"))
        # end if
        #// @var resource $fp
        #// @var bool The original value of ParagonIE_Sodium_Compat::$fastMult
        orig = ParagonIE_Sodium_Compat.fastMult
        #// Set ParagonIE_Sodium_Compat::$fastMult to true to speed up verification.
        ParagonIE_Sodium_Compat.fastMult = True
        #// @var ParagonIE_Sodium_Core32_Curve25519_Ge_P3 $A
        A = ParagonIE_Sodium_Core32_Ed25519.ge_frombytes_negate_vartime(publicKey)
        hs = hash_init("sha512")
        hash_update(hs, self.substr(sig, 0, 32))
        hash_update(hs, self.substr(publicKey, 0, 32))
        #// @var resource $hs
        hs = self.updatehashwithfile(hs, fp, size)
        #// @var string $hDigest
        hDigest = hash_final(hs, True)
        #// @var string $h
        h = ParagonIE_Sodium_Core32_Ed25519.sc_reduce(hDigest) + self.substr(hDigest, 32)
        #// @var ParagonIE_Sodium_Core32_Curve25519_Ge_P2 $R
        R = ParagonIE_Sodium_Core32_Ed25519.ge_double_scalarmult_vartime(h, A, self.substr(sig, 32))
        #// @var string $rcheck
        rcheck = ParagonIE_Sodium_Core32_Ed25519.ge_tobytes(R)
        #// Close the file handle
        php_fclose(fp)
        #// Reset ParagonIE_Sodium_Compat::$fastMult to what it was before.
        ParagonIE_Sodium_Compat.fastMult = orig
        return self.verify_32(rcheck, self.substr(sig, 0, 32))
    # end def verify_core32
    #// 
    #// Encrypt a file (32-bit)
    #// 
    #// @param resource $ifp
    #// @param resource $ofp
    #// @param int $mlen
    #// @param string $nonce
    #// @param string $key
    #// @return bool
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def secretbox_encrypt_core32(self, ifp=None, ofp=None, mlen=None, nonce=None, key=None):
        
        plaintext = fread(ifp, 32)
        if (not php_is_string(plaintext)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not read input file"))
        # end if
        first32 = self.ftell(ifp)
        #// @var string $subkey
        subkey = ParagonIE_Sodium_Core32_HSalsa20.hsalsa20(nonce, key)
        #// @var string $realNonce
        realNonce = ParagonIE_Sodium_Core32_Util.substr(nonce, 16, 8)
        #// @var string $block0
        block0 = php_str_repeat(" ", 32)
        #// @var int $mlen - Length of the plaintext message
        mlen0 = mlen
        if mlen0 > 64 - ParagonIE_Sodium_Crypto.secretbox_xsalsa20poly1305_ZEROBYTES:
            mlen0 = 64 - ParagonIE_Sodium_Crypto.secretbox_xsalsa20poly1305_ZEROBYTES
        # end if
        block0 += ParagonIE_Sodium_Core32_Util.substr(plaintext, 0, mlen0)
        #// @var string $block0
        block0 = ParagonIE_Sodium_Core32_Salsa20.salsa20_xor(block0, realNonce, subkey)
        state = php_new_class("ParagonIE_Sodium_Core32_Poly1305_State", lambda : ParagonIE_Sodium_Core32_Poly1305_State(ParagonIE_Sodium_Core32_Util.substr(block0, 0, ParagonIE_Sodium_Crypto.onetimeauth_poly1305_KEYBYTES)))
        #// Pre-write 16 blank bytes for the Poly1305 tag
        start = self.ftell(ofp)
        fwrite(ofp, php_str_repeat(" ", 16))
        #// @var string $c
        cBlock = ParagonIE_Sodium_Core32_Util.substr(block0, ParagonIE_Sodium_Crypto.secretbox_xsalsa20poly1305_ZEROBYTES)
        state.update(cBlock)
        fwrite(ofp, cBlock)
        mlen -= 32
        #// @var int $iter
        iter = 1
        #// @var int $incr
        incr = self.BUFFER_SIZE >> 6
        #// 
        #// Set the cursor to the end of the first half-block. All future bytes will
        #// generated from salsa20_xor_ic, starting from 1 (second block).
        #//
        fseek(ifp, first32, SEEK_SET)
        while True:
            
            if not (mlen > 0):
                break
            # end if
            blockSize = self.BUFFER_SIZE if mlen > self.BUFFER_SIZE else mlen
            plaintext = fread(ifp, blockSize)
            if (not php_is_string(plaintext)):
                raise php_new_class("SodiumException", lambda : SodiumException("Could not read input file"))
            # end if
            cBlock = ParagonIE_Sodium_Core32_Salsa20.salsa20_xor_ic(plaintext, realNonce, iter, subkey)
            fwrite(ofp, cBlock, blockSize)
            state.update(cBlock)
            mlen -= blockSize
            iter += incr
        # end while
        try: 
            ParagonIE_Sodium_Compat.memzero(block0)
            ParagonIE_Sodium_Compat.memzero(subkey)
        except SodiumException as ex:
            block0 = None
            subkey = None
        # end try
        end_ = self.ftell(ofp)
        #// 
        #// Write the Poly1305 authentication tag that provides integrity
        #// over the ciphertext (encrypt-then-MAC)
        #//
        fseek(ofp, start, SEEK_SET)
        fwrite(ofp, state.finish(), ParagonIE_Sodium_Compat.CRYPTO_SECRETBOX_MACBYTES)
        fseek(ofp, end_, SEEK_SET)
        state = None
        return True
    # end def secretbox_encrypt_core32
    #// 
    #// Decrypt a file (32-bit)
    #// 
    #// @param resource $ifp
    #// @param resource $ofp
    #// @param int $mlen
    #// @param string $nonce
    #// @param string $key
    #// @return bool
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def secretbox_decrypt_core32(self, ifp=None, ofp=None, mlen=None, nonce=None, key=None):
        
        tag = fread(ifp, 16)
        if (not php_is_string(tag)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not read input file"))
        # end if
        #// @var string $subkey
        subkey = ParagonIE_Sodium_Core32_HSalsa20.hsalsa20(nonce, key)
        #// @var string $realNonce
        realNonce = ParagonIE_Sodium_Core32_Util.substr(nonce, 16, 8)
        #// @var string $block0
        block0 = ParagonIE_Sodium_Core32_Salsa20.salsa20(64, ParagonIE_Sodium_Core32_Util.substr(nonce, 16, 8), subkey)
        #// Verify the Poly1305 MAC -before- attempting to decrypt!
        state = php_new_class("ParagonIE_Sodium_Core32_Poly1305_State", lambda : ParagonIE_Sodium_Core32_Poly1305_State(self.substr(block0, 0, 32)))
        if (not self.onetimeauth_verify_core32(state, ifp, tag, mlen)):
            raise php_new_class("SodiumException", lambda : SodiumException("Invalid MAC"))
        # end if
        #// 
        #// Set the cursor to the end of the first half-block. All future bytes will
        #// generated from salsa20_xor_ic, starting from 1 (second block).
        #//
        first32 = fread(ifp, 32)
        if (not php_is_string(first32)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not read input file"))
        # end if
        first32len = self.strlen(first32)
        fwrite(ofp, self.xorstrings(self.substr(block0, 32, first32len), self.substr(first32, 0, first32len)))
        mlen -= 32
        #// @var int $iter
        iter = 1
        #// @var int $incr
        incr = self.BUFFER_SIZE >> 6
        #// Decrypts ciphertext, writes to output file.
        while True:
            
            if not (mlen > 0):
                break
            # end if
            blockSize = self.BUFFER_SIZE if mlen > self.BUFFER_SIZE else mlen
            ciphertext = fread(ifp, blockSize)
            if (not php_is_string(ciphertext)):
                raise php_new_class("SodiumException", lambda : SodiumException("Could not read input file"))
            # end if
            pBlock = ParagonIE_Sodium_Core32_Salsa20.salsa20_xor_ic(ciphertext, realNonce, iter, subkey)
            fwrite(ofp, pBlock, blockSize)
            mlen -= blockSize
            iter += incr
        # end while
        return True
    # end def secretbox_decrypt_core32
    #// 
    #// One-time message authentication for 32-bit systems
    #// 
    #// @param ParagonIE_Sodium_Core32_Poly1305_State $state
    #// @param resource $ifp
    #// @param string $tag
    #// @param int $mlen
    #// @return bool
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def onetimeauth_verify_core32(self, state=None, ifp=None, tag="", mlen=0):
        
        #// @var int $pos
        pos = self.ftell(ifp)
        #// @var int $iter
        iter = 1
        #// @var int $incr
        incr = self.BUFFER_SIZE >> 6
        while True:
            
            if not (mlen > 0):
                break
            # end if
            blockSize = self.BUFFER_SIZE if mlen > self.BUFFER_SIZE else mlen
            ciphertext = fread(ifp, blockSize)
            if (not php_is_string(ciphertext)):
                raise php_new_class("SodiumException", lambda : SodiumException("Could not read input file"))
            # end if
            state.update(ciphertext)
            mlen -= blockSize
            iter += incr
        # end while
        res = ParagonIE_Sodium_Core32_Util.verify_16(tag, state.finish())
        fseek(ifp, pos, SEEK_SET)
        return res
    # end def onetimeauth_verify_core32
    #// 
    #// @param resource $resource
    #// @return int
    #// @throws SodiumException
    #//
    def ftell(self, resource=None):
        
        return_ = ftell(resource)
        if (not php_is_int(return_)):
            raise php_new_class("SodiumException", lambda : SodiumException("ftell() returned false"))
        # end if
        return php_int(return_)
    # end def ftell
# end class ParagonIE_Sodium_File
