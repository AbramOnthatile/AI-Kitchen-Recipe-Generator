import { useLocation } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { api } from '../services/api'

const copyText = async (text) => {
  await navigator.clipboard.writeText(text)
  alert('Copied to clipboard!')
}

export default function Results() {
  const { state } = useLocation()
  const [result, setResult] = useState(state?.result || null)
  const [platform, setPlatform] = useState('Instagram')
  const [tab, setTab] = useState('recipe')
  const [imageLoading, setImageLoading] = useState(false)
  const [imageError, setImageError] = useState('')

  useEffect(() => {
    if (state?.result) {
      setResult(state.result)
      if (state.result.image?.status === 'error' || state.result.image?.status === 'unavailable') {
        setImageError(state.result.image.error || 'Your recipe is ready, but its image could not be generated. Please try again.')
      } else {
        setImageError('')
      }
    }
  }, [state])

  if (!result) {
    return (
      <main className="empty-state">
        <h1>No recipe generated yet</h1>
        <p>Go to the kitchen page and add your ingredients.</p>
      </main>
    )
  }

  const recipe = result.recipe
  const post = result.social_media_post
  const image = result.image || { status: 'unavailable' }

  const handleRegenerateImage = async () => {
    const recipeId = result.recipe_id || result.history_id
    if (!recipeId) return
    setImageLoading(true)
    setImageError('')
    try {
      const nextImage = await api.regenerateImage(recipeId)
      const nextResult = { ...result, image: nextImage.image }
      setResult(nextResult)
      if (nextImage.image.status === 'success') {
        setImageError('')
      } else {
        setImageError(nextImage.image.error || 'Your recipe is ready, but its image could not be generated. Please try again.')
      }
    } catch (error) {
      setImageError(error.message || 'Your recipe is ready, but its image could not be generated. Please try again.')
    } finally {
      setImageLoading(false)
    }
  }

  return (
    <main className="page-shell results-page">
      <div className="result-hero">
        <div className="image-panel">
          {image.status === 'success' && image.url ? (
            <img src={image.url} alt={recipe.name} className="food-image" />
          ) : imageLoading ? (
            <div className="image-placeholder">Generating image…</div>
          ) : (
            <div className="image-error">
              <strong>Image unavailable</strong>
              <p>{image.error || 'Your recipe is ready, but its image could not be generated. Please try again.'}</p>
            </div>
          )}
        </div>

        <div className="page-heading">
          <div>
            <span className="eyebrow">Generation complete</span>
            <h1>{recipe.name}</h1>
          </div>
          <span className="mode-badge">{result.local_mode ? 'Local Demo Mode' : 'AI Connected'}</span>
          {(image.status === 'error' || image.status === 'unavailable') && (
            <div className="image-actions">
              <button className="primary" onClick={handleRegenerateImage} disabled={imageLoading}>{imageLoading ? 'Generating...' : 'Regenerate Image'}</button>
            </div>
          )}
        </div>
      </div>

      {imageError && <div className="alert error">{imageError}</div>}

      <div className="tabs">
        <button className={tab === 'recipe' ? 'active' : ''} onClick={() => setTab('recipe')}>Recipe</button>
        <button className={tab === 'instructions' ? 'active' : ''} onClick={() => setTab('instructions')}>Cooking Instructions</button>
        <button className={tab === 'post' ? 'active' : ''} onClick={() => setTab('post')}>Social Post</button>
      </div>

      {tab === 'recipe' && (
        <section className="card-grid">
          <article className="content-card wide">
            <span className="card-label">Recipe</span>
            <h2>{recipe.name}</h2>
            <p>{recipe.description}</p>
            <div className="metric-grid">
              <div><small>Servings</small><strong>{recipe.servings}</strong></div>
              <div><small>Preparation</small><strong>{recipe.preparation_time}</strong></div>
              <div><small>Cooking</small><strong>{recipe.cooking_time}</strong></div>
              <div><small>Difficulty</small><strong>{recipe.difficulty}</strong></div>
            </div>
            <div className="match-card">
              <div><span>Ingredient Match</span><strong>{result.match.percentage}%</strong></div>
              <div className="progress"><i style={{ width: `${result.match.percentage}%` }} /></div>
              <p>Available: {result.match.available.join(', ') || 'No direct matches'}</p>
              <p>Missing: {result.match.missing.join(', ') || 'None'}</p>
              <button className="secondary" onClick={() => copyText(JSON.stringify(recipe, null, 2))}>Copy Recipe</button>
            </div>
          </article>
        </section>
      )}

      {tab === 'instructions' && (
        <section className="content-card">
          <span className="card-label">Cooking instructions</span>
          <ol className="steps">
            {result.instructions.map((step, index) => (
              <li key={index}><span>{index + 1}</span><p>{step}</p></li>
            ))}
          </ol>
          <button className="secondary" onClick={() => copyText(result.instructions.join('\n'))}>Copy Instructions</button>
        </section>
      )}

      {tab === 'post' && (
        <section className="content-card">
          <span className="card-label">Social media post</span>
          <div className="platform-picker">
            {['Instagram', 'Facebook', 'LinkedIn', 'X'].map((item) => (
              <button key={item} className={platform === item ? 'active' : ''} onClick={() => setPlatform(item)}>{item}</button>
            ))}
          </div>
          <div className="post-preview">
            <p>{post.text}</p>
            <strong>Call to action</strong>
            <p>{post.call_to_action}</p>
            <div className="hashtags">{post.hashtags.map((tag) => <span key={tag}>{tag}</span>)}</div>
          </div>
          <button className="secondary" onClick={() => copyText(post.text)}>Copy Post</button>
        </section>
      )}
    </main>
  )
}
