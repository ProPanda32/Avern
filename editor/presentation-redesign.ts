import './presentation-redesign.css'

type Slide={title:string;kicker:string;variant:string;items?:string[];quote?:string;note?:string;metric?:[string,string][];source?:boolean}
const slides:Slide[]=[
  {title:'The problem',kicker:'01 / The challenge',variant:'problem',items:['Digital experiences often feel static and generic.','Businesses struggle to present products and services in engaging, memorable ways.','Finding a trustworthy creative provider can be difficult.'],source:true},
  {title:'Why it matters',kicker:'02 / The opportunity',variant:'matters',items:['AI makes conventional digital content easier to produce, increasing competition.','Poor presentation can reduce customer interest, trust and engagement.','3D interactive experiences can improve understanding, engagement and brand memorability.','Businesses are already investing in these experiences.']},
  {title:'The evidence is visible',kicker:'03 / Existing examples',variant:'examples',items:['Audemars Piguet — House of Wonders','Rebecca Minkoff — interactive commerce'],note:'The original slide includes case studies and credibility research links.',source:true},
  {title:'Business owner feedback',kicker:'04 / Listen first',variant:'feedback',quote:'“The question is whether that interaction helps the business achieve its goal.”',items:['Understand how the brand’s customers want to explore and buy.','Test interaction with a selected product category before expanding.','The right level of interactivity depends on the business and use case.','A hybrid experience can serve both interactive and conventional preferences.'],source:true},
  {title:'Two landing pages. One clear preference.',kicker:'05 / Nocturne comparison',variant:'comparison',metric:[['~70%','Interactive'],['~30%','Conventional']],items:['About 60 people compared the two websites.','Most replies selected Website 1 or Website 2; the split is approximate.'],note:'Respondents were asked about engagement, product interest and what could be improved.'},
  {title:'In their own words',kicker:'06 / Respondent reactions',variant:'responses',items:['Original respondent screenshots are preserved in the source slide.'],source:true},
  {title:'More voices from the comparison',kicker:'07 / Respondent reactions',variant:'responses',items:['Additional original respondent screenshots are preserved in the source slide.'],source:true},
  {title:'Who I want to work with',kicker:'08 / Target customers',variant:'customers',items:['Visually driven businesses where presentation influences how customers understand value.','Teams seeking to communicate clearly, stand apart and add a richer layer for users.','The initial focus spans multiple industries while learning which customers benefit most.']},
  {title:'A signal of demand',kicker:'09 / Real outreach',variant:'outreach',items:['An introduction from a networking event at Soho House led to an email about the work.','The response suggests potential commercial demand for creative websites and interactive experiences.','Portfolio led businesses may especially value work that impresses prospective clients.'],source:true}
]

export function mountPresentation(app:HTMLElement){
  const list=app.querySelector<HTMLElement>('.presentation-slides')!
  const viewer=app.querySelector<HTMLDialogElement>('#deck-viewer')!
  const viewerImage=viewer.querySelector<HTMLImageElement>('img')!
  const esc=(value:string)=>value.replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]!))
  const image=(index:number)=>'/Avern/slides/slide-'+(index+1)+'.png'
  slides.forEach((slide,index)=>{
    const card=document.createElement('article')
    card.className='av-slide av-slide--'+slide.variant
    card.setAttribute('aria-label','Presentation slide '+(index+1)+': '+slide.title)
    const num=String(index+1).padStart(2,'0')
    const items=slide.items?.map((item,i)=>'<li><span class="av-item-no">'+String(i+1).padStart(2,'0')+'</span><span>'+esc(item)+'</span></li>').join('')||''
    const metrics=slide.metric?.map(([value,label])=>'<div class="av-metric"><strong>'+esc(value)+'</strong><span>'+esc(label)+'</span></div>').join('')||''
    const evidence=slide.source?'<button class="av-source" type="button" aria-label="View original slide '+(index+1)+'">View original slide <span aria-hidden="true">↗</span></button>':''
    const sourceVisual=slide.source?'<div class="av-evidence"><img src="'+image(index)+'" alt="Original presentation slide '+(index+1)+'" loading="lazy"></div>':''
    card.innerHTML='<div class="av-orbit" aria-hidden="true"></div><div class="av-top"><span class="av-brand">AVERNA<span class="av-brand-mark">✳</span></span><span class="av-kicker">'+esc(slide.kicker)+'</span></div><div class="av-main"><div class="av-copy"><div class="av-index">'+num+' <span>—</span> 09</div><h2>'+esc(slide.title)+'</h2>'+(slide.quote?'<blockquote>'+esc(slide.quote)+'</blockquote>':'')+(metrics?'<div class="av-metrics">'+metrics+'</div>':'')+(items?'<ol>'+items+'</ol>':'')+(slide.note?'<p class="av-note">'+esc(slide.note)+'</p>':'')+evidence+'</div>'+sourceVisual+'</div><div class="av-bottom"><span>Design · Create · Innovate</span><span>'+num+' / 09</span></div>'
    card.querySelector<HTMLButtonElement>('.av-source')?.addEventListener('click',()=>{viewerImage.src=image(index);viewerImage.alt='Original presentation slide '+(index+1);viewer.showModal()})
    list.append(card)
  })
}
