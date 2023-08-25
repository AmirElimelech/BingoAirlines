# this file is used to schedule tasks to run in the background , for example the download_airline_logo task , which is used to download the logo of the airline company from the API and save it in the database , is scheduled to run every 24 hours , so that the logo is always up to date , and the user doesn't have to wait for the logo to be downloaded every time he/she searches for a flight.

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.start()



