FROM python:3.10

# main dir
WORKDIR /searchservice

# copy paste files
COPY ./poetry.lock /searchservice
COPY ./pyproject.toml /searchservice
COPY ./src /searchservice/src
COPY ./main.py /searchservice/main.py


# instal environment
RUN pip3 install poetry
# RUN poetry config virtualenvs.create false
RUN poetry install


# run application
# ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
# ENTRYPOINT ["poetry", "run", "python", "main.py"]

# ENTRYPOINT ["poetry", "run", "start_app"]
