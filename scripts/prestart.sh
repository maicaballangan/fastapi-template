#! /usr/bin/env bash

set -e
set -x

# Run migrations
aerich upgrade

# Create initial data in DB
python app/initial_data.py
