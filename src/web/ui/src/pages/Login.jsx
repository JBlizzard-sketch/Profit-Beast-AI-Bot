import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { loginWithApiKey } from '../api'

export default function Login(){
  const [apiKey, setApiKey] = useState('')
  const [err, setErr] = useState('')
  const nav = useNavigate()

  async function doLogin(e){
    e.preventDefault()
    try{
      const data = await loginWithApiKey(apiKey)
      localStorage.setItem('alttrade_token', data.token)
      nav('/')
    }catch(err){
      setErr(err.response?.data?.detail || 'Login failed')
    }
  }

  return (
    <div className="max-w-md mx-auto mt-20 bg-white p-6 rounded shadow">
      <h2 className="text-xl mb-4">Admin Login</h2>
      <form onSubmit={doLogin}>
        <label className="block mb-2">API Key</label>
        <input value={apiKey} onChange={e=>setApiKey(e.target.value)} className="w-full p-2 border rounded mb-3"/>
        <button className="w-full p-2 bg-blue-600 text-white rounded">Login</button>
      </form>
      {err && <div className="mt-3 text-red-600">{err}</div>}
    </div>
  )
}
