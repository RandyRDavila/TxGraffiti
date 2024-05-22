from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from TxGraffiti.functions.make_inequalities import make_all_upper_linear_conjectures, make_all_lower_linear_conjectures
from TxGraffiti.functions.make_inequalities import filter_conjectures, dalmatian, write_on_the_wall
from pyfiglet import figlet_format
import os

app = Flask(__name__)

# Default data paths
DATASETS = {
    "graphs": "math_data/data/graphs.csv",
    "integers": "math_data/data/integers.csv"
}
DEFAULT_DALMATIAN_ANSWER = "n"

@app.route('/')
def index():
    dataset = request.args.get('dataset', 'graphs')
    csv_path = DATASETS[dataset]
    df = pd.read_csv(csv_path)

    # Gather all of the numerical columns in the dataframe.
    numerical_columns = [column for column in df.columns if df[column].dtype == "float64" or df[column].dtype == "int64"]

    # Gather all of the boolean columns in the dataframe.
    boolean_columns = [column for column in df.columns if df[column].dtype == "bool"]

    return render_template('index.html',
                           numerical_columns=numerical_columns,
                           boolean_columns=boolean_columns,
                           default_dalmatian_answer=DEFAULT_DALMATIAN_ANSWER,
                           selected_dataset=dataset)

@app.route('/conjecture', methods=['POST'])
def conjecture():
    if request.method == 'POST':
        dataset = request.form.get('dataset')
        invariant_column = request.form.get('invariant_column')
        single_property = request.form.get('single_property')
        dalmatian_answer = request.form.get('dalmatian_answer', DEFAULT_DALMATIAN_ANSWER)

        # Read the selected CSV file into a dataframe.
        csv_path = DATASETS[dataset]
        df = pd.read_csv(csv_path)

        # Gather all of the numerical columns in the dataframe.
        numerical_columns = [column for column in df.columns if df[column].dtype == "float64" or df[column].dtype == "int64"]

        # Gather all of the boolean columns in the dataframe.
        boolean_columns = [column for column in df.columns if df[column].dtype == "bool"]

        if single_property and single_property != 'none':
            if dalmatian_answer == "y":
                conjectures = write_on_the_wall(df, [invariant_column], numerical_columns, [single_property])
            else:
                conjectures = write_on_the_wall(df, [invariant_column], numerical_columns, [single_property], use_dalmation=False)
        else:
            if dalmatian_answer == "y":
                conjectures = write_on_the_wall(df, [invariant_column], numerical_columns, boolean_columns)
            else:
                conjectures = write_on_the_wall(df, [invariant_column], numerical_columns, boolean_columns, use_dalmation=False)

        # Format the conjectures for display
        formatted_conjectures = [f"Conjecture {i}: {conjecture} (touch = {conjecture.touch})" for i, conjecture in enumerate(conjectures)]

        return render_template('results.html', conjectures=formatted_conjectures)

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server = request.environ.get('werkzeug.server.shutdown')
    if shutdown_server:
        shutdown_server()
    return 'Server shutting down...'

if __name__ == '__main__':
    app.run(debug=True, port=5002)
