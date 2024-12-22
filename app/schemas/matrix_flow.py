import uuid
from typing import Union
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

class MatrixFlowEdge(BaseModel):
    id: str
    source: str
    target: str

class MatrixFlowViewport(BaseModel):
    x: int
    y: int
    zoom: int

class CreateMatrixFlowPayload(BaseModel):
    nodes: list[dict] = []
    edges: list[MatrixFlowEdge] = []
    viewport: MatrixFlowViewport

class MatrixFlow(BaseModel):
    id: uuid.UUID
    nodes: list[dict] = []
    edges: list[MatrixFlowEdge] = []
    viewport: MatrixFlowViewport
