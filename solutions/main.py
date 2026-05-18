
from library import download_video
from library import read_urls_from_csv
from multiprocessing import Pool
import time

if __name__ == "__main__":
    urls = read_urls_from_csv("data/video_urls.csv")

    # Measure total serial execution time
    total_serial_time = 0.0
    for url in urls:
        start = time.perf_counter()
        download_video(url)
        end = time.perf_counter()
        total_serial_time += end - start
    total_serial_time = round(total_serial_time, 2)
    print(f"Serial execution: {total_serial_time}")

    # Measure total parallel execution time
    start = time.perf_counter()
    with Pool() as pool:
        pool.map(download_video, urls)
    end = time.perf_counter()
    parallel_time = round(end - start, 2)
    print(f"Parallel execution: {parallel_time}")

    speed_improvement = round(
        ((total_serial_time - parallel_time) / total_serial_time) * 100, 2
    ) if total_serial_time > 0 else 0.0

    with open("reports/sequential_report.md", "w") as f:
        f.write("# Report\n\n")
        f.write("## Serial execution\n\n")
        f.write(f"Total time: {total_serial_time:.2f} seconds\n\n")
        f.write("## Parallel execution\n\n")
        f.write(f"Total time: {parallel_time:.2f} seconds\n\n")
        f.write("## Comparison\n\n")
        f.write(f"Speed improvement: {speed_improvement:.2f}%\n")
