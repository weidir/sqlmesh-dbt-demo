#!/bin/bash
export PYTHONPATH=$(pwd):$(pwd)/data:$(pwd)/data/src:$(pwd)/data/utils
python3 -m coverage run -m pytest