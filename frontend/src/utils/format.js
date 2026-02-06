export const formatCurrency = (value) =>
  new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(Number(value))

export const formatDate = (value) => {
  if (!value) return ''
  if (typeof value === 'string' && value.includes('-')) {
    const [year, month, day] = value.split('-')
    return `${day}/${month}/${year}`
  }
  return new Date(value).toLocaleDateString('pt-BR')
}
