import { useNavigate } from 'react-router-dom'
import LogoPlaceholder from '../components/LogoPlaceholder'
import ScienceDecorations from '../components/ScienceDecorations'
import { EVENT_NAME, INSTITUTION_NAME } from '../constants/eventIdentity'
import './WelcomeScreen.css'

interface WelcomeScreenProps {
  onStart?: () => void
}

export default function WelcomeScreen({ onStart }: WelcomeScreenProps) {
  const navigate = useNavigate()

  const handleStart = () => {
    if (onStart) {
      onStart()
      return
    }
    navigate('/setup')
  }

  return (
    <div className="welcome-screen">
      <ScienceDecorations />

      <div className="welcome-screen__content">
        <div className="welcome-screen__logo">
          <LogoPlaceholder size="large" />
        </div>

        <h1 className="welcome-screen__title">{EVENT_NAME.toUpperCase()}</h1>
        <p className="welcome-screen__school">{INSTITUTION_NAME}</p>
        <p className="welcome-screen__tagline">¡Demuestra cuánto aprendiste!</p>

        <div className="welcome-screen__mascots">
          <img
            src="/assets/neo-esperancita-full.png"
            alt="Neo y Esperancita, mascotas de Expociencia"
            className="welcome-screen__mascots-image"
          />
        </div>

        <button type="button" className="welcome-screen__btn" onClick={handleStart}>
          INICIAR DESAFÍO
        </button>

        <button
          type="button"
          className="welcome-screen__config-btn"
          onClick={() => navigate('/event-config')}
        >
          ⚙ CONFIGURAR EVENTO
        </button>

        <button
          type="button"
          className="welcome-screen__config-btn"
          onClick={() => navigate('/questions')}
        >
          📚 CONFIGURAR PREGUNTAS
        </button>
      </div>
    </div>
  )
}
