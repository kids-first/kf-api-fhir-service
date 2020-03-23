FROM nginx:latest

WORKDIR /etc/nginx

RUN apt-get update -y && apt-get install -y vim procps iputils-ping openssl

RUN rm -f /etc/nginx/conf.d/default.conf

RUN mkdir ssl
COPY ssl/ ssl/

RUN cd ssl && openssl req -x509 -newkey rsa:2048 -out ca.cer -outform PEM \
   -keyout ca.pvk -days 10000 -verbose -config ca.cnf -nodes -sha256 \
   -subj "/CN=localhost" && \
   openssl req -newkey rsa:2048 -keyout server.pvk -out server.req \
    -subj "/CN=localhost" -sha256 -nodes && \
    openssl x509 -req -CA ca.cer -CAkey ca.pvk -in server.req -out server.cer \
    -days 10000 -extfile server.ext -sha256 -set_serial 0x1111 && \
    openssl dhparam -out dhparams.pem 2048
