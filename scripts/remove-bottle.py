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
text = text[:start] + '''    <section class="fragrance-section" id="fragrance" aria-label="Presentation slides">
      <button class="slide-tile" type="button" aria-label="Open The Problem slide">
        <img src="/Avern/assets/the-problem-slide.png" alt="Preview of The Problem presentation slide">
      </button>
    </section>
  </main>
  <dialog id="problem-slide" class="problem-slide" aria-label="The Problem slide">
    <button class="problem-slide-close dialog-close" type="button" aria-label="Close slide">×</button>
    <img src="/Avern/assets/the-problem-slide.png" alt="The Problem: many websites feel static; examples of interactive websites">
  </dialog>
''' + text[end:]
slide_anchor = "const hero=app.querySelector<HTMLElement>('.site-hero')!"
slide_actions = """const problemSlide=app.querySelector<HTMLDialogElement>('#problem-slide')!
app.querySelector<HTMLButtonElement>('.slide-tile')!.addEventListener('click',()=>problemSlide.showModal())
problemSlide.addEventListener('click',event=>{if(event.target===problemSlide)problemSlide.close()})
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
  try {
    const saved=JSON.parse(localStorage.getItem(particleStoreKey)||'null') as Record<string,number>|null
    if(saved)for(const key of ['count','size','opacity','brightness','speed','ambientSpeed','repulsion','radius','mossStrength'] as const){
      if(typeof saved[key]==='number'&&Number.isFinite(saved[key]))config.particles[key]=saved[key]
    }
  } catch { /* Use the original composition when no saved settings exist. */ }
"""
assert hero_text.count(load_anchor) == 1, "Config load anchor changed"
hero_text = hero_text.replace(load_anchor, load_extra)
panel_anchor = "  resize();rebuildGarden()\n"
panel_extra = """  resize();rebuildGarden()
  const particlePanel=document.createElement('details')
  particlePanel.className='avern-particle-settings'
  particlePanel.setAttribute('aria-label','Particle composition settings')
  const particleSummary=document.createElement('summary')
  particleSummary.textContent='Particle settings'
  particlePanel.append(particleSummary)
  const particleFields=[
    ['Density','count',.2,1.5,.05],
    ['Size','size',.2,4,.05],
    ['Opacity','opacity',0,1,.05],
    ['Brightness','brightness',0,4,.05],
    ['Movement','speed',0,4,.05],
    ['Ambient drift','ambientSpeed',0,5,.05],
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
  const resetParticles=document.createElement('button')
  resetParticles.type='button';resetParticles.textContent='Reset particles'
  resetParticles.addEventListener('click',()=>{
    config.particles={...production.particles}
    for(const [,key] of particleFields){
      const input=particleInputs[key]!
      input.value=String(config.particles[key])
      input.nextElementSibling!.textContent=input.value
    }
    try{localStorage.removeItem(particleStoreKey)}catch{}
    applyConfig()
  })
  particlePanel.append(resetParticles)
  hero.append(particlePanel)
"""
assert hero_text.count(panel_anchor) == 1, "Garden setup anchor changed"
hero_text = hero_text.replace(panel_anchor, panel_extra)
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
