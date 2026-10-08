import { Link } from 'react-router-dom'

export default function Home() {
  return (
    <main className="home-hero">
      <section className="hero-copy">
        <div className="eyebrow">Prompt engineering · recipe intelligence · AI productivity</div>
        <h1>Turn your kitchen ingredients <span>into ideas.</span></h1>
        <p>Enter what you have in your kitchen and let AI create a recipe, cooking instructions, and social media content—without an API key in your browser.</p>
        <div className="hero-actions"><Link className="primary large" to="/kitchen">Start Cooking →</Link><Link className="text-link" to="/about">How it works</Link></div>
        <div className="feature-row"><span>✓ Ingredient matching</span><span>✓ Prompt library</span><span>✓ Local demo mode</span></div>
      </section>
      <section className="hero-visual">
        <div className="food-orbit"><span>🥕</span><span>🥕</span><span>🌿</span></div>
        <div className="ai-card"><div className="ai-card-top"><span>AI Recipe Studio</span><span className="live-dot">Live</span></div><h3>Chicken • Rice • Tomato</h3><div className="match-meter"><span>Ingredient match</span><strong>100%</strong><div><i /></div></div><div className="mini-steps"><span>✓ Recipe generated</span><span>✓ Instructions created</span><span>✓ Post prepared</span></div></div>
      </section>
    </main>
  )
}
