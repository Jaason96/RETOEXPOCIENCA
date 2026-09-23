import type { GameStatus } from '../types/game'

export type PlayerRoundStatus = 'waiting' | 'buzzed' | 'failed'

const STATUS_LABELS: Record<GameStatus, string> = {
  LOBBY: 'Lobby',
  QUESTION: 'Pregunta',
  BUZZ_OPEN: 'Pulsadores activos',
  BUZZ_LOCKED: 'Esperando respuesta',
  ANSWER_RESULT: 'Resultado',
  SCOREBOARD: 'Marcador',
  FINISHED: 'Finalizada',
}

export function getGameStatusLabel(status: GameStatus): string {
  return STATUS_LABELS[status] ?? status
}

export function getPlayerRoundStatus(
  playerId: number,
  buzzPlayerId: number | null | undefined,
  failedPlayerIds: number[],
): PlayerRoundStatus | null {
  if (buzzPlayerId === playerId) {
    return 'buzzed'
  }
  if (failedPlayerIds.includes(playerId)) {
    return 'failed'
  }
  return null
}

export function getPlayerRoundStatusLabel(status: PlayerRoundStatus | null): string {
  switch (status) {
    case 'buzzed':
      return 'Pulsó primero'
    case 'failed':
      return 'Falló en esta ronda'
    default:
      return 'En juego'
  }
}
