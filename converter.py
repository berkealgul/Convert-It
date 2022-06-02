import os
import sys
import imageio
from PIL import Image   
from pydub import AudioSegment


formats = {"Audio" : ["aac", "mp3", "wav", "m4a"],
            "Image" : ["png", "jpeg", "jpg"],
            "Video" : ["mp4"]}

COMPLETED = 0
ERROR_INVALID_FORMAT = 1
UNKNOWN_ERROR = -1

def formatType(format):
    for type in formats:
        if format in formats[type]:
            return type

def convert(mediaItem, globalTargetDir=None):
    # if there is no global dir use input dir
    if globalTargetDir is None:
        targetPath = mediaItem.dir +  mediaItem.name + "." + mediaItem.targetFormat
    else:
        targetPath = globalTargetDir + mediaItem.name + "." + mediaItem.targetFormat

    inputType = formatType(mediaItem.format)
    targetType = formatType(mediaItem.format)


    if inputType is None or targetType is None:
        return ERROR_INVALID_FORMAT
    try:
        if inputType == targetType == "Audio":
            AudioSegment.from_file(mediaItem.path, format=mediaItem.format).export(targetPath, format="mp3")
        elif inputType == targetType == "Image":
            Image.open(mediaItem.path).save(targetPath)
        elif inputType == targetType == "Video":
            print("video-video") 
        elif inputType == "Video" and targetType == "Audio":
            print("video-audio")
    except Exception as e:
        print(e)
        return UNKNOWN_ERROR, str(e)

    return COMPLETED, None
