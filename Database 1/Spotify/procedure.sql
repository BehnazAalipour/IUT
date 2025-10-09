USE spotify;
GO

CREATE TRIGGER updateWallet
ON spotify.dbo.Users
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO spotify.dbo.Wallet (UserID, Balance)
    SELECT UserID, 0
    FROM inserted;
END;

CREATE TRIGGER CancelConcert
ON spotify.dbo.Concerts
AFTER UPDATE
AS
BEGIN
    DECLARE @ConcertID INT
    DECLARE @Price DECIMAL(10, 2)

    -- Check if the update includes cancellation of a concert
    IF EXISTS (SELECT * FROM inserted WHERE IsCancelled = 1 AND IsCancelled <> (SELECT IsCancelled FROM deleted))
    BEGIN
        -- Get the ConcertID and Price of the cancelled concert
        SELECT @ConcertID = ConcertID, @Price = Price FROM inserted WHERE IsCancelled = 1
        
        -- Update the Wallet balances for users who purchased tickets for the cancelled concert
        UPDATE w
        SET w.Balance = w.Balance + @Price
        FROM spotify.dbo.Wallet w
        INNER JOIN spotify.dbo.Tickets t ON w.UserID = t.UserID
        WHERE t.ConcertID = @ConcertID

        -- Mark the tickets as expired
        UPDATE spotify.dbo.Tickets
        SET IsExpired = 1
        WHERE ConcertID = @ConcertID
    END
END


CREATE TRIGGER updateFollowList
ON spotify.dbo.FriendRequests
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    -- Check if the status has been changed to 'Accepted' from 'Pending'
    IF EXISTS (
        SELECT 1
        FROM inserted i
        JOIN deleted d ON i.SenderRequestID = d.SenderRequestID AND i.ReceiverRequestID = d.ReceiverRequestID
        WHERE d.Status = 'Pending' AND i.Status = 'Accepted'
    )
    BEGIN
        -- Insert into FollowList
        INSERT INTO spotify.dbo.FollowList (FollowedID, FollowerID)
        SELECT i.ReceiverRequestID, i.SenderRequestID
        FROM inserted i
        WHERE i.Status = 'Accepted';
	end
end

CREATE TRIGGER trg_DeleteSongsOnAlbumDelete
ON spotify.dbo.Albums
INSTEAD OF DELETE
AS
BEGIN
    DELETE FROM spotify.dbo.Songs
    WHERE AlbumID IN (SELECT AlbumID FROM DELETED);

    DELETE FROM spotify.dbo.Albums
    WHERE AlbumID IN (SELECT AlbumID FROM DELETED);
END;



select * from spotify.dbo.Wallet
select * from spotify.dbo.Users
select * from spotify.dbo.FriendRequests
select * from spotify.dbo.MessageList
select * from spotify.dbo.FollowList
select * from spotify.dbo.Concerts
select * from spotify.dbo.Tickets
select * from spotify.dbo.Artists
select * from spotify.dbo.Albums
select * from spotify.dbo.Songs
select * from spotify.dbo.Likes
select * from spotify.dbo.Comments
select * from spotify.dbo.Users


DELETE FROM spotify.dbo.Users;
DELETE FROM spotify.dbo.FriendRequests;
DELETE FROM spotify.dbo.Wallet;
DELETE FROM spotify.dbo.Artists;
DELETE FROM spotify.dbo.Songs;
DELETE FROM spotify.dbo.Albums;
DELETE FROM spotify.dbo.FollowList;
DELETE FROM spotify.dbo.MessageList;
DELETE FROM spotify.dbo.Concerts;
