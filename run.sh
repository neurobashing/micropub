#!/bin/sh

source ~/.virtualenvs/micropub/bin/activate

export FLASK_APP=micropub.py
export FLASK_ENV=development
flask run
