CREATE TABLE participants (
    id integer primary key autoincrement not null,
    userhash text not null,
    gender text not null,
    age integer not null, 
    handedness text not null,
    created text not null
);

CREATE TABLE trials (
    id integer primary key autoincrement not null,
    participant_id integer not null references participants(id),
    session_num integer not null,
    block_num integer not null,
    trial_num integer not null,
    timestamp text not null,
    rt text not null
);


CREATE TABLE frames (
	id integer primary key autoincrement not null,
	participant_id text not null,
	session_num integer not null,
	block_num integer not null,
	trial_num integer not null,
	timestamp text not null,
	buffeting_force integer not null,
	user_input integer not null,
	displacement integer not null,
	PVT_occurring text not null,
	rt text not null
);

CREATE TABLE assessments (
	id integer primary key autoincrement not null,
	participant_id text not null,
    session_num integer not null,
	block_num integer not null,
	trial_num integer not null,
	timestamp text not null,
	mean_rt text not null,
	lapses integer not null,
	samples integer not null
)

