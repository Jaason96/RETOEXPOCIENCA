import './TimerCircle.css'

interface TimerCircleProps {
  remainingSeconds: number
  totalSeconds: number
  size?: number
}

export default function TimerCircle({ remainingSeconds, totalSeconds, size = 90 }: TimerCircleProps) {
  const radius = (size - 8) / 2
  const circumference = 2 * Math.PI * radius
  const progress = totalSeconds > 0 ? remainingSeconds / totalSeconds : 0

  return (
    <div className="timer-circle" style={{ width: size, height: size }}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        <circle
          className="timer-circle__track"
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          strokeWidth="6"
        />
        <circle
          className="timer-circle__progress"
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          strokeWidth="6"
          strokeDasharray={circumference}
          strokeDashoffset={circumference * (1 - progress)}
          transform={`rotate(-90 ${size / 2} ${size / 2})`}
        />
      </svg>
      <span className="timer-circle__value">{remainingSeconds}</span>
    </div>
  )
}
