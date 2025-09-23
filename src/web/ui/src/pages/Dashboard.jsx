import React, {useEffect, useState} from 'react'
import client from '../api'

export default function Dashboard(){
  const [stats, setStats] = useState(null)
  useEffect(()=>{ client.get('/admin/system_stats').then(r=>setStats(r.data)).catch(()=>setStats(null)) },[])
  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
      {stats ? (
        <div className="grid grid-cols-3 gap-4">
          <div className="p-4 bg-white rounded shadow">Mode: {stats.mode}</div>
          <div className="p-4 bg-white rounded shadow">CPU: {stats.cpu_percent}%</div>
          <div className="p-4 bg-white rounded shadow">Mem: {stats.mem_percent}%</div>
        </div>
      ) : <div>Loading stats...</div>}
    </div>
  )
}
