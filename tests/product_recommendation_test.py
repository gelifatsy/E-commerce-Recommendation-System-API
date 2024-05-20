import sys
import pytest
import pandas as pd
import os
# print(os.getcwd())
sys.path.append('..')

from utils.products_recommendation import ProductRecommender, load_and_preprocess_data

# Define a fixture to load and preprocess the data once per test session
@pytest.fixture(scope='session')
def load_data():
    user_path = 'C:/Users/Elias_A/Documents/ChipChip/Notebook/CleanedData/filtered_users.csv'
    user_products_path = 'C:/Users/Elias_A/Documents/ChipChip/Notebook/CleanedData/user_product.csv'
    products_path = 'C:/Users/Elias_A/Documents/ChipChip/Notebook/CleanedData/cleaned_products.csv'
    merged_user_product_path = 'C:/Users/Elias_A/Documents/ChipChip/Notebook/CleanedData/user_product_info.csv'
    user_df, user_product_df, products_df, merged_user_product_df = load_and_preprocess_data(user_path, user_products_path, products_path, merged_user_product_path)
    return user_df, user_product_df, products_df, merged_user_product_df

class TestProductRecommender:

    def test_init(self, load_data):
        user_df, user_product_df, products_df, merged_user_product_df = load_data
        recommender = ProductRecommender(user_df, user_product_df, products_df)  # Update the arguments here
        assert recommender.user_df.shape[0] > 0, "The user_df should have rows"
        assert recommender.user_product_df.shape[0] > 0, "The user_product_df should have rows"
        assert recommender.products_df.shape[0] > 0, "The products_df should have rows"

    def test_has_interactions(self, load_data):
        user_df, user_product_df, products_df, merged_user_product_df = load_data
        user_id = "ad752023-a7af-4b14-95d0-6399f95c6eb6"  # Replace with a valid user ID
        recommender = ProductRecommender(user_df, user_product_df, products_df)  # Update the arguments here
        assert recommender.has_interactions(user_id) in [True, False], "has_interactions should return True or False"

    def test_item_based_recommendations(self, load_data):
        user_df, user_product_df, products_df, merged_user_product_df = load_data
        user_id = "ad752023-a7af-4b14-95d0-6399f95c6eb6"  # Replace with a valid user ID
        recommender = ProductRecommender(user_df, user_product_df, products_df)  # Update the arguments here
        recommendations = recommender.item_based_recommendations(user_id)
        assert 'recommended_products' in recommendations, "The recommendations should contain a 'recommended_products' key"
        assert len(recommendations['recommended_products']) > 0, "The item-based recommendations should return at least one product"

    def test_popular_items_recommendation(self, load_data):
        user_df, user_product_df, products_df, merged_user_product_df = load_data
        user_id = "c6376a5e-c705-4b7c-aa86-491473ab2969"  # Replace with a valid user ID
        recommender = ProductRecommender(user_df, user_product_df, products_df)  # Update the arguments here
        recommendations = recommender.popular_items_recommendation(user_id)
        assert 'recommended_products' in recommendations, "The recommendations should contain a 'recommended_products' key"
        assert len(recommendations['recommended_products']) > 0, "The popular items recommendations should return at least one product"

    def test_recommend_products(self, load_data):
        user_df, user_product_df, products_df, merged_user_product_df = load_data
        user_id = "ad752023-a7af-4b14-95d0-6399f95c6eb6"  # Replace with a valid user ID
        recommender = ProductRecommender(user_df, user_product_df, products_df)  # Update the arguments here
        recommendations = recommender.recommend_products(user_id)
        assert 'recommended_products' in recommendations, "The recommendations should contain a 'recommended_products' key"
        assert len(recommendations['recommended_products']) > 0, "The recommend_products method should return at least one product"

if __name__ == "__main__":
    # Run all tests
    pytest.main(["-v", "--capture=no", "--html=product_recommendation_test_report.html", "--self-contained-html"])