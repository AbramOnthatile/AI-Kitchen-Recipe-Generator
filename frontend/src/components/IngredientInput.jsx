import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../services/api'

const common = ['Chicken', 'Rice', 'Onion', 'Tomato', 'Garlic', 'Egg', 'Pasta', 'Milk', 'Spinach', 'Potato']

export default function IngredientInput({ onGenerated }) {
  const [ingredients, setIngredients] = useState(['Chicken', 'Rice', 'Onion', 'Tomato'])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const addIngredient = (value) => {
    const clean = value.trim().replace(/\s+/g, ' ')
    if (clean && !ingredients.some((item) => item.toLowerCase() === clean.toLowerCase())) setIngredients((current) => [...current, clean])
    setInput('')
  }

  const handleGenerate = async () => {
    if (!ingredients.length) return setError('Add at least one ingredient first.')
    setLoading(true)
    setError('')
    try {
      const result = await api.generate(ingredients)
      if (typeof onGenerated === 'function') onGenerated(result)
      navigate('/results', { state: { result } })
    } catch (exception) {
      console.error('Recipe generation failed:', exception)
      setError(exception.message || 'Unable to generate a recipe.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="panel kitchen-panel">
      <div className="eyebrow">Kitchen intelligence</div>
      <h2>What's in your kitchen?</h2>
      <p className="lead">Add the ingredients you already have. We will match them with a recipe and create useful content.</p>
      <div className="ingredient-editor">
        <div className="chip-input">
          {ingredients.map((item) => <span className="ingredient-chip" key={item}>{item}<button aria-label={`Remove ${item}`} onClick={() => setIngredients((current) => current.filter((value) => value !== item))}>×</button></span>)}
          <input value={input} onChange={(event) => setInput(event.target.value)} onKeyDown={(event) => event.key === 'Enter' && (event.preventDefault(), addIngredient(input))} placeholder="Add ingredient..." />
        </div>
        <div className="quick-add">{common.map((item) => <button key={item} onClick={() => addIngredient(item)}>{item}+ </button>)}</div>
        <div className="input-actions">
          <button className="secondary" onClick={() => setIngredients([])}>Clear ingredients</button>
          <button className="primary" onClick={handleGenerate} disabled={loading}>{loading ? 'Analyzing your kitchen…' : 'Generate Everything'}</button>
        </div>
        {error && <div className="alert error">{error}</div>}
      </div>
    </section>
  )
}
