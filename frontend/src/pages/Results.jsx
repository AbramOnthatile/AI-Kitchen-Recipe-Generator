import { useLocation } from 'react-router-dom'
import { useState } from 'react'

const copyText = async (text) => {
  await navigator.clipboard.writeText(text)
  alert('Copied to clipboard!')
}

export default function Results() {
  const { state } = useLocation()
  const result = state?.result
  const [platform, setPlatform] = useState('Instagram')
  const [tab, setTab] = useState('recipe')

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

  return (
    <main className="page-shell results-page">
      <div className="page-heading">
        <div>
          <span className="eyebrow">Generation complete</span>
          <h1>{recipe.name}</h1>
        </div>
        <span className="mode-badge">{result.local_mode ? 'Local Demo Mode' : 'AI Model Mode'}</span>
      </div>

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
