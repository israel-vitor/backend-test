import json

a_file = open("./config/development.json", "r")

json_object = json.load(a_file)

a_file.close()


json_object[4]["value"] = "development_db_1"


a_file = open("./config/development.json", "w")

json.dump(json_object, a_file)

a_file.close()

