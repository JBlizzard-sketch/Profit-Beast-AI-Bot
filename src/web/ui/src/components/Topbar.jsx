import React from 'react'
import { useNavigate } from 'react-router-dom'

export default function Topbar(){
  const nav = useNavigate()
  const logout = () => {
    localStorage.removeItem('alttrade_token')
    nav('/login')
  }
  return (
    <div className="flex justify-between items-center mb-4">
      <div><strong>Admin Dashboard</strong></div>
      <div>
        <button onClick={logout} className="px-3 py-1 bg-red-500 text-white rounded">Logout</button>
      </div>
    </div>
  )
}
