export const formatCurrency = (value) => {
  const numeric = Number(value)
  const safeValue = Number.isFinite(numeric) ? numeric : 0
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(safeValue)
}

export const formatDate = (value) => {
  if (!value) return ''
  if (typeof value === 'string' && value.includes('-')) {
    const [year, month, day] = value.split('-')
    return `${day}/${month}/${year}`
  }
  return new Date(value).toLocaleDateString('pt-BR')
}
