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
import json
import os

class Config:
    src_dir = ""
    target_dir = ""
    working_dir = "./"

    def load_config(working_dir, config_path):
        log.info(f"Setting working dir to {working_dir}")
        Config.working_dir = working_dir

        log.info(f"Loading config from {config_path}")

        try:
            with open(config_path, 'r') as file:
                config = json.load(file)
            
            Config.src_dir = os.path.join(working_dir, config['src_dir'])
            Config.target_dir = os.path.join(working_dir, config['target_dir'])
            
            log.info(f"Source directory: {Config.src_dir}")
            log.info(f"Target directory: {Config.target_dir}")

        except FileNotFoundError:
            log.fatal(f"The file '{config_path}' was not found.")
        except json.JSONDecodeError:
            log.fatal(f"Error: The file '{config_path}' contains invalid JSON.")
        except KeyError as e:
            log.fatal(f"Error: The configuration is missing a required key: {e}")

        # todo check if src_dir and target_dir are proper directories

        if Config.src_dir == "" or Config.target_dir == "":
            log.fatal("Both src_dir and target_dir have to be properly specified to work safely")

        if Config.src_dir == Config.target_dir:
            log.fatal("src_dir and target_dir cannot be the same")
