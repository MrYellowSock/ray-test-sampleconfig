from pydantic import BaseModel
from ray import serve
from ray.serve.handle import DeploymentHandle, DeploymentResponse

@serve.deployment
class Adder:
    def __init__(self, increment: int):
        self._increment = increment

    def __call__(self, val: int) -> int:
        return val + self._increment


@serve.deployment
class Multiplier:
    def __init__(self, multiple: int):
        self._multiple = multiple

    def __call__(self, val: int) -> int:
        return val * self._multiple


@serve.deployment
class Ingress:
    def __init__(self, adder: DeploymentHandle, multiplier: DeploymentHandle):
        self._adder = adder
        self._multiplier = multiplier

    async def __call__(self, input: int) -> int:
        adder_response: DeploymentResponse = self._adder.remote(input)
        # Pass the adder response directly into the multipler (no `await` needed).
        multiplier_response: DeploymentResponse = self._multiplier.remote(adder_response)
        # `await` the final chained response.
        return await multiplier_response

adder = Adder.bind(increment=1)
multiplier = Multiplier.bind(multiple=2)
ingress = Ingress.bind(adder, multiplier)
