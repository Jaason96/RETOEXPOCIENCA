import type { AnswerLetter, DisplayQuestion, GameStatus } from '../../types/game'
import AnswerOption from '../AnswerOption'
import BuzzActiveBanner from '../BuzzActiveBanner'
import BuzzBanner from '../BuzzBanner'
import TimerCircle from '../TimerCircle'
import './ModeratorQuestionPanel.css'

interface ModeratorQuestionPanelProps {
  question: DisplayQuestion
  status: GameStatus
  canSubmitAnswer: boolean
  buzzPlayerName: string | null
  hasFailedPlayers: boolean
  remainingSeconds: number
  responseTimeLimitSeconds: number
  onAnswerClick: (letter: AnswerLetter) => void
}

export default function ModeratorQuestionPanel({
  question,
  status,
  canSubmitAnswer,
  buzzPlayerName,
  hasFailedPlayers,
  remainingSeconds,
  responseTimeLimitSeconds,
  onAnswerClick,
}: ModeratorQuestionPanelProps) {
  return (
    <section className="moderator-question-panel">
      <h2 className="moderator-question-panel__text">{question.text}</h2>

      <div className="moderator-question-panel__answers">
        {question.answers.map((answer) => (
          <AnswerOption
            key={answer.letter}
            letter={answer.letter}
            text={answer.text}
            color={answer.color}
            onClick={() => onAnswerClick(answer.letter)}
            disabled={!canSubmitAnswer}
            selectable={canSubmitAnswer}
          />
        ))}
      </div>

      {status === 'BUZZ_OPEN' && (
        <BuzzActiveBanner
          message={hasFailedPlayers ? '¡LOS DEMÁS PUEDEN PULSAR!' : 'PULSADORES ACTIVOS'}
        />
      )}

      {status === 'BUZZ_LOCKED' && buzzPlayerName && (
        <div className="moderator-question-panel__buzz-locked">
          <BuzzBanner playerName={buzzPlayerName} />
          <TimerCircle
            remainingSeconds={remainingSeconds}
            totalSeconds={responseTimeLimitSeconds}
          />
          <p className="moderator-question-panel__hint">
            Selecciona la respuesta indicada por {buzzPlayerName}
          </p>
        </div>
      )}
    </section>
  )
}
