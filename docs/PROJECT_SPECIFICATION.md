# EdgeVision
## Benchmarking and Optimizing AI Inference on ARM-Based Edge Devices

**Version:** 2.1  
**Date:** 7 November 2026  
**Status:** Project specification and implementation plan

---

## 1. Project Overview

EdgeVision is an embedded AI project focused on deploying, evaluating and optimizing computer vision models on the Raspberry Pi 5.

The main application is road-scene perception using recorded video files transferred from a Windows PC to the Raspberry Pi.

The project focuses on practical Edge AI engineering and experimental evaluation, rather than simply demonstrating that an AI model can run on embedded hardware.

The central objective is to study the trade-offs between model accuracy, inference latency, computational resource usage and thermal behaviour.

## 2. Hardware and Development Environment

### Target device
- Raspberry Pi 5
- CPU: ARM Cortex-A76
- Architecture: ARM64 (aarch64)
- RAM: 4 GB
- Operating system: Debian GNU/Linux 13 (Trixie)

### Development computer
- Windows PC
- Visual Studio Code
- Git and GitHub

### Input method
Recorded video files will initially be transferred from the PC to the Raspberry Pi.

A physical camera is optional and is not required for the first release.

## 3. Main Objectives

1. Build a modular computer vision pipeline for recorded video.
2. Deploy an object detection model on the Raspberry Pi 5.
3. Evaluate inference performance on ARM64 hardware.
4. Compare model configurations and optimization techniques.
5. Measure accuracy, latency, FPS, RAM consumption and temperature.
6. Produce reproducible experiments and documented results.

## 4. Release 1: Core Project Scope

Release 1 is the primary deliverable. Its scope is deliberately limited.

### Phase 0: Environment and repository preparation
- Inspect the Raspberry Pi environment.
- Prepare an isolated Python environment.
- Organize the repository.
- Document software versions and dependencies.

### Phase 1: Video input and preprocessing
- Transfer recorded videos from PC to Raspberry Pi.
- Implement video file input using OpenCV.
- Read and decode video frames.
- Measure video decoding performance.
- Save basic benchmark results.

### Phase 2: Object detection
- Select a lightweight object detection model.
- Evaluate compatible inference runtimes.
- Run inference on recorded videos.
- Save detection results.
- Measure baseline accuracy and performance.

The runtime and model format will be selected after compatibility testing. No runtime is assumed to be optimal before measurement.

### Phase 3: Optimization and quantization
Compare suitable model configurations, including:

- Original precision model.
- Reduced precision or INT8 model, when supported.
- Different input resolutions.
- Different inference configurations.

Evaluate:
- Accuracy changes.
- Model size.
- Inference latency.
- FPS.
- RAM consumption.

Conversion correctness must be checked against the original model before reporting performance improvements.

### Phase 4: Additional perception modules
After object detection and optimization are working:

- Implement multi-object tracking.
- Add a lane detection baseline using OpenCV.
- Integrate the modules into a common pipeline.

These modules must remain modular and should not compromise the reliability of the core detection system.

### Phase 5: Benchmarking and documentation
Produce:
- Benchmark scripts.
- CSV or JSON measurement files.
- Performance comparison tables.
- Latency distributions, including P50 and P95.
- CPU, RAM and temperature measurements.
- Reproducible experiment instructions.
- Technical conclusions and limitations.

## 5. Main Research Questions

**RQ1: Model deployment**

How do different lightweight model configurations perform on Raspberry Pi 5?

**RQ2: Quantization**

What is the trade-off between model accuracy, size and inference latency when applying quantization?

**RQ3: Resolution**

How does input resolution affect inference performance and detection quality?

**RQ4: Frame scheduling**

How does performing detection every N frames affect computational cost and tracking continuity?

**RQ5: Resource consumption**

How do CPU utilization, memory consumption and temperature evolve during sustained inference?

**RQ6: Pipeline integration**

What is the computational cost of combining object detection, tracking and lane detection?

These are research questions, not predetermined results. Conclusions must be based on actual experiments.

## 6. Experimental Methodology

Each experiment must document:

- Experiment identifier.
- Hardware and operating system.
- Software and runtime versions.
- Model name and configuration.
- Dataset or video identifier.
- Input resolution.
- Precision and quantization settings.
- Number of tested frames.
- Warm-up procedure.
- Measurement procedure.

### Performance metrics

| Metric | Purpose |
|---|---|
| FPS | Processing throughput |
| P50 latency | Typical inference latency |
| P95 latency | High-percentile inference latency |
| CPU usage | Processor consumption |
| RAM usage | Memory consumption |
| Temperature | Thermal behaviour |
| Model size | Deployment footprint |
| Accuracy | Prediction quality |

Performance and accuracy must be evaluated separately.

Experiments should use consistent input videos and comparable configurations.

## 7. Release 2: Battery AI Extension

This is a future extension, not a requirement for Release 1.

The objective is to connect EdgeVision with the Master's thesis project on battery state estimation.

Potential work:

- Deploy the existing Transformer-based SoC model.
- Deploy the existing XGBoost-based SoH model.
- Evaluate model compatibility with Raspberry Pi 5.
- Compare original and optimized model versions.
- Measure prediction accuracy, latency and memory usage.

This extension will demonstrate embedded deployment of both computer vision and time-series AI models.

## 8. Future Extensions

The following subjects are not part of the initial release:

- Edge and Fog computing.
- IoT and sensor integration.
- TinyML on a suitable microcontroller.
- DataOps and MLOps.
- GIS and remote sensing.
- NLP and Generative AI.

They may be explored later if they support a clear technical objective.

A small model running on Raspberry Pi is Edge AI, not automatically TinyML.

## 9. Repository Organization

The repository will grow progressively.

```text
edgevision-adas/
├── README.md
├── .gitignore
├── requirements.txt
├── configs/
├── docs/
│   ├── PROJECT_SPECIFICATION.md
│   ├── PROGRESS.md
│   └── experiments/
├── data/
│   └── README.md
├── models/
│   └── README.md
├── src/
│   └── edgevision/
│       ├── video/
│       ├── detection/
│       ├── tracking/
│       ├── lanes/
│       └── benchmarking/
├── benchmarks/
├── tests/
└── scripts/
```

Large datasets, generated videos and model files should not be committed directly to Git unless there is a clear reason. Their sources, versions and download instructions should be documented.

## 10. Project Quality Requirements

- Use modular and maintainable code.
- Keep configuration separate from implementation.
- Use an isolated Python environment.
- Record dependency and runtime versions.
- Add tests for important components.
- Preserve experiment configurations.
- Keep benchmark results reproducible.
- Never invent or estimate experimental results.
- Clearly distinguish measured results from hypotheses.

## 11. Safety and Limitations

EdgeVision is an educational and research prototype.

It is not a certified ADAS or autonomous driving system.

Testing must use recorded videos, public datasets, simulation or stationary camera input.

The system must not control a real vehicle or be used to make real-world driving decisions.

## 12. Release 1 Completion Criteria

Release 1 is considered complete when:

- [ ] Raspberry Pi environment is documented.
- [ ] Recorded video can be processed locally.
- [ ] Video decoding benchmark is available.
- [ ] Object detection runs on Raspberry Pi 5.
- [ ] Baseline detection results are documented.
- [ ] At least one optimization experiment is completed.
- [ ] Accuracy and performance comparisons are available.
- [ ] Benchmark scripts and results are reproducible.
- [ ] Technical documentation is published.

Tracking and lane detection will be completed after the core detection and optimization experiments.

---

**Final principle:** Complete, measure and document a small working system before expanding its functionality.