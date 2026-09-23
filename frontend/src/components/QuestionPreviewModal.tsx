import { useEffect } from 'react'
import type { QuestionPreviewData } from '../types/question'
import AnswerOption from './AnswerOption'
import './QuestionPreviewModal.css'

interface QuestionPreviewModalProps {
  preview: QuestionPreviewData
  onClose: () => void
}

export default function QuestionPreviewModal({
  preview,
  onClose,
}: QuestionPreviewModalProps) {
  useEffect(() => {
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        onClose()
      }
    }
    window.addEventListener('keydown', handleEscape)
    return () => window.removeEventListener('keydown', handleEscape)
  }, [onClose])

  return (
    <div className="question-preview" role="dialog" aria-modal="true">
      <div className="question-preview__backdrop" onClick={onClose} />
      <div className="question-preview__card">
        <div className="question-preview__header">
          <h2 className="question-preview__title">Vista previa</h2>
          <button type="button" className="question-preview__close" onClick={onClose}>
            ✕
          </button>
        </div>

        <p className="question-preview__question">{preview.text}</p>

        <div className="question-preview__answers">
          {preview.options.map((option) => (
            <AnswerOption
              key={option.letter}
              letter={option.letter}
              text={option.text}
              color={option.color}
            />
          ))}
        </div>
      </div>
    </div>
  )
}
