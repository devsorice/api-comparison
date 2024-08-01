FROM alpine:latest

# Install lighttpd
RUN apk update && apk add lighttpd

# Create directories for lighttpd
RUN mkdir -p /var/www/localhost/htdocs
RUN mkdir -p /etc/lighttpd

# Copy lighttpd configuration file
COPY lighttpd.conf /etc/lighttpd/lighttpd.conf

# Copy static files to the web server directory
COPY ./ /var/www/localhost/htdocs

# Expose port 80
EXPOSE 80

# Start lighttpd
CMD ["lighttpd", "-D", "-f", "/etc/lighttpd/lighttpd.conf"]
