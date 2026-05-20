def create_tables(self):
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute('''
                        CREATE TABLE IF NOT EXISTS warehouse (
                            id SERIAL PRIMARY KEY, 
                            name VARCHAR(255) NOT NULL, 
                            location VARCHAR(255) NOT NULL,
                            capacity FLOAT NOT NULL
                        )
                                
                        CREATE TABLE IF NOT EXISTS shipment (
                            id SERIAL PRIMARY KEY, 
                            tracking_number VARCHAR(255) UNIQUE NOT NULL,
                            weight FLOAT NOT NULL,  
                            status VARCHAR(50) NOT NULL DEFAULT 'на складе',
                            warehouse_id INTEGER NOT NULL,
                            FOREIGN KEY (warehouse_id) REFERENCES warehouse(id) ON DELETE CASCADE
                        )  

                        CREATE TABLE IF NOT EXISTS driver (         
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(255) NOT NULL, 
                            license_number VARCHAR(255) UNIQUE NOT NULL,
                            constraint unique_license UNIQUE (license_number)
                        )

                        CREATE TABLE IF NOT EXISTS shipment_driver (
                            id SERIAL PRIMARY KEY,
                            shipment_id INTEGER NOT NULL,   
                            driver_id INTEGER NOT NULL,
                            delivery_date DATE NOT NULL,
                            FOREIGN KEY (shipment_id) REFERENCES shipment(id) ON DELETE CASCADE,
                            FOREIGN KEY (driver_id) REFERENCES driver(id) ON DELETE CASCADE,
                            UNIQUE (shipment_id, driver_id, delivery_date
                        )        
                    ''')
                except Exception as e:
                        conn.rollback()
                        raise e