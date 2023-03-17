This guide will walk you through the simple steps needed to build and train a natural language processor on Rising Cloud.

1. Install the Rising Cloud Command Line Interface (CLI)
In order to run the Rising Cloud commands in this guide, you will need to install the Rising Cloud Command Line Interface. This program provides you with the utilities to setup your Rising Cloud Task or Web Service, upload your application to Rising Cloud, setup authentication, and more.

2. Login to Rising Cloud Using the CLI
Using a command line console (called terminal on Mac OS X and command prompt on Windows) run the Rising Cloud login command. The interface will request your Rising Cloud email address and password.

risingcloud login
3. Initialize Your Rising Cloud Task
Create a new directory on your workstation to place your project files in, then open this directory with your command line.

Using the command line in your project directory, run the following command replacing $GPU_TYPE with your preference of GPU server and $TASK_URL with your unique task name. Your unique task name must be at least 12 characters long and consist of only alphanumeric characters and hyphens (-). This task name is unique to all tasks on Rising Cloud. A unique URL will be provided to you for sending jobs to your task. If a task name is not available, the CLI will return with an error so you can try again.

risingcloud init -s --gpu $GPU_TYPE $TASK_URL
Use the following command to get a list of currently available GPU’s

risingcloud lsrr
This creates a risingcloud.yaml file in your project directory. This file will be used to configure your build script.

4. Create your Rising Cloud Task
Configuring your I/O

When a Rising Cloud Job is run, input is written to request.json in the top level of your project directory. Your application will need to read this to respond to it. When your application terminates, output is read from response.json, if it exists, and is stored in Rising Cloud’s Job Results database for retrieval.

Input to Rising Cloud Tasks has to come a JSON. If you are planning on using pdfs, images, or other non-JSONable data as input to your neural net, you will have to use the input JSON to give your application URLs to download the data from. Likewise, if the output of your application is an image, you will need your application to store the application in a database and return information on how to retrieve it in the output (such as a URL to an Amazon S3 object.) See our Statelessness guide to understand why this is, and for information about connecting to external data sources.

Create Your NLP Program

Create a new file called "main.py”

import json
import requests

with open("request.json", "r") as f:
    req = json.load(f)

# Send request to flask server
tf_server = "http://localhost:5000"
res = requests.post(tf_server + "/predict", json=req)

# Write to response
with open("response.json", "w") as f:
    json.dump({
        "request": {**req},
        "response": res.json()
    }, f)
Create Your Requirements File

Create a file named “requirements.txt”, and in it, write the following contents:

Flask==2.2.3
tensorflow==2.11.0
transformers==4.27.1
Configure your risingcloud.yaml

When you ran risingcloud init, a new risingcloud.yaml file should have generated in your project directory. Open that file now in your editor.  Change the from Base Image and Deps to the following:

from: tensorflow:latest-gpu
deps:
  - pip3 install -r requirements.txt
We need to setup a daemon:

daemons:
  - python3 -m flask --app serve run
We need to tell Rising Cloud what to run when a new request comes in. Change the run command to:

run: python3 main.py
5. Build and Deploy your Rising Cloud Task
Use the push command to push your updated risingcloud.yaml to your Task on Rising Cloud.

risingcloud push
Use the build command to zip, upload, and build your app on Rising Cloud.

risingcloud build
Use the deploy command to deploy your app as soon as the build is complete. Change $TASK to your unique task name.

risingcloud deploy $TASK
Alternatively, you could also use a combination to push, build and deploy all at once.

risingcloud build -r -d
Rising Cloud will now build out the infrastructure necessary to run and scale your application including networking, load balancing and DNS. Allow DNS a few minutes to propogate and then your app will be ready and available to use!

7. Queue a Job
Rising Cloud will take some time to build and deploy your Rising Cloud Task. Once it is done, you can make HTTPS POST requests with JSON bodies to https://{your project URL}.risingcloud.app/risingcloud/jobs to queue jobs for Rising Cloud Task. These requests will return JSON responses with a “jobId” field containing the ID of your job. Make an HTTP GET request to https://{your project URL}.risingcloud.app/risingcloud/jobs/{job ID} in order to check on the status of the job. If the response’s “status” field is “Completed”, the result of the job will appear under the “result” field in the JSON object.

Making a request with a JSON body of:

{
  "prompt": "You overhear Dave having a conversation in a coffee shop",
  "max_length": 200,
  "num_return_sequences": 1
}
should cause the “result” field in a completed Job Status to be:

Hello, World!

Congratulations, built a Natural Language Processor on Rising Cloud!
