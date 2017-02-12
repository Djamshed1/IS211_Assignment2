#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Week 2 assignment 1"""

import urllib2
import csv
import datetime
import logging
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', help="Enter a URL linking to a .csv file.")
args = parser.parse_args()

logging.basicConfig(filename='errors.log', level=logging.ERROR)
logger = logging.getLogger('assignment2')

def downloadData(url):
    """It downloads the contents located at the url and return it to the caller.

    Args:
        url(str): A string for a URL.
    Returns:
        datafile(various): A variable linked to an applicable datafile.
    Example:
        >>> downloadData('https://s3.amazonaws.com/cuny-is211-spring2015
        /birthdays100.csv')
        <addinfourl at 3043697356L whose fp = <socket._fileobject object at
        0xb5682eec>>
    """
    csvData = urllib2.urlopen(url)
    return csvData

def processData(csvData):
    """It takes the contents of the file as the first parameter, processes
    the file line by line, and returns a dictionary that maps a person’s
    ID to a tuple of the form (name, birthday).
    
    Args:
        csvdata(file): A .csv file with data in it.
    Returns:
        newdict(dict): A dictionary containing keys comprised of the userid in
        the supplied csv file.
    Example:
        >>> load = downloadData('https://s3.amazonaws.com/cuny-is211-spring2015
        /birthdays100.csv')
        >>> processData(load)
        ('24': ('Stewart Bond', datetime.datetime(2008, 2, 15, 0, 0)),
        '25': ('Colin Turner', datetime.datetime(1994, 6, 6, 0, 0)),
        '26': ('Pippa Glover', datetime.datetime(2001, 8, 15, 0, 0)),
        '20': ('Jack Poole', datetime.datetime(1997, 8, 3, 0, 0))
    """
    readfile = csv.DictReader(csvData)
    newdict = {}

    for x, line in enumerate(readfile):
        try:
            born = datetime.datetime.strptime(line['birthday'], '%d/%m/%Y')
            newdict[line['id']] = (line['name'], born)
        except:
            logging.error('Error processing line #{} for ID# {}'.format(
                x, line['id']))
    return newdict

def displayPerson(id, personData):
    """Looks up the id number in a supplied dictionary, and returns the name and
       date of birth associated with the id number.
       Args:
           id(int, str): The number to be checked against the dictionary and
           return the associated person.
           persondata(dict): A dictionary containing a tuple of the username
           and date of birth.
        Returns:
            (str): A string displaying either the person and date of birth which
            which corresponds with the input id number, or a string indicating
            the id is not associated with anyone in the supplied dictionary.
        Examples:
            >>> displayperson(11, persondata)
            Person #11 is Angela Watson with a birthday of 1994-04-15
            >>> displayperson(1000, persondata)
            No user found with that ID.
        """
    y = str(id)
    if y in personData.keys():
        print 'Person #{} is {} with a birthday of {}'.format(id,
                personData[y][0], datetime.datetime.strftime
                (personData[y][1], '%Y-%m-%d'))
    else:
        print 'No user found with that ID.'

def main():
    """Combines downloadData, processData, and displayPerson into one
    program to be run from the command line.
    """
    if not args.url:
        raise SystemExit
    try:
        csvData = downloadData(args.url)
    except urllib2.urlError:
        print 'Please enter a valid URL.'
        raise
    else:
        personData = processData(csvData)
        chooseid = raw_input('Please enter an ID# for lookup:')
        print chooseid
        chooseid = int(chooseid)
        if chooseid <= 0:
            print 'Number equal to or less than zero entered. Exiting program.'
            raise SystemExit
        else:
            displayPerson(chooseid, personData)
            main()

if __name__ == '__main__':
    main()
