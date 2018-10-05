FROM ubuntu:14.04

# Update package list and upgrade all packages
RUN apt-get -qq update

# Add PG apt repo:
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main" > "/etc/apt/sources.list.d/pgdg.list"

# Add PGDG repo key:
RUN DEBIAN_FRONTEND=noninteractive apt-get -qq install -y wget && wget --quiet -O - https://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | apt-key add -

#  Install PostgreSQL
#  There are some warnings (in red) that show up during the build. You can hide
#  them by prefixing each apt-get statement with DEBIAN_FRONTEND=noninteractive
ENV PG_VERSION=9.6
ARG PGIS_VERSION=2.3
ARG APP_DB_NAME=toopath
ARG APP_DB_USER=django
ARG APP_DB_PASS=toopath3

RUN apt-get -qq update && DEBIAN_FRONTEND=noninteractive apt-get -qq install -y postgresql-${PG_VERSION} postgresql-contrib-${PG_VERSION}

# Explicitly set default client_encoding
ARG PG_CONF="/etc/postgresql/${PG_VERSION}/main/postgresql.conf"
ARG PG_HBA="/etc/postgresql/${PG_VERSION}/main/pg_hba.conf"

# Adjust PostgreSQL configuration so that remote connections to the database are possible.
RUN echo "host all  all    0.0.0.0/0  md5" >> "${PG_HBA}"

# And add ``listen_addresses`` to ``postgresql.conf``
RUN sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" "${PG_CONF}"
RUN echo "client_encoding = utf8" >> "${PG_CONF}"

RUN DEBIAN_FRONTEND=noninteractive apt-get -qq install -y postgresql-${PG_VERSION}-postgis-${PGIS_VERSION}

# Run the rest of the commands as the ``postgres`` user created by the ``postgres`` package when it was ``apt-get installed``
USER postgres

# Create a PostgreSQL role named ``docker`` with ``docker`` as the password and
# then create a database `docker` owned by the ``docker`` role.
# Note: here we use ``&&\`` to run commands one after the other - the ``\``
#       allows the RUN command to span multiple lines.
RUN    /etc/init.d/postgresql start &&\
    psql --command "CREATE USER ${APP_DB_USER} WITH SUPERUSER PASSWORD '${APP_DB_PASS}';" &&\
    psql --command "CREATE DATABASE ${APP_DB_NAME} WITH OWNER=${APP_DB_USER} ENCODING='UTF8' TEMPLATE=template0;" &&\
    psql -d ${APP_DB_NAME} --command "CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology"


ENV PATH $PATH:/usr/lib/postgresql/${PG_VERSION}/bin
ENV PGDATA /var/lib/postgresql/data
RUN mkdir -p "$PGDATA" && chown -R postgres:postgres "$PGDATA" && chmod 777 "$PGDATA"

# Add VOLUMEs to allow backup of config, logs and databases
VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

# Expose the PostgreSQL port
EXPOSE 5432

# Set the default command to run when starting the container
#CMD ["/bin/bash"]
CMD /usr/lib/postgresql/${PG_VERSION}/bin/postgres -D /var/lib/postgresql/${PG_VERSION}/main -c config_file=/etc/postgresql/${PG_VERSION}/main/postgresql.conf