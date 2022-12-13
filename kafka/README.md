## Setup Kafka VM

![kafka](../images/kafka.jpg)

The ticketsim and kafka will run in two different docker process with architecture like above image. Ticketsim will publish events to port `9092` of kafka broker in the docker-composed containers of kafka.

- Access to your kafka VM terminal
- Clone git repo and cd to kafka folder

  ```bash
  git clone https://github.com/locdoan12121997/ticketsim.git && cd ticketsim/kafka
  ```


Kafka advertised listener need KAFKA_ADDRESS to return to kafka clients
export KAFKA_ADDRESS=10.148.0.2
export GCP_GCS_BUCKET=ticketsim
docker-compose up
docker-compose down