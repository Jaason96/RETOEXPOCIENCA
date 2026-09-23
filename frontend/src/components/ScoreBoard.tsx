import type { DisplayPlayer } from '../types/game'
import './ScoreBoard.css'

interface ScoreBoardProps {
  players: DisplayPlayer[]
  variant?: 'tv' | 'compact'
}

export default function ScoreBoard({ players, variant = 'tv' }: ScoreBoardProps) {
  return (
    <div className={`scoreboard scoreboard--${variant}`}>
      {players.map((player) => (
        <div key={player.id} className="scoreboard__item">
          <span
            className="scoreboard__dot"
            style={{ backgroundColor: player.color }}
          />
          <span className="scoreboard__name">{player.name}</span>
          <span className="scoreboard__score">
            {player.score.toLocaleString('es-CO')} pts
          </span>
        </div>
      ))}
    </div>
  )
}
