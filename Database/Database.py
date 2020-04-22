from Database.config import *
import traceback
import tkinter as tk
from tkinter import messagebox

def set_artist(track_title, track_genre, track_location, track_artist):
    """
    Function to set only artist details
    Returns boolean True if set else False
    gets invoked in the get song function
    """

    try:
        collection = db.collection(u'artist').document(track_artist)
        collection.set({
            'name': track_artist,
            'image_url':''
        })
        artistTracks = db.collection(u'artist/' + track_artist + '/tracks').document(track_title)
        artistTracks.set({
            'title': track_title,
            'genre': track_genre,
            'location': track_location,
            'artist':track_artist

        })
        print('artist added')
        return True
    except Exception as ex:
        messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
        
        print('Exception Occurred which is of type :', ex.__class__.__name__)
        y = input('If you want to see Traceback press 1 : ')
        if y == '1':
            traceback.print_exc()
        return False


def Check_artist(artist):
    """
    Returns boolean value if the artist exist or not in the database
    """
    try:
        doc_ref = db.collection(u'artist').document(artist)
        if doc_ref.get().to_dict() is None:
            raise Exception('Not such artist registered')
        print('Artist got successfully')
        return True
    except Exception as ex:
        messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
        
        print('Exception Occurred which is of type :', ex.__class__.__name__)
        y = input('If you want to see Traceback press 1 : ')
        if y == '1':
            traceback.print_exc()
        return False


def get_artist_tracks(artist):
    """
    Returns a list of the objects of tracks
    if the artist exist or else returns False

    """
    try:
        doc_ref = db.collection(u'artist/' + artist + '/tracks')
        if list(doc_ref.stream()) is None:
            raise Exception('Not such artist registered')
        tracks = list(map(lambda x: x.to_dict(), list(doc_ref.stream())))
        return tracks
    except Exception as ex:
        messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
        
        print('Exception Occurred which is of type :', ex.__class__.__name__)
        y = input('If you want to see Traceback press 1 : ')
        if y == '1':
            traceback.print_exc()
        return False


def set_track(track_title, track_genre, track_location, track_artist):
    """
    Function to set only track details
    Returns boolean depending if the value is successfully set then 'True' else 'False'

    """
    if track_artist == '' or track_genre == '' or track_location == '' or track_title == '':
        raise Exception('Cannot generate with empty Field')
    try:
        collection = db.collection(u'Tracks').document(track_title)
        collection.set({
            'artist': track_artist,
            'genre': track_genre,
            'location': track_location,
            'title': track_title
        })
        print('Track added successfully')
        set_artist(track_title, track_genre, track_location, track_artist)
        set_genre(track_genre)
        return True
    except Exception as ex:
        messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
        
        print('Exception Occurred which is of type :', ex.__class__.__name__)
        y = input('If you want to see Traceback press 1 : ')
        if y == '1':
            traceback.print_exc()
        return False


def get_track(trackName):
    """
    Fetch particular track for user
    returns dictitonary with the keys as
    artist, genre, location , title
    if failed returns false
    """
    try:
        doc_ref = db.collection(u'Tracks').document(trackName)
        if doc_ref.get().to_dict() is None:
            raise Exception("No such track found")
        return doc_ref.get().to_dict()
    except Exception as ex:
        messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
        
        print('Exception Occurred which is of type :', ex.__class__.__name__)
        y = input('If you want to see Traceback press 1 : ')
        if y == '1':
            traceback.print_exc()
        return False


def register_user(username, email, phone_number, password):
    """
    Returns user uid if successfully registered
    else returns false
    """
    from firebase_admin import auth
    try:
        if username == '' or email == '' or phone_number == '':
            raise Exception('Some of fields were found to be empty')
        elif len(password) <= 6:
            raise Exception('Password length less then equal to 6')
        user = auth.create_user(
            email=email,
            phone_number='+91' + phone_number,
            password=password,
            display_name=username,
            email_verified = False,

        )
        doc_ref = db.collection(u'users').document(user.uid)
        doc_ref.set({
            'email': email,
            'phone_number': '+91' + phone_number,
            'password': password,
            'display_name': username,
            'email_verified':False
        })
        print('Successfully created new user: {0}'.format(user.uid))
        return user.uid
    except firebase_admin._auth_utils.EmailAlreadyExistsError as ex:
        from Pages.UserAuthentication.Exceptions import Email_already_exists
        Email_already_exists()
        return False
    except firebase_admin._auth_utils.PhoneNumberAlreadyExistsError as ex:
        from Pages.UserAuthentication.Exceptions import Phone_already_exists
        Phone_already_exists()
        return False
    except firebase_admin._auth_utils.UserNotFoundError as ex:
        from Pages.UserAuthentication.Exceptions import User_not_Found
        User_not_Found()
        return False
    except Exception as ex:
        messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
        
        print('Exception Occurred which is of type :', ex.__class__.__name__)
        y = input('If you want to see Traceback press 1 : ')
        if y == '1':
            traceback.print_exc()
        return False


def set_album(track_title, album_name, artist):
    """
 Returns boolean value depending upon success
 and atleast one track in needed for the album.
    """
    try:
        track_object = get_track(track_title)
        doc_ref = db.collection(u'albums/' + album_name + '/tracks').document(track_object['title'])
        doc_ref.set(track_object)
        doc_ref = db.collection(u'albums').document(album_name)
        doc_ref.set({
            'album_title': album_name,
            'artist': artist
        })
        print('Album Created Successfully')
        return True
    except Exception as ex:
        messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
        
        print('Exception Occured which is of type :', ex.__class__.__name__)
        y = input('If you want to see Traceback press 1 : ')
        if y == '1':
            traceback.print_exc()
        return False


def get_album(**kwargs):
    """
    parameters : album_name, artist_name
    if want all the albums dont pass any argument else pass name of the album or artist of the album.
    eg:- get_album(album_name = devdatta)
    Kwargs : album_name
    """

    if 'album_name' in kwargs:
        try:
            doc_ref = db.collection(u'albums/' + kwargs['album_name'] + '/tracks')
            snapshots = list(doc_ref.stream())
            if len(snapshots):
                tracks = list(map(lambda x: x.to_dict(), snapshots))
                return tracks
        except Exception as ex:
            messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
            
            print('Exception Occured which is of type :', ex.__class__.__name__)
            y = input('If you want to see Traceback press 1 : ')
            if y == '1':
                traceback.print_exc()
            return False
    elif 'artist' in kwargs:
        try:
            doc_ref = db.collection('albums')
            snapshots = list(doc_ref.where(u'artist', u'==', kwargs['artist']).stream())

            if len(snapshots):
                object_list = list(map(lambda x: x.to_dict(), snapshots))
                return object_list
            else:
                raise Exception('No data with the give artist found')
        except Exception as ex:
            messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
            
            print('Exception Occurred which is of type :', ex.__class__.__name__)
            y = input('If you want to see Traceback press 1 : ')
            if y == '1':
                traceback.print_exc()
            return False
    else:
        try:
            collection = db.collection(u'albums')
            print(list(map(lambda x: x.to_dict(), collection.stream())))
        except Exception as ex:
            messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
            
            print('Exception Occurred which is of type :', ex.__class__.__name__)
            y = input('If you want to see Traceback press 1 : ')
            if y == '1':
                traceback.print_exc()
            return False


def get_all_tracks():
    """
    Returns a list of all track objects
    if failed returns a false
    """
    try:
        collection = db.collection(u'Tracks')
        return list(map(lambda x: x.to_dict(), collection.stream()))
    except Exception as ex:
        messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
        
        print('Exception Occurred which is of type :', ex.__class__.__name__)
        y = input('If you want to see Traceback press 1 : ')
        if y == '1':
            traceback.print_exc()
        return False

def set_genre(genre):
    '''


    :param genre:
    This is the name of the genre

    :return:
    Bool if success

    '''
    try:
        doc_ref = db.collection(u'genres').document(genre)
        doc_ref.set({
            'genre_name' : genre,
            'genre_image':'',

        })
        return True
    except Exception as ex:
        messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
        
        print('Exception Occurred which is of type :', ex.__class__.__name__)
        y = input('If you want to see Traceback press 1 : ')
        if y == '1':
            traceback.print_exc()
        return False
def get_tracks_by_genre(**kwargs):
    """
    Returns a list of songs with particular genre
    kwarg : genre = 'required genre'
    else return the list of all genres
    if failed returns false
    """
    if 'genre' in kwargs:
        try:
            doc_ref = db.collection('Tracks')
            snapshots = list(doc_ref.where(u'genre', u'==', kwargs['genre']).stream())
            if len(snapshots):
                object_list = list(map(lambda x: x.to_dict(), snapshots))
                # print(object_list)
                return object_list
        except Exception as ex:
            messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
            print('Exception Occurred which is of type :', ex.__class__.__name__)
            y = input('If you want to see Traceback press 1 : ')
            if y == '1':
                traceback.print_exc()
            return False
    else:
        try:
            doc_ref = db.collection(u'genres').stream()
            object_list = list(map(lambda x: x.to_dict(), doc_ref))
            # print(object_list)
            all_dicts = []
            for i in range(len(object_list)):
                my_dict = {
                    'text': object_list[i]['genre_name'],
                     'url': object_list[i]['genre_image'],
                }
                all_dicts.append(my_dict)
            # print(all_dicts)
            return all_dicts
        except Exception as ex:
            messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
            
            print('Exception Occurred which is of type :', ex.__class__.__name__)
            y = input('If you want to see Traceback press 1 : ')
            if y == '1':
                traceback.print_exc()
            return False


def get_user(uid):
    """
    Returns a user object that is dictionary
    of the user with attributes:
    display_name , email , password, phone_number
    """
    # [START get_user]
    from firebase_admin import auth
    try:
        user = auth.get_user(uid)
        print('Successfully fetched user data: {0}'.format(user.uid))
        doc = db.collection(u'users').document(user.uid)
        doc = doc.get().to_dict()
        return doc
    except firebase_admin._auth_utils.UserNotFoundError as ex:
        from Pages.UserAuthentication.Exceptions import User_not_Found
        User_not_Found()
        return False
    except Exception as ex:
        messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
        
        print('Exception Occurred which is of type :', ex.__class__.__name__)
        y = input('If you want to see Traceback press 1 : ')
        if y == '1':
            traceback.print_exc()
        return False

    # [END get_user]


def get_user_by_email(email):
    """
    Returns a user object that is dictionary
    of the user with attributes:
    display_name , email , password, phone_number
    """
    # [START get_user_by_email]
    import firebase_admin
    from firebase_admin import auth 
    try:

        user = auth.get_user_by_email(email)
        doc = db.collection(u'users').document(user.uid)
        doc = doc.get().to_dict()
        return doc
    except firebase_admin._auth_utils.UserNotFoundError as ex:
        from Pages.UserAuthentication.Exceptions import User_not_Found
        User_not_Found()
        return False
    except Exception as ex:
        messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
        
        print('Exception Occurred which is of type :', ex.__class__.__name__)
        y = input('If you want to see Traceback press 1 : ')
        if y == '1':
            traceback.print_exc()
        return False


def get_user_by_phone_number(phone):
    """
    Returns a user object that is dictionary
    of the user with attributes:
    display_name , email , password, phone_number
    """

    from firebase_admin import auth
    try:
        user = auth.get_user_by_phone_number(phone)
        doc = db.collection(u'users').document(user.uid)
        doc = doc.get().to_dict()
        return doc
    
    except firebase_admin._auth_utils.UserNotFoundError as ex:
        from Pages.UserAuthentication.Exceptions import User_not_Found
        User_not_Found()
        return False
    except Exception as ex:
        messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
        
        print('Exception Occurred which is of type :', ex.__class__.__name__)
        y = input('If you want to see Traceback press 1 : ')
        if y == '1':
            traceback.print_exc()
        return False

        # [END get_user_by_phone]


def sign_in_with_phone():
    pass


def sign_in_with_email_and_password(email, password):
    """
    Returns boolean True if user is signed in succesfully
    else false
    """
    from os import path

    try:
        if path.exists('user'):
            f = open('user', 'r')
            doc = get_user(f.readline())
            f.close()
            return doc
        from firebase_admin import auth
        user = auth.get_user_by_email(email)
        doc = get_user_by_email(email)
        if doc['email'] == email and doc['password'] == password:
            f = open('user', "w+")
            f.write(user.uid)
            return doc
        else:
            raise Exception('Credentials invalid')
            # return False
    except firebase_admin._auth_utils.UserNotFoundError as ex:
        from Pages.UserAuthentication.Exceptions import User_not_Found
        User_not_Found()
        return False
    except Exception as ex:
        messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
        
        print('Exception Occurred which is of type :', ex.__class__.__name__)
        y = input('If you want to see Traceback press 1 : ')
        if y == '1':
            traceback.print_exc()
        return False


def sign_out():
    """

    returns True
    if signed out else false
    also remove the user files

    """
    import os
    try:
        os.remove("user")
    except Exception as ex:
        messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
        
        print('Exception Occured which is of type :', ex.__class__.__name__)
        y = input('If you want to see Traceback press 1 : ')
        if y == '1':
            traceback.print_exc()
        return False

    # sign_out()
# myuser = register_user('devdatta','dkhoche70@gmail.com','9145253235','15412342')
def generate_otp(uid):
    import string
    import random

    # Takes random choices from
    # ascii_letters and digits
    try:
        generate_pass = ''.join([random.choice(
                                               string.digits)
                                 for n in range(6)])

        doc_ref = db.collection(u'users').document(uid)
        doc_ref.update({
            'verification_code'  : generate_pass
        })
        print(generate_pass)
        return generate_pass
    except firebase_admin._auth_utils.UserNotFoundError as ex:
        from Pages.UserAuthentication.Exceptions import User_not_Found
        User_not_Found()
        return False
    except Exception as ex:
        messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
        
        print('Exception Occurred which is of type :', ex.__class__.__name__)
        y = input('If you want to see Traceback press 1 : ')
        if y == '1':
            traceback.print_exc()
        return False


def check_verification(email):
    user  = get_user_by_email(email)
    return user['email_verified']


def send_email_verification_otp(email):
    '''

    :param otp:
           email: email of the user
    :return: bool


    '''
    try:
        from firebase_admin import auth
        
        import smtplib
        user = auth.get_user_by_email(email)
        otp = generate_otp(user.uid)
        fromaddr = 'amplifyteam1234@gmail.com.'
        toaddrs = email
        Text = 'Hello '+ user.display_name  + ',\nEnter the following OTP to verify your email address. \nYour verification code is verification code is '+otp+'\nIf you didn’t ask to verify this address, you can ignore this email.\nThanks,\nYour AmplifyTeam'
        subject = 'Email Verification'
        username = 'amplifyteam1234@gmail.com'
        password = '15412342'
        print('i ma in the funtion')
        message = 'Subject: {}\n\n{}'.format(subject, Text)
        message = message.encode()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(fromaddr, toaddrs, message)
        server.quit()
    except firebase_admin._auth_utils.UserNotFoundError as ex:
        from Pages.UserAuthentication.Exceptions import User_not_Found
        User_not_Found()
        return False
    except Exception as ex:
        messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
        
        print('Exception Occurred which is of type :', ex.__class__.__name__)
        y = input('If you want to see Traceback press 1 : ')
        if y == '1':
            traceback.print_exc()
        return False



def verify_email_database(email,entered_otp):
    '''
    Verifies if the OTP is correct 
    Returns bool depending on Success
    '''
    
    from firebase_admin import auth
    user = auth.get_user_by_email(email)
    db_user = get_user_by_email(email)
    if entered_otp == db_user['verification_code']:
        auth.update_user(user.uid, email_verified = True)
        doc_ref = db.collection(u'users').document(user.uid)
        doc_ref.update({
            'email_verified': True
        })
        return True
    else:
        return False

# send_email_verification_otp('dkhoche2000@gmail.com')
def user_create_playlist(uid,playlist_name):
    '''


    :param uid: Unique Identification of the user which is saved in the user file in the root directory
    :param playlist_name: Name of the playlist to be created
    :return: Bool;
    '''
    try:
        collection = db.collection(u'users/'+uid+'/playlists').document(playlist_name)
        collection.set({
            'name':playlist_name
        })
        print('playlist created successfully')
        return True
    except Exception as ex:
        messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
        
        print('Exception Occured which is of type :', ex.__class__.__name__)
        y = input('If you want to see Traceback press 1 : ')
        if y == '1':
            traceback.print_exc()
        return False

# user_create_playlist('1DXAOpIfWdYLylWaGe1Hmm1O6vh2','myplalist')
def add_song_to_playlist(uid,playlist_name,track_name):
    '''

    :param uid: unique identification of the user
    :param playlist_name: name of the particular playlist
    :param track_name: track_title which is to be added
    :return: bool
    '''
    try:
        collection = db.collection(u'users/' + uid + '/playlists/'+playlist_name+'/Tracks').document(track_name)
        track_object = get_track(track_name)
        collection.set(track_object)
        return True
    except Exception as ex:
        messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
        
        print('Exception Occured which is of type :', ex.__class__.__name__)
        y = input('If you want to see Traceback press 1 : ')
        if y == '1':
            traceback.print_exc()
        return False

def get_playlists(uid,**kwargs):
    '''

    :param uid: unique identification of the user
    :param kwargs: playlist = 'required Playlist'
    :return: if mentioned playlist as kwarg then return a list of the all tracks of the particular playlist.
            elseif left no kwarg is passed gives the names aof all the playlist
            else returns false
            If there are no songs then returns a empty list

    '''
    try:
        if 'playlist' in kwargs :
            doc_ref = db.collection(u'users/'+uid+'/playlists/'+kwargs['playlist']+'/Tracks')
            snapshots = list(doc_ref.stream())
            if len(snapshots):
                tracks = list(map(lambda x: x.to_dict(), snapshots))
                return tracks
            return []
        else:
            doc_ref = db.collection(u'users/'+uid+'/playlists').stream()
            object_list = list(map(lambda x: x.to_dict(), doc_ref))
            return object_list
    except Exception as ex:
        messagebox.showerror('Error','Oops!! Something went wrong!!\nTry again later.')
        
        print('Exception Occured which is of type :', ex.__class__.__name__)
        y = input('If you want to see Traceback press 1 : ')
        if y == '1':
            traceback.print_exc()
        return False





# get_playlists('1DXAOpIfWdYLylWaGe1Hmm1O6vh2',playlist = 'myplalist')
