from pydub import AudioSegment
#ss
path = "C:\Berke\Sound-Video-Converter\src\Heartbeat flatline.mp3"
media_type = path[-4:0] 
AudioSegment.from_file(path, format=media_type).export("demo.wav", format='wav')