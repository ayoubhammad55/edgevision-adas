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

#### Measurement Definitions

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
- PyTorch baseline: `results/detection/pytorch_baseline.csv`

**Status:** Windows FP32 detection baseline established. Raspberry Pi deployment and validation are pending.

---

### Phase 3: ONNX Export and Model Quantization

#### 3.1 ONNX Export

- [x] ONNX Runtime installed.
- [x] YOLO11n exported from PyTorch to ONNX.
- [x] ONNX model loading verified.
- [x] Input and output tensor shapes inspected.
- [x] ONNX object detection tested on recorded video.
- [x] Five-run ONNX benchmark completed.

#### ONNX Model Configuration

- Original model: YOLO11n FP32
- Export format: ONNX
- ONNX opset: 18
- Input name: `images`
- Input shape: `1 × 3 × 640 × 640`
- Output name: `output0`
- Output shape: `1 × 84 × 8400`
- Execution provider: ONNX Runtime CPUExecutionProvider
- ONNX model size: approximately 10.2 MB

#### Five-Run ONNX FP32 Results

| Metric | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 |
|---|---:|---:|---:|---:|---:|
| Inference FPS | 6.36 | 4.91 | 5.08 | 6.55 | 6.51 |
| Pipeline FPS | 5.29 | 4.12 | 4.28 | 5.43 | 5.40 |
| Average latency (ms) | 157.15 | 203.53 | 196.96 | 152.57 | 153.69 |
| Median latency (ms) | 147.00 | 182.40 | 167.09 | 146.09 | 138.19 |
| P95 latency (ms) | 230.60 | 341.11 | 341.61 | 226.58 | 243.07 |
| RAM at end (MB) | 447.61 | 448.07 | 445.21 | 452.83 | 446.05 |

#### Five-Run ONNX Median Baseline

| Metric | Median Result |
|---|---:|
| Inference FPS | **6.36** |
| Pipeline FPS | **5.29** |
| Average inference latency | **157.15 ms** |
| Median inference latency | **147.00 ms** |
| P95 inference latency | **243.07 ms** |
| Process RAM at end | **447.61 MB** |

#### PyTorch vs ONNX

The preliminary comparison shows that ONNX did not provide a meaningful overall CPU performance improvement over PyTorch in these Windows experiments.

The two formats have similar inference and pipeline throughput, while the ONNX model uses more memory and has a larger file size.

#### ONNX Files

- Exported model: `models/yolo11n.onnx` (excluded from Git)
- PyTorch baseline: `results/detection/pytorch_baseline.csv`
- ONNX baseline: `results/detection/onnx_baseline.csv`

---

#### 3.2 INT8 Static Quantization

Static INT8 quantization was investigated to reduce model size and evaluate its effect on inference performance.

The experiments used ONNX Runtime quantization tools and calibration frames extracted from the recorded video.

##### Experiment 1: Initial INT8 Quantization

- Quantization method: Static quantization
- Quantization format: QDQ
- Activation type: QUInt8
- Weight type: QInt8
- Calibration frames: 100
- Quantized model size: approximately 3.04 MB
- Model size reduction: approximately 70.2%

**Problem observed:**

The initial INT8 model produced zero nonzero class confidence scores in the raw output comparison.

Consequently, the model did not produce usable object detections.

**Status:** Initial quantization experiment unsuccessful for object detection.

##### Experiment 2: Improved INT8 Quantization

A second experiment was performed to preserve detection-head outputs.

Changes included:

- Letterbox preprocessing during calibration.
- Calibration using 100 video frames.
- Exclusion of six detection-head convolution operators from quantization.
- Static QDQ quantization using ONNX Runtime.
- A separate output model to preserve the first experiment.

Quantized model:

`models/yolo11n_int8_v2.onnx`

Model size: approximately 3.13 MB.

Model size reduction compared with FP32 ONNX: approximately 69.3%.

##### Raw Output Validation

The raw outputs of the FP32 ONNX model and both INT8 models were compared using the same letterbox preprocessing.

| Metric | FP32 ONNX | INT8 v1 | INT8 v2 |
|---|---:|---:|---:|
| Maximum class score | 0.8982 | 0.0000 | 0.8994 |
| Nonzero class scores | 621,403 | 0 | 576,698 |
| Output shape | 1 × 84 × 8400 | 1 × 84 × 8400 | 1 × 84 × 8400 |

The second INT8 model preserved nonzero class confidence scores, unlike the first attempt.

##### Functional Detection Test

The second INT8 model was tested on 100 frames of `Manhattan.mp4`.

Results:

- Processed frames: 100
- Detections reported at progress checkpoints: 6, 8, 7 and 7
- Inference FPS: 5.21
- Pipeline FPS: 4.49
- Average latency: 192.05 ms
- Median latency: 187.64 ms
- P95 latency: 269.64 ms
- RAM at end: 451.42 MB

An annotated video was generated and visually inspected. Bounding boxes and labels appeared correctly.

**Status:** INT8 v2 functional detection test passed.

---

#### 3.3 Five-Run INT8 v2 Benchmark

After the functional test, five benchmark runs were performed using the same video and detection configuration.

Configuration:

- Model: `yolo11n_int8_v2.onnx`
- Platform: Windows
- Execution device: CPU
- Execution provider: ONNX Runtime CPUExecutionProvider
- Video: `Manhattan.mp4`
- Input image size: 640 × 640
- Confidence threshold: 0.25
- Maximum frames per run: 100
- Number of runs: 5

##### Five-Run Results

| Metric | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 |
|---|---:|---:|---:|---:|---:|
| Inference FPS | 4.66 | 4.05 | 4.27 | 4.28 | 4.27 |
| Pipeline FPS | 4.04 | 3.55 | 3.73 | 3.74 | 3.71 |
| Average latency (ms) | 214.80 | 247.11 | 234.37 | 233.55 | 233.98 |
| Median latency (ms) | 208.58 | 230.47 | 225.45 | 221.94 | 226.05 |
| P95 latency (ms) | 301.92 | 334.62 | 306.77 | 300.73 | 285.27 |
| RAM at end (MB) | 451.00 | 451.07 | 452.61 | 450.96 | 452.21 |

##### Five-Run Median Results

| Metric | Median Result |
|---|---:|
| Inference FPS | **4.27** |
| Pipeline FPS | **3.73** |
| Average inference latency | **234.37 ms** |
| Median inference latency | **225.45 ms** |
| P95 inference latency | **301.92 ms** |
| Process RAM at end | **451.07 MB** |

##### INT8 v2 Benchmark Files

- Quantization script: `src/detection/quantize_onnx.py`
- Output comparison script: `src/detection/compare_outputs.py`
- Quantized model: `models/yolo11n_int8_v2.onnx` (excluded from Git)
- INT8 benchmark CSV: `results/detection/int8_v2_baseline.csv`
- Annotated test video: `results/detection/manhattan_int8_v2_test.mp4` (excluded from Git)

---

#### 3.4 Overall Model Comparison

The following table compares the five-run median results for the three model formats.

| Metric | PyTorch FP32 | ONNX FP32 | ONNX INT8 v2 |
|---|---:|---:|---:|
| Inference FPS | 6.48 | 6.36 | 4.27 |
| Pipeline FPS | 5.35 | 5.29 | 3.73 |
| Average latency (ms) | 154.44 | 157.15 | 234.37 |
| Median latency (ms) | 131.95 | 147.00 | 225.45 |
| P95 latency (ms) | 251.47 | 243.07 | 301.92 |
| RAM at end (MB) | 391.57 | 447.61 | 451.07 |
| Model size (MB) | 5.35 | 10.2 | 3.13 |

##### Preliminary Observations

1. ONNX FP32 achieved similar inference throughput to PyTorch FP32 in the Windows CPU experiments.
2. ONNX FP32 had a larger model file and higher process memory usage than the PyTorch model.
3. INT8 v2 reduced ONNX model size by approximately 69.3%.
4. INT8 v2 successfully preserved object detection functionality.
5. INT8 v2 was slower than FP32 ONNX in the five-run Windows comparison.
6. The measured RAM at the end of processing was similar for ONNX FP32 and INT8 v2.

**Main finding:** INT8 quantization significantly reduced model size but did not improve CPU inference speed in the current Windows experiments.

These results are preliminary and specific to the tested Windows environment. The effect of quantization may differ on ARM64 hardware, particularly the Raspberry Pi 5.

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
- Clearly distinguish functional validation from benchmark performance.
- Do not interpret raw output similarity as proof of detection accuracy.
- Do not use the prototype for vehicle control or real-world driving decisions.

## Next Tasks

1. Review and commit the completed Phase 3 documentation and benchmark CSV files.
2. Investigate additional inference optimizations, such as input resolution and execution settings.
3. Evaluate detection quality using a more systematic comparison against FP32 outputs.
4. Resume Raspberry Pi testing with a suitable power supply.
5. Run the video decoding benchmark on Raspberry Pi 5.
6. Deploy the FP32 PyTorch, FP32 ONNX and INT8 ONNX models on Raspberry Pi 5 where compatible.
7. Measure inference FPS, pipeline FPS, latency, CPU usage, RAM and temperature on ARM64.
8. Compare model performance and quantization effects between Windows and Raspberry Pi 5.
9. Investigate further optimization methods based on the measured results.

## Current Status

- Phase 0: Environment and project setup completed.
- Phase 1: Windows video decoding baseline completed.
- Phase 2: Windows YOLO11n FP32 detection baseline completed.
- Phase 3: ONNX export and INT8 quantization experiments completed on Windows.
- Raspberry Pi 5 video decoding and AI inference validation pending.

**Last Updated:** 2026-11-07