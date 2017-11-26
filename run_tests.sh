#!/bin/bash

cd test
PYTHONPATH=../ python -m unittest *.py
cd ..

exit 0