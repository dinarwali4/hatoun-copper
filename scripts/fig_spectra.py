import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
F=np.load('data/emit_feat.npz'); G=np.load('data/zone_grid.npz'); zone=G['zone']
fig,axs=plt.subplots(2,2,figsize=(13,7.2),dpi=130)
for col,d in enumerate(['20230609','20260624']):
    z=np.load(f'data/emit_aoi_{d}.npz'); C=z['cube']; wl=z['wl']; glon,glat=z['glon'],z['glat']; LON,LAT=np.meshgrid(glon,glat)
    valid=F[f'{d}_valid']
    def box(a,b,c,dd): return (LON>=a)&(LON<=c)&(LAT>=b)&(LAT<=dd)
    sets=[('HZ1 east tributary',zone&box(73.796,36.272,73.819,36.279)&valid,'#c0392b'),('HZ2 west cluster',zone&box(73.771,36.303,73.783,36.311)&valid,'#d68910'),('Control SW slopes (bare only)',box(73.69,36.21,73.73,36.24)&valid,'#5d6d7e')]
    for row,(lo,hi,marks) in enumerate(((480,1250,[(900,'Fe³⁺ 900')]),(2120,2420,[(2200,'Al-OH 2200 (sericite)'),(2265,'jarosite 2265'),(2330,'Mg-OH / CO₃ 2330')]))):
        ax=axs[row,col]
        for k,(n,m,c) in enumerate(sets):
            sel=(wl>lo)&(wl<hi); w=wl[sel]; s=np.nanmean(C[m][:,sel].astype('float32'),0)
            cont=s[0]+(s[-1]-s[0])*(w-w[0])/(w[-1]-w[0]); ax.plot(w,s/cont-0.05*k,color=c,lw=1.7,label=f'{n} (n={int(m.sum())})')
        for j,(x,t) in enumerate(marks): ax.axvline(x,color='#999',ls='--',lw=.7); ax.text(x+2,ax.get_ylim()[1],t,fontsize=7,color='#333',va='top',rotation=90)
        ax.spines[['top','right']].set_visible(False); ax.grid(alpha=.2)
        if row==0: ax.set_title(f'EMIT {d[:4]}-{d[4:6]}-{d[6:]}'+(' (independent test date)' if d.startswith('2026') else ''),fontsize=10)
        if row==1: ax.set_xlabel('Wavelength (nm)')
    axs[1,col].legend(frameon=False,fontsize=7,loc='lower left')
axs[0,0].set_ylabel('Continuum-removed (offset 0.05)'); axs[1,0].set_ylabel('Continuum-removed (offset 0.05)')
plt.tight_layout(); plt.savefig('fig/spectra.png'); print('ok')
