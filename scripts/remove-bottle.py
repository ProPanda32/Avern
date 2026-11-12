from pathlib import Path

hero = Path("source/src/hero.ts")
text = hero.read_text(encoding="utf-8")
old_import = "import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js'\n"
old_model = """  const gltf=await new GLTFLoader().loadAsync(new URL('../Public/Assets/Models/nocturne-bottle.glb',import.meta.url).href)
  stage.configure(gltf.scene)
  const bounds=new THREE.Box3().setFromObject(gltf.scene);bottleSize=bounds.getSize(new THREE.Vector3())
  gltf.scene.position.sub(bounds.getCenter(new THREE.Vector3()));root.add(gltf.scene);applyConfig()
  target.hidden=false;status.hidden=true;hero.dataset.state='ready'
"""
new_model = "  status.hidden=true;hero.dataset.state='ready'\n"
assert text.count(old_import) == 1, "Bottle loader import changed in source"
assert text.count(old_model) == 1, "Bottle model block changed in source"
text = text.replace(old_import, "").replace(old_model, new_model)
start = text.index('    <section class="fragrance-section"')
end = text.index('  <dialog id="menu-dialog"', start)
text = text[:start] + '''    <section class="fragrance-section" id="fragrance" aria-label="Averna presentation">
      <div class="presentation-slides" role="list"></div>
    </section>
  </main>
  <dialog id="deck-viewer" class="deck-viewer" aria-label="Presentation slide">
    <button class="dialog-close deck-close" type="button" aria-label="Close slide">×</button>
    <img alt="">
  </dialog>
''' + text[end:]
slide_anchor = "const hero=app.querySelector<HTMLElement>('.site-hero')!"
slide_actions = """const deckList=app.querySelector<HTMLDivElement>('.presentation-slides')!
const deckViewer=app.querySelector<HTMLDialogElement>('#deck-viewer')!
const deckImage=deckViewer.querySelector<HTMLImageElement>('img')!
fetch('/Avern/slides/manifest.json').then(async response=>{
  if(!response.ok)throw new Error('Presentation slides are unavailable')
  return await response.json() as string[]
}).then(files=>{
  files.forEach((file,index)=>{
    const button=document.createElement('button')
    button.className='deck-slide';button.type='button';button.setAttribute('role','listitem')
    button.setAttribute('aria-label','Open presentation slide '+(index+1))
    const image=document.createElement('img')
    image.src='/Avern/slides/'+file;image.alt='Averna presentation slide '+(index+1)
    image.loading=index===0?'eager':'lazy'
    button.append(image)
    button.addEventListener('click',()=>{deckImage.src=image.src;deckImage.alt=image.alt;deckViewer.showModal()})
    deckList.append(button)
  })
}).catch(error=>{console.error(error);deckList.textContent='Presentation slides could not load.'})
"""
assert text.count(slide_anchor) == 1, "Slide script anchor changed"
text = text.replace(slide_anchor, slide_actions + slide_anchor)
hero.write_text(text, encoding="utf-8")

vite = Path("source/vite.config.ts")
config = vite.read_text(encoding="utf-8")
assert config.count("'/Nocturne/'") == 1, "Pages base path changed in source"
vite.write_text(config.replace("'/Nocturne/'", "'/Avern/'"), encoding="utf-8")

# Hide the entire landing header, including its icons.
hero_css = Path("source/src/hero.css")
hero_css.write_text(
    hero_css.read_text(encoding="utf-8")
    + "\n.site-header, .bottle-controls { display: none !important; }\n",
    encoding="utf-8",
)

# A diagonal, softly illuminated seam carries the hero into the next section.
hero_css.write_text(
    hero_css.read_text(encoding="utf-8")
    + """
:root { --diagonal-cut: clamp(70px, 10vw, 150px); }
.fragrance-section {
  position: relative;
  z-index: 4;
  margin-top: 0;
  padding-top: calc(clamp(60px, 8vw, 140px) + var(--diagonal-cut));
  clip-path: polygon(0 var(--diagonal-cut), 100% 0, 100% 100%, 0 100%);
}
.fragrance-section::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: calc(var(--diagonal-cut) + 8px);
  pointer-events: none;
  background: linear-gradient(90deg, rgba(241,206,143,.4), rgba(255,250,226,.98) 48%, rgba(220,173,102,.4));
  clip-path: polygon(0 calc(var(--diagonal-cut) - 4px), 100% 0, 100% 8px, 0 calc(var(--diagonal-cut) + 8px));
  opacity: .85;
  background-size: 150% 100%;
  filter: drop-shadow(0 0 12px rgba(255,228,172,.7));
}
@media (max-width: 700px) {
  :root { --diagonal-cut: 70px; }
  .fragrance-section { padding-top: 135px; }
}
@media (prefers-reduced-motion: no-preference) {
  .fragrance-section::before { animation: diagonal-glow 4s ease-in-out infinite alternate; }
}
@keyframes diagonal-glow { from { opacity: .6; background-position: 0% 0; } to { opacity: .95; background-position: 100% 0; } }
""",
    encoding="utf-8",
)

# The space after the transition is a single uninterrupted cream canvas.
hero_css.write_text(
    hero_css.read_text(encoding="utf-8")
    + "\n.fragrance-section { min-height: 100svh; background: #eee9df; }\n",
    encoding="utf-8",
)

# Add a compact, saved particle composition panel to the published scene.
hero_text = hero.read_text(encoding="utf-8")
load_anchor = "  let config=loadConfig(creatorMode)\n"
load_extra = """  let config=loadConfig(creatorMode)
  const particleStoreKey='avern.particles.v1'
  const spreadStoreKey='avern.particle.spread.v1'
  const gapStoreKey='avern.particle.gap.v1'
  const motionStoreKey='avern.particle.motion.v1'
  const greenBrightnessKey='avern.particle.green-brightness.v1'
  const sceneToneKey='avern.scene.tone.v1'
  let sceneTone={hue:0,saturation:1,temperature:0,light:1}
  try {
    const saved=JSON.parse(localStorage.getItem(sceneToneKey)||'null') as Partial<typeof sceneTone>|null
    if(saved)for(const key of ['hue','saturation','temperature','light'] as const){
      if(typeof saved[key]==='number'&&Number.isFinite(saved[key]))sceneTone[key]=saved[key]!
    }
  } catch { /* Keep neutral scene colour. */ }
  const savedSpread=Number(localStorage.getItem(spreadStoreKey))
  let particleSpread=Number.isFinite(savedSpread)&&savedSpread>=.6&&savedSpread<=1.6?savedSpread:1
  const savedGap=Number(localStorage.getItem(gapStoreKey))
  let particleGap=Number.isFinite(savedGap)&&savedGap>=.7&&savedGap<=1.4?savedGap:1
  const savedMotion=Number(localStorage.getItem(motionStoreKey))
  let particleMotionAmount=Number.isFinite(savedMotion)&&savedMotion>=0&&savedMotion<=6?savedMotion:0
  const savedGreenBrightness=Number(localStorage.getItem(greenBrightnessKey))
  let greenBrightness=Number.isFinite(savedGreenBrightness)&&savedGreenBrightness>=0&&savedGreenBrightness<=5?savedGreenBrightness:0
  try {
    const saved=JSON.parse(localStorage.getItem(particleStoreKey)||'null') as Record<string,number>|null
    if(saved)for(const key of ['count','size','opacity','brightness','speed','ambientSpeed','repulsion','radius','mossStrength'] as const){
      if(typeof saved[key]==='number'&&Number.isFinite(saved[key]))config.particles[key]=key==='ambientSpeed'?Math.max(0,Math.min(2,saved[key])):saved[key]
    }
  } catch { /* Use the original composition when no saved settings exist. */ }
"""
assert hero_text.count(load_anchor) == 1, "Config load anchor changed"
hero_text = hero_text.replace(load_anchor, load_extra)
panel_anchor = "  resize();rebuildGarden()\n"
panel_extra = """  resize();rebuildGarden()
  const particlePanel=document.createElement('details')
  particlePanel.className='avern-particle-settings'
  particlePanel.open=true
  particlePanel.setAttribute('aria-label','Particle composition settings')
  const particleSummary=document.createElement('summary')
  particleSummary.textContent='Particle settings'
  particlePanel.append(particleSummary)
  const particleFields=[
    ['Density','count',.2,1.5,.05],
    ['Size','size',.2,4,.05],
    ['Opacity','opacity',0,1,.05],
    ['Brightness','brightness',0,4,.05],
    ['Interaction speed','speed',0,4,.05],
    ['Drift speed','ambientSpeed',0,2,.05],
    ['Cursor response','repulsion',0,5,.05],
    ['Response radius','radius',.1,4,.05],
    ['Green detail','mossStrength',0,4,.05],
  ] as const
  const particleInputs:Partial<Record<keyof typeof config.particles,HTMLInputElement>>={}
  for(const [label,key,min,max,step] of particleFields){
    const row=document.createElement('label')
    row.className='avern-particle-row'
    const name=document.createElement('span')
    name.textContent=label
    const input=document.createElement('input')
    input.type='range';input.min=String(min);input.max=String(max);input.step=String(step)
    input.value=String(config.particles[key])
    const value=document.createElement('output')
    value.textContent=input.value
    input.addEventListener(key==='count'?'change':'input',()=>{
      config.particles[key]=Number(input.value)
      value.textContent=input.value
      applyConfig()
      try{localStorage.setItem(particleStoreKey,JSON.stringify(config.particles))}catch{}
    })
    row.append(name,input,value)
    particlePanel.append(row)
    particleInputs[key]=input
  }
  const spreadRow=document.createElement('label')
  spreadRow.className='avern-particle-row'
  const spreadName=document.createElement('span')
  spreadName.textContent='Composition spread'
  const spreadInput=document.createElement('input')
  spreadInput.type='range';spreadInput.min='.6';spreadInput.max='1.6';spreadInput.step='.05';spreadInput.value=String(particleSpread)
  const spreadValue=document.createElement('output')
  spreadValue.textContent=spreadInput.value
  spreadInput.addEventListener('change',()=>{
    particleSpread=Number(spreadInput.value)
    spreadValue.textContent=spreadInput.value
    try{localStorage.setItem(spreadStoreKey,spreadInput.value)}catch{}
    rebuildGarden()
  })
  spreadRow.append(spreadName,spreadInput,spreadValue)
  particlePanel.append(spreadRow)
  const gapRow=document.createElement('label')
  gapRow.className='avern-particle-row'
  const gapName=document.createElement('span')
  gapName.textContent='Center opening'
  const gapInput=document.createElement('input')
  gapInput.type='range';gapInput.min='.7';gapInput.max='1.4';gapInput.step='.05';gapInput.value=String(particleGap)
  const gapValue=document.createElement('output')
  gapValue.textContent=gapInput.value
  gapInput.addEventListener('change',()=>{
    particleGap=Number(gapInput.value);gapValue.textContent=gapInput.value
    try{localStorage.setItem(gapStoreKey,gapInput.value)}catch{}
    rebuildGarden()
  })
  gapRow.append(gapName,gapInput,gapValue)
  particlePanel.append(gapRow)
  const motionRow=document.createElement('label')
  motionRow.className='avern-particle-row'
  const motionName=document.createElement('span')
  motionName.textContent='Motion amount'
  const motionInput=document.createElement('input')
  motionInput.type='range';motionInput.min='0';motionInput.max='6';motionInput.step='.05';motionInput.value=String(particleMotionAmount)
  const motionValue=document.createElement('output')
  motionValue.textContent=motionInput.value
  motionInput.addEventListener('input',()=>{
    particleMotionAmount=Number(motionInput.value);motionValue.textContent=motionInput.value
    garden?.setMotionAmount(particleMotionAmount)
    try{localStorage.setItem(motionStoreKey,motionInput.value)}catch{}
  })
  motionRow.append(motionName,motionInput,motionValue)
  particlePanel.append(motionRow)
  const greenRow=document.createElement('label');greenRow.className='avern-particle-row'
  const greenName=document.createElement('span');greenName.textContent='Green brightness'
  const greenInput=document.createElement('input');greenInput.type='range';greenInput.min='0';greenInput.max='5';greenInput.step='.05';greenInput.value=String(greenBrightness)
  const greenValue=document.createElement('output');greenValue.textContent=greenInput.value
  greenInput.addEventListener('input',()=>{greenBrightness=Number(greenInput.value);greenValue.textContent=greenInput.value;garden?.setGreenBrightness(greenBrightness);try{localStorage.setItem(greenBrightnessKey,greenInput.value)}catch{}})
  greenRow.append(greenName,greenInput,greenValue);particlePanel.append(greenRow)
  const resetParticles=document.createElement('button')
  resetParticles.type='button';resetParticles.textContent='Reset particles'
  resetParticles.addEventListener('click',()=>{
    config.particles={...production.particles}
    for(const [,key] of particleFields){
      const input=particleInputs[key]!
      input.value=String(config.particles[key])
      input.nextElementSibling!.textContent=input.value
    }
    particleSpread=1;spreadInput.value='1';spreadValue.textContent='1'
    particleGap=1;gapInput.value='1';gapValue.textContent='1'
    particleMotionAmount=0;motionInput.value='0';motionValue.textContent='0'
    greenBrightness=0;greenInput.value='0';greenValue.textContent='0'
    try{localStorage.removeItem(particleStoreKey);localStorage.removeItem(spreadStoreKey);localStorage.removeItem(gapStoreKey);localStorage.removeItem(motionStoreKey);localStorage.removeItem(greenBrightnessKey)}catch{}
    rebuildGarden()
  })
  particlePanel.append(resetParticles)
  hero.append(particlePanel)
  const scenePanel=document.createElement('details')
  scenePanel.className='avern-scene-settings'
  scenePanel.open=true
  scenePanel.setAttribute('aria-label','Whole scene colour and light settings')
  const sceneSummary=document.createElement('summary')
  sceneSummary.textContent='Scene light & colour'
  scenePanel.append(sceneSummary)
  function applySceneTone(){
    const hue=THREE.MathUtils.clamp(sceneTone.hue,-180,180)+config.atmosphere.hue
    const saturation=THREE.MathUtils.clamp(sceneTone.saturation,0,2)
    const temperature=THREE.MathUtils.clamp(sceneTone.temperature,-100,100)
    const light=THREE.MathUtils.clamp(sceneTone.light,.4,1.8)
    const tint=temperature<0?`sepia(${Math.abs(temperature)/200}) hue-rotate(180deg)`:`sepia(${temperature/180})`
    const filter=`hue-rotate(${hue}deg) saturate(${saturation}) ${tint} brightness(${light})`
    renderer.domElement.style.filter=filter
    hero.querySelectorAll<HTMLElement>('.averna-hero-art').forEach(image=>{image.style.filter=filter+' drop-shadow(0 12px 32px #0008)'})
  }
  const toneFields=[['Hue','hue',-180,180,1],['Saturation','saturation',0,2,.05],['Temperature','temperature',-100,100,1],['Light','light',.4,1.8,.05]] as const
  const toneInputs:Partial<Record<keyof typeof sceneTone,HTMLInputElement>>={}
  for(const [label,key,min,max,step] of toneFields){
    const row=document.createElement('label');row.className='avern-particle-row'
    const name=document.createElement('span');name.textContent=label
    const input=document.createElement('input');input.type='range';input.min=String(min);input.max=String(max);input.step=String(step);input.value=String(sceneTone[key])
    const value=document.createElement('output');value.textContent=input.value
    input.addEventListener('input',()=>{sceneTone[key]=Number(input.value);value.textContent=input.value;applySceneTone();try{localStorage.setItem(sceneToneKey,JSON.stringify(sceneTone))}catch{}})
    row.append(name,input,value);scenePanel.append(row);toneInputs[key]=input
  }
  const resetTone=document.createElement('button');resetTone.type='button';resetTone.textContent='Reset scene colour'
  resetTone.addEventListener('click',()=>{
    sceneTone={hue:0,saturation:1,temperature:0,light:1}
    for(const [,key] of toneFields){const input=toneInputs[key]!;input.value=String(sceneTone[key]);input.nextElementSibling!.textContent=input.value}
    applySceneTone();try{localStorage.removeItem(sceneToneKey)}catch{}
  })
  scenePanel.append(resetTone);hero.append(scenePanel);applySceneTone()
"""
assert hero_text.count(panel_anchor) == 1, "Garden setup anchor changed"
hero_text = hero_text.replace(panel_anchor, panel_extra)
old_filter="renderer.domElement.style.filter='hue-rotate('+config.atmosphere.hue+'deg)'"
assert hero_text.count(old_filter)==1, 'Scene filter anchor changed'
hero_text=hero_text.replace(old_filter,'applySceneTone()')
old_garden_call='config.particles.count);hero.dataset.particles'
assert hero_text.count(old_garden_call) == 1, 'Garden call changed in source'
hero_text = hero_text.replace(old_garden_call,'config.particles.count,particleSpread,particleGap,particleMotionAmount);hero.dataset.particles')
hero.write_text(hero_text, encoding="utf-8")
hero_css.write_text(
    hero_css.read_text(encoding="utf-8")
    + """
.avern-particle-settings{position:fixed;z-index:100;right:18px;top:18px;width:min(300px,calc(100vw - 36px));max-height:calc(100svh - 36px);overflow:auto;color:#f3eadb;background:#101714e8;border:1px solid #bc9b6b88;box-shadow:0 12px 40px #0008;backdrop-filter:blur(16px);font:12px/1.4 Arial,sans-serif}
.avern-particle-settings summary{list-style:none;cursor:pointer;padding:12px 15px;letter-spacing:.08em}
.avern-particle-settings summary::-webkit-details-marker{display:none}
.avern-particle-settings summary::after{content:"+";float:right}
.avern-particle-settings[open] summary::after{content:"−"}
.avern-particle-row{display:grid;grid-template-columns:1fr 85px 32px;gap:8px;align-items:center;padding:6px 15px}
.avern-particle-row input{width:100%;accent-color:#d6aa6e}
.avern-particle-row output{text-align:right;font-variant-numeric:tabular-nums}
.avern-particle-settings button{margin:12px 15px 15px;padding:7px 11px;border:1px solid #b79a73;background:#252e28;color:#f3eadb;cursor:pointer}
@media(max-width:700px){.avern-particle-settings{right:10px;top:10px;width:min(280px,calc(100vw - 20px))}}
.avern-scene-settings{position:fixed;z-index:101;right:18px;top:72px;width:min(300px,calc(100vw - 36px));color:#f3eadb;background:#101714e8;border:1px solid #bc9b6b88;box-shadow:0 12px 40px #0008;backdrop-filter:blur(16px);font:12px/1.4 Arial,sans-serif}
.avern-scene-settings summary{cursor:pointer;padding:12px 15px;letter-spacing:.08em}
.avern-scene-settings button{margin:12px 15px 15px;padding:7px 11px;border:1px solid #b79a73;background:#252e28;color:#f3eadb;cursor:pointer}
.avern-particle-settings[open]~.avern-scene-settings{top:auto;bottom:18px}
@media(max-width:700px){.avern-scene-settings{right:10px;top:62px;width:min(280px,calc(100vw - 20px))}}
""",
    encoding="utf-8",
)

# Show the new image as a clickable presentation slide.
hero_css.write_text(
    hero_css.read_text(encoding="utf-8")
    + """
.fragrance-section{display:grid;place-items:center}
.slide-tile{display:block;width:min(76vw,920px);aspect-ratio:16/10;padding:0;border:1px solid #d6cec1;background:#fff;box-shadow:0 24px 70px #3a302b24;cursor:pointer;overflow:hidden;transition:transform .35s ease,box-shadow .35s ease}
.slide-tile:hover{transform:translateY(-6px);box-shadow:0 32px 80px #3a302b35}
.slide-tile:focus-visible{outline:3px solid #9c754b;outline-offset:6px}
.slide-tile img{display:block;width:100%;height:100%;object-fit:contain}
.problem-slide{width:min(94vw,1100px);max-width:1100px;max-height:94svh;padding:40px 22px 22px;border:0;background:#eee9df;box-shadow:0 24px 100px #0009}
.problem-slide::backdrop{background:#070b0ae0;backdrop-filter:blur(8px)}
.problem-slide img{display:block;max-width:100%;max-height:calc(94svh - 70px);margin:auto;object-fit:contain}
.problem-slide-close{position:absolute;top:8px;right:12px;border:0;background:transparent;color:#29261f;font:30px Arial,sans-serif;cursor:pointer}
@media(max-width:700px){.slide-tile{width:88vw;aspect-ratio:4/5}.problem-slide{padding:35px 8px 8px}}
@media(prefers-reduced-motion:reduce){.slide-tile{transition:none}}
""",
    encoding="utf-8",
)

# Make continuous motion visibly affect every particle; zero still pauses the drift.
garden = Path("source/src/garden.ts")
garden_text = garden.read_text(encoding="utf-8")
old_drift = "p+=vec3(sin(time*ambientSpeed*.18+p.y*3.),cos(time*ambientSpeed*.13+p.x*2.),0.)*.009;"
new_drift = "p+=vec3(sin(time*ambientSpeed*.18+p.y*3.),cos(time*ambientSpeed*.13+p.x*2.),0.)*.009*ambientStrength;"
assert garden_text.count(old_drift) == 1, "Particle drift shader changed in source"
garden_text = garden_text.replace(old_drift, new_drift)
old_tick = """      for(const {mesh,home,phase} of spheres){
        if(!mesh.visible)continue
        mesh.position.copy(home)
        const options=mesh.userData.settings as SphereTransform|undefined
        if(!reduced){mesh.position.y+=Math.sin(seconds*.3*(options?.floatSpeed??1)+phase)*.006;mesh.rotation.y+=delta*.015*(options?.floatSpeed??1)}
      }
"""
new_tick = """      const drift=reduced?0:ambientSpeed.value
      const amount=reduced?0:motionAmount
      moss.position.set(Math.sin(seconds*.18*drift)*.025*amount,Math.cos(seconds*.14*drift)*.016*amount,0)
      leaves.position.set(Math.sin(seconds*.16*drift+1.3)*.022*amount,Math.cos(seconds*.12*drift+.6)*.018*amount,0)
      branches.position.set(Math.sin(seconds*.13*drift+.8)*.012*amount,Math.cos(seconds*.11*drift)*.012*amount,0)
      beads.position.set(Math.sin(seconds*.2*drift+2.1)*.018*amount,Math.cos(seconds*.16*drift)*.014*amount,0)
      for(const {mesh,home,phase} of spheres){
        if(!mesh.visible)continue
        mesh.position.copy(home)
        const options=mesh.userData.settings as SphereTransform|undefined
        if(drift>0&&amount>0){mesh.position.y+=Math.sin(seconds*.18*drift*(options?.floatSpeed??1)+phase)*.008*amount;mesh.rotation.y+=delta*.014*drift*amount*(options?.floatSpeed??1)}
      }
"""
assert garden_text.count(old_tick) == 1, "Garden animation loop changed in source"
garden_text = garden_text.replace(old_tick, new_tick)
old_signature = "compact: boolean, density=1) {"
assert garden_text.count(old_signature) == 1, "Garden signature changed in source"
garden_text = garden_text.replace(old_signature, "compact: boolean, density=1, spreadFactor=1, gapFactor=1, motionAmount=0) {")
old_spread = "spread:r(.075,.20)"
assert garden_text.count(old_spread) == 1, "Garden cluster spread changed in source"
garden_text = garden_text.replace(old_spread, "spread:r(.075,.20)*spreadFactor")
old_exclusion = "const exclusion = portrait ? .39 : .225"
assert garden_text.count(old_exclusion) == 1, "Garden center opening changed in source"
garden_text = garden_text.replace(old_exclusion, "const exclusion = (portrait ? .39 : .225)*gapFactor")
old_uniform = "brightnessMultiplier:{value:1},ambientSpeed,hoverPointer"
assert garden_text.count(old_uniform) == 1, "Particle uniforms changed in source"
garden_text = garden_text.replace(old_uniform, "brightnessMultiplier:{value:1},ambientSpeed,ambientStrength:{value:motionAmount},hoverPointer")
old_declaration = "sizeMultiplier,ambientSpeed,hoverActive"
assert garden_text.count(old_declaration) == 1, "Particle shader uniforms changed in source"
garden_text = garden_text.replace(old_declaration, "sizeMultiplier,ambientSpeed,ambientStrength,hoverActive")
old_return = "    count, root, spheres, syncSpheres, probeMoss,"
assert garden_text.count(old_return) == 1, "Garden controls changed in source"
garden_text = garden_text.replace(old_return, "    count, root, spheres, syncSpheres, probeMoss,\n    setMotionAmount(value:number){motionAmount=value;material.uniforms.ambientStrength.value=value},\n    setGreenBrightness(value:number){mossMaterial.emissive.set('#79ff4e');mossMaterial.emissiveIntensity=value;mossOrb.emissive.set('#79ff4e');mossOrb.emissiveIntensity=value},")
old_spheres = """  const accents=[[-.99,-.62,2.65,.23,4],[1.02,-.86,2.7,.24,4],[-.68,-.85,2.45,.16,1],
    [.84,-.61,1.8,.16,3],[-.49,.43,-.15,.13,0],[.62,.02,-.8,.10,4],
    [.35,-.37,.1,.10,4],[-.54,-.34,-.25,.09,4],[.87,.26,-.6,.10,1],[-.72,.28,-.6,.07,4]]
  const orbCount=compact?32:57
  for(let i=0;i<orbCount;i++) {
    let x:number,y:number,z:number,radius:number,kind:number
    if(i<accents.length){[x,y,z,radius,kind]=accents[i];if(portrait){x*=1.12;radius*=.62}}
    else {
      x=r(-1.05,1.05);y=r(-.65,.85);z=r(-3.6,.6);radius=r(.022,.072)
      if(Math.abs(x)<exclusion+.05)x=(x<0?-1:1)*(exclusion+.07+random()*.28)
      kind=i%6;if(kind===4 && i%3)kind=0
    }
"""
new_spheres = """  const accents=[[-.88,-.58,2.4,.17,4],[.88,-.58,2.4,.17,4],[-.67,-.28,1.2,.11,1],
    [.67,-.28,1.2,.11,3],[-.74,.35,-.3,.10,0],[.74,.35,-.3,.10,1],
    [-.56,.64,-1,.07,2],[.56,.64,-1,.07,5],[-.88,.06,-.6,.08,4],[.88,.06,-.6,.08,0]]
  const orbCount=compact?32:57
  for(let i=0;i<orbCount;i++) {
    let x:number,y:number,z:number,radius:number,kind:number
    if(i<accents.length){[x,y,z,radius,kind]=accents[i];if(portrait){x*=1.12;radius*=.62}}
    else {
      const n=i-accents.length,side=n%2===0?-1:1,row=Math.floor(n/2)
      const column=Math.floor(row/12),step=row%12
      x=side*(.53+column*.27+(random()-.5)*.035)
      y=-.57+step*.113+(random()-.5)*.035
      z=-2.6+column*.45+(random()-.5)*.35
      radius=.025+(step%4)*.007
      kind=[0,1,2,5,3,4][(step+column)%6]
      if(portrait){x*=1.12;radius*=.72}
    }
"""
assert garden_text.count(old_spheres) == 1, "Sphere layout changed in source"
garden.write_text(garden_text.replace(old_spheres, new_spheres), encoding="utf-8")

# Make the dedicated formation editor available through the existing Creator Studio.
hero_text = hero.read_text(encoding="utf-8")
old_creator = "const creatorMode=import.meta.env.DEV && new URLSearchParams(location.search).get('creator')==='1'"
assert hero_text.count(old_creator) == 1, "Creator Studio gate changed in source"
hero_text = hero_text.replace(old_creator, "const creatorMode=new URLSearchParams(location.search).get('creator')==='1'")
import_anchor = "import { createCreatorStudio } from './creator-studio'"
assert hero_text.count(import_anchor) == 1, "Creator Studio import changed in source"
hero_text = hero_text.replace(import_anchor, import_anchor + "\nimport { createParticleCompositionEditor } from './particle-composition'")
setup_anchor = "  const studio=creatorMode?createCreatorStudio(hero,config,next=>{config=next;applyConfig()}):undefined"
assert hero_text.count(setup_anchor) == 1, "Creator Studio setup changed in source"
hero_text = hero_text.replace(setup_anchor, "  const studio=undefined as ReturnType<typeof createCreatorStudio>|undefined\n  if(creatorMode)createParticleCompositionEditor(hero,scene,camera)")
garden_anchor = "hero.dataset.particles=String(garden.count);"
assert hero_text.count(garden_anchor) == 1, "Garden setup changed in source"
hero_text = hero_text.replace(garden_anchor, "garden.setGreenBrightness(greenBrightness);" + garden_anchor)
# Keep the garden visible so its density, colour and motion settings affect the scene.
hero.write_text(hero_text, encoding="utf-8")

# Place the supplied transparent Averna artwork over the existing landing scene.
hero_text = hero.read_text(encoding="utf-8")
art_anchor = '      <div class="scene-layer" aria-hidden="true"></div>'
assert hero_text.count(art_anchor) == 1, "Hero scene markup changed in source"
hero_text = hero_text.replace(art_anchor, art_anchor + '\n      <img class="averna-hero-art" src="/Avern/assets/averna-hero.png" alt="AVERNA — Design, Create, Innovate">')
hero.write_text(hero_text, encoding="utf-8")
hero_css.write_text(
    hero_css.read_text(encoding="utf-8")
    + """
.averna-hero-art{position:absolute;z-index:4;left:50%;top:50%;transform:translate(-50%,-50%);width:min(92vw,1400px);max-height:82svh;object-fit:contain;pointer-events:none;filter:drop-shadow(0 12px 32px #0008)}
.site-hero .hero-copy{display:none}
@media(max-width:700px){.averna-hero-art{width:105vw;max-height:70svh}}
""",
    encoding="utf-8",
)

# Put the rainbow inside the 3D scene, behind the garden particles.
hero_text = hero.read_text(encoding="utf-8")
old_art = '<img class="averna-hero-art" src="/Avern/assets/averna-hero.png" alt="AVERNA — Design, Create, Innovate">'
new_art = '<img class="averna-hero-art averna-hero-logo" src="/Avern/assets/averna-hero.png" alt="AVERNA — Design, Create, Innovate">\n      <img class="averna-hero-art averna-hero-flower" src="/Avern/assets/averna-hero.png" alt="" aria-hidden="true">'
assert hero_text.count(old_art) == 1, "Averna artwork markup changed"
hero_text = hero_text.replace(old_art, new_art)
old_stage_import = "import { createOpticalStage } from './optical-stage'"
assert hero_text.count(old_stage_import) == 1, "Stage import changed"
hero_text = hero_text.replace(old_stage_import, "import { createOpticalStage, WORLD } from './optical-stage'")
art_setup_anchor = "  camera.position.z=5\n"
art_setup = """  camera.position.z=5
  const artworkTexture=new THREE.TextureLoader().load('/Avern/assets/averna-hero.png')
  artworkTexture.colorSpace=THREE.SRGBColorSpace
  const artwork=new THREE.Mesh(new THREE.PlaneGeometry(1,1),new THREE.MeshBasicMaterial({map:artworkTexture,transparent:true,depthWrite:false,toneMapped:false}))
  artwork.layers.set(WORLD);artwork.position.z=-7;scene.add(artwork)
  function fitArtwork(){
    const viewHeight=2*Math.tan(THREE.MathUtils.degToRad(camera.fov/2))*(camera.position.z+7)
    const width=Math.min(viewHeight*camera.aspect*.92,viewHeight*.82*2)
    artwork.scale.set(width,width/2,1)
    artwork.position.x=camera.position.x;artwork.position.y=camera.position.y
  }
"""
assert hero_text.count(art_setup_anchor) == 1, "Camera setup changed"
hero_text = hero_text.replace(art_setup_anchor, art_setup)
old_resize = "renderer.setSize(w,h,false);frame()"
assert hero_text.count(old_resize) == 1, "Hero resize changed"
hero_text = hero_text.replace(old_resize, "renderer.setSize(w,h,false);fitArtwork();frame()")
old_camera_update = "camera.updateProjectionMatrix()\n    applySceneTone()"
assert hero_text.count(old_camera_update) == 1, "Camera config changed"
hero_text = hero_text.replace(old_camera_update, "camera.updateProjectionMatrix();fitArtwork()\n    applySceneTone()")
hero.write_text(hero_text, encoding="utf-8")
hero_css.write_text(
    hero_css.read_text(encoding="utf-8")
    + """
.averna-hero-logo{clip-path:polygon(12% 20%,68% 20%,68% 56%,18% 56%,18% 43%,12% 43%)}
.averna-hero-flower{clip-path:polygon(66% 12%,88% 12%,88% 52%,66% 52%)}
""",
    encoding="utf-8",
)

# Mask the 3D backdrop texture to the rainbow band only; the logo and orchid stay
# in their separate foreground crops, avoiding doubled text and petals.
hero_text = hero.read_text(encoding="utf-8")
old_material = "  const artwork=new THREE.Mesh(new THREE.PlaneGeometry(1,1),new THREE.MeshBasicMaterial({map:artworkTexture,transparent:true,depthWrite:false,toneMapped:false}))"
new_material = """  const artworkMaterial=new THREE.MeshBasicMaterial({map:artworkTexture,transparent:true,depthWrite:false,toneMapped:false})
  artworkMaterial.onBeforeCompile=shader=>{
    shader.fragmentShader=shader.fragmentShader.replace('#include <map_fragment>',`#include <map_fragment>
      float rainbowX=vMapUv.x;
      float rainbowY=1.0-vMapUv.y;
      float rainbowTop=.38+.19*(1.0-pow(abs(rainbowX*2.0-1.0),1.35));
      float rainbowBottom=rainbowTop+.30;
      vec3 rainbowColor=texture2D(map,vMapUv).rgb;
      float rainbowChroma=max(max(rainbowColor.r,rainbowColor.g),rainbowColor.b)-min(min(rainbowColor.r,rainbowColor.g),rainbowColor.b);
      diffuseColor.a*=smoothstep(rainbowTop,rainbowTop+.035,rainbowY)
        *(1.0-smoothstep(rainbowBottom-.04,rainbowBottom,rainbowY))
        *smoothstep(.18,.38,rainbowChroma)
        *smoothstep(.22,.42,rainbowX)
        *(1.0-smoothstep(.84,.96,rainbowX));`)
  }
  artworkMaterial.customProgramCacheKey=()=> 'averna-rainbow-mask-v1'
  const artwork=new THREE.Mesh(new THREE.PlaneGeometry(1,1),artworkMaterial)"""
assert hero_text.count(old_material) == 1, "Averna scene material changed"
hero_text = hero_text.replace(old_material, new_material)
hero.write_text(hero_text, encoding="utf-8")

# Remove saturated ribbon pixels from the foreground logo copy, preserving
# its light lettering while the rainbow remains solely in the 3D backdrop.
hero_text = hero.read_text(encoding="utf-8")
logo_anchor = "const hero=app.querySelector<HTMLElement>('.site-hero')!"
logo_cleaner = """const logoArt=app.querySelector<HTMLImageElement>('.averna-hero-logo')!
let logoCleaned=false
const cleanLogo=()=>{
  if(logoCleaned||!logoArt.naturalWidth)return
  logoCleaned=true
  const canvas=document.createElement('canvas')
  canvas.width=logoArt.naturalWidth;canvas.height=logoArt.naturalHeight
  const context=canvas.getContext('2d')!
  context.drawImage(logoArt,0,0)
  const pixels=context.getImageData(0,0,canvas.width,canvas.height)
  for(let i=0;i<pixels.data.length;i+=4){
    const red=pixels.data[i],green=pixels.data[i+1],blue=pixels.data[i+2]
    const high=Math.max(red,green,blue),low=Math.min(red,green,blue)
    if(high<150||high-low>110)pixels.data[i+3]=0
  }
  context.putImageData(pixels,0,0)
  logoArt.src=canvas.toDataURL('image/png')
}
logoArt.addEventListener('load',cleanLogo,{once:true})
if(logoArt.complete&&logoArt.naturalWidth)cleanLogo()
"""
assert hero_text.count(logo_anchor) == 1, "Logo setup anchor changed"
hero_text = hero_text.replace(logo_anchor, logo_cleaner + logo_anchor)
hero.write_text(hero_text, encoding="utf-8")

# One presentation image per row; clicking a slide opens it at full size.
hero_css.write_text(
    hero_css.read_text(encoding="utf-8")
    + """
.fragrance-section{display:block}
.presentation-slides{display:grid;grid-template-columns:minmax(0,1fr);gap:clamp(24px,4vw,64px);width:min(90vw,1200px);margin:0 auto}
.deck-slide{display:block;width:100%;padding:0;border:1px solid #d4cdc0;background:#fff;box-shadow:0 20px 55px #352d2424;cursor:pointer}
.deck-slide img{display:block;width:100%;height:auto}
.deck-slide:focus-visible{outline:3px solid #9c754b;outline-offset:6px}
.deck-viewer{width:min(96vw,1600px);max-width:none;max-height:95svh;padding:38px 14px 14px;border:0;background:#eee9df}
.deck-viewer::backdrop{background:#080b0af0;backdrop-filter:blur(8px)}
.deck-viewer img{display:block;max-width:100%;max-height:calc(95svh - 52px);margin:auto;object-fit:contain}
.deck-close{position:absolute;top:4px;right:12px;border:0;background:transparent;color:#29261f;font:30px Arial,sans-serif;cursor:pointer}
""",
    encoding="utf-8",
)
