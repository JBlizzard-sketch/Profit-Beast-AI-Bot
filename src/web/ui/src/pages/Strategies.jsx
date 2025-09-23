import React, {useEffect, useState} from 'react'
import client from '../api'

export default function Strategies(){
  const [items, setItems] = useState(null)
  useEffect(()=>{ client.get('/admin/strategies').then(r=>setItems(r.data.strategies)).catch(()=>setItems([])) },[])
  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Strategies</h1>
      {items ? items.length ? items.map(s=>(
        <div key={s[0]} className="p-3 bg-white rounded mb-2">{s[2]} by {s[1]} ({s[3]})</div>
      )) : <div>No strategies</div> : <div>Loading...</div>}
    </div>
  )
}
