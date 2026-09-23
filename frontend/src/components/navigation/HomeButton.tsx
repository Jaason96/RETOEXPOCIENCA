import { useNavigate } from 'react-router-dom'
import './HomeButton.css'

interface HomeButtonProps {
  className?: string
}

export default function HomeButton({ className = '' }: HomeButtonProps) {
  const navigate = useNavigate()

  return (
    <button
      type="button"
      className={`home-button ${className}`.trim()}
      onClick={() => navigate('/')}
    >
      <span className="home-button__icon" aria-hidden="true">
        🏠
      </span>
      Inicio
    </button>
  )
}
