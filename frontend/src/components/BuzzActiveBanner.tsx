import './BuzzActiveBanner.css'

interface BuzzActiveBannerProps {
  message?: string
}

export default function BuzzActiveBanner({
  message = 'PULSADORES ACTIVOS',
}: BuzzActiveBannerProps) {
  return (
    <div className="buzz-active-banner" role="status">
      <span className="buzz-active-banner__icon">⚡</span>
      <span className="buzz-active-banner__text">{message}</span>
    </div>
  )
}
