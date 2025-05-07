# Use the official AWS Lambda Python 3.10 base image
FROM public.ecr.aws/lambda/python:3.10

# Install ffmpeg and git (required for whisper/pytube and others)
RUN yum install -y ffmpeg git

# Copy Python dependencies file and install packages
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the lambda function code and utils folder from outside lambda/
COPY lambda/ ./lambda/

# Set working directory
WORKDIR /lambda
