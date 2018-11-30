FROM python:3.6

COPY quoter /quoter
WORKDIR /quoter

RUN pip3 install --upgrade pip -r requirements/quoter_requirements.txt

EXPOSE 8000
ENTRYPOINT ["gunicorn", "--config", "configs/gunicorn_config.py", "app:create_app()"]