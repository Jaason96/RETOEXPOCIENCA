from pydantic import BaseModel, Field, field_validator


class QuestionOptionResponse(BaseModel):
    letter: str
    text: str


class QuestionResponse(BaseModel):
    id: int
    text: str
    options: list[QuestionOptionResponse]
    correct_answer: str
    explanation: str
    order: int
    active: bool


class QuestionPublicResponse(BaseModel):
    id: int
    text: str
    options: list[QuestionOptionResponse]
    order: int


class QuestionBankSummary(BaseModel):
    active_count: int
    total_count: int


class QuestionBankResponse(BaseModel):
    summary: QuestionBankSummary
    questions: list[QuestionResponse]


class CreateQuestionRequest(BaseModel):
    text: str = Field(min_length=1, max_length=300)
    option_a: str = Field(min_length=1, max_length=200)
    option_b: str = Field(min_length=1, max_length=200)
    option_c: str = Field(min_length=1, max_length=200)
    option_d: str = Field(min_length=1, max_length=200)
    correct_answer: str
    explanation: str = Field(min_length=1, max_length=500)
    active: bool = True

    @field_validator("text", "option_a", "option_b", "option_c", "option_d", "explanation")
    @classmethod
    def strip_text(cls, value: str) -> str:
        return value.strip()

    @field_validator("correct_answer")
    @classmethod
    def validate_correct_answer(cls, value: str) -> str:
        normalized = value.strip().upper()
        if normalized not in {"A", "B", "C", "D"}:
            raise ValueError("La respuesta correcta debe ser A, B, C o D")
        return normalized


class UpdateQuestionRequest(BaseModel):
    text: str | None = Field(default=None, min_length=1, max_length=300)
    option_a: str | None = Field(default=None, min_length=1, max_length=200)
    option_b: str | None = Field(default=None, min_length=1, max_length=200)
    option_c: str | None = Field(default=None, min_length=1, max_length=200)
    option_d: str | None = Field(default=None, min_length=1, max_length=200)
    correct_answer: str | None = None
    explanation: str | None = Field(default=None, min_length=1, max_length=500)
    active: bool | None = None

    @field_validator("text", "option_a", "option_b", "option_c", "option_d", "explanation")
    @classmethod
    def strip_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip()

    @field_validator("correct_answer")
    @classmethod
    def validate_correct_answer(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip().upper()
        if normalized not in {"A", "B", "C", "D"}:
            raise ValueError("La respuesta correcta debe ser A, B, C o D")
        return normalized


class QuestionActiveRequest(BaseModel):
    active: bool


class QuestionMoveRequest(BaseModel):
    direction: str

    @field_validator("direction")
    @classmethod
    def validate_direction(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized not in {"up", "down"}:
            raise ValueError("La dirección debe ser up o down")
        return normalized
