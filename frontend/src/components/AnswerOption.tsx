import type { CSSProperties } from 'react'
import './AnswerOption.css'

interface AnswerOptionProps {
  letter: 'A' | 'B' | 'C' | 'D'
  text: string
  color: string
  onClick?: () => void
  disabled?: boolean
  selectable?: boolean
}

export default function AnswerOption({
  letter,
  text,
  color,
  onClick,
  disabled = false,
  selectable = false,
}: AnswerOptionProps) {
  const className = [
    'answer-option',
    selectable ? 'answer-option--selectable' : '',
    disabled ? 'answer-option--disabled' : '',
  ]
    .filter(Boolean)
    .join(' ')

  if (onClick) {
    return (
      <button
        type="button"
        className={className}
        style={{ '--option-color': color } as CSSProperties}
        onClick={onClick}
        disabled={disabled}
      >
        <span className="answer-option__letter">{letter}</span>
        <span className="answer-option__text">{text}</span>
      </button>
    )
  }

  return (
    <div className={className} style={{ '--option-color': color } as CSSProperties}>
      <span className="answer-option__letter">{letter}</span>
      <span className="answer-option__text">{text}</span>
    </div>
  )
}
