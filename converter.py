import os
import sys
import imageio
from pydub import AudioSegment


formats = {"Audio" : ["mp3", "wav", "m4a"],
            "Image" : ["png", "jpeg", "jpg"]}

class Converter:
    def convert(inputPath, inputFormat, targetDir, targetFormat, inputName):
        targetPath = targetDir+inputName+"."+targetFormat
        AudioSegment.from_file(inputPath, format=inputFormat).export(targetPath, format=targetFormat)
        print("Complete")
    
    def convert(mediaItem, globalTargetDir=None):
        # if there is none global dir use input dir
        if globalTargetDir is None:
            targetPath = "C:/Berke/"+mediaItem.name+"."+mediaItem.targetFormat
        else:
            targetPath = globalTargetDir+mediaItem.name+"."+mediaItem.targetFormat

        AudioSegment.from_file(mediaItem.path, format=mediaItem.format).export(targetPath, format="mp3")
        print("Complete")


# ----------IRRELEVANT BELLOW------------
def convertFile(inputPath, targetFormat):
    outputPath = os.path.splitext(inputPath)[0] + targetFormat
    print("converting\r\n\t{0}\r\nto\r\n\t{1}".format(inputPath, outputPath))

    reader = imageio.get_reader(inputPath)
    fps = reader.get_meta_data()['fps']

    writer = imageio.get_writer(outputPath, fps=fps)
    for i,im in enumerate(reader):
        sys.stdout.write("\rframe {0}".format(i))
        sys.stdout.flush()
        writer.append_data(im)
    print("\r\nFinalizing...")
    writer.close()
    print("Done.")

def convert(inputPath, targetFormat):
    inputFormat = os.path.splitext(inputPath)[1][1:]
    outputPath = os.path.splitext(inputPath)[0] + "." + targetFormat
    print(inputPath)
    print(inputFormat)

    AudioSegment.from_file(inputPath, format=inputFormat).export(outputPath, format=targetFormat)

def readme():
    print("Arguments")
    print("-i <input file>")
    print("-o <output directory>")
    print("-f <output format>")
    print("help for getting this list again in future")


if __name__ == "__main__":
    import getopt

    argv = sys.argv[1:]

    if(len(argv) == 0):
        readme()
        sys.exit(1)
    elif(argv[0] == "help"):
        readme()

    try:
        opts, args = getopt.getopt(argv,"i:o:f:")
    except getopt.GetoptError:
        print("error")
        sys.exit(1)

    for opt, arg in opts:
        print(opt, arg)
        if opt == '-h':
            sys.exit()
        elif opt in ("-i"):
            inputfile = arg
        elif opt in ("-o"):
            outputfile = arg
        elif opt in ("-f"):
            pass

    convert(inputfile, "wav")
    
    