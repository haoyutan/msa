# 1. Prepare
	$ cd docker/dist-example
	$ cp docker/msa-data-base/data-helper.sh ./

We also need to copy the required package installation files
(`.whl` or `.tar.gz`) to `msa-master-server-0.0.1/packages`.

# 2. Build images
	$ sudo docker build -t msa/data-base msa-data-base
	$ sudo docker build -t msa/api-base msa-api-base

# 3. Create a data container
We can set the name of the data container by modifying `DATA_CONTAINER_NAME`
in `data-helper.sh`. The default name is `msa-data-example`.

	$ ./data-helper.sh start

# 4. Upload dist
	$ ./data-helper.sh upload msa-master-server-0.0.1
	$ ./data-helper.sh exec mv /data/.msa-tmp/msa-master-server-0.0.1 /data/dist

# 5. Setup application
	$ sudo docker run -it --name msa-api-example-tmp --volumes-from msa-data-example msa/api-base setup
	$ sudo docker rm msa-api-example-tmp

# 6. Start application
	$ sudo docker run -d --name msa-api-example --volumes-from msa-data-example -p 8001:8443 msa/api-base start

# 7. Stop application
	$ sudo docker stop msa-data-example
	$ sudo docker rm msa-data-example
