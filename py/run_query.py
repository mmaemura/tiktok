from query_functions import *

##to run
##in C: ... \tiktok
##virtualenv env
##cd env\Scripts
##activate
##cd ..
##cd ..
##python run_query.py

verifyFp = "" #found by following Youtube tutorial from API devoloper: https://www.youtube.com/watch?v=zwLmLfVI-VQ&t=2s
get_tiktok_data(verifyFp = verifyFp, k = 100, get_transcription = True, to_db = True, db_file_name = "tiktok.db", to_csv = False)