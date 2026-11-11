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

# Keep the header controls but remove the visible words shown in the screenshot.
hero_css = Path("source/src/hero.css")
hero_css.write_text(
    hero_css.read_text(encoding="utf-8")
    + "\n.site-header .header-menu span, .site-header .header-search span, "
      ".site-header .header-logo, .site-header .world-link { display: none !important; }\n",
    encoding="utf-8",
)
