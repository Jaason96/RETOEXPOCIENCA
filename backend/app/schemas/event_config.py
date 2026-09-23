from pydantic import BaseModel, Field, field_validator


class EventConfigResponse(BaseModel):
    correct_answer_points: int
    response_time_seconds: int
    player_1_key: str
    player_2_key: str
    player_3_key: str
    player_4_key: str


class UpdateEventConfigRequest(BaseModel):
    correct_answer_points: int = Field(ge=1, le=100000)
    response_time_seconds: int = Field(ge=1, le=120)
    player_1_key: str = Field(min_length=1, max_length=40)
    player_2_key: str = Field(min_length=1, max_length=40)
    player_3_key: str = Field(min_length=1, max_length=40)
    player_4_key: str = Field(min_length=1, max_length=40)

    @field_validator("player_4_key")
    @classmethod
    def validate_unique_player_keys(cls, player_4_key: str, info) -> str:
        keys = [
            info.data.get("player_1_key"),
            info.data.get("player_2_key"),
            info.data.get("player_3_key"),
            player_4_key,
        ]
        if len(set(keys)) != len(keys):
            raise ValueError("No se puede asignar la misma tecla a más de un jugador")
        return player_4_key
