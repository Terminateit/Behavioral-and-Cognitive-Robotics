# Behavioral-and-Cognitive-Robotics

All the tasks you can find in the folders.

# Clone the repository

```bash
git clone https://github.com/Terminateit/Behavioral-and-Cognitive-Robotics.git
```

# Download the container

```bash
docker pull vkurenkov/cognitive-robotics
```

# Run container

```bash
docker run -it \
  -p 6080:6080 \
  -p 8888:8888 \
  --mount source=cognitive-robotics-opt-volume,target=/opt \
  vkurenkov/cognitive-robotics
  
```

# Play!