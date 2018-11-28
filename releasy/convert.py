
import yaml
import json
import sys
import os
import codecs

in_file = sys.argv[1]
out_file = sys.argv[2]

if os.path.exists(in_file):
    with open(in_file, 'rb') as stream:
        raw_issues = yaml.load(stream)

        with open(out_file, 'wb') as outfile:
            json.dump(raw_issues, codecs.getwriter('utf-8')(outfile), ensure_ascii=False)
