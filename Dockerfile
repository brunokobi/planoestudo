FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY agenda/ /usr/share/nginx/html/
COPY plano-ppcomp-2027.html /usr/share/nginx/html/plano.html
EXPOSE 80
