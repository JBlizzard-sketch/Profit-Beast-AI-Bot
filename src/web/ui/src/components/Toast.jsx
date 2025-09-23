import React from 'react'
export default function Toast({msg}){ return msg ? <div className="fixed bottom-4 right-4 bg-black text-white p-3 rounded">{msg}</div> : null }
