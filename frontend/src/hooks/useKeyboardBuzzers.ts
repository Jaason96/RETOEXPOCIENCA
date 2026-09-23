import { useEffect, useMemo } from 'react'
import { useModeratorActions } from '../context/GameSessionContext'
import { useEventConfig } from '../context/EventConfigContext'
import { DEFAULT_PLAYER_KEY_CODES } from '../constants/gameConstants'
import type { GameDetail } from '../types/game'

interface UseKeyboardBuzzersOptions {
  game: GameDetail | null
  enabled: boolean
}

export function useKeyboardBuzzers({ game, enabled }: UseKeyboardBuzzersOptions) {
  const { registerBuzz } = useModeratorActions()
  const { config } = useEventConfig()

  // event.code (posición física de la tecla) en vez de event.key: no depende
  // del layout de teclado y sí puede distinguir ControlLeft de ControlRight,
  // necesario para dejar configurar teclas como Ctrl o Alt.
  const playerNumberByKeyCode = useMemo<Record<string, number>>(
    () => ({
      [config?.player_1_key ?? DEFAULT_PLAYER_KEY_CODES[1]]: 1,
      [config?.player_2_key ?? DEFAULT_PLAYER_KEY_CODES[2]]: 2,
      [config?.player_3_key ?? DEFAULT_PLAYER_KEY_CODES[3]]: 3,
      [config?.player_4_key ?? DEFAULT_PLAYER_KEY_CODES[4]]: 4,
    }),
    [config],
  )

  useEffect(() => {
    if (!enabled || !game) {
      return
    }

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.repeat) {
        return
      }

      const target = event.target as HTMLElement | null
      if (
        target &&
        (target.tagName === 'INPUT' ||
          target.tagName === 'TEXTAREA' ||
          target.isContentEditable)
      ) {
        return
      }

      if (game.status !== 'BUZZ_OPEN') {
        return
      }

      const playerNumber = playerNumberByKeyCode[event.code]
      if (!playerNumber) {
        return
      }

      const playerExists = game.players.some(
        (player) => player.player_number === playerNumber,
      )
      if (!playerExists) {
        return
      }

      const player = game.players.find(
        (currentPlayer) => currentPlayer.player_number === playerNumber,
      )
      if (!player || game.failed_player_ids.includes(player.id)) {
        return
      }

      event.preventDefault()
      registerBuzz(playerNumber)
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [enabled, game, registerBuzz, playerNumberByKeyCode])
}
