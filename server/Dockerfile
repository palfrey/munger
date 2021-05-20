FROM python:3-alpine
WORKDIR /app

RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev tiff-tools ghostscript
RUN apk add --no-cache --repository http://dl-3.alpinelinux.org/alpine/edge/testing/ netpbm
RUN pamtotiff
RUN tiff2pdf -h > /dev/null
RUN gs --version

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.0.0

RUN pip install poetry==$POETRY_VERSION "cryptography<3"

ADD pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi
ADD munger.py ./
ENTRYPOINT ["python", "munger.py"]