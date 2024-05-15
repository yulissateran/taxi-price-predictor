FROM python:3.8.13 as base

# Append /home/app/.local/bin/ to PATH variable because
# gunicorn is installed there.
ENV PYTHONPATH=$PYTHONPATH:/src/
ENV PATH=$PATH:/home/app/.local/bin/

COPY ./ /api

WORKDIR /api

RUN pip install --upgrade pip && pip install -r requirements.txt

FROM base as build
ENTRYPOINT ["gunicorn", "--workers=8", "--bind", "0.0.0.0:5001", "app:app"]