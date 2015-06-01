FROM debian:jessie
MAINTAINER Haoyu Tan <haoyutan@gmail.com>

# add msa user and group
RUN groupadd msa && useradd -g msa msa

# grab gosu for easy step-down from root
RUN gpg --keyserver pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/* \
	&& curl -o /usr/local/bin/gosu -SL "https://github.com/tianon/gosu/releases/download/1.4/gosu-$(dpkg --print-architecture)" \
	&& curl -o /usr/local/bin/gosu.asc -SL "https://github.com/tianon/gosu/releases/download/1.4/gosu-$(dpkg --print-architecture).asc" \
	&& gpg --verify /usr/local/bin/gosu.asc \
	&& rm /usr/local/bin/gosu.asc \
	&& chmod +x /usr/local/bin/gosu \
	&& apt-get purge -y --auto-remove curl

# make the "en_US.UTF-8" locale
RUN apt-get update && apt-get install -y locales \
	&& rm -rf /var/lib/apt/lists/* \
	&& localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

# install softwares
RUN apt-get update && apt-get install -y tar openssl nginx
RUN apt-get update && apt-get install -y python3.4 python3.4-venv python3-pip

COPY entrypoint.sh /entrypoint.sh
COPY msa-entrypoint.sh /msa-entrypoint.sh

EXPOSE 8443

ENTRYPOINT ["/entrypoint.sh"]
CMD ["start"]
