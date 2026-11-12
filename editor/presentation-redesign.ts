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
      const button=document.createElement('button')
      button.className='deck-slide'
      button.type='button'
      button.setAttribute('role','listitem')
      button.setAttribute('aria-label','Open original presentation slide '+(index+1))
      const image=document.createElement('img')
      image.src='/Avern/slides/'+encodeURIComponent(file)
      image.alt='Original Averna PowerPoint slide '+(index+1)
      image.loading=index===0?'eager':'lazy'
      button.append(image)
      button.addEventListener('click',()=>{viewerImage.src=image.src;viewerImage.alt=image.alt;viewer.style.backgroundColor='#071719';viewerImage.style.mixBlendMode='normal';viewer.showModal()})
      list.append(button)
    })
  }).catch(error=>{console.error(error);list.textContent='Presentation slides could not load.'})
}
