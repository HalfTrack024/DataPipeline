from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from modules import opcua_mod as opcua
from modules import ads_mod as ads


class OPCUA_SUB(BaseModel):
    endpoint: str | None = None
    nodes: list | None = None


class ADS_SUB(BaseModel):
    endpoint: str | None = None
    tag_name: str | None = None
    plc_datatype: str | None = None


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


@app.post("/ads/subscribe/")
async def ads_subscribe(ads_sub: ADS_SUB):
    try:
        handle = await ads.add_subscriber(ads_sub.tag_name, ads_sub.plc_datatype)
        return {"message": "Subscription Added: ", "handle": handle}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ads/unsubscribe/")
async def ads_subscribe(ads_sub: ADS_SUB):
    try:
        handle = await ads.remove_subscriber(ads_sub.tag_name, ads_sub.plc_datatype)
        return {"message": "Subscription Removed: ", "handle": handle}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
