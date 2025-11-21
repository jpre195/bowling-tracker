drop table if exists arsenal;
drop table if exists game;
drop table if exists bowler;
drop table if exists ball;
drop table if exists practice;
drop table if exists league;
drop table if exists tournament;
drop table if exists house;

drop sequence if exists bowler_sequence;
drop sequence if exists ball_sequence;
drop sequence if exists house_sequence;
drop sequence if exists practice_sequence;
drop sequence if exists league_sequence;
drop sequence if exists tournament_sequence;
drop sequence if exists game_sequence;

create sequence bowler_sequence start 1;
create sequence ball_sequence start 1;
create sequence house_sequence start 1;
create sequence practice_sequence start 1;
create sequence league_sequence start 1;
create sequence tournament_sequence start 1;
create sequence game_sequence start 1;

create table bowler (
    bowlerID integer primary key default nextval('bowler_sequence'),
    bowler_name varchar(128) not null,
    dob date,
    hand varchar(32) not null check (hand in ('1HR','1HL','2HR','2HL'))
);

create table ball (
    ballID integer primary key default nextval('ball_sequence'),
    brand varchar(32) not null,
    ball_name varchar(64) not null,
    coverstock varchar(64) check (coverstock in ('Solid', 'Hybrid', 'Pearl', 'Urethane')),
    rg double not null check (rg > 0),
    diff double not null check (diff > 0),
    int_diff double
);

create table arsenal (
    bowlerID integer not null references bowler(bowlerID),
    ballID integer  not null references ball(ballID),
    primary key (bowlerID, ballID)
);

create table house (
    houseID integer primary key default nextval('house_sequence'),
    house_name varchar(128)
);

create table practice (
    practiceID integer primary key default nextval('practice_sequence'),
    houseID integer not null references house(houseID),
    event_date date
);

create table league (
    leagueID integer primary key default nextval('league_sequence'),
    houseID integer not null references house(houseID),
    season varchar(32),
    event_date date,
    league_name varchar(128)
);

create table tournament (
    tournamentID integer primary key default nextval('tournament_sequence'),
    houseID integer not null references house(houseID),
    event_date date,
    tournament_name varchar(128)
);

create table game (
    gameID integer primary key default nextval('game_sequence'),
    bowlerID integer not null references bowler(bowlerID),
    ballID integer not null references ball(ballID),
    practiceID integer references practice(practiceID),
    leagueID integer references league(leagueID),
    tournamentID integer references tournament(tournamentID),
    game_num integer not null,
    score integer,
    check (
        (case when practiceID is not null then 1 else 0 end)
        + (case when leagueID is not null then 1 else 0 end)
        + (case when tournamentID is not null then 1 else 0 end) = 1
    )
);

insert into bowler(bowler_name, dob, hand) values
    ('Jeff Preston', '1989-10-19', '2HR'),
    ('Lillian Preston', '2014-09-08', '2HR');

insert into ball(brand, ball_name, coverstock, rg, diff, int_diff) values
    ('Storm', 'Phaze II', 'Hybrid', 2.49, 0.048, 0.040),
    ('Brunswick', 'Kingpin Crush', 'Pearl', 2.56, 0.052, NULL);

insert into house(house_name) values
    ('Clermont Lanes'),
    ('Lakeside Lanes');

insert into practice(houseID, event_date) values
    (1, '2025-11-10'),
    (2, '2025-11-15');

insert into league(houseID, season, event_date, league_name) values
    (1, '2025', '2025-10-20', 'Tuesday Night Mixed');

insert into tournament(houseID, event_date, tournament_name) values
    (2, '2025-09-05', 'All-Star Open');

insert into arsenal(bowlerID, ballID) values
    (1, 1),
    (1, 2),
    (2, 2);

insert into game(bowlerID, ballID, practiceID, leagueID, tournamentID, game_num, score) values
    (1, 1, 1, NULL, NULL, 1, 200),
    (1, 1, 1, NULL, NULL, 2, 300),
    (1, 2, 1, NULL, NULL, 3, 250),
    (2, 2, NULL, 1, NULL, 1, 215),
    (2, 2, NULL, NULL, 1, 1, 180),
    (2, 2, NULL, NULL, 1, 1, 180);
