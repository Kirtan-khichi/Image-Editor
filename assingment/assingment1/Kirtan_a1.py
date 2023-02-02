"""
Module for currency exchange
This module provides several string parsing functions to
implement a simple currency exchange routine using an online currency service.
The primary function in this module is exchange.
Author: Kirtan Khichi.
Date: 24 november,2022.
"""
import requests #Here we are importing request module.

def before_space(s):
	'''
	Returns a copy of s up to, but not including, the first space.

	In this function we are doing a string slicing in which we are doing string slice and get substring before space.
	
	Parameter s: the string to slice.
	Precondition: s is a string with at least one space.
	
	Doctests:-
	>>> before_space('2.45 Euro')   #When one space between two words.
	'2.45'
	>>> before_space('2.456  USD')  #When two spaces between words.
	'2.456'
	>>> before_space(' 2.456 USD')  #When start with space and also contain space between words.
	'2.456'
	'''
	s=s.strip()
	string_space_index=s.find(' ')    #Just Giving the index of first space.
	word=s[:string_space_index]       #Here slicing done before space
	return word


def after_space(s):
	'''
	Returns a copy of s after the first space.

	In this function we are doing string slicing in which we are giving output after first space substring.
	#Test cases are returning a substring after the first space. 

	Parameter s: the string to slice.
	Precondition: s is a string with at least one space.
	Doctest:-
	>>> after_space('2.45 Euro')   #When one space in between two words.
	'Euro'
	>>> after_space('2.456  USD')  #When two spaces between two words.
	' USD'
	>>> after_space(' 2.456 USD')  #When string also starts from space and also have space between two words.
	'USD'
	'''
	s=s.strip()
	string_space_index=s.find(' ')      #Just giving the first space of s
	word=s[string_space_index+1:]
	return word


def first_inside_quotes(s):
	'''
	Returns the first substring of s between two (double) quotes. 

	A quote character is one that is inside a string, not one that delimits it.
	We typically use single quotes (') to delimit a string if we want to use a double quote character (") inside of it.
	first_inside_quotes('A "B C" D') returns 'B C'
	first_inside_quotes('A "B C" D "E F" G') returns 'B C'


	because it only picks the first such substring
	
	Parameter s: a string to search.
	Precondition: s is a string containing at least two double quotes.
	
	Doctests:-
	>>> first_inside_quotes('A "B C" D')    #When contain only one double quote substring.
	'B C'
	>>> first_inside_quotes(' A "B C" D')   #When string contain one double quote substring and also start with space.
	'B C'
	>>> first_inside_quotes('A "B C" D "E F" G')          #When string contains two double quote substrings. 
	'B C'
	>>> first_inside_quotes(' A "B C" D "E F" G "H I"')   #when string contains three double quote substring.
	'B C'
	'''
	s=s.strip()
	double_quote_index=s.find('"')    #gives the index number of first double quote.
	double_quote_index_end=s.find('"',double_quote_index+1)  #gives the second double quote index number. 
	result=s[double_quote_index+1:double_quote_index_end] 
	return result


def get_lhs(json):
	'''
	Returns the lhs value in the response to a currency query.

	Given a JSON response to a currency query, this returns the string inside double quotes (") immediately 
	following the keyword.
	"lhs". For example, if the JSON is'{ "lhs" : "1 Bitcoin", "rhs" : "19995.85429186 Euros", "err" : "" }'
	then this function returns '1 Bitcoin' (not '"1 Bitcoin"').
	This function returns the empty string if the JSON response contains an error message.
	Examples:('{ "lhs" : "1 Bitcoin", "rhs" : "19995.85429186 Euros", "err" : "" }') returns '1 Bitcoin'
	
	Parameter json: a json string to parse.
	Precondition: json is the response to a currency query.
	Doctest:-
	>>> get_lhs('{ "lhs" : "1 Bitcoin", "rhs" : "19995.85429186 Euros", "err" : "" }') #When currency is correct.
	'1 Bitcoin'
	>>> get_lhs('{ "lhs" : "", "rhs" : "", "err" : "Exchange currency code is invalid." }') #when error is contains.
	''
	'''
	json_colon=json.index(':')       #gives the index number of colon.
	json_colon_end=json.index(',')   #gives the index number of comma.
	return json[json_colon+3:json_colon_end-1]


def get_rhs(json):
	'''
	Returns the rhs value in the response to a currency query.

	Given a JSON response to a currency query, this returns the string inside double quotes (") immediately 
	following the keyword.
	"rhs". For example, if the JSON is '{ "lhs" : "1 Bitcoin", "rhs" : "19995.85429186 Euros", "err" : "" }'
	then this function returns '19995.85429186 Euros' (not '"38781.518240835 Euros"').
	This function returns the empty string if the JSON response contains an error message.
	Example:('{ "lhs" : "1 Bitcoin", "rhs" : "19995.85429186 Euros", "err" : "" }') returns '19995.85429186 Euros'

	Parameter json: a json string to parse.
	Precondition: json is the response to a currency query.

	Doctest:- 
	>>> get_rhs('{ "lhs" : "1 Bitcoin", "rhs" : "19995.85429186 Euros", "err" : "" }')       #When currency is correct.
	'19995.85429186 Euros'
	>>> get_rhs('{ "lhs" : "", "rhs" : "", "err" : "Exchange currency code is invalid." }')  #when error is contain.
	''
	'''

	json_colon=json.index(':')       #gives index number of first colon.
	json_comma=json.index(',')       #gives index number of first colon.
	json_second_colon=json.index(':',json_colon+1)    #gives the index number of second colon.
	json_second_comma=json.index(',',json_comma+1 )   #gives the index number of second comma.
	return json[json_second_colon+3:json_second_comma-1]


def has_error(json):
	'''
	Returns True if the query has an error; False otherwise.

	Given a JSON response to a currency query, this returns True if there is an error message. 
	For example, if the JSON is '{ "lhs" : "", "rhs" : "", "err" : "Currency amount is invalid." }'
	then the query is not valid, so this function returns True (It does NOT return the message 'Currency amount is 
	invalid.').

	Parameter json: a json string to parse
	Precondition: json is the response to a currency query
	Doctest:-
	>>> has_error('{ "lhs":"2 Namibian Dollars", "rhs":"2 Lesotho Maloti","err":""}')           #When have no error.
	False
	>>> has_error('{ "lhs" : "", "rhs" : "", "err" : "Exchange currency code is invalid." }')   #When contains error.
	True
	'''
	return 'invalid' in json


def query_website(old,new,amt):
	'''
	Returns a JSON string that is a response to a currency query.

	A currency query converts amt money in currency old to the currency new. The response should be a string of the 
	form '{ "lhs":"<old-amt>", "rhs":"<new-amt>", "err":"" }'where the values old-amount and new-amount contain 
	the value and name for the old and new currencies. If the query is invalid, both old-amount and new-amount 
	will be empty, while "err" will have an error message.
	
	Parameter old: the currency on hand.
	Precondition: old is a string with no spaces or non-letters.
	Parameter new: the currency to convert to.
	Precondition: new is a string with no spaces or non-letters.
	Parameter amt: amount of currency to convert.
	Precondition: amt is a float.

	Doctests:-
	>>> query_website('USD','INR','1.45')     #This Returns string from web service when input are correct.
	'{ "lhs" : "1.45 United States Dollars", "rhs" : "115.69261885 Indian Rupees", "err" : "" }'
	>>> query_website('USD','Eurokjh',1.45)   #This Returns string from web service when input are wrong.
	'{ "lhs" : "", "rhs" : "", "err" : "Exchange currency code is invalid." }'
	
	'''

	target_url=f'http://cs1110.cs.cornell.edu/2022fa/a1/?old={old}&new={new}&amt={amt}'
	json = (requests.get(target_url)).text
	return json


def is_currency(code):
	'''
	Returns: True if code is a valid (3 letter code for a) currency.It returns False otherwise.
	
	In this function we are checking that the currency code is correct or not.

	Parameter code: the currency code to verify
	Precondition: code is a string with no spaces or non-letters.
	Doctest:-
	>>> is_currency('USD')    #When currency code is correct.
	True
	>>> is_currency('uqd')    #When currency code is incorrect.
	False
	>>> is_currency('usd')    #When currency code is lower case.
	True
	>>> is_currency('UsD')    #When mix upper & lower case.
	True
	'''

	amt=0  
	return not(has_error(query_website(code.upper(),code.upper(),amt)))


def exchange(old, new, amt):
	'''
	Returns the amount of currency received in the given exchange.

	In this exchange, the user is changing amt money in currency old to the currency new.
	The value returned represents the amount in currency new.The value returned has type float.

	Parameter old: the currency on hand.
	Precondition: old is a string with no spaces or non-letters.
	Parameter new: the currency to convert to.
	Precondition: new is a string with no spaces or non-letters.
	Parameter amt: amount of currency to convert.
	Precondition: amt is a float.
	'''

	return before_space(get_rhs(query_website(old,new,amt)))