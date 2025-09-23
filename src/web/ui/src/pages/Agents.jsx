import React, {useEffect, useState} from 'react'
import client from '../api'

export default function Agents(){
  const [agents, setAgents] = useState(null)
  useEffect(()=>{ client.get('/admin/agents').then(r=>setAgents(r.data.agents)).catch(()=>setAgents([])) },[])
  const startAgent = ()=> client.post('/admin/agent/start', {owner_id:1}).then(()=>client.get('/admin/agents').then(r=>setAgents(r.data.agents)))
  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Agents</h1>
      <button onClick={startAgent} className="px-3 py-1 bg-green-600 text-white rounded mb-4">Start Agent</button>
      {agents ? agents.map(a=>(
        <div key={a.id} className="p-2 bg-white rounded mb-2">{a.id} - {a.status}</div>
      )) : <div>Loading...</div>}
    </div>
  )
}
