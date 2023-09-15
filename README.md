# Kafka Pipeline

## Architecture

![Alt text](/docs/static/architecture.png?raw=true)


### Components

#### Load Balancer

Distributes the load across multiple instances of the _Ingestion API_.
It is a NGINX reverse proxy. Here's its [nginx.conf](/api_load_balancer/nginx.conf).

#### WIP


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
 * 2 instances of the Ingestion API_.
 * As many _Data Processors_ as specified by *RAW_DATA_TOPIC_PARTITIONS*.
 * As many _DatabaseSync_ as specified by *PROCESSED_DATA_TOPIC_PARTITIONS*.

And you can scale up or down with a single command:
```bash
docker compose up -d --scale api=10
```
