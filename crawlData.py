import requests
from bs4 import BeautifulSoup
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import os

def add_id_to_dict(d):
    stack = [d]
    while stack:
        current = stack.pop()
        if isinstance(current, dict):
            if "_id" not in current:
                current["_id"] = str(ObjectId())
            stack.extend(current.values())
        elif isinstance(current, list):
            stack.extend(current)

# Kết nối đến MongoDB
client = MongoClient(os.environ.get('MONGODB_URL'))
db = client['test']
collection = db['shows']

target_url = "https://www.netflix.com/browse?jbv=81665914"
headers = {'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7'}
resp = requests.get(target_url, headers=headers)
resp.encoding = 'utf-8' # Thiết lập encoding
html = resp.text

soup = BeautifulSoup(html, 'html.parser')

o = {}
casts = []
genres = []
episodes = []
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

img_tag = soup.find('source', {'srcset': True})
if img_tag:
    o["poster_path"] = img_tag['srcset']

overview = soup.find("div", {"class": "title-info-synopsis"})
if overview is not None:
    o["overview"] = overview.text
else:
    o["overview"] = ""

# trailer = soup.find("img", {"class":"additional-video-image-preloader"})
# if trailer:
o["trailer"] = ""
# else:
    # o["trailer"] = trailer["src"]

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

cast_tags = soup.find_all("span", {"class": "item-cast"})
for tag in cast_tags:
    cast_object = {
        "name": tag.text
    }
    casts.append(cast_object)

o["casts"] = casts

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