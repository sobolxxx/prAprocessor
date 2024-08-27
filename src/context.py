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

class Context:
    # todo this is not ready for multithreaded processing


    def __init__(self):
        self.reset()


    def reset(self):
        self.global_context = {}
        self.local_context = {}
        self.currently_processed_filename = ""
        self.ifdef_stack = []


    def on_file_start(self, filename):
        log.info(f"Starting new local context for file '{filename}'")
        self.currently_processed_filename = filename
        self.local_context = {}


    def on_file_end(self):
        # todo should check that local context is empty and handle error appropriately

        log.info(f"Closing local context for file '{self.currently_processed_filename}'")
        self.currently_processed_filename = ""
        self.local_context = {}


    def set_global_variable(self, var_name, value = True):
        log.info(f"Global variable '{var_name}' set to '{value}'")
        self.global_context[var_name] = value


    def set_local_variable(self, var_name, value = True):
        log.info(f"Local variable '{var_name}' set to '{value}'")
        self.local_context[var_name] = value


    def is_variable_set(self, var_name):
        if var_name in self.global_context and self.global_context[var_name]:
            return True
        return var_name in self.local_context and self.local_context[var_name]


    def ifdefed(self):
        if self.ifdef_stack:
            return self.ifdef_stack[-1][1]
        return False


    def push_stack(self, var_name: str, ifdefed: bool):
        ifdefed = ifdefed or self.ifdefed()
        self.ifdef_stack.append((var_name, ifdefed))
        log.info(f" + Stack push '{var_name}, curr size = {len(self.ifdef_stack)}', ifdefed = {self.ifdefed()}")


    def pop_stack(self) -> str:
        if not self.ifdef_stack:
            log.error("Trying to pop from ifdef_stack, but stack already empty")
            return ""
        to_ret = self.ifdef_stack.pop()
        log.info(f" - Stack pop '{to_ret[0]}, curr size = {len(self.ifdef_stack)}', ifdefed = {self.ifdefed()}")
        return to_ret[0]


context = Context()
