import api from './client'

export const listTransactions = async (params) => {
  const { data } = await api.get('/transactions', { params })
  return data
}

export const createTransaction = async (payload) => {
  const { data } = await api.post('/transactions', payload)
  return data
}

export const updateTransaction = async (id, payload) => {
  const { data } = await api.put(`/transactions/${id}`, payload)
  return data
}

export const deleteTransaction = async (id) => {
  await api.delete(`/transactions/${id}`)
}

export const exportTransactions = async (params) => {
  const response = await api.get('/transactions/export', {
    params,
    responseType: 'blob'
  })
  return response.data
}
