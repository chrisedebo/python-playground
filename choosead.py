#! /usr/bin/python3

import os
import re
import random

prestr = 'pre-'
poststr = 'post-'
preposttypes = {'cine': 2, 'ad': 3 }
videotypes = {'trailer': 1}
dirtypes = {'cine': 'ads', 'ad': 'ads', 'trailer': 'ads'}

def selectrandomfiles(searchstr,noofitems,dir):
	"Select random number of files based on searchstr in directory dir"
	randomfiles = [f for f in os.listdir(dir) if re.match(searchstr + '*',f)]
	selectedrandomfiles = random.sample(randomfiles,noofitems)

	return selectedrandomfiles

def printvideos(videos):
	for videotype, videolist in videos.items():
		print("=====" + videotype + "=====")
		print("\n".join(videolist))
#Get Pre videos
prevideos = {}
for tstr, items in preposttypes.items():
	prevideos[tstr] = selectrandomfiles(prestr + tstr,items,dirtypes[tstr])

print("================Pre Videos================")
printvideos(prevideos)

#get other video types
othervideos = {}
for tstr, items in videotypes.items():
	othervideos[tstr] = selectrandomfiles(tstr,items,dirtypes[tstr])

print("================Other Videos================")
printvideos(othervideos)

#Select post videos to match Pre
postvideos = {}
for tstr, vidlist in prevideos.items():
	if type(vidlist) is list:
		postvideos[tstr] = [v.replace(prestr,poststr) for v in vidlist]
	else :
		postvideos[tstr] = vidlist.replace(prestr,poststr)

print("================Post Videos================")
printvideos(postvideos)


