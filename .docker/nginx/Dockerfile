FROM nginx:latest

ADD nginx.conf /etc/nginx/nginx.conf

RUN mkdir -p /etc/ssl/cert/
ADD ./ssl/* /etc/ssl/cert/
