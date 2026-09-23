import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from 'react'
import { fetchEventConfig } from '../api/client'
import type { EventConfig } from '../types/eventConfig'

interface EventConfigContextValue {
  config: EventConfig | null
  isLoading: boolean
  error: string | null
  refreshConfig: () => Promise<void>
  setConfig: (config: EventConfig) => void
}

const EventConfigContext = createContext<EventConfigContextValue | null>(null)

export function EventConfigProvider({ children }: { children: ReactNode }) {
  const [config, setConfigState] = useState<EventConfig | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const refreshConfig = useCallback(async () => {
    setIsLoading(true)
    setError(null)

    try {
      const loadedConfig = await fetchEventConfig()
      setConfigState(loadedConfig)
    } catch {
      setError('No se pudo cargar la configuración del evento.')
    } finally {
      setIsLoading(false)
    }
  }, [])

  useEffect(() => {
    void refreshConfig()
  }, [refreshConfig])

  const setConfig = useCallback((updatedConfig: EventConfig) => {
    setConfigState(updatedConfig)
  }, [])

  const value = useMemo(
    () => ({
      config,
      isLoading,
      error,
      refreshConfig,
      setConfig,
    }),
    [config, isLoading, error, refreshConfig, setConfig],
  )

  return (
    <EventConfigContext.Provider value={value}>{children}</EventConfigContext.Provider>
  )
}

export function useEventConfig() {
  const context = useContext(EventConfigContext)
  if (!context) {
    throw new Error('useEventConfig debe usarse dentro de EventConfigProvider')
  }
  return context
}
