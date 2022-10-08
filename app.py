from urllib import response
from urllib.parse import urlparse
from flask import Flask, render_template, request,jsonify,url_for, make_response, redirect
import numpy as np
import pandas as pd
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
from io import BytesIO
import re
import psycopg2
import shap
import os

img_size=100

app = Flask(__name__)

def get_db_connection():
	db_uri = os.environ.get('DB_URI', None)
	result = urlparse(db_uri)
	username = result.username
	password = result.password
	database = result.path[1:]
	hostname = result.hostname
	port = result.port
	# conn = psycopg2.connect(host='localhost', database='thesis_db', user='nijelp', password='master')
	conn = psycopg2.connect(
		database = database,
		user = username,
		password = password,
		host = hostname,
		port = port
	)
	return conn




@app.route("/")
def index():
	print('index')
	conn = get_db_connection()
	cur = conn.cursor()
	cur.execute('SELECT * FROM crm_input;')
	crm_input = cur.fetchall()
	dict={'Customer Interested':'interested','Customer will buy for better rate':'rate','Customer Rejected': 'rejected','':'none','Customer Not Reachable': 'unreachable'}
	crm_input1=[x + (dict[x[24]],) for x in crm_input]
	cur.close()
	conn.close()
	return render_template('index.html', crm_input=crm_input1)
	
	# print(os.getcwd())
	# datacsv=pd.read_csv("static/Check.csv")
	
	# return render_template(("index.html"),tables=[datacsv.to_html(classes='data')], titles=datacsv.columns.values)



@app.route("/details", methods=["POST"])
def details():
	print('details')
	cif = request.get_json(force=True, silent=True, cache=False)
	print(cif)
	fit_model=pd.read_pickle('model/fit_model.pkl')
	conn = get_db_connection()
	stmt = "select * from crm_shap;"
	stmt2="select * from crm_input;"
	data_df = pd.io.sql.read_sql(stmt, conn)
	data_crm = pd.io.sql.read_sql(stmt2, conn)
	indexpos=data_df.index[data_df['Customer']==int(cif)].tolist()
	# intcif=int(cif)
	# indexpos=data_df['Customer'].loc[lambda x:x==intcif].index

	explainer = shap.TreeExplainer(fit_model.best_estimator_)
	plt.figure()
	data_df=data_df.drop("Customer", axis=1)
	shap_values = explainer.shap_values(data_df)
	shap.force_plot(explainer.expected_value, shap_values[indexpos[0]], data_df.iloc[indexpos[0]], text_rotation=15, matplotlib=True, show=False) 
	buf = BytesIO()
	plt.tight_layout()
	plt.title("SHAP Force Plot")
	plt.savefig(buf,
            format = "png",
            dpi = 160,
			transparent=True,
			bbox_inches="tight",
			)
	plot_url = base64.b64encode(buf.getbuffer()).decode("ascii")
	return plot_url
	# message = request.get_json(force=True)
	# encoded = message['image']
	# decoded = base64.b64decode(encoded)
	# dataBytesIO=io.BytesIO(decoded)
	# dataBytesIO.seek(0)
	# img = Image.open(dataBytesIO)
	# img=np.array(img)
	# res2 = skimage.segmentation.felzenszwalb(img, scale=1000)
	
	# plt.imshow(res2)
	# plt.title("Graph based Image segmentation")
	# plt.xticks([]),plt.yticks([])
	
	    
	# img1 = io.BytesIO()
	# plt.tight_layout()
	# plt.savefig(img1, format='png')
	# #plt.savefig('/static/edgeplot.png', format='png')
	# plt.close()
	# img1.seek(0)
	# #plot_data = urllib.parse.quote(base64.b64encode(img.read()).decode())
	# plot_url = base64.b64encode(img1.getvalue()).decode('utf8')
	
	# #response = {'plot_url': plot_url}

	# return plot_url


@app.route("/lead", methods=["POST"])
def lead():
	print('lead')
	message = request.get_json(force=True, silent=True, cache=False)
	print(message)

	sql = """ UPDATE "crm_input"
                SET "Status" = %s,
				"Description" = %s
                WHERE "Customer" = %s"""
	conn = None
	updated_rows = 0
	
	try:
        # connect to the PostgreSQL database
		conn = get_db_connection()
        # create a new cursor
		cur = conn.cursor()
        # execute the UPDATE  statement
		cur.execute(sql, (message['status'], message['details'],int(message['customer'])))
        # get the number of updated rows
		updated_rows = cur.rowcount
        # Commit the changes to the database
		conn.commit()
        # Close communication with the PostgreSQL database
		cur.close()

	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()
	data=request.get_json(force=True, silent=True, cache=False)
	
	return 'Leads_Updated'



if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)

#<img src="" id="img" crossorigin="anonymous" width="400" alt="Image preview...">
