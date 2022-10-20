ARG FUNCTION_DIR="/function"

FROM ghcr.io/eloco/local-lambda-playwright:latest

ARG FUNCTION_DIR

COPY app/* ${FUNCTION_DIR}/

RUN python -m pip install -r ${FUNCTION_DIR}/requirements.txt \
        --target ${FUNCTION_DIR} \
        --no-cache-dir 

CMD ["app.handler"]
