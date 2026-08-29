document.documentElement.classList.add('js');
var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ---- mobile menu ----
   Built on <body> rather than inside the header. A transform or backdrop-filter
   on an ancestor makes position:fixed resolve against that ancestor instead of
   the viewport, which is what previously squashed the panel into the header. */
var burger = document.getElementById('burger');
var nav    = document.getElementById('nav');

var veil = document.createElement('div');
veil.className = 'mnav-veil';

var panel = document.createElement('nav');
panel.className = 'mnav';
panel.id = 'mnav';
panel.setAttribute('aria-label', 'Mobile');

var mtop = document.createElement('div');
mtop.className = 'mnav__top';
mtop.innerHTML = '<svg class="logo__svg" aria-hidden="true"><use href="#ri-lockup"/></svg>' +
  '<button class="mnav__x" type="button" aria-label="Close menu">' +
  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" ' +
  'stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg></button>';
panel.appendChild(mtop);

nav.querySelectorAll('a').forEach(function(a){
  var link = a.cloneNode(true);
  link.className = 'mnav__link';
  panel.appendChild(link);
});

var cta = document.querySelector('.hdr .quote');
if(cta){
  var wrap = document.createElement('div');
  wrap.className = 'mnav__cta';
  wrap.appendChild(cta.cloneNode(true));
  panel.appendChild(wrap);
}

var meta = document.createElement('div');
meta.className = 'mnav__meta';
meta.innerHTML = 'Unit 3 Metro Triangle,<br>Mount Street, Birmingham B7 5QT<br>' +
  '<a href="mailto:sales@essentialtechgb.co.uk">sales@essentialtechgb.co.uk</a>';
panel.appendChild(meta);

document.body.appendChild(veil);
document.body.appendChild(panel);

function setMenu(open){
  panel.classList.toggle('on', open);
  veil.classList.toggle('on', open);
  document.body.classList.toggle('nav-open', open);
  burger.classList.toggle('x', open);
  burger.setAttribute('aria-expanded', open);
  burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
}
burger.setAttribute('aria-controls', 'mnav');
burger.addEventListener('click', function(){ setMenu(!panel.classList.contains('on')); });
veil.addEventListener('click', function(){ setMenu(false); });
mtop.querySelector('.mnav__x').addEventListener('click', function(){ setMenu(false); });
panel.addEventListener('click', function(e){ if(e.target.closest('a')) setMenu(false); });
document.addEventListener('keydown', function(e){ if(e.key === 'Escape') setMenu(false); });

/* ---- hero slider: text + photo together ---- */
var slides=document.querySelectorAll('.hero .slide'),
    shots=document.querySelectorAll('.circ__slide'),
    dots=document.querySelectorAll('.dots button'),
    cNum=document.getElementById('cNum'),
    cBar=document.getElementById('cBar'),
    i=0,timer;

function go(n){
  i=(n+slides.length)%slides.length;
  slides.forEach(function(s,k){s.classList.toggle('on',k===i)});
  if(!reduce){
    var h=slides[i].querySelector('h1,.h1x');
    if(h){ resetWords(h); requestAnimationFrame(function(){ requestAnimationFrame(function(){ playWords(h); }); }); }
  }
  shots.forEach(function(s,k){s.classList.toggle('on',k===i)});
  dots.forEach(function(d,k){d.setAttribute('aria-selected',k===i)});
  cNum.textContent='0'+(i+1)+'.';
  cBar.style.width=((i+1)/slides.length*100)+'%';
}
function play(){clearInterval(timer);timer=setInterval(function(){go(i+1)},6500);}
dots.forEach(function(d){d.addEventListener('click',function(){go(+d.dataset.go);play();})});
if(!reduce){
  play();
  setTimeout(function(){
    var h=slides[0].querySelector('h1,.h1x');
    if(h) playWords(h);
  }, 900);
}else{
  document.querySelectorAll('.w').forEach(function(w){w.classList.add('go')});
}

/* ---- scroll reveal ---- */
var items=document.querySelectorAll('.rise,.riseL,.riseR,.zoom');
if('IntersectionObserver' in window && !reduce){
  var io=new IntersectionObserver(function(en){
    en.forEach(function(e,k){
      if(e.isIntersecting){
        e.target.style.transitionDelay=(k*90)+'ms';
        e.target.classList.add('in');
        io.unobserve(e.target);
      }
    });
  },{threshold:.12,rootMargin:'0px 0px -50px'});
  items.forEach(function(el){io.observe(el)});
}else{
  items.forEach(function(el){el.classList.add('in')});
}

/* ---- counting numbers ---- */
var nums=document.querySelectorAll('.num');
function countUp(el){
  var to=+el.dataset.to, sfx=el.dataset.suffix||'', dur=1600, t0=null;
  function step(ts){
    if(!t0) t0=ts;
    var p=Math.min((ts-t0)/dur,1);
    var eased=1-Math.pow(1-p,3);
    el.textContent=Math.round(to*eased).toLocaleString('en-GB')+sfx;
    if(p<1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}
if('IntersectionObserver' in window && !reduce){
  var io2=new IntersectionObserver(function(en){
    en.forEach(function(e){ if(e.isIntersecting){countUp(e.target);io2.unobserve(e.target);} });
  },{threshold:.4});
  nums.forEach(function(el){io2.observe(el)});
}else{
  nums.forEach(function(el){el.textContent=(+el.dataset.to).toLocaleString('en-GB')+(el.dataset.suffix||'')});
}

/* ---- seamless marquee ---- */
var mq=document.getElementById('mq');
if(mq && !reduce){ mq.appendChild(mq.querySelector('ul').cloneNode(true)); }

/* ---- hero parallax ---- */
var heroBg=document.getElementById('heroBg'), ticking=false;
function onScroll(){
  if(!ticking && !reduce){
    ticking=true;
    requestAnimationFrame(function(){
      var y=window.scrollY;
      if(y<1000 && heroBg) heroBg.style.transform='translateY('+(y*0.22)+'px)';
      ticking=false;
    });
  }
  document.getElementById('toTop').classList.toggle('show', window.scrollY>700);
}
window.addEventListener('scroll',onScroll,{passive:true});

document.getElementById('toTop').addEventListener('click',function(){
  window.scrollTo({top:0,behavior:reduce?'auto':'smooth'});
});

/* ---- preloader ---- */
(function(){
  var pre=document.getElementById('pre');
  if(!pre) return;
  var seen = false;                       // only once per browsing session
  try { seen = sessionStorage.getItem('ri-pre') === '1'; } catch(err) {}
  if(reduce || seen){ pre.remove(); return; }
  try { sessionStorage.setItem('ri-pre','1'); } catch(err) {}
  var done=false;
  function hide(){ if(done) return; done=true; pre.classList.add('done');
    setTimeout(function(){ pre.remove(); },800); }
  window.addEventListener('load',function(){ setTimeout(hide,700); });
  setTimeout(hide,2600); // safety net if an asset stalls
})();

/* ---- split headings into masked words ---- */
function splitWords(el){
  if(el.dataset.split) return;
  el.dataset.split='1';
  var out='';
  el.textContent.trim().split(/\s+/).forEach(function(word,k){
    out+='<span class="w" style="transition-delay:'+(k*60)+'ms"><i style="transition-delay:'+(k*60)+'ms">'+word+'</i></span> ';
  });
  el.innerHTML=out;
}
function playWords(el){
  el.querySelectorAll('.w').forEach(function(w){ w.classList.add('go'); });
}
function resetWords(el){
  el.querySelectorAll('.w').forEach(function(w){ w.classList.remove('go'); });
}
if(!reduce){
  document.querySelectorAll('.hero h1, .hero .h1x, .head h2, .cta h2').forEach(splitWords);
  // section headings animate as they scroll in
  var ioW=new IntersectionObserver(function(en){
    en.forEach(function(e){
      if(e.isIntersecting){ playWords(e.target); ioW.unobserve(e.target); }
    });
  },{threshold:.3});
  document.querySelectorAll('.head h2, .cta h2').forEach(function(h){ ioW.observe(h); });
}

/* ---- sticky header ---- */
(function(){
  var hdr=document.querySelector('.hdr'), hero=document.getElementById('top'), last=0;
  function onS(){
    var y=window.scrollY, trigger=(hero?hero.offsetHeight:700)*0.55;
    if(y>trigger){
      hdr.classList.add('hdr--stick');
      hdr.classList.toggle('up', y<last || y<trigger+40);
    }else{
      hdr.classList.remove('hdr--stick','up');
    }
    last=y;
  }
  window.addEventListener('scroll',onS,{passive:true});
})();

/* ---- scroll progress ---- */
(function(){
  var bar=document.getElementById('prog');
  window.addEventListener('scroll',function(){
    var h=document.documentElement.scrollHeight-window.innerHeight;
    bar.style.width=(h>0?(window.scrollY/h*100):0)+'%';
  },{passive:true});
})();

/* ---- progress bars (About / Reviews) ---- */
(function(){
  var bars = document.querySelectorAll('.bar__fill');
  if(!bars.length) return;
  if(!('IntersectionObserver' in window) || reduce){
    bars.forEach(function(b){ b.style.width = b.dataset.pct + '%'; });
    return;
  }
  var io = new IntersectionObserver(function(en){
    en.forEach(function(e){
      if(e.isIntersecting){
        e.target.style.width = e.target.dataset.pct + '%';
        io.unobserve(e.target);
      }
    });
  },{threshold:.5});
  bars.forEach(function(b){ io.observe(b); });
})();

/* ---- mark the current page in the nav ---- */
(function(){
  var here = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav a, .mnav__link').forEach(function(a){
    var target = a.getAttribute('href');
    if(!target) return;
    if(target.split('#')[0] === here || (here === 'index.html' && target === 'index.html')){
      a.setAttribute('aria-current','page');
    }else{
      a.removeAttribute('aria-current');
    }
  });
})();

/* ---- safety net: never leave content hidden ---- */
setTimeout(function(){
  document.querySelectorAll('.rise,.riseL,.riseR,.zoom').forEach(function(el){ el.classList.add('in'); });
  document.querySelectorAll('.w').forEach(function(w){ w.classList.add('go'); });
}, 2500);

/* ---- contact form: post to FormSubmit without reloading the page ---- */
document.querySelectorAll('form.form').forEach(function(form){
  var msg = form.querySelector('.fmsg');
  var btn = form.querySelector('button[type=submit]');
  form.addEventListener('submit', function(e){
    e.preventDefault();
    if(!form.reportValidity()) return;
    var label = btn ? btn.innerHTML : '';
    if(btn){ btn.disabled = true; btn.innerHTML = '<span>Sending…</span>'; }
    if(msg){ msg.hidden = true; msg.className = 'fmsg'; }

    var data = {};
    new FormData(form).forEach(function(v,k){ data[k] = v; });

    fetch(form.action, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(data)
    })
    .then(function(r){ return r.json(); })
    .then(function(res){
      var ok = String(res.success) === 'true';
      if(msg){
        msg.hidden = false;
        msg.className = 'fmsg ' + (ok ? 'fmsg--ok' : 'fmsg--bad');
        msg.textContent = ok
          ? 'Thanks — your message has been sent. We will reply within one working day.'
          : (res.message || 'Something went wrong. Please email us directly instead.');
      }
      if(ok) form.reset();
    })
    .catch(function(){
      if(msg){
        msg.hidden = false;
        msg.className = 'fmsg fmsg--bad';
        msg.textContent = 'Could not send just now. Please email sales@essentialtechgb.co.uk instead.';
      }
    })
    .finally(function(){
      if(btn){ btn.disabled = false; btn.innerHTML = label; }
    });
  });
});
