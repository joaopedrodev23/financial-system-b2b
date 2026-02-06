import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { register as apiRegister } from '../api/auth'
import { useAuth } from '../hooks/useAuth'

export default function Login() {
  const navigate = useNavigate()
  const { login } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [mode, setMode] = useState('login')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError('')
    setLoading(true)
    try {
      if (mode === 'register') {
        await apiRegister(email, password)
      }
      await login(email, password)
      navigate('/')
    } catch (err) {
      setError('Não foi possível autenticar. Verifique os dados.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-layout">
      <div className="auth-card">
        <div className="auth-header">
          <div className="brand-mark">SF</div>
          <div>
            <h1>Sistema Financeiro</h1>
            <p>Controle financeiro operacional para pequenas empresas.</p>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          <label>
            E-mail
            <input
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              placeholder="seu@email.com"
              required
            />
          </label>
          <label>
            Senha
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              placeholder="Mínimo 6 caracteres"
              required
            />
          </label>

          {error && <div className="alert">{error}</div>}

          <button className="btn btn-primary" type="submit" disabled={loading}>
            {mode === 'login' ? 'Entrar' : 'Criar conta'}
          </button>

          <button
            className="btn btn-link"
            type="button"
            onClick={() => setMode(mode === 'login' ? 'register' : 'login')}
          >
            {mode === 'login'
              ? 'Primeiro acesso? Crie sua conta'
              : 'Já tem conta? Fazer login'}
          </button>
        </form>
      </div>
    </div>
  )
}
