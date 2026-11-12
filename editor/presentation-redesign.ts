import './presentation-redesign.css'

function makeEvidenceSlide(url:string,open:()=>void){
  const card=document.createElement('article')
  card.className='deck-slide evidence-slide'
  card.setAttribute('role','listitem')
  card.setAttribute('aria-label','Why it matters: case studies and credibility evidence')
  const crop=(kind:string,label:string)=>'<div class="evidence-crop evidence-crop--'+kind+'"><img src="'+url+'" alt="'+label+'"></div>'
  card.innerHTML='<div class="evidence-top"><strong>AVERNA <span>✳</span></strong><span>02 / EXISTING EXAMPLES</span></div><div class="evidence-heading"><div><small>WHY IT MATTERS / EVIDENCE</small><h2>Interaction, backed by examples.</h2></div><button type="button" class="evidence-original">View original slide ↗</button></div><div class="evidence-grid"><section class="evidence-panel evidence-chart"><div class="evidence-label">01 / DESIGN CREDIBILITY</div>'+crop('chart','Stanford chart of website credibility and design look')+'<p>How people evaluate a website’s credibility</p><small>Source: Stanford Web Credibility Research</small></section><div class="evidence-cases"><section class="evidence-panel evidence-case"><div class="evidence-label">02 / AUDEMARS PIGUET</div><div class="evidence-case-body">'+crop('audemars','Audemars Piguet House of Wonders')+'<div class="evidence-stats"><div><strong>80%</strong><span>engagement rate</span></div><div><strong>10+ min</strong><span>average visit</span></div><div><strong>311K</strong><span>visits in three months</span></div></div></div><small>House of Wonders · Make Me Pulse</small></section><section class="evidence-panel evidence-case"><div class="evidence-label">03 / REBECCA MINKOFF</div><div class="evidence-case-body">'+crop('rebecca','Rebecca Minkoff interactive shopping example')+'<div class="evidence-rebecca"><blockquote>“3D media makes for a more interactive shopping experience. Customers can examine our products from every angle, including the option to view products in augmented reality, which helps them get a better sense of quality, size, and other details that matter.”</blockquote><div class="evidence-stats"><div><strong>44%</strong><span>more likely to add to cart</span></div><div><strong>27%</strong><span>more likely to order after 3D</span></div><div><strong>65%</strong><span>more likely to order after AR</span></div></div></div></div><small>Case study · Shopify</small></section></div></div><div class="evidence-bottom"><span>Sources and full quotation available in the original slide</span><span>AVERNA · 03 / 09</span></div>'
  card.querySelector<HTMLButtonElement>('.evidence-original')!.addEventListener('click',open)
  return card
}

export function mountPresentation(app:HTMLElement){
  const list=app.querySelector<HTMLElement>('.presentation-slides')!
  const viewer=app.querySelector<HTMLDialogElement>('#deck-viewer')!
  const viewerImage=viewer.querySelector<HTMLImageElement>('img')!
  fetch('/Avern/slides/manifest.json').then(async response=>{
    if(!response.ok)throw new Error('Presentation slides are unavailable')
    return await response.json() as string[]
  }).then(files=>{
    files.forEach((file,index)=>{
      if(index===2){
        const url='/Avern/slides/'+encodeURIComponent(file)+'?v=gradient-1'
        list.append(makeEvidenceSlide(url,()=>{viewerImage.src=url;viewerImage.alt='Original Averna PowerPoint slide 3';viewer.style.backgroundColor='#071719';viewerImage.style.mixBlendMode='normal';viewer.showModal()}))
        return
      }
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
