from repository import UserRepository
from opentelemetry import trace

tracer = trace.get_tracer("service.tracer")

class UserServices:
    def __init__(self):
        self.repository = UserRepository()

    def register_new_user(self, user_data: dict) -> dict:
        with tracer.start_as_current_span("service_register_pipeline") as span:
            existing_user = self.repository.get_user_by_email(user_data["email"])
            if existing_user:
                raise ValueError("User with this email already exists.")
            return self.repository.save_user(user_data)