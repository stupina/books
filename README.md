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
```

3. Initialize database
```bash
docker-compose up -d db
docker-compose run --rm api /bin/bash -c "python -c  'import api.db as db; db.init_db()'"
```

4. Bring up the app
```bash
docker-compose up
```

5. Browse to [link](http://localhost:5000) to see the app in action.
