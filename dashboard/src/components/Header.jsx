import { useState, useEffect } from "react";

export default function Header({ session, onStart, onStop }) {
  const [now, setNow] = useState(new Date());

  useEffect(() => {
    const id = setInterval(() => setNow(new Date()), 60000); // update every minute
    return () => clearInterval(id);
  }, []);

  const dateStr = now.toLocaleDateString("en-US", {
    weekday: "long", year: "numeric", month: "long", day: "numeric",
  });

  return (
    <div className="header">
      <div className="header-left">
        <h1>Face<span>Check</span></h1>
        <p>{dateStr}</p>
      </div>
      <div className="header-right">
        <div className={`session-badge ${session ? "active" : "inactive"}`}>
          <div className={`dot ${session ? "active" : "inactive"}`} />
          {session ? "Session Active" : "Session Inactive"}
        </div>
        {session
          ? <button className="btn btn-stop"  onClick={onStop}>End Session</button>
          : <button className="btn btn-start" onClick={onStart}>Start Session</button>
        }
      </div>
    </div>
  );
}
