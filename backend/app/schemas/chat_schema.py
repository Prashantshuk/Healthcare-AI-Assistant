from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class ChatSessionCreate(BaseModel):

    title: str = Field(
        min_length=2,
        max_length=100
    )


class ChatMessageCreate(BaseModel):

    message: str = Field(
        min_length=1
    )


class ChatMessageResponse(BaseModel):

    id: int

    sender: str

    message: str

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class ChatSessionResponse(BaseModel):

    id: int

    title: str

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )