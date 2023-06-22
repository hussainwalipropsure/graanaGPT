
import requests
import json
from fuzzywuzzy import fuzz

def get_city_id(city_in):
    """
    get the city id from provided city
    """
    city_in =str(city_in).strip()
    x = [{'id': 1, 'name': 'Islamabad'}, {'id': 169, 'name': 'Karachi'}, {'id': 2, 'name': 'Lahore'}, {'id': 176, 'name': 'Peshawar'}, {'id': 3, 'name': 'Rawalpindi'}, {'id': 182, 'name': 'Abbottabad '}, {'id': 180, 'name': 'Attock '}, {'id': 221, 'name': 'Bagh'}, {'id': 175, 'name': 'Bahawalpur'}, {'id': 201, 'name': 'Bannu'}, {'id': 218, 'name': 'Batgram'}, {'id': 229, 'name': 'Bhimber'}, {'id': 213, 'name': 'Buner'}, {'id': 177, 'name': 'Chakwal'}, {'id': 197, 'name': 'Charsadda'}, {'id': 212, 'name': 'Chitral'}, {'id': 188, 'name': 'Daska'}, {'id': 189, 'name': 'Dera Ghazi Khan'}, {'id': 203, 'name': 'DI Khan'}, {'id': 243, 'name': 'Dina'}, {'id': 211, 'name': 'Dir Lower'}, {'id': 210, 'name': 'Dir Upper'}, {'id': 170, 'name': 'Faisalabad'}, {'id': 196, 'name': 'Fateh Jhang'}, {'id': 228, 'name': 'Ghanche'}, {'id': 184, 'name': 'Gilgit'}, {'id': 241, 'name': 'Gujar Khan'}, {'id': 174, 'name': 'Gujranwala'}, {'id': 233, 'name': 'Gujrat'}, {'id': 179, 'name': 'Gwadar'}, {'id': 202, 'name': 'Hangu'}, {'id': 214, 'name': 'Haripur'}, {'id': 181, 'name': 'Hasanabdal'}, {'id': 222, 'name': 'Haveli'}, {'id': 226, 'name': 'Hunza'}, {'id': 183, 'name': 'Hyderabad'}, {'id': 193, 'name': 'Jhelum'}, {'id': 200, 'name': 'Karak'}, {'id': 191, 'name': 'Kashmir'}, {'id': 273, 'name': 'Kasur'}, {'id': 240, 'name': 'Khanewal'}, {'id': 185, 'name': 'Khanpur'}, {'id': 235, 'name': 'Kharian'}, {'id': 199, 'name': 'Kohat'}, {'id': 216, 'name': 'Kohistan'}, {'id': 220, 'name': 'Kotli'}, {'id': 205, 'name': 'Lakki Marwat'}, {'id': 234, 'name': 'Lalamusa'}, {'id': 208, 'name': 'Malakand PA'}, {'id': 244, 'name': 'Mangla'}, {'id': 215, 'name': 'Mansehra'}, {'id': 171, 'name': 'Mardan'}, {'id': 192, 'name': 'Mirpur (Azad Kashmir)'}, {'id': 168, 'name': 'Multan'}, {'id': 167, 'name': 'Murree'}, {'id': 219, 'name': 'Muzaffarabad'}, {'id': 232, 'name': 'Nawabshah'}, {'id': 225, 'name': 'Neelam'}, {'id': 195, 'name': 'Nowshera'}, {'id': 194, 'name': 'Okara'}, {'id': 223, 'name': 'Poonch'}, {'id': 187, 'name': 'Quetta'}, {'id': 230, 'name': 'Sarai Alamgir'}, {'id': 172, 'name': 'Sargodha'}, {'id': 209, 'name': 'Shangla'}, {'id': 186, 'name': 'Sheikhupura'}, {'id': 190, 'name': 'Sialkot'}, {'id': 227, 'name': 'Skardu'}, {'id': 224, 'name': 'Sudhanoti'}, {'id': 207, 'name': 'Sukkur'}, {'id': 198, 'name': 'Swabi'}, {'id': 206, 'name': 'Swat'}, {'id': 178, 'name': 'Talagang'}, {'id': 204, 'name': 'Tank'}, {'id': 166, 'name': 'Taxila'}, {'id': 217, 'name': 'Torghar'}, {'id': 173, 'name': 'Wah'}, {'id': 236, 'name': 'Wazirabad'}]
    for city in x:
        if city['name'].lower() == city_in.lower():
            return city['id']
    return None

def get_area_id(in_area, city_id):
    
    in_area = str(in_area).strip()
    try:
        if(city_id and in_area):
            url =f"https://xstage.graana.rocks/search/cityArea?cityId={city_id}&searchQuery={in_area}"
            # url="https://www.graana.com/search/cityArea?searchQuery=scheme&cityId="+str(city_id)
            
            x = requests.get(url)
            x =json.loads(x.text)
            
            #  Set match threshold 
            threshold = 60
            
            for area in x['data']:                
                if area['name']==in_area:
                    return area['areaId']
            
            for area in x['data']:
                # Get fuzz ratio for search name and area name
                ratio = fuzz.partial_ratio(in_area.lower(), area['name'].lower())
                # Check if ratio above threshold
                if ratio >= threshold:  
                    areaId = area['areaId']
                    return areaId
    except Exception as e:
        print(f"\n\n get_area_id Exception 93: {e=}\n")
        
    return None

def get_property_card(city_id,area_id=None,purpose="buy", type="residential"):
    import requests
    import json
    url=f"https://www.graana.com/search/listings?"
    if city_id:
        url+=f"cityId={city_id}"
    if area_id:
        url+=f"&areaId[]={area_id}"
    if purpose:
        url+=f"&purpose={purpose}"
    if type:
        url+=f"&type={type}"
    print(f"\n\n{url=}\n")
    
    response = requests.get(url)

    data = json.loads(response.text)['data']
    
    data = data[:3]
    cards = []
    for prop in data:
        if len(prop['propertyImages']):
            image = prop['propertyImages'][0]['url']
        else:
            image = "#"
        property_fields = {
            "customTitle": str(prop["customTitle"]).strip(),
            "price": "Rs."+prop["price"],
            "id": prop["id"],
            "size": str(prop["size"])+" "+str(prop["sizeUnit"]).title(),
        }
        if image:
            property_fields['image'] = image
        property_fields['link']='-'.join(property_fields['customTitle'].split(' '))+'-'+str(property_fields['id'])
        cards.append(property_fields)
      
    return cards

def get_property_data(city, area=None, purpose="buy"):    
    city_id = get_city_id(city)
    
    area_id = None
    if(area):
        area_id = get_area_id(area,city_id)
    
    response = get_property_card(city_id,area_id, purpose)
    
    return response
