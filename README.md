# Toolbox

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
  - ghcr.io/growlf/toolbox:latest

## Examples

### Monitor packets in local network

Using `tcpdump` can either be done from within a shell of the toolbox container, or direct commandline like so:

    docker run --rm -it --net=host ghcr.io/growlf/toolbox sudo tcpdump

### Running scripts and commands

You can also run arbitrary commands and scripts directly from the commandline like so:

    docker compose run --rm -it app1 ./test_net.sh

## Invoke

Some tasks to add to the default options:

- test for proxy
- test for internet access
- scan ports on target
- get network response times
- setup a reverse proxe for remote shell (outbond from container host to remote support system)

## Notes

- https://ohmyz.sh/#install
- https://github.com/deluan/zsh-in-docker/
- https://github.com/romkatv/powerlevel10k
- https://medium.com/nerd-for-tech/my-python-boilerplate-and-a-little-python-fu-e0ed59d97627
- https://pypi.org/project/portscan/
- https://docs.pyinvoke.org/en/stable/
- https://docker-py.readthedocs.io/en/stable/
