#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import re
import pickle
import os

PAGE = "http://localhost:8000/auto_mpg.html"

def process_car_blocks(soup):
  """Extract Information from repeated divisions"""
  car_blocks = soup.find_all('div',class_='car_block')
  rows=[]
  for cb in car_blocks:
    year,territory = extract_territory_year(cb)

    row = dict(
    name=extract_name(cb),
    cylinders=extract_cyliders(cb),
    weight=extract_weight(cb),
    year=year,
    territory=territory,
    acceleration=extract_acceleration(cb),
    mpg=extract_mpg(cb),
    hp=extract_hp(cb),
    displacement=extract_displacement(cb.text)
    )
    rows.append(row)
  print(f"We have {len(rows)} rows of scrapped car data")
  print(rows[0])
  print(rows[-1])

def extract_name(cb):
  str_name = cb.find('span',class_='car_name').text
  return str_name 

def extract_cyliders(cb):
    str_cylinders = cb.find('span',class_='cylinders').text
    cylinders = int(str_cylinders)
    assert cylinders > 0, f"Expecting cylinders to be positive not {cylinders}"
    return cylinders

def extract_weight(cb):
    str_weight = cb.find('span', class_='weight').text
    weight = int(str_weight.replace(',',''))
    assert weight > 0, f"Expecting cylinders to be positive not {weight}"
    return weight

def extract_territory_year(cb):
    str_from = cb.find('span',class_='from').text
    year,territory = str_from.strip('()').split(',')
    year = int(year.strip(''))
    territory = territory.strip()
    assert year > 0, f"Expecting cylinders to be positive not {year}"
    assert len(territory) > 1, f"Expecting territory to be a useful string not {territory}"
    return year,territory

def extract_acceleration(cb):
  acceleration = float(cb.find('span',class_='acceleration').text)
  assert acceleration > 0, f"Expecting acceleration to be positive not {acceleration}"
  return acceleration



def extract_mpg(cb):
    try:
      mpg_str = cb.find('span',class_='mpg').text
      mpg = float(mpg_str.split(' ')[0])
      assert mpg > 0 , f"Expecting mpg to be positive not {mpg}"
    except ValueError:
      mpg="NULL"
    return mpg

def extract_hp(cb):
    hp_str = cb.find('span',class_='horsepower').text
    try:
      hp = float(hp_str)
      assert hp > 0 , f"Expecting hp to be positive not {hp}"
    except ValueError:
      hp = "NULL"
    return hp

def extract_displacement(text):
    displacement_str = re.findall('.* (\d+.\d+) cubic inches', text)[0]
    displacement = float(displacement_str)
    assert displacement > 60 , f"Expecting displacement to be reasonable not {displacement}"
    return displacement

if __name__ == "__main__":
  filename = 'scraped_page_result.pickle'
  if os.path.exists(filename):
    with open(filename,'rb') as f:
      print(f"loading cached {filename}")
      result = pickle.load(f)
  else:
    print(f"fetching {PAGE} from internet")
    result = requests.get(PAGE)
    with open(filename,'wb') as f:
      print(f"Writing cached {filename}")
      pickle.dump(result,f)
    assert result.status_code == 200, f"Got status  code {result.status_code} \
which is not a success"

  source = result.text
  soup = BeautifulSoup(source, 'html.parser')
  process_car_blocks(soup)
