[![Build Status](https://github.com/goretk/pygore/actions/workflows/cicd.yml/badge.svg)](https://github.com/goretk/pygore/actions/workflows/cicd.yml)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pygore)
![PyPI](https://img.shields.io/pypi/v/pygore)
# pyGoRE - Python library for analyzing Go binaries

## How to use

1. Use `pip install pygore` to download and install the library.
2. Import it into your project.
3. Write a new cool tool.

### Sample code
```python
import pygore

testfile = '/path/to/go/binary/file'

f = pygore.GoFile(testfile)
c = f.get_compiler_version()

print('Compiler: {}\nTimestamp: {}\nSHA {}\n'.
      format(c.name, c.timestamp, c.sha))

pkgs = f.get_packages()
types = f.get_types()
f.close()
for p in pkgs:
    print('Package: {}'.format(p.name))
    print("Functions:")
    for f in p.functions:
        print('{} from {} to {}'.format(f.name, hex(f.offset), hex(f.end)))
    print("Methods:")
    for m in p.methods:
        print('{} {} from {} to {}'.format(m.receiver, m.name,
                                           hex(m.offset), hex(m.end)))
    print("Types:")
    for t in types:
        print('Package path: {} | Type name: {}'.format(t.packagePath, t.name))
```

