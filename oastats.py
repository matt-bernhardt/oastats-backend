from __future__ import print_function

import os

os.environ.setdefault("OASTATS_SETTINGS", "pipeline.settings")

import fileinput
import sys
from pipeline.conf import settings
from pipeline.parse_log import parse
from pipeline.load_json import get_collection, insert
from pipeline.request import add_country, str_to_dt, req_to_url
import pygeoip
import logging
import apachelog

ip_log = logging.getLogger("ip_log")
req_log = logging.getLogger("req_log")

collection = get_collection(settings.MONGO_DB,
                            settings.MONGO_COLLECTION,
                            settings.MONGO_CONNECTION)

def main():
    """Parse stream of requests and insert into MongoDB collection.

    This script will accept input from either stdin or one or more files as
    arguments. Requests that are unparseable or whose IP address cannot be
    mapped to a country are skipped and written as is to separate log files.

    """
    for line in fileinput.input():
        try:
            request = parse(line)
        except apachelog.ApacheLogParserError:
            # log unparseable requests
            req_log.error(line.strip('\n'))
            continue
        if request is not None:
            request = str_to_dt(request)
            try:
                request = add_country(request)
            except (pygeoip.GeoIPError, KeyError):
                # log unresolveable IP addresses
                ip_log.error(line.strip('\n'))
                continue
            request = req_to_url(request)
            insert(collection, request)

    lines = fileinput.filelineno()
    if not lines:
        sys.exit("No requests to process")
    print("{0} requests processed".format(fileinput.filelineno()))


if __name__ == '__main__':
    main()
