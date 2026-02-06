import { NavLink } from 'react-router-dom'

export default function Sidebar() {
  const linkClass = ({ isActive }) => (isActive ? 'active' : '')

  return (
    <aside className="sidebar">
      <div className="brand">
        <span className="brand-mark">SF</span>
        <div>
          <strong>Sistema Financeiro</strong>
          <small>Gestão simples</small>
        </div>
      </div>

      <nav className="nav">
        <NavLink to="/" end className={linkClass}>
          Dashboard
        </NavLink>
        <NavLink to="/transactions" className={linkClass}>
          Lançamentos
        </NavLink>
        <NavLink to="/categories" className={linkClass}>
          Categorias
        </NavLink>
      </nav>

      <div className="sidebar-footer">
        <p>Versão 1.0</p>
      </div>
    </aside>
  )
}
