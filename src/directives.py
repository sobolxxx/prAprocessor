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
from .util import get_first_non_whitespace_substring, get_string_after_tag_safe, remove_after
from .context import context


def parse_directive(src_line_after_directive):
    if '#' not in src_line_after_directive:
        log.error(f"Directive not enclosed with #, unsupported yet -> '{src_line_after_directive}'")
        return ""
    tmp = remove_after(src_line_after_directive, "#")
    return get_first_non_whitespace_substring(tmp)


def ifdef_handler(src_line_after_directive):
    variable_name = parse_directive(src_line_after_directive)
    if variable_name == "":
        log.error(f"'#ifdef{src_line_after_directive}' - missing variable name")
        return False
    context.push_stack(variable_name, not context.is_variable_set(variable_name))
    return True


def ifndef_handler(src_line_after_directive):
    variable_name = parse_directive(src_line_after_directive)
    if variable_name == "":
        log.error(f"'#ifndef{src_line_after_directive}' - missing variable name")
        return False
    context.push_stack(variable_name, context.is_variable_set(variable_name))
    return True


def endif_handler(src_line_after_directive):
    parse_directive(src_line_after_directive)
    context.pop_stack()
    return True

#todo add else directive

#todo add define directive

# todo - make a possibility to overwrite directives in config file
# for example: if someone wants to have %ifdef% instead of #ifdef for some reason
# otherwise the tool is not really language agnostic
handlers = {
    "#ifdef": ifdef_handler,
    "#ifndef": ifndef_handler,
    "#endif": endif_handler
}


all_directives = list(handlers.keys())


def get_directive(src_line):
    # todo - for performance reasons file should be processed letter by letter and trie should be built
    call_directive = None
    for directive in all_directives:
        if directive in src_line:
            if call_directive != None:
                # todo - file should be first checked for errors and then processed separately in second pass to prevent errors in output
                log.error("Multiple directives in one line '{src_line}'")
                return None
            call_directive = directive
    return call_directive


def handle_line(src_line):
    # log.info(f"Handle line -> '{src_line}'")
    call_directive = get_directive(src_line)
    if call_directive == None:
        return False
    log.info(f" ### {call_directive} handler called for line '{src_line}'")
    return handlers[call_directive](get_string_after_tag_safe(src_line, call_directive))
