import {useState} from 'react';
import {Panel,Badge,Empty,Fresh} from './Common';
import type {State} from '../types';
const steps=['Detect failure','Identify segment','Calculate position','Navigate to point','Deploy JR node','Establish bypass','Validate link','Restore connection'];
export function NetworkPanel({s,expanded=false}:{s:State;expanded?:boolean}){
 const [selected,setSelected]=useState('R2'),n=s.network;
 if(!n)return <Panel title="UNDERGROUND COMMUNICATION"><Empty label="WAITING FOR NETWORK"/></Panel>;
 const pos=(id:string):[number,number]=>id.startsWith('JR')?[355+(Number(id.slice(-2))-1)*70,160]:[50+['BASE','R1','R2','R3','R4','R01'].indexOf(id)*122,65];
 const node=n.nodes.find(v=>v.id===selected);
 return <Panel title="UNDERGROUND COMMUNICATION" sub="Relay topology & autonomous recovery" aside={<Badge value={n.status}/>}>
 <svg className="topology" viewBox="0 0 710 205" aria-label="Interactive relay network topology">
 {n.links.map((l,i)=>{const [x,y]=pos(l.source),[xx,yy]=pos(l.target);return <g key={i}><line x1={x} y1={y} x2={xx} y2={yy} stroke={l.status==='FAILED'?'#fa7777':l.kind==='WIRELESS'?'#64b4ee':'#5dba9d'} strokeWidth="2" strokeDasharray={l.status==='FAILED'?'6 7':l.kind==='WIRELESS'?'4 4':undefined} className={l.kind==='WIRELESS'?'flow':''}/>{l.status==='FAILED'&&<text x={(x+xx)/2} y={(y+yy)/2-12} fill="#fa7777" textAnchor="middle">BREAK</text>}</g>;})}
 {n.nodes.map(v=>{const [x,y]=pos(v.id);return <g key={v.id} onClick={()=>setSelected(v.id)} onKeyDown={e=>e.key==='Enter'&&setSelected(v.id)} tabIndex={0} role="button" aria-label={'Inspect '+v.id} className="network-node" transform={'translate('+x+','+y+')'}><rect x="-23" y="-23" rx="7" width="46" height="46" fill={v.id===selected?'#244139':'#16252b'} stroke={v.id.startsWith('JR')?'#69b9f3':'#5db49b'}/><path d="M-8 4H8M-5 -3H5M0 -10V10" stroke="#a6c9bd" strokeWidth="2"/><text y="42" textAnchor="middle">{v.id}</text></g>;})}
 </svg>
 {node&&<div className="node-details"><b>{node.id}</b><span>{node.role}</span><Badge value={node.status}/><span>{node.signal??'—'} dBm</span><span>{node.latency??'—'} ms</span><Fresh timestamp={node.last_heartbeat}/></div>}
 {(expanded||n.recovery_step>0)&&<div className="recovery"><div className="row"><h3>AUTONOMOUS NETWORK RECOVERY</h3><strong>{n.recovery_step}/8</strong></div><div className="recovery-steps">{steps.map((v,i)=><div key={v} className={i<n.recovery_step?'done':''}><span>{i<n.recovery_step?'✓':i+1}</span><small>{v}</small></div>)}</div><div className="row muted"><span>{n.failed_segment?'Failed segment: '+n.failed_segment:'Awaiting recovery event'}</span><span>{Math.round(n.recovery_duration)}s · {n.deployment}</span></div></div>}
 </Panel>;
}
