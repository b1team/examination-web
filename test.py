import multitimer
import time

def job(t):
    while t:
        mins, secs = divmod(t, 60)
        ti = '{:02d}:{:02d}'.format(mins, secs)
        print(ti, end="\r")
        time.sleep(1)
        t -= 1
    timer.stop()

timer = multitimer.MultiTimer(interval=1, function=job, kwargs={"t": 10})
def ko():
    timer.start()
    return 'ok'

if __name__ == "__main__":
    k = ko()
    print(k)

