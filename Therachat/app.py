import telegram.ext
import pickle
import pandas as pd
import random
#data files
df=pd.read_csv("Updated_map.csv")
filename1 = "finalized_model.sav"
filename2= "classify_model.sav"
response_model = pickle.load(open(filename1, 'rb'))
classify_model=pickle.load(open(filename2,'rb'))
tf = pickle.load(open('scaler.pkl', 'rb'))
tf2 = pickle.load(open('scaler2.pkl', 'rb'))
suggestions=pd.read_csv('Mental Health Suggestions.csv',header=None)
suggestions[0]=suggestions[0].str.replace('\d+', '')
#Custom class for data manipulation
from Data_Manipulation import Manipulate
#Bot Functions
def start(update, context):
    update.message.reply_text("Hi I am Therachat! How are you feeling today??")
    
def help(update,context):
    update.message.reply_text("""
        Ask questions and get suitable answers
     """)

def generate_suggestion(update,context):
    update.message.reply_text("Here are some suggestions: ")
    flash=[]
    while len(flash)<5:
        n = random.randint(0,50)
        if n not in flash:
            flash.append(n)
    
    for x in suggestions[0][flash].to_list():
        update.message.reply_text(x)
    
def handle_message(update, context):
    test=[update.message.text]
    test=Manipulate(test).transform_data()
    testing2=tf2.transform(test)
    testing=tf.transform(test)
    classify=classify_model.predict(testing2)
    response=response_model.predict(testing)
    print(response[0])
    print(classify[0])
    if classify==0:
        update.message.reply_text("Overview: Positive")
        update.message.reply_text("Glad to hear!")
    else:
        update.message.reply_text("Overview: Negative")
        reply=df['answerText'][df['Answers_Code']==response[0]].to_list()[0]
        print(reply)
    # update.message.reply_text(f"You said {update.message.text}, use the commands using /")
        update.message.reply_text(f"{reply}")


Token = ####
#print(bot.get_me())
updater = telegram.ext.Updater(Token, use_context=True)
disp = updater.dispatcher

disp.add_handler(telegram.ext.CommandHandler('start',start))
disp.add_handler(telegram.ext.CommandHandler('help',help))
disp.add_handler(telegram.ext.CommandHandler('suggestions',generate_suggestion))
disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))
updater.start_polling()
updater.idle()