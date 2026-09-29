import numpy as np, json, netCDF4, re
z=np.load('data/emit_feat.npz'); glon,glat=z['glon'],z['glat']; LON,LAT=np.meshgrid(glon,glat); d='20260624'
def rz(a): med=np.nanmedian(a); mad=1.4826*np.nanmedian(abs(a-med)); return (a-med)/mad
def box(a,b,c,dd): return (LON>=a)&(LON<=c)&(LAT>=b)&(LAT<=dd)
Z={k:rz(z[f'{d}_{k}']) for k in ('Fe3_900','AlOH_2200','Jar_2265','MgOH_2330')}
reg={'HZ1 cluster':box(73.770,36.300,73.800,36.316),'Control SW':box(73.69,36.21,73.73,36.24),'East bank (secondary)':box(73.80,36.24,73.84,36.30)}
res={}
for n,m in reg.items():
    res[n]={k:round(float(np.nanmedian(v[m])),2) for k,v in Z.items()}; res[n]['valid']=round(float(np.isfinite(Z['Fe3_900'][m]).mean()),2)
    trip=((Z['Fe3_900']>1.5)&(Z['AlOH_2200']>1)&(Z['Jar_2265']>1.5))[m]
    res[n]['triple_anomaly_pct']=round(float(np.nanmean(trip)*100),2); print(n,res[n])
# EMIT L2B MIN 2026 at HZ1
ds=netCDF4.Dataset('data/emit/EMIT_L2B_MIN_001_20260624T041757_2617503_010.nc'); ds.set_auto_mask(False)
gt=ds.getncattr('geotransform'); gx=ds['location/glt_x'][:]; gy=ds['location/glt_y'][:]; names=dict(zip(ds['mineral_metadata/index'][:].tolist(),[str(x) for x in ds['mineral_metadata/name'][:]]))
H,W=gx.shape; lo=gt[0]+(np.arange(W)+.5)*gt[1]; la=gt[3]+(np.arange(H)+.5)*gt[5]; LO,LA=np.meshgrid(lo,la); v=(gx>0)&(gy>0)
import collections
for n,(a,b,c,dd) in {'HZ1 cluster':(73.770,36.300,73.800,36.316),'Control SW':(73.69,36.21,73.73,36.24)}.items():
    m=v&(LO>=a)&(LO<=c)&(LA>=b)&(LA<=dd); cnt=collections.Counter()
    for g in (1,2):
        raw=ds[f'group_{g}_mineral_id'][:]; o=raw[gy[m]-1,gx[m]-1]
        for x in o[o>0]: cnt[names[int(x)]]+=1
    tot=m.sum(); fam=lambda rx: sum(v_ for k_,v_ in cnt.items() if re.search(rx,k_,re.I))
    res[n+' EMIT-MIN 2026']=dict(px=int(tot),sulphate_pct=round(100*fam(r'jarosit|copiap|schwertm')/tot,2),ferric_pct=round(100*fam(r'hematite|goethite|fe-hydrox')/tot,1),
        whitemica_pct=round(100*fam(r'muscov|illite|sericit')/tot,1),cu_pct=round(100*fam(r'malachite|azurite|chrysocol')/tot,2))
    print(n,'2026 MIN',res[n+' EMIT-MIN 2026'])
json.dump(res,open('validation_2026.json','w'),indent=1)
