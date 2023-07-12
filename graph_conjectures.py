from TxGraffiti.functions.make_inequalities import filter_known_conjectures, write_on_the_wall
import pandas as pd
from pyfiglet import figlet_format
from halo import Halo
import time
from datetime import datetime, timedelta

__version__ = '1.0.0'

# Print the title of the program.
print(figlet_format('TxGRAFFITI', font='slant'))
print('Version ' + __version__)
print('Copyright ' + u'\u00a9' + ' 2023 Randy Davila')
print()
print("TxGraffiti is a program that conjectures on data.")
print()
print()

# Read the csv file into a dataframe.
df = pd.read_csv(f"math_data/data/graphs.csv")

# Gather all of the numerical columns in the dataframe.
numerical_columns = [column for column in df.columns if df[column].dtype == "float64" or df[column].dtype == "int64"]

# Gather all of the boolean columns in the dataframe.
boolean_columns = [column for column in df.columns if df[column].dtype == "bool"]

# Print the numerical columns as the invariants.
print("The invariants are:")
for i, column in enumerate(numerical_columns):
    print(f"{i}: {column} \n")

# Ask the user to select a single invariant to conjecture on.
invariant_index = int(input("Enter the index of the invariant to conjecture on: "))
print()

# Ask the user if they would like to only consider a single property.
single_property_answer = input("Would you like to only consider a single property? (y/n): ")
print()

if single_property_answer == "y":
    # Print the Boolean columns as the invariants.
    print("The types of objects are:")
    for i, column in enumerate(boolean_columns):
        print(f"{i}: {column} \n")
    print()


    # Ask the user to select a single property to conjecture on.
    property_index = int(input("Enter the index of the property to conjecture on: "))
    print()

    # Ask if the user wants to apply Dalmatian to the data.
    dalmatian_answer = input("Apply Dalmatian to the data? (y/n): ")
    print()

    # write on the wall, i.e., conjecture on the data.
    if dalmatian_answer == "y":
        conjectures = write_on_the_wall(df, [numerical_columns[invariant_index]], numerical_columns, [boolean_columns[property_index]])
    else:
        conjectures = write_on_the_wall(df, [numerical_columns[invariant_index]], numerical_columns, [boolean_columns[property_index]], use_dalmation=False)

    # Remove the known conjectures from the list of conjectures.
    conjectures = filter_known_conjectures(conjectures, known_conjectures)

    # print the conjectures.
    print("The conjectures are:")
    for i, conjecture in enumerate(conjectures):
        print(f"Conjecture {i}: {conjecture} (touch = {conjecture.touch}) \n")
else:
    # Ask if the user wants to apply Dalmatian to the data.
    dalmatian_answer = input("Apply Dalmatian to the data? (y/n): ")
    print()

    # write on the wall, i.e., conjecture on the data.
    if dalmatian_answer == "y":
        conjectures = write_on_the_wall(df, [numerical_columns[invariant_index]], numerical_columns, boolean_columns)
    else:
        conjectures = write_on_the_wall(df, [numerical_columns[invariant_index]], numerical_columns, boolean_columns, use_dalmation=False)

    # print the conjectures.
    print("The conjectures are:")
    for i, conjecture in enumerate(conjectures):
        print(f"Conjecture {i}: {conjecture} (touch = {conjecture.touch}) \n")



