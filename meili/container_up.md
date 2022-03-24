# Fetch the latest version of Meilisearch image from DockerHub
    
    docker pull getmeili/meilisearch:latest

# Launch Meilisearch

docker run -it --rm \
    -p 7700:7700 \
    -v $(pwd)/data.ms:/data.ms \
    getmeili/meilisearch:latest
 