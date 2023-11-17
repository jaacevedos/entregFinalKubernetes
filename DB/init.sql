CREATE SEQUENCE actor_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."actor" (
    "id" integer DEFAULT nextval('actor_id_seq') NOT NULL,
    "name" character varying,
    "film_id" integer NOT NULL,
    CONSTRAINT "actor_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

CREATE SEQUENCE cinema_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."cinema" (
    "id" integer DEFAULT nextval('cinema_id_seq') NOT NULL,
    "name" character varying,
    "film_id" integer NOT NULL,
    CONSTRAINT "cinema_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


CREATE TABLE "public"."alembic_version" (
    "version_num" character varying(32) NOT NULL,
    CONSTRAINT "alembic_version_pkc" PRIMARY KEY ("version_num")
) WITH (oids = false);


CREATE SEQUENCE film_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."film" (
    "id" integer DEFAULT nextval('film_id_seq') NOT NULL,
    "title" character varying,
    "length" integer,
    "year" integer,
    "director" character varying,
    CONSTRAINT "film_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


ALTER TABLE ONLY "public"."actor" ADD CONSTRAINT "actor_film_id_fkey" FOREIGN KEY (film_id) REFERENCES film(id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."cinema" ADD CONSTRAINT "cinema_film_id_fkey" FOREIGN KEY (film_id) REFERENCES film(id) NOT DEFERRABLE;