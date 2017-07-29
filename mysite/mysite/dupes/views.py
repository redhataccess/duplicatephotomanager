import pickle
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse
import dhash
from pybktree import BKTree
import os
import wand
import re

def load_tree():
    pickle_tree_path = "/home/brose/bktree"
    if os.path.isfile(pickle_tree_path):
        return pickle.load(open(pickle_tree_path, "rb"))
    else:
        tree = create_tree()
        pickle.dump(tree, open(pickle_tree_path, "wb"))
        return tree

def mybitsdifferent(x, y):
    return dhash.get_num_bits_different(x.hashvalue, y.hashvalue)

class MyImage():
    def __init__(self, hashvalue, filepath=None):
        self.hashvalue = hashvalue
        self.filepath = filepath

def create_tree():

    #tree = BKTree(dhash.get_num_bits_different)
    tree = BKTree(mybitsdifferent)
    static_path = '/home/brose/Pictures/'

    for root, dirs, filenames in os.walk(static_path):
        for f in filenames:
            if '.jpg' in f or '.JPG' in f:
                path = os.path.join(root, f)
                try:
                    with wand.image.Image(filename=path) as image:
                        #row_hash, col_hash = dhash.dhash_row_col(image, 8)
                        hash_long = dhash.dhash_int(image, size=8)
                        print("hash value for %s: %s" % (f, hash_long))
                        path = re.sub(static_path, '', path)
                        tree.add(MyImage(hash_long, path))
                except:
                    continue
    return tree

def create_dupe_index():
    distance = 10
    dupe_index = {}
    tree = load_tree()
    for image in tree:
        #create dict entry whether or not matches present for now.. consider leaving it this way
        if not dupe_index.get(image.filepath):
            dupe_index[image.filepath] = tree.find(image, distance)
    return dupe_index

def load_dupe_index():
    dupe_index_path = "/home/brose/dupe_index"
    if os.path.isfile(dupe_index_path):
        return pickle.load(open(dupe_index_path, "rb"))
    else:
        dupe_index = create_dupe_index()
        pickle.dump(dupe_index, open(dupe_index_path, "wb"))
        return dupe_index
"""
def search_tree(my_image, distance):
    tree = load_tree()
    print("tree is type: %s" % type(tree))
    found = tree.find(my_image, distance)
    pics = []
    for distance, image in found:
        print("tree item is type: %s" % type(image))
        print("distance is %s" % distance)
        print("item is %s" % image)
        pics.append(image.filepath)

    context = {
        'images': pics,
    }
    #return render('dupes/index.html', context)
    return context
"""

def index(request):
    #distance = int(request.GET.get('distance', 0))
    #context = search_tree(MyImage(320015714244132890896587944663344678851L), distance)
    #context = search_tree(MyImage(119349068980206672214822919316039535229L), distance)
    dupe_index = load_dupe_index()

    paginator = Paginator(dupe_index.items(), 10)
    page = request.GET.get('page')
    try:
        dupe_lists = paginator.page(page)
    except PageNotAnInteger:
        dupe_lists = paginator.page(1)
    except EmptyPage:
        dupe_lists = paginator.page(paginator.num_pages)
    context = {'dupe_lists':dupe_lists}
    return render(request, 'dupes/index.html', context)
