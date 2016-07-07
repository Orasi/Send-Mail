from WriteEmail import WriteEmail


page_method = WriteEmail
myfile = open(page_method.results_file_name, 'r')
results = myfile.read()
page_method.send_mail(page_method, results)
myfile.close()