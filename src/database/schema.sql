CREATE TABLE "ChamadosProcon" (
	"id" serial PRIMARY KEY,
	"dataAtendimento" DATE NOT NULL,
	"codigoRegiao" integer NOT NULL,
	"nomeRegiao" varchar NOT NULL,
	"ufRegiao" varchar NOT NULL,
	"codigoTipoAtendimento" integer NOT NULL,
	"descricaoAtendimento" varchar NOT NULL,
	"codigoAssunto" integer NOT NULL,
	"descricaoAssunto" varchar NOT NULL,
	"codigoProblema" varchar NOT NULL,
	"descricaoProblema" varchar NOT NULL,
	"sexo" varchar(1) NOT NULL,
	"faixaEtaria" varchar NOT NULL,
	"cep" varchar NOT NULL
) WITH (
  OIDS=FALSE
);


CREATE TABLE "Periodo" (
	"dataAtendimento" DATE NOT NULL
) WITH (
  OIDS=FALSE
);


CREATE TABLE "Regiao" (
	"codigoRegiao" integer NOT NULL,
	"nomeRegiao" varchar NOT NULL,
	"ufRegiao" varchar NOT NULL
) WITH (
  OIDS=FALSE
);



CREATE TABLE "TipoAtendimento" (
	"codigoTipoAtendimento" integer NOT NULL,
	"descricaoAtendimento" varchar NOT NULL
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Assunto" (
	"codigoAssunto" integer NOT NULL,
	"descricaoAssunto" varchar NOT NULL
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Problema" (
	"codigoProblema" varchar NOT NULL,
	"descricaoProblema" varchar NOT NULL
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Consumidor" (
	"sexo" varchar(1) NOT NULL,
	"faixaEtaria" varchar NOT NULL,
	"cep" varchar NOT NULL
) WITH (
  OIDS=FALSE
);