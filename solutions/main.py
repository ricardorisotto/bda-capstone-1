
from library import download_video
from library import read_urls_from_csv
from library import get_video_metadata
from multiprocessing import Pool
import time
import csv

if __name__ == "__main__":
    urls = read_urls_from_csv("data/video_urls.csv")
    results = []
    successful_count = 0
    failed_count = 0

    # Measure total serial execution time
    total_serial_time = 0.0
    for url in urls:
        start = time.perf_counter()
        result = download_video(url)
        end = time.perf_counter()
        results.append(result)
        total_serial_time += end - start
    total_serial_time = round(total_serial_time, 2)
    print(f"Serial execution: {total_serial_time}")

    with open("reports/sequential_report.md", "w") as f:
        f.write("# Report\n\n")
        f.write("## Serial execution\n\n")
        f.write(f"Total time: {total_serial_time:.2f} seconds\n\n")
        f.write("## Download status\n\n")
        for result in results:
            f.write(f"- {result['url']}: {result['status']}")
            if result['status'] == "failed":
                print(f"\n*** Error downloading {result['url']}: {result['error']}\n")
                failed_count += 1
            else:
                successful_count += 1
                
            f.write("\n")
    
        f.write("\n## Download status\n\n")
        f.write(f"- Successful downloads: {successful_count}\n")
        f.write(f"- Failed downloads: {failed_count}\n")


    # Measure total parallel execution time
    start = time.perf_counter()
    with Pool() as pool:
        parallel_results = pool.map(download_video, urls)
    end = time.perf_counter()
    parallel_time = round(end - start, 2)
    print(f"Parallel execution: {parallel_time}")

    # Count parallel results
    parallel_successful = sum(1 for r in parallel_results if r['status'] == 'success')
    parallel_failed = sum(1 for r in parallel_results if r['status'] == 'failed')

    speed_improvement = round(
        ((total_serial_time - parallel_time) / total_serial_time) * 100, 2
    ) if total_serial_time > 0 else 0.0

    with open("reports/sequential_report.md", "a") as f:
        f.write("\n## Parallel execution\n\n")
        f.write(f"Total time: {parallel_time:.2f} seconds\n\n")
        f.write("## Parallel download status\n\n")
        for result in parallel_results:
            f.write(f"- {result['url']}: {result['status']}")
            f.write("\n")
        f.write(f"\n- Successful downloads: {parallel_successful}\n")
        f.write(f"- Failed downloads: {parallel_failed}\n\n")
        f.write("## Comparison\n\n")
        f.write(f"Speed improvement: {speed_improvement:.2f}%\n")
    
    # Get metadata for all videos and save to a new CSV file

    metadata_rows = []

    for url in urls:        
        metadata = get_video_metadata(url)
        metadata_rows.append(metadata)


    # create the new CSV of metadata after the loop finishes
    with open("data/video_metadata.csv", "w", newline="") as file:
        fieldnames = ["title", "duration", "uploader", "view_count", "ext", "url"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(metadata_rows)
