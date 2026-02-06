import { useEffect, useState } from 'react'
import Layout from '../components/Layout'
import { createCategory, deleteCategory, listCategories } from '../api/categories'

export default function Categories() {
  const [categories, setCategories] = useState([])
  const [form, setForm] = useState({ name: '', type: 'income' })

  const loadData = async () => {
    const data = await listCategories()
    setCategories(data)
  }

  useEffect(() => {
    loadData()
  }, [])

  const handleSubmit = async (event) => {
    event.preventDefault()
    await createCategory(form)
    setForm({ name: '', type: 'income' })
    loadData()
  }

  const handleDelete = async (id) => {
    await deleteCategory(id)
    loadData()
  }

  return (
    <Layout title="Categorias">
      <section className="panel">
        <div className="panel-header">
          <h2>Nova categoria</h2>
          <p>Organize seus lançamentos financeiros.</p>
        </div>
        <form className="form-grid" onSubmit={handleSubmit}>
          <label>
            Nome
            <input
              type="text"
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              required
            />
          </label>
          <label>
            Tipo
            <select value={form.type} onChange={(e) => setForm({ ...form, type: e.target.value })}>
              <option value="income">Entrada</option>
              <option value="expense">Saída</option>
              <option value="both">Ambos</option>
            </select>
          </label>
          <div className="form-actions">
            <button className="btn btn-primary" type="submit">
              Salvar categoria
            </button>
          </div>
        </form>
      </section>

      <section className="panel">
        <div className="panel-header">
          <h2>Categorias cadastradas</h2>
          <p>Total: {categories.length}</p>
        </div>
        <div className="table">
          <div className="table-row table-head">
            <span>Nome</span>
            <span>Tipo</span>
            <span>Ação</span>
          </div>
          {categories.map((category) => (
            <div className="table-row" key={category.id}>
              <span>{category.name}</span>
              <span>{category.type === 'income' ? 'Entrada' : category.type === 'expense' ? 'Saída' : 'Ambos'}</span>
              <button className="btn btn-link" type="button" onClick={() => handleDelete(category.id)}>
                Excluir
              </button>
            </div>
          ))}
          {!categories.length && <p className="empty">Nenhuma categoria encontrada.</p>}
        </div>
      </section>
    </Layout>
  )
}
