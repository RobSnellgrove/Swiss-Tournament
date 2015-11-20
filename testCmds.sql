-- drop view winLossPlayed;

-- create view winLossPlayed as
-- select
-- 	losses.lossesID as id,
-- 	name,
-- 	wins.noOfWins as wins,
-- 	losses.noOfLosses as losses,
-- 	wins.noOfWins + losses.noOfLosses as no_of_Matches
-- from losses, wins, players
-- where
-- 	losses.lossesID = wins.winsID
-- 	and
-- 	players.id = losses.lossesID
-- order by wins desc;

select * from winLossPlayed where no_of_Matches = (select min(no_of_Matches) from winLossPlayed);