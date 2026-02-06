import Sidebar from './Sidebar'
import Topbar from './Topbar'

export default function Layout({ title, children }) {
  return (
    <div className="app-shell">
      <Sidebar />
      <div className="app-main">
        <Topbar title={title} />
        <div className="page">{children}</div>
      </div>
    </div>
  )
}
