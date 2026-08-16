create domain likert_score as smallint
check (value between 1 and 5);

create table forms (
    id uuid primary key default gen_random_uuid(),

    cb_01 likert_score not null,
    cb_02 likert_score not null,
    cb_03 likert_score not null,
    cb_04 likert_score not null,
    cb_05 likert_score not null,
    cb_06 likert_score not null,
    cb_07 likert_score not null,
    cb_08 likert_score not null,
    cb_09 likert_score not null,

    fomo_01 likert_score not null,
    fomo_02 likert_score not null,
    fomo_03 likert_score not null,
    fomo_04 likert_score not null,
    fomo_05 likert_score not null,
    fomo_06 likert_score not null,
    fomo_07 likert_score not null,
    fomo_08 likert_score not null,
    fomo_09 likert_score not null,
    fomo_10 likert_score not null,

    csct_01 likert_score not null,
    csct_02 likert_score not null,
    csct_03 likert_score not null,
    csct_04 likert_score not null,
    csct_05 likert_score not null,
    csct_06 likert_score not null,
    csct_07 likert_score not null,

    created_at timestamptz not null default now()
);

create table predictions (
    form_id uuid primary key references forms(id),

    pais_01 likert_score not null,
    pais_02 likert_score not null,
    pais_03 likert_score not null,
    pais_04 likert_score not null,
    pais_05 likert_score not null,
    pais_06 likert_score not null,
    pais_07 likert_score not null,
    pais_avg real not null,

    model text not null,

    created_at timestamptz not null default now()
);

grant select, insert, update, delete on table forms to anon, authenticated;
grant select, insert, update, delete on table predictions to anon, authenticated;