# Настройки подключения к БД (DATABASE_URL, DSN)

DB_USER = "postgres"
DB_PASS = "1"
DB_HOST = "localhost"
DB_PORT = "5433"
DB_NAME = "logistic_company"

DATABASE_DSN = f"host={DB_HOST} dbname={DB_NAME} user={DB_USER} password={DB_PASS} port={DB_PORT}"
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"