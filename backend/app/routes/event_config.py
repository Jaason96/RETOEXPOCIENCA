from fastapi import APIRouter, HTTPException

from app.database import get_connection
from app.schemas.event_config import EventConfigResponse, UpdateEventConfigRequest
from app.services import event_config_service

router = APIRouter(prefix="/event-config", tags=["event-config"])


@router.get("", response_model=EventConfigResponse)
def get_event_config() -> EventConfigResponse:
    with get_connection() as connection:
        try:
            return event_config_service.get_event_config(connection)
        except event_config_service.EventConfigNotFoundError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error


@router.put("", response_model=EventConfigResponse)
def update_event_config(request: UpdateEventConfigRequest) -> EventConfigResponse:
    with get_connection() as connection:
        try:
            return event_config_service.update_event_config(connection, request)
        except event_config_service.EventConfigNotFoundError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error
