import numpy as np, json
from skimage import measure
from scipy import ndimage as ndi
from shapely.geometry import Polygon
G=np.load('data/zone_grid.npz'); zone=G['zone']; glon,glat=G['glon'],G['glat']
Z=json.load(open('zones.json'))
for z in Z: z['class']='B transported / valley-floor material' if z['mean_slope']<15 else 'A in-situ alteration on bedrock or scree'
json.dump(Z,open('zones.json','w'),indent=1)
lab,n=ndi.label(zone,structure=np.ones((3,3)))
def zid(z):
    i=int(round((glat[0]-z['peak'][0])/0.0005)); j=int(round((z['peak'][1]-glon[0])/0.0005)); return lab[i,j]
k=['<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document><name>Hatoun copper — RegenX alteration zones (Sep 2026)</name>',
 '<Style id="zA"><LineStyle><color>ff2e9cff</color><width>3</width></LineStyle><PolyStyle><color>552e9cff</color></PolyStyle></Style>',
 '<Style id="zB"><LineStyle><color>ffd0d0d0</color><width>2</width></LineStyle><PolyStyle><color>33d0d0d0</color></PolyStyle></Style>',
 '<Style id="lab"><IconStyle><scale>0.7</scale><Icon><href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href></Icon></IconStyle><LabelStyle><color>ff2edcff</color><scale>1.2</scale></LabelStyle></Style>',
 '<Style id="pub"><IconStyle><color>ff0000ff</color><scale>1.1</scale><Icon><href>http://maps.google.com/mapfiles/kml/paddle/red-stars.png</href></Icon></IconStyle><LabelStyle><color>ff7f7fff</color><scale>1.0</scale></LabelStyle></Style>']
k.append('<Placemark><name>Published coordinate (village)</name><description>36°15′39.13″N 73°45′23″E as published; lies on cultivated valley floor.</description><styleUrl>#pub</styleUrl><Point><coordinates>73.756425,36.260869,0</coordinates></Point></Placemark>')
k.append('<Folder><name>Alteration zones (EMIT Fe3+ + Al-OH + jarosite on ≥2 of 3 dates)</name>')
for z in Z:
    if z['cells']<6 and z['id'] not in ('HZ13',): continue
    m=lab==zid(z); mm=ndi.binary_dilation(m,iterations=1)
    for c in measure.find_contours(np.pad(mm.astype(float),1),0.5):
        p=Polygon([(glon[0]+(cc-1)*0.0005,glat[0]-(r-1)*0.0005) for r,cc in c]).simplify(0.00015)
        if not p.is_valid or p.area<5e-8: continue
        co=' '.join(f'{x:.6f},{y:.6f},0' for x,y in p.exterior.coords)
        st='zA' if z['class'][0]=='A' else 'zB'
        k.append(f'<Placemark><name>{z["id"]}</name><styleUrl>#{st}</styleUrl><Polygon><tessellate>1</tessellate><altitudeMode>clampToGround</altitudeMode><outerBoundaryIs><LinearRing><coordinates>{co}</coordinates></LinearRing></outerBoundaryIs></Polygon></Placemark>')
    k.append(f'<Placemark><name>{z["id"]}</name><description>{z["class"]}. {z["area_ha"]} ha; peak {z["peak"][0]}N {z["peak"][1]}E; elev {z["elev_range"][0]}–{z["elev_range"][1]} m; mean slope {z["mean_slope"]}°; triple anomaly on {z["dates_at_peak"]}/3 dates; {z["dist_published_km"]} km from published point.</description><styleUrl>#lab</styleUrl><Point><coordinates>{z["peak"][1]},{z["peak"][0]},0</coordinates></Point></Placemark>')
k.append('</Folder></Document></kml>')
open('Hatoun_Copper_RegenX_zones.kml','w').write('\n'.join(k)); print('ok')
for z in Z[:13]: print(z['id'],z['class'][0],z['area_ha'],z['peak'],z['mean_slope'])
