from Tools.functions.get_properties import get_city_id, get_area_id
import requests

def get_price_estimate(city, area=None, bed=4, general_size=2600,type="residential", subtype="house",purpose="Buy",):
    city_id = get_city_id(city)
    
    area_id = None
    if(area):
        area_id = get_area_id(area,city_id)
    url = f"https://stage.arms.graana.rocks/api/ai/price/predict?area_id={area_id}&city_id={city_id}&bed={bed}&general_size={general_size}&type={type}&subtype={subtype}&purpose={purpose}"

    response = requests.get(url)
    print(f"\n\n get_price_estimate 171: {response.json()=}\n")

    return response.json()['results']
