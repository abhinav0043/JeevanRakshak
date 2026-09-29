import type {ReactNode} from 'react';
import {AreaChart,Area,ResponsiveContainer,Tooltip,XAxis,YAxis,CartesianGrid} from 'recharts';
import {age} from '../services/live';
export function Badge({value}:{value?:string|null}){
 const text=value||'UNAVAILABLE',kind=/CRITICAL|EMERGENCY|LOST|FAILED|SAFE STOP/.test(text)?'red':/WARNING|DEGRADED|WAITING|UNAVAILABLE|OFFLINE/.test(text)?'amber':/DEMO/.test(text)?'demo':'green';
 return <span className={'badge '+kind}>{text}</span>;
}
export function Panel({title,sub,children,aside,className=''}:{title:string;sub?:string;children:ReactNode;aside?:ReactNode;className?:string}){return <section className={'panel '+className}><div className="panel-head"><div><h2>{title}</h2>{sub&&<p>{sub}</p>}</div>{aside}</div><div className="panel-body">{children}</div></section>;}
export function Empty({label='WAITING FOR SENSOR'}:{label?:string}){return <div className="empty"><span className="empty-symbol">◎</span>{label}<small>No current data received</small></div>;}
export function Fresh({timestamp}:{timestamp?:string}){const n=age(timestamp);return <span className={n>10?'stale':'muted'}>{Number.isFinite(n)?n>10?'STALE · '+n+'s ago':n+'s ago':'NO TELEMETRY'}</span>;}
export function Chart({data,keys=['value'],small=false}:{data:any[];keys?:string[];small?:boolean}){return <div style={{height:small?42:180,minWidth:0}}><ResponsiveContainer width="100%" height="100%"><AreaChart data={data}>{!small&&<><CartesianGrid stroke="#29383e" vertical={false}/><XAxis dataKey="time" hide/><YAxis width={32} tick={{fill:'#91a2aa',fontSize:12}}/><Tooltip contentStyle={{background:'#172228',border:'1px solid #34464e',color:'#ecf2f3'}}/></>}{keys.map((key,i)=><Area key={key} dataKey={key} type="monotone" stroke={['#65d6b0','#69b7ec','#edc777','#e89b98'][i%4]} fill={['#65d6b020','#69b7ec15'][i%2]} isAnimationActive={false} dot={false}/>)}</AreaChart></ResponsiveContainer></div>;}
