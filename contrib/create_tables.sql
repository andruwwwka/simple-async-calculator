CREATE TABLE tasks (
    id          SERIAL                      PRIMARY KEY,
    created     TIMESTAMP WITH TIME ZONE    NOT NULL,
    updated     TIMESTAMP WITH TIME ZONE    NOT NULL,
    x           INTEGER                     NOT NULL,
    y           INTEGER                     NOT NULL,
    operator    VARCHAR(1)                  NOT NULL,
    status      VARCHAR(10)                 NOT NULL,
    result      DECIMAL
);