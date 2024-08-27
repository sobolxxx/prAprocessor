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
from src.context import Context
from src.log import log



class TestContexBasicOperations(unittest.TestCase):
    
    def setUp(self):
        self.context = Context()


    @patch.object(log, 'info')
    def test_on_file_start(self, _):
        filename = "testfile.txt"
        self.context.on_file_start(filename)
        self.assertEqual(self.context.currently_processed_filename, filename)
        self.assertEqual(self.context.local_context, {})


    @patch.object(log, 'info')
    def test_on_file_end(self, _):
        filename = "testfile.txt"
        self.context.on_file_start(filename)        
        self.context.on_file_end()
        self.assertEqual(self.context.currently_processed_filename, "")
        self.assertEqual(self.context.local_context, {})


    @patch.object(log, 'info')
    def test_on_file_start_dirty_context(self, _):
        filename = "testfile.txt"
        self.context.local_context = {'a': 'aa', 'b': 'bb'}
        self.context.on_file_start(filename)
        self.assertEqual(self.context.currently_processed_filename, filename)
        self.assertEqual(self.context.local_context, {})


    @patch.object(log, 'info')
    def test_set_global_variable(self, _):
        var_name = "global_var"
        value = True
        self.context.set_global_variable(var_name, value)
        self.assertEqual(self.context.global_context, {var_name: value})

    @patch.object(log, 'info')
    def test_set_local_variable(self, _):
        var_name = "local_var"
        value = False
        self.context.set_local_variable(var_name, value)
        self.assertEqual(self.context.local_context, {var_name: value})

    @patch.object(log, 'info')
    def test_is_variable_set_global_true(self, _):
        var_name = "global_var"
        self.context.set_global_variable(var_name, True)
        result = self.context.is_variable_set(var_name)
        self.assertTrue(result)

    @patch.object(log, 'info')
    def test_is_variable_set_local_true(self, _):
        var_name = "local_var"
        self.context.set_local_variable(var_name, True)
        result = self.context.is_variable_set(var_name)
        self.assertTrue(result)

    @patch.object(log, 'info')
    def test_is_variable_set_global_false_when_set_to_false(self, _):
        var_name = "global_var"
        self.context.set_global_variable(var_name, False)
        result = self.context.is_variable_set(var_name)
        self.assertFalse(result)

    @patch.object(log, 'info')
    def test_is_variable_set_local_false_when_set_to_false(self, _):
        var_name = "local_var"
        self.context.set_local_variable(var_name, False)
        result = self.context.is_variable_set(var_name)
        self.assertFalse(result)

    @patch.object(log, 'info')
    def test_is_variable_set_not_set(self, _):
        var_name = "non_existent_var"
        result = self.context.is_variable_set(var_name)
        self.assertFalse(result)




class TestContextIfdefStack(unittest.TestCase):
    
    def setUp(self):
        self.context = Context()


    @patch.object(log, 'info')
    def test_empty_stack_ifdefed(self, _):
        self.assertFalse(self.context.ifdefed())  

    @patch.object(log, 'info')
    def test_push_stack(self, _):
        var_name = "test_var"
        ifdefed = True
        self.context.push_stack(var_name, ifdefed)
        self.assertEqual(self.context.ifdef_stack, [(var_name, ifdefed)])
        self.assertTrue(self.context.ifdefed())

    @patch.object(log, 'info')
    def test_pop_stack(self, _):
        self.context.push_stack("test_var", True)
        result = self.context.pop_stack()
        self.assertEqual(result, "test_var")
        self.assertEqual(self.context.ifdef_stack, [])
        self.assertFalse(self.context.ifdefed())

    @patch.object(log, 'error')
    def test_pop_stack_empty(self, mock_error):
        result = self.context.pop_stack()
        mock_error.assert_called_once()
        self.assertEqual(self.context.ifdef_stack, [])
        self.assertEqual(result, "")


    @patch.object(log, 'info')
    @patch.object(log, 'error')
    def test_stack_push_pop_sequence(self, mock_error, _):
        self.context.push_stack("var1", False)
        self.assertEqual(self.context.ifdefed(), False)

        self.context.push_stack("var2", False)
        self.assertEqual(self.context.ifdefed(), False)

        self.context.push_stack("var3", True)
        self.assertEqual(self.context.ifdefed(), True)

        self.context.push_stack("var4", False)
        self.assertEqual(self.context.ifdefed(), True)

        res = self.context.pop_stack()
        self.assertEqual(self.context.ifdefed(), True)
        self.assertEqual(res, "var4")

        res = self.context.pop_stack()
        self.assertEqual(self.context.ifdefed(), False)
        self.assertEqual(res, "var3")

        self.context.push_stack("var5", True)
        self.assertEqual(self.context.ifdefed(), True)

        res = self.context.pop_stack()
        self.assertEqual(self.context.ifdefed(), False)
        self.assertEqual(res, "var5")

        res = self.context.pop_stack()
        self.assertEqual(self.context.ifdefed(), False)
        self.assertEqual(res, "var2")

        res = self.context.pop_stack()
        self.assertEqual(self.context.ifdefed(), False)
        self.assertEqual(res, "var1")

        result = self.context.pop_stack()
        mock_error.assert_called_once()
        self.assertEqual(self.context.ifdef_stack, [])
        self.assertEqual(result, "")
