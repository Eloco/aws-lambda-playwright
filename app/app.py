#!/usr/bin/env python
# coding=utf-8

import asyncio
import base64
import os,sys,json
import traceback
import copy
import tempfile
from pprint import pprint
from pydoc import locate
import importlib.machinery
from urllib import parse

def handler(event, context):
    status_code = 200
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_file="async_template.py"
    result="Hello AWS LAMBDA!"
    data=event
    pprint(event)

    if "httpMethod" in event:
        if event["httpMethod"]=="GET":
            print("this is GET")
            if not event["isBase64Encoded"]:
                data=event["queryStringParameters"]
        elif event["httpMethod"]=="POST":
            print("this is POST")
            if not event["isBase64Encoded"]:
                data=event["body"]
            else:
                data=event["body"]
                data=base64.b64decode(data).decode('utf-8')
                data=parse.parse_qsl(data)

    data = json.loads(data) if type(data)==str else data
    
    if_stealth   = bool(data.get('stealth', False))
    if_reindent  = bool(data.get('reindent', True))
    browser_name = str(data.get('browser', 'webkit')).strip().lower()
    device_name  = str(data.get('device', '')).strip().lower()
    run_code     = str(data.get('run', f'result="{result}"')).strip()


    try:
        run_code=base64.b64decode(run_code).decode('utf-8')
    except:pass
    run_code     = run_code.replace('\r','\n').replace('\n','\n'+" "*4*2)

    with tempfile.TemporaryDirectory() as tmpdirname:
        try:
            template=open(os.path.join(script_dir,template_file)).read()
            template=template.replace('<run_code>',run_code)
            dynamic_path=os.path.join(tmpdirname,"dynamic.py")
            with open(dynamic_path,"w") as f:
                f.write(template)
                del template
            if if_reindent:os.system(f"python -m reindent {dynamic_path} &> /dev/null; \
                        python -m autopep8 {dynamic_path} --select=E121,E101,E11 --in-place &> /dev/null; \
                        cat {dynamic_path}")

            loader = importlib.machinery.SourceFileLoader('dynamic', dynamic_path)
            handle = loader.load_module('dynamic')
            loop = asyncio.get_event_loop()
            result=loop.run_until_complete( \
                    handle.main(browser_name=browser_name,\
                                if_stealth=if_stealth,\
                                device_name=device_name))

        except Exception as e:
            result=traceback.format_exc()
            traceback.print_exc()
            status_code = 500

        message= {
                'code'   : status_code ,
                'result' : result      ,
               }
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(message)
        }

