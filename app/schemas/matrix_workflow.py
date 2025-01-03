import uuid

from datetime import datetime
from typing import Union, Optional
from pydantic import BaseModel, ConfigDict

# class MatrixFlowNodeData(BaseModel):
#     label: str

# class MatrixFlowNode(BaseModel):
#     id: str
#     data: MatrixFlowNodeData
#     type: str

class MatrixWorkflowEdge(BaseModel):
    id: str
    source: str
    target: str

class MatrixWorkflowViewport(BaseModel):
    x: float
    y: float
    zoom: float

class MatrixWorkflowGraph(BaseModel):
    nodes: list[dict] = []
    edges: list[MatrixWorkflowEdge] = []
    viewport: MatrixWorkflowViewport

class CreateMatrixWorkflowPayload(BaseModel):
    name: str
    description: Union[str, None] = None
    graph: MatrixWorkflowGraph

class GetMatrixWorkflowResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: Union[str, None] = None
    graph: MatrixWorkflowGraph
    created_at: datetime
    updated_at: datetime

class GetMatrixWorkflowListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: Union[str, None] = None
    created_at: datetime
    updated_at: datetime


class MatrixWorkflow(BaseModel):
    id: uuid.UUID
    nodes: list[dict] = []
    edges: list[MatrixWorkflowEdge] = []
    viewport: MatrixWorkflowViewport
    created_at: datetime
    updated_at: datetime

class UpdateMatrixWorkflowPayload(BaseModel):
    graph: Optional[MatrixWorkflowGraph] = None
    name: Optional[str] = None
    description: Optional[str] = None
