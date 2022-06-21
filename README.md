# Introduce

# URLS
## Local
* [Admin](http://localhost:8000/admin/) 

# Develop
## Deploy
- create virtualenv & install requirements
```bash
pyenv virtualenv 3.9.1 blabla_bot
pyenv activate blabla_bot
pip install -U pip poetry
poetry install
``` 
- `pre-commit install`
- create DB in Postgres
- add envs from [.env.dev](.docker/.env.debug)
- apply DB migrations ```./manage.py migrate```
- create super user ```./manage.py create_super_user```

## Run WEB
- runserver ```./manage.py runserver```
- open [localhost:8000/admin/sup-sec/](http://localhost:8000/admin/) and login with created user credentials

## Run Telegram bot
- runserver ```./manage.py run_bot```

## Commit
- call `make pre-commit` before a new commit

## Running tests
To running tests deploy the project according to point above and add to envs ```ROLE=tests```

### Create certs for bot
```shell
openssl req -newkey rsa:2048 -sha256 -nodes -keyout .docker/nginx/ssl/cert.key -x509 -days 3650 -out .docker/nginx/ssl/cert.pem -subj "/C=US/ST=New York/L=Brooklyn/O=Example Brooklyn Company/CN=bot.${DOMAIN}"
```

Put SSL cert to .docker/nginx/ssl/private.key & .docker/nginx/ssl/certificate.crt . 