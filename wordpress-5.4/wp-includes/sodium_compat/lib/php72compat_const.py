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
SODIUM_LIBRARY_MAJOR_VERSION = 9
SODIUM_LIBRARY_MINOR_VERSION = 1
SODIUM_LIBRARY_VERSION = "1.0.8"
SODIUM_BASE64_VARIANT_ORIGINAL = 1
SODIUM_BASE64_VARIANT_ORIGINAL_NO_PADDING = 3
SODIUM_BASE64_VARIANT_URLSAFE = 5
SODIUM_BASE64_VARIANT_URLSAFE_NO_PADDING = 7
SODIUM_CRYPTO_AEAD_AES256GCM_KEYBYTES = 32
SODIUM_CRYPTO_AEAD_AES256GCM_NSECBYTES = 0
SODIUM_CRYPTO_AEAD_AES256GCM_NPUBBYTES = 12
SODIUM_CRYPTO_AEAD_AES256GCM_ABYTES = 16
SODIUM_CRYPTO_AEAD_CHACHA20POLY1305_KEYBYTES = 32
SODIUM_CRYPTO_AEAD_CHACHA20POLY1305_NSECBYTES = 0
SODIUM_CRYPTO_AEAD_CHACHA20POLY1305_NPUBBYTES = 8
SODIUM_CRYPTO_AEAD_CHACHA20POLY1305_ABYTES = 16
SODIUM_CRYPTO_AEAD_CHACHA20POLY1305_IETF_KEYBYTES = 32
SODIUM_CRYPTO_AEAD_CHACHA20POLY1305_IETF_NSECBYTES = 0
SODIUM_CRYPTO_AEAD_CHACHA20POLY1305_IETF_NPUBBYTES = 12
SODIUM_CRYPTO_AEAD_CHACHA20POLY1305_IETF_ABYTES = 16
SODIUM_CRYPTO_AEAD_XCHACHA20POLY1305_IETF_KEYBYTES = 32
SODIUM_CRYPTO_AEAD_XCHACHA20POLY1305_IETF_NSECBYTES = 0
SODIUM_CRYPTO_AEAD_XCHACHA20POLY1305_IETF_NPUBBYTES = 24
SODIUM_CRYPTO_AEAD_XCHACHA20POLY1305_IETF_ABYTES = 16
SODIUM_CRYPTO_AUTH_BYTES = 32
SODIUM_CRYPTO_AUTH_KEYBYTES = 32
SODIUM_CRYPTO_BOX_SEALBYTES = 16
SODIUM_CRYPTO_BOX_SECRETKEYBYTES = 32
SODIUM_CRYPTO_BOX_PUBLICKEYBYTES = 32
SODIUM_CRYPTO_BOX_KEYPAIRBYTES = 64
SODIUM_CRYPTO_BOX_MACBYTES = 16
SODIUM_CRYPTO_BOX_NONCEBYTES = 24
SODIUM_CRYPTO_BOX_SEEDBYTES = 32
SODIUM_CRYPTO_KDF_BYTES_MIN = 16
SODIUM_CRYPTO_KDF_BYTES_MAX = 64
SODIUM_CRYPTO_KDF_CONTEXTBYTES = 8
SODIUM_CRYPTO_KDF_KEYBYTES = 32
SODIUM_CRYPTO_KX_BYTES = 32
SODIUM_CRYPTO_KX_PRIMITIVE = "x25519blake2b"
SODIUM_CRYPTO_KX_SEEDBYTES = 32
SODIUM_CRYPTO_KX_KEYPAIRBYTES = 64
SODIUM_CRYPTO_KX_PUBLICKEYBYTES = 32
SODIUM_CRYPTO_KX_SECRETKEYBYTES = 32
SODIUM_CRYPTO_KX_SESSIONKEYBYTES = 32
SODIUM_CRYPTO_GENERICHASH_BYTES = 32
SODIUM_CRYPTO_GENERICHASH_BYTES_MIN = 16
SODIUM_CRYPTO_GENERICHASH_BYTES_MAX = 64
SODIUM_CRYPTO_GENERICHASH_KEYBYTES = 32
SODIUM_CRYPTO_GENERICHASH_KEYBYTES_MIN = 16
SODIUM_CRYPTO_GENERICHASH_KEYBYTES_MAX = 64
SODIUM_CRYPTO_PWHASH_SALTBYTES = 16
SODIUM_CRYPTO_PWHASH_STRPREFIX = "$argon2id$"
SODIUM_CRYPTO_PWHASH_ALG_ARGON2I13 = 1
SODIUM_CRYPTO_PWHASH_ALG_ARGON2ID13 = 2
SODIUM_CRYPTO_PWHASH_MEMLIMIT_INTERACTIVE = 33554432
SODIUM_CRYPTO_PWHASH_OPSLIMIT_INTERACTIVE = 4
SODIUM_CRYPTO_PWHASH_MEMLIMIT_MODERATE = 134217728
SODIUM_CRYPTO_PWHASH_OPSLIMIT_MODERATE = 6
SODIUM_CRYPTO_PWHASH_MEMLIMIT_SENSITIVE = 536870912
SODIUM_CRYPTO_PWHASH_OPSLIMIT_SENSITIVE = 8
SODIUM_CRYPTO_PWHASH_SCRYPTSALSA208SHA256_SALTBYTES = 32
SODIUM_CRYPTO_PWHASH_SCRYPTSALSA208SHA256_STRPREFIX = "$7$"
SODIUM_CRYPTO_PWHASH_SCRYPTSALSA208SHA256_OPSLIMIT_INTERACTIVE = 534288
SODIUM_CRYPTO_PWHASH_SCRYPTSALSA208SHA256_MEMLIMIT_INTERACTIVE = 16777216
SODIUM_CRYPTO_PWHASH_SCRYPTSALSA208SHA256_OPSLIMIT_SENSITIVE = 33554432
SODIUM_CRYPTO_PWHASH_SCRYPTSALSA208SHA256_MEMLIMIT_SENSITIVE = 1073741824
SODIUM_CRYPTO_SCALARMULT_BYTES = 32
SODIUM_CRYPTO_SCALARMULT_SCALARBYTES = 32
SODIUM_CRYPTO_SHORTHASH_BYTES = 8
SODIUM_CRYPTO_SHORTHASH_KEYBYTES = 16
SODIUM_CRYPTO_SECRETBOX_KEYBYTES = 32
SODIUM_CRYPTO_SECRETBOX_MACBYTES = 16
SODIUM_CRYPTO_SECRETBOX_NONCEBYTES = 24
SODIUM_CRYPTO_SECRETSTREAM_XCHACHA20POLY1305_ABYTES = 17
SODIUM_CRYPTO_SECRETSTREAM_XCHACHA20POLY1305_HEADERBYTES = 24
SODIUM_CRYPTO_SECRETSTREAM_XCHACHA20POLY1305_KEYBYTES = 32
SODIUM_CRYPTO_SECRETSTREAM_XCHACHA20POLY1305_TAG_PUSH = 0
SODIUM_CRYPTO_SECRETSTREAM_XCHACHA20POLY1305_TAG_PULL = 1
SODIUM_CRYPTO_SECRETSTREAM_XCHACHA20POLY1305_TAG_REKEY = 2
SODIUM_CRYPTO_SECRETSTREAM_XCHACHA20POLY1305_TAG_FINAL = 3
SODIUM_CRYPTO_SECRETSTREAM_XCHACHA20POLY1305_MESSAGEBYTES_MAX = 274877906816
SODIUM_CRYPTO_SIGN_BYTES = 64
SODIUM_CRYPTO_SIGN_SEEDBYTES = 32
SODIUM_CRYPTO_SIGN_PUBLICKEYBYTES = 32
SODIUM_CRYPTO_SIGN_SECRETKEYBYTES = 64
SODIUM_CRYPTO_SIGN_KEYPAIRBYTES = 96
SODIUM_CRYPTO_STREAM_KEYBYTES = 32
SODIUM_CRYPTO_STREAM_NONCEBYTES = 24