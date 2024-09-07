#  Reference https://realpython.com/python-send-email/
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from threading import Thread, Lock
import time
from collections import deque
import logging
logger = logging.getLogger('MainLogger')
from ..models.IncidentModel import IncidentModel
from ..models.EventModel import EventModel
import os


class GMailing:
    def __init__(self):
        super(GMailing, self).__init__()
        self.sender_email = "ddskaawal@gmail.com"
        self.password = "zzdxckqgcoixzinz"
        self._elements = deque()

        t = Thread(target=self.process_email_queue)
        t.daemon = True
        t.start()

    def process_email_queue(self):
         while True:
            try:
                if len(self._elements) > 0:
                    logger.info('Sending email')
                    email_info = self.dequeue()
                    text =  email_info["text"]
                    html = email_info["html"]
                    receiver_email = email_info["receipients"]

                    message = MIMEMultipart("alternative")
                    message["Subject"] = email_info["subject"]
                    message["From"] = self.sender_email
                    message["To"] =   ", ".join(email_info["receipients"]) 
                    part1 = MIMEText(text, "plain")
                    part2 = MIMEText( html, "html")
                    message.attach(part1)
                    message.attach(part2)

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()  # Use TLS encryption
                    server.login(self.sender_email, self.password)
                    server.sendmail(self.sender_email, receiver_email, message.as_string())

                    print(self.sender_email, receiver_email, "DONE")
                    server.quit()
                    logger.info('Sending email done without failure')
            except Exception as e:
                logger.error('Sending email error', e)
                print(e)
            time.sleep(0.1)



    def send(self, receipients, subject, text, html):
        data = {
            "receipients" : receipients,
            "subject": subject,
            "text" : text,
            "html" : html
        }

        print(f'Insert email in queue for receipients of {receipients} with {subject}')
        logger.info(f'Insert email in queue for receipients of {receipients} with {subject}')

        self._elements.append(data)

    def send_incident(self,  incident: IncidentModel, emails, location, device):
        logger.info(f'send_incident emails={emails} location= {location}, device-{device}')

        mapUrl="https://maps.google.com/?q="+ str(incident.latitude) + "," + str(incident.longitude)
        
        imageUrl = os.getenv('API_PUBLIC_URL')+ "incident/image/" + str(incident.imagepath)
        imageDisplayUrl = os.getenv('API_PUBLIC_URL')+ "incident/image_display/" + str(incident.imagepath)

        videoUrl = os.getenv('API_PUBLIC_URL')+ "incident/video/" + str(incident.videopath)
        videoDisplayUrl = os.getenv('API_PUBLIC_URL')+ "incident/video_display/" + str(incident.videopath)

        incident_datetime = incident.datetime.strftime("%d/%m/%Y %H:%M:%S")

        text = f"<h5>Incident Alert!!!</h5>"
        text += f"Incident Type: {incident.incidenttype}"
        text += "<br/>"
        text += "<br/>"
        text += f"Date & Time : {incident_datetime}"
        text += "<br/>"
        text += f"Location : {location}"
        text += "<br/>"
        text += f"Device Name: {device}"
        text += "<br/>"
        text += "<br/>"
        text += "<h5>Alert Details</h5>"
        text += f"Section: {incident.section}"
        text += "<br/>"
        text += f"Azimuth: {incident.positionx} degree"
        text += "<br/>"
        text += f"Distance: {incident.distanceinmeter} meter"
        text += "<br/>"
        text += "<br/>"
        text += f"Thermal Image: <a href = {imageUrl}>View</a>"
        text += "<br/>"
        text += f"RGB Image: <a href = {imageDisplayUrl}>View</a>"
        text += "<br/>"
        text += "<br/>"
        text += f"Thermal Video: <a href = {videoUrl}>View</a>"
        text += "<br/>"
        text += f"RGB Video: <a href = {videoDisplayUrl}>View</a>"
        text += "<br/>"
        text += "<br/>"
        text += f"Map Location: <a href = {mapUrl}>View</a>"
        text += "<br/>"
        text += "<h5>Recommended Actions</h5>"

        text += "Secure the Area: <br/>If safe to do so, deploy security personnel to the affected area and ensure the safety of occupants."
        text += "<br/><br/>"
        text += "Review Camera Footage: <br/>Examine the recorded footage for further analysis and identify any additional details that may aid in the investigation."
        text += "<br/><br/>"
        text += "Assess Security Measures: <br/>Evaluate the effectiveness of existing security measures and consider any necessary improvements."
        text += "<br/><br/>"
        text += "Notify Key Personnel: <br/>Inform the relevant stakeholders, including management, security personnel, and property owners, about the intrusion."
        text += "<br/><br/>"
        text += "Please take appropriate action promptly to ensure the safety and security of the premises."
        text += "<br/><br/>"
        text += "Contact Authorities: <br/>Immediately notify the local law enforcement authorities and provide them with the relevant details."
        text += "<br/>"

        self.send(
            receipients = emails,
            subject=f"Incident Alert at [{location}] from devices [{device}]",
            text = text,
            html = text
            )


    def send_event(self,  event: EventModel, emails, location, device = None):
        logger.info(f'send_event emails={emails} location= {location}, device-{device}')

        event_datetime = event.datetime.strftime("%d/%m/%Y %H:%M:%S")
        text = f"<h5>Event Type: {location}</h5>"
        text += f"Date & Time : {event_datetime}"
        text += "<br/>"
        text += f"Location : {location}"
        text += "<br/>"
        if device is not None:
            text += f"Device Name: {device}"
            text += "<br/>"
        text += f"Source: {event.source}"
        text += "<br/>"
        text += f"Info: {event.info}"
        text += "<br/>"
        text += f"Details: {event.details}"
        text += "<br/>"

        subject = f"Event Notification from [{location}]"
        if device is not None:
            subject += f" at devices [{device}]"
            

        self.send(
            receipients = emails,
            subject=subject,
            text = text,
            html = text
            )

    def dequeue(self):
        return self._elements.popleft()
    

if __name__ == "__main__":
    mail = GMailing()
    time.sleep(1)

    text = """no url"""

    mail.send(['fakhrul@flybots.tech','fakhrulazran@gmail.com'],'Test Email', text, html= text )
    time.sleep(5)
