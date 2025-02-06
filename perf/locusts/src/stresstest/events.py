from locust import events

######################################
#
#           Events
#
######################################

@events.spawning_complete.add_listener
def event_spawn_user(user_count, **kwargs):
    print(f"[event] spawn_user : {user_count}")

@events.user_error.add_listener
def event_user_error():
    print(f"[event] user_error")

@events.report_to_master.add_listener
def event_report_to_master(client_id, data):
    print(f"[event] report_to_master : {client_id} {data}")

@events.worker_report.add_listener
def event_worker_report(client_id, data):
    print(f"[event] worker_report : {client_id} {data}")

@events.worker_connect.add_listener
def event_worker_connect(client_id):
    print(f"[event] worker_connect : {client_id}")

@events.spawning_complete.add_listener
def event_spawning_complete(user_count):
    print(f"[event] spawning_complete : {user_count}")

@events.quitting.add_listener
def event_quitting(environment):
    print(f"[event] quitting {environment}")

@events.quit.add_listener
def event_quit(exit_code):
    print(f"[event] quit {exit_code}")

@events.init.add_listener
def event_init(environment, runner, web_ui):
    print(f"[event] init {environment} {runner} {web_ui}")

@events.init_command_line_parser.add_listener
def event_init_command_line_parser(parser):
    print(f"[event] init_command_line_parser")

@events.test_start.add_listener
def event_test_start(environment):
    print(f"[event] test_start {environment}")

@events.test_stopping.add_listener
def event_test_stopping(environment):
    print(f"[event] test_stopping {environment}")

@events.test_stop.add_listener
def event_test_stop(environment):
    print(f"[event] test_stop")

@events.reset_stats.add_listener
def event_reset_stats():
    print(f"[event] reset_stats")

@events.cpu_warning.add_listener
def event_cpu_warning(environment, cpu_usage):
    print(f"[event] cpu_warning !")

@events.heartbeat_sent.add_listener
def event_heartbeat_sent(client_id, timestamp):
    print(f"[event] heartbeat_sent from {client_id} [{timestamp}]")

@events.heartbeat_received.add_listener
def event_heartbeat_received(client_id, timestamp):
    print(f"[event] heartbeat_received from {client_id} [{timestamp}]")

@events.usage_monitor.add_listener
def event_usage_monitor(environment, cpu_usage, memory_usage):
    print(f"[event] usage_monitor : CPU:{cpu_usage} / MEM:{memory_usage}")
    print(f"[event] fail ratio : {environment.stats.total.fail_ratio}")
    if environment.stats.total.fail_ratio > 0.2:
        print("[event] WARNING : too many fail")



