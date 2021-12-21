## Setup
> JDK version 11  
> Scala version 2.6.13

## Run locally
### Set environment variables
`source .env
`
### Run all simulations
`./gradlew gatlingRun --rerun-tasks`

### Run a simulation
`./gradlew gatlingRun-passemploi.test.ConnectionSimulation --rerun-tasks`

## Run with docker
### Build
`docker build -t gatling .`

### Run all simulations
`docker run gatling`

### Run a simulation
`docker run gating passemploi.test.ConnectionSimulation`
