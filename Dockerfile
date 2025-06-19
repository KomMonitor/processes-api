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

RUN mkdir -p /app/results

# copy runner
COPY run.sh .
RUN chmod +x run.sh

# copy application files
COPY processor processor
COPY ressources ressources

ENV PYTHONUNBUFFERED=1
CMD ["./run.sh"]