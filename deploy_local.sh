# docker image build local compuet
docker build -t fastapi_hypercorn .

# launch in background
# -d = detached
# -p = port
# docker run on local host
docker run -d --network='host' fastapi_hypercorn

# docker list ALL running containers
docker ps -a

# docker kill all running containers
# docker kill $(docker ps -a -q)

# kill process on port 8000
# lsof -i :8000

#lsof means list open files
# -i means list files by network

# kill pid 14761
# kill 14761