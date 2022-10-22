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

def handler(event, context):
    status_code = 200
    script_dir = os.path.dirname(os.path.abspath(__file__))
    

    result="Hello AWS LAMBDA!"
    print(r"init",result)

    if_stealth   = bool(event.get('stealth', False))
    if_reindent  = bool(event.get('reindent', True))
    browser_name = str(event.get('browser', 'webkit')).strip().lower()
    device_name  = str(event.get('device', '')).strip().lower()
    run_code     = str(event.get('run', f'result="{result}"')).strip()

    template_file="async_template.py"

    try:
        run_code=base64.b64decode(run_code).decode('utf-8')
    except:pass
    run_code     = run_code.replace('\r','\n').replace('\n','\n'+" "*4*2)

    with tempfile.TemporaryDirectory() as tmpdirname:
        try:
            template=open(os.path.join(script_dir,template_file)).read()
            template=template.replace('<run_code>',run_code)
            file_path=os.path.join(tmpdirname,"dynamic.py")
            with open(file_path,"w") as f:
                f.write(template)
                del template
            if if_reindent:os.system(f"python -m reindent {file_path} &> /dev/null; \
                        python -m autopep8 {file_path} --select=E121,E101,E11 --in-place &> /dev/null; \
                        cat {file_path}")

            loader = importlib.machinery.SourceFileLoader('dynamic', file_path)
            handle = loader.load_module('dynamic')
            loop = asyncio.get_event_loop()
            result=loop.run_until_complete( \
                    handle.main(browser_name=browser_name,if_stealth=if_stealth,device_name=device_name))

        except Exception as e:
            result=traceback.format_exc()
            traceback.print_exc()
            status_code = 500

        return {
                'code'   : status_code ,
                'result' : result      ,
               }