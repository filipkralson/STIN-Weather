FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl apt-transport-https gnupg
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

WORKDIR /app
COPY . /app/

RUN pip install gunicorn
RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "app:create_app(option=',')", "-b", "0.0.0.0:8000"]

