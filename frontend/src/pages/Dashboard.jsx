import { useEffect, useState } from 'react'
import Layout from '../components/Layout'
import Card from '../components/Card'
import { getDashboardSummary } from '../api/dashboard'
import { listTransactions } from '../api/transactions'
import { formatCurrency, formatDate } from '../utils/format'

export default function Dashboard() {
  const [summary, setSummary] = useState(null)
  const [transactions, setTransactions] = useState([])
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')

  const loadData = async () => {
    const params = {}
    if (startDate) params.start_date = startDate
    if (endDate) params.end_date = endDate

    const [summaryData, transactionsData] = await Promise.all([
      getDashboardSummary(params),
      listTransactions(params)
    ])

    setSummary(summaryData)
    setTransactions(transactionsData.slice(0, 5))
  }

  useEffect(() => {
    loadData()
  }, [])

  return (
    <Layout title="Dashboard">
      <section className="filters">
        <div>
          <label>
            Início
            <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
          </label>
        </div>
        <div>
          <label>
            Fim
            <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
          </label>
        </div>
        <button className="btn btn-outline" type="button" onClick={loadData}>
          Atualizar
        </button>
      </section>

      <section className="cards-grid">
        <Card title="Total de entradas" value={formatCurrency(summary?.total_income || 0)} tone="positive" />
        <Card title="Total de saídas" value={formatCurrency(summary?.total_expense || 0)} tone="negative" />
        <Card title="Saldo" value={formatCurrency(summary?.balance || 0)} tone="neutral" />
      </section>

      <section className="panel">
        <div className="panel-header">
          <h2>Últimos lançamentos</h2>
          <p>Acompanhe as movimentações mais recentes.</p>
        </div>
        <div className="table">
          <div className="table-row table-head">
            <span>Data</span>
            <span>Tipo</span>
            <span>Descrição</span>
            <span>Valor</span>
          </div>
          {transactions.map((item) => (
            <div className="table-row" key={item.id}>
              <span>{formatDate(item.date)}</span>
              <span className={`badge ${item.type}`}>{item.type === 'income' ? 'Entrada' : 'Saída'}</span>
              <span>{item.description || 'Sem descrição'}</span>
              <span>{formatCurrency(item.amount)}</span>
            </div>
          ))}
          {!transactions.length && <p className="empty">Nenhum lançamento encontrado.</p>}
        </div>
      </section>
    </Layout>
  )
}
