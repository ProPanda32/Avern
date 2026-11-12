import './presentation-redesign.css'

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
      card.className='original-slide'
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
      card.append(header,button,footer)
      list.append(card)
    })
  }).catch(error=>{console.error(error);list.textContent='Presentation slides could not load.'})
}
