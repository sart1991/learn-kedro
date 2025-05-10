FROM --platform=linux/amd64 python:3.9-slim as runtime-environment

# Install Java (required for PySpark)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    default-jre \
    procps \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/* \

ENV JAVA_HOME=/usr/lib/jvm/default-java
# Add JAVA_HOME/bin to the PATH
ENV PATH=$JAVA_HOME/bin:$PATH

# update pip and install uv
RUN python -m pip install -U "pip>=21.2"
RUN pip install uv

# install project requirements
COPY requirements.txt /tmp/requirements.txt
RUN uv pip install --system --no-cache-dir -r /tmp/requirements.txt && rm -f /tmp/requirements.txt

# add kedro user
ARG KEDRO_UID=999
ARG KEDRO_GID=0
RUN groupadd -f -g ${KEDRO_GID} kedro_group && \
    useradd -m -d /home/kedro_docker -s /bin/bash -g ${KEDRO_GID} -u ${KEDRO_UID} kedro_docker

WORKDIR /home/kedro_docker
USER kedro_docker

FROM runtime-environment

# copy the whole project except what is in .dockerignore
ARG KEDRO_UID=999
ARG KEDRO_GID=0
COPY --chown=${KEDRO_UID}:${KEDRO_GID} . .

EXPOSE 8888

CMD ["kedro", "run"]