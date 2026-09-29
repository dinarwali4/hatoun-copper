import numpy as np, json
from pyproj import Transformer
f=np.load('data/s2_raw.npz'); S=f['stack'].astype('float32'); ids=list(f['ids']); bn=list(f['bandnames']); B=f['bounds']
yrs=np.array([int(i.split('_')[2][:4]) for i in ids]); print(dict(zip(*np.unique(yrs,return_counts=True))))
scl=S[:,bn.index('SCL')]; good=np.isin(scl,[4,5,7])
R=S[:,:10]/10000.0; R[~np.repeat(good[:,None],10,1)]=np.nan; R[R<=0]=np.nan
def comp(sel):
    c=np.nanmedian(R[sel],0); b={k:c[i] for i,k in enumerate(bn[:10])}
    ndvi=(b['B08']-b['B04'])/(b['B08']+b['B04']); ndsi=(b['B03']-b['B11'])/(b['B03']+b['B11'])
    rock=np.isfinite(c).all(0)&(ndvi<0.25)&(ndsi<0.3)&(b['B02']>0.02)&(b['B04']>0.02)
    idx={'ironox_B4B2':b['B04']/b['B02'],'gossan_B11B4':b['B11']/b['B04'],'clay_B11B12':b['B11']/b['B12'],'ferrous':b['B12']/b['B08']+b['B03']/b['B04']}
    return b,rock,ndvi,idx
def rz(v,m): med=np.nanmedian(v[m]); mad=1.4826*np.nanmedian(np.abs(v[m]-med)); return (v-med)/mad
out={}
for tag,sel in (('all',np.ones(len(ids),bool)),('2021',yrs==2021),('2023',yrs==2023),('2025',yrs==2025)):
    b,rock,ndvi,idx=comp(sel)
    out[tag]={'rock':rock,**{k:np.where(rock,rz(v,rock),np.nan).astype('float32') for k,v in idx.items()}}
    if tag=='all': rgb=np.stack([b['B04'],b['B03'],b['B02']]).astype('float32'); ndvi_all=ndvi
    print(tag,'n',int(sel.sum()),'rock frac',round(float(rock.mean()),3))
H,W=rgb.shape[1:]
r,c=np.mgrid[0:H,0:W]; lon,lat=Transformer.from_crs(32643,4326,always_xy=True).transform(B[0]+(c+.5)*20,B[3]-(r+.5)*20)
np.savez_compressed('data/s2_cu.npz',rgb=rgb,ndvi=ndvi_all.astype('float32'),lon=lon.astype('float32'),lat=lat.astype('float32'),B=B,
    **{f'{t}_{k}':v for t,d in out.items() for k,v in d.items()})
def box(a,b_,cc,d): return (lon>=a)&(lon<=cc)&(lat>=b_)&(lat<=d)
reg={'HZ1 cluster':box(73.770,36.300,73.800,36.316),'Control SW':box(73.70,36.225,73.73,36.24),'Control E':box(73.80,36.24,73.82,36.27)}
for t in ('2021','2023','2025'):
    print(t,{n:{k:round(float(np.nanmedian(out[t][k][m])),2) for k in ('ironox_B4B2','gossan_B11B4','clay_B11B12')} for n,m in reg.items()})
