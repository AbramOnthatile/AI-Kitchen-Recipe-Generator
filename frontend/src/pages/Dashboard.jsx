import { useEffect, useState } from 'react'
import { api } from '../services/api'

export default function Dashboard() {
  const [history, setHistory] = useState([])
  const [stats, setStats] = useState({})
  useEffect(() => { api.getHistory().then((items) => { setHistory(items); setStats({ generated: items.length, recipes: items.length, posts: items.length, prompts: 3 }) }) }, [])
  return <main className="page-shell"><div className="page-heading"><div><span className="eyebrow">AI productivity dashboard</span><h1>Your kitchen workflow</h1></div></div><div className="stat-grid"><Stat label="Recipes Generated" value={stats.recipes || 0} /><Stat label="Cooking Instructions" value={stats.recipes || 0} /><Stat label="Social Posts" value={stats.posts || 0} /><Stat label="Prompts Optimized" value={stats.prompts || 0} /><Stat label="Prompt Library" value={3} /><Stat label="Recent Activity" value={history.length} /></div><section className="panel"><h2>Recent activity</h2>{history.length ? <div className="activity-list">{history.slice(0, 5).map((item) => <div key={item.id}><strong>{item.recipe?.name || 'Kitchen recipe'}</strong><span>{new Date(item.created_at).toLocaleDateString()}</span></div>)}</div> : <p>No generation history yet.</p>}</section></main>
}

function Stat({ label, value }) { return <article className="stat-card"><span>{label}</span><strong>{value}</strong></article> }
