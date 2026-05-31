from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from service import UserServices

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

app = FastAPI(title="Telemetry and Architecture Hub")
user_services = UserServices()

resource = Resource(attributes={"service.name": "MONITORING"})
provider = TracerProvider(resource=resource)

local_jaeger_exporter = OTLPSpanExporter(
    endpoint="http://localhost:4318/v1/traces"
)

processor = BatchSpanProcessor(local_jaeger_exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

FastAPIInstrumentor.instrument_app(app)

class UserRegisterSchema(BaseModel):
    name: str
    email: str

@app.post("/register")
def register(user: UserRegisterSchema):
    try:
        result = user_services.register_new_user(user.model_dump())
        return {"status": "success", "data": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print("ERROR LOG:", e)
        raise HTTPException(status_code=500, detail="Internal server error")