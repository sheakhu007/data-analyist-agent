from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass

from .enums import ErrorCategory, ExecutionStatus

@dataclass
class ToolResult:
    tool: str
    status: str
    result: dict | None = None
    message: str | None = None


@dataclass
class Plan:
    goal: str
    steps: list[str]
    current_step: int = 0


@dataclass(kw_only=True)
class MemoryItem:
    content: str
    importance: float = Field(ge=0.0, le=1.0)
    category: str
    timestamp: str


class RepairDecision(BaseModel):
    """
    Represents the outcome of execution analysis performed by the
    Reflection/RepairService.

    This model acts as the contract between Reflection and the LangGraph
    routing logic.
    """

    status: ExecutionStatus = Field(
        ...,
        description="Overall execution status."
    )

    requires_repair: bool = Field(
        default=False,
        description="Whether the execution should be repaired."
    )

    retry_allowed: bool = Field(
        default=False,
        description="Whether another repair attempt is permitted."
    )

    error_category: ErrorCategory = Field(
        default=ErrorCategory.UNKNOWN,
        description="Normalized category of the execution failure."
    )

    failure_reason: Optional[str] = Field(
        default=None,
        description="Human-readable explanation of the failure."
    )

    repair_instruction: str = Field(
        default="",
        description="Guidance for the compatibility repair workflow."
    )

    failed_tool: Optional[str] = Field(
        default=None,
        description="Name of the tool that failed."
    )

    retry_count: int = Field(
        default=0,
        ge=0,
        description="Current repair attempt count."
    )

    class Config:
        frozen = True


class RepairRecord(BaseModel):

    attempt: int

    failure_reason: str

    previous_plan: Plan

    repaired_plan: Plan

    timestamp: datetime
