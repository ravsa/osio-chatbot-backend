#!/bin/bash

#train
python3 main.py train all

#run server
python3 main.py run http-server
