#!/usr/bin/env python
# coding=utf-8

from playwright.sync_api import sync_playwright

def handler(event, context):
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(headless=False, 
                                            args= args=["--no-sandbox",
                                                        "--single-process",
                                                        "--disable-dev-shm-usage",
                                                        "--disable-gpu",
                                                        "--no-zygote",])
        context = browser.new_context()
        page    = context.new_page()
        page.goto('http://example.com/')

        return {
            'statusCode': 200,
            'body': page.content(),
        }
