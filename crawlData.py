import requests
from bs4 import BeautifulSoup
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def add_id_to_dict(d):
    stack = [d]
    while stack:
        current = stack.pop()
        if isinstance(current, dict):
            if "_id" not in current:
                current["_id"] = ObjectId()
            stack.extend(current.values())
        elif isinstance(current, list):
            stack.extend(current)

# Kết nối đến MongoDB
# client = MongoClient(os.environ.get('MONGODB_URL'))
client = MongoClient('mongodb+srv://admin:admin@finder.yo9axq1.mongodb.net/?retryWrites=true&w=majority')

db = client['test']
collection = db['movies']

target_url = "https://www.netflix.com/browse?jbv=81574246"
headers = {'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7'}
resp = requests.get(target_url, headers=headers)
resp.encoding = 'utf-8' # Thiết lập encoding
html = resp.text

soup = BeautifulSoup(html, 'html.parser')

o = {}
casts = []
programs = []
genres = []
creators = []
episodes = []
posters = []
e = {}

title = soup.find("h1", {"class": "title-title"})
if title:
    o['title'] = title.text
else:
    o['title'] = ""

img_tag = soup.find("img", {"class": "logo"})
if img_tag:
    o["logo"] = img_tag["src"]

o["duration"] = soup.find("span", {"class": "duration"}).text
release_date = soup.find("span", {"class": "item-year"})
if release_date:
    o["release_date"] = release_date.text

img_tag = soup.find_all('source', {'srcset': True})
for img in img_tag:
    img_object = {
        "path": img['srcset']
    }
    posters.append(img_object)
o["poster_path"] = posters

overview = soup.find("div", {"class": "title-info-synopsis"})
if overview is not None:
    o["overview"] = overview.text
else:
    o["overview"] = ""

def search_youtube(query):
    base_url = "https://www.youtube.com"
    search_url = f"{base_url}/results?search_query={query}"
    
    # Cấu hình Selenium WebDriver
    # driver_service = Service('path/to/chromedriver')
    driver = webdriver.Chrome()
    
    driver.get(search_url)
    
    video_element = driver.find_element(By.CSS_SELECTOR, ".style-scope.ytd-video-renderer")
    child_elements = video_element.find_elements(By.CSS_SELECTOR, "a")
    if child_elements:
        first_child_element = child_elements[0]
        video_url = first_child_element.get_attribute("href")
        return video_url
    
    driver.quit()  # Đóng trình duyệt
    
    return None

# Tìm kiếm trên Google
query = "Trailer+" + o['title'].replace(" ", "+")
trailer_url = search_youtube(query)

if trailer_url:
    trailer = trailer_url.replace('watch?v=', 'embed/')
    o["trailer"] = trailer.split('&')[0]

o["video"] = ""

genre_tags = soup.find_all("span", {"class": "item-genres"})
genre_collection = db["genres"]

for tag in genre_tags:
    genre_name = tag.text.replace(",", "")
    genre_obj = genre_collection.find_one({"name": genre_name})
    if genre_obj:
        genre_obj["_id"] = str(genre_obj["_id"])
    else:
        genre_obj = {"name": genre_name}
        genre_collection.insert_one(genre_obj)
        genre_obj["_id"] = str(genre_obj["_id"])
    genres.append(genre_obj)
o["genres"] = genres

episodes_tags = soup.find_all("li", {"class": "episode"})
for tag in episodes_tags:
    e["episode_title"]=tag.find("h3",{"class":"episode-title"}).text
    e["episode_runtime"]=tag.find("span",{"class":"episode-runtime"}).text
    e["episode_image"]=tag.find("img",{"class":"episode-thumbnail-image"})["src"]
    e["episode_description"]=tag.find("p",{"class":"epsiode-synopsis"}).text
    episodes.append(e)
    e={}

o["episodes"] = episodes

casts_collection = db['casts']
cast_tags = soup.find_all("span", {"class": "item-cast"})
for tag in cast_tags:
    cast_object = casts_collection.find_one({"name": tag.text})
    if cast_object:
        cast_object["_id"] = str(cast_object["_id"])
    else:
        cast_object = {"name": tag.text}
        casts_collection.insert_one(cast_object)
        cast_object["_id"] = str(cast_object["_id"])
    casts.append(cast_object)

o["casts"] = casts

program_type = soup.find_all("span", {"class": "more-details-item item-mood-tag"})
for types in program_type:
    name = types.text.replace(",", "")
    if name:
        program_object = {
            "name": name
        }
        programs.append(program_object)
o["program_type"] = programs

age_rating = soup.find("span", {"class": "maturity-number"})
if age_rating:
    o["age_rating"] = age_rating.text.strip()

info_creators = soup.find("span", {"data-uia": "info-creators"})
if info_creators:
    creators_list = info_creators.text.split(",")
    for creator in creators_list:
        creator_object = {
            "name": creator.strip() # Sử dụng strip() để loại bỏ khoảng trắng thừa
        }
        creators.append(creator_object)
o["creators"] = creators

item_genre = soup.find("a", {"class": "title-info-metadata-item item-genre"})
if item_genre:
    o["item_genre"] = item_genre.text


add_id_to_dict(o) # Thêm `_id` cho tất cả các object con trong document

class MyDocument:
    def __init__(self, data):
        self.data = data
        self.createdAt = datetime.utcnow()
        self.updatedAt = datetime.utcnow()

    def to_dict(self):
        return {
            **self.data,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }

    @classmethod
    def from_dict(cls, doc_dict):
        obj = cls(doc_dict["data"])
        obj.createdAt = doc_dict.get("createdAt")
        obj.updatedAt = doc_dict.get("updatedAt")
        return obj

def my_document_post_save(doc):
    doc.updatedAt = datetime.utcnow()
    collection.update_one({"_id": doc._id}, {"$set": {"updatedAt": doc.updatedAt}})

exists_document = collection.find_one({"title": title.text, "release_date": release_date.text})

doc = MyDocument(o)
doc_dict = doc.to_dict()

if exists_document:
    print("Phim này đã tồn tại trong hệ thống!")
else:
    # Nếu document chưa tồn tại thì thực hiện insert vào database
    collection.insert_one(doc_dict)
    print("Thêm phim thành công vào cơ sở dữ liệu.")