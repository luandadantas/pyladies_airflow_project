FROM quay.io/astronomer/astro-runtime:12.7.1

COPY requirements.txt .

RUN pip install -r requirements.txt