import type { AnswerLetter } from '../types/game'

export const PLAYER_COUNTS = [2, 3, 4] as const

export const MAX_PLAYER_NAME_LENGTH = 20

// Valor de respaldo mientras se carga la configuración del evento, y solo
// para dimensionar el círculo de cuenta regresiva. El servidor decide
// cuándo termina el turno usando event_config.response_time_seconds.
export const DEFAULT_RESPONSE_TIME_SECONDS = 7

// Debe coincidir con DEFAULT_PLAYER_KEY_CODES en backend/app/constants.py —
// usado como valor local de "restaurar predeterminados" y como respaldo en
// useKeyboardBuzzers mientras la configuración del evento aún no carga.
export const DEFAULT_PLAYER_KEY_CODES: Record<number, string> = {
  1: 'KeyA',
  2: 'KeyF',
  3: 'KeyJ',
  4: 'KeyL',
}

export const PLAYER_COLORS: Record<number, { hex: string; emoji: string }> = {
  1: { hex: '#018EE0', emoji: '🔵' },
  2: { hex: '#009256', emoji: '🟢' },
  3: { hex: '#E6A817', emoji: '🟡' },
  4: { hex: '#D94F4F', emoji: '🔴' },
}

export const ANSWER_COLORS: Record<AnswerLetter, string> = {
  A: '#018EE0',
  B: '#009256',
  C: '#E6A817',
  D: '#D94F4F',
}
