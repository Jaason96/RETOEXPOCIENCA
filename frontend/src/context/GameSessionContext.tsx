import {

  createContext,

  useCallback,

  useContext,

  useEffect,

  useMemo,

  useRef,

  useState,

  type ReactNode,

} from 'react'

import type {

  AnswerLetter,

  AnswerResult,

  GameDetail,

  WebSocketAction,

  WebSocketMessage,

} from '../types/game'

import { fetchGame, ApiError } from '../api/client'

import { GameWebSocketClient } from '../api/websocket'



interface GameSessionContextValue {

  gameId: number

  game: GameDetail | null

  isLoading: boolean

  error: string | null

  lastIncorrectResult: AnswerResult | null

  sendAction: (action: WebSocketAction) => void

  refreshGame: () => Promise<void>

  clearIncorrectResult: () => void

}



const GameSessionContext = createContext<GameSessionContextValue | null>(null)



interface GameSessionProviderProps {

  gameId: number

  children: ReactNode

}



export function GameSessionProvider({ gameId, children }: GameSessionProviderProps) {

  const [game, setGame] = useState<GameDetail | null>(null)

  const [isLoading, setIsLoading] = useState(true)

  const [error, setError] = useState<string | null>(null)

  const [lastIncorrectResult, setLastIncorrectResult] = useState<AnswerResult | null>(null)

  const socketRef = useRef(new GameWebSocketClient())



  const refreshGame = useCallback(async () => {

    setIsLoading(true)

    setError(null)



    try {

      const loadedGame = await fetchGame(gameId)

      setGame(loadedGame)

    } catch (caughtError) {

      const message =

        caughtError instanceof ApiError

          ? caughtError.message

          : 'No se pudo cargar la partida.'

      setError(message)

    } finally {

      setIsLoading(false)

    }

  }, [gameId])



  useEffect(() => {

    refreshGame()

  }, [refreshGame])



  useEffect(() => {

    const socket = socketRef.current

    socket.connect(gameId)



    const handleMessage = (message: WebSocketMessage) => {

      if (message.type === 'game_state') {

        setGame(message.payload as GameDetail)

      }



      if (message.type === 'answer_result') {

        const answerResult = message.payload as AnswerResult

        if (!answerResult.is_correct) {

          setLastIncorrectResult(answerResult)

        } else {

          setLastIncorrectResult(null)

        }

      }



      if (message.type === 'question_changed' || message.type === 'game_finished') {

        setLastIncorrectResult(null)

      }



      if (message.type === 'error') {

        const payload = message.payload as { message?: string }

        if (payload.message) {

          setError(payload.message)

        }

      }

    }



    const unsubscribe = socket.subscribe(handleMessage)



    return () => {

      unsubscribe()

      socket.disconnect()

    }

  }, [gameId])



  const sendAction = useCallback((action: WebSocketAction) => {

    setError(null)

    socketRef.current.send(action)

  }, [])



  const clearIncorrectResult = useCallback(() => {

    setLastIncorrectResult(null)

  }, [])



  const value = useMemo(

    () => ({

      gameId,

      game,

      isLoading,

      error,

      lastIncorrectResult,

      sendAction,

      refreshGame,

      clearIncorrectResult,

    }),

    [

      gameId,

      game,

      isLoading,

      error,

      lastIncorrectResult,

      sendAction,

      refreshGame,

      clearIncorrectResult,

    ],

  )



  return (

    <GameSessionContext.Provider value={value}>{children}</GameSessionContext.Provider>

  )

}



export function useGameSession() {

  const context = useContext(GameSessionContext)

  if (!context) {

    throw new Error('useGameSession debe usarse dentro de GameSessionProvider')

  }

  return context

}



export function useModeratorActions() {

  const { sendAction } = useGameSession()



  return {

    lockBuzzers: () => sendAction({ action: 'lock_buzzers' }),

    resetBuzzers: () => sendAction({ action: 'reset_buzzers' }),

    registerBuzz: (playerNumber: number) =>

      sendAction({ action: 'register_buzz', player_number: playerNumber }),

    submitAnswer: (answer: AnswerLetter) =>

      sendAction({ action: 'submit_answer', answer }),

    nextQuestion: () => sendAction({ action: 'next_question' }),

    finishGame: () => sendAction({ action: 'finish_game' }),

  }

}

