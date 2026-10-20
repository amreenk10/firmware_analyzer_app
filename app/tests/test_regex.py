import unittest
from app.tests.test_base import BaseTestCase
from app.services.analyzer import TOKEN_REGEX

class TestTokenRegex(BaseTestCase):
    def test_regex_matching_rules(self):
        self.assertTrue(bool(TOKEN_REGEX.match("<Tkn435JFIRKTkn>")))
        self.assertFalse(bool(TOKEN_REGEX.match("<Tkn435jfirkTkn>")), "Rejected: contained lowercase letters.")
        self.assertFalse(bool(TOKEN_REGEX.match("<Tkn43JFIRKTkn>")), "Rejected: missing third digit.")
        self.assertFalse(bool(TOKEN_REGEX.match("<Tkn435JFIRTkn>")), "Rejected: missing fifth capital letter.")

if __name__ == '__main__':
    unittest.main()
