
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix


def load_and_preprocess_data(user_path, user_products_path, products_path, merged_user_product_path):
    user_df = pd.read_csv(user_path)
    user_product_df = pd.read_csv(user_products_path)
    products_df = pd.read_csv(products_path)
    merged_user_product_df = pd.read_csv(merged_user_product_path)

    # interactions_matrix = user_product_df.pivot_table(index='product_id', columns='user_id', values='product_id', aggfunc=len, fill_value=0)
    # interactions_csr = csr_matrix(interactions_matrix.values)
    return user_df,user_product_df,products_df,merged_user_product_df

# Pre-load and pre-process
user_path = 'C:/Users/Elias_A/Documents/ChipChip/Notebook/CleanedData/filtered_users.csv'
user_products_path = 'C:/Users/Elias_A/Documents/ChipChip/Notebook/CleanedData/user_product.csv'
products_path='C:/Users/Elias_A/Documents/ChipChip/Notebook/CleanedData/cleaned_products.csv'
merged_user_product_path = 'C:/Users/Elias_A/Documents/ChipChip/Notebook/CleanedData/user_product_info.csv'

user_df,user_product_df,products_df,merged_user_product_df = load_and_preprocess_data(user_path,user_products_path,products_path,merged_user_product_path)



class ProductRecommender:
    """
        A class for generating product recommendations based on user interactions and popularity.

        Attributes:
        - user_df: DataFrame containing user demographic information.
        - user_product_df: DataFrame containing user-product interactions.
        - products_df: DataFrame containing product information.

        Methods:
        - has_interactions(user_id): Checks if the user has any interactions.
        - item_based_recommendations(user_id, num_recommendations): Generates item-based recommendations for the user.
        - popular_items_recommendation(user_id, num_recommendations): Generates popularity-based recommendations for the user.
        - recommend_products(user_id, num_recommendations): Recommends products based on user interactions or popularity.

    """
    def __init__(self, user_df, user_product_df, products_df):
        self.user_df = user_df
        self.user_product_df = user_product_df
        self.products_df = products_df
        self.merged_user_product_df = merged_user_product_df

    def has_interactions(self, user_id):
        return self.user_product_df['user_id'].isin([user_id]).any()

    def item_based_recommendations(self, user_id, num_recommendations=10):
        # Create a pivot table
        interactions_matrix = self.user_product_df.pivot_table(index='product_id', columns='user_id', values='product_id', aggfunc=len, fill_value=0)
        interactions_csr = csr_matrix(interactions_matrix.values)

        # Compute item-item similarity matrix
        item_similarity = cosine_similarity(interactions_csr)
        item_similarity_df = pd.DataFrame(item_similarity, index=interactions_matrix.index, columns=interactions_matrix.index)

        # Get user interactions
        interacted_items = self.user_product_df[self.user_product_df['user_id'] == user_id]['product_id'].tolist()
        interacted_items_set = set(interacted_items)

        recommendations = {}
        for item_id in interacted_items:
            similar_items = item_similarity_df[item_id].sort_values(ascending=False).index[1:]
            for similar_item in similar_items:
                if similar_item not in interacted_items_set:
                    recommendations[similar_item] = recommendations.get(similar_item, 0) + item_similarity_df.loc[item_id, similar_item]

        # Sort by score and merge categories
        recommended_items = pd.DataFrame(list(recommendations.items()), columns=['product_id', 'score']).sort_values('score', ascending=False)
        recommended_items = recommended_items.merge(self.products_df[['product_id', 'product_category']], on='product_id', how='left')

        # Ensure initial category diversity
        final_recommendations = []
        seen_categories = set()
        additional_recommendations = []

        for _, row in recommended_items.iterrows():
            if row['product_category'] not in seen_categories:
                final_recommendations.append(row['product_id'])
                seen_categories.add(row['product_category'])
            else:
                additional_recommendations.append(row['product_id'])

            if len(final_recommendations) >= num_recommendations:
                break

        # Add additional recommendations if needed
        if len(final_recommendations) < num_recommendations:
            needed = num_recommendations - len(final_recommendations)
            final_recommendations.extend(additional_recommendations[:needed])

        # return final_recommendations
        return {'recommended_products': final_recommendations}

    # def popular_items_recommendation(self, user_id, num_recommendations=10):
    #     # Retrieve user demographic information
    #     user_info = self.user_df.loc[self.user_df['user_id'] == user_id]
    #     gender = user_info['gender'].iloc[0]
    #     age = user_info['age'].iloc[0]

    #     # Determine the demographic segment
    #     if age < 25:
    #         age_group = '18-24'
    #     elif age <= 35:
    #         age_group = '25-35'
    #     else:
    #         age_group = '36+'

    #     # Filter user_product_df for products popular within the user's demographic segment
    #     demographic_segment = f"{gender}_{age_group}"
    #     filtered_products = self.user_product_df[self.user_product_df['demographic_segment'] == demographic_segment]

    #     # Get most popular items within this segment
    #     popular_items = filtered_products['product_id'].value_counts().head(20).index.tolist()

    #     # Merge to get categories
    #     popular_items_with_cat = self.products_df[self.products_df['product_id'].isin(popular_items)]

    #     # Ensure category diversity
    #     seen_categories = set()
    #     diverse_popular_items = []
    #     for _, row in popular_items_with_cat.iterrows():
    #         if row['product_category'] not in seen_categories:
    #             diverse_popular_items.append(row['product_id'])
    #             seen_categories.add(row['product_category'])
    #         if len(diverse_popular_items) == num_recommendations:
    #             break

    #     # return diverse_popular_items
    #     return {'recommended_products': diverse_popular_items}
    def popular_items_recommendation(self, user_id, num_recommendations=10):
        # Retrieve user demographic information
        user_info = self.user_df.loc[self.user_df['user_id'] == user_id]
        gender = user_info['gender'].iloc[0]
        age = user_info['age'].iloc[0]

        # Determine the demographic segment
        if age < 25:
            age_group = '18-24'
        elif age <= 35:
            age_group = '25-35'
        else:
            age_group = '36+'

        # # Filter user_product_df for products popular within the user's demographic segment
        # demographic_segment = f"{gender}_{age_group}"
        # filtered_products = self.user_product_df[self.user_product_df['demographic_segment'] == demographic_segment]
        filtered_products = self.merged_user_product_df[self.merged_user_product_df['demographic_segment'] == age_group]

    # Get most popular items within this segment
        popular_items = filtered_products['product_id'].value_counts().head(20).index.tolist()

            # Merge to get categories
        popular_items_with_cat = self.products_df[self.products_df['product_id'].isin(popular_items)]

        # Ensure category diversity
        seen_categories = set()
        diverse_popular_items = []
        additional_popular_items = []

        for _, row in popular_items_with_cat.iterrows():
            if row['product_category'] not in seen_categories:
                diverse_popular_items.append(row['product_id'])
                seen_categories.add(row['product_category'])
            else:
                additional_popular_items.append(row['product_id'])

            if len(diverse_popular_items) >= num_recommendations:
                break

        # Add additional popular items if needed
        if len(diverse_popular_items) < num_recommendations:
            needed = num_recommendations - len(diverse_popular_items)
            diverse_popular_items.extend(additional_popular_items[:needed])

        return {'recommended_products': diverse_popular_items}

    
    
    def recommend_products(self, user_id, num_recommendations=10):
            """
            Recommends products based on user interactions or popularity.
            
            Args:
            - user_id: ID of the user for whom recommendations are to be generated.
            - num_recommendations: Number of recommendations to be returned.
            
            Returns:
            - List of recommended product IDs.
            """
            if self.has_interactions(user_id):
                # Generate item-based recommendations
                return self.item_based_recommendations(user_id, num_recommendations=10)
            else:
                # Generate popularity-based recommendations
                return self.popular_items_recommendation(user_id, num_recommendations=10)
            


# Create an instance of ProductRecommender
if __name__ == "__main__":
    # product_recommender = ProductRecommender(user_df, user_product_df, products_df)

    # Generate recommendations for a specific user

    # user_id = 'ad752023-a7af-4b14-95d0-6399f95c6eb6'  # Replace with the actual user ID
    # num_recommendations = 10  # Replace with the desired number of recommendations
    # recommendations = product_recommender.recommend_products(user_id, num_recommendations)
    # print(recommendations)

    product_recommender = ProductRecommender(user_df, user_product_df, products_df)
    user_id = "79d54965-a338-4f96-8a05-5cb978f0219f"
    recommendations = product_recommender.recommend_products(user_id)
    print(recommendations)
