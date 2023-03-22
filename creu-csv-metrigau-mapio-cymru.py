import sys
import requests
import json
import time

overpass_url = "http://overpass-api.de/api/interpreter"

eitemau = ["place=city", "place=town", "place=village", "designation=community", "natural=peak", "waterway=river"]
enwau = ["name", "name:cy", "wikidata"]

print("eitem,enw,count,count:nodes,count:ways,count:relations")

for eitem in eitemau:
	for enw in enwau:
		overpass_query = '[out:csv(::count, ::"count:nodes", ::"count:ways", ::"count:relations"; false; ",")][timeout:90];' \
		'area[name="Cymru / Wales"][boundary=administrative]->.searchArea;' \
		'(' \
		'node[{eitem}]["{enw}"](area.searchArea);' \
		'way[{eitem}]["{enw}"](area.searchArea);' \
		'relation[{eitem}]["{enw}"](area.searchArea);' \
		');' \
		'out count;'.format(eitem=eitem,enw=enw)

		#print(overpass_query)

		codymateb = 0
		ceisiadau = 0
		while(codymateb != 200):
			response = requests.get(overpass_url, params={'data': overpass_query})
			codymateb = response.status_code
			response.encoding = 'utf-8'
			time.sleep(30)
			ceisiadau += 1
			if(ceisiadau > 3):
				print("\nMae gwall API ar hyn o bryd - yn anffodus. Y cod yw: " . codymateb)
				quit()
			
		allbwn = response.text.replace('\n', '')
		print(eitem + "," + enw + "," + allbwn)
