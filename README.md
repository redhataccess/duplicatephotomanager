# duplicatephotomanager
This is a project to find and safely delete duplicate photos.

last edited on 08.01.2017


Currently it implements a dhash and kbtree mechanism to store/find distances in a reduced representation of each photo.

This allows detection of slightly different images such as resized or lower resolution that is not found in an md5 comparison.

References:
http://tech.jetsetter.com/2017/03/21/duplicate-image-detection/


Steps to run

1. gather photos and directories of photos so they have a common directory root
1. in another directory clone and cd into project
1. pip install -r requirements.txt
1. replace STATICFILES\_DIR to include a fully qualified path to the "root" directory from first step
1. replace pickle\_tree\_path, static\_path, and dup\_index\_path in mysite/mysite/dupes/views.py with directories that make sense to you
1. run the command `python manage.py runserver` from the mysite/mysite directory
1. open a browser and go to http://127.0.0.1:8000/

**Note: It may take significant amount of time to load the first time you load the page, depending on your system and the number of images.**

