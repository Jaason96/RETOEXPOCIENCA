import type { CSSProperties } from 'react'
import type { DisplayPlayer } from '../types/game'
import './PlayerCard.css'

interface PlayerCardProps {
  player: DisplayPlayer
  selected?: boolean
  playerNumber?: number
  onClick?: () => void
}

export default function PlayerCard({ player, selected = false, playerNumber, onClick }: PlayerCardProps) {
  return (
    <button
      type="button"
      className={`player-card ${selected ? 'player-card--selected' : ''}`}
      onClick={onClick}
      style={{ '--player-color': player.color } as CSSProperties}
    >
      {playerNumber !== undefined && (
        <span className="player-card__number">{playerNumber}</span>
      )}
      <div className="player-card__avatar">{player.avatarInitial}</div>
      <span className="player-card__name">{player.name}</span>
    </button>
  )
}
