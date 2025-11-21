with q1 as (
    select
        g.gameID,
        g.bowlerID,
        g.ballID,
        g.game_num,
        g.score,
        case
            when g.practiceid is not null then p.event_date
            when g.leagueid is not null then l.event_date
            else t.event_date
        end event_date
    from game g
    left join practice p on p.practiceID = g.practiceID
    left join league l on l.leagueID = g.leagueID
    left join tournament t on t.tournamentID = g.tournamentID
    order by bowlerID, event_date, game_num
)

select
    bowlerID,
    event_date,
    avg(score) avg_score
from q1
group by bowlerid, event_date
order by bowlerid, event_date
;
