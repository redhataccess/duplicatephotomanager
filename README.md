# duplicatephotomanager
This is a project to find and safely delete duplicate photos.
There is currently an issue pending to make this work across platforms.
Developed on linux.

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
1. open a browser and go to http://127.0.0.1:8000/dupes/
1. click on any files you want to delete on the current page
1. click the delete button
1. the image should be replaced by an icon indicating that it could not be loaded
1. in a terminal, go to the 'root' photos directory that you set before and run find . -iname 'deleteME\_\*' and you should see the ones you deleted come back in the results
1. to actually delete them, run find . -iname 'deleteME\_\*' | xargs rm -f
1. to change the names back, run something like this example (linux):

`find . -iname 'deleteME_*' | sed 's/ /\\ /g' | sed 's/\(\(.*\)deleteME_\(.*\)\)/ mv \1 \2\3/g' | sh`


The resulting duplicate listings are paginated, so there is a small navigation link at the very bottom, but the app responds to arrow keys as well.

It is planned to create a preview page of images 'deleted' (renamed) and buttons to really delete them or undo (which will just remove the prepended 'deleteME\_' from the file name.

**Note: It may take significant amount of time to load the first time you load the page, depending on your system and the number of images.**

