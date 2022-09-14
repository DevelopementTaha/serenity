FROM python:3.7


RUN pip install flask urllib3 requests Jinja2 gunicorn

COPY src/ index/
WORKDIR /index

ENV PORT 8080
#   exec gunicorn --bind (empty means 0.0.0.0)         fileName:app.run (check last line)
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 index:app
