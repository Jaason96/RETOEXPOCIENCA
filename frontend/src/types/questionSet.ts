export interface QuestionSetSummary {
  id: number
  name: string
  description: string
  active: boolean
  created_at: string
  question_count: number
  active_question_count: number
}

export interface QuestionSetItem {
  id: number
  question_id: number
  question_order: number
  text: string
  active: boolean
}

export interface QuestionSetDetail extends QuestionSetSummary {
  items: QuestionSetItem[]
}

export interface QuestionSetFormData {
  name: string
  description: string
  question_ids: number[]
}
