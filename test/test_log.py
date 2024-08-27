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
import io
import sys
from src.log import Log


class TestLog(unittest.TestCase):
    def setUp(self):
        self.log = Log()

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_info_verbose(self, mock_stdout):
        self.log.setVerbose(True)
        self.log.info("Test message")
        self.assertEqual(mock_stdout.getvalue(), "INFO: Test message\n")


    @patch('sys.stdout', new_callable=io.StringIO)
    def test_info_not_verbose(self, mock_stdout):
        self.log.info("Test message")
        self.assertEqual(mock_stdout.getvalue(), "")


    @patch('sys.stdout', new_callable=io.StringIO)
    def test_error_not_silent(self, mock_stdout):
        self.log.error("Test error")
        self.assertEqual(mock_stdout.getvalue(), "ERROR: Test error\n")


    @patch('sys.stdout', new_callable=io.StringIO)
    def test_error_silent(self, mock_stdout):
        self.log.setSilent(True)
        self.log.error("Test error")
        self.assertEqual(mock_stdout.getvalue(), "")


    @patch('sys.stdout', new_callable=io.StringIO)
    def test_fatal(self, mock_stdout):
        with self.assertRaises(SystemExit) as cm:
            self.log.fatal("Fatal error")
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("!!! FATAL ERROR !!!", mock_stdout.getvalue())
        self.assertIn("message: Fatal error", mock_stdout.getvalue())
