const data = require("./example.json")
// const fs = require("fs")

function flatten(obj, parentKey, out, headers) {
    const keys = Object.keys(obj);

    for (const key of keys) {
        const value = obj[key]
        const k = parentKey ? parentKey + "." + key : key;
        if (Array.isArray(value)) {
            for (const v of value) {
                flatten(v, k, out, headers)
            }
        } else if (value instanceof Object) {
            flatten(value, k, out, headers)
        } else {
            headers.add(k);
            out.push({
                name: k,
                value: value
            })
        }
    }
}

function json2csv(obj) {
    const out = [];
    const headers = new Set();

    flatten(obj, "", out, headers)

    const p = {}
    const results = []
    const headerProps = {}
    for (const header of headers) {
        const group = out.filter(f => f.name === header)
        if (group.length > 0) {
            p[header] = group
        }
        headerProps[header] = null;
    }

    for (const pp in p) {
        const r = p[pp];
        if (r.length > 1) {
            for (const m of r) {
                headerProps[pp] = m['value']
                results.push({
                    ...headerProps
                })
            }
        } else if (!Array.isArray(r[0])) {
            headerProps[pp] = r[0]['value']
        }

    }

    
    return results
}

const results = json2csv(data);

// fs.writeFileSync("out.json", JSON.stringify(results))