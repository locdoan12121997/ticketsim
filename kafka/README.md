## Setup Kafka VM

![kafka](../images/kafka.jpg)

The ticketsim and kafka will run in two different docker process with architecture like above image. Ticketsim will publish events to port `9092` of kafka broker in the docker-composed containers of kafka.

- Access to your kafka VM terminal
- Clone git repo and cd to kafka folder

  ```bash
  git clone https://github.com/locdoan12121997/ticketsim.git
  ```

- Install docker & docker-compose

  ```bash
  bash ~/ticketsim/scripts/vm_setup.sh && exec newgrp docker
  ```

- Set the evironment variables. Kafka advertised listener need KAFKA_ADDRESS to return to kafka clients

  - External IP of the Kafka VM

    ```bash
    export KAFKA_ADDRESS=IP.ADD.RE.SS
    ```

     **Note**: You will have to setup these env vars every time you create a new shell session. Or if you stop/start your VM. The IP can be internal as it does not change when you start/ stop VM

- Start Kafka 

  ```bash
  cd ~/ticketsim/kafka && docker-compose build && docker-compose up 
  ```

  **Note**: Sometimes the `broker` & `schema-registry` containers die during startup. You should just stop all the containers with `docker-compose down` and then rerun `docker-compose up`.

- The Kafka Control Center should be available on port `9021`. Open and check if everything is working fine.

- Open another terminal session for the Kafka VM and start sending messages to your Kafka broker with Eventsim

  ```bash
  cd ~/ticketsim/ticketsim && docker build -t ticketsim:1.0 . && docker run --rm -d --network=host --name=ticketsim ticketsim:1.0
  ```

This will create around 1 million events of ticket buying and waiting to Kafka.

- You can check incoming messages in port `9092` of VM
