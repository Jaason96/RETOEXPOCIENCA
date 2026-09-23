import { useCallback, useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import type { Question } from '../types/game'
import type { QuestionPreviewData } from '../types/question'
import type { QuestionSetSummary } from '../types/questionSet'
import {
  ApiError,
  deleteQuestion,
  deleteQuestionSet,
  duplicateQuestion,
  duplicateQuestionSet,
  fetchQuestionBank,
  fetchQuestionSets,
  moveQuestion,
  setQuestionActive,
} from '../api/client'
import { ANSWER_COLORS } from '../constants/gameConstants'
import { INSTITUTION_NAME } from '../constants/eventIdentity'
import LogoPlaceholder from '../components/LogoPlaceholder'
import HomeButton from '../components/navigation/HomeButton'
import QuestionPreviewModal from '../components/QuestionPreviewModal'
import './QuestionsBankScreen.css'

function getCorrectAnswerLabel(question: Question): string {
  const correctOption = question.options.find(
    (option) => option.letter === question.correct_answer,
  )
  return `${question.correct_answer} — ${correctOption?.text ?? ''}`
}

export default function QuestionsBankScreen() {
  const navigate = useNavigate()
  const [questionSets, setQuestionSets] = useState<QuestionSetSummary[]>([])
  const [questions, setQuestions] = useState<Question[]>([])
  const [activeCount, setActiveCount] = useState(0)
  const [totalCount, setTotalCount] = useState(0)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [successMessage, setSuccessMessage] = useState<string | null>(null)
  const [previewData, setPreviewData] = useState<QuestionPreviewData | null>(null)

  const loadQuestions = useCallback(async () => {
    setIsLoading(true)
    setError(null)

    try {
      const [bank, sets] = await Promise.all([fetchQuestionBank(), fetchQuestionSets()])
      setQuestions(bank.questions)
      setActiveCount(bank.summary.active_count)
      setTotalCount(bank.summary.total_count)
      setQuestionSets(sets)
    } catch (caughtError) {
      const message =
        caughtError instanceof ApiError
          ? caughtError.message
          : 'No se pudo cargar el banco de preguntas.'
      setError(message)
    } finally {
      setIsLoading(false)
    }
  }, [])

  useEffect(() => {
    loadQuestions()
  }, [loadQuestions])

  useEffect(() => {
    if (!successMessage) {
      return
    }
    const timer = window.setTimeout(() => setSuccessMessage(null), 3200)
    return () => window.clearTimeout(timer)
  }, [successMessage])

  const handleDuplicate = async (questionId: number) => {
    try {
      await duplicateQuestion(questionId)
      setSuccessMessage('Pregunta duplicada correctamente.')
      await loadQuestions()
    } catch (caughtError) {
      setError(caughtError instanceof ApiError ? caughtError.message : 'No se pudo duplicar.')
    }
  }

  const handleToggleActive = async (question: Question) => {
    try {
      await setQuestionActive(question.id, !question.active)
      setSuccessMessage(
        question.active ? 'Pregunta desactivada.' : 'Pregunta activada.',
      )
      await loadQuestions()
    } catch (caughtError) {
      setError(caughtError instanceof ApiError ? caughtError.message : 'No se pudo cambiar el estado.')
    }
  }

  const handleMove = async (questionId: number, direction: 'up' | 'down') => {
    try {
      await moveQuestion(questionId, direction)
      await loadQuestions()
    } catch (caughtError) {
      setError(caughtError instanceof ApiError ? caughtError.message : 'No se pudo mover la pregunta.')
    }
  }

  const handleDelete = async (question: Question) => {
    const confirmed = window.confirm('¿Seguro que deseas eliminar esta pregunta?')
    if (!confirmed) {
      return
    }

    try {
      await deleteQuestion(question.id)
      setSuccessMessage('Pregunta eliminada correctamente.')
      await loadQuestions()
    } catch (caughtError) {
      setError(caughtError instanceof ApiError ? caughtError.message : 'No se pudo eliminar.')
    }
  }

  const handleDeleteSet = async (questionSet: QuestionSetSummary) => {
    const confirmed = window.confirm('¿Seguro que deseas eliminar esta lista de preguntas?')
    if (!confirmed) {
      return
    }

    try {
      await deleteQuestionSet(questionSet.id)
      setSuccessMessage('Lista eliminada correctamente.')
      await loadQuestions()
    } catch (caughtError) {
      setError(caughtError instanceof ApiError ? caughtError.message : 'No se pudo eliminar la lista.')
    }
  }

  const handleDuplicateSet = async (questionSetId: number) => {
    try {
      await duplicateQuestionSet(questionSetId)
      setSuccessMessage('Lista duplicada correctamente.')
      await loadQuestions()
    } catch (caughtError) {
      setError(caughtError instanceof ApiError ? caughtError.message : 'No se pudo duplicar la lista.')
    }
  }

  const handlePreview = (question: Question) => {
    setPreviewData({
      text: question.text,
      options: question.options.map((option) => ({
        letter: option.letter,
        text: option.text,
        color: ANSWER_COLORS[option.letter],
      })),
    })
  }

  return (
    <div className="questions-bank">
      <header className="questions-bank__header">
        <LogoPlaceholder size="small" />
        <div className="questions-bank__header-text">
          <h1 className="questions-bank__title">BANCO DE PREGUNTAS</h1>
          <p className="questions-bank__subtitle">
            {INSTITUTION_NAME}
          </p>
        </div>
        <HomeButton />
      </header>

      <section className="questions-bank__summary">
        <p className="questions-bank__count">
          {activeCount} preguntas activas de {totalCount} disponibles
        </p>
        <p className="questions-bank__active-label">Preguntas activas: {activeCount}</p>
        {activeCount === 0 && (
          <p className="questions-bank__warning" role="alert">
            Debes activar al menos una pregunta antes de iniciar una partida.
          </p>
        )}
      </section>

      <section className="questions-bank__sets-section">
        <div className="questions-bank__sets-header">
          <h2 className="questions-bank__section-title">LISTAS DE PREGUNTAS</h2>
          <button
            type="button"
            className="questions-bank__new-set-btn"
            onClick={() => navigate('/questions/sets/new')}
          >
            + NUEVA LISTA
          </button>
        </div>

        <div className="questions-bank__sets-grid">
          {questionSets.map((questionSet) => (
            <article key={questionSet.id} className="questions-bank__set-card">
              <h3 className="questions-bank__set-name">📚 {questionSet.name}</h3>
              <p className="questions-bank__set-count">
                {questionSet.active_question_count} preguntas activas · {questionSet.question_count} en total
              </p>
              {questionSet.description && (
                <p className="questions-bank__set-description">{questionSet.description}</p>
              )}
              <div className="questions-bank__actions">
                <button
                  type="button"
                  className="questions-bank__action-btn"
                  onClick={() => navigate(`/questions/sets/${questionSet.id}/edit`)}
                >
                  EDITAR
                </button>
                <button
                  type="button"
                  className="questions-bank__action-btn"
                  onClick={() => handleDuplicateSet(questionSet.id)}
                >
                  DUPLICAR
                </button>
                <button
                  type="button"
                  className="questions-bank__action-btn questions-bank__action-btn--danger"
                  onClick={() => handleDeleteSet(questionSet)}
                >
                  ELIMINAR
                </button>
              </div>
            </article>
          ))}
        </div>
      </section>

      <h2 className="questions-bank__section-title questions-bank__section-title--global">
        PREGUNTAS DEL BANCO
      </h2>

      <div className="questions-bank__toolbar">
        <button
          type="button"
          className="questions-bank__new-btn"
          onClick={() => navigate('/questions/new')}
        >
          + NUEVA PREGUNTA
        </button>
      </div>

      {error && (
        <p className="questions-bank__message questions-bank__message--error" role="alert">
          {error}
        </p>
      )}

      {successMessage && (
        <p className="questions-bank__message questions-bank__message--success" role="status">
          {successMessage}
        </p>
      )}

      {isLoading ? (
        <p className="questions-bank__loading">Cargando preguntas...</p>
      ) : (
        <div className="questions-bank__list">
          {questions.map((question) => (
            <article
              key={question.id}
              className={`questions-bank__item ${
                question.active ? '' : 'questions-bank__item--inactive'
              }`}
            >
              <div className="questions-bank__item-header">
                <span className="questions-bank__order">{question.order}</span>
                <span
                  className={`questions-bank__status ${
                    question.active
                      ? 'questions-bank__status--active'
                      : 'questions-bank__status--inactive'
                  }`}
                >
                  {question.active ? '✅ ACTIVA' : '⏸ INACTIVA'}
                </span>
              </div>

              <p className="questions-bank__text">{question.text}</p>
              <p className="questions-bank__correct">
                Respuesta correcta: {getCorrectAnswerLabel(question)}
              </p>

              <div className="questions-bank__actions">
                <button
                  type="button"
                  className="questions-bank__action-btn"
                  onClick={() => navigate(`/questions/${question.id}/edit`)}
                >
                  EDITAR
                </button>
                <button
                  type="button"
                  className="questions-bank__action-btn"
                  onClick={() => handleDuplicate(question.id)}
                >
                  DUPLICAR
                </button>
                <button
                  type="button"
                  className="questions-bank__action-btn"
                  onClick={() => handlePreview(question)}
                >
                  VISTA PREVIA
                </button>
                <button
                  type="button"
                  className="questions-bank__action-btn"
                  onClick={() => handleToggleActive(question)}
                >
                  {question.active ? 'DESACTIVAR' : 'ACTIVAR'}
                </button>
                <button
                  type="button"
                  className="questions-bank__action-btn questions-bank__action-btn--icon"
                  onClick={() => handleMove(question.id, 'up')}
                  aria-label="Subir pregunta"
                >
                  ↑
                </button>
                <button
                  type="button"
                  className="questions-bank__action-btn questions-bank__action-btn--icon"
                  onClick={() => handleMove(question.id, 'down')}
                  aria-label="Bajar pregunta"
                >
                  ↓
                </button>
                <button
                  type="button"
                  className="questions-bank__action-btn questions-bank__action-btn--danger"
                  onClick={() => handleDelete(question)}
                >
                  ELIMINAR
                </button>
              </div>
            </article>
          ))}
        </div>
      )}

      {previewData && (
        <QuestionPreviewModal preview={previewData} onClose={() => setPreviewData(null)} />
      )}
    </div>
  )
}
