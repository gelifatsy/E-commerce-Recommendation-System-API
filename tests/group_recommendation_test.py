import sys
import pytest
import pandas as pd

sys.path.append('..')

from utils.group_recommendation import RecommendationSystem, load_and_preprocess_data
from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import linkage, fcluster
from functools import lru_cache

# Define a fixture to load and preprocess the data once per test session
@pytest.fixture(scope='session')
def load_data():
    groups_df_path = "C:/Users/Elias_A/Documents/ChipChip/Notebook/CleanedData/cleaned_groups.csv"
    groups_df, interaction_matrix, similarity_matrix = load_and_preprocess_data(groups_df_path)
    return groups_df, interaction_matrix, similarity_matrix

class TestRecommendationSystem:

    def test_init(self, load_data):
        groups_df, interaction_matrix, similarity_matrix = load_data
        recommender = RecommendationSystem(groups_df, interaction_matrix, similarity_matrix)
        assert recommender.groups_df.shape[0] > 0, "The groups_df should have rows"

    def test_cluster_users(self, load_data):
        groups_df, interaction_matrix, similarity_matrix = load_data
        recommender = RecommendationSystem(groups_df, interaction_matrix, similarity_matrix)
        clusters = recommender.cluster_users()
        assert len(set(clusters)) > 1, "There should be more than one cluster"

    def test_get_user_recommendations(self, load_data):
        groups_df, interaction_matrix, similarity_matrix = load_data
        user_id = "ad752023-a7af-4b14-95d0-6399f95c6eb6"   # Replace with a valid user ID
        recommender = RecommendationSystem(groups_df, interaction_matrix, similarity_matrix)
        recommendations = recommender.get_user_recommendations(user_id)
        assert 'recommended_users' in recommendations, "The recommendations should contain a 'recommended_users' key"

    def test_check_user_interactions(self, load_data):
        groups_df, interaction_matrix, similarity_matrix = load_data
        user_id = "ad752023-a7af-4b14-95d0-6399f95c6eb6"  # Replace with a valid user ID
        recommender = RecommendationSystem(groups_df, interaction_matrix, similarity_matrix)
        assert recommender.check_user_interactions(user_id) == True or False, "Check_user_interactions should return True or False"

    def test_recommend_top_users(self, load_data):
        groups_df, interaction_matrix, similarity_matrix = load_data
        recommender = RecommendationSystem(groups_df, interaction_matrix, similarity_matrix)
        top_users = recommender.recommend_top_users()
        assert len(top_users) > 0, "The recommend_top_users function should return at least one user"


   
if __name__ == "__main__":
    # Run tests and generate report
    pytest.main(["-v", "--capture=no", "--html=group_recommendation_test_report.html", "--self-contained-html"])