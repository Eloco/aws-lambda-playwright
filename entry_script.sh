#!/bin/sh
if [ -z "${AWS_LAMBDA_RUNTIME_API}" ]; then
  exec /usr/local/bin/aws-lambda-rie python -m awslambdaric $@
else
  exec python -m awslambdaric $@
fi
