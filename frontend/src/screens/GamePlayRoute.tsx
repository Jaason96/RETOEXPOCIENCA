import { useParams } from 'react-router-dom'
import { GameSessionProvider, useGameSession } from '../context/GameSessionContext'
import GamePlayScreen from './GamePlayScreen'
import GameRequiredMessage from '../components/GameRequiredMessage'

function PlayContent() {
  const { game, isLoading } = useGameSession()

  if (isLoading && !game) {
    return <div className="game-loading">Cargando partida...</div>
  }

  if (!game) {
    return <GameRequiredMessage screenName="el juego" />
  }

  return <GamePlayScreen />
}

export default function GamePlayRoute() {
  const { gameId = '' } = useParams()
  const parsedGameId = Number(gameId)

  if (!parsedGameId) {
    return <GameRequiredMessage screenName="el juego" />
  }

  return (
    <GameSessionProvider gameId={parsedGameId}>
      <PlayContent />
    </GameSessionProvider>
  )
}
