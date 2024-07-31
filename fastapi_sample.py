from fastapi import FastAPI
from typing import Dict
from ray import serve
import ray
import subprocess
import sys

def install():
    return subprocess.check_call([sys.executable, "-m", "pip", "install", "-r requirements.txt"],
        check=True,
        capture_output=True,
        text=True)

api = FastAPI()
@serve.deployment
@serve.ingress(api)
class MyModelDeployment:
    def __init__(self):
        self._msg = "WHY"
        try:
            result = install()
            self._msg = result.stdout
        except subprocess.CalledProcessError as e:
            self._msg = e.stderr
        
    @api.get("/")
    def root(self) -> Dict:
        import os
        import pandas as pd
        current_file_location = os.path.abspath(__file__)
        cwd = os.getcwd()
    
        return {
            "result": self._msg, 
            "hostname": os.uname()[1], 
            "pd_version":pd.__version__, 
            "current_file_location":current_file_location,
            "cwd":cwd
        }

    @api.post("/ping")
    def ping(self,name:str) -> Dict:
        return {"result": f"pong {name}"}

app = MyModelDeployment.bind()
