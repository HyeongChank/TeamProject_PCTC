CREATE TABLE YCOperation (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    con_number VARCHAR(255),
    op_code VARCHAR(255),
    ship_code VARCHAR(255),
    con_year INTEGER,
    voyage VARCHAR(255),
    block VARCHAR(255),
    bay_x INTEGER,
    row_y INTEGER,
    tier_z INTEGER,
    block2 VARCHAR(255),
    bay_x2 INTEGER,
    row_y2 INTEGER,
    tier_z2 INTEGER,
    yard_truck_number VARCHAR(255),
    full_or_empty CHAR(1),
    container_size_code VARCHAR(255),
    equipment_number VARCHAR(255),
    op_creation_time TIMESTAMP,
    op_completion_time TIMESTAMP,
    op_time DOUBLE
);

CREATE TABLE ScheduledContainer (
                                    id BIGINT PRIMARY KEY,
                                    conNumber VARCHAR(255),
                                    containerSizeCode VARCHAR(255),
                                    containerTypeCode VARCHAR(255),
                                    shipCode VARCHAR(255),
                                    yearCol INTEGER,
                                    voyage VARCHAR(255),
                                    weight DOUBLE,
                                    destinationPort VARCHAR(255),
                                    shippingPort VARCHAR(255),
                                    time TIMESTAMP
);

CREATE TABLE YardStatus (
                            id BIGINT PRIMARY KEY,
                            conNumber VARCHAR(255),
                            shipCode VARCHAR(255),
                            Conyear INTEGER,
                            voyage VARCHAR(255),
                            operatorCode VARCHAR(255),
                            fullOrEmpty CHAR(1),
                            containerSizeCode VARCHAR(255),
                            containerTypeCode VARCHAR(255),
                            weightInTons DOUBLE,
                            destinationCode VARCHAR(255),
                            block VARCHAR(255),
                            bay_x INTEGER,
                            row_y INTEGER,
                            tier_z INTEGER,
                            isExport BOOLEAN
);
