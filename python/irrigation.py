from datetime import date,timedelta
CROPS={'Soybean':(.40,1.15,.50),'Cotton':(.35,1.15,.70),'Wheat':(.40,1.15,.40),'Sugarcane':(.40,1.25,.75),'Onion':(.50,1.05,.75),'Tomato':(.60,1.15,.80),'Tur':(.40,1.10,.50),'Maize':(.30,1.20,.60),'Groundnut':(.40,1.15,.60),'Chickpea':(.40,1.00,.35)}
EFFICIENCY={'Drip':.90,'Sprinkler':.75,'Surface':.60}; SOIL_TARGET={'Black':38,'Red':28,'Sandy':18,'Loamy':32,'Clay':40}
def calculate(p,w):
 vals=CROPS.get(p['crop_name']); daily=w.get('daily',{}); et=(daily.get('et0_fao_evapotranspiration') or [None])[0]
 if not vals or et is None:return {'available':False,'limitations':['Crop coefficient or live ET₀ data is unavailable.']}
 stage=p['growth_stage'].lower(); kc=vals[0] if 'initial' in stage else vals[2] if ('late' in stage or 'matur' in stage) else vals[1]
 rain=sum(x or 0 for x in (daily.get('precipitation_sum') or [])[:3]); deficit=max(0,et*kc-rain*.8); assumptions=[]
 moisture=p.get('soil_moisture')
 if moisture is None: assumptions.append('No soil-moisture reading: weather-only water balance used.')
 else:
  target=SOIL_TARGET[p['soil_type']]
  if float(moisture)<target*.65:deficit+=min(12,(target-float(moisture))*.35)
  elif float(moisture)>target:deficit=0
 efficiency=EFFICIENCY[p['irrigation_method']]; gross=deficit/efficiency; hectares=float(p['area'])*(.404685642 if p['area_unit']=='acre' else 1); liters=gross*hectares*10000; required=gross>=1; flow=p.get('flow_rate_lph'); duration=liters/float(flow) if flow else None
 return {'available':True,'required':required,'kc':kc,'et0':round(et,2),'etc':round(et*kc,2),'effective_rain':round(rain*.8,2),'net_mm':round(deficit,2),'gross_mm':round(gross,2),'liters':round(liters),'efficiency':round(efficiency*100),'duration_hours':round(duration,1) if duration else None,'recommended_date':str(date.today() if required else date.today()+timedelta(days=3)),'reason':'Crop demand exceeds effective rain and available soil water.' if required else 'Rain and/or soil moisture covers estimated crop demand.','assumptions':assumptions,'confidence':'medium' if assumptions else 'high'}
