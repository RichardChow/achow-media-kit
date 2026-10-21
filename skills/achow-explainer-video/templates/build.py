#!/usr/bin/env python3
"""Build one explainer video.  usage: python3 build.py <issue_dir> [--keyframes-only]
issue_dir must contain: config.json, script.json, page.html  (optional: page.css, init.js)"""
import json,os,sys,subprocess,concurrent.futures as cf,shutil
HERE=os.path.dirname(os.path.abspath(__file__))
D=os.path.abspath(sys.argv[1]);KF='--keyframes-only' in sys.argv
cfg=json.load(open(f'{D}/config.json'));S=json.load(open(f'{D}/script.json'))
rd=lambda f:open(f'{D}/{f}').read() if os.path.exists(f'{D}/{f}') else ''
# 1 TTS (edge-tts)
os.makedirs(f'{D}/vo',exist_ok=True)
def tts(i):
    out=f'{D}/vo/{i:02d}.mp3'
    if os.path.exists(out) and os.path.exists(out+'.txt') and open(out+'.txt').read()==S[i][3]: return
    subprocess.run(['edge-tts','--voice',cfg.get('voice','zh-CN-YunxiNeural'),f"--rate={cfg.get('rate','+12%')}",'--text',S[i][3],'--write-media',out],check=True)
    open(out+'.txt','w').write(S[i][3])
list(cf.ThreadPoolExecutor(6).map(tts,range(len(S))))
# 2 audio mix + timing
subprocess.run([sys.executable,f'{HERE}/audio.py',D],check=True)
# 3 compose html
av=cfg.get('presenter','A')
if len(av)==1: av=f'{HERE}/../assets/presenters/{av}'
elif not os.path.isabs(av): av=os.path.join(D,av)
for f in ('avatar.png','avatar_closed.png'): shutil.copy(f'{av}/{f}',f'{D}/{f}')
h=open(f'{HERE}/template.html').read()
h=h.replace('{{PAGE}}',rd('page.html')).replace('/*{{CSS}}*/',rd('page.css')).replace('/*{{INIT}}*/',rd('init.js'))
h=h.replace('{{SERIES}}',cfg['series']).replace('{{NAME}}',cfg.get('name','Name')).replace('{{TAGLINE}}',cfg.get('tagline',''))
open(f'{D}/index.html','w').write(h)
cap=f'{HERE}/cap.mjs';T=json.load(open(f'{D}/timing.json'));N=int(T['total']*30)
if KF:
    shutil.rmtree(f'{D}/kf',ignore_errors=True)
    times=[round(N/30*k/13,2) for k in range(1,13)]
    subprocess.run(['node',cap,D,'0','0',f'{D}/kf'],env={**os.environ,'TIMES':','.join(map(str,times))},check=True)
    subprocess.run(f"ffmpeg -loglevel error -y -pattern_type glob -i '{D}/kf/*.jpg' -vf scale=270:-1,tile=6x2 {D}/kf_sheet.jpg",shell=True,check=True);sys.exit()
# 4 capture: each frame rendered exactly once, by index, in parallel workers
shutil.rmtree(f'{D}/fr',ignore_errors=True);
if os.path.exists(f'{D}/overlap.log'): os.remove(f'{D}/overlap.log')
W=7;C=(N+W-1)//W
ps=[subprocess.Popen(['node',cap,D,str(i*C),str(min(N,(i+1)*C)),f'{D}/fr']) for i in range(W)]
assert all(p.wait()==0 for p in ps)
assert len(os.listdir(f'{D}/fr'))==N,'frame count mismatch'
# 5 encode constant 30fps from image sequence
out=cfg.get('out','./out/video.mp4')
if not os.path.isabs(out): out=os.path.join(D,out)
os.makedirs(os.path.dirname(out),exist_ok=True)
subprocess.run(['ffmpeg','-loglevel','error','-y','-framerate','30','-start_number','0','-i',f'{D}/fr/%05d.jpg','-i',f'{D}/mix.wav','-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-r','30','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',out],check=True)
# 6 checks
fz=subprocess.run(['ffmpeg','-i',out,'-vf','freezedetect=n=0.003:d=0.8','-map','0:v','-f','null','-'],capture_output=True,text=True).stderr
fr=[l.split('freeze_start: ')[1] for l in fz.splitlines() if 'freeze_start' in l]
ov=open(f'{D}/overlap.log').read().split() if os.path.exists(f'{D}/overlap.log') else []
a=T['amp'];gaps=[];run=0
for i,v in enumerate(a+[1]):
    if v<0.03: run+=1
    else:
        if run>18 and i-run>40 and i<len(a): gaps.append(round((i-run)/30,2))
        run=0
# contact sheet
os.makedirs(f'{D}/keyframes',exist_ok=True)
for k in range(1,13):
    f=int(N*k/13);shutil.copy(f'{D}/fr/{f:05d}.jpg',f'{D}/keyframes/kf_{k:02d}.jpg')
subprocess.run(f"ffmpeg -loglevel error -y -pattern_type glob -i '{D}/keyframes/kf_*.jpg' -vf scale=270:-1,tile=6x2 {D}/keyframes/contact_sheet.jpg",shell=True,check=True)
print(json.dumps({'out':out,'duration':round(N/30,2),'frames':N,'freezes>=0.8s':fr,'overlap_frames':len(ov),'voice_gaps>0.6s':gaps}))
