"""import"""

import requests
from bs4 import BeautifulSoup
import time
import json
import csv


"""inital values"""
name_res_list = []
location_url_list = []
categories_list = []
working_hour_list = []
cuisines_list = []
url_rewrite_name_list = []
total_review_shopee_food_list = []
avg_point_list = []
address_list = []
min_price_list = []
max_price_list = []
avg_price_list = []
minimum_shipping_fee_list = []
district_list = []
menu_list = []
short_description_list = []
has_contract_list = []
is_open_list = []
lattitude_list = []
longitude_list = []

# foody
location_rating_list = []
price_rating_list = []
quality_rating_list = []
service_rating_list = []
space_rating_list =[]


"""base_link"""
base_link_foody = "https://www.foody.vn/"
base_link_shopee_food="https://shopeefood.vn/"

headers = {
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'x-foody-access-token': '7b9634bdd9bf448c026ddc2289f94df661222707f986d45a70e98ee3c3a30543b330d998a58a0bd88e9388eb6da665c22b5b9e9bd8d5e5967b3383ec30272946',
    'x-foody-api-version': '1',
    'x-foody-app-type': '1004',
    'x-foody-client-id':'1',
    'x-foody-client-language': 'vi',
    'x-foody-client-type': '6',
    'x-foody-client-version': '3.0.0',
    'content-type': "application/json;charset=UTF-8",
    'accept': 'application/json, text/plain, /'
}



"""helper functions"""

def handle_None(x):
    if x is None:
        return ""
    else:
        return x.text

def check_None_list(x):
    if x is None:
        return ""
    else:
        return x




def get_dish_list_from_delivery_id(delivery_id):
    """
    It takes a delivery_id as input, and returns a list of dishes that are available for delivery
    
    :param delivery_id: the id of the restaurant
    :return: A list of dishes
    """
    url = f'https://gappapi.deliverynow.vn/api/dish/get_delivery_dishes?request_id={delivery_id}&id_type=1'
    res = requests.get(url, headers=headers)
    data = res.json()
    
    if data["reply"] is None:
        return None
    
    dist_list = []
    for i in data["reply"]["menu_infos"]:
        for food_item in i["dishes"]:
              dist_list.append(food_item["name"])

    return dist_list



def get_data(start=0, end=1000000, filter_location=[], output_file="test_api.xlsx"):
    """
    > The function will get data from Shopee Food API and Foody API, then save the data to an Excel file
    
    :param start: the start offset of the request_id, defaults to 0 (optional)
    :param end: the last record you want to get, defaults to 1000000 (optional)
    :param filter_location: list of location_urls that you want to scrape
    :param output_file: the name of the output file, defaults to test_api.xlsx (optional)
    """
    for i in range(start, end+1):
        shopee_food_url = f"https://gappapi.deliverynow.vn/api/delivery/get_detail?id_type=2&request_id={i}"
        print(shopee_food_url)
        res = requests.get(url = shopee_food_url, headers = headers)
        data = res.json()
        
        if (data["result"] == 'success'):
            
            # location_url
            location_url = data["reply"]["delivery_detail"]["location_url"]
            if location_url in filter_location:
                location_url_list.append(location_url)
                
                # name of restaurant
                name_res = data["reply"]["delivery_detail"]["name"]
                name_res_list.append(name_res)
                
                # categories
                if(data["reply"]["delivery_detail"]["categories"] is None or \
                   data["reply"]["delivery_detail"]["categories"] == []):
                    categories = ""
                else:
                    categories = str(data["reply"]["delivery_detail"]["categories"])
                categories_list.append(categories)
        
                # cuisines
                if (data["reply"]["delivery_detail"]["cuisines"] is None or \
                    data["reply"]["delivery_detail"]["cuisines"] == []):
                    cuisines = ""
                else:
                    cuisines = str(data["reply"]["delivery_detail"]["cuisines"])
                cuisines_list.append(cuisines)
                
                # short_description
                short_description = str(data["reply"]["delivery_detail"]["short_description"])
                short_description_list.append(short_description)
                
                # is_open
                is_open = data["reply"]["delivery_detail"]["delivery"]["is_open"]
                is_open_list.append(is_open)
                
                # url_rewrite_name
                url_rewrite_name = data["reply"]["delivery_detail"]["url_rewrite_name"]
                url_rewrite_name_list.append(url_rewrite_name)
        
                # Total review in Shopee Food
                total_review_shopee_food = data["reply"]["delivery_detail"]["rating"]["total_review"]
                total_review_shopee_food_list.append(total_review_shopee_food)
                
                # has_contract
                has_contract = data["reply"]["delivery_detail"]["delivery"]["has_contract"]
                has_contract_list.append(has_contract)
                
                # avg point
                avg_point = data["reply"]["delivery_detail"]["rating"]["avg"]
                avg_point_list.append(avg_point)
        
                # address
                address = data["reply"]["delivery_detail"]["address"]
                address_list.append(address)
        
                # price_range
                min_price = data["reply"]["delivery_detail"]["price_range"]["min_price"]
                min_price_list.append(min_price)
                max_price = data["reply"]["delivery_detail"]["price_range"]["max_price"]
                max_price_list.append(max_price)
                
                # minimum shipping fee
                minimum_shipping_fee = data["reply"]["delivery_detail"]["delivery"]["shipping_fee"]["minimum_fee"]
                minimum_shipping_fee_list.append(minimum_shipping_fee)
                
                #Lattitude
                lattitude = data["reply"]["delivery_detail"]["position"]["latitude"]
                lattitude_list.append(lattitude)

                #Longitude
                longitude = data["reply"]["delivery_detail"]["position"]["longitude"]
                longitude_list.append(longitude)
        
                # Ratings foody
                url_foody = base_link_foody + location_url + "/" + url_rewrite_name
                foody_res = requests.get(url = url_foody)
                soup = BeautifulSoup(foody_res.text, 'html.parser')
        
                rate_quality, rate_price, rate_location, rate_service, rate_space = soup.find_all('div', class_="microsite-top-points")
                
                location_rating = handle_None(rate_quality.find('span'))
                price_rating = handle_None(rate_price.find('span'))
                quality_rating = handle_None(rate_location.find('span'))
                service_rating = handle_None(rate_service.find('span'))
                space_rating = handle_None(rate_space.find('span'))
                
                location_rating_list.append(location_rating)
                price_rating_list.append(price_rating)
                quality_rating_list.append(quality_rating)
                service_rating_list.append(service_rating)
                space_rating_list.append(space_rating)
                
                # working_hour
                working_hour = soup.find('div', class_="micro-timesopen") \
                                    .find_all('span')[2].text.replace("\xa0", "")
                
                working_hour_list.append(working_hour)
                
                # avg_price
                if (soup.find('div', class_="microsite-point-avg") is None):
                    avg_price = ""
                else:
                    avg_price = soup.find('div', class_="microsite-point-avg").text \
                                    .replace("\n", " ").replace(" ", "").strip("\r")
                avg_price_list.append(avg_price)
                
                # District:
                district = handle_None(soup.find('div', class_="res-common-add")
                                           .find('span', itemprop="addressLocality"))
                district_list.append(district)
                
                # MENU:
                menu = str(get_dish_list_from_delivery_id(data["reply"]["delivery_detail"]["restaurant_id"]))
                menu_list.append(menu)
                
                
                # Lưu vào file real_time
                print(f"Dang ghi vao file {output_file}")
                row = [name_res, working_hour, is_open, categories, cuisines, short_description,
                       has_contract, url_rewrite_name, total_review_shopee_food, avg_point,
                       address, district, location_url, min_price, max_price, avg_price,
                       minimum_shipping_fee, lattitude, longitude, location_rating,
                       price_rating, quality_rating, service_rating, space_rating, menu]
                    

                with open(output_file,'a') as fwrite:
                    writer = csv.writer(fwrite)
                    writer.writerow(row)
                print(f'Ghi vao file {output_file} thanh cong')
                
  
        
        with open(".env", "w") as writer_curr_record:
            curr_record_json = {"start_offset": i,
                                 "end_offset": end_offset,
                                 "locations": filter_location, 
                                 "output_file": output_file}
            json.dump(curr_record_json, writer_curr_record)
            print('Cap nhat offset thanh cong')
        
        time.sleep(2)


if __name__ == "__main__":

    # read env file to get current row
    with open('.env', 'r') as fi:
        curr = json.loads(fi.read())

    # start row
    start_offset = int(curr['start_offset'])

    # end offset
    end_offset = int(curr['end_offset'])

    # locations
    location = list(curr['locations'])

    # output file
    output_file = curr["output_file"]

    get_data(start=start_offset, end=end_offset, filter_location=location, output_file=output_file)

