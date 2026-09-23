import { useState } from 'react'
import './MascotPlaceholder.css'

interface MascotPlaceholderProps {
  variant?: 'both' | 'neo' | 'esperancita'
  size?: 'small' | 'medium' | 'large'
  className?: string
}

export default function MascotPlaceholder({
  variant = 'both',
  size = 'medium',
  className = '',
}: MascotPlaceholderProps) {
  const [hasError, setHasError] = useState(false)

  if (hasError) {
    return (
      <div
        className={`mascot-placeholder mascot-placeholder--${size} mascot-placeholder--${variant} ${className}`}
        aria-label="Neo y Esperancita"
      >
        {variant !== 'esperancita' && (
          <div className="mascot-placeholder__char mascot-placeholder__char--neo">
            <div className="mascot-placeholder__head" />
            <div className="mascot-placeholder__coat" />
            <span className="mascot-placeholder__name">Neo</span>
          </div>
        )}
        {variant !== 'neo' && (
          <div className="mascot-placeholder__char mascot-placeholder__char--esperancita">
            <div className="mascot-placeholder__head" />
            <div className="mascot-placeholder__coat" />
            <span className="mascot-placeholder__name">Esperancita</span>
          </div>
        )}
        <span className="mascot-placeholder__hint">Neo & Esperancita</span>
      </div>
    )
  }

  return (
    <img
      src="/assets/neo-esperancita.png"
      alt="Neo y Esperancita — mascotas del colegio"
      className={`mascot-img mascot-img--${size} ${className}`}
      onError={() => setHasError(true)}
    />
  )
}
