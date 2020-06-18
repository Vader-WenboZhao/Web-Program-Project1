import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE_URL="postgresql://postgres:zhaowenbo2305@localhost:5432/Books"

engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("/Users/zhaowenbo/2nd_grade_3/Web高级程序设计/project1-Vader-WenboZhao-master/Test/books.csv")
    print(f)
    reader = csv.reader(f)
    # The type of data in first 3 columns in books are all VARCHAR, the year column is in type of INTEGER
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                    {"isbn": isbn, "title": title, "author": author, "year": year})
        print(f"Added book with isbn of {isbn} and title of {title}. ")
    db.commit()

if __name__ == "__main__":
    main()
