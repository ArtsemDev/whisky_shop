FROM python:3.11.4

WORKDIR /whisky

COPY requirements.txt /whisky/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /whisky