from pathlib import Path

hero = Path("source/src/hero.ts")
text = hero.read_text(encoding="utf-8")
old = "  if(creatorMode)createParticleCompositionEditor(hero,scene,camera)"
new = "  const compositionEditor=createParticleCompositionEditor(hero,scene,camera,creatorMode)"
assert text.count(old) == 1
text = text.replace(old,new)
old = "if(creatorMode)garden.root.getObjectByName('GPU botanical bead field')!.visible=false;"
new = "garden.root.getObjectByName('GPU botanical bead field')!.visible=!compositionEditor.hasSavedComposition();"
assert text.count(old) == 1
hero.write_text(text.replace(old,new),encoding="utf-8")

studio = Path("source/src/creator-studio.ts")
text = studio.read_text(encoding="utf-8")
old = "  for(const title of ['Bottle','Particles','Spheres','Lighting','Atmosphere','Brushes','Camera','Presets']){"
new = "  for(const title of ['Particles','Spheres','Lighting','Atmosphere','Brushes','Camera','Presets']){"
assert text.count(old) == 1
text = text.replace(old,new)
text = text.replace("d.open=title==='Bottle'","d.open=title==='Particles'")
text = text.replace("panel.querySelector('details:nth-child(3)')!.setAttribute('open','')","panel.querySelectorAll('details')[1]!.setAttribute('open','')")
text = text.replace("(panel.querySelectorAll('details')[2] as HTMLDetailsElement).open","(panel.querySelectorAll('details')[1] as HTMLDetailsElement).open")
studio.write_text(text,encoding="utf-8")
