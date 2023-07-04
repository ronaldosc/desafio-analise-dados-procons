CREATE TABLE "Regiao" (
	"idRegiao" serial PRIMARY KEY,
	"nomeRegiao" varchar NOT NULL,
	"ufRegiao" varchar NOT NULL
) WITH (
  OIDS=FALSE
);



CREATE TABLE "TipoAtendimento" (
	"idTipoAtendimento" serial PRIMARY KEY,
	"descricaoAtendimento" varchar NOT NULL
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Assunto" (
	"idAssunto" serial PRIMARY KEY,
	"descricaoAssunto" varchar NOT NULL
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Problema" (
	"idProblema" serial PRIMARY KEY,
	"descricaoProblema" varchar NOT NULL
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Atendimento" (
	"idAtendimento" serial PRIMARY KEY,
	"sexo" varchar(1) NOT NULL,
	"faixaEtaria" varchar NOT NULL,
	"cep" varchar NOT NULL,
	"dataAtendimento" DATE NOT NULL,
	"idRegiao" serial NOT NULL,
	"idTipoAtendimento" serial NOT NULL,
	"idAssunto" serial NOT NULL,
	"idProblema" serial NOT NULL
) WITH (
  OIDS=FALSE
);



ALTER TABLE "Atendimento" ADD CONSTRAINT "Atendimento_fk0" FOREIGN KEY ("idRegiao") REFERENCES "Regiao"("idRegiao");
ALTER TABLE "Atendimento" ADD CONSTRAINT "Atendimento_fk1" FOREIGN KEY ("idTipoAtendimento") REFERENCES "TipoAtendimento"("idTipoAtendimento");
ALTER TABLE "Atendimento" ADD CONSTRAINT "Atendimento_fk2" FOREIGN KEY ("idAssunto") REFERENCES "Assunto"("idAssunto");
ALTER TABLE "Atendimento" ADD CONSTRAINT "Atendimento_fk3" FOREIGN KEY ("idProblema") REFERENCES "Problema"("idProblema");