# Behavioral-and-Cognitive-Robotics

All the tasks you can find in the folders.

# Download the container

```bash
docker pull vkurenkov/cognitive-robotics
```

If you have troubles with permissions, use:
```bash
sudo usermod -a -G docker username
```
# Run container

```bash
docker run -it \
  -p 6080:6080 \
  -p 8888:8888 \
  --mount source=cognitive-robotics-opt-volume,target=/opt \
  vkurenkov/cognitive-robotics
  
```

# Clone the repository in it

```bash
git clone https://github.com/Terminateit/Behavioral-and-Cognitive-Robotics.git
```

To open Remote Desktop, write in your browser
```bash
localhost:6080 (or 8888)
```

# Play!

You can connect your container with VScode application. You will need to attach VScode window to launched container.

The working directory is /opt for a reason. If you restart the container, the files will only be saved within this folder.
