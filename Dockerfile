# Define function directory
#https://docs.aws.amazon.com/lambda/latest/dg/images-create.html
ARG FUNCTION_DIR="/function"
ARG PY_VERSION=3.10
ARG UBUNTU_TAG=22.04

FROM ubuntu:${UBUNTU_TAG} as build-image

# Install aws-lambda-cpp build dependencies
RUN apt-get update && \
  apt-get install -y \
  g++ \
  make \
  cmake \
  unzip \
  libcurl4-openssl-dev \
  software-properties-common

# install python
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y python${PY_VERSION} python3-distutils python3-pip python3-apt

# Include global arg in this stage of the build
ARG FUNCTION_DIR
# Create function directory
RUN mkdir -p ${FUNCTION_DIR}

# Copy function code
COPY app/requirements.txt ${FUNCTION_DIR}

# Install the runtime interface client
RUN pip install -r ${FUNCTION_DIR}/requirements.txt \
        --target ${FUNCTION_DIR} \
        --no-cache-dir 

# Multi-stage build: grab a fresh copy of the base image
FROM ubuntu:${UBUNTU_TAG}

# Include global arg in this stage of the build
ARG FUNCTION_DIR
# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}

# Copy in the build image dependencies
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

# Install tools
RUN apt-get update && \
  apt-get install -y \
  mat \
  jq \
  unzip \
  xvfb \
  httpie \
  tesseract-ocr tesseract-ocr-chi-sim \
  libcurl4-openssl-dev \
  software-properties-common

# install python
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y python${PY_VERSION} python3-distutils python3-pip python3-apt

# install playwright deps
RUN playwright install-deps && \
        playwright install webkit

  # Copy requirements
ADD app/* ${FUNCTION_DIR}/

#RIE support
#https://docs.aws.amazon.com/lambda/latest/dg/images-test.html
COPY ./entry_script.sh /entry_script.sh
ADD aws-lambda-rie-x86_64 /usr/bin/aws-lambda-rie
ENTRYPOINT [ "/entry_script.sh" ]

CMD [ "app.handler" ]
