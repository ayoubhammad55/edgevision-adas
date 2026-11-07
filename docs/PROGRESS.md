# EdgeVision - Project Progress

## Project

**EdgeVision: Benchmarking and Optimizing AI Inference on ARM-Based Edge Devices**

Repository: https://github.com/ayoubhammad55/edgevision-adas

## Target Hardware

- Device: Raspberry Pi 5
- CPU: Cortex-A76, 4 cores
- Architecture: ARM64 (aarch64)
- RAM: 4 GB
- OS: Debian 13 (Trixie)
- Python: 3.13.5

## Development Environment

- Development PC: Windows
- Editor: VS Code
- Windows Python: 3.11.0
- Windows virtual environment: `.venv`
- Raspberry Pi project directory: `~/edgevision`
- Video input: Recorded video files

---

## Current Progress

### Phase 0: Environment and Project Setup

- [x] Raspberry Pi operating system inspected.
- [x] CPU architecture and processor inspected.
- [x] RAM and storage inspected.
- [x] Python version checked.
- [x] GitHub repository created and configured.
- [x] Project specification documented.
- [x] Development environments prepared on Windows and Raspberry Pi.

### Phase 1: Video Input and Decoding

- [x] Video input directory created.
- [x] Recorded test video transferred to Raspberry Pi.
- [x] Video metadata inspected using FFprobe.
- [x] OpenCV video decoding benchmark implemented.
- [x] Progress reporting added to the benchmark.
- [x] CPU and memory monitoring added.
- [x] CSV benchmark export implemented.
- [x] Initial benchmark executed on Windows.

#### Test Video

- File: `Manhattan.mp4`
- Codec: H.264
- Resolution: 1280 × 720
- Source frame rate: 30 FPS
- Duration: 89.59 seconds
- Frames decoded: 2685
- OpenCV metadata frame count: 2688
- FFprobe decoded frame count: 2685

The difference between the OpenCV metadata count and the decoded frame count is recorded as a metadata discrepancy, not as confirmed missing frames.

#### Windows Baseline

Three benchmark runs were performed.

| Metric | Run 1 | Run 2 | Run 3 |
|---|---:|---:|---:|
| Average FPS | 139.06 | 181.49 | 135.45 |
| Average latency (ms) | 6.381 | 5.484 | 7.364 |
| Median latency (ms) | 5.808 | 4.935 | 6.171 |
| P95 latency (ms) | 10.445 | 8.509 | 13.573 |
| Average CPU (%) | 195.86 | 227.61 | 186.72 |
| Peak sampled RAM (MB) | 92.75 | 94.40 | 95.77 |

Median of the three average-FPS results: **139.06 FPS**.

The Windows results show variability between runs. They are an initial development baseline, not a stable hardware comparison or a substitute for Raspberry Pi measurements.

#### Benchmark Files

- Script: `src/video/decode_benchmark.py`
- Official Windows baseline: `results/benchmarks/windows_baseline.csv`

### Raspberry Pi Benchmark Status

- [x] Video file transferred to Raspberry Pi.
- [x] Video metadata inspected on Raspberry Pi.
- [ ] Complete a reliable Raspberry Pi decoding benchmark.
- [ ] Compare Raspberry Pi results with the Windows baseline.

**Status:** Raspberry Pi benchmark execution and validation are pending.

---

## Important Methodology Rules

- Do not invent benchmark results.
- Record actual measurements.
- Keep experiments reproducible.
- Distinguish video decoding FPS from AI inference FPS.
- Record hardware and software configurations.
- Use recorded videos initially.
- Camera input is optional.
- Do not use the prototype for vehicle control or real-world driving decisions.

## Next Tasks

1. Commit the video decoding benchmark and official Windows baseline.
2. Resume Raspberry Pi testing with a suitable power supply.
3. Obtain a reliable Raspberry Pi decoding baseline.
4. Implement object detection on recorded videos.
5. Measure AI inference performance on ARM64.

## Last Updated

2026-11-07
