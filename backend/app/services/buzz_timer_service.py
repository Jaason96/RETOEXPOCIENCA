import asyncio
import logging
from typing import Awaitable, Callable

logger = logging.getLogger(__name__)

BuzzTimeoutCallback = Callable[[int, int], Awaitable[None]]


class BuzzTimerService:
    """Tracks the server-side answer countdown for each in-progress game.

    One asyncio task runs per game_id, independent of any WebSocket
    connection, so the countdown survives a moderator reconnect and is not
    tied to how many clients are currently watching a given game.
    """

    def __init__(self) -> None:
        self._pending_timeouts: dict[int, asyncio.Task[None]] = {}

    def schedule_timeout(
        self,
        game_id: int,
        buzz_player_id: int,
        seconds: float,
        on_timeout: BuzzTimeoutCallback,
    ) -> None:
        self.cancel(game_id)
        self._pending_timeouts[game_id] = asyncio.create_task(
            self._wait_and_notify(game_id, buzz_player_id, seconds, on_timeout)
        )

    def cancel(self, game_id: int) -> None:
        pending_task = self._pending_timeouts.pop(game_id, None)
        if pending_task is not None:
            pending_task.cancel()

    async def _wait_and_notify(
        self,
        game_id: int,
        buzz_player_id: int,
        seconds: float,
        on_timeout: BuzzTimeoutCallback,
    ) -> None:
        await asyncio.sleep(seconds)
        self._pending_timeouts.pop(game_id, None)

        try:
            await on_timeout(game_id, buzz_player_id)
        except Exception:
            logger.exception(
                "Error al resolver el tiempo agotado de la partida %s", game_id
            )


buzz_timer_service = BuzzTimerService()
