export default function Header({onAdd}) {
  return (
    <header>
      <div>
        <h1>Dashboard Carbon Card</h1>
        <p>Suivi et impact CO₂ des initiatives locales</p>
      </div>
      <button onClick={onAdd}>Ajouter une action</button>
    </header>
  );
}
