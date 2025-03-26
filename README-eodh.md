For testing locally, try:

* You might need `sudo /usr/sbin/sysctl -w vm.max_map_count=262144` if vm.max_map_count is less than 64k.
* `make image-deploy-es` to build an image using `dockerfiles/Dockerfile.dev.es`
* `docker-compose up app-elasticsearch` to start ES and stac-fastapi
* `curl http://localhost:8080/` to see the root Catalog. Add api.html to use the transaction API to add more records.

