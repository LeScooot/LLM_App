import boto3
from tempfile import NamedTemporaryFile
import pygame

class Speaker:
    def __init__(self):
        self.polly = boto3.client('polly', region_name='us-east-1')
        pygame.mixer.init()
        pygame.mixer.music.set_volume(1.0)


    def GenerateSpeech(self, text):
        response = self.polly.synthesize_speech(
            Engine='neural',
            Text=text,
            OutputFormat='mp3',
            VoiceId='Arthur'
        )

        if 'AudioStream' in response:
            with NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
                temp_audio_file.write(response['AudioStream'].read())
                temp_audio_file_path = temp_audio_file.name

            pygame.mixer.music.load(temp_audio_file_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        else:
            print("Could not stream audio")

