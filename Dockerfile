FROM python:3.11

WORKDIR /app

# Install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Workaround for failing install of prefect dependencies
COPY requirements_nodeps.txt .
RUN pip install --no-deps -r requirements_nodeps.txt

# Install data-management-client
COPY data-management-client data-management-client
RUN cd data-management-client && python setup.py install --user

# copy application files
COPY processor processor
COPY example-openapi.yml .
COPY pygeoapi-config.yml .

ENV PYTHONUNBUFFERED=1
ENV KC_CLIENT_ID=kommonitor-processor
ENV KC_CLIENT_SECRET=secret
ENV PYGEOAPI_CONFIG=../pygeoapi-config.yml
ENV PYGEOAPI_OPENAPI=../example-openapi.yml

WORKDIR /app/processor

# TODO(specki): refactor to use gunicorn
CMD ["python3", "app.py"]