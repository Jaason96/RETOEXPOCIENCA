import { useState } from 'react'
import './LogoPlaceholder.css'

interface LogoPlaceholderProps {
  size?: 'small' | 'medium' | 'large'
  className?: string
}

export default function LogoPlaceholder({ size = 'medium', className = '' }: LogoPlaceholderProps) {
  const [hasError, setHasError] = useState(false)

  if (hasError) {
    return (
      <div className={`logo-placeholder logo-placeholder--${size} ${className}`} aria-label="Logo del colegio">
        <div className="logo-placeholder__shield">
          <span className="logo-placeholder__text">CNE</span>
        </div>
        <span className="logo-placeholder__label">Logo del colegio</span>
      </div>
    )
  }

  return (
    <img
      src="/assets/logo-expociencia.png"
      alt="Colegio La Nueva Esperanza"
      className={`logo-img logo-img--${size} ${className}`}
      onError={() => setHasError(true)}
    />
  )
}
