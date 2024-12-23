from typing_extensions import Optional
import uuid

from datetime import datetime
from typing import Union, Optional
from pydantic import BaseModel, ConfigDict

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

class MatrixFlowResponseGraph(BaseModel):
    nodes: list[dict] = []
    edges: list[MatrixFlowEdge] = []
    viewport: MatrixFlowViewport

class CreateMatrixFlowPayload(BaseModel):
    nodes: list[dict] = []
    edges: list[MatrixFlowEdge] = []
    viewport: MatrixFlowViewport

class GetMatrixFlowResponse(BaseModel):
    id: uuid.UUID
    graph: MatrixFlowResponseGraph
    created_at: datetime
    updated_at: datetime

class GetMatrixFlowListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class MatrixFlow(BaseModel):
    id: uuid.UUID
    nodes: list[dict] = []
    edges: list[MatrixFlowEdge] = []
    viewport: MatrixFlowViewport
    created_at: datetime
    updated_at: datetime

class UpdateMatrixFlowPayload(BaseModel):
    graph: Optional[MatrixFlowResponseGraph] = None
