FROM mcr.microsoft.com/playwright/python:latest as build-image

ENV FUNCTION_DIR="/function"
ENV PLAYWRIGHT_BROWSERS_PATH=${FUNCTION_DIR}/pw-browsers

# Install aws-lambda-cpp build dependencies
RUN apt-get update && \
  apt-get install -y \
  xvfb && \
  apt-get clean && \
  apt-get autoremove

# Create function directory
RUN mkdir -p ${FUNCTION_DIR}

# Copy function code
COPY app/* ${FUNCTION_DIR}

# move playwright browsers 
RUN mv /ms-playwright ${PLAYWRIGHT_BROWSERS_PATH}

# Install the runtime interface client
RUN pip uninstall playwright -y; \
        pip install \
        --target ${FUNCTION_DIR} \
        --no-cache-dir \
        awslambdaric playwright

# Multi-stage build: grab a fresh copy of the base image
FROM mcr.microsoft.com/playwright/python:latest

# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}

# Copy in the build image dependencies
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

COPY ./entry_script.sh              /
COPY ./xvfb-lambda-entrypoint.sh    /
ADD  ./aws-lambda-rie               /usr/local/bin/aws-lambda-rie  

RUN python -m playwright install 

RUN chmod -R +x /entry_script.sh /xvfb-lambda-entrypoint.sh  /usr/local/bin/aws-lambda-rie ${FUNCTION_DIR}

ENTRYPOINT [ "/xvfb-lambda-entrypoint.sh" ]

CMD [ "app.handler" ]
