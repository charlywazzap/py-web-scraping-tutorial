import unittest
import scraper

def test_extract_displacement():
  displacement = scraper.extract_displacement('something 71.2 cubic inches')
  assert displacement == 71.2