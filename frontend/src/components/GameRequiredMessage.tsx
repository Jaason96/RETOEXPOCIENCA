import './GameRequiredMessage.css'

interface GameRequiredMessageProps {
  screenName: string
}

export default function GameRequiredMessage({ screenName }: GameRequiredMessageProps) {
  return (
    <div className="game-required">
      <p className="game-required__title">Partida no iniciada</p>
      <p className="game-required__text">
        Para ver <strong>{screenName}</strong>, primero crea una partida en la pantalla
        de jugadores.
      </p>
    </div>
  )
}
