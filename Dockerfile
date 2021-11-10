FROM python:3.8

WORKDIR /flaskProject

RUN pip install -U pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_IN_PROJECT=1 pipenv install --deploy --system
COPY ./ .

EXPOSE 5000
CMD ["python", "./wsgi.py"]
