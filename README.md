# Toolbox

Containerized tools for on the go troubleshooting

By: Garth Johnson & others

The purpose of this container image is to provide tools that I use on a regular basis and would like to use on other systems without installing them to the bare-metal (leave minimal footprint and cleanup).

Additionally, this container can also be easily used for 

- devlopment new container prototypes
- debugging container builds and deployments
- educational intents for container development/examples

You can find more at:

- source: https://github.com/growlf/toolbox/
- image: https://hub.docker.com/repository/docker/netyeti/toolbox/

## Examples

### Monitor packets in local network

Using `tcpdump` can either be done from within a shell of the toolbox container, or direct commandline like so:

    docker run --rm -it --net=host ghcr.io/growlf/toolbox sudo tcpdump

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


[![Docker](https://github.com/growlf/toolbox/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/growlf/toolbox/actions/workflows/docker-publish.yml)