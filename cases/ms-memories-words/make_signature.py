"""Turns logo.png into a pen-writing mask: logo_ink2.png (the ink, underline removed, 2x) and logo_t2.png (per-pixel pen time, 16-bit in R,G).
The pen walks each connected stroke from its leftmost end along the skeleton; strokes are written left to right with a short lift between them."""
import numpy as np, collections
from PIL import Image
from scipy import ndimage as ndi
from skimage.morphology import skeletonize
S=2
im=Image.open('logo.png').convert('RGBA'); w,h=im.size
big=im.resize((w*S,h*S),Image.LANCZOS); A=np.array(big)[:,:,3].astype(float)
# the underline is drawn separately at the end — cut it out of the ink (traced centreline, logo crop coordinates)
UL=[(400,497),(430,492),(460,488),(490,484),(520,480),(550,477),(580,474.5),(610,472),(640,469.5),(670,467.5),(700,465.5),(730,464),(760,462.5),(790,461),(820,459.5),(850,458.5),(880,458.5),(915,458.5)]
from PIL import ImageDraw
m=Image.new('L',big.size,0); d=ImageDraw.Draw(m); pts=[((x-60)*S,(y-225)*S) for x,y in UL]; d.line(pts,fill=255,width=3)
dist=ndi.distance_transform_edt(np.array(m)==0)
cut=(dist<9.5*S)
# keep the M's tail where it crosses the underline: only cut where the underline stroke itself is (right of x=520 orig) and thin region
xs=np.arange(big.size[0])[None,:]
cut&=(xs>(520-60)*S)
A2=A.copy(); A2[cut]=0
ink=A2>100
lab,n=ndi.label(ink,structure=np.ones((3,3)))
sk=skeletonize(ink)
# nearest skeleton pixel for every ink pixel
idx=ndi.distance_transform_edt(~sk,return_indices=True)[1]
T=np.zeros(A.shape); comps=[]
for c in range(1,n+1):
    cs=sk&(lab==c)
    if cs.sum()<2:
        continue
    ys,xs_=np.nonzero(cs); i0=np.argmin(xs_); start=(ys[i0],xs_[i0])
    D={start:0}; q=collections.deque([start])
    while q:
        y,x=q.popleft()
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                if dy==dx==0: continue
                p=(y+dy,x+dx)
                if p in D or not (0<=p[0]<cs.shape[0] and 0<=p[1]<cs.shape[1]) or not cs[p]: continue
                D[p]=D[(y,x)]+(1.414 if dy and dx else 1); q.append(p)
    comps.append((c,start[1],max(D.values()),D))
comps.sort(key=lambda t:t[1]); gap=40*S; off=0; sched={}
for c,sx,L,D in comps: sched[c]=(off,D); off+=L+gap
total=off-gap
Dmap=np.full(A.shape,-1.0)
for c,(o,D) in sched.items():
    for (y,x),v in D.items(): Dmap[y,x]=o+v
Tn=np.zeros(A.shape)
inkidx=np.argwhere(ink)
for y,x in inkidx:
    ny,nx=idx[0][y,x],idx[1][y,x]; v=Dmap[ny,nx]
    if v<0: continue                           # a speck with no skeleton (the full stop): timed below, right after the stroke written before it
    Tn[y,x]=v/total
ends={c:o+max(D.values()) for c,(o,D) in sched.items()}
for c in range(1,n+1):
    if c in sched: continue
    msk=(lab==c)&ink
    if not msk.any(): continue
    xc=np.nonzero(msk)[1].mean(); prior=[(sx,cc) for cc,sx,L,D in comps if sx<xc]
    Tn[msk]=((ends[max(prior)[1]]+8*S)/total) if prior else 0
# the soft anti-aliased fringe (alpha below the ink threshold) takes the pen time of its nearest ink pixel, so no ghost shows early
near=ndi.distance_transform_edt(~ink,return_indices=True)[1]
Tn=Tn[near[0],near[1]]
Tn=np.clip(Tn,0,1)
t16=(Tn*65534).astype(np.uint16)
rgb=np.zeros(A.shape+(3,),np.uint8); rgb[:,:,0]=t16>>8; rgb[:,:,1]=t16&255
Image.fromarray(rgb).save('logo_t2.png')
out=np.zeros(A.shape+(4,),np.uint8); out[:,:,3]=np.clip(A2,0,255).astype(np.uint8); Image.fromarray(out).save('logo_ink2.png')
print('components',n,'with skeleton',len(comps),'total pen length',int(total),'size',big.size)
