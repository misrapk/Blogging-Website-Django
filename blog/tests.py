from django.contrib.auth import get_user_model  #to reference our active User
from django.test import Client, TestCase   #client is used as dummy webbrowser for GET and POST requests
from django.urls import reverse

from .models import Post

class BlogTests(TestCase):
    
    #create sample blog post
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = 'testuser',
            email = 'test@email.com',
            password = 'secret'
        )
        
        self.post = Post.objects.create(
            title = 'A good title',
            body ='Nice body content',
            author = self.user,
        )
        
    #to confirm that string representation is correct
    def test_string_representation(self):
        post = Post(title = 'A sample title')
        self.assertEqual(str(post), post.title)
        
    #to confirm that post content is correct
    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'A good title')
        self.assertEqual(f'{self.post.author}','testuser')
        self.assertEqual(f'{self.post.body}', 'Nice body content')
      
      
    #to confirm that our homepage returns a 200 HTTP status code, contain body text and uses home.html  
    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nice body content')
        self.assertTemplateUsed(response, 'home.html')
        
    
    #test detail page; if incorrect then return 404
    def test_post_detail_view(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'A good title')
        self.assertTemplateUsed(response, 'post_detail.html')
        