
#access_log  /var/log/nginx/access.log;
#error_log  /var/log/nginx/error.log info;

server {
    listen ${LISTEN_PORT};

    location /static {
        alias /vol/static;
    }

    location / {    
        uwsgi_pass              ${APP_HOST}:${APP_PORT};
        include                 /etc/nginx/uwsgi_params;
        client_max_body_size    10M;
    }
}