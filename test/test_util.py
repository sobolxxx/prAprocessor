# MIT License

# Copyright (c) 2024 sobolxxx

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import unittest
from unittest.mock import patch
from src.util import *



class TestGetFirstNonWhitespaceSubstring(unittest.TestCase):
    def test_leading_whitespace(self):
        self.assertEqual(get_first_non_whitespace_substring("   Hello world"), "Hello")
    
    def test_trailing_whitespace(self):
        self.assertEqual(get_first_non_whitespace_substring("Hello world   "), "Hello")
    
    def test_middle_whitespace(self):
        self.assertEqual(get_first_non_whitespace_substring("   Hello   world"), "Hello")
    
    def test_no_whitespace(self):
        self.assertEqual(get_first_non_whitespace_substring("Hello"), "Hello")
    
    def test_empty_string(self):
        self.assertEqual(get_first_non_whitespace_substring(""), "")
    
    def test_only_whitespace(self):
        self.assertEqual(get_first_non_whitespace_substring("       "), "")
    
    def test_multiple_whitespace_characters(self):
        self.assertEqual(get_first_non_whitespace_substring("\t\n  \tHello\tWorld\n"), "Hello")



class TestGetStringAfterTagSafe(unittest.TestCase):
    @patch.object(log, 'fatal')
    def test_tag_found(self, mock_fatal):
        full_string = "abcdefghijk"
        tag = "cde"
        result = get_string_after_tag_safe(full_string, tag)
        self.assertEqual(result, "fghijk")
        mock_fatal.assert_not_called()
    
    @patch.object(log, 'fatal')
    def test_tag_not_found(self, mock_fatal):
        full_string = "abcdefghijk"
        tag = "xyz"
        result = get_string_after_tag_safe(full_string, tag)
        self.assertEqual(result, "")
        mock_fatal.assert_called_once()

    @patch.object(log, 'fatal')
    def test_tag_at_end(self, mock_fatal):
        full_string = "abcdefghijk"
        tag = "ijk"
        result = get_string_after_tag_safe(full_string, tag)
        self.assertEqual(result, "")
        mock_fatal.assert_not_called()

    @patch.object(log, 'fatal')
    def test_empty_string(self, mock_fatal):
        full_string = ""
        tag = "anytag"
        result = get_string_after_tag_safe(full_string, tag)
        self.assertEqual(result, "")
        mock_fatal.assert_called_once()

    @patch.object(log, 'fatal')
    def test_empty_tag(self, mock_fatal):
        full_string = "abcdefghijk"
        tag = ""
        result = get_string_after_tag_safe(full_string, tag)
        self.assertEqual(result, "abcdefghijk")
        mock_fatal.assert_not_called()



class TestRemoveAfter(unittest.TestCase):
    def test_tag_found(self):
        string = "abcdef#ghijk"
        after = "#"
        result = remove_after(string, after)
        self.assertEqual(result, "abcdef")
    
    def test_tag_not_found(self):
        string = "abcdefghijk"
        after = "#"
        result = remove_after(string, after)
        self.assertEqual(result, "abcdefghijk")
    
    def test_tag_at_end(self):
        string = "abcdef#"
        after = "#"
        result = remove_after(string, after)
        self.assertEqual(result, "abcdef")
    
    def test_empty_string(self):
        string = ""
        after = "#"
        result = remove_after(string, after)
        self.assertEqual(result, "")
    
    def test_empty_tag(self):
        string = "abcdefghijk"
        after = ""
        result = remove_after(string, after)
        self.assertEqual(result, "abcdefghijk")
    
    def test_tag_is_prefix(self):
        string = "#abcdef"
        after = "#"
        result = remove_after(string, after)
        self.assertEqual(result, "")
    
    def test_tag_is_prefix_with_space(self):
        string = " #abcdef"
        after = "#"
        result = remove_after(string, after)
        self.assertEqual(result, " ")
