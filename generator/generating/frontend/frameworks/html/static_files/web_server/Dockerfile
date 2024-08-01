# Stage 1: Build lighttpd with required modules
FROM alpine:3.20.2 AS build

ARG VERSION="1.4.76"
ARG CHECKSUM="ba14a030889518194fd88b33e419d51cc38c8fe917126d5a7a965be79b53e995"

ADD https://download.lighttpd.net/lighttpd/releases-1.4.x/lighttpd-$VERSION.tar.gz /tmp/lighttpd.tar.gz

RUN [ "$(sha256sum /tmp/lighttpd.tar.gz | awk '{print $1}')" = "$CHECKSUM" ] && \
  apk add bsd-compat-headers build-base pcre2-dev scons && \
  tar -C /tmp -xf /tmp/lighttpd.tar.gz && \
  cd /tmp/lighttpd-$VERSION && \
  scons -j 4 build_fullstatic=1 build_dynamic=0

RUN mkdir -p /rootfs/bin && \
  cp /tmp/lighttpd-$VERSION/sconsbuild/fullstatic/build/lighttpd /rootfs/bin/ && \
  mkdir -p /rootfs/etc /rootfsvar/tmp && \
  echo "nogroup:*:10000:nobody" > /rootfs/etc/group && \
  echo "nobody:*:10000:10000:::" > /rootfs/etc/passwd

###############################################################
###############################################################
###############################################################
# Stage 2: Create a minimal runtime environment using scratch##
FROM scratch as base
COPY --from=build --chown=10000:10000 /rootfs /

## WE ARE NOT RUNNING AS ROOT
USER 10000:10000

# THE HTTP SERVER RUNS AT PORT 80
EXPOSE 80

# Set the entrypoint to lighttpd
ENTRYPOINT ["/bin/lighttpd"]
CMD ["-D", "-f", "/lighttpd.conf"]

###################################################################
###################################################################
############# This is the container that will run our app #############
FROM base as server
# Copy lighttpd configuration file
COPY lighttpd.conf /lighttpd.conf
# Copy static files to the web server directory
COPY ./ /var/www/localhost/htdocs
