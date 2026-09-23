import type { GamePlayer, DisplayPlayer, Question, DisplayQuestion, GameDetail } from '../types/game'
import { ANSWER_COLORS } from '../constants/gameConstants'

export function getAvatarInitial(name: string): string {
  const trimmedName = name.trim()
  return trimmedName ? trimmedName.charAt(0).toUpperCase() : '?'
}

export function mapPlayersForDisplay(players: GamePlayer[]): DisplayPlayer[] {
  return players.map((player) => ({
    id: player.id,
    name: player.name,
    color: player.color,
    score: player.score,
    avatarInitial: getAvatarInitial(player.name),
    playerNumber: player.player_number,
  }))
}

export function sortPlayersByScore(players: DisplayPlayer[]): DisplayPlayer[] {
  return [...players].sort((left, right) => {
    if (right.score !== left.score) {
      return right.score - left.score
    }
    return left.playerNumber - right.playerNumber
  })
}

export function mapQuestionForDisplay(
  question: Question | null,
  currentIndex: number,
  totalQuestions: number,
): DisplayQuestion | null {
  if (!question) {
    return null
  }

  const correctOption = question.options.find(
    (option) => option.letter === question.correct_answer,
  )

  return {
    number: currentIndex,
    total: totalQuestions,
    text: question.text,
    answers: question.options.map((option) => ({
      letter: option.letter,
      text: option.text,
      color: ANSWER_COLORS[option.letter],
    })),
    correctLetter: question.correct_answer,
    correctText: correctOption?.text ?? '',
    explanation: question.explanation,
  }
}

export function getDisplayQuestion(game: GameDetail) {
  return mapQuestionForDisplay(
    game.current_question,
    game.current_question_index,
    game.total_questions,
  )
}

export function getDisplayPlayers(game: GameDetail) {
  return mapPlayersForDisplay(game.players)
}

export function isLastQuestion(game: GameDetail) {
  return game.current_question_index >= game.total_questions
}
