FROM python:3.6

COPY quoter /quoter
COPY requirements/quoter_requirements.txt /quoter/quoter_requirements.txt
WORKDIR /quoter

RUN pip3 install --upgrade pip -r quoter_requirements.txt

EXPOSE 8000
ENTRYPOINT ["gunicorn", "--config", "gunicorn_config.py", "--bind", ":8000", "app:api"]