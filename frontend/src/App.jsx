import { Link, Route, Routes } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Kitchen from './pages/Kitchen'
import Results from './pages/Results'
import PromptLibrary from './pages/PromptLibrary'
import PromptOptimizer from './pages/PromptOptimizer'
import History from './pages/History'
import Dashboard from './pages/Dashboard'
import About from './pages/About'

export default function App() {
  return (
    <div className="app-shell">
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/kitchen" element={<Kitchen />} />
        <Route path="/results" element={<Results />} />
        <Route path="/prompts" element={<PromptLibrary />} />
        <Route path="/optimizer" element={<PromptOptimizer />} />
        <Route path="/history" element={<History />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/about" element={<About />} />
        <Route path="*" element={<main className="empty-state"><h1>Page not found</h1><Link className="primary" to="/">Return home</Link></main>} />
      </Routes>
      <footer>
        <span>AI Kitchen Recipe Generator</span>
        <span>Built for creative, practical AI workflows.</span>
      </footer>
    </div>
  )
}
