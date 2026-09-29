import numpy as np, json, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt, matplotlib.patheffects as pe
from pyproj import Transformer
from scipy import ndimage as ndi
J=json.load(open('emit_min.json'))['persist']
fams=[('sulphate','Jarosite / copiapite'),('whitemica','White mica / sericite'),('cu_mineral','Cu minerals (azurite etc.)'),('nonmineral','Non-mineral control'),('ferric','Ferric iron'),('carbonate','Carbonate')]
fig,ax=plt.subplots(figsize=(8.5,3.8),dpi=130)
lift=[J[k]['obs_ge3']/max(J[k]['exp_ge3'],0.5) for k,_ in fams]
cols=['#c0392b','#d68910','#1e8449','#7f8c8d','#a04000','#5d6d7e']
ax.barh([n for _,n in fams][::-1],lift[::-1],color=cols[::-1]); ax.axvline(1,color='k',lw=.8)
for i,(k,n) in enumerate(fams[::-1]): ax.text(lift[::-1][i]*1.05+0.3,i,f"{J[k]['obs_ge3']} obs vs {J[k]['exp_ge3']} expected",va='center',fontsize=7.5)
ax.set_xscale('log'); ax.set_xlabel('Lift: cells identified on ≥3 of 8 dates ÷ chance expectation (log)'); ax.spines[['top','right']].set_visible(False)
ax.set_title('EMIT mineral-ID persistence, Hatoun AOI (2023–2024 dates)',fontsize=10); plt.tight_layout(); plt.savefig('fig/persistence.png')
# zone map
s=np.load('data/s2_cu.npz'); B=s['B']; rgb=np.transpose(s['rgb'],(1,2,0)); img=np.nan_to_num(np.clip(rgb/0.32,0,1)**(1/1.5))
import rasterio
from rasterio.warp import reproject, Resampling
H,W=img.shape[:2]; T=rasterio.transform.from_origin(B[0],B[3],20,20); dem=np.zeros((H,W),'float32')
reproject(rasterio.band(rasterio.open('data/dem_N36E073.tif'),1),dem,dst_transform=T,dst_crs='EPSG:32643',resampling=Resampling.bilinear)
gy,gx=np.gradient(dem,20); sl=np.arctan(np.hypot(gx,gy)); asp=np.arctan2(-gx,gy); hs=np.clip(np.sin(np.radians(45))*np.cos(sl)+np.cos(np.radians(45))*np.sin(sl)*np.cos(np.radians(315)-asp),0,1)
fw=Transformer.from_crs(4326,32643,always_xy=True)
def rc(lo,la): x,y=fw.transform(lo,la); return (B[3]-y)/20,(x-B[0])/20
G=np.load('data/zone_grid.npz'); zone=G['zone']; glon,glat=G['glon'],G['glat']; Z=json.load(open('zones.json'))
fig,ax=plt.subplots(figsize=(12,8.4),dpi=130); ax.imshow(img*(0.55+0.45*hs[...,None]))
yy,xx=np.where(zone); r,c=rc(glon[xx],glat[yy]); ax.scatter(c,r,s=7,marker='s',color='#ff9c2e',alpha=.75,linewidths=0)
for z in Z[:13]:
    r,c=rc(z['peak'][1],z['peak'][0]); ax.text(c+5,r-5,z['id'],fontsize=8,color='#ffd08a',weight='bold',path_effects=[pe.withStroke(linewidth=2,foreground='k')])
r,c=rc(73.756425,36.260869); ax.plot(c,r,'*',ms=16,color='#ff3b30',mec='k'); ax.text(c+8,r+14,'Published coordinate',fontsize=8,color='#ff9b94',path_effects=[pe.withStroke(linewidth=2,foreground='k')])
for lo in np.arange(73.70,73.83,0.02):
    r,c=rc(lo,36.221); ax.text(c,H-6,f'{lo:.2f}°E',fontsize=7,color='w',ha='center',path_effects=[pe.withStroke(linewidth=1.5,foreground='k')])
for la in np.arange(36.23,36.30,0.01):
    r,c=rc(73.701,la); ax.text(4,r,f'{la:.2f}°N',fontsize=7,color='w',va='center',path_effects=[pe.withStroke(linewidth=1.5,foreground='k')])
ax.set_xlim(0,W); ax.set_ylim(H,0); ax.set_xticks([]); ax.set_yticks([])
ax.set_title('Persistent triple anomaly (Fe³⁺ 900 + Al-OH 2200 + jarosite 2265, ≥2 of 3 EMIT dates), over Sentinel-2 and hillshade',fontsize=9.5)
plt.tight_layout(); plt.savefig('fig/zone_map.png',bbox_inches='tight'); print('ok')
