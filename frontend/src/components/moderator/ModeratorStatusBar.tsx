import type { GameStatus } from '../../types/game'
import { getGameStatusLabel } from '../../utils/moderatorUtils'
import './ModeratorStatusBar.css'

interface ModeratorStatusBarProps {
  eventName: string
  institution: string
  currentQuestionIndex: number
  totalQuestions: number
  status: GameStatus
}

export default function ModeratorStatusBar({
  eventName,
  institution,
  currentQuestionIndex,
  totalQuestions,
  status,
}: ModeratorStatusBarProps) {
  const progress = totalQuestions > 0 ? (currentQuestionIndex / totalQuestions) * 100 : 0
  const statusLabel = getGameStatusLabel(status)
  const isBuzzOpen = status === 'BUZZ_OPEN'
  const isBuzzLocked = status === 'BUZZ_LOCKED'
  const isAnswerResult = status === 'ANSWER_RESULT'

  return (
    <header className="moderator-status-bar">
      <div className="moderator-status-bar__brand">
        <p className="moderator-status-bar__event">{eventName}</p>
        <p className="moderator-status-bar__institution">{institution}</p>
      </div>

      <div className="moderator-status-bar__progress-block">
        <p className="moderator-status-bar__question-count">
          Pregunta {currentQuestionIndex} de {totalQuestions}
        </p>
        <div className="moderator-status-bar__progress-track">
          <div
            className="moderator-status-bar__progress-fill"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      <div
        className={[
          'moderator-status-bar__status',
          isBuzzOpen ? 'moderator-status-bar__status--open' : '',
          isBuzzLocked ? 'moderator-status-bar__status--locked' : '',
          isAnswerResult ? 'moderator-status-bar__status--result' : '',
        ]
          .filter(Boolean)
          .join(' ')}
      >
        <span className="moderator-status-bar__status-dot" />
        <span>{statusLabel}</span>
      </div>
    </header>
  )
}
