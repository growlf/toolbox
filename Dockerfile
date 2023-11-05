FROM python:3.11-slim-bullseye

# Install updates and docker
RUN apt-get -yq update && apt-get -yq install \
        curl \
        gnupg \
    && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - \
    && echo "deb https://download.docker.com/linux/ubuntu focal stable" | tee /etc/apt/sources.list.d/docker.list \
    && apt-get -yq update \
    && apt-get -yq install --no-install-recommends \
        docker-ce-cli docker-compose

# Install apps/tools
RUN apt-get -yq install --no-install-recommends \
        mosquitto-clients \
        nano vim less \
        tcpdump traceroute iproute2 dnsutils whois mtr iftop iputils-ping \
        dialog htop \
        netcat-traditional \
        wget nmap \
        zsh git \
        sudo \
    # Clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# ensure that there is a place to mount the host files
RUN mkdir /host

# Set tthe working directory for installations and login
WORKDIR /app

# Copy in any/all additional files from our project
ADD src .

# Istall Python basic libraries
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Setup a user to match the host and reduce the frustration/confusion of file ownership
ARG USERNAME=netyeti
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME
USER $USERNAME

# Install ZSH, OhMyZSH, themes and plugins
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
RUN ./zsh-in-docker.sh \
    -p git \
    -p https://github.com/zsh-users/zsh-autosuggestions \
    -p https://github.com/zsh-users/zsh-completions \
    -p https://github.com/zsh-users/zsh-history-substring-search \
    -p https://github.com/zsh-users/zsh-syntax-highlighting \
    -p 'history-substring-search' \
    -p docker \
    -p colorize \
    -p invoke \
    -p aws \
    -p sudo \
    -p tig \
    -p dirhistory \
    -a 'bindkey "\$terminfo[kcuu1]" history-substring-search-up' \
    -a 'bindkey "\$terminfo[kcud1]" history-substring-search-down'

# Set default command
CMD ["/bin/zsh"]