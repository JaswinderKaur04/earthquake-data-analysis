FROM python:3.13-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir pandas requests matplotlib numpy

CMD ["sh", "-c", "python E_fetch.py && python E_main.py"]