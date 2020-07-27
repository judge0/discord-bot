FROM python:3.7
RUN pip install --no-cache-dir pipenv

WORKDIR /bot

COPY Pipfile* ./
RUN pipenv install

COPY . .

CMD ["pipenv", "run", "start"]

LABEL maintainer="Herman Zvonimir Došilović <hermanz.dosilovic@gmail.com>"
