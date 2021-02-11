import csv

def exporter(results,keyword):
  # opening the csv file in 'w+' mode 
  file = open(f'search_for_{keyword}.csv', 'w', newline ='', encoding='utf-8') 
  # writing the data into the file 
  with file:     
      write = csv.writer(file) 
      write.writerows(results)
  return 'OK'