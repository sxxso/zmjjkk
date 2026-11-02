(() => {
'use strict';
const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
const motionQuery=matchMedia('(prefers-reduced-motion: reduce)');
let saved=null;try{saved=localStorage.getItem('kk-motion')}catch{}
let reduced=saved===null?motionQuery.matches:saved==='reduce';
const animated=!!window.gsap&&!!window.ScrollTrigger;
if(animated)gsap.registerPlugin(ScrollTrigger);
const contours=`<svg viewBox="0 0 1440 1000" preserveAspectRatio="xMidYMid slice"><path d="M-160 180C90-160 350 380 550 80S1050-60 1110 180 1530 130 1630-70M-180 280C100-50 380 480 620 170S1100 20 1170 290 1510 220 1660 80M-100 440C130 250 320 590 550 370S920 200 1060 440 1290 350 1540 310M-200 680C150 400 310 850 590 610S870 350 990 680 1360 510 1630 520M-190 910C110 580 340 1090 610 830S930 600 1080 910 1360 820 1550 700M160-100C-90 160 230 250 130 490S410 850 230 1140M780-120C520 130 870 290 730 490S960 760 760 1140M1310-100C1130 160 1350 310 1240 580S1480 840 1280 1120"/></svg>`;
$$('.contours').forEach(e=>e.innerHTML=contours);
// One displaced organic field replaces fixed strips. Its source subjects remain transparent.
const hero=$('.hero'),heroViewport=$('.hero-viewport'),canvas=$('#hero-reveal'),ctx=canvas.getContext('2d');
const base=document.createElement('canvas'),alt=document.createElement('canvas'),mask=document.createElement('canvas'),mix=document.createElement('canvas'),fluid=document.createElement('canvas');
const bctx=base.getContext('2d'),actx=alt.getContext('2d'),mctx=mask.getContext('2d'),xctx=mix.getContext('2d'),fctx=fluid.getContext('2d');
const player=new Image(),jett=new Image();
let w=0,h=0,dpr=1,ready=false,frame=0,inView=true,lastTime=0,full=false,fieldPixels=null,fw=0,fh=0;
let cover=0,hover=0,inside=false,px=0,py=0,tx=0,ty=0,tilt=0,lastRaster=0;
const noise=new Float32Array(256*256);
for(let y=0;y<256;y++)for(let x=0;x<256;x++){
 const a=x/256*Math.PI*2,b=y/256*Math.PI*2;
 noise[y*256+x]=.5+.20*Math.sin(a+Math.sin(b*2)*.9)+.15*Math.cos(b*2+Math.sin(a)*1.2)+.11*Math.sin(a*3-b*2);
}
function resize(){w=heroViewport.clientWidth;h=heroViewport.clientHeight;dpr=Math.min(devicePixelRatio||1,1.35);[canvas,base,alt,mask,mix].forEach(c=>{c.width=Math.round(w*dpr);c.height=Math.round(h*dpr)});[ctx,bctx,actx,mctx,xctx].forEach(c=>c.setTransform(dpr,0,0,dpr,0,0));fw=w<700?150:260;fh=Math.round(fw*h/w);fluid.width=fw;fluid.height=fh;fieldPixels=fctx.createImageData(fw,fh);px=tx=w/2;py=ty=h*.46;prepare();}
function prepare(){if(!w||!player.naturalWidth||!jett.naturalWidth)return;bctx.clearRect(0,0,w,h);actx.clearRect(0,0,w,h);const scale=h*(w<700?.00136:.00162);bctx.drawImage(player,w/2-680*scale,h*(w<700?.13:.085),player.naturalWidth*scale,player.naturalHeight*scale);actx.drawImage(jett,w/2-775*scale,h*(w<700?.13:.085)-80*scale,jett.naturalWidth*scale,jett.naturalHeight*scale);ready=true;hero.classList.add('canvas-ready');hero.dataset.revealMethod='organic-field';requestPaint();}
function requestPaint(){if(!frame&&inView&&!document.hidden&&ready)frame=requestAnimationFrame(paint)}
function organicField(time){
 const data=fieldPixels.data,phase=time*.00035,ox=px/w*53+Math.sin(phase)*13,oy=py/h*47+phase*7;
 for(let y=0;y<fh;y++){
  const v=y/fh,sy=v*252+oy,iy=Math.floor(sy),fy=sy-iy,dy=(v-py/h)*.88;
  const row0=(iy&255)*256,row1=((iy+1)&255)*256;
  for(let x=0;x<fw;x++){
   const u=x/fw,sx=u*216+ox,ix=Math.floor(sx),fx=sx-ix,dx=(u-px/w)*1.15;
   const n0=noise[row0+(ix&255)]*(1-fx)+noise[row0+((ix+1)&255)]*fx;
   const n1=noise[row1+(ix&255)]*(1-fx)+noise[row1+((ix+1)&255)]*fx;
   const threshold=1.10-hover*.70+(dx*dx+dy*dy)*1.15;
   const t=Math.max(0,Math.min(1,(n0*(1-fy)+n1*fy-threshold+.012)/.024));
   const i=(y*fw+x)*4;data[i]=data[i+1]=data[i+2]=255;data[i+3]=Math.round(t*t*(3-2*t)*255);
  }
 }
 fctx.putImageData(fieldPixels,0,0);mctx.imageSmoothingEnabled=true;mctx.drawImage(fluid,0,0,w,h);
}
function paint(time){
 frame=0;if(!ready||!inView||document.hidden)return;
 if(!reduced&&inside&&time-lastRaster<25){requestPaint();return}lastRaster=time;
 const dt=Math.min(50,time-(lastTime||time-16));lastTime=time;const ease=1-Math.pow(.80,dt/16.67),wanted=full?1:0,wantedHover=inside&&!reduced&&!full?1:0;
 cover=reduced?wanted:cover+(wanted-cover)*ease*.58;hover+=(wantedHover-hover)*ease;px+=(tx-px)*ease;py+=(ty-py)*ease;tilt+=(((tx/w)-.5)*14-tilt)*ease;
 if(Math.abs(cover-wanted)<.001)cover=wanted;if(Math.abs(hover-wantedHover)<.001)hover=wantedHover;
 mctx.clearRect(0,0,w,h);mctx.fillStyle='#fff';
 if(hover>.001&&cover<.99)organicField(time);
 if(cover>.001){mctx.beginPath();mctx.ellipse(w*.5,h*.45,Math.hypot(w,h)*cover,Math.hypot(w,h)*cover,0,0,Math.PI*2);mctx.fill()}
 if(cover<.002){mctx.globalCompositeOperation='destination-in';mctx.save();mctx.translate(reduced?0:tilt,0);mctx.drawImage(alt,0,0,w,h);mctx.restore();mctx.globalCompositeOperation='source-over';}
 ctx.clearRect(0,0,w,h);ctx.save();ctx.translate(reduced?0:tilt,0);ctx.drawImage(base,0,0,w,h);ctx.restore();ctx.globalCompositeOperation='destination-out';ctx.drawImage(mask,0,0,w,h);ctx.globalCompositeOperation='source-over';
 xctx.clearRect(0,0,w,h);xctx.save();xctx.translate(reduced?0:tilt,0);xctx.drawImage(alt,0,0,w,h);xctx.restore();xctx.globalCompositeOperation='destination-in';xctx.drawImage(mask,0,0,w,h);xctx.globalCompositeOperation='source-over';ctx.drawImage(mix,0,0,w,h);
 hero.dataset.revealState=full?'jett':hover>.02?'hover':'player';
 if((inside&&!reduced&&!full)||Math.abs(cover-wanted)>.0001||Math.abs(hover-wantedHover)>.0001||Math.abs(px-tx)>.15||Math.abs(py-ty)>.15||Math.abs(tilt-(tx/w-.5)*14)>.15)requestPaint();
}
function point(e){if(Number(hero.dataset.zoomProgress||0)>.04)return;const r=canvas.getBoundingClientRect();tx=(e.clientX-r.left)*w/r.width;ty=(e.clientY-r.top)*h/r.height;inside=true;requestPaint()}
canvas.addEventListener('pointerenter',point);canvas.addEventListener('pointermove',point);canvas.addEventListener('pointerdown',point);
function leave(){inside=false;tx=w/2;requestPaint()}
canvas.addEventListener('pointerleave',leave);canvas.addEventListener('pointercancel',leave);canvas.addEventListener('pointerup',e=>{if(e.pointerType!=='mouse')leave()});
$('#reveal-toggle').addEventListener('click',()=>{full=!full;$('#reveal-toggle').setAttribute('aria-pressed',String(full));$('#hero-hint').textContent=full?'捷风 / Jett':'划过人物，唤醒捷风';requestPaint()});
if(matchMedia('(pointer:coarse)').matches)$('#hero-hint').textContent='滑动人物，唤醒捷风';
new ResizeObserver(resize).observe(heroViewport);new IntersectionObserver(entries=>{inView=entries[0].isIntersecting;if(inView){lastTime=0;requestPaint()}else{cancelAnimationFrame(frame);frame=0;inside=false;}},{threshold:0}).observe(heroViewport);
player.onload=prepare;jett.onload=prepare;player.src='assets/kangkang-cutout.webp';jett.src='assets/jett-pose-v3.webp';
player.onerror=jett.onerror=()=>{hero.classList.remove('canvas-ready');$('#hero-hint').textContent='图片暂未加载完成，请刷新重试'};
document.addEventListener('visibilitychange',()=>{if(document.hidden){cancelAnimationFrame(frame);frame=0}else{lastTime=0;requestPaint()}});
const gallery=$('.gallery'),galleryWindow=$('.gallery-window'),shots=$$('.shot');
let motionContext=null,media=null,galleryTrigger=null,agentTween=null;
function progress(p){$('.gallery-progress i').style.transform=`scaleX(${Math.max(.03,Math.min(1,p))})`;$('.gallery-caption').style.opacity=Math.max(0,1-p*12);const center=p*(gallery.scrollWidth-galleryWindow.clientWidth)+galleryWindow.clientWidth*.4;const nearest=shots.reduce((a,b)=>Math.abs(a.offsetLeft-center)<Math.abs(b.offsetLeft-center)?a:b);$$('[data-gallery-year]').forEach(b=>b.setAttribute('aria-current',String(b.dataset.galleryYear===nearest.dataset.year)))}
function configureMotion(){
 media?.revert();motionContext?.revert();galleryTrigger=null;document.documentElement.classList.toggle('reduced-motion',reduced);
 hero.dataset.zoomProgress='0';$('#motion-resume').hidden=!reduced;$('#motion-toggle').textContent=`减少动态：${reduced?'开':'关'}`;$('#motion-toggle').setAttribute('aria-pressed',String(reduced));
 galleryWindow.style.overflowX='auto';$('[data-count]').textContent='111';inside=false;hover=0;cover=full?1:0;requestPaint();
 agentTween?.kill();if(animated)gsap.set('.agent-details',{clearProps:'opacity,transform'});
 if(!animated||reduced){updateHeader();return}
 motionContext=gsap.context(()=>{
  const intro=gsap.timeline({scrollTrigger:{trigger:'.hero-shell',start:'top top',end:'bottom bottom',scrub:.8,onUpdate:self=>{hero.dataset.zoomProgress=self.progress.toFixed(3);if(self.progress>.04&&inside)leave();updateHeader()}}});
  intro.fromTo('.hero-viewport',{scale:1,filter:'brightness(1) saturate(1)'},{scale:()=>innerWidth<700?.70:.34,filter:'brightness(.53) saturate(.35)',duration:.82,ease:'power2.inOut'},0)
   .fromTo('.hero-message',{autoAlpha:0,y:35},{autoAlpha:1,y:0,duration:.45,ease:'power2.out'},.47)
   .fromTo('.hero-marquee',{opacity:0},{opacity:1,duration:.5},.25)
   .fromTo('.hero-marquee>div:first-child',{xPercent:-12},{xPercent:6,duration:1,ease:'none'},0)
   .fromTo('.hero-marquee>div:last-child',{xPercent:2},{xPercent:-16,duration:1,ease:'none'},0)
   .fromTo('.signature-trigger',{clipPath:'inset(0 100% 0 0)'},{clipPath:'inset(0 0% 0 0)',duration:.48,ease:'power2.inOut'},.48)
   .to('.champion-badge,.hero-tools,.scroll-cue',{autoAlpha:0,duration:.2,ease:'none'},0);
  const faces=gsap.timeline({scrollTrigger:{trigger:'.faceoff',start:'top bottom',end:'top top',scrub:1}});
  faces.fromTo('.faceoff-jett',{xPercent:-42,yPercent:12,scale:1.15},{xPercent:0,yPercent:0,scale:1,duration:1,ease:'power2.out'},0)
   .fromTo('.faceoff-kk',{xPercent:42,yPercent:12,scale:1.15},{xPercent:0,yPercent:0,scale:1,duration:1,ease:'power2.out'},0)
   .fromTo('.faceoff-links',{y:55,opacity:0},{y:0,opacity:1,duration:.5},.45);
  gsap.fromTo('.manifesto h2>span',{y:60,opacity:.18},{y:0,opacity:1,stagger:.1,ease:'none',scrollTrigger:{trigger:'.manifesto',start:'top 65%',end:'center 48%',scrub:.7}});
  media=gsap.matchMedia();media.add('(min-width:701px)',()=>{
   galleryWindow.scrollLeft=0;galleryWindow.style.overflowX='hidden';
   const distance=()=>Math.max(0,gallery.scrollWidth-innerWidth);
   const tl=gsap.timeline({scrollTrigger:{trigger:'.moments-stage',start:'top top',end:()=>'+='+distance()*1.05,pin:true,scrub:1,invalidateOnRefresh:true,onUpdate:s=>progress(s.progress)}});
   tl.to(gallery,{x:()=>-distance(),duration:1,ease:'none'},0);
   shots.forEach(e=>tl.fromTo(e,{y:()=>Number(e.dataset.depth)*innerHeight},{y:()=>-Number(e.dataset.depth)*innerHeight,duration:1,ease:'none'},0));
   tl.to('.moments .contours',{xPercent:-9,rotation:6,duration:1,ease:'none'},0);galleryTrigger=tl.scrollTrigger;
   return()=>{galleryTrigger=null;galleryWindow.style.overflowX='auto'};
  });
  gsap.fromTo('.agent-card',{y:i=>i%2?140:70},{y:0,ease:'none',scrollTrigger:{trigger:'.agent-cards',start:'top bottom',end:'center 55%',scrub:1}});
  gsap.fromTo('.champion-image',{clipPath:'inset(0 6%)'},{clipPath:'inset(0 0%)',ease:'none',scrollTrigger:{trigger:'.champion',start:'top 85%',end:'top top',scrub:1}});
  gsap.fromTo('.champion-image img',{scale:1.13,yPercent:-4},{scale:1,yPercent:4,ease:'none',scrollTrigger:{trigger:'.champion',start:'top bottom',end:'bottom top',scrub:1}});
  const count={n:0};gsap.to(count,{n:111,duration:1.6,ease:'power2.out',scrollTrigger:{trigger:'.kill-stat',start:'top 85%',once:true},onUpdate:()=>{$('[data-count]').textContent=Math.round(count.n)}});
  gsap.to('.watch-photo-a',{xPercent:22,yPercent:22,rotation:3,ease:'none',scrollTrigger:{trigger:'.watch',start:'top bottom',end:'bottom top',scrub:1}});
  gsap.to('.watch-photo-b',{xPercent:-22,yPercent:-22,rotation:-4,ease:'none',scrollTrigger:{trigger:'.watch',start:'top bottom',end:'bottom top',scrub:1}});
 });updateHeader();
}
$('#motion-toggle').addEventListener('click',()=>{reduced=!reduced;try{localStorage.setItem('kk-motion',reduced?'reduce':'full')}catch{}configureMotion()});
$('#motion-resume').addEventListener('click',()=>$('#motion-toggle').click());
motionQuery.addEventListener('change',()=>{let c=null;try{c=localStorage.getItem('kk-motion')}catch{}if(c===null){reduced=motionQuery.matches;configureMotion()}});
function stepGallery(dir){if(galleryTrigger){const p=Math.max(0,Math.min(1,galleryTrigger.progress+dir*.24));scrollTo({top:galleryTrigger.start+(galleryTrigger.end-galleryTrigger.start)*p,behavior:'smooth'})}else galleryWindow.scrollBy({left:innerWidth*.9*dir,behavior:reduced?'instant':'smooth'})}
$$('[data-gallery-step]').forEach(b=>b.addEventListener('click',()=>stepGallery(Number(b.dataset.galleryStep))));
$$('[data-gallery-year]').forEach(b=>b.addEventListener('click',()=>{const shot=shots.find(s=>s.dataset.year===b.dataset.galleryYear);const distance=Math.max(1,gallery.scrollWidth-galleryWindow.clientWidth);const x=Math.max(0,Math.min(distance,shot.offsetLeft-galleryWindow.clientWidth*.08));if(galleryTrigger)scrollTo({top:galleryTrigger.start+(galleryTrigger.end-galleryTrigger.start)*x/distance,behavior:reduced?'instant':'smooth'});else galleryWindow.scrollTo({left:x,behavior:reduced?'instant':'smooth'})}));
gallery.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();stepGallery(e.key==='ArrowRight'?1:-1)}});
galleryWindow.addEventListener('scroll',()=>{if(!galleryTrigger)progress(galleryWindow.scrollLeft/Math.max(1,galleryWindow.scrollWidth-galleryWindow.clientWidth))},{passive:true});
let drag=null,suppress=false;
galleryWindow.addEventListener('pointerdown',e=>{if(e.pointerType!=='mouse'||e.button!==0)return;drag={x:e.clientX,scroll:galleryWindow.scrollLeft,page:scrollY};suppress=false});
galleryWindow.addEventListener('pointermove',e=>{if(!drag)return;const dx=e.clientX-drag.x;if(Math.abs(dx)>7){suppress=true;galleryWindow.setPointerCapture(e.pointerId);if(galleryTrigger)scrollTo({top:Math.max(galleryTrigger.start,Math.min(galleryTrigger.end,drag.page-dx*1.5)),behavior:'instant'});else galleryWindow.scrollLeft=drag.scroll-dx}});
function endDrag(){drag=null;setTimeout(()=>suppress=false,80)}galleryWindow.addEventListener('pointerup',endDrag);galleryWindow.addEventListener('pointercancel',endDrag);window.addEventListener('pointerup',endDrag);
const closing=new WeakSet();
function openDialog(d){if(d.open)return;d.showModal();if(!animated||reduced)return;gsap.killTweensOf(d);if(d.id==='menu-dialog'){gsap.fromTo(d,{clipPath:'inset(0 0 100% 0 round 0 0 30% 30%)'},{clipPath:'inset(0 0 0% 0 round 0 0 0% 0%)',duration:.7,ease:'power3.inOut',clearProps:'clipPath'});gsap.fromTo('#menu-dialog nav a',{y:70,opacity:0},{y:0,opacity:1,delay:.25,duration:.6,stagger:.06,ease:'power3.out',clearProps:'opacity,transform'});}else gsap.fromTo(d,{opacity:0,scale:.97},{opacity:1,scale:1,duration:.25,clearProps:'opacity,transform'})}
function closeDialog(d,after){if(closing.has(d))return;closing.add(d);const done=()=>{d.close();closing.delete(d);if(animated)gsap.set(d,{clearProps:'transform,opacity,clipPath'});after?.()};if(!reduced&&animated&&d.id==='menu-dialog')gsap.to(d,{yPercent:-100,duration:.45,ease:'power3.inOut',onComplete:done});else done()}
$('.menu-toggle').addEventListener('click',()=>openDialog($('#menu-dialog')));
$$('dialog').forEach(d=>{$('.dialog-close',d).addEventListener('click',()=>closeDialog(d));d.addEventListener('cancel',e=>{e.preventDefault();closeDialog(d)});d.addEventListener('click',e=>{if(e.target===d){const r=d.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)closeDialog(d)}})});
// Explicit navigation animation avoids CSS smooth-scroll interfering with pin measurements.
$$('a[href^="#"]').filter(a=>!a.closest('#menu-dialog')&&!a.classList.contains('skip')).forEach(a=>a.addEventListener('click',e=>{const target=$(a.getAttribute('href'));if(!target)return;e.preventDefault();target.scrollIntoView({behavior:reduced?'instant':'smooth'})}));
let resizeRefresh=0;addEventListener('resize',()=>{clearTimeout(resizeRefresh);resizeRefresh=setTimeout(()=>window.ScrollTrigger?.refresh(),220)});
$$('#menu-dialog nav a').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();closeDialog($('#menu-dialog'),()=>{$(a.getAttribute('href')).scrollIntoView({behavior:reduced?'instant':'smooth'})})}));
$$('[data-open]').forEach(b=>b.addEventListener('click',()=>openDialog(document.getElementById(b.dataset.open))));
let photoIndex=0;function showPhoto(index){photoIndex=(index+shots.length)%shots.length;const b=shots[photoIndex];$('#photo-dialog>img').src=b.dataset.photo;$('#photo-dialog>img').alt=$('img',b).alt;$('#photo-dialog>p').textContent=b.dataset.caption;$('#photo-source').href=b.dataset.source;openDialog($('#photo-dialog'))}
shots.forEach((b,i)=>b.addEventListener('click',e=>{if(suppress){e.preventDefault();return}showPhoto(i)}));$('#photo-prev').addEventListener('click',()=>showPhoto(photoIndex-1));$('#photo-next').addEventListener('click',()=>showPhoto(photoIndex+1));$('#photo-dialog').addEventListener('keydown',e=>{if(e.key==='ArrowLeft')showPhoto(photoIndex-1);if(e.key==='ArrowRight')showPhoto(photoIndex+1)});
const agents=window.KK_AGENT_DATA.agents,tabs=$$('.agent-card');let selected='jett';
function chooseAgent(id){const a=agents.find(a=>a.id===id);if(!a||selected===id)return;selected=id;agentTween?.kill();$('.agents').style.setProperty('--agent-accent',a.color);$('#agent-name').textContent=a.name;$('#agent-en').textContent=id[0].toUpperCase()+id.slice(1)+'.';$('#agent-maps').textContent=a.maps;$('#agent-use').textContent=a.use;$('#agent-acs').textContent=a.acs;$('#agent-kd').textContent=a.kd;$('#agent-kills').textContent=a.kills.toLocaleString('en-US');$('#agent-fk').textContent=a.firstKills.toLocaleString('en-US');$('#agent-panel').setAttribute('aria-labelledby','tab-'+id);tabs.forEach(b=>{b.setAttribute('aria-selected',String(b.dataset.agent===id));b.tabIndex=b.dataset.agent===id?0:-1});$('#agent-announcement').textContent=`${a.name}，${a.maps} 张职业地图，ACS ${a.acs}，击杀死亡比 ${a.kd}`;if(animated&&!reduced)agentTween=gsap.fromTo('.agent-details',{y:18,opacity:.2},{y:0,opacity:1,duration:.45,ease:'power2.out',clearProps:'transform,opacity'})}
tabs.forEach((b,i)=>{b.addEventListener('click',()=>chooseAgent(b.dataset.agent));b.addEventListener('keydown',e=>{let n=i;if(e.key==='ArrowRight')n=(i+1)%tabs.length;else if(e.key==='ArrowLeft')n=(i-1+tabs.length)%tabs.length;else if(e.key==='Home')n=0;else if(e.key==='End')n=tabs.length-1;else return;e.preventDefault();tabs[n].focus();chooseAgent(tabs[n].dataset.agent)})});
$$('.maps details').forEach(d=>d.addEventListener('toggle',()=>{if(d.open)$$('.maps details').filter(x=>x!==d).forEach(x=>x.open=false);window.ScrollTrigger?.refresh()}));
function updateHeader(){$('.header').classList.toggle('scrolled',scrollY>innerHeight*.35);const el=document.elementFromPoint(innerWidth*.25,35);const heroDark=scrollY<$('.hero-shell').offsetHeight&&(Number(hero.dataset.zoomProgress||0)>.14||(reduced&&scrollY>heroViewport.clientHeight-60));$('.header').classList.toggle('on-dark',heroDark||!!el?.closest('.manifesto,.agents,.champion,footer'))}
let queued=false;addEventListener('scroll',()=>{if(!queued){queued=true;requestAnimationFrame(()=>{updateHeader();queued=false})}},{passive:true});
configureMotion();document.fonts.ready.then(()=>window.ScrollTrigger?.refresh());addEventListener('load',()=>{window.ScrollTrigger?.refresh();updateHeader()});
})();
