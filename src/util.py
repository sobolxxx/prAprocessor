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


from .log import log

def get_first_non_whitespace_substring(input_string: str) -> str:
    substrings = input_string.split()
    if substrings:
        return substrings[0]    
    return ""


def get_string_after_tag_safe(full_string: str, tag: str) -> str:
    tag_index = full_string.find(tag)
    if tag_index != -1:
        return full_string[tag_index + len(tag):]
    log.fatal("Internal error - seems like get string after tag was called for src line that doesn't contain that tag.")
    return ""


def remove_after(string: str, after: str) -> str:
    if after == "":
        return string
    index = string.find(after)
    if index != -1:
        return string[:index]
    return string

