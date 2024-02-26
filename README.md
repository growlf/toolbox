# Toolbox

[![GitHub Release](https://img.shields.io/github/v/release/growlf/toolbox?logo=docker&logoColor=white)](https://github.com/growlf/toolbox/pkgs/container/toolbox)
[![GitHub Tag](https://img.shields.io/github/v/tag/growlf/toolbox?logo=docker&logoColor=white&label=Latest)](https://github.com/growlf/toolbox/pkgs/container/toolbox)
![Docker Image Size with architecture (latest by date/latest semver)](https://img.shields.io/docker/image-size/netyeti/toolbox)

[![PyTest](https://github.com/growlf/toolbox/actions/workflows/python-app.yml/badge.svg)](https://github.com/growlf/toolbox/actions/workflows/python-app.yml)
[![ghcr.io](https://github.com/growlf/toolbox/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/growlf/toolbox/actions/workflows/docker-publish.yml)
[![Docker Hub](https://github.com/growlf/toolbox/actions/workflows/docker-publish-dh.yml/badge.svg)](https://github.com/growlf/toolbox/actions/workflows/docker-publish-dh.yml)

Containerized tools for on-the-go troubleshooting and developing in alien environments.

By: Garth Johnson & others

The purpose of this container image is to provide tools that can help diagnose issues and ease/simplify development struggles on alien envirnments.

Additionally, this container image can easily used for:

- devlopment new container prototypes
- debugging container builds and deployments
- educational intents for container development/examples (i.e. workflows and devcontainers)

You can find more at:

- source: https://github.com/growlf/toolbox/
- release images:
  - https://hub.docker.com/repository/docker/netyeti/toolbox/
  - https://ghcr.io/growlf/toolbox:latest

## Batteries included

### Custom Shell 

Using the `docker-compose.yml` file (included) makes certain tasks easier.  For example, opening a self-removing ZShell instance can be done lke so:

    docker compose run --rm app1

### Monitor packets in the local network

Using `tcpdump` can either be done from within a shell of the toolbox container, or direct commandline like so:

    docker run --rm -it --net=host ghcr.io/growlf/toolbox sudo tcpdump

### Running scripts and commands 

You can also run arbitrary commands and scripts directly from the commandline like so:

    docker compose run --rm -it app1 ./test_net.sh

## Using the Invoke Command

This image implements [Python Invoke](https://www.pyinvoke.org/), for managing shell-oriented subprocesses and organizing executable Python code into CLI-invokable tasks. There are a few basic tasks defined as examples already.

List available invoke commands from outside the container:

    docker compose exec app1 inv --list

Check internet speed using speedtest:

    docker compose exec app1 inv speedtest

Use a command that requires elevated privileges:

    docker compose exec -u root app1 inv dockerinfo

Some possible tasks to add-to/replace the default options:

- test for proxy in the environment
- test for internet access issues
- scan ports on target host
- get network response times
- setup a reverse proxy for remote shell (outbond from container host to remote support system)
- create a container project from defined template


## Use with Portainer

Use the `portainer-compose.yml` file and modify to your hearts content.

## Notes

- https://ohmyz.sh/#install
- https://github.com/deluan/zsh-in-docker/
- https://github.com/romkatv/powerlevel10k
- https://medium.com/nerd-for-tech/my-python-boilerplate-and-a-little-python-fu-e0ed59d97627
- https://pypi.org/project/portscan/
- https://docs.pyinvoke.org/en/stable/
- https://docker-py.readthedocs.io/en/stable/

