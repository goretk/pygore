import pygore

testfile = '/path/to/file'

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
