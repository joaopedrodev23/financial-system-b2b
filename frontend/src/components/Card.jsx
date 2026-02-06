export default function Card({ title, value, tone }) {
  return (
    <div className={`card ${tone || ''}`.trim()}>
      <span>{title}</span>
      <strong>{value}</strong>
    </div>
  )
}
