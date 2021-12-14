#!/bin/sh
export PATHONPATH=`pwd`
coverage run --timid --branch --source fe,bookstore --concurrency=thread -m pytest -v --ignore=fe/data
# coverage run --timid --branch --source fe,bookstore --concurrency=thread -m pytest --workers 8
coverage combine
coverage report
coverage html
