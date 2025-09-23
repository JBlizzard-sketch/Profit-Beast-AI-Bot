import React, {useState} from 'react'
import client from '../api'
export default function MLTraining(){
  const [res,setRes]=useState(null)
  const retrain = ()=> client.post('/admin/retrain').then(r=>setRes(r.data)).catch(e=>setRes({error:true}))
  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">ML Training</h1>
      <button onClick={retrain} className="px-3 py-1 bg-indigo-600 text-white rounded">Retrain Models</button>
      {res && <pre className="mt-3 bg-white p-3 rounded">{JSON.stringify(res,null,2)}</pre>}
    </div>
  )
}
