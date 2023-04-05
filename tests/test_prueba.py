import pytest
from unittest.mock import patch, MagicMock, Mock
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse

import django
django.setup()

from scraper.models import Page, Link
from scraper.serializers import PageSerializer, LinkSerializer
from scraper.views import PageViewSet, LinksPagination
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, APILiveServerTestCase, APIClient

@pytest.mark.django_db
class TestPageViewSet(APILiveServerTestCase):
    def setUp(self):
        self.client = APIClient()

    def test_add_page(self):
        url = reverse('page-list')
        data = {'url': 'https://www.google.com'}
        response = self.client.post('/api/add_page/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Page.objects.count() == 1
        mymodel = Page.objects.get()
        assert mymodel.url == 'https://www.google.com'

    def test_add_page_invalid_data(self):
        url = reverse('page-list')
        data = {'url':'BadUrl'}
        response = self.client.post('/api/add_page/', data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Page.objects.count() == 0

    def test_links(self):
        page = Page.objects.create(url='https://www.example.com')
        Link.objects.create(page=page, url='https://www.example.com/link1/', name='Link 1')
        Link.objects.create(page=page, url='https://www.example.com/link2/', name='Link 2')
        response = self.client.get(f'/api/scraped_pages/{page.id}/links/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)

    @patch('requests.get')
    def test_scrape_page(self, mock_get):
        mock_response = """
        <html>
            <head><title>Test Page</title></head>
        <body>
            <a href="http://test.com/foo">Foo</a>
            <a href="http://test.com/bar">Bar</a>
        </body>
        </html>
        """
        mock_get.return_value.content = mock_response.encode()
        page_viewset = PageViewSet()
        url = 'http://test.com'
        links, title = page_viewset.scrape_page(url)
        self.assertEqual(title, 'Test Page')
        self.assertEqual(len(links), 2)
        self.assertEqual(links[0], ('http://test.com/foo', 'Foo'))
        self.assertEqual(links[1], ('http://test.com/bar', 'Bar'))

    def test_save_scraped_data(self):
        page = Page.objects.create(url='http://example.com', title='Example')
        page_viewset = PageViewSet()

        # patch the return data from scrape_page method to isolate save_scraped_data functionality
        with patch('scraper.views.PageViewSet.scrape_page') as mock_scrape_page:
            mock_scrape_page.return_value = ([
                ('http://example.com/foo', 'Foo'),
                ('http://example.com/bar', 'Bar'),
            ], 'Example')
            page_viewset.save_scraped_data(page)

        page.refresh_from_db()
        assert page.title == 'Example'
        assert page.num_links == 2

        links = Link.objects.filter(page=page)
        assert len(links) == 2
        assert links[0].url == 'http://example.com/foo'
        assert links[0].name == 'Foo'
        assert links[1].url == 'http://example.com/bar'
        assert links[1].name == 'Bar'

    def test_page_pagination(self):
        for i in range(14):
            Page.objects.create(url=f"www.Test{i}.com")
        
        response = self.client.get('/api/scraped_pages/')
        assert response.status_code == 200
        assert len(response.data['results']) == 5 # default page size
        
        # go to second page
        response = self.client.get('/api/scraped_pages/?page=2')
        assert response.status_code == 200
        assert len(response.data['results']) == 5
        
        # go to third page, which should return the remaining 4 pages
        response = self.client.get('/api/scraped_pages/?page=3')
        assert response.status_code == 200
        assert len(response.data['results']) == 4

    def test_links_pagination(self):
        page = Page.objects.create(url=f"www.Test.com")
        
        for i in range(14):
            link = Link.objects.create(page=page, url=f"www.Test.com/link{i}", name=f'Test Link {i}')

        response = self.client.get(f'/api/scraped_pages/{page.id}/links/')
        assert response.status_code == 200
        assert len(response.data['results']) == 5 # default page size

         # go to second page
        response = self.client.get(f'/api/scraped_pages/{page.id}/links/?page=2')
        assert response.status_code == 200
        assert len(response.data['results']) == 5

        # go to third page, which should return the remaining 4 pages
        response = self.client.get(f'/api/scraped_pages/{page.id}/links/?page=3')
        assert response.status_code == 200
        assert len(response.data['results']) == 4