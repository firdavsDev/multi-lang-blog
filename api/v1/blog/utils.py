def clean_query_data(query_data: dict):
    """for get request, we need to clean the query data

    Args:
        query_data (dict): query data from get request

    Returns:
        _type_: query data cleaned
    """
    query_data_new = query_data.copy()
    for i in query_data:
        if not query_data[i]:
            query_data_new.pop(i)
        elif query_data[i].lower() in ["undefined", "null", "none"]:
            query_data_new.pop(i)
    return query_data_new
