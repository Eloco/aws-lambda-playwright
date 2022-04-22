ARG FUNCTION_DIR="/function"

FROM mcr.microsoft.com/playwright/python:latest as build-image

# Install aws-lambda-cpp build dependencies
RUN apt-get update && \
  apt-get install -y \
  g++ \
  make \
  cmake \
  unzip \
  libcurl4-openssl-dev \
  xvfb

# Include global arg in this stage of the build
ARG FUNCTION_DIR

# Create function directory
RUN mkdir -p ${FUNCTION_DIR}

# Copy function code
COPY app/* ${FUNCTION_DIR}

RUN pip uninstall \
        playwright -y

# Install the runtime interface client
RUN pip install \
        --target ${FUNCTION_DIR} \
        --no-cache-dir \
        awslambdaric virtualenv playwright


# Multi-stage build: grab a fresh copy of the base image
FROM mcr.microsoft.com/playwright/python:latest

# remove playwright browsers 
RUN rm -rf /ms-playwright

# Include global arg in this stage of the build
ARG FUNCTION_DIR

# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}

# Copy in the build image dependencies
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

# create virtualenv
RUN python -m virtualenv venv

COPY ./entry_script.sh              /
COPY ./xvfb-lambda-entrypoint.sh    /
ADD aws-lambda-rie /usr/local/bin/aws-lambda-rie  

RUN chmod -R +x /entry_script.sh /xvfb-lambda-entrypoint.sh  /usr/local/bin/aws-lambda-rie ${FUNCTION_DIR}

ENV PLAYWRIGHT_BROWSERS_PATH=${FUNCTION_DIR}/pw-browsers

RUN . venv/bin/activate; python -m playwright install 

ENTRYPOINT [ "/xvfb-lambda-entrypoint.sh" ]

CMD [ "app.handler" ]
