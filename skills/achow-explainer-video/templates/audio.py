import json,subprocess,numpy as np,wave,re
import sys,os
D=sys.argv[1] if len(sys.argv)>1 else '.';os.chdir(D)
SR=48000;S=json.load(open('script.json'));LEAD=1.0;GAP=0.22;TAIL=2.0
def rd(p):
    raw=subprocess.run(['ffmpeg','-loglevel','error','-i',p,'-f','s16le','-ac','1','-ar',str(SR),'-'],capture_output=True).stdout
    return np.frombuffer(raw,np.int16).astype(np.float32)/32768
segs=[];t=LEAD;clips=[]
for i,s in enumerate(S):
    x=rd(f'vo/{i:02d}.mp3')
    # trim silence
    nz=np.where(np.abs(x)>0.02)[0];x=x[max(0,nz[0]-600):nz[-1]+1200]
    e=np.convolve(np.abs(x),np.ones(480)/480,'same');q=e<0.012;out=[];i=0;n=len(x)
    while i<n:
        if q[i]:
            j=i
            while j<n and q[j]: j+=1
            L=j-i;keep=min(L,int(0.32*SR));out.append(x[i:i+keep//2]);out.append(x[j-(keep-keep//2):j]);i=j
        else:
            j=i
            while j<n and not q[j]: j+=1
            out.append(x[i:j]);i=j
    x=np.concatenate(out)
    d=len(x)/SR;segs.append({'id':s[0],'zh':s[1],'en':s[2],'text':s[3],'target':(s[4] if len(s)>4 else None),'scale':(s[5] if len(s)>5 else 1),'start':t,'end':t+d});clips.append((t,x));t+=d+GAP
total=t-GAP+TAIL;N=int(total*SR)
vo=np.zeros(N,np.float32)
for st,x in clips:a=int(st*SR);vo[a:a+len(x)]+=x
# subtitles: split on punctuation, time by char count
subs=[]
for s in segs:
    parts=[p for p in re.split(r'(?<=[，。、])',s['text']) if p.strip()]
    # merge short parts
    m=[]
    for p in parts:
        if m and len(m[-1].rstrip('，。、'))<6: m[-1]+=p
        else: m.append(p)
    n=sum(len(p) for p in m);tt=s['start'];dur=s['end']-s['start']
    for p in m:
        d=dur*len(p)/n;subs.append([round(tt,3),round(tt+d,3),p.rstrip('，。、')]);tt+=d
# mouth: smoothed env at 30fps with hysteresis + min hold 3 frames
F=30;nf=int(total*F);hop=SR//F
env=np.array([np.sqrt(np.mean(vo[i*hop:(i+1)*hop]**2)) for i in range(nf)])
env/=env.max()+1e-9
sm=np.convolve(env,np.ones(3)/3,'same')
mouth=[];state=0;hold=0
for v in sm:
    hold+=1
    want=1 if (v>0.18 if state==0 else v>0.08) else 0
    if want!=state and hold>=3: state=want;hold=0
    mouth.append(state)
# force alternation cap ~5Hz: if open run >9 frames while speaking, add a brief close
m2=mouth[:];run=0
for i in range(len(m2)):
    run=run+1 if m2[i] else 0
    if run>=8 and sm[i]>0.08: m2[i]=0;m2[min(i+1,len(m2)-1)]=0;run=-1
cfg=json.load(open('config.json')) if os.path.exists('config.json') else {}
json.dump({'em':cfg.get('em','曝光'),'segs':segs,'subs':subs,'mouth':m2,'amp':[round(float(v),3) for v in sm],'total':total},open('timing.json','w'),ensure_ascii=False)
# music
t_=np.arange(N)/SR;bpm=112;beat=60/bpm
chords=[[261.6,329.6,392.0],[196.0,246.9,293.7],[220.0,261.6,329.6],[174.6,220.0,261.6]]
bgm=np.zeros(N,np.float32)
bar=4*beat
for k in range(int(total/bar)+1):
    a=int(k*bar*SR);b=min(N,int((k+1)*bar*SR))
    if a>=N:break
    tt=t_[a:b]-k*bar;c=chords[k%4];env_=np.minimum(1,tt/0.3)*np.exp(-tt*0.25)
    for f in c: bgm[a:b]+=0.05*env_*(np.sin(2*np.pi*f*tt)+0.3*np.sin(2*np.pi*2*f*tt))
    bgm[a:b]+=0.06*env_*np.sin(2*np.pi*c[0]/2*tt)
    for j in range(8):  # pluck arps 8ths
        s0=int((k*bar+j*beat/2)*SR)
        if s0>=N:break
        L=min(int(0.3*SR),N-s0);u=np.arange(L)/SR;f=c[j%3]*2
        bgm[s0:s0+L]+=0.035*np.exp(-u*12)*np.sin(2*np.pi*f*u)
rng=np.random.default_rng(1)
for k in range(int(total/beat)):
    s0=int(k*beat*SR);L=min(int(0.25*SR),N-s0);u=np.arange(L)/SR
    if L<=0:break
    bgm[s0:s0+L]+=0.12*np.exp(-u*18)*np.sin(2*np.pi*(50+80*np.exp(-u*30))*u)  # kick
    h=int((k*beat+beat/2)*SR);L2=min(int(0.05*SR),N-h)
    if L2>0: bgm[h:h+L2]+=0.02*rng.standard_normal(L2)*np.exp(-np.arange(L2)/SR*80)
# fade
fi=int(1.5*SR);bgm[:fi]*=np.linspace(0,1,fi);fo=int(2.5*SR);bgm[-fo:]*=np.linspace(1,0,fo)
# duck by voice env
ve=np.repeat(sm,hop)[:N];ve=np.pad(ve,(0,N-len(ve)))
duck=np.convolve((ve>0.05).astype(np.float32),np.ones(int(0.25*SR))/int(0.25*SR),'same')
bgm*=1-0.6*np.clip(duck,0,1)
# sfx
sfx=np.zeros(N,np.float32)
def add(at,x):
    a=int(at*SR);L=min(len(x),N-a);sfx[a:a+L]+=x[:L]
L=int(0.45*SR);u=np.arange(L)/SR;nz=rng.standard_normal(L)
wh=np.convolve(nz,np.ones(6)/6,'same')*np.sin(np.pi*u/0.45)**2*0.08
L=int(0.6*SR);u=np.arange(L)/SR;ding=0.09*np.exp(-u*6)*(np.sin(2*np.pi*1318.5*u)+0.4*np.sin(2*np.pi*2637*u))
L=int(0.04*SR);u=np.arange(L)/SR;click=0.15*np.exp(-u*150)*np.sin(2*np.pi*2200*u)
for i,s in enumerate(segs):
    if i>0: add(s['start']-0.7,wh)
    if 0<i<len(segs)-1: add(s['start']+0.05,click);add(s['start']+0.1,ding)
mix=vo*1.0+bgm+sfx
mix/=max(1,np.abs(mix).max()/0.95)
st=np.stack([mix,mix],1)
w=wave.open('mix.wav','wb');w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((st*32767).astype(np.int16).tobytes());w.close()
print(total,[round(s['start'],1) for s in segs])
