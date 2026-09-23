import { useEffect, useState } from 'react'
import type { AnswerFailureReason } from '../types/game'
import './IncorrectAnswerOverlay.css'

const DISPLAY_MS = 1500
const FADE_OUT_MS = 250

const OVERLAY_CONTENT: Record<
  AnswerFailureReason,
  { title: string; buildMessage: (playerName: string) => string }
> = {
  INCORRECT: {
    title: '❌ RESPUESTA INCORRECTA',
    buildMessage: (playerName) => `${playerName} no puede volver a responder esta pregunta.`,
  },
  TIMEOUT: {
    title: '⏱️ TIEMPO AGOTADO',
    buildMessage: (playerName) => `${playerName} no respondió a tiempo y pierde el turno.`,
  },
}

interface IncorrectAnswerOverlayProps {
  playerName: string
  reason: AnswerFailureReason
  onDismiss: () => void
}

export default function IncorrectAnswerOverlay({
  playerName,
  reason,
  onDismiss,
}: IncorrectAnswerOverlayProps) {
  const [isExiting, setIsExiting] = useState(false)

  useEffect(() => {
    setIsExiting(false)
    const exitTimer = window.setTimeout(() => setIsExiting(true), DISPLAY_MS)
    return () => window.clearTimeout(exitTimer)
  }, [onDismiss, playerName, reason])

  useEffect(() => {
    if (!isExiting) {
      return
    }

    const dismissTimer = window.setTimeout(onDismiss, FADE_OUT_MS)
    return () => window.clearTimeout(dismissTimer)
  }, [isExiting, onDismiss])

  const content = OVERLAY_CONTENT[reason]

  return (
    <div
      className={`incorrect-overlay${isExiting ? ' incorrect-overlay--exiting' : ''}`}
      role="alert"
    >
      <div className="incorrect-overlay__card">
        <p className="incorrect-overlay__title">{content.title}</p>
        <p className="incorrect-overlay__player">{content.buildMessage(playerName)}</p>
      </div>
    </div>
  )
}
