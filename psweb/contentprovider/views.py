import psycopg2
import json
from django.views.generic import TemplateView
import ssl
from http.client import HTTPSConnection
from django.http import HttpResponse
from base64 import b64encode
from .models import *
from learn.models import Course, CourseTag, CourseProvider, DifficultyChoice, Instructor
import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import timedelta

userAndPass = b64encode(b"GpxNVedkBslJE6CTga0f56iRG4vzzmYU24gzH0g5:FGMx5x8Vjr7LyBokikzIT9t4uFSSa30HMhMGcEHZBy38FV2snjwew0l9o3ctugs1KRcIvBQyZDidYKuMKrWUGHCA0qRNYMvFg859QhpatbpBPZW3QNAeJzpHBAYNkBoy").decode("ascii")
headers = { 'Authorization' : 'Basic %s' %  userAndPass }

class UdemyImport(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        courseProvider = CourseProvider.objects.get(name='Udemy')
        # for each category and each level, get all the courses
        for category in UdemyCourseCategory.objects.all():
            defaults = {'priority': 100}
            categorytag, created = CourseTag.objects.get_or_create(name=category.title, defaults = defaults)
            if created:
                categorytag.save()
            for level in [('beginner', DifficultyChoice.Beginner), ('intermediate', DifficultyChoice.Intermediate), ('expert', DifficultyChoice.Advanced)]:
                for duration in [('short', 2), ('medium', 5), ('long', 12), ('extraLong', 22),]:
                    payload = {'category': category.title, 'instructional_level': level[0], 'page_size': 1000,
                               'duration': duration[0]}
                    request = requests.request('GET', 'https://www.udemy.com/api-2.0/courses', params=payload,
                                               headers=headers)
                    while True:
                        # c.request('GET', '/api-2.0/courses?page_size=10', headers=headers)
                        # get the response back
                        res = request.json()
                        # at this point you could check the status etc
                        # this gets the page text
                        # data = res.read()

                        # str_data = data.decode('utf8')
                        # json_data = json.loads(str_data)
                        results = res['results']
                        # print (results)
                        # data here is a list of dicts

                        for courseitem in results:
                            defaults = { 'title' : courseitem['title'], 'url' : courseProvider.url + courseitem['url'],
                                            'provider' : courseProvider, 'difficulty' : level[1].value, 'status' : 1,
                                            'price' : courseitem['price_detail']['amount'],
                                            'thumbnail' : courseitem['image_480x270'], 'duration' : timedelta(hours=duration[1]) }

                            course, created = Course.objects.get_or_create(course_id=courseitem['id'], defaults=defaults)
                            if created:
                                course.save()
                                course.tags.add(categorytag)
                                # add instructors
                                for instructor in courseitem['visible_instructors']:
                                    defaults = {'url' : courseProvider.url + instructor['url'], 'photo' : instructor['image_100x100']}
                                    newInstructor, created = Instructor.objects.get_or_create(name=instructor['name'], defaults = defaults)
                                    if created:
                                        newInstructor.save()
                                    course.instructors.add(newInstructor)
                        if res['next']:
                            request = requests.request('GET', res['next'], headers=headers)
                        else:
                            break

        return HttpResponse("Success")



#This sets up the https connection
c = HTTPSConnection("www.udemy.com", context=ssl._create_unverified_context())
#we need to base 64 encode it 
#and then decode it to acsii as python 3 stores it as a byte string
#then connect

# conn = psycopg2.connect(database='purpleskillsdb', user='psroot', password='pswhatever1', host='127.0.0.1', port='')
# udemyPrefix = "https://www.udemy.com"
# #print (data)
# cur = conn.cursor()
#
#
# cur.execute("INSERT INTO learn_courseprovider (name, status, logo) SELECT %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM learn_courseprovider where name = \'Udemy\') ", ("Udemy","0","https://www.udemy.com/staticx/udemy/images/v6/mstile-144x144.png"))
#
# for item in results:
#     my_data = {field: item[field] for field in fields}
#     cur.execute("INSERT INTO contentprovider_udemycourse (id,title,url) VALUES (%s, %s, %s) ON CONFLICT(id) DO NOTHING ", (my_data['id'],my_data['title'],udemyPrefix+my_data['url']))
#     cur.execute("INSERT INTO learn_course (title,url, provider_id) SELECT  %s, %s, ID FROM learn_courseprovider where name = \'Udemy\' AND  NOT EXISTS (SELECT 1 FROM learn_course where title=%s)", (my_data['title'],udemyPrefix+my_data['url'], my_data['title']))
#
#
#
#
# # commit changes
# conn.commit()
# # Close the connection
# conn.close()
