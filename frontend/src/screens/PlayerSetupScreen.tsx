import { useNavigate } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { MAX_PLAYER_NAME_LENGTH, PLAYER_COUNTS } from '../constants/gameConstants'
import { createGame, fetchQuestionSets, ApiError } from '../api/client'
import { INSTITUTION_NAME } from '../constants/eventIdentity'
import type { QuestionSetSummary } from '../types/questionSet'
import PlayerNameInput from '../components/PlayerNameInput'
import LogoPlaceholder from '../components/LogoPlaceholder'
import HomeButton from '../components/navigation/HomeButton'
import './PlayerSetupScreen.css'

const DEFAULT_NAMES = ['', '', '', '']

export default function PlayerSetupScreen() {
  const navigate = useNavigate()
  const [questionSets, setQuestionSets] = useState<QuestionSetSummary[]>([])
  const [selectedQuestionSetId, setSelectedQuestionSetId] = useState<number | null>(null)
  const [playerCount, setPlayerCount] = useState<number>(4)
  const [playerNames, setPlayerNames] = useState<string[]>(DEFAULT_NAMES)
  const [validationError, setValidationError] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [isLoadingSets, setIsLoadingSets] = useState(true)

  useEffect(() => {
    const loadQuestionSets = async () => {
      setIsLoadingSets(true)
      try {
        const sets = await fetchQuestionSets()
        setQuestionSets(sets)
      } catch {
        setError('No se pudieron cargar las listas de preguntas.')
      } finally {
        setIsLoadingSets(false)
      }
    }

    loadQuestionSets()
  }, [])

  const selectedQuestionSet = questionSets.find((set) => set.id === selectedQuestionSetId) ?? null

  const handleCountChange = (count: number) => {
    setPlayerCount(count)
    setValidationError(null)
    setError(null)
  }

  const handleNameChange = (index: number, value: string) => {
    setPlayerNames((previousNames) => {
      const updatedNames = [...previousNames]
      updatedNames[index] = value
      return updatedNames
    })
    setValidationError(null)
    setError(null)
  }

  const validateForm = (): string | null => {
    if (selectedQuestionSetId === null) {
      return 'Selecciona una lista de preguntas para comenzar.'
    }

    const selectedSet = questionSets.find((set) => set.id === selectedQuestionSetId)
    if (selectedSet && selectedSet.active_question_count === 0) {
      return 'La lista seleccionada no contiene preguntas activas.'
    }

    for (let index = 0; index < playerCount; index += 1) {
      const trimmedName = playerNames[index].trim()
      if (!trimmedName) {
        return `El jugador ${index + 1} necesita un nombre`
      }
      if (trimmedName.length > MAX_PLAYER_NAME_LENGTH) {
        return `Los nombres no pueden superar ${MAX_PLAYER_NAME_LENGTH} caracteres`
      }
    }
    return null
  }

  const handleStartGame = async () => {
    const validationMessage = validateForm()
    if (validationMessage) {
      setValidationError(validationMessage)
      return
    }

    const players = Array.from({ length: playerCount }, (_, index) => ({
      number: index + 1,
      name: playerNames[index].trim(),
    }))

    setIsLoading(true)
    setError(null)

    try {
      const createdGame = await createGame(selectedQuestionSetId!, players)
      navigate(`/game/${createdGame.id}/play`)
    } catch (caughtError) {
      const message =
        caughtError instanceof ApiError
          ? caughtError.message
          : 'No se pudo crear la partida. Verifica que el backend esté activo.'
      setError(message)
    } finally {
      setIsLoading(false)
    }
  }

  const visibleError = validationError ?? error

  return (
    <div className="player-setup">
      <div className="player-setup__top-bar screen-with-home">
        <HomeButton className="home-button--corner" />
        <div className="player-setup__header">
          <LogoPlaceholder size="small" />
          <h1 className="player-setup__title">Preparar Partida</h1>
          <p className="player-setup__subtitle">{INSTITUTION_NAME}</p>
        </div>
      </div>

      <div className="player-setup__set-section">
        <h2 className="player-setup__section-title">Lista para esta ronda</h2>
        {isLoadingSets ? (
          <p className="player-setup__set-loading">Cargando listas...</p>
        ) : (
          <>
            <select
              className="player-setup__set-select"
              value={selectedQuestionSetId ?? ''}
              onChange={(event) => {
                const value = event.target.value
                setSelectedQuestionSetId(value ? Number(value) : null)
                setValidationError(null)
                setError(null)
              }}
            >
              <option value="">Selecciona una lista de preguntas</option>
              {questionSets.map((questionSet) => (
                <option key={questionSet.id} value={questionSet.id}>
                  {questionSet.name} · {questionSet.active_question_count} preguntas
                </option>
              ))}
            </select>

            {selectedQuestionSet && (
              <div className="player-setup__set-card">
                <p className="player-setup__set-card-name">{selectedQuestionSet.name}</p>
                <p className="player-setup__set-card-count">
                  {selectedQuestionSet.active_question_count} preguntas activas
                </p>
                {selectedQuestionSet.description && (
                  <p className="player-setup__set-card-description">
                    {selectedQuestionSet.description}
                  </p>
                )}
              </div>
            )}
          </>
        )}
      </div>

      <div className="player-setup__count-section">
        <h2 className="player-setup__section-title">Número de jugadores</h2>
        <div className="player-setup__count-options">
          {PLAYER_COUNTS.map((count) => (
            <button
              key={count}
              type="button"
              className={`player-setup__count-btn ${playerCount === count ? 'player-setup__count-btn--active' : ''}`}
              onClick={() => handleCountChange(count)}
            >
              {count} jugadores
            </button>
          ))}
        </div>
      </div>

      <div className="player-setup__players-section">
        <h2 className="player-setup__section-title">Nombres de los jugadores</h2>
        <div className="player-setup__inputs">
          {Array.from({ length: playerCount }, (_, index) => (
            <PlayerNameInput
              key={index + 1}
              playerNumber={index + 1}
              value={playerNames[index]}
              onChange={(value) => handleNameChange(index, value)}
              maxLength={MAX_PLAYER_NAME_LENGTH}
            />
          ))}
        </div>
      </div>

      {visibleError && (
        <p className="player-setup__error" role="alert">
          {visibleError}
        </p>
      )}

      <button
        type="button"
        className="player-setup__start-btn"
        onClick={handleStartGame}
        disabled={isLoading || isLoadingSets}
      >
        {isLoading ? 'CREANDO PARTIDA...' : 'COMENZAR PARTIDA'}
      </button>
    </div>
  )
}
