import { useEffect, useState } from 'react'
import { api } from '../services/api'

const starterPrompts = [
  { name: 'Recipe Generator', category: 'Recipe', purpose: 'Generates a recipe from kitchen ingredients.', prompt_text: 'Create a recipe using these ingredients: {ingredients}.', variables: ['ingredients'] },
  { name: 'Cooking Instructions', category: 'Cooking', purpose: 'Creates simple beginner-friendly instructions.', prompt_text: 'Translate this recipe into clear numbered steps: {recipe}.', variables: ['recipe'] },
  { name: 'Social Media Post', category: 'Social Media', purpose: 'Creates social content for a recipe.', prompt_text: 'Create a {platform} post for this recipe: {recipe}.', variables: ['platform', 'recipe'] },
]

export default function PromptLibrary() {
  const [prompts, setPrompts] = useState(starterPrompts)
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('All')
  const [editor, setEditor] = useState(null)
  const [message, setMessage] = useState('')

  useEffect(() => { api.getPrompts().then(setPrompts).catch(() => {}) }, [])
  const filtered = prompts.filter((item) => (category === 'All' || item.category === category) && `${item.name} ${item.purpose}`.toLowerCase().includes(search.toLowerCase()))
  const save = async () => {
    const payload = { ...editor, variables: editor.variables || [] }
    if (editor.id) await api.updatePrompt(editor.id, payload)
    else await api.createPrompt(payload)
    setMessage('Prompt saved.')
    setEditor(null)
  }
  const copy = async (prompt) => { await navigator.clipboard.writeText(prompt.prompt_text); setMessage('Prompt copied.') }
  const remove = async (id) => { await api.deletePrompt(id); setPrompts((current) => current.filter((item) => item.id !== id)); setMessage('Prompt deleted.') }
  return <main className="page-shell"><div className="page-heading"><div><span className="eyebrow">Reusable prompt system</span><h1>Prompt Library</h1><p>Search, edit, copy, and reuse structured prompts.</p></div><button className="primary" onClick={() => setEditor({ name: '', category: 'Recipe', purpose: '', prompt_text: '', variables: [] })}>+ Create Prompt</button></div><div className="filters"><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search prompts" /><select value={category} onChange={(event) => setCategory(event.target.value)}><option>All</option><option>Recipe</option><option>Cooking</option><option>Social Media</option></select></div>{message && <div className="alert success">{message}</div>}<div className="prompt-grid">{filtered.map((prompt) => <article className="content-card prompt-card" key={prompt.id || prompt.name}><div className="card-meta"><span>{prompt.category}</span><span>{prompt.purpose}</span></div><h3>{prompt.name}</h3><p>{prompt.prompt_text}</p><div className="card-actions"><button onClick={() => copy(prompt)}>Copy</button><button onClick={() => setEditor(prompt)}>Edit</button><button onClick={() => remove(prompt.id)}>Delete</button></div></article>)}</div>{editor && <section className="panel editor-panel"><h2>{editor.id ? 'Edit prompt' : 'Create custom prompt'}</h2><input value={editor.name} onChange={(event) => setEditor({ ...editor, name: event.target.value })} placeholder="Prompt name" /><select value={editor.category} onChange={(event) => setEditor({ ...editor, category: event.target.value })}><option>Recipe</option><option>Cooking</option><option>Social Media</option></select><textarea value={editor.prompt_text} onChange={(event) => setEditor({ ...editor, prompt_text: event.target.value })} placeholder="Prompt text" /><input value={editor.variables.join(', ')} onChange={(event) => setEditor({ ...editor, variables: event.target.value.split(',').map((value) => value.trim()).filter(Boolean) })} placeholder="Variables, separated by commas" /><button className="primary" onClick={save}>Save Prompt</button></section>}</main>
}
