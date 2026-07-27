todos = []


def create_todo(category, task):
    todo = {
        "category": category,
        "task": task
    }

    todos.append(todo)

    return todo

def get_todo():
    return todos