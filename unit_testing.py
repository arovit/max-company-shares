#! /usr/bin/python

# -*- encoding: ASCII -*-

# Author - Arovit Narula
# Version - 1.3

# unit tests for Max share value problem

import unittest
import random
import max_shares
from cStringIO import StringIO
import os
import io

# Best way to test is have 'Randomize' testcases
class RandomCSVInput(unittest.TestCase):   
    """ Base class to generate Randomized csv input """
    def setUp(self):
        self.years = range(1990, 2013)      # Default years - 1990-2013, Derived classes can change it
        self.months = ['Jan', 'Feb', 'Mar', 'April', 'May', 'June', 'July', 'Aug', 'Sep',\
                      'Oct', 'Nov', 'Dec']  # Jan-Dec 
        self.share_values = range(10, 100)  # Default 10-100, Derived classes can change it
        self.no_companies = 5               # Default 5 companies, Derived classes can change it 
        self.no_entries = (2013 - 1990)*12  # Default 5 entries, Derived classes can change it
        self.csv_rand_input = ['Year', 'Month']
        self.check_dict = {}
        # Construct the header of CSV file     
        for i in range(self.no_companies):
            self.csv_rand_input.append('Comp%s'%str(i+1))
        self.csv_rand_input = ','.join(self.csv_rand_input) + '\n'

        # Construct the body of CSV file     
        for i in range(self.no_entries):
            year = random.choice(self.years)   # Random year
            month = random.choice(self.months) # Random month
            svalues = [year, month]           
            				# Random  share values for each company
            for j in range(self.no_companies):
                share_val = random.choice(self.share_values)
                svalues.append(share_val)
                self.check_dict.setdefault('Comp%s'%(j+1), {}) 
                self.check_dict['Comp%s'%(j+1)].setdefault(share_val, [])
                self.check_dict['Comp%s'%(j+1)][share_val].append(str(year)+':'+str(month))
            entry = ','.join(map(str, svalues)) + '\n'
            self.csv_rand_input = self.csv_rand_input + entry



class BadCSVInput(RandomCSVInput):   # Uses Random csv input from base class
    """ Class to test for bad input """
    # Bad input - no header

    def test_sharevalues(self):
        """ When CSV input has wrong (string) share values """
        self.csv_rand_input = self.csv_rand_input.split('\n') 
        self.csv_rand_input_second_line = ','.join(self.csv_rand_input[1].split(',')[:-1] + ["hello world"])
        self.csv_rand_input[1] = self.csv_rand_input_second_line 
        self.csv_rand_input = '\n'.join(self.csv_rand_input)
        ret_val = max_shares.main(self.csv_rand_input)
        self.assertTrue('Critical' in ret_val)



class ValidateOutput(RandomCSVInput):  # Uses Random csv input from base class
    """ Class to validate for output """  
    # Validate results
    def test_results(self):
        ret_val = max_shares.main(self.csv_rand_input)
        self.assertTrue(not 'Critical' in ret_val)
        for company_info in ret_val.split('\n'):
           if not company_info:
               continue
           companyname, year, month = company_info.split(':') 
           self.assertTrue(str(year)+':'+str(month) in self.check_dict[companyname][max(self.check_dict[companyname].keys())])
        
    def test_all_companies(self):
        ret_val = max_shares.main(self.csv_rand_input)
        self.assertTrue(not 'Critical' in ret_val)
        for key in self.check_dict:
            self.assertTrue(key in ret_val)


            

if __name__ == "__main__":
   # Put this inside a for loop for hundreds of randomized testcases 
    unittest.main()
