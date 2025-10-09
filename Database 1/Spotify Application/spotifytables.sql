DROP TABLE IF EXISTS spotify.dbo.PlaylistSongs;
DROP TABLE IF EXISTS spotify.dbo.Playlists;
DROP TABLE IF EXISTS spotify.dbo.FavoriteList;
DROP TABLE IF EXISTS spotify.dbo.Likes;
DROP TABLE IF EXISTS spotify.dbo.Comments;
DROP TABLE IF EXISTS spotify.dbo.FriendRequests;
DROP TABLE IF EXISTS spotify.dbo.FollowList;
DROP TABLE IF EXISTS spotify.dbo.MessageList;
DROP TABLE IF EXISTS spotify.dbo.Tickets;
DROP TABLE IF EXISTS spotify.dbo.Concerts;
DROP TABLE IF EXISTS spotify.dbo.Friends;
DROP TABLE IF EXISTS spotify.dbo.Wallet;
DROP TABLE IF EXISTS spotify.dbo.Songs;
DROP TABLE IF EXISTS spotify.dbo.Albums;
DROP TABLE IF EXISTS spotify.dbo.Artists;
DROP TABLE IF EXISTS spotify.dbo.Users;


CREATE TABLE spotify.dbo.Users (
    UserID INT NOT NULL UNIQUE,
    Username VARCHAR(50) NOT NULL UNIQUE,
    PasswordHash VARCHAR(50) NOT NULL,
    BirthDate Date,
    Email VARCHAR(100)  UNIQUE,
	Locationn varchar(300),
    SubscriptionType varchar(20) NOT NULL CHECK (SubscriptionType IN('Free', 'Premium', 'Artist')),
    RegistrationDate  DATETIME2(3) DEFAULT CURRENT_TIMESTAMP ,
	PRIMARY KEY (UserID)
);

CREATE TABLE spotify.dbo.Artists (
    ArtistID INT UNIQUE,
    UserID INT UNIQUE,
    FOREIGN KEY (UserID) REFERENCES spotify.dbo.Users(UserID),
	PRIMARY KEY (ArtistID)
);

CREATE TABLE spotify.dbo.Albums (
    AlbumID INT PRIMARY KEY IDENTITY(1, 1),
    AlbumName VARCHAR(100) NOT NULL,
    ArtistID INT,
    ReleaseDate DATE,
    FOREIGN KEY (ArtistID) REFERENCES spotify.dbo.Artists(ArtistID)
);

CREATE TABLE spotify.dbo.Songs (
    SongID INT PRIMARY KEY IDENTITY(1, 1),
    SongName VARCHAR(100) NOT NULL,
    ArtistID INT,
    AlbumID INT,
    Genre VARCHAR(50),
    ReleaseDate DATE,
    Lyrics TEXT,
    IsAddableToPlaylist BIT DEFAULT 1,
	IsAvailble BIT DEFAULT 1,
    FOREIGN KEY (ArtistID) REFERENCES spotify.dbo.Artists(ArtistID),
    FOREIGN KEY (AlbumID) REFERENCES spotify.dbo.Albums(AlbumID)
);

CREATE TABLE spotify.dbo.Playlists (
    PlaylistID INT PRIMARY KEY IDENTITY(1, 1),
    UserID INT,
    PlaylistName VARCHAR(100),
    IsPublic BIT DEFAULT 0,
    CreationDate DATETIME2(3) DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES spotify.dbo.Users(UserID)
);

CREATE TABLE spotify.dbo.PlaylistSongs (
    PlaylistID INT,
    SongID INT,
    PRIMARY KEY (PlaylistID, SongID),
    FOREIGN KEY (PlaylistID) REFERENCES spotify.dbo.Playlists(PlaylistID),
    FOREIGN KEY (SongID) REFERENCES spotify.dbo.Songs(SongID)
);

CREATE TABLE spotify.dbo.FavoriteList (
    UserID INT NOT NULL,
    ItemID INT,
    ItemType varchar(20) NOT NULL CHECK (ItemType IN('Song', 'Playlist')) ,
	PRIMARY KEY (UserID,ItemID,ItemType),
    FOREIGN KEY (UserID) REFERENCES spotify.dbo.Users(UserID)
);

CREATE TABLE spotify.dbo.Likes (
    UserID INT,
    ItemID INT,  
    ItemType varchar(20) NOT NULL CHECK (ItemType IN('Song', 'Playlist','Album')) ,
    LikeDate DATETIME2(3) DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (UserID,ItemID, ItemType),
    FOREIGN KEY (UserID) REFERENCES spotify.dbo.Users(UserID)
);

CREATE TABLE spotify.dbo.Comments (
    UserID INT,
    ItemID INT,  
    ItemType varchar(20) NOT NULL CHECK (ItemType IN('Song', 'Playlist','Album')) ,
    CommentText varchar(300),
	PRIMARY KEY (UserID,ItemID,ItemType,CommentText),
    CommentDate DATETIME2(3) DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES spotify.dbo.Users(UserID)
);

CREATE TABLE spotify.dbo.FriendRequests (
    SenderRequestID INT,
    ReceiverRequestID INT,
    Status varchar(20) NOT NULL CHECK (Status IN('Pending', 'Accepted', 'Rejected')),
    RequestDate DATETIME2(3) DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (SenderRequestID,ReceiverRequestID),
    FOREIGN KEY (SenderRequestID) REFERENCES spotify.dbo.Users(UserID),
    FOREIGN KEY (ReceiverRequestID) REFERENCES spotify.dbo.Users(UserID)
);

CREATE TABLE spotify.dbo.FollowList (
    FollowedID INT,
    FollowerID INT,
	--IsArtist BIT DEFAULT 0,
	--IsFriend BIT DEFAULT 0,
    PRIMARY KEY (FollowerID, FollowedID),
    FOREIGN KEY (FollowerID) REFERENCES spotify.dbo.Users(UserID),
    FOREIGN KEY (FollowedID) REFERENCES spotify.dbo.Users(UserID)
);

CREATE TABLE spotify.dbo.MessageList (
    SenderID INT,
    ReceiverID INT,
    MessageText TEXT,
    SentDate DATETIME2(3) DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (SenderID,ReceiverID,SentDate),
    FOREIGN KEY (SenderID) REFERENCES spotify.dbo.Users(UserID),
    FOREIGN KEY (ReceiverID) REFERENCES spotify.dbo.Users(UserID)
);

CREATE TABLE spotify.dbo.Concerts (
    ConcertID INT PRIMARY KEY IDENTITY(1, 1),
    ArtistID INT,
    Title VARCHAR(100),
	NumberOfTkickets Int,
    Date DATE,
    Price DECIMAL(10, 2),
    IsCancelled BIT DEFAULT 0,
    FOREIGN KEY (ArtistID) REFERENCES spotify.dbo.Artists(ArtistID)
);

CREATE TABLE spotify.dbo.Tickets (
    UserID INT,
    ConcertID INT,
    PurchaseDate DATETIME2(3) DEFAULT CURRENT_TIMESTAMP,
    ExpiryDate DATE,
    IsExpired BIT DEFAULT 0,
	PRIMARY KEY (UserID,ConcertID),
    FOREIGN KEY (UserID) REFERENCES spotify.dbo.Users(UserID),
    FOREIGN KEY (ConcertID) REFERENCES spotify.dbo.Concerts(ConcertID)
);



CREATE TABLE spotify.dbo.Wallet(
	UserID INT,
	Balance INT,
	PRIMARY KEY (UserID,Balance),
	FOREIGN KEY (UserID) REFERENCES spotify.dbo.Users(UserID)
);




INSERT INTO spotify.dbo.Users (UserID, Username, PasswordHash, BirthDate, Email, Locationn, SubscriptionType)
VALUES 
(1, 'user1', 'hash1', '1990-01-01', 'user1@example.com', 'Location 1', 'Free'),
(2, 'user2', 'hash2', '1992-02-02', 'user2@example.com', 'Location 2', 'Premium'),
(3, 'user3', 'hash3', '1994-03-03', 'user3@example.com', 'Location 3', 'Free');

INSERT INTO spotify.dbo.Artists (ArtistID, UserID)
VALUES 
(1, 1),
(2, 2),
(3, 3);

INSERT INTO spotify.dbo.Albums (AlbumName, ArtistID, ReleaseDate)
VALUES 
('Album 1', 1, '2020-01-01'),
('Album 2', 2, '2021-02-02'),
('Album 3', 3, '2022-03-03');

INSERT INTO spotify.dbo.Songs (SongName, ArtistID, AlbumID, Genre, ReleaseDate, Lyrics)
VALUES 
('Song 1', 1, 1, 'Rock', '2020-01-01', 'Lyrics of Song 1'),
('Song 4', 2, 2, 'Pop', '2021-02-02', 'Lyrics of Song 4'),
('Song 5', 3, 2, 'Jazz', '2022-03-03', 'Lyrics of Song 5'),
('Song 6', 3, 3, 'Jazz', '2022-03-04', 'Lyrics of Song 6'),
('Song 7', 1, 1, 'Rock', '2020-01-11', 'Lyrics of Song 7'),
('Song 8', 2, 2, 'Pop', '2021-02-06', 'Lyrics of Song 8'),
('Song 9', 3, 3, 'Jazz', '2022-03-05', 'Lyrics of Song 9');

INSERT INTO spotify.dbo.Playlists (UserID, PlaylistName, IsPublic)
VALUES 
(1, 'Playlist 1', 1),
(2, 'Playlist 2', 0),
(3, 'Playlist 3', 1);

INSERT INTO spotify.dbo.PlaylistSongs (PlaylistID, SongID)
VALUES 
(1, 8),
(1, 7),
(2, 6),
(2, 4),
(3, 5);

INSERT INTO spotify.dbo.FavoriteList (UserID, ItemID, ItemType)
VALUES 
(1, 1, 'Song'),
(1, 1, 'Playlist'),
(2, 2, 'Song'),
(3, 3, 'Song'),
(3, 3, 'Playlist');

INSERT INTO spotify.dbo.Likes (UserID, ItemID, ItemType)
VALUES 
(1, 1, 'Song'),
(1, 2, 'Song'),
(1, 1, 'Album'),
(2, 3, 'Song'),
(2, 4, 'Song'),
(2, 2, 'Album'),
(3, 5, 'Song'),
(3, 3, 'Album');

INSERT INTO spotify.dbo.Comments (UserID, ItemID, ItemType, CommentText)
VALUES 
(1, 1, 'Song', 'Great song!'),
(2, 3, 'Song', 'Love this track.'),
(3, 5, 'Song', 'Awesome jazz piece.');

INSERT INTO spotify.dbo.FriendRequests (SenderRequestID, ReceiverRequestID, Status)
VALUES 
(1, 2, 'Accepted'),
(2, 3, 'Pending'),
(3, 1, 'Rejected');

INSERT INTO spotify.dbo.FollowList (FollowedID, FollowerID)
VALUES 
(1, 2),
(2, 3),
(3, 1);

INSERT INTO spotify.dbo.MessageList (SenderID, ReceiverID, MessageText)
VALUES 
(1, 2, 'Hello!'),
(2, 3, 'Hi there!'),
(3, 1, 'Good morning!');

INSERT INTO spotify.dbo.Concerts (ArtistID, Title,NumberOfTkickets,Date, Price)
VALUES 
(1, 'Concert 1', 10,'2023-01-01', 100.00),
(2, 'Concert 2', 10,'2023-02-02', 150.00),
(3, 'Concert 3', 10,'2023-03-03', 200.00);

INSERT INTO spotify.dbo.Tickets (UserID, ConcertID, ExpiryDate, IsExpired)
VALUES 
(1, 1, '2023-12-31', 0),
(2, 2, '2023-12-31', 0),
(3, 3, '2023-12-31', 0);

INSERT INTO spotify.dbo.Transactions (UserID, Amount, TransactionType)
VALUES 
(1, 50.00, 'Deposit'),
(2, 75.00, 'Deposit'),
(3, 100.00, 'Deposit');

INSERT INTO spotify.dbo.Wallet (UserID, Balance)
VALUES 
(1, 50),
(2, 75),
(3, 100);


