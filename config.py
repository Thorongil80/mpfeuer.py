import configparser
Config = configparser.ConfigParser()
Config.read("config.ini")
print(Config.sections())



def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

	
db_path = ConfigSectionMap("database")['db_path'].strip('"')
db_port = ConfigSectionMap("database")['db_port'].strip('"')
db_user = ConfigSectionMap("database")['db_user'].strip('"')
db_pass = ConfigSectionMap("database")['db_pass'].strip('"')
db_host = ConfigSectionMap("database")['db_host'].strip('"')
db_char = ConfigSectionMap("database")['db_char'].strip('"')

#print("db_path:" + db_path)
#print("db_port:" + db_port)
#print("db_host:" + db_host)
#print("db_char:" + db_char)
#print("db_user:" + db_user)
#print("db_pass:" + db_pass)


mail_server = ConfigSectionMap("mail")['server'].strip('"')
mail_port = ConfigSectionMap("mail")['port'].strip('"')
mail_user = ConfigSectionMap("mail")['user'].strip('"')
mail_from = ConfigSectionMap("mail")['from'].strip('"')
mail_pass = ConfigSectionMap("mail")['pass'].strip('"')