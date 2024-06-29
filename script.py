import json
import csv

def flatten(row_index, obj, parent_key, out, headers):
    for key, value in obj.items():
        k = f"{parent_key}.{key}" if parent_key else key
        if isinstance(value, list):
            for v in value:
                flatten(row_index, v, k, out, headers)
        elif isinstance(value, dict):
            flatten(row_index, value, k, out, headers)
        else:
            headers.add(k)
            out.append({
                "rowIndex": row_index,
                "name": k,
                "value": value
            })

def json2csv(obj):
    out = []
    headers = set()

    flatten(0, obj, "", out, headers)

    p = {}
    results = []
    header_props = {header: None for header in headers}
    
    for header in headers:
        group = [f for f in out if f["name"] == header]
        if group:
            p[header] = group

    for pp, r in p.items():
        if len(r) > 1:
            for m in r:
                header_props[pp] = m["value"]
                results.append(header_props.copy())
        elif not isinstance(r[0], list):
            header_props[pp] = r[0]["value"]

    return dict({
        'headers': [*headers],
        'result': results
    })

# Load data from example.json file
with open('example.json') as f:
    data = json.load(f)
    
    with open('out2.json', 'wt', encoding='utf8', newline='') as w:
        
        results = json2csv(data)
        field_names = results.get('headers')
    
        csv_writer = csv.DictWriter(w, fieldnames=field_names)
        csv_writer.writeheader()
        
        csv_writer.writerows(results.get('result'))
        
    
        print('done')