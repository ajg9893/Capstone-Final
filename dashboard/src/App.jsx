import { useState, useEffect, useCallback } from "react";
import "./index.css";
import Header from "./components/Header";
import StatsBar from "./components/StatsBar";
import AttendanceTable from "./components/AttendanceTable";
import AbsentList from "./components/AbsentList";

const API = "http://localhost:5000/api";
const POLL_MS = 5000;

export default function App() {
  const [session, setSession]           = useState(false);
  const [stats, setStats]               = useState({ present: 0, tardy: 0 });
  const [records, setRecords]           = useState([]);
  const [absent, setAbsent]             = useState([]);
  const [statusFilter, setStatusFilter] = useState("all");

  // ── Fetch all data ──────────────────────────────────────────────
  const fetchAll = useCallback(async () => {
    try {
      const [sessionRes, statsRes, absentRes] = await Promise.all([
        fetch(`${API}/session`),
        fetch(`${API}/stats`),
        fetch(`${API}/attendance/absent`),
      ]);

      setSession((await sessionRes.json()).active ?? false);
      setStats(await statsRes.json());
      setAbsent(await absentRes.json());
    } catch (err) {
      console.error("Fetch error:", err);
    }
  }, []);

  const fetchRecords = useCallback(async () => {
    try {
      const params = new URLSearchParams();
      if (statusFilter !== "all") params.set("status", statusFilter);

      const res  = await fetch(`${API}/attendance/today?${params}`);
      const data = await res.json();
      setRecords(data);
    } catch (err) {
      console.error("Fetch records error:", err);
    }
  }, [statusFilter]);

  // ── Poll every 5 seconds ────────────────────────────────────────
  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchAll();
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchRecords();
    const id = setInterval(() => { fetchAll(); fetchRecords(); }, POLL_MS);
    return () => clearInterval(id);
  }, [fetchAll, fetchRecords]);

  // ── Session controls ────────────────────────────────────────────
  const startSession = async () => {
    await fetch(`${API}/session/start`, { method: "POST" });
    setSession(true);
  };

  const stopSession = async () => {
    await fetch(`${API}/session/stop`, { method: "POST" });
    setSession(false);
  };

  return (
    <div className="app">
      <Header session={session} onStart={startSession} onStop={stopSession} />

      <StatsBar
        present={stats.present}
        tardy={stats.tardy}
        absent={absent.length}
      />

      <AttendanceTable
        records={records}
        statusFilter={statusFilter}
        setStatusFilter={setStatusFilter}
      />

      <AbsentList students={absent} />
    </div>
  );
}
