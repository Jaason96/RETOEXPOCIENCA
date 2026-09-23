import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'
import { EventConfigProvider } from './context/EventConfigContext'
import './styles/global.css'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <EventConfigProvider>
      <App />
    </EventConfigProvider>
  </StrictMode>,
)
