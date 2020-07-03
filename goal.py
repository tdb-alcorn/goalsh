import datetime
import hashlib
import json
import os
import os.path
import pytz
import sys
import time


goals_dir = os.path.join(os.path.expanduser('~'), '.goals')
goals_file = os.path.join(goals_dir, 'goals.json')
current_goal_file = os.path.join(goals_dir, 'current_goal.txt')


class Goal:
    def __init__(self, parent: str, text: str, done: bool,
            created_at: datetime.datetime, completed_at: datetime.datetime):
        # TODO add created_at, completed_at timestamps
        self.parent = parent
        self.text = text
        self.done = done
        self.created_at = created_at
        self.completed_at = completed_at

    def __eq__(self, other) -> bool:
        if type(other) is not Goal:
            return False
        return (self.text == other.text and
                self.parent == other.parent and
                self.done == other.done and
                self.created_at == self.created_at and
                self.completed_at == self.completed_at)

    def __hash__(self) -> int:
        return hash((self.parent, self.text, self.done, self.created_at,
            self.completed_at))

    def id(self) -> str:
        h = hashlib.md5()
        if self.parent is not None:
            h.update(bytes(self.parent, 'utf8'))
        h.update(bytes(self.text, 'utf8'))
        h.update(bytes(str(self.created_at), 'utf8'))
        return h.hexdigest()


class GoalJSONEncoder(json.JSONEncoder):
    def default(self, o) -> str:
        if type(o) is Goal:
            return {
                'parent': o.parent,
                'text': o.text,
                'done': o.done,
                'created_at': o.created_at,
                'completed_at': o.completed_at,
            }
        elif type(o) is datetime.datetime:
            return time_to_str(o)
        return json.JSONEncoder.default(self, o)


def decode_goal(obj: dict) -> Goal:
    if ('parent' in obj and 'text' in obj and 'done' in obj and
        'created_at' in obj and 'completed_at' in obj):
        completed_at = None
        if obj['completed_at'] is not None:
            completed_at = time_from_str(obj['completed_at'])
        return Goal(obj['parent'], obj['text'], obj['done'],
                time_from_str(obj['created_at']),
                completed_at)
    return obj


def ensure_goals_file_exists():
    if not os.path.exists(goals_dir):
        os.mkdir(goals_dir)
    if not os.path.exists(goals_file):
        open(goals_file, 'x')


def write_goals(goals: 'Dict[str, Goal]', current: Goal):
    if current is not None:
        current = current.id()
    with open(goals_file, 'w') as f:
        enc = GoalJSONEncoder()
        f.write(enc.encode({
            'goals': goals,
            'current': current,
        }))


def read_goals():
    with open(goals_file, 'r') as f:
        s = f.read()
        if s == '':
            return {
                'goals': dict(),
                'current': None,
            }
        dec = json.JSONDecoder(object_hook=decode_goal)
        return dec.decode(s)


def now() -> datetime.datetime:
    return datetime.datetime.now(pytz.utc)


time_format = '%Y-%m-%dT%H:%M:%S.%f%z'


def time_to_str(d: datetime.datetime) -> str:
    return d.strftime(time_format)


def time_from_str(d: str) -> datetime.datetime:
    return datetime.datetime.strptime(d, time_format)


def push(goals: 'Dict[str, Goal]', current: Goal, text: str) -> Goal:
    if current is None:
        parent = None
    else:
        parent = current.id()
    goal = Goal(parent, text, False, now(), None)
    goals[goal.id()] = goal
    return goal


def pop(goals: 'Dict[str, Goal]', current: Goal) -> Goal:
    if current is None:
        return None
    current.done = True
    current.completed_at = now()
    if current.parent is None:
        return None
    return goals[current.parent]


def main():
    ensure_goals_file_exists()

    d = read_goals()
    goals = d['goals']
    current = d['current']
    if current is not None:
        current = goals[current]

    action = sys.argv[1]

    if action == 'push':
        arg = sys.argv[2]
        current = push(goals, current, arg)
    elif action == 'pop':
        current = pop(goals, current)

    if current is None:
        # TODO victory
        print("All goals finished!")
        with open(current_goal_file, 'w+') as f:
            f.write('')
    else:
        with open(current_goal_file, 'w+') as f:
            f.write('[' + current.text + '] ')

    write_goals(goals, current)

if __name__ == '__main__':
    main()

