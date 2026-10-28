const nav=document.getElementById('nav');
const onScroll=()=>nav.classList.toggle('solid',scrollY>60||document.body.classList.contains('menu'));
addEventListener('scroll',onScroll);onScroll();
const menu=nav.querySelector('ul');
nav.querySelector('.burger').onclick=()=>{menu.classList.toggle('open');document.body.classList.toggle('menu');onScroll()};
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12});
document.querySelectorAll('.rv').forEach(el=>io.observe(el));
const lb=document.getElementById('lb');
if(lb){
  const pics=()=>[...document.querySelectorAll('.gal img,.mas img:not(.off)')];
  let k=0;
  const show=i=>{const p=pics();k=(i+p.length)%p.length;lb.querySelector('img').src=p[k].src;lb.classList.add('on')};
  document.addEventListener('click',e=>{const i=pics().indexOf(e.target);if(i>-1)show(i)});
  lb.onclick=e=>{if(e.target.classList.contains('ar'))show(k+(e.target.classList.contains('nx')?1:-1));else lb.classList.remove('on')};
  addEventListener('keydown',e=>{if(!lb.classList.contains('on'))return;if(e.key=='Escape')lb.classList.remove('on');if(e.key=='ArrowRight')show(k+1);if(e.key=='ArrowLeft')show(k-1)});
}
