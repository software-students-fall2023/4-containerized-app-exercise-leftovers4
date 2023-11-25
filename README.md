# Music Classification Containerized App

![Build Status](https://github.com/software-students-fall2023/4-containerized-app-exercise-leftovers4/actions/workflows/build.yaml/badge.svg)

## What Does The App Do?

Our containerized app helps to classify the genre of a short piece of music. The user can record the piece using their microphone and this recording will be saved into our database as a binary file. Every 30 seconds, the Machine Learning client will run and classify new entries in the system with one of the following genres: Rock, Pop, Country, EDM, Classical, HipHopAndRap, R&BAndSoul, Reggae, Disco, Jazz. The machine learning client is pre-trained on approximately 1500 recordings, using feature extraction and the K-Nearest Neighbor algorithm to classify a new entry. However, a new entry will not retrain the model, it merely classifies it. You can view the results of the classifications on the results page.

## How To Run?

Method 1: Cloning the Github

1. Using Git Bash, clone the directory using:

```
git clone https://github.com/software-students-fall2023/4-containerized-app-exercise-leftovers4.git
```

2. Open Docker Desktop

3. Open command prompt (accessible through windows search)

4. Go to the directory where you cloned the repository with:
```
cd "path_to_directory"
```

5. You should be in the root directory. Now, do:
```
docker-compose build
docker-compose up
```

6. Open your default internet explorer (if the app did not do so automatically), and go to: http://localhost:5000/

You should now see tha app running.

## Importing Starter Data?

There is no option to import starter data as the ML client is pre-trained (training takes too long with 1500 files). The user can only run and classify new files, and the ML client will not be retrained.

## Contributors

- [Capksz](https://github.com/Capksz)
- [IvanJing](https://github.com/IvanJing)
- [FrozenEclipse](https://github.com/FrozenEclipse)
- [jeffreysaeteros](https://github.com/jeffreysaeteros)


