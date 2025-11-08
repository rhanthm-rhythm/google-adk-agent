from typing import Dict
import pathlib
import wave

from google.adk.tools import ToolContext
from google import genai
from google.genai import types


def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    """Helper function to save audio data as a wave file"""
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)
        

async def generate_podcast_audio(podcast_script: str, tool_context: ToolContext, filename: str = "'ai_today_podcast") -> Dict[str, str]:
    """
    Generates audio from a podcast script using Gemini API and saves it as a WAV file.

    Args:
        podcast_script: The conversational script to be converted to audio.
        tool_context: The ADK tool context.
        filename: Base filename for the audio file (without extension).

    Returns:
        Dictionary with status and file information.
    """
    try:
        client = genai.Client()
        prompt = f"TTS the following conversation between Joe and Jane:\n\n{podcast_script}"

        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-tts",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                        speaker_voice_configs=[
                            types.SpeakerVoiceConfig(speaker='Joe', 
                                                     voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name='Kore'))),
                            types.SpeakerVoiceConfig(speaker='Jane', 
                                                     voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name='Puck')))
                        ]
                    )
                )
            )
        )

        data = response.candidates[0].content.parts[0].inline_data.data

        if not filename.endswith(".wav"):
            filename += ".wav"

        # ** BUG FIX **: This logic now runs for all cases, not just when the extension is added.
        current_directory = pathlib.Path.cwd()
        file_path = current_directory / filename
        wave_file(str(file_path), data)

        return {
            "status": "success",
            "message": f"Successfully generated and saved podcast audio to {file_path.resolve()}",
            "file_path": str(file_path.resolve()),
            "file_size": len(data)
        }

    except Exception as e:
        error_msg = str(e)[:200]
        return {"status": "error", "message": f"Audio generation failed: {error_msg}"}
