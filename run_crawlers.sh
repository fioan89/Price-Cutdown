#!/usr/bin/env bash
scl enable python27 'python run_scrapy_commands.py crawl cel -o cel_items.json'
scl enable python27 'python run_scrapy_commands.py crawl emag -o emag_items.json'
