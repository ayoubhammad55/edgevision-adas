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

### Phase 2: Object Detection

#### Model Setup

- [x] Detection source directory created: `src/detection/`.
- [x] Detection results directory created: `results/detection/`.
- [x] Model directory created: `models/`.
- [x] Ultralytics installed in the Windows virtual environment.
- [x] Pretrained YOLO11n weights downloaded.
- [x] Model loading and configuration verified.
- [x] Video object detection script implemented.
- [x] Initial detection performed on recorded video.
- [x] Annotated output video generated.
- [x] Detection benchmark CSV export implemented.

#### Model Configuration

- Model: YOLO11n
- Task: Object detection
- Architecture: DetectionModel
- Layers: 181
- Parameters: 2,624,080
- Parameter precision: FP32
- Weight file size: 5.35 MB
- Number of classes: 80 (COCO)
- Input image size: 640 × 640
- Computational complexity: 6.7 GFLOPs

The model is pretrained. No additional training or fine-tuning was performed as part of this project. Current experiments focus on inference performance and deployment optimization.

#### Detection Test Configuration

- Platform: Windows
- Execution device: CPU
- Video: `Manhattan.mp4`
- Video resolution: 1280 × 720
- Source frame rate: 30 FPS
- Maximum processed frames per run: 100
- Model: YOLO11n
- Input image size: 640 × 640
- Confidence threshold: 0.25
- Number of benchmark runs: 5

#### Five-Run Windows FP32 Results

| Metric | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 |
|---|---:|---:|---:|---:|---:|
| Inference FPS | 3.24 | 6.48 | 8.18 | 7.99 | 6.24 |
| Pipeline FPS | 2.80 | 5.35 | 6.56 | 6.46 | 5.16 |
| Average latency (ms) | 308.40 | 154.44 | 122.32 | 125.12 | 160.29 |
| Median latency (ms) | 271.22 | 131.95 | 116.25 | 116.19 | 149.55 |
| P95 latency (ms) | 574.17 | 312.85 | 162.47 | 169.49 | 251.47 |
| RAM at end (MB) | 388.61 | 391.36 | 391.58 | 391.57 | 392.63 |

#### Five-Run Median Baseline

| Metric | Median Result |
|---|---:|
| Inference FPS | **6.48** |
| Pipeline FPS | **5.35** |
| Average inference latency | **154.44 ms** |
| Median inference latency | **131.95 ms** |
| P95 inference latency | **251.47 ms** |
| Process RAM at end | **391.57 MB** |

The median values were independently calculated from the benchmark CSV.

**Measurement definitions:**

- Inference FPS: processed frames divided by cumulative `model.predict()` execution time.
- Pipeline FPS: processed frames divided by total processing-loop time.
- Inference latency: time spent in the Ultralytics prediction call, including its preprocessing and postprocessing.
- RAM at end: process resident memory measured after processing. It is not peak RAM usage.

The five runs show noticeable performance variation, particularly in the first run. The five-run median is used as the preliminary reference rather than selecting the fastest result.

#### Detection Files

- Detection script: `src/detection/detect_video.py`
- Model weights: `models/yolo11n.pt` (excluded from Git)
- Annotated output: `results/detection/manhattan_yolo11n.mp4` (excluded from Git)
- Benchmark results: `results/detection/detection_benchmark.csv`

**Status:** Windows FP32 detection baseline established. Raspberry Pi deployment and validation are pending.

---

## Important Methodology Rules

- Do not invent benchmark results.
- Record actual measurements.
- Keep experiments reproducible.
- Distinguish video decoding FPS from AI inference FPS.
- Distinguish model inference latency from complete pipeline throughput.
- Record hardware and software configurations.
- Use recorded videos initially.
- Camera input is optional.
- Keep original FP32 model results as the reference for optimization comparisons.
- Compare optimized models under the same test conditions.
- Do not use the prototype for vehicle control or real-world driving decisions.

## Next Tasks

1. Validate and commit the five-run Windows YOLO11n FP32 baseline.
2. Export YOLO11n to ONNX.
3. Benchmark ONNX inference on Windows CPU.
4. Compare ONNX performance against the FP32 PyTorch baseline.
5. Investigate INT8 quantization and its effect on model size, speed and detection accuracy.
6. Resume Raspberry Pi testing with a suitable power supply.
7. Obtain reliable Raspberry Pi video decoding and AI inference baselines.
8. Deploy and benchmark the optimized models on ARM64.

## Last Updated

2026-11-07