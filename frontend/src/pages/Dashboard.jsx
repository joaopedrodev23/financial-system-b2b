import { useEffect, useRef, useState } from 'react'
import Layout from '../components/Layout'
import Card from '../components/Card'
import { getDashboardSummary } from '../api/dashboard'
import { listTransactions } from '../api/transactions'
import { formatCurrency, formatDate } from '../utils/format'

export default function Dashboard() {
  const isMounted = useRef(true)
  const [summary, setSummary] = useState(null)
  const [transactions, setTransactions] = useState([])
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')

  const loadData = async () => {
    try {
      const params = {}
      if (startDate) params.start_date = startDate
      if (endDate) params.end_date = endDate

      const [summaryData, transactionsData] = await Promise.all([
        getDashboardSummary(params),
        listTransactions(params)
      ])

      if (!isMounted.current) return
      setSummary(summaryData)
      setTransactions(transactionsData.slice(0, 5))
    } catch (error) {
      console.error('Falha ao carregar dados do dashboard.', error)
    }
  }

  useEffect(() => {
    loadData()
    return () => {
      isMounted.current = false
    }
  }, [])

  return (
    <Layout title="Resumo">
      <section className="filters">
        <div>
          <label>
            Data inicial
            <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
          </label>
        </div>
        <div>
          <label>
            Data final
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
          <h2>Últimas movimentações</h2>
          <p>Veja as entradas e saídas mais recentes.</p>
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
          {!transactions.length && <p className="empty">Nenhuma movimentação encontrada.</p>}
        </div>
      </section>
    </Layout>
  )
}
