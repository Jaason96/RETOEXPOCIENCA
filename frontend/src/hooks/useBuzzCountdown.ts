import { useEffect, useState } from 'react'

const COUNTDOWN_TICK_INTERVAL_MS = 250

function computeRemainingSeconds(buzzDeadline: string | null): number {
  if (!buzzDeadline) {
    return 0
  }

  const millisecondsRemaining = new Date(buzzDeadline).getTime() - Date.now()
  return Math.max(0, Math.ceil(millisecondsRemaining / 1000))
}

/**
 * Renders the server-authoritative buzz deadline as a per-second countdown.
 * Purely presentational: the backend, not this hook, decides when a turn ends.
 */
export function useBuzzCountdown(buzzDeadline: string | null): number {
  const [remainingSeconds, setRemainingSeconds] = useState(() =>
    computeRemainingSeconds(buzzDeadline),
  )

  useEffect(() => {
    setRemainingSeconds(computeRemainingSeconds(buzzDeadline))

    if (!buzzDeadline) {
      return
    }

    const intervalId = window.setInterval(() => {
      setRemainingSeconds(computeRemainingSeconds(buzzDeadline))
    }, COUNTDOWN_TICK_INTERVAL_MS)

    return () => window.clearInterval(intervalId)
  }, [buzzDeadline])

  return remainingSeconds
}
