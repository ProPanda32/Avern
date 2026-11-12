import './presentation-redesign.css'

const chapters=[
  {title:'The problem',eyebrow:'01 / The challenge',accent:'#a6f3cf'},
  {title:'Why it matters',eyebrow:'02 / The opportunity',accent:'#81d8fa'},
  {title:'The case for interaction',eyebrow:'03 / Examples and research',accent:'#e8c18a'},
  {title:'Business owner feedback',eyebrow:'04 / Listen first',accent:'#dbc4f8'},
  {title:'The Nocturne comparison',eyebrow:'05 / Consumer response',accent:'#91e7d8'},
  {title:'What respondents said',eyebrow:'06 / Original responses',accent:'#e9b5ce'},
  {title:'More respondent voices',eyebrow:'07 / Original responses',accent:'#e9b5ce'},
  {title:'Who I want to work with',eyebrow:'08 / Target customers',accent:'#b7d2ff'},
  {title:'A signal of demand',eyebrow:'09 / Real outreach',accent:'#f2d294'}
]

export function mountPresentation(app:HTMLElement){
  const list=app.querySelector<HTMLElement>('.presentation-slides')!
  const viewer=app.querySelector<HTMLDialogElement>('#deck-viewer')!
  const viewerImage=viewer.querySelector<HTMLImageElement>('img')!
  fetch('/Avern/slides/manifest.json').then(async response=>{
    if(!response.ok)throw new Error('Presentation slides are unavailable')
    return await response.json() as string[]
  }).then(files=>{
    files.forEach((file,index)=>{
      const number=String(index+1).padStart(2,'0')
      const card=document.createElement('article')
      card.className='original-slide combined-slide'
      const chapter=chapters[index]
      card.style.setProperty('--slide-accent',chapter?.accent||'#a6f3cf')
      card.setAttribute('aria-label','Original Averna presentation slide '+(index+1))
      const header=document.createElement('div')
      header.className='original-slide-header'
      const brand=document.createElement('span')
      brand.textContent='AVERNA / PRESENTATION'
      const count=document.createElement('span')
      count.textContent=number+' / '+String(files.length).padStart(2,'0')
      header.append(brand,count)
      const button=document.createElement('button')
      button.className='original-slide-image'
      button.type='button'
      button.setAttribute('aria-label','Enlarge original slide '+(index+1))
      const image=document.createElement('img')
      image.src='/Avern/slides/'+encodeURIComponent(file)
      image.alt='Original Averna PowerPoint slide '+(index+1)
      image.loading=index===0?'eager':'lazy'
      button.append(image)
      button.addEventListener('click',()=>{viewerImage.src=image.src;viewerImage.alt=image.alt;viewer.showModal()})
      const footer=document.createElement('div')
      footer.className='original-slide-footer'
      footer.innerHTML='<span>Original slide · all text and imagery preserved</span><span>Click to enlarge ↗</span>'
      const feature=document.createElement('div')
      feature.className='combined-slide-feature'
      const eyebrow=document.createElement('span')
      eyebrow.className='combined-slide-eyebrow'
      eyebrow.textContent=chapter?.eyebrow||'Original presentation'
      const title=document.createElement('h2')
      title.textContent=chapter?.title||'Averna presentation slide '+(index+1)
      const caption=document.createElement('p')
      caption.textContent='The complete original slide appears below, with all of its information and images.'
      feature.append(eyebrow,title,caption)
      card.append(header,feature,button,footer)
      list.append(card)
    })
  }).catch(error=>{console.error(error);list.textContent='Presentation slides could not load.'})
}
