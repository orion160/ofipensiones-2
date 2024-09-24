# baremetal

## web

```
sudo apt update -y

sudo apt upgrade -y

curl -LsSf https://astral.sh/uv/install.sh | sh

git clone <url> ofipensiones

cd ofipensiones

uv sync --frozen --no-dev --compile-bytecode

. .venv/bin/activate

# configure launch environment variables
# on linux
. set_vars.sh
# on windows
.\set_vars.ps1

cd ofipensiones

gunicorn ofipensiones.wsgi -w <ncores> -b <listen_ip>:8000
```

Also run 

```
. .venv/bin/activate

python run manage.py collectstatic
```

download the generated folder and delete it from VM.

## postgres

```
sudo apt update -y

sudo apt upgrade -y

sudo -u postgres psql

sudo -u postgres psql

CREATE USER ofipensiones_web;

CREATE DATABASE ofipensiones_andes OWNER ofipensiones_web;

ALTER USER ofipensiones_web WITH PASSWORD 'passwd';
```

```
sudo vim /etc/postgresql/15/main/postgresql.conf

// Add at /etc/postgresql/15/main/postgresql.conf
listen_addresses = '<internal ips>'
```

```
// Add at /etc/postgresql/15/main/pg_hba.conf

# IPv4 remote connections
host    all             all             0.0.0.0/0               scram-sha-256
```

## nginx

override `/etc/nginx/sites-availabile/default`

```
upstream ofipensiones {
    server <internal_ip>:8000;
    server <internal_ip>:8000;
}

server {
    listen 80;

    location = /favicon.ico { 
        access_log off; 
        log_not_found off; 
    }

    location /static/ {
        alias /staticfiles/;
    }

    location / {
        proxy_pass http://ofipensiones;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
}
```

The static files from django are uploaded into the VM at `/staticfiles/`.

## deploy

- 2 web servers (DJANGO) - port 8000
- DB (postgres) - port 5432
- load balancer & reverse proxy (nginx) - port 80

create 2 firewalls

- http-ofipensiones - allow 80
- postgres-ofipensiones - allow 5432

Recomendacion `GCP` VM

- `n4-highcpu-2` (2 V-core, 4GB RAM)
