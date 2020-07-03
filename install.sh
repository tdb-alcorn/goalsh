#!/bin/bash

# echo "source ~/.goals/current_goal.sh" >> ~/.zshrc
# echo "source ~/.goals/current_goal.sh" >> ~/.bashrc

echo "alias goal=\"python3 $(pwd)/goal.py\"" >> current_goal.sh

mkdir -p ~/.goals
rm ~/.goals/current_goal.sh
ln -s $(pwd)/current_goal.sh ~/.goals/current_goal.sh

