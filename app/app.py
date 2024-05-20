#FAST API

import sys
import pandas as pd


sys.path.append('..')
from utils.group_recommendation import RecommendationSystem
from sklearn.metrics.pairwise import cosine_similarity
from utils.products_recommendation import ProductRecommender

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html

app = FastAPI()


# Load and preprocess data for group recommendations
def load_and_preprocess_group_data(groups_df_path):
    groups_df = pd.read_csv(groups_df_path)
    interaction_matrix = groups_df.pivot_table(index='user_id', columns='product_id', aggfunc='size', fill_value=0)
    similarity_matrix = cosine_similarity(interaction_matrix)

    return groups_df, interaction_matrix,similarity_matrix

def load_and_preprocess_products(user_path, user_products_path, products_path,merged_user_product_path):
    user_df = pd.read_csv(user_path)
    user_product_df = pd.read_csv(user_products_path)
    products_df = pd.read_csv(products_path)
    merged_user_product_df = pd.read_csv(merged_user_product_path)
    # interactions_matrix = user_product_df.pivot_table(index='product_id', columns='user_id', values='product_id', aggfunc=len, fill_value=0)
    # interactions_csr = csr_matrix(interactions_matrix.values)
    return user_df,user_product_df,products_df,merged_user_product_df
# Prepare the RecommendationSystem and ProductRecommender instances
# Pre-load and pre-process
user_path = 'C:/Users/Elias_A/Documents/E-commerce-Recommendation-System-API/Notebook/CleanedData/filtered_users.csv'
user_products_path = 'C:/Users/Elias_A/Documents/E-commerce-Recommendation-System-API/Notebook/CleanedData/user_product.csv'
products_path='C:/Users/Elias_A/Documents/E-commerce-Recommendation-System-API/Notebook/CleanedData/cleaned_products.csv'
merged_user_product_path = 'C:/Users/Elias_A/Documents/E-commerce-Recommendation-System-API/Notebook/CleanedData/user_product_info.csv'
user_df,user_product_df,products_df,merged_user_product_df = load_and_preprocess_products(user_path, user_products_path, products_path,merged_user_product_path)

groups_df_path = 'C:/Users/Elias_A/Documents/E-commerce-Recommendation-System-API/Notebook/CleanedData/cleaned_groups.csv'
groups_df, interaction_matrix,similarity_matrix = load_and_preprocess_group_data(groups_df_path)
recommender = RecommendationSystem(groups_df, interaction_matrix,similarity_matrix)

product_recommender = ProductRecommender(user_df, user_product_df, products_df)



app = FastAPI(title="ChipChip Recommendation API", version="1.0.0")

async def get_user_id(request: Request):
    user_id = request.cookies.get("user_id")  # Try to retrieve user_id from cookies
    # if not user_id:
    #     user_id = request.session.get("user_id")  # Try to retrieve user_id from session
    if not user_id:
        # If user_id is not found in cookies or session, use a default value for testing
        user_id = "c6376a5e-c705-4b7c-aa86-491473ab2969"  # Replace with your desired default user_id
    return user_id

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="ChipChip Recommendation API",
        version="1.0.0",
        description="API for group and product recommendations",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get("/group_recommendations/", response_description="Group recommendations for the user")
async def get_group_recommendations(user_id: str = Depends(get_user_id)):
    """
    Retrieve group recommendations for the given user.

    Args:
        user_id (str): The ID of the user.

    Returns:
        List[dict]: A list of group recommendations.
    """
    try:
        recommendations = recommender.get_user_recommendations(user_id)
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/product_recommendations/", response_description="Product recommendations for the user")
async def get_product_recommendations(user_id: str = Depends(get_user_id)):
    """
    Retrieve product recommendations for the given user.

    Args:
        user_id (str): The ID of the user.

    Returns:
        List[dict]: A list of product recommendations.
    """
    try:
        recommendations = product_recommender.recommend_products(user_id)
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
