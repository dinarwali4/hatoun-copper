import numpy as np, json, rasterio, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt, matplotlib.patheffects as pe
from rasterio.merge import merge
z=np.load('data/emit_aoi_20260624.npz'); C=z['cube']; wl=z['wl']; glon,glat=z['glon'],z['glat']
bi=lambda w:int(np.argmin(abs(wl-w)))
rgb=np.stack([C[...,bi(650)],C[...,bi(560)],C[...,bi(470)]],-1).astype('float32'); rgb=np.nan_to_num(np.clip(rgb/0.30,0,1)**(1/1.4))
src=rasterio.open('data/dem_N36E073.tif'); mos,_=merge([src],bounds=(73.68,36.20,73.84,36.32),res=(0.0005,0.0005)); D=mos[0][:len(glat),:len(glon)].astype(float)
gy,gx=np.gradient(D,(0.0005*110574),(0.0005*89700)); sl=np.arctan(np.hypot(gx,gy)); asp=np.arctan2(-gx,gy)
hs=np.clip(np.sin(np.radians(45))*np.cos(sl)+np.cos(np.radians(45))*np.sin(sl)*np.cos(np.radians(315)-asp),0,1)
G=np.load('data/zone_grid.npz'); zone=G['zone']; Z=json.load(open('zones.json'))
ext=[glon[0]-0.00025,glon[-1]+0.00025,glat[-1]-0.00025,glat[0]+0.00025]
fig,ax=plt.subplots(figsize=(12,9.2),dpi=130); ax.imshow(rgb*(0.5+0.5*hs[...,None]),extent=ext,aspect=1/np.cos(np.radians(36.26)))
ov=np.zeros(zone.shape+(4,)); ov[zone]=[1,0.61,0.18,0.8]; ax.imshow(ov,extent=ext,aspect=1/np.cos(np.radians(36.26)),interpolation='nearest')
for q in Z[:13]:
    t=ax.text(q['peak'][1]+0.0012,q['peak'][0]+0.0008,q['id'],fontsize=8.5,color='#ffd08a',weight='bold',path_effects=[pe.withStroke(linewidth=2.2,foreground='k')]); t.set_clip_on(True)
ax.plot(73.756425,36.260869,'*',ms=16,color='#ff3b30',mec='k'); ax.text(73.7575,36.2575,'Published coordinate\n(village fields)',fontsize=8,color='#ffb3ad',path_effects=[pe.withStroke(linewidth=2,foreground='k')])
ax.text(73.692,36.212,'Control SW slopes: 0 zone cells',fontsize=8,color='w',path_effects=[pe.withStroke(linewidth=2,foreground='k')])
ax.add_patch(plt.Rectangle((73.69,36.21),0.04,0.03,fill=False,ec='w',ls='--',lw=1))
ax.set_xlabel('Longitude °E'); ax.set_ylabel('Latitude °N'); ax.set_xlim(ext[0],ext[1]); ax.set_ylim(ext[2],ext[3])
ax.set_title('Hatoun: persistent triple anomaly (Fe³⁺ 900 + Al-OH 2200 + jarosite 2265 nm on ≥2 of 3 EMIT dates) — orange',fontsize=9.5)
plt.tight_layout(); plt.savefig('fig/zone_map.png',bbox_inches='tight'); print('ok')
