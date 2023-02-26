#!/usr/bin/env bash

python -m black timerdo test
python -m flake8 timerdo test
python -m isort timerdo test