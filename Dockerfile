FROM openfabric/tee-python-cpu:latest

RUN mkdir application
WORKDIR /application

COPY poetry.lock pyproject.toml requirements.txt /application/

RUN pip install -r requirements.txt

COPY . .

RUN poetry install -vvv --no-dev

EXPOSE 5500

CMD ["sh", "start.sh"]