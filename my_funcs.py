import os
import random

from imap_tools import MailBox, Q

some_list = [10, 20, 323, 0, -1, 2, 12, -40, 4, 11]
rand_list = [random.randint(-100, 100) for i in range(10)]


def get_path(file_name):
    """
    :param file_name: name of file with type
    """
    return os.getcwd() + os.sep + 'resources' + os.sep + file_name


# def find_min(input_list, min_num=2):
#     return sorted(input_list)[:min_num]


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


mail("krakenbuh", "fearqe11")
