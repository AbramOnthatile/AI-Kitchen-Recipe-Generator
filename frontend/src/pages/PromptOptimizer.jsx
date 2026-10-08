import { useState } from 'react'
import { api } from '../services/api'

export default function PromptOptimizer() {
  const [original, setOriginal] = useState('Make something with chicken and rice.')
  const [goal, setGoal] = useState('Create a practical beginner recipe.')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const optimize = async () => { setLoading(true); try { setResult(await api.optimizePrompt(original, goal)) } finally { setLoading(false) } }
  return <main className="page-shell"><div className="page-heading"><div><span className="eyebrow">Prompt optimization lab</span><h1>Make prompts work better</h1><p>Compare an original prompt with an AI-assisted optimized version.</p></div></div><div className="optimizer-grid"><section className="panel"><h2>Original Prompt</h2><textarea value={original} onChange={(event) => setOriginal(event.target.value)} /><h2>Optimization Goal</h2><textarea value={goal} onChange={(event) => setGoal(event.target.value)} /><button className="primary" onClick={optimize} disabled={loading}>{loading ? 'Optimizing…' : 'Optimize Prompt'}</button></section>{result && <section className="panel"><h2>Optimized Prompt</h2><div className="score-badge">Prompt Score: {result.score}/100</div><p className="optimized-prompt">{result.optimized}</p><h3>Why it was improved</h3><ul className="check-list">{result.improvements.map((item) => <li key={item}>✓ {item}</li>)}</ul><p className="note">Prompt score is an AI-assisted estimate, not a scientifically validated measure.</p></section>}</div></main>
}
