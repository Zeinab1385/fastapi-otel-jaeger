import psycopg2
from psycopg2.extras import RealDictCursor
from opentelemetry import trace

tracer = trace.get_tracer("repository.tracer")

class UserRepository:
    def __init__(self):
        self.db_config ={
            "dbname":"telemetry_db",
            "user":"postgres",
            "password":"1234",
            "host":"localhost",
            "port":"5432"
        }

    def _get_connection(self):
        return psycopg2.connect(**self.db_config , cursor_factory=RealDictCursor)

    def save_user(self,user_data:dict)->dict:
        query="insert into users (name , email) values(%s, %s) returning id , name , email;"

        with tracer.start_as_current_span("repository_save_user_database") as span:
            span.set_attribute("user.email", user_data["email"])

            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (user_data["name"], user_data["email"]))
                    result = cur.fetchone()
                    conn.commit()
                    return dict(result)

    def get_user_by_email(self,email:str)->dict:
        query="select * from users where email=%s;"

        with tracer.start_as_current_span("repository_get_user_by_email") as span:

            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query,(email,))
                    result = cur.fetchone()
                    return dict(result) if result else None