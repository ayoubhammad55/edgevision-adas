
import cv2
import time
import argparse
import platform
import statistics
import csv
import psutil

from pathlib import Path
from datetime import datetime


def benchmark_video(video_path, run_number, total_runs):

    video_path = Path(video_path)

    if not video_path.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")

    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        raise RuntimeError("Could not open video.")

    source_fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    frame_times = []
    decoded_frames = 0

    process = psutil.Process()
    process.cpu_percent(interval=None)

    cpu_samples = []
    peak_ram_mb = 0

    sample_interval = 0.5
    last_sample = time.perf_counter()

    print(f"\nStarting run {run_number}/{total_runs}")
    start_time = time.perf_counter()

    while True:

        frame_start = time.perf_counter()
        success, frame = cap.read()
        frame_end = time.perf_counter()

        if not success:
            break

        frame_times.append((frame_end - frame_start) * 1000)
        decoded_frames += 1

        now = time.perf_counter()

        if now - last_sample >= sample_interval:

            cpu_samples.append(process.cpu_percent(interval=None))

            ram_mb = process.memory_info().rss / (1024 ** 2)
            peak_ram_mb = max(peak_ram_mb, ram_mb)

            last_sample = now

        if decoded_frames % 100 == 0:

            elapsed = now - start_time
            current_fps = decoded_frames / elapsed

            progress = (
                decoded_frames / total_frames * 100
                if total_frames > 0 else 0
            )

            print(
                f"\rProgress: {decoded_frames}/{total_frames} "
                f"({progress:.1f}%) | "
                f"Elapsed: {elapsed:.1f}s | "
                f"FPS: {current_fps:.1f}",
                end="",
                flush=True
            )

    end_time = time.perf_counter()
    cap.release()

    total_time = end_time - start_time

    avg_fps = decoded_frames / total_time if total_time > 0 else 0

    avg_latency = statistics.mean(frame_times) if frame_times else 0
    median_latency = statistics.median(frame_times) if frame_times else 0

    p95_latency = (
        statistics.quantiles(frame_times, n=100)[94]
        if len(frame_times) >= 100 else 0
    )

    final_ram_mb = process.memory_info().rss / (1024 ** 2)
    peak_ram_mb = max(peak_ram_mb, final_ram_mb)

    average_cpu = (
        statistics.mean(cpu_samples)
        if cpu_samples else 0
    )

    missing_frames = max(0, total_frames - decoded_frames)

    frame_match = decoded_frames == total_frames

    print(
        f"\rCompleted: {decoded_frames}/{total_frames} frames "
        f"| {total_time:.2f}s"
    )

    results = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "run": run_number,
        "video": video_path.name,
        "resolution": f"{width}x{height}",
        "source_fps": round(source_fps, 2),
        "metadata_frame_count": total_frames,
        "decoded_frames": decoded_frames,
        "metadata_count_difference": max(0, total_frames - decoded_frames),
        "metadata_count_matches": decoded_frames == total_frames,
        "total_time_s": round(total_time, 3),
        "average_fps": round(avg_fps, 2),
        "average_latency_ms": round(avg_latency, 3),
        "median_latency_ms": round(median_latency, 3),
        "p95_latency_ms": round(p95_latency, 3),
        "average_cpu_percent": round(average_cpu, 2),
        "peak_ram_mb": round(peak_ram_mb, 2),
        "architecture": platform.machine(),
        "opencv_version": cv2.__version__
    }

    return results


def save_results(results, output_file):

    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    file_exists = output_file.exists()

    with output_file.open("a", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=results[0].keys()
        )

        if not file_exists:
            writer.writeheader()

        writer.writerows(results)


def main():

    parser = argparse.ArgumentParser(
        description="EdgeVision video decoding benchmark"
    )

    parser.add_argument(
        "--video",
        required=True,
        help="Path to input video"
    )

    parser.add_argument(
        "--runs",
        type=int,
        default=3,
        help="Number of benchmark runs"
    )

    parser.add_argument(
        "--output",
        default="results/benchmarks/decode_results.csv",
        help="CSV output path"
    )

    args = parser.parse_args()

    if args.runs < 1:
        parser.error("--runs must be at least 1")

    all_results = []

    for run in range(1, args.runs + 1):

        result = benchmark_video(
            args.video,
            run,
            args.runs
        )

        all_results.append(result)

    save_results(all_results, args.output)

    print("\n========== EDGEVISION BENCHMARK ==========")

    for result in all_results:

        print(f"\nRun: {result['run']}")
        print(f"Decoded frames: {result['decoded_frames']}")
        print(f"Metadata frame count: {result['metadata_frame_count']}")
        print(f"Metadata count difference: {result['metadata_count_difference']}")
        print(f"Metadata count matches: {result['metadata_count_matches']}")
        print(f"Average FPS: {result['average_fps']}")
        print(f"Average latency: {result['average_latency_ms']} ms")
        print(f"Median latency: {result['median_latency_ms']} ms")
        print(f"P95 latency: {result['p95_latency_ms']} ms")
        print(f"Average CPU: {result['average_cpu_percent']}%")
        print(f"Peak RAM: {result['peak_ram_mb']} MB")

    print("\nCSV saved to:", args.output)
    print("==========================================\n")


if __name__ == "__main__":
    main()
