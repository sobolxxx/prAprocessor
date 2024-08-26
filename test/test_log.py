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
