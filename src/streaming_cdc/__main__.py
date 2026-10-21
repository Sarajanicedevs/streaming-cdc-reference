import argparse
import json
from .processor import process

parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True)
args = parser.parse_args()
with open(args.input, encoding="utf-8") as stream:
    events = [json.loads(line) for line in stream if line.strip()]
print(json.dumps(process(events), indent=2))
