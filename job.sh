#!/bin/bash

cd /home/rhenry/openfoodfacts/Cr-ez-une-plateforme-pour-amateurs-de-Nutella/
pipenv install
export ENV="PRODUCTION"
export SECRET_KEY="(5(^\!fhzo4qb_a\!-r_=+ig\!i8j2c^+3(ntiri\!jl5#e@qg49"
export DB_PASSWORD="Thomas040417!"
pipenv run python3 manage.py update_data

