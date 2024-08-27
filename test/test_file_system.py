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
import os
import tempfile
import shutil
from unittest.mock import Mock
from src.file_system import create_file_with_content, for_each_file_recursive, wipeout
from src.log import log


class TestCreateFileWithContent(unittest.TestCase):
    def setUp(self):
        log.setSilent(True)
        self.test_dir = tempfile.mkdtemp()


    def tearDown(self):
        log.setSilent(False)
        shutil.rmtree(self.test_dir)


    def test_create_new_file(self):
        file_path = os.path.join(self.test_dir, "new_file.txt")
        content = "Hello, World!"
        result = create_file_with_content(file_path, content)
        
        self.assertTrue(result)
        self.assertTrue(os.path.exists(file_path))
        with open(file_path, 'r') as f:
            self.assertEqual(f.read(), content)


    def test_create_file_in_new_directory(self):
        file_path = os.path.join(self.test_dir, "new_dir", "new_file.txt")
        content = "New content"
        result = create_file_with_content(file_path, content)
        
        self.assertTrue(result)
        self.assertTrue(os.path.exists(file_path))
        with open(file_path, 'r') as f:
            self.assertEqual(f.read(), content)


    def test_overwrite_existing_file(self):
        file_path = os.path.join(self.test_dir, "existing_file.txt")
        initial_content = "Initial content"
        with open(file_path, 'w') as f:
            f.write(initial_content)

        new_content = "New content"
        result = create_file_with_content(file_path, new_content)
        
        self.assertTrue(result)
        with open(file_path, 'r') as f:
            self.assertEqual(f.read(), new_content)


    def test_error_handling(self):
        # Create a directory with the same name as the file we want to create
        file_path = os.path.join(self.test_dir, "error_case")
        os.mkdir(file_path)
        
        result = create_file_with_content(file_path, "Some content")
        self.assertFalse(result)



class TestForEachFileRecursive(unittest.TestCase):
    def setUp(self):
        log.setSilent(True)
        self.test_dir = tempfile.mkdtemp()


    def tearDown(self):
        log.setSilent(False)
        shutil.rmtree(self.test_dir)


    def test_if_properly_crawls_root_dir_files(self):
        with open(os.path.join(self.test_dir, 'file1.txt'), 'w') as f:
            f.write("Content of file 1")
        with open(os.path.join(self.test_dir, 'file2.txt'), 'w') as f:
            f.write("Content of file 2")
        
        mock_callback = Mock()
        for_each_file_recursive(self.test_dir, mock_callback)
        self.assertEqual(mock_callback.call_count, 2)
        # todo those tests are not cross platform, '/' should not be hardcoded
        mock_callback.assert_any_call("Content of file 1", "/file1.txt")
        mock_callback.assert_any_call("Content of file 2", "/file2.txt")


    def test_if_properly_crawls_subdir_files(self):
        os.makedirs(os.path.join(self.test_dir, 'subdir_1'))
        os.makedirs(os.path.join(self.test_dir, 'subdir_2'))
        
        with open(os.path.join(self.test_dir, 'subdir_1', 'file1.txt'), 'w') as f:
            f.write("Content of file 1")
        with open(os.path.join(self.test_dir, 'subdir_2', 'file2.txt'), 'w') as f:
            f.write("Content of file 2")
        
        mock_callback = Mock()
        for_each_file_recursive(self.test_dir, mock_callback)
        self.assertEqual(mock_callback.call_count, 2)
        mock_callback.assert_any_call("Content of file 1", "/subdir_1/file1.txt")
        mock_callback.assert_any_call("Content of file 2", "/subdir_2/file2.txt")

    def test_if_properly_crawls_deep_subdir_files(self):
        os.makedirs(os.path.join(self.test_dir, 'subdir_1', 'a', 'b', 'c'))
        os.makedirs(os.path.join(self.test_dir, 'subdir_2', 'a', 'b'))
        
        with open(os.path.join(self.test_dir, 'subdir_1', 'a', 'b', 'c', 'file1.txt'), 'w') as f:
            f.write("Content of file 1")
        with open(os.path.join(self.test_dir, 'subdir_2', 'a', 'b', 'file2.txt'), 'w') as f:
            f.write("Content of file 2")
        
        mock_callback = Mock()
        for_each_file_recursive(self.test_dir, mock_callback)
        self.assertEqual(mock_callback.call_count, 2)
        mock_callback.assert_any_call("Content of file 1", "/subdir_1/a/b/c/file1.txt")
        mock_callback.assert_any_call("Content of file 2", "/subdir_2/a/b/file2.txt")



class TestWipeout(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()


    def tearDown(self):
        shutil.rmtree(self.test_dir)


    def test_wipeout_empty_directory(self):
        wipeout(self.test_dir)
        self.assertTrue(os.path.exists(self.test_dir))
        self.assertTrue(os.path.isdir(self.test_dir))
        self.assertEqual(os.listdir(self.test_dir), [])


    def test_wipeout_with_files(self):
        for i in range(3):
            with open(os.path.join(self.test_dir, f"file{i}.txt"), "w") as f:
                f.write("test content")

        self.assertNotEqual(os.listdir(self.test_dir), [])
        wipeout(self.test_dir)
        self.assertTrue(os.path.exists(self.test_dir))
        self.assertTrue(os.path.isdir(self.test_dir))
        self.assertEqual(os.listdir(self.test_dir), [])


    def test_wipeout_with_subdirectories(self):
        for i in range(2):
            subdir = os.path.join(self.test_dir, f"subdir{i}")
            os.mkdir(subdir)
            with open(os.path.join(subdir, "file.txt"), "w") as f:
                f.write("test content")

        self.assertNotEqual(os.listdir(self.test_dir), [])
        wipeout(self.test_dir)
        self.assertTrue(os.path.exists(self.test_dir))
        self.assertTrue(os.path.isdir(self.test_dir))
        self.assertEqual(os.listdir(self.test_dir), [])


    def test_wipeout_with_mixed_content(self):
        with open(os.path.join(self.test_dir, "file.txt"), "w") as f:
            f.write("test content")
        subdir = os.path.join(self.test_dir, "subdir")
        os.mkdir(subdir)
        with open(os.path.join(subdir, "subfile.txt"), "w") as f:
            f.write("test content")

        self.assertNotEqual(os.listdir(self.test_dir), [])
        wipeout(self.test_dir)
        self.assertTrue(os.path.exists(self.test_dir))
        self.assertTrue(os.path.isdir(self.test_dir))
        self.assertEqual(os.listdir(self.test_dir), [])
