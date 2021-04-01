FROM nginx:1.19.8-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx.conf /etc/nginx/conf.d

CMD sed -i -e 's/$PORT/'"$PORT"'/g' /etc/nginx/conf.d/nginx.conf && nginx -g 'daemon off;'

# COPY ./nginx.conf /etc/nginx/conf.d/default.conf
# FROM jwilder/nginx-proxy
# COPY vhost.d/default /etc/nginx/vhost.d/default
# COPY custom.conf /etc/nginx/conf.d/custom.conf