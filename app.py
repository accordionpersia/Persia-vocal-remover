import gradio as gr
import subprocess
import os
import tempfile
import shutil


def remove_vocals(audio_file):
    if audio_file is None:
        return None, None

    work_dir = tempfile.mkdtemp()

    try:
        subprocess.run(
            [
                "python",
                "-m",
                "demucs",
                "--two-stems=vocals",
                "-o",
                work_dir,
                audio_file,
            ],
            check=True,
        )

        song_name = os.path.splitext(os.path.basename(audio_file))[0]

        output_dir = os.path.join(
            work_dir,
            "htdemucs",
            song_name
        )

        vocals = os.path.join(output_dir, "vocals.wav")
        instrumental = os.path.join(output_dir, "no_vocals.wav")

        final_vocals = "/tmp/persia_vocals.wav"
        final_instrumental = "/tmp/persia_instrumental.wav"

        shutil.copy(vocals, final_vocals)
        shutil.copy(instrumental, final_instrumental)

        return final_vocals, final_instrumental

    except Exception as e:
        raise gr.Error(f"Processing error: {str(e)}")


with gr.Blocks(title="Persia Vocal Remover") as app:

    gr.Markdown(
        """
        # 🎵 Persia Vocal Remover
        ### Persia Accordion

        حذف صدای خواننده از آهنگ با هوش مصنوعی

        فایل آهنگ خود را انتخاب کنید و صدای خواننده و موسیقی
        را به صورت جداگانه دریافت کنید.

        **www.accordions.ir**
        """
    )

    audio_input = gr.Audio(
        type="filepath",
        label="انتخاب آهنگ"
    )

    process_button = gr.Button(
        "حذف صدای خواننده"
    )

    vocals_output = gr.Audio(
        label="صدای خواننده"
    )

    instrumental_output = gr.Audio(
        label="موسیقی بدون صدای خواننده"
    )

    process_button.click(
        fn=remove_vocals,
        inputs=audio_input,
        outputs=[
            vocals_output,
            instrumental_output
        ]
    )


app.launch()
