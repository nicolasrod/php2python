#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
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
    def box(self, inputFile_=None, outputFile_=None, nonce_=None, keyPair_=None):
        
        
        #// Type checks:
        if (not php_is_string(inputFile_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be a string, " + gettype(inputFile_) + " given."))
        # end if
        if (not php_is_string(outputFile_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 2 must be a string, " + gettype(outputFile_) + " given."))
        # end if
        if (not php_is_string(nonce_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 3 must be a string, " + gettype(nonce_) + " given."))
        # end if
        #// Input validation:
        if (not php_is_string(keyPair_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 4 must be a string, " + gettype(keyPair_) + " given."))
        # end if
        if self.strlen(nonce_) != ParagonIE_Sodium_Compat.CRYPTO_BOX_NONCEBYTES:
            raise php_new_class("TypeError", lambda : TypeError("Argument 3 must be CRYPTO_BOX_NONCEBYTES bytes"))
        # end if
        if self.strlen(keyPair_) != ParagonIE_Sodium_Compat.CRYPTO_BOX_KEYPAIRBYTES:
            raise php_new_class("TypeError", lambda : TypeError("Argument 4 must be CRYPTO_BOX_KEYPAIRBYTES bytes"))
        # end if
        #// @var int $size
        size_ = filesize(inputFile_)
        if (not php_is_int(size_)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not obtain the file size"))
        # end if
        #// @var resource $ifp
        ifp_ = fopen(inputFile_, "rb")
        if (not is_resource(ifp_)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not open input file for reading"))
        # end if
        #// @var resource $ofp
        ofp_ = fopen(outputFile_, "wb")
        if (not is_resource(ofp_)):
            php_fclose(ifp_)
            raise php_new_class("SodiumException", lambda : SodiumException("Could not open output file for writing"))
        # end if
        res_ = self.box_encrypt(ifp_, ofp_, size_, nonce_, keyPair_)
        php_fclose(ifp_)
        php_fclose(ofp_)
        return res_
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
    def box_open(self, inputFile_=None, outputFile_=None, nonce_=None, keypair_=None):
        
        
        #// Type checks:
        if (not php_is_string(inputFile_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be a string, " + gettype(inputFile_) + " given."))
        # end if
        if (not php_is_string(outputFile_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 2 must be a string, " + gettype(outputFile_) + " given."))
        # end if
        if (not php_is_string(nonce_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 3 must be a string, " + gettype(nonce_) + " given."))
        # end if
        if (not php_is_string(keypair_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 4 must be a string, " + gettype(keypair_) + " given."))
        # end if
        #// Input validation:
        if self.strlen(nonce_) != ParagonIE_Sodium_Compat.CRYPTO_BOX_NONCEBYTES:
            raise php_new_class("TypeError", lambda : TypeError("Argument 4 must be CRYPTO_BOX_NONCEBYTES bytes"))
        # end if
        if self.strlen(keypair_) != ParagonIE_Sodium_Compat.CRYPTO_BOX_KEYPAIRBYTES:
            raise php_new_class("TypeError", lambda : TypeError("Argument 4 must be CRYPTO_BOX_KEYPAIRBYTES bytes"))
        # end if
        #// @var int $size
        size_ = filesize(inputFile_)
        if (not php_is_int(size_)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not obtain the file size"))
        # end if
        #// @var resource $ifp
        ifp_ = fopen(inputFile_, "rb")
        if (not is_resource(ifp_)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not open input file for reading"))
        # end if
        #// @var resource $ofp
        ofp_ = fopen(outputFile_, "wb")
        if (not is_resource(ofp_)):
            php_fclose(ifp_)
            raise php_new_class("SodiumException", lambda : SodiumException("Could not open output file for writing"))
        # end if
        res_ = self.box_decrypt(ifp_, ofp_, size_, nonce_, keypair_)
        php_fclose(ifp_)
        php_fclose(ofp_)
        try: 
            ParagonIE_Sodium_Compat.memzero(nonce_)
            ParagonIE_Sodium_Compat.memzero(ephKeypair_)
        except SodiumException as ex_:
            ephKeypair_ = None
        # end try
        return res_
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
    def box_seal(self, inputFile_=None, outputFile_=None, publicKey_=None):
        
        
        #// Type checks:
        if (not php_is_string(inputFile_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be a string, " + gettype(inputFile_) + " given."))
        # end if
        if (not php_is_string(outputFile_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 2 must be a string, " + gettype(outputFile_) + " given."))
        # end if
        if (not php_is_string(publicKey_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 3 must be a string, " + gettype(publicKey_) + " given."))
        # end if
        #// Input validation:
        if self.strlen(publicKey_) != ParagonIE_Sodium_Compat.CRYPTO_BOX_PUBLICKEYBYTES:
            raise php_new_class("TypeError", lambda : TypeError("Argument 3 must be CRYPTO_BOX_PUBLICKEYBYTES bytes"))
        # end if
        #// @var int $size
        size_ = filesize(inputFile_)
        if (not php_is_int(size_)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not obtain the file size"))
        # end if
        #// @var resource $ifp
        ifp_ = fopen(inputFile_, "rb")
        if (not is_resource(ifp_)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not open input file for reading"))
        # end if
        #// @var resource $ofp
        ofp_ = fopen(outputFile_, "wb")
        if (not is_resource(ofp_)):
            php_fclose(ifp_)
            raise php_new_class("SodiumException", lambda : SodiumException("Could not open output file for writing"))
        # end if
        #// @var string $ephKeypair
        ephKeypair_ = ParagonIE_Sodium_Compat.crypto_box_keypair()
        #// @var string $msgKeypair
        msgKeypair_ = ParagonIE_Sodium_Compat.crypto_box_keypair_from_secretkey_and_publickey(ParagonIE_Sodium_Compat.crypto_box_secretkey(ephKeypair_), publicKey_)
        #// @var string $ephemeralPK
        ephemeralPK_ = ParagonIE_Sodium_Compat.crypto_box_publickey(ephKeypair_)
        #// @var string $nonce
        nonce_ = ParagonIE_Sodium_Compat.crypto_generichash(ephemeralPK_ + publicKey_, "", 24)
        #// @var int $firstWrite
        firstWrite_ = fwrite(ofp_, ephemeralPK_, ParagonIE_Sodium_Compat.CRYPTO_BOX_PUBLICKEYBYTES)
        if (not php_is_int(firstWrite_)):
            php_fclose(ifp_)
            php_fclose(ofp_)
            ParagonIE_Sodium_Compat.memzero(ephKeypair_)
            raise php_new_class("SodiumException", lambda : SodiumException("Could not write to output file"))
        # end if
        if firstWrite_ != ParagonIE_Sodium_Compat.CRYPTO_BOX_PUBLICKEYBYTES:
            ParagonIE_Sodium_Compat.memzero(ephKeypair_)
            php_fclose(ifp_)
            php_fclose(ofp_)
            raise php_new_class("SodiumException", lambda : SodiumException("Error writing public key to output file"))
        # end if
        res_ = self.box_encrypt(ifp_, ofp_, size_, nonce_, msgKeypair_)
        php_fclose(ifp_)
        php_fclose(ofp_)
        try: 
            ParagonIE_Sodium_Compat.memzero(nonce_)
            ParagonIE_Sodium_Compat.memzero(ephKeypair_)
        except SodiumException as ex_:
            ephKeypair_ = None
        # end try
        return res_
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
    def box_seal_open(self, inputFile_=None, outputFile_=None, ecdhKeypair_=None):
        
        
        #// Type checks:
        if (not php_is_string(inputFile_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be a string, " + gettype(inputFile_) + " given."))
        # end if
        if (not php_is_string(outputFile_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 2 must be a string, " + gettype(outputFile_) + " given."))
        # end if
        if (not php_is_string(ecdhKeypair_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 3 must be a string, " + gettype(ecdhKeypair_) + " given."))
        # end if
        #// Input validation:
        if self.strlen(ecdhKeypair_) != ParagonIE_Sodium_Compat.CRYPTO_BOX_KEYPAIRBYTES:
            raise php_new_class("TypeError", lambda : TypeError("Argument 3 must be CRYPTO_BOX_KEYPAIRBYTES bytes"))
        # end if
        publicKey_ = ParagonIE_Sodium_Compat.crypto_box_publickey(ecdhKeypair_)
        #// @var int $size
        size_ = filesize(inputFile_)
        if (not php_is_int(size_)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not obtain the file size"))
        # end if
        #// @var resource $ifp
        ifp_ = fopen(inputFile_, "rb")
        if (not is_resource(ifp_)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not open input file for reading"))
        # end if
        #// @var resource $ofp
        ofp_ = fopen(outputFile_, "wb")
        if (not is_resource(ofp_)):
            php_fclose(ifp_)
            raise php_new_class("SodiumException", lambda : SodiumException("Could not open output file for writing"))
        # end if
        ephemeralPK_ = fread(ifp_, ParagonIE_Sodium_Compat.CRYPTO_BOX_PUBLICKEYBYTES)
        if (not php_is_string(ephemeralPK_)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not read input file"))
        # end if
        if self.strlen(ephemeralPK_) != ParagonIE_Sodium_Compat.CRYPTO_BOX_PUBLICKEYBYTES:
            php_fclose(ifp_)
            php_fclose(ofp_)
            raise php_new_class("SodiumException", lambda : SodiumException("Could not read public key from sealed file"))
        # end if
        nonce_ = ParagonIE_Sodium_Compat.crypto_generichash(ephemeralPK_ + publicKey_, "", 24)
        msgKeypair_ = ParagonIE_Sodium_Compat.crypto_box_keypair_from_secretkey_and_publickey(ParagonIE_Sodium_Compat.crypto_box_secretkey(ecdhKeypair_), ephemeralPK_)
        res_ = self.box_decrypt(ifp_, ofp_, size_, nonce_, msgKeypair_)
        php_fclose(ifp_)
        php_fclose(ofp_)
        try: 
            ParagonIE_Sodium_Compat.memzero(nonce_)
            ParagonIE_Sodium_Compat.memzero(ephKeypair_)
        except SodiumException as ex_:
            ephKeypair_ = None
        # end try
        return res_
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
    def generichash(self, filePath_=None, key_="", outputLength_=32):
        
        
        #// Type checks:
        if (not php_is_string(filePath_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be a string, " + gettype(filePath_) + " given."))
        # end if
        if (not php_is_string(key_)):
            if php_is_null(key_):
                key_ = ""
            else:
                raise php_new_class("TypeError", lambda : TypeError("Argument 2 must be a string, " + gettype(key_) + " given."))
            # end if
        # end if
        if (not php_is_int(outputLength_)):
            if (not php_is_numeric(outputLength_)):
                raise php_new_class("TypeError", lambda : TypeError("Argument 3 must be an integer, " + gettype(outputLength_) + " given."))
            # end if
            outputLength_ = php_int(outputLength_)
        # end if
        #// Input validation:
        if (not php_empty(lambda : key_)):
            if self.strlen(key_) < ParagonIE_Sodium_Compat.CRYPTO_GENERICHASH_KEYBYTES_MIN:
                raise php_new_class("TypeError", lambda : TypeError("Argument 2 must be at least CRYPTO_GENERICHASH_KEYBYTES_MIN bytes"))
            # end if
            if self.strlen(key_) > ParagonIE_Sodium_Compat.CRYPTO_GENERICHASH_KEYBYTES_MAX:
                raise php_new_class("TypeError", lambda : TypeError("Argument 2 must be at most CRYPTO_GENERICHASH_KEYBYTES_MAX bytes"))
            # end if
        # end if
        if outputLength_ < ParagonIE_Sodium_Compat.CRYPTO_GENERICHASH_BYTES_MIN:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 3 must be at least CRYPTO_GENERICHASH_BYTES_MIN"))
        # end if
        if outputLength_ > ParagonIE_Sodium_Compat.CRYPTO_GENERICHASH_BYTES_MAX:
            raise php_new_class("SodiumException", lambda : SodiumException("Argument 3 must be at least CRYPTO_GENERICHASH_BYTES_MAX"))
        # end if
        #// @var int $size
        size_ = filesize(filePath_)
        if (not php_is_int(size_)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not obtain the file size"))
        # end if
        #// @var resource $fp
        fp_ = fopen(filePath_, "rb")
        if (not is_resource(fp_)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not open input file for reading"))
        # end if
        ctx_ = ParagonIE_Sodium_Compat.crypto_generichash_init(key_, outputLength_)
        while True:
            
            if not (size_ > 0):
                break
            # end if
            blockSize_ = 64 if size_ > 64 else size_
            read_ = fread(fp_, blockSize_)
            if (not php_is_string(read_)):
                raise php_new_class("SodiumException", lambda : SodiumException("Could not read input file"))
            # end if
            ParagonIE_Sodium_Compat.crypto_generichash_update(ctx_, read_)
            size_ -= blockSize_
        # end while
        php_fclose(fp_)
        return ParagonIE_Sodium_Compat.crypto_generichash_final(ctx_, outputLength_)
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
    def secretbox(self, inputFile_=None, outputFile_=None, nonce_=None, key_=None):
        
        
        #// Type checks:
        if (not php_is_string(inputFile_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be a string, " + gettype(inputFile_) + " given.."))
        # end if
        if (not php_is_string(outputFile_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 2 must be a string, " + gettype(outputFile_) + " given."))
        # end if
        if (not php_is_string(nonce_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 3 must be a string, " + gettype(nonce_) + " given."))
        # end if
        #// Input validation:
        if self.strlen(nonce_) != ParagonIE_Sodium_Compat.CRYPTO_SECRETBOX_NONCEBYTES:
            raise php_new_class("TypeError", lambda : TypeError("Argument 3 must be CRYPTO_SECRETBOX_NONCEBYTES bytes"))
        # end if
        if (not php_is_string(key_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 4 must be a string, " + gettype(key_) + " given."))
        # end if
        if self.strlen(key_) != ParagonIE_Sodium_Compat.CRYPTO_SECRETBOX_KEYBYTES:
            raise php_new_class("TypeError", lambda : TypeError("Argument 4 must be CRYPTO_SECRETBOX_KEYBYTES bytes"))
        # end if
        #// @var int $size
        size_ = filesize(inputFile_)
        if (not php_is_int(size_)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not obtain the file size"))
        # end if
        #// @var resource $ifp
        ifp_ = fopen(inputFile_, "rb")
        if (not is_resource(ifp_)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not open input file for reading"))
        # end if
        #// @var resource $ofp
        ofp_ = fopen(outputFile_, "wb")
        if (not is_resource(ofp_)):
            php_fclose(ifp_)
            raise php_new_class("SodiumException", lambda : SodiumException("Could not open output file for writing"))
        # end if
        res_ = self.secretbox_encrypt(ifp_, ofp_, size_, nonce_, key_)
        php_fclose(ifp_)
        php_fclose(ofp_)
        return res_
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
    def secretbox_open(self, inputFile_=None, outputFile_=None, nonce_=None, key_=None):
        
        
        #// Type checks:
        if (not php_is_string(inputFile_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be a string, " + gettype(inputFile_) + " given."))
        # end if
        if (not php_is_string(outputFile_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 2 must be a string, " + gettype(outputFile_) + " given."))
        # end if
        if (not php_is_string(nonce_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 3 must be a string, " + gettype(nonce_) + " given."))
        # end if
        if (not php_is_string(key_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 4 must be a string, " + gettype(key_) + " given."))
        # end if
        #// Input validation:
        if self.strlen(nonce_) != ParagonIE_Sodium_Compat.CRYPTO_SECRETBOX_NONCEBYTES:
            raise php_new_class("TypeError", lambda : TypeError("Argument 4 must be CRYPTO_SECRETBOX_NONCEBYTES bytes"))
        # end if
        if self.strlen(key_) != ParagonIE_Sodium_Compat.CRYPTO_SECRETBOX_KEYBYTES:
            raise php_new_class("TypeError", lambda : TypeError("Argument 4 must be CRYPTO_SECRETBOXBOX_KEYBYTES bytes"))
        # end if
        #// @var int $size
        size_ = filesize(inputFile_)
        if (not php_is_int(size_)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not obtain the file size"))
        # end if
        #// @var resource $ifp
        ifp_ = fopen(inputFile_, "rb")
        if (not is_resource(ifp_)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not open input file for reading"))
        # end if
        #// @var resource $ofp
        ofp_ = fopen(outputFile_, "wb")
        if (not is_resource(ofp_)):
            php_fclose(ifp_)
            raise php_new_class("SodiumException", lambda : SodiumException("Could not open output file for writing"))
        # end if
        res_ = self.secretbox_decrypt(ifp_, ofp_, size_, nonce_, key_)
        php_fclose(ifp_)
        php_fclose(ofp_)
        try: 
            ParagonIE_Sodium_Compat.memzero(key_)
        except SodiumException as ex_:
            key_ = None
        # end try
        return res_
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
    def sign(self, filePath_=None, secretKey_=None):
        
        
        #// Type checks:
        if (not php_is_string(filePath_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be a string, " + gettype(filePath_) + " given."))
        # end if
        if (not php_is_string(secretKey_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 2 must be a string, " + gettype(secretKey_) + " given."))
        # end if
        #// Input validation:
        if self.strlen(secretKey_) != ParagonIE_Sodium_Compat.CRYPTO_SIGN_SECRETKEYBYTES:
            raise php_new_class("TypeError", lambda : TypeError("Argument 2 must be CRYPTO_SIGN_SECRETKEYBYTES bytes"))
        # end if
        if PHP_INT_SIZE == 4:
            return self.sign_core32(filePath_, secretKey_)
        # end if
        #// @var int $size
        size_ = filesize(filePath_)
        if (not php_is_int(size_)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not obtain the file size"))
        # end if
        #// @var resource $fp
        fp_ = fopen(filePath_, "rb")
        if (not is_resource(fp_)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not open input file for reading"))
        # end if
        #// @var string $az
        az_ = hash("sha512", self.substr(secretKey_, 0, 32), True)
        az_[0] = self.inttochr(self.chrtoint(az_[0]) & 248)
        az_[31] = self.inttochr(self.chrtoint(az_[31]) & 63 | 64)
        hs_ = hash_init("sha512")
        hash_update(hs_, self.substr(az_, 32, 32))
        #// @var resource $hs
        hs_ = self.updatehashwithfile(hs_, fp_, size_)
        #// @var string $nonceHash
        nonceHash_ = hash_final(hs_, True)
        #// @var string $pk
        pk_ = self.substr(secretKey_, 32, 32)
        #// @var string $nonce
        nonce_ = ParagonIE_Sodium_Core_Ed25519.sc_reduce(nonceHash_) + self.substr(nonceHash_, 32)
        #// @var string $sig
        sig_ = ParagonIE_Sodium_Core_Ed25519.ge_p3_tobytes(ParagonIE_Sodium_Core_Ed25519.ge_scalarmult_base(nonce_))
        hs_ = hash_init("sha512")
        hash_update(hs_, self.substr(sig_, 0, 32))
        hash_update(hs_, self.substr(pk_, 0, 32))
        #// @var resource $hs
        hs_ = self.updatehashwithfile(hs_, fp_, size_)
        #// @var string $hramHash
        hramHash_ = hash_final(hs_, True)
        #// @var string $hram
        hram_ = ParagonIE_Sodium_Core_Ed25519.sc_reduce(hramHash_)
        #// @var string $sigAfter
        sigAfter_ = ParagonIE_Sodium_Core_Ed25519.sc_muladd(hram_, az_, nonce_)
        #// @var string $sig
        sig_ = self.substr(sig_, 0, 32) + self.substr(sigAfter_, 0, 32)
        try: 
            ParagonIE_Sodium_Compat.memzero(az_)
        except SodiumException as ex_:
            az_ = None
        # end try
        php_fclose(fp_)
        return sig_
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
    def verify(self, sig_=None, filePath_=None, publicKey_=None):
        
        
        #// Type checks:
        if (not php_is_string(sig_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be a string, " + gettype(sig_) + " given."))
        # end if
        if (not php_is_string(filePath_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 2 must be a string, " + gettype(filePath_) + " given."))
        # end if
        if (not php_is_string(publicKey_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 3 must be a string, " + gettype(publicKey_) + " given."))
        # end if
        #// Input validation:
        if self.strlen(sig_) != ParagonIE_Sodium_Compat.CRYPTO_SIGN_BYTES:
            raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be CRYPTO_SIGN_BYTES bytes"))
        # end if
        if self.strlen(publicKey_) != ParagonIE_Sodium_Compat.CRYPTO_SIGN_PUBLICKEYBYTES:
            raise php_new_class("TypeError", lambda : TypeError("Argument 3 must be CRYPTO_SIGN_PUBLICKEYBYTES bytes"))
        # end if
        if self.strlen(sig_) < 64:
            raise php_new_class("SodiumException", lambda : SodiumException("Signature is too short"))
        # end if
        if PHP_INT_SIZE == 4:
            return self.verify_core32(sig_, filePath_, publicKey_)
        # end if
        #// Security checks
        if ParagonIE_Sodium_Core_Ed25519.chrtoint(sig_[63]) & 240 and ParagonIE_Sodium_Core_Ed25519.check_s_lt_l(self.substr(sig_, 32, 32)):
            raise php_new_class("SodiumException", lambda : SodiumException("S < L - Invalid signature"))
        # end if
        if ParagonIE_Sodium_Core_Ed25519.small_order(sig_):
            raise php_new_class("SodiumException", lambda : SodiumException("Signature is on too small of an order"))
        # end if
        if self.chrtoint(sig_[63]) & 224 != 0:
            raise php_new_class("SodiumException", lambda : SodiumException("Invalid signature"))
        # end if
        d_ = 0
        i_ = 0
        while i_ < 32:
            
            d_ |= self.chrtoint(publicKey_[i_])
            i_ += 1
        # end while
        if d_ == 0:
            raise php_new_class("SodiumException", lambda : SodiumException("All zero public key"))
        # end if
        #// @var int $size
        size_ = filesize(filePath_)
        if (not php_is_int(size_)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not obtain the file size"))
        # end if
        #// @var resource $fp
        fp_ = fopen(filePath_, "rb")
        if (not is_resource(fp_)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not open input file for reading"))
        # end if
        #// @var bool The original value of ParagonIE_Sodium_Compat::$fastMult
        orig_ = ParagonIE_Sodium_Compat.fastMult
        #// Set ParagonIE_Sodium_Compat::$fastMult to true to speed up verification.
        ParagonIE_Sodium_Compat.fastMult = True
        #// @var ParagonIE_Sodium_Core_Curve25519_Ge_P3 $A
        A_ = ParagonIE_Sodium_Core_Ed25519.ge_frombytes_negate_vartime(publicKey_)
        hs_ = hash_init("sha512")
        hash_update(hs_, self.substr(sig_, 0, 32))
        hash_update(hs_, self.substr(publicKey_, 0, 32))
        #// @var resource $hs
        hs_ = self.updatehashwithfile(hs_, fp_, size_)
        #// @var string $hDigest
        hDigest_ = hash_final(hs_, True)
        #// @var string $h
        h_ = ParagonIE_Sodium_Core_Ed25519.sc_reduce(hDigest_) + self.substr(hDigest_, 32)
        #// @var ParagonIE_Sodium_Core_Curve25519_Ge_P2 $R
        R_ = ParagonIE_Sodium_Core_Ed25519.ge_double_scalarmult_vartime(h_, A_, self.substr(sig_, 32))
        #// @var string $rcheck
        rcheck_ = ParagonIE_Sodium_Core_Ed25519.ge_tobytes(R_)
        #// Close the file handle
        php_fclose(fp_)
        #// Reset ParagonIE_Sodium_Compat::$fastMult to what it was before.
        ParagonIE_Sodium_Compat.fastMult = orig_
        return self.verify_32(rcheck_, self.substr(sig_, 0, 32))
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
    def box_encrypt(self, ifp_=None, ofp_=None, mlen_=None, nonce_=None, boxKeypair_=None):
        
        
        if PHP_INT_SIZE == 4:
            return self.secretbox_encrypt(ifp_, ofp_, mlen_, nonce_, ParagonIE_Sodium_Crypto32.box_beforenm(ParagonIE_Sodium_Crypto32.box_secretkey(boxKeypair_), ParagonIE_Sodium_Crypto32.box_publickey(boxKeypair_)))
        # end if
        return self.secretbox_encrypt(ifp_, ofp_, mlen_, nonce_, ParagonIE_Sodium_Crypto.box_beforenm(ParagonIE_Sodium_Crypto.box_secretkey(boxKeypair_), ParagonIE_Sodium_Crypto.box_publickey(boxKeypair_)))
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
    def box_decrypt(self, ifp_=None, ofp_=None, mlen_=None, nonce_=None, boxKeypair_=None):
        
        
        if PHP_INT_SIZE == 4:
            return self.secretbox_decrypt(ifp_, ofp_, mlen_, nonce_, ParagonIE_Sodium_Crypto32.box_beforenm(ParagonIE_Sodium_Crypto32.box_secretkey(boxKeypair_), ParagonIE_Sodium_Crypto32.box_publickey(boxKeypair_)))
        # end if
        return self.secretbox_decrypt(ifp_, ofp_, mlen_, nonce_, ParagonIE_Sodium_Crypto.box_beforenm(ParagonIE_Sodium_Crypto.box_secretkey(boxKeypair_), ParagonIE_Sodium_Crypto.box_publickey(boxKeypair_)))
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
    def secretbox_encrypt(self, ifp_=None, ofp_=None, mlen_=None, nonce_=None, key_=None):
        
        
        if PHP_INT_SIZE == 4:
            return self.secretbox_encrypt_core32(ifp_, ofp_, mlen_, nonce_, key_)
        # end if
        plaintext_ = fread(ifp_, 32)
        if (not php_is_string(plaintext_)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not read input file"))
        # end if
        first32_ = self.ftell(ifp_)
        #// @var string $subkey
        subkey_ = ParagonIE_Sodium_Core_HSalsa20.hsalsa20(nonce_, key_)
        #// @var string $realNonce
        realNonce_ = ParagonIE_Sodium_Core_Util.substr(nonce_, 16, 8)
        #// @var string $block0
        block0_ = php_str_repeat(" ", 32)
        #// @var int $mlen - Length of the plaintext message
        mlen0_ = mlen_
        if mlen0_ > 64 - ParagonIE_Sodium_Crypto.secretbox_xsalsa20poly1305_ZEROBYTES:
            mlen0_ = 64 - ParagonIE_Sodium_Crypto.secretbox_xsalsa20poly1305_ZEROBYTES
        # end if
        block0_ += ParagonIE_Sodium_Core_Util.substr(plaintext_, 0, mlen0_)
        #// @var string $block0
        block0_ = ParagonIE_Sodium_Core_Salsa20.salsa20_xor(block0_, realNonce_, subkey_)
        state_ = php_new_class("ParagonIE_Sodium_Core_Poly1305_State", lambda : ParagonIE_Sodium_Core_Poly1305_State(ParagonIE_Sodium_Core_Util.substr(block0_, 0, ParagonIE_Sodium_Crypto.onetimeauth_poly1305_KEYBYTES)))
        #// Pre-write 16 blank bytes for the Poly1305 tag
        start_ = self.ftell(ofp_)
        fwrite(ofp_, php_str_repeat(" ", 16))
        #// @var string $c
        cBlock_ = ParagonIE_Sodium_Core_Util.substr(block0_, ParagonIE_Sodium_Crypto.secretbox_xsalsa20poly1305_ZEROBYTES)
        state_.update(cBlock_)
        fwrite(ofp_, cBlock_)
        mlen_ -= 32
        #// @var int $iter
        iter_ = 1
        #// @var int $incr
        incr_ = self.BUFFER_SIZE >> 6
        #// 
        #// Set the cursor to the end of the first half-block. All future bytes will
        #// generated from salsa20_xor_ic, starting from 1 (second block).
        #//
        fseek(ifp_, first32_, SEEK_SET)
        while True:
            
            if not (mlen_ > 0):
                break
            # end if
            blockSize_ = self.BUFFER_SIZE if mlen_ > self.BUFFER_SIZE else mlen_
            plaintext_ = fread(ifp_, blockSize_)
            if (not php_is_string(plaintext_)):
                raise php_new_class("SodiumException", lambda : SodiumException("Could not read input file"))
            # end if
            cBlock_ = ParagonIE_Sodium_Core_Salsa20.salsa20_xor_ic(plaintext_, realNonce_, iter_, subkey_)
            fwrite(ofp_, cBlock_, blockSize_)
            state_.update(cBlock_)
            mlen_ -= blockSize_
            iter_ += incr_
        # end while
        try: 
            ParagonIE_Sodium_Compat.memzero(block0_)
            ParagonIE_Sodium_Compat.memzero(subkey_)
        except SodiumException as ex_:
            block0_ = None
            subkey_ = None
        # end try
        end_ = self.ftell(ofp_)
        #// 
        #// Write the Poly1305 authentication tag that provides integrity
        #// over the ciphertext (encrypt-then-MAC)
        #//
        fseek(ofp_, start_, SEEK_SET)
        fwrite(ofp_, state_.finish(), ParagonIE_Sodium_Compat.CRYPTO_SECRETBOX_MACBYTES)
        fseek(ofp_, end_, SEEK_SET)
        state_ = None
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
    def secretbox_decrypt(self, ifp_=None, ofp_=None, mlen_=None, nonce_=None, key_=None):
        
        
        if PHP_INT_SIZE == 4:
            return self.secretbox_decrypt_core32(ifp_, ofp_, mlen_, nonce_, key_)
        # end if
        tag_ = fread(ifp_, 16)
        if (not php_is_string(tag_)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not read input file"))
        # end if
        #// @var string $subkey
        subkey_ = ParagonIE_Sodium_Core_HSalsa20.hsalsa20(nonce_, key_)
        #// @var string $realNonce
        realNonce_ = ParagonIE_Sodium_Core_Util.substr(nonce_, 16, 8)
        #// @var string $block0
        block0_ = ParagonIE_Sodium_Core_Salsa20.salsa20(64, ParagonIE_Sodium_Core_Util.substr(nonce_, 16, 8), subkey_)
        #// Verify the Poly1305 MAC -before- attempting to decrypt!
        state_ = php_new_class("ParagonIE_Sodium_Core_Poly1305_State", lambda : ParagonIE_Sodium_Core_Poly1305_State(self.substr(block0_, 0, 32)))
        if (not self.onetimeauth_verify(state_, ifp_, tag_, mlen_)):
            raise php_new_class("SodiumException", lambda : SodiumException("Invalid MAC"))
        # end if
        #// 
        #// Set the cursor to the end of the first half-block. All future bytes will
        #// generated from salsa20_xor_ic, starting from 1 (second block).
        #//
        first32_ = fread(ifp_, 32)
        if (not php_is_string(first32_)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not read input file"))
        # end if
        first32len_ = self.strlen(first32_)
        fwrite(ofp_, self.xorstrings(self.substr(block0_, 32, first32len_), self.substr(first32_, 0, first32len_)))
        mlen_ -= 32
        #// @var int $iter
        iter_ = 1
        #// @var int $incr
        incr_ = self.BUFFER_SIZE >> 6
        #// Decrypts ciphertext, writes to output file.
        while True:
            
            if not (mlen_ > 0):
                break
            # end if
            blockSize_ = self.BUFFER_SIZE if mlen_ > self.BUFFER_SIZE else mlen_
            ciphertext_ = fread(ifp_, blockSize_)
            if (not php_is_string(ciphertext_)):
                raise php_new_class("SodiumException", lambda : SodiumException("Could not read input file"))
            # end if
            pBlock_ = ParagonIE_Sodium_Core_Salsa20.salsa20_xor_ic(ciphertext_, realNonce_, iter_, subkey_)
            fwrite(ofp_, pBlock_, blockSize_)
            mlen_ -= blockSize_
            iter_ += incr_
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
    def onetimeauth_verify(self, state_=None, ifp_=None, tag_="", mlen_=0):
        
        
        #// @var int $pos
        pos_ = self.ftell(ifp_)
        #// @var int $iter
        iter_ = 1
        #// @var int $incr
        incr_ = self.BUFFER_SIZE >> 6
        while True:
            
            if not (mlen_ > 0):
                break
            # end if
            blockSize_ = self.BUFFER_SIZE if mlen_ > self.BUFFER_SIZE else mlen_
            ciphertext_ = fread(ifp_, blockSize_)
            if (not php_is_string(ciphertext_)):
                raise php_new_class("SodiumException", lambda : SodiumException("Could not read input file"))
            # end if
            state_.update(ciphertext_)
            mlen_ -= blockSize_
            iter_ += incr_
        # end while
        res_ = ParagonIE_Sodium_Core_Util.verify_16(tag_, state_.finish())
        fseek(ifp_, pos_, SEEK_SET)
        return res_
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
    def updatehashwithfile(self, hash_=None, fp_=None, size_=0):
        
        
        #// Type checks:
        if PHP_VERSION_ID < 70200:
            if (not is_resource(hash_)):
                raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be a resource, " + gettype(hash_) + " given."))
            # end if
        else:
            if (not php_is_object(hash_)):
                raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be an object (PHP 7.2+), " + gettype(hash_) + " given."))
            # end if
        # end if
        if (not is_resource(fp_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 2 must be a resource, " + gettype(fp_) + " given."))
        # end if
        if (not php_is_int(size_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 3 must be an integer, " + gettype(size_) + " given."))
        # end if
        #// @var int $originalPosition
        originalPosition_ = self.ftell(fp_)
        #// Move file pointer to beginning of file
        fseek(fp_, 0, SEEK_SET)
        i_ = 0
        while i_ < size_:
            
            #// @var string|bool $message
            message_ = fread(fp_, size_ - i_ if size_ - i_ > self.BUFFER_SIZE else self.BUFFER_SIZE)
            if (not php_is_string(message_)):
                raise php_new_class("SodiumException", lambda : SodiumException("Unexpected error reading from file."))
            # end if
            #// @var string $message
            #// @psalm-suppress InvalidArgument
            hash_update(hash_, message_)
            i_ += self.BUFFER_SIZE
        # end while
        #// Reset file pointer's position
        fseek(fp_, originalPosition_, SEEK_SET)
        return hash_
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
    def sign_core32(self, filePath_=None, secretKey_=None):
        
        
        #// @var int|bool $size
        size_ = filesize(filePath_)
        if (not php_is_int(size_)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not obtain the file size"))
        # end if
        #// @var int $size
        #// @var resource|bool $fp
        fp_ = fopen(filePath_, "rb")
        if (not is_resource(fp_)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not open input file for reading"))
        # end if
        #// @var resource $fp
        #// @var string $az
        az_ = hash("sha512", self.substr(secretKey_, 0, 32), True)
        az_[0] = self.inttochr(self.chrtoint(az_[0]) & 248)
        az_[31] = self.inttochr(self.chrtoint(az_[31]) & 63 | 64)
        hs_ = hash_init("sha512")
        hash_update(hs_, self.substr(az_, 32, 32))
        #// @var resource $hs
        hs_ = self.updatehashwithfile(hs_, fp_, size_)
        #// @var string $nonceHash
        nonceHash_ = hash_final(hs_, True)
        #// @var string $pk
        pk_ = self.substr(secretKey_, 32, 32)
        #// @var string $nonce
        nonce_ = ParagonIE_Sodium_Core32_Ed25519.sc_reduce(nonceHash_) + self.substr(nonceHash_, 32)
        #// @var string $sig
        sig_ = ParagonIE_Sodium_Core32_Ed25519.ge_p3_tobytes(ParagonIE_Sodium_Core32_Ed25519.ge_scalarmult_base(nonce_))
        hs_ = hash_init("sha512")
        hash_update(hs_, self.substr(sig_, 0, 32))
        hash_update(hs_, self.substr(pk_, 0, 32))
        #// @var resource $hs
        hs_ = self.updatehashwithfile(hs_, fp_, size_)
        #// @var string $hramHash
        hramHash_ = hash_final(hs_, True)
        #// @var string $hram
        hram_ = ParagonIE_Sodium_Core32_Ed25519.sc_reduce(hramHash_)
        #// @var string $sigAfter
        sigAfter_ = ParagonIE_Sodium_Core32_Ed25519.sc_muladd(hram_, az_, nonce_)
        #// @var string $sig
        sig_ = self.substr(sig_, 0, 32) + self.substr(sigAfter_, 0, 32)
        try: 
            ParagonIE_Sodium_Compat.memzero(az_)
        except SodiumException as ex_:
            az_ = None
        # end try
        php_fclose(fp_)
        return sig_
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
    def verify_core32(self, sig_=None, filePath_=None, publicKey_=None):
        
        
        #// Security checks
        if ParagonIE_Sodium_Core32_Ed25519.check_s_lt_l(self.substr(sig_, 32, 32)):
            raise php_new_class("SodiumException", lambda : SodiumException("S < L - Invalid signature"))
        # end if
        if ParagonIE_Sodium_Core32_Ed25519.small_order(sig_):
            raise php_new_class("SodiumException", lambda : SodiumException("Signature is on too small of an order"))
        # end if
        if self.chrtoint(sig_[63]) & 224 != 0:
            raise php_new_class("SodiumException", lambda : SodiumException("Invalid signature"))
        # end if
        d_ = 0
        i_ = 0
        while i_ < 32:
            
            d_ |= self.chrtoint(publicKey_[i_])
            i_ += 1
        # end while
        if d_ == 0:
            raise php_new_class("SodiumException", lambda : SodiumException("All zero public key"))
        # end if
        #// @var int|bool $size
        size_ = filesize(filePath_)
        if (not php_is_int(size_)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not obtain the file size"))
        # end if
        #// @var int $size
        #// @var resource|bool $fp
        fp_ = fopen(filePath_, "rb")
        if (not is_resource(fp_)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not open input file for reading"))
        # end if
        #// @var resource $fp
        #// @var bool The original value of ParagonIE_Sodium_Compat::$fastMult
        orig_ = ParagonIE_Sodium_Compat.fastMult
        #// Set ParagonIE_Sodium_Compat::$fastMult to true to speed up verification.
        ParagonIE_Sodium_Compat.fastMult = True
        #// @var ParagonIE_Sodium_Core32_Curve25519_Ge_P3 $A
        A_ = ParagonIE_Sodium_Core32_Ed25519.ge_frombytes_negate_vartime(publicKey_)
        hs_ = hash_init("sha512")
        hash_update(hs_, self.substr(sig_, 0, 32))
        hash_update(hs_, self.substr(publicKey_, 0, 32))
        #// @var resource $hs
        hs_ = self.updatehashwithfile(hs_, fp_, size_)
        #// @var string $hDigest
        hDigest_ = hash_final(hs_, True)
        #// @var string $h
        h_ = ParagonIE_Sodium_Core32_Ed25519.sc_reduce(hDigest_) + self.substr(hDigest_, 32)
        #// @var ParagonIE_Sodium_Core32_Curve25519_Ge_P2 $R
        R_ = ParagonIE_Sodium_Core32_Ed25519.ge_double_scalarmult_vartime(h_, A_, self.substr(sig_, 32))
        #// @var string $rcheck
        rcheck_ = ParagonIE_Sodium_Core32_Ed25519.ge_tobytes(R_)
        #// Close the file handle
        php_fclose(fp_)
        #// Reset ParagonIE_Sodium_Compat::$fastMult to what it was before.
        ParagonIE_Sodium_Compat.fastMult = orig_
        return self.verify_32(rcheck_, self.substr(sig_, 0, 32))
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
    def secretbox_encrypt_core32(self, ifp_=None, ofp_=None, mlen_=None, nonce_=None, key_=None):
        
        
        plaintext_ = fread(ifp_, 32)
        if (not php_is_string(plaintext_)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not read input file"))
        # end if
        first32_ = self.ftell(ifp_)
        #// @var string $subkey
        subkey_ = ParagonIE_Sodium_Core32_HSalsa20.hsalsa20(nonce_, key_)
        #// @var string $realNonce
        realNonce_ = ParagonIE_Sodium_Core32_Util.substr(nonce_, 16, 8)
        #// @var string $block0
        block0_ = php_str_repeat(" ", 32)
        #// @var int $mlen - Length of the plaintext message
        mlen0_ = mlen_
        if mlen0_ > 64 - ParagonIE_Sodium_Crypto.secretbox_xsalsa20poly1305_ZEROBYTES:
            mlen0_ = 64 - ParagonIE_Sodium_Crypto.secretbox_xsalsa20poly1305_ZEROBYTES
        # end if
        block0_ += ParagonIE_Sodium_Core32_Util.substr(plaintext_, 0, mlen0_)
        #// @var string $block0
        block0_ = ParagonIE_Sodium_Core32_Salsa20.salsa20_xor(block0_, realNonce_, subkey_)
        state_ = php_new_class("ParagonIE_Sodium_Core32_Poly1305_State", lambda : ParagonIE_Sodium_Core32_Poly1305_State(ParagonIE_Sodium_Core32_Util.substr(block0_, 0, ParagonIE_Sodium_Crypto.onetimeauth_poly1305_KEYBYTES)))
        #// Pre-write 16 blank bytes for the Poly1305 tag
        start_ = self.ftell(ofp_)
        fwrite(ofp_, php_str_repeat(" ", 16))
        #// @var string $c
        cBlock_ = ParagonIE_Sodium_Core32_Util.substr(block0_, ParagonIE_Sodium_Crypto.secretbox_xsalsa20poly1305_ZEROBYTES)
        state_.update(cBlock_)
        fwrite(ofp_, cBlock_)
        mlen_ -= 32
        #// @var int $iter
        iter_ = 1
        #// @var int $incr
        incr_ = self.BUFFER_SIZE >> 6
        #// 
        #// Set the cursor to the end of the first half-block. All future bytes will
        #// generated from salsa20_xor_ic, starting from 1 (second block).
        #//
        fseek(ifp_, first32_, SEEK_SET)
        while True:
            
            if not (mlen_ > 0):
                break
            # end if
            blockSize_ = self.BUFFER_SIZE if mlen_ > self.BUFFER_SIZE else mlen_
            plaintext_ = fread(ifp_, blockSize_)
            if (not php_is_string(plaintext_)):
                raise php_new_class("SodiumException", lambda : SodiumException("Could not read input file"))
            # end if
            cBlock_ = ParagonIE_Sodium_Core32_Salsa20.salsa20_xor_ic(plaintext_, realNonce_, iter_, subkey_)
            fwrite(ofp_, cBlock_, blockSize_)
            state_.update(cBlock_)
            mlen_ -= blockSize_
            iter_ += incr_
        # end while
        try: 
            ParagonIE_Sodium_Compat.memzero(block0_)
            ParagonIE_Sodium_Compat.memzero(subkey_)
        except SodiumException as ex_:
            block0_ = None
            subkey_ = None
        # end try
        end_ = self.ftell(ofp_)
        #// 
        #// Write the Poly1305 authentication tag that provides integrity
        #// over the ciphertext (encrypt-then-MAC)
        #//
        fseek(ofp_, start_, SEEK_SET)
        fwrite(ofp_, state_.finish(), ParagonIE_Sodium_Compat.CRYPTO_SECRETBOX_MACBYTES)
        fseek(ofp_, end_, SEEK_SET)
        state_ = None
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
    def secretbox_decrypt_core32(self, ifp_=None, ofp_=None, mlen_=None, nonce_=None, key_=None):
        
        
        tag_ = fread(ifp_, 16)
        if (not php_is_string(tag_)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not read input file"))
        # end if
        #// @var string $subkey
        subkey_ = ParagonIE_Sodium_Core32_HSalsa20.hsalsa20(nonce_, key_)
        #// @var string $realNonce
        realNonce_ = ParagonIE_Sodium_Core32_Util.substr(nonce_, 16, 8)
        #// @var string $block0
        block0_ = ParagonIE_Sodium_Core32_Salsa20.salsa20(64, ParagonIE_Sodium_Core32_Util.substr(nonce_, 16, 8), subkey_)
        #// Verify the Poly1305 MAC -before- attempting to decrypt!
        state_ = php_new_class("ParagonIE_Sodium_Core32_Poly1305_State", lambda : ParagonIE_Sodium_Core32_Poly1305_State(self.substr(block0_, 0, 32)))
        if (not self.onetimeauth_verify_core32(state_, ifp_, tag_, mlen_)):
            raise php_new_class("SodiumException", lambda : SodiumException("Invalid MAC"))
        # end if
        #// 
        #// Set the cursor to the end of the first half-block. All future bytes will
        #// generated from salsa20_xor_ic, starting from 1 (second block).
        #//
        first32_ = fread(ifp_, 32)
        if (not php_is_string(first32_)):
            raise php_new_class("SodiumException", lambda : SodiumException("Could not read input file"))
        # end if
        first32len_ = self.strlen(first32_)
        fwrite(ofp_, self.xorstrings(self.substr(block0_, 32, first32len_), self.substr(first32_, 0, first32len_)))
        mlen_ -= 32
        #// @var int $iter
        iter_ = 1
        #// @var int $incr
        incr_ = self.BUFFER_SIZE >> 6
        #// Decrypts ciphertext, writes to output file.
        while True:
            
            if not (mlen_ > 0):
                break
            # end if
            blockSize_ = self.BUFFER_SIZE if mlen_ > self.BUFFER_SIZE else mlen_
            ciphertext_ = fread(ifp_, blockSize_)
            if (not php_is_string(ciphertext_)):
                raise php_new_class("SodiumException", lambda : SodiumException("Could not read input file"))
            # end if
            pBlock_ = ParagonIE_Sodium_Core32_Salsa20.salsa20_xor_ic(ciphertext_, realNonce_, iter_, subkey_)
            fwrite(ofp_, pBlock_, blockSize_)
            mlen_ -= blockSize_
            iter_ += incr_
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
    def onetimeauth_verify_core32(self, state_=None, ifp_=None, tag_="", mlen_=0):
        
        
        #// @var int $pos
        pos_ = self.ftell(ifp_)
        #// @var int $iter
        iter_ = 1
        #// @var int $incr
        incr_ = self.BUFFER_SIZE >> 6
        while True:
            
            if not (mlen_ > 0):
                break
            # end if
            blockSize_ = self.BUFFER_SIZE if mlen_ > self.BUFFER_SIZE else mlen_
            ciphertext_ = fread(ifp_, blockSize_)
            if (not php_is_string(ciphertext_)):
                raise php_new_class("SodiumException", lambda : SodiumException("Could not read input file"))
            # end if
            state_.update(ciphertext_)
            mlen_ -= blockSize_
            iter_ += incr_
        # end while
        res_ = ParagonIE_Sodium_Core32_Util.verify_16(tag_, state_.finish())
        fseek(ifp_, pos_, SEEK_SET)
        return res_
    # end def onetimeauth_verify_core32
    #// 
    #// @param resource $resource
    #// @return int
    #// @throws SodiumException
    #//
    def ftell(self, resource_=None):
        
        
        return_ = ftell(resource_)
        if (not php_is_int(return_)):
            raise php_new_class("SodiumException", lambda : SodiumException("ftell() returned false"))
        # end if
        return php_int(return_)
    # end def ftell
# end class ParagonIE_Sodium_File
