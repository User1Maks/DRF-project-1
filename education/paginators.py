from rest_framework.pagination import PageNumberPagination


class EducationPaginator(PageNumberPagination):
    page_size = 2  # кол-во сущностей, которое будет выведено на 1 стр

    # если пользователь передаст в запросе
    # параметр page_size, то он может указать кол-во записей на стр
    # самостоятельно
    page_size_query_param = 'page_size'
    max_page_size = 10  # максимальный page_size на стр
