import { useGameSession } from '../context/GameSessionContext'
import { getDisplayQuestion } from '../utils/gameUtils'
import MascotPlaceholder from '../components/MascotPlaceholder'
import './CorrectAnswerScreen.css'

interface CorrectAnswerScreenProps {
  onNextQuestion: () => void
  onFinishGame: () => void
  isLastQuestion: boolean
  hideNavigationButton?: boolean
}

export default function CorrectAnswerScreen({
  onNextQuestion,
  onFinishGame,
  isLastQuestion,
  hideNavigationButton = false,
}: CorrectAnswerScreenProps) {
  const { game } = useGameSession()

  if (!game || !game.last_answer_result) {
    return null
  }

  const answerResult = game.last_answer_result
  const displayQuestion = getDisplayQuestion(game)
  const correctText =
    answerResult.correct_answer_text ??
    displayQuestion?.correctText ??
    'Respuesta correcta'
  const allFailed = !answerResult.is_correct && !answerResult.player_name

  return (
    <div
      className={[
        'correct-screen',
        hideNavigationButton ? 'correct-screen--embedded' : '',
      ]
        .filter(Boolean)
        .join(' ')}
    >
      <div className="correct-screen__celebration">
        <div className="correct-screen__check">
          {answerResult.is_correct ? '✓' : allFailed ? '✦' : '✗'}
        </div>
        <h1 className="correct-screen__title">
          {answerResult.is_correct
            ? `✅ ¡CORRECTO, ${answerResult.player_name.toUpperCase()}!`
            : allFailed
              ? 'Nadie acertó esta vez'
              : '❌ RESPUESTA INCORRECTA'}
        </h1>
        {answerResult.is_correct && (
          <p className="correct-screen__points">
            +{answerResult.points_awarded.toLocaleString('es-CO')} puntos
          </p>
        )}
        {(answerResult.is_correct || allFailed) && (
          <>
            <p className="correct-screen__answer">{correctText}</p>
            {!answerResult.is_correct && allFailed && (
              <p className="correct-screen__points">Nadie sumó puntos en esta pregunta</p>
            )}
          </>
        )}
      </div>

      <div className="correct-screen__mascot">
        <MascotPlaceholder size="medium" variant="esperancita" />
      </div>

      {(answerResult.is_correct || allFailed) && (
        <section className="correct-screen__fact">
          <h2 className="correct-screen__fact-title">¿Sabías que...?</h2>
          <p className="correct-screen__fact-text">
            {answerResult.explanation ?? displayQuestion?.explanation}
          </p>
        </section>
      )}

      {!hideNavigationButton && (
        <button
          type="button"
          className="correct-screen__next-btn"
          onClick={isLastQuestion ? onFinishGame : onNextQuestion}
        >
          {isLastQuestion ? 'VER RESULTADOS' : 'SIGUIENTE PREGUNTA'}
        </button>
      )}
    </div>
  )
}
