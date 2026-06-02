function formatTime(isoStr) {
  if (!isoStr) return "—";
  return new Date(isoStr).toLocaleTimeString("en-US", {
    hour: "numeric", minute: "2-digit", hour12: true,
  });
}

function StatusBadge({ status, verified }) {
  if (!verified) return <span className="badge mismatch">Mismatch</span>;
  if (status === "tardy")   return <span className="badge tardy">Tardy</span>;
  return <span className="badge present">Present</span>;
}

export default function AttendanceTable({ records, statusFilter, setStatusFilter, homerooms, homeroom, setHomeroom }) {
  return (
    <div className="panel">
      <div className="panel-header">
        <div>
          <h2>Check-ins Today</h2>
          <div className="subtitle">{records.length} record{records.length !== 1 ? "s" : ""}</div>
        </div>
        <div className="filters">
          {["all", "present", "tardy"].map(f => (
            <button
              key={f}
              className={`filter-btn ${statusFilter === f ? "active" : ""}`}
              onClick={() => setStatusFilter(f)}
            >
              {f.charAt(0).toUpperCase() + f.slice(1)}
            </button>
          ))}
          <select
            className="homeroom-select"
            value={homeroom}
            onChange={e => setHomeroom(e.target.value)}
          >
            <option value="">All Homerooms</option>
            {homerooms.map(h => (
              <option key={h} value={h}>Homeroom {h}</option>
            ))}
          </select>
        </div>
      </div>

      {records.length === 0 ? (
        <div className="empty">No check-ins match the current filter.</div>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Student ID</th>
              <th>Time</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {records.map(r => (
              <tr key={r.id}>
                <td><strong>{r.name}</strong></td>
                <td style={{ color: "#6b7280" }}>{r.studentId}</td>
                <td>{formatTime(r.timestamp)}</td>
                <td><StatusBadge status={r.status} verified={r.verified} /></td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
