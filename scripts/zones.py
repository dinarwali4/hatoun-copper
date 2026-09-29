import numpy as np, json, rasterio
from scipy import ndimage as ndi
from pyproj import Geod
z=np.load('data/emit_feat.npz'); glon,glat=z['glon'],z['glat']; LON,LAT=np.meshgrid(glon,glat); dates=['20230609','20240626','20260624']
def rz(a): med=np.nanmedian(a); mad=1.4826*np.nanmedian(abs(a-med)); return (a-med)/mad
trip=[];score=[]
for d in dates:
    F,A,J=rz(z[f'{d}_Fe3_900']),rz(z[f'{d}_AlOH_2200']),rz(z[f'{d}_Jar_2265'])
    trip.append((F>1.5)&(A>1)&(J>1.5)); score.append((np.nan_to_num(F)+np.nan_to_num(A)+np.nan_to_num(J))/3)
ntrip=np.sum(trip,0); sc=np.mean(score,0)
zone=ndi.binary_opening(ntrip>=2,structure=np.ones((2,2)))|(ntrip>=3)
dem=rasterio.open('data/dem_N36E073.tif'); Zg=np.array([v[0] for v in dem.sample(zip(LON.ravel(),LAT.ravel()))]).reshape(LON.shape)
gy,gx=np.gradient(Zg,55.5); slope=np.degrees(np.arctan(np.hypot(gx,gy)))
def box(a,b,c,d): return (LON>=a)&(LON<=c)&(LAT>=b)&(LAT<=d)
for n,m in {'Control SW':box(73.69,36.21,73.73,36.24),'HZ1':box(73.770,36.300,73.800,36.316)}.items(): print(n,'zone cells',int((zone&m).sum()),'of',int(m.sum()))
lab,n=ndi.label(zone,structure=np.ones((3,3))); sz=ndi.sum(zone,lab,range(1,n+1))
G=Geod(ellps='WGS84'); P=(36.260869,73.756425); pix_ha=0.0005*111320*np.cos(np.radians(36.27))*0.0005*110574/1e4
Zs=[]
for k in np.argsort(-sz)+1:
    m=lab==k
    if m.sum()<3: continue
    w=np.where(m,sc,-9); i=np.unravel_index(np.argmax(w),w.shape); _,_,dist=G.inv(P[1],P[0],LON[i],LAT[i])
    Zs.append(dict(cells=int(m.sum()),area_ha=round(float(m.sum()*pix_ha),1),peak=[round(float(LAT[i]),5),round(float(LON[i]),5)],centroid=[round(float(LAT[m].mean()),5),round(float(LON[m].mean()),5)],
        peak_score=round(float(sc[i]),2),mean_score=round(float(sc[m].mean()),2),dates_at_peak=int(ntrip[i]),elev_range=[int(Zg[m].min()),int(Zg[m].max())],mean_slope=round(float(slope[m].mean()),1),
        dist_published_km=round(dist/1000,2),bbox=[round(float(LON[m].min()),5),round(float(LAT[m].min()),5),round(float(LON[m].max()),5),round(float(LAT[m].max()),5)]))
for j,t in enumerate(Zs): t['id']=f'HZ{j+1}'; print(t)
json.dump(Zs,open('zones.json','w'),indent=1)
np.savez_compressed('data/zone_grid.npz',zone=zone,ntrip=ntrip.astype('uint8'),score=sc.astype('float32'),glon=glon,glat=glat)
