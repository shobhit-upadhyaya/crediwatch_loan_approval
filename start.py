from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from db_module.db_helper import *
from loan_decision_model.model import *
import json

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


with open('config.json') as j:

    config = json.loads(j.read())
    print(config)


class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    
    @app.route("/",)
    def hello():    
        return render_template('hello.html')

    @app.route('/result',methods = ['POST', 'GET'])
    def result():

        if request.method == 'POST':

            result = request.form
            print(result.keys)
            #[('Monthly Income', ''), ('Loan tenure', ''), ('Loan Amount', ''), ('Interest Rate', ''), ('Current Debt', ''), ('CIN', 'U80900MH2020NPL335760')]
            CIN = result['CIN']
            print(CIN)
            curr_datapoint = filter_df_cin(CIN,config['pickel_dir']+"/"+config['db_name'],config['enhanced_info'])
            print(curr_datapoint)

            extra = {
            'loan_interest' : result['Interest Rate'],
            'loan_age' : result['Loan tenure'],
            'loan_amount' : result['Loan Amount'],
            'c_debts' : result['Loan tenure'],
            'monthly_income' : result['Monthly Income'],           
            }

            print(result)

            print("--------------------------------------------------------")
            loan_request = prediction(curr_datapoint, extra)
            print(loan_request)

            
            final_info_to_save = {k:v for k,v in result.items()}
            for k,v in loan_request.items():
                final_info_to_save[k] = v

            print(final_info_to_save)
            insert_result(config['pickel_dir']+"/"+config['db_name'], config['loan_request_results'], final_info_to_save)
            

            return render_template("result.html",result = result, extra = extra, loan_request = loan_request)





def init_db():
    df = pd.read_csv('./data_set.csv')
    save_data(df,config['pickel_dir']+"/"+config['db_name'], config['base_info'])
    create_table(config['pickel_dir']+"/"+config['db_name'], config['loan_request_results'])
    # tmp_df = load_data('loan_tmp_database.db')
    # print(tmp_df.shape)
    # print(tmp_df.head())
    # saved_results = load_data(config['pickel_dir']+"/"+config['db_name'], config['loan_request_results'])
    # print(saved_results.shape)

if __name__ == "__main__":

    init_db()
    build_model(False)
    app.run()