import { useEffect, useMemo, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import type { Question } from '../types/game'
import {
  ApiError,
  createQuestionSet,
  fetchQuestionBank,
  fetchQuestionSet,
  updateQuestionSet,
} from '../api/client'
import LogoPlaceholder from '../components/LogoPlaceholder'
import HomeButton from '../components/navigation/HomeButton'
import './QuestionSetFormScreen.css'

export default function QuestionSetFormScreen() {
  const navigate = useNavigate()
  const { questionSetId = '' } = useParams()
  const isEditing = Boolean(questionSetId)
  const parsedQuestionSetId = Number(questionSetId)

  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [availableQuestions, setAvailableQuestions] = useState<Question[]>([])
  const [selectedQuestionIds, setSelectedQuestionIds] = useState<number[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const loadData = async () => {
      setIsLoading(true)
      setError(null)

      try {
        const bank = await fetchQuestionBank()
        setAvailableQuestions(bank.questions)

        if (isEditing && parsedQuestionSetId) {
          const questionSet = await fetchQuestionSet(parsedQuestionSetId)
          setName(questionSet.name)
          setDescription(questionSet.description)
          setSelectedQuestionIds(questionSet.items.map((item) => item.question_id))
        }
      } catch (caughtError) {
        setError(
          caughtError instanceof ApiError
            ? caughtError.message
            : 'No se pudo cargar la información de la lista.',
        )
      } finally {
        setIsLoading(false)
      }
    }

    loadData()
  }, [isEditing, parsedQuestionSetId])

  const selectedQuestions = useMemo(
    () =>
      selectedQuestionIds
        .map((questionId) => availableQuestions.find((question) => question.id === questionId))
        .filter((question): question is Question => question !== undefined),
    [availableQuestions, selectedQuestionIds],
  )

  const toggleQuestion = (question: Question) => {
    if (!question.active && !selectedQuestionIds.includes(question.id)) {
      return
    }

    setSelectedQuestionIds((previousIds) => {
      if (previousIds.includes(question.id)) {
        return previousIds.filter((id) => id !== question.id)
      }
      return [...previousIds, question.id]
    })
    setError(null)
  }

  const moveSelectedQuestion = (questionId: number, direction: 'up' | 'down') => {
    const currentIndex = selectedQuestionIds.indexOf(questionId)
    if (currentIndex === -1) {
      return
    }

    const swapIndex = direction === 'up' ? currentIndex - 1 : currentIndex + 1
    if (swapIndex < 0 || swapIndex >= selectedQuestionIds.length) {
      return
    }

    const reorderedIds = [...selectedQuestionIds]
    reorderedIds[currentIndex] = reorderedIds[swapIndex]
    reorderedIds[swapIndex] = questionId
    setSelectedQuestionIds(reorderedIds)
  }

  const handleSubmit = async () => {
    if (!name.trim()) {
      setError('El nombre de la lista es obligatorio.')
      return
    }
    if (selectedQuestionIds.length === 0) {
      setError('Debes seleccionar al menos una pregunta.')
      return
    }

    setIsSaving(true)
    setError(null)

    const payload = {
      name: name.trim(),
      description: description.trim(),
      question_ids: selectedQuestionIds,
    }

    try {
      if (isEditing && parsedQuestionSetId) {
        await updateQuestionSet(parsedQuestionSetId, payload)
      } else {
        await createQuestionSet(payload)
      }
      navigate('/questions')
    } catch (caughtError) {
      setError(caughtError instanceof ApiError ? caughtError.message : 'No se pudo guardar la lista.')
    } finally {
      setIsSaving(false)
    }
  }

  if (isLoading) {
    return (
      <div className="question-set-form__loading screen-with-home">
        <HomeButton className="home-button--corner" />
        Cargando lista...
      </div>
    )
  }

  return (
    <div className="question-set-form">
      <div className="question-set-form__header-wrap screen-with-home">
        <header className="question-set-form__header">
          <LogoPlaceholder size="small" />
          <div>
            <h1 className="question-set-form__title">
              {isEditing ? 'EDITAR LISTA' : 'NUEVA LISTA'}
            </h1>
            <Link to="/questions" className="question-set-form__back-link">
              Volver al banco
            </Link>
          </div>
        </header>
        <HomeButton className="home-button--corner" />
      </div>

      <div className="question-set-form__body">
        <label className="question-set-form__field">
          <span className="question-set-form__label">Nombre</span>
          <input
            className="question-set-form__input"
            value={name}
            maxLength={100}
            onChange={(event) => setName(event.target.value)}
            placeholder="Lista A — Ronda 1"
          />
        </label>

        <label className="question-set-form__field">
          <span className="question-set-form__label">Descripción</span>
          <textarea
            className="question-set-form__textarea"
            value={description}
            maxLength={300}
            rows={2}
            onChange={(event) => setDescription(event.target.value)}
            placeholder="Preguntas utilizadas para el primer grupo"
          />
        </label>

        <section className="question-set-form__section">
          <h2 className="question-set-form__section-title">Seleccionar preguntas</h2>
          <div className="question-set-form__question-list">
            {availableQuestions.map((question) => {
              const isSelected = selectedQuestionIds.includes(question.id)
              const isDisabled = !question.active && !isSelected

              return (
                <label
                  key={question.id}
                  className={`question-set-form__question-item ${
                    isDisabled ? 'question-set-form__question-item--disabled' : ''
                  } ${!question.active ? 'question-set-form__question-item--inactive' : ''}`}
                >
                  <input
                    type="checkbox"
                    checked={isSelected}
                    disabled={isDisabled}
                    onChange={() => toggleQuestion(question)}
                  />
                  <span className="question-set-form__question-text">{question.text}</span>
                  {!question.active && (
                    <span className="question-set-form__inactive-badge">INACTIVA</span>
                  )}
                </label>
              )
            })}
          </div>
        </section>

        <section className="question-set-form__section">
          <h2 className="question-set-form__section-title">
            Orden de la lista ({selectedQuestionIds.length} preguntas seleccionadas)
          </h2>
          {selectedQuestions.length === 0 ? (
            <p className="question-set-form__empty">Selecciona al menos una pregunta.</p>
          ) : (
            <div className="question-set-form__selected-list">
              {selectedQuestions.map((question, index) => (
                <div key={question.id} className="question-set-form__selected-item">
                  <span className="question-set-form__selected-order">{index + 1}</span>
                  <span className="question-set-form__selected-text">{question.text}</span>
                  <div className="question-set-form__selected-actions">
                    <button
                      type="button"
                      className="question-set-form__move-btn"
                      onClick={() => moveSelectedQuestion(question.id, 'up')}
                      disabled={index === 0}
                    >
                      ↑
                    </button>
                    <button
                      type="button"
                      className="question-set-form__move-btn"
                      onClick={() => moveSelectedQuestion(question.id, 'down')}
                      disabled={index === selectedQuestions.length - 1}
                    >
                      ↓
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>

        {error && (
          <p className="question-set-form__error" role="alert">
            {error}
          </p>
        )}

        <div className="question-set-form__actions">
          <button
            type="button"
            className="question-set-form__btn question-set-form__btn--secondary"
            onClick={() => navigate('/questions')}
          >
            CANCELAR
          </button>
          <button
            type="button"
            className="question-set-form__btn question-set-form__btn--primary"
            disabled={isSaving}
            onClick={handleSubmit}
          >
            {isSaving ? 'GUARDANDO...' : 'GUARDAR LISTA'}
          </button>
        </div>
      </div>
    </div>
  )
}
