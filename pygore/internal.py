# Copyright 2019 The GoRE.tk Authors. All rights reserved.
# Use of this source code is governed by the license that
# can be found in the LICENSE file.

import os
from sys import platform
from ctypes import Structure, POINTER, c_char_p, c_int, c_uint, c_ulong, \
                   c_ulonglong, c_void_p, cdll

libFile = ""

if platform == 'linux' or platform == 'linux2':
    libFile = 'libgore.so'
elif platform == 'win32':
    libFile = 'libgore.dll'
elif platform == 'darwin':
    libFile = 'libgore.dylib'
else:
    raise Exception('{} not supported'.format(platform))

lib = cdll.LoadLibrary(os.path.dirname(__file__) + '/' + libFile)


class _CompilerVersion(Structure):
    _fields_ = [('name',  c_char_p),
                ('sha', c_char_p),
                ('timestamp', c_char_p)]


class _Function(Structure):
    _fields_ = [('name', c_char_p),
                ('srcLineLength', c_int),
                ('srcLineStart', c_int),
                ('srcLineEnd', c_int),
                ('offset', c_ulonglong),
                ('end', c_ulonglong),
                ('fileName', c_char_p),
                ('packageName', c_char_p)]


class _Method(Structure):
    _fields_ = [('receiver', c_char_p),
                ('function', POINTER(_Function))]


class _Package(Structure):
    _fields_ = [('name', c_char_p),
                ('filepath', c_char_p),
                ('functions', POINTER(POINTER(_Function))),
                ('methods', POINTER(POINTER(_Method))),
                ('numFuncs', c_ulong),
                ('numMeths', c_ulong)]


class _Packages(Structure):
    _fields_ = [('packages', POINTER(POINTER(_Package))),
                ('length', c_ulong)]


class _Type(Structure):
    pass


class _Types(Structure):
    pass


class _Method_Type(Structure):
    _fields_ = [('name', c_char_p),
                ('gotype', POINTER(_Type)),
                ('ifaceAddr', c_ulonglong),
                ('funcAddr', c_ulonglong)]


class _Methods_Type(Structure):
    _fields_ = [('methods', POINTER(POINTER(_Method_Type))),
                ('length', c_ulong)]


_Type._fields_ = [('kind', c_uint),
                  ('name', c_char_p),
                  ('addr', c_ulonglong),
                  ('ptrResolved', c_ulonglong),
                  ('packagePath', c_char_p),
                  ('fields', POINTER(_Types)),
                  ('fieldName', c_char_p),
                  ('fieldTag', c_char_p),
                  ('fieldAnon', c_int),
                  ('element', POINTER(_Type)),
                  ('length', c_int),
                  ('chanDir', c_int),
                  ('key', POINTER(_Type)),
                  ('funcArgs', POINTER(_Types)),
                  ('funcReturns', POINTER(_Types)),
                  ('isVariadic', c_int),
                  ('methods', POINTER(_Methods_Type))]


_Types._fields_ = [('types', POINTER(POINTER(_Type))),
                   ('length', c_ulong)]


# Call top open a go file.
_c_open = lib.gore_open
_c_open.argtypes = [c_char_p]

# Call top open a go file.
_c_close = lib.gore_close
_c_close.argtypes = [c_char_p]

# Call to set the compiler version
_c_setCompilerVersion = lib.gore_setGoVersion
_c_setCompilerVersion.argtypes = [c_void_p, c_void_p]
_c_setCompilerVersion.restype = c_int

# Call to get compiler version.
_c_getCompilerVersion = lib.gore_getCompilerVersion
_c_getCompilerVersion.argtypes = [c_void_p]
_c_getCompilerVersion.restype = POINTER(_CompilerVersion)

# Call to get packages.
_c_getPackages = lib.gore_getPackages
_c_getPackages.argtypes = [c_void_p]
_c_getPackages.restype = POINTER(_Packages)

# Call to get vendor packages.
_c_getVendors = lib.gore_getVendors
_c_getVendors.argtypes = [c_void_p]
_c_getVendors.restype = POINTER(_Packages)

# Call to get standard library packages.
_c_getstd = lib.gore_getSTDLib
_c_getstd.argtypes = [c_void_p]
_c_getstd.restype = POINTER(_Packages)

# Get packages that failed to be classified.
_c_getunknown = lib.gore_getUnknown
_c_getunknown.argtypes = [c_void_p]
_c_getunknown.restype = POINTER(_Packages)

# Get types
_c_getTypes = lib.gore_getTypes
_c_getTypes.argtypes = [c_void_p]
_c_getTypes.restype = POINTER(_Types)

# Get Build ID
_c_build_id = lib.gore_build_id
_c_build_id.argtypes = [c_void_p]
_c_build_id.restype = c_char_p
