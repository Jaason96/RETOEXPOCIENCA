const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export function getWebSocketUrl(gameId: number): string {
  const apiUrl = new URL(API_BASE_URL)
  const protocol = apiUrl.protocol === 'https:' ? 'wss:' : 'ws:'
  return `${protocol}//${apiUrl.host}/ws/games/${gameId}`
}

export type WebSocketListener = (message: import('../types/game').WebSocketMessage) => void

export class GameWebSocketClient {
  private socket: WebSocket | null = null
  private gameId: number | null = null
  private listeners = new Set<WebSocketListener>()
  private reconnectTimer: number | null = null
  private shouldReconnect = true

  connect(gameId: number) {
    this.gameId = gameId
    this.shouldReconnect = true
    this.openConnection()
  }

  disconnect() {
    this.shouldReconnect = false
    if (this.reconnectTimer !== null) {
      window.clearTimeout(this.reconnectTimer)
      this.reconnectTimer = null
    }
    this.socket?.close()
    this.socket = null
    this.listeners.clear()
  }

  send(message: import('../types/game').WebSocketAction) {
    if (this.socket?.readyState !== WebSocket.OPEN) {
      return
    }
    this.socket.send(JSON.stringify(message))
  }

  subscribe(listener: WebSocketListener) {
    this.listeners.add(listener)
    return () => {
      this.listeners.delete(listener)
    }
  }

  private openConnection() {
    if (this.gameId === null) {
      return
    }

    this.socket?.close()
    this.socket = new WebSocket(getWebSocketUrl(this.gameId))

    this.socket.onmessage = (event) => {
      const message = JSON.parse(event.data) as import('../types/game').WebSocketMessage
      this.listeners.forEach((listener) => listener(message))
    }

    this.socket.onclose = () => {
      if (!this.shouldReconnect || this.gameId === null) {
        return
      }
      this.reconnectTimer = window.setTimeout(() => {
        this.openConnection()
      }, 1500)
    }
  }
}
