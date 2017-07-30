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

static_path = '/home/brose/testing_images/'

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

def find_largest(node_tuples, match_exact=True):
    largest_size = None
    largest_image = None
    original_hash = None
    hash_passes = True
    for node_tuple in node_tuples:
        filepath = node_tuple[1].filepath
        #TODO - handle exception in case file was moved or corrupted
        try:
            filesize = os.path.getsize("%s%s" % (static_path, filepath))
        except:
            continue
        filehash = node_tuple[0]
        if not original_hash:
            print("Looking at ORIGINAL key: %s" % filepath)
            original_hash = node_tuple[1].hashvalue
        print("\tcomparing with: %s" % filepath)
        if filehash == original_hash or not match_exact:
            hash_passes = True
            print("\tfound match: %s" % filepath)
        else:
            hash_passes = False
            print("\tNOT match: %s" % filepath)
        if not largest_size or largest_size < filesize and hash_passes:
            largest_size = filesize
            largest_image = node_tuple[1]
    return largest_image

def create_dupe_index():
    distance = 10
    dupe_index = {}
    tree = load_tree()
    for image in tree:
        print("tree image filepath: %s" % image.filepath)
        matches = tree.find(image, distance)
        if not len(matches) > 1:
            print("NO MATCHES FOUND\n")
            continue
        print("FOUND MATCHES:::\n")
        for match in matches:
            print("\t\t%s\n" % match[1].filepath)
        largest_image = find_largest(matches)
        if matches and not dupe_index.get(image.filepath):
            minus_key = [x for x in matches if x[1].filepath != largest_image.filepath]
            dupe_index[largest_image.filepath] = minus_key
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

    paginator = Paginator(dupe_index.items(), 5)
    page = request.GET.get('page')
    try:
        dupe_lists = paginator.page(page)
    except PageNotAnInteger:
        dupe_lists = paginator.page(1)
    except EmptyPage:
        dupe_lists = paginator.page(paginator.num_pages)
    context = {'dupe_lists':dupe_lists}
    return render(request, 'dupes/index.html', context)

