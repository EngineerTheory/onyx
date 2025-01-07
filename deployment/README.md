<!-- DANSWER_METADATA={"link": "https://github.com/onyx-dot-app/onyx/blob/main/deployment/README.md"} -->

# Deploying ONYX

The two options provided here are the easiest ways to get ONYX up and running.
All the features of ONYX are fully available regardless of the deployment option.

For information on setting up connectors, check out https://docs.onyx.app/connectors/overview

## Docker Compose

Docker Compose provides the easiest way to get ONYX up and running.

This section is for getting started quickly without setting up GPUs. For deployments to leverage GPU, please refer to [this](https://github.com/onyx-dot-app/onyx/blob/main/deployment/docker_compose/README.md) documentation.

1. To run ONYX, navigate to `docker_compose` directory and run the following:
   - `docker compose -f docker-compose.dev.yml -p onyx-stack up -d --pull always --force-recreate` - or run: `docker compose -f docker-compose.dev.yml -p onyx-stack up -d --build --force-recreate`
   - To stop the containers: `docker compose -f docker-compose.dev.yml -p onyx-stack stop`
   - To delete the containers: `docker compose -f docker-compose.dev.yml -p onyx-stack down`

3. To completely remove ONYX run:
   - `docker compose -f docker-compose.dev.yml -p onyx-stack down -v`

## Kubernetes

1. To run ONYX, navigate to `kubernetes` directory and run the following:
   - `kubectl apply -f .`

2. To remove ONYX, run:
   - `kubectl delete -f .`
