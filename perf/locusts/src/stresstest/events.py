from locust import events

######################################
#
#           Events
#
######################################

@events.spawning_complete.add_listener
def event_spawn_user(user_count, **kwargs):
    print(f"[EVENT] spawn_user : {user_count}")

@events.user_error.add_listener
def event_user_error():
    print(f"[EVENT] user_error")

@events.report_to_master.add_listener
def event_report_to_master(client_id, data):
    print(f"[EVENT] report_to_master : {client_id} {data}")

@events.worker_report.add_listener
def event_worker_report(client_id, data):
    print(f"[EVENT] worker_report : {client_id} {data}")

@events.worker_connect.add_listener
def event_worker_connect(client_id):
    print(f"[EVENT] worker_connect : {client_id}")

@events.spawning_complete.add_listener
def event_spawning_complete(user_count):
    print(f"[EVENT] spawning_complete : {user_count}")

@events.quitting.add_listener
def event_quitting(environment):
    print(f"[EVENT] quitting {environment}")

@events.quit.add_listener
def event_quit(exit_code):
    print(f"[EVENT] quit {exit_code}")

@events.init.add_listener
def event_init(environment, runner, web_ui):
    print(f"[EVENT] init {environment} {runner} {web_ui}")

@events.init_command_line_parser.add_listener
def event_init_command_line_parser(parser):
    print(f"[EVENT] init_command_line_parser")

@events.test_start.add_listener
def event_test_start(environment):
    print(f"[EVENT] test_start {environment}")

@events.test_stopping.add_listener
def event_test_stopping(environment):
    print(f"[EVENT] test_stopping {environment}")

@events.test_stop.add_listener
def event_test_stop(environment):
    print(f"[EVENT] test_stop")

@events.reset_stats.add_listener
def event_reset_stats():
    print(f"[EVENT] reset_stats")

@events.cpu_warning.add_listener
def event_cpu_warning(environment, cpu_usage):
    print(f"[EVENT] cpu_warning !")

@events.heartbeat_sent.add_listener
def event_heartbeat_sent(client_id, timestamp):
    print(f"[EVENT] heartbeat_sent from {client_id} [{timestamp}]")

@events.heartbeat_received.add_listener
def event_heartbeat_received(client_id, timestamp):
    print(f"[EVENT] heartbeat_received from {client_id} [{timestamp}]")

@events.usage_monitor.add_listener
def event_usage_monitor(environment, cpu_usage, memory_usage):
    print(f"[EVENT] usage_monitor : CPU:{cpu_usage} / MEM:{memory_usage}")
    print(f"[EVENT] fail ratio    : {environment.stats.total.fail_ratio}")
    if environment.stats.total.fail_ratio > 0.2:
        print("[EVENT] WARNING : too many fail")



