#!/bin/sh
if [ -z "${AWS_LAMBDA_RUNTIME_API}" ]; then
  exec /usr/bin/aws-lambda-rie /usr/bin/python -m awslambdaric $@
else
  exec /usr/bin/python -m awslambdaric $@
fi
