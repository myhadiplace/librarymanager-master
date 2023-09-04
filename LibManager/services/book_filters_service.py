from ..repository.repository import get_book_by_filters

def filter_book_service(genre=None,author_country=None,price_max=None,price_min=None):
            all_book = get_book_by_filters(genre,author_country,price_min,price_max)
            if not all_book['error']:
                books = [all_book.book for book in all_book]
            return books
        
   