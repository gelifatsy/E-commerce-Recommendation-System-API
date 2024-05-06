# E-commerce-Recommendation-System API

## Overview
The Product and purchase group Recommendation System is a comprehensive solution that provides personalized product recommendations to users based on their interactions and demographic information. The system employs two main approaches: item-based collaborative filtering for users with prior interactions and popularity-based recommendations for new users.

## Features
1. **Item-based Collaborative Filtering**:
   - Calculates item-item similarity based on user interaction patterns
   - Leverages item similarities to recommend products that are similar to those the user has already interacted with
   - Ensures diversity by recommending items from different categories

2. **Popularity-based Recommendations**:
   - Provides recommendations based on the popularity of products within the user's demographic segment
   - Considers the user's gender and age group to determine the relevant demographic segment
   - Ensures diversity by selecting popular items from different product categories

3. **Purchase Group Recommendation System**:
   - Utilizes user-based collaborative filtering and hierarchical clustering
   - Identifies similar users based on their interaction patterns
   - Generates personalized recommendations for active users within the same cluster
   - Provides popularity-based recommendations for new or inactive users

## Architecture
The recommendation system is built upon the following components:

1. **Item-based Collaborative Filtering**:
   - Interaction matrix creation
   - Item-item similarity calculation using cosine similarity
   - Personalized recommendation generation

2. **Popularity-based Recommendations**:
   - User demographic information retrieval
   - Demographic segment determination
   - Popular item selection within the user's demographic segment

3. **Purchase Group Recommendation System**:
   - User-based collaborative filtering using cosine similarity
   - Hierarchical clustering with Ward's method
   - Cluster-based personalized recommendations for active users
   - Popularity-based recommendations for new or inactive users

## Usage
The `recommend_products` function serves as the entry point for generating product recommendations. It takes the user ID and the desired number of recommendations as input, and returns the recommended products.

```python
recommended_products = recommend_products(user_id, num_recommendations=10)
```

## Dependencies
- Python
- Pandas
- NumPy
- Scipy
- Scikit-learn


## Installation
1. Clone the repository:
   ```
   git clone https://github.com/gelifatsy/E-commerce-Recommendation-System-API.git 
   ```
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Contributions
Contributions to the ChipChip Product Recommendation System are welcome. If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License
This project is licensed under the [MIT License](LICENSE).