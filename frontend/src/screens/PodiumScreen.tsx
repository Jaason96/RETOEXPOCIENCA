import { useNavigate } from 'react-router-dom'
import { useGameSession } from '../context/GameSessionContext'
import { getDisplayPlayers, sortPlayersByScore } from '../utils/gameUtils'
import { EVENT_NAME, INSTITUTION_NAME } from '../constants/eventIdentity'
import Confetti from '../components/Confetti'
import './PodiumScreen.css'

interface PodiumScreenProps {
  showNewGameButton?: boolean
}

export default function PodiumScreen({ showNewGameButton = false }: PodiumScreenProps) {
  const { game } = useGameSession()
  const navigate = useNavigate()

  if (!game) {
    return null
  }

  const rankedPlayers = sortPlayersByScore(getDisplayPlayers(game))
  const [first, second, third, ...remainingPlayers] = rankedPlayers
  const fourth = remainingPlayers[0]

  return (
    <div className="podium-screen">
      <Confetti />

      <h1 className="podium-screen__title">
        🏆 RESULTADOS DE {EVENT_NAME.toUpperCase()}
      </h1>

      <div className="podium-screen__podium">
        {second && (
          <div className="podium-screen__place podium-screen__place--2">
            <div className="podium-screen__avatar" style={{ backgroundColor: second.color }}>
              {second.avatarInitial}
            </div>
            <span className="podium-screen__medal">🥈</span>
            <span className="podium-screen__name">{second.name}</span>
            <span className="podium-screen__score">
              {second.score.toLocaleString('es-CO')} pts
            </span>
            <div className="podium-screen__block podium-screen__block--2">2</div>
          </div>
        )}

        {first && (
          <div className="podium-screen__place podium-screen__place--1">
            <div
              className="podium-screen__avatar podium-screen__avatar--winner"
              style={{ backgroundColor: first.color }}
            >
              {first.avatarInitial}
            </div>
            <span className="podium-screen__medal">🥇</span>
            <span className="podium-screen__name">{first.name}</span>
            <span className="podium-screen__score">
              {first.score.toLocaleString('es-CO')} pts
            </span>
            <div className="podium-screen__block podium-screen__block--1">1</div>
          </div>
        )}

        {third && (
          <div className="podium-screen__place podium-screen__place--3">
            <div className="podium-screen__avatar" style={{ backgroundColor: third.color }}>
              {third.avatarInitial}
            </div>
            <span className="podium-screen__medal">🥉</span>
            <span className="podium-screen__name">{third.name}</span>
            <span className="podium-screen__score">
              {third.score.toLocaleString('es-CO')} pts
            </span>
            <div className="podium-screen__block podium-screen__block--3">3</div>
          </div>
        )}
      </div>

      {fourth && (
        <div className="podium-screen__fourth">
          <span className="podium-screen__fourth-rank">4.</span>
          <span className="podium-screen__fourth-name">{fourth.name}</span>
          <span className="podium-screen__fourth-score">
            {fourth.score.toLocaleString('es-CO')} pts
          </span>
        </div>
      )}

      <div className="podium-screen__mascots">
        <img
          src="/assets/neo-esperancita-victoria-transparente.png"
          alt="Neo y Esperancita celebrando con el trofeo"
          className="podium-screen__mascots-image"
        />
      </div>

      <div className="podium-screen__footer">
        <p className="podium-screen__thanks">¡Gracias por participar!</p>
        <p className="podium-screen__school">{INSTITUTION_NAME}</p>
        {showNewGameButton && (
          <button
            type="button"
            className="podium-screen__new-game-btn"
            onClick={() => navigate('/setup')}
          >
            NUEVA PARTIDA
          </button>
        )}
      </div>
    </div>
  )
}
