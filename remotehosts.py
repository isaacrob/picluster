c = get_config()
c.LocalControllerLauncher.controller_args=['--log-to-file','--log-level=20','--ip=10.40.3.12']
c.SSHEngineSetLauncher.engines = {'10.40.3.36':1,'10.40.2.157':1,'10.40.2.158':1,'10.40.2.159':1,'10.40.3.27':1,}
