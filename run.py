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


import argparse
import os
from src.main import run_full, run_watch
from src.log import log
from src.config import Config


def run():
    working_dir = "./"
    config_file = ""
    watch_mode = False

    parser = argparse.ArgumentParser(description="prAprocessor CLI tool")
    parser.add_argument("working_dir", nargs="?", default="./", help="Path to the working directory (default: ./)")
    parser.add_argument("--config", help="Path to the configuration file")
    parser.add_argument("--watch", action="store_true", help="Run in watch mode")
    parser.add_argument("--verbose", action="store_true", help="Verbose output - show all info messages.")
    parser.add_argument("--silent", action="store_true", help="Silent output - don't show errors.")

    args = parser.parse_args()

    if args.verbose:
        log.setVerbose(True)

    if args.silent:
        log.setSilent(True)

    log.info(f"Parsing arguments...")

    if args.working_dir:
        working_dir = os.path.abspath(args.working_dir)
        if not os.path.isdir(working_dir):
            log.fatal(f"The specified working directory '{working_dir}' does not exist or is not a directory.")

    if args.config:
        config_file = args.config
    else:
        config_file = os.path.join(working_dir, "praprocessor.config.json")

    if args.watch:
        log.info("Watch mode enabled.")
        watch_mode = True
 
    log.info(f"Loading config...")
    Config.load_config(working_dir=working_dir, config_path=config_file)
 
    log.info(f"Running...")
    run_full()
    if watch_mode:
        run_watch()


if __name__ == '__main__':
    run()

