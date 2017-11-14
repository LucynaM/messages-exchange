import argparse
from clcrypto import check_password
from models import User
from message import Message
from connection import mysql_connection



def set_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username",
                        action="store", dest="username", default=None,
                        help="Set user login")
    parser.add_argument("-p", "--password",
                        action="store", dest="password", default=None,
                        help="Set user password")
    parser.add_argument("-l", "--list",
                        action="store_true", dest="list", default=False,
                        help="List all msg")
    parser.add_argument("-t", "--to",
                        action="store", dest="to", default=None,
                        help="Set to_usr")
    parser.add_argument("-s", "--send",
                        action="store", dest="send", default=None,
                        help="Send msg")

    options = parser.parse_args()
    return options



def solution(options):



    if options.username and options.password:
        err_msg = ""

        all_users = mysql_connection(User.load_all_users)
        test = [True for user in all_users if options.username in user.username]
        if not test:
            err_msg += "Login is incorrect "
            print(err_msg)
        else:
            usr = mysql_connection(User.load_user_by_login, login=options.username)
            if check_password(options.password, usr.hashed_password):
                # send message -t, -s
                if options.to and options.send:
                    # check if to_usr exists in db
                    to_usr = mysql_connection(User.load_user_by_login, login=options.to)
                    if not to_usr:
                        err_msg += "Unknown recipient"
                        print(err_msg)
                        return False
                    if options.send == "":
                        err_msg += "Message can't be empty value"
                        print(err_msg)
                        return False
                    # set new message
                    msg = Message()
                    msg.set_date()
                    msg.from_usr = usr.id
                    msg.to_usr = to_usr.id
                    msg.text = options.send
                    mysql_connection(msg.save_to_db)
                    print("Message sent")

                # list message to user -l
                elif options.list:
                    for msg in mysql_connection(Message.load_all_msg_for_user, usr.id):
                        print("from: %s \ndate: %s  \nmessage: %s " % (usr.username, msg.date, msg.text))

            else:
                err_msg += "Password is incorrect "
                print(err_msg)


if __name__ == "__main__":

    solution(set_options())

# options to obiekt Namespace, gdzie username, passworrd itd. stają się atrybutami, wartość domyślna = false, jeżeli użyjemy - true
# jeżeli przy odpalaniu tego pliku w terminalu użyjesz flagi -m, -c, -p, -t
# wartość przechowywana w options.movies, options.cinemas, options.payments i options.tickets będzie True
# jak się to ma do flaska
# dlaczego w help jest "display all movies itd" kiedy zadanie brzmi - usuń
