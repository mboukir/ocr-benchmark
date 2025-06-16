import glob
import os
import subprocess
import time


def main():
    image_folder = "/workspaces/ocr/data"  # Replace with your image folder path
    ocr_engines = ["TesseractOCR", "EasyOCR", "MMOCR", "PaddleOCR"]
    results_folder = "./results"

    os.makedirs(results_folder, exist_ok=True)

    for engine in ocr_engines:
        # Launch the benchmark as a subprocess
        subprocess.run(
            [
                "python3.8",
                "benchmark.py",
                engine,
                image_folder
            ]
        )
        print(f"Benchmark for {engine} completed.")
        
        # Wait 5 seconds before starting the next benchmark
        time.sleep(5)


if __name__ == "__main__":
    main()