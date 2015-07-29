c = get_config()
c.LocalControllerLauncher.controller_args=['--log-to-file','--log-level=20','--ip=10.40.16.106']
c.SSHEngineSetLauncher.engines = {'10.40.16.107':2,'10.40.16.108':2,'10.40.16.110':2,}
