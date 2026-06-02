export default function StatsBar({ present, tardy, absent }) {
  return (
    <div className="stats">
      <div className="stat-card present">
        <div className="label">Present</div>
        <div className="value">{present}</div>
      </div>
      <div className="stat-card tardy">
        <div className="label">Tardy</div>
        <div className="value">{tardy}</div>
      </div>
      <div className="stat-card absent">
        <div className="label">Not Yet In</div>
        <div className="value">{absent}</div>
      </div>
    </div>
  );
}
