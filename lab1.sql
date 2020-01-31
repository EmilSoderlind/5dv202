/*
   Fill in the queries between the "SELECT QUERY#" and "SELECT END" 
   If there are any uncertainties contact Klas (klasa@cs.umu.se)
*/

SELECT 'Query 1';
-- Select names of all the programs aired on channel 'P1'
-- VÃ¤lj namnen fÃ¶r alla program som sÃ¤nds pÃ¥ kanalen 'P1'
SELECT program.name FROM program,channel WHERE program.channel=channel.channel_id AND channel.name='P1' ;
SELECT 'END';


SELECT 'Query 2';
-- Select name of all programs with the category 'Humor' on channel 'P1' 
-- VÃ¤lj namnen av alla program med kategori 'Humor' pÃ¥ kanalen 'P1' 
SELECT program.name FROM program,channel,category WHERE program.channel=channel.channel_id AND channel.name='P1' AND program.category=category.category_id AND category.name = 'Humor';
SELECT 'END';


SELECT 'Query 3';
-- Select program name and category of all programs with which are not 'Humor' programs aired on channel 'P2' 
-- VÃ¤lj programnamn och kateogorinamn av alla program som inte Ã¤r av kategorien 'Humor' och sÃ¤nds pÃ¥ kanal 'P2'
SELECT program.name,category.name FROM program,channel,category WHERE program.channel=channel.channel_id AND channel.name='P2' AND program.category=category.category_id AND category.name != 'Humor';
SELECT 'END';


SELECT 'Query 4';
-- Select editors and total time of their broadcasts, ordered from most to least total time
-- VÃ¤lj redaktÃ¶r samt total tid av deras broadcasts, sorterat pÃ¥ total tid sjunkande
SELECT program.editor,SUM(broadcast.duration) AS total_time FROM program,broadcast WHERE program.program_id=broadcast.program GROUP BY program.editor ORDER BY SUM(broadcast.duration) DESC;
SELECT 'END';


SELECT 'Query 5';
--List the top five editors by how many distinct categories they have worked on. When you present the list, give the editor name, the number of categories they have worked on. Order by the number of categories from most to least for these 5 most versatile editors. 
-- Lista de fem fÃ¶rsta redaktÃ¶rerna samt hur mÃ¥nga distinkta kategorier de har jobbat med. Presentera det som redakÃ¶rens namn, samt hur mÃ¥nga kategorier hen har jobbat pÃ¥, lista de fem med flest kategorier. 
SELECT foo.editor, count(foo.editor) from (SELECT program.editor FROM program,broadcast WHERE program.program_id=broadcast.program GROUP BY program.editor,program.category ORDER BY program.editor) as foo GROUP BY foo.editor ORDER BY count(foo.editor) DESC limit 5;
SELECT 'END';


SELECT 'Query 6';
-- Select average broadcast duration of all broadcasts on channel 'P2'
-- VÃ¤lj den genomsnittliga sÃ¤ndningstiden fÃ¶r alla sÃ¤ndingar pÃ¥ kanalen 'P2'
SELECT AVG(broadcast.duration) from broadcast,program,channel WHERE broadcast.program=program.program_id AND program.channel=channel.channel_id AND channel.name='P2';
SELECT 'END';


SELECT 'Query 7';
-- Select editors who have worked on the same channels as 'Magnus Quick' but never on channel 'P1'
-- VÃ¤lj redaktÃ¶rer som har jobbat pÃ¥ samma kanaler som 'Magnus Quick' men aldrig pÃ¥ kanal 'P1'
SELECT distinct program.editor FROM program,channel, (SELECT channel.channel_id FROM channel,program WHERE channel.channel_id=program.channel AND program.editor='Magnus Quick') as magCh WHERE program.channel=channel.channel_id AND channel.channel_id=magCh.channel_id EXCEPT SELECT distinct program.editor FROM program,channel WHERE program.channel=channel.channel_id AND channel.name='P1';
SELECT 'END';


SELECT 'Query 8';
-- Select total amount of time channel P2 spend on broadcasting programs starting between 01:00 and 09:00 grouped by category. (broadcastDate >= 01:00, broadcastDate <= 9:00)
-- VÃ¤lj totala tiden kanal 'P2' sÃ¤nder program som startar mellan 01:00 och 09:00 grupperat efter kategori. (broadcastDate >= 01:00, broadcastDate <= 9:00)

select sum(broadcast.duration), category.name from channel, broadcast, program, category where CAST(broadcast.broadcast_date as TIME) >= '01:00' AND CAST(broadcast.broadcast_date as TIME) <= '09:00' AND category.category_id = program.category AND broadcast.program = program.program_id AND program.channel = channel.channel_id AND channel.name = 'P2' GROUP BY category.name, category.name order by category.name;


SELECT 'END';


 
SELECT 'Query 9';
-- Select average starting time on the exact format '(hour:minute)' of all broadcasts with the category 'Nyheter' or 'Drama'
-- VÃ¤lj den genomsnittliga starttiden med det exakta formatet '(timme:minut)' av alla sÃ¤ndingar med kategorin 'Nyheter' eller 'Drama'

select to_char(avg(cast(broadcast.broadcast_date as TIME)), 'HH24:MI') from broadcast, program, category where category.category_id = program.category AND broadcast.program = program.program_id
AND (category.name = 'Drama' OR category.name = 'Nyheter');

SELECT 'END';



SELECT 'Query 10';
-- An editor works alongside another editor if they both work on programs at the same chanel. An editor is in the community of another editor if there is a chain of editors where each link in the chain work alongside each other. So if Alice works alongside Bob, and Bob works alongside Charlie, and Charlie works alongside Dan, then all these four editors are in the symmetric relation "same community". Hint: Use recursion.

-- Select the distinct editors in the community of 'Magnus Quick'. Hints: 'Ole Isak Mienna is not in, but 'Nina Glans' is. (71 people), use recursion
-- VÃ¤lj ut de distinkta redakÃ¶rerna i gemenskapen av 'Magnus Quick'. Tips: 'Ole Isak Mienna' Ã¤r inte med, men t.ex 'Nina Glans' Ã¤r det. (71 st), anvÃ¤nd rekursion

with recursive MQ_chain as (
	select program.editor, program.channel
	from program
	where program.editor = 'Magnus Quick'
	union
		select child.editor, child.channel
		from program as child
	join MQ_chain on (MQ_chain.channel = child.channel) OR (MQ_chain.editor = child.editor)
)
select distinct MQ_chain.editor
from MQ_chain ORDER BY MQ_chain.editor;
SELECT 'END';

