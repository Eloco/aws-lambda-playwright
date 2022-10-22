# aws-lambda-playwright

AWS lambda with ASYNC Playwright (Only supprt Webkit due to lib and permission issue on chrommium and firefox)

(test passed on HTTP API gat way)

## INTRO

build on
- https://gallery.ecr.aws/w3s2d0z8/aws-lambda-playwright
- https://github.com/Eloco/aws-lambda-playwright/pkgs/container/aws-lambda-playwright

base on:
- https://github.com/Eloco/normal-playwright-api

note: support aws cloud && local Docker

## pull or build

```
sudo docker pull public.ecr.aws/w3s2d0z8/aws-lambda-playwright:main
sudo docker pull ghcr.io/eloco/aws-lambda-playwright:latest
sudo docker run --rm=True -p 8080:8080 ghcr.io/eloco/aws-lambda-playwright
```

## Usage

```
param = {
        run      : "result='AWS Lambda POST'"   ; # base64 or normal run code
        browser  : "webkit"                     ; # browser name(only support webkit)
        device   : "iPhone X"                   ; # device for webkit
        stealth  : false                        ; # if stealth mode
        reindent : true                         ; # if reindent run code
        }
```
>device can see here
https://github.com/microsoft/playwright/blob/main/packages/playwright-core/src/server/deviceDescriptorsSource.json


```
$ bs64=`echo "await page.goto('http://whatsmyuseragent.org/',wait_until='commit'); result=await page.content()" | base64 -w 0`
$ http POST http://127.0.0.1:8080/2015-03-31/functions/function/invocations  run=${bs64} browser="webkit" device="iphone 6" stealth="True"

$ curl -s -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"webkit":"random","run":"'${bs64}'"}' | jq .result  | html2text -utf8  | sed -r "s/\\\n//g"  | grep -v '^\s*$' | grep -v '^"'

 What's my User Agent?
Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38
(KHTML, like Gecko) Version/15.4 Mobile/15A372 Safari/604.1
My IP Address: 34.251.234.37
Copyright © What's my User Agent 2015
```

## Other

BTW: if u need to set proxy, marksure add the code into your post['run']:
>https://playwright.dev/python/docs/network

>You can configure pages to load over the HTTP(S) proxy or SOCKSv5. Proxy can be either set globally for the entire browser, or for each browser context individually.
You can optionally specify username and password for HTTP(S) proxy, you can also specify hosts to bypass proxy for.
```
browser = await chromium.launch(proxy={
  "server": "http://myproxy.com:3128",
  "username": "usr",
  "password": "pwd"
})
```
