user_table = """
    create table if not exists "public"."user"
    (
        id                  serial
                constraint user_pk
                    primary key,
        name                varchar(20)              not null,
        account             varchar(20)              not null,
        address             varchar(100),
        sex                 varchar(1)               not null,
        phone               varchar(20),
        token               varchar(100)             not null,
        password            varchar(100)             not null,
        email               varchar(20),
        state               boolean default false    not null,
        role                smallint default 1       not null,
        application_time    timestamp with time zone not null,
        last_login_time     timestamp with time zone, 
        last_logout_time    timestamp with time zone,
        update_time         timestamp with time zone,
        "desc"              varchar(400),
        try_count           smallint default 0       not null,
        locked_time         timestamp with time zone,
        first_try_time      timestamp with time zone,
        commitment_letter   smallint                 not null
    );
    alter table "public"."user" owner to postgres;
"""
