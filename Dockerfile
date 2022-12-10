FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code


COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
CMD ['sh', 'code/posstgres_config.sh']
COPY . /