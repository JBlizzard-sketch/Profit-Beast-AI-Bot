import React, {useEffect, useState} from 'react'
import client from '../api'
export default function SystemStats(){
  const [stats,setStats]=useState(null)
  useEffect(()=>{ client.get('/admin/system_stats').then(r=>setStats(r.data)).catch(()=>setStats(null)) },[])
  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">System Stats</h1>
      {stats ? <div className="p-3 bg-white rounded">CPU: {stats.cpu_percent}%, Mem: {stats.mem_percent}%</div> : <div>Loading...</div>}
    </div>
  )
}
