from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from service import UserServices
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from prometheus_client import start_http_server
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


reader = PrometheusMetricReader()
meter_provider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(meter_provider)

meter = metrics.get_meter("api.metrics")

register_counter = meter.create_counter(
    name="user_registration_total",
    description="Total number of users registered",
    unit="1"
)

def cpu_check_callback(options):
    import random
    yield metrics.Observation(random.randint(15, 40))

meter.create_observable_gauge(
    name="system_cpu_usage",
    description="Asynchronous observation of CPU usage",
    callbacks=[cpu_check_callback],
    unit="%",
)

FastAPIInstrumentor.instrument_app(app, meter_provider=meter_provider)

start_http_server(8042)


@app.on_event("startup")
async def initialize_metrics():
    register_counter.add(0, {"status": "success"})
    register_counter.add(0, {"status": "failed", "reason": "validation"})
    register_counter.add(0, {"status": "failed", "reason": "server_error"})
    print("🚀 CANTER INITIALIZED SUCCESSFULLY!")


class UserRegisterSchema(BaseModel):
    name: str
    email: str


@app.post("/register")
def register(user: UserRegisterSchema):
    try:
        result = user_services.register_new_user(user.model_dump())
        register_counter.add(1, {"status": "success"})
        return {"status": "success", "data": result}
    except ValueError as e:
        register_counter.add(1, {"status": "failed", "reason": "validation"})
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        register_counter.add(1, {"status": "failed", "reason": "server_error"})
        print("ERROR LOG:", e)
        raise HTTPException(status_code=500, detail="Internal server error")
