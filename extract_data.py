import json
with open('/Users/ariaagarwal/Documents/GitHub/ds_4300_hw3/fda_reports.json') as f:
    data = json.load(f)
with open('/Users/ariaagarwal/Documents/GitHub/ds_4300_hw3/fda_reports_flat.json', 'w') as f:
    for record in data['results']:
        f.write(json.dumps(record) + '\n')
