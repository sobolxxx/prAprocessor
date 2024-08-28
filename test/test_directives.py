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
from unittest.mock import create_autospec, patch
from src.directives import *
from src.log import log
from src.util import *
from src.context import context



class TestParseDirective(unittest.TestCase):
    @patch.object(log, 'error')
    def test_integration_parse_directive_valid(self, mock_error):
        result = parse_directive("some_text # other_text")
        self.assertEqual(result, "some_text")
        mock_error.error.assert_not_called()

    @patch.object(log, 'error')
    def test_parse_directive_no_hash(self, mock_error):
        result = parse_directive("some text without hash")
        self.assertEqual(result, "")
        mock_error.assert_called_once()



class TestHandlers(unittest.TestCase):
    def setUp(self):
        # todo this is not threadsafe
        context.reset()
        log.setSilent(True)

    def tearDown(self):
        # todo this is not threadsafe
        context.reset()
        log.setSilent(False)


    def test_all_directives_proper(self):
        self.assertEqual(len(all_directives), len(handlers))
        for item in all_directives:
            self.assertTrue(item in handlers)


    @patch.object(log, 'error')
    def test_integration_after_defined_ifdef_context_ifdefed_false(self, mock_error):
        # todo not threadsafe due to global context
        # todo should be unit test with mocked dependencies

        context.set_global_variable("var1", True)
        self.assertFalse(context.ifdefed())

        result = ifdef_handler("var1#")
        self.assertTrue(result)
        self.assertFalse(context.ifdefed())
        mock_error.assert_not_called()


    @patch.object(log, 'error')
    def test_integration_after_undefined_ifdef_context_ifdefed_true(self, mock_error):
        # todo not threadsafe due to global context
        # todo should be unit test with mocked dependencies

        self.assertFalse(context.ifdefed())

        result = ifdef_handler("var1#")
        self.assertTrue(result)
        self.assertTrue(context.ifdefed())
        mock_error.assert_not_called()


    @patch.object(log, 'error')
    def test_integration_ifdef_should_require_variable_name(self, mock_error):
        # todo should be unit test with mocked dependencies
        result = ifdef_handler("#")
        self.assertFalse(result)
        mock_error.assert_called()
    

    @patch.object(log, 'error')
    def test_integration_after_defined_ifndef_context_ifdefed_true(self, mock_error):
        # todo not threadsafe due to global context
        # todo should be unit test with mocked dependencies

        context.set_global_variable("var1", True)
        self.assertFalse(context.ifdefed())

        result = ifndef_handler("var1#")
        self.assertTrue(result)
        self.assertTrue(context.ifdefed())
        mock_error.assert_not_called()


    @patch.object(log, 'error')
    def test_integration_after_undefined_ifndef_context_ifdefed_false(self, mock_error):
        # todo not threadsafe due to global context
        # todo should be unit test with mocked dependencies

        self.assertFalse(context.ifdefed())

        result = ifndef_handler("var1#")
        self.assertTrue(result)
        self.assertFalse(context.ifdefed())
        mock_error.assert_not_called()


    @patch.object(log, 'error')
    def test_integration_ifndef_should_require_variable_name(self, mock_error):
        # todo should be unit test with mocked dependencies
        result = ifndef_handler("#")
        self.assertFalse(result)
        mock_error.assert_called()
    

    @patch.object(log, 'error')
    def test_integration_endif_should_pop_from_ifdef_stack_and_return_true(self, mock_error):
        # todo not threadsafe due to global context
        # todo should be unit test with mocked dependencies

        context.push_stack("var1", True)
        result = endif_handler("#")
        self.assertTrue(result)
        self.assertFalse(context.ifdefed())

    @patch.object(log, 'error')
    def test_get_directive_proper_input_returns_proper_directive(self, mock_error):
        result = get_directive("#ifdef A#")
        self.assertEqual(result, "#ifdef")
        result = get_directive("#endif#")
        self.assertEqual(result, "#endif")
        mock_error.assert_not_called()


    @patch.object(log, 'error')
    def test_get_directive_proper_input_with_additional_text_returns_proper_directive(self, mock_error):
        # todo - this actually should not happen in the future, there are two options:
        # 1) either prevent having anything apart from directive in a line - but then its tricky to make it language agnostic
        # 2) or allow constructs like #ifdef A# x = 10 #endif# with multiple directives
        result = get_directive("   asdf #ifdef A# ljkjf")
        self.assertEqual(result, "#ifdef")
        result = get_directive("lkjdklsjf#endif#   ")
        self.assertEqual(result, "#endif")
        mock_error.assert_not_called()

    @patch.object(log, 'error')
    def test_get_directive_proper_input_without_directive_returns_none_without_error(self, mock_error):
        result = get_directive("ifdef something whatever not a directive")
        self.assertEqual(result, None)
        result = get_directive("something endif #comment")
        self.assertEqual(result, None)
        mock_error.assert_not_called()

    @patch.object(log, 'error')
    def test_get_directive_multiple_directives_returns_none_with_error(self, mock_error):
        result = get_directive("  #ifdef something whatever #endif ")
        self.assertEqual(result, None)
        self.assertEqual(mock_error.call_count, 1)
        result = get_directive(" #endif asdf #ifndef ")
        self.assertEqual(result, None)
        self.assertEqual(mock_error.call_count, 2)
