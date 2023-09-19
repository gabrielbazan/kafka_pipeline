# Simple Kafka Pipeline

This repo aims to show an example of how to implement a simple data pipeline with *Apache Kafka*. 

For our particular example, we'll build an API that receives some user data containing geographical coordinates, and behind it a pipeline that gets the timezone for the given coordinates, and then saves the processed data into a database. It is of course not a very useful pipeline, but it should give you an idea of how to build a pipeline that actually does a more complex processing.

We'll use technologies like *Apache Kafka*, *NGINX*, *Python*, *FastAPI*, *Docker*, and *MongoDB*.


## Architecture

First of all, lest take a look at the overall architecture, which of course would vary depending on your needs:
![Alt text](/docs/static/architecture.png?raw=true)


### Components

#### Load Balancer

Distributes the load across multiple instances of the _Ingestion API_.

It is a NGINX reverse proxy. Here you can find its [nginx.conf](/api_load_balancer/nginx.conf) file.

#### Ingestion API

This is the API that receives, validates and sends the data to an *Apache Kafka* topic (the *Raw Data Topic*) to be processed by the pipeline. It could be any kind of data.

In our implementation, it's a very simple FastAPI API.

And in our example, this API receives messages like the following:

```json
{
    "user_id": "user_A",
    "lat": -31.677696,
    "long": -65.030317,
    "timestamp": "2023-09-17T00:32:50.156000"
}
```

#### Raw Data Topic

It is an *Apache Kafka* topic, with multiple partitions (if needed). It stores the data produced by the *Ingestion API* into this topic.

When the *Ingestion API* produces a message into this topic, it uses the *User ID* as the *message key*.
 * This way, messages are distributed *consistently* across the available partitions. This means that the messages of a certain user will always be sent to the same partition. Depending on your needs, this could be really useful.
 * Enables *Paralellism* and *Horizontal scalability*. We take advantage of Kafka's partitions to increase throughput.

#### Data Processor

It consumes messages from the *Raw Data Topic*, and performs whatever processing you need and sends the processed data to the *Processed Data Topic*.

In our example, it adds a new "timezone" field to the data, based on its coordinates ("lat" and "long" fields). To do so, it uses [timezonefinder](https://timezonefinder.readthedocs.io/en/latest/index.html) and it's [in-memory mode](https://timezonefinder.readthedocs.io/en/latest/7_performance.html) to increase performance. Then, it sends it to the *Processed Data Topic* using the *User ID* as *message key*.

#### Processed Data Topic

It is another *Apache Kafka* topic, with multiple partitions (if needed). It stores the data produced by the *Data Processor* into this topic.

An example of a message from this topic:
```json
{
    "user_id": "user_A",
    "lat": -31.677696,
    "long": -65.030317,
    "timestamp": "2023-09-17T00:32:50.156000",
    "timezone": "America/Argentina/Cordoba"
}
```

#### Database Populator

A very simple process that consumes from the *Processed Data Topic* and inserts the data into the *Database*.

#### Database

It persists all the processed data. 

In our example, the processed data is the data that came from the API, plus an additional "timezone" field.

This data is stored in a single collection in a MongoDB instance.

An example of a record:

![An example of a record](/docs/static/mongodb_record_with_timezone.png?raw=true)


## Repo structure

It is a _Docker Compose_ application (at least in our local environment), with multiple services. Each service is dockerized and resides on its own folder:
 * [API Load Balancer (NGINX)](/api_load_balancer/).
 * [Ingestion API](/api/).
 * [Data Processor](/data_processor/).
 * [Database Sync](/database_sync/).

In a real-world project, each component would live in its own repository. Here we've chosen to have it all in a single repo to keep it simple, but all services are completely decoupled from each other.


## How to use

### Local environment setup (for development)

#### Install GIT Hooks (pre-commit)

```bash
make install_git_hooks
```

To manually run them:
```bash
make run_git_hooks
```

#### Create the virtualenv

```bash
make create_virtualenv
```

#### Install requirements

```bash
make install_requirements
make install_dev_requirements
```

### Tests

To run the tests, use:
```bash
make run_tests
```

### Services

#### Start services

```bash
make up
```

#### Stop services

```bash
make down
```

#### Cleanup

```bash
make rm
```


## Scaling

You can very simply adjust the number of partitions for both topics. This is a decision you make depending on your needs, but is as simple as setting the *RAW_DATA_TOPIC_PARTITIONS* and *PROCESSED_DATA_TOPIC_PARTITIONS* environment variables in the [.env](/.env) file. This will configure the number of partitions for these topics, __AND__ provision the same number of for consumers for them (_Data Processor_ and _Database Sync_).

By default, it runs:
 * 2 instances of the _Ingestion API_.
 * As many _Data Processors_ as specified by *RAW_DATA_TOPIC_PARTITIONS*.
 * As many _DatabaseSync_ as specified by *PROCESSED_DATA_TOPIC_PARTITIONS*.

And you can scale up or down with a single command:
```bash
docker compose up -d --scale api=10
```
