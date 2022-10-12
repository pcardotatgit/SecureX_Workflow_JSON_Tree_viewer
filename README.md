# SecureX JSON workflows parser

This tools is a JSON parser that is dedicated to SecureX Workflow JSON files.

It gives a Visual Tree representation view of SecureX workflows that help you to easily understand their structure and how they work.

All workflow content are represented, with python scripts as well. 

The tool aims to help you to easily clean, optimize, secure the workflows you might create. In a more easier way than the Workflow editor allows.

## Dependancies

You need to install the 2 following python modules :

- crayons
- ijson

## Installation

Clone the whole content of this repository into your Python Workstation.

    git clone https://github.com/pcardotatgit/SecureX_Workflow_JSON_Tree_viewer.git

Install crayons and ijson 

    pip install crayons
    pip install ijson

And that's it

## Run the application


- Step 1 you must copy and paste the SecureX JSON workflow export into the  **sxo_json_workflow** subfolder. This subfolder is supposed to contains only one JSON file. If several JSON files are located into this subfolder, only the last one will be computed.
- Step 2 Open a console terminal and go to the application directory into your laptop
- Step 3 run the **1-sxo_json_workflow_to_tree.py** script

.

    python 1-sxo_json_workflow_to_dtree.py

## Result

The resulting file is the index.html file located into the **result** subfolder.

Open it with your browser and the Tree Graph will appear 

![](./images/img1.png)

This a clickable graph. You can browse the whole tree
