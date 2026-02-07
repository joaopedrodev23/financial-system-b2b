import { useEffect, useRef, useState } from 'react'
import Layout from '../components/Layout'
import { createCategory, deleteCategory, listCategories, updateCategory } from '../api/categories'

const emptyForm = { name: '', type: 'income' }

export default function Categories() {
  const isMounted = useRef(true)
  const [categories, setCategories] = useState([])
  const [form, setForm] = useState(emptyForm)
  const [editingId, setEditingId] = useState(null)

  const loadData = async () => {
    try {
      const data = await listCategories()
      if (!isMounted.current) return
      setCategories(data)
    } catch (error) {
      console.error('Falha ao carregar categorias.', error)
    }
  }

  useEffect(() => {
    loadData()
    return () => {
      isMounted.current = false
    }
  }, [])

  const handleSubmit = async (event) => {
    event.preventDefault()
    if (editingId) {
      await updateCategory(editingId, form)
      setEditingId(null)
    } else {
      await createCategory(form)
    }
    setForm(emptyForm)
    loadData()
  }

  const handleDelete = async (id) => {
    await deleteCategory(id)
    loadData()
  }

  const handleEdit = (category) => {
    setEditingId(category.id)
    setForm({ name: category.name, type: category.type })
  }

  const handleCancelEdit = () => {
    setEditingId(null)
    setForm(emptyForm)
  }

  return (
    <Layout title="Categorias">
      <section className="panel">
        <div className="panel-header">
          <h2>{editingId ? 'Editar categoria' : 'Nova categoria'}</h2>
          <p>Organize suas movimentações por tipo.</p>
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
              {editingId ? 'Salvar alterações' : 'Salvar categoria'}
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
          <h2>Categorias salvas</h2>
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
              <div className="table-actions">
                <button className="btn btn-link" type="button" onClick={() => handleEdit(category)}>
                  Editar
                </button>
                <button className="btn btn-link" type="button" onClick={() => handleDelete(category.id)}>
                  Excluir
                </button>
              </div>
            </div>
          ))}
          {!categories.length && <p className="empty">Nenhuma categoria encontrada.</p>}
        </div>
      </section>
    </Layout>
  )
}
