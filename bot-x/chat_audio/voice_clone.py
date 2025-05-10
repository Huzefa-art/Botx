import torch
from TTS.api import TTS

class VoiceCloner:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VoiceCloner, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_name = "tts_models/multilingual/multi-dataset/your_tts"
        self.tts = TTS(model_name=self.model_name, progress_bar=True).to(device)

    def clone_voice(self, text, input_audio_path, output_audio_file_path):
        self.tts.tts_to_file(
            text=text, 
            speaker_wav=input_audio_path, 
            language="en", 
            file_path=output_audio_file_path
        )
        print('output_voice_path', output_audio_file_path)
        return output_audio_file_path

# Example usage
if __name__ == '__main__':
    cloner = VoiceCloner()
    cloner.clone_voice(
        'Hi my name is faizan, I am currently working as a Software Engineer at xloop',
        '../media/audio/hello.mp3',
        '../media/audio/output4.mp3'
    )
