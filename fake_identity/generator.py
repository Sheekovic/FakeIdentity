
import random
import re
import argparse
import sys
import requests  # Add this import for API requests
from typing import Dict

# A small built-in pool to avoid external deps
_FIRST_NAMES = [
    "Avery","Cameron","Dakota","Dylan","Harper","Jordan","Logan","Morgan",
    "Parker","Quinn","Riley","Rowan","Skyler","Taylor","Alex","Casey",
    "Jamie","Jesse","Lee","Shawn","Sam","Noah","Mia","Liam","Emma"
]
_LAST_NAMES = [
    "Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis",
    "Rodriguez","Martinez","Hernandez","Lopez","Gonzalez","Wilson"]