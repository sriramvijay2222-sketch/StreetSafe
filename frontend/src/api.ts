import type {Report, ReportDraft, Stats, StatusHistory} from './types';
const base=import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
async function call<T>(path:string, init?:RequestInit):Promise<T>{ const r=await fetch(base+path,init); if(!r.ok){const d=await r.json().catch(()=>null); throw new Error(d?.detail || `Request failed (${r.status})`)} return r.json() }
export const api={
  reports:()=>call<Report[]>('/api/reports'),
  stats:()=>call<Stats>('/api/stats'),
  create:(body:ReportDraft)=>call<Report>('/api/reports',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}),
  history:(id:string,key:string)=>call<StatusHistory[]>(`/api/reports/${id}/history`,{headers:{'X-Admin-Key':key}}),
  update:(id:string,body:{status:string;note:string},key:string)=>call<Report>(`/api/reports/${id}/status`,{method:'PATCH',headers:{'Content-Type':'application/json','X-Admin-Key':key},body:JSON.stringify(body)})
};
