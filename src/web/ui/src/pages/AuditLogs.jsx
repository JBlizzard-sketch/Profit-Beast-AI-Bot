import React, {useEffect, useState} from 'react'
import client from '../api'
export default function AuditLogs(){
  const [logs,setLogs]=useState(null)
  useEffect(()=>{ client.get('/admin/audit_logs').then(r=>setLogs(r.data.audit_logs)).catch(()=>setLogs([])) },[])
  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Audit Logs</h1>
      {logs ? logs.map(l=>(<div key={l[0]} className="p-2 bg-white rounded mb-2">{l[2]} {l[4]}</div>)) : <div>Loading...</div>}
    </div>
  )
}
