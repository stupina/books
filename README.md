# books
Project about authors and their books

## Bringing up

1. Clone this project and go to the directory
```bash
git clone https://github.com/stupina/books && cd books
```

2. Add file "env_file" to the our root directory. Add to params to file:
```bash
POSTGRES_USER=postgres_user
POSTGRES_PASSWORD=postgres_user_password
POSTGRES_DB=postgress_db_name
APP_SECRET_KEY=app_secret_key
FLASK_APP=main.py
```

3. Bring up the app
```bash
docker-compose up -d
docker-compose run --rm api /bin/bash -c "flask db init && flask db migrate && flask db upgrade"
```

4. Browse to [link](http://localhost:5000) to see the app in action.
