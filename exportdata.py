
import answer_bot

if __name__ == "__main__":
    mc = answer_bot.memcached_login()
    data = mc.get("stale_scores")
    f = open("data.py", "w")
    f.write("import datetime\n")
    f.write(repr(data))
    f.write("\n")
    f.close()

    print("Data saved to 'data.py'.  This file still needs to be processed")
    print("(reorganized/processed/titles downloaded/etc).  Copy it to a machine")
    print("that has memory (not heroku...), make sure it's named 'data.py', and")
    print("then run process.py which should take care of everything and dump out")
    print("a postdata.py file for you.")

