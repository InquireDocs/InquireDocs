

host = "test_host"
port = 1234
db = "test_db"
user = "test_user"
password = "test_password"

CONNECTION_STRING = PGVector.connection_string_from_db_params(
    driver="psycopg",
    host=host,
    port=port,
    database=db,
    user=user,
    password=password,
)
