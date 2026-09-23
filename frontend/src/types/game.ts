export type AnswerLetter = 'A' | 'B' | 'C' | 'D'

export type AnswerFailureReason = 'INCORRECT' | 'TIMEOUT'

export type GameStatus =
  | 'LOBBY'
  | 'QUESTION'
  | 'BUZZ_OPEN'
  | 'BUZZ_LOCKED'
  | 'ANSWER_RESULT'
  | 'SCOREBOARD'
  | 'FINISHED'

export interface QuestionOption {
  letter: AnswerLetter
  text: string
}

export interface Question {
  id: number
  text: string
  options: QuestionOption[]
  correct_answer: AnswerLetter
  explanation: string
  order: number
  active?: boolean
}

export interface GamePlayer {
  id: number
  player_number: number
  name: string
  color: string
  score: number
  active: boolean
}

export interface BuzzPlayer {
  id: number
  player_number: number
  name: string
}

export interface AnswerResult {
  player_id: number
  player_name: string
  selected_answer: AnswerLetter | ''
  is_correct: boolean
  points_awarded: number
  correct_answer?: AnswerLetter | null
  correct_answer_text?: string | null
  explanation?: string | null
  reason?: AnswerFailureReason | null
}

export interface GameDetail {
  id: number
  created_at: string
  status: GameStatus
  current_question_index: number
  finished: boolean
  total_questions: number
  players: GamePlayer[]
  current_question: Question | null
  buzz_player: BuzzPlayer | null
  buzz_deadline: string | null
  failed_player_ids: number[]
  last_answer_result: AnswerResult | null
  reveal_correct_answer: boolean
}

export interface CreatePlayerInput {
  number: number
  name: string
}

export interface DisplayPlayer {
  id: number
  name: string
  color: string
  score: number
  avatarInitial: string
  playerNumber: number
}

export interface DisplayQuestion {
  number: number
  total: number
  text: string
  answers: {
    letter: AnswerLetter
    text: string
    color: string
  }[]
  correctLetter: AnswerLetter
  correctText: string
  explanation: string
}

export type WebSocketAction =
  | { action: 'lock_buzzers' }
  | { action: 'reset_buzzers' }
  | { action: 'register_buzz'; player_number: number }
  | { action: 'submit_answer'; answer: AnswerLetter }
  | { action: 'next_question' }
  | { action: 'finish_game' }

export type WebSocketEventType =
  | 'game_state'
  | 'buzz_registered'
  | 'answer_result'
  | 'question_changed'
  | 'game_finished'
  | 'error'

export interface WebSocketMessage {
  type: WebSocketEventType
  payload: unknown
}
