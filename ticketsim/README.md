Chang to this directory: 
docker build -t ticketsim:1.0 .


Run docker image:
- Using same network as host
- Detached mode
- Remove container when exits
docker run --rm -d --network=host --name=ticketsim ticketsim:1.0