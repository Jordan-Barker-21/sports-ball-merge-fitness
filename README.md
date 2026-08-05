# 🏀 Sports Ball Merge Fitness Game

A fitness game that uses computer vision and pose detection to control sports ball merging mechanics through exercise!

## 🎮 Game Overview

Combine fitness with gaming! Use side lunges to move balls and squats to drop them. Merge same-value sports balls to unlock new ones!

### 🏆 Sports Ball Collection (12 to collect!)
| Value | Sport | Emoji |
|-------|-------|-------|
| 1 | Tennis Ball | 🎾 |
| 2 | Baseball | ⚾ |
| 4 | Golf Ball | 🏌️ |
| 8 | Soccer Ball | ⚽ |
| 16 | Basketball | 🏀 |
| 32 | Volleyball | 🏐 |
| 64 | American Football | 🏈 |
| 128 | Bowling Ball | 🎳 |
| 256 | Rugby Ball | 🏉 |
| 512 | Cricket Ball | 🏏 |
| 1024 | Beach Ball | 🏖️ |
| 2048 | Planet Earth | 🌍 |

## ✨ Features

- **Real-time Pose Detection** using MediaPipe
- **Two Game Modes:** Endless & Timed (60-second)
- **12 Unique Sports Balls** with procedural rendering
- **Squat Detection** requiring BOTH legs at 80° flexion
- **Side Lunge Control** for horizontal movement
- **Live Camera Feed** with pose overlay

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Webcam
- Good lighting for pose detection

### Setup

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/sports-ball-merge-fitness.git
cd sports-ball-merge-fitness
