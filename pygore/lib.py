# Copyright 2019 The GoRE.tk Authors. All rights reserved.
# Use of this source code is governed by the license that
# can be found in the LICENSE file.

import pygore.internal as internal
from ctypes import c_char_p
from enum import Enum


class Kind(Enum):
    Invalid = 0
    Bool = 1
    Int = 2
    Int8 = 3
    Int16 = 4
    Int32 = 5
    Int64 = 6
    Uint = 7
    Uint8 = 8
    Uint16 = 9
    Uint32 = 10
    Uint64 = 11
    Uintptr = 12
    Float32 = 13
    Float64 = 14
    Complex64 = 15
    Complex128 = 16
    Array = 17
    Chan = 18
    Func = 19
    Interface = 20
    Map = 21
    Ptr = 22
    Slice = 23
    String = 24
    Struct = 25
    UnsafePointer = 26
    KindEnd = 27


class ChanDir(Enum):
    ChanRecv = 1 << 0
    ChanSend = 1 << 1
    ChanBoth = (1 << 0) | (1 << 1)


class CompilerVersion:
    '''
    CompilerVersion is a representation of the Go compiler used to compile
    the binary

    Attributes
    ----------
    name : str
        the go versions string for the compiler version.
    sha : str
        the git sha hash of the release commit.
    timestamp : str
        string of the time stamp the git tag was committed.
    '''
    def __init__(self, name, sha, timestamp):
        '''
        Parameters
        ----------
        name : str
            the go version string.
        sha : str
            the sha hash of the release commit.
        timestamp : str
            the time stamp the git tag was committed.
        '''
        self.name = name
        self.sha = sha
        self.timestamp = timestamp


class Function:
    '''
    Function is a representation of a Go function.

    Attributes
    ----------
    name : str
        the extracted function name.
    line_length : int
        the number of source code lines for the function.
    line_start : int
        the starting source code line number for the function.
    line_end : int `json:"srcEnd"`
        the ending source code line number for the function.
    offset : int
        the starting location for the subroutine in the binary.
    end : int
        the end location for the subroutine in the binary.
    filename : str
        the name of the source code file for the function.
    package_name : str
        the name of the Go package the function belongs to.
    '''
    def __init__(self, name, line_length, line_start, line_end,
                 offset, end, filename, package_name):
        self.name = name
        self.line_length = line_length
        self.line_start = line_start
        self.line_end = line_end
        self.offset = offset
        self.end = end
        self.filename = filename
        self.package_name = package_name


class Method(Function):
    '''
    Method is a representation of a go method.

    Attributes
    ----------
    name : str
        the extracted method name.
    line_length : int
        the number of source code lines for the method.
    line_start : int
        the starting source code line number for the method.
    line_end : int `json:"srcend"`
        the ending source code line number for the method.
    offset : int
        the starting location for the subroutine in the binary.
    end : int
        the end location for the subroutine in the binary.
    filename : str
        the name of the source code file for the method.
    package_name : str
        the name of the go package the method belongs to.
    receiver : str
        the name of the method receiver.
    '''
    def __init__(self, name, line_length, line_start, line_end,
                 offset, end, filename, package_name, receiver):
        self.receiver = receiver
        super().__init__(name, line_length, line_start, line_end, offset, end,
                         filename, package_name)


class Package:
    '''
    Package is a representation of a Go package.

    Attributes
    ----------
    name : str
        the extracted package name.
    filepath : str
        the extracted file path for the package.
    functions : list of Function
        a list of functions that are part of the package.
    methods : list of Method
        a list of methods that are part of the package.
    '''
    def __init__(self, name, filepath, functions, methods):
        self.name = name
        self.filepath = filepath
        self.functions = functions
        self.methods = methods


class Method_Type:
    '''
    Method-Type is the description of a method owned by the Type.
    It holds the method type information.

    Attributes
    ----------
    name : str
        the string name for the method.
    type : Type
        the specific function type for the method.  This can be None. If it is
        None, the method is not part of an implementation of an interface or it
        is not exported.
    ifaceOffset : int
        the offset from the beginning of the .text section where the function
        code starts. According to code comments in the standard library, it is
        used for interface calls.  Can be 0 if the code is not called in the
        binary and was optimized out by the compiler or linker.
    funcOffset : int
        the offset from the beginning of the .text section where the function
        code starts. According to code comments in the standard library, it is
        used for normal method calls.  Can be 0 if the code is not called in
        the binary and was optimized out by the compiler or linker.
    '''
    def __init__(self, name, type, ifaceOffset, funcOffset):
        self.name = name
        self.type = type
        self.ifaceOffset = ifaceOffset
        self.funcOffset = funcOffset


class Type:
    '''
    Type is a representation of all types in Go.

    Attributes
    ----------
    kind : Kind
        indicates the specific kind of type the Type
    name : str
        the name of the type.
    addr : int
        the virtual address to where the type struct is defined.
    ptrResolved : int
        the address to where the resolved structure is located if the Type is
        of pointer kind.
    packagePath : str
        the name of the package import path for the GoType.
    fields : list of Type
        is a list of the struct fields if the Type is of kind struct.
    fieldName : str
        the name of the field if the Type is a struct field.
    fieldTag : str
        holds the extracted tag for the field.
    fieldAnon : boolean
        is true if the field does not have a name and is an embedded type.
    element : Type
        the element type for arrays, sliceis chans or the resolved type for a
        pointer type. For example int if the slice is a []int.
    length : int
        the array or slice length.
    chanDir : ChanDir
        the channel direction.
    key : Type
        the key type for a map.
    funcArgs : list of Type
        the argument types for the function if the type is a function kind.
    funcReturns : list of Type
        the return types for the function if the type is a function kind.
    isVariadic : boolean
        true if the last argument type is variadic. For example "func(s
        striing, n ...int)"
    methods : list of Method_Type
        holds information of the types methods.
    '''
    def __init__(self, kind=None, name=None, addr=None,
                 ptrResolved=None, packagePath=None, fields=None,
                 fieldName=None, fieldTag=None, fieldAnon=None,
                 element=None, length=None, chanDir=None, key=None,
                 funcArgs=None, funcReturns=None, isVariadic=None):
        self.kind = kind
        self.name = name
        self.addr = addr
        self.ptrResolved = ptrResolved
        self.packagePath = packagePath
        self.fields = fields
        self.fieldName = fieldName
        self.fieldTag = fieldTag
        self.fieldAnon = fieldAnon
        self.element = element
        self.length = length
        self.chanDir = chanDir
        self.key = key
        self.funcArgs = funcArgs
        self.funcReturns = funcReturns
        self.isVariadic = isVariadic


class GoFile:
    '''
    GoFile is a representation of a Go binary file.

    Attributes
    ----------
    path : str
        path to the binary.
    '''
    def __init__(self, path):
        self.path = path.encode('utf-8')
        internal._c_open(self.path)

    def close(self):
        '''
        Closes the file handler and freeing up all memory allocated by the Go
        runtime and objects on the C-heap. This must be called when done with
        the files, otherwise it will lead to memory leak.
        '''
        internal._c_close(self.path)
        self.path = None

    def set_compiler_version(self, version):
        '''
        Set an assumed compiler version to be used when extracting information
        from the binary.
        '''
        c_ver = c_char_p(version.encode('utf-8'))
        v = internal._c_setCompilerVersion(self.path, c_ver)
        if v != 0:
            return True
        return False

    def get_compiler_version(self):
        '''
        Returns compiler information extracted from the binary.
        '''
        return _get_compiler_version(self.path)

    def get_packages(self):
        '''
        Returns all Go packages gore thinks is part of the main project.
        '''
        pps = internal._c_getPackages(self.path)
        return _parsePackages(pps)

    def get_vendor_packages(self):
        '''
        Returns all Go packages gore thinks is vendor or 3rd-party packages.
        '''
        pps = internal._c_getVendors(self.path)
        return _parsePackages(pps)

    def get_std_lib_packages(self):
        '''
        Returns all Go packages gore thinks is standard library packages.
        '''
        pps = internal._c_getstd(self.path)
        return _parsePackages(pps)

    def get_unknown_packages(self):
        '''
        Returns all Go packages gore could not classify.
        '''
        pps = internal._c_getunknown(self.path)
        return _parsePackages(pps)

    def get_types(self):
        '''
        Returns all Go types extracted from the binary.
        '''
        types = internal._c_getTypes(self.path)
        cache = dict()
        return _parseTypes(types, cache)

    def get_build_id(self):
        '''
        Returns the extracted build id from the binary.
        '''
        return str(internal._c_build_id(self.path).decode('utf-8', 'replace'))


def _get_compiler_version(path):
    pcv = internal._c_getCompilerVersion(path)
    cv = pcv.contents
    return CompilerVersion(str(cv.name.decode('utf-8', 'replace')),
                           str(cv.sha.decode('utf-8', 'replace')),
                           str(cv.timestamp.decode('utf-8', 'replace')))


def _parsePackages(pps):
    pkgs = []
    for i in range(pps.contents.length):
        fcks = []
        meths = []
        p = pps.contents.packages[i][0]

        # Functions
        for j in range(p.numFuncs):
            f = p.functions[j][0]
            name = str(f.name.decode('utf-8', 'replace'))
            srcl = int(f.srcLineLength)
            srcs = int(f.srcLineStart)
            srce = int(f.srcLineEnd)
            off = int(f.offset)
            end = int(f.end)
            fn = str(f.fileName.decode('utf-8', 'replace'))
            pn = str(f.packageName.decode('utf-8', 'replace'))
            fcks.append(Function(name, srcl, srcs, srce, off, end,
                                 fn, pn))
        # Methods
        for j in range(p.numMeths):
            f = p.methods[j][0]
            name = str(f.function[0].name.decode('utf-8', 'replace'))
            srcl = int(f.function[0].srcLineLength)
            srcs = int(f.function[0].srcLineStart)
            srce = int(f.function[0].srcLineEnd)
            off = int(f.function[0].offset)
            end = int(f.function[0].end)
            fn = str(f.function[0].fileName.decode('utf-8', 'replace'))
            pn = str(f.function[0].packageName.decode('utf-8', 'replace'))
            rec = str(f.receiver.decode('utf-8', 'replace'))
            meths.append(Method(name, srcl, srcs, srce, off, end,
                                fn, pn, rec))

        # Package
        name = str(p.name.decode('utf-8', 'replace'))
        fp = str(p.filepath.decode('utf-8', 'replace'))
        pkgs.append(Package(name, fp, fcks, meths))
    return pkgs


def _parse_method_type(ms, cache):
    methods = []
    for i in range(ms.contents.length):
        m = ms.contents.methods[i][0]
        typ = _convert_type(m.gotype.contents, cache) if m.gotype else None
        methods.append(Method_Type(str(m.name.decode('utf-8', 'replace')), typ,
                                   int(m.ifaceAddr), int(m.funcAddr)))
    return methods


def _convert_type(t, cache):
    try:
        return cache[int(t.addr)]
    except KeyError:
        pass

    typ = Type()
    typ.addr = int(t.addr)
    typ.kind = Kind(t.kind)
    typ.name = str(t.name.decode('utf-8', 'replace'))
    typ.ptrResolved = int(t.ptrResolved)
    typ.packagePath = str(t.packagePath.decode('utf-8', 'replace'))

    # If the type is a struct and has fields, extract field information.
    if t.kind == Kind.Struct and t.fields:
        typ.fields = []
        for i in range(t.fields.contents.length):
            field = t.fields.contents.types[i].contents
            f = Type()
            f.fieldName = str(field.fieldName.decode('utf-8', 'replace'))
            if field.fieldTag:
                f.fieldTag = str(field.fieldTag.decode('utf-8', 'replace'))
            f.typeAnon = True if field.fieldAnon > 0 else False
            f.kind = Kind(field.kind)
            f.addr = int(field.addr)
            f.name = str(field.name.decode('utf-8', 'replace'))
            typ.fields.append(f)

    typ.length = int(t.length)
    if t.chanDir != 0:
        typ.chanDir = ChanDir(t.chanDir)

    cache[int(t.addr)] = typ
    
    typ.isVariadic = True if t.isVariadic > 0 else False
    typ.element = _convert_type(t.element.contents,
                                cache) if t.element else None
    typ.key = _convert_type(t.key.contents,
                            cache) if t.key else None
    typ.funcArgs = _parseTypes(t.funcArgs, cache) if t.funcArgs else None
    typ.funcReturns = _parseTypes(t.funcReturns,
                                  cache) if t.funcReturns else None
    typ.methods = _parse_method_type(t.methods, cache) if t.methods else None

    return typ


def _parseTypes(types, cache):
    vals = []
    for i in range(types.contents.length):
        t = types.contents.types[i][0]
        vals.append(_convert_type(t, cache))
    return vals
