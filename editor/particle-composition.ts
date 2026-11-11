import * as THREE from 'three'
import { WORLD } from './optical-stage'
import './particle-composition.css'

type Shape='cloud'|'ring'|'spiral'|'sphere'|'arc'|'custom'
type Gradient='uniform'|'center'|'edge'|'focus'
type Layer='foreground'|'bottle'|'background'
type Vec=[number,number,number]
type Formation={id:string;name:string;shape:Shape;count:number;position:Vec;dimensions:Vec;rotation:Vec;distribution:number;spacing:number;gradient:Gradient;focus:Vec;layer:Layer;custom:Vec[]}
type Zone={id:string;center:Vec;radius:number}
type State={formations:Formation[];zones:Zone[];selected:string;selectedZone:string}
const key='avern.particle-composition.v1'
const presetKey='avern.particle-composition-presets.v1'
const uid=()=>crypto.randomUUID()
const fresh=(name:string):Formation=>({id:uid(),name,shape:'cloud',count:450,position:[0,0,-1],dimensions:[1.6,1.2,1],rotation:[0,0,0],distribution:1,spacing:1,gradient:'uniform',focus:[0,0,0],layer:'bottle',custom:[]})
const initial=():State=>{const left=fresh('Left formation'),right=fresh('Right formation');left.position=[-1.35,.1,-1];right.position=[1.35,.1,-1];return {formations:[left,right],zones:[{id:uid(),center:[0,0,0],radius:.55}],selected:left.id,selectedZone:''}}
const clamp=(n:number,min:number,max:number)=>Math.min(max,Math.max(min,n))
const numeric=(v:unknown,fallback:number,min:number,max:number)=>typeof v==='number'&&Number.isFinite(v)?clamp(v,min,max):fallback
function clean(value:unknown):State{
  const base=initial();if(!value||typeof value!=='object')return base
  const raw=value as Record<string,unknown>
  if(!Array.isArray(raw.formations))return base
  const formations:Formation[]=raw.formations.slice(0,20).filter(x=>x&&typeof x==='object').map((x,i)=>{
    const f=x as Partial<Formation>,d=fresh('Formation '+(i+1))
    const vec=(v:unknown,b:Vec,limit=8):Vec=>Array.isArray(v)&&v.length===3?[0,1,2].map(j=>numeric(v[j],b[j],-limit,limit)) as Vec:b
    return {id:typeof f.id==='string'?f.id:uid(),name:typeof f.name==='string'?f.name.slice(0,40):d.name,
      shape:['cloud','ring','spiral','sphere','arc','custom'].includes(String(f.shape))?f.shape!:d.shape,
      count:numeric(f.count,d.count,1,4000),position:vec(f.position,d.position),dimensions:vec(f.dimensions,d.dimensions),rotation:vec(f.rotation,d.rotation,6.29),
      distribution:numeric(f.distribution,1,.2,3),spacing:numeric(f.spacing,1,.2,3),
      gradient:['uniform','center','edge','focus'].includes(String(f.gradient))?f.gradient!:d.gradient,focus:vec(f.focus,d.focus),
      layer:['foreground','bottle','background'].includes(String(f.layer))?f.layer!:d.layer,
      custom:Array.isArray(f.custom)?f.custom.slice(0,300).filter(p=>Array.isArray(p)&&p.length===3).map(p=>vec(p,[0,0,0])):[]}
  })
  const zones:Zone[]=Array.isArray(raw.zones)?raw.zones.slice(0,20).filter(x=>x&&typeof x==='object').map(x=>{const z=x as Partial<Zone>;return {id:typeof z.id==='string'?z.id:uid(),center:Array.isArray(z.center)&&z.center.length===3?z.center.map(v=>numeric(v,0,-8,8)) as Vec:[0,0,0],radius:numeric(z.radius,.5,.05,5)}}):base.zones
  return {formations, zones, selected:typeof raw.selected==='string'?raw.selected:formations[0]?.id??'',selectedZone:typeof raw.selectedZone==='string'?raw.selectedZone:''}
}
const read=(k:string)=>{try{return JSON.parse(localStorage.getItem(k)||'null') as unknown}catch{return null}}
const save=(k:string,v:unknown)=>{try{localStorage.setItem(k,JSON.stringify(v))}catch{}}
function rng(seed:number){return()=>{seed=(seed+0x6d2b79f5)|0;let t=Math.imul(seed^seed>>>15,1|seed);t=(t+Math.imul(t^t>>>7,61|t))^t;return((t^t>>>14)>>>0)/4294967296}}
function seedOf(id:string){let n=2166136261;for(const ch of id)n=Math.imul(n^ch.charCodeAt(0),16777619);return n}
function pointsFor(f:Formation,zones:Zone[]):Float32Array{
  const random=rng(seedOf(f.id)),out:number[]=[],euler=new THREE.Euler(...f.rotation)
  const target=Math.round(f.count),attempts=target*8
  for(let i=0;i<attempts&&out.length/3<target;i++){
    const t=(out.length/3+.5)/target,angle=random()*Math.PI*2
    let x=0,y=0,z=0
    if(f.shape==='custom'&&f.custom.length){const p=f.custom[Math.floor(random()*f.custom.length)];x=p[0];y=p[1];z=p[2]}
    else if(f.shape==='ring'){const radius=.4+(random()-.5)*.16;x=Math.cos(angle)*radius;y=Math.sin(angle)*radius;z=(random()-.5)*.22}
    else if(f.shape==='arc'){const a=-Math.PI*.85+random()*Math.PI*1.7;x=Math.cos(a)*.5;y=Math.sin(a)*.5;z=(random()-.5)*.15}
    else if(f.shape==='spiral'){const a=t*Math.PI*8;x=Math.cos(a)*(.08+t*.45);y=Math.sin(a)*(.08+t*.45);z=t-.5}
    else if(f.shape==='sphere'){const v=random()*2-1,r=Math.cbrt(random())*.5,a=random()*Math.PI*2;x=Math.cos(a)*Math.sqrt(1-v*v)*r;y=Math.sin(a)*Math.sqrt(1-v*v)*r;z=v*r}
    else{x=random()-.5;y=random()-.5;z=random()-.5}
    let p=new THREE.Vector3(x,y,z)
    const radius=p.length()
    if(f.gradient==='center')p.multiplyScalar(Math.pow(random(),f.distribution))
    if(f.gradient==='edge'&&radius>.001)p.multiplyScalar(.65+.35*random()/radius)
    if(f.gradient==='focus')p.lerp(new THREE.Vector3(...f.focus).multiplyScalar(.5),clamp(f.distribution/3,0,.85)*random())
    if(f.gradient==='uniform')p.multiplyScalar(Math.pow(random(),(f.distribution-1)*.5+1))
    p.multiply(new THREE.Vector3(...f.dimensions)).multiplyScalar(f.spacing).applyEuler(euler).add(new THREE.Vector3(...f.position))
    if(zones.some(zone=>p.distanceTo(new THREE.Vector3(...zone.center))<zone.radius))continue
    out.push(p.x,p.y,p.z)
  }
  return new Float32Array(out)
}
const numberRow=(label:string,field:string,value:number,min:number,max:number,step=.05)=>`<label class="pc-row"><span>${label}</span><input type="range" data-field="${field}" min="${min}" max="${max}" step="${step}" value="${value}"><output>${value.toFixed(2)}</output></label>`
export function createParticleCompositionEditor(host:HTMLElement,scene:THREE.Scene,camera:THREE.PerspectiveCamera){
  let state=clean(read(key)),presets=read(presetKey) as Record<string,State>|null
  if(!presets||typeof presets!=='object'||Array.isArray(presets))presets={}
  const rendered=new Map<string,THREE.Points>(),panel=document.createElement('aside')
  panel.className='pc-editor';panel.setAttribute('aria-label','Particle Composition Editor');host.append(panel)
  const persist=()=>save(key,state)
  const redraw=()=>{
    for(const p of rendered.values()){scene.remove(p);p.geometry.dispose();(p.material as THREE.Material).dispose()}
    rendered.clear()
    for(const f of state.formations){
      const geometry=new THREE.BufferGeometry();geometry.setAttribute('position',new THREE.BufferAttribute(pointsFor(f,state.zones),3))
      const color=f.id===state.selected?'#e7c694':'#bdab87'
      const material=new THREE.PointsMaterial({color,size:.025,transparent:true,opacity:.8,depthWrite:false,sizeAttenuation:true})
      const cloud=new THREE.Points(geometry,material);cloud.layers.set(WORLD);cloud.userData.formationId=f.id;scene.add(cloud);rendered.set(f.id,cloud)
    }
  }
  const selected=()=>state.formations.find(f=>f.id===state.selected)
  const render=()=>{
    const f=selected(),z=state.zones.find(v=>v.id===state.selectedZone)
    panel.innerHTML=`<header><strong>Particle Composition Editor</strong><button type="button" data-action="close" aria-label="Close editor">×</button></header>
      <div class="pc-actions"><select data-action="formation" aria-label="Select formation"></select><button data-action="add">Add group</button><button data-action="duplicate">Duplicate</button><button data-action="delete">Delete</button></div>
      <label class="pc-drag"><input type="checkbox" data-action="drag" checked> Drag formations on the scene</label>
      ${f?`<section><h3>Position</h3>${numberRow('X','position.0',f.position[0],-5,5)}${numberRow('Y','position.1',f.position[1],-5,5)}${numberRow('Z','position.2',f.position[2],-6,5)}
      <h3>Dimensions</h3>${numberRow('Width','dimensions.0',f.dimensions[0],.1,5)}${numberRow('Height','dimensions.1',f.dimensions[1],.1,5)}${numberRow('Depth','dimensions.2',f.dimensions[2],.1,5)}
      <h3>Rotation</h3>${numberRow('X','rotation.0',f.rotation[0],-3.14,3.14)}${numberRow('Y','rotation.1',f.rotation[1],-3.14,3.14)}${numberRow('Z','rotation.2',f.rotation[2],-3.14,3.14)}
      <h3>Formation</h3><label>Shape <select data-field="shape"><option>cloud</option><option>ring</option><option>spiral</option><option>sphere</option><option>arc</option><option>custom</option></select></label>
      <label>Depth layer <select data-field="layer"><option>foreground</option><option>bottle</option><option>background</option></select></label>
      <label>Density gradient <select data-field="gradient"><option>uniform</option><option>center</option><option>edge</option><option>focus</option></select></label>
      ${numberRow('Particles','count',f.count,1,4000,1)}${numberRow('Distribution','distribution',f.distribution,.2,3)}${numberRow('Spacing','spacing',f.spacing,.2,3)}
      <h3>Selected region</h3>${numberRow('Focus X','focus.0',f.focus[0],-1,1)}${numberRow('Focus Y','focus.1',f.focus[1],-1,1)}${numberRow('Focus Z','focus.2',f.focus[2],-1,1)}
      <div class="pc-actions"><button data-action="custom-add">Add custom point</button><button data-action="custom-clear">Clear custom points</button></div><small>${f.custom.length} custom points. Select Custom shape to use them.</small></section>`:''}
      <section><h3>Exclusion zones</h3><div class="pc-actions"><select data-action="zone" aria-label="Select exclusion zone"></select><button data-action="zone-add">Add zone</button><button data-action="zone-delete">Delete</button></div>
      ${z?`${numberRow('X','zone.0',z.center[0],-5,5)}${numberRow('Y','zone.1',z.center[1],-5,5)}${numberRow('Z','zone.2',z.center[2],-6,5)}${numberRow('Radius','zone.radius',z.radius,.05,5)}`:''}</section>
      <section><h3>Composition presets</h3><div class="pc-actions"><select data-action="preset" aria-label="Select saved preset"></select><button data-action="save">Save</button><button data-action="load">Load</button><button data-action="preset-delete">Delete</button></div></section>`
    const formSelect=panel.querySelector<HTMLSelectElement>('[data-action="formation"]')!
    for(const item of state.formations)formSelect.add(new Option(item.name,item.id));formSelect.value=state.selected
    const zoneSelect=panel.querySelector<HTMLSelectElement>('[data-action="zone"]')!
    zoneSelect.add(new Option('Select zone',''));state.zones.forEach((item,i)=>zoneSelect.add(new Option('Zone '+(i+1),item.id)));zoneSelect.value=state.selectedZone
    const presetSelect=panel.querySelector<HTMLSelectElement>('[data-action="preset"]')!
    for(const name of Object.keys(presets!))presetSelect.add(new Option(name,name))
    if(f){panel.querySelector<HTMLSelectElement>('[data-field="shape"]')!.value=f.shape;panel.querySelector<HTMLSelectElement>('[data-field="layer"]')!.value=f.layer;panel.querySelector<HTMLSelectElement>('[data-field="gradient"]')!.value=f.gradient}
  }
  const change=(field:string,value:string)=>{
    const f=selected();if(!f)return
    if(field==='shape')f.shape=value as Shape
    else if(field==='layer'){f.layer=value as Layer;f.position[2]=value==='foreground'?2:value==='background'?-3:0}
    else if(field==='gradient')f.gradient=value as Gradient
    else if(field.startsWith('zone.')){const z=state.zones.find(v=>v.id===state.selectedZone);if(!z)return;const part=field.split('.')[1];if(part==='radius')z.radius=Number(value);else z.center[Number(part)]=Number(value)}
    else if(field.includes('.')){const [part,index]=field.split('.');(f[part as 'position'|'dimensions'|'rotation'|'focus'] as Vec)[Number(index)]=Number(value)}
    else if(field==='count'||field==='distribution'||field==='spacing')f[field]=Number(value)
    redraw();persist()
  }
  panel.addEventListener('input',event=>{const target=event.target as HTMLInputElement;if(!target.dataset.field)return;change(target.dataset.field,target.value);const output=target.nextElementSibling;if(output)output.textContent=Number(target.value).toFixed(2)})
  panel.addEventListener('change',event=>{const target=event.target as HTMLSelectElement;if(target.dataset.field){change(target.dataset.field,target.value);render()}else if(target.dataset.action==='formation'){state.selected=target.value;redraw();render();persist()}else if(target.dataset.action==='zone'){state.selectedZone=target.value;render();persist()}})
  panel.addEventListener('click',event=>{
    const action=(event.target as HTMLElement).closest<HTMLElement>('[data-action]')?.dataset.action;if(!action)return
    const f=selected()
    if(action==='close'){panel.hidden=true;return}
    if(action==='add'){const next=fresh('Formation '+(state.formations.length+1));state.formations.push(next);state.selected=next.id}
    if(action==='duplicate'&&f){const copy=structuredClone(f);copy.id=uid();copy.name=f.name+' copy';copy.position[0]+=.3;state.formations.push(copy);state.selected=copy.id}
    if(action==='delete'&&f){state.formations=state.formations.filter(v=>v.id!==f.id);state.selected=state.formations[0]?.id??''}
    if(action==='custom-add'&&f){f.custom.push([0,0,0]);f.shape='custom'}
    if(action==='custom-clear'&&f)f.custom=[]
    if(action==='zone-add'){const z={id:uid(),center:[0,0,0] as Vec,radius:.5};state.zones.push(z);state.selectedZone=z.id}
    if(action==='zone-delete'){state.zones=state.zones.filter(z=>z.id!==state.selectedZone);state.selectedZone=''}
    if(action==='save'){const name=prompt('Preset name')?.trim();if(name){presets![name]=structuredClone(state);save(presetKey,presets)}}
    if(action==='load'){const name=panel.querySelector<HTMLSelectElement>('[data-action="preset"]')!.value;if(name&&presets![name])state=clean(structuredClone(presets![name]))}
    if(action==='preset-delete'){const name=panel.querySelector<HTMLSelectElement>('[data-action="preset"]')!.value;if(name){delete presets![name];save(presetKey,presets)}}
    redraw();render();persist()
  })
  let dragging:{id:string;offset:THREE.Vector3;z:number}|undefined
  const raycaster=new THREE.Raycaster();raycaster.params.Points.threshold=.12
  const pointer=(event:PointerEvent)=>{const box=host.getBoundingClientRect();return new THREE.Vector2((event.clientX-box.left)/box.width*2-1,-(event.clientY-box.top)/box.height*2+1)}
  const planePoint=(event:PointerEvent,z:number)=>{raycaster.setFromCamera(pointer(event),camera);const hit=new THREE.Vector3();return raycaster.ray.intersectPlane(new THREE.Plane(new THREE.Vector3(0,0,1),-z),hit)?hit:null}
  host.addEventListener('pointerdown',event=>{
    if(panel.hidden||panel.contains(event.target as Node)||!panel.querySelector<HTMLInputElement>('[data-action="drag"]')?.checked)return
    raycaster.setFromCamera(pointer(event),camera)
    const hit=raycaster.intersectObjects([...rendered.values()])[0]
    if(!hit)return
    const id=hit.object.userData.formationId as string,f=state.formations.find(x=>x.id===id);if(!f)return
    state.selected=id;const at=planePoint(event,f.position[2]);if(!at)return
    dragging={id,offset:new THREE.Vector3(...f.position).sub(at),z:f.position[2]}
    host.setPointerCapture(event.pointerId);render();redraw();event.preventDefault()
  })
  host.addEventListener('pointermove',event=>{if(!dragging)return;const f=state.formations.find(x=>x.id===dragging!.id),at=planePoint(event,dragging.z);if(!f||!at)return;f.position[0]=at.x+dragging.offset.x;f.position[1]=at.y+dragging.offset.y;redraw();for(const axis of [0,1]){const input=panel.querySelector<HTMLInputElement>(`[data-field="position.${axis}"]`);if(input){input.value=String(f.position[axis]);input.nextElementSibling!.textContent=f.position[axis].toFixed(2)}}})
  const release=()=>{if(dragging){dragging=undefined;persist()}}
  host.addEventListener('pointerup',release);host.addEventListener('pointercancel',release)
  redraw();render()
  return {open(){panel.hidden=false},dispose(){for(const p of rendered.values()){scene.remove(p);p.geometry.dispose();(p.material as THREE.Material).dispose()}panel.remove()}}
}
