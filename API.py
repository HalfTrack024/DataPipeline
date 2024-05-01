from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from modules import opcua_mod as opcua

class OPCUA_SUB(BaseModel):
    endpoint: str | None = None
    nodes: list | None = None


app = FastAPI()



@app.post("/opcua/create-client/")
async def create_opcua_client(opc: OPCUA_SUB):
    endpoint_url = opc.endpoint
    await opcua.opcua_client_setup(endpoint_url)
    return {"message": "Started or updated monitoring nodes"}

@app.post("/opcua/add-subscriber/")
async def add_subscribers(opc: OPCUA_SUB):
    node_ids = opc.nodes
    await opcua.opcua_add_subscribers(node_ids)
    return {"message": "Added Nodes"}

@app.post("/opcua/remove-subscriber/")
async def remove_subscribers(opc: OPCUA_SUB):
    node_ids = opc.nodes
    await opcua.opcua_remove_subscribers(node_ids)
    return {"message": "Removed Nodes "}

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
