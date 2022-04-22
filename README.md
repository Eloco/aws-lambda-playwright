# aws-lambda-playwright
AWS lambda with Playwright (Webkit)

build on
- https://gallery.ecr.aws/w3s2d0z8/aws-lambda-playwright
- https://github.com/Eloco/aws-lambda-playwright/pkgs/container/aws-lambda-playwright

note: it can run on local docker
```
sudo docker pull public.ecr.aws/w3s2d0z8/aws-lambda-playwright:main
sudo docker pull ghcr.io/eloco/aws-lambda-playwright:latest
sudo docker run --rm=True -p 9000:8080 ghcr.io/eloco/aws-lambda-playwright
```


```
bs64=`echo "stealth_sync(page);page.goto('http://whatsmyuseragent.org/',wait_until='commit'); result=page.content()" | base64 -w 0`
curl -s -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"webkit":"iPhone SE","run":"'${bs64}'"}' | jq .body | html2text | sed  's/[\\n" ]//g' | grep -v '^$'
curl -s -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"webkit":"random","run":"'${bs64}'"}' | jq .body | html2text | sed  's/[\\n" ]//g' | grep -v '^$'

__[__What'smyUserAget?](#page-top)
*[](#page-top)
Mozilla/5.0(iPad;CPUOS12_2likeMacOSX)AppleWebKit/605.1.15(KHTML,
likeGecko)Versio/15.4Mobile/15E148Safari/604.1
MyIPAddress:36.161.237.194
Copyright©What'smyUserAget2015
```
