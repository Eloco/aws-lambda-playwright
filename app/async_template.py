#!/usr/bin/env python
# coding=utf-8
import datetime,time,random
import requests
import base64
import os,sys,json
import tempfile
import traceback
import random
import copy
import sh
import re

from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
import asyncio

async def main(browser_name,if_stealth,device_name):
    async with async_playwright() as playwright:
        if bool(browser_name):
            if browser_name=="chromium":
                browser = await playwright.chromium.launch(headless=True)
                context = await browser.new_context()
            elif browser_name=="firefox":
                browser = await playwright.firefox.launch(headless=True)
                context = await browser.new_context()
            else:
                browser = await playwright.webkit.launch(headless=True)
                if device_name == "random":
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
                context     = await browser.new_context(**device,)
            await context.clear_cookies()
            page = await context.new_page()
            if if_stealth:
                print("page is stealth!")
                stealth_async(page)
        <run_code>

        return(result)
