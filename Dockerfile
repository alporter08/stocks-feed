FROM public.ecr.aws/lambda/python:3.10

ENV POETRY_VERSION=1.7.1
RUN pip install "poetry==$POETRY_VERSION"

# Copy requirements.txt
# COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
# RUN pip install -r requirements.txt

WORKDIR ${LAMBDA_TASK_ROOT}

COPY /poetry.lock ${LAMBDA_TASK_ROOT}
COPY /pyproject.toml ${LAMBDA_TASK_ROOT}
COPY /stocks_feed ${LAMBDA_TASK_ROOT}/stocks_feed

# Copy function code
COPY lambda_function/lambda_function.py ${LAMBDA_TASK_ROOT}/


RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.lambda_handler" ]