# lambda-playwright-python
AWS lambda with Playwright official docker base image 

sudo docker pull ghcr.io/eloco/lambda-playwright-python:latest
sudo docker run --rm=True -p 9000:8080 ghcr.io/eloco/lambda-playwright-python
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}' # will show http://www.example.com content in body
