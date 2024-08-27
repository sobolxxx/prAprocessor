#!/bin/bash

if [[ "$*" == *--test* ]]; then
    echo "Running tests..."
    python3 -m unittest
else
    python3 run.py
fi
