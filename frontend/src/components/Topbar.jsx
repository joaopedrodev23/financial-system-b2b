import { useAuth } from '../hooks/useAuth'

export default function Topbar({ title }) {
  const { user, logout } = useAuth()

  return (
    <header className="topbar">
      <div>
        <h1>{title}</h1>
        <p>Controle financeiro rápido e confiável.</p>
      </div>
      <div className="topbar-user">
        <div>
          <strong>{user?.email || 'Usuário'}</strong>
          <small>Conta ativa</small>
        </div>
        <button className="btn btn-outline" onClick={logout} type="button">
          Sair
        </button>
      </div>
    </header>
  )
}
