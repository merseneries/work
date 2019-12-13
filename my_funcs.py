import email
import os
import random

from imap_tools import MailBox, Q
from imapclient import IMAPClient

some_list = [10, 20, 323, 0, -1, 2, 12, -40, 4, 11]
rand_list = [random.randint(-100, 100) for i in range(10)]


def get_path(file_name):
    """
    :param file_name: name of file with type
    """
    return os.getcwd() + os.sep + 'resources' + os.sep + file_name


def list_min(array, min_values=2):
    arr_len = len(array)
    for j in range(arr_len):
        for i in range(arr_len - 1):
            if array[i] > array[i + 1]:
                array[i], array[i + 1] = array[i + 1], array[i]
    return array[:min_values]


def mail(username, password):
    mailbox = MailBox("imap.gmail.com")
    mailbox.login(username, password, initial_folder='INBOX')
    recent_msg = [[m.subject, m.from_] for m in mailbox.fetch(Q(new=True))]
    unseen_msg = [[m.subject, m.from_] for m in mailbox.fetch(Q(seen=False), mark_seen=False)]
    mailbox.logout()
    print(recent_msg)
    print(unseen_msg)


# mail("krakenbuh", "fearqe11")


HOST = 'imap.gmail.com'
USERNAME = 'krakenbuh'
PASSWORD = 'fearqe11'

with IMAPClient(HOST) as server:
    server.login(USERNAME, PASSWORD)
    server.select_folder('INBOX', readonly=True)

    messages = server.search("UNSEEN")
    for uid, message_data in server.fetch(messages, 'RFC822').items():
        email_message = email.message_from_bytes(message_data[b'RFC822'])
        print(uid, email_message.get('From'), email_message.get('Subject'), email_message.get('Flag'))
