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

import os
from .log import log
import shutil

def create_file_with_content(file_path, content):
    """
        Create a file and all necessary directories in its path.

        :param file_path: The full path to the file, including the filename.
        :param content: The content of the file to create.
        :return: True if no errors.
    """
    file_path = os.path.normpath(file_path)
    dir_path = os.path.dirname(file_path)
    os.makedirs(dir_path, exist_ok=True)
    
    file_exists = os.path.exists(file_path)

    try:
        with open(file_path, 'w') as f:
            if file_exists:
                log.info(f"Overwriting existing file: '{file_path}'")
            else:
                log.info(f"New file created: '{file_path}'")

            f.write(content)
            f.close()
            return True
    except IOError as e:
        log.error("Creating file '{file_path}': {e}")
    return False



def for_each_file_recursive(root_folder, callback):
    """
        Recursively process all files in the root_folder and its subfolders.
        For each file, call the callback function with the file's content.

        example:
            def sample_callback(input_file_content: str, relative_path: str) -> str:
                output_file_content = input_file_content + "\n" + relative_path
                return output_file_content

        :param root_folder: The path to the root folder to start processing from.
        :param callback: A function that takes two parameters - file content and relative path to that file counting from root as input, and return preprocessed file content as output
    """
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                relative_path = file_path[len(root_folder):]
                callback(content, relative_path)
            except Exception as e:
                log.error(f"Crawler exception when processing {file_path}: {str(e)}")



def wipeout(directory):
    """
        Remove all content of directory but keep the directory itself.
        :param directory root directory to be wiped out
    """
    log.info(f"Wipeout of directory '{directory}'")
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            os.remove(item_path)  # Remove files
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)  # Remove directories and their contents
