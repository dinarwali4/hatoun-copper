import numpy as np, json
z=np.load('data/emit_feat.npz'); glon,glat=z['glon'],z['glat']; LON,LAT=np.meshgrid(glon,glat); dates=list(z['dates'])
def rz(a): med=np.nanmedian(a); mad=1.4826*np.nanmedian(abs(a-med)); return (a-med)/mad
def box(a,b,c,d): return (LON>=a)&(LON<=c)&(LAT>=b)&(LAT<=d)
reg={'HZ1 cluster (H01–H12)':box(73.770,36.300,73.800,36.316),'Published point ±500 m':box(73.7508,36.2564,73.7620,36.2654),'H17 (Cu hit)':box(73.785,36.258,73.792,36.263),
     'Control SW slopes':box(73.69,36.21,73.73,36.24),'Control E slopes':box(73.81,36.24,73.84,36.27)}
for d in dates:
    print('==',d)
    Z={k:rz(z[f'{d}_{k}']) for k in ('Fe3_900','AlOH_2200','Jar_2265','MgOH_2330')}
    for n,m in reg.items():
        print(f'  {n:26s}'+'  '.join(f'{k} {np.nanmedian(Z[k][m]):+.2f}' for k in Z)+f'  valid {np.isfinite(Z["Fe3_900"][m]).mean():.2f}')
    for k,v in Z.items(): np.save(f'data/z_{k}_{d}.npy',v.astype('float32'))
