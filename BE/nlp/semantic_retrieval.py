from vector_db import search_index


def get_similar_interactions(query, index, interaction_history, k=5):
    similar_indices = search_index(query, index, k)
    similar_interactions = [interaction_history[i] for i in similar_indices]
    return similar_interactions