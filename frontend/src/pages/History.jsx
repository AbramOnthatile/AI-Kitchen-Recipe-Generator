import { useEffect, useState } from 'react'
import { api } from '../services/api'

export default function History() {
  const [items, setItems] = useState([])
  useEffect(() => { api.getHistory().then(setItems) }, [])
  const remove = async (id) => { await api.deleteHistory(id); setItems((current) => current.filter((item) => item.id !== id)) }
  return <main className="page-shell"><div className="page-heading"><div><span className="eyebrow">Generation memory</span><h1>History</h1><p>Review, copy, and regenerate previous kitchen workflows.</p></div></div>{items.length ? <div className="history-list">{items.map((item) => <article className="content-card" key={item.id}><div><span>{new Date(item.created_at).toLocaleString()}</span><h3>{item.recipe?.name || 'Kitchen recipe'}</h3><p>{item.ingredients.join(', ')}</p></div><div className="card-actions"><button onClick={() => navigator.clipboard.writeText(JSON.stringify(item.recipe))}>View</button><button onClick={() => navigator.clipboard.writeText(JSON.stringify(item.recipe))}>Copy</button><button className="danger" onClick={() => remove(item.id)}>Delete</button></div></article>)}</div> : <div className="empty-state"><h2>No history yet</h2><p>Generate a recipe to save it here.</p></div>}</main>
}
