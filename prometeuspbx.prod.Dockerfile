FROM python:3.9

ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY ./requirements.txt /code/

COPY ./prometeuspbx.production.yaml /etc/prometeuspbx/prometeuspbx.yaml

RUN pip install -r requirements.txt

COPY ./ /code/

ENTRYPOINT ["/bin/bash", "/code/docker-entrypoint.sh"]
STOPSIGNAL SIGINT

CMD ["gunicorn", "--bind", ":8000", "PrometeusPBX.wsgi:application"]
