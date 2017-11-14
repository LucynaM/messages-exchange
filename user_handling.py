import argparse
from clcrypto import check_password
from models import User
from connection import mysql_connection



def set_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username",
                        action="store", dest="username", default=None,
                        help="Specify user login")
    parser.add_argument("-p", "--password",
                        action="store", dest="password", default=None,
                        help="Specify user password")
    parser.add_argument("-n", "--new-pass",
                        action="store", dest="newpass", default=None,
                        help="Change user password")
    parser.add_argument("-l", "--list",
                        action="store_true", dest="list", default=False,
                        help="List all users")
    parser.add_argument("-d", "--delete",
                        action="store_true", dest="delete", default=False,
                        help="Delete user")
    parser.add_argument("-e", "--edit",
                        action="store_true", dest="edit", default=False,
                        help="Edit user")

    options = parser.parse_args()
    return options



def solution(options):

    if options.username and options.password:
        err_msg = ""

        all_users = mysql_connection(User.load_all_users)
        test = [True for user in all_users if options.username in user.username]

        # register new user
        if not options.edit and not options.newpass and not options.delete:
            if test:
                err_msg += "Login has to be unique "
            if len(options.password) < 8:
                err_msg += "Password must be at least 8 characters long "

            if err_msg:
                print(err_msg)
            else:
                new_user = User()
                new_user.username = options.username
                new_user.set_email()
                new_user.set_password(options.password, None)
                #print(new_user.__dict__)
                mysql_connection(new_user.save_to_db)

        # handle existing user
        else:
            if not test:
                err_msg += "Login is incorrect "
            else:
                existing_user = mysql_connection(User.load_user_by_login, login=options.username)
                # check if password is correct
                if check_password(options.password, existing_user.hashed_password):
                    # delete user
                    if options.delete:
                        mysql_connection(existing_user.delete)
                    # edit user - incorrect data
                    elif options.edit and not options.newpass:
                        err_msg += "New password is required"
                        print(err_msg)
                    # edit user
                    elif options.edit and options.newpass:
                        if len(options.newpass) < 8:
                            err_msg += "Password must be at least 8 characters long"
                            print(err_msg)
                        else:
                            existing_user.set_password(options.newpass, None)
                            mysql_connection(existing_user.save_to_db)
                else:
                    err_msg += "Password is incorrect "
                    print(err_msg)

    elif options.list:
        for user in mysql_connection(User.load_all_users):
            print(user.username, user.email, user.id)


if __name__ == "__main__":

    solution(set_options())

# options to obiekt Namespace, gdzie username, password itd. stają się atrybutami, wartość domyślna = false, jeżeli użyjemy - true
# jeżeli przy odpalaniu tego pliku w terminalu użyjesz flagi -p, -u, -p, -t
# wartość przechowywana w options.movies, options.cinemas, options.payments i options.tickets będzie True
