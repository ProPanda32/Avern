from pathlib import Path
hero=Path("source/src/hero.ts")
text=hero.read_text(encoding="utf-8")
old_import="import { createCreatorStudio } from './creator-studio'"
assert text.count(old_import)==1
text=text.replace(old_import,old_import+"\nimport { mountPresentation } from './presentation-redesign'")
start=text.index("const deckList=app.querySelector<HTMLDivElement>('.presentation-slides')!")
end=text.index("const hero=app.querySelector<HTMLElement>('.site-hero')!",start)
text=text[:start]+"mountPresentation(app)\n"+text[end:]
hero.write_text(text,encoding="utf-8")
