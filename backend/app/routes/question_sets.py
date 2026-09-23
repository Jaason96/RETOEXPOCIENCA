from fastapi import APIRouter, HTTPException

from app.database import get_connection
from app.schemas.question_set import (
    CreateQuestionSetRequest,
    QuestionSetDetailResponse,
    QuestionSetMoveRequest,
    QuestionSetSummary,
    UpdateQuestionSetRequest,
)
from app.services import question_set_service

router = APIRouter(prefix="/question-sets", tags=["question-sets"])


@router.get("", response_model=list[QuestionSetSummary])
def list_question_sets() -> list[QuestionSetSummary]:
    with get_connection() as connection:
        return question_set_service.get_all_question_sets(connection)


@router.get("/{question_set_id}", response_model=QuestionSetDetailResponse)
def get_question_set(question_set_id: int) -> QuestionSetDetailResponse:
    try:
        with get_connection() as connection:
            return question_set_service.get_question_set_detail(connection, question_set_id)
    except question_set_service.QuestionSetNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.post("", response_model=QuestionSetDetailResponse, status_code=201)
def create_question_set(request: CreateQuestionSetRequest) -> QuestionSetDetailResponse:
    try:
        with get_connection() as connection:
            return question_set_service.create_question_set(connection, request)
    except question_set_service.InvalidQuestionSetError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.put("/{question_set_id}", response_model=QuestionSetDetailResponse)
def update_question_set(
    question_set_id: int,
    request: UpdateQuestionSetRequest,
) -> QuestionSetDetailResponse:
    try:
        with get_connection() as connection:
            return question_set_service.update_question_set(
                connection,
                question_set_id,
                request,
            )
    except question_set_service.QuestionSetNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except question_set_service.InvalidQuestionSetError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.delete("/{question_set_id}", status_code=204)
def delete_question_set(question_set_id: int) -> None:
    try:
        with get_connection() as connection:
            question_set_service.delete_question_set(connection, question_set_id)
    except question_set_service.QuestionSetNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.post("/{question_set_id}/duplicate", response_model=QuestionSetDetailResponse, status_code=201)
def duplicate_question_set(question_set_id: int) -> QuestionSetDetailResponse:
    try:
        with get_connection() as connection:
            return question_set_service.duplicate_question_set(connection, question_set_id)
    except question_set_service.QuestionSetNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.post("/{question_set_id}/move", response_model=QuestionSetDetailResponse)
def move_question_in_set(
    question_set_id: int,
    request: QuestionSetMoveRequest,
) -> QuestionSetDetailResponse:
    try:
        with get_connection() as connection:
            return question_set_service.move_question_in_set(
                connection,
                question_set_id,
                request.question_id,
                request.direction,
            )
    except question_set_service.QuestionSetNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except question_set_service.InvalidQuestionSetError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
