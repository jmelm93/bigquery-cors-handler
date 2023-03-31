# docker image build local compuet
docker build -t fastapi_hypercorn .

# launch in background
docker run -d --network='host' fastapi_hypercorn

# docker list ALL running containers
docker ps -a