export default function AbsentList({ students }) {
  return (
    <div className="panel">
      <div className="panel-header">
        <div>
          <h2>Not Yet Checked In</h2>
          <div className="subtitle">{students.length} student{students.length !== 1 ? "s" : ""} absent</div>
        </div>
      </div>
      {students.length === 0 ? (
        <div className="empty">Everyone is accounted for.</div>
      ) : (
        <div className="absent-grid">
          {students.map(s => (
            <div key={s.id} className="absent-chip">
              <span>{s.name}</span> · {s.homeroom}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
