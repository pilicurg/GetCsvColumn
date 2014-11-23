'''Test GetCsvColumn'''

from GetCsvColumn import CsvFile,EXCLUDE

csvfilename = 'demo.csv'
csvfile = CsvFile(csvfilename)

# example 1: get a column by its header
print 'example 1:', csvfile.get_column('Name')

# example 2: get a column filtered by another column
print 'example 2:', csvfile.get_column('Name', Gender='M')

# example 3: get a column filtered by other columns
print 'example 3:', csvfile.get_column('Name', Gender='M', Age=9)

# example 4: exclusive filters
print 'example 4:', csvfile.get_column('Name', Gender=EXCLUDE('M'))

# example 5: get a column filtered by other column with multi-criteria
print 'example 5:', csvfile.get_column('Name', Age=[8, 9, 13])

# example 6: get a column exclusively filtered by other column with multi-criteria
print 'example 6:', csvfile.get_column('Name', Age=EXCLUDE([8, 9, 13]))

# example 7: get multiple columns for unpacking
no, name = csvfile.get_column('No', 'Name')
print 'example 7:', no, name