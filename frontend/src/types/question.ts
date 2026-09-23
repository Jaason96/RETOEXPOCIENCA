import type { AnswerLetter } from './game'

export interface QuestionFormData {
  text: string
  option_a: string
  option_b: string
  option_c: string
  option_d: string
  correct_answer: AnswerLetter
  explanation: string
  active: boolean
}

export interface QuestionBankSummary {
  active_count: number
  total_count: number
}

export interface QuestionBank {
  summary: QuestionBankSummary
  questions: import('./game').Question[]
}

export interface QuestionPreviewData {
  text: string
  options: { letter: AnswerLetter; text: string; color: string }[]
}
