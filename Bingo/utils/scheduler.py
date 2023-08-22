from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.start()



# this is the function that will be called by the scheduler to download the airline logo from the URL if not supplied by the user