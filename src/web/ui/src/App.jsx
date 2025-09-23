import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Users from './pages/Users'
import Strategies from './pages/Strategies'
import Agents from './pages/Agents'
import AuditLogs from './pages/AuditLogs'
import Payments from './pages/Payments'
import Broadcast from './pages/Broadcast'
import MarketplaceAdmin from './pages/MarketplaceAdmin'
import Sandbox from './pages/Sandbox'
import MLTraining from './pages/MLTraining'
import SystemStats from './pages/SystemStats'
import ProtectedRoute from './components/ProtectedRoute'
import Sidebar from './components/Sidebar'
import Topbar from './components/Topbar'

function App(){
  return (
    <div className="flex">
      <Sidebar />
      <div className="content">
        <Topbar />
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<ProtectedRoute><Dashboard/></ProtectedRoute>} />
          <Route path="/users" element={<ProtectedRoute><Users/></ProtectedRoute>} />
          <Route path="/strategies" element={<ProtectedRoute><Strategies/></ProtectedRoute>} />
          <Route path="/agents" element={<ProtectedRoute><Agents/></ProtectedRoute>} />
          <Route path="/audit" element={<ProtectedRoute><AuditLogs/></ProtectedRoute>} />
          <Route path="/payments" element={<ProtectedRoute><Payments/></ProtectedRoute>} />
          <Route path="/broadcast" element={<ProtectedRoute><Broadcast/></ProtectedRoute>} />
          <Route path="/marketplace" element={<ProtectedRoute><MarketplaceAdmin/></ProtectedRoute>} />
          <Route path="/sandbox" element={<ProtectedRoute><Sandbox/></ProtectedRoute>} />
          <Route path="/ml" element={<ProtectedRoute><MLTraining/></ProtectedRoute>} />
          <Route path="/stats" element={<ProtectedRoute><SystemStats/></ProtectedRoute>} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </div>
  )
}
export default App
