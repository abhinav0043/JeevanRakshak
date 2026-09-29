import {createContext,useContext,useEffect,useState,ReactNode,useRef} from 'react';
import type {State,Event} from '../types';
export async function api(path:string,body?:unknown){
 const r=await fetch('/api/'+path,{method:body===undefined?'GET':'POST',headers:{'Content-Type':'application/json'},body:body===undefined?undefined:JSON.stringify(body)});
 if(!r.ok){const e=await r.json().catch(()=>({detail:r.statusText}));throw Error(typeof e.detail==='string'?e.detail:JSON.stringify(e.detail));}return r.json();
}
export type Sample={time:string;heart_rate?:number|null;spo2?:number|null;temperature?:number|null;humidity?:number|null;mq4?:number|null;mq135?:number|null;[key:string]:string|number|null|undefined};
const Context=createContext<{state:State|null;connected:boolean;error:string;history:Record<string,Sample[]>}>({state:null,connected:false,error:'',history:{}});
export function LiveProvider({children}:{children:ReactNode}){
 const [state,setState]=useState<State|null>(null),[connected,setConnected]=useState(false),[error,setError]=useState(''),[history,setHistory]=useState<Record<string,Sample[]>>({});
 const mission=useRef('');
 useEffect(()=>{let alive=true,ws:WebSocket,timer:ReturnType<typeof setTimeout>,attempt=0;
 const ingest=(e:Event)=>{if(e.type==='event.batch'){(e.payload as Event[]).forEach(ingest);return;}if(e.type==='system.snapshot'){
 const s=e.payload as State;
 setState(prev=>({...s,map:{...s.map,cloud:s.map.cloud??(prev?.mission_id===s.mission_id?prev.map.cloud:[])}}));
 const reset=mission.current!==s.mission_id;mission.current=s.mission_id;
 setHistory(prev=>{const out:Record<string,Sample[]>={...(reset?{}:prev)};const time=new Date(s.timestamp).toLocaleTimeString();
 s.workers.forEach(w=>{out[w.worker_id]=[...(out[w.worker_id]||[]),{time,heart_rate:w.heart_rate,spo2:w.spo2,temperature:w.temperature,humidity:w.humidity,mq4:w.mq4,mq135:w.mq135}].slice(-120);});
 Object.entries(s.environment).forEach(([k,v])=>{out[k]=[...(out[k]||[]),{time,value:v.value}].slice(-120);});return out;});
 }};
 const connect=()=>{if(!alive)return;ws=new WebSocket((location.protocol==='https:'?'wss:':'ws:')+'//'+location.host+'/ws/live');
 ws.onopen=()=>{attempt=0;setConnected(true);setError('');};
 ws.onmessage=m=>{try{ingest(JSON.parse(m.data));}catch{setError('Invalid stream message');}};
 ws.onerror=()=>setError('Backend connection interrupted');
 ws.onclose=()=>{setConnected(false);if(alive)timer=setTimeout(connect,Math.min(10000,1000*2**attempt++));};
 };
 api('state').then(s=>alive&&ingest({type:'system.snapshot',payload:s} as Event)).catch(e=>setError(e.message));connect();
 return()=>{alive=false;clearTimeout(timer);ws?.close();};
 },[]);
 return <Context.Provider value={{state,connected,error,history}}>{children}</Context.Provider>;
}
export const useLive=()=>useContext(Context);
export const age=(timestamp?:string)=>timestamp?Math.max(0,Math.floor((Date.now()-new Date(timestamp).getTime())/1000)):Infinity;
export const stale=(timestamp?:string)=>age(timestamp)>10;
