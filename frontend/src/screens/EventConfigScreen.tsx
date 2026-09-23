import { useEffect, useState } from 'react'
import { ApiError, updateEventConfig } from '../api/client'
import { useEventConfig } from '../context/EventConfigContext'
import type { EventConfigFormData } from '../types/eventConfig'
import { eventConfigToFormData } from '../types/eventConfig'
import { DEFAULT_PLAYER_KEY_CODES } from '../constants/gameConstants'
import { formatKeyCodeLabel } from '../utils/keyboardKeyLabels'
import HomeButton from '../components/navigation/HomeButton'
import LogoPlaceholder from '../components/LogoPlaceholder'
import ToastMessage from '../components/ToastMessage'
import './EventConfigScreen.css'

const PLAYER_NUMBERS = [1, 2, 3, 4] as const

type PlayerKeyField = 'player_1_key' | 'player_2_key' | 'player_3_key' | 'player_4_key'

const PLAYER_KEY_FIELDS: Record<(typeof PLAYER_NUMBERS)[number], PlayerKeyField> = {
  1: 'player_1_key',
  2: 'player_2_key',
  3: 'player_3_key',
  4: 'player_4_key',
}

const EMPTY_FORM: EventConfigFormData = {
  correct_answer_points: '1000',
  response_time_seconds: '7',
  player_1_key: DEFAULT_PLAYER_KEY_CODES[1],
  player_2_key: DEFAULT_PLAYER_KEY_CODES[2],
  player_3_key: DEFAULT_PLAYER_KEY_CODES[3],
  player_4_key: DEFAULT_PLAYER_KEY_CODES[4],
}

// null cuando el campo está vacío o no es un número válido — distinto de un
// 0 real, para no confundir "sin escribir todavía" con "el usuario puso 0".
function parseFormNumber(value: string): number | null {
  const trimmed = value.trim()
  if (trimmed === '') {
    return null
  }
  const parsed = Number(trimmed)
  return Number.isFinite(parsed) ? parsed : null
}

export default function EventConfigScreen() {
  const { config, isLoading, setConfig } = useEventConfig()
  const [form, setForm] = useState<EventConfigFormData>(EMPTY_FORM)
  const [isSaving, setIsSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [showSuccessToast, setShowSuccessToast] = useState(false)
  const [capturingPlayer, setCapturingPlayer] = useState<(typeof PLAYER_NUMBERS)[number] | null>(
    null,
  )

  useEffect(() => {
    if (config) {
      setForm(eventConfigToFormData(config))
    }
  }, [config])

  const updateField = <K extends keyof EventConfigFormData>(
    field: K,
    value: EventConfigFormData[K],
  ) => {
    setForm((previousForm) => ({ ...previousForm, [field]: value }))
    setError(null)
    setShowSuccessToast(false)
  }

  // Escucha la siguiente pulsación física mientras se captura la tecla de un
  // jugador. Escape cancela sin cambiar nada; una tecla ya usada por otro
  // jugador se rechaza mostrando cuál la tiene asignada.
  useEffect(() => {
    if (capturingPlayer === null) {
      return
    }

    const handleKeyDown = (event: KeyboardEvent) => {
      event.preventDefault()

      if (event.code === 'Escape') {
        setCapturingPlayer(null)
        return
      }

      const conflictingPlayer = PLAYER_NUMBERS.find(
        (playerNumber) =>
          playerNumber !== capturingPlayer &&
          form[PLAYER_KEY_FIELDS[playerNumber]] === event.code,
      )

      if (conflictingPlayer) {
        setError(`Esta tecla ya está asignada al Jugador ${conflictingPlayer}.`)
        setCapturingPlayer(null)
        return
      }

      updateField(PLAYER_KEY_FIELDS[capturingPlayer], event.code)
      setCapturingPlayer(null)
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [capturingPlayer, form])

  const handleRestoreDefaultKeys = () => {
    setForm((previousForm) => ({
      ...previousForm,
      player_1_key: DEFAULT_PLAYER_KEY_CODES[1],
      player_2_key: DEFAULT_PLAYER_KEY_CODES[2],
      player_3_key: DEFAULT_PLAYER_KEY_CODES[3],
      player_4_key: DEFAULT_PLAYER_KEY_CODES[4],
    }))
    setCapturingPlayer(null)
    setError(null)
    setShowSuccessToast(false)
  }

  const validateForm = (): string | null => {
    const correctAnswerPoints = parseFormNumber(form.correct_answer_points)
    if (correctAnswerPoints === null || correctAnswerPoints < 1) {
      return 'Los puntos deben ser al menos 1.'
    }

    const responseTimeSeconds = parseFormNumber(form.response_time_seconds)
    if (responseTimeSeconds === null || responseTimeSeconds < 1 || responseTimeSeconds > 120) {
      return 'El tiempo para responder debe estar entre 1 y 120 segundos.'
    }

    return null
  }

  const handleSubmit = async () => {
    const validationMessage = validateForm()
    if (validationMessage) {
      setError(validationMessage)
      return
    }

    const correctAnswerPoints = parseFormNumber(form.correct_answer_points)
    const responseTimeSeconds = parseFormNumber(form.response_time_seconds)
    if (correctAnswerPoints === null || responseTimeSeconds === null) {
      return
    }

    setIsSaving(true)
    setError(null)
    setShowSuccessToast(false)

    try {
      const updatedConfig = await updateEventConfig({
        correct_answer_points: correctAnswerPoints,
        response_time_seconds: responseTimeSeconds,
        player_1_key: form.player_1_key,
        player_2_key: form.player_2_key,
        player_3_key: form.player_3_key,
        player_4_key: form.player_4_key,
      })
      setConfig(updatedConfig)
      setForm(eventConfigToFormData(updatedConfig))
      setShowSuccessToast(true)
    } catch (caughtError) {
      setError(
        caughtError instanceof ApiError
          ? caughtError.message
          : 'No se pudo guardar la configuración del evento.',
      )
    } finally {
      setIsSaving(false)
    }
  }

  return (
    <div className="event-config">
      <div className="event-config__top-bar screen-with-home">
        <header className="event-config__header">
          <LogoPlaceholder size="small" />
          <div>
            <h1 className="event-config__title">Configuración del Evento</h1>
            <p className="event-config__subtitle">
              Ajusta los parámetros generales del Reto Científico
            </p>
          </div>
        </header>
        <HomeButton className="home-button--corner" />
      </div>

      {showSuccessToast && (
        <ToastMessage
          message="Configuración guardada correctamente"
          onClose={() => setShowSuccessToast(false)}
        />
      )}

      {isLoading ? (
        <p className="event-config__loading">Cargando configuración...</p>
      ) : (
        <form
          className="event-config__form"
          onSubmit={(event) => {
            event.preventDefault()
            void handleSubmit()
          }}
        >
          <label className="event-config__field">
            <span>Puntos por respuesta correcta</span>
            <input
              type="number"
              min={1}
              max={100000}
              value={form.correct_answer_points}
              onChange={(event) => updateField('correct_answer_points', event.target.value)}
            />
          </label>

          <label className="event-config__field">
            <span>Tiempo para responder (segundos)</span>
            <input
              type="number"
              min={1}
              max={120}
              value={form.response_time_seconds}
              onChange={(event) => updateField('response_time_seconds', event.target.value)}
            />
          </label>

          <div className="event-config__divider" />

          <h2 className="event-config__section-title">Pulsadores</h2>

          <div className="event-config__players">
            {PLAYER_NUMBERS.map((playerNumber) => {
              const isCapturing = capturingPlayer === playerNumber
              const currentKey = form[PLAYER_KEY_FIELDS[playerNumber]]

              return (
                <div className="event-config__player-row" key={playerNumber}>
                  <span className="event-config__player-label">Jugador {playerNumber}</span>
                  <div className="event-config__player-controls">
                    <span
                      className={[
                        'event-config__key-badge',
                        isCapturing ? 'event-config__key-badge--capturing' : '',
                      ]
                        .filter(Boolean)
                        .join(' ')}
                    >
                      {isCapturing ? 'Presiona una tecla...' : formatKeyCodeLabel(currentKey)}
                    </span>
                    <button
                      type="button"
                      className="event-config__key-btn"
                      disabled={capturingPlayer !== null && !isCapturing}
                      onClick={() => {
                        setError(null)
                        setCapturingPlayer(playerNumber)
                      }}
                    >
                      CAMBIAR
                    </button>
                  </div>
                </div>
              )
            })}
          </div>

          <button
            type="button"
            className="event-config__restore-btn"
            onClick={handleRestoreDefaultKeys}
          >
            RESTAURAR PREDETERMINADOS
          </button>

          <div className="event-config__divider" />

          {error && (
            <p className="event-config__message event-config__message--error" role="alert">
              {error}
            </p>
          )}

          <div className="event-config__actions">
            <button type="submit" className="event-config__save-btn" disabled={isSaving}>
              {isSaving ? 'GUARDANDO...' : 'GUARDAR CONFIGURACIÓN'}
            </button>
          </div>
        </form>
      )}
    </div>
  )
}
