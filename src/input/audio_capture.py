"""Audio capture from microphone"""

import pyaudio
import numpy as np
import soundfile as sf
from src.core.logger import logger

class AudioCapture:
    """Captures audio from microphone"""
    
    def __init__(self, sample_rate=16000, chunk_size=1024):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.format = pyaudio.paFloat32
        self.channels = 1
        self.p = pyaudio.PyAudio()
    
    def record(self, duration=5, device_index=None):
        """Record audio from microphone"""
        try:
            logger.info(f"Recording audio for {duration} seconds...")
            
            stream = self.p.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=self.chunk_size
            )
            
            frames = []
            for _ in range(0, int(self.sample_rate / self.chunk_size * duration)):
                data = stream.read(self.chunk_size)
                frames.append(np.frombuffer(data, dtype=np.float32))
            
            stream.stop_stream()
            stream.close()
            
            audio_data = np.concatenate(frames)
            logger.info("Recording completed")
            return audio_data
            
        except Exception as e:
            logger.error(f"Recording error: {e}")
            raise
    
    def load_audio_file(self, file_path):
        """Load audio from file"""
        try:
            audio_data, sr = sf.read(file_path)
            
            # Convert to mono if stereo
            if len(audio_data.shape) > 1:
                audio_data = np.mean(audio_data, axis=1)
            
            # Resample if necessary
            if sr != self.sample_rate:
                import librosa
                audio_data = librosa.resample(audio_data, orig_sr=sr, target_sr=self.sample_rate)
            
            return audio_data
            
        except Exception as e:
            logger.error(f"File loading error: {e}")
            raise
    
    def save_audio_file(self, audio_data, file_path):
        """Save audio to file"""
        try:
            sf.write(file_path, audio_data, self.sample_rate)
            logger.info(f"Audio saved to {file_path}")
        except Exception as e:
            logger.error(f"File saving error: {e}")
            raise
    
    def list_devices(self):
        """List available audio devices"""
        device_count = self.p.get_device_count()
        devices = []
        for i in range(device_count):
            info = self.p.get_device_info_by_index(i)
            devices.append({
                "index": i,
                "name": info['name'],
                "channels": info['maxInputChannels']
            })
        return devices
    
    def __del__(self):
        """Cleanup"""
        try:
            self.p.terminate()
        except:
            pass