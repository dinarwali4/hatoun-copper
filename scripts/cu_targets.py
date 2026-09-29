import numpy as np, json, rasterio
from scipy import ndimage as ndi
from pyproj import Geod
E=np.load('data/emit_min_persist.npz'); x0,y0,res=E['grid']; ny,nx=E['cu_mineral'].shape
LON=x0+(np.arange(nx)+.5)*res; LAT=y0-(np.arange(ny)+.5)*res; LON,LAT=np.meshgrid(LON,LAT)
dem=rasterio.open('data/dem_N36E073.tif'); Z=np.array([v[0] for v in dem.sample(zip(LON.ravel(),LAT.ravel()))]).reshape(LON.shape)
cu=E['cu_mineral']; su=E['sulphate']; fe=E['ferric']; wm=E['whitemica']; nm=E['nonmineral']
# evidence layers (dates identified), smoothed over 3x3 (≈180 m) to allow for geolocation jitter
def s(a,t): return ndi.maximum_filter((a>=t).astype(int),size=3)
score=s(cu,2)*2+s(su,2)*2+s(fe,3)+s(wm,3)
core=(cu>=2)|(su>=2)
cand=core&(score>=4)&(nm<2)
lab,n=ndi.label(ndi.binary_dilation(cand,iterations=1),structure=np.ones((3,3)))
g=Geod(ellps='WGS84'); P=(36.260869,73.756425)
T=[]
for k in range(1,n+1):
    m=(lab==k)&cand
    if m.sum()==0: continue
    w=np.where(m,score*10+cu+su,-1); i=np.unravel_index(np.argmax(w),w.shape)
    _,_,dist=g.inv(P[1],P[0],LON[i],LAT[i])
    T.append(dict(peak=[round(float(LAT[i]),5),round(float(LON[i]),5)],cells=int(m.sum()),score=int(score[i]),cu_dates=int(cu[m].max()),sulphate_dates=int(su[m].max()),
        ferric_dates=int(fe[m].max()),whitemica_dates=int(wm[m].max()),elev=int(Z[i]),dist_from_published_km=round(dist/1000,2)))
T=sorted(T,key=lambda t:(-t['score'],-t['cells']))
for j,t in enumerate(T): t['id']=f'H{j+1:02d}'
for t in T[:25]: print(t)
print('total',len(T))
json.dump(T,open('cu_targets.json','w'),indent=1)
np.savez_compressed('data/cu_score.npz',score=score.astype('uint8'),cand=cand,LON=LON.astype('float32'),LAT=LAT.astype('float32'),Z=Z.astype('float32'))
