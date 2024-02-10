FROM python:3.10-slim

WORKDIR /app

# Copia solo los archivos necesarios para instalar dependencias primero para aprovechar la caché de Docker
COPY Pipfile Pipfile.lock /app/

# Instala las dependencias
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

# Copia el resto de los archivos
COPY . /app/

EXPOSE 3000

# Comando para iniciar el servidor
CMD pipenv run gunicorn -w 4 -b 0.0.0.0:3000 src.app:app --log-file -

