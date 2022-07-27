#!/usr/bin/env python
# coding=utf-8

from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import base64
import os,sys,json
import datetime,time,random
import httpx,requests
import traceback

body = """ u need to send param  event[run] with base64 encode """

def handler(event, context):
    status_code = 200
    try:
        with sync_playwright() as playwright:
            global body
            if "webkit" in event:
                browser = playwright.webkit.launch(headless=True)
                device_name = event["webkit"]
                if device_name.lower() == "random":
                    device_name = random.choice(list(playwright.devices.keys()))
                else:
                    for d in playwright.devices.keys():
                        if device_name.lower() == d.lower():
                            device_name = d
                            break
                    if device_name not in playwright.devices.keys():
                        device_name = "Desktop Firefox"  # use default

                print(f"webkit using [{device_name}]")
                device      = playwright.devices[device_name]
                context     = browser.new_context(**device,)
                page = context.new_page()

            run="global body;"
            if "run" in event.keys():
                try:
                    run+=base64.b64decode(event["run"]).decode('utf-8')
                except:
                    run+=event["run"]
            print(run)
            exec(run)

    except Exception as e:
        body=str(e)
        traceback.print_exc()
        status_code = 500

    return {
        'statusCode'  : status_code,
        'body': body,
    }
