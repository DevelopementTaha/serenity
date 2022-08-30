FROM python:3.7


RUN pip install flask urllib3 requests Jinja2 gunicorn

COPY src/ index/
WORKDIR /index

ENV PORT 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 index:app
