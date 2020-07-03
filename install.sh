#!/bin/bash

mkdir -p ~/.goals
rm ~/.goals/current_goal.sh
ln -s $(pwd)/current_goal.sh ~/.goals/current_goal.sh

