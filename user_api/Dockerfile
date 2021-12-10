FROM python:3.8

LABEL maintainer='Washington Barbosa <wassuncaon@gmail.com>'

WORKDIR /user_api
COPY . /user_api

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip uninstall Werkzeug==1.0.1 -y
RUN pip install --no-cache-dir -r requirements-dev.txt

ENV FLASK_RUN_PORT=8080
ENV DATABASE_URL='postgresql://postgres:postgres@localhost:5432/user_db'

EXPOSE 8080

ENTRYPOINT ["python3"]
CMD ["main.py"]
