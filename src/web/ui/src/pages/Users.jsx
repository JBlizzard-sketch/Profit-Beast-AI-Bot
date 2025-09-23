import React, {useEffect, useState} from 'react'
import client from '../api'

export default function Users(){
  const [users, setUsers] = useState(null)
  useEffect(()=>{ client.get('/admin/users').then(r=>setUsers(r.data.users)).catch(()=>setUsers([])) },[])
  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Users</h1>
      {users ? users.length ? (
        <table className="min-w-full bg-white">
          <thead><tr><th>ID</th><th>Username</th><th>Created</th></tr></thead>
          <tbody>
            {users.map(u=>(<tr key={u[0]}><td>{u[0]}</td><td>{u[1]}</td><td>{u[2]}</td></tr>))}
          </tbody>
        </table>
      ) : <div>No users</div> : <div>Loading...</div>}
    </div>
  )
}
