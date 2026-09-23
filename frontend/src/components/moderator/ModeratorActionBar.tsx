import type { GameStatus } from '../../types/game'
import './ModeratorActionBar.css'

interface ModeratorActionBarProps {
  status: GameStatus
  showResetBuzzers: boolean
  showNextQuestion: boolean
  showFinishGame: boolean
  onResetBuzzers: () => void
  onNextQuestion: () => void
  onFinishGame: () => void
}

export default function ModeratorActionBar({
  status,
  showResetBuzzers,
  showNextQuestion,
  showFinishGame,
  onResetBuzzers,
  onNextQuestion,
  onFinishGame,
}: ModeratorActionBarProps) {
  const hasActions = showResetBuzzers || showNextQuestion || showFinishGame

  return (
    <footer className="moderator-action-bar">
      <div className="moderator-action-bar__hint">
        {status === 'BUZZ_OPEN' && 'Esperando pulsación de jugadores'}
        {status === 'BUZZ_LOCKED' && 'Evalúa la respuesta del jugador activo'}
        {status === 'ANSWER_RESULT' && 'Avanza cuando el grupo esté listo'}
      </div>

      <div className="moderator-action-bar__actions">
        {showResetBuzzers && (
          <button type="button" className="moderator-action-bar__btn" onClick={onResetBuzzers}>
            REINICIAR PULSADORES
          </button>
        )}

        {showNextQuestion && (
          <button
            type="button"
            className="moderator-action-bar__btn moderator-action-bar__btn--primary"
            onClick={onNextQuestion}
          >
            SIGUIENTE PREGUNTA
          </button>
        )}

        {showFinishGame && (
          <button
            type="button"
            className="moderator-action-bar__btn moderator-action-bar__btn--primary"
            onClick={onFinishGame}
          >
            VER RESULTADOS
          </button>
        )}

        {!hasActions && (
          <span className="moderator-action-bar__placeholder">Sin acciones disponibles</span>
        )}
      </div>
    </footer>
  )
}
