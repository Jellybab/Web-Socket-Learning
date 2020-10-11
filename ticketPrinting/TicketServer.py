#!/usr/bin/python           # This is server.py file
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

import socket, pickle  # Import socket module


import cgi
import tempfile
import win32api
import win32print



def Main():
    while True:

        host = socket.gethostname()  # Get local machine name
        port = 12345  # Reserve a port for your service.

        s = socket.socket()  # Create a socket object
        s.bind((host, port))  # Bind to the port

        s.listen(5)  # Now wait for client connection.
        c, addr = s.accept()  # Establish connection with client.
        print('Got connection from' + str(addr))
        while True:
            data = c.recv(1024)
            if not data:
                break
            commands = pickle._loads(data)
            if commands[0].upper() == 'DISCONNECT':
                c.close()
                break
            else:
                serverCommands(commands)

        c.close()  # Close the connection



def serverCommands(data):
    if data[0].upper() == 'PRINT':
        printTest()


def printTest():
    source_file_name = "c:/temp/temp.txt"
    pdf_file_name = tempfile.mktemp(".pdf")

    styles = getSampleStyleSheet()
    h1 = styles["h1"]
    normal = styles["Normal"]

    doc = SimpleDocTemplate(pdf_file_name)
    #
    # reportlab expects to see XML-compliant
    #  data; need to escape ampersands &c.
    #
    text = cgi.escape(open(source_file_name).read()).splitlines()

    #
    # Take the first line of the document as a
    #  header; the rest are treated as body text.
    #
    story = [Paragraph(text[0], h1)]
    for line in text[1:]:
        story.append(Paragraph(line, normal))
        story.append(Spacer(1, 0.2 * inch))

    doc.build(story)
    win32api.ShellExecute(
        0,
        "print",
        pdf_file_name,
        '/d:"%s"' % win32print.GetDefaultPrinter(),
        ".",
        1

    )


if __name__ == '__main__':
    Main()

