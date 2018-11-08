#!/bin/sh
set -e
coverage run -m pytest "$@"
coverage report -m
