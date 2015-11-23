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

-- select * from winLossPlayed where no_of_Matches = (select min(no_of_Matches) from winLossPlayed);
-- select * from players;

create view wins2 as
select id, count(matches.winner) as wins from players left join matches on players.id = matches.winner group by players.id;

create view losses2 as
select id, count(matches.loser) as losses from players left join matches on players.id = matches.loser group by players.id;