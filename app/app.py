#FAST API

import sys
import pandas as pd


sys.path.append('..')

from fastapi import FastAPI, HTTPException
from utils.group_recommendation import RecommendationSystem
from sklearn.metrics.pairwise import cosine_similarity
from utils.products_recommendation import ProductRecommender

app = FastAPI()