import React from 'react'
import { Link, useLocation } from 'react-router-dom'

const items = [
  {to:'/', label:'Dashboard'},
  {to:'/users', label:'Users'},
  {to:'/strategies', label:'Strategies'},
  {to:'/agents', label:'Agents'},
  {to:'/audit', label:'Audit Logs'},
  {to:'/payments', label:'Payments'},
  {to:'/broadcast', label:'Broadcast'},
  {to:'/marketplace', label:'Marketplace'},
  {to:'/sandbox', label:'Sandbox'},
  {to:'/ml', label:'ML Training'},
  {to:'/stats', label:'System Stats'}
]

export default function Sidebar(){
  const loc = useLocation()
  return (
    <div className="sidebar">
      <h2 className="text-xl font-bold mb-4">AltTrade Admin</h2>
      <nav>
        {items.map(i => (
          <div key={i.to} className={`mb-2 ${loc.pathname===i.to ? 'font-semibold' : ''}`}>
            <Link to={i.to}>{i.label}</Link>
          </div>
        ))}
      </nav>
    </div>
  )
}
