from graph import Graph
from fastapi import FastAPI

app = FastAPI()
graph = Graph()

@app.get("/update/{network}/{address_a}")    
def get_update_user(address_a, network):
    return graph.query_update_user(address_a, network)