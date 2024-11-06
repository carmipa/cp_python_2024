-- Gerado por Oracle SQL Developer Data Modeler 23.1.0.087.0806
--   em:        2024-11-06 12:59:33 BRT
--   site:      Oracle Database 21c
--   tipo:      Oracle Database 21c


-- predefined type, no DDL - MDSYS.SDO_GEOMETRY

-- predefined type, no DDL - XMLTYPE

CREATE TABLE cargos (
    cargo_id           INTEGER NOT NULL,
    cargo_descricao    VARCHAR2(45) NOT NULL,
    cargo_departamento VARCHAR2(30) NOT NULL
)
ORGANIZATION HEAP NOCOMPRESS
    NOCACHE
        NOPARALLEL
    NOROWDEPENDENCIES DISABLE ROW MOVEMENT;

ALTER TABLE cargos
    ADD CONSTRAINT cargos_pk PRIMARY KEY ( cargo_id ) NOT DEFERRABLE ENABLE VALIDATE;

CREATE SEQUENCE cargos_cargo_id_seq
    START WITH 1
    INCREMENT BY 1
    NOMINVALUE
    NOMAXVALUE
    NOCYCLE
    NOCACHE
    ORDER;

CREATE OR REPLACE TRIGGER cargos_cargo_id_trg
BEFORE INSERT ON cargos
FOR EACH ROW
WHEN ( new.cargo_id IS NULL )
BEGIN
    :new.cargo_id := cargos_cargo_id_seq.nextval;
END;
/

CREATE TABLE funcionarios (
    funcionario_id      INTEGER NOT NULL,
    funcionario_cpf     INTEGER NOT NULL,
    funcionario_nome    VARCHAR2(50) NOT NULL,
    funcionario_salario FLOAT NOT NULL,
    funcionario_integer INTEGER NOT NULL,
    cargos_cargo_id     INTEGER NOT NULL
)
ORGANIZATION HEAP NOCOMPRESS
    NOCACHE
        NOPARALLEL
    NOROWDEPENDENCIES DISABLE ROW MOVEMENT;

ALTER TABLE funcionarios
    ADD CONSTRAINT funcionarios_pk PRIMARY KEY ( funcionario_id ) NOT DEFERRABLE ENABLE VALIDATE;

ALTER TABLE funcionarios
    ADD CONSTRAINT funcionarios_cargos_fk FOREIGN KEY ( cargos_cargo_id )
        REFERENCES cargos ( cargo_id );

CREATE SEQUENCE funcionarios_funcionario_id
    START WITH 1
    INCREMENT BY 1
    NOMINVALUE
    NOMAXVALUE
    NOCYCLE
    NOCACHE
    ORDER;

CREATE OR REPLACE TRIGGER funcionarios_funcionario_id
BEFORE INSERT ON funcionarios
FOR EACH ROW
WHEN ( new.funcionario_id IS NULL )
BEGIN
    :new.funcionario_id := funcionarios_funcionario_id.nextval;
END;
/

-- Criação de índices para chaves estrangeiras

CREATE INDEX funcionarios_cargos_fk_idx
    ON funcionarios ( cargos_cargo_id );

-- Relatório do Resumo do Oracle SQL Developer Data Modeler:
--
-- CREATE TABLE                             2
-- CREATE INDEX                             1
-- ALTER TABLE                              3
-- CREATE VIEW                              0
-- ALTER VIEW                               0
-- CREATE PACKAGE                           0
-- CREATE PACKAGE BODY                      0
-- CREATE PROCEDURE                         0
-- CREATE FUNCTION                          0
-- CREATE TRIGGER                           2
-- ALTER TRIGGER                            0
-- CREATE COLLECTION TYPE                   0
-- CREATE STRUCTURED TYPE                   0
-- CREATE STRUCTURED TYPE BODY              0
-- CREATE CLUSTER                           0
-- CREATE CONTEXT                           0
-- CREATE DATABASE                          0
-- CREATE DIMENSION                         0
-- CREATE DIRECTORY                         0
-- CREATE DISK GROUP                        0
-- CREATE ROLE                              0
-- CREATE ROLLBACK SEGMENT                  0
-- CREATE SEQUENCE                          2
-- CREATE MATERIALIZED VIEW                 0
-- CREATE MATERIALIZED VIEW LOG             0
-- CREATE SYNONYM                           0
-- CREATE TABLESPACE                        0
-- CREATE USER                              0
--
-- DROP TABLESPACE                          0
-- DROP DATABASE                            0
--
-- REDACTION POLICY                         0
--
-- ORDS DROP SCHEMA                         0
-- ORDS ENABLE SCHEMA                       0
-- ORDS ENABLE OBJECT                       0
--
-- ERRORS                                   0
-- WARNINGS                                 0
