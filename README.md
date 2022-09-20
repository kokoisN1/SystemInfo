system info app

Overview:
This application will return a REST message when called with the URL 
http://< IP >< PORT >:/api/SystemInfo.
the REST message will describe the system information that is is ruuning on.

Time UTC On Server: <current time on server in UTC timezone - iso8601 format>
Local IP Address: <loop all interfaces and find first ip4 addr which is not 127.0.0.1>
External IP Address: <send request to https://ident.me, example: 81.2.3.4. set timeout 10s>
CPU Model: <example: Intel(R) Core(TM) i7-1065G7>
CPU Cores: <number of cores, ex: 4>
GPU Type: <ex. Mesa Intel(R) Iris(R) Plus Graphics. If no gpu, display “No GPU found”>
Memory Size: <ex: 8G>

exampleoutput (JSON format):
{"CPU Cores":12,"CPU Model":"Intel(R) Core(TM) i7-9850H CPU @ 2.60GHz","External IP":"199.203.251.96","External IP Address":"172.17.0.5","GPU Type":"No GPU found","Memory Size":12,"Time UTC On Server":"2022-09-20T08:23:13.114114"}

working enviroment mini guide:
please install:
Docker Desktop - https://www.docker.com/products/docker-desktop/ 
(install WSL2 as recommanded)
Minikube - https://minikube.sigs.k8s.io/docs/start/
terraform - https://www.terraform.io/downloads

Building the app / Docker image:
run "docker build . --tag systeminfo" in this folder.
(if you with to set the docker port default now run:
"docker build . --build-arg LISTEN_PORT=5000 --tag systeminfo") 

Pushing to dockerhub:
1. login to docker desktop with your dockerhub account.
2. push the docker to dockerhub:
	"docker tag systeminfo:latest icnaan/systeminfo:v1.0.0
	docker push icnaan/systeminfo:v1.0.0"

Testing locally (docker only)
docker run --rm -p 5000:5000 --env PORT=5000 icnaan/systeminfo:v1.0.0
use you browser to access http://localhost:5000/api/SystemInfo 
output should be similar to:
{"CPU Cores":12,"CPU Model":"Intel(R) Core(TM) i7-9850H CPU @ 2.60GHz","External IP":"199.203.251.96","External IP Address":"172.17.0.5","GPU Type":"No GPU found","Memory Size":12,"Time UTC On Server":"2022-09-20T08:23:13.114114"}

now stop the running container. 

Testing with K8s:
run the commands: 
1. minikube start 
2. kubectl create --save-config -f .\webapp.yaml
3. kubectl create --save-config -f .\service.yaml
4. minikube  service webapp-k8s-service
the last command will create a port forwarding and open a browser that looks like this:
http://127.0.0.1:64705/ ...
add /api/SystemInfo to the URL and expect to see the REST rsponse"
{"CPU Cores":12,"CPU Model":"Intel(R) Core(TM) i7-9850H CPU @ 2.60GHz","External IP":"199.203.251.96","External IP Address":"172.17.0.5","GPU Type":"No GPU found","Memory Size":12,"Time UTC On Server":"2022-09-20T08:23:13.114114"} 

Testing with Terraform:
eun the commands:
1. terraform plan
2. terraform apply 
3. minikube  service webapp-service
the last command will create a port forwarding and open a browser that looks like this:
http://127.0.0.1:64706/ ...
add /api/SystemInfo to the URL and expect to see the REST rsponse"
{"CPU Cores":12,"CPU Model":"Intel(R) Core(TM) i7-9850H CPU @ 2.60GHz","External IP":"199.203.251.96","External IP Address":"172.17.0.5","GPU Type":"No GPU found","Memory Size":12,"Time UTC On Server":"2022-09-20T08:23:13.114114"} 

Please cleanup the k8s manual and terraform running services.

Known issues:
the memory value returned is in GB , but does not have the "G" suffix.




