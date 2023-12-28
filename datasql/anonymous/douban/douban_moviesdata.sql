create table if not exists douban_moviesdata
(
    movie        varchar(255) null,
    actors       varchar(255) null,
    directors    longtext     null,
    douban_score float        null,
    douban_votes int          null,
    genre        varchar(255) null,
    languages    varchar(255) null,
    duration     int          null,
    regions      varchar(255) null,
    release_date varchar(255) null,
    storyline    longtext     null,
    tags         longtext     null,
    year         int          null
);



