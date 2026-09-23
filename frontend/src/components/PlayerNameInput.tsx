import type { CSSProperties } from 'react'
import { PLAYER_COLORS } from '../constants/gameConstants'
import './PlayerNameInput.css'

interface PlayerNameInputProps {
  playerNumber: number
  value: string
  onChange: (value: string) => void
  maxLength?: number
}

export default function PlayerNameInput({
  playerNumber,
  value,
  onChange,
  maxLength = 20,
}: PlayerNameInputProps) {
  const playerColor = PLAYER_COLORS[playerNumber]

  return (
    <label
      className="player-name-input"
      style={{ '--player-color': playerColor.hex } as CSSProperties}
    >
      <span className="player-name-input__label">
        Jugador {playerNumber} {playerColor.emoji}
      </span>
      <input
        type="text"
        className="player-name-input__field"
        value={value}
        maxLength={maxLength}
        placeholder={`Nombre del jugador ${playerNumber}`}
        onChange={(event) => onChange(event.target.value)}
        autoComplete="off"
      />
    </label>
  )
}
