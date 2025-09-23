import React, {useEffect, useState} from 'react'
import client from '../api'
export default function Payments(){
  const [payments,setPayments]=useState(null)
  useEffect(()=>{ client.get('/admin/payments').then(r=>setPayments(r.data.payments)).catch(()=>setPayments([])) },[])
  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Payments</h1>
      {payments ? payments.map(p=>(<div key={p.id} className="p-2 bg-white rounded mb-2">{p.id} - {p.status} - {p.amount}</div>)) : <div>Loading...</div>}
    </div>
  )
}
