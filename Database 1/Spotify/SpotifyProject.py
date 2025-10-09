from tkinter import messagebox
def insertToUsers():
    try:
        connection = pyodbc.connect('DRIVER={SQL Server};'
                                    r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                    'Database=spotify;'
                                    'Trusted_Connection=True')
        connection.autocommit = True

        cursor = connection.cursor()
        query = "INSERT INTO Users (UserID, UserName, PasswordHash, BirthDate, Email,Locationn ,SubscriptionType) VALUES (?, ?, ?, ?, ?,?, ?)"
        cursor.execute(query, (entry_id.get(), entry_firstName.get(), entry_password.get(), entry_birthDay.get(), entry_email.get(),entry_location.get(), entry_registrationType.get()))

        connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.close()

def fetchSongsFromDbF():
    connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                    r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                    r'Database=spotify;'
                                    r'Trusted_Connection=True')
    cursor = connection.cursor()
    cursor.execute("select * from Songs")
    return cursor


#premium user:

#follower
def fetchFollowers(userID):
    try:
        connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                    r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                    r'Database=spotify;'
                                    r'Trusted_Connection=True')
        cursor = connection.cursor()
        cursor.execute("SELECT u.UserName FROM Users u JOIN FollowList f ON u.UserID = f.FollowerID WHERE f.FollowedID = ?", (userID,))
        followers = cursor.fetchall()
        cursor.close()
        return followers
    except Exception as e:
        print(f"Error fetching followers: {e}")
        return []

def showFollower():
    followers_window = tk.Toplevel()
    followers_window.title("Followers")

    followers_list = tk.Listbox(followers_window, height=10, width=50)
    followers_list.pack(padx=20, pady=20)

    userID = entry_id.get()
    followers = fetchFollowers(userID)
    
    for follower in followers:
        followers_list.insert(tk.END, follower[0])

    # Button to remove selected follower

    # Button to remove selected follower
    def removeFollower():
        selected_index = followers_list.curselection()
        if selected_index:
            follower_name = followers_list.get(selected_index)
            follower_id = getFollowerIDByName(follower_name)  # Example function to get follower ID
            if follower_id:
                if removeFollowerFromDatabase(userID, follower_id):
                    tkinter.messagebox.showinfo("Remove Follower", f"Removed follower: {follower_name}")
                    followers_list.delete(selected_index)
                else:
                    tkinter.messagebox.showerror("Error", "Failed to remove follower")
            else:
                tkinter.messagebox.showerror("Error", "Follower ID not found")

    remove_button = tk.Button(followers_window, text="Remove Follower", command=removeFollower)
    remove_button.pack(pady=10)

    followers_window.mainloop()

def removeFollowerFromDatabase(userID, followerID):
    try:
        connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                    r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                    r'Database=spotify;'
                                    r'Trusted_Connection=True')
        cursor = connection.cursor()
        cursor.execute("DELETE FROM FollowList WHERE FollowedID = ? AND FollowerID = ?", (userID, followerID))
        connection.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"Error removing follower: {e}")
        return False
    finally:
        connection.close()

def getFollowerIDByName(followerName):
    try:
        connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                    r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                    r'Database=spotify;'
                                    r'Trusted_Connection=True')
        cursor = connection.cursor()
        cursor.execute("SELECT UserID FROM Users WHERE UserName = ?", (followerName,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return row[0]
        else:
            return None
    except Exception as e:
        print(f"Error fetching follower ID: {e}")
        return None
    finally:
        connection.close()



#following
def fetchFollowing(userID):
    try:
        connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                    r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                    r'Database=spotify;'
                                    r'Trusted_Connection=True')
        cursor = connection.cursor()
        cursor.execute("SELECT u.UserName, u.UserID FROM Users u JOIN FollowList f ON u.UserID = f.FollowedID WHERE f.FollowerID = ?", (userID,))
        following = cursor.fetchall()
        cursor.close()
        return following
    except Exception as e:
        print(f"Error fetching following: {e}")
        return []

def removeFollowingFromDatabase(userID, followedID):
    try:
        connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                    r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                    r'Database=spotify;'
                                    r'Trusted_Connection=True')
        cursor = connection.cursor()
        cursor.execute("DELETE FROM FollowList WHERE FollowerID = ? AND FollowedID = ?", (userID, followedID))
        connection.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"Error removing following: {e}")
        return False
    finally:
        connection.close()

def fetchLikedOrCommentedSongs(userID):
    try:
        connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                    r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                    r'Database=spotify;'
                                    r'Trusted_Connection=True')
        cursor = connection.cursor()
        
        following = fetchFollowing(userID)
        
        liked_or_commented_songs = {}
        
        for user in following:
            user_name, user_id = user
            
            cursor.execute("""
                SELECT ItemID, 'Liked' AS Action
                FROM spotify.dbo.Likes
                WHERE UserID = ? AND ItemType = 'Song'
            """, (user_id,))
            liked_songs = cursor.fetchall()
            
            cursor.execute("""
                SELECT ItemID, 'Commented' AS Action
                FROM spotify.dbo.Comments
                WHERE UserID = ? AND ItemType = 'Song'
            """, (user_id,))
            commented_songs = cursor.fetchall()
            
            for song in liked_songs:
                song_id = song[0]
                if song_id not in liked_or_commented_songs:
                    liked_or_commented_songs[song_id] = []
                liked_or_commented_songs[song_id].append(f"{user_name} liked")
            
            for song in commented_songs:
                song_id = song[0]
                if song_id not in liked_or_commented_songs:
                    liked_or_commented_songs[song_id] = []
                liked_or_commented_songs[song_id].append(f"{user_name} commented")
        
        cursor.close()
        return liked_or_commented_songs
        
    except Exception as e:
        print(f"Error fetching liked or commented songs: {e}")
        return {}

def showFollowingSongs():
    try:
        userID = int(entry_id.get())
        following_song = tk.Tk()
        following_song.title("Following Songs")
        
        following_list_song = tk.Listbox(following_song, height=10, width=50)
        following_list_song.pack(padx=20, pady=20)
        
        liked_or_commented_songs = fetchLikedOrCommentedSongs(userID)
        
        for song_id, actions in liked_or_commented_songs.items():
            song_info = f"Song ID: {song_id}, Actions: {', '.join(actions)}"
            following_list_song.insert(tk.END, song_info)
        
        following_song.mainloop()
            
    except Exception as e:
        print(f"Error displaying following songs: {e}")

def getUserIDByName(userName):
    try:
        connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                    r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                    r'Database=spotify;'
                                    r'Trusted_Connection=True')
        cursor = connection.cursor()
        cursor.execute("SELECT UserID FROM Users WHERE UserName = ?", (userName,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return row[0]
        else:
            return None
    except Exception as e:
        print(f"Error fetching user ID: {e}")
        return None
    finally:
        connection.close()

def showFollowing():
    following_window = tk.Toplevel()
    following_window.title("Following")

    following_list = tk.Listbox(following_window, height=10, width=50)
    following_list.pack(padx=20, pady=20)

    userID = int(entry_id.get())
    following = fetchFollowing(userID)
    
    for followed_user in following:
        user_name, user_id = followed_user
        following_list.insert(tk.END, user_name)

    def removeFollowing():
        selected_index = following_list.curselection()
        if selected_index:
            following_name = following_list.get(selected_index)
            following_id = getUserIDByName(following_name)
            if following_id:
                if removeFollowingFromDatabase(userID, following_id):
                    tk.messagebox.showinfo("Remove Following", f"Removed following: {following_name}")
                    following_list.delete(selected_index)
                else:
                    tk.messagebox.showerror("Error", "Failed to remove following")
            else:
                tk.messagebox.showerror("Error", "Following ID not found")

    remove_button = tk.Button(following_window, text="Remove Following", command=removeFollowing)
    remove_button.pack(pady=10)
    song_button = tk.Button(following_window, text="Following Songs", command=showFollowingSongs)
    song_button.pack(padx=20, pady=22)




#show songs
def fetchSongsFromDb():
    try:
        connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                    r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                    r'Database=spotify;'
                                    r'Trusted_Connection=True')
        cursor = connection.cursor()
        cursor.execute("SELECT SongID, SongName, ArtistID, AlbumID, Genre, ReleaseDate, Lyrics, IsAddableToPlaylist  FROM Songs WHERE IsAvailble = 1")
        songs = cursor.fetchall()
        cursor.close()
        return songs
    except Exception as e:
        print(f"Error fetching songs: {e}")
        return []
    finally:
        connection.close()

def showLyrics(lyrics):
    lyrics_window = tk.Toplevel()
    lyrics_window.title("Lyrics")
    text_widget = tk.Text(lyrics_window, wrap=tk.WORD)
    text_widget.pack(expand=True, fill='both')
    text_widget.insert(tk.END, lyrics)
    text_widget.config(state=tk.DISABLED)

def commentOnSong(song_id):
    def submitComment():
        comment = comment_entry.get()
        user_id = entry_id.get()  # Assuming you have the user's ID from somewhere
        if comment:
            addCommentToDatabase(user_id, song_id, comment, 'Song')
            comment_window.destroy()

    comment_window = tk.Toplevel()
    comment_window.title("Comment on Song")

    comment_label = tk.Label(comment_window, text="Enter your comment:")
    comment_label.pack(padx=10, pady=10)

    comment_entry = tk.Entry(comment_window, width=50)
    comment_entry.pack(padx=10, pady=10)

    submit_button = tk.Button(comment_window, text="Submit", command=submitComment)
    submit_button.pack(padx=10, pady=10)

def addCommentToDatabase(user_id, song_id, comment_text,type_item):
    try:
        connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                    r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                    r'Database=spotify;'
                                    r'Trusted_Connection=True')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Comments (UserID, ItemID, ItemType, CommentText) VALUES (?, ?, ?, ?)", (user_id, song_id,type_item, comment_text))
        connection.commit()
        cursor.close()
        messagebox.showinfo("Comment", "Comment added successfully!")
    except Exception as e:
        print(f"Error adding comment: {e}")
        messagebox.showerror("Error", "Failed to add comment")
    finally:
        connection.close()

def likeSong(song_id):
    user_id = entry_id.get()  # Assuming you have the user's ID from somewhere
    try:
        connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                    r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                    r'Database=spotify;'
                                    r'Trusted_Connection=True')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Likes (UserID, ItemID, ItemType) VALUES (?, ?, 'Song')", (user_id, song_id))
        connection.commit()
        cursor.close()
        messagebox.showinfo("Like", "Song liked successfully!")
    except Exception as e:
        print(f"Error liking song: {e}")
        messagebox.showerror("Error", "Failed to like song")
    finally:
        connection.close()

def addToFavorites(song_id):
    user_id = entry_id.get()  # Assuming you have the user's ID from somewhere
    try:
        connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                    r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                    r'Database=spotify;'
                                    r'Trusted_Connection=True')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO FavoriteList (UserID, ItemID, ItemType) VALUES (?, ?, 'Song')", (user_id, song_id))
        connection.commit()
        cursor.close()
        messagebox.showinfo("Favorites", "Song added to favorites successfully!")
    except Exception as e:
        print(f"Error adding to favorites: {e}")
        messagebox.showerror("Error", "Failed to add to favorites")
    finally:
        connection.close()

def addToPlaylist(song_id):
    def submitPlaylist():
        playlist_id = playlist_entry.get()
        user_id = entry_id.get()  # Assuming you have the user's ID from somewhere
        if playlist_id:
            addSongToPlaylist(user_id, song_id, playlist_id)
            playlist_window.destroy()

    playlist_window = tk.Toplevel()
    playlist_window.title("Add Song to Playlist")

    playlist_label = tk.Label(playlist_window, text="Enter Playlist ID:")
    playlist_label.pack(padx=10, pady=10)

    playlist_entry = tk.Entry(playlist_window, width=20)
    playlist_entry.pack(padx=10, pady=10)

    submit_button = tk.Button(playlist_window, text="Submit", command=submitPlaylist)
    submit_button.pack(padx=10, pady=10)

def addSongToPlaylist(user_id, song_id, playlist_id):
    try:
        connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                    r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                    r'Database=spotify;'
                                    r'Trusted_Connection=True')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO PlaylistSongs (PlaylistID, SongID) VALUES (?, ?)", (playlist_id, song_id))
        connection.commit()
        cursor.close()
        messagebox.showinfo("Playlist", "Song added to playlist successfully!")
    except Exception as e:
        print(f"Error adding to playlist: {e}")
        messagebox.showerror("Error", "Failed to add to playlist")
    finally:
        connection.close()
  
#end show songs



#start show playlist
def fetchPlaylistsFromDb():
    user_id = entry_id.get()  
    try:
        connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                    r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                    r'Database=spotify;'
                                    r'Trusted_Connection=True')
        cursor = connection.cursor()
        cursor.execute(f'''
        SELECT PlaylistID ,UserID, PlaylistName,IsPublic, CreationDate FROM Playlists WHERE IsPublic = 1 OR UserID={user_id} OR UserID IN
         (
            SELECT DISTINCT 
                CASE 
                    WHEN SenderRequestID = {user_id} THEN ReceiverRequestID
                    WHEN ReceiverRequestID = {user_id}  THEN SenderRequestID
                END AS FriendUserID
            FROM FriendRequests
            WHERE 
                (SenderRequestID = {user_id} OR ReceiverRequestID = {user_id} )
                AND Status = 'Accepted'
                ); ''')
        playlist = cursor.fetchall()
        cursor.close()
        return playlist
    except Exception as e:
        print(f"Error fetching playlist: {e}")
        return []
    finally:
        connection.close()

def commentOnPlaylist(playlist_id):
    def submitComment():
        comment = comment_entry.get()
        user_id = entry_id.get()  # Assuming you have the user's ID from somewhere
        if comment:
            addCommentToDatabase(user_id, playlist_id, comment, 'Playlist')
            comment_window.destroy()

    comment_window = tk.Toplevel()
    comment_window.title("Comment on Playlist")

    comment_label = tk.Label(comment_window, text="Enter your comment:")
    comment_label.pack(padx=10, pady=10)

    comment_entry = tk.Entry(comment_window, width=50)
    comment_entry.pack(padx=10, pady=10)

    submit_button = tk.Button(comment_window, text="Submit", command=submitComment)
    submit_button.pack(padx=10, pady=10)

def likePlaylist(playlist_id):
    user_id = entry_id.get()  # Assuming you have the user's ID from somewhere
    try:
        connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                    r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                    r'Database=spotify;'
                                    r'Trusted_Connection=True')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Likes (UserID, ItemID, ItemType) VALUES (?, ?, 'Playlist')", (user_id, playlist_id))
        connection.commit()
        cursor.close()
        messagebox.showinfo("Like", "Playlist liked successfully!")
    except Exception as e:
        print(f"Error liking song: {e}")
        messagebox.showerror("Error", "Failed to like song")
    finally:
        connection.close()

def addToFavoritesplaylist(playlist_id):
    user_id = entry_id.get()  # Assuming you have the user's ID from somewhere
    try:
        connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                    r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                    r'Database=spotify;'
                                    r'Trusted_Connection=True')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO FavoriteList (UserID, ItemID, ItemType) VALUES (?, ?, 'Playlist')", (user_id, playlist_id))
        connection.commit()
        cursor.close()
        messagebox.showinfo("Favorites", "Playlist added to favorites successfully!")
    except Exception as e:
        print(f"Error adding to favorites: {e}")
        messagebox.showerror("Error", "Failed to add to favorites")
    finally:
        connection.close()

def addTomyPlaylist(playlist_id):
    user_id = entry_id.get()  
    try:
        connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                    r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                    r'Database=spotify;'
                                    r'Trusted_Connection=True')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Playlists (UserID,PlaylistName) VALUES (?, 'playlistbyadded')", (user_id ))
        connection.commit()
        cursor.close()
        messagebox.showinfo("Playlist", "playlist added to my playlist successfully!")
    except Exception as e:
        print(f"Error adding to playlist: {e}")
        messagebox.showerror("Error", "Failed to add to playlist")
    finally:
        connection.close() 
#end show playlist

#start show Album
def fetchAlbumsFromDb():
    try:
        connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                    r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                    r'Database=spotify;'
                                    r'Trusted_Connection=True')
        cursor = connection.cursor()
        cursor.execute("SELECT AlbumID, AlbumName, ArtistID,ReleaseDate FROM Albums")
        albums = cursor.fetchall()
        cursor.close()
        return albums
    except Exception as e:
        print(f"Error fetching albums: {e}")
        return []
    finally:
        connection.close()

def fetchSongsFromAlbum(album_id):
    try:
        connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                    r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                    r'Database=spotify;'
                                    r'Trusted_Connection=True')
        cursor = connection.cursor()
        cursor.execute("SELECT SongID, SongName, ArtistID, AlbumID, Genre, ReleaseDate, Lyrics, IsAddableToPlaylist FROM Songs WHERE IsAvailble = 1 AND AlbumID = ?", (album_id))
        songs = cursor.fetchall()
        cursor.close()
        return songs
    except Exception as e:
        print(f"Error fetching songs: {e}")
        return []
    finally:
        connection.close()

def showSongsOfAlbum(album_id):
    songs_window = tk.Toplevel()
    songs_window.title("Songs of Album")
    songs_window.geometry("1000x1000")

    songs = fetchSongsFromAlbum(album_id)

    for i, song in enumerate(songs):
        song_id = song[0]
        song_name = song[1]
        artist_id = song[2]
        album_id = song[3]
        genre = song[4]
        release_date = song[5]
        lyrics = song[6]
        
        song_label = tk.Label(songs_window, text=f"{song_name} by ArtistID {artist_id}, Genre: {genre}, Released on: {release_date}")
        song_label.grid(row=i, column=0, padx=10, pady=5, sticky='w')

        comment_button = tk.Button(songs_window, text="Comment", command=lambda song_id=song_id: commentOnSong(song_id))
        comment_button.grid(row=i, column=1, padx=5)

        like_button = tk.Button(songs_window, text="Like", command=lambda song_id=song_id: likeSong(song_id))
        like_button.grid(row=i, column=2, padx=5)

        favorite_button = tk.Button(songs_window, text="Add to Favorites", command=lambda song_id=song_id: addToFavorites(song_id))
        favorite_button.grid(row=i, column=3, padx=5)

        playlist_button = tk.Button(songs_window, text="Add to Playlist", command=lambda song_id=song_id: addToPlaylist(song_id))
        playlist_button.grid(row=i, column=4, padx=5)



        lyrics_button = tk.Button(songs_window, text="Lyrics", command=lambda s=lyrics: showLyrics(s))
        lyrics_button.grid(row=i, column=5, padx=5)

    songs_window.mainloop()

def commentOnAlbum(album_id):
    def submitComment():
        comment = comment_entry.get()
        user_id = entry_id.get()  # Assuming you have the user's ID from somewhere
        if comment:
            addCommentToDatabase(user_id, album_id, comment,'Album')
            comment_window.destroy()

    comment_window = tk.Toplevel()
    comment_window.title("Comment on Album")

    comment_label = tk.Label(comment_window, text="Enter your comment:")
    comment_label.pack(padx=10, pady=10)

    comment_entry = tk.Entry(comment_window, width=50)
    comment_entry.pack(padx=10, pady=10)

    submit_button = tk.Button(comment_window, text="Submit", command=submitComment)
    submit_button.pack(padx=10, pady=10)

def likeAlbum(album_id):
    user_id = entry_id.get()  # Assuming you have the user's ID from somewhere
    try:
        connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                    r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                    r'Database=spotify;'
                                    r'Trusted_Connection=True')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Likes (UserID, ItemID, ItemType) VALUES (?, ?, 'Album')", (user_id, album_id))
        connection.commit()
        cursor.close()
        messagebox.showinfo("Like", "Album liked successfully!")
    except Exception as e:
        print(f"Error liking album: {e}")
        messagebox.showerror("Error", "Failed to like album")
    finally:
        connection.close()
# end show album 

#show favorite list 
def fetchfavoritelist():
    user_id = entry_id.get()  
    try:
        connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                    r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                    r'Database=spotify;'
                                    r'Trusted_Connection=True')
        cursor = connection.cursor()
        cursor.execute("SELECT ItemID, ItemType FROM FavoriteList WHERE UserID = ?", (user_id))
        favorite = cursor.fetchall()
        cursor.close()
        return favorite
    except Exception as e:
        print(f"Error fetching favorite: {e}")
        return []    
#end show favorite list 

#show suggestions list 
def fetchsuggestionslist():
    user_id = entry_id.get()  
    try:
        connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                    r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                    r'Database=spotify;'
                                    r'Trusted_Connection=True')
        cursor = connection.cursor()
        cursor.execute('''
            SELECT s.SongName, a.AlbumName, a.ReleaseDate
            FROM Songs s JOIN Albums a ON s.AlbumID = a.AlbumID
            WHERE s.Genre IN (
                SELECT Genre FROM Songs
                WHERE SongID IN ( SELECT ItemID FROM Likes WHERE UserID = ? AND ItemType = 'Song'))
            ORDER BY s.ReleaseDate DESC;
        '''
        , (user_id))
        suggestion = cursor.fetchall()
        cursor.close()
        return suggestion
    except Exception as e:
        print(f"Error fetching suggestion: {e}")
        return []    
#end show suggestions list 




def premiumUserMainWindow():
    premiumMainwindow= tkinter.Tk()
    premiumMainwindow.geometry("800x800")
    premiumMainwindow.title(f'{entry_firstName.get()}')

    # Create a frame to hold the buttons
    button_frame = tkinter.Frame(premiumMainwindow)
    button_frame.pack(side=tkinter.TOP, pady=10)

    Followerbutton = tkinter.Button(button_frame, text="Follower", command=showFollower)
    Followerbutton.grid(row=0, column=0, padx=5)
    Followingbutton = tkinter.Button(button_frame, text="Following", command=showFollowing)
    Followingbutton.grid(row=0, column=1, padx=5)
    # Friendsbutton = tkinter.Button(button_frame, text="Friends", command=showFriends)
    # Friendsbutton.grid(row=0, column=2, padx=5)

    # Add search bar and button
    search_frame = tkinter.Frame(premiumMainwindow)
    search_frame.pack(side=tkinter.TOP, pady=10)
    search_entry = tkinter.Entry(search_frame, font=("Arial", 14), bd=2, relief=tkinter.GROOVE, justify=tkinter.LEFT)
    search_entry.grid(row=0, column=0, padx=5)

    def performSearch():
        search_term = search_entry.get()
        # results = searchUsers(search_term)
        # result_text_widget.delete('1.0', tk.END)
        # for user in results:
        #     result_text_widget.insert(tk.END, f"{user[0]} {user[1]} {user[2]} {user[3]} {user[4]} {user[5]} {user[6]}\n")

    search_button = tkinter.Button(search_frame, text="Search", command=performSearch)
    search_button.grid(row=0, column=1, padx=5)

    # # Add a text widget to display search results
    # result_text_widget = tk.Text(premiumMainwindow, font=("Arial", 12))
    # result_text_widget.pack(expand=True, fill='both')


    def openSongsWindow():
        songs_window = tk.Toplevel()
        songs_window.title("Songs")
        songs_window.geometry("1300x1300")

        songs = fetchSongsFromDb()

        for i, song in enumerate(songs):
            song_id = song[0]
            song_name = song[1]
            artist_id = song[2]
            album_id = song[3]
            genre = song[4]
            release_date = song[5]
            lyrics = song[6]
            addable = song[7]

            song_label = tk.Label(songs_window, text=f"{song_name} by ArtistID {artist_id} from AlbumID {album_id}, Genre: {genre}, Released on: {release_date}")
            song_label.grid(row=i, column=0, padx=10, pady=5, sticky='w')


            comment_button = tk.Button(songs_window, text="Comment", command=lambda song_id=song_id: commentOnSong(song_id))
            comment_button.grid(row=i, column=1, padx=5)

            like_button = tk.Button(songs_window, text="Like", command=lambda song_id=song_id: likeSong(song_id))
            like_button.grid(row=i, column=2, padx=5)

            favorite_button = tk.Button(songs_window, text="Add to Favorites", command=lambda song_id=song_id: addToFavorites(song_id))
            favorite_button.grid(row=i, column=3, padx=5)

            if (addable==1):
                playlist_button = tk.Button(songs_window, text="Add to Playlist", command=lambda song_id=song_id: addToPlaylist(song_id))
                playlist_button.grid(row=i, column=4, padx=5)

            lyrics_button = tk.Button(songs_window, text="Lyrics", command=lambda s=lyrics: showLyrics(s))
            lyrics_button.grid(row=i, column=5, padx=5)


        #start of search a song
        search_frame = tkinter.Frame(songs_window)
        search_frame.grid(row=i+4,  padx=5)
        search_entry = tkinter.Entry(search_frame, font=("Arial", 14), bd=2, relief=tkinter.GROOVE, justify=tkinter.LEFT)
        search_entry.grid(row=i+4, column=0, padx=5)


        def searchSongs(search_term):
            try:
                connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                            r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                            r'Database=spotify;'
                                            r'Trusted_Connection=True')
                cursor = connection.cursor()
                query = '''
                SELECT SongID, SongName, ArtistID, AlbumID, Genre, ReleaseDate, Lyrics
                FROM Songs
                WHERE IsAvailble = 1
                AND (SongName LIKE ? OR ArtistID LIKE ? OR AlbumID LIKE ? OR Genre LIKE ?)
                '''
                search_term = f"%{search_term}%"
                cursor.execute(query, (search_term, search_term, search_term, search_term))
                songs = cursor.fetchall()
                cursor.close()
                return songs
            except Exception as e:
                print(f"Error fetching songs: {e}")
                return []
            finally:
                connection.close()        

        def performSearchsong():
            search_term = search_entry.get()
            results = searchSongs(search_term)
            result_text_widget.delete('1.0', tk.END)
            for song in results:
                result_text_widget.insert(tk.END, f"{song[0]} {song[1]} {song[2]} {song[3]} {song[4]} {song[5]} {song[6]}\n")

        search_button = tkinter.Button(search_frame, text="Search", command=performSearchsong)
        search_button.grid(row=i+4, column=1, padx=5)

        # Add a text widget to display search results
        result_text_widget = tk.Text(songs_window, font=("Arial", 12))
        result_text_widget.grid(row=i+5, column=0, padx=5)

        #end of search a song

        songs_window.mainloop()        
            

    def openAlbumsWindow():
        albums_window = tk.Toplevel()
        albums_window.title("Albums")
        albums_window.geometry("1000x1000")

        albums = fetchAlbumsFromDb()
        m = 0
        for i, album in enumerate(albums):
            album_id = album[0]
            album_name = album[1]
            artist_id = album[2]
            release_date = album[3]

            album_label = tk.Label(albums_window, text=f"{album_name} by ArtistID {artist_id},  Released on: {release_date}")
            album_label.grid(row=i, column=0, padx=10, pady=5, sticky='w')

            comment_button = tk.Button(albums_window, text="Comment", command=lambda album_id=album_id: commentOnAlbum(album_id))
            comment_button.grid(row=i, column=1, padx=5)

            like_button = tk.Button(albums_window, text="Like", command=lambda album_id=album_id: likeAlbum(album_id))
            like_button.grid(row=i, column=2, padx=5)

            show_songs_button = tk.Button(albums_window, text="Show Songs", command=lambda album_id=album_id: showSongsOfAlbum(album_id))
            show_songs_button.grid(row=i, column=3, padx=5)
            m=i
        # Search functionality for albums
        i = m
        search_frame = tk.Frame(albums_window)
        search_frame.grid(row=i+1, padx=5)
        search_entry = tk.Entry(search_frame, font=("Arial", 14), bd=2, relief=tk.GROOVE, justify=tk.LEFT)
        search_entry.grid(row=0, column=0, padx=5)

        def searchAlbums(search_term):
            try:
                connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                            r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                            r'Database=spotify;'
                                            r'Trusted_Connection=True')
                cursor = connection.cursor()
                query = '''
                SELECT AlbumID, AlbumName, ArtistID, ReleaseDate
                FROM Albums
                WHERE (AlbumName LIKE ? OR ArtistID LIKE ?)
                '''
                search_term = f"%{search_term}%"
                cursor.execute(query, (search_term, search_term))
                albums = cursor.fetchall()
                cursor.close()
                return albums
            except Exception as e:
                print(f"Error fetching albums: {e}")
                return []
            finally:
                connection.close()        

        def performSearchAlbum():
            search_term = search_entry.get()
            results = searchAlbums(search_term)
            result_text_widget.delete('1.0', tk.END)
            for album in results:
                result_text_widget.insert(tk.END, f"{album[0]} {album[1]} {album[2]} {album[3]}\n")

        search_button = tk.Button(search_frame, text="Search", command=performSearchAlbum)
        search_button.grid(row=0, column=1, padx=5)

        result_text_widget = tk.Text(albums_window, font=("Arial", 12))
        result_text_widget.grid(row=i+2, column=0, columnspan=5, padx=5)

        albums_window.mainloop()


    def openPlaylistsWindow():
        playlist_window = tk.Toplevel()
        playlist_window.title("PlayLists")
        playlist_window.geometry("1300x1300")

        playlists = fetchPlaylistsFromDb()

        m=0
        for i, playlist in enumerate(playlists):
            playlist_id = playlist[0]
            user_id = playlist[1]
            playlist_name = playlist[2]
            is_publick = playlist[3]
            creation_date = playlist[4]


            playlist_label = tk.Label(playlist_window, text=f"{playlist_name} by UserID {user_id}")
            playlist_label.grid(row=i, column=0, padx=10, pady=5, sticky='w')


            comment_button = tk.Button(playlist_window, text="Comment", command=lambda playlist_id=playlist_id: commentOnPlaylist(playlist_id))
            comment_button.grid(row=i, column=1, padx=5)

            like_button = tk.Button(playlist_window, text="Like", command=lambda playlist_id=playlist_id: likePlaylist(playlist_id))
            like_button.grid(row=i, column=2, padx=5)

            favorite_button = tk.Button(playlist_window, text="Add to Favorites", command=lambda playlist_id=playlist_id: addToFavoritesplaylist(playlist_id))
            favorite_button.grid(row=i, column=3, padx=5)

            playlist_button = tk.Button(playlist_window, text="Add to Playlist", command=lambda playlist_id=playlist_id: addTomyPlaylist(playlist_id))
            playlist_button.grid(row=i, column=4, padx=5)
            m=i

        #start of search a song
        i=m
        search_frame = tkinter.Frame(playlist_window)
        search_frame.grid(row=i+4,  padx=5)
        search_entry = tkinter.Entry(search_frame, font=("Arial", 14), bd=2, relief=tkinter.GROOVE, justify=tkinter.LEFT)
        search_entry.grid(row=i+4, column=0, padx=5)


        def searchPlaylists(search_term):
            try:
                connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                            r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                            r'Database=spotify;'
                                            r'Trusted_Connection=True')
                cursor = connection.cursor()
                query = '''
                SELECT PlaylistID, PlaylistName, UserID, CreationDate
                FROM Playlists
                WHERE IsPublic = 1
                AND (PlaylistID LIKE ? OR PlaylistName LIKE ? OR UserID LIKE ?)
                '''
                search_term = f"%{search_term}%"
                cursor.execute(query, (search_term, search_term, search_term))
                playlists = cursor.fetchall()
                cursor.close()
                return playlists
            except Exception as e:
                print(f"Error fetching playlist: {e}")
                return []
            finally:
                connection.close()        

        def performSearchplaylist():
            search_term = search_entry.get()
            results = searchPlaylists(search_term)
            result_text_widget.delete('1.0', tk.END)
            for playlist in results:
                result_text_widget.insert(tk.END, f"{playlist[0]} {playlist[1]} {playlist[2]} \n")

        search_button = tkinter.Button(search_frame, text="Search", command=performSearchplaylist)
        search_button.grid(row=i+4, column=1, padx=5)

        # Add a text widget to display search results
        result_text_widget = tk.Text(playlist_window, font=("Arial", 12))
        result_text_widget.grid(row=i+5, column=0, padx=5)

        #end of search a song

        playlist_window.mainloop()        


    def openMyFavoriteWindow():
        my_favorite_window = tkinter.Toplevel(premiumMainwindow)
        my_favorite_window.title("My Favorite")
        favoritelist = fetchfavoritelist()
        for i, favorite in enumerate(favoritelist):
            Item_ID = favorite[0]
            Item_Type = favorite[1]

            favorite_label = tk.Label(my_favorite_window, text=f"{Item_Type} by Item ID: {Item_ID} ")
            favorite_label.grid(row=i, column=0, padx=10, pady=5, sticky='w')


    def openWalletWindow():     
        def cashWithdrawal():
            connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                            r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                            r'Database=spotify;'
                                            r'Trusted_Connection=True')
            cursor = connection.cursor()
            query="UPDATE Wallet SET Balance = Balance + ? WHERE UserID = ?"
            cursor.execute(query,entry_amount.get(),entry_id.get())
            connection.commit()
            cursor.close() 

        transactionToPayPremium=tkinter.Tk()
        transactionToPayPremium.geometry("500x700")
        transactionToPayPremium.title('Pay For Premium')
        pay_label=tkinter.Label(transactionToPayPremium,text="Enter your ID and Transaction Amount")
        pay_label.config(font=("Courier",14))
        pay_label.pack()

        entry_amount = tkinter.Entry(transactionToPayPremium, font=("Arial", 14), bd=2, relief=tkinter.GROOVE, justify=tkinter.LEFT)
        entry_amount.insert(0, "Transaction Amount")
        entry_amount.place(relx=0.2, rely=0.2, relwidth=0.6)

        pay_button=tkinter.Button(transactionToPayPremium,text="Insert",command=cashWithdrawal)
        pay_button.place(relx=0.2,rely=0.3,relwidth=0.6)
        transactionToPayPremium.mainloop() 

    def openSuggestionListWindow():
        suggestion_list_window = tkinter.Toplevel(premiumMainwindow)
        suggestion_list_window.title("Suggestion List")
        suggestions = fetchsuggestionslist()
        for i, suggestion in enumerate(suggestions):
            SongName = suggestion[0]
            AlbumName = suggestion[1]
            ReleaseDate = suggestion[2]

            suggestion_label = tk.Label(suggestion_list_window, text=f"song : {SongName} in Album: {AlbumName} release date: {ReleaseDate} ")
            suggestion_label.grid(row=i, column=0, padx=10, pady=5, sticky='w')




    
    def friendShipRequests():
        def InsertToFreindRequest():
            connection = pyodbc.connect('DRIVER={SQL Server};'
                                    r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                    'Database=spotify;'
                                    'Trusted_Connection=True')
            connection.autocommit = True

            cursor = connection.cursor()
            query = "INSERT INTO  FriendRequests ( SenderRequestID, ReceiverRequestID, Status) VALUES (?, ?, ?)"
            cursor.execute(query, (int(entry_id.get()), entry_ReciverId.get(), 'Pending'))
            #cursor.execute("updateWallet")
            connection.commit()
            cursor.close()

        friendShipRequestWindow=tkinter.Tk()
        friendShipRequestWindow.geometry("200x400")
        friendShipRequestWindow.title('Request')

        entry_ReciverId = tkinter.Entry(friendShipRequestWindow, font=("Arial", 14), bd=2, relief=tkinter.GROOVE, justify=tkinter.LEFT)
        entry_ReciverId.insert(0, "Your Friend's ID")
        entry_ReciverId.place(relx=0.2, rely=0.1, relwidth=0.6)

        display_button=tkinter.Button(friendShipRequestWindow,text="Request",command=InsertToFreindRequest)
        display_button.place(relx=0.2,rely=0.2,relwidth=0.6)    
        friendShipRequestWindow.mainloop()
   
    def ShowRequestTable():
        def ShowFreindRequest():
            connection = pyodbc.connect('DRIVER={SQL Server};'
                                    r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                    'Database=spotify;'
                                    'Trusted_Connection=True')
            connection.autocommit = True
            cursor = connection.cursor()
            query="select * from FriendRequests where ReceiverRequestID=? and Status=?"
            cursor.execute(query,(int(entry_id.get()),'Pending'))
            i=0
            for request in cursor:
                for j in range(len(request)):
                    e= tkinter.Label(whoRequested,width=8,fg='blue',text=request[j],
                         relief='ridge',anchor="w")
                    e.grid(row=i,column=j)
                i=i+1
            connection.commit()
            cursor.close()
        def acceptOrRejectt():
            try:
                connection = pyodbc.connect('DRIVER={SQL Server};'
                                        r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                        'Database=spotify;'
                                        'Trusted_Connection=True')
                connection.autocommit = True
                cursor = connection.cursor()
                query="update FriendRequests set Status=? where ReceiverRequestID=? and SenderRequestID=? and Status=?"
                cursor.execute(query,(entry_status.get(),int(entry_id.get()) ,entry_idd.get(),'Pending'))
                if(entry_status.get()=='Accepted'):
                    cursor.execute("updateFollowList")
                
            except Exception as e:
                print(f"Error updating friend request: {e}")
            finally:
                cursor.close()
                connection.close()
            
        whoRequested=tkinter.Tk()
        whoRequested.geometry("200x400")
        whoRequested.title('Who Requested To Me')

        display_button=tkinter.Button(whoRequested,text="Show",command=ShowFreindRequest)
        display_button.place(relx=0.2,rely=0.2,relwidth=0.6)  
              
        entry_idd = tkinter.Entry(whoRequested, font=("Arial", 14), bd=2, relief=tkinter.GROOVE, justify=tkinter.LEFT)
        entry_idd.insert(0, "ID that you want to accept")
        entry_idd.place(relx=0.2, rely=0.7, relwidth=0.6)

        entry_status = tkinter.Entry(whoRequested, font=("Arial", 14), bd=2, relief=tkinter.GROOVE, justify=tkinter.LEFT)
        entry_status.insert(0, "Accepted,Rejected")
        entry_status.place(relx=0.2, rely=0.8, relwidth=0.6)

        display_button=tkinter.Button(whoRequested,text="Set",command=acceptOrRejectt)
        display_button.place(relx=0.2,rely=0.9,relwidth=0.6)     

        whoRequested.mainloop()
    
    def messageing():
        def messageingToYourFolwing():
            try:
                connection = pyodbc.connect('DRIVER={SQL Server};'
                                        r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                        'Database=spotify;'
                                        'Trusted_Connection=True')
                connection.autocommit = True
                cursor = connection.cursor()
                sender_id = int(entry_id.get())
                receiver_id = int(entry_idRecive.get())
                message_text = entry_txt.get()

                    # Check if there is an accepted friend request between sender and receiver
                query_check_request = """
                    SELECT 1
                    FROM spotify.dbo.FriendRequests
                    WHERE SenderRequestID = ?
                        AND ReceiverRequestID = ?
                        AND Status = 'Accepted';
                """
                cursor.execute(query_check_request, (sender_id, receiver_id))
                if not cursor.fetchone():
                    messagebox.showwarning("Error", "No accepted friend request found between these users.")
                    return
                
                # Insert the message into MessageList table
                query_insert_message = """
                    INSERT INTO spotify.dbo.MessageList (SenderID, ReceiverID, MessageText)
                    VALUES (?, ?, ?);
                """
                cursor.execute(query_insert_message, (sender_id, receiver_id, message_text))
                
                messagebox.showinfo("Success", "Message sent successfully!")
                
            except Exception as e:
                print(f"Error : {e}")
            finally:
                cursor.close()
                connection.close()

        messageTo=tkinter.Tk()
        messageTo.geometry("300x400")
        messageTo.title('send Messeage to your following')    

        entry_idRecive = tkinter.Entry(messageTo, font=("Arial", 14), bd=2, relief=tkinter.GROOVE, justify=tkinter.LEFT)
        entry_idRecive.insert(0, "Yor friend's Id")
        entry_idRecive.place(relx=0.2, rely=0.3, relwidth=0.6)

        entry_txt = tkinter.Entry(messageTo, font=("Arial", 14), bd=2, relief=tkinter.GROOVE, justify=tkinter.LEFT)
        entry_txt.insert(0, "text")
        entry_txt.place(relx=0.2, rely=0.4, relwidth=0.6)

        send_button=tkinter.Button(messageTo,text="Set",command=messageingToYourFolwing)
        send_button.place(relx=0.2,rely=0.5,relwidth=0.6)     
        messageTo.mainloop()

    def showRejectAndAccepted():
        def showAcc():
            connection = pyodbc.connect('DRIVER={SQL Server};'
                                    r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                    'Database=spotify;'
                                    'Trusted_Connection=True')
            connection.autocommit = True
            cursor = connection.cursor()
            query="select * from FriendRequests where ReceiverRequestID=? and Status=?"
            cursor.execute(query,int(entry_id.get()),'Accepted')
            i=0
            for request in cursor:
                for j in range(len(request)):
                    e= tkinter.Label(ShowRejAndAcc,width=8,fg='blue',text=request[j],
                        relief='ridge',anchor="w")
                    e.grid(row=i,column=j)
                i=i+1
            connection.commit()
            cursor.close()
        def showRej():
            connection = pyodbc.connect('DRIVER={SQL Server};'
                                    r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                    'Database=spotify;'
                                    'Trusted_Connection=True')
            connection.autocommit = True
            cursor = connection.cursor()
            query="select * from FriendRequests where ReceiverRequestID=? and Status=?"
            cursor.execute(query,int(entry_id.get()),'Rejected')
            i=0
            for request in cursor:
                for j in range(len(request)):
                    e= tkinter.Label(ShowRejAndAcc,width=8,fg='blue',text=request[j],
                        relief='ridge',anchor="w")
                    e.grid(row=i,column=j)
                i=i+1
            connection.commit()
            cursor.close()
        ShowRejAndAcc=tkinter.Tk()
        ShowRejAndAcc.geometry("300x400")
        ShowRejAndAcc.title('Rejected and Accepted people')  

        send_buttonAccept=tkinter.Button(ShowRejAndAcc,text="accepted",command=showAcc)
        send_buttonAccept.place(relx=0.2,rely=0.3,relwidth=0.6)
        send_buttonReiect=tkinter.Button(ShowRejAndAcc,text="rejected",command=showRej)
        send_buttonReiect.place(relx=0.2,rely=0.4,relwidth=0.6)     
        ShowRejAndAcc.mainloop()

    def showConcerts():
        def show():
            connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                r'Database=spotify;'
                                r'Trusted_Connection=True')
            cursor = connection.cursor()
    
            # Execute the query to fetch concerts
            query = "SELECT * FROM Concerts"
            cursor.execute(query)
            concerts = cursor.fetchall()
    
            # Clear any previous content in the main_frame
            for widget in main_frame.winfo_children():
                widget.destroy()
            
            # Display the column headers
            headers = ["ConcertID", "ArtistID", "Title", "NumberOfTickets", "Date", "Price", "IsCancelled"]
            for j, header in enumerate(headers):
                e = tk.Label(main_frame, width=15, fg='black', text=header, relief='ridge', anchor='w')
                e.grid(row=0, column=j)
            
            # Display the concert data
            for i, concert in enumerate(concerts, start=1):
                for j, value in enumerate(concert):
                    e = tk.Label(main_frame, width=15, fg='blue', text=value, relief='ridge', anchor='w')
                    e.grid(row=i, column=j)
            
            # Close the connection
            connection.close()

        def purchase_ticket():
            try:
                connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                                        r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                                        r'Database=spotify;'
                                                        r'Trusted_Connection=True')
                cursor = connection.cursor()
                user_id = int(entry_id.get())
                concert_id = int(entry_concertID.get())
            
            # Check if concert is cancelled or sold out
                cursor.execute("""
                    SELECT NumberOfTkickets, Price, IsCancelled , Date
                    FROM spotify.dbo.Concerts 
                    WHERE ConcertID = ?
                """, (concert_id,))
                concert = cursor.fetchone()
            
                if not concert:
                    messagebox.showerror("Error", "Concert not found")
                    return
                
                number_of_tickets, price, is_cancelled ,DateConcert= concert
            
                if is_cancelled:
                    messagebox.showerror("Error", "Concert is cancelled")
                    return
                
                if number_of_tickets == 0:
                    messagebox.showerror("Error", "Concert is sold out")
                    return
            
                # Check if user has sufficient balance
                cursor.execute("""
                    SELECT Balance 
                    FROM spotify.dbo.Wallet 
                    WHERE UserID = ?
                """, (user_id,))
                wallet = cursor.fetchone()
                
                if not wallet:
                    messagebox.showerror("Error", "User not found")
                    return
                
                balance = wallet[0]
                
                if balance < price:
                    messagebox.showerror("Error", "Insufficient balance")
                    return
            
                # Update the Tickets table
                cursor.execute("""
                    INSERT INTO Tickets (UserID, ConcertID, ExpiryDate) 
                    VALUES (?, ?,?)
                """, (user_id, concert_id,DateConcert))
            
                # Update the Wallet table
                cursor.execute("""
                    UPDATE Wallet 
                    SET Balance = Balance - ? 
                    WHERE UserID = ?
                """, (price, user_id))
                
                # Update the Concerts table
                cursor.execute("""
                    UPDATE Concerts 
                    SET NumberOfTkickets = NumberOfTkickets - 1 
                    WHERE ConcertID = ?
                """, (concert_id,))
        
                messagebox.showinfo("Success", "Ticket purchased successfully")
    
            except pyodbc.Error as e:
                messagebox.showerror("Database Error", str(e))
    
            finally:
                connection.commit()
                cursor.close()



        ShowConcert_wind=tkinter.Tk()
        ShowConcert_wind.geometry("900x400")
        ShowConcert_wind.title('Concerts')  
        main_frame = tk.Frame(ShowConcert_wind)
        main_frame.pack(pady=20)

        show_concert=tkinter.Button(ShowConcert_wind,text="show",command=show)
        show_concert.place(relx=0.2,rely=0.7,relwidth=0.6)
        entry_concertID = tkinter.Entry(ShowConcert_wind, font=("Arial", 14), bd=2, relief=tkinter.GROOVE, justify=tkinter.LEFT)
        entry_concertID.insert(0, "Which concert do you want to attend?")
        entry_concertID.place(relx=0.2, rely=0.8, relwidth=0.6)
        buy_ticket=tkinter.Button(ShowConcert_wind,text="buy",command=purchase_ticket)
        buy_ticket.place(relx=0.2,rely=0.9,relwidth=0.6)

        ShowConcert_wind.mainloop()
    def showTickets():
        def showNotExpiredTick():
            connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                r'Database=spotify;'
                                r'Trusted_Connection=True')
            cursor = connection.cursor()
    
            # Execute the query to fetch concerts
            query = '''SELECT ConcertID,PurchaseDate,ExpiryDate FROM Tickets
                     where UserID=? and IsExpired=0 '''
            cursor.execute(query,(int(entry_id.get())))
            tickets = cursor.fetchall()
    
            # Clear any previous content in the main_frame
            for widget in main_frame.winfo_children():
                widget.destroy()
            
            # Display the column headers
            headers = ["ConcertID", "PurchaseDate", "ExpiryDate"]
            for j, header in enumerate(headers):
                e = tk.Label(main_frame, width=15, fg='black', text=header, relief='ridge', anchor='w')
                e.grid(row=0, column=j)
            # Display the concert data
            for i, concert in enumerate(tickets, start=1):
                for j, value in enumerate(concert):
                    e = tk.Label(main_frame, width=15, fg='blue', text=value, relief='ridge', anchor='w')
                    e.grid(row=i, column=j)
            connection.close()
        def showExpiredTick():
            connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                r'Database=spotify;'
                                r'Trusted_Connection=True')
            cursor = connection.cursor()
    
            # Execute the query to fetch concerts
            query = '''SELECT ConcertID,PurchaseDate,ExpiryDate FROM Tickets
                     where UserID=? and IsExpired=1 '''
            cursor.execute(query,(int(entry_id.get())))
            tickets = cursor.fetchall()
    
            # Clear any previous content in the main_frame
            for widget in main_frame.winfo_children():
                widget.destroy()
            
            # Display the column headers
            headers = ["ConcertID", "PurchaseDate", "ExpiryDate"]
            for j, header in enumerate(headers):
                e = tk.Label(main_frame, width=15, fg='black', text=header, relief='ridge', anchor='w')
                e.grid(row=0, column=j)
            # Display the concert data
            for i, concert in enumerate(tickets, start=1):
                for j, value in enumerate(concert):
                    e = tk.Label(main_frame, width=15, fg='blue', text=value, relief='ridge', anchor='w')
                    e.grid(row=i, column=j)
            connection.close()
        ShowTicket_wind=tkinter.Tk()
        ShowTicket_wind.geometry("300x400")
        ShowTicket_wind.title('Ticketss')  
        main_frame = tk.Frame(ShowTicket_wind)
        main_frame.pack(pady=20)
        show_notTicket=tkinter.Button(ShowTicket_wind,text="show Not Expired",command=showNotExpiredTick)
        show_notTicket.place(relx=0.2,rely=0.5,relwidth=0.6)
        show_ticket=tkinter.Button(ShowTicket_wind,text="show Expired",command=showExpiredTick)
        show_ticket.place(relx=0.2,rely=0.6,relwidth=0.6)


    button_frame = tkinter.Frame(premiumMainwindow)
    button_frame.pack(side=tkinter.TOP, pady=10)
    buttons_data = [
        ("Songs", openSongsWindow),
        ("Albums", openAlbumsWindow),
        ("Playlists", openPlaylistsWindow),
        ("My Favorite", openMyFavoriteWindow),
        ("Wallet", openWalletWindow),
        ("Suggestion List", openSuggestionListWindow),
        ("My Requests",friendShipRequests),
        ("Who Requestedto To Me",ShowRequestTable),
        ("message to folowing",messageing),
        ("Who I rejected and accepted",showRejectAndAccepted),
        ("Concerts",showConcerts),
        ("My Tickets",showTickets),
    ]

    columns = 4 
    for index, (text, command) in enumerate(buttons_data): 
        row = index // columns 
        column = index % columns 
        button = tk.Button(button_frame, text=text, command=command) 
        button.grid(row=row, column=column, padx=5, pady=5)



    premiumMainwindow.mainloop()


#end premium


def ArtistMainWindow():
    premiumMainwindow= tkinter.Tk()
    premiumMainwindow.geometry("800x800")
    premiumMainwindow.title(f'{entry_firstName.get()}')

    # Create a frame to hold the buttons
    button_frame = tkinter.Frame(premiumMainwindow)
    button_frame.pack(side=tkinter.TOP, pady=10)

    Followerbutton = tkinter.Button(button_frame, text="Follower", command=showFollower)
    Followerbutton.grid(row=0, column=0, padx=5)
    Followingbutton = tkinter.Button(button_frame, text="Following", command=showFollowing)
    Followingbutton.grid(row=0, column=1, padx=5)
    # Friendsbutton = tkinter.Button(button_frame, text="Friends", command=showFriends)
    # Friendsbutton.grid(row=0, column=2, padx=5)

    # Add search bar and button
    search_frame = tkinter.Frame(premiumMainwindow)
    search_frame.pack(side=tkinter.TOP, pady=10)
    search_entry = tkinter.Entry(search_frame, font=("Arial", 14), bd=2, relief=tkinter.GROOVE, justify=tkinter.LEFT)
    search_entry.grid(row=0, column=0, padx=5)

    def performSearch():
        search_term = search_entry.get()
        # results = searchUsers(search_term)
        # result_text_widget.delete('1.0', tk.END)
        # for user in results:
        #     result_text_widget.insert(tk.END, f"{user[0]} {user[1]} {user[2]} {user[3]} {user[4]} {user[5]} {user[6]}\n")

    search_button = tkinter.Button(search_frame, text="Search", command=performSearch)
    search_button.grid(row=0, column=1, padx=5)

    # # Add a text widget to display search results
    # result_text_widget = tk.Text(premiumMainwindow, font=("Arial", 12))
    # result_text_widget.pack(expand=True, fill='both')


    def openSongsWindow():
        songs_window = tk.Toplevel()
        songs_window.title("Songs")
        songs_window.geometry("1300x1300")

        songs = fetchSongsFromDb()

        for i, song in enumerate(songs):
            song_id = song[0]
            song_name = song[1]
            artist_id = song[2]
            album_id = song[3]
            genre = song[4]
            release_date = song[5]
            lyrics = song[6]
            addable = song[7]

            song_label = tk.Label(songs_window, text=f"{song_name} by ArtistID {artist_id} from AlbumID {album_id}, Genre: {genre}, Released on: {release_date}")
            song_label.grid(row=i, column=0, padx=10, pady=5, sticky='w')


            comment_button = tk.Button(songs_window, text="Comment", command=lambda song_id=song_id: commentOnSong(song_id))
            comment_button.grid(row=i, column=1, padx=5)

            like_button = tk.Button(songs_window, text="Like", command=lambda song_id=song_id: likeSong(song_id))
            like_button.grid(row=i, column=2, padx=5)

            favorite_button = tk.Button(songs_window, text="Add to Favorites", command=lambda song_id=song_id: addToFavorites(song_id))
            favorite_button.grid(row=i, column=3, padx=5)

            if (addable==1):
                playlist_button = tk.Button(songs_window, text="Add to Playlist", command=lambda song_id=song_id: addToPlaylist(song_id))
                playlist_button.grid(row=i, column=4, padx=5)

            lyrics_button = tk.Button(songs_window, text="Lyrics", command=lambda s=lyrics: showLyrics(s))
            lyrics_button.grid(row=i, column=5, padx=5)


        #start of search a song
        search_frame = tkinter.Frame(songs_window)
        search_frame.grid(row=i+4,  padx=5)
        search_entry = tkinter.Entry(search_frame, font=("Arial", 14), bd=2, relief=tkinter.GROOVE, justify=tkinter.LEFT)
        search_entry.grid(row=i+4, column=0, padx=5)


        def searchSongs(search_term):
            try:
                connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                            r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                            r'Database=spotify;'
                                            r'Trusted_Connection=True')
                cursor = connection.cursor()
                query = '''
                SELECT SongID, SongName, ArtistID, AlbumID, Genre, ReleaseDate, Lyrics
                FROM Songs
                WHERE IsAvailble = 1
                AND (SongName LIKE ? OR ArtistID LIKE ? OR AlbumID LIKE ? OR Genre LIKE ?)
                '''
                search_term = f"%{search_term}%"
                cursor.execute(query, (search_term, search_term, search_term, search_term))
                songs = cursor.fetchall()
                cursor.close()
                return songs
            except Exception as e:
                print(f"Error fetching songs: {e}")
                return []
            finally:
                connection.close()        

        def performSearchsong():
            search_term = search_entry.get()
            results = searchSongs(search_term)
            result_text_widget.delete('1.0', tk.END)
            for song in results:
                result_text_widget.insert(tk.END, f"{song[0]} {song[1]} {song[2]} {song[3]} {song[4]} {song[5]} {song[6]}\n")

        search_button = tkinter.Button(search_frame, text="Search", command=performSearchsong)
        search_button.grid(row=i+4, column=1, padx=5)

        # Add a text widget to display search results
        result_text_widget = tk.Text(songs_window, font=("Arial", 12))
        result_text_widget.grid(row=i+5, column=0, padx=5)

        #end of search a song

        songs_window.mainloop()        
            

    def openAlbumsWindow():
        albums_window = tk.Toplevel()
        albums_window.title("Albums")
        albums_window.geometry("1000x1000")

        albums = fetchAlbumsFromDb()
        m = 0
        for i, album in enumerate(albums):
            album_id = album[0]
            album_name = album[1]
            artist_id = album[2]
            release_date = album[3]

            album_label = tk.Label(albums_window, text=f"{album_name} by ArtistID {artist_id},  Released on: {release_date}")
            album_label.grid(row=i, column=0, padx=10, pady=5, sticky='w')

            comment_button = tk.Button(albums_window, text="Comment", command=lambda album_id=album_id: commentOnAlbum(album_id))
            comment_button.grid(row=i, column=1, padx=5)

            like_button = tk.Button(albums_window, text="Like", command=lambda album_id=album_id: likeAlbum(album_id))
            like_button.grid(row=i, column=2, padx=5)

            show_songs_button = tk.Button(albums_window, text="Show Songs", command=lambda album_id=album_id: showSongsOfAlbum(album_id))
            show_songs_button.grid(row=i, column=3, padx=5)
            m=i
        # Search functionality for albums
        i = m
        search_frame = tk.Frame(albums_window)
        search_frame.grid(row=i+1, padx=5)
        search_entry = tk.Entry(search_frame, font=("Arial", 14), bd=2, relief=tk.GROOVE, justify=tk.LEFT)
        search_entry.grid(row=0, column=0, padx=5)

        def searchAlbums(search_term):
            try:
                connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                            r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                            r'Database=spotify;'
                                            r'Trusted_Connection=True')
                cursor = connection.cursor()
                query = '''
                SELECT AlbumID, AlbumName, ArtistID, ReleaseDate
                FROM Albums
                WHERE (AlbumName LIKE ? OR ArtistID LIKE ?)
                '''
                search_term = f"%{search_term}%"
                cursor.execute(query, (search_term, search_term))
                albums = cursor.fetchall()
                cursor.close()
                return albums
            except Exception as e:
                print(f"Error fetching albums: {e}")
                return []
            finally:
                connection.close()        

        def performSearchAlbum():
            search_term = search_entry.get()
            results = searchAlbums(search_term)
            result_text_widget.delete('1.0', tk.END)
            for album in results:
                result_text_widget.insert(tk.END, f"{album[0]} {album[1]} {album[2]} {album[3]}\n")

        search_button = tk.Button(search_frame, text="Search", command=performSearchAlbum)
        search_button.grid(row=0, column=1, padx=5)

        result_text_widget = tk.Text(albums_window, font=("Arial", 12))
        result_text_widget.grid(row=i+2, column=0, columnspan=5, padx=5)

        albums_window.mainloop()


    def openPlaylistsWindow():
        playlist_window = tk.Toplevel()
        playlist_window.title("PlayLists")
        playlist_window.geometry("1300x1300")

        playlists = fetchPlaylistsFromDb()

        m=0
        for i, playlist in enumerate(playlists):
            playlist_id = playlist[0]
            user_id = playlist[1]
            playlist_name = playlist[2]
            is_publick = playlist[3]
            creation_date = playlist[4]


            playlist_label = tk.Label(playlist_window, text=f"{playlist_name} by UserID {user_id}")
            playlist_label.grid(row=i, column=0, padx=10, pady=5, sticky='w')


            comment_button = tk.Button(playlist_window, text="Comment", command=lambda playlist_id=playlist_id: commentOnPlaylist(playlist_id))
            comment_button.grid(row=i, column=1, padx=5)

            like_button = tk.Button(playlist_window, text="Like", command=lambda playlist_id=playlist_id: likePlaylist(playlist_id))
            like_button.grid(row=i, column=2, padx=5)

            favorite_button = tk.Button(playlist_window, text="Add to Favorites", command=lambda playlist_id=playlist_id: addToFavoritesplaylist(playlist_id))
            favorite_button.grid(row=i, column=3, padx=5)

            playlist_button = tk.Button(playlist_window, text="Add to Playlist", command=lambda playlist_id=playlist_id: addTomyPlaylist(playlist_id))
            playlist_button.grid(row=i, column=4, padx=5)
            m=i

        #start of search a song
        i=m
        search_frame = tkinter.Frame(playlist_window)
        search_frame.grid(row=i+4,  padx=5)
        search_entry = tkinter.Entry(search_frame, font=("Arial", 14), bd=2, relief=tkinter.GROOVE, justify=tkinter.LEFT)
        search_entry.grid(row=i+4, column=0, padx=5)


        def searchPlaylists(search_term):
            try:
                connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                            r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                            r'Database=spotify;'
                                            r'Trusted_Connection=True')
                cursor = connection.cursor()
                query = '''
                SELECT PlaylistID, PlaylistName, UserID, CreationDate
                FROM Playlists
                WHERE IsPublic = 1
                AND (PlaylistID LIKE ? OR PlaylistName LIKE ? OR UserID LIKE ?)
                '''
                search_term = f"%{search_term}%"
                cursor.execute(query, (search_term, search_term, search_term))
                playlists = cursor.fetchall()
                cursor.close()
                return playlists
            except Exception as e:
                print(f"Error fetching playlist: {e}")
                return []
            finally:
                connection.close()        

        def performSearchplaylist():
            search_term = search_entry.get()
            results = searchPlaylists(search_term)
            result_text_widget.delete('1.0', tk.END)
            for playlist in results:
                result_text_widget.insert(tk.END, f"{playlist[0]} {playlist[1]} {playlist[2]} \n")

        search_button = tkinter.Button(search_frame, text="Search", command=performSearchplaylist)
        search_button.grid(row=i+4, column=1, padx=5)

        # Add a text widget to display search results
        result_text_widget = tk.Text(playlist_window, font=("Arial", 12))
        result_text_widget.grid(row=i+5, column=0, padx=5)

        #end of search a song

        playlist_window.mainloop()        


    def openMyFavoriteWindow():
        my_favorite_window = tkinter.Toplevel(premiumMainwindow)
        my_favorite_window.title("My Favorite")
        favoritelist = fetchfavoritelist()
        for i, favorite in enumerate(favoritelist):
            Item_ID = favorite[0]
            Item_Type = favorite[1]

            favorite_label = tk.Label(my_favorite_window, text=f"{Item_Type} by Item ID: {Item_ID} ")
            favorite_label.grid(row=i, column=0, padx=10, pady=5, sticky='w')


    def openWalletWindow():     
        def cashWithdrawal():
            connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                            r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                            r'Database=spotify;'
                                            r'Trusted_Connection=True')
            cursor = connection.cursor()
            query="UPDATE Wallet SET Balance = Balance + ? WHERE UserID = ?"
            cursor.execute(query,entry_amount.get(),entry_id.get())
            connection.commit()
            cursor.close() 

        transactionToPayPremium=tkinter.Tk()
        transactionToPayPremium.geometry("500x700")
        transactionToPayPremium.title('Pay For Premium')
        pay_label=tkinter.Label(transactionToPayPremium,text="Enter your ID and Transaction Amount")
        pay_label.config(font=("Courier",14))
        pay_label.pack()


        entry_amount = tkinter.Entry(transactionToPayPremium, font=("Arial", 14), bd=2, relief=tkinter.GROOVE, justify=tkinter.LEFT)
        entry_amount.insert(0, "Transaction Amount")
        entry_amount.place(relx=0.2, rely=0.2, relwidth=0.6)

        pay_button=tkinter.Button(transactionToPayPremium,text="Insert",command=cashWithdrawal)
        pay_button.place(relx=0.2,rely=0.3,relwidth=0.6)
        transactionToPayPremium.mainloop() 

    def openSuggestionListWindow():
        suggestion_list_window = tkinter.Toplevel(premiumMainwindow)
        suggestion_list_window.title("Suggestion List")
        suggestions = fetchsuggestionslist()
        for i, suggestion in enumerate(suggestions):
            SongName = suggestion[0]
            AlbumName = suggestion[1]
            ReleaseDate = suggestion[2]

            suggestion_label = tk.Label(suggestion_list_window, text=f"song : {SongName} in Album: {AlbumName} release date: {ReleaseDate} ")
            suggestion_label.grid(row=i, column=0, padx=10, pady=5, sticky='w')


    
    def friendShipRequests():
        def InsertToFreindRequest():
            connection = pyodbc.connect('DRIVER={SQL Server};'
                                    r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                    'Database=spotify;'
                                    'Trusted_Connection=True')
            connection.autocommit = True

            cursor = connection.cursor()
            query = "INSERT INTO  FriendRequests ( SenderRequestID, ReceiverRequestID, Status) VALUES (?, ?, ?)"
            cursor.execute(query, (int(entry_id.get()), entry_ReciverId.get(), 'Pending'))
            #cursor.execute("updateWallet")
            connection.commit()
            cursor.close()

        friendShipRequestWindow=tkinter.Tk()
        friendShipRequestWindow.geometry("200x400")
        friendShipRequestWindow.title('Request')

        entry_ReciverId = tkinter.Entry(friendShipRequestWindow, font=("Arial", 14), bd=2, relief=tkinter.GROOVE, justify=tkinter.LEFT)
        entry_ReciverId.insert(0, "Your Friend's ID")
        entry_ReciverId.place(relx=0.2, rely=0.1, relwidth=0.6)

        display_button=tkinter.Button(friendShipRequestWindow,text="Request",command=InsertToFreindRequest)
        display_button.place(relx=0.2,rely=0.2,relwidth=0.6)    
        friendShipRequestWindow.mainloop()
   
    def ShowRequestTable():
        def ShowFreindRequest():
            connection = pyodbc.connect('DRIVER={SQL Server};'
                                    r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                    'Database=spotify;'
                                    'Trusted_Connection=True')
            connection.autocommit = True
            cursor = connection.cursor()
            query="select * from FriendRequests where ReceiverRequestID=? and Status=?"
            cursor.execute(query,(int(entry_id.get()),'Pending'))
            i=0
            for request in cursor:
                for j in range(len(request)):
                    e= tkinter.Label(whoRequested,width=8,fg='blue',text=request[j],
                         relief='ridge',anchor="w")
                    e.grid(row=i,column=j)
                i=i+1
            connection.commit()
            cursor.close()
        def acceptOrRejectt():
            try:
                connection = pyodbc.connect('DRIVER={SQL Server};'
                                        r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                        'Database=spotify;'
                                        'Trusted_Connection=True')
                connection.autocommit = True
                cursor = connection.cursor()
                query="update FriendRequests set Status=? where ReceiverRequestID=? and SenderRequestID=? and Status=?"
                cursor.execute(query,(entry_status.get(),int(entry_id.get()) ,entry_idd.get(),'Pending'))
                if(entry_status.get()=='Accepted'):
                    cursor.execute("updateFollowList")
                
            except Exception as e:
                print(f"Error updating friend request: {e}")
            finally:
                cursor.close()
                connection.close()
            
        whoRequested=tkinter.Tk()
        whoRequested.geometry("200x400")
        whoRequested.title('Who Requested To Me')

        display_button=tkinter.Button(whoRequested,text="Show",command=ShowFreindRequest)
        display_button.place(relx=0.2,rely=0.2,relwidth=0.6)  
              
        entry_idd = tkinter.Entry(whoRequested, font=("Arial", 14), bd=2, relief=tkinter.GROOVE, justify=tkinter.LEFT)
        entry_idd.insert(0, "ID that you want to accept")
        entry_idd.place(relx=0.2, rely=0.7, relwidth=0.6)

        entry_status = tkinter.Entry(whoRequested, font=("Arial", 14), bd=2, relief=tkinter.GROOVE, justify=tkinter.LEFT)
        entry_status.insert(0, "Accepted,Rejected")
        entry_status.place(relx=0.2, rely=0.8, relwidth=0.6)

        display_button=tkinter.Button(whoRequested,text="Set",command=acceptOrRejectt)
        display_button.place(relx=0.2,rely=0.9,relwidth=0.6)     

        whoRequested.mainloop()
    
    def messageing():
        def messageingToYourFolwing():
            try:
                connection = pyodbc.connect('DRIVER={SQL Server};'
                                        r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                        'Database=spotify;'
                                        'Trusted_Connection=True')
                connection.autocommit = True
                cursor = connection.cursor()
                sender_id = int(entry_id.get())
                receiver_id = int(entry_idRecive.get())
                message_text = entry_txt.get()

                    # Check if there is an accepted friend request between sender and receiver
                query_check_request = """
                    SELECT 1
                    FROM spotify.dbo.FriendRequests
                    WHERE SenderRequestID = ?
                        AND ReceiverRequestID = ?
                        AND Status = 'Accepted';
                """
                cursor.execute(query_check_request, (sender_id, receiver_id))
                if not cursor.fetchone():
                    messagebox.showwarning("Error", "No accepted friend request found between these users.")
                    return
                
                # Insert the message into MessageList table
                query_insert_message = """
                    INSERT INTO spotify.dbo.MessageList (SenderID, ReceiverID, MessageText)
                    VALUES (?, ?, ?);
                """
                cursor.execute(query_insert_message, (sender_id, receiver_id, message_text))
                
                messagebox.showinfo("Success", "Message sent successfully!")
                
            except Exception as e:
                print(f"Error : {e}")
            finally:
                cursor.close()
                connection.close()

        messageTo=tkinter.Tk()
        messageTo.geometry("300x400")
        messageTo.title('send Messeage to your following')    

        entry_idRecive = tkinter.Entry(messageTo, font=("Arial", 14), bd=2, relief=tkinter.GROOVE, justify=tkinter.LEFT)
        entry_idRecive.insert(0, "Yor friend's Id")
        entry_idRecive.place(relx=0.2, rely=0.3, relwidth=0.6)

        entry_txt = tkinter.Entry(messageTo, font=("Arial", 14), bd=2, relief=tkinter.GROOVE, justify=tkinter.LEFT)
        entry_txt.insert(0, "text")
        entry_txt.place(relx=0.2, rely=0.4, relwidth=0.6)

        send_button=tkinter.Button(messageTo,text="Set",command=messageingToYourFolwing)
        send_button.place(relx=0.2,rely=0.5,relwidth=0.6)     
        messageTo.mainloop()

    def showRejectAndAccepted():
        def showAcc():
            connection = pyodbc.connect('DRIVER={SQL Server};'
                                    r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                    'Database=spotify;'
                                    'Trusted_Connection=True')
            connection.autocommit = True
            cursor = connection.cursor()
            query="select * from FriendRequests where ReceiverRequestID=? and Status=?"
            cursor.execute(query,int(entry_id.get()),'Accepted')
            i=0
            for request in cursor:
                for j in range(len(request)):
                    e= tkinter.Label(ShowRejAndAcc,width=8,fg='blue',text=request[j],
                        relief='ridge',anchor="w")
                    e.grid(row=i,column=j)
                i=i+1
            connection.commit()
            cursor.close()
        def showRej():
            connection = pyodbc.connect('DRIVER={SQL Server};'
                                    r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                    'Database=spotify;'
                                    'Trusted_Connection=True')
            connection.autocommit = True
            cursor = connection.cursor()
            query="select * from FriendRequests where ReceiverRequestID=? and Status=?"
            cursor.execute(query,int(entry_id.get()),'Rejected')
            i=0
            for request in cursor:
                for j in range(len(request)):
                    e= tkinter.Label(ShowRejAndAcc,width=8,fg='blue',text=request[j],
                        relief='ridge',anchor="w")
                    e.grid(row=i,column=j)
                i=i+1
            connection.commit()
            cursor.close()
        ShowRejAndAcc=tkinter.Tk()
        ShowRejAndAcc.geometry("300x400")
        ShowRejAndAcc.title('Rejected and Accepted people')  

        send_buttonAccept=tkinter.Button(ShowRejAndAcc,text="accepted",command=showAcc)
        send_buttonAccept.place(relx=0.2,rely=0.3,relwidth=0.6)
        send_buttonReiect=tkinter.Button(ShowRejAndAcc,text="rejected",command=showRej)
        send_buttonReiect.place(relx=0.2,rely=0.4,relwidth=0.6)     
        ShowRejAndAcc.mainloop()

    def showConcerts():
        def show():
            connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                r'Database=spotify;'
                                r'Trusted_Connection=True')
            cursor = connection.cursor()
    
            # Execute the query to fetch concerts
            query = "SELECT * FROM Concerts"
            cursor.execute(query)
            concerts = cursor.fetchall()
    
            # Clear any previous content in the main_frame
            for widget in main_frame.winfo_children():
                widget.destroy()
            
            # Display the column headers
            headers = ["ConcertID", "ArtistID", "Title", "NumberOfTickets", "Date", "Price", "IsCancelled"]
            for j, header in enumerate(headers):
                e = tk.Label(main_frame, width=15, fg='black', text=header, relief='ridge', anchor='w')
                e.grid(row=0, column=j)
            
            # Display the concert data
            for i, concert in enumerate(concerts, start=1):
                for j, value in enumerate(concert):
                    e = tk.Label(main_frame, width=15, fg='blue', text=value, relief='ridge', anchor='w')
                    e.grid(row=i, column=j)
            
            # Close the connection
            connection.close()

        def purchase_ticket():
            try:
                connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                                        r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                                        r'Database=spotify;'
                                                        r'Trusted_Connection=True')
                cursor = connection.cursor()
                user_id = int(entry_id.get())
                concert_id = int(entry_concertID.get())
            
            # Check if concert is cancelled or sold out
                cursor.execute("""
                    SELECT NumberOfTkickets, Price, IsCancelled , Date
                    FROM spotify.dbo.Concerts 
                    WHERE ConcertID = ?
                """, (concert_id,))
                concert = cursor.fetchone()
            
                if not concert:
                    messagebox.showerror("Error", "Concert not found")
                    return
                
                number_of_tickets, price, is_cancelled ,DateConcert= concert
            
                if is_cancelled:
                    messagebox.showerror("Error", "Concert is cancelled")
                    return
                
                if number_of_tickets == 0:
                    messagebox.showerror("Error", "Concert is sold out")
                    return
            
                # Check if user has sufficient balance
                cursor.execute("""
                    SELECT Balance 
                    FROM spotify.dbo.Wallet 
                    WHERE UserID = ?
                """, (user_id,))
                wallet = cursor.fetchone()
                
                if not wallet:
                    messagebox.showerror("Error", "User not found")
                    return
                
                balance = wallet[0]
                
                if balance < price:
                    messagebox.showerror("Error", "Insufficient balance")
                    return
            
                # Update the Tickets table
                cursor.execute("""
                    INSERT INTO Tickets (UserID, ConcertID, ExpiryDate) 
                    VALUES (?, ?,?)
                """, (user_id, concert_id,DateConcert))
            
                # Update the Wallet table
                cursor.execute("""
                    UPDATE Wallet 
                    SET Balance = Balance - ? 
                    WHERE UserID = ?
                """, (price, user_id))
                
                # Update the Concerts table
                cursor.execute("""
                    UPDATE Concerts 
                    SET NumberOfTkickets = NumberOfTkickets - 1 
                    WHERE ConcertID = ?
                """, (concert_id,))
        
                messagebox.showinfo("Success", "Ticket purchased successfully")
    
            except pyodbc.Error as e:
                messagebox.showerror("Database Error", str(e))
    
            finally:
                connection.commit()
                cursor.close()



        ShowConcert_wind=tkinter.Tk()
        ShowConcert_wind.geometry("900x400")
        ShowConcert_wind.title('Concerts')  
        main_frame = tk.Frame(ShowConcert_wind)
        main_frame.pack(pady=20)

        show_concert=tkinter.Button(ShowConcert_wind,text="show",command=show)
        show_concert.place(relx=0.2,rely=0.7,relwidth=0.6)
        entry_concertID = tkinter.Entry(ShowConcert_wind, font=("Arial", 14), bd=2, relief=tkinter.GROOVE, justify=tkinter.LEFT)
        entry_concertID.insert(0, "Which concert do you want to attend?")
        entry_concertID.place(relx=0.2, rely=0.8, relwidth=0.6)
        buy_ticket=tkinter.Button(ShowConcert_wind,text="buy",command=purchase_ticket)
        buy_ticket.place(relx=0.2,rely=0.9,relwidth=0.6)

        ShowConcert_wind.mainloop()
    def showTickets():
        def showNotExpiredTick():
            connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                r'Database=spotify;'
                                r'Trusted_Connection=True')
            cursor = connection.cursor()
    
            # Execute the query to fetch concerts
            query = '''SELECT ConcertID,PurchaseDate,ExpiryDate FROM Tickets
                     where UserID=? and IsExpired=0 '''
            cursor.execute(query,(int(entry_id.get())))
            tickets = cursor.fetchall()
    
            # Clear any previous content in the main_frame
            for widget in main_frame.winfo_children():
                widget.destroy()
            
            # Display the column headers
            headers = ["ConcertID", "PurchaseDate", "ExpiryDate"]
            for j, header in enumerate(headers):
                e = tk.Label(main_frame, width=15, fg='black', text=header, relief='ridge', anchor='w')
                e.grid(row=0, column=j)
            # Display the concert data
            for i, concert in enumerate(tickets, start=1):
                for j, value in enumerate(concert):
                    e = tk.Label(main_frame, width=15, fg='blue', text=value, relief='ridge', anchor='w')
                    e.grid(row=i, column=j)
            connection.close()
        def showExpiredTick():
            connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                r'Database=spotify;'
                                r'Trusted_Connection=True')
            cursor = connection.cursor()
    
            # Execute the query to fetch concerts
            query = '''SELECT ConcertID,PurchaseDate,ExpiryDate FROM Tickets
                     where UserID=? and IsExpired=1 '''
            cursor.execute(query,(int(entry_id.get())))
            tickets = cursor.fetchall()
    
            # Clear any previous content in the main_frame
            for widget in main_frame.winfo_children():
                widget.destroy()
            
            # Display the column headers
            headers = ["ConcertID", "PurchaseDate", "ExpiryDate"]
            for j, header in enumerate(headers):
                e = tk.Label(main_frame, width=15, fg='black', text=header, relief='ridge', anchor='w')
                e.grid(row=0, column=j)
            # Display the concert data
            for i, concert in enumerate(tickets, start=1):
                for j, value in enumerate(concert):
                    e = tk.Label(main_frame, width=15, fg='blue', text=value, relief='ridge', anchor='w')
                    e.grid(row=i, column=j)
            connection.close()
        ShowTicket_wind=tkinter.Tk()
        ShowTicket_wind.geometry("300x400")
        ShowTicket_wind.title('Ticketss')  
        main_frame = tk.Frame(ShowTicket_wind)
        main_frame.pack(pady=20)
        show_notTicket=tkinter.Button(ShowTicket_wind,text="show Not Expired",command=showNotExpiredTick)
        show_notTicket.place(relx=0.2,rely=0.5,relwidth=0.6)
        show_ticket=tkinter.Button(ShowTicket_wind,text="show Expired",command=showExpiredTick)
        show_ticket.place(relx=0.2,rely=0.6,relwidth=0.6)


    def openAddSongWindow():

        add_song_window = tkinter.Toplevel(premiumMainwindow)
        add_song_window.title("Add Song")    
        add_song_window.geometry("500x700")

        def savesong():
            try:
                connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                            r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                            r'Database=spotify;'
                                            r'Trusted_Connection=True')
                cursor = connection.cursor()
                query = f"INSERT INTO Songs (SongName, ArtistID, AlbumID, Genre, ReleaseDate, Lyrics, IsAddableToPlaylist, IsAvailble) VALUES ('{song_name_entry.get()}', {entry_id.get()}, {album_entry.get()}, '{Genre_entry.get()}', '{date.today()}', '{lyr_entry.get()}', {addable_entry.get()}, {ava_entry.get()})"
                cursor.execute(query)
                connection.commit()
                cursor.close()
                messagebox.showinfo("Like", "Song add successfully!")
            except Exception as e:
                print(f"Error liking song: {e}")
                messagebox.showerror("Error", "Failed to add song")
            finally:
                connection.close()  
        # Create widgets for the Add Song window
        song_name_label = tkinter.Label(add_song_window, text="Song Title:")
        song_name_entry = tkinter.Entry(add_song_window)
        song_name_label.grid(row=0, column=0)
        song_name_entry.grid(row=0, column=1)

        album_label = tkinter.Label(add_song_window, text="Album ID:")
        album_entry = tkinter.Entry(add_song_window)
        album_label.grid(row=1, column=0)
        album_entry.grid(row=1, column=1)

        Genre_label = tkinter.Label(add_song_window, text="Genre :")
        Genre_entry = tkinter.Entry(add_song_window)
        Genre_label.grid(row=2, column=0)
        Genre_entry.grid(row=2, column=1)

        lyr_label = tkinter.Label(add_song_window, text="Lyrics :")
        lyr_entry = tkinter.Entry(add_song_window)
        lyr_label.grid(row=3, column=0)
        lyr_entry.grid(row=3, column=1)

        addable_label = tkinter.Label(add_song_window, text="Is Addable to Playlists?(1=yes)")
        addable_entry = tkinter.Entry(add_song_window)
        addable_label.grid(row=4, column=0)
        addable_entry.grid(row=4, column=1)

        ava_label = tkinter.Label(add_song_window, text="Is Available? (1=yes)")
        ava_entry = tkinter.Entry(add_song_window)
        ava_label.grid(row=5, column=0)
        ava_entry.grid(row=5, column=1)


        save_button=tkinter.Button(add_song_window,text="Save",command=savesong)
        save_button.grid(row=7, column=3)

        add_song_window.mainloop()

    def openDeleteSongWindow():
        delete_song_window = tkinter.Toplevel(premiumMainwindow)
        delete_song_window.title("Delete Song")    
        delete_song_window.geometry("500x700")
        def deletesong():
            try:
                connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                            r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                            r'Database=spotify;'
                                            r'Trusted_Connection=True')
                cursor = connection.cursor()
                query = f"DELETE FROM Songs WHERE SongName = '{song_name_entry.get()}' AND ArtistID= {entry_id.get()} "
                cursor.execute(query)
                connection.commit()
                cursor.close()
                messagebox.showinfo("Like", "Song delete successfully!")
            except Exception as e:
                print(f"Error delete song: {e}")
                messagebox.showerror("Error", "Failed to delete song")
            finally:
                connection.close()            

        song_name_label = tkinter.Label(delete_song_window, text="Song Title:")
        song_name_entry = tkinter.Entry(delete_song_window)
        song_name_label.grid(row=0, column=0)
        song_name_entry.grid(row=0, column=1)

        del_button=tkinter.Button(delete_song_window,text="Delete",command=deletesong)
        del_button.grid(row=4, column=3)

        
    def openAddAlbumWindow():
        add_album_window = tkinter.Toplevel(premiumMainwindow)
        add_album_window.title("Add Album")    
        add_album_window.geometry("500x700")

        def savealbum():
            try:
                connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                            r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                            r'Database=spotify;'
                                            r'Trusted_Connection=True')
                cursor = connection.cursor()
                query = f"INSERT INTO Albums (AlbumName, ArtistID, ReleaseDate) VALUES ('{album_name_entry.get()}', {entry_id.get()},'{date.today()}')"
                cursor.execute(query)
                connection.commit()
                cursor.close()
                messagebox.showinfo("add", "album add successfully!")
            except Exception as e:
                print(f"Error add album: {e}")
                messagebox.showerror("Error", "Failed to add album")
            finally:
                connection.close() 


        album_name_label = tkinter.Label(add_album_window, text="Album Title:")
        album_name_entry = tkinter.Entry(add_album_window)
        album_name_label.grid(row=0, column=0)
        album_name_entry.grid(row=0, column=1)

        save_button=tkinter.Button(add_album_window,text="Save",command=savealbum)
        save_button.grid(row=7, column=3)
        save_button=tkinter.Button(add_album_window,text="Add Song to Album",command=openAddSongWindow)
        save_button.grid(row=9, column=3)


    def openDeleteAlbumWindow():
        delete_album_window = tkinter.Toplevel(premiumMainwindow)
        delete_album_window.title("Delete Album")    
        delete_album_window.geometry("500x700")
        def deletealbum():
            try:
                connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                            r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                            r'Database=spotify;'
                                            r'Trusted_Connection=True')
                cursor = connection.cursor()
                query = f"DELETE FROM Albums WHERE AlbumName = '{album_name_entry.get()}' AND ArtistID= {entry_id.get()} "
                cursor.execute(query)
                connection.commit()
                cursor.close()
                messagebox.showinfo("delete", " delete successfully!")
            except Exception as e:
                print(f"Error delete : {e}")
                messagebox.showerror("Error", "Failed to delete ")
            finally:
                connection.close()            

        album_name_label = tkinter.Label(delete_album_window, text="Album Title:")
        album_name_entry = tkinter.Entry(delete_album_window)
        album_name_label.grid(row=0, column=0)
        album_name_entry.grid(row=0, column=1)

        del_button=tkinter.Button(delete_album_window,text="Delete",command=deletealbum)
        del_button.grid(row=4, column=3)
        

    def PlanForConcert():
        def create():
            def create_concertFunc():
                try:
                    user_id = int(entry_id.get())
                    title = entry_title.get()
                    date = entry_date.get()
                    num_tickets = int(entry_num_tickets.get())
                    price = float(entry_price.get())
                    connection = pyodbc.connect('DRIVER={SQL Server};'
                                                r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                                'Database=spotify;'
                                                'Trusted_Connection=True')
                    connection.autocommit = True
                    cursor = connection.cursor()
                    
                    # Get the ArtistID from the UserID
                    cursor.execute("SELECT ArtistID FROM Artists WHERE UserID = ?", (user_id,))
                    artist = cursor.fetchone()
                
                    if not artist:
                        messagebox.showerror("Error", "Artist not found for the given UserID")
                        return
                    
                    artist_id = artist[0]
                    
                    # Insert the new concert into the Concerts table
                    cursor.execute('''
                        INSERT INTO spotify.dbo.Concerts (ArtistID, Title, NumberOfTkickets, Date, Price)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (artist_id, title, num_tickets, date, price))
                    
                    connection.commit()
                    messagebox.showinfo("Success", "Concert created successfully")
                
                except pyodbc.Error as e:
                    messagebox.showerror("Database Error", str(e))
                
                finally:
                    cursor.close()

            concertInfoForInserting=tkinter.Tk()
            concertInfoForInserting.geometry("300x300")
            concertInfoForInserting.title("Insert Your Concert Info")
            #tk.Label(concertInfoForInserting, text="Title:").place(relx=0.2, rely=0.1, relwidth=0.3)
            entry_title = tk.Entry(concertInfoForInserting,font=("Arial", 14), bd=2, relief=tkinter.GROOVE, justify=tkinter.LEFT)
            entry_title.insert(0,"Title")
            entry_title.place(relx=0.2, rely=0.1, relwidth=0.5)

            # Concert Date entry
            #tk.Label(concertInfoForInserting, text="Date (YYYY-MM-DD):").pack(pady=5)
            entry_date = DateEntry(concertInfoForInserting, font=("Arial", 14), bd=2, relief=tk.GROOVE, justify=tk.LEFT, date_pattern='y-mm-dd')
            entry_date.insert(0, "Date")
            entry_date.place(relx=0.2, rely=0.2, relwidth=0.6)

            # Number of Tickets entry
            #tk.Label(concertInfoForInserting, text="Number of Tickets:").place(relx=0.2, rely=0.1, relwidth=0.3)
            entry_num_tickets = tk.Entry(concertInfoForInserting,font=("Arial", 14), bd=2, relief=tkinter.GROOVE, justify=tkinter.LEFT)
            entry_num_tickets.insert(0,"Number Of Tickets")
            entry_num_tickets.place(relx=0.2, rely=0.3, relwidth=0.5)

            # Price entry
            #tk.Label(concertInfoForInserting, text="Price:").place(relx=0.2, rely=0.1, relwidth=0.3)
            entry_price = tk.Entry(concertInfoForInserting,font=("Arial", 14), bd=2, relief=tkinter.GROOVE, justify=tkinter.LEFT)
            entry_price.insert(0,"Price")
            entry_price.place(relx=0.2, rely=0.4, relwidth=0.5)
            create_concert_button = tk.Button(concertInfoForInserting, text="Create Concert", command=create_concertFunc)
            create_concert_button.place(relx=0.2, rely=0.5, relwidth=0.5)
            concertInfoForInserting.mainloop()
        def Cancel():
            def concertCanceling():
                concert_id = int(entry_concert_id.get())
                user_id = int(entry_id.get())
        
                try:
                    connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                                r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                                r'Database=spotify;'
                                                r'Trusted_Connection=True')
                    cursor = connection.cursor()
                    
                    # Verify if the concert exists and belongs to the given user
                    cursor.execute('''
                        SELECT c.ConcertID
                        FROM spotify.dbo.Concerts c
                        INNER JOIN spotify.dbo.Artists a ON c.ArtistID = a.ArtistID
                        WHERE c.ConcertID = ? AND a.UserID = ?
                    ''', (concert_id, user_id))
            
                    concert = cursor.fetchone()
                    
                    if not concert:
                        messagebox.showerror("Error", "Concert ID does not exist or does not belong to the specified user.")
                        return
                    
                    # Update the concert status to cancelled
                    cursor.execute('''
                        UPDATE spotify.dbo.Concerts
                        SET IsCancelled = 1
                        WHERE ConcertID = ?
                    ''', (concert_id,))
                    
                    connection.commit()
                    messagebox.showinfo("Success", "Concert has been cancelled successfully.")
            
                except pyodbc.Error as e:
                    messagebox.showerror("Database Error", str(e))
                finally:
                    cursor.close()
                    connection.close()

            cancelingConcertWindow = tkinter.Tk()
            cancelingConcertWindow.geometry("400x300")
            cancelingConcertWindow.title("Cancel Concert Info")
            tk.Label(cancelingConcertWindow, text="Concert ID:").pack(pady=5)
            entry_concert_id = tk.Entry(cancelingConcertWindow)
            entry_concert_id.place(relx=0.2, rely=0.1, relwidth=0.3)
            cancel_concert_button = tk.Button(cancelingConcertWindow, text="Cancel Concert", command=concertCanceling)
            cancel_concert_button.place(relx=0.2, rely=0.2, relwidth=0.3)
            cancelingConcertWindow.mainloop()
        concert_window = tkinter.Tk()
        concert_window.geometry("200x200")
        concert_window.title("Concert")
        create_button=tkinter.Button(concert_window,text="create concert",command=create)
        create_button.place(relx=0.2,rely=0.2,relwidth=0.6)
        cancel_button=tkinter.Button(concert_window,text="cancel concert",command=Cancel)
        cancel_button.place(relx=0.2,rely=0.3,relwidth=0.6)
        concert_window.mainloop()



    button_frame = tkinter.Frame(premiumMainwindow)
    button_frame.pack(side=tkinter.TOP, pady=10)
    buttons_data = [
        ("Songs", openSongsWindow),
        ("Albums", openAlbumsWindow),
        ("Playlists", openPlaylistsWindow),
        ("My Favorite", openMyFavoriteWindow),
        ("Wallet", openWalletWindow),
        ("Suggestion List", openSuggestionListWindow),
        ("My Requests",friendShipRequests),
        ("Who Requestedto To Me",ShowRequestTable),
        ("message to folowing",messageing),
        ("Who I rejected and accepted",showRejectAndAccepted),
        ("Concerts",showConcerts),
        ("My Tickets",showTickets),
        ("My Concerts",PlanForConcert),
        ("Add New Song", openAddSongWindow),
        ("Add New Album", openAddAlbumWindow),
        ("Delete a Song", openDeleteSongWindow),
        ("Delete a Album", openDeleteAlbumWindow),
    ]

    columns = 4 
    for index, (text, command) in enumerate(buttons_data): 
        row = index // columns 
        column = index % columns 
        button = tk.Button(button_frame, text=text, command=command) 
        button.grid(row=row, column=column, padx=5, pady=5)


    premiumMainwindow.mainloop()


def AreYouArtist():
    def yesOrNo():
        if(entry_areYou.get()=="Yes"):
            def InsertYorArtistId():
                try:
                    connection = pyodbc.connect('DRIVER={SQL Server};'
                                                r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                                'Database=spotify;'
                                                'Trusted_Connection=True')
                    connection.autocommit = True

                    cursor = connection.cursor()
                    query = "INSERT INTO Artists (ArtistID,UserID) VALUES (?, ?)"
                    cursor.execute(query, (entry_ArtistId.get(),entry_id.get()))

                    connection.commit()
                    cursor.close()
                except Exception as e:
                    print(f"Error: {e}")
                finally:
                    connection.close()
            artistIdInserting_window= tkinter.Tk()
            artistIdInserting_window.geometry("500x700")
            artistIdInserting_window.title('Artist Info')

            entry_ArtistId = tkinter.Entry(artistIdInserting_window, font=("Arial", 14), bd=2, relief=tkinter.GROOVE, justify=tkinter.LEFT)
            entry_ArtistId.insert(0, "You Artist Id")
            entry_ArtistId.place(relx=0.2, rely=0.1, relwidth=0.6)
            
            insertArtistId_button=tkinter.Button(artistIdInserting_window,text="Insert",command=lambda: [InsertYorArtistId(),ArtistMainWindow()])
            insertArtistId_button.place(relx=0.2,rely=0.3,relwidth=0.6)
            artistIdInserting_window.mainloop() 
        elif(entry_areYou.get()=="No"):
            premiumUserMainWindow()
    
    areYou_window= tkinter.Tk()
    areYou_window.geometry("500x700")
    areYou_window.title('Are You An Artist')

    entry_areYou = tkinter.Entry(areYou_window, font=("Arial", 14), bd=2, relief=tkinter.GROOVE, justify=tkinter.LEFT)
    entry_areYou.insert(0, "Yes or No")
    entry_areYou.place(relx=0.2, rely=0.1, relwidth=0.6)
    
    insert_button=tkinter.Button(areYou_window,text="Insert",command=yesOrNo)
    insert_button.place(relx=0.2,rely=0.3,relwidth=0.6)
    areYou_window.mainloop() 

    


def openNewWindowAfterRegistration():
    if (entry_registrationType.get()=='Free'):
        songListWindow= tkinter.Tk()
        songListWindow.geometry("500x700")
        songListWindow.title('songs')

        cursor=fetchSongsFromDbF()

        i=0
        for song in cursor:
            for j in range(len(song)):
                e= tkinter.Label(songListWindow,width=8,fg='blue',text=song[j],
                         relief='ridge',anchor="w")
                e.grid(row=i,column=j)
            i=i+1
        songListWindow.mainloop()
    elif (entry_registrationType.get()=='Premium'):
        def cashWithdrawal():
            connection = pyodbc.connect(r'DRIVER={SQL Server};'
                                            r'Server=DESKTOP-18I9O44\SQLEXPRESS;'
                                            r'Database=spotify;'
                                            r'Trusted_Connection=True')
            cursor = connection.cursor()
            query="UPDATE Wallet SET Balance = Balance + ? WHERE UserID = ?"
            cursor.execute(query,entry_amount.get(),entry_id.get())
            connection.commit()
            cursor.close() 

        transactionToPayPremium=tkinter.Tk()
        transactionToPayPremium.geometry("500x700")
        transactionToPayPremium.title('Pay For Premium')
        pay_label=tkinter.Label(transactionToPayPremium,text="Pay 10$ for premium")
        pay_label.config(font=("Courier",14))
        pay_label.pack()

        entry_amount = tkinter.Entry(transactionToPayPremium, font=("Arial", 14), bd=2, relief=tkinter.GROOVE, justify=tkinter.LEFT)
        entry_amount.insert(0, "Transaction Amount")
        entry_amount.place(relx=0.2, rely=0.2, relwidth=0.6)

        pay_button=tkinter.Button(transactionToPayPremium,text="Insert",command=lambda: [cashWithdrawal(),AreYouArtist()])
        pay_button.place(relx=0.2,rely=0.3,relwidth=0.6)
        transactionToPayPremium.mainloop() 



        
        









import tkinter.messagebox
import tkinter.ttk
import pyodbc
import customtkinter
import tkinter as tk
from tkcalendar import DateEntry
import tkinter as ttk

from datetime import date



root =tkinter.Tk()
root.geometry("500x700")
root.title("welcome to Spotify")

wellcom=tkinter.Label(root,text="Enter the requested information")
wellcom.config(font=("Courier",14))
wellcom.pack()

entry_id = tkinter.Entry(root, font=("Arial", 14), bd=2, relief=tkinter.GROOVE, justify=tkinter.LEFT)
entry_id.insert(0, "ID")
entry_id.place(relx=0.2, rely=0.1, relwidth=0.6)

entry_firstName = tkinter.Entry(root, font=("Arial", 14), bd=2, relief=tkinter.GROOVE, justify=tkinter.LEFT)
entry_firstName.insert(0, "Name")
entry_firstName.place(relx=0.2, rely=0.2, relwidth=0.6)

entry_password = tkinter.Entry(root, font=("Arial", 14), bd=2, relief=tkinter.GROOVE, justify=tkinter.LEFT)
entry_password.insert(0, "Password")
entry_password.place(relx=0.2, rely=0.3, relwidth=0.6)

entry_birthDay = DateEntry(root, font=("Arial", 14), bd=2, relief=tk.GROOVE, justify=tk.LEFT, date_pattern='y-mm-dd')
entry_birthDay.place(relx=0.2, rely=0.4, relwidth=0.6)

entry_email = tkinter.Entry(root, font=("Arial", 14), bd=2, relief=tkinter.GROOVE, justify=tkinter.LEFT)
entry_email.insert(0, "Email Address")
entry_email.place(relx=0.2, rely=0.5, relwidth=0.6)

entry_location = tkinter.Entry(root, font=("Arial", 14), bd=2, relief=tkinter.GROOVE, justify=tkinter.LEFT)
entry_location.insert(0, "Location")
entry_location.place(relx=0.2, rely=0.6, relwidth=0.6)

entry_registrationType = tkinter.Entry(root, font=("Arial", 14), bd=2, relief=tkinter.GROOVE, justify=tkinter.LEFT)
entry_registrationType.insert(0, "Free or Premium")
entry_registrationType.place(relx=0.2, rely=0.7, relwidth=0.6) 
 

insert_button=tkinter.Button(root,text="Insert",command=lambda: [insertToUsers(), openNewWindowAfterRegistration()])
insert_button.place(relx=0.2,rely=0.8,relwidth=0.6)
tkinter.mainloop()












