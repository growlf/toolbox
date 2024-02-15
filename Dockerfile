FROM python:3.12-slim-bullseye

# Passed from Github Actions
ARG GIT_VERSION_TAG=unspecified
ARG GIT_COMMIT_MESSAGE=unspecified
ARG GIT_VERSION_HASH=unspecified

# Install updates and docker
RUN apt-get -yq update && apt-get -yq install \
        curl \
        gnupg \
    && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - \
    && echo "deb https://download.docker.com/linux/debian bullseye stable" | tee /etc/apt/sources.list.d/docker.list \
    && apt-get -yq update \
    && apt-get -yq install --no-install-recommends \
        docker-ce-cli docker-compose-plugin

# Install apps/tools
RUN apt-get -yq install --no-install-recommends \
        sudo openssh-client mosquitto-clients \
        nano vim less \
        zsh git rsync bzip2 \
        tcpdump traceroute iproute2 dnsutils whois mtr iftop iputils-ping wget nmap netcat-traditional \
        procps \
        htop \
        screen tmux \
        unzip zip \
        jq \
        build-essential \
        software-properties-common \
        tree \
        lsof \
        fish \
        && sh -c "curl -fsSL https://starship.rs/install.sh | bash -s -- --yes" \
        && apt-get clean -y \
        && rm -rf /var/lib/apt/lists/*

# ensure that there is a place to mount the host files
RUN mkdir /host

# Set the working directory for installations and login
WORKDIR /app

# Copy in any/all additional files from our project
ADD src/requirements.txt .

# Install Python basic libraries
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Setup a user to match the host and reduce the frustration/confusion of file ownership
ARG USERNAME=ubuntu
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME && groupadd --gid 999 docker \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME
RUN usermod -aG docker $USERNAME

# You can read these files for the information in your application
RUN echo $GIT_VERSION_TAG > GIT_VERSION_TAG.txt
RUN echo $GIT_COMMIT_MESSAGE > GIT_COMMIT_MESSAGE.txt
RUN echo $GIT_VERSION_HASH > GIT_VERSION_HASH.txt

# Switch to the user now so that file ownership matches
USER $USERNAME

# Install ZSH, OhMyZSH, themes and plugins
ADD --chown=1000:1000  --chmod=+x src/zsh-in-docker.sh .
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
    -p history \
    -a 'bindkey "\$terminfo[kcuu1]" history-substring-search-up' \
    -a 'bindkey "\$terminfo[kcud1]" history-substring-search-down' \
    -a '[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh'
#    -p fzf-zsh-plugin \
ADD --chown=1000:1000 src/.p10k.zsh /home/$USERNAME/.p10k.zsh

ADD --chown=1000:1000 src/.zshrc /home/$USERNAME/.zshrc
ADD --chown=1000:1000 src/.p10k.zsh /home/$USERNAME/.p10k.zsh

ADD --chown=1000:1000 --chmod=+x src/tasks.py .
ADD --chown=1000:1000 --chmod=+x https://private-sw-downloads.s3.amazonaws.com/archfx_broker/preflight/broker_preflight.sh .

ADD --chown=1000:1000 --chmod=+x src/test_net.sh .
ADD --chown=1000:1000 src/nodes.list .

# Set default command
CMD ["/bin/zsh"]
