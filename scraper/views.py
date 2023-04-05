from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Page, Link
from .serializers import PageSerializer, LinkSerializer
import requests
from bs4 import BeautifulSoup
import threading
from rest_framework.pagination import PageNumberPagination
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class PagePagination(PageNumberPagination):
    page_size = 5

class LinksPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    pagination_class = PagePagination

    @action(detail=True)
    def links(self, request, pk=None):
        page = self.get_object()
        links = Link.objects.filter(page=page)
        paginator = LinksPagination()
        result_page = paginator.paginate_queryset(links, request)
        serializer = LinkSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_page(self, request):
        url = request.data.get('url')
        try: 
            validator = URLValidator()
            validator(url)
            page = Page.objects.create(url=url, is_processing=True)
            thread = threading.Thread(target=self.save_scraped_data, args=(page,))
            thread.start()
            serializer = PageSerializer(page)
            return Response(serializer.data, status=201)
        except ValidationError as exception:
            return Response({'error':'Invalid URL'},status=400)
        except:
            return Response({'error': str(e)}, status=400)

    def save_scraped_data(self,page):
        try:
            links, page_name = self.scrape_page(page.url)
            page.title = page_name
            page.num_links = len(links)
            page.is_processing = False
            page.save()
            for link_url, link_name in links:
                Link.objects.create(page=page, url=link_url, name=link_name)
        except Exception as e:
            print(f"Error scraping page: {page.url} - {e}")
            return Response({'error': str(e)}, status=400)

    def scrape_page(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a')
        link_list = []
        for link in links:
            if link.has_attr('href'):
                link_url = link['href']
                link_name = link.text.strip()
                link_list.append((link_url, link_name))
        return link_list, soup.title.string

