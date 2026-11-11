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
hero.write_text(text.replace(old_import, "").replace(old_model, new_model), encoding="utf-8")

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
