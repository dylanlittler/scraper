import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(from_email, email_server, password, to_email, scrape_data):
    me = from_email
    my_password = password
    you = to_email

    # initialise dict with email components to be handled by MIMEMultipart
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Links"
    msg['From'] = me
    msg['To'] = you

    # scrape_data is passed in externally, in dict form, so this must be unpacked
    scrape_values = scrape_data.items()

    # key and value for scrape_data are passed to a list with html tags for email formatting
    scrape_links = []
    for title, link in scrape_values:
        scrape_links.append('<li><a href="' + link + '" target="blank">' + title + '</a></li>')

    # list items are joined into one html entity
    html = ''.join(scrape_links)
    # pass html to email handling function to be formatted as html
    part2 = MIMEText(html, 'html')

    # call attach function of MIMEMultipart to attach html as body of email
    msg.attach(part2)

    # Open SSL connection to email server
    s = smtplib.SMTP_SSL(email_server)

    # Displays debugging information if this is run as main in the terminal
    s.set_debuglevel(1)

    s.login(me, my_password)

    s.sendmail(me, you, msg.as_string())
    s.quit()

# Test to confirm module works. scraping.py must be imported to run test    
if __name__ == "__main__":
    import scraping
    email = raw_input("Enter email: ")
    server = raw_input("Enter the server and port number for this email: ")
    password = raw_input("Enter password: ")
    to_email = raw_input("Enter the email you would like to send to: ")
    scrape = scraping.search_stackoverflow("http://stackoverflow.com/unanswered/tagged/python", "a", "question-hyperlink", "http://stackoverflow.com")
    send_email(email, server, password, to_email, scrape)
