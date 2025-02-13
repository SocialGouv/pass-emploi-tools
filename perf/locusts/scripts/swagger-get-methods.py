#!/usr/bin/env python3

import sys
import json
import requests

# ---------------------------------------------
#   Quick & Dirty App to get Swagger Methods
# ---------------------------------------------

urls = sys.argv[1:]

def get_swagger_doc(text : str = ""):
    text = text[text.find("swaggerDoc") - 8:]
    text = text[text.find("{"):]
    text = text[:text.find("};") + 1]
    return text

def read(source):
    if source.startswith("http"):
        # read by requests
        method_open = requests.get
        method_read = "text"
    else:
        # read by file
        method_open = open
        method_read = "read"

    with method_open(source) as result:
        read = getattr(result, method_read)
        if isinstance(read, str):
            return read
        else:
            return read()

for url in urls:
    text = read(url)
    text = get_swagger_doc(text)
    swagger = json.loads(text).get("swaggerDoc")
    for path, parameters in swagger.get("paths").items():
        print(f"└── {path}")
        for method, values in parameters.items():
            print(f"   └── {method.upper()}")
            for param in values.get("parameters"):
                print(f"      └── {param.get('name')} ({param.get('schema').get('type')})")

