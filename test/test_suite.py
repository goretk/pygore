import unittest
import os

import pygore

golden_file = os.path.dirname(__file__) + '/' + 'resources/golden'
gold_build_id = ('W11rzA8dxCieF64mk9rO/wmqBULPx6tMOdPbSBabM/X40xrZ4nVRHkrWOKb'
                 'wZw/JpQDPeWBsrG9Rn_jzf3s')


class TestPyGore(unittest.TestCase):
    def setUp(self):
        self.file = pygore.GoFile(golden_file)

    def tearDown(self):
        self.file.close()

    def test_compiler(self):
        cv = self.file.get_compiler_version()
        self.assertEqual(cv.name, 'go1.12', msg='Wrong version')

    def test_package(self):
        pkgs = self.file.get_packages()
        self.assertEqual(len(pkgs), 1, msg='Wrong number of packages')
        self.assertEqual(pkgs[0].filepath, '/build', msg='Wrong path')
        self.assertEqual(len(pkgs[0].functions), 2, msg='Should have 2 funcs')
        self.assertEqual(len(pkgs[0].methods), 1, msg='Should have 1 meth')
        m = pkgs[0].methods[0]
        self.assertEqual(m.name, 'String', msg='Wrong method name')
        self.assertEqual(m.receiver, '(*simpleStruct)', msg='Wrong receiver')

    def test_types(self):
        typs = self.file.get_types()
        ss = None
        cs = None
        for t in typs:
            if t.name == 'main.myComplexStruct':
                cs = t
                self.assertEqual(t.kind, pygore.Kind.Struct)
            elif t.name == 'main.simpleStruct':
                ss = t
                self.assertEqual(t.kind, pygore.Kind.Struct)

        self.assertIsNotNone(ss, msg='Types should include simpleStruct')
        self.assertIsNotNone(cs, msg='Types should include myComplexStruct')

    def test_build_id(self):
        build_id = self.file.get_build_id()
        self.assertEqual(gold_build_id, build_id)

class TestBug14(unittest.TestCase):
    def setUp(self):
        golden_file = os.path.dirname(__file__) + '/' + 'resources/bettercap'
        self.file = pygore.GoFile(golden_file)

    def tearDown(self):
        self.file.close()

    def test_blank_field_name(self):
        types = self.file.get_types()
        for t in types:
            if t.fields is None:
                continue
            for f in t.fields:
                pass
                self.assertIsNot(f.fieldName, "", msg="Empty field name for {} field".format(t.name))


if __name__ == '__main__':
    unittest.main()
