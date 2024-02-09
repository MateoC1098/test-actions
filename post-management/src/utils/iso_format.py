import re

def is_iso_datetime(string):
    iso_datetime_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.*')

    return bool(iso_datetime_pattern.match(string))