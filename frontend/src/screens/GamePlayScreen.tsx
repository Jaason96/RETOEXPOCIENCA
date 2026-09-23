import { useGameSession, useModeratorActions } from '../context/GameSessionContext'
import { useEventConfig } from '../context/EventConfigContext'
import { useKeyboardBuzzers } from '../hooks/useKeyboardBuzzers'
import { useBuzzCountdown } from '../hooks/useBuzzCountdown'
import {
  getDisplayPlayers,
  getDisplayQuestion,
  isLastQuestion,
} from '../utils/gameUtils'
import { DEFAULT_PLAYER_KEY_CODES, DEFAULT_RESPONSE_TIME_SECONDS } from '../constants/gameConstants'
import { EVENT_NAME, INSTITUTION_NAME } from '../constants/eventIdentity'
import { formatKeyCodeLabel } from '../utils/keyboardKeyLabels'
import type { AnswerLetter } from '../types/game'
import ModeratorPanelLayout from '../components/moderator/ModeratorPanelLayout'
import ModeratorStatusBar from '../components/moderator/ModeratorStatusBar'
import ModeratorPlayerBoard from '../components/moderator/ModeratorPlayerBoard'
import ModeratorQuestionPanel from '../components/moderator/ModeratorQuestionPanel'
import ModeratorActionBar from '../components/moderator/ModeratorActionBar'
import IncorrectAnswerOverlay from '../components/IncorrectAnswerOverlay'
import CorrectAnswerScreen from './CorrectAnswerScreen'
import PodiumScreen from './PodiumScreen'

export default function GamePlayScreen() {
  const { game, lastIncorrectResult, clearIncorrectResult } = useGameSession()
  const { config } = useEventConfig()
  const { resetBuzzers, submitAnswer, nextQuestion, finishGame } = useModeratorActions()

  useKeyboardBuzzers({ game, enabled: true })
  const remainingSeconds = useBuzzCountdown(game?.buzz_deadline ?? null)

  if (!game) {
    return null
  }

  if (game.status === 'FINISHED') {
    return <PodiumScreen showNewGameButton />
  }

  const responseTimeLimitSeconds = config?.response_time_seconds ?? DEFAULT_RESPONSE_TIME_SECONDS
  const playerKeyLabels: Record<number, string> = {
    1: formatKeyCodeLabel(config?.player_1_key ?? DEFAULT_PLAYER_KEY_CODES[1]),
    2: formatKeyCodeLabel(config?.player_2_key ?? DEFAULT_PLAYER_KEY_CODES[2]),
    3: formatKeyCodeLabel(config?.player_3_key ?? DEFAULT_PLAYER_KEY_CODES[3]),
    4: formatKeyCodeLabel(config?.player_4_key ?? DEFAULT_PLAYER_KEY_CODES[4]),
  }
  const displayPlayers = getDisplayPlayers(game)
  const displayQuestion = getDisplayQuestion(game)
  const lastQuestion = isLastQuestion(game)
  const isAnswerResult = game.status === 'ANSWER_RESULT'
  const canSubmitAnswer = game.status === 'BUZZ_LOCKED' && game.buzz_player !== null
  const showResetBuzzers = game.status === 'BUZZ_LOCKED'
  const hasFailedPlayers = game.failed_player_ids.length > 0
  const buzzPlayerName = game.buzz_player?.name ?? null

  const handleAnswerClick = (letter: AnswerLetter) => {
    if (!canSubmitAnswer) {
      return
    }
    submitAnswer(letter)
  }

  return (
    <>
      <ModeratorPanelLayout
        statusBar={
          <ModeratorStatusBar
            eventName={EVENT_NAME}
            institution={INSTITUTION_NAME}
            currentQuestionIndex={game.current_question_index}
            totalQuestions={game.total_questions}
            status={game.status}
          />
        }
        playerBoard={
          <ModeratorPlayerBoard
            players={displayPlayers}
            buzzPlayer={game.buzz_player}
            failedPlayerIds={game.failed_player_ids}
            status={game.status}
            playerKeyLabels={playerKeyLabels}
          />
        }
        actionBar={
          <ModeratorActionBar
            status={game.status}
            showResetBuzzers={showResetBuzzers}
            showNextQuestion={isAnswerResult && !lastQuestion}
            showFinishGame={isAnswerResult && lastQuestion}
            onResetBuzzers={resetBuzzers}
            onNextQuestion={nextQuestion}
            onFinishGame={finishGame}
          />
        }
      >
        {isAnswerResult ? (
          <CorrectAnswerScreen
            onNextQuestion={nextQuestion}
            onFinishGame={finishGame}
            isLastQuestion={lastQuestion}
            hideNavigationButton
          />
        ) : displayQuestion ? (
          <ModeratorQuestionPanel
            question={displayQuestion}
            status={game.status}
            canSubmitAnswer={canSubmitAnswer}
            buzzPlayerName={buzzPlayerName}
            hasFailedPlayers={hasFailedPlayers}
            remainingSeconds={remainingSeconds}
            responseTimeLimitSeconds={responseTimeLimitSeconds}
            onAnswerClick={handleAnswerClick}
          />
        ) : null}
      </ModeratorPanelLayout>

      {lastIncorrectResult && (
        <IncorrectAnswerOverlay
          playerName={lastIncorrectResult.player_name}
          reason={lastIncorrectResult.reason ?? 'INCORRECT'}
          onDismiss={clearIncorrectResult}
        />
      )}
    </>
  )
}
