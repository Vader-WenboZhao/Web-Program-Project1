# Project 1 Wenbo ZHAO 201792259

Web Programming with Python and HTML


All Files:

	API_test.py
	application.py
	books.csv
	import.py
	README.md
	requirements.txt
	__pycache__
		application.cpython-37.pyc
	flask_session
		2029240f6d1128be89ddc32729463129
	templates
		detail.html
		error.html
		index.html
		layout.html
		login.html
		register.html
		result.html
		search.html
		success.html
		userpage.html



All tables:

	1.books:
		                    Table "public.books"
 		 Column |       Type        | Collation | Nullable | Default 
		--------+-------------------+-----------+----------+---------
 		 isbn   | character varying |           | not null | 
 		 title  | character varying |           | not null | 
 		 author | character varying |           | not null | 
 		 year   | integer  
		Indexes:
    			"books_pkey" PRIMARY KEY, btree (isbn) 
	
	2.reviews:
		                                 Table "public.reviews"
		 Column |       Type        | Collation | Nullable |               Default               
		--------+-------------------+-----------+----------+-------------------------------------
 		 id     | integer           |           | not null | nextval('reviews_id_seq'::regclass)
 		 isbn   | character varying |           | not null | 
 		 star   | integer           |           |          | 
 		 review | character varying |           |          | 
		Indexes:
    			"reviews_pkey" PRIMARY KEY, btree (id)
	
	3.users:
		                     Table "public.users"
		  Column  |       Type        | Collation | Nullable | Default 
		----------+-------------------+-----------+----------+---------
		 username | character varying |           | not null | 
		 password | character varying |           | not null | 
		Indexes:
  			  "users_pkey" PRIMARY KEY, btree (username)
