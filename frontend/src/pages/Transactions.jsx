import { useEffect, useState } from 'react'
import Layout from '../components/Layout'
import { listCategories } from '../api/categories'
import {
  createTransaction,
  deleteTransaction,
  exportTransactions,
  listTransactions
} from '../api/transactions'
import { formatCurrency, formatDate } from '../utils/format'

export default function Transactions() {
  const [transactions, setTransactions] = useState([])
  const [categories, setCategories] = useState([])
  const [filters, setFilters] = useState({
    start_date: '',
    end_date: '',
    type: '',
    category_id: ''
  })
  const [form, setForm] = useState({
    date: '',
    type: 'income',
    amount: '',
    description: '',
    category_id: ''
  })

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
    await createTransaction({
      ...form,
      amount: Number(form.amount),
      category_id: form.category_id || null
    })
    setForm({ date: '', type: 'income', amount: '', description: '', category_id: '' })
    loadData()
  }

  const handleDelete = async (id) => {
    await deleteTransaction(id)
    loadData()
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
    <Layout title="Lançamentos">
      <section className="panel">
        <div className="panel-header">
          <h2>Novo lançamento</h2>
          <p>Registre entradas e saídas financeiras.</p>
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
              Salvar lançamento
            </button>
          </div>
        </form>
      </section>

      <section className="panel">
        <div className="panel-header">
          <h2>Filtros</h2>
          <p>Use para localizar períodos e tipos específicos.</p>
        </div>
        <div className="filters">
          <label>
            Início
            <input
              type="date"
              value={filters.start_date}
              onChange={(e) => setFilters({ ...filters, start_date: e.target.value })}
            />
          </label>
          <label>
            Fim
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
            Aplicar filtros
          </button>
          <button className="btn btn-outline" type="button" onClick={handleExport}>
            Exportar CSV
          </button>
        </div>
      </section>

      <section className="panel">
        <div className="panel-header">
          <h2>Lista de lançamentos</h2>
          <p>Total de registros: {transactions.length}</p>
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
              <button className="btn btn-link" type="button" onClick={() => handleDelete(item.id)}>
                Excluir
              </button>
            </div>
          ))}
          {!transactions.length && <p className="empty">Nenhum lançamento encontrado.</p>}
        </div>
      </section>
    </Layout>
  )
}
