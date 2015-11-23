CREATE DATABASE tournament;

CREATE TABLE players(id SERIAL primary key, name text);

CREATE TABLE matches(
winner integer references players(id),
loser integer references players(id),
);

CREATE VIEW wins AS
SELECT id, count(matches.winner) AS wins FROM players LEFT JOIN matches ON players.id = matches.winner GROUP BY players.id;

CREATE VIEW losses AS
SELECT id, count(matches.loser) AS losses FROM players LEFT JOIN matches ON players.id = matches.loser GROUP BY players.id;

CREATE VIEW winLossPlayed AS
SELECT
	losses.lossesID AS id,
	name,
	wins.noOfWins AS wins,
	losses.noOfLosses AS losses,
	wins.noOfWins + losses.noOfLosses AS no_of_Matches
FROM losses, wins, players
WHERE
	losses.lossesID = wins.winsID
	AND
	players.id = losses.lossesID
ORDER BY wins DESC;