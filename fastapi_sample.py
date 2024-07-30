from fastapi import FastAPI
from typing import Dict
from ray import serve
import ray
import subprocess
def install_dependencies():
    subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)

api = FastAPI()
@serve.deployment
@serve.ingress(api)
class MyModelDeployment:
    def __init__(self):
        self._msg = "WHY"
        install_dependencies()

    @api.get("/")
    def root(self) -> Dict:
        import os
        import pandas as pd
        return {"result": self._msg, "hostname": os.uname()[1], "pd_version":pd.__version__}

    @api.post("/ping")
    def ping(self,name:str) -> Dict:
        return {"result": f"pong {name}"}

app = MyModelDeployment.bind()
