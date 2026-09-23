from pydantic import BaseModel, Field, field_validator


class QuestionSetItemResponse(BaseModel):
    id: int
    question_id: int
    question_order: int
    text: str
    active: bool


class QuestionSetSummary(BaseModel):
    id: int
    name: str
    description: str
    active: bool
    created_at: str
    question_count: int
    active_question_count: int


class QuestionSetDetailResponse(QuestionSetSummary):
    items: list[QuestionSetItemResponse]


class CreateQuestionSetRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(default="", max_length=300)
    question_ids: list[int] = Field(min_length=1)

    @field_validator("name", "description")
    @classmethod
    def strip_text(cls, value: str) -> str:
        return value.strip()

    @field_validator("question_ids")
    @classmethod
    def validate_unique_questions(cls, question_ids: list[int]) -> list[int]:
        if len(question_ids) != len(set(question_ids)):
            raise ValueError("No se puede repetir la misma pregunta dentro de la lista")
        return question_ids


class UpdateQuestionSetRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=300)
    question_ids: list[int] | None = Field(default=None, min_length=1)

    @field_validator("name", "description")
    @classmethod
    def strip_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip()

    @field_validator("question_ids")
    @classmethod
    def validate_unique_questions(
        cls,
        question_ids: list[int] | None,
    ) -> list[int] | None:
        if question_ids is None:
            return None
        if len(question_ids) != len(set(question_ids)):
            raise ValueError("No se puede repetir la misma pregunta dentro de la lista")
        return question_ids


class QuestionSetMoveRequest(BaseModel):
    question_id: int
    direction: str

    @field_validator("direction")
    @classmethod
    def validate_direction(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized not in {"up", "down"}:
            raise ValueError("La dirección debe ser up o down")
        return normalized
