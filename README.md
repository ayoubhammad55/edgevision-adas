# EdgeVision ADAS

A modular Edge-AI computer vision perception pipeline designed to run on a Raspberry Pi 5 using CPU-only inference.

## Project Status

🚧 **Phase 1 - Project Foundation**

The project is currently being developed.

### Planned Pipeline

```text
Recorded Driving Video
          ↓
   Video Preprocessing
          ↓
 ┌────────┼─────────┐
 ↓        ↓         ↓
Object   Lane     Traffic
Detection Detection Signs
 ↓        ↓         ↓
 └────────┼─────────┘
          ↓
       Tracking
          ↓
  Scene Understanding
          ↓
 Advisory Indicators
          ↓
   Performance Monitor