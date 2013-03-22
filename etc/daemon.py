import os, sys, time, signal
if __name__ == "__main__":
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    open("parent.pid", "w").write("%d\n"%os.getpid())
    if os.fork() != 0:
        time.sleep(60)
        sys.exit(0)
    os.setsid()
    open("zombie.pid", "w").write("%d\n"%os.getpid())
    if os.fork() != 0:
        os._exit(0)
    open("daemon.pid", "w").write("%d\n"%os.getpid())
    sys.exit(0)

