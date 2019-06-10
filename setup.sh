pip freeze > requirements.txt
export DATABASE_URL=postgres://$(whoami)@localhost:5432/card_data