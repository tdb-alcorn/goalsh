import sys
import json
import os.path
import hashlib


goals_dir = os.path.join(os.path.expanduser('~'), '.goals')
goals_file = os.path.join(goals_dir, 'goals.json')


class Goal:
    def __init__(self, parent: str, text: str, done: bool):
        # TODO add created_at, completed_at timestamps
        self.parent = parent
        self.text = text
        self.done = done

    def __eq__(self, other) -> bool:
        if type(other) is not Goal:
            return False
        return (self.text == other.text and
                self.parent == other.parent and
                self.done == other.done)

    def __hash__(self) -> int:
        return hash((self.parent, self.text, self.done))

    def id(self) -> str:
        h = hashlib.md5()
        if self.parent is not None:
            h.update(bytes(self.parent, 'utf8'))
        h.update(bytes(self.text, 'utf8'))
        return h.hexdigest()


class GoalJSONEncoder(json.JSONEncoder):
    def default(self, o) -> str:
        if type(o) is Goal:
            return {
                'parent': o.parent,
                'text': o.text,
                'done': o.done,
            }
        return json.JSONEncoder.default(self, o)


def decode_goal(obj: dict) -> Goal:
    if 'parent' in obj and 'text' in obj and 'done' in obj:
        return Goal(obj['parent'], obj['text'], obj['done'])
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


def push(goals: 'Dict[str, Goal]', current: Goal, text: str) -> Goal:
    if current is None:
        goal = Goal(None, text, False)
    else:
        goal = Goal(current.id(), text, False)
    goals[goal.id()] = goal
    return goal


def pop(goals: 'Dict[str, Goal]', current: Goal) -> Goal:
    current.done = True
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
        pass

    write_goals(goals, current)

if __name__ == '__main__':
    main()

