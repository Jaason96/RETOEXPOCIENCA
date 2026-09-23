from fastapi import APIRouter, HTTPException

from app.schemas.game import CreateGameRequest, GameDetailResponse
from app.services.game_service import (
    GameNotFoundError,
    InvalidGameRequestError,
    create_game,
    fetch_game,
)

router = APIRouter(prefix="/games", tags=["games"])


@router.post("", response_model=GameDetailResponse, status_code=201)
def create_new_game(request: CreateGameRequest) -> GameDetailResponse:
    try:
        return create_game(request)
    except InvalidGameRequestError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.get("/{game_id}", response_model=GameDetailResponse)
def get_game(game_id: int) -> GameDetailResponse:
    try:
        return fetch_game(game_id)
    except GameNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
