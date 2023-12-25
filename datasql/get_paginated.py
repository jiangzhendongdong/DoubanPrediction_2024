
def get_paginated_results(query, page, page_size):
    start = (page - 1) * page_size
    end = start + page_size
    items = query.slice(start, end).all()
    item_count = query.count()
    page_count = item_count // page_size + 1 if item_count % page_size != 0 else item_count // page_size
    return items, item_count, page_count
