import api from './client'

export const getDashboardSummary = async (params) => {
  const { data } = await api.get('/dashboard/summary', { params })
  return data
}
