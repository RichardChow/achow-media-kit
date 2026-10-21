import {chromium} from 'playwright-core';
import fs from 'fs';
const [,,DIR,a,b,dir]=process.argv;const timing=fs.readFileSync(DIR+'/timing.json','utf8');
fs.mkdirSync(dir,{recursive:true});
const br=await chromium.launch({executablePath:process.env.CHROME_PATH||'/usr/bin/google-chrome'});const p=await br.newPage({viewport:{width:1080,height:1920}});
await p.addInitScript(`window.TIMING=${timing}`);
await p.goto('file://'+DIR+'/index.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(400);
const list=process.env.TIMES?process.env.TIMES.split(',').map(Number):null;
const frames=list?list.map(t=>Math.round(t*30)):Array.from({length:+b-+a},(_,i)=>+a+i);
for(const f of frames){await p.evaluate(t=>render(t),f/30);const ov=await p.evaluate(()=>{const s=document.querySelector('#sub span'),a=document.getElementById('av');if(getComputedStyle(s).display==='none')return 0;const r=s.getBoundingClientRect(),q=a.getBoundingClientRect();return (r.left<q.right&&r.right>q.left&&r.top<q.bottom&&r.bottom>q.top)?1:0});if(ov)fs.appendFileSync(DIR+'/overlap.log',f+'\n');await p.screenshot({path:`${dir}/${String(f).padStart(5,'0')}.jpg`,type:'jpeg',quality:92})}
await br.close();
