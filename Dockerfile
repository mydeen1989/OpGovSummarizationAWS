# Use the official AWS Lambda Python 3.11 base image
FROM public.ecr.aws/lambda/python:3.10

# Set working dir to Lambda task root
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy function code into the Lambda execution directory
COPY lambda/ .

# Copy and install Python dependencies
COPY requirements.txt .
RUN yum install -y ffmpeg git
RUN pip install --upgrade pip 
RUN pip3 install -r requirements.txt
