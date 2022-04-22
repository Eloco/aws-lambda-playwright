#!/usr/bin/env python
# coding=utf-8

from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import base64
import os,sys,json
import datetime,time,random
import httpx,requests

result = """ u need to send param  event[run] with base64 encode """

def handler(event, context):
    with sync_playwright() as playwright:
        global result
        if "webkit" in event:
            browser = playwright.webkit.launch(headless=True)
            if   event["webkit"] in playwright.devices:
                device_name = event["webkit"]
                device      = playwright.devices[device_name]
                context     = browser.new_context(**device,)
            elif event["webkit"] == "random":
                device_name = random.choice(list(playwright.devices.keys()))
                device      = playwright.devices[device_name]
                context     = browser.new_context(**device,)
            else:
                context = browser.new_context()
            page = context.new_page()

        run="global result;"
        if "run" in event.keys():
            try:
                run+=base64.b64decode(event["run"]).decode('utf-8')
            except:
                run+=event["run"]

        exec(run)

        return {
            'statusCode': 200,
            'body': result,
        }
