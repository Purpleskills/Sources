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
                            title = courseitem['title'] if 'title' in courseitem else None
                            url = courseProvider.url + courseitem['url'] if 'url' in courseitem else None
                            price = courseitem['price_detail']['amount'] if 'price_detail' in courseitem else None
                            thumbnail = courseitem['image_480x270'] if 'image_480x270' in courseitem else None

                            if title and url:
                                defaults = { 'title' : title, 'url' : url, 'provider' : courseProvider,
                                            'difficulty' : level[1].value, 'status' : 1,
                                            'price' : price,
                                            'thumbnail' : thumbnail, 'duration' : timedelta(hours=duration[1])}

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
import csv
import urllib3

class PluralSightImport(LoginRequiredMixin, TemplateView):
    levels = {}
    levels[0] = {'fundamentals', 'beginner', 'introduction', 'meet', 'getting started', 'introduces', 'basics'}
    levels[1] = {'advanced'}
    ignore_words = {'team-foundation', 'team foundation'}

    def computeDifficulty(self, courseId, courseTitle, courseDesc):
        courseTitle = courseTitle.lower()
        courseDesc = courseDesc.lower()
        # first remove ignore words
        for word_to_ignore in self.ignore_words:
            courseId = courseId.replace(word_to_ignore, '')
            courseTitle = courseTitle.replace(word_to_ignore, '')
            courseDesc = courseDesc.replace(word_to_ignore, '')

        courseId = courseId.split('-')
        courseTitle = courseTitle.split()
        courseDesc = courseDesc.split()

        if len(self.levels[0].intersection(courseId)) > 0 or len(self.levels[0].intersection(courseTitle)) > 0:
            return DifficultyChoice.Beginner.value

        if len(self.levels[1].intersection(courseId)) > 0 or len(self.levels[1].intersection(courseTitle)) > 0:
            return DifficultyChoice.Advanced.value

        if len(self.levels[0].intersection(courseDesc)) > 0:
            return DifficultyChoice.Beginner.value

        if len(self.levels[1].intersection(courseDesc)) > 0:
            return DifficultyChoice.Advanced.value

        return DifficultyChoice.Intermediate.value

    def get(self, request, *args, **kwargs):
        courseProvider = CourseProvider.objects.get(name='PluralSight')
        url = 'http://api.pluralsight.com/api-v0.9/courses'
        http = urllib3.PoolManager()
        response = http.request('GET', url)
        cr = csv.reader(response.data.decode("utf-8").splitlines())
        omittedFirstRow = False
        for courseitem in cr:
            if omittedFirstRow == False:
                omittedFirstRow = True
            else:
                if courseitem[5] == 'Live':
                    defaults = {'course_id': courseitem[0], 'title': courseitem[1], 'url': courseProvider.url + '/' + courseitem[0],
                                'provider': courseProvider, 'difficulty': self.computeDifficulty(courseitem[0], courseitem[1], courseitem[4]), 'status': 1,
                                'description': courseitem[4], 'duration': timedelta(seconds=int(courseitem[2]))}

                    course, created = Course.objects.get_or_create(course_id=courseitem[0], defaults=defaults)
                    if created:
                        course.save()

        return HttpResponse("Success")


# https://api.coursera.org/api/courses.v1?start=0&limit=3&includes=instructorIds,partnerIds,specializations,s12nlds,v1Details,v2Details,instructors.v1(title)&fields=instructorIds,partnerIds,specializations,s12nlds,description,display,photoUrl,description,v1Details,v2Details,instructors.v1(title),totalDuration
