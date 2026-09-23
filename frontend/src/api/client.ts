import type { CreatePlayerInput, GameDetail, Question } from '../types/game'
import type { QuestionBank, QuestionFormData } from '../types/question'
import type {
  QuestionSetDetail,
  QuestionSetFormData,
  QuestionSetSummary,
} from '../types/questionSet'
import type { EventConfig } from '../types/eventConfig'

const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

class ApiError extends Error {
  status: number

  constructor(message: string, status: number) {
    super(message)
    this.status = status
  }
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  })

  if (!response.ok) {
    let errorMessage = `Error ${response.status}`

    try {
      const errorBody = await response.json()
      if (typeof errorBody.detail === 'string') {
        errorMessage = errorBody.detail
      } else if (Array.isArray(errorBody.detail)) {
        errorMessage = errorBody.detail.map((item: { msg?: string }) => item.msg).join(', ')
      }
    } catch {
      errorMessage = response.statusText || errorMessage
    }

    throw new ApiError(errorMessage, response.status)
  }

  if (response.status === 204) {
    return undefined as T
  }

  return response.json() as Promise<T>
}

export async function checkHealth(): Promise<{ status: string; application: string }> {
  return request('/api/health')
}

export async function fetchQuestions(): Promise<Question[]> {
  return request('/api/questions')
}

export async function fetchQuestionBank(): Promise<QuestionBank> {
  return request('/api/questions/bank')
}

export async function fetchQuestion(questionId: number): Promise<Question> {
  return request(`/api/questions/${questionId}`)
}

export async function createQuestion(payload: QuestionFormData): Promise<Question> {
  return request('/api/questions', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export async function updateQuestion(
  questionId: number,
  payload: Partial<QuestionFormData>,
): Promise<Question> {
  return request(`/api/questions/${questionId}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

export async function deleteQuestion(questionId: number): Promise<void> {
  return request(`/api/questions/${questionId}`, {
    method: 'DELETE',
  })
}

export async function duplicateQuestion(questionId: number): Promise<Question> {
  return request(`/api/questions/${questionId}/duplicate`, {
    method: 'POST',
  })
}

export async function setQuestionActive(
  questionId: number,
  active: boolean,
): Promise<Question> {
  return request(`/api/questions/${questionId}/active`, {
    method: 'PATCH',
    body: JSON.stringify({ active }),
  })
}

export async function moveQuestion(
  questionId: number,
  direction: 'up' | 'down',
): Promise<Question> {
  return request(`/api/questions/${questionId}/move`, {
    method: 'POST',
    body: JSON.stringify({ direction }),
  })
}

export async function fetchEventConfig(): Promise<EventConfig> {
  return request('/api/event-config')
}

export async function updateEventConfig(payload: EventConfig): Promise<EventConfig> {
  return request('/api/event-config', {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

export async function fetchQuestionSets(): Promise<QuestionSetSummary[]> {
  return request('/api/question-sets')
}

export async function fetchQuestionSet(questionSetId: number): Promise<QuestionSetDetail> {
  return request(`/api/question-sets/${questionSetId}`)
}

export async function createQuestionSet(payload: QuestionSetFormData): Promise<QuestionSetDetail> {
  return request('/api/question-sets', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export async function updateQuestionSet(
  questionSetId: number,
  payload: Partial<QuestionSetFormData>,
): Promise<QuestionSetDetail> {
  return request(`/api/question-sets/${questionSetId}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

export async function deleteQuestionSet(questionSetId: number): Promise<void> {
  return request(`/api/question-sets/${questionSetId}`, {
    method: 'DELETE',
  })
}

export async function duplicateQuestionSet(questionSetId: number): Promise<QuestionSetDetail> {
  return request(`/api/question-sets/${questionSetId}/duplicate`, {
    method: 'POST',
  })
}

export async function moveQuestionInSet(
  questionSetId: number,
  questionId: number,
  direction: 'up' | 'down',
): Promise<QuestionSetDetail> {
  return request(`/api/question-sets/${questionSetId}/move`, {
    method: 'POST',
    body: JSON.stringify({ question_id: questionId, direction }),
  })
}

export async function createGame(
  questionSetId: number,
  players: CreatePlayerInput[],
): Promise<GameDetail> {
  return request('/api/games', {
    method: 'POST',
    body: JSON.stringify({ question_set_id: questionSetId, players }),
  })
}

export async function fetchGame(gameId: number): Promise<GameDetail> {
  return request(`/api/games/${gameId}`)
}

export { ApiError }
