import logging
import sys

# Configure which fields from the Apache log will be retained and what field
# they will be mapped to in the final JSON object.
APACHE_FIELD_MAPPINGS = {
    '%h': 'ip_address',
    '%t': 'time',
    '%r': 'request',
    '%>s': 'status',
    '%{Referer}i': 'referer',
    '%{User-agent}i': 'user_agent',
    '%b': 'filesize',
}

# Should be a tuple with either host and port, MongoDB URI, or empty
# ex: ('localhost', 27017,) or ('mongodb://localhost:27017',) remember the trailing comma!
MONGO_CONNECTION = ('localhost', 27017,)
MONGO_DB = 'oastats'
MONGO_COLLECTION = 'requests'
MONGO_SUMMARY_COLLECTION = 'summary'

# Location of the GeoIPv4 and GeoIPv6 databases
GEOIP4_DB = ''
GEOIP6_DB = ''

# Configure logging for the application
log = logging.getLogger('pipeline')
log.addHandler(logging.StreamHandler(sys.stderr))
log.setLevel(logging.WARNING)

# Configure unresolveable IP address log
ip_log = logging.getLogger('ip_log')
ip_log.addHandler(logging.FileHandler('logs/ip.log'))
ip_log.setLevel(logging.ERROR)

# Configure unparseable request log
req_log = logging.getLogger('req_log')
req_log.addHandler(logging.FileHandler('logs/req.log'))
req_log.setLevel(logging.ERROR)
