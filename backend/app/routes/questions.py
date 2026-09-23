from fastapi import APIRouter, HTTPException

from app.database import get_connection
from app.schemas.question import (
    CreateQuestionRequest,
    QuestionActiveRequest,
    QuestionBankResponse,
    QuestionMoveRequest,
    QuestionResponse,
    UpdateQuestionRequest,
)
from app.services import question_service

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("", response_model=list[QuestionResponse])
def list_active_questions() -> list[QuestionResponse]:
    with get_connection() as connection:
        return question_service.get_active_questions(connection)


@router.get("/bank", response_model=QuestionBankResponse)
def get_question_bank() -> QuestionBankResponse:
    with get_connection() as connection:
        return question_service.get_question_bank(connection)


@router.get("/{question_id}", response_model=QuestionResponse)
def get_question(question_id: int) -> QuestionResponse:
    try:
        with get_connection() as connection:
            return question_service.get_question_by_id(connection, question_id)
    except question_service.QuestionNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.post("", response_model=QuestionResponse, status_code=201)
def create_question(request: CreateQuestionRequest) -> QuestionResponse:
    with get_connection() as connection:
        return question_service.create_question(connection, request)


@router.put("/{question_id}", response_model=QuestionResponse)
def update_question(
    question_id: int,
    request: UpdateQuestionRequest,
) -> QuestionResponse:
    try:
        with get_connection() as connection:
            return question_service.update_question(connection, question_id, request)
    except question_service.QuestionNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.delete("/{question_id}", status_code=204)
def delete_question(question_id: int) -> None:
    try:
        with get_connection() as connection:
            question_service.delete_question(connection, question_id)
    except question_service.QuestionNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.post("/{question_id}/duplicate", response_model=QuestionResponse, status_code=201)
def duplicate_question(question_id: int) -> QuestionResponse:
    try:
        with get_connection() as connection:
            return question_service.duplicate_question(connection, question_id)
    except question_service.QuestionNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.patch("/{question_id}/active", response_model=QuestionResponse)
def set_question_active(
    question_id: int,
    request: QuestionActiveRequest,
) -> QuestionResponse:
    try:
        with get_connection() as connection:
            return question_service.set_question_active(
                connection,
                question_id,
                request.active,
            )
    except question_service.QuestionNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.post("/{question_id}/move", response_model=QuestionResponse)
def move_question(
    question_id: int,
    request: QuestionMoveRequest,
) -> QuestionResponse:
    try:
        with get_connection() as connection:
            return question_service.move_question(
                connection,
                question_id,
                request.direction,
            )
    except question_service.QuestionNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except question_service.InvalidQuestionError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
