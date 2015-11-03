#! /usr/bin/env python

"""
cipher.py

Written by Geremy Condra
Released on 18 March 2010
Licensed under MIT License

This module provides a basic interface to OpenSSL's EVP
cipher functions.

All the functions in this module raise CipherError on
malfunction.

From an end-user perspective, this module should be used
in situations where you want to have a single generally
human-readable or human-generated key used for both
encryption and decryption. 

This means that as a general rule, if your application 
involves transmitting this key over an insecure channel
you should not be using this module, but rather 
evpy.envelope.

Usage:

	>>> from evpy import cipher
	>>> message = b"this is data"
	>>> pw = b"mypassword"
	>>> salt, iv, enc = cipher.encrypt(message, pw)
	>>> cipher.decrypt(salt, iv, enc, pw)
	'this is data'
"""

import ctypes
import time

import AndroidCryptoevp


class CipherError(AndroidCryptoevp.SSLError):
	pass

def teardown():
	AndroidCryptoevp.EVP_cleanup();
	AndroidCryptoevp.ERR_free_strings()

def encrypt(data,aes_key, iv):
	"""Encrypts the given data, raising CipherError on failure.

	"""

	# build and initialize the context
	ctx = AndroidCryptoevp.EVP_CIPHER_CTX_new()
	if not ctx:
		raise CipherError("Could not create context")
	AndroidCryptoevp.EVP_CIPHER_CTX_init(ctx)

	# get the cipher object
	cipher_object = AndroidCryptoevp.EVP_aes_128_cbc()
	if not cipher_object:
		raise CipherError("Could not create cipher object")

	# finish the context and cipher object
	if not AndroidCryptoevp.EVP_EncryptInit_ex(ctx, cipher_object, None, aes_key, iv):
		raise CipherError("Could not finish context")

	# build the output buffer
	buf =ctypes.create_string_buffer(len(data) + 16)
	written = ctypes.c_int(0)
	final = ctypes.c_int(0)

	# update
	if not AndroidCryptoevp.EVP_EncryptUpdate(ctx, buf, ctypes.byref(written), data, len(data)):
		raise CipherError("Could not update ciphertext")
	output = buf.raw[:written.value]

	# finalize
	if not AndroidCryptoevp.EVP_EncryptFinal_ex(ctx, buf, ctypes.byref(final)):
		raise CipherError("Could not finalize ciphertext")
	output += buf.raw[:final.value]

	# ...and go home
	return output


def decrypt(data,key, iv):
	"""Decrypts the given data, raising CipherError on failure.
	

	"""
	# ensure inputs are the correct size
	if not len(data):
		raise CipherError("Data must actually exist")

	# build and initialize the context
	ctx = AndroidCryptoevp.EVP_CIPHER_CTX_new()
	if not ctx:
		raise CipherError("Could not create context")
	AndroidCryptoevp.EVP_CIPHER_CTX_init(ctx)

	# get the cipher object
	cipher_object = AndroidCryptoevp.EVP_aes_128_cbc()
	if not cipher_object:
		raise CipherError("Could not create cipher object")

	# start decrypting the ciphertext
	if not AndroidCryptoevp.EVP_DecryptInit_ex(ctx, cipher_object, None, key, iv):
		raise CipherError("Could not open envelope")

	# build the output buffers
	buf = ctypes.create_string_buffer(len(data) + 16)
	written = ctypes.c_int(0)
	final = ctypes.c_int(0)

	# update
	if not AndroidCryptoevp.EVP_DecryptUpdate(ctx, buf, ctypes.byref(written), data, len(data)):
		raise CipherError("Could not update plaintext")
	output = buf.raw[:written.value]

	# finalize
	if not AndroidCryptoevp.EVP_DecryptFinal_ex(ctx, buf, ctypes.byref(final)):
		raise CipherError("Could not finalize decryption")
	output += buf.raw[:final.value]

	return output