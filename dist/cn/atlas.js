(() => {
'use strict';
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)],data=window.VCT_CATALOG;
const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
const players=data.players,teams=data.teams,grid=$('#player-grid');
let team='all',query='',role='all',order='team',includeBench=true,view='grid';
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const img=(src,cls,alt,loading='lazy')=>`<img src="${esc(src)}" class="${cls}" alt="${esc(alt)}" loading="${loading}" decoding="async">`;
function card(p){return `<a class="player-card" href="${p.url}" style="--accent:${p.color};--team-paper:${p.paper}"><div class="card-image">${p.agentImage?img(p.agentImage,'agent-ghost',''):''}${img(p.portrait,'player-cutout',p.portraitMissing?'暂无公开选手肖像':p.handle)}<div class="card-top">${img('assets/teams/'+p.team.toLowerCase()+'.webp','',p.team)}<span class="roster-tag">${esc(p.portraitMissing?'待补肖像':p.rosterStatus==='阵容选手'?p.team:p.rosterStatus)}</span></div><span class="card-open" aria-hidden="true">↗</span></div><div class="card-caption"><h3>${esc(p.handle)}</h3><span>${esc(p.name)}</span></div><div class="card-foot"><b>${esc(p.team)}</b><span>${esc(p.agentName||'资料收录中')}</span><span>${p.maps?p.maps+' 张地图':'暂无统计'}</span></div></a>`}
function sync(){const hash=new URLSearchParams();if(team!=='all')hash.set('team',team);if(query)hash.set('q',query);if(role!=='all')hash.set('role',role);if(order!=='team')hash.set('sort',order);if(!includeBench)hash.set('active','1');if(view!=='grid')hash.set('view',view);try{history.replaceState(null,'',location.pathname+location.search+(hash.size?'#'+hash:''))}catch{}}
function render(){let shown=players.filter(p=>(team==='all'||p.team===team)&&(!query||[p.handle,p.realName,p.name,p.team,p.teamName].join(' ').toLowerCase().includes(query.toLowerCase()))&&(role==='all'||p.role===role)&&(includeBench||p.rosterStatus==='阵容选手'));
 if(order==='maps')shown.sort((a,b)=>b.maps-a.maps);else if(order==='kills')shown.sort((a,b)=>b.kills-a.kills);else if(order==='name')shown.sort((a,b)=>a.handle.localeCompare(b.handle,'en'));
 const oldHeight=grid.offsetHeight;grid.style.minHeight=Math.min(oldHeight,innerHeight)+'px';grid.innerHTML=shown.map(card).join('');grid.classList.toggle('list-view',view==='list');
 $('#result-count').textContent=`${shown.length} / ${players.length} 位选手`;$('#empty-state').hidden=shown.length>0;
 if(!reduced&&window.gsap&&shown.length)gsap.fromTo([...grid.children],{opacity:0,y:16},{opacity:1,y:0,duration:.4,stagger:{each:.018,amount:Math.min(.35,shown.length*.018)},clearProps:'all'});
 requestAnimationFrame(()=>grid.style.minHeight='');$$('[data-team]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.team===team)));$$('[data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===view)));sync();
}
function restore(){const state=new URLSearchParams(location.hash.slice(1));team=teams.some(t=>t.code===state.get('team'))?state.get('team'):'all';query=state.get('q')||'';role=state.get('role')||'all';order=state.get('sort')||'team';view=state.get('view')==='list'?'list':'grid';includeBench=state.get('active')!=='1';$('#player-search').value=query;$('#role-filter').value=role;$('#sort-order').value=order;$('#include-bench').checked=includeBench;render()}
$$('[data-team]').forEach(b=>b.addEventListener('click',()=>{team=b.dataset.team;render()}));
let searchTimer=0;$('#player-search').addEventListener('input',e=>{query=e.target.value.trim();clearTimeout(searchTimer);searchTimer=setTimeout(render,120)});
$('#clear-search').addEventListener('click',()=>{query='';$('#player-search').value='';$('#player-search').focus();render()});
$('#role-filter').addEventListener('change',e=>{role=e.target.value;render()});$('#sort-order').addEventListener('change',e=>{order=e.target.value;render()});$('#include-bench').addEventListener('change',e=>{includeBench=e.target.checked;render()});
$$('[data-view]').forEach(b=>b.addEventListener('click',()=>{view=b.dataset.view;render()}));$('#reset-filters').addEventListener('click',()=>{try{history.replaceState(null,'',location.pathname)}catch{}restore()});
addEventListener('hashchange',()=>{if(location.hash!=='#directory')restore()});
$$('a[href="#directory"]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();$('#directory').scrollIntoView({behavior:reduced?'instant':'smooth'})}));$('#back-to-top').addEventListener('click',()=>scrollTo({top:0,behavior:reduced?'instant':'smooth'}));
const featured=data.featured.map(id=>players.find(p=>p.id===id)).filter(Boolean);let featuredIndex=0;
function switchCast(dir){featuredIndex=(featuredIndex+dir+featured.length)%featured.length;const cur=featured[featuredIndex],prev=featured[(featuredIndex-1+featured.length)%featured.length],next=featured[(featuredIndex+1)%featured.length];const portraits=$$('.stack-portrait');const apply=()=>{[prev,cur,next].forEach((p,i)=>{portraits[i].src=p.portrait;portraits[i].alt=p.handle});$('#featured-link').href=cur.url;$('#featured-name').textContent=cur.handle;$('#featured-team').textContent=cur.team+' / '+cur.name;$('#cast-announcement').textContent='当前选手 '+cur.handle+'，'+cur.team;};if(!reduced&&window.gsap){gsap.to('.portrait-stack',{opacity:0,y:15,duration:.17,onComplete:()=>{apply();gsap.to('.portrait-stack',{opacity:1,y:0,duration:.5,ease:'power3.out'})}})}else apply()}
$$('[data-cast]').forEach(b=>b.addEventListener('click',()=>switchCast(Number(b.dataset.cast))));
$('.atlas-hero').addEventListener('pointermove',e=>{if(reduced||e.pointerType==='touch'||!window.gsap)return;gsap.to('.portrait-stack',{x:(e.clientX/innerWidth-.5)*18,y:(e.clientY/innerHeight-.5)*10,duration:1.2,ease:'power2.out',overwrite:'auto'})});
if(!reduced&&window.gsap){gsap.from('.hero-copy h1 span',{y:80,opacity:0,stagger:.12,duration:1,ease:'power3.out',clearProps:'all'});gsap.from('.portrait-stack',{opacity:0,y:55,duration:1.2,delay:.2,ease:'power3.out',clearProps:'opacity,transform'})}
const initialFilter=location.hash.includes('=');restore();if(initialFilter)requestAnimationFrame(()=>$('#directory').scrollIntoView({behavior:'instant'}));
})();
