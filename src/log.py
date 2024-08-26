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

class Log:

    def __init__(self):
        # todo - add verbose and silent mode to config
        self.__verbose = False
        self.__silent = False

    def setVerbose(self, new_value):
        if self.__silent:
            self.error("Cannot be both silent and verbose")
            return
        self.__verbose = new_value

    def setSilent(self, new_value):
        if self.__verbose:
            self.error("Cannot be both verbose and silent")
            return
        self.__silent = new_value

    def info(self, message):
        if self.__verbose:
            print(f"INFO: {message}")

    def error(self, message):
        if not self.__silent:
            print(f"ERROR: {message}")

    def fatal(self, message):
        print(f"\n!!! FATAL ERROR !!!\nmessage: {message}\n")
        exit(1)

log = Log()
