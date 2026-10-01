# nhl_immaculate API

## backend setup
- uv installed (pip install uv)
- run uv sync/lock
- start venv (./.venv/Scripts/activate.bat)
- flask --app main.py run / python main.py
- for docs, we have Swagger (using flasgger) at /apidocs

## running with docker
- `docker build -t immaculate-api .`
- `docker run -d --name immaculate-api-dev --env-file .env.{ENV} -p 8000:8000 immaculate-api`

# info
- originally part of nhl immaculate project, broken out so that it could be run separately (consumed by different applications)