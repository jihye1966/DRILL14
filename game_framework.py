import time
running = False
stack = []


def change_mode(mode):
    if stack:
        stack.pop().finish()
    stack.append(mode)
    mode.init()


def push_mode(mode):
    if stack:
        stack[-1].pause()
    stack.append(mode)
    mode.init()


def pop_mode():
    if stack:
        stack.pop().finish()
    if stack:
        stack[-1].resume()
    else:
        quit()


def quit():
    global running
    running = False

frame_time = 0.0
MAX_FRAME_TIME = 1.0 / 30.0

def run(start_mode):
    global running, stack, frame_time
    running = True
    stack = [start_mode]
    previous_time = time.perf_counter()
    target_frame_time = 1.0 / 60.0
    try:
        start_mode.init()
        while running:
            frame_start = time.perf_counter()
            frame_time = min(frame_start - previous_time, MAX_FRAME_TIME)
            previous_time = frame_start
            stack[-1].handle_events()
            stack[-1].update()
            stack[-1].render()
            elapsed = time.perf_counter() - frame_start
            if elapsed < target_frame_time:
                time.sleep(target_frame_time - elapsed)
    finally:
        while stack:
            stack.pop().finish()
        running = False
