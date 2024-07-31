from fastapi import FastAPI
from typing import Dict
from ray import serve
import ray

api = FastAPI()
@serve.deployment
@serve.ingress(api)
class MyModelDeployment:
    def __init__(self):
        self._msg = "WHY"

    @api.get("/")
    def root(self) -> Dict:
        import os
        import pandas as pd
        current_file_location = os.path.abspath(__file__)
        return {"result": self._msg, "hostname": os.uname()[1], "pd_version":pd.__version__, "current_file_location":current_file_location}

    @api.post("/ping")
    def ping(self,name:str) -> Dict:
        return {"result": f"pong {name}"}

app = MyModelDeployment.bind()
