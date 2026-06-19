# VR-Based Automated Eye Screening System

Undergraduate Engineering Thesis

An automated eye examination system built into a VR headset enclosure. Combines a Snellen visual acuity test with AI-based glaucoma screening using a fundus camera.

## System Components

| Component | Location | Description |
|---|---|---|
| Snellen Test App | `software/snellen-app/` | Visual acuity test with voice input |
| Glaucoma Detection | `software/glaucoma-model/` | ML model trained on G1020 fundus dataset |
| ESP32 Firmware | `software/firmware/` | Camera capture and USB transmission |
| Web App | `web/` | Patient records and results dashboard |

## Hardware

- Custom 3D-printed VR headset enclosure
- 7-inch HDMI display (Snellen chart)
- Biconvex lens (simulates 6m viewing distance)
- 20D condensing lens (fundus imaging optics)
- SEEED XIAO ESP32-S3 with OV5640 camera
- IR LED ring (retinal illumination)
- USB microphone

## Getting Started

See the README inside each component folder for setup instructions.

## Thesis Document

Chapter drafts are in `docs/chapters/`.
