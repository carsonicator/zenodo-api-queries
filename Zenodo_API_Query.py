# Change to work with your environment
#!/usr/bin/env python

import requests
from collections import Counter
import json
import time
import os.path
import csv

ACCESS_TOKEN = 'Your key here'

# Number of records to return
size = 10

response = requests.get('https://zenodo.org/api/records',
                        params={'q': '_exists_:contributors', 'size': size, 'page': 1, 'status': 'published', 'sort': 'bestmatch', 'all_versions': 'false', 'access_token': ACCESS_TOKEN})

records = response.json()

# Print ID, resource type, and contributor role(s) for each record
results = []

for i in range(len(records['hits']['hits'])):
    c = []
    contributors = ''

    record_id = records['hits']['hits'][i]['id']
    if 'resource_type' in records['hits']['hits'][i]['metadata']:
        resource_type = records['hits']['hits'][i]['metadata']['resource_type']['title']
    else:
        resource_type = "none"
    if 'title' in records['hits']['hits'][i]['metadata']:
        title = records['hits']['hits'][i]['metadata']['title']
    else:
        title = "none"
    if 'contributors' in records['hits']['hits'][i]['metadata']:
        for j in range(len(records['hits']['hits'][i]['metadata']['contributors'])):
            c.append(records['hits']['hits'][i]['metadata']['contributors'][j]['type'])

        contributor_counts = Counter(c)

        count = 0
        for contrib in contributor_counts.keys():
            if (count > 0):
                contributors += ','
            contributors += contrib + "=" + str(contributor_counts[contrib])
            count += 1
    else:
        contributors = 'none'

    results.append([record_id,title,resource_type,contributors])

# Get the current time
timestr = time.strftime("%Y%m%d-%H%M%S")

# Print all records to a file in JSON format
records_path = "./contrib_records"
record_dump_fn = "zenodo_contrib_records_" + str(size) + "_" + timestr + ".json"
complete_rd_fn = os.path.join(records_path, record_dump_fn)
with open(complete_rd_fn, 'w') as f:
    json.dump(records, f, indent = 4, sort_keys = True)
f.close()

# Print selected output from records
parsed_path = "parsed_output"
parsed_records_fn = "zenodo_parsed_records" + "_" + timestr + ".csv"
complete_pr_fn = os.path.join(parsed_path, parsed_records_fn)

header = ['id','title','resource_type','contributor_role']

with open(complete_pr_fn, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(results)
f.close()
