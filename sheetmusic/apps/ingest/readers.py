import csv
import json
import gzip
from io import TextIOWrapper


def iter_csv(fp, flags=None):
    flags = flags or []
    if 'gzip' in flags:
        fp = gzip.open(fp, 'rt', newline='')
    else:
        fp = TextIOWrapper(fp) if hasattr(fp, 'read') else open(fp, newline='')
    dialect = csv.excel
    if 'pipe-delim' in flags:
        dialect = csv.excel_tab
        dialect.delimiter = '|'
    reader = csv.DictReader(fp)
    for row in reader:
        yield row


def iter_jsonl(fp, flags=None):
    flags = flags or []
    if 'gzip' in flags:
        fp = gzip.open(fp, 'rt')
    else:
        fp = TextIOWrapper(fp) if hasattr(fp, 'read') else open(fp)
    for line in fp:
        if 'utf8-bom' in flags:
            line = line.lstrip('\ufeff')
        yield json.loads(line)
