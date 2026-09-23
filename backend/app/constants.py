MIN_PLAYERS = 2
MAX_PLAYERS = 4

DEFAULT_CORRECT_ANSWER_POINTS = 1000

# Valor sembrado en configuracion_evento.tiempo_respuesta_segundos para partidas
# nuevas. El valor real en tiempo de ejecución lo decide la configuración del
# evento (event_config_service), no esta constante.
DEFAULT_BUZZ_RESPONSE_TIME_SECONDS = 7

# Teclas (event.code del navegador) sembradas para cada jugador. El valor real
# en tiempo de ejecución lo decide la configuración del evento, no esta
# constante — igual que DEFAULT_BUZZ_RESPONSE_TIME_SECONDS.
DEFAULT_PLAYER_KEY_CODES = {
    1: "KeyA",
    2: "KeyF",
    3: "KeyJ",
    4: "KeyL",
}
