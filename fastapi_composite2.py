from fastapi import FastAPI
from pydantic import BaseModel
from ray import serve
from ray.serve.handle import DeploymentHandle, DeploymentResponse

app = FastAPI()

@serve.deployment
@serve.ingress(app)
class Adder:
    def __init__(self, increment: int):
        self._increment = increment

    @app.get("/add/{val}")
    def add(self, val: int) -> int:
        return val + self._increment


@serve.deployment
@serve.ingress(app)
class Multiplier:
    def __init__(self, multiple: int):
        self._multiple = multiple
    
    @app.get("/mult/{val}")
    def mult(self, val: int) -> int:
        return val * self._multiple


@serve.deployment
@serve.ingress(app)
class Ingress:
    def __init__(self, adder, multiplier):
        self._adder = adder
        self._multiplier = multiplier

    @app.get("/process/{input}")
    async def process(self, input: int) -> int:
        adder_response: DeploymentResponse = self._adder.add(input)
        # Pass the adder response directly into the multipler (no `await` needed).
        multiplier_response: DeploymentResponse = self._multiplier.mult(adder_response)
        # `await` the final chained response.
        return await multiplier_response

adder = Adder.bind(increment=1)
multiplier = Multiplier.bind(multiple=2)
ingress = Ingress.bind(adder, multiplier)
