#!/bin/sh
export PATHONPATH=`pwd`
coverage run --timid --branch --source fe,bookstore --concurrency=thread -m pytest -v --ignore=fe/data # --ignore=fe/test/test_bench.py
# coverage run --timid --branch --source fe,bookstore --concurrency=thread -m pytest --workers 8
coverage combine
coverage report
coverage html
