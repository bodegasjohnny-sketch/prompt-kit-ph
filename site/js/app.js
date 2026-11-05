// Open Source Prompt PH: vanilla JS. No network requests, nothing stored.
(function(){
var d=document, rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
d.documentElement.classList.add('js');
// scroll reveal
var rv=d.querySelectorAll('.rv');
if(rm||!('IntersectionObserver' in window)){rv.forEach(function(e){e.classList.add('in')})}
else{var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});rv.forEach(function(e){io.observe(e)})}
// sticky mobile CTA bar
var bar=d.querySelector('.mbar');
if(bar){var f=function(){bar.classList.toggle('show',scrollY>420)};addEventListener('scroll',f,{passive:true});f()}
// copy buttons
function copy(t,b){var done=function(){var o=b.textContent;b.textContent='Copied';b.classList.add('ok');setTimeout(function(){b.textContent=o;b.classList.remove('ok')},1600)};
 if(navigator.clipboard&&isSecureContext){navigator.clipboard.writeText(t).then(done,fb)}else fb();
 function fb(){var a=d.createElement('textarea');a.value=t;a.setAttribute('readonly','');a.style.position='absolute';a.style.left='-9999px';d.body.appendChild(a);a.select();try{d.execCommand('copy')}catch(e){}d.body.removeChild(a);done()}}
d.addEventListener('click',function(e){var b=e.target.closest('.copy');if(!b)return;var p=d.getElementById(b.getAttribute('data-target'));if(p)copy(p.innerText,b)});
var pr=d.querySelector('[data-print]');if(pr)pr.addEventListener('click',function(){print()});
// prompt notebook
var nb=d.getElementById('notebook');
if(nb){var tabs=nb.querySelectorAll('.chip'),parts=nb.querySelectorAll('.part'),auto=null,i=0;
 function show(n){tabs.forEach(function(t,k){t.setAttribute('aria-pressed',k<=n?'true':'false')});parts.forEach(function(p,k){p.classList.toggle('on',k<=n)})}
 tabs.forEach(function(t,k){t.addEventListener('click',function(){clearInterval(auto);show(k)})});
 show(rm?2:0);if(!rm){auto=setInterval(function(){i=(i+1)%3;show(i)},2200)}}
// animated step highlight
var st=d.querySelectorAll('.steps li');
if(st.length&&!rm){var s=0;st[0].classList.add('on');setInterval(function(){st[s].classList.remove('on');s=(s+1)%st.length;st[s].classList.add('on')},1800)}
// kit search + filter
var q=d.getElementById('q');
if(q){var cards=d.querySelectorAll('[data-kit]'),cnt=d.getElementById('count'),cat='All',chips=d.querySelectorAll('.filters .chip');
 var lim=24,mb=d.getElementById('more');function run(){var v=q.value.trim().toLowerCase(),n=0;cards.forEach(function(c){var ok=(cat==='All'||c.dataset.cat===cat)&&(!v||c.dataset.text.indexOf(v)>-1);if(ok)n++;c.hidden=!ok||n>lim});var s=Math.min(n,lim);cnt.textContent=(n>s?'Showing '+s+' of ':'')+n+(n===1?' kit':' kits');if(mb)mb.hidden=n<=lim}
 if(mb)mb.addEventListener('click',function(){lim+=24;run()});
 q.addEventListener('input',function(){lim=24;run()});chips.forEach(function(c){c.addEventListener('click',function(){cat=c.dataset.cat;lim=24;chips.forEach(function(x){x.setAttribute('aria-pressed',x===c?'true':'false')});run()})});run()}
// builder
var bf=d.getElementById('builder');
if(bf){var fm='Short video script',fc=bf.querySelectorAll('.fmt'),outs={
 'Short video script':'Give me a 6 scene script for a 60 second video, with one line of narration per scene and one image prompt per scene.',
 'Carousel':'Give me text for a 7 slide carousel: a hook slide, five content slides and a closing slide.',
 'Image prompts':'Give me 5 detailed image prompts in a consistent illustrated style, no text or logos in the images.',
 'Blog outline':'Give me a blog outline with an H1, five H2 sections and two bullet points under each.'};
 fc.forEach(function(c){c.addEventListener('click',function(){fm=c.dataset.f;fc.forEach(function(x){x.setAttribute('aria-pressed',x===c?'true':'false')});gen()})});
 function gen(){var t=(d.getElementById('topic').value.trim()||'[YOUR TOPIC]'),a=(d.getElementById('aud').value.trim()||'curious beginners');
  d.getElementById('o1').textContent='You are a friendly, careful explainer who writes for '+a+'.';
  d.getElementById('o2').textContent='Topic: '+t+'. Audience: '+a+'. Tone: clear and honest. Mark every factual claim I should verify, and do not invent quotes or statistics.';
  d.getElementById('o3').textContent=outs[fm]+' End with a numbered list of claims to fact-check.';
  d.getElementById('built').textContent=d.getElementById('o1').textContent+'\n'+d.getElementById('o2').textContent+'\n'+d.getElementById('o3').textContent}
 bf.addEventListener('input',gen);bf.addEventListener('submit',function(e){e.preventDefault();gen()});gen()}
// toc highlight
var tl=d.querySelectorAll('.toc a');
if(tl.length&&'IntersectionObserver' in window){var to=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){tl.forEach(function(a){a.classList.toggle('on',a.getAttribute('href')==='#'+e.target.id)})}})},{rootMargin:'-20% 0px -70% 0px'});tl.forEach(function(a){var h=d.getElementById(a.getAttribute('href').slice(1));if(h)to.observe(h)})}
})();
// mobile menu toggle (nav stays visible without JS)
(function(){var b=document.querySelector('.menubtn'),n=document.getElementById('mainnav');if(!b||!n)return;document.documentElement.classList.add('js');b.addEventListener('click',function(){var o=b.getAttribute('aria-expanded')==='true';b.setAttribute('aria-expanded',o?'false':'true');n.classList.toggle('open',!o)});n.addEventListener('click',function(e){if(e.target.closest('a')){b.setAttribute('aria-expanded','false');n.classList.remove('open')}})})();
