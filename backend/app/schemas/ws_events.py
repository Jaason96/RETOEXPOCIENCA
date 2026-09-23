from typing import Any

from pydantic import BaseModel

from app.schemas.game import AnswerResultResponse, GameDetailResponse


class WebSocketEvent(BaseModel):
    type: str
    payload: dict[str, Any]


class GameStateEvent(BaseModel):
    type: str = "game_state"
    payload: GameDetailResponse


class BuzzRegisteredEvent(BaseModel):
    type: str = "buzz_registered"
    payload: dict[str, int | str]


class AnswerResultEvent(BaseModel):
    type: str = "answer_result"
    payload: AnswerResultResponse


class QuestionChangedEvent(BaseModel):
    type: str = "question_changed"
    payload: dict[str, int]


class GameFinishedEvent(BaseModel):
    type: str = "game_finished"
    payload: dict[str, int]
