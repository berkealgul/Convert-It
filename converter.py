import os
import sys
import imageio
from PIL import Image   
from pydub import AudioSegment
import moviepy.editor as mp


formats = {"Audio" : ["mp3", "wav", "flac", "ogg", "aiff", "m4a", "acc", "wma"],
            "Image" : ["bmp", "png", "jpeg", "jpg", "gif", "webp", "tiff", "raw", "svg", "tga", "tiff"],
            "Video" : ["mp4", "mkv", "flv", "avi", "webm", "wmv", "ogv", "mpg", "mov"]}

# coversion result codes
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
    targetType = formatType(mediaItem.targetFormat)

    if inputType is None or targetType is None:
        return ERROR_INVALID_FORMAT
    try:
        if inputType == targetType == "Audio":
            AudioSegment.from_file(mediaItem.path, format=mediaItem.format).export(targetPath, mediaItem.targetFormat)
        elif inputType == targetType == "Image":
            Image.open(mediaItem.path).save(targetPath)
        elif inputType == targetType == "Video":
            clip = mp.VideoFileClip(mediaItem.path)
            clip.write_videofile(targetPath)
        elif inputType == "Video" and targetType == "Audio":
            clip = mp.VideoFileClip(mediaItem.path)
            clip.audio.write_audiofile(targetPath)
    except Exception as e:
        print(e)
        return UNKNOWN_ERROR, str(e)

    return COMPLETED, None

# unused for now
def convertVideoToSound(videoPath, soundPath):
    clip = mp.VideoFileClip(videoPath)
    clip.audio.write_audiofile(soundPath)
