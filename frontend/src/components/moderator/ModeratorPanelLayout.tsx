import type { ReactNode } from 'react'
import './ModeratorPanelLayout.css'

interface ModeratorPanelLayoutProps {
  statusBar: ReactNode
  playerBoard: ReactNode
  actionBar: ReactNode
  children: ReactNode
}

export default function ModeratorPanelLayout({
  statusBar,
  playerBoard,
  actionBar,
  children,
}: ModeratorPanelLayoutProps) {
  return (
    <div className="moderator-panel">
      {statusBar}
      <div className="moderator-panel__body">
        <aside className="moderator-panel__sidebar">{playerBoard}</aside>
        <main className="moderator-panel__main">{children}</main>
      </div>
      {actionBar}
    </div>
  )
}
