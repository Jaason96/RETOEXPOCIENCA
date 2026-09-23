import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import type { AnswerLetter } from '../types/game'
import type { QuestionFormData, QuestionPreviewData } from '../types/question'
import {
  ApiError,
  createQuestion,
  fetchQuestion,
  updateQuestion,
} from '../api/client'
import { ANSWER_COLORS } from '../constants/gameConstants'
import LogoPlaceholder from '../components/LogoPlaceholder'
import HomeButton from '../components/navigation/HomeButton'
import QuestionPreviewModal from '../components/QuestionPreviewModal'
import './QuestionFormScreen.css'

const EMPTY_FORM: QuestionFormData = {
  text: '',
  option_a: '',
  option_b: '',
  option_c: '',
  option_d: '',
  correct_answer: 'A',
  explanation: '',
  active: true,
}

const ANSWER_LETTERS: AnswerLetter[] = ['A', 'B', 'C', 'D']

function questionToForm(question: Awaited<ReturnType<typeof fetchQuestion>>): QuestionFormData {
  return {
    text: question.text,
    option_a: question.options.find((option) => option.letter === 'A')?.text ?? '',
    option_b: question.options.find((option) => option.letter === 'B')?.text ?? '',
    option_c: question.options.find((option) => option.letter === 'C')?.text ?? '',
    option_d: question.options.find((option) => option.letter === 'D')?.text ?? '',
    correct_answer: question.correct_answer,
    explanation: question.explanation,
    active: question.active ?? true,
  }
}

export default function QuestionFormScreen() {
  const navigate = useNavigate()
  const { questionId = '' } = useParams()
  const isEditing = Boolean(questionId)
  const parsedQuestionId = Number(questionId)

  const [formData, setFormData] = useState<QuestionFormData>(EMPTY_FORM)
  const [isLoading, setIsLoading] = useState(isEditing)
  const [isSaving, setIsSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [successMessage, setSuccessMessage] = useState<string | null>(null)
  const [previewData, setPreviewData] = useState<QuestionPreviewData | null>(null)

  useEffect(() => {
    if (!isEditing || !parsedQuestionId) {
      return
    }

    const loadQuestion = async () => {
      setIsLoading(true)
      setError(null)

      try {
        const question = await fetchQuestion(parsedQuestionId)
        setFormData(questionToForm(question))
      } catch (caughtError) {
        setError(
          caughtError instanceof ApiError
            ? caughtError.message
            : 'No se pudo cargar la pregunta.',
        )
      } finally {
        setIsLoading(false)
      }
    }

    loadQuestion()
  }, [isEditing, parsedQuestionId])

  const updateField = <K extends keyof QuestionFormData>(
    field: K,
    value: QuestionFormData[K],
  ) => {
    setFormData((previous) => ({ ...previous, [field]: value }))
    setError(null)
  }

  const validateForm = (): string | null => {
    if (!formData.text.trim()) return 'La pregunta es obligatoria.'
    if (!formData.option_a.trim()) return 'La opción A es obligatoria.'
    if (!formData.option_b.trim()) return 'La opción B es obligatoria.'
    if (!formData.option_c.trim()) return 'La opción C es obligatoria.'
    if (!formData.option_d.trim()) return 'La opción D es obligatoria.'
    if (!formData.explanation.trim()) return 'La explicación es obligatoria.'
    return null
  }

  const handleSubmit = async () => {
    const validationMessage = validateForm()
    if (validationMessage) {
      setError(validationMessage)
      return
    }

    setIsSaving(true)
    setError(null)

    try {
      if (isEditing && parsedQuestionId) {
        await updateQuestion(parsedQuestionId, formData)
        setSuccessMessage('Pregunta actualizada correctamente.')
        window.setTimeout(() => navigate('/questions'), 1200)
      } else {
        await createQuestion(formData)
        navigate('/questions')
      }
    } catch (caughtError) {
      setError(caughtError instanceof ApiError ? caughtError.message : 'No se pudo guardar.')
    } finally {
      setIsSaving(false)
    }
  }

  const handlePreview = () => {
    const validationMessage = validateForm()
    if (validationMessage) {
      setError(validationMessage)
      return
    }

    setPreviewData({
      text: formData.text.trim(),
      options: [
        { letter: 'A', text: formData.option_a.trim(), color: ANSWER_COLORS.A },
        { letter: 'B', text: formData.option_b.trim(), color: ANSWER_COLORS.B },
        { letter: 'C', text: formData.option_c.trim(), color: ANSWER_COLORS.C },
        { letter: 'D', text: formData.option_d.trim(), color: ANSWER_COLORS.D },
      ],
    })
  }

  if (isLoading) {
    return (
      <div className="question-form__loading screen-with-home">
        <HomeButton className="home-button--corner" />
        Cargando pregunta...
      </div>
    )
  }

  return (
    <div className="question-form">
      <div className="question-form__header-wrap screen-with-home">
        <header className="question-form__header">
          <LogoPlaceholder size="small" />
          <div>
            <h1 className="question-form__title">
              {isEditing ? 'EDITAR PREGUNTA' : 'NUEVA PREGUNTA'}
            </h1>
            <Link to="/questions" className="question-form__back-link">
              Volver al banco
            </Link>
          </div>
        </header>
        <HomeButton className="home-button--corner" />
      </div>

      <form
        className="question-form__body"
        onSubmit={(event) => {
          event.preventDefault()
          handleSubmit()
        }}
      >
        <label className="question-form__field">
          <span className="question-form__label">Pregunta</span>
          <textarea
            className="question-form__textarea"
            value={formData.text}
            maxLength={300}
            rows={3}
            onChange={(event) => updateField('text', event.target.value)}
          />
        </label>

        <label className="question-form__field">
          <span className="question-form__label">Opción A</span>
          <input
            className="question-form__input"
            value={formData.option_a}
            maxLength={200}
            onChange={(event) => updateField('option_a', event.target.value)}
          />
        </label>

        <label className="question-form__field">
          <span className="question-form__label">Opción B</span>
          <input
            className="question-form__input"
            value={formData.option_b}
            maxLength={200}
            onChange={(event) => updateField('option_b', event.target.value)}
          />
        </label>

        <label className="question-form__field">
          <span className="question-form__label">Opción C</span>
          <input
            className="question-form__input"
            value={formData.option_c}
            maxLength={200}
            onChange={(event) => updateField('option_c', event.target.value)}
          />
        </label>

        <label className="question-form__field">
          <span className="question-form__label">Opción D</span>
          <input
            className="question-form__input"
            value={formData.option_d}
            maxLength={200}
            onChange={(event) => updateField('option_d', event.target.value)}
          />
        </label>

        <fieldset className="question-form__field">
          <legend className="question-form__label">Respuesta correcta</legend>
          <div className="question-form__answers">
            {ANSWER_LETTERS.map((letter) => (
              <label key={letter} className="question-form__answer-option">
                <input
                  type="radio"
                  name="correct_answer"
                  checked={formData.correct_answer === letter}
                  onChange={() => updateField('correct_answer', letter)}
                />
                <span>{letter}</span>
              </label>
            ))}
          </div>
        </fieldset>

        <label className="question-form__field">
          <span className="question-form__label">Explicación</span>
          <textarea
            className="question-form__textarea"
            value={formData.explanation}
            maxLength={500}
            rows={4}
            onChange={(event) => updateField('explanation', event.target.value)}
          />
        </label>

        <label className="question-form__checkbox">
          <input
            type="checkbox"
            checked={formData.active}
            onChange={(event) => updateField('active', event.target.checked)}
          />
          <span>Usar esta pregunta en las partidas</span>
        </label>

        {error && (
          <p className="question-form__error" role="alert">
            {error}
          </p>
        )}

        {successMessage && (
          <p className="question-form__success" role="status">
            {successMessage}
          </p>
        )}

        <div className="question-form__actions">
          <button
            type="button"
            className="question-form__btn question-form__btn--secondary"
            onClick={handlePreview}
          >
            VISTA PREVIA
          </button>
          <button
            type="button"
            className="question-form__btn question-form__btn--secondary"
            onClick={() => navigate('/questions')}
          >
            CANCELAR
          </button>
          <button
            type="submit"
            className="question-form__btn question-form__btn--primary"
            disabled={isSaving}
          >
            {isSaving ? 'GUARDANDO...' : 'GUARDAR PREGUNTA'}
          </button>
        </div>
      </form>

      {previewData && (
        <QuestionPreviewModal preview={previewData} onClose={() => setPreviewData(null)} />
      )}
    </div>
  )
}
