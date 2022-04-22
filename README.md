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
