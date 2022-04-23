# aws-lambda-playwright
AWS lambda with Playwright (Webkit)

build on
- https://gallery.ecr.aws/w3s2d0z8/aws-lambda-playwright
- https://github.com/Eloco/aws-lambda-playwright/pkgs/container/aws-lambda-playwright

base on:
- https://github.com/Eloco/local-lambda-playwright  (not support cloud aws due to lib and permission issue on chrommium and firefox)

note: support aws cloud (webkit version)
```
sudo docker pull public.ecr.aws/w3s2d0z8/aws-lambda-playwright:main
sudo docker pull ghcr.io/eloco/aws-lambda-playwright:latest
sudo docker run --rm=True -p 9000:8080 ghcr.io/eloco/aws-lambda-playwright
```

>device can see here
https://github.com/microsoft/playwright/blob/main/packages/playwright-core/src/server/deviceDescriptorsSource.json
```
bs64=`echo "stealth_sync(page);page.goto('http://whatsmyuseragent.org/',wait_until='commit'); result=page.content()" | base64 -w 0`
curl -s -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"webkit":"iPhone SE","run":"'${bs64}'"}' | jq .result  | html2text -utf8  | sed -r "s/\\\n//g"  | grep -v '^\s*$' | grep -v '^"'
curl -s -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"webkit":"random","run":"'${bs64}'"}' | jq .result  | html2text -utf8  | sed -r "s/\\\n//g"  | grep -v '^\s*$' | grep -v '^"'

 What's my User Agent?
Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38
(KHTML, like Gecko) Version/15.4 Mobile/15A372 Safari/604.1
My IP Address: 34.251.234.37
Copyright © What's my User Agent 2015
```
