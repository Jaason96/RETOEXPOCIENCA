import './BuzzBanner.css'

interface BuzzBannerProps {
  playerName: string
}

export default function BuzzBanner({ playerName }: BuzzBannerProps) {
  return (
    <div className="buzz-banner" role="status">
      <div className="buzz-banner__glow" />
      <div className="buzz-banner__content">
        <span className="buzz-banner__icon">⚡</span>
        <span className="buzz-banner__text">
          ¡{playerName.toUpperCase()} PULSÓ PRIMERO!
        </span>
        <span className="buzz-banner__icon">⚡</span>
      </div>
    </div>
  )
}
