import json
from PIL import Image, ImageDraw, ImageFont
F=lambda s,b=True: ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf' if b else '/System/Library/Fonts/Supplemental/Arial.ttf',s)
Z={z['id']:z for z in json.load(open('zones.json'))}
jobs=[('Hatoun_A1_zones_valley_2026-07','Hatoun copper prospect: surface alteration zones','Airbus imagery 19 Jul 2026 · EMIT hyperspectral 2023, 2024, 2026',['HZ1','HZ2','HZ3','HZ5','HZ6','HZ8']),
 ('Hatoun_A2_zone_HZ1_2026-07','Zone HZ1: east tributary, largest persistent alteration','68 ha · sericite + jarosite + ferric iron on 3 of 3 dates',['HZ1','HZ8']),
 ('Hatoun_A3_zones_west_2026-07','West-bank cluster: zones HZ2, HZ3, HZ5, HZ6, HZ10','Bleached scree and bedrock, 2,000–3,300 m',['HZ2','HZ3','HZ5','HZ6','HZ10']),
 ('Hatoun_A4_zones_near_published_2026-07','Near the published coordinate','The published point lies on village fields; nearest anomalies HZ11–HZ13 are 1.5–2.4 km east',['HZ11','HZ12','HZ13']),
 ('Hatoun_A5_oblique_west_2026-07','3D view WNW over the west-bank cluster','Google Earth terrain, zones draped',[]),
 ('Hatoun_A6_oblique_HZ1_2026-07','3D view east up the HZ1 tributary','Google Earth terrain, zones draped',['HZ1','HZ8','HZ13'])]
for f,t,s,ids in jobs:
    im=Image.open(f'ge/img/{f}.jpg').convert('RGB'); w,h=im.size; d=ImageDraw.Draw(im)
    d.rectangle([0,0,w,122],fill=(18,22,20)); d.text((28,14),t,font=F(40),fill=(255,255,255)); d.text((30,66),s,font=F(24,False),fill=(205,212,208))
    d.text((w-560,24),'RegenX.eco Geospatial Computational Model',font=F(22),fill=(143,193,83)); d.text((w-560,58),'Prepared by Dinar Wali · Sep 2026',font=F(22,False),fill=(205,212,208))
    d.rectangle([w-430,122,w,236],fill=(18,22,20))
    d.rectangle([w-410,140,w-380,160],outline=(255,156,46),width=4); d.text((w-368,136),'Alteration zone, in-situ (A)',font=F(20,False),fill=(235,235,235))
    d.rectangle([w-410,172,w-380,192],outline=(208,208,208),width=3); d.text((w-368,168),'Zone on valley floor (B)',font=F(20,False),fill=(235,235,235))
    d.ellipse([w-404,202,w-386,220],fill=(230,40,40)); d.text((w-368,200),'Published coordinate (village)',font=F(20,False),fill=(235,235,235))
    if ids:
        bx,by=24,h-60-44*len(ids)-50; d.rectangle([bx-10,by-10,bx+640,h-40],fill=(18,22,20))
        d.text((bx,by),'Zone peaks (WGS84, ±60 m) · area · dates',font=F(22),fill=(255,255,255))
        for i,k in enumerate(ids):
            z=Z[k]; d.text((bx,by+40+i*44),f"{k:5s} {z['peak'][0]:.5f}°N {z['peak'][1]:.5f}°E · {z['area_ha']} ha · {z['dates_at_peak']}/3",font=F(23,False),fill=(255,176,64))
    im.save(f'fig/{f.replace("Hatoun_","annot_")}.jpg',quality=90)
print('ok')
