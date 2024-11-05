-- Gerado por Oracle SQL Developer Data Modeler 23.1.0.087.0806
--   em:        2024-11-05 09:54:47 BRT
--   site:      Oracle Database 21c
--   tipo:      Oracle Database 21c



-- Gerado por Oracle SQL Developer Data Modeler 23.1.0.087.0806
--   em:        2024-11-05 09:54:47 BRT
--   site:      Oracle Database 21c
--   tipo:      Oracle Database 21c


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

CREATE TABLE d_f (
    cf_id                       INTEGER NOT NULL,
    cargos_cargo_id             INTEGER NOT NULL,
    funcionarios_funcionario_id INTEGER NOT NULL
)
ORGANIZATION HEAP NOCOMPRESS
    NOCACHE
        NOPARALLEL
    NOROWDEPENDENCIES DISABLE ROW MOVEMENT;

ALTER TABLE d_f
    ADD CONSTRAINT d_f_pk PRIMARY KEY ( cf_id,
                                        cargos_cargo_id,
                                        funcionarios_funcionario_id ) NOT DEFERRABLE ENABLE VALIDATE;

CREATE TABLE funcionarios (
    funcionario_id      INTEGER NOT NULL,
    funcionario_cpf     INTEGER NOT NULL,
    funcionario_nome    VARCHAR2(50) NOT NULL,
    funcionario_salario FLOAT NOT NULL,
    funcionario_integer INTEGER NOT NULL
)
ORGANIZATION HEAP NOCOMPRESS
    NOCACHE
        NOPARALLEL
    NOROWDEPENDENCIES DISABLE ROW MOVEMENT;

ALTER TABLE funcionarios
    ADD CONSTRAINT funcionarios_pk PRIMARY KEY ( funcionario_id ) NOT DEFERRABLE ENABLE VALIDATE;

ALTER TABLE d_f
    ADD CONSTRAINT d_f_cargos_fk FOREIGN KEY ( cargos_cargo_id )
        REFERENCES cargos ( cargo_id );

ALTER TABLE d_f
    ADD CONSTRAINT d_f_funcionarios_fk FOREIGN KEY ( funcionarios_funcionario_id )
        REFERENCES funcionarios ( funcionario_id );

CREATE SEQUENCE cargos_cargo_id_seq START WITH 1 INCREMENT BY 1 NOMINVALUE NOMAXVALUE NOCYCLE NOCACHE ORDER;

CREATE OR REPLACE TRIGGER cargos_cargo_id_trg BEFORE
    INSERT ON cargos
    FOR EACH ROW
    WHEN ( new.cargo_id IS NULL )
BEGIN
    :new.cargo_id := cargos_cargo_id_seq.nextval;
END;
/

CREATE SEQUENCE d_f_cf_id_seq START WITH 1 INCREMENT BY 1 NOMINVALUE NOMAXVALUE NOCYCLE NOCACHE ORDER;

CREATE OR REPLACE TRIGGER d_f_cf_id_trg BEFORE
    INSERT ON d_f
    FOR EACH ROW
    WHEN ( new.cf_id IS NULL )
BEGIN
    :new.cf_id := d_f_cf_id_seq.nextval;
END;
/

CREATE SEQUENCE funcionarios_funcionario_id_seq START WITH 1 INCREMENT BY 1 NOMINVALUE NOMAXVALUE NOCYCLE NOCACHE ORDER;

CREATE OR REPLACE TRIGGER funcionarios_funcionario_id_trg BEFORE
    INSERT ON funcionarios
    FOR EACH ROW
    WHEN ( new.funcionario_id IS NULL )
BEGIN
    :new.funcionario_id := funcionarios_funcionario_id_seq.nextval;
END;
/

-- Índices para otimizar as consultas
CREATE INDEX idx_cargo_descricao ON cargos (cargo_descricao);
CREATE INDEX idx_funcionario_cpf ON funcionarios (funcionario_cpf);
CREATE INDEX idx_df_cargos_cargo_id ON d_f (cargos_cargo_id);
CREATE INDEX idx_df_funcionarios_funcionario_id ON d_f (funcionarios_funcionario_id);



