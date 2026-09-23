import type { BuzzPlayer, DisplayPlayer, GameStatus } from '../../types/game'
import { getPlayerRoundStatus, getPlayerRoundStatusLabel } from '../../utils/moderatorUtils'
import './ModeratorPlayerBoard.css'

interface ModeratorPlayerBoardProps {
  players: DisplayPlayer[]
  buzzPlayer: BuzzPlayer | null
  failedPlayerIds: number[]
  status: GameStatus
  playerKeyLabels: Record<number, string>
}

export default function ModeratorPlayerBoard({
  players,
  buzzPlayer,
  failedPlayerIds,
  status,
  playerKeyLabels,
}: ModeratorPlayerBoardProps) {
  const buzzIsRelevant = status === 'BUZZ_OPEN' || status === 'BUZZ_LOCKED'

  return (
    <section className="moderator-player-board" aria-label="Jugadores">
      <h2 className="moderator-player-board__title">Jugadores</h2>

      <ul className="moderator-player-board__list">
        {players.map((player) => {
          const roundStatus = buzzIsRelevant
            ? getPlayerRoundStatus(player.id, buzzPlayer?.id, failedPlayerIds)
            : null
          const roundLabel = getPlayerRoundStatusLabel(roundStatus)
          const buzzerKey = playerKeyLabels[player.playerNumber] ?? '—'

          return (
            <li
              key={player.id}
              className={[
                'moderator-player-board__item',
                roundStatus === 'buzzed' ? 'moderator-player-board__item--buzzed' : '',
                roundStatus === 'failed' ? 'moderator-player-board__item--failed' : '',
              ]
                .filter(Boolean)
                .join(' ')}
            >
              <div className="moderator-player-board__avatar" style={{ backgroundColor: player.color }}>
                {player.avatarInitial}
              </div>

              <div className="moderator-player-board__info">
                <div className="moderator-player-board__name-row">
                  <span className="moderator-player-board__name">{player.name}</span>
                  <span className="moderator-player-board__key">{buzzerKey}</span>
                </div>
                <span className="moderator-player-board__score">
                  {player.score.toLocaleString('es-CO')} pts
                </span>
                <span className="moderator-player-board__status">{roundLabel}</span>
              </div>
            </li>
          )
        })}
      </ul>

      <div className="moderator-player-board__legend">
        <p className="moderator-player-board__legend-title">Teclas pulsador</p>
        <div className="moderator-player-board__legend-keys">
          {Object.entries(playerKeyLabels).map(([playerNumber, key]) => (
            <span key={playerNumber} className="moderator-player-board__legend-item">
              J{playerNumber} → {key}
            </span>
          ))}
        </div>
      </div>
    </section>
  )
}
