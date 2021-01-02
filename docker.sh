#!/bin/bash
docker-compose build
docker-compose up
open -a "Google Chrome" http://127.0.0.1:8000