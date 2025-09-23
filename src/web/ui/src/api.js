import axios from 'axios'

const API_BASE = '/'

function getToken(){
  return localStorage.getItem('alttrade_token')
}

const client = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
})

client.interceptors.request.use(config => {
  const token = getToken()
  if(token){
    config.headers['Authorization'] = `Bearer ${token}`
  }
  return config
})

export async function loginWithApiKey(apiKey){
  // sends X-API-KEY header for login
  const resp = await client.post('/admin/login', {}, { headers: { 'X-API-KEY': apiKey }})
  return resp.data
}

export async function fetchUsers(){
  const resp = await client.get('/admin/users', { params: { api_key: '' }})
  return resp.data
}

export default client
