import unittest
from abap_parser import parse_abap_file, parse_object_base

class TestAbapParser(unittest.TestCase):
    def test_parse_abap_file(self):
        counts = parse_abap_file('sample.abap')
        self.assertEqual(counts['form'], 1)
        self.assertEqual(counts['class'], 1)
        self.assertEqual(counts['function'], 0)

    def test_parse_object_base(self):
        objects = parse_object_base('object_base.txt')
        self.assertIn(('CL_EXAMPLE', 'class'), objects)
        self.assertIn(('ZFUNC_EXAMPLE', 'function'), objects)
        self.assertIn(('ZREPORT_EXAMPLE', 'report'), objects)

if __name__ == '__main__':
    unittest.main()
