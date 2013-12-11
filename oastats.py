#!/usr/bin/env python

import os

os.environ.setdefault("OASTATS_SETTINGS", "pipeline.settings")

import fileinput
import time
from datetime import datetime
from pipeline.conf import settings
from pipeline.parse_log import parse
from pipeline.load_json import get_collection, insert


collection = get_collection(settings.MONGO_DB,
                            settings.MONGO_COLLECTION,
                            settings.MONGO_CONNECTION)

def main():
    for line in fileinput.input():
        request = parse(line)
        t = time.strptime(request['time'].split(' ')[0], "[%d/%b/%Y:%H:%M:%S")
        request['time'] = datetime.fromtimestamp(time.mktime(t))
        insert(collection, request)

if __name__ == '__main__':
    main()
