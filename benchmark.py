import time
import psutil
import argparse
import threading
import os
import glob
import numpy as np
import json

from ocr import TesseractOCR, EasyOCR, MMOCR, PaddleOCR

class Benchmark:
    def __init__(self, ocr_engine, image_paths):
        self.ocr_engine = ocr_engine
        self.image_paths = image_paths
        self.monitoring = True
        self.peak_memory = 0
        self.peak_cpu = 0
        self.median_memory_usage = 0
        self.median_cpu_usage = 0
        self.n_cpu = psutil.cpu_count(logical=True)
        self.n_images = len(image_paths)
        
    def _compute_base_memory(self):
        # Monitor the base memory usage before starting the benchmark
        memory_samples = []
        cpu_samples = []
        psutil.cpu_percent(interval=0)
        
        for _ in range(10):
            memory_info = psutil.virtual_memory()
            memory_samples.append(memory_info.used / (1024 * 1024))
            cpu_samples.append(psutil.cpu_percent(interval=0))

            time.sleep(1)  # Sleep for 10ms to avoid busy waiting

        self.median_memory_usage = np.median(memory_samples)
        self.median_cpu_usage = np.median(cpu_samples)
        
    def _monitor_resources(self):
        """Monitor global memory and CPU usage in a separate thread."""
        while self.monitoring:
            memory_info = psutil.virtual_memory()
            self.peak_memory = max(self.peak_memory, memory_info.used / (1024 * 1024))  # Convert to MB
            self.peak_cpu = max(self.peak_cpu, psutil.cpu_percent(interval=0))
            time.sleep(0.1)  # Monitor every 10ms

    def run(self):
        self._compute_base_memory()
        self.ocr_engine.initialize()

        start_time = time.time()

        # Start resource monitoring in a separate thread
        monitor_thread = threading.Thread(target=self._monitor_resources)
        monitor_thread.start()

        # Process the images
        for path in self.image_paths:
            text = self.ocr_engine.process_image(path)

        # Stop monitoring
        self.monitoring = False
        monitor_thread.join()

        elapsed_time = time.time() - start_time

        self.ocr_engine.cleanup()

        results = {
            "elapsed_time": elapsed_time,
            "mean_elapsed_time": elapsed_time / self.n_images,
            "peak_cpu": self.peak_cpu - self.median_cpu_usage,  # Peak CPU usage
            "peak_logical_cpu": (self.peak_cpu - self.median_cpu_usage) * self.n_cpu / 100, # Scale the cpu usage to logical CPUs
            "peak_memory": self.peak_memory - self.median_memory_usage,  # Peak global memory usage
        }
        
        json.dump(results, open(f'./results/{self.ocr_engine.__class__.__name__}_results.json', 'w+'), indent=4)
        
def main():
    parser = argparse.ArgumentParser(description="Run OCR benchmark.")
    parser.add_argument("ocr_engine", type=str, help="The OCR engine to benchmark (e.g., TesseractOCR, EasyOCR).")
    parser.add_argument("image_folder", type=str, help="Path to the folder containing images.")
    
    args = parser.parse_args()

    # Map OCR engine names to their respective classes
    ocr_engine_classes = {
        "TesseractOCR": TesseractOCR,
        "EasyOCR": EasyOCR,
        "MMOCR": MMOCR,
        "PaddleOCR": PaddleOCR,
    }

    if args.ocr_engine not in ocr_engine_classes:
        print(f"Error: Unknown OCR engine '{args.ocr_engine}'.")
        return

    # Initialize the OCR engine
    ocr_engine_class = ocr_engine_classes[args.ocr_engine]
    ocr_engine = ocr_engine_class()

    # Read image paths from the folder
    if not os.path.exists(args.image_folder):
        print(f"Error: Image folder '{args.image_folder}' does not exist.")
        return

    image_paths = glob.glob(f'{args.image_folder}/*.jpg')
    if not image_paths:
        print(f"Error: No images found in folder '{args.image_folder}'.")
        return

    # Run the benchmark
    benchmark = Benchmark(ocr_engine, image_paths)
    benchmark.run()

if __name__ == "__main__":
    main()