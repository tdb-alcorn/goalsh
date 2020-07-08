# Goal

Goal is a shell utility that tracks a stack of goals you create and modifies your prompt to display the current goal.


## Usage

```
$ goal status
Goal stack is empty.
$ goal push "add feature X"
[add feature X] $ goal push "add unit test for X"
[add unit test for X] $ goal status
* add unit test for X - created at ...
  add feature X - created at ...
[add unit test for X] $ goal pop
[add feature X] $ goal status
* add feature X - created at ...
[add feature X] $ goal pop
All goals finished. Time for cake!
```


## Install

Clone this repo and run `./install.sh`. Then add the following line to your .bashrc file:

```
source ~/.goals/current_goal.sh
```

You can achieve this by running the following command:

```
echo "source ~/.goals/current_goal.sh" >> ~/.bashrc
```

If you use a shell other than bash, you'll need to modify the appropriate rc file. For example, if you use zsh you should modify the `.zshrc` file instead.
