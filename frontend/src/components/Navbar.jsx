import { Link, NavLink } from 'react-router-dom'

const links = [
  ['Home', '/'], ['Kitchen', '/kitchen'], ['Results', '/results'],
  ['Prompt Library', '/prompts'], ['Optimizer', '/optimizer'], ['History', '/history'], ['About', '/about'],
]

export default function Navbar() {
  return (
    <nav className="nav-shell">
      <Link className="brand" to="/">
        <span className="brand-mark">AI</span><span>Kitchen<span className="brand-accent">Chef</span></span>
      </Link>
      <div className="nav-links">
        {links.map(([label, to]) => <NavLink key={to} to={to}>{label}</NavLink>)}
      </div>
    </nav>
  )
}
