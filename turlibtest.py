# -*- coding: utf-8 -*-
import unittest
import turlib

class TurlibTest(unittest.TestCase):
    def test_get_base_url(self):
        url ="http://www.gamet.com.tr/gelecege-donus/"
        base_url = "http://www.gamet.com.tr"
        self.assertEqual(base_url, turlib.get_base_url(url))
        self.assertEqual("www.google.com",turlib.get_base_url("www.google.com/testing/retesting/x/"))

if __name__ == "__main__":
    unittest.main()

