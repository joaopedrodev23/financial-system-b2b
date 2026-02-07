import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { login as apiLogin, me as apiMe } from '../api/auth'

const AuthContext = createContext(null)
const TOKEN_KEY = 'finance_token'

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem(TOKEN_KEY))
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let active = true

    async function loadUser() {
      if (!token) {
        setLoading(false)
        return
      }
      try {
        const data = await apiMe()
        if (active) {
          setUser(data)
        }
      } catch (error) {
        localStorage.removeItem(TOKEN_KEY)
        if (active) {
          setToken(null)
          setUser(null)
        }
      } finally {
        if (active) {
          setLoading(false)
        }
      }
    }

    loadUser()
    return () => {
      active = false
    }
  }, [token])

  const login = async (email, password) => {
    const data = await apiLogin(email, password)
    localStorage.setItem(TOKEN_KEY, data.access_token)
    setToken(data.access_token)
    const me = await apiMe()
    setUser(me)
  }

  const logout = () => {
    localStorage.removeItem(TOKEN_KEY)
    setToken(null)
    setUser(null)
  }

  const value = useMemo(
    () => ({
      token,
      user,
      loading,
      isAuthenticated: !!token,
      login,
      logout
    }),
    [token, user, loading]
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  return useContext(AuthContext)
}
