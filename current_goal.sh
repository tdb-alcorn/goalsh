#!/bin/bash

function current_goal () {
	cat ~/.goals/current_goal.txt
}

local cg='$(current_goal)'

export PS1="${cg}${PS1}"

