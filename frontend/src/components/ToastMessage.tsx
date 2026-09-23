import { useEffect } from 'react'
import './ToastMessage.css'

interface ToastMessageProps {
  message: string
  onClose: () => void
  durationMs?: number
}

export default function ToastMessage({
  message,
  onClose,
  durationMs = 3000,
}: ToastMessageProps) {
  useEffect(() => {
    const timer = window.setTimeout(onClose, durationMs)
    return () => window.clearTimeout(timer)
  }, [durationMs, message, onClose])

  return (
    <div className="toast-message" role="status" aria-live="polite">
      <span className="toast-message__icon">✓</span>
      <span className="toast-message__text">{message}</span>
    </div>
  )
}
