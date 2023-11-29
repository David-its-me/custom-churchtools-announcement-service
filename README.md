# Custom Churchtools Calendar Service

This service polls upcomming calendar entries and event data from a churchtools server and generates annoucement slides that visualize the upcomming events.

### Build a Container Image
The service is made as a Docker container. Before you build the container, please enter your churchtools credentials in the [/secret/churchtools_credentials.json](/secret/churchtools_credentials.json) file.
Now to build an run the Docker container, Docker must be installed on your operating system already.
If everithing is setup open a terminal go into the root directory of this reposiory and build the project with the following command:
```
docker build -t <tag> .
```
Please invent your own name for the container image in ```<tag>```.

### Run the Container Image
After build was successful you can run your container image with the follwing command:
```
docker run -p 80:80 <tag>
```
The ```-p``` option opens a port between the operating system and the container, to be able to access the container on port 80.

Now you can open http://127.0.0.1/ or http://localhost/ and see if everything is working!

### Custom Configuration
It is possible to add filter and manipulation rules for the calendar entries. 
All of them can be changed in the [/custom-configuration](/custom-configuration) folder.

TODO explain that a bit more.
