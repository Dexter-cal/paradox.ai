import os
import signal
import sys
import threading

class KillSwitchEngine:
    def __init__(self, swarm_engine):
        self.swarm = swarm_engine
        self.is_halted = False

    def activate(self):
        """Halts all autonomous activities and prepares for shutdown."""
        print("[KILL_SWITCH] EMERGENCY ACTIVATION INITIATED")
        self.is_halted = True

        # 1. Stop all swarm missions
        tasks = self.swarm.get_status()
        for task_id in tasks:
            print(f"[KILL_SWITCH] Terminating task: {task_id}")
            # In a real system we'd use thread events to stop them gracefully or kill them
            self.swarm.active_tasks[task_id]['status'] = 'TERMINATED_BY_KILL_SWITCH'

        # 2. Schedule server shutdown
        def shutdown():
            time.sleep(2)
            print("[KILL_SWITCH] Shutting down system process...")
            os.kill(os.getpid(), signal.SIGINT)

        import time
        threading.Thread(target=shutdown).start()

        return "Prob AI is entering emergency halt. Server will terminate in 2 seconds."
