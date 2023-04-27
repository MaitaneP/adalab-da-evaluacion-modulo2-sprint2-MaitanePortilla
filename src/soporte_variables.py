# lista de paises a estudiar
paises = ['Argentina', 'Canada', 'United States']

# creación tablas en BBDD MySQL WorkBench
sustituir_provincias = {'NV': 'Nevada', 
                    'TX': 'Texas', 
                    'IN': 'Indianapolis',
                    'CA': 'California',
                    'VA': 'Virginia',
                    'NY': 'New York',
                    'MI': 'Michigan',
                    'GA': 'Georgia',
                    'ND': 'North Dakota',
                    'New York, NY' : 'New York',
                    'Ciudad Autónoma de Buenos Aires': 'Buenos Aires'}

tabla_paises = '''CREATE TABLE IF NOT EXISTS `bd_universidades`.`paises` (
                    `idestado` INT NOT NULL AUTO_INCREMENT,
                    `nombre_pais` VARCHAR(45) NOT NULL,
                    `nombre_provincia` VARCHAR(45) NOT NULL,
                    `latitud` DECIMAL(15,10),
                    `longitud` DECIMAL(15,10),
                    PRIMARY KEY (`idestado`))
                    ENGINE = InnoDB;
                '''

tabla_universidades = ''' CREATE TABLE IF NOT EXISTS `bd_universidades`.`universidades` (
                        `iduniversidades` INT NOT NULL AUTO_INCREMENT,
                        `nombre_universidad` VARCHAR(100) NOT NULL,
                        `pagina_web` VARCHAR(100) NOT NULL,
                        `paises_idestado` INT NOT NULL,
                        PRIMARY KEY (`iduniversidades`),
                        INDEX `fk_universidades_paises_idx` (`paises_idestado` ASC) VISIBLE,
                        CONSTRAINT `fk_universidades_paises`
                            FOREIGN KEY (`paises_idestado`)
                            REFERENCES `bd_universidades`.`paises` (`idestado`)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE)
                        ENGINE = InnoDB;
                    '''

# datos de acceso para conexión con la BBDD de MySQL WorkBench
acceso_sql = {'user': 'root', 
                'password': 'AlumnaAdalab',
                'host': '127.0.0.1',
                'raise_on_warnings': True
                }

acceso_bbdd = {'user': 'root', 
                'password': 'AlumnaAdalab',
                'host': '127.0.0.1',
                'database': 'bd_universidades',
                'raise_on_warnings': True
                }
