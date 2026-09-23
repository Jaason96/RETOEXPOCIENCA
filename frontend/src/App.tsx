import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import WelcomeScreen from './screens/WelcomeScreen'
import PlayerSetupScreen from './screens/PlayerSetupScreen'
import GamePlayRoute from './screens/GamePlayRoute'
import QuestionsBankScreen from './screens/QuestionsBankScreen'
import QuestionFormScreen from './screens/QuestionFormScreen'

import QuestionSetFormScreen from './screens/QuestionSetFormScreen'
import EventConfigScreen from './screens/EventConfigScreen'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<WelcomeScreen />} />
        <Route path="/setup" element={<PlayerSetupScreen />} />
        <Route path="/event-config" element={<EventConfigScreen />} />
        <Route path="/questions" element={<QuestionsBankScreen />} />
        <Route path="/questions/new" element={<QuestionFormScreen />} />
        <Route path="/questions/sets/new" element={<QuestionSetFormScreen />} />
        <Route path="/questions/sets/:questionSetId/edit" element={<QuestionSetFormScreen />} />
        <Route path="/questions/:questionId/edit" element={<QuestionFormScreen />} />
        <Route path="/game/:gameId/play" element={<GamePlayRoute />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
