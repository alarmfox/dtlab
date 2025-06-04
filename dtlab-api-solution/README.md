# DTLAB-API
This is an activity for DTLAB class about chapters 5-6 of DEVASC course.

## Description

You will work together to create a simple REST service that manages network devices.

The app will provide 3 core functionalities:
* **Managing switches**: users will have a CRUD interface for switches;
* **Managing routers**: users will have a CRUD interface for routers;

You will work to create a Docker deployment for this Flask application.

## Instructions

### Part 1 - Create a development environment

The application uses [Flask](https://flask.palletsprojects.com/en/2.1.x/) and [Postgres](https://www.postgresql.org/docs/). 
First of all, as you learned in *Module 1*, you will have to create a new virtual environment for Python which will be used to install project dependencies.

Then you may install project requirements with the following command:

```sh
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

We will use *Postgresql*. It is a relational database (all data is stored into tables).
Start a Postgres instance using Docker. The application loads database configuration from `.env` file. In order to start Postgres, use the following command:

```sh
docker run -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:alpine
```

*Think*: what does this command do? Try to understand every parameter to be able to explain it to other groups!

*WARNING* The application reads the database connection string from `.env` file. If you change the `POSTGRES_PASSWORD` you must adapt the `.env` password with your password. You should know 
that the standard format for a complete Postgres URI is: `postgresql://user:password@hostname:port/database_name?query_params`.

Now let's create the REST server using Flask, using the following command:

```sh
flask run
```

*HINT* to enable hot reload (the application restarts when you modify a file) when developing, use `--debug` flag when running the application:

```sh
flask run --debug
```

Now you can try the application in Postman using the collection provided in `DTLab API.postman_collection.json` (you will have to import it).

## Prepare a Dockerfile

To build a Docker image, you will need a Dockerfile. Create a Dockerfile in the root folder of the project and use the activity `6.2.7` as reference.
A Dockerfile must have 3 sections:
* **FROM** directive: specify a base image. You will need something with a Python environment set up;
* **COPY** directive: copy all source code in the image;
* **ENTRYPOINT** directive: give a command to start the application;

## Build a Docker image
You can build the image with the following command:

```sh
docker build -t <image_name> .
```

## Run the image

Run the built image with the following command:

```sh
docker run -p 5000:5000 -e DB_URI=postgresql://postgres:postgres@localhost:5432/postgres?sslmode=disable <image_name>
```

### Discuss in class
Does the application work? Why? Discuss with your instructor.

## A more real-life example
Building an image manually from a Dockerfile is fine for small applications. Imagine your service has 6 images. The deploy process will be very boring and error prone. There's an automated way of executing all these Docker commands: docker-compose. Docker-compose is a python script that generates Docker commands from a .yml file. In this repository you will find a `docker-compose.yml` file. As you can see, the database is already there and you will need to create a similar structure for your application, as shown in the following steps:

* Below the database, add an `app` object with the following data:
```yaml
app:
    build: .
    environment:
        - DB_URI=postgresql://postgres:postgres@db:5432/postgres?sslmode=disable
    depends_on:
        - db
```

Now you can try to spin up the application with the following command:

```sh
docker-compose up
```
