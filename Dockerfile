FROM python:3.10-slim

WORKDIR /melipolibre-api

COPY . /melipolibre-api
RUN mkdir -p run/
RUN pip install --no-cache-dir -r requirements.txt
CMD ["task", "api_run"]

