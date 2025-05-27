import os
from dotenv import load_dotenv
import requests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime, timezone
from sqlalchemy import create_engine, Column, Integer, Float, DateTime, MetaData, Table
from sqlalchemy.orm import sessionmaker



def main ():
    URL = "https://api.porssisahko.net/v1/latest-prices.json"

    try:
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()
        prices = data['prices']

        price_list = []
        timestamps = []
        for entry in prices:
            price_list.append(entry['price'])
            timestamps.append(datetime.fromisoformat(entry["startDate"].replace("Z", "+00:00")))

        # Lets draw a picture using e-price data
        plt.plot(timestamps,price_list,label="Hinta: snt/kWh")
        plt.legend()
        plt.title("Pörssisähkön hinta")
        plt.ylabel("Hinta snt/kWh")
        plt.xlabel("Aika [h]")
        plt.xticks(rotation=35)
        plt.grid()
        #plt.show()
        plt.savefig("EpricePlot.png")
        
        # After saving the plot, let's place the timeseries to postgres database
        # Load environment variables for DB connection
        load_dotenv()
        db_url = os.getenv("DATABASE_URL")  # Example: "postgresql://user:password@localhost/dbname"

        # Create SQLAlchemy engine for database connection
        engine = create_engine(db_url)
        # Create SQLAlchemy metadata for schema definition
        metadata = MetaData()
        
        

        # Define table if not exists
        prices_table = Table(
            'electricity_prices', metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('timestamp', DateTime(timezone=True), nullable=False),
            Column('price', Float, nullable=False),
        )

        metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        # Insert timeseries data
        insert_data = [
            {'timestamp': ts, 'price': price}
            for ts, price in zip(timestamps, price_list)
        ]
        with engine.begin() as conn:
            conn.execute(prices_table.insert(), insert_data)

        session.close()
        
        
    except requests.RequestException as e:
        print(f"Exception: {e}")
if __name__ == "__main__":
    main()
    
    