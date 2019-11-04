/* Welcome to the SQL mini project. For this project, you will use
Springboard' online SQL platform.

The data you need is in the "country_club" database. This database
contains 3 tables:
    i) the "Bookings" table,
    ii) the "Facilities" table, and
    iii) the "Members" table.

  Bookings
    bookid -- PK
    facid
    memid
    starttime
    slots
  Facilities
    facid -- PK
    name
    membercost
    guestcost
    initialoutlay
    monthlymaintenance
  Members
    memid -- PK
    surname
    firstname
    address
    zipcode
    telephone
    recomendedby
    joindate
*/

/* Q1: Some of the facilities charge a fee to members, but some do not.
Please list the names of the facilities that do. */
select name
  from Facilities
  where membercost > 0 ;

/* Q2: How many facilities do not charge a fee to members? */
select count(*)
  from Facilities
  where membercost = 0 ;

/* Q3: How can you produce a list of facilities that charge a fee to members,
where the fee is less than 20% of the facility's monthly maintenance cost?
Return the facid, facility name, member cost, and monthly maintenance of the
facilities in question. */
select  facid,
        name,
        membercost,
        monthlymaintenance
  from Facilities
  where membercost > 0
    and monthlymaintenance * 0.2 > membercost ;

/* Q4: How can you retrieve the details of facilities with ID 1 and 5?
Write the query without using the OR operator. */
select *
  from Facilities
  where facid in (1,5) ;

/* Q5: How can you produce a list of facilities, with each labelled as
'cheap' or 'expensive', depending on if their monthly maintenance cost is
more than $100? Return the name and monthly maintenance of the facilities
in question. */
select  name,
        monthlymaintenance,
        case when monthlymaintenance > 100 then 'expensive'
             else 'cheap'
             end as cost
  from Facilities ;

/* Q6: You'd like to get the first and last name of the last member(s)
who signed up. Do not use the LIMIT clause for your solution. */
select  firstname,
        surname
  from Members
  where surname <> 'GUEST'
    and joindate = (
      select max(joindate)
        from Members
        where surname <> 'GUEST'
    ) ;

/* Q7: How can you produce a list of all members who have used a tennis court?
Include in your output the name of the court, and the name of the member
formatted as a single column. Ensure no duplicate data, and order by
the member name. */
select  distinct
        f.name,
        concat(m.surname, ", ", m.firstname) as user
  from Bookings b
  inner join Facilities f
    on f.facid = b.facid
  inner join Members m
    on b.memid = m.memid
  where f.name like 'Tennis Court%'
    and m.surname <> 'GUEST'
  order by m.surname, m.firstname ;

/* Q8: How can you produce a list of bookings on the day of 2012-09-14 which
will cost the member (or guest) more than $30? Remember that guests have
different costs to members (the listed costs are per half-hour 'slot'), and
the guest user's ID is always 0. Include in your output the name of the
facility, the name of the member formatted as a single column, and the cost.
Order by descending cost, and do not use any subqueries. */
select  f.name,
        concat(m.surname, ", ", m.firstname) as user,
        case when m.surname = 'GUEST' then f.guestcost
          else f.membercost
          end * b.slots as cost
  from Bookings b
  inner join Facilities f
    on b.facid = f.facid
  inner join Members m
    on b.memid = m.memid
  where cast(b.starttime as date) = '2012-09-14'
    and case when m.surname = 'GUEST' then f.guestcost else f.membercost end * b.slots > 30
  order by 3 desc ;

/* Q9: This time, produce the same result as in Q8, but using a subquery. */
select *
  from (
    select  f.name,
            concat(m.surname, ", ", m.firstname) as user,
            case when m.surname = 'GUEST' then f.guestcost
              else f.membercost
              end * b.slots as cost
    from Bookings b
    inner join Facilities f
    on b.facid = f.facid
    inner join Members m
    on b.memid = m.memid
    where cast(b.starttime as date) = '2012-09-14'
  ) x
  where x.cost > 30
  order by x.cost desc ;

/* Q10: Produce a list of facilities with a total revenue less than 1000.
The output of facility name and total revenue, sorted by revenue. Remember
that there's a different cost for guests and members! */
select *
  from (
    select  f.name,
            sum(case when b.memid = 0 then f.guestcost
              else f.membercost
              end * b.slots
            ) as revenue
      from Bookings b
      inner join Facilities f
        on b.facid = f.facid
      group by f.name
  ) x
  where x.revenue < 1000 ;
