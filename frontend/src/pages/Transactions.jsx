import { useEffect, useState } from 'react'
import Layout from '../components/Layout'
import { listCategories } from '../api/categories'
import {
  createTransaction,
  deleteTransaction,
  exportTransactions,
  listTransactions,
  updateTransaction
} from '../api/transactions'
import { formatCurrency, formatDate } from '../utils/format'

const emptyForm = {
  date: '',
  type: 'income',
  amount: '',
  description: '',
  category_id: ''
}

export default function Transactions() {
  const [transactions, setTransactions] = useState([])
  const [categories, setCategories] = useState([])
  const [editingId, setEditingId] = useState(null)
  const [filters, setFilters] = useState({
    start_date: '',
    end_date: '',
    type: '',
    category_id: ''
  })
  const [form, setForm] = useState(emptyForm)

  const loadData = async () => {
    const params = {}
    if (filters.start_date) params.start_date = filters.start_date
    if (filters.end_date) params.end_date = filters.end_date
    if (filters.type) params.type = filters.type
    if (filters.category_id) params.category_id = filters.category_id

    const [transactionsData, categoriesData] = await Promise.all([
      listTransactions(params),
      listCategories()
    ])
    setTransactions(transactionsData)
    setCategories(categoriesData)
  }

  useEffect(() => {
    loadData()
  }, [])

  const handleSubmit = async (event) => {
    event.preventDefault()
    const payload = {
      ...form,
      amount: Number(form.amount),
      category_id: form.category_id || null
    }

    if (editingId) {
      await updateTransaction(editingId, payload)
      setEditingId(null)
    } else {
      await createTransaction(payload)
    }

    setForm(emptyForm)
    loadData()
  }

  const handleDelete = async (id) => {
    await deleteTransaction(id)
    loadData()
  }

  const handleEdit = (item) => {
    setEditingId(item.id)
    setForm({
      date: item.date,
      type: item.type,
      amount: String(item.amount),
      description: item.description || '',
      category_id: item.category_id || ''
    })
  }

  const handleCancelEdit = () => {
    setEditingId(null)
    setForm(emptyForm)
  }

  const handleExport = async () => {
    const params = {}
    if (filters.start_date) params.start_date = filters.start_date
    if (filters.end_date) params.end_date = filters.end_date
    if (filters.type) params.type = filters.type
    if (filters.category_id) params.category_id = filters.category_id

    const blob = await exportTransactions(params)
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = 'transacoes.csv'
    link.click()
    window.URL.revokeObjectURL(url)
  }

  return (
    <Layout title="Movimentações">
      <section className="panel">
        <div className="panel-header">
          <h2>{editingId ? 'Editar movimentação' : 'Nova movimentação'}</h2>
          <p>Registre entradas e saídas do caixa.</p>
        </div>
        <form className="form-grid" onSubmit={handleSubmit}>
          <label>
            Data
            <input
              type="date"
              value={form.date}
              onChange={(e) => setForm({ ...form, date: e.target.value })}
              required
            />
          </label>
          <label>
            Tipo
            <select value={form.type} onChange={(e) => setForm({ ...form, type: e.target.value })}>
              <option value="income">Entrada</option>
              <option value="expense">Saída</option>
            </select>
          </label>
          <label>
            Valor
            <input
              type="number"
              step="0.01"
              value={form.amount}
              onChange={(e) => setForm({ ...form, amount: e.target.value })}
              required
            />
          </label>
          <label>
            Categoria
            <select
              value={form.category_id}
              onChange={(e) => setForm({ ...form, category_id: e.target.value })}
            >
              <option value="">Sem categoria</option>
              {categories.map((category) => (
                <option key={category.id} value={category.id}>
                  {category.name}
                </option>
              ))}
            </select>
          </label>
          <label className="full">
            Descrição
            <input
              type="text"
              value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
              placeholder="Ex: Pagamento de cliente"
            />
          </label>
          <div className="form-actions">
            <button className="btn btn-primary" type="submit">
              {editingId ? 'Salvar alterações' : 'Salvar movimentação'}
            </button>
            {editingId && (
              <button className="btn btn-outline" type="button" onClick={handleCancelEdit}>
                Cancelar
              </button>
            )}
          </div>
        </form>
      </section>

      <section className="panel">
        <div className="panel-header">
          <h2>Filtros</h2>
          <p>Escolha um período ou tipo de movimentação.</p>
        </div>
        <div className="filters">
          <label>
            Data inicial
            <input
              type="date"
              value={filters.start_date}
              onChange={(e) => setFilters({ ...filters, start_date: e.target.value })}
            />
          </label>
          <label>
            Data final
            <input
              type="date"
              value={filters.end_date}
              onChange={(e) => setFilters({ ...filters, end_date: e.target.value })}
            />
          </label>
          <label>
            Tipo
            <select value={filters.type} onChange={(e) => setFilters({ ...filters, type: e.target.value })}>
              <option value="">Todos</option>
              <option value="income">Entrada</option>
              <option value="expense">Saída</option>
            </select>
          </label>
          <label>
            Categoria
            <select
              value={filters.category_id}
              onChange={(e) => setFilters({ ...filters, category_id: e.target.value })}
            >
              <option value="">Todas</option>
              {categories.map((category) => (
                <option key={category.id} value={category.id}>
                  {category.name}
                </option>
              ))}
            </select>
          </label>
          <button className="btn btn-outline" type="button" onClick={loadData}>
            Filtrar
          </button>
          <button className="btn btn-outline" type="button" onClick={handleExport}>
            Baixar CSV
          </button>
        </div>
      </section>

      <section className="panel">
        <div className="panel-header">
          <h2>Lista de movimentações</h2>
          <p>Total de movimentações: {transactions.length}</p>
        </div>
        <div className="table">
          <div className="table-row table-head">
            <span>Data</span>
            <span>Tipo</span>
            <span>Descrição</span>
            <span>Valor</span>
            <span>Ação</span>
          </div>
          {transactions.map((item) => (
            <div className="table-row" key={item.id}>
              <span>{formatDate(item.date)}</span>
              <span className={`badge ${item.type}`}>{item.type === 'income' ? 'Entrada' : 'Saída'}</span>
              <span>{item.description || 'Sem descrição'}</span>
              <span>{formatCurrency(item.amount)}</span>
              <div className="table-actions">
                <button className="btn btn-link" type="button" onClick={() => handleEdit(item)}>
                  Editar
                </button>
                <button className="btn btn-link" type="button" onClick={() => handleDelete(item.id)}>
                  Excluir
                </button>
              </div>
            </div>
          ))}
          {!transactions.length && <p className="empty">Nenhuma movimentação encontrada.</p>}
        </div>
      </section>
    </Layout>
  )
}
