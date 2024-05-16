import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import linkage, fcluster
from functools import lru_cache

def load_and_preprocess_data(groups_df_path):
    groups_df = pd.read_csv(groups_df_path)
    interaction_matrix = groups_df.pivot_table(index='user_id', columns='product_id', aggfunc='size', fill_value=0)
    similarity_matrix = cosine_similarity(interaction_matrix)

    return groups_df, interaction_matrix, similarity_matrix

# Pre-load and pre-process
groups_df_path = 'C:/Users/Elias_A/Documents/ChipChip/Notebook/CleanedData/cleaned_groups.csv'
groups_df, interaction_matrix, similarity_matrix = load_and_preprocess_data(groups_df_path)


class RecommendationSystem:
    def __init__(self, groups_df, interaction_matrix, similarity_matrix, max_d=7.5):
        self.groups_df = groups_df
        self.max_d = max_d
        self.interaction_matrix = interaction_matrix
        self.similarity_matrix = pd.DataFrame(similarity_matrix, index=interaction_matrix.index, columns=interaction_matrix.index)
        self.clusters = self.cluster_users()

        # Map clusters to users
        self.groups_df['cluster'] = self.groups_df['user_id'].map(self.clusters)

    @lru_cache(maxsize=None)  # Cache this method to avoid recalculating clusters
    def cluster_users(self):
        Z = linkage(self.similarity_matrix.values, method='ward')
        max_d = 7.5
        clusters = pd.Series(fcluster(Z, max_d, criterion='distance'), index=self.similarity_matrix.index)
        self.groups_df['cluster'] = self.groups_df['user_id'].map(clusters)
        return clusters

    def get_user_recommendations(self, user_id):
        return self.analyze_clusters(user_id)

    def analyze_clusters(self, user_id):
        if not self.check_user_interactions(user_id):
            return {'recommended_users': self.recommend_top_users()}

        user_cluster = self.groups_df.loc[self.groups_df['user_id'] == user_id, 'cluster'].values[0]
        cluster_users = self.groups_df.loc[self.groups_df['cluster'] == user_cluster, 'user_id']
        cluster_users = cluster_users[cluster_users != user_id]

        cluster_similarity_scores = self.similarity_matrix.loc[user_id, cluster_users].sort_values(ascending=False)
        recommended_users = cluster_similarity_scores.head(2).index.tolist()
        
        if len(recommended_users) < 2:
            other_users = self.groups_df.loc[~self.groups_df['user_id'].isin(cluster_users), 'user_id']
            other_similarity_scores = self.similarity_matrix.loc[user_id, other_users].sort_values(ascending=False)
            remaining_recommended_users = other_similarity_scores.head(2 - len(recommended_users)).index.tolist()
            recommended_users.extend(remaining_recommended_users)

        return {'recommended_users': recommended_users}

    def check_user_interactions(self, user_id):
        return user_id in self.interaction_matrix.index and self.interaction_matrix.loc[user_id].sum() > 0

    def recommend_top_users(self, n=2):
        user_interactions_count = self.interaction_matrix.sum(axis=1)
        top_users = user_interactions_count.nlargest(n).index.tolist()
        return top_users

# Example usage within the same module
if __name__ == "__main__":
    # path='C:/Users/Elias_A/Documents/ChipChip/Notebook/CleanedData/cleaned_groups.csv'
    recommender = RecommendationSystem(groups_df, interaction_matrix, similarity_matrix)
    user_id = "ad752023-a7af-4b14-95d0-6399f95c6eb6"
    recommendations = recommender.get_user_recommendations(user_id)
    print(recommendations)