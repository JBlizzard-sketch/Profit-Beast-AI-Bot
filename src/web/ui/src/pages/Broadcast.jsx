import React, {useState} from 'react'
import client from '../api'
export default function Broadcast(){
  const [msg,setMsg]=useState('')
  const [res,setRes]=useState(null)
  const send = ()=> client.post('/admin/broadcast', {message: msg}).then(r=>setRes(r.data)).catch(e=>setRes({error:true}))
  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Broadcast</h1>
      <textarea value={msg} onChange={e=>setMsg(e.target.value)} className="w-full p-2 border rounded mb-2" rows={4}/>
      <button onClick={send} className="px-3 py-2 bg-blue-600 text-white rounded">Send Broadcast</button>
      {res && <div className="mt-3 p-2 bg-white rounded">{JSON.stringify(res)}</div>}
    </div>
  )
}
