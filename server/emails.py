from imap_tools import MailBox, Q
from imapclient import IMAPClient

from my_funcs import get_path


def file_read(name):
    full_path = get_path(name)
    with open(full_path, "r") as file:
        data = file.readline()
    return data


def file_write(name, input_data="0"):
    full_path = get_path(name)
    with open(full_path, "w") as file:
        file.write(input_data)


def print_data(data):
    if len(data) != 0:
        for v in data:
            print(v)
    return "Empty"


def mail(username, password):
    mailbox = MailBox("imap.gmail.com")
    mailbox.login(username, password, initial_folder='INBOX')
    recent_msg = [[m.subject, m.from_] for m in mailbox.fetch(Q(new=True))]
    unseen_msg = [[m.subject, m.from_] for m in mailbox.fetch(Q(seen=False), mark_seen=False)]
    mailbox.logout()
    print(recent_msg)
    print(unseen_msg)

    # mail("krakenbuh", "fearqe11")

    USERNAME = "testmeallseasons"
    PASSWORD = "testqe13"


def imap_client(user, password):
    HOST = "imap.gmail.com"
    FILE_NAME = "server_count"

    with IMAPClient(HOST) as server:
        server.login(user, password)
        server.select_folder("INBOX", readonly=True)

        messages = server.search("UNSEEN")
        data = dict()
        for uid, message_data in server.fetch(messages, 'RFC822').items():
            email_message = email.message_from_bytes(message_data[b'RFC822'])
            data[uid] = [email_message.get('From'), email_message.get('Subject')]

        counter = int(file_read(FILE_NAME))
        last_uid = list(data)[-1]
        msg_len = len(data)
        diff_len = msg_len - (last_uid - counter) - 1
        new_msg = []

        if counter < last_uid:
            new_msg = [data[n] for n in list(data)[msg_len:diff_len:-1]]
            file_write(FILE_NAME, str(last_uid))
        old_msg = [data[n] for n in list(data)[diff_len:0:-1]]

        print("New", len(new_msg), "\n", print_data(new_msg))
        print("Old", len(old_msg)), "\n", print_data(old_msg)


USERNAME = "krakenbuh"
PASSWORD = "fearqe11"

# pop_client(USERNAME, PASSWORD)
# imap_client(USERNAME, PASSWORD)
