from typing import Literal

from pydantic import BaseModel, Field, field_validator

from app.models.game_status import GameStatus
from app.schemas.question import QuestionPublicResponse, QuestionResponse

AnswerFailureReason = Literal["INCORRECT", "TIMEOUT"]


class CreatePlayerRequest(BaseModel):
    number: int = Field(ge=1, le=99)
    name: str = Field(min_length=1, max_length=20)

    @field_validator("name")
    @classmethod
    def strip_name(cls, name: str) -> str:
        return name.strip()


class CreateGameRequest(BaseModel):
    question_set_id: int = Field(ge=1)
    players: list[CreatePlayerRequest] = Field(min_length=1, max_length=99)

    @field_validator("players")
    @classmethod
    def validate_unique_player_numbers(cls, players: list[CreatePlayerRequest]) -> list[CreatePlayerRequest]:
        numbers = [player.number for player in players]
        if len(numbers) != len(set(numbers)):
            raise ValueError("Los números de jugador no pueden repetirse")
        return players


class PlayerResponse(BaseModel):
    id: int
    player_number: int
    name: str
    color: str
    score: int
    active: bool


class BuzzPlayerResponse(BaseModel):
    id: int
    player_number: int
    name: str


class AnswerResultResponse(BaseModel):
    player_id: int
    player_name: str
    selected_answer: str
    is_correct: bool
    points_awarded: int
    correct_answer: str | None = None
    correct_answer_text: str | None = None
    explanation: str | None = None
    reason: AnswerFailureReason | None = None


class GameResponse(BaseModel):
    id: int
    created_at: str
    status: GameStatus
    current_question_index: int
    finished: bool
    total_questions: int
    players: list[PlayerResponse]
    current_question: QuestionPublicResponse | None = None
    buzz_player: BuzzPlayerResponse | None = None
    buzz_deadline: str | None = None
    failed_player_ids: list[int] = Field(default_factory=list)
    last_answer_result: AnswerResultResponse | None = None
    reveal_correct_answer: bool = False


class GameDetailResponse(GameResponse):
    current_question: QuestionResponse | None = None
