import React, {useEffect, useState} from 'react'
import client from '../api'
export default function MarketplaceAdmin(){
  const [items,setItems]=useState(null)
  useEffect(()=>{ client.get('/admin/marketplace').then(r=>setItems(r.data.marketplace)).catch(()=>setItems([])) },[])
  const approve = (id)=> client.post(`/admin/marketplace/${id}/approve`).then(()=>client.get('/admin/marketplace').then(r=>setItems(r.data.marketplace)))
  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Marketplace Admin</h1>
      {items ? items.map(i=>(<div key={i[0]} className="p-2 bg-white rounded mb-2">{i[2]} - <button onClick={()=>approve(i[0])} className="ml-2 px-2 py-1 bg-green-600 text-white rounded">Approve</button></div>)) : <div>Loading...</div>}
    </div>
  )
}
